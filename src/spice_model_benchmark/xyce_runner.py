"""
Xyce Simulation Runner.

Manages execution of XyceNF simulations, generates compatible netlists,
and coordinates post-processing for MOSFET device benchmarks.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any

from .logger import Logger
from .xyce_post_processor import XycePostProcessor


def _find_xyce_binary() -> Optional[Path]:
    """Locate Xyce binary on system."""
    candidates = [
        os.environ.get("XYCE_BIN"),
        "/home/yongfu/local/bin/xyce",
        shutil.which("xyce"),
        shutil.which("Xyce"),
    ]
    for c in candidates:
        if c and Path(c).is_file() and os.access(c, os.X_OK):
            return Path(c).resolve()
    return None


def _expand_includes(file_path: Path, visited=None) -> str:
    """Recursively expand .inc and .include files into a single flattened string."""
    if visited is None:
        visited = set()
    resolved_path = file_path.resolve()
    if resolved_path in visited or not resolved_path.exists():
        return ""
    visited.add(resolved_path)

    lines = resolved_path.read_text(errors="replace").splitlines()
    out = []
    base_dir = resolved_path.parent
    for line in lines:
        stripped = line.strip()
        m = re.match(r'^\s*\.(?:inc|include)\s+[\'"]?([^\'"\s]+)[\'"]?(.*)', stripped, re.IGNORECASE)
        if m:
            target = m.group(1)
            target_path = Path(target)
            if not target_path.is_absolute():
                target_path = (base_dir / target).resolve()
            if target_path.exists():
                out.append(f"* Inlined include: {target_path}")
                out.append(_expand_includes(target_path, visited))
            else:
                out.append(line)
        else:
            out.append(line)
    return "\n".join(out)


def _extract_model_info(model_file: Path) -> Tuple[str, str, int]:
    """Extract (nmos_name, pmos_name, level) from model file."""
    nmos, pmos = "nmos_vtg", "pmos_vtg"
    level = 54
    if not model_file.exists():
        return nmos, pmos, level

    try:
        content = _expand_includes(model_file)
        nm = re.search(r'\.model\s+(\w+)\s+(?:nmos|NMOS)', content)
        if nm:
            nmos = nm.group(1)
        pm = re.search(r'\.model\s+(\w+)\s+(?:pmos|PMOS)', content)
        if pm:
            pmos = pm.group(1)

        lev = re.search(r'level\s*=\s*(\d+)', content, re.IGNORECASE)
        if lev:
            level = int(lev.group(1))
    except Exception:
        pass

    return nmos, pmos, level


class XyceRunner:
    """Orchestrates Xyce benchmark simulations and results parsing."""

    def __init__(self,
                 logger: Optional[Logger] = None,
                 output_dir: str = "results_xyce",
                 model_file: Optional[str] = None,
                 model_name: Optional[str] = None):
        self.logger = logger or Logger()
        self.output_dir = Path(output_dir).resolve()
        self.work_dir = self.output_dir / "xyce_work"
        self.data_dir = self.output_dir / "data"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.model_file = Path(model_file).resolve() if model_file else None
        self.model_name = model_name
        self.xyce_bin = _find_xyce_binary()

        # Extract model info
        if self.model_file:
            self._nmos, self._pmos, self._raw_level = _extract_model_info(self.model_file)
            if self.model_name and self.model_name not in ["nmos_bsim4", "nmos_vtg"]:
                self._nmos = self.model_name
        else:
            self._nmos, self._pmos, self._raw_level = "nmos_vtg", "pmos_vtg", 54

        self.post_processor = XycePostProcessor(self.logger, str(self.output_dir))

    def _prepare_model_for_xyce(self) -> Path:
        """Adapt model file for Xyce compatibility (inlines includes, level=72 -> level=110, removes HSPICE wrappers)."""
        if not self.model_file or not self.model_file.exists():
            dummy = self.work_dir / "fallback_bsim4.mod"
            dummy.write_text(
                f".model {self._nmos} nmos level=54 version=4.5 vth0=0.4 u0=300 tox=1.5e-9\n"
                f".model {self._pmos} pmos level=54 version=4.5 vth0=-0.4 u0=150 tox=1.5e-9\n"
            )
            return dummy

        # In-line all nested includes to guarantee Xyce sees every model card
        content = _expand_includes(self.model_file)

        # Map Level 72 (HSPICE BSIM-CMG) to Level 110 (Xyce BSIM-CMG)
        if self._raw_level == 72 or "level=72" in content.lower():
            content = re.sub(r'level\s*=\s*72\b', 'level=110', content, flags=re.IGNORECASE)

        # Strip HSPICE-only wrapper keywords
        content = re.sub(r'^\s*\.lib\b.*', '', content, flags=re.MULTILINE | re.IGNORECASE)
        content = re.sub(r'^\s*\.endl\b.*', '', content, flags=re.MULTILINE | re.IGNORECASE)

        out_model = self.work_dir / f"xyce_flattened_{self.model_file.name}.mod"
        out_model.write_text(content)
        return out_model

    def _execute(self, netlist_path: Path) -> Tuple[bool, str]:
        """Run Xyce on a netlist."""
        if not self.xyce_bin:
            err = "Xyce executable not found."
            self.logger.logger.error(err)
            return False, err

        cmd = [str(self.xyce_bin), netlist_path.name]
        try:
            res = subprocess.run(
                cmd,
                cwd=str(netlist_path.parent),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=120
            )
            output = res.stdout + "\n" + res.stderr
            success = (res.returncode == 0) and not ("fatal error" in output.lower())
            if not success:
                self.logger.logger.warning(f"Xyce run failed on {netlist_path.name}:\n{output[:400]}")
            return success, output
        except Exception as e:
            self.logger.logger.error(f"Xyce exception: {e}")
            return False, str(e)

    def run_dc_simulation(self) -> bool:
        """Run complete set of DC benchmark simulations."""
        self.logger.logger.info("Executing Xyce DC Benchmark Simulations...")
        model_path = self._prepare_model_for_xyce()
        success = True

        # 1. Temperature sweeps (-40, 0, 25, 50, 100, 150)
        temps = ["-40", "0", "25", "50", "100", "150"]
        for t in temps:
            net_path = self.work_dir / f"dc_iv_{t}.cir"
            net_content = f"""* Xyce DC IV Sweep at Temp {t}C
.options device temp={t}
.include '{model_path.as_posix()}'

Vds d 0 DC 0
Vgs g 0 DC 0
Vs s 0 DC 0
Vb b 0 DC 0
M1 d g s b {self._nmos} L=0.045u W=10u

.dc Vds 0 1.2 0.02 Vgs 0 1.2 0.2
.print dc format=noindex v(d) v(g) i(Vds) i(Vs) i(Vb) i(Vgs)
.end
"""
            net_path.write_text(net_content)
            ok, _ = self._execute(net_path)
            if ok:
                prn = self.work_dir / f"dc_iv_{t}.cir.prn"
                self.post_processor.process_dc_iv(prn, temp=t)
            else:
                success = False

        # 2. Bias point operating analysis
        net_bias = self.work_dir / "dc_bias.cir"
        bias_content = f"""* Xyce DC Bias Point
.options device temp=27
.include '{model_path.as_posix()}'

Vds d 0 DC 1.0
Vgs g 0 DC 1.0
Vs s 0 DC 0
Vb b 0 DC 0
M1 d g s b {self._nmos} L=0.045u W=10u

.step temp list 27
.dc Vds 1.0 1.0 1.0
.print dc format=noindex v(d) v(g) i(Vds) i(Vgs) i(Vs) i(Vb)
.end
"""
        net_bias.write_text(bias_content)
        ok_b, _ = self._execute(net_bias)
        if ok_b:
            self.post_processor.process_bias_point(self.work_dir / "dc_bias.cir.prn")

        # 3. Gummel Symmetry Test (GST)
        net_gst = self.work_dir / "dc_gst.cir"
        gst_content = f"""* Xyce Gummel Symmetry Test
.options device temp=27
.include '{model_path.as_posix()}'

Vx vx 0 DC 0
Ed d 0 vx 0 0.5
Es s 0 vx 0 -0.5
Vg g 0 DC 0.6
Vb b 0 DC 0
Vsens_d d d_int DC 0
Vsens_s s s_int DC 0
M1 d_int g s_int b {self._nmos} L=0.045u W=10u

.dc Vx -0.2 0.2 0.002
.print dc format=noindex v(vx) i(Vsens_d) i(Vsens_s)
.end
"""
        net_gst.write_text(gst_content)
        ok_g, _ = self._execute(net_gst)
        if ok_g:
            self.post_processor.process_gst(self.work_dir / "dc_gst.cir.prn")

        # 4. Zero-Bias Passivity
        net_zb = self.work_dir / "dc_zero_bias.cir"
        zb_content = f"""* Xyce Zero Bias Passivity
.options device temp=27
.include '{model_path.as_posix()}'

Vd d 0 DC 0
Vg g 0 DC 0
Vs s 0 DC 0
Vb b 0 DC 0
M1 d g s b {self._nmos} L=0.045u W=10u

.dc Vd 0 0 1
.print dc format=noindex i(Vd) i(Vg) i(Vs) i(Vb)
.end
"""
        net_zb.write_text(zb_content)
        ok_zb, _ = self._execute(net_zb)
        if ok_zb:
            self.post_processor.process_zero_bias(self.work_dir / "dc_zero_bias.cir.prn")

        # 5. Transfer characteristics (Id vs Vgs, derivatives)
        net_tr = self.work_dir / "dc_transfer.cir"
        tr_content = f"""* Xyce Transfer Characteristics
.options device temp=27
.include '{model_path.as_posix()}'

Vd d 0 DC 1.0
Vg g 0 DC 0
Vs s 0 DC 0
Vb b 0 DC 0
M1 d g s b {self._nmos} L=0.045u W=10u

.dc Vg 0 1.2 0.005
.print dc format=noindex v(g) i(Vd)
.end
"""
        net_tr.write_text(tr_content)
        ok_tr, _ = self._execute(net_tr)
        if ok_tr:
            self.post_processor.process_transfer(self.work_dir / "dc_transfer.cir.prn")

        # 6. Output conductance (Id vs Vds, derivatives)
        net_out = self.work_dir / "dc_output.cir"
        out_content = f"""* Xyce Output Conductance
.options device temp=27
.include '{model_path.as_posix()}'

Vd d 0 DC 0
Vg g 0 DC 1.0
Vs s 0 DC 0
Vb b 0 DC 0
M1 d g s b {self._nmos} L=0.045u W=10u

.dc Vd 0 1.2 0.005
.print dc format=noindex v(d) i(Vd)
.end
"""
        net_out.write_text(out_content)
        ok_out, _ = self._execute(net_out)
        if ok_out:
            self.post_processor.process_output(self.work_dir / "dc_output.cir.prn")

        # 7. Asymptotic Extrapolation
        net_asymp = self.work_dir / "dc_asymptotic.cir"
        asymp_content = f"""* Xyce Asymptotic Extrapolation
.options device temp=27
.include '{model_path.as_posix()}'

Vd d 0 DC 1.0
Vg g 0 DC -2.0
Vs s 0 DC 0
Vb b 0 DC 0
M1 d g s b {self._nmos} L=0.045u W=10u

.dc Vg -2.0 2.5 0.02
.print dc format=noindex v(g) i(Vd)
.end
"""
        net_asymp.write_text(asymp_content)
        ok_asymp, _ = self._execute(net_asymp)
        if ok_asymp:
            self.post_processor.process_asymptotic(self.work_dir / "dc_asymptotic.cir.prn")

        return success

    def run_ac_simulation(self) -> bool:
        """Run AC benchmark simulation in Xyce."""
        self.logger.logger.info("Executing Xyce AC Benchmark Simulations...")
        model_path = self._prepare_model_for_xyce()

        # AC CV sweep
        net_ac = self.work_dir / "ac_cv.cir"
        ac_content = f"""* Xyce AC Capacitance Sweep
.options device temp=27
.include '{model_path.as_posix()}'

Vg g 0 DC 0 AC 1.0
Vd d 0 DC 1.0
Vs s 0 DC 0
Vb b 0 DC 0
M1 d g s b {self._nmos} L=0.045u W=10u

.step Vg -1.2 1.2 0.05
.ac lin 1 1e6 1e6
.print ac format=noindex v(g) i(Vg)
.end
"""
        net_ac.write_text(ac_content)
        ok_ac, _ = self._execute(net_ac)
        if ok_ac:
            self.post_processor.process_ac_cv(self.work_dir / "ac_cv.cir.prn")

        # Dynamic self heating AC sweep
        net_sh = self.work_dir / "ac_self_heating.cir"
        sh_content = f"""* Xyce AC Admittance / Dynamic Self-Heating Sweep
.options device temp=27
.include '{model_path.as_posix()}'

Vd d 0 DC 1.0 AC 1.0
Vg g 0 DC 1.0
Vs s 0 DC 0
Vb b 0 DC 0
M1 d g s b {self._nmos} L=0.045u W=10u

.ac dec 10 1 100G
.print ac format=noindex frequency ir(Vd) ii(Vd)
.end
"""
        net_sh.write_text(sh_content)
        ok_sh, _ = self._execute(net_sh)
        if ok_sh:
            self.post_processor.process_self_heating(self.work_dir / "ac_self_heating.cir.prn")

        return ok_ac or ok_sh

    def run_transient_simulation(self) -> bool:
        """Run transient benchmark simulations in Xyce."""
        self.logger.logger.info("Executing Xyce Transient Benchmark Simulations...")
        model_path = self._prepare_model_for_xyce()

        # Large-signal pulse response
        net_tran = self.work_dir / "tran_pulse.cir"
        tran_content = f"""* Xyce Transient Large Signal Pulse
.options device temp=27
.include '{model_path.as_posix()}'

Vin in 0 PULSE(0 1.0 100p 50p 50p 1n 2n)
Vdd d 0 DC 1.0
Vs s 0 DC 0
Vb b 0 DC 0
M1 d in s b {self._nmos} L=0.045u W=10u

.tran 10p 3n
.print tran format=noindex time v(in) v(d) i(Vdd)
.end
"""
        net_tran.write_text(tran_content)
        ok, _ = self._execute(net_tran)
        return ok

    def run_noise_simulation(self) -> bool:
        """Run noise simulation in Xyce."""
        self.logger.logger.info("Executing Xyce Noise Benchmark Simulations...")
        model_path = self._prepare_model_for_xyce()

        net_noise = self.work_dir / "noise.cir"
        noise_content = f"""* Xyce Noise Simulation
.options device temp=27
.include '{model_path.as_posix()}'

Vin in 0 DC 0.6 AC 1.0
Vdd d 0 DC 0.6
Vs s 0 DC 0
Vb b 0 DC 0
M1 d in s b {self._nmos} L=0.045u W=10u

.noise v(d) Vin dec 10 1 10G
.print noise format=noindex frequency onoise inoise
.end
"""
        net_noise.write_text(noise_content)
        ok, _ = self._execute(net_noise)
        return ok

    def run_simulations_by_mode(self, modes: List[str]) -> bool:
        """Execute simulations for selected analysis modes."""
        status = True
        if "dc" in modes:
            status = self.run_dc_simulation() and status
        if "ac" in modes:
            status = self.run_ac_simulation() and status
        if "transient" in modes:
            status = self.run_transient_simulation() and status
        if "noise" in modes:
            status = self.run_noise_simulation() and status
        return status
