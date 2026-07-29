"""
Spectre Post-Processor: Converts Spectre PSF ASCII output to ngspice-compatible text files.

Reads Spectre's PSF ASCII format and generates the identical text files
that the existing DataReader/PlotGenerator/VerificationManager pipeline expects.
"""
import re
import math
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional

from .ac_metrics import polar, y_to_s


class _CaseInsensitiveValues(dict):
    """PSF signal mapping whose lookups are insensitive to simulator casing."""

    def get(self, key, default=None):
        if key in self:
            return super().get(key, default)
        lowered = str(key).lower()
        for actual, value in self.items():
            if str(actual).lower() == lowered:
                return value
        return default


class SpectrePostProcessor:
    """Convert Spectre PSF ASCII output to ngspice-compatible text data files."""

    def __init__(self, logger, data_dir: str):
        self.logger = logger
        self.data_dir = Path(data_dir)

    # ====================================================================
    # PSF ASCII Parser for DC sweep files
    # ====================================================================

    def _parse_psf_dc_groups(self, filepath: Path) -> Dict:
        """Parse a Spectre PSF ASCII DC file, extracting grouped trace values.

        The PSF VALUE section contains N values per step, where N = number of traces.
        Each step's values are written sequentially.

        Returns dict with:
          - 'header': {key: value_or_str}
          - 'trace_names': ordered list of trace names
          - 'trace_types': {trace_name: type_string}
          - 'values': {trace_name: np.array}
          - 'n_steps': number of sweep points
        """
        header = {}
        trace_names = []
        trace_types = {}
        values_raw = {}  # trace_name -> list of floats

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        lines = content.split('\n')

        section = None
        in_prop = False
        type_name = None

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped == 'END':
                break
            if stripped == 'HEADER':
                section = 'header'
                continue
            if stripped == 'TYPE':
                section = 'type'
                continue
            if stripped == 'SWEEP':
                section = 'sweep'
                continue
            if stripped == 'TRACE':
                section = 'trace'
                continue
            if stripped == 'VALUE':
                section = 'value'
                continue

            if section == 'header':
                # Parse "key" "value" or "key" number
                m = re.match(r'"([^"]*)"\s+"([^"]*)"', stripped)
                if m:
                    key = m.group(1)
                    val = m.group(2)
                    try:
                        header[key] = float(val)
                    except ValueError:
                        header[key] = val
                else:
                    m = re.match(r'"([^"]*)"\s+([\d.eE+\-]+)', stripped)
                    if m:
                        try:
                            header[m.group(1)] = float(m.group(2))
                        except ValueError:
                            header[m.group(1)] = m.group(2)

            elif section == 'type':
                if stripped == ')':
                    in_prop = False
                    continue
                if 'PROP(' in stripped:
                    in_prop = True
                    continue
                if in_prop:
                    continue
                # Type definition: "name" TYPE [PROP(...)]
                m = re.match(r'"([^"]*)"\s+(\w+)', stripped)
                if m:
                    type_name = m.group(1)
                    trace_types[type_name] = m.group(2)

            elif section == 'trace':
                if stripped == ')':
                    continue
                # Trace definition: "name" "type" [PROP(...)]
                m = re.match(r'"([^"]*)"\s+"(\w+)"', stripped)
                if m:
                    tname = m.group(1)
                    ttype = m.group(2)
                    trace_names.append(tname)
                    trace_types[tname] = ttype
                    values_raw[tname] = []

            elif section == 'value':
                if stripped == ')':
                    continue
                # Value entry: "name" number
                m = re.match(r'"([^"]*)"\s+([\d.eE+\-]+)', stripped)
                if m is None:
                    m = re.match(
                        r'"([^"]*)"\s+"[^"]+"\s+([\d.eE+\-]+)',
                        stripped,
                    )
                if m:
                    tname = m.group(1)
                    try:
                        val = float(m.group(2))
                        if tname not in values_raw:
                            values_raw[tname] = []
                        values_raw[tname].append(val)
                    except ValueError:
                        pass

        # Determine number of steps - check time/dc/frequency then trace_names
        n_steps = 0
        for tname in ['time', 'dc', 'sweep', 'frequency']:
            if tname in values_raw and len(values_raw[tname]) > 0:
                n_steps = len(values_raw[tname])
                break
        if n_steps == 0 and trace_names:
            n_steps = len(values_raw.get(trace_names[0], []))
        if n_steps == 0 and values_raw:
            n_steps = max(len(values) for values in values_raw.values())

        # Convert to numpy arrays, truncating to n_steps
        result = {
            'header': header,
            'trace_names': trace_names,
            'trace_types': trace_types,
            'values': _CaseInsensitiveValues(),
            'n_steps': n_steps,
        }
        # Copy all parsed values (including time/dc from SWEEP section)
        for tname, vals_list in values_raw.items():
            vals = vals_list
            if len(vals) > n_steps:
                vals = vals[:n_steps]
            elif 0 < len(vals) < n_steps:
                vals = vals + [0.0] * (n_steps - len(vals))
            result['values'][tname] = np.array(vals, dtype=float) if vals else np.array([])

        return result

    # ====================================================================
    # DC Post-Processing
    # ====================================================================

    def process_dc(self, raw_dir: Path) -> bool:
        """Process DC simulation results.

        Generates:
          - iv_data_{temp}.txt: IV curves per temperature
          - bias_point_data.txt: Operating point data at 27C
        """
        self.logger.logger.info("Post-processing Spectre DC output...")
        raw_dir = Path(raw_dir)

        # ---- IV Sweep Files ----
        dc_files = sorted(raw_dir.glob("sw_temp-*_sw_vgs-*_dc_iv.dc"))
        generated_names = False
        short_names = False
        if not dc_files:
            dc_files = sorted(raw_dir.glob(
                "benchmark_temp_*-*_benchmark_dc_*_outer-*_benchmark_dc_*.dc"
            ))
            if not dc_files:
                dc_files = sorted(raw_dir.glob(
                    "benchmark_dc_*_outer-*_benchmark_dc_*.dc"
                ))
            generated_names = bool(dc_files)
        if not dc_files:
            dc_files = sorted(raw_dir.glob("t*-*_x*_outer-*_x*.dc"))
            short_names = bool(dc_files)
        if not dc_files:
            self.logger.logger.error("No DC IV sweep files found")
            return False

        # Group files by temperature index
        # File: sw_temp-TIDX_sw_vgs-GIDX_dc_iv.dc
        temp_groups: Dict[int, Dict[int, Path]] = {}
        for f in dc_files:
            if short_names:
                m = re.match(
                    r't(\d+)-\d+_x\d+_outer-(\d+)_x\d+\.dc',
                    f.name,
                )
            elif generated_names:
                m = re.search(
                    r'benchmark_dc_(\d+)_outer-(\d+)_benchmark_dc_\d+\.dc',
                    f.name,
                )
            else:
                m = re.match(r'sw_temp-(\d+)_sw_vgs-(\d+)_dc_iv\.dc', f.name)
            if m:
                tidx = int(m.group(1))
                gidx = int(m.group(2))
                temp_groups.setdefault(tidx, {})[gidx] = f

        # Parse each file and write combined output per temperature
        for tidx in sorted(temp_groups.keys()):
            vgs_files = temp_groups[tidx]
            temp = None

            # Write combined output with ngspice-compatible header
            # Header: v-sweep v(drain_iv) v(gate_iv) id is ib ig kcl
            out_lines = [
                "v-sweep v(drain_iv) v(gate_iv) id is ib ig kcl\n"
            ]
            sweep_idx = 0
            for gidx in sorted(vgs_files.keys()):
                f = vgs_files[gidx]
                data = self._parse_psf_dc_groups(f)

                if temp is None:
                    temp = data['header'].get('temp', None)

                vals = data['values']

                # Map PSF trace names to our expected signals
                vds = vals.get('drain_iv', vals.get('dc', np.array([])))
                vgs_vals = vals.get('gate_iv', np.array([]))
                vgs_val = float(vgs_vals[0]) if len(vgs_vals) > 0 else 0.0

                id_ = vals.get('Vds_iv:p', np.array([]))
                is_ = vals.get('Vs_iv:p', np.array([]))
                ib_ = vals.get('Vb_iv:p', np.array([]))
                ig_ = vals.get('Vgs_iv:p', np.array([]))

                n = min(len(vds), len(id_), len(is_), len(ib_), len(ig_))
                if n == 0:
                    continue

                for j in range(n):
                    vd = vds[j] if j < len(vds) else 0.0
                    # PSF ``Vsource:p`` is already the current entering the
                    # positive terminal of that source, which is the same
                    # terminal-current convention used by the canonical
                    # ngspice/HSPICE data schema.  Negating it here mirrored
                    # every Spectre DC, bias, and temperature curve.
                    id_val = id_[j] if j < len(id_) else 0.0
                    is_val = is_[j] if j < len(is_) else 0.0
                    ib_val = ib_[j] if j < len(ib_) else 0.0
                    ig_val = ig_[j] if j < len(ig_) else 0.0
                    kcl = abs(id_val + is_val + ig_val + ib_val)
                    out_lines.append(
                        f" {sweep_idx:.10e}  {vd:.10e}  {vgs_val:.10e}  "
                        f"{id_val:.10e}  {is_val:.10e}  {ib_val:.10e}  "
                        f"{ig_val:.10e}  {kcl:.10e}\n"
                    )
                    sweep_idx += 1

            # Determine temperature value
            if temp is not None and temp == int(temp):
                temp_name = f"{int(temp)}"
            elif temp is not None:
                temp_name = f"{temp:.0f}"
            else:
                temp_map = {
                    0: "-40", 1: "0", 2: "25",
                    3: "50", 4: "100", 5: "150",
                }
                temp_name = temp_map.get(tidx, f"{tidx}")

            out_path = self.data_dir / f"iv_data_{temp_name}.txt"
            with open(out_path, 'w') as f:
                f.writelines(out_lines)
            self.logger.logger.info(f"  Written: {out_path} ({len(out_lines) - 1} points)")

        # ---- Bias Point Files ----
        self._process_dc_bias(raw_dir)

        self.logger.logger.info("DC post-processing complete.")
        return True

    def _process_dc_bias(self, raw_dir: Path):
        """Process bias point sweep files."""
        bias_files = sorted(raw_dir.glob("sw_bias-000_sw_vds_bias-*_sw_vgs_bias-*_dc_bias.dc"))
        if not bias_files:
            bias_files = sorted(raw_dir.glob("*op*.dc"))
        if not bias_files:
            self.logger.logger.info("  No dedicated bias files, extracting from IV data")
            self._extract_bias_from_iv()
            return

        out_lines = []
        for f in bias_files:
            data = self._parse_psf_dc_groups(f)
            vals = data['values']

            vd = vals.get('drain_bias', np.array([]))
            vg = vals.get('gate_bias', np.array([]))
            id_ = vals.get('Vds_bias:p', np.array([]))
            is_ = vals.get('Vs_bias:p', np.array([]))
            ib_ = vals.get('Vb_bias:p', np.array([]))
            ig_ = vals.get('Vgs_bias:p', np.array([]))

            # Get the first (and only) point
            vd_val = float(vd[0]) if len(vd) > 0 else 0.0
            vg_val = float(vg[0]) if len(vg) > 0 else 0.0
            id_val = float(id_[0]) if len(id_) > 0 else 0.0
            is_val = float(is_[0]) if len(is_) > 0 else 0.0
            ib_val = float(ib_[0]) if len(ib_) > 0 else 0.0
            ig_val = float(ig_[0]) if len(ig_) > 0 else 0.0

            out_lines.append(
                f"{vd_val:.10e} {vg_val:.10e} {id_val:.10e} "
                f"{ig_val:.10e} {is_val:.10e} {ib_val:.10e}\n"
            )

        # Prepend header
        out_lines.insert(0, "v(drain_bias) v(gate_bias) id_bias ig_bias is_bias ib_bias\n")

        out_path = self.data_dir / "bias_point_data.txt"
        with open(out_path, 'w') as f:
            f.writelines(out_lines)
        self.logger.logger.info(f"  Written: {out_path} ({len(out_lines) - 1} bias points)")

    def _extract_bias_from_iv(self):
        """Fallback: extract bias points from IV data at 25C."""
        for temp in ['25', '27', '0']:
            iv_file = self.data_dir / f"iv_data_{temp}.txt"
            if iv_file.exists():
                data = np.loadtxt(iv_file, skiprows=1)
                bias_pts = [
                    (0.0, 0.0), (0.0, 0.6), (0.0, 1.2),
                    (0.6, 0.0), (0.6, 0.6), (0.6, 1.2),
                    (1.2, 0.0), (1.2, 0.6), (1.2, 1.2),
                ]
                out_path = self.data_dir / "bias_point_data.txt"
                with open(out_path, 'w') as f:
                    f.write("v(drain_bias) v(gate_bias) id_bias ig_bias is_bias ib_bias\n")
                    for vds, vgs in bias_pts:
                        mask = (
                            (np.abs(data[:, 1] - vds) < 0.001)
                            & (np.abs(data[:, 2] - vgs) < 0.001)
                        )
                        row = data[mask]
                        if len(row) > 0:
                            r = row[0]
                            f.write(
                                f"{r[1]:.10e} {r[2]:.10e} {r[3]:.10e} "
                                f"{r[6]:.10e} {r[4]:.10e} {r[5]:.10e}\n"
                            )
                self.logger.logger.info(f"  Written (from IV): {out_path}")
                return

    # ====================================================================
    # AC Complex Parser
    # ====================================================================

    def _parse_ac_complex(self, filepath: Path) -> dict:
        """Parse AC PSF extracting complex values in (real, imag) format."""
        result = {}
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        in_value = False
        for line in content.split('\n'):
            s = line.strip()
            if s == 'VALUE': in_value = True; continue
            if s == 'END' and in_value: break
            if not in_value: continue
            m = re.match(r'"([^"]*)"\s+\(([\d.eE+\-]+)\s+([\d.eE+\-]+)\)', s)
            if m:
                try:
                    result[m.group(1)] = complex(float(m.group(2)), float(m.group(3)))
                except ValueError: pass
            else:
                m = re.match(r'"([^"]*)"\s+([\d.eE+\-]+)', s)
                if m:
                    try: result[m.group(1)] = float(m.group(2))
                    except ValueError: pass
        return result

    # ====================================================================
    # AC Post-Processing
    # ====================================================================

    def process_ac(self, raw_dir: Path) -> bool:
        """Extract every AC metric from its corresponding AST analysis case."""
        self.logger.logger.info("Post-processing Spectre AC output...")
        raw_dir = Path(raw_dir)
        vg_values = [-0.8 + i * 0.05 for i in range(41)]

        def find_case_file(case, suffix=".ac"):
            matches = sorted(raw_dir.glob(f"*x{case}{suffix}"))
            if len(matches) != 1:
                raise ValueError(
                    "expected one Spectre result for AST case %d, found %d"
                    % (case, len(matches))
                )
            return matches[0]

        def value(mapping, name, expected_type=None):
            lowered = name.lower()
            matches = [
                item for key, item in mapping.items()
                if str(key).lower() == lowered
            ]
            if len(matches) != 1:
                raise ValueError(f"missing Spectre signal {name}")
            result = matches[0]
            if expected_type is not None and not isinstance(
                result, expected_type
            ):
                raise ValueError(
                    f"Spectre signal {name} has wrong value type"
                )
            return result

        def ac_case(case, frequency):
            result = self._parse_ac_complex(find_case_file(case))
            actual = float(value(result, "freq"))
            if abs(actual - frequency) > max(abs(frequency), 1.0) * 1e-9:
                raise ValueError(
                    "Spectre AST case %d frequency %.10g != %.10g"
                    % (case, actual, frequency)
                )
            return result

        cv_lines = [
            "Vg Cgg_1kHz Cgg_10kHz Cgg_100kHz Cgg_1MHz "
            "Cgb_1MHz Cgs_1MHz Cgd_1MHz"
        ]
        matrix_lines = [
            "Vg Cgg Cdg Csg Cbg Cgd Cdd Csd Cbd "
            "Cgs Cds Css Cbs Cgb Cdb Csb Cbb"
        ]
        for gate_index, gate_voltage in enumerate(vg_values):
            base = gate_index * 8
            capacitances = []
            for offset, frequency in enumerate((1e3, 1e4, 1e5, 1e6)):
                result = ac_case(base + offset, frequency)
                capacitances.append(
                    -value(result, "vg:p", complex).imag
                    / (2.0 * math.pi * frequency)
                )
            matrix_columns = []
            for column in range(4):
                result = ac_case(base + 4 + column, 1e6)
                matrix_columns.append([
                    -value(result, source + ":p", complex).imag
                    / (2.0 * math.pi * 1e6)
                    for source in ("vg", "vd", "vs", "vb")
                ])
            cv_lines.append(
                f"{gate_voltage:.6e} "
                + " ".join(f"{item:.6e}" for item in capacitances)
                + " "
                + " ".join(
                    f"{matrix_columns[0][index]:.6e}"
                    for index in (3, 2, 1)
                )
            )
            matrix_lines.append(
                f"{gate_voltage:.6e} "
                + " ".join(
                    f"{item:.6e}"
                    for column in matrix_columns
                    for item in column
                )
            )
        (self.data_dir / "cv_data.txt").write_text(
            "\n".join(cv_lines) + "\n"
        )
        (self.data_dir / "cmatrix_data.txt").write_text(
            "\n".join(matrix_lines) + "\n"
        )

        sparameter_lines = [
            "# S-parameter analysis",
            "# freq s11_mag s11_phase s12_mag s12_phase "
            "s21_mag s21_phase s22_mag s22_phase",
        ]
        for offset, frequency in enumerate((1e6, 1e7, 1e8, 1e9)):
            gate = ac_case(328 + 2 * offset, frequency)
            drain = ac_case(329 + 2 * offset, frequency)
            gate_voltage = value(gate, "gate_in2", complex)
            drain_voltage = value(drain, "drain_in2", complex)
            if abs(gate_voltage) < 1e-15 or abs(drain_voltage) < 1e-15:
                raise ValueError(
                    f"zero Spectre S-parameter excitation at {frequency:g} Hz"
                )
            y11 = -value(gate, "vgs:p", complex) / gate_voltage
            y21 = -value(gate, "vds:p", complex) / gate_voltage
            y12 = -value(drain, "vgs:p", complex) / drain_voltage
            y22 = -value(drain, "vds:p", complex) / drain_voltage
            s11, s12, s21, s22 = y_to_s(y11, y12, y21, y22)
            fields = [
                *polar(s11), *polar(s12),
                *polar(s21), *polar(s22),
            ]
            sparameter_lines.append(
                f"{frequency:.6e} "
                + " ".join(f"{item:.6e}" for item in fields)
            )
        (self.data_dir / "sparams_data.txt").write_text(
            "\n".join(sparameter_lines) + "\n"
        )

        nqs_lines = [
            "# Non-quasi-static effects analysis - phase shifts",
            "# freq vg_phase id_phase phase_diff",
        ]
        for offset, frequency in enumerate((1e7, 1e8, 1e9, 1e10)):
            result = ac_case(336 + offset, frequency)
            gate_phase = math.degrees(
                math.atan2(
                    value(result, "gate_1", complex).imag,
                    value(result, "gate_1", complex).real,
                )
            )
            drain_phase = math.degrees(
                math.atan2(
                    value(result, "vd:p", complex).imag,
                    value(result, "vd:p", complex).real,
                )
            )
            nqs_lines.append(
                f"{frequency:.6e} {gate_phase:.6e} "
                f"{drain_phase:.6e} "
                f"{(gate_phase - drain_phase):.6e}"
            )
        (self.data_dir / "nqs_effects.txt").write_text(
            "\n".join(nqs_lines) + "\n"
        )

        charge_file = find_case_file(340, ".tran.tran")
        values = self._parse_psf_dc_groups(charge_file)["values"]
        required = ("time", "gate_3", "vgq:p", "vdq:p", "vsq:p", "vbq:p")
        arrays = []
        for name in required:
            item = values.get(name)
            if item is None:
                raise ValueError(f"missing Spectre charge signal {name}")
            arrays.append(item)
        count = min(len(item) for item in arrays)
        if count < 2:
            raise ValueError("insufficient Spectre charge samples")
        out_path = self.data_dir / "charge_conservation.txt"
        with out_path.open("w") as stream:
            stream.write("Title: Spectre charge conservation analysis\n")
            stream.write("Plotname: Transient Analysis\nFlags: real\n")
            stream.write("No. Variables: 6\n")
            stream.write(f"No. Points: {count}\nVariables:\n")
            stream.write("\t0\ttime\ttime\n\t1\tv(gate_3)\tvoltage\n")
            stream.write(
                "\t2\ti(vgq)\tcurrent\n\t3\ti(vdq)\tcurrent\n"
                "\t4\ti(vsq)\tcurrent\n\t5\ti(vbq)\tcurrent\nValues:\n"
            )
            for index in range(count):
                stream.write(f" {index}\t{arrays[0][index]:.10e}\n")
                for signal in arrays[1:]:
                    stream.write(f"\t{signal[index]:.10e}\n")
                stream.write("\n")

        self.logger.logger.info("AC post-processing complete.")
        return True

    # ====================================================================
    # Transient Post-Processing
    # ====================================================================

    def process_transient(self, raw_dir: Path) -> bool:
        """Process transient simulation results.

        Generates 8 text files matching ngspice transient_circuit.cir output.
        """
        self.logger.logger.info("Post-processing Spectre transient output...")
        raw_dir = Path(raw_dir)

        # Helper: read PSF tran file, write text with double-time + data columns
        def _write_tran_file(psf_name: str, out_name: str,
                             voltage_cols: list, current_cols: list):
            """Parse a transient PSF file and write ngspice-compatible text."""
            psf_files = sorted(raw_dir.glob(psf_name))
            generated_index = {
                "tran_ls.tran.tran": 0,
                "tran_sw.tran.tran": 1,
                "tran_delay.tran.tran": 2,
                "sw_pwr_27-000_tran_pwr_27.tran.tran": 3,
                "sw_pwr_100-000_tran_pwr_100.tran.tran": 4,
                "tran_qs.tran.tran": 5,
                "tran_charge.tran.tran": 6,
            }.get(psf_name)
            if not psf_files and generated_index is not None:
                psf_files = sorted(
                    raw_dir.glob(f"*x{generated_index}.tran.tran")
                )
                if not psf_files:
                    psf_files = sorted(
                        raw_dir.glob(
                            f"benchmark_tran_{generated_index}.tran.tran"
                        )
                    )
            if not psf_files:
                self.logger.logger.warning(f"  No PSF for {out_name} ({psf_name})")
                return False
            data = self._parse_psf_dc_groups(psf_files[0])
            vals = data['values']

            # Build time array
            time = vals.get('time')
            if time is None:
                raise ValueError(f"missing Spectre time signal for {out_name}")
            n = len(time)
            if n == 0:
                raise ValueError(f"empty Spectre transient result for {out_name}")

            # Build header and data columns
            col_names = ["time", "time"]
            arrays = [time, time]

            for vcol in voltage_cols:
                key = vcol  # e.g., "gate_tran"
                col_names.append(f"v({key})")
                arr = vals.get(key)
                if arr is None or len(arr) != n:
                    raise ValueError(
                        f"missing/incomplete Spectre signal {key} for {out_name}"
                    )
                arrays.append(arr[:n])

            for ccol in current_cols:
                key = ccol  # e.g., "Vds_tran:p"
                col_names.append(f"i({key.replace(':p', '')})")
                arr = vals.get(key)
                if arr is None or len(arr) != n:
                    raise ValueError(
                        f"missing/incomplete Spectre signal {key} for {out_name}"
                    )
                arrays.append(arr[:n])

            # Write file matching ngspice wrdata format
            out_path = self.data_dir / out_name
            with open(out_path, 'w') as f:
                f.write(" " + " ".join(col_names) + "\n")
                for j in range(n):
                    row = " ".join(f"{a[j]:.10e}" for a in arrays)
                    f.write(f" {row}\n")
            self.logger.logger.info(f"  Written: {out_path} ({n} points)")
            return True

        # ---- 1. Large-Signal Transient ----
        ok = _write_tran_file(
            "tran_ls.tran.tran", "tran_large_signal.txt",
            ["gate_tran", "drain_tran"],
            ["Vds_tran:p", "Vgs_tran:p", "Vs_tran:p", "Vb_tran:p"],
        )

        # ---- 2. Switching Response ----
        ok &= _write_tran_file(
            "tran_sw.tran.tran", "tran_switching.txt",
            ["in_inv", "out_inv"], ["Vdd_inv:p"],
        )

        # ---- 3. Switching Power (computed) ----
        sw_files = sorted(raw_dir.glob("tran_sw.tran.tran"))
        if not sw_files:
            sw_files = sorted(raw_dir.glob("*x1.tran.tran"))
        if sw_files:
            data = self._parse_psf_dc_groups(sw_files[0])
            vals = data['values']
            time = vals.get('time')
            vdd = vals.get('vdd_inv')
            ivdd = vals.get('Vdd_inv:p')
            if time is None or vdd is None or ivdd is None:
                raise ValueError("missing Spectre switching-power signal")
            n = min(len(time), len(vdd), len(ivdd))
            if n > 0:
                power = -np.array(vdd[:n]) * np.array(ivdd[:n])
                out_path = self.data_dir / "tran_switching_power.txt"
                with open(out_path, 'w') as f:
                    f.write(" time time power_switching\n")
                    for j in range(n):
                        f.write(f" {time[j]:.10e} {time[j]:.10e} {power[j]:.10e}\n")
                self.logger.logger.info(f"  Written: {out_path} ({n} points)")
            else:
                raise ValueError("empty Spectre switching-power result")
        else:
            raise ValueError("missing Spectre switching-power PSF")

        # ---- 4. Delay Effect ----
        ok &= _write_tran_file(
            "tran_delay.tran.tran", "tran_delay.txt",
            ["in_delay", "mid1_delay", "mid2_delay", "out_delay"], [],
        )

        # ---- 5 & 6. Power Dissipation at 27C and 100C ----
        for temp_tag, psf_pat in [("27C", "sw_pwr_27-000_tran_pwr_27.tran.tran"),
                                   ("100C", "sw_pwr_100-000_tran_pwr_100.tran.tran")]:
            psf_files = sorted(raw_dir.glob(psf_pat))
            if not psf_files:
                generated_index = 3 if temp_tag == "27C" else 4
                psf_files = sorted(
                    raw_dir.glob(f"*x{generated_index}.tran.tran")
                )
            if not psf_files:
                raise ValueError(
                    f"missing Spectre power PSF for {temp_tag}"
                )
            data = self._parse_psf_dc_groups(psf_files[0])
            vals = data['values']
            required = (
                "time",
                "in_power",
                "out_power",
                "vdd_power",
                "Vdd_power:p",
            )
            arrays = [vals.get(name) for name in required]
            if any(item is None for item in arrays):
                raise ValueError(
                    f"missing Spectre power signal for {temp_tag}"
                )
            time, vin, vout, vdd, idd = arrays
            n = min(len(item) for item in arrays)
            if n < 2:
                raise ValueError(
                    f"empty Spectre power result for {temp_tag}"
                )
            power_diss = (
                -np.asarray(vdd[:n]) * np.asarray(idd[:n])
            )
            energy = np.zeros(n)
            for index in range(1, n):
                energy[index] = (
                    energy[index - 1]
                    + 0.5
                    * (power_diss[index] + power_diss[index - 1])
                    * (time[index] - time[index - 1])
                )
            out_path = self.data_dir / f"tran_power_{temp_tag}.txt"
            with open(out_path, 'w') as f:
                f.write(" time time v(in_power) v(out_power) power_diss energy\n")
                for j in range(n):
                    f.write(f" {time[j]:.10e} {time[j]:.10e} "
                            f"{vin[j]:.10e} {vout[j]:.10e} "
                            f"{power_diss[j]:.10e} {energy[j]:.10e}\n")
            self.logger.logger.info(f"  Written: {out_path} ({n} points)")

        # ---- 7. Quasi-Static ----
        ok &= _write_tran_file(
            "tran_qs.tran.tran", "tran_quasi_static.txt",
            ["gate_qs", "drain_qs"], ["Vds_qs:p"],
        )

        # ---- 8. Charge Conservation ----
        ok &= _write_tran_file(
            "tran_charge.tran.tran", "tran_charge.txt",
            ["gate_charge"],
            ["Vg_charge:p", "Vd_charge:p", "Vs_charge:p", "Vb_charge:p"],
        )

        self.logger.logger.info("Transient post-processing complete.")
        return bool(ok)

    # ====================================================================
    # Noise Post-Processing
    # ====================================================================

    def process_noise(self, raw_dir: Path) -> bool:
        """Extract every noise setup directly from its AST analysis case."""
        self.logger.logger.info("Post-processing Spectre noise output...")
        raw_dir = Path(raw_dir)

        def case(case_index):
            files = sorted(raw_dir.glob(f"*x{case_index}.noise"))
            if len(files) != 1:
                raise ValueError(
                    "expected one Spectre noise result for AST case %d, "
                    "found %d" % (case_index, len(files))
                )
            frequency, density = self._parse_noise_psf(files[0])
            if len(frequency) < 2 or len(density) != len(frequency):
                raise ValueError(
                    f"invalid Spectre noise result for AST case {case_index}"
                )
            return frequency, density

        biases = (
            ("0.3", "0.3"), ("0.3", "0.6"), ("0.3", "0.9"),
            ("0.3", "1.2"), ("0.6", "0.3"), ("0.6", "0.6"),
        )
        for case_index, (vgs, vds) in enumerate(biases):
            frequency, density = case(case_index)
            output = (
                self.data_dir
                / f"thermal_noise_vgs{vgs}_vds{vds}.txt"
            )
            self._write_noise_file(output, frequency, density)

        for case_index, filename in (
            (6, "flicker_noise.txt"), (7, "shot_noise.txt")
        ):
            frequency, density = case(case_index)
            self._write_noise_file(
                self.data_dir / filename, frequency, density
            )

        for case_index, temperature in enumerate(
            (-40, 0, 27, 50, 100, 150), start=8
        ):
            frequency, density = case(case_index)
            self._write_noise_file(
                self.data_dir / f"noise_temp{temperature}.txt",
                frequency,
                density,
            )

        self.logger.logger.info("Noise post-processing complete.")
        return True

    def _parse_noise_psf(self, filepath: Path):
        """Parse Spectre noise PSF extracting freq and output noise."""
        freq_vals = []
        noise_vals = []
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        lines = content.split('\n')
        in_value = False
        i = 0
        while i < len(lines):
            s = lines[i].strip()
            if s == 'VALUE': in_value = True; i += 1; continue
            if s == 'END' and in_value: break
            if not in_value: i += 1; continue
            # Extract freq
            m = re.match(r'"freq"\s+([\d.eE+\-]+)', s)
            if m:
                freq_vals.append(float(m.group(1)))
                # Scan forward for "out" value in this block
                j = i + 1
                while j < len(lines):
                    ns = lines[j].strip()
                    if ns.startswith('"freq"') or ns == 'END':
                        break
                    om = re.match(r'"out"\s+([\d.eE+\-]+)', ns)
                    if om:
                        # Convert V²/Hz → V/√Hz
                        noise_vals.append(np.sqrt(float(om.group(1))))
                        break
                    j += 1
                if len(noise_vals) < len(freq_vals):
                    noise_vals.append(0.0)
            i += 1
        return np.array(freq_vals), np.array(noise_vals)

    def _write_noise_file(self, filepath: Path, freq: np.ndarray, noise: np.ndarray):
        """Write ngspice-format noise file with Values: section."""
        n = min(len(freq), len(noise))
        with open(filepath, 'w') as f:
            f.write("Title: * noise analysis\n")
            f.write("Date: 2026-07-20\n")
            f.write("Plotname: Noise Spectral Density Curves\n")
            f.write("Flags: real\n")
            f.write(f"No. Variables: 3\n")
            f.write(f"No. Points: {n}\n")
            f.write("Variables:\n")
            f.write("\t0\tfrequency\tfrequency\tgrid=3\n")
            f.write("\t1\tfreq\tfrequency\n")
            f.write("\t2\tnoise_spectrum\tvoltage-density\n")
            f.write("Values:\n")
            for j in range(n):
                f.write(f" {j}\t{freq[j]:.15e}\n")
                f.write(f"\t{freq[j]:.15e}\n")
                f.write(f"\t{noise[j]:.15e}\n")

    # ====================================================================
    # Helpers
    # ====================================================================

    def _ensure_file(self, filename: str, content: str):
        """Create a file if it doesn't exist."""
        path = self.data_dir / filename
        if not path.exists():
            with open(path, 'w') as f:
                f.write(content)
            self.logger.logger.info(f"  Created stub: {path}")

    # ====================================================================
    # Main dispatch
    # ====================================================================

    def process_all(self, raw_dir: Path, modes: List[str]) -> bool:
        """Run all post-processing for selected modes."""
        success = True
        if 'dc' in modes:
            if not self.process_dc(raw_dir):
                success = False
        if 'ac' in modes:
            if not self.process_ac(raw_dir):
                success = False
        if 'transient' in modes:
            if not self.process_transient(raw_dir):
                success = False
        if 'noise' in modes:
            if not self.process_noise(raw_dir):
                success = False
        return success
