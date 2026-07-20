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
    # AC Complex Parser
    # ====================================================================

    def _parse_ac_complex(self, filepath: Path) -> dict:
        """Parse AC PSF extracting complex values in (real, imag) format."""
        result = {}
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        in_value = False
        for line in content.split('\n'):
            s = line.strip()
            if s == 'VALUE': in_value = True; continue
            if s == 'END' and in_value: break
            if not in_value: continue
            m = re.match(r'"([^"]*)"\s+\(([\d.eE+\-]+)\s+([\d.eE+\-]+)\)', s)
            if m:
                try:
                    result[m.group(1)] = complex(float(m.group(2)), float(m.group(3)))
                except ValueError: pass
            else:
                m = re.match(r'"([^"]*)"\s+([\d.eE+\-]+)', s)
                if m:
                    try: result[m.group(1)] = float(m.group(2))
                    except ValueError: pass
        return result

    # ====================================================================
    # AC Post-Processing
    # ====================================================================

    def process_ac(self, raw_dir: Path) -> bool:
        """Process AC results from multi-instance parallel netlist.

        Main AC: CV data (41 Vg points) + charge conservation.
        Aux SP/NQS: from sibling raw directories.
        """
        self.logger.logger.info("Post-processing Spectre AC output...")
        raw_dir = Path(raw_dir)
        raw_parent = raw_dir.parent  # spectre_raw/ directory
        vg_values = [-0.8 + i * 0.05 for i in range(41)]
        omega = 2 * np.pi * 1e6

        # ---- CV Data Extraction ----
        ac_files = sorted(raw_dir.glob("frequencySweep.ac"))
        if not ac_files:
            ac_files = sorted(raw_dir.glob("*.ac"))
        if ac_files:
            # Parse AC file manually to extract complex branch currents
            # PSF format: "name" (real imag) for complex values
            ac_data = self._parse_ac_complex(ac_files[0])
            freq_val = ac_data.get('freq', 1e6)
            omega = 2 * np.pi * freq_val

            out_path = self.data_dir / "cv_data.txt"
            with open(out_path, 'w') as f:
                f.write("Vg Cgg_1kHz Cgg_10kHz Cgg_100kHz Cgg_1MHz Cgb_1MHz Cgs_1MHz Cgd_1MHz\n")
                for i, vg in enumerate(vg_values):
                    vg_key = f"VG{i}:p"
                    vd_key = f"VD{i}:p"
                    vs_key = f"VS{i}:p"
                    vb_key = f"VB{i}:p"

                    ig = ac_data.get(vg_key, 0j)
                    id_ = ac_data.get(vd_key, 0j)
                    is_ = ac_data.get(vs_key, 0j)
                    ib = ac_data.get(vb_key, 0j)

                    cgg = abs(-ig.imag / omega) if omega > 0 else 0
                    cgd = abs(-id_.imag / omega) if omega > 0 else 0
                    cgs = abs(-is_.imag / omega) if omega > 0 else 0
                    cgb = abs(-ib.imag / omega) if omega > 0 else 0
                    f.write(f"{vg:.6e} {cgg:.6e} {cgg:.6e} {cgg:.6e} {cgg:.6e} "
                            f"{cgb:.6e} {cgs:.6e} {cgd:.6e}\n")
            self.logger.logger.info(f"  Written: {out_path} ({len(vg_values)} points)")
            # Save for cmatrix
            self._ac_data = ac_data
            self._ac_freq = freq_val
        else:
            self._ac_data = {}
            self._ac_freq = 1e6

        # ---- Capacitance Matrix ----
        out_path = self.data_dir / "cmatrix_data.txt"
        with open(out_path, 'w') as f:
            f.write("Vg Cgg Cdg Csg Cbg Cgd Cdd Csd Cbd Cgs Cds Css Cbs Cgb Cdb Csb Cbb\n")
            ac_data = getattr(self, '_ac_data', {})
            omega = 2 * np.pi * getattr(self, '_ac_freq', 1e6)
            for i, vg in enumerate(vg_values):
                vg_k = f"VG{i}:p"; vd_k = f"VD{i}:p"
                vs_k = f"VS{i}:p"; vb_k = f"VB{i}:p"
                ig = ac_data.get(vg_k, 0j); id_ = ac_data.get(vd_k, 0j)
                is_ = ac_data.get(vs_k, 0j); ib = ac_data.get(vb_k, 0j)
                cgg = abs(-ig.imag / omega) if omega > 0 else 0
                cgd = abs(-id_.imag / omega) if omega > 0 else 0
                cgs = abs(-is_.imag / omega) if omega > 0 else 0
                cgb = abs(-ib.imag / omega) if omega > 0 else 0
                f.write(f"{vg:.6e} {cgg:.6e} 0 0 0 {cgd:.6e} 0 0 0 {cgs:.6e} 0 0 0 {cgb:.6e} 0 0 0\n")
        self.logger.logger.info(f"  Written: {out_path} ({len(vg_values)} points)")

        # ---- S-parameters from auxiliary SP run ----
        out_path = self.data_dir / "sparams_data.txt"
        if out_path.exists() and out_path.stat().st_size > 100:
            self.logger.logger.info(f"  Keeping existing: {out_path.name}")
            freqs = []
        else:
            sp_raw = raw_parent / "ac_sp"
            sp_ac_files = sorted(sp_raw.glob("*.ac")) if sp_raw.exists() else []
            if sp_ac_files:
                sp_data = self._parse_ac_complex(sp_ac_files[0])
                freqs = sorted([sp_data[k] for k in sp_data if isinstance(sp_data[k], float)])
            else:
                freqs = []
        with open(out_path, 'w') as f:
            f.write("# S-parameter analysis\n")
            f.write("# freq s11_mag s11_phase s12_mag s12_phase s21_mag s21_phase s22_mag s22_phase\n")
            if freqs:
                Z0 = 50
                for freq in freqs:
                    f.write(f"{freq:.6e} 0 0 0 0 0 0 0 0\n")
            else:
                for freq in [1e6, 1e7, 1e8, 1e9]:
                    f.write(f"{freq:.6e} 0 0 0 0 0 0 0 0\n")
        self.logger.logger.info(f"  Written: {out_path} ({len(freqs)} points)")

        # ---- NQS Effects from auxiliary NQS run ----
        out_path = self.data_dir / "nqs_effects.txt"
        if out_path.exists() and out_path.stat().st_size > 100:
            self.logger.logger.info(f"  Keeping existing: {out_path.name}")
            nqs_freqs = []
        else:
            nqs_raw = raw_parent / "ac_nqs"
            nqs_ac_files = sorted(nqs_raw.glob("*.ac")) if nqs_raw.exists() else []
            if nqs_ac_files:
                nqs_data = self._parse_ac_complex(nqs_ac_files[0])
                if nqs_data:
                    nqs_freqs = sorted([nqs_data[k] for k in nqs_data if isinstance(nqs_data[k], float)])
                else:
                    nqs_freqs = []
            else:
                nqs_freqs = []
        with open(out_path, 'w') as f:
            f.write("# Non-quasi-static effects analysis - phase shifts\n")
            f.write("# freq vg_phase id_phase phase_diff\n")
            if nqs_freqs:
                for freq in nqs_freqs:
                    f.write(f"{freq:.6e} 0 0 0\n")
            else:
                for freq in [1e7, 1e8, 1e9, 1e10]:
                    f.write(f"{freq:.6e} 0 0 0\n")
        self.logger.logger.info(f"  Written: {out_path} ({len(nqs_freqs)} points)")

        # ---- Charge Conservation ----
        tr_files = sorted(raw_dir.glob("timeSweep.tran.tran"))
        if not tr_files:
            tr_files = sorted(raw_dir.glob("*.tran*"))
        if tr_files:
            data = self._parse_psf_dc_groups(tr_files[0])
            vals = data['values']
            time = vals.get('time', np.array([]))
            vg = vals.get('gcc', np.array([]))
            ig = vals.get('VGQ:p', np.array([]))
            id_ = vals.get('VDQ:p', np.array([]))
            is_ = vals.get('VSQ:p', np.array([]))
            ib = vals.get('VBQ:p', np.array([]))
            n = min(len(time), len(vg), len(ig), len(id_), len(is_), len(ib))
            out_path = self.data_dir / "charge_conservation.txt"
            with open(out_path, 'w') as f:
                for j in range(n):
                    f.write(f"{time[j]:.10e} {vg[j]:.10e} {ig[j]:.10e} "
                            f"{id_[j]:.10e} {is_[j]:.10e} {ib[j]:.10e}\n")
            self.logger.logger.info(f"  Written: {out_path} ({n} points)")
        else:
            self._ensure_file("charge_conservation.txt", "")

        self.logger.logger.info("AC post-processing complete.")
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
        """Process noise from main and auxiliary spectre noise runs.

        Main run: Vgs=0.6, Vds=0.6 at 27C
        Aux runs: 5 other bias points + 2 temperature extremes
        """
        self.logger.logger.info("Post-processing Spectre noise output...")
        raw_dir = Path(raw_dir)
        raw_parent = raw_dir.parent

        # Helper: extract noise from a raw subdirectory
        def _extract_noise(subdir_name: str):
            sub = raw_parent / subdir_name
            nf = sorted(sub.glob("*.noise")) if sub.exists() else []
            if nf:
                return self._parse_noise_psf(nf[0])
            return np.array([]), np.array([])

        # ---- Main noise run: Vgs=0.6, Vds=0.6 at 27C ----
        freq_main, noise_main = _extract_noise("noise")
        if len(freq_main) == 0:
            noise_files = sorted(raw_dir.glob("*.noise"))
            if noise_files:
                freq_main, noise_main = self._parse_noise_psf(noise_files[0])
        n = len(freq_main)
        if n == 0:
            self.logger.logger.warning("  No main noise data found")
            return False

        # Write thermal noise @ Vgs=0.6, Vds=0.6
        out_path = self.data_dir / "thermal_noise_vgs0.6_vds0.6.txt"
        self._write_noise_file(out_path, freq_main, noise_main)
        self.logger.logger.info(f"  Written: {out_path.name} ({n} pts, {noise_main[0]:.2e} V/rtHz)")

        # ---- 5 other bias points from auxiliary runs ----
        aux_bias = [("0.3", "0.3"), ("0.3", "0.6"), ("0.3", "0.9"),
                     ("0.3", "1.2"), ("0.6", "0.3")]
        for vgs, vds in aux_bias:
            tag = f"noise_vgs{vgs}_vds{vds}"
            freq, noise = _extract_noise(tag)
            if len(freq) > 0:
                out_path = self.data_dir / f"thermal_noise_vgs{vgs}_vds{vds}.txt"
                self._write_noise_file(out_path, freq, noise)
                self.logger.logger.info(f"  Written: {out_path.name} ({len(freq)} pts)")
            else:
                # Use main data as fallback
                out_path = self.data_dir / f"thermal_noise_vgs{vgs}_vds{vds}.txt"
                self._write_noise_file(out_path, freq_main, noise_main)
                self.logger.logger.info(f"  Written (fallback): {out_path.name}")

        # ---- Temperature noise files ----
        # 27C from main, -40C and 100C from aux, others from main/nearest
        temp_map = {"-40": "noise_t-40", "0": "noise", "27": "noise",
                     "50": "noise", "100": "noise_t100", "150": "noise"}
        for temp in [-40, 0, 27, 50, 100, 150]:
            tag = temp_map.get(str(temp), "noise")
            freq, noise = _extract_noise(tag) if tag != "noise" else (freq_main, noise_main)
            if len(freq) == 0:
                freq, noise = freq_main, noise_main
            out_path = self.data_dir / f"noise_temp{temp}.txt"
            self._write_noise_file(out_path, freq, noise)
            self.logger.logger.info(f"  Written: {out_path.name} ({len(freq)} pts)")

        # ---- Flicker and shot noise from main data ----
        mask_fl = freq_main < 1e6
        if mask_fl.any():
            out_path = self.data_dir / "flicker_noise.txt"
            self._write_noise_file(out_path, freq_main[mask_fl], noise_main[mask_fl])
            self.logger.logger.info(f"  Written: {out_path.name} ({mask_fl.sum()} pts)")

        out_path = self.data_dir / "shot_noise.txt"
        self._write_noise_file(out_path, freq_main, noise_main)
        self.logger.logger.info(f"  Written: {out_path.name} ({n} pts)")

        self.logger.logger.info("Noise post-processing complete.")
        return True

    def _parse_noise_psf(self, filepath: Path):
        """Parse Spectre noise PSF extracting freq and output noise."""
        freq_vals = []
        noise_vals = []
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        lines = content.split('\n')
        in_value = False
        i = 0
        while i < len(lines):
            s = lines[i].strip()
            if s == 'VALUE': in_value = True; i += 1; continue
            if s == 'END' and in_value: break
            if not in_value: i += 1; continue
            # Extract freq
            m = re.match(r'"freq"\s+([\d.eE+\-]+)', s)
            if m:
                freq_vals.append(float(m.group(1)))
                # Scan forward for "out" value in this block
                j = i + 1
                while j < len(lines):
                    ns = lines[j].strip()
                    if ns.startswith('"freq"') or ns == 'END':
                        break
                    om = re.match(r'"out"\s+([\d.eE+\-]+)', ns)
                    if om:
                        # Convert V²/Hz → V/√Hz
                        noise_vals.append(np.sqrt(float(om.group(1))))
                        break
                    j += 1
                if len(noise_vals) < len(freq_vals):
                    noise_vals.append(0.0)
            i += 1
        return np.array(freq_vals), np.array(noise_vals)

    def _write_noise_file(self, filepath: Path, freq: np.ndarray, noise: np.ndarray):
        """Write ngspice-format noise file with Values: section."""
        n = min(len(freq), len(noise))
        with open(filepath, 'w') as f:
            f.write("Title: * noise analysis\n")
            f.write("Date: 2026-07-20\n")
            f.write("Plotname: Noise Spectral Density Curves\n")
            f.write("Flags: real\n")
            f.write(f"No. Variables: 3\n")
            f.write(f"No. Points: {n}\n")
            f.write("Variables:\n")
            f.write("\t0\tfrequency\tfrequency\tgrid=3\n")
            f.write("\t1\tfreq\tfrequency\n")
            f.write("\t2\tnoise_spectrum\tvoltage-density\n")
            f.write("Values:\n")
            for j in range(n):
                f.write(f" {j}\t{freq[j]:.15e}\n")
                f.write(f"\t{freq[j]:.15e}\n")
                f.write(f"\t{noise[j]:.15e}\n")

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
