"""
Spectre Simulation Runner: Execute spectre simulations and manage output files.

Parallel to SimulationRunner (ngspice) but invokes spectre instead.
"""
import os
import subprocess
from pathlib import Path
from typing import Optional, List, Union
import shutil
import re

from .spectre_post_processor import SpectrePostProcessor


# Spectre installation paths
SPECTRE_HOME = "/eda/cadence/SPECTRE241"
SPECTRE_BIN = f"{SPECTRE_HOME}/bin/spectre"
CDS_LIC_FILE = "/eda/license/cadence.dat"


def _build_spectre_env() -> dict:
    """Build environment variables dictionary for running spectre."""
    env = os.environ.copy()

    # Library paths
    lib64_dirs = []
    lib_dirs = []
    for root, dirs, files in os.walk(f"{SPECTRE_HOME}/tools.lnx86"):
        depth = root.replace(f"{SPECTRE_HOME}/tools.lnx86", "").count(os.sep)
        if depth > 4:
            continue
        if os.path.basename(root) == "64bit":
            lib64_dirs.append(root)
        elif os.path.basename(root) == "lib" and "64bit" not in root:
            lib_dirs.append(root)

    # Also add TPtools
    tp_root = f"{SPECTRE_HOME}/tools.lnx86/TPtools"
    if os.path.exists(tp_root):
        for root, dirs, files in os.walk(tp_root):
            depth = root.replace(tp_root, "").count(os.sep)
            if depth > 3:
                continue
            if os.path.basename(root) == "lib64":
                lib64_dirs.append(root)

    ld_path = ":".join(lib64_dirs + lib_dirs)
    existing_ld = env.get("LD_LIBRARY_PATH", "")
    if existing_ld:
        ld_path = f"{ld_path}:{existing_ld}"

    env["LD_LIBRARY_PATH"] = ld_path
    env["PATH"] = f"{SPECTRE_HOME}/tools.lnx86/spectre/bin/64bit:{SPECTRE_HOME}/tools.lnx86/spectre/bin:{SPECTRE_HOME}/bin:{env.get('PATH', '')}"
    env["CDS_LIC_FILE"] = CDS_LIC_FILE

    return env


class SpectreRunner:
    """Handles running Spectre simulations and managing output files.

    Attributes:
        logger: Logger instance
        output_dir: Directory where simulation results will be stored
        dc_circuit_file: Path to DC analysis circuit file (.scs)
        ac_circuit_file: Path to AC analysis circuit file (.scs)
        transient_circuit_file: Path to transient circuit file (.scs)
        noise_circuit_file: Path to noise circuit file (.scs)
    """

    def __init__(self,
                 logger,
                 output_dir: str = 'results',
                 dc_circuit_file: Optional[str] = None,
                 transient_circuit_file: Optional[str] = None,
                 noise_circuit_file: Optional[str] = None,
                 ac_circuit_file: Optional[str] = None,
                 model_file: Optional[str] = None,
                 model_name: Optional[str] = None):
        self.logger = logger
        self.output_dir = output_dir

        self.dc_circuit_file = Path(dc_circuit_file) if dc_circuit_file else None
        self.transient_circuit_file = Path(transient_circuit_file) if transient_circuit_file else None
        self.noise_circuit_file = Path(noise_circuit_file) if noise_circuit_file else None
        self.ac_circuit_file = Path(ac_circuit_file) if ac_circuit_file else None
        self.model_file = Path(model_file).resolve() if model_file else None
        self.model_name = model_name or "nmos_bsim4"

        self.output_dir_path = Path(output_dir).resolve()
        self.output_dir_path.mkdir(exist_ok=True)

        self.data_dir = self.output_dir_path / 'data'
        self.data_dir.mkdir(exist_ok=True)

        self.raw_dir = self.output_dir_path / 'spectre_raw'
        self.raw_dir.mkdir(exist_ok=True)

        self._work_dir = self.output_dir_path / 'spectre_work'
        self._work_dir.mkdir(exist_ok=True)

        # Extract model names from model file
        self._nmos, self._pmos = "NMOS_VTG", "PMOS_VTG"
        if self.model_file and self.model_file.exists():
            try:
                content = self.model_file.read_text(errors='replace')
                nm = re.search(r'\.model\s+(\w+)\s+(?:nmos|NMOS)', content)
                pm = re.search(r'\.model\s+(\w+)\s+(?:pmos|PMOS)', content)
                if nm: self._nmos = nm.group(1)
                if pm: self._pmos = pm.group(1)
            except Exception:
                pass
        self._has_pmos = self._pmos != "PMOS_VTG"

        self.post_processor = SpectrePostProcessor(logger, str(self.data_dir))
        self._env = _build_spectre_env()

    def _prepare_circuit(self, circuit_file: Path) -> Path:
        """Copy circuit file to work dir, substituting model include and model names."""
        if not circuit_file or not circuit_file.exists():
            return circuit_file

        content = circuit_file.read_text(errors='replace')

        # Replace model include path
        if self.model_file:
            content = re.sub(
                r'\.inc\s+.*?FreePDK45/nom\.inc',
                f".inc '{self.model_file}'",
                content
            )

        # Track if PMOS was present in original content
        needs_pmos = 'PMOS_VTG' in content

        # Replace model names
        content = content.replace('NMOS_VTG', self._nmos)
        content = content.replace('PMOS_VTG', self._pmos)

        # If no PMOS found in model, inject a basic PMOS model
        if not self._has_pmos and needs_pmos:
            pmos_model = (
                f"\n* Auto-generated PMOS model (no PMOS found in source)\n"
                f".model {self._pmos} PMOS ( LEVEL=54 VERSION=4.5\n"
                f"+ VTH0=-0.4 TOX=1.4e-9 U0=150 VSAT=80000\n"
                f"+ RDSW=200 ETA0=0.08 PCLM=1.2 PDIBLC1=0.4 PDIBLC2=0.001\n"
                f"+ DROUT=0.5 PSCBE1=5e8 PSCBE2=1e-5 PVAG=0.01 DELTA=0.01\n"
                f"+ A0=1.1 AGS=0.25 A1=0 A2=1 B0=0 B1=0 K1=0.4\n"
                f"+ K2=0.01 K3=0 K3B=0 W0=2.5e-6 DVT0=1.5 DVT1=0.45\n"
                f"+ DVT2=0.02 DSUB=0.2 CIT=0 CDSC=2.4e-4 CDSCB=0 CDSCD=0\n"
                f"+ NFACTOR=1.5 XJ=1e-8 LINT=1e-9 WINT=1e-9 DWG=0 DWB=0\n"
                f"+ VOFF=-0.1 MINV=1 CKAPPA=0.6 CGDO=5e-10 CGSO=5e-10\n"
                f"+ CGBO=1e-12 CJ=0.001 MJ=0.5 PB=0.9 CJSW=1e-10\n"
                f"+ MJSW=0.33 PBSW=0.9 CF=0 PVTH0=0 PRDSW=0 PK2=0\n"
                f"+ WKETA=0 LKETA=0 PU0=0 PUA=0 PUB=0\n"
                f"+ TNOM=27 UTE=-1.5 KT1=-0.11 KT1L=0 KT2=0.022 UA1=4.31e-9\n"
                f"+ UB1=-7.61e-18 UC1=-5.6e-11 AT=33000 PRT=0\n"
                f"+ WL=0 WLN=1 WW=-1e-15 WWN=1 WWL=0 LL=0 LLN=1\n"
                f"+ LW=0 LWN=1 LWL=0\n"
                f"+ CAPMOD=2 XPART=0.5\n"
                f"+ JSS=1e-7 JSWS=1e-12 JSWGS=1e-12 NJS=1 XTI=3\n"
                f"+ CLC=0.1e-6 CLE=0.6 NOFF=1 VOFFCV=0\n"
                f"+ )\n"
            )
            # Inject after the .inc line (inside simulator lang=spice section)
            content = content.replace(
                f".inc '{self.model_file}'",
                f".inc '{self.model_file}'\n{pmos_model}"
            )

        # Write to work directory
        work_path = self._work_dir / circuit_file.name
        work_path.write_text(content)
        self.logger.logger.info(f"Prepared circuit: {work_path} (model={self._nmos}/{self._pmos})")
        return work_path

    def run_simulation(self, circuit_file: Union[str, Path], analysis_type: str) -> bool:
        """Run spectre simulation for a single circuit file.

        Args:
            circuit_file: Path to the .scs netlist file
            analysis_type: Type of analysis (dc, ac, trans, noise) for naming

        Returns:
            bool: True if successful
        """
        try:
            circuit_path = Path(circuit_file).resolve()
            if not circuit_path.exists():
                self.logger.logger.error(f"Circuit file not found: {circuit_path}")
                return False

            self.logger.logger.info(f"Starting Spectre {analysis_type} simulation: {circuit_path.name}")

            circuit_dir = circuit_path.parent
            original_dir = Path.cwd()

            try:
                os.chdir(circuit_dir)

                # Use -format psfascii for parseable output
                raw_name = f"raw_{analysis_type}"
                cmd = [
                    SPECTRE_BIN,
                    '-raw', raw_name,
                    '-format', 'psfascii',
                    circuit_path.name
                ]

                self.logger.logger.info(f"Running: {' '.join(cmd)}")
                self.logger.logger.info(f"Working dir: {circuit_dir}")

                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=self._env
                )
                stdout_b, stderr_b = process.communicate(timeout=600)
                stdout = stdout_b.decode('utf-8', errors='replace') if stdout_b else ''
                stderr = stderr_b.decode('utf-8', errors='replace') if stderr_b else ''

                if stdout:
                    self.logger.logger.debug(f"Spectre stdout:\n{stdout[-2000:]}")
                if stderr:
                    self.logger.logger.debug(f"Spectre stderr:\n{stderr[-2000:]}")

                if process.returncode != 0:
                    self.logger.logger.error(f"Spectre failed (rc={process.returncode}): {stderr[-500:]}")
                    return False

                # Move raw directory to output
                raw_src = circuit_dir / raw_name
                if raw_src.exists():
                    raw_dst = self.raw_dir / analysis_type
                    if raw_dst.exists():
                        shutil.rmtree(raw_dst)
                    shutil.move(str(raw_src), str(raw_dst))
                    self.logger.logger.info(f"Moved raw output to: {raw_dst}")
                else:
                    # Spectre might have created raw_name as a file not dir
                    raw_file = Path(str(raw_src))
                    if raw_file.exists():
                        raw_dst = self.raw_dir / analysis_type
                        if raw_dst.exists():
                            shutil.rmtree(raw_dst)
                        shutil.move(str(raw_src), str(raw_dst))

                self.logger.logger.info(f"Spectre {analysis_type} simulation completed")
                return True

            finally:
                os.chdir(original_dir)

        except subprocess.TimeoutExpired:
            self.logger.logger.error(f"Spectre {analysis_type} simulation timed out")
            process.kill()
            return False
        except Exception as e:
            self.logger.logger.error(f"Error running Spectre {analysis_type}: {e}", exc_info=True)
            return False

    def run_dc_simulation(self) -> bool:
        if not self.dc_circuit_file or not self.dc_circuit_file.exists():
            self.logger.logger.error(f"DC circuit file not found: {self.dc_circuit_file}")
            return False

        self.logger.logger.info("Starting Spectre DC analysis...")
        circuit = self._prepare_circuit(self.dc_circuit_file)
        if not self.run_simulation(circuit, "dc"):
            return False

        # Post-process
        raw_path = self.raw_dir / "dc"
        if raw_path.exists():
            self.post_processor.process_dc(raw_path)

        return True

    def run_ac_simulation(self) -> bool:
        if not self.ac_circuit_file or not self.ac_circuit_file.exists():
            self.logger.logger.error(f"AC circuit file not found: {self.ac_circuit_file}")
            return False

        self.logger.logger.info("Starting Spectre AC analysis...")
        circuit = self._prepare_circuit(self.ac_circuit_file)
        if not self.run_simulation(circuit, "ac"):
            return False

        # Run auxiliary SP and NQS netlists
        aux_dir = self.ac_circuit_file.parent
        for aux_name, tag in [("_sp.scs", "ac_sp"), ("_nqs.scs", "ac_nqs")]:
            aux_path = aux_dir / aux_name
            if aux_path.exists():
                self.logger.logger.info(f"Running auxiliary {tag}...")
                aux_prepared = self._prepare_circuit(aux_path)
                self.run_simulation(aux_prepared, tag)

        raw_path = self.raw_dir / "ac"
        if raw_path.exists():
            self.post_processor.process_ac(raw_path)

        return True

    def run_transient_simulation(self) -> bool:
        if not self.transient_circuit_file or not self.transient_circuit_file.exists():
            self.logger.logger.error(f"Transient circuit file not found: {self.transient_circuit_file}")
            return False

        self.logger.logger.info("Starting Spectre transient analysis...")
        circuit = self._prepare_circuit(self.transient_circuit_file)
        if not self.run_simulation(circuit, "transient"):
            return False

        raw_path = self.raw_dir / "transient"
        if raw_path.exists():
            self.post_processor.process_transient(raw_path)

        return True

    def run_noise_simulation(self) -> bool:
        if not self.noise_circuit_file or not self.noise_circuit_file.exists():
            self.logger.logger.error(f"Noise circuit file not found: {self.noise_circuit_file}")
            return False

        self.logger.logger.info("Starting Spectre noise analysis...")
        circuit = self._prepare_circuit(self.noise_circuit_file)
        if not self.run_simulation(circuit, "noise"):
            return False

        # Run auxiliary noise netlists for all bias points and temperatures
        aux_dir = self.noise_circuit_file.parent
        self._run_aux_noise_netlists(aux_dir)

        raw_path = self.raw_dir / "noise"
        if raw_path.exists():
            self.post_processor.process_noise(raw_path)

        return True

    def _run_aux_noise_netlists(self, aux_dir: Path):
        """Generate and run auxiliary noise netlists for all bias points and temps."""
        model_inc = str(self.model_file) if self.model_file else "../../models/FreePDK45/nom.inc"
        mname = self._nmos  # Use extracted NMOS model name

        # 5 additional thermal noise bias points (Vgs=0.6,Vds=0.6 is in main netlist)
        bias_points = [
            ("0.3", "0.3"), ("0.3", "0.6"), ("0.3", "0.9"),
            ("0.3", "1.2"), ("0.6", "0.3"),
        ]
        for vgs, vds in bias_points:
            tag = f"noise_vgs{vgs}_vds{vds}"
            netlist = (
                f"simulator lang=spice\n"
                f".option temp=27 tnom=27 gmin=1e-15\n"
                f".include '{model_inc}'\n"
                f"Vdd_n vdd_n 0 DC 1.2\n"
                f"Vin_n in_n 0 DC {vgs} AC 1\n"
                f"Rb_n in_n gate_n 1k\nRd_n vdd_n drain_n 10k\nRs_n source_n 0 100\n"
                f"M_n drain_n gate_n source_n 0 {mname} L=0.045u W=10u\n"
                f"Vgs_n gate_n source_n DC {vgs}\nVds_n drain_n source_n DC {vds}\n"
                f".noise v(drain_n) Vin_n dec 20 1 1G\n"
            )
            self._run_aux_netlist(aux_dir, tag, netlist)

        # Temperature noise at -40C and 100C (27C in main, others interpolated)
        for temp in ["-40", "100"]:
            tag = f"noise_t{temp}"
            netlist = (
                f"simulator lang=spice\n"
                f".option temp={temp} tnom=27 gmin=1e-15\n"
                f".include '{model_inc}'\n"
                f"Vdd_n vdd_n 0 DC 1.2\n"
                f"Vin_n in_n 0 DC 0.6 AC 1\n"
                f"Rb_n in_n gate_n 1k\nRd_n vdd_n drain_n 10k\nRs_n source_n 0 100\n"
                f"M_n drain_n gate_n source_n 0 {mname} L=0.045u W=10u\n"
                f"Vgs_n gate_n source_n DC 0.6\nVds_n drain_n source_n DC 0.6\n"
                f".noise v(drain_n) Vin_n dec 20 1 1G\n"
            )
            self._run_aux_netlist(aux_dir, tag, netlist)

    def _run_aux_netlist(self, aux_dir: Path, tag: str, netlist_content: str):
        """Write and run an auxiliary spectre netlist."""
        scs_path = aux_dir / f"_{tag}.scs"
        try:
            with open(scs_path, 'w') as f:
                f.write(netlist_content)
            self.run_simulation(scs_path, tag)
        except Exception as e:
            self.logger.logger.warning(f"Aux netlist {tag} failed: {e}")

    def run_simulations_by_mode(self, modes: List[str]) -> bool:
        """Run simulations based on selected modes."""
        if 'all' in modes:
            modes = ['dc', 'ac', 'transient', 'noise']

        success = True

        for mode in modes:
            if mode == 'dc':
                if not self.run_dc_simulation():
                    success = False
            elif mode == 'ac':
                if not self.run_ac_simulation():
                    success = False
            elif mode == 'transient':
                if not self.run_transient_simulation():
                    success = False
            elif mode == 'noise':
                if not self.run_noise_simulation():
                    success = False

        if success:
            self.logger.logger.info("All Spectre simulations completed successfully")
        return success
