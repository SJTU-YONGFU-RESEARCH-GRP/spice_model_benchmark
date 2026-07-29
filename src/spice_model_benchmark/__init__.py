"""
SPICE Model Benchmark System

A comprehensive benchmarking system for SPICE models, allowing for the automated
verification and validation of semiconductor device models with a focus on MOSFETs.
"""

import os
import re
from pathlib import Path
from typing import Optional, Union, List
from .mosfet_simulation import MOSFETSimulation
from .logger import Logger
from .simulation_runner import SimulationRunner
from .data_reader import DataReader
from .plot_generator import PlotGenerator
from .verification_manager import VerificationManager
from .circuit_ast import (
    Analysis,
    CircuitAST,
    CircuitSyntaxError,
    Dialect,
    Element,
    emit_circuit,
    parse_circuit,
    translate_circuit,
    translate_circuit_set,
)
from .fixture_geometry import apply_primary_geometry, read_geometry_override

__version__ = "1.0.0"
__all__ = [
    "MOSFETSimulation",
    "Logger",
    "SimulationRunner",
    "DataReader",
    "PlotGenerator",
    "VerificationManager",
    "Analysis",
    "CircuitAST",
    "CircuitSyntaxError",
    "Dialect",
    "Element",
    "emit_circuit",
    "parse_circuit",
    "translate_circuit",
    "translate_circuit_set",
    "benchmark_spice_model",
    "cli",
]


def benchmark_spice_model(
    model_file: Union[str, Path],
    output_dir: Union[str, Path] = "spice_benchmark_results",
    modes: Optional[List[str]] = None,
    dpi: int = 300,
    log_level: str = "INFO",
    dc_circuit: Optional[Union[str, Path]] = None,
    transient_circuit: Optional[Union[str, Path]] = None,
    noise_circuit: Optional[Union[str, Path]] = None,
    ac_circuit: Optional[Union[str, Path]] = None,
) -> bool:
    """
    Run comprehensive SPICE model benchmarking with a single model file.

    This function provides a simplified interface for benchmarking SPICE models.
    It can automatically use default circuit files or accept custom circuit files.

    Args:
        model_file: Path to the SPICE model file (.inc, .lib, or .model file)
        output_dir: Directory to save results (default: "spice_benchmark_results")
        modes: List of analysis modes to run. Options: ['dc', 'transient', 'ac', 'noise']
               If None, runs all modes.
        dpi: Resolution for generated plots (default: 300)
        log_level: Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        dc_circuit: Path to custom DC analysis circuit file (optional)
        transient_circuit: Path to custom transient analysis circuit file (optional)
        noise_circuit: Path to custom noise analysis circuit file (optional)
        ac_circuit: Path to custom AC analysis circuit file (optional)

    Returns:
        bool: True if benchmarking completed successfully, False otherwise

    Example:
        >>> from spice_model_benchmark import benchmark_spice_model
        >>> success = benchmark_spice_model("my_model.inc")
        >>> if success:
        ...     print("Benchmarking completed successfully!")

    Note:
        If custom circuit files are not provided, the function will look for default
        circuit files in the 'netlists/' directory relative to the current working
        directory, or use built-in default circuits.
    """
    # Convert paths to Path objects
    model_file = Path(model_file)
    output_dir = Path(output_dir)

    # Set default modes if not specified
    if modes is None:
        modes = ['dc', 'transient', 'ac', 'noise']

    # Locate netlists directory early (needed for circuit adaptation during conversion).
    candidate_netlists_dirs = [
        Path.cwd() / "netlists",
        Path(__file__).resolve().parent.parent / "netlists",
    ]
    default_circuit_dir = next((p for p in candidate_netlists_dirs if p.exists()), None)

    if dc_circuit is None and default_circuit_dir is not None:
        default_dc = default_circuit_dir / "dc_circuit.cir"
        dc_circuit = str(default_dc) if default_dc.exists() else None

    if transient_circuit is None and default_circuit_dir is not None:
        default_transient = default_circuit_dir / "transient_circuit.cir"
        transient_circuit = str(default_transient) if default_transient.exists() else None

    if noise_circuit is None and default_circuit_dir is not None:
        default_noise = default_circuit_dir / "noise_circuit.cir"
        noise_circuit = str(default_noise) if default_noise.exists() else None

    if ac_circuit is None and default_circuit_dir is not None:
        default_ac = default_circuit_dir / "ac_circuit.cir"
        ac_circuit = str(default_ac) if default_ac.exists() else None

    # Check if required circuit files exist (or were resolved).
    missing_circuits = []
    if 'dc' in modes and (not dc_circuit or not Path(dc_circuit).exists()):
        missing_circuits.append(f"DC circuit: {dc_circuit or '<not found>'}")
    if 'transient' in modes and (not transient_circuit or not Path(transient_circuit).exists()):
        missing_circuits.append(f"Transient circuit: {transient_circuit or '<not found>'}")
    if 'noise' in modes and (not noise_circuit or not Path(noise_circuit).exists()):
        missing_circuits.append(f"Noise circuit: {noise_circuit or '<not found>'}")
    if 'ac' in modes and (not ac_circuit or not Path(ac_circuit).exists()):
        missing_circuits.append(f"AC circuit: {ac_circuit or '<not found>'}")

    if missing_circuits:
        print(f"Error: Missing required circuit files:")
        for circuit in missing_circuits:
            print(f"  - {circuit}")
        if default_circuit_dir is None:
            print("\nHint: could not locate a 'netlists/' folder from the current working directory.")
            print("      Run from your repo root (where netlists/ exists) or pass --dc-circuit/--ac-circuit, etc.")
        else:
            print(f"\nHint: resolved netlists directory: {default_circuit_dir}")
        print("\nPlease ensure circuit files exist or provide custom circuit files.")
        return False

    # Adapt the stock FreePDK45 decks to the model that the caller actually
    # requested.  Previously model_file was accepted by this API but never
    # used by the ngspice path, so three of four modes silently kept the
    # repository-relative FreePDK45 include and failed outside netlists/.
    model_text = model_file.read_text(errors="replace")
    model_cards = [
        (match.group(1), match.group(2).lower())
        for match in re.finditer(
            r"(?i)\.model\s+(\S+)\s+(nmos|pmos)\b",
            model_text,
        )
    ]
    source_cards = [
        card for card in model_cards if not card[0].lower().startswith("__fixture_")
    ]
    if not source_cards:
        raise ValueError(
            f"No non-fixture MOS model card found in {model_file}; "
            "the benchmark will not substitute a fallback device model"
        )
    selected_match = re.search(
        r"(?im)^\s*\*\s*BENCHMARK_PRIMARY_MODEL:\s*(\S+)\s*$",
        model_text,
    )
    selected_card = None
    if selected_match:
        selected_name = selected_match.group(1)
        selected_card = next(
            (
                card
                for card in source_cards
                if card[0].lower() == selected_name.lower()
            ),
            None,
        )
        if selected_card is None:
            raise ValueError(
                f"Selected benchmark card {selected_name} is not present in "
                f"{model_file}"
            )
    source_nmos = next(
        (re.sub(r"\.\d+$", "", name) for name, kind in source_cards if kind == "nmos"),
        None,
    )
    source_pmos = next(
        (re.sub(r"\.\d+$", "", name) for name, kind in source_cards if kind == "pmos"),
        None,
    )
    if selected_card is not None:
        if selected_card[1] == "nmos":
            source_nmos = selected_card[0]
        else:
            source_pmos = selected_card[0]
    fixture_nmos = next(
        (name for name, kind in model_cards if kind == "nmos" and name.lower().startswith("__fixture_")),
        None,
    )
    fixture_pmos = next(
        (name for name, kind in model_cards if kind == "pmos" and name.lower().startswith("__fixture_")),
        None,
    )
    nmos_name = source_nmos or fixture_nmos
    pmos_name = source_pmos or fixture_pmos
    if nmos_name is None or pmos_name is None:
        missing = "NMOS" if nmos_name is None else "PMOS"
        raise ValueError(
            f"Benchmark circuit requires an explicit {missing} model card; "
            "no fallback model will be generated"
        )
    primary_name = source_nmos or source_pmos
    primary_is_pmos = source_nmos is None and source_pmos is not None
    adapted_dir = output_dir / "_ngspice_netlists"
    adapted_dir.mkdir(parents=True, exist_ok=True)

    def adapt_circuit(circuit: Optional[Union[str, Path]]) -> Optional[str]:
        if circuit is None:
            return None
        source = Path(circuit)
        content = source.read_text(errors="replace")
        content = re.sub(
            r"(?im)^\s*\.inc(?:lude)?\s+.*?FreePDK45/nom\.inc\s*$",
            f".include '{model_file.resolve()}'",
            content,
        )
        # Mark the single-device analyses before filling the complementary
        # circuit roles.  For PMOS-only inputs this keeps the actual PMOS as
        # the device under characterization while the fixture NMOS is used
        # only by the CMOS inverter sections.
        single_instances = r"(?:M1|M2|M3|M_tran|M_charge|M_qs|M_noise|M_flicker|M_shot)"
        content = re.sub(
            rf"(?im)^(\s*{single_instances}\b(?:\s+\S+){{4}}\s+)\S+",
            rf"\g<1>{primary_name}",
            content,
        )
        content = content.replace("NMOS_VTG", nmos_name)
        content = content.replace("PMOS_VTG", pmos_name)
        content = apply_primary_geometry(
            content,
            primary_name,
            read_geometry_override(model_file),
        )
        if primary_is_pmos:
            # Bias a PMOS referenced to ground with negative VDS/VGS.  Only
            # sources belonging to the marked single-device sections are
            # changed; positive-supply CMOS inverter sections remain intact.
            primary_sources = (
                "Vds_iv", "Vgs_iv", "Vds_bias", "Vgs_bias",
                "VG", "VD", "VGS", "VDS", "VGQ", "VDQ",
                "Vgs_tran", "Vds_tran", "Vg_charge", "Vd_charge",
                "Vgs_qs", "Vds_qs", "Vgs_noise", "Vds_noise",
                "Vdd_noise", "Vin_noise", "Vbias_f", "Vgs_flicker",
                "Vdd_shot", "Vgs_shot",
            )
            source_pattern = "|".join(map(re.escape, primary_sources))

            def negate_source_line(match: re.Match) -> str:
                line = match.group(0)
                return re.sub(
                    r"(?<![-\w.])((?:1\.2|1\.0|0\.9|0\.8|0\.6|0\.3))(?![\w.])",
                    r"-\1",
                    line,
                )

            content = re.sub(
                rf"(?im)^\s*(?:{source_pattern})\b.*$",
                negate_source_line,
                content,
            )
            content = re.sub(
                rf"(?im)^(\s*alter\s+(?:{source_pattern})\s*=\s*)"
                r"(?!(?:0(?:\.0*)?)\s*$)([+]?(?:\d+(?:\.\d*)?|\.\d+))",
                lambda match: match.group(1) + "-" + match.group(2).lstrip("+"),
                content,
            )
            content = re.sub(
                r"(?im)^(\s*dc\s+Vds_iv\s+)0\s+1\.2\s+0\.01"
                r"(\s+Vgs_iv\s+)0\s+1\.2\s+0\.2",
                r"\g<1>0 -1.2 -0.01\g<2>0 -1.2 -0.2",
                content,
            )
            content = re.sub(
                r"(?im)^(\s*let\s+vg_start\s*=\s*)-0\.8.*$",
                r"\g<1>0.8",
                content,
            )
            content = re.sub(
                r"(?im)^(\s*let\s+vg_stop\s*=\s*)1\.2.*$",
                r"\g<1>-1.2",
                content,
            )
            content = re.sub(
                r"(?im)^(\s*let\s+vg_step\s*=\s*)0\.05.*$",
                r"\g<1>-0.05",
                content,
            )
        destination = adapted_dir / source.name
        destination.write_text(content)
        return str(destination)

    dc_circuit = adapt_circuit(dc_circuit)
    transient_circuit = adapt_circuit(transient_circuit)
    noise_circuit = adapt_circuit(noise_circuit)
    ac_circuit = adapt_circuit(ac_circuit)

    # Create simulation instance
    simulation = MOSFETSimulation(
        dc_circuit_file=dc_circuit,
        transient_circuit_file=transient_circuit,
        noise_circuit_file=noise_circuit,
        ac_circuit_file=ac_circuit,
        output_dir=str(output_dir),
        dpi=dpi,
        log_level=log_level,
    )

    # Run the benchmark
    return simulation.run(modes=modes)
