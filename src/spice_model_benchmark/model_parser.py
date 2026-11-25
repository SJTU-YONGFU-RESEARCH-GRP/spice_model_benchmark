"""SPICE Model Parser.

Parses SPICE model files (.inc, .lib, .model, .sp, .cir, .pm, .va) to discover
all active device models (.model) and subcircuits (.subckt). Extracts polarity,
device type (primitive vs subcircuit), level/version, pin connections, dimensions,
and nominal operating voltages so that evaluation netlists can be synthesized on the fly.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union


def parse_spice_val(val_str: str) -> Optional[float]:
    """Parse a SPICE engineering notation string into a float."""
    if not val_str:
        return None
    val_str = val_str.strip().lower()
    # Strip non-numeric suffixes after engineering units (e.g. '1.2v' -> '1.2', '10u' -> '10e-6')
    scale_factors = {
        't': 1e12,
        'g': 1e9,
        'meg': 1e6,
        'k': 1e3,
        'm': 1e-3,
        'u': 1e-6,
        'n': 1e-9,
        'p': 1e-12,
        'f': 1e-15,
        'a': 1e-18,
    }

    # Handle scientific notation like 1.2e-6
    try:
        return float(val_str)
    except ValueError:
        pass

    # Check for engineering suffix
    m = re.match(r'^([+-]?[\d\.]+)\s*([a-z]+)', val_str)
    if m:
        num_part = float(m.group(1))
        unit_part = m.group(2)
        for unit, factor in sorted(scale_factors.items(), key=lambda x: -len(x[0])):
            if unit_part.startswith(unit):
                return num_part * factor
        try:
            return num_part
        except ValueError:
            return None
    return None


@dataclass
class DeviceSpec:
    """Specification of an active device discovered in a SPICE model."""
    name: str
    polarity: str  # 'nmos', 'pmos', 'npn', 'pnp', 'diode', 'unknown'
    device_type: str = "primitive"  # 'primitive' (M...) or 'subcircuit' (X...)
    level: Optional[int] = None
    version: Optional[str] = None
    pins: List[str] = field(default_factory=lambda: ["d", "g", "s", "b"])
    default_l: float = 45e-9
    default_w: float = 10e-6
    default_vdd: float = 1.2
    vth0: Optional[float] = None
    tox: Optional[float] = None
    params: Dict[str, str] = field(default_factory=dict)
    instance_params: str = ""
    source_file: Optional[Path] = None

    @property
    def is_nmos(self) -> bool:
        return self.polarity == "nmos"

    @property
    def is_pmos(self) -> bool:
        return self.polarity == "pmos"

    @property
    def inst_prefix(self) -> str:
        return "X" if self.device_type == "subcircuit" else "M"

    def format_instance(
        self,
        inst_name: str,
        d_pin: str,
        g_pin: str,
        s_pin: str,
        b_pin: str,
        l: Optional[float] = None,
        w: Optional[float] = None,
        extra_params: str = "",
    ) -> str:
        """Format a SPICE netlist instance line for this device."""
        l_val = l if l is not None else self.default_l
        w_val = w if w is not None else self.default_w

        prefix = self.inst_prefix
        # Build pin list
        pins_str = f"{d_pin} {g_pin} {s_pin} {b_pin}"

        # Build parameter string
        param_parts = []
        if self.device_type == "primitive":
            param_parts.append(f"L={l_val:.3e} W={w_val:.3e}")
        else:
            # Subcircuit: include L and W if supported or default
            param_parts.append(f"L={l_val:.3e} W={w_val:.3e}")

        if self.instance_params:
            param_parts.append(self.instance_params)
        if extra_params:
            param_parts.append(extra_params)

        param_str = " ".join(filter(None, param_parts))
        return f"{prefix}_{inst_name} {pins_str} {self.name} {param_str}".strip()


@dataclass
class ModelInfo:
    """Catalog of all models and devices parsed from a SPICE model library."""
    source_file: Path
    devices: List[DeviceSpec] = field(default_factory=list)
    includes: List[Path] = field(default_factory=list)
    raw_lines: List[str] = field(default_factory=list)

    @property
    def nmos_devices(self) -> List[DeviceSpec]:
        return [d for d in self.devices if d.is_nmos]

    @property
    def pmos_devices(self) -> List[DeviceSpec]:
        return [d for d in self.devices if d.is_pmos]

    @property
    def primary_nmos(self) -> Optional[DeviceSpec]:
        """Return the primary or default NMOS device."""
        for d in self.nmos_devices:
            # Prefer standard VT or nominal if multiple
            if any(term in d.name.lower() for term in ["nom", "svt", "rvt", "vtg", "core", "01v8", "tt"]):
                return d
        return self.nmos_devices[0] if self.nmos_devices else None

    @property
    def primary_pmos(self) -> Optional[DeviceSpec]:
        """Return the primary or default PMOS device."""
        for d in self.pmos_devices:
            if any(term in d.name.lower() for term in ["nom", "svt", "rvt", "vtg", "core", "01v8", "tt"]):
                return d
        return self.pmos_devices[0] if self.pmos_devices else None

    def get_device(self, name: Optional[str] = None) -> Optional[DeviceSpec]:
        """Retrieve a device by name, or return the primary NMOS (or first device)."""
        if not self.devices:
            return None
        if not name:
            return self.primary_nmos or self.devices[0]
        for d in self.devices:
            if d.name.lower() == name.lower():
                return d
        return None


class ModelParser:
    """Parser for SPICE models, libraries, and includes."""

    def __init__(self, workspace_root: Optional[Union[str, Path]] = None):
        self.workspace_root = Path(workspace_root).resolve() if workspace_root else Path.cwd()

    def parse(self, model_file: Union[str, Path], recursive: bool = True) -> ModelInfo:
        """Parse a SPICE model file and return a ModelInfo object."""
        model_path = Path(model_file).resolve()
        if not model_path.exists():
            raise FileNotFoundError(f"SPICE model file not found: {model_path}")

        visited_files: Set[Path] = set()
        devices: List[DeviceSpec] = []
        includes: List[Path] = []

        self._parse_file(model_path, devices, includes, visited_files, recursive=recursive)

        # Post-process devices to refine defaults
        for dev in devices:
            self._refine_device_spec(dev)

        return ModelInfo(
            source_file=model_path,
            devices=devices,
            includes=includes,
        )

    def _parse_file(
        self,
        file_path: Path,
        devices: List[DeviceSpec],
        includes: List[Path],
        visited: Set[Path],
        recursive: bool = True,
    ) -> None:
        """Parse a single file and optionally recurse into includes."""
        if file_path in visited:
            return
        visited.add(file_path)

        try:
            content = file_path.read_text(errors="replace")
        except Exception:
            return

        # Preprocess lines (join continuations, strip comments)
        logical_lines = self._get_logical_lines(content)

        in_subckt = False
        current_subckt_name = ""
        current_subckt_pins: List[str] = []
        current_subckt_lines: List[str] = []

        for line in logical_lines:
            tokens = line.strip().split()
            if not tokens:
                continue

            first = tokens[0].lower()

            # Handle .include / .inc
            if first in [".include", ".inc"]:
                inc_target = self._resolve_include_path(line, file_path.parent)
                if inc_target and inc_target.exists():
                    includes.append(inc_target)
                    if recursive:
                        self._parse_file(inc_target, devices, includes, visited, recursive=recursive)
                continue

            # Handle .lib <path> <corner>
            if first == ".lib":
                # Some .lib lines include another file: .lib 'filename' corner
                if len(tokens) >= 2:
                    inc_target = self._resolve_include_path(line, file_path.parent)
                    if inc_target and inc_target.exists():
                        includes.append(inc_target)
                        if recursive:
                            self._parse_file(inc_target, devices, includes, visited, recursive=recursive)
                continue

            # Handle .subckt start
            if first == ".subckt":
                in_subckt = True
                current_subckt_name = tokens[1] if len(tokens) > 1 else "unknown"
                # Extract pins before params: or key=value
                current_subckt_pins = []
                for tok in tokens[2:]:
                    if "=" in tok or tok.lower().startswith("param"):
                        break
                    current_subckt_pins.append(tok)
                current_subckt_lines = [line]
                continue

            # Handle .ends end
            if first == ".ends":
                if in_subckt:
                    dev = self._analyze_subcircuit(
                        current_subckt_name,
                        current_subckt_pins,
                        current_subckt_lines,
                        file_path,
                    )
                    if dev:
                        # Avoid duplicates
                        if not any(d.name.lower() == dev.name.lower() for d in devices):
                            devices.append(dev)
                in_subckt = False
                current_subckt_name = ""
                current_subckt_pins = []
                current_subckt_lines = []
                continue

            if in_subckt:
                current_subckt_lines.append(line)
                # Note: models inside subckts are local to subcircuit, but we still record them if relevant
                continue

            # Handle .model outside subcircuit
            if first == ".model":
                dev = self._parse_model_directive(line, file_path)
                if dev and not any(d.name.lower() == dev.name.lower() for d in devices):
                    devices.append(dev)

    def _get_logical_lines(self, content: str) -> List[str]:
        """Combine line continuations (+) and clean comments."""
        raw_lines = content.splitlines()
        logical: List[str] = []
        current = ""

        for line in raw_lines:
            # Strip comments
            # Full line comment starts with * or $ or //
            stripped = line.strip()
            if not stripped or stripped.startswith(("*", "//")):
                continue

            # Strip inline comment (starting with ; or // or $)
            # Avoid stripping inside quoted strings
            cleaned = self._strip_inline_comments(stripped)
            if not cleaned:
                continue

            if cleaned.startswith("+"):
                current += " " + cleaned[1:].strip()
            else:
                if current:
                    logical.append(current.strip())
                current = cleaned

        if current:
            logical.append(current.strip())

        return logical

    def _strip_inline_comments(self, line: str) -> str:
        """Strip inline comments while preserving quoted strings."""
        in_quote = False
        quote_char = ""
        res = []
        i = 0
        n = len(line)
        while i < n:
            ch = line[i]
            if ch in ['"', "'"]:
                if not in_quote:
                    in_quote = True
                    quote_char = ch
                elif ch == quote_char:
                    in_quote = False
            elif not in_quote:
                if ch == ";" or (ch == "/" and i + 1 < n and line[i + 1] == "/"):
                    break
                if ch == "$" and (i == 0 or line[i - 1].isspace()):
                    break
            res.append(ch)
            i += 1
        return "".join(res).strip()

    def _resolve_include_path(self, line: str, parent_dir: Path) -> Optional[Path]:
        """Resolve .inc / .include path relative to parent directory or workspace root."""
        # Find path inside quotes or as token
        m = re.search(r'(?:\.include|\.inc|\.lib)\s+["\']?([^"\'\s]+)["\']?', line, re.IGNORECASE)
        if not m:
            return None
        raw_path = m.group(1).strip()
        candidate = Path(raw_path)

        if candidate.is_absolute() and candidate.exists():
            return candidate

        # Try relative to parent_dir
        rel_parent = (parent_dir / candidate).resolve()
        if rel_parent.exists():
            return rel_parent

        # Try relative to workspace root
        rel_ws = (self.workspace_root / candidate).resolve()
        if rel_ws.exists():
            return rel_ws

        # Try models/public-models relative path
        models_root = self.workspace_root / "models" / "public-models"
        rel_models = (models_root / candidate).resolve()
        if rel_models.exists():
            return rel_models

        return None

    def _parse_model_directive(self, line: str, file_path: Path) -> Optional[DeviceSpec]:
        """Parse a .model line into a DeviceSpec."""
        # Format: .model <name> <type> [(params...)]
        m = re.match(r'^\.model\s+(\w+)\s+(\w+)(?:\s*\(?\s*(.*)\)?)?', line, re.IGNORECASE)
        if not m:
            return None

        name = m.group(1)
        m_type = m.group(2).lower()
        param_str = m.group(3) or ""

        polarity = "unknown"
        if m_type in ["nmos", "nch", "nfet", "nmos_vtg", "nmos_bsim4", "nmos_bsimcmg"] or "nmos" in m_type or "nfet" in m_type:
            polarity = "nmos"
        elif m_type in ["pmos", "pch", "pfet", "pmos_vtg", "pmos_bsim4", "pmos_bsimcmg"] or "pmos" in m_type or "pfet" in m_type:
            polarity = "pmos"
        elif m_type in ["npn"]:
            polarity = "npn"
        elif m_type in ["pnp"]:
            polarity = "pnp"
        elif m_type in ["d", "diode"]:
            polarity = "diode"

        # Check name if type was generic
        if polarity == "unknown":
            name_lower = name.lower()
            if any(k in name_lower for k in ["nmos", "nch", "nfet", "n_"]):
                polarity = "nmos"
            elif any(k in name_lower for k in ["pmos", "pch", "pfet", "p_"]):
                polarity = "pmos"

        # Parse key=value parameters
        params = {}
        for match in re.finditer(r'(\w+)\s*=\s*([^\s\(\)]+)', param_str):
            key = match.group(1).upper()
            val = match.group(2).strip().rstrip(")")
            params[key] = val

        level = int(params["LEVEL"]) if "LEVEL" in params and params["LEVEL"].isdigit() else None
        version = params.get("VERSION")

        l_val = parse_spice_val(params.get("LMIN")) or parse_spice_val(params.get("L")) or 45e-9
        w_val = parse_spice_val(params.get("WMIN")) or parse_spice_val(params.get("W")) or 10e-6
        vth0 = parse_spice_val(params.get("VTH0"))
        tox = parse_spice_val(params.get("TOX")) or parse_spice_val(params.get("TOXE"))

        return DeviceSpec(
            name=name,
            polarity=polarity,
            device_type="primitive",
            level=level,
            version=version,
            pins=["d", "g", "s", "b"],
            default_l=l_val,
            default_w=w_val,
            vth0=vth0,
            tox=tox,
            params=params,
            source_file=file_path,
        )

    def _analyze_subcircuit(
        self,
        subckt_name: str,
        pins: List[str],
        lines: List[str],
        file_path: Path,
    ) -> Optional[DeviceSpec]:
        """Analyze a .subckt definition to see if it represents a 3-pin or 4-pin MOSFET/transistor."""
        # Filter out multi-transistor cells (like NAND, NOR, Inverter) unless they are 4-terminal FET subcircuits
        if len(pins) not in [3, 4, 5]:
            return None

        # Look for polarity hints in name
        name_lower = subckt_name.lower()
        polarity = "unknown"
        if any(k in name_lower for k in ["nfet", "nmos", "nch", "lv_nmos", "nsvt", "nlvt"]):
            polarity = "nmos"
        elif any(k in name_lower for k in ["pfet", "pmos", "pch", "lv_pmos", "psvt", "plvt"]):
            polarity = "pmos"

        # Look inside subcircuit lines for internal MOSFET instance
        has_fet = False
        default_l = 45e-9
        default_w = 10e-6
        for l in lines:
            l_strip = l.strip().lower()
            if l_strip.startswith("m"):
                has_fet = True
                if "nmos" in l_strip or "nfet" in l_strip:
                    polarity = "nmos"
                elif "pmos" in l_strip or "pfet" in l_strip:
                    polarity = "pmos"
                # Check for default L, W
                m_l = re.search(r'\bl\s*=\s*([^\s]+)', l_strip)
                m_w = re.search(r'\bw\s*=\s*([^\s]+)', l_strip)
                if m_l:
                    parsed_l = parse_spice_val(m_l.group(1))
                    if parsed_l: default_l = parsed_l
                if m_w:
                    parsed_w = parse_spice_val(m_w.group(1))
                    if parsed_w: default_w = parsed_w

        if not has_fet and polarity == "unknown":
            return None

        return DeviceSpec(
            name=subckt_name,
            polarity=polarity if polarity != "unknown" else "nmos",
            device_type="subcircuit",
            pins=pins[:4] if len(pins) >= 4 else pins + ["b"],
            default_l=default_l,
            default_w=default_w,
            source_file=file_path,
        )

    def _refine_device_spec(self, dev: DeviceSpec) -> None:
        """Infer default Vdd and reasonable geometry for the device."""
        name_lower = dev.name.lower()

        # Infer nominal Vdd from device name or oxide thickness
        if "01v8" in name_lower or "1v8" in name_lower:
            dev.default_vdd = 1.8
            dev.default_l = max(dev.default_l, 0.15e-6)
        elif "03v3" in name_lower or "3v3" in name_lower or "3.3" in name_lower:
            dev.default_vdd = 3.3
            dev.default_l = max(dev.default_l, 0.28e-6)
        elif "05v0" in name_lower or "5v0" in name_lower or "5.0" in name_lower:
            dev.default_vdd = 5.0
            dev.default_l = max(dev.default_l, 0.5e-6)
        elif "01v2" in name_lower or "1v2" in name_lower:
            dev.default_vdd = 1.2
        elif "01v0" in name_lower or "1v0" in name_lower or "nom" in name_lower:
            dev.default_vdd = 1.0
        elif dev.tox and dev.tox > 3e-9:
            dev.default_vdd = 3.3
        elif dev.tox and dev.tox > 2e-9:
            dev.default_vdd = 1.8
        else:
            dev.default_vdd = 1.2

        # Level 72 (BSIM-CMG FinFET / Nanosheet) usually has NFIN and small L
        if dev.level == 72 or any(k in name_lower for k in ["fin", "cmg", "nanosheet", "gaa"]):
            dev.default_vdd = 0.75
            dev.default_l = 12e-9 if dev.default_l > 1e-6 else dev.default_l
            dev.instance_params = "NFIN=2"
