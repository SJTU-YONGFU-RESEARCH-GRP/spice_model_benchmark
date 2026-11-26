"""
Command-line interface for SPICE Model Benchmark System.

Supports running multiple simulators simultaneously and comparing results.
"""
import argparse
import shlex
import sys
import time
from pathlib import Path
from typing import List, Optional, Dict


def main(args: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="SPICE Model Benchmark System - Comprehensive MOSFET verification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with ngspice (default)
  spice-benchmark model.inc

  # Run with Spectre
  spice-benchmark model.inc --simulator spectre

  # Run both simulators and compare
  spice-benchmark model.inc --simulator ngspice spectre

  # Compare only DC mode
  spice-benchmark model.inc --simulator ngspice spectre --modes dc
        """
    )

    parser.add_argument(
        "model_file",
        type=str,
        nargs="?",
        default=None,
        help="Path to the SPICE model file (optional when using --circuit-stress or --regression)"
    )

    parser.add_argument(
        "--circuit-stress",
        action="store_true",
        help="Run IEEE TCAD 2026 / IEEE TED 2025 circuit-level stress convergence suite (Inverter, RO, 6T-SRAM, 5T OTA)"
    )

    parser.add_argument(
        "--regression",
        action="store_true",
        help="Run multi-corner regression suite across all 10 foundry PDKs"
    )

    parser.add_argument(
        "--cross-sim",
        action="store_true",
        help="Run multi-EDA cross-simulator correlation benchmark (ngspice vs Xyce vs HSPICE vs Spectre)"
    )

    parser.add_argument(
        "--pkp3",
        action="store_true",
        help="Run in-depth PKP3 3nm GAAFET (PHIMO-Fusion) characterization: geometry scaling & CMOS inverter"
    )

    parser.add_argument(
        "--commercial",
        action="store_true",
        help="Run commercial foundry PDK benchmark suite (Cadence GPDK45, Synopsys SAED14/32, SMIC 180, TSMC 16)"
    )

    parser.add_argument(
        "--monte-carlo",
        action="store_true",
        help="Run statistical variation & Monte Carlo mismatch benchmark (Pelgrom spread, Inverter, 6T-SRAM SNM)"
    )

    parser.add_argument(
        "--mc-runs",
        type=int,
        default=50,
        help="Number of Monte Carlo iterations for statistical analysis (default: 50)"
    )

    parser.add_argument(
        "--va-lint",
        type=str,
        nargs="*",
        help="Run Verilog-A physical & LRM quality linter on specified .va files or default models"
    )

    parser.add_argument(
        "--va-compile",
        type=str,
        nargs="+",
        help="Compile specified Verilog-A (.va) file(s) to OSDI shared library via OpenVAF"
    )

    parser.add_argument(
        "--pdk",
        type=str,
        nargs="+",
        help="Specific PDKs or corners to evaluate under --circuit-stress or --regression (default: all)"
    )

    parser.add_argument(
        "--simulator",
        type=str,
        nargs="+",
        choices=["ngspice", "spectre", "hspice", "xyce"],
        default=["ngspice"],
        help="Simulators to run - supports multiple for comparison (default: ngspice)"
    )

    parser.add_argument(
        "--modes",
        type=str,
        nargs="+",
        choices=["dc", "transient", "ac", "noise"],
        default=["dc", "transient", "ac", "noise"],
        help="Analysis modes to run (default: all modes)"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="spice_benchmark_results",
        help="Output directory for results (default: spice_benchmark_results)"
    )

    parser.add_argument(
        "-j", "--jobs",
        type=int,
        default=4,
        help="Number of concurrent worker threads for multi-PDK benchmarking (default: 4)"
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Resolution for generated plots (default: 300)"
    )

    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)"
    )

    parser.add_argument(
        "--dc-circuit",
        type=str,
        help="Path to custom DC analysis circuit file"
    )

    parser.add_argument(
        "--transient-circuit",
        type=str,
        help="Path to custom transient analysis circuit file"
    )

    parser.add_argument(
        "--noise-circuit",
        type=str,
        help="Path to custom noise analysis circuit file"
    )

    parser.add_argument(
        "--ac-circuit",
        type=str,
        help="Path to custom AC analysis circuit file"
    )

    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="Specific device model/subcircuit name to evaluate from the SPICE model file (default: primary device)"
    )

    parser.add_argument(
        "--all-devices",
        action="store_true",
        help="Evaluate all discovered devices in the SPICE model file sequentially"
    )

    parser.add_argument(
        "--bridge",
        action="append",
        default=[],
        metavar='"TOOL [ARGS...]"',
        help="Chain to downstream tool after benchmark"
    )

    if args is None:
        args = sys.argv[1:]

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit as e:
        return e.code

    # 1. Circuit Stress Mode
    if parsed_args.circuit_stress:
        from .circuit_stress_runner import CircuitStressRunner
        out_dir = parsed_args.output_dir if parsed_args.output_dir != "spice_benchmark_results" else "results/circuit_stress"
        user_specified_sim = any(a.startswith("--sim") for a in args) if args else False
        sim = parsed_args.simulator[0] if user_specified_sim else "auto"
        runner = CircuitStressRunner(output_dir=out_dir)
        results = runner.run_all(selected_pdks=parsed_args.pdk, simulator=sim, max_workers=parsed_args.jobs)
        return 0 if any(r.get("success") for r in results) else 1

    # 2. Multi-Corner Regression Mode
    if parsed_args.regression:
        from .regression_runner import RegressionRunner
        out_dir = parsed_args.output_dir if parsed_args.output_dir != "spice_benchmark_results" else "results"
        user_specified_sim = any(a.startswith("--sim") for a in args) if args else False
        sim = parsed_args.simulator[0] if user_specified_sim else "auto"
        runner = RegressionRunner(output_dir=out_dir)
        runner.run_all(selected_corners=parsed_args.pdk, simulator=sim)
        return 0

    # 3. Cross-Simulator Correlation Mode
    if parsed_args.cross_sim:
        from .cross_simulator_benchmark import CrossSimulatorBenchmark
        out_dir = parsed_args.output_dir if parsed_args.output_dir != "spice_benchmark_results" else "results/specialized/cross_simulator"
        cid = parsed_args.pdk[0] if parsed_args.pdk else "FreePDK45_VTG_TT"
        sims = parsed_args.simulator if any(a.startswith("--sim") for a in args) else ["ngspice", "xyce", "hspice", "spectre"]
        bench = CrossSimulatorBenchmark(output_dir=out_dir)
        bench.run_benchmark(corner_id=cid, simulators=sims)
        return 0

    # 4. PKP3 3nm Characterization Mode
    if parsed_args.pkp3:
        from .pkp3_nanosheet_benchmark import PKP3NanosheetBenchmark
        out_dir = parsed_args.output_dir if parsed_args.output_dir != "spice_benchmark_results" else "results/specialized/pkp3_characterization"
        bench = PKP3NanosheetBenchmark(output_dir=out_dir)
        bench.run_all()
        return 0

    # 5. Commercial Foundry PDK Mode
    if parsed_args.commercial:
        from .commercial_pdk_benchmark import CommercialPDKBenchmark
        out_dir = parsed_args.output_dir if parsed_args.output_dir != "spice_benchmark_results" else "results/specialized/commercial_pdk"
        bench = CommercialPDKBenchmark(output_dir=out_dir)
        target_pdks = parsed_args.pdk if parsed_args.pdk else None
        bench.run_all(target_pdks=target_pdks)
        return 0

    # 6. Statistical Variation & Monte Carlo Mismatch Mode
    if parsed_args.monte_carlo:
        from .monte_carlo_benchmark import MonteCarloBenchmark
        out_dir = parsed_args.output_dir if parsed_args.output_dir != "spice_benchmark_results" else "results/specialized/monte_carlo"
        pdk_name = parsed_args.pdk[0] if parsed_args.pdk else "FreePDK45"
        bench = MonteCarloBenchmark(output_dir=out_dir, num_runs=parsed_args.mc_runs)
        bench.run_benchmark(pdk_name=pdk_name, num_runs=parsed_args.mc_runs)
        return 0

    # 7. Verilog-A Linter Mode
    if parsed_args.va_lint is not None:
        from .veriloga_linter_and_compiler import VerilogABenchmarkSuite
        out_dir = parsed_args.output_dir if parsed_args.output_dir != "spice_benchmark_results" else "results/specialized/veriloga"
        suite = VerilogABenchmarkSuite(output_dir=out_dir)
        targets = parsed_args.va_lint if len(parsed_args.va_lint) > 0 else None
        suite.run_all(target_files=targets)
        return 0

    # 8. OpenVAF Compilation Mode
    if parsed_args.va_compile:
        from .veriloga_linter_and_compiler import OpenVAFCompiler
        out_dir = parsed_args.output_dir if parsed_args.output_dir != "spice_benchmark_results" else "results/specialized/veriloga/osdi_cache"
        compiler = OpenVAFCompiler(cache_dir=out_dir)
        for va_f in parsed_args.va_compile:
            va_p = Path(va_f).resolve()
            res = compiler.compile(va_p)
            if res.get("status") == "PASS":
                print(f"[SUCCESS] Compiled {va_p.name} -> {res.get('osdi_path')}")
            else:
                print(f"[FAILED] Failed to compile {va_p.name}: {res.get('error')}")
        return 0

    if not parsed_args.model_file:
        print("Error: model_file is required when not running --circuit-stress or --regression.")
        parser.print_help()
        return 1

    model_path = Path(parsed_args.model_file)
    if not model_path.exists():
        print(f"Error: Model file '{parsed_args.model_file}' does not exist.")
        return 1

    simulators = parsed_args.simulator
    modes = parsed_args.modes
    base_output = parsed_args.output_dir

    print(f"SPICE Model Benchmark: {parsed_args.model_file}")
    print(f"Simulators: {', '.join(simulators)}")
    print(f"Modes: {', '.join(modes)}")
    print("-" * 60)

    # Run each simulator and collect results
    runner_results: Dict[str, dict] = {}

    for sim in simulators:
        sim_output_dir = f"{base_output}/{sim}"
        print(f"\n{'='*60}")
        print(f"  Running: {sim.upper()}")
        print(f"  Output:  {sim_output_dir}")
        print(f"{'='*60}")

        t_start = time.time()

        try:
            if sim == 'spectre':
                from .spectre_mosfet_simulation import benchmark_spice_model_spectre
                _mname = parsed_args.device
                if not _mname:
                    try:
                        import re as _re
                        with open(parsed_args.model_file) as _f:
                            _mm = _re.search(r'\.model\s+(\w+)\s', _f.read())
                            if _mm: _mname = _mm.group(1)
                    except: pass
                success = benchmark_spice_model_spectre(
                    model_file=parsed_args.model_file,
                    output_dir=sim_output_dir,
                    modes=modes,
                    dpi=parsed_args.dpi,
                    log_level=parsed_args.log_level,
                    dc_circuit=parsed_args.dc_circuit,
                    transient_circuit=parsed_args.transient_circuit,
                    noise_circuit=parsed_args.noise_circuit,
                    ac_circuit=parsed_args.ac_circuit,
                    model_name=_mname,
                )
            elif sim == 'hspice':
                from .hspice_mosfet_simulation import benchmark_spice_model_hspice
                _mname = parsed_args.device
                if not _mname:
                    try:
                        import re as _re
                        with open(parsed_args.model_file) as _f:
                            _mm = _re.search(r'\.model\s+(\w+)\s', _f.read())
                            if _mm: _mname = _mm.group(1)
                    except: pass
                success = benchmark_spice_model_hspice(
                    model_file=parsed_args.model_file,
                    output_dir=sim_output_dir,
                    modes=modes,
                    dpi=parsed_args.dpi,
                    log_level=parsed_args.log_level,
                    model_name=_mname,
                )
            elif sim == 'xyce':
                from .xyce_mosfet_simulation import benchmark_spice_model_xyce
                _mname = parsed_args.device
                if not _mname:
                    try:
                        import re as _re
                        with open(parsed_args.model_file) as _f:
                            _mm = _re.search(r'\.model\s+(\w+)\s', _f.read())
                            if _mm: _mname = _mm.group(1)
                    except: pass
                success = benchmark_spice_model_xyce(
                    model_file=parsed_args.model_file,
                    output_dir=sim_output_dir,
                    modes=modes,
                    dpi=parsed_args.dpi,
                    log_level=parsed_args.log_level,
                    model_name=_mname,
                )
            else:
                from . import benchmark_spice_model
                success = benchmark_spice_model(
                    model_file=parsed_args.model_file,
                    output_dir=sim_output_dir,
                    modes=modes,
                    dpi=parsed_args.dpi,
                    log_level=parsed_args.log_level,
                    dc_circuit=parsed_args.dc_circuit,
                    transient_circuit=parsed_args.transient_circuit,
                    noise_circuit=parsed_args.noise_circuit,
                    ac_circuit=parsed_args.ac_circuit,
                    device_name=parsed_args.device,
                    evaluate_all=parsed_args.all_devices,
                )
        except Exception as e:
            print(f"  ✗ {sim} crashed: {e}")
            runner_results[sim] = {
                'success': False,
                'elapsed': time.time() - t_start,
                'error': str(e),
            }
            continue

        elapsed = time.time() - t_start
        runner_results[sim] = {
            'success': success,
            'elapsed': elapsed,
            'output_dir': sim_output_dir,
        }

        status = "✓ PASS" if success else "✗ FAIL"
        print(f"\n  {sim}: {status}  ({elapsed:.1f}s)")

    # --- Bridge chaining ---
    if parsed_args.bridge:
        context = {
            "model_file": parsed_args.model_file,
            "output_dir": parsed_args.output_dir,
        }
        _run_bridges(context, parsed_args.bridge)

    # --- Comparison summary ---
    if len(runner_results) > 1:
        _print_comparison(runner_results, simulators, modes)
    elif len(runner_results) == 1:
        sim = list(runner_results.keys())[0]
        r = runner_results[sim]
        if r['success']:
            print(f"\n✓ Benchmark completed: {r['output_dir']}")
        else:
            print(f"\n✗ Benchmark failed: {r['output_dir']}")

    all_ok = all(r['success'] for r in runner_results.values())
    return 0 if all_ok else 1


def _print_comparison(results: Dict[str, dict], simulators: List[str], modes: List[str]):
    """Print a comparison table for multi-simulator runs."""
    print(f"\n{'='*70}")
    print("  SIMULATOR COMPARISON")
    print(f"{'='*70}")

    # Header
    col_w = max(16, max(len(s) for s in simulators) + 2)
    header = f"  {'Metric':<20}" + "".join(f"{s.upper():>{col_w}}" for s in simulators)
    print(header)
    print("  " + "-" * (20 + col_w * len(simulators)))

    # Status
    status_row = f"  {'Status':<20}"
    for s in simulators:
        r = results.get(s, {})
        st = "✓ PASS" if r.get('success') else "✗ FAIL"
        status_row += f"{st:>{col_w}}"
    print(status_row)

    # Elapsed time
    time_row = f"  {'Elapsed':<20}"
    for s in simulators:
        r = results.get(s, {})
        t = r.get('elapsed', 0)
        time_row += f"{f'{t:.1f}s':>{col_w}}"
    print(time_row)

    # Fastest
    valid = {s: r['elapsed'] for s, r in results.items() if r.get('success')}
    if valid:
        fastest = min(valid, key=valid.get)
        slowest = max(valid, key=valid.get)
        speedup = valid[slowest] / valid[fastest] if valid[fastest] > 0 else 1
        print(f"  {'Speedup':<20}{f'{speedup:.1f}x ({fastest} faster)':>{col_w * len(simulators)}}")

    # Modes tested
    mode_row = f"  {'Modes':<20}"
    mode_str = ",".join(modes)
    mode_row += f"{mode_str:>{col_w * len(simulators)}}"
    print(mode_row)

    # Output dirs
    for s in simulators:
        r = results.get(s, {})
        od = r.get('output_dir', 'N/A')
        print(f"  {s} output: {od}")

    print(f"{'='*70}")


def _run_bridges(context: dict, bridge_directives: list[str]) -> None:
    """Execute bridge directives after benchmarking completes."""
    project_root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(project_root))
    if bridge_directives:
        print("[bridge] Bridge functionality has been removed. Use spice_ast directly.")


if __name__ == "__main__":
    sys.exit(main())
