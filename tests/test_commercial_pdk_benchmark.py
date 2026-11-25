"""Unit tests for Commercial Foundry PDK Benchmark Engine."""

import pytest
import numpy as np
from pathlib import Path
from spice_model_benchmark.commercial_pdk_benchmark import (
    CommercialPDKBenchmark,
    CommercialPDKSpec,
    CommercialCorner
)


def test_commercial_pdk_spec_initialization():
    bench = CommercialPDKBenchmark()
    assert len(bench.specs) >= 1
    pdk_ids = [s.pdk_id for s in bench.specs]
    assert "Cadence_GPDK045" in pdk_ids
    assert "Synopsys_SAED14" in pdk_ids


def test_extract_dc_metrics():
    bench = CommercialPDKBenchmark()
    vg = np.linspace(0.0, 1.0, 101)
    # MOSFET model with subthreshold + velocity saturation
    vov = np.maximum(0.0, vg - 0.3)
    id_arr = np.where(vg > 0.3, 1e-3 * vov**2 / (1.0 + 2.0 * vov), 1e-12)

    metrics = bench._extract_dc_metrics(vg, id_arr, vdd=1.0, runtime=0.05)
    assert metrics["status"] == "PASS"
    assert metrics["ion_mA"] > 0.0
    assert 0.20 <= metrics["vth_V"] <= 0.60
    assert metrics["peak_gm_mS"] > 0.0


def test_extract_vtc_metrics():
    bench = CommercialPDKBenchmark()
    vin = np.linspace(0.0, 1.0, 201)
    # Smooth inverter VTC model
    vout = 0.5 * (1.0 - np.tanh((vin - 0.5) / 0.08))

    vtc = bench._extract_vtc_metrics(vin, vout, vdd=1.0)
    assert vtc["status"] == "PASS"
    assert vtc["vm_V"] == pytest.approx(0.5, abs=0.02)
    assert vtc["max_gain"] > 5.0
    assert vtc["nml_V"] > 0.1
    assert vtc["nmh_V"] > 0.1
