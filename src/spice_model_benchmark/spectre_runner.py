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
SPECTRE_BIN = f"{SPECTRE_HOME}/tools.lnx86/spectre/bin/64bit/spectre"
CDS_LIC_FILE = "/eda/cadence/license.dat"


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
                 ac_circuit_file: Optional[str] = None):
        self.logger = logger
        self.output_dir = output_dir

        self.dc_circuit_file = Path(dc_circuit_file) if dc_circuit_file else None
        self.transient_circuit_file = Path(transient_circuit_file) if transient_circuit_file else None
        self.noise_circuit_file = Path(noise_circuit_file) if noise_circuit_file else None
        self.ac_circuit_file = Path(ac_circuit_file) if ac_circuit_file else None

        self.output_dir_path = Path(output_dir).resolve()
        self.output_dir_path.mkdir(exist_ok=True)

        self.data_dir = self.output_dir_path / 'data'
        self.data_dir.mkdir(exist_ok=True)

        self.raw_dir = self.output_dir_path / 'spectre_raw'
        self.raw_dir.mkdir(exist_ok=True)

        self.post_processor = SpectrePostProcessor(logger, str(self.data_dir))
        self._env = _build_spectre_env()

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
                    text=True,
                    env=self._env
                )
                stdout, stderr = process.communicate(timeout=600)

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
        if not self.run_simulation(self.dc_circuit_file, "dc"):
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
        if not self.run_simulation(self.ac_circuit_file, "ac"):
            return False

        raw_path = self.raw_dir / "ac"
        if raw_path.exists():
            self.post_processor.process_ac(raw_path)

        return True

    def run_transient_simulation(self) -> bool:
        if not self.transient_circuit_file or not self.transient_circuit_file.exists():
            self.logger.logger.error(f"Transient circuit file not found: {self.transient_circuit_file}")
            return False

        self.logger.logger.info("Starting Spectre transient analysis...")
        if not self.run_simulation(self.transient_circuit_file, "transient"):
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
        if not self.run_simulation(self.noise_circuit_file, "noise"):
            return False

        raw_path = self.raw_dir / "noise"
        if raw_path.exists():
            self.post_processor.process_noise(raw_path)

        return True

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
