import argparse
import subprocess
from pathlib import Path
import numpy as np
import shutil
import re

def run_ngspice(netlist_path, cwd):
    cmd = f"ngspice -b {netlist_path.name}"
    result = subprocess.run(
        cmd, shell=True, cwd=cwd, capture_output=True, text=True
    )
    return result.stdout

def parse_tran_cap_from_stdout(stdout, vdd):
    # Look for "q_total             =  -1.22281e-16"
    match = re.search(r"q_total\s*=\s*([\d.eE+-]+)", stdout)
    if match:
        q_total = float(match.group(1))
        return -q_total / vdd
    return None

def generate_netlist(template_path, out_path, L, W, VDD):
    text = template_path.read_text()
    text = re.sub(r"\.param L_dut=[\d.u]+", f".param L_dut={L}u", text)
    text = re.sub(r"\.param W_dut=[\d.u]+", f".param W_dut={W}u", text)
    text = re.sub(r"\.param VDD=[\d.]+", f".param VDD={VDD}", text)
    out_path.write_text(text)

def main():
    parser = argparse.ArgumentParser(description="Run Transient Capacitance Sweep")
    parser.add_argument("--max-L-count", type=int, default=None)
    parser.add_argument("--max-W-count", type=int, default=None)
    parser.add_argument("--vdd", type=float, default=1.2)
    args = parser.parse_args()

    root_dir = Path(__file__).resolve().parents[1]
    netlists_dir = root_dir / "netlists"
    results_dir = root_dir / "test_cap_param/results/tran_sweep"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    template_path = netlists_dir / "freepdk45_tran_cap_template.cir"
    
    # Define Sweep
    L_list = [0.045, 0.06, 0.09, 0.15, 0.3, 0.5, 1.0]
    W_list = [0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]
    
    if args.max_L_count:
        L_list = L_list[:args.max_L_count]
    if args.max_W_count:
        W_list = W_list[:args.max_W_count]
        
    records = []
    
    print(f"Starting sweep: {len(L_list)} L points x {len(W_list)} W points")
    
    for L in L_list:
        for W in W_list:
            netlist_name = f"tran_cap_L{L}_W{W}.cir"
            netlist_path = netlists_dir / netlist_name
            
            generate_netlist(template_path, netlist_path, L, W, args.vdd)
            
            # Run
            print(f"Running L={L}u W={W}u...")
            stdout = run_ngspice(netlist_path, cwd=netlists_dir)
            
            # Parse
            cap = parse_tran_cap_from_stdout(stdout, args.vdd)
            if cap is not None:
                print(f"  -> C_ls = {cap*1e15:.4f} fF")
                records.append((L, W, cap))
            else:
                print(f"  -> Failed")
                
    # Save CSV
    csv_path = results_dir / "cap_vs_LW_tran.csv"
    with csv_path.open("w") as f:
        f.write("L_um,W_um,Cgg_tran_fF\n")
        for L, W, cap in records:
            f.write(f"{L},{W},{cap*1e15}\n")
            
    print(f"Saved results to {csv_path}")

if __name__ == "__main__":
    main()
