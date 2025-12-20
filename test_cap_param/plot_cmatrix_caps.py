#!/usr/bin/env python3
"""Plot C-V curves for each entry in the 4x4 small-signal capacitance matrix.

Reads:
  <input-dir>/data/cmatrix_data.txt

Writes (default):
  <input-dir>/plots/cmatrix_caps/<cap>.png

Examples:
    python test_cap_param/plot_cmatrix_caps.py
    python test_cap_param/plot_cmatrix_caps.py --cap cgg cgs
    python test_cap_param/plot_cmatrix_caps.py --input-dir results_ac_cmatrix
    python test_cap_param/plot_cmatrix_caps.py --input-dir results_ac_cmatrix --cap cgg cgs
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


_ALL_CAPS = [
    "cgg",
    "cgd",
    "cgs",
    "cgb",
    "cdg",
    "cdd",
    "cds",
    "cdb",
    "csg",
    "csd",
    "css",
    "csb",
    "cbg",
    "cbd",
    "cbs",
    "cbb",
]


def _repo_root() -> Path:
    # test_cap_param/<this_file>.py -> repo root is one level up
    return Path(__file__).resolve().parents[1]


def _resolve_dir_arg(path_arg: str, *, base_dir: Path) -> Path:
    """Resolve a directory arg, trying CWD first then repo-root relative."""
    p = Path(path_arg)
    if p.is_absolute():
        return p
    p_cwd = p
    if p_cwd.exists():
        return p_cwd
    p_base = base_dir / p
    return p_base


def _normalize_caps(caps: list[str] | None) -> list[str]:
    if not caps:
        return list(_ALL_CAPS)

    normalized: list[str] = []
    for cap in caps:
        c = cap.strip().lower()
        if not c:
            continue
        if not c.startswith("c"):
            c = "c" + c
        normalized.append(c)

    unknown = sorted(set(normalized) - set(_ALL_CAPS))
    if unknown:
        raise SystemExit(
            "Unknown --cap entries: "
            + ", ".join(unknown)
            + "\nValid caps: "
            + " ".join(_ALL_CAPS)
        )

    # de-dupe while preserving order
    seen: set[str] = set()
    ordered: list[str] = []
    for c in normalized:
        if c not in seen:
            seen.add(c)
            ordered.append(c)
    return ordered


def _load_cmatrix_table(input_dir: Path) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    cmatrix_path = input_dir / "data" / "cmatrix_data.txt"
    if not cmatrix_path.exists():
        raise SystemExit(f"cmatrix_data.txt not found: {cmatrix_path}")

    with cmatrix_path.open("r", encoding="utf-8") as f:
        header = f.readline().strip().split()

    raw = np.genfromtxt(cmatrix_path, skip_header=1)
    if raw.size == 0:
        raise SystemExit(f"cmatrix_data.txt has no data rows: {cmatrix_path}")
    if raw.ndim == 1:
        raw = raw[None, :]

    col = {name.lower(): i for i, name in enumerate(header)}
    if "vg" not in col:
        raise SystemExit(f"Missing Vg column in header: {header}")

    vg = raw[:, col["vg"]]

    caps: dict[str, np.ndarray] = {}
    for cap in _ALL_CAPS:
        key = cap.lower()
        if key in col:
            caps[cap] = raw[:, col[key]]
            continue

        # Fallbacks for unusual header casing
        key2 = (cap[0].upper() + cap[1:]).lower()
        if key2 in col:
            caps[cap] = raw[:, col[key2]]
            continue

        key3 = cap.upper().lower()
        if key3 in col:
            caps[cap] = raw[:, col[key3]]
            continue

            raise SystemExit(
                f"Missing column '{cap}' in {cmatrix_path}. Header: {header}"
            )

    return vg, caps


def _plot_one(
    vg: np.ndarray,
    c_f: np.ndarray,
    cap: str,
    out_path: Path,
    y_unit: str,
) -> None:
    if y_unit == "F":
        y = c_f
        y_label = "Capacitance (F)"
    elif y_unit == "fF":
        y = c_f * 1e15
        y_label = "Capacitance (fF)"
    else:
        raise SystemExit(f"Unsupported --y-unit: {y_unit}")

    plt.figure(figsize=(7.2, 4.8))
    plt.plot(vg, y, linewidth=1.6)
    plt.xlabel("Vg (V)")
    plt.ylabel(y_label)
    plt.title(f"{cap.upper()} vs Vg")
    plt.grid(True, alpha=0.25)
    plt.tight_layout()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.close()


def main() -> int:
    repo_root = _repo_root()
    default_input_dir = repo_root / "results_ac_cmatrix"

    parser = argparse.ArgumentParser(
        description="Plot C-V curves for each entry of the 4x4 capacitance matrix (from cmatrix_data.txt)."
    )
    parser.add_argument(
        "--input-dir",
        default=str(default_input_dir),
        help=(
            "Simulation output directory containing data/cmatrix_data.txt. "
            "If relative, it is resolved against the current directory first, then the repo root. "
            f"(default: {default_input_dir})"
        ),
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help=(
            "Directory to save plots. If relative, it is resolved against the current directory first, "
            "then the repo root. (default: <input-dir>/plots/cmatrix_caps)"
        ),
    )
    parser.add_argument(
        "--cap",
        nargs="*",
        default=None,
        help=(
            "Capacitance entries to plot (default: all). Example: --cap cgg cgs. "
            "Valid: " + " ".join(_ALL_CAPS)
        ),
    )
    parser.add_argument(
        "--y-unit",
        choices=["fF", "F"],
        default="fF",
        help="Y-axis unit (default: fF)",
    )

    args = parser.parse_args()

    input_dir = _resolve_dir_arg(args.input_dir, base_dir=repo_root)
    if not input_dir.exists():
        raise SystemExit(f"input-dir not found: {input_dir}")

    caps_to_plot = _normalize_caps(args.cap)

    if args.out_dir:
        out_dir = _resolve_dir_arg(args.out_dir, base_dir=repo_root)
    else:
        out_dir = input_dir / "plots" / "cmatrix_caps"

    vg, caps = _load_cmatrix_table(input_dir)

    for cap in caps_to_plot:
        out_path = out_dir / f"{cap}.png"
        _plot_one(vg, caps[cap], cap, out_path, args.y_unit)

    print(f"Generated {len(caps_to_plot)} plot(s) in: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
