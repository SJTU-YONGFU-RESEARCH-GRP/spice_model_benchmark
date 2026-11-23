"""Reusable matplotlib style constants (canonical dev-plot skill implementation).

Provides consistent matplotlib style for repository benchmark figures:
- MATLAB-aligned blue/red/purple palette
- Bold typography (sans-serif, bold axes labels/titles)
- Thick lines (4.0 main, 3.0 secondary)
- Full visible spines with 2.0 width
- Dual export (SVG vector + high-res PNG for markdown preview)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Union, Optional, Tuple, List
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIGSIZE = (11, 5)
FIGSIZE_SQUARE = (8, 8)
FIGSIZE_TALL = (11, 7.5)

BAR_COLOR = "#0033cc"  # MATLAB [0 0.2 1]
BAR_EDGE_COLOR = "#002080"
BAR_EDGE_WIDTH = 1.0

PRIMARY_BLUE = "#0033cc"
SECONDARY_RED = "#cc0000"
ACCENT_PURPLE = "#7f3fbf"
TWIN_ORANGE = "#e67300"
HIGHLIGHT_GREEN = "#006400"
MUTED_GRAY = "#666666"

LINE_COLORS = {
    "primary": PRIMARY_BLUE,
    "secondary": SECONDARY_RED,
    "accent": ACCENT_PURPLE,
    "orange": TWIN_ORANGE,
    "green": HIGHLIGHT_GREEN,
    "gray": MUTED_GRAY,
    # SPICE-specific semantic keys
    "id": PRIMARY_BLUE,
    "gm": SECONDARY_RED,
    "gst": PRIMARY_BLUE,
    "gst_deriv": SECONDARY_RED,
    "vin": MUTED_GRAY,
    "vout": PRIMARY_BLUE,
    "gain": SECONDARY_RED,
    "stage1": PRIMARY_BLUE,
    "stage2": SECONDARY_RED,
    "stage3": ACCENT_PURPLE,
    "hold_snm": PRIMARY_BLUE,
    "read_snm": SECONDARY_RED,
    "bode_mag": PRIMARY_BLUE,
    "bode_phase": SECONDARY_RED,
}

MULTI_SERIES_COLORS = (
    "#0033cc",  # Blue
    "#cc0000",  # Red
    "#7f3fbf",  # Purple
    "#e67300",  # Orange
    "#006400",  # Dark Green
    "#008080",  # Teal
    "#8b0000",  # Dark Red
    "#4b0082",  # Indigo
    "#b8860b",  # Dark Goldenrod
    "#2f4f4f",  # Dark Slate Gray
)

LINEWIDTH_MAIN = 4.0
LINEWIDTH_SECONDARY = 3.0
LINEWIDTH_BAR_EDGE = 1.0

GRID_ALPHA = 0.35
GRID_LINEWIDTH = 1.1

TITLE_SIZE = 17
LABEL_SIZE = 13
TICK_SIZE = 10
LEGEND_SIZE = 10

SPINE_WIDTH = 2.0


def apply_rcparams() -> None:
    """Set global typography once per process per dev-plot specification."""
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["axes.titlesize"] = TITLE_SIZE
    plt.rcParams["axes.labelsize"] = LABEL_SIZE
    plt.rcParams["xtick.labelsize"] = TICK_SIZE
    plt.rcParams["ytick.labelsize"] = TICK_SIZE
    plt.rcParams["legend.fontsize"] = LEGEND_SIZE
    plt.rcParams["figure.titlesize"] = TITLE_SIZE
    plt.rcParams["axes.linewidth"] = SPINE_WIDTH
    plt.rcParams["grid.alpha"] = GRID_ALPHA
    plt.rcParams["grid.linewidth"] = GRID_LINEWIDTH
    plt.rcParams["lines.linewidth"] = LINEWIDTH_SECONDARY


def apply_style(ax: plt.Axes, *, grid_axis: Optional[str] = None) -> None:
    """Apply consistent dev-plot axis styling to an axes object."""
    if grid_axis is None:
        ax.grid(alpha=GRID_ALPHA, linewidth=GRID_LINEWIDTH)
    else:
        ax.grid(axis=grid_axis, alpha=GRID_ALPHA, linewidth=GRID_LINEWIDTH)

    ax.tick_params(axis="both", labelsize=TICK_SIZE, width=1.5, length=4)
    for spine in ax.spines.values():
        spine.set_linewidth(SPINE_WIDTH)
    ax.spines["top"].set_visible(True)
    ax.spines["right"].set_visible(True)


def save_dev_figure(fig: plt.Figure, output_path: Union[str, Path], dpi: int = 300) -> Tuple[Path, Path]:
    """Save figure conforming to dev-plot (saves both SVG vector and high-res PNG).

    Returns:
        (png_path, svg_path)
    """
    p = Path(output_path).resolve()
    p.parent.mkdir(parents=True, exist_ok=True)

    png_path = p.with_suffix(".png")
    svg_path = p.with_suffix(".svg")

    fig.tight_layout()
    fig.savefig(svg_path, format="svg")
    fig.savefig(png_path, format="png", dpi=dpi)
    plt.close(fig)
    return png_path, svg_path


def downsample_stride(length: int, *, combined: bool = False) -> int:
    """Stride for long series before plotting."""
    divisor = 256 if combined else 512
    return max(length // divisor, 1)
