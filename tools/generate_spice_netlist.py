#!/usr/bin/env python3
"""Generate an adapted SPICE netlist from a base template.

This script uses the SPICE AST parser to help adapt a generic
"baseline" netlist to a *specific SPICE model file* with minimal
manual editing.

You provide:

- A base netlist (e.g. ``dc_circuit.cir``) that uses a placeholder
  MOS model name such as ``NMOS_VTG``.
- A SPICE model file (``--model-file``) that contains one or more
  ``.model`` or ``.subckt`` definitions.
- The exact model/subcircuit name to use (``--device-name``).

The script will:

1. Parse the base netlist using SPICEParser to detect how MOS devices
   are instantiated:
   - "model" style: ``Mxxx d g s b MODEL_NAME ...`` (uses ``.model``)
   - "subckt" style: ``Xxxx d g s b SUBCKT_NAME ...`` (uses ``.subckt``)

2. Parse the given model file and locate the requested device name as
   either a ``.model`` or ``.subckt`` definition, and infer a reasonable
   VDD from the model names/parameters.

3. Create one or more new netlists by:
   - Keeping the original include line from the base netlist
     (e.g. a FreePDK45 include that defines PMOS devices), and
     inserting an additional ``.include" that points to the chosen
     model file.
   - Rewriting the MOS device model name in the base netlist
     (by default, the first model name seen in MOS/subckt instances),
     or a user-specified name via ``--from-model-name``.

The script focuses on a single NMOS device family (typical for the
benchmark netlists that only use NMOS explicitly). It does not attempt
to automatically handle PMOS selection or change supply voltages; it
only prints the VDD inferred from the model file so you can adjust
biases manually if desired.
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Set

# Import sibling tools
THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR))

from spice_parser import SPICEParser, SPICEModelExtractor  # type: ignore


@dataclass
class BaseNetlistInfo:
    """Information extracted from the baseline netlist."""

    style: str  # "model", "subckt", or "unknown"
    mos_prefixes: Set[str]
    model_names: List[str]


def analyze_base_netlist(base_netlist: Path) -> BaseNetlistInfo:
    """Parse the base netlist and infer MOS instantiation style.

    We look at device instances and collect:
    - Which leading letters are used (M for MOS, X for subckt, etc.).
    - The distinct model/subckt names attached to those instances.
    """

    parser = SPICEParser()
    ast = parser.parse_file(base_netlist)

    mos_prefixes: Set[str] = set()
    model_names: List[str] = []

    for dev in ast.devices:
        # SPICEParser uses device_type = first character of instance name
        prefix = dev.device_type.upper()
        if prefix in {"M", "X"}:  # focus on MOS/subckt-style devices
            mos_prefixes.add(prefix)
            if dev.model_name and dev.model_name not in model_names:
                model_names.append(dev.model_name)

    if "M" in mos_prefixes:
        style = "model"
    elif "X" in mos_prefixes:
        style = "subckt"
    else:
        style = "unknown"

    return BaseNetlistInfo(style=style, mos_prefixes=mos_prefixes, model_names=model_names)


@dataclass
class ChosenDevice:
    """Represents the chosen NMOS device from the PDK scan."""

    name: str
    style: str  # "model" or "subckt"
    file: Path  # absolute path to the file defining the device
    inferred_vdd: float


def preprocess_hspice_model_for_ngspice(chosen: ChosenDevice) -> ChosenDevice:
    """Create a lightly preprocessed copy of an HSPICE-style model file.

    Many industrial PDK model files use the HSPICE ``.lib`` / ``.endl``
    mechanism for corner selection, which ngspice does not implement.

    To improve compatibility without trying to fully emulate HSPICE,
    this helper creates a sibling file next to ``chosen.file`` where
    all ``.lib`` and ``.endl`` lines are commented out, leaving the
    underlying ``.model`` / ``.subckt`` and ``.param`` statements
    visible to ngspice.

    The processed file lives in the **same directory** as the original
    so that any relative ``.include`` paths continue to work.
    """

    src = chosen.file
    try:
        text = src.read_text(encoding="utf-8")
    except OSError as e:
        raise RuntimeError(f"Failed to read model file for HSPICE preprocessing: {src}: {e}")

    # Fast path: if the file does not contain any .lib/.endl, return as-is
    lowered = text.lower()
    if ".lib" not in lowered and ".endl" not in lowered:
        return chosen

    lines = text.splitlines(keepends=True)
    processed: List[str] = []

    for line in lines:
        stripped = line.lstrip()
        lower = stripped.lower()
        if lower.startswith(".lib") or lower.startswith(".endl"):
            # Comment out HSPICE .lib/.endl directives to avoid
            # "unimplemented dot command '.lib'" errors in ngspice.
            leading_ws = line[: len(line) - len(stripped)]
            if stripped.startswith("*"):
                processed.append(line)
            else:
                processed.append(f"{leading_ws}* {stripped}")
        else:
            processed.append(line)

    # Write a sibling file next to the original so that any relative
    # includes inside the model file remain valid.
    dst = src.with_name(src.name + ".ngspice")
    try:
        dst.write_text("".join(processed), encoding="utf-8")
    except OSError as e:
        raise RuntimeError(f"Failed to write preprocessed HSPICE model file: {dst}: {e}")

    return ChosenDevice(
        name=chosen.name,
        style=chosen.style,
        file=dst,
        inferred_vdd=chosen.inferred_vdd,
    )


def choose_device_from_model_file(model_file: Path, device_name: str) -> ChosenDevice:
    """Select a device defined in a single SPICE model file.

    The caller is responsible for providing the exact model/subckt name.
    We only need to determine whether it is a .model or .subckt so that
    downstream code can decide whether an M->X conversion is required.
    """

    if not model_file.exists():
        raise RuntimeError(f"Model file does not exist: {model_file}")

    parser = SPICEParser()
    ast = parser.parse_file(model_file)
    extractor = SPICEModelExtractor(ast)

    # Try .model first
    model = extractor.get_model_by_name(device_name)
    style = "model"
    if model is None:
        subckt = extractor.get_subcircuit_by_name(device_name)
        if subckt is None:
            raise RuntimeError(
                f"Device '{device_name}' not found as .model or .subckt in {model_file}"
            )
        style = "subckt"

    inferred_vdd = extractor.infer_vdd()

    return ChosenDevice(
        name=device_name,
        style=style,
        file=model_file.resolve(),
        inferred_vdd=inferred_vdd,
    )


def make_include_line(model_file: Path, output_netlist: Path) -> str:
    """Construct a .include line using a path relative to the output netlist.

    The resulting path is quoted to be robust to spaces.
    """

    import os

    rel_str = os.path.relpath(str(model_file), str(output_netlist.parent))
    rel_path = Path(rel_str)
    return f'.include "{rel_path.as_posix()}"'


def transform_netlist(
    base_netlist: Path,
    output_netlist: Path,
    chosen_device: ChosenDevice,
    old_model_name: Optional[str] = None,
) -> None:
    """Rewrite the base netlist with new include and model name.

    - Replaces the first .include/.inc/.lib line with one that points
      to chosen_device.file.
    - If old_model_name is provided, replaces that token in MOS/subckt
      instance lines with chosen_device.name. If not provided, uses the
      first model name discovered in MOS/subckt instances.
    """

    base_text = base_netlist.read_text(encoding="utf-8")
    lines = base_text.splitlines(keepends=True)

    # Analyze base netlist again to determine default old_model_name if needed
    info = analyze_base_netlist(base_netlist)
    if info.style == "unknown":
        raise RuntimeError("Could not detect MOS device style (M/X) in base netlist")

    # Decide which model name to replace
    if old_model_name is None:
        if not info.model_names:
            raise RuntimeError("No device model/subckt names found in base netlist")
        old_model_name = info.model_names[0]

    include_line = make_include_line(chosen_device.file, output_netlist)

    new_lines: List[str] = []
    include_replaced = False

    include_prefixes = (".include", ".inc", ".lib")

    base_style = info.style
    device_style = chosen_device.style

    for line in lines:
        stripped = line.lstrip()
        lower = stripped.lower()

        if not include_replaced and any(lower.startswith(p) for p in include_prefixes):
            # Keep the original include/lib line and insert the new one directly after it.
            # This ensures that any base-netlist models (e.g. PMOS_VTG) remain available
            # while still adding the PDK-specific NMOS model include.
            new_lines.append(line)
            new_lines.append(include_line + "\n")
            include_replaced = True
            continue

        # Only touch non-comment device lines
        if stripped and not stripped.startswith("*"):
            first_char = stripped[0].upper()

            # If the base netlist uses .model-style MOS (M-devices) but the
            # selected PDK NMOS is a subcircuit, convert Mxxx to Xxxx so that
            # ngspice instantiates the subcircuit instead of a MOS model.
            if base_style == "model" and device_style == "subckt" and first_char == "M":
                leading_ws = line[: len(line) - len(line.lstrip())]
                rest = line.lstrip()
                if rest and (rest[0] == "M" or rest[0] == "m"):
                    rest = "X" + rest[1:]
                    line = leading_ws + rest
                    stripped = line.lstrip()
                    first_char = "X"

            # We currently do not support the opposite conversion (X->M)
            if base_style == "subckt" and device_style == "model" and first_char == "X":
                raise RuntimeError(
                    "Base netlist uses subcircuit-style MOS devices (X...), but "
                    "the selected PDK NMOS is a .model device; automatic X->M "
                    "conversion is not implemented."
                )

            if first_char in {"M", "X"}:
                # Replace model/subckt name token using a word boundary regex
                pattern = r"\b" + re.escape(old_model_name) + r"\b"
                line = re.sub(pattern, chosen_device.name, line)

        new_lines.append(line)

    # If there was no include/lib line, inject one after the last .option
    if not include_replaced:
        injected = False
        for idx, line in enumerate(new_lines):
            stripped = line.lstrip().lower()
            if stripped.startswith(".option"):
                new_lines.insert(idx + 1, include_line + "\n")
                injected = True
                break
        if not injected:
            new_lines.insert(0, include_line + "\n")

    output_netlist.parent.mkdir(parents=True, exist_ok=True)
    output_netlist.write_text("".join(new_lines), encoding="utf-8")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate adapted SPICE netlists from a base template and a model file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  # Basic usage: adapt a DC netlist using a single model file
  python generate_spice_netlist.py \
    --base-netlist netlists/dc_circuit.cir \
    --output-netlist netlists/my_dc_auto.cir \
    --model-file path/to/models.inc \
    --from-model-name NMOS_VTG \
    --device-name NMOS_VTG

  # Generate DC/AC/Tran/Noise netlists in one call
  python generate_spice_netlist.py \
    --base-netlist netlists/dc_circuit.cir \
    --output-netlist netlists/mypdk_dc_auto.cir \
    --ac-base-netlist netlists/ac_circuit.cir \
    --ac-output-netlist netlists/mypdk_ac_auto.cir \
    --tran-base-netlist netlists/transient_circuit.cir \
    --tran-output-netlist netlists/mypdk_tran_auto.cir \
    --noise-base-netlist netlists/noise_circuit.cir \
    --noise-output-netlist netlists/mypdk_noise_auto.cir \
    --from-model-name NMOS_VTG \
    --model-file path/to/models.inc \
    --device-name some_nmos_model_name
""",
    )

    parser.add_argument(
        "--base-netlist",
        type=str,
        required=True,
        help="Path to baseline SPICE netlist to adapt (e.g. dc_circuit.cir)",
    )
    parser.add_argument(
        "--output-netlist",
        type=str,
        required=True,
        help="Path to write the adapted netlist",
    )
    parser.add_argument(
        "--from-model-name",
        type=str,
        help=(
            "Model/subckt name used in the base netlist for the MOS device. "
            "If omitted, the first name detected in MOS/subckt instances is used."
        ),
    )
    parser.add_argument(
        "--model-file",
        type=str,
        required=True,
        help=(
            "SPICE model file containing the target .model or .subckt definition "
            "for the MOS device (e.g. models.inc)."
        ),
    )
    parser.add_argument(
        "--device-name",
        type=str,
        required=True,
        help=(
            "Exact .model or .subckt name in --model-file to use for the MOS device."
        ),
    )
    parser.add_argument(
        "--ac-base-netlist",
        type=str,
        help="Optional AC analysis base netlist to adapt using the same PDK device",
    )
    parser.add_argument(
        "--ac-output-netlist",
        type=str,
        help="Output path for the adapted AC analysis netlist (requires --ac-base-netlist)",
    )
    parser.add_argument(
        "--tran-base-netlist",
        type=str,
        help="Optional transient analysis base netlist to adapt using the same PDK device",
    )
    parser.add_argument(
        "--tran-output-netlist",
        type=str,
        help=(
            "Output path for the adapted transient analysis netlist "
            "(requires --tran-base-netlist)"
        ),
    )
    parser.add_argument(
        "--noise-base-netlist",
        type=str,
        help="Optional noise analysis base netlist to adapt using the same PDK device",
    )
    parser.add_argument(
        "--noise-output-netlist",
        type=str,
        help=(
            "Output path for the adapted noise analysis netlist "
            "(requires --noise-base-netlist)"
        ),
    )
    args = parser.parse_args(argv)

    base_netlist = Path(args.base_netlist).resolve()
    output_netlist = Path(args.output_netlist).resolve()
    ac_base: Optional[Path] = None
    ac_output: Optional[Path] = None
    tran_base: Optional[Path] = None
    tran_output: Optional[Path] = None
    noise_base: Optional[Path] = None
    noise_output: Optional[Path] = None
    model_file: Optional[Path] = None
    if args.model_file:
        model_file = Path(args.model_file).resolve()

    if not base_netlist.exists():
        print(f"Error: base netlist does not exist: {base_netlist}")
        return 1
    if model_file is None or not model_file.exists():
        print(f"Error: model file does not exist: {model_file}")
        return 1

    # Validate optional AC/transient/noise netlist pairs
    if args.ac_base_netlist or args.ac_output_netlist:
        if not (args.ac_base_netlist and args.ac_output_netlist):
            print("Error: --ac-base-netlist and --ac-output-netlist must be provided together")
            return 1
        ac_base = Path(args.ac_base_netlist).resolve()
        ac_output = Path(args.ac_output_netlist).resolve()
        if not ac_base.exists():
            print(f"Error: AC base netlist does not exist: {ac_base}")
            return 1

    if args.tran_base_netlist or args.tran_output_netlist:
        if not (args.tran_base_netlist and args.tran_output_netlist):
            print("Error: --tran-base-netlist and --tran-output-netlist must be provided together")
            return 1
        tran_base = Path(args.tran_base_netlist).resolve()
        tran_output = Path(args.tran_output_netlist).resolve()
        if not tran_base.exists():
            print(f"Error: transient base netlist does not exist: {tran_base}")
            return 1

    if args.noise_base_netlist or args.noise_output_netlist:
        if not (args.noise_base_netlist and args.noise_output_netlist):
            print("Error: --noise-base-netlist and --noise-output-netlist must be provided together")
            return 1
        noise_base = Path(args.noise_base_netlist).resolve()
        noise_output = Path(args.noise_output_netlist).resolve()
        if not noise_base.exists():
            print(f"Error: noise base netlist does not exist: {noise_base}")
            return 1

    info = analyze_base_netlist(base_netlist)
    if info.style == "unknown":
        print("Error: could not detect MOS device style (M or X) in base netlist")
        return 1

    print(f"Base netlist: {base_netlist}")
    print(f"  Detected style: {info.style} (prefixes: {', '.join(sorted(info.mos_prefixes))})")
    if info.model_names:
        print(f"  Detected model/subckt names: {', '.join(info.model_names)}")
    else:
        print("  No model/subckt names found in base netlist devices")

    try:
        chosen = choose_device_from_model_file(model_file, args.device_name)
    except Exception as e:
        print(f"Error while selecting device from model file: {e}")
        return 1

    # Automatically apply a light-weight HSPICE compatibility preprocessing
    # step to the selected model file. The helper is a no-op for pure SPICE
    # files (no .lib/.endl), and only creates a sibling *.ngspice file when
    # HSPICE-style library sections are present.
    try:
        chosen = preprocess_hspice_model_for_ngspice(chosen)
    except Exception as e:
        print(
            "Warning: HSPICE compatibility pre-processing failed, "
            f"using original model file: {e}"
        )

    print("\nSelected SPICE device:")
    print(f"  Name : {chosen.name}")
    print(f"  Style: {chosen.style}")
    print(f"  File : {chosen.file}")
    print(f"  Inferred VDD from model file: {chosen.inferred_vdd:.3f} V (not applied automatically)")

    # Adapt the primary base netlist and any optional AC/transient/noise netlists
    netlist_tasks = [("primary", base_netlist, output_netlist)]
    if ac_base and ac_output:
        netlist_tasks.append(("AC", ac_base, ac_output))
    if tran_base and tran_output:
        netlist_tasks.append(("transient", tran_base, tran_output))
    if noise_base and noise_output:
        netlist_tasks.append(("noise", noise_base, noise_output))

    for label, src, dst in netlist_tasks:
        try:
            transform_netlist(
                base_netlist=src,
                output_netlist=dst,
                chosen_device=chosen,
                old_model_name=args.from_model_name,
            )
        except Exception as e:
            print(f"Error while transforming {label} netlist ({src} -> {dst}): {e}")
            return 1
        print(f"\nAdapted {label} netlist written to: {dst}")

    print("You may want to manually review supply voltages and any PMOS devices.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
