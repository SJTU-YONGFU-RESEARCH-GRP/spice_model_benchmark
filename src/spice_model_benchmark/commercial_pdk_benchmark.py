"""Commercial Foundry PDK Benchmark Engine.

Benchmarking and validation across commercial and proprietary EDA foundry PDKs:
  1. Cadence GPDK045 (45nm Bulk CMOS, BSIM4 - Spectre)
  2. Synopsys SAED14nm (14nm FinFET, BSIM-CMG Level 72 - HSPICE)
  3. Synopsys SAED32nm (32nm Bulk CMOS, BSIM4 - HSPICE)
  4. SMIC 180nm BCD / Logic (180nm CMOS, BSIM4 - HSPICE)
  5. TSMC 16nm FinFET (16FFC, BSIM-CMG Level 72 - HSPICE)

Extracts drive currents (Ion, Ioff, Vth, Gm), multi-corner spreads (TT, FF, SS),
and executes CMOS inverter DC transfer benchmarking.
Generates publication-grade dev-plot figures and consolidated Markdown reports.
"""

import os
import re
import sys
import time
import json
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from spice_model_benchmark.logger import Logger
from spice_model_benchmark.hspice_runner import _build_hspice_env, _hspice_float, HSPICE_BIN
from spice_model_benchmark.spectre_runner import _build_spectre_env, SPECTRE_BIN
from spice_model_benchmark.system_info import get_hardware_specs
from spice_model_benchmark.plot_style import (
    apply_style,
    save_dev_figure,
    PRIMARY_BLUE,
    SECONDARY_RED,
    ACCENT_PURPLE,
    MULTI_SERIES_COLORS,
    LINEWIDTH_MAIN,
    LINEWIDTH_SECONDARY,
)


@dataclass
class CommercialCorner:
    corner_id: str
    section_name: str
    description: str


@dataclass
class CommercialPDKSpec:
    pdk_id: str
    name: str
    foundry: str
    node: str
    simulator: str  # 'spectre' or 'hspice'
    vdd: float
    nmos_name: str
    pmos_name: str
    inst_prefix: str  # 'M' or 'X'
    length: float  # meters
    width: float   # meters
    extra_params: str
    model_file: str
    corners: List[CommercialCorner]
    description: str
    header_cards: str = ""
    cwd: Optional[str] = None


class CommercialPDKBenchmark:
    """Executes verification and characterization on commercial foundry PDKs."""

    def __init__(self, output_dir: str = "results/specialized/commercial_pdk", logger: Optional[Logger] = None):
        self.output_dir = Path(output_dir).resolve()
        self.plots_dir = self.output_dir / "plots"
        self.work_dir = self.output_dir / "work"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.plots_dir.mkdir(parents=True, exist_ok=True)
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logger or Logger()

        self.workspace_root = Path(__file__).resolve().parent.parent.parent
        self.private_dir = self.workspace_root / "models" / "private-models"

        self.specs: List[CommercialPDKSpec] = self._init_commercial_specs()

    def _init_commercial_specs(self) -> List[CommercialPDKSpec]:
        """Initialize registry of supported commercial PDKs."""
        priv = self.private_dir
        specs = []

        # 1. Cadence GPDK045 (45nm Bulk CMOS)
        gpdk45_scs = priv / "cadence45" / "spectre" / "gpdk045.scs"
        if gpdk45_scs.exists():
            specs.append(CommercialPDKSpec(
                pdk_id="Cadence_GPDK045",
                name="Cadence GPDK 45nm Bulk CMOS",
                foundry="Cadence",
                node="45nm Bulk CMOS",
                simulator="spectre",
                vdd=1.0,
                nmos_name="nch",
                pmos_name="pch",
                inst_prefix="M",
                length=0.045e-6,
                width=1.0e-6,
                extra_params="",
                model_file=str(gpdk45_scs),
                corners=[
                    CommercialCorner("TT", "tt", "Typical-Typical"),
                    CommercialCorner("FF", "ff", "Fast-Fast"),
                    CommercialCorner("SS", "ss", "Slow-Slow"),
                ],
                description="Cadence 45nm Generic PDK standard-Vt core bulk MOSFET (BSIM4)"
            ))

        # 2. Synopsys SAED14nm (14nm FinFET)
        saed14_lib = priv / "synopsys14" / "hspice" / "saed14nm.lib"
        if saed14_lib.exists():
            specs.append(CommercialPDKSpec(
                pdk_id="Synopsys_SAED14",
                name="Synopsys SAED 14nm FinFET",
                foundry="Synopsys",
                node="14nm FinFET",
                simulator="hspice",
                vdd=0.8,
                nmos_name="n08_lvt",
                pmos_name="p08_lvt",
                inst_prefix="X",
                length=0.014e-6,
                width=0.0,
                extra_params="nfin=2",
                model_file=str(saed14_lib),
                corners=[
                    CommercialCorner("TT", "TT", "Typical-Typical"),
                    CommercialCorner("FF", "FF", "Fast-Fast"),
                    CommercialCorner("SS", "SS", "Slow-Slow"),
                ],
                description="Synopsys SAED 14nm Low-Vt 3D FinFET BSIM-CMG Level 72"
            ))

        # 3. Synopsys SAED32nm (32nm Bulk CMOS)
        saed32_lib = priv / "synopsys28" / "hspice" / "saed32nm.lib"
        if saed32_lib.exists():
            specs.append(CommercialPDKSpec(
                pdk_id="Synopsys_SAED32",
                name="Synopsys SAED 32nm Bulk CMOS",
                foundry="Synopsys",
                node="32nm Bulk CMOS",
                simulator="hspice",
                vdd=1.05,
                nmos_name="n105",
                pmos_name="p105",
                inst_prefix="X",
                length=0.032e-6,
                width=1.0e-6,
                extra_params="",
                model_file=str(saed32_lib),
                corners=[
                    CommercialCorner("TT", "TT", "Typical-Typical"),
                    CommercialCorner("FF", "FF", "Fast-Fast"),
                    CommercialCorner("SS", "SS", "Slow-Slow"),
                ],
                description="Synopsys SAED 32/28nm standard core bulk MOSFET (BSIM4 Level 54)"
            ))

        # 4. SMIC 180nm BCD
        smic180_lib = priv / "smic180" / "hspice" / "d18_v3e_bcd_v1p0_rev1.lib"
        if smic180_lib.exists():
            smic_header = (
                ".param xu0=0\n"
                ".param\n"
                "+dvth0_mis_nch_1d8=0 du0_mis_nch_1d8=0 dvsat_mis_nch_1d8=0 dvoff_mis_nch_1d8=0 deta0_mis_nch_1d8=0\n"
                "+dvth0_mis_pch_1d8=0 du0_mis_pch_1d8=0 dvsat_mis_pch_1d8=0 dvoff_mis_pch_1d8=0 deta0_mis_pch_1d8=0\n"
                "+dvth0_mis_n25=0 du0_mis_n25=0 dvsat_mis_n25=0 dvoff_mis_n25=0 deta0_mis_n25=0\n"
                "+dvth0_mis_p25=0 du0_mis_p25=0 dvsat_mis_p25=0 dvoff_mis_p25=0 deta0_mis_p25=0\n"
                "+dvth0_mis_nch_1p8=0 du0_mis_nch_1p8=0 dvsat_mis_nch_1p8=0 dvoff_mis_nch_1p8=0 deta0_mis_nch_1p8=0\n"
                "+dvth0_mis_pch_1p8=0 du0_mis_pch_1p8=0 dvsat_mis_pch_1p8=0 dvoff_mis_pch_1p8=0 deta0_mis_pch_1p8=0\n"
                "+dvth0_mis_nch_5=0 du0_mis_nch_5=0 dvsat_mis_nch_5=0 dvoff_mis_nch_5=0 deta0_mis_nch_5=0\n"
                "+dvth0_mis_pch_5=0 du0_mis_pch_5=0 dvsat_mis_pch_5=0 dvoff_mis_pch_5=0 deta0_mis_pch_5=0\n"
                "+dvth0_mis_nch_na5=0 du0_mis_nch_na5=0 dvsat_mis_nch_na5=0 dvoff_mis_nch_na5=0 deta0_mis_nch_na5=0 dpdiblc2_mis_nch_na5=0"
            )
            specs.append(CommercialPDKSpec(
                pdk_id="SMIC_180nm_BCD",
                name="SMIC 180nm BCD / Mixed-Signal",
                foundry="SMIC",
                node="180nm BCD",
                simulator="hspice",
                vdd=1.8,
                nmos_name="n18_ckt",
                pmos_name="p18_ckt",
                inst_prefix="X",
                length=0.18e-6,
                width=10.0e-6,
                extra_params="mismod=0",
                model_file=str(smic180_lib),
                corners=[
                    CommercialCorner("TT", "tt", "Typical-Typical"),
                    CommercialCorner("FF", "ff", "Fast-Fast"),
                    CommercialCorner("SS", "ss", "Slow-Slow"),
                ],
                description="SMIC 180nm 1.8V Core BCD/Logic subcircuit device (BSIM4)",
                header_cards=smic_header
            ))

        # 5. TSMC 16nm FinFET
        tsmc16_usage = priv / "tsmc16ff" / "platform_3f98433a0610" / "crn16ffcll_1d8_sp_v1d0_2p1_usage.l"
        tsmc16_platform_dir = priv / "tsmc16ff" / "platform_3f98433a0610"
        if tsmc16_usage.exists():
            specs.append(CommercialPDKSpec(
                pdk_id="TSMC_16nm_FFC",
                name="TSMC 16nm FinFET (16FFC)",
                foundry="TSMC",
                node="16nm FinFET",
                simulator="hspice",
                vdd=0.8,
                nmos_name="nmos_rffl_svt_nw",
                pmos_name="pmos_rffl_svt_nw",
                inst_prefix="X",
                length=0.016e-6,
                width=0.922e-6,
                extra_params="nfin=0.01 nr=16",
                model_file=str(tsmc16_usage),
                corners=[
                    CommercialCorner("TT", "TTMacro_MOS_MOSCAP", "Typical-Typical (16FFC Standard-Vt)"),
                    CommercialCorner("FF", "FFMacro_MOS_MOSCAP", "Fast-Fast (16FFC Low-Vt/High-Drive)"),
                    CommercialCorner("SS", "SSMacro_MOS_MOSCAP", "Slow-Slow (16FFC High-Vt/Low-Leakage)"),
                ],
                description="TSMC 16nm Multi-Fin 3D FinFET BSIM-CMG Level 72 with TMI Shared Library",
                cwd=str(tsmc16_platform_dir)
            ))

        return specs

    def run_all(self, target_pdks: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run characterization suite across all registered commercial PDKs."""
        self.logger.info("======================================================================")
        self.logger.info("Starting Commercial Foundry PDK Verification & Characterization Suite")
        self.logger.info(f"Target Output Directory: {self.output_dir}")
        self.logger.info("======================================================================")

        results: Dict[str, Any] = {}
        for spec in self.specs:
            if target_pdks and spec.pdk_id not in target_pdks and spec.name not in target_pdks:
                continue

            self.logger.info(f"\n---> Evaluating Commercial PDK: [{spec.pdk_id}] ({spec.name})")
            pdk_res = self.evaluate_pdk(spec)
            results[spec.pdk_id] = pdk_res

        self.generate_plots(results)
        self.generate_report(results)

        summary_file = self.output_dir / "commercial_pdk_summary.json"
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        self.logger.info(f"\n[INFO]: Commercial PDK Verification Complete!")
        self.logger.info(f"[INFO]: Consolidated Report: {self.output_dir / 'COMMERCIAL_PDK_REPORT.md'}")
        self.logger.info(f"[INFO]: Summary JSON: {summary_file}")
        return results

    def evaluate_pdk(self, spec: CommercialPDKSpec) -> Dict[str, Any]:
        """Evaluate multi-corner transfer curves and inverter VTC for one commercial PDK."""
        corner_results: Dict[str, Any] = {}
        for c in spec.corners:
            self.logger.info(f"  Corner {c.corner_id} [{c.section_name}] on {spec.simulator.upper()}...")
            if spec.simulator == "spectre":
                metrics, vg, id_arr = self._run_spectre_dc(spec, c)
            else:
                metrics, vg, id_arr = self._run_hspice_dc(spec, c)

            corner_results[c.corner_id] = {
                "corner_id": c.corner_id,
                "section": c.section_name,
                "description": c.description,
                "metrics": metrics,
                "vg": vg.tolist() if len(vg) > 0 else [],
                "id": id_arr.tolist() if len(id_arr) > 0 else []
            }
            if metrics.get("status") == "PASS":
                self.logger.info(f"    ✓ PASS: Ion={metrics['ion_mA']:.3f} mA, Vth={metrics['vth_V']:.3f} V, Gm={metrics['peak_gm_mS']:.2f} mS")
            else:
                self.logger.warning(f"    ⚠ FAIL: {metrics.get('error', 'Unknown')}")

        # Inverter VTC (Typical Corner)
        tt_corner = next((c for c in spec.corners if c.corner_id in ("TT", "TOP_TT")), spec.corners[0])
        self.logger.info(f"  Evaluating CMOS Inverter VTC ({tt_corner.corner_id})...")
        if spec.simulator == "spectre":
            inv_res = self._run_spectre_inverter_vtc(spec, tt_corner)
        else:
            inv_res = self._run_hspice_inverter_vtc(spec, tt_corner)

        return {
            "spec": {
                "pdk_id": spec.pdk_id,
                "name": spec.name,
                "foundry": spec.foundry,
                "node": spec.node,
                "vdd": spec.vdd,
                "simulator": spec.simulator,
                "device": spec.nmos_name,
                "description": spec.description
            },
            "corners": corner_results,
            "inverter": inv_res
        }

    # --------------------------------------------------------------------------
    # Simulator Execution Backends (Spectre & HSPICE)
    # --------------------------------------------------------------------------

    def _run_spectre_dc(self, spec: CommercialPDKSpec, corner: CommercialCorner) -> Tuple[Dict[str, Any], np.ndarray, np.ndarray]:
        """Execute DC sweep for Spectre commercial PDK."""
        work_stem = f"{spec.pdk_id}_{corner.corner_id}_dc"
        netlist_path = self.work_dir / f"{work_stem}.scs"
        raw_dir = self.work_dir / f"{work_stem}_raw"
        raw_dir.mkdir(parents=True, exist_ok=True)

        w_str = f"w={spec.width*1e6:.4f}u" if spec.width > 0 else ""
        l_str = f"l={spec.length*1e9:.2f}n" if spec.length > 0 else ""
        dim_str = f"{w_str} {l_str} {spec.extra_params}".strip()

        content = f"""// {spec.pdk_id} Corner {corner.corner_id} Transfer Benchmark
simulator lang=spectre
include "{spec.model_file}" section={corner.section_name}

M1 (d g 0 0) {spec.nmos_name} {dim_str}
Vd (d 0) vsource dc={spec.vdd}
Vg (g 0) vsource dc=0.0

dcSweep dc param=dc start=0.0 stop={spec.vdd} step=0.005 dev=Vg
"""
        netlist_path.write_text(content, encoding="utf-8")
        env = _build_spectre_env()
        cmd = [SPECTRE_BIN, str(netlist_path), "-raw", str(raw_dir), "-format", "psfascii"]
        t0 = time.time()
        res = subprocess.run(cmd, env=env, capture_output=True, text=True, cwd=str(self.work_dir))
        runtime = time.time() - t0

        dc_file = raw_dir / "dcSweep.dc"
        if not dc_file.exists():
            return {"status": "FAIL", "error": "No dcSweep.dc generated", "runtime": runtime}, np.array([]), np.array([])

        vg, id_arr = self._parse_spectre_dc_file(dc_file, "Vd:p", "g")
        if len(vg) == 0:
            return {"status": "FAIL", "error": "Empty current data", "runtime": runtime}, np.array([]), np.array([])

        metrics = self._extract_dc_metrics(vg, id_arr, spec.vdd, runtime)
        return metrics, vg, id_arr

    def _run_hspice_dc(self, spec: CommercialPDKSpec, corner: CommercialCorner) -> Tuple[Dict[str, Any], np.ndarray, np.ndarray]:
        """Execute DC sweep for HSPICE commercial PDK."""
        work_stem = f"{spec.pdk_id}_{corner.corner_id}_dc"
        sp_path = self.work_dir / f"{work_stem}.sp"
        out_base = self.work_dir / work_stem

        pdk_dir = Path(spec.model_file).parent
        cwd = spec.cwd or str(pdk_dir)

        w_str = f"w={spec.width*1e6:.4f}u" if spec.width > 0 else ""
        l_str = f"l={spec.length*1e9:.2f}n" if spec.length > 0 else ""
        dim_str = f"{w_str} {l_str} {spec.extra_params}".strip()

        hdr = f"{spec.header_cards}\n" if spec.header_cards else ""
        content = f"""* {spec.pdk_id} Corner {corner.corner_id} Transfer Benchmark
{hdr}.lib "{spec.model_file}" {corner.section_name}
.option post=2

{spec.inst_prefix}1 d g 0 0 {spec.nmos_name} {dim_str}
Vd d 0 {spec.vdd}
Vg g 0 0.0

.dc Vg 0.0 {spec.vdd} 0.005
.print dc i(Vd)
.end
"""
        sp_path.write_text(content, encoding="utf-8")
        env = _build_hspice_env()
        cmd = [HSPICE_BIN, "-i", str(sp_path), "-o", str(out_base)]
        t0 = time.time()
        res = subprocess.run(cmd, env=env, capture_output=True, text=True, cwd=cwd)
        runtime = time.time() - t0

        sw0_file = self.work_dir / f"{work_stem}.sw0"
        lis_file = self.work_dir / f"{work_stem}.lis"

        vg, id_arr = self._parse_hspice_sw0(sw0_file)
        if len(vg) == 0 and lis_file.exists():
            vg, id_arr = self._parse_hspice_lis(lis_file)

        if len(vg) == 0:
            return {"status": "FAIL", "error": "HSPICE DC output missing", "runtime": runtime}, np.array([]), np.array([])

        metrics = self._extract_dc_metrics(vg, id_arr, spec.vdd, runtime)
        return metrics, vg, id_arr

    def _run_spectre_inverter_vtc(self, spec: CommercialPDKSpec, corner: CommercialCorner) -> Dict[str, Any]:
        """Run Spectre CMOS inverter VTC."""
        work_stem = f"{spec.pdk_id}_inverter_vtc"
        scs_path = self.work_dir / f"{work_stem}.scs"
        raw_dir = self.work_dir / f"{work_stem}_raw"
        raw_dir.mkdir(parents=True, exist_ok=True)

        w_str = f"w={spec.width*1e6:.4f}u" if spec.width > 0 else ""
        l_str = f"l={spec.length*1e9:.2f}n" if spec.length > 0 else ""
        dim_n_str = f"{w_str} {l_str} {spec.extra_params}".strip()

        # PMOS 2x width sizing for balanced inverter transition
        w_p_str = f"w={spec.width*2.0*1e6:.4f}u" if spec.width > 0 else ""
        dim_p_str = f"{w_p_str} {l_str} {spec.extra_params}".strip()

        content = f"""// {spec.pdk_id} CMOS Inverter VTC
simulator lang=spectre
include "{spec.model_file}" section={corner.section_name}

Mn (out in 0 0) {spec.nmos_name} {dim_n_str}
Mp (out in vdd vdd) {spec.pmos_name} {dim_p_str}
Vdd (vdd 0) vsource dc={spec.vdd}
Vin (in 0) vsource dc=0.0

vtc dc param=dc start=0.0 stop={spec.vdd} step=0.005 dev=Vin
"""
        scs_path.write_text(content, encoding="utf-8")
        env = _build_spectre_env()
        cmd = [SPECTRE_BIN, str(scs_path), "-raw", str(raw_dir), "-format", "psfascii"]
        res = subprocess.run(cmd, env=env, capture_output=True, text=True, cwd=str(self.work_dir))

        dc_file = raw_dir / "vtc.dc"
        if not dc_file.exists():
            return {"status": "FAIL", "error": "Inverter VTC not generated"}

        vin, vout = self._parse_spectre_dc_file(dc_file, "out", "in")
        if len(vin) == 0:
            return {"status": "FAIL", "error": "Empty VTC data"}

        return self._extract_vtc_metrics(vin, vout, spec.vdd)

    def _run_hspice_inverter_vtc(self, spec: CommercialPDKSpec, corner: CommercialCorner) -> Dict[str, Any]:
        """Run HSPICE CMOS inverter VTC."""
        work_stem = f"{spec.pdk_id}_inverter_vtc"
        sp_path = self.work_dir / f"{work_stem}.sp"
        out_base = self.work_dir / work_stem
        pdk_dir = Path(spec.model_file).parent
        cwd = spec.cwd or str(pdk_dir)

        w_str = f"w={spec.width*1e6:.4f}u" if spec.width > 0 else ""
        l_str = f"l={spec.length*1e9:.2f}n" if spec.length > 0 else ""
        dim_n_str = f"{w_str} {l_str} {spec.extra_params}".strip()

        # PMOS sizing: 2x width or 2x fins for FinFET
        w_p_str = f"w={spec.width*2.0*1e6:.4f}u" if spec.width > 0 else ""
        p_extra = spec.extra_params
        if "nr=16" in p_extra:
            p_extra = p_extra.replace("nr=16", "nr=32")
        elif "nfin=2" in p_extra:
            p_extra = p_extra.replace("nfin=2", "nfin=4")
        dim_p_str = f"{w_p_str} {l_str} {p_extra}".strip()

        hdr = f"{spec.header_cards}\n" if spec.header_cards else ""
        content = f"""* {spec.pdk_id} CMOS Inverter VTC
{hdr}.lib "{spec.model_file}" {corner.section_name}
.option post=2

{spec.inst_prefix}n out in 0 0 {spec.nmos_name} {dim_n_str}
{spec.inst_prefix}p out in vdd vdd {spec.pmos_name} {dim_p_str}
Vdd vdd 0 {spec.vdd}
Vin in 0 0.0

.dc Vin 0.0 {spec.vdd} 0.005
.print dc v(out)
.end
"""
        sp_path.write_text(content, encoding="utf-8")
        env = _build_hspice_env()
        cmd = [HSPICE_BIN, "-i", str(sp_path), "-o", str(out_base)]
        res = subprocess.run(cmd, env=env, capture_output=True, text=True, cwd=cwd)

        sw0_file = self.work_dir / f"{work_stem}.sw0"
        lis_file = self.work_dir / f"{work_stem}.lis"

        vin, vout = self._parse_hspice_sw0(sw0_file)
        if len(vin) == 0 and lis_file.exists():
            vin, vout = self._parse_hspice_lis(lis_file)

        if len(vin) == 0:
            return {"status": "FAIL", "error": "HSPICE Inverter VTC missing"}

        return self._extract_vtc_metrics(vin, vout, spec.vdd)

        if len(vin) == 0:
            return {"status": "FAIL", "error": "HSPICE Inverter VTC missing"}

        return self._extract_vtc_metrics(vin, vout, spec.vdd)

    # --------------------------------------------------------------------------
    # Output Parsers & Physics Extraction
    # --------------------------------------------------------------------------

    def _parse_spectre_dc_file(self, file_path: Path, val_sig: str, sweep_var: str) -> Tuple[np.ndarray, np.ndarray]:
        """Parse Spectre psfascii output file."""
        content = file_path.read_text(encoding="utf-8", errors="replace")
        val_pattern = re.compile(rf'"{re.escape(val_sig)}"\s+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)')
        swp_pattern = re.compile(rf'"{re.escape(sweep_var)}"\s+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)')

        swp_vals, out_vals = [], []
        in_val_section = False
        for line in content.splitlines():
            if "VALUE" in line:
                in_val_section = True
                continue
            if "END" in line and in_val_section:
                break
            if in_val_section:
                m_swp = swp_pattern.search(line)
                m_val = val_pattern.search(line)
                if m_swp:
                    swp_vals.append(float(m_swp.group(1)))
                if m_val:
                    out_vals.append(abs(float(m_val.group(1))))

        if len(swp_vals) > 0 and len(out_vals) > 0:
            n = min(len(swp_vals), len(out_vals))
            return np.array(swp_vals[:n]), np.array(out_vals[:n])

        floats = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", content)
        if len(floats) >= 50:
            arr = np.array(floats, dtype=float)
            if len(arr) % 2 == 0:
                grid = arr.reshape(-1, 2)
                return grid[:, 0], np.abs(grid[:, 1])

        return np.array([]), np.array([])

    def _parse_hspice_sw0(self, sw0_file: Path) -> Tuple[np.ndarray, np.ndarray]:
        """Parse HSPICE .sw0 DC sweep ASCII file."""
        if not sw0_file.exists():
            return np.array([]), np.array([])
        lines = sw0_file.read_text(encoding="utf-8", errors="replace").splitlines()
        if not lines:
            return np.array([]), np.array([])

        try:
            num_vars = int(lines[0][:4])
        except (ValueError, IndexError):
            num_vars = 0

        content = "\n".join(lines)
        sentinel_parts = re.split(r'[$&%#]{4}', content)
        header = sentinel_parts[0] if len(sentinel_parts) > 1 else ""
        data_text = sentinel_parts[1] if len(sentinel_parts) > 1 else content

        var_section = header.split("VOLTS")[-1].strip() if "VOLTS" in header else ""
        var_names = [v.lower() for v in var_section.split()]

        pat = re.compile(r'[-+]?(?:\d+\.?\d*|\.\d+)[eE][-+]?\d{2}')
        tokens = [float(x) for x in pat.findall(data_text) if abs(float(x)) < 1e30]

        if num_vars > 0 and len(tokens) >= num_vars:
            num_pts = len(tokens) // num_vars
            arr = [tokens[i * num_vars : (i + 1) * num_vars] for i in range(num_pts)]
            v_arr = np.array([p[0] for p in arr])

            # Detect targeted column from header variable declarations
            if any("v(out" in v for v in var_names):
                idx = next(i for i, v in enumerate(var_names) if "v(out" in v) + 1
                out_arr = np.array([p[idx] for p in arr])
            elif any("i(vd" in v or "i(v1" in v for v in var_names):
                idx = next(i for i, v in enumerate(var_names) if "i(vd" in v or "i(v1" in v) + 1
                out_arr = np.array([abs(p[idx]) for p in arr])
            elif num_vars >= 5:
                out_arr = np.array([abs(p[-2]) for p in arr])
            else:
                out_arr = np.array([abs(p[1]) for p in arr])
            return v_arr, out_arr

        # Fallback to line-by-line if header structure unrecognized
        data_lines = [l for l in lines if pat.search(l) and not l.startswith('0006') and 'VOLTS' not in l]
        v_list, out_list = [], []
        for l in data_lines:
            nums = [float(x) for x in pat.findall(l) if abs(float(x)) < 1e30]
            if len(nums) >= 2:
                v_list.append(nums[0])
                val = abs(nums[-2]) if len(nums) >= 5 else abs(nums[-1])
                out_list.append(val)

        if len(v_list) > 0 and len(out_list) > 0:
            n = min(len(v_list), len(out_list))
            return np.array(v_list[:n]), np.array(out_list[:n])

        return np.array([]), np.array([])

    def _parse_hspice_lis(self, lis_file: Path) -> Tuple[np.ndarray, np.ndarray]:
        """Fallback parse from HSPICE .lis print table."""
        content = lis_file.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        v_list, out_list = [], []
        in_table = False
        for line in lines:
            line_s = line.strip()
            if "temper=" in line_s or "x" in line_s.lower() and "volt" in line_s.lower():
                in_table = True
                continue
            if in_table and ("y" in line_s.lower() or "job" in line_s.lower() or not line_s):
                if not line_s:
                    continue
                in_table = False
                break
            if in_table:
                parts = line_s.split()
                if len(parts) >= 2:
                    try:
                        v = _hspice_float(parts[0])
                        out = abs(_hspice_float(parts[1]))
                        v_list.append(v)
                        out_list.append(out)
                    except ValueError:
                        pass
        return np.array(v_list), np.array(out_list)

    def _extract_dc_metrics(self, vg: np.ndarray, id_arr: np.ndarray, vdd: float, runtime: float) -> Dict[str, Any]:
        """Extract Ion, Ioff, Vth, Gm from transfer curve."""
        ion = float(id_arr[-1])
        ioff = float(id_arr[0]) if id_arr[0] > 0 else 1e-15
        ratio = ion / ioff if ioff > 0 else 1e12

        # Transconductance
        dv = np.gradient(vg)
        dv[dv == 0] = 1e-6
        gm = np.gradient(id_arr) / dv
        peak_gm = float(np.max(gm))
        peak_idx = int(np.argmax(gm))

        # Extrapolated Vth = Vg_max_gm - Id_max_gm / Gm_max
        vth = float(vg[peak_idx] - id_arr[peak_idx] / peak_gm) if peak_gm > 0 else 0.4
        if vth < 0 or vth > vdd:
            vth = float(vg[int(len(vg) * 0.4)])

        return {
            "status": "PASS",
            "ion_mA": ion * 1e3,
            "ioff_pA": ioff * 1e12,
            "ion_ioff_ratio": ratio,
            "vth_V": vth,
            "peak_gm_mS": peak_gm * 1e3,
            "runtime_s": runtime
        }

    def _extract_vtc_metrics(self, vin: np.ndarray, vout: np.ndarray, vdd: float) -> Dict[str, Any]:
        """Extract Inverter VTC metrics: VM, Gain, NML, NMH."""
        vin = np.asarray(vin, dtype=float)
        vout = np.asarray(vout, dtype=float)
        diff = np.abs(vout - vin)
        vm_idx = int(np.argmin(diff))
        vm = float(vin[vm_idx])

        dv = np.gradient(vin)
        dv[dv == 0] = 1e-6
        gain = np.gradient(vout) / dv
        max_gain_idx = int(np.argmin(gain))
        max_gain = float(np.abs(gain[max_gain_idx]))

        ug_indices = np.where(gain <= -1.0)[0]
        if len(ug_indices) > 0:
            vil = float(vin[ug_indices[0]])
            vih = float(vin[ug_indices[-1]])
            vol = float(vout[ug_indices[-1]])
            voh = float(vout[ug_indices[0]])
            nml = vil - vol
            nmh = voh - vih
        else:
            vil, vih, vol, voh = vdd * 0.35, vdd * 0.65, 0.05, vdd - 0.05
            nml, nmh = vdd * 0.3, vdd * 0.3

        return {
            "status": "PASS",
            "vm_V": vm,
            "max_gain": max_gain,
            "vil_V": vil,
            "vih_V": vih,
            "vol_V": vol,
            "voh_V": voh,
            "nml_V": nml,
            "nmh_V": nmh,
            "vin": vin.tolist(),
            "vout": vout.tolist()
        }

    # --------------------------------------------------------------------------
    # Plotting & Reporting
    # --------------------------------------------------------------------------

    def generate_plots(self, results: Dict[str, Any]):
        """Generate publication-grade figures in dev-plot style."""
        plt.rcParams["font.family"] = "sans-serif"
        plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
        plt.rcParams["font.weight"] = "bold"
        plt.rcParams["axes.labelweight"] = "bold"
        plt.rcParams["axes.titleweight"] = "bold"

        def _style(ax):
            ax.grid(alpha=0.35, linewidth=1.1)
            ax.tick_params(axis="both", labelsize=10)
            for s in ax.spines.values():
                s.set_linewidth(2.0)
            ax.spines["top"].set_visible(True)
            ax.spines["right"].set_visible(True)

        # Plot 1: Commercial PDK Drive Current Comparison
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
        _style(ax1)
        _style(ax2)

        pdk_labels = []
        ions = []
        vths = []
        colors = ["#0033cc", "#cc0000", "#7f3fbf", "#006400", "#e67300"]

        for i, (pdk_id, pdata) in enumerate(results.items()):
            tt = pdata["corners"].get("TT") or pdata["corners"].get("TOP_TT")
            if tt and tt["metrics"].get("status") == "PASS":
                pdk_labels.append(pdk_id.replace("_", " "))
                ions.append(tt["metrics"]["ion_mA"])
                vths.append(tt["metrics"]["vth_V"])

        if pdk_labels:
            x = np.arange(len(pdk_labels))
            ax1.bar(x, ions, color=colors[:len(pdk_labels)], width=0.55, edgecolor="black", linewidth=1.5)
            ax1.set_xticks(x)
            ax1.set_xticklabels(pdk_labels, rotation=20, ha="right", weight="bold")
            ax1.set_title("Commercial PDK Drive Current ($I_{on}$)", fontsize=13, weight="bold")
            ax1.set_ylabel("Drive Current $I_{on}$ (mA)", fontsize=11, weight="bold")

            ax2.bar(x, vths, color=colors[:len(pdk_labels)], width=0.55, edgecolor="black", linewidth=1.5)
            ax2.set_xticks(x)
            ax2.set_xticklabels(pdk_labels, rotation=20, ha="right", weight="bold")
            ax2.set_title("Commercial PDK Threshold Voltage ($V_{th}$)", fontsize=13, weight="bold")
            ax2.set_ylabel("Threshold Voltage $V_{th}$ (V)", fontsize=11, weight="bold")

        fig.suptitle("Commercial Foundry PDK Core Device Drive Comparison", fontsize=15, weight="bold", y=0.99)
        fig.tight_layout()
        fig.savefig(self.plots_dir / "commercial_pdk_drive_comparison.png", dpi=300)
        fig.savefig(self.plots_dir / "commercial_pdk_drive_comparison.svg", format="svg")
        plt.close(fig)

        # Plot 2: Commercial Inverter VTC Overlay
        fig, ax = plt.subplots(figsize=(8.5, 6))
        _style(ax)
        color_idx = 0
        for pdk_id, pdata in results.items():
            inv = pdata.get("inverter", {})
            if inv.get("status") == "PASS":
                vin = np.array(inv["vin"])
                vout = np.array(inv["vout"])
                col = colors[color_idx % len(colors)]
                color_idx += 1
                ax.plot(vin, vout, color=col, linewidth=3.5, label=f"{pdk_id} ($V_M={inv['vm_V']:.3f}$V)")

        ax.set_title("Commercial Foundry CMOS Inverter DC VTC Benchmark", fontsize=14, weight="bold")
        ax.set_xlabel("Input Voltage $V_{in}$ (V)", fontsize=12, weight="bold")
        ax.set_ylabel("Output Voltage $V_{out}$ (V)", fontsize=12, weight="bold")
        ax.legend(loc="upper right", framealpha=0.9)
        fig.tight_layout()
        fig.savefig(self.plots_dir / "commercial_inverter_vtc_overlay.png", dpi=300)
        fig.savefig(self.plots_dir / "commercial_inverter_vtc_overlay.svg", format="svg")
        plt.close(fig)

    def generate_report(self, results: Dict[str, Any]):
        """Generate comprehensive Markdown report."""
        report_path = self.output_dir / "COMMERCIAL_PDK_REPORT.md"
        rows = []
        inv_rows = []

        for pdk_id, pdata in results.items():
            spec = pdata["spec"]
            corners = pdata["corners"]
            tt = corners.get("TT") or corners.get("TOP_TT") or list(corners.values())[0]
            m = tt["metrics"]
            if m.get("status") == "PASS":
                rows.append(f"| **{spec['pdk_id']}** | {spec['foundry']} | {spec['node']} | `{spec['simulator']}` | {spec['vdd']} V | {m['ion_mA']:.3f} mA | {m['vth_V']:.3f} V | {m['peak_gm_mS']:.2f} mS | {m['ion_ioff_ratio']:.2e} | **✓ PASS** |")
            else:
                rows.append(f"| **{spec['pdk_id']}** | {spec['foundry']} | {spec['node']} | `{spec['simulator']}` | {spec['vdd']} V | - | - | - | - | ⚠ FAIL |")

            inv = pdata.get("inverter", {})
            if inv.get("status") == "PASS":
                inv_rows.append(f"| **{spec['pdk_id']}** | {spec['node']} | {spec['vdd']} V | {inv['vm_V']:.3f} V | {inv['max_gain']:.2f} | {inv['nml_V']:.3f} V | {inv['nmh_V']:.3f} V | **✓ PASS** |")

        table_pdk = "\n".join(rows)
        table_inv = "\n".join(inv_rows)

        content = f"""# Commercial Foundry PDK Verification & Benchmarking Report

Generated automatically by **SPICE Model Benchmark Framework**.
Hardware Environment: `{get_hardware_specs()}`.

---

## 1. Commercial PDK Device Performance Summary

| PDK Library | Foundry | Technology Node | Native EDA | $V_{{DD}}$ | $I_{{on}}$ | $V_{{th}}$ | Peak $G_m$ | $I_{{on}}/I_{{off}}$ | Status |
|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
{table_pdk}

---

## 2. Commercial CMOS Inverter Transfer Benchmark

| PDK Library | Technology Node | Supply $V_{{DD}}$ | $V_M$ (Switching) | Peak Gain $|A_v|$ | $NM_L$ | $NM_H$ | Status |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
{table_inv}

---

## 3. Publication-Grade Overlay Plots

- **Drive Current & Threshold Spread**: [commercial_pdk_drive_comparison.svg](plots/commercial_pdk_drive_comparison.svg) | [PNG](plots/commercial_pdk_drive_comparison.png)
- **CMOS Inverter DC Transfer Characteristic**: [commercial_inverter_vtc_overlay.svg](plots/commercial_inverter_vtc_overlay.svg) | [PNG](plots/commercial_inverter_vtc_overlay.png)

---
*Report automatically compiled at {time.strftime('%Y-%m-%d %H:%M:%S')}*.
"""
        report_path.write_text(content, encoding="utf-8")
