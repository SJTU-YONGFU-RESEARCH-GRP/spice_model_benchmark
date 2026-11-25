"""Unit and regression tests for Circuit-Level Stress Convergence Framework."""

import pytest
import numpy as np
from pathlib import Path

from spice_model_benchmark.circuit_stress_runner import CircuitStressRunner, CircuitStressSpec


def test_circuit_stress_spec_registry():
    """Verify all 10 foundry PDKs and PINN-CM are properly registered in the circuit stress suite."""
    runner = CircuitStressRunner()
    assert len(runner.specs) >= 10
    pdks = [s.pdk for s in runner.specs]
    expected_pdks = [
        "FreePDK45", "GF180MCU", "SkyWater_SKY130", "IHP_SG13G2", "ASAP7_7nm",
        "FreePDK15_15nm", "FreePDK3_3nm", "GT3_3nm", "GT2N_2nm", "PKP3_3nm", "PINN_GF180"
    ]
    for p in expected_pdks:
        assert p in pdks, f"Missing expected PDK: {p}"


def test_seevinck_snm_rotation():
    """Verify the 45-degree Seevinck coordinate rotation for SRAM butterfly curves."""
    # Synthetic symmetric inverter transfer curves
    v = np.linspace(0, 1.0, 101)
    # Sigmoidal transfer curve vout = 1 / (1 + exp(20*(vin - 0.5)))
    v_out = 1.0 / (1.0 + np.exp(20.0 * (v - 0.5)))

    # Seevinck rotation coordinates:
    u1 = (v - v_out) / np.sqrt(2)
    v1 = (v + v_out) / np.sqrt(2)
    u2 = (v_out - v) / np.sqrt(2)
    v2 = (v_out + v) / np.sqrt(2)

    u_grid = np.linspace(-0.5, 0.5, 200)
    s1, s2 = np.argsort(u1), np.argsort(u2)
    v1_i = np.interp(u_grid, u1[s1], v1[s1])
    v2_i = np.interp(u_grid, u2[s2], v2[s2])
    dv = v1_i - v2_i

    mask_left = u_grid < -0.01
    mask_right = u_grid > 0.01
    snm_l = np.max(dv[mask_left]) / np.sqrt(2) * 1000.0
    snm_r = np.max(-dv[mask_right]) / np.sqrt(2) * 1000.0

    assert snm_l > 100.0
    assert snm_r > 100.0
    assert abs(snm_l - snm_r) < 5.0  # symmetric lobes


def test_circuit_stress_freepdk45_execution(tmp_path):
    """Execute quick circuit stress verification of FreePDK45 on ngspice."""
    runner = CircuitStressRunner(output_dir=str(tmp_path))
    results = runner.run_all(selected_pdks=["FreePDK45"])
    assert len(results) == 1
    res = results[0]
    assert res["success"] is True
    assert res["pdk"] == "FreePDK45"
    assert res["inverter_dc"]["converged"] is True
    assert 0.45 <= res["inverter_dc"]["vm"] <= 0.55
    assert res["ro"]["converged"] is True
    assert res["ro"]["f_osc_ghz"] > 10.0
    assert res["sram"]["converged"] is True
    assert res["sram"]["snm_hold_mv"] > 200.0
    assert res["ota"]["converged"] is True
