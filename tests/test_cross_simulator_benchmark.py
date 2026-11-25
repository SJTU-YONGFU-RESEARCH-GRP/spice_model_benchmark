import pytest
import numpy as np
from pathlib import Path
from spice_model_benchmark.cross_simulator_benchmark import CrossSimulatorBenchmark


def test_cross_simulator_nrmsd_and_r2():
    """Verify NRMSD and R^2 mathematical formulas on synthetic curves."""
    cs = CrossSimulatorBenchmark(output_dir="results/test_cross_sim")

    # Generate synthetic reference and test curves
    vg = np.linspace(0, 1.0, 101)
    ref_id = 1e-3 * (vg ** 2)

    # 1. Identical curve -> NRMSD = 0%, R^2 = 1.0
    synth_results = {
        "ngspice": {
            "elapsed_s": 0.1,
            "metrics": {"ion_mA": 1.0, "vth_V": 0.3, "peak_gm_mS_per_mm": 2.0},
            "curves": {"vg": vg.tolist(), "id_tr": ref_id.tolist()}
        },
        "spectre": {
            "elapsed_s": 0.2,
            "metrics": {"ion_mA": 1.0, "vth_V": 0.3, "peak_gm_mS_per_mm": 2.0},
            "curves": {"vg": vg.tolist(), "id_tr": ref_id.tolist()}
        }
    }

    corr = cs._compute_correlation(synth_results, ref_sim="ngspice")
    assert corr["spectre"]["nrmsd_pct"] == pytest.approx(0.0, abs=1e-5)
    assert corr["spectre"]["r_squared"] == pytest.approx(1.0, abs=1e-5)
    assert corr["spectre"]["delta_ion_pct"] == pytest.approx(0.0, abs=1e-5)

    # 2. 1% scaled curve -> NRMSD ~ 1%
    synth_results["hspice"] = {
        "elapsed_s": 0.15,
        "metrics": {"ion_mA": 1.01, "vth_V": 0.3, "peak_gm_mS_per_mm": 2.02},
        "curves": {"vg": vg.tolist(), "id_tr": (ref_id * 1.01).tolist()}
    }
    corr2 = cs._compute_correlation(synth_results, ref_sim="ngspice")
    assert corr2["hspice"]["delta_ion_pct"] == pytest.approx(1.0, abs=0.01)
    assert corr2["hspice"]["r_squared"] == pytest.approx(1.0, abs=1e-4)


def test_cross_simulator_initialization(tmp_path):
    """Verify CrossSimulatorBenchmark initializes directories correctly."""
    cs = CrossSimulatorBenchmark(output_dir=str(tmp_path / "cross_sim_run"))
    assert cs.output_dir.exists()
    assert cs.plots_dir.exists()
