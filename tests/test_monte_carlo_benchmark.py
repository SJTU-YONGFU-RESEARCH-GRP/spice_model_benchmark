"""Unit tests for Statistical Monte Carlo Mismatch Benchmark Engine."""

import pytest
import numpy as np
from pathlib import Path
from spice_model_benchmark.monte_carlo_benchmark import (
    MonteCarloBenchmark,
    compute_distribution_stats,
    DistributionStats
)


def test_compute_distribution_stats():
    # Gaussian distribution with mean 10.0 and std 2.0
    np.random.seed(42)
    samples = np.random.normal(10.0, 2.0, 5000)

    stats = compute_distribution_stats(samples)
    assert stats.mean == pytest.approx(10.0, abs=0.1)
    assert stats.std == pytest.approx(2.0, abs=0.1)
    assert stats.cv_pct == pytest.approx(20.0, abs=1.0)
    assert abs(stats.skewness) < 0.15
    assert stats.sigma_minus_3 == pytest.approx(stats.mean - 3.0 * stats.std)
    assert stats.sigma_plus_3 == pytest.approx(stats.mean + 3.0 * stats.std)


def test_snm_butterfly_calculation():
    bench = MonteCarloBenchmark(output_dir="/tmp/test_mc")
    grid = np.linspace(0.0, 1.0, 201)
    # Complementary inverter curves
    v_out1 = 0.5 * (1.0 - np.tanh((grid - 0.5) / 0.08))
    v_out2 = 0.5 * (1.0 - np.tanh((grid - 0.5) / 0.08))

    snm = bench._compute_snm(grid, v_out1, grid, v_out2)
    assert 0.20 <= snm <= 0.45


def test_monte_carlo_initialization():
    bench = MonteCarloBenchmark(output_dir="/tmp/test_mc", num_runs=20)
    assert bench.num_runs == 20
    assert bench.output_dir == Path("/tmp/test_mc").resolve()
