"""
Spectre Post-Processor: Converts Spectre PSF ASCII output to ngspice-compatible text files.

Reads Spectre's PSF ASCII format and generates the identical text files
that the existing DataReader/PlotGenerator/VerificationManager pipeline expects.
"""
import re
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional


class SpectrePostProcessor:
    """Convert Spectre PSF ASCII output to ngspice-compatible text data files."""

    def __init__(self, logger, data_dir: str):
        self.logger = logger
        self.data_dir = Path(data_dir)

    # ====================================================================
    # PSF ASCII Parser for DC sweep files
    # ====================================================================

    def _parse_psf_dc_groups(self, filepath: Path) -> Dict:
        """Parse a Spectre PSF ASCII DC file, extracting grouped trace values.

        The PSF VALUE section contains N values per step, where N = number of traces.
        Each step's values are written sequentially.

        Returns dict with:
          - 'header': {key: value_or_str}
          - 'trace_names': ordered list of trace names
          - 'trace_types': {trace_name: type_string}
          - 'values': {trace_name: np.array}
          - 'n_steps': number of sweep points
        """
        header = {}
        trace_names = []
        trace_types = {}
        values_raw = {}  # trace_name -> list of floats

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        lines = content.split('\n')

        section = None
        in_prop = False
        type_name = None

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped == 'END':
                break
            if stripped == 'HEADER':
                section = 'header'
                continue
            if stripped == 'TYPE':
                section = 'type'
                continue
            if stripped == 'SWEEP':
                section = 'sweep'
                continue
            if stripped == 'TRACE':
                section = 'trace'
                continue
            if stripped == 'VALUE':
                section = 'value'
                continue

            if section == 'header':
                # Parse "key" "value" or "key" number
                m = re.match(r'"([^"]*)"\s+"([^"]*)"', stripped)
                if m:
                    key = m.group(1)
                    val = m.group(2)
                    try:
                        header[key] = float(val)
                    except ValueError:
                        header[key] = val
                else:
                    m = re.match(r'"([^"]*)"\s+([\d.eE+\-]+)', stripped)
                    if m:
                        try:
                            header[m.group(1)] = float(m.group(2))
                        except ValueError:
                            header[m.group(1)] = m.group(2)

            elif section == 'type':
                if stripped == ')':
                    in_prop = False
                    continue
                if 'PROP(' in stripped:
                    in_prop = True
                    continue
                if in_prop:
                    continue
                # Type definition: "name" TYPE [PROP(...)]
                m = re.match(r'"([^"]*)"\s+(\w+)', stripped)
                if m:
                    type_name = m.group(1)
                    trace_types[type_name] = m.group(2)

            elif section == 'trace':
                if stripped == ')':
                    continue
                # Trace definition: "name" "type" [PROP(...)]
                m = re.match(r'"([^"]*)"\s+"(\w+)"', stripped)
                if m:
                    tname = m.group(1)
                    ttype = m.group(2)
                    trace_names.append(tname)
                    trace_types[tname] = ttype
                    values_raw[tname] = []

            elif section == 'value':
                if stripped == ')':
                    continue
                # Value entry: "name" number
                m = re.match(r'"([^"]*)"\s+([\d.eE+\-]+)', stripped)
                if m:
                    tname = m.group(1)
                    try:
                        val = float(m.group(2))
                        if tname not in values_raw:
                            values_raw[tname] = []
                        values_raw[tname].append(val)
                    except ValueError:
                        pass

        # Determine number of steps - check time/dc/frequency then trace_names
        n_steps = 0
        for tname in ['time', 'dc', 'sweep', 'frequency']:
            if tname in values_raw and len(values_raw[tname]) > 0:
                n_steps = len(values_raw[tname])
                break
        if n_steps == 0 and trace_names:
            n_steps = len(values_raw.get(trace_names[0], []))

        # Convert to numpy arrays, truncating to n_steps
        result = {
            'header': header,
            'trace_names': trace_names,
            'trace_types': trace_types,
            'values': {},
            'n_steps': n_steps,
        }
        # Copy all parsed values (including time/dc from SWEEP section)
        for tname, vals_list in values_raw.items():
            vals = vals_list
            if len(vals) > n_steps:
                vals = vals[:n_steps]
            elif 0 < len(vals) < n_steps:
                vals = vals + [0.0] * (n_steps - len(vals))
            result['values'][tname] = np.array(vals, dtype=float) if vals else np.array([])

        return result

    # ====================================================================
    # DC Post-Processing
    # ====================================================================

    def process_dc(self, raw_dir: Path) -> bool:
        """Process DC simulation results.

        Generates:
          - iv_data_{temp}.txt: IV curves per temperature
          - bias_point_data.txt: Operating point data at 27C
        """
        self.logger.logger.info("Post-processing Spectre DC output...")
        raw_dir = Path(raw_dir)

        # ---- IV Sweep Files ----
        dc_files = sorted(raw_dir.glob("sw_temp-*_sw_vgs-*_dc_iv.dc"))
        if not dc_files:
            self.logger.logger.error("No DC IV sweep files found")
            return False

        # Group files by temperature index
        # File: sw_temp-TIDX_sw_vgs-GIDX_dc_iv.dc
        temp_groups: Dict[int, Dict[int, Path]] = {}
        for f in dc_files:
            m = re.match(r'sw_temp-(\d+)_sw_vgs-(\d+)_dc_iv\.dc', f.name)
            if m:
                tidx = int(m.group(1))
                gidx = int(m.group(2))
                temp_groups.setdefault(tidx, {})[gidx] = f

        # Parse each file and write combined output per temperature
        for tidx in sorted(temp_groups.keys()):
            vgs_files = temp_groups[tidx]
            temp = None

            # Write combined output with ngspice-compatible header
            # Header: v-sweep v(drain_iv) v(gate_iv) id is ib ig kcl
            out_lines = ["v-sweep v(drain_iv) v(gate_iv) id is ib ig kcl\n"]
            sweep_idx = 0
            for gidx in sorted(vgs_files.keys()):
                f = vgs_files[gidx]
                data = self._parse_psf_dc_groups(f)

                if temp is None:
                    temp = data['header'].get('temp', None)

                vals = data['values']

                # Map PSF trace names to our expected signals
                vds = vals.get('drain_iv', vals.get('dc', np.array([])))
                vgs_vals = vals.get('gate_iv', np.array([]))
                vgs_val = float(vgs_vals[0]) if len(vgs_vals) > 0 else 0.0

                id_ = vals.get('Vds_iv:p', np.array([]))
                is_ = vals.get('Vs_iv:p', np.array([]))
                ib_ = vals.get('Vb_iv:p', np.array([]))
                ig_ = vals.get('Vgs_iv:p', np.array([]))

                n = min(len(vds), len(id_), len(is_), len(ib_), len(ig_))
                if n == 0:
                    continue

                for j in range(n):
                    vd = vds[j] if j < len(vds) else 0.0
                    id_val = -id_[j] if j < len(id_) else 0.0
                    is_val = -is_[j] if j < len(is_) else 0.0
                    ib_val = -ib_[j] if j < len(ib_) else 0.0
                    ig_val = -ig_[j] if j < len(ig_) else 0.0
                    kcl = abs(id_val + is_val + ig_val + ib_val)
                    out_lines.append(
                        f" {sweep_idx:.10e}  {vd:.10e}  {vgs_val:.10e}  "
                        f"{id_val:.10e}  {is_val:.10e}  {ib_val:.10e}  "
                        f"{ig_val:.10e}  {kcl:.10e}\n"
                    )
                    sweep_idx += 1

            # Determine temperature value
            if temp is not None and temp == int(temp):
                temp_name = f"{int(temp)}"
            elif temp is not None:
                temp_name = f"{temp:.0f}"
            else:
                temp_map = {0: "-40", 1: "0", 2: "25", 3: "50", 4: "100", 5: "150"}
                temp_name = temp_map.get(tidx, f"{tidx}")

            out_path = self.data_dir / f"iv_data_{temp_name}.txt"
            with open(out_path, 'w') as f:
                f.writelines(out_lines)
            self.logger.logger.info(f"  Written: {out_path} ({len(out_lines) - 1} points)")

        # ---- Bias Point Files ----
        self._process_dc_bias(raw_dir)

        self.logger.logger.info("DC post-processing complete.")
        return True

    def _process_dc_bias(self, raw_dir: Path):
        """Process bias point sweep files."""
        bias_files = sorted(raw_dir.glob("sw_bias-000_sw_vds_bias-*_sw_vgs_bias-*_dc_bias.dc"))
        if not bias_files:
            self.logger.logger.info("  No dedicated bias files, extracting from IV data")
            self._extract_bias_from_iv()
            return

        out_lines = []
        for f in bias_files:
            data = self._parse_psf_dc_groups(f)
            vals = data['values']

            vd = vals.get('drain_bias', np.array([]))
            vg = vals.get('gate_bias', np.array([]))
            id_ = vals.get('Vds_bias:p', np.array([]))
            is_ = vals.get('Vs_bias:p', np.array([]))
            ib_ = vals.get('Vb_bias:p', np.array([]))
            ig_ = vals.get('Vgs_bias:p', np.array([]))

            # Get the first (and only) point
            vd_val = float(vd[0]) if len(vd) > 0 else 0.0
            vg_val = float(vg[0]) if len(vg) > 0 else 0.0
            id_val = -float(id_[0]) if len(id_) > 0 else 0.0
            is_val = -float(is_[0]) if len(is_) > 0 else 0.0
            ib_val = -float(ib_[0]) if len(ib_) > 0 else 0.0
            ig_val = -float(ig_[0]) if len(ig_) > 0 else 0.0

            out_lines.append(
                f"{vd_val:.10e} {vg_val:.10e} {id_val:.10e} "
                f"{ig_val:.10e} {is_val:.10e} {ib_val:.10e}\n"
            )

        # Prepend header
        out_lines.insert(0, "v(drain_bias) v(gate_bias) id_bias ig_bias is_bias ib_bias\n")

        out_path = self.data_dir / "bias_point_data.txt"
        with open(out_path, 'w') as f:
            f.writelines(out_lines)
        self.logger.logger.info(f"  Written: {out_path} ({len(out_lines) - 1} bias points)")

    def _extract_bias_from_iv(self):
        """Fallback: extract bias points from IV data at 25C."""
        for temp in ['25', '27', '0']:
            iv_file = self.data_dir / f"iv_data_{temp}.txt"
            if iv_file.exists():
                data = np.loadtxt(iv_file)
                bias_pts = [
                    (0.0, 0.0), (0.0, 0.6), (0.0, 1.2),
                    (0.6, 0.0), (0.6, 0.6), (0.6, 1.2),
                    (1.2, 0.0), (1.2, 0.6), (1.2, 1.2),
                ]
                out_path = self.data_dir / "bias_point_data.txt"
                with open(out_path, 'w') as f:
                    f.write("v(drain_bias) v(gate_bias) id_bias ig_bias is_bias ib_bias\n")
                    for vds, vgs in bias_pts:
                        mask = (np.abs(data[:, 0] - vds) < 0.001) & (np.abs(data[:, 1] - vgs) < 0.001)
                        row = data[mask]
                        if len(row) > 0:
                            r = row[0]
                            f.write(f"{r[0]:.10e} {r[1]:.10e} {r[2]:.10e} "
                                    f"{r[5]:.10e} {r[3]:.10e} {r[4]:.10e}\n")
                self.logger.logger.info(f"  Written (from IV): {out_path}")
                return

    # ====================================================================
    # AC Post-Processing (placeholder - to be completed)
    # ====================================================================

    def process_ac(self, raw_dir: Path) -> bool:
        """Process AC simulation results."""
        self.logger.logger.info("Post-processing Spectre AC output...")
        # Stub: generate empty expected files so pipeline doesn't crash
        self._ensure_file("cv_data.txt",
                          "Vg Cgg_1kHz Cgg_10kHz Cgg_100kHz Cgg_1MHz Cgb_1MHz Cgs_1MHz Cgd_1MHz\n")
        self._ensure_file("cmatrix_data.txt",
                          "Vg Cgg Cdg Csg Cbg Cgd Cdd Csd Cbd Cgs Cds Css Cbs Cgb Cdb Csb Cbb\n")
        self._ensure_file("sparams_data.txt",
                          "# S-parameter analysis\n# freq s11_mag s11_phase s12_mag s12_phase s21_mag s21_phase s22_mag s22_phase\n")
        self._ensure_file("nqs_effects.txt",
                          "# Non-quasi-static effects analysis\n# freq vg_phase id_phase phase_diff\n")
        self._ensure_file("charge_conservation.txt", "")
        self.logger.logger.info("AC post-processing complete (stub).")
        return True

    # ====================================================================
    # Transient Post-Processing (placeholder)
    # ====================================================================

    def process_transient(self, raw_dir: Path) -> bool:
        """Process transient simulation results.

        Generates 8 text files matching ngspice transient_circuit.cir output.
        """
        self.logger.logger.info("Post-processing Spectre transient output...")
        raw_dir = Path(raw_dir)

        # Helper: read PSF tran file, write text with double-time + data columns
        def _write_tran_file(psf_name: str, out_name: str,
                             voltage_cols: list, current_cols: list):
            """Parse a transient PSF file and write ngspice-compatible text."""
            psf_files = sorted(raw_dir.glob(psf_name))
            if not psf_files:
                self.logger.logger.warning(f"  No PSF for {out_name} ({psf_name})")
                return False
            data = self._parse_psf_dc_groups(psf_files[0])
            vals = data['values']

            # Build time array
            time = vals.get('time', np.array([]))
            n = len(time)
            if n == 0:
                return False

            # Build header and data columns
            col_names = ["time", "time"]
            arrays = [time, time]

            for vcol in voltage_cols:
                key = vcol  # e.g., "gate_tran"
                col_names.append(f"v({key})")
                arr = vals.get(key, np.zeros(n))
                if len(arr) < n:
                    arr = np.pad(arr, (0, n - len(arr)), constant_values=0)
                arrays.append(arr[:n])

            for ccol in current_cols:
                key = ccol  # e.g., "Vds_tran:p"
                col_names.append(f"i({key.replace(':p', '')})")
                arr = vals.get(key, np.zeros(n))
                if len(arr) < n:
                    arr = np.pad(arr, (0, n - len(arr)), constant_values=0)
                arrays.append(arr[:n])

            # Write file matching ngspice wrdata format
            out_path = self.data_dir / out_name
            with open(out_path, 'w') as f:
                f.write(" " + " ".join(col_names) + "\n")
                for j in range(n):
                    row = " ".join(f"{a[j]:.10e}" for a in arrays)
                    f.write(f" {row}\n")
            self.logger.logger.info(f"  Written: {out_path} ({n} points)")
            return True

        # ---- 1. Large-Signal Transient ----
        _write_tran_file("tran_ls.tran.tran", "tran_large_signal.txt",
                         ["gate_tran", "drain_tran"],
                         ["Vds_tran:p", "Vgs_tran:p", "Vs_tran:p", "Vb_tran:p"])

        # ---- 2. Switching Response ----
        _write_tran_file("tran_sw.tran.tran", "tran_switching.txt",
                         ["in_inv", "out_inv"],
                         ["Vdd_inv:p"])

        # ---- 3. Switching Power (computed) ----
        sw_files = sorted(raw_dir.glob("tran_sw.tran.tran"))
        if sw_files:
            data = self._parse_psf_dc_groups(sw_files[0])
            vals = data['values']
            time = vals.get('time', np.array([]))
            vdd = vals.get('vdd_inv', np.zeros(len(time)) if len(time) > 0 else np.array([]))
            ivdd = vals.get('Vdd_inv:p', np.zeros(len(time)) if len(time) > 0 else np.array([]))
            n = min(len(time), len(vdd), len(ivdd))
            if n > 0:
                power = -np.array(vdd[:n]) * np.array(ivdd[:n])
                out_path = self.data_dir / "tran_switching_power.txt"
                with open(out_path, 'w') as f:
                    f.write(" time time power_switching\n")
                    for j in range(n):
                        f.write(f" {time[j]:.10e} {time[j]:.10e} {power[j]:.10e}\n")
                self.logger.logger.info(f"  Written: {out_path} ({n} points)")

        # ---- 4. Delay Effect ----
        _write_tran_file("tran_delay.tran.tran", "tran_delay.txt",
                         ["in_delay", "mid1_delay", "mid2_delay", "out_delay"],
                         [])

        # ---- 5 & 6. Power Dissipation at 27C and 100C ----
        for temp_tag, psf_pat in [("27C", "sw_pwr_27-000_tran_pwr_27.tran.tran"),
                                   ("100C", "sw_pwr_100-000_tran_pwr_100.tran.tran")]:
            psf_files = sorted(raw_dir.glob(psf_pat))
            if psf_files:
                data = self._parse_psf_dc_groups(psf_files[0])
                vals = data['values']
                time = vals.get('time', np.array([]))
                vin = vals.get('in_power', np.array([]))
                vout = vals.get('out_power', np.array([]))
                idd = vals.get('Vdd_power:p', np.array([]))
                n = min(len(time), len(vin), len(vout), len(idd))
                if n > 0:
                    vdd_power = 1.2  # VDD = 1.2V
                    power_diss = -vdd_power * np.array(idd[:n])
                    # Energy = cumulative integral
                    energy = np.cumsum(power_diss) * (time[1] - time[0]) if n > 1 else np.zeros(n)
                    out_path = self.data_dir / f"tran_power_{temp_tag}.txt"
                    with open(out_path, 'w') as f:
                        f.write(" time time v(in_power) v(out_power) power_diss energy\n")
                        for j in range(n):
                            f.write(f" {time[j]:.10e} {time[j]:.10e} "
                                    f"{vin[j]:.10e} {vout[j]:.10e} "
                                    f"{power_diss[j]:.10e} {energy[j]:.10e}\n")
                    self.logger.logger.info(f"  Written: {out_path} ({n} points)")

        # ---- 7. Quasi-Static ----
        _write_tran_file("tran_qs.tran.tran", "tran_quasi_static.txt",
                         ["gate_qs", "drain_qs"],
                         ["Vds_qs:p"])

        # ---- 8. Charge Conservation ----
        _write_tran_file("tran_charge.tran.tran", "tran_charge.txt",
                         ["gate_charge"],
                         ["Vg_charge:p", "Vd_charge:p", "Vs_charge:p", "Vb_charge:p"])

        self.logger.logger.info("Transient post-processing complete.")
        return True

    # ====================================================================
    # Noise Post-Processing (placeholder)
    # ====================================================================

    def process_noise(self, raw_dir: Path) -> bool:
        """Process noise simulation results."""
        self.logger.logger.info("Post-processing Spectre noise output...")
        self._ensure_file("thermal_noise_vgs0.6_vds0.6.txt", "")
        self._ensure_file("flicker_noise.txt", "")
        self._ensure_file("shot_noise.txt", "")
        for t in [-40, 0, 27, 50, 100, 150]:
            self._ensure_file(f"noise_temp{t}.txt", "")
        self.logger.logger.info("Noise post-processing complete (stub).")
        return True

    # ====================================================================
    # Helpers
    # ====================================================================

    def _ensure_file(self, filename: str, content: str):
        """Create a file if it doesn't exist."""
        path = self.data_dir / filename
        if not path.exists():
            with open(path, 'w') as f:
                f.write(content)
            self.logger.logger.info(f"  Created stub: {path}")

    # ====================================================================
    # Main dispatch
    # ====================================================================

    def process_all(self, raw_dir: Path, modes: List[str]) -> bool:
        """Run all post-processing for selected modes."""
        success = True
        if 'dc' in modes:
            if not self.process_dc(raw_dir):
                success = False
        if 'ac' in modes:
            if not self.process_ac(raw_dir):
                success = False
        if 'transient' in modes:
            if not self.process_transient(raw_dir):
                success = False
        if 'noise' in modes:
            if not self.process_noise(raw_dir):
                success = False
        return success
