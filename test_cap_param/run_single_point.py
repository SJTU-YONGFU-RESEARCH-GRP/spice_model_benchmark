import argparse
import sys
from pathlib import Path

# Add the project root to sys.path to allow imports
sys.path.append(str(Path(__file__).resolve().parents[1]))

from test_cap_param.run_cap_param_sweep import generate_tran_netlist_from_template, parse_q_total, run_ngspice

def main():
    parser = argparse.ArgumentParser(description="Run TRAN capacitance extraction for a single L/W point.")
    parser.add_argument("--pdk", type=str, default="FreePDK45_nom_T27", help="PDK label")
    parser.add_argument(
        "--tran-netlist",
        type=str,
        default="netlists/freepdk45_tran_cap_template.cir",
        help="Path to NMOS transient template",
    )
    parser.add_argument(
        "--tran-netlist-pmos",
        type=str,
        default="netlists/freepdk45_tran_cap_template_pmos.cir",
        help="Path to PMOS transient template",
    )
    parser.add_argument("--L", type=float, required=True, help="Length in um")
    parser.add_argument("--W", type=float, required=True, help="Width in um")
    parser.add_argument("--vdd", type=float, default=1.2, help="VDD voltage")
    
    args = parser.parse_args()
    
    base_netlists_dir = Path("netlists").resolve()
    template_path = Path(args.tran_netlist).resolve()
    template_path_p = Path(args.tran_netlist_pmos).resolve()
    
    # Create output directory for netlists
    pdk_netlist_dir = base_netlists_dir / args.pdk.lower()
    pdk_netlist_dir.mkdir(parents=True, exist_ok=True)
    
    netlist_name = f"{template_path.stem}_L{args.L}u_W{args.W}u.cir"
    netlist_path = pdk_netlist_dir / netlist_name
    
    print(f"[INFO] Generating TRAN netlist for L={args.L}um, W={args.W}um -> {netlist_path}")
    generate_tran_netlist_from_template(template_path, netlist_path, args.L, args.W, vdd=args.vdd)
    
    print(f"[INFO] Running ngspice for {netlist_name}")
    try:
        netlist_rel = netlist_path.relative_to(base_netlists_dir)
        stdout = run_ngspice(netlist_rel, cwd=base_netlists_dir)
    except Exception as e:
        print(f"[ERROR] ngspice failed: {e}")
        return

    q_total = parse_q_total(stdout)
    if q_total is None:
        print("[ERROR] Could not find q_total in ngspice output")
        return
    cgg = abs(q_total) / args.vdd
    print("\n=== NMOS Large Signal Capacitance (TRAN) ===")
    print(f"L={args.L}um, W={args.W}um")
    print(f"Cgg = {cgg:.6e} F ({cgg*1e15:.4f} fF)")

    if template_path_p.exists():
        netlist_name_p = f"{template_path_p.stem}_L{args.L}u_W{args.W}u.cir"
        netlist_path_p = pdk_netlist_dir / netlist_name_p
        print(f"\n[INFO] Generating PMOS TRAN netlist -> {netlist_path_p}")
        generate_tran_netlist_from_template(template_path_p, netlist_path_p, args.L, args.W, vdd=args.vdd)
        try:
            netlist_rel_p = netlist_path_p.relative_to(base_netlists_dir)
            stdout_p = run_ngspice(netlist_rel_p, cwd=base_netlists_dir)
            q_total_p = parse_q_total(stdout_p)
            if q_total_p is not None:
                cgg_p = abs(q_total_p) / args.vdd
                print("\n=== PMOS Large Signal Capacitance (TRAN) ===")
                print(f"L={args.L}um, W={args.W}um")
                print(f"Cgg = {cgg_p:.6e} F ({cgg_p*1e15:.4f} fF)")
        except Exception as e:
            print(f"[WARN] PMOS ngspice failed: {e}")

if __name__ == "__main__":
    main()
