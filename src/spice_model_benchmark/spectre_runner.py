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
from .fixture_geometry import apply_primary_geometry, read_geometry_override


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

        # Extract model names from the explicitly supplied model file.  A
        # malformed or empty input is an error; it must never select a bundled
        # device model as the benchmark target.
        if not self.model_file or not self.model_file.is_file():
            raise ValueError(
                "Spectre benchmark requires an explicit MOS model file; "
                "fallback models are disabled"
            )
        content = self.model_file.read_text(errors='replace')
        cards = [
            (match.group(1), match.group(2).lower())
            for match in re.finditer(
                r'(?i)\.model\s+(\S+)\s+(nmos|pmos)\b',
                content,
            )
        ]
        source_cards = [
            card for card in cards
            if not card[0].lower().startswith('__fixture_')
        ]
        if not source_cards:
            raise ValueError(
                f"No non-fixture MOS model card found in {self.model_file}; "
                "Spectre benchmark fallback models are disabled"
            )
        selected_match = re.search(
            r'(?im)^\s*\*\s*BENCHMARK_PRIMARY_MODEL:\s*(\S+)\s*$',
            content,
        )
        selected_card = None
        if selected_match:
            selected_name = selected_match.group(1)
            selected_card = next(
                (
                    card
                    for card in source_cards
                    if card[0].lower() == selected_name.lower()
                ),
                None,
            )
            if selected_card is None:
                raise ValueError(
                    f"Selected benchmark card {selected_name} is not present "
                    f"in {self.model_file}"
                )
        source_nmos = next(
            (re.sub(r'\.\d+$', '', name) for name, kind in source_cards if kind == 'nmos'),
            None,
        )
        source_pmos = next(
            (re.sub(r'\.\d+$', '', name) for name, kind in source_cards if kind == 'pmos'),
            None,
        )
        if selected_card is not None:
            if selected_card[1] == 'nmos':
                source_nmos = selected_card[0]
            else:
                source_pmos = selected_card[0]
        fixture_nmos = next(
            (name for name, kind in cards if kind == 'nmos' and name.lower().startswith('__fixture_')),
            None,
        )
        fixture_pmos = next(
            (name for name, kind in cards if kind == 'pmos' and name.lower().startswith('__fixture_')),
            None,
        )
        self._nmos = source_nmos or fixture_nmos
        self._pmos = source_pmos or fixture_pmos
        if self._nmos is None or self._pmos is None:
            missing = "NMOS" if self._nmos is None else "PMOS"
            raise ValueError(
                f"Spectre benchmark circuit requires an explicit {missing} "
                "model card; fallback models are disabled"
            )
        self._primary = source_nmos or source_pmos
        self._primary_is_pmos = source_nmos is None and source_pmos is not None
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
                r"(?im)^\s*\.(?:inc|include)\s+.*$",
                f".inc '{Path(self.model_file).resolve()}'",
                content,
            )
            content = re.sub(
                r'(?im)^\s*include\s+(?:".*?"|\'.*?\'|\S+)\s*$',
                (
                    "simulator lang=spice\n"
                    f".inc '{Path(self.model_file).resolve()}'\n"
                    "simulator lang=spectre"
                ),
                content,
            )

        single_instances = (
            r'(?:M_iv|M_bias|M\d+|Msp|Mnqs|M_noise\d+|M_fl|M_sh|'
            r'M_noise|M_flicker|M_shot|M_tran|M_qs|M_charge)'
        )
        content = re.sub(
            rf'(?im)^(\s*{single_instances}\b(?:\s+\S+){{4}}\s+)\S+',
            rf'\g<1>{self._primary}',
            content,
        )
        content = re.sub(
            rf'(?im)^(\s*{single_instances}\s*\([^)]*\)\s+)\S+',
            rf'\g<1>{self._primary}',
            content,
        )

        # Replace model names
        content = content.replace('NMOS_VTG', self._nmos)
        content = content.replace('PMOS_VTG', self._pmos)
        content = apply_primary_geometry(
            content,
            self._primary,
            read_geometry_override(self.model_file),
        )

        if self._primary_is_pmos:
            name = circuit_file.name.lower()

            def flip_number(token: str) -> str:
                value = float(token)
                if value == 0.0:
                    return token
                # This adapter may receive a deck already normalized by the
                # shared benchmark front end.  Keep PMOS biasing negative on
                # repeated application instead of toggling its polarity.
                return f"{-abs(value):g}"

            if name.startswith('dc_'):
                content = re.sub(
                    r'(?im)^(\s*(?:sw_vgs|sw_vds_bias|sw_vgs_bias)\b.*)$',
                    lambda match: re.sub(
                        r'(?<![\w.-])([+]?(?:\d+(?:\.\d*)?|\.\d+))(?![\w.])',
                        lambda number: flip_number(number.group(1)),
                        match.group(1),
                    ),
                    content,
                )
                content = re.sub(
                    r'(?im)^(\s*dc_(?:iv|bias)\b.*)$',
                    lambda match: re.sub(
                        r'\b(start|stop|step)=([+]?(?:\d+(?:\.\d*)?|\.\d+))',
                        lambda number: (
                            number.group(1) + "=" + flip_number(number.group(2))
                        ),
                        match.group(1),
                    ),
                    content,
                )
            elif name.startswith('ac_') or name in {'_sp.scs', '_nqs.scs'}:
                content = re.sub(
                    r'(?im)^(\s*V(?:G|D)\w*\b.*?\bDC\s+)([-+]?(?:\d+(?:\.\d*)?|\.\d+))',
                    lambda match: match.group(1) + flip_number(match.group(2)),
                    content,
                )
            elif name.startswith('transient_'):
                selected_sources = r'(?:Vgs_tran|Vds_tran|Vgs_qs|Vds_qs|Vg_charge|Vd_charge)'
                content = re.sub(
                    rf'(?im)^(\s*{selected_sources}\b.*?\bdc=)([-+]?(?:\d+(?:\.\d*)?|\.\d+))',
                    lambda match: match.group(1) + flip_number(match.group(2)),
                    content,
                )
                content = re.sub(
                    rf'(?im)^(\s*{selected_sources}\b.*\\\s*\n\s*val0=0\s+val1=)'
                    r'([-+]?(?:\d+(?:\.\d*)?|\.\d+))',
                    lambda match: match.group(1) + flip_number(match.group(2)),
                    content,
                )
            elif name.startswith('noise_') or name.startswith('_noise_'):
                content = re.sub(
                    r'(?im)^(\s*V(?:dd|in|gs|ds)\w*\b.*?\bDC\s+)'
                    r'([-+]?(?:\d+(?:\.\d*)?|\.\d+))',
                    lambda match: match.group(1) + flip_number(match.group(2)),
                    content,
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
                stdout_b, stderr_b = process.communicate()
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
            return self.post_processor.process_dc(raw_path)

        return False

    def run_ac_simulation(self) -> bool:
        if not self.ac_circuit_file or not self.ac_circuit_file.exists():
            self.logger.logger.error(f"AC circuit file not found: {self.ac_circuit_file}")
            return False

        self.logger.logger.info("Starting Spectre AC analysis...")
        circuit = self._prepare_circuit(self.ac_circuit_file)
        if not self.run_simulation(circuit, "ac"):
            return False

        raw_path = self.raw_dir / "ac"
        if raw_path.exists():
            return self.post_processor.process_ac(raw_path)

        return False

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
            return self.post_processor.process_transient(raw_path)

        return False

    def run_noise_simulation(self) -> bool:
        if not self.noise_circuit_file or not self.noise_circuit_file.exists():
            self.logger.logger.error(f"Noise circuit file not found: {self.noise_circuit_file}")
            return False

        self.logger.logger.info("Starting Spectre noise analysis...")
        circuit = self._prepare_circuit(self.noise_circuit_file)
        if not self.run_simulation(circuit, "noise"):
            return False

        raw_path = self.raw_dir / "noise"
        if raw_path.exists():
            return self.post_processor.process_noise(raw_path)

        return False

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
