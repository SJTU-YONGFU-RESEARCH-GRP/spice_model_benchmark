"""
Benchmark → Reduction bridge.

After benchmarking a model, optionally trigger model reduction.
The benchmark baseline can inform the reduction error tolerance.
"""

import argparse
from pathlib import Path


def run(context: dict, args: list[str]) -> dict:
    """B→R: trigger reduction after benchmark.

    context keys:
        model_file:   Path to the model file
        output_dir:   Directory where benchmark results were written

    args (from --bridge "reduce --error-tolerance 0.05 --min-params 10"):
        --error-tolerance   Target error tolerance (default: 0.05)
        --min-params        Minimum parameter count (default: 10)
        --max-iter          Maximum optimization iterations (default: 100)
        --opt-method        Optimization method (default: genetic)
        --red-method        Reduction method (default: sensitivity)
    """
    parser = argparse.ArgumentParser(prog="bridge-reduce")
    parser.add_argument("--error-tolerance", type=float, default=0.05)
    parser.add_argument("--min-params", type=int, default=10)
    parser.add_argument("--max-iter", type=int, default=100)
    parser.add_argument("--opt-method", type=str, default="genetic")
    parser.add_argument("--red-method", type=str, default="sensitivity")
    parsed = parser.parse_args(args)

    from ._common import import_module

    bmr_mod = import_module("spice_model_reduction", "bmr.core.config")
    reducer_mod = import_module("spice_model_reduction", "bmr.core.reducer")
    if bmr_mod is None or reducer_mod is None:
        print("[bridge:reduce] spice_model_reduction not found — skipping")
        return {"ok": False, "reason": "reduction not found"}

    model_file = Path(context["model_file"])
    output_dir = Path(context.get("output_dir", ".")) / "reduced"
    output_dir.mkdir(parents=True, exist_ok=True)

    config = bmr_mod.ReductionConfig(
        original_model_path=model_file,
        target_circuit_path=Path("dummy.sp"),
        output_dir=output_dir,
        analyses=[],
        analysis_config=bmr_mod.AnalysisConfig(
            mosfet_test=bmr_mod.MOSFETTestConfig(
                test_type=bmr_mod.TestType.DC_IV,
                device_type="nmos",
            )
        ),
        target_error_tolerance=parsed.error_tolerance,
        min_parameters=parsed.min_params,
        max_parameters=None,
        use_iterative_reduction=True,
        reduction_stages=3,
        initial_reduction_ratio=0.8,
        sensitivity_threshold=0.01,
        optimization_config=bmr_mod.OptimizationConfig(
            method=bmr_mod.OptimizationMethod(parsed.opt_method),
            max_iterations=parsed.max_iter,
        ),
        reduction_method=bmr_mod.ReductionMethod(parsed.red_method),
    )

    reducer = reducer_mod.BSIMReducer(config)
    results = reducer.reduce_model()
    print(f"[bridge:reduce] Reduction complete — "
          f"{results['performance_metrics']['reduced_parameters']} params "
          f"({results['performance_metrics']['reduction_ratio']:.1%})")
    return {"ok": True, "output_dir": str(output_dir), "metrics": results.get("performance_metrics", {})}
