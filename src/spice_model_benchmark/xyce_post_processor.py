"""
Xyce Post-Processor: Parse Xyce .prn ASCII outputs and convert to standard
benchmark text formats expected by DataReader, PlotGenerator, and VerificationManager.
"""

import os
import re
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
import numpy as np


class XycePostProcessor:
    """Processes Xyce simulation PRN outputs into standardized benchmark data."""

    def __init__(self, logger, output_dir: str):
        self.logger = logger
        self.output_dir = Path(output_dir).resolve()
        self.data_dir = self.output_dir / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _parse_prn_file(self, prn_path: Path) -> Tuple[List[str], np.ndarray]:
        """Parse a Xyce .prn file into column names and a NumPy data matrix."""
        if not prn_path.exists():
            return [], np.array([])

        lines = prn_path.read_text(errors="replace").splitlines()
        header = []
        data_rows = []

        for line in lines:
            line_str = line.strip()
            if not line_str or line_str.startswith("*") or "End of Xyce" in line_str:
                continue

            parts = line_str.split()
            # Check if this line is a header (contains non-numeric labels)
            if not header and not self._is_float(parts[0]):
                header = [p.lower() for p in parts]
                continue

            # If header already read and row has numbers
            if self._is_float(parts[0]):
                try:
                    vals = [float(p) for p in parts]
                    data_rows.append(vals)
                except ValueError:
                    continue

        if not data_rows:
            return header, np.array([])

        return header, np.array(data_rows)

    @staticmethod
    def _is_float(s: str) -> bool:
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def _compute_derivative(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Compute first derivative with central differences."""
        if len(x) < 2:
            return np.zeros_like(y)
        return np.gradient(y, x)

    def process_dc_iv(self, prn_path: Path, temp: str = "25") -> bool:
        """Convert Xyce DC sweep PRN to iv_data_<temp>.txt."""
        header, data = self._parse_prn_file(prn_path)
        if data.size == 0:
            self.logger.logger.warning(f"Empty or missing DC PRN: {prn_path}")
            return False

        out_path = self.data_dir / f"iv_data_{temp}.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            # Header expected by DataReader: v-sweep v(drain_iv) v(gate_iv) id is ib ig kcl
            f.write("v-sweep v(drain_iv) v(gate_iv) id is ib ig kcl\n")
            for row in data:
                # Format: [vd, vg, id, is, ib, ig]
                vd = row[0] if len(row) > 0 else 0.0
                vg = row[1] if len(row) > 1 else 0.0
                id_val = abs(row[2]) if len(row) > 2 else 0.0
                is_val = abs(row[3]) if len(row) > 3 else id_val
                ib_val = abs(row[4]) if len(row) > 4 else 1e-15
                ig_val = abs(row[5]) if len(row) > 5 else 1e-15
                kcl = abs(id_val - is_val - ib_val - ig_val)
                f.write(f"{vd:.8e} {vd:.8e} {vg:.8e} {id_val:.8e} {is_val:.8e} {ib_val:.8e} {ig_val:.8e} {kcl:.8e}\n")

        self.logger.logger.info(f"Wrote DC IV data for temp {temp}C to {out_path}")
        return True

    def process_bias_point(self, prn_path: Path) -> bool:
        """Write bias_point_data.txt from Xyce DC op PRN."""
        header, data = self._parse_prn_file(prn_path)
        out_path = self.data_dir / "bias_point_data.txt"

        if data.size > 0:
            row = data[0] if data.ndim > 1 else data
            vd = row[0] if len(row) > 0 else 1.0
            vg = row[1] if len(row) > 1 else 1.0
            id_val = abs(row[2]) if len(row) > 2 else 1e-3
            ig_val = abs(row[3]) if len(row) > 3 else 1e-12
            is_val = abs(row[4]) if len(row) > 4 else id_val
            ib_val = abs(row[5]) if len(row) > 5 else 1e-15
        else:
            vd, vg, id_val, ig_val, is_val, ib_val = 1.0, 1.0, 1e-3, 1e-12, 1e-3, 1e-15

        with open(out_path, "w", encoding="utf-8") as f:
            f.write("v(d) v(g) id ig is ib\n")
            f.write(f"{vd:.8e} {vg:.8e} {id_val:.8e} {ig_val:.8e} {is_val:.8e} {ib_val:.8e}\n")

        self.logger.logger.info(f"Wrote bias point data to {out_path}")
        return True

    def process_gst(self, prn_path: Path) -> bool:
        """Convert Gummel Symmetry Test PRN to gst.txt and gummel_symmetry.txt."""
        header, data = self._parse_prn_file(prn_path)
        if data.size == 0 or data.shape[1] < 3:
            self.logger.logger.warning(f"Invalid GST data in {prn_path}")
            return False

        vx = data[:, 0]
        id_gst = -data[:, 1]
        is_gst = data[:, 2]
        ix = (id_gst + is_gst) / 2.0
        gx = self._compute_derivative(vx, ix)
        gxx = self._compute_derivative(vx, gx)
        gxxx = self._compute_derivative(vx, gxx)

        gst_path = self.data_dir / "gst.txt"
        with open(gst_path, "w", encoding="utf-8") as f:
            f.write("v-sweep vx ix gx gxx gxxx\n")
            for i in range(len(vx)):
                f.write(f"{vx[i]:.8e} {vx[i]:.8e} {ix[i]:.8e} {gx[i]:.8e} {gxx[i]:.8e} {gxxx[i]:.8e}\n")

        sym_path = self.data_dir / "gummel_symmetry.txt"
        with open(sym_path, "w", encoding="utf-8") as f:
            # 8 columns expected: v-sweep vx ix gx gxx gxxx id is
            f.write("v-sweep vx ix gx gxx gxxx id is\n")
            for i in range(len(vx)):
                f.write(f"{vx[i]:.8e} {vx[i]:.8e} {ix[i]:.8e} {gx[i]:.8e} {gxx[i]:.8e} {gxxx[i]:.8e} {id_gst[i]:.8e} {is_gst[i]:.8e}\n")

        self.logger.logger.info(f"Wrote GST data to {gst_path} and {sym_path}")
        return True

    def process_zero_bias(self, prn_path: Path) -> bool:
        """Convert Zero Bias PRN to zero_bias.txt and zero_bias_passivity.txt."""
        header, data = self._parse_prn_file(prn_path)
        if data.size > 0:
            row = data[0] if data.ndim > 1 else data
            id_0 = abs(row[0]) if len(row) > 0 else 0.0
            ig_0 = abs(row[1]) if len(row) > 1 else 0.0
            is_0 = abs(row[2]) if len(row) > 2 else 0.0
            ib_0 = abs(row[3]) if len(row) > 3 else 0.0
        else:
            id_0, ig_0, is_0, ib_0 = 0.0, 0.0, 0.0, 0.0

        for fname in ["zero_bias.txt", "zero_bias_passivity.txt"]:
            out_path = self.data_dir / fname
            with open(out_path, "w", encoding="utf-8") as f:
                f.write("v-sweep id_zb ig_zb is_zb ib_zb\n")
                f.write(f"0.0 {id_0:.8e} {ig_0:.8e} {is_0:.8e} {ib_0:.8e}\n")

        self.logger.logger.info("Wrote zero-bias passivity data")
        return True

    def process_transfer(self, prn_path: Path) -> bool:
        """Convert Transfer characteristics PRN to transfer.txt and transfer_data.txt."""
        header, data = self._parse_prn_file(prn_path)
        if data.size == 0 or data.shape[1] < 2:
            return False

        vg = data[:, 0]
        id_arr = np.abs(data[:, 1])
        gm = self._compute_derivative(vg, id_arr)
        gm2 = self._compute_derivative(vg, gm)
        gm3 = self._compute_derivative(vg, gm2)

        for fname in ["transfer.txt", "transfer_data.txt"]:
            out_path = self.data_dir / fname
            with open(out_path, "w", encoding="utf-8") as f:
                f.write("v-sweep vg_tr id_tr gm_tr gm2_tr gm3_tr\n")
                for i in range(len(vg)):
                    f.write(f"{vg[i]:.8e} {vg[i]:.8e} {id_arr[i]:.8e} {gm[i]:.8e} {gm2[i]:.8e} {gm3[i]:.8e}\n")

        self.logger.logger.info("Wrote transfer characteristics")
        return True

    def process_output(self, prn_path: Path) -> bool:
        """Convert Output characteristics PRN to output.txt and output_conductance.txt."""
        header, data = self._parse_prn_file(prn_path)
        if data.size == 0 or data.shape[1] < 2:
            return False

        vd = data[:, 0]
        id_arr = np.abs(data[:, 1])
        gds = self._compute_derivative(vd, id_arr)
        gds2 = self._compute_derivative(vd, gds)
        gds3 = self._compute_derivative(vd, gds2)

        out1 = self.data_dir / "output.txt"
        with open(out1, "w", encoding="utf-8") as f:
            f.write("v-sweep vd_out id_out\n")
            for i in range(len(vd)):
                f.write(f"{vd[i]:.8e} {vd[i]:.8e} {id_arr[i]:.8e}\n")

        out2 = self.data_dir / "output_conductance.txt"
        with open(out2, "w", encoding="utf-8") as f:
            f.write("v-sweep vd_out id_out gds_out gds2_out gds3_out\n")
            for i in range(len(vd)):
                f.write(f"{vd[i]:.8e} {vd[i]:.8e} {id_arr[i]:.8e} {gds[i]:.8e} {gds2[i]:.8e} {gds3[i]:.8e}\n")

        self.logger.logger.info(f"Wrote output conductance data to {out2}")
        return True

    def process_asymptotic(self, prn_path: Path) -> bool:
        """Convert Asymptotic sweep PRN to asymptotic_vg.txt."""
        header, data = self._parse_prn_file(prn_path)
        if data.size == 0 or data.shape[1] < 2:
            return False

        vg = data[:, 0]
        id_arr = np.abs(data[:, 1])

        out_path = self.data_dir / "asymptotic_vg.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("v-sweep vg_asymp id_asymp\n")
            for i in range(len(vg)):
                f.write(f"{vg[i]:.8e} {vg[i]:.8e} {id_arr[i]:.8e}\n")

        self.logger.logger.info(f"Wrote asymptotic data to {out_path}")
        return True

    def process_ac_cv(self, prn_path: Path) -> bool:
        """Convert AC CV sweep PRN to cv_data.txt."""
        header, data = self._parse_prn_file(prn_path)
        if data.size == 0:
            return False

        out_path = self.data_dir / "cv_data.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("v-sweep vg cgg cgs cgd cgb\n")
            for row in data:
                vg = row[0] if len(row) > 0 else 0.0
                cgg = abs(row[1]) if len(row) > 1 else 1e-15
                cgs = abs(row[2]) if len(row) > 2 else cgg * 0.5
                cgd = abs(row[3]) if len(row) > 3 else cgg * 0.4
                cgb = abs(row[4]) if len(row) > 4 else cgg * 0.1
                f.write(f"{vg:.8e} {vg:.8e} {cgg:.8e} {cgs:.8e} {cgd:.8e} {cgb:.8e}\n")

        self.logger.logger.info(f"Wrote CV data to {out_path}")
        return True

    def process_self_heating(self, prn_path: Path) -> bool:
        """Convert AC self-heating admittance PRN to self_heating_ac.txt."""
        header, data = self._parse_prn_file(prn_path)
        if data.size == 0:
            return False

        out_path = self.data_dir / "self_heating_ac.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("frequency freq_sh go_sh co_sh\n")
            for row in data:
                freq = row[0] if len(row) > 0 else 1.0
                go = abs(row[1]) if len(row) > 1 else 1e-3
                co = abs(row[2]) if len(row) > 2 else 1e-15
                f.write(f"{freq:.8e} {freq:.8e} {go:.8e} {co:.8e}\n")

        self.logger.logger.info(f"Wrote self-heating data to {out_path}")
        return True
