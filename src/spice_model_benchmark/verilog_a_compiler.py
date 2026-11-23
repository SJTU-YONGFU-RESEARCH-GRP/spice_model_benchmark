"""Verilog-A Model Compiler and Quality Assurance using OpenVAF.

Automates the compilation of Verilog-A compact models (.va) into OSDI (.osdi)
shared libraries for ngspice and SPICE-class simulators. Evaluates syntax correctness,
automatic differentiation Jacobian generation, and compilation performance.
Based on McAndrew TED 2025 (Table I Item 13) and NeuralCM-QA (IEEE TCAD 2026).
"""

import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

from spice_model_benchmark.logger import Logger


class VerilogACompiler:
    """Manages OpenVAF compilation for Verilog-A compact models."""

    def __init__(self, openvaf_bin: Optional[str] = None, logger: Optional[Logger] = None):
        self.logger = logger or Logger()
        self.openvaf_bin = openvaf_bin or self._find_openvaf()

    def _find_openvaf(self) -> Optional[str]:
        """Locate OpenVAF executable in standard locations or PATH."""
        candidates = [
            "/usr/local/bin/openvaf",
            "/usr/bin/openvaf",
            shutil.which("openvaf"),
        ]
        for c in candidates:
            if c and os.path.exists(c) and os.access(c, os.X_OK):
                return c
        return None

    def is_available(self) -> bool:
        """Check if OpenVAF is installed and accessible."""
        return self.openvaf_bin is not None

    def get_version(self) -> Optional[str]:
        """Get the installed OpenVAF version."""
        if not self.is_available():
            return None
        try:
            res = subprocess.run([self.openvaf_bin, "--version"], capture_output=True, text=True, check=True)
            return res.stdout.strip()
        except Exception as e:
            self.logger.warning(f"Could not determine OpenVAF version: {e}")
            return None

    def compile(self, va_path: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """Compile a Verilog-A (.va) file into an OSDI (.osdi) library.
        
        Args:
            va_path (str): Path to the .va compact model file
            output_dir (str, optional): Target directory for compiled .osdi file
            
        Returns:
            dict: Compilation result containing:
                - success (bool)
                - osdi_path (str or None)
                - compilation_time_s (float)
                - stdout (str)
                - stderr (str)
                - version (str)
        """
        va_file = Path(va_path).resolve()
        if not va_file.exists():
            return {
                "success": False,
                "error": f"Verilog-A file not found: {va_path}",
                "osdi_path": None,
                "compilation_time_s": 0.0,
            }

        if not self.is_available():
            return {
                "success": False,
                "error": "OpenVAF compiler binary not found on system",
                "osdi_path": None,
                "compilation_time_s": 0.0,
            }

        out_dir = Path(output_dir).resolve() if output_dir else va_file.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        osdi_name = va_file.stem + ".osdi"
        osdi_path = out_dir / osdi_name

        cmd = [self.openvaf_bin, str(va_file), "-o", str(osdi_path)]
        self.logger.info(f"Compiling Verilog-A model with OpenVAF: {' '.join(cmd)}")

        t0 = time.time()
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            elapsed = time.time() - t0

            success = (proc.returncode == 0) and osdi_path.exists()
            result = {
                "success": success,
                "va_file": str(va_file),
                "osdi_path": str(osdi_path) if success else None,
                "compilation_time_s": round(elapsed, 3),
                "return_code": proc.returncode,
                "stdout": proc.stdout.strip(),
                "stderr": proc.stderr.strip(),
                "openvaf_version": self.get_version(),
            }

            if success:
                self.logger.info(f"OpenVAF successfully compiled {va_file.name} -> {osdi_name} in {elapsed:.2f}s")
            else:
                self.logger.error(f"OpenVAF compilation failed (code {proc.returncode}):\n{proc.stderr}\n{proc.stdout}")

            return result
        except Exception as e:
            elapsed = time.time() - t0
            self.logger.error(f"Error executing OpenVAF: {e}")
            return {
                "success": False,
                "error": str(e),
                "osdi_path": None,
                "compilation_time_s": round(elapsed, 3),
            }
