"""Tests for dev-plot styling module and dual SVG/PNG export."""

from pathlib import Path
import tempfile
import matplotlib.pyplot as plt
import numpy as np

from spice_model_benchmark.plot_style import (
    apply_rcparams,
    apply_style,
    save_dev_figure,
    PRIMARY_BLUE,
    SECONDARY_RED,
    SPINE_WIDTH,
    GRID_ALPHA,
)
from spice_model_benchmark.plot_generator import PlotGenerator


def test_dev_plot_rcparams():
    """Verify rcParams follow dev-plot specifications."""
    apply_rcparams()
    assert plt.rcParams["font.weight"] == "bold"
    assert plt.rcParams["axes.labelweight"] == "bold"
    assert plt.rcParams["axes.titleweight"] == "bold"
    assert plt.rcParams["axes.linewidth"] == SPINE_WIDTH


def test_dev_plot_axes_styling_and_export():
    """Verify apply_style sets full spines and save_dev_figure creates both SVG and PNG."""
    apply_rcparams()
    fig, ax = plt.subplots(figsize=(11, 5))
    x = np.linspace(0, 1, 50)
    ax.plot(x, x**2, color=PRIMARY_BLUE, label="Quadratic")
    apply_style(ax)

    # Check spines
    assert ax.spines["top"].get_visible() is True
    assert ax.spines["right"].get_visible() is True
    assert ax.spines["left"].get_linewidth() == SPINE_WIDTH
    assert ax.spines["bottom"].get_linewidth() == SPINE_WIDTH

    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test_figure.png"
        png_p, svg_p = save_dev_figure(fig, test_file)

        assert png_p.exists()
        assert svg_p.exists()
        assert png_p.suffix == ".png"
        assert svg_p.suffix == ".svg"
        assert png_p.stat().st_size > 0
        assert svg_p.stat().st_size > 0


def test_plot_generator_dev_plot_integration():
    """Verify PlotGenerator uses dev-plot palette and exports both SVG and PNG."""
    with tempfile.TemporaryDirectory() as tmpdir:
        pg = PlotGenerator(tmpdir, dpi=150)
        assert pg.colors["blue"] == PRIMARY_BLUE
        assert pg.colors["red"] == SECONDARY_RED

        vds = np.array([0.0, 0.5, 1.0])
        vgs = np.array([1.0, 1.0, 1.0])
        ids = np.array([0.0, 1e-3, 2e-3])

        out_png = pg.plot_dc_iv_characteristics(tmpdir, vds, vgs, ids)
        out_svg = Path(out_png).with_suffix(".svg")

        assert Path(out_png).exists()
        assert out_svg.exists()
