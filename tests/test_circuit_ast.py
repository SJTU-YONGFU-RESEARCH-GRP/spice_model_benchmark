import json
import tempfile
import unittest
from pathlib import Path

from spice_model_benchmark.circuit_ast import (
    Dialect,
    emit_circuit,
    parse_circuit,
    translate_circuit_set,
)
from spice_model_benchmark.cli import (
    _archive_executed_netlists,
    _rewrite_report_netlist_paths,
)


SPICE_SOURCES = {
    "dc": """.title DC
V1 in 0 DC 0
R1 in out 1k
R2 out 0 2k
.DC V1 0 1 0.1
.END
""",
    "ac": """.title AC
V1 in 0 DC 0 AC 1
R1 in out 1k
C1 out 0 1p
.AC DEC 10 1k 1meg
.END
""",
    "transient": """.title transient
V1 in 0 PULSE(0 1 0 1n 1n 5n 10n)
R1 in out 1k
C1 out 0 1p
.TRAN 0.1n 20n
.END
""",
    "noise": """.title noise
V1 in 0 DC 0 AC 1
R1 in out 1k
R2 out 0 2k
.NOISE V(out) V1 DEC 10 1 1meg
.END
""",
}

HSPICE_SOURCES = {
    mode: text.replace(".title", "* HSPICE").replace(
        "\n", "\n.OPTION POST=1\n", 1
    )
    for mode, text in SPICE_SOURCES.items()
}

SPECTRE_SOURCES = {
    "dc": """simulator lang=spectre
V1 (in 0) vsource dc=0
R1 (in out) resistor r=1k
R2 (out 0) resistor r=2k
test dc dev=V1 start=0 stop=1 step=0.1
""",
    "ac": """simulator lang=spectre
V1 (in 0) vsource dc=0 ac=1
R1 (in out) resistor r=1k
C1 (out 0) capacitor c=1p
test ac sweeptype=dec points=10 start=1k stop=1meg
""",
    "transient": """simulator lang=spectre
V1 (in 0) vsource type=pulse val0=0 val1=1 delay=0 rise=1n fall=1n width=5n period=10n
R1 (in out) resistor r=1k
C1 (out 0) capacitor c=1p
test tran start=0 stop=20n maxstep=0.1n
""",
    "noise": """simulator lang=spectre
V1 (in 0) vsource dc=0 ac=1
R1 (in out) resistor r=1k
R2 (out 0) resistor r=2k
test noise oProbe=V(out) iprobe=V1 sweeptype=dec points=10 start=1 stop=1meg
""",
}


class CircuitASTTest(unittest.TestCase):
    def test_archive_contains_exact_executed_deck_for_each_mode(self):
        modes = ["dc", "transient", "ac", "noise"]
        layouts = {
            "ngspice": (
                "_ngspice_netlists",
                lambda mode: mode + ".cir",
            ),
            "spectre": (
                "spectre_work",
                lambda mode: mode + ".scs",
            ),
            "hspice": (
                "netlists",
                lambda mode: "hspice_%s_ast.sp" % mode,
            ),
        }
        extensions = {
            "ngspice": ".cir",
            "spectre": ".scs",
            "hspice": ".sp",
        }
        with tempfile.TemporaryDirectory() as temporary:
            for simulator, (directory, source_name) in layouts.items():
                output = Path(temporary) / simulator
                source_dir = output / directory
                source_dir.mkdir(parents=True)
                for mode in modes:
                    (source_dir / source_name(mode)).write_text(
                        "%s:%s\n" % (simulator, mode)
                    )
                _archive_executed_netlists(simulator, output, modes)
                expected = {
                    mode + extensions[simulator] for mode in modes
                }
                actual = {
                    path.name for path in (output / "netlist").iterdir()
                }
                self.assertEqual(actual, expected)

    def test_report_names_all_four_archived_netlists(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "spectre"
            netlist_dir = output / "netlist"
            netlist_dir.mkdir(parents=True)
            archived = {}
            for mode in ("dc", "transient", "ac", "noise"):
                path = netlist_dir / ("%s.scs" % mode)
                path.write_text(mode)
                archived[mode] = str(path)
            report = output / "REPORT.md"
            report.write_text(
                "## 1. Simulation Setup and Execution\n"
                "- [<span style='color: green'>✓</span>] "
                "Circuit file exists and is readable\n"
                "  - Path: /tmp/intermediate/dc.scs\n"
                "- [<span style='color: green'>✓</span>] "
                "Simulator is properly installed\n"
            )
            _rewrite_report_netlist_paths(output, archived)
            text = report.read_text()
            self.assertIn(
                "Circuit files exist and are readable",
                text,
            )
            self.assertNotIn("/tmp/intermediate", text)
            for mode, path in archived.items():
                self.assertIn(
                    "  - %s: %s" % (mode.upper(), Path(path).resolve()),
                    text,
                )

    def test_three_source_dialects_to_three_targets_for_all_modes(self):
        sources = {
            Dialect.NGSPICE: SPICE_SOURCES,
            Dialect.HSPICE: HSPICE_SOURCES,
            Dialect.SPECTRE: SPECTRE_SOURCES,
        }
        for source_dialect, mode_sources in sources.items():
            for mode, text in mode_sources.items():
                with self.subTest(source=source_dialect.value, mode=mode):
                    original = parse_circuit(
                        text, source_dialect, analysis_hint=mode
                    )
                    for target in Dialect:
                        rendered = emit_circuit(original, target)
                        reparsed = parse_circuit(
                            rendered, target, analysis_hint=mode
                        )
                        self.assertEqual(
                            original.semantic_fingerprint(),
                            reparsed.semantic_fingerprint(),
                        )
        for mode in SPICE_SOURCES:
            fingerprints = {
                parse_circuit(
                    mode_sources[mode],
                    source_dialect,
                    analysis_hint=mode,
                ).semantic_fingerprint()
                for source_dialect, mode_sources in sources.items()
            }
            self.assertEqual(
                len(fingerprints),
                1,
                "three source dialects must describe the same %s circuit" % mode,
            )

    def test_repository_standard_and_spectre_decks_round_trip(self):
        root = Path(__file__).resolve().parents[1]
        for mode in ("dc", "ac", "transient", "noise"):
            for source in (
                root / "netlists" / ("%s_circuit.cir" % mode),
                root / "netlists" / "spectre" / ("%s_circuit.scs" % mode),
            ):
                original = parse_circuit(source, analysis_hint=mode)
                for target in Dialect:
                    reparsed = parse_circuit(
                        emit_circuit(original, target),
                        target,
                        analysis_hint=mode,
                    )
                    self.assertEqual(
                        original.semantic_fingerprint(),
                        reparsed.semantic_fingerprint(),
                    )

    def test_compact_alter_assignments_are_physical_and_translated(self):
        source = """Compact alter regression
VGS gate 0 DC 0.8 AC 0
VDS drain 0 DC 1.0 AC 0
R1 gate drain 50
.control
alter @VGS[acmag]=1
alter @VDS[acmag]=0
ac lin 1 1meg 1meg
alter @VGS[acmag]=0
alter @VDS[acmag]=1
ac lin 1 10meg 10meg
.endc
.end
"""
        ast = parse_circuit(source, Dialect.NGSPICE, analysis_hint="ac")
        self.assertEqual(
            ast.analyses[0].alterations,
            {"@VGS[acmag]": "1", "@VDS[acmag]": "0"},
        )
        self.assertEqual(
            ast.analyses[1].alterations,
            {"@VGS[acmag]": "0", "@VDS[acmag]": "1"},
        )
        spectre = emit_circuit(ast, Dialect.SPECTRE)
        hspice = emit_circuit(ast, Dialect.HSPICE)
        self.assertIn(
            "sweep param=mag dev=vgs values=[1]", spectre.lower()
        )
        self.assertIn(
            "sweep param=mag dev=vds values=[1]", spectre.lower()
        )
        self.assertRegex(hspice.lower(), r"vgs\s+gate\s+0\s+dc\s+0\.8\s+ac\s+1")
        self.assertRegex(hspice.lower(), r"vds\s+drain\s+0\s+dc\s+1\.0\s+ac\s+1")

    def test_parameterized_hspice_ac_cases_are_reconstructed(self):
        source = """Parameterized HSPICE AC regression
VG gate 0 DC 0 AC 1
VD drain 0 DC 1 AC 0
R1 gate drain 50
.PARAM AST_AC_FREQUENCY=1000
.AC LIN 1 AST_AC_FREQUENCY AST_AC_FREQUENCY
.ALTER AST_CASE_0
VG gate 0 DC -0.8 AC 1
.TEMP 27
.PARAM AST_AC_FREQUENCY=1000
.ALTER AST_CASE_1
VG gate 0 DC -0.7 AC 0
VD drain 0 DC 1 AC 1
.TEMP 27
.PARAM AST_AC_FREQUENCY=1000000
.ALTER AST_CASE_2
VG gate 0 DC 0.8 AC 1
VD drain 0 DC 1 AC 0
.TEMP 27
.TRAN 1e-11 5e-9
.END
"""
        ast = parse_circuit(
            source,
            Dialect.HSPICE,
            analysis_hint="ac",
        )
        self.assertEqual(
            [analysis.kind for analysis in ast.analyses],
            ["ac", "ac", "tran"],
        )
        first, second, transient = [
            analysis.semantic() for analysis in ast.analyses
        ]
        self.assertEqual(first["parameters"]["start"], 1000.0)
        self.assertEqual(first["alterations"], {"vg": -0.8})
        self.assertEqual(second["parameters"]["start"], 1000000.0)
        self.assertEqual(
            second["alterations"],
            {"@vg[acmag]": 0.0, "@vd[acmag]": 1.0, "vg": -0.7},
        )
        self.assertEqual(transient["parameters"]["stop"], 5e-9)
        self.assertEqual(transient["alterations"], {"vg": 0.8})

    def test_translate_set_writes_manifest_and_all_twelve_decks(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sources = {}
            for mode, text in SPICE_SOURCES.items():
                path = root / ("%s.cir" % mode)
                path.write_text(text)
                sources[mode] = path
            result = translate_circuit_set(sources, root / "translated")
            self.assertEqual(set(result), {item.value for item in Dialect})
            self.assertEqual(
                sum(len(paths) for paths in result.values()), 12
            )
            manifest = json.loads(
                (root / "translated" / "manifest.json").read_text()
            )
            self.assertEqual(set(manifest["semantic_fingerprints"]), set(sources))


if __name__ == "__main__":
    unittest.main()
