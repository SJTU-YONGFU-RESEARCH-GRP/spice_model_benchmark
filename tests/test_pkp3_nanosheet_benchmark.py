import pytest
import numpy as np
from pathlib import Path
from spice_model_benchmark.pkp3_nanosheet_benchmark import PKP3NanosheetBenchmark


def test_pkp3_nanosheet_benchmark_init(tmp_path):
    """Verify PKP3 benchmark directory creation."""
    bench = PKP3NanosheetBenchmark(output_dir=str(tmp_path / "pkp3_test"))
    assert bench.output_dir.exists()
    assert bench.work_dir.exists()
    assert bench.plots_dir.exists()


def test_pkp3_crossing_detection():
    """Verify interpolation of 50% voltage crossing for delay extraction."""
    bench = PKP3NanosheetBenchmark(output_dir="results/test_pkp3_crossing")

    # Synthetic waveform rising from 0 to 1V
    t = np.array([0.0, 10e-12, 20e-12, 30e-12])
    v_rise = np.array([0.0, 0.25, 0.75, 1.0])

    t_cross = bench._find_crossing(t, v_rise, target=0.5, rising=True)
    assert t_cross == pytest.approx(15e-12, abs=1e-13)

    # Falling waveform
    v_fall = np.array([1.0, 0.75, 0.25, 0.0])
    t_cross_f = bench._find_crossing(t, v_fall, target=0.5, rising=False)
    assert t_cross_f == pytest.approx(15e-12, abs=1e-13)
