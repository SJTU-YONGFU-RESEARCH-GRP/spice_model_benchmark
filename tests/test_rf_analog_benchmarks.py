import pytest
import numpy as np
from pathlib import Path
from spice_model_benchmark.rf_analog_benchmarks import (
    calculate_derivatives,
    audit_derivative_smoothness,
    evaluate_rf_analog_linearity,
    plot_rf_analog_derivatives,
    RFAnalogMetrics
)


def test_calculate_derivatives_polynomial():
    """Verify gm, gm2, gm3 on polynomial id(v) = a*v + b*v^2 + c*v^3."""
    vg = np.linspace(0.0, 1.0, 201)
    a, b, c = 2.0, 3.0, 4.0
    id_arr = a * vg + b * (vg ** 2) + c * (vg ** 3)

    gm, gm2, gm3 = calculate_derivatives(vg, id_arr)

    # Expected values
    expected_gm = a + 2 * b * vg + 3 * c * (vg ** 2)
    expected_gm2 = 2 * b + 6 * c * vg
    expected_gm3 = 6 * c * np.ones_like(vg)

    # Interior points check (ignoring boundary edge effects of finite difference)
    interior = slice(5, -5)
    assert np.allclose(gm[interior], expected_gm[interior], rtol=1e-2)
    assert np.allclose(gm2[interior], expected_gm2[interior], rtol=1e-2)
    assert np.allclose(gm3[interior], expected_gm3[interior], rtol=5e-2)


def test_linearity_distortion_metrics():
    """Verify HD2, HD3, IIP3 metrics on known polynomial at interior bias point."""
    vg = np.linspace(-0.5, 0.5, 201)
    # id = 10mA/V * v + 2mA/V^2 * v^2 + 0.5mA/V^3 * v^3
    a1 = 0.010
    a2 = 0.002
    a3 = 0.0005
    id_arr = a1 * vg + a2 * (vg ** 2) + a3 * (vg ** 3)

    # At vg = 0 (interior point), gm = a1, gm2 = 2*a2, gm3 = 6*a3
    metrics = evaluate_rf_analog_linearity(vg, id_arr, vbias=0.0, vin_amp=0.05)

    assert isinstance(metrics, RFAnalogMetrics)
    assert metrics.rf_qa_passed is True
    assert metrics.vbias_V == pytest.approx(0.0, abs=1e-3)
    assert metrics.gm_at_bias_mS == pytest.approx(10.0, rel=0.05)

    # HD2 = 0.5 * (a2 / a1) * Vin = 0.5 * (0.002 / 0.010) * 0.05 = 0.005 (0.5%)
    assert metrics.hd2_pct == pytest.approx(0.5, rel=0.1)


def test_audit_derivative_smoothness_ripples():
    """Verify ripple detection on smooth vs noisy curves."""
    vg = np.linspace(0.0, 1.0, 100)
    smooth_gm2 = 5.0 - 2.0 * vg
    smooth_gm3 = -2.0 * np.ones_like(vg)

    r2, r3, roughness = audit_derivative_smoothness(vg, smooth_gm2, smooth_gm3)
    assert r2 == 0
    assert r3 == 0

    # Curve with intentional oscillations
    noisy_gm2 = np.sin(20 * np.pi * vg)
    noisy_gm3 = np.cos(20 * np.pi * vg)
    r2_n, r3_n, _ = audit_derivative_smoothness(vg, noisy_gm2, noisy_gm3)
    assert r2_n > 5
    assert r3_n > 5


def test_plot_rf_analog_derivatives(tmp_path):
    """Verify dev-plot derivative figure generation (SVG and PNG)."""
    vg = np.linspace(0.0, 1.0, 101)
    id_arr = 1e-3 * (vg ** 2)
    gm, gm2, gm3 = calculate_derivatives(vg, id_arr)

    out_file = tmp_path / "rf_deriv_test"
    png_path, svg_path = plot_rf_analog_derivatives(
        vg, id_arr, gm, gm2, gm3, "Test Device", out_file, vbias=0.5
    )

    assert png_path.exists() and png_path.stat().st_size > 1000
    assert svg_path.exists() and svg_path.stat().st_size > 1000
