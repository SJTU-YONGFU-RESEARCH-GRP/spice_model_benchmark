import subprocess
from pathlib import Path
import sys
import re

def run_command(cmd, cwd=None):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(result.stderr)
        return None
    return result.stdout

def parse_ac_ls(output):
    # Parse output from analyze_cv_ls_from_cv.py
    # Look for "C_ls(AC)       : 1.123695e-14 F"
    match = re.search(r"C_ls\(AC\)\s*:\s*([\d.eE+-]+)\s*F", output)
    if match:
        return float(match.group(1))
    return None

def parse_dc_ls(output):
    # Parse output from analyze_cv_ls_from_cv.py
    # Look for "Cgg_LS(DC,sum) : 3.409344e-15 F"
    match = re.search(r"Cgg_LS\(DC,sum\)\s*:\s*([\d.eE+-]+)\s*F", output)
    if match:
        return float(match.group(1))
    return None

def parse_tran_ls(file_path):
    # Read results/tran_cap.txt
    # Content: C_ls_tran = 1.125e-14
    if not file_path.exists():
        return None
    content = file_path.read_text()
    match = re.search(r"C_ls_tran\s*=\s*([\d.eE+-]+)", content)
    if match:
        return float(match.group(1))
    return None

def main():
    root_dir = Path(__file__).resolve().parents[2]
    sandbox_dir = root_dir / "sandbox/expt_cv"
    results_dir = sandbox_dir / "results"
    results_dir.mkdir(exist_ok=True)

    print("=== Running Comparison Study ===")
    
    # 1. Run AC Simulation
    print("\n[1/3] Running AC Simulation...")
    run_command("./run_cv_sim.sh", cwd=sandbox_dir)
    
    # 2. Run DC Simulation (Single Point)
    print("\n[2/3] Running DC Simulation (L=0.045u, W=10u)...")
    run_command(
        "python test_cap_param/run_single_point.py --L 0.045 --W 10.0",
        cwd=root_dir
    )
    
    # 3. Run Transient Simulation
    print("\n[3/3] Running Transient Simulation...")
    run_command("ngspice -b tran_mos_realistic.cir", cwd=sandbox_dir)
    
    # 4. Analyze and Compare
    print("\n[4/4] Analyzing Results...")
    
    # Run analysis script to get AC and DC LS caps
    analysis_cmd = (
        f"python -m sandbox.expt_cv.analyze_cv_ls_from_cv "
        f"--cv-file {sandbox_dir}/results/cv_full_data.txt "
        f"--dc-file {root_dir}/netlists/ls_caps_dc.txt "
        f"--freq 1000000 --v1 0.0 --v2 1.2"
    )
    analysis_out = run_command(analysis_cmd, cwd=root_dir)
    
    c_ac = parse_ac_ls(analysis_out)
    c_dc = parse_dc_ls(analysis_out)
    c_tran = parse_tran_ls(results_dir / "tran_cap.txt")
    
    print("\n" + "="*40)
    print("SUMMARY OF LARGE SIGNAL CAPACITANCE")
    print("="*40)
    print(f"Geometry: L=0.045um, W=10um, VDD=1.2V")
    print("-" * 40)
    
    if c_ac:
        print(f"AC Derived (Integration): {c_ac*1e15:.4f} fF")
    else:
        print("AC Derived: Failed to extract")
        
    if c_tran:
        print(f"Transient Derived (Q/V):  {c_tran*1e15:.4f} fF")
    else:
        print("Transient Derived: Failed to extract")
        
    if c_dc:
        print(f"DC Derived (Method 5.1):  {c_dc*1e15:.4f} fF")
    else:
        print("DC Derived: Failed to extract")
        
    print("-" * 40)
    
    if c_ac and c_tran and c_dc:
        diff_ac_tran = abs(c_ac - c_tran) / c_tran * 100
        diff_dc_tran = abs(c_dc - c_tran) / c_tran * 100
        print(f"Difference AC vs Tran: {diff_ac_tran:.2f}%")
        print(f"Difference DC vs Tran: {diff_dc_tran:.2f}%")
        
        if diff_dc_tran > 10:
            print("\nCONCLUSION: DC Method 5.1 is INCONSISTENT with Transient/AC.")
            print("Likely cause: ngspice 'op' analysis @M[qg] misses overlap/fringing charge.")
        else:
            print("\nCONCLUSION: Methods are consistent.")

if __name__ == "__main__":
    main()
