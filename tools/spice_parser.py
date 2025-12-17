#!/usr/bin/env python3
"""
SPICE Model File AST Parser

A universal parser for SPICE model files that works across different PDKs and formats
(NGSPICE, HSPICE, Spectre .scs, etc.)

Features:
- Parse .model statements (model definitions)
- Parse .subckt statements (subcircuit definitions with port order)
- Parse .lib/.include statements (file inclusion)
- Extract all SPICE parameters (key=value pairs)
- Handle continuation lines (+)
- Case-insensitive parsing
- Support for multiple SPICE dialects

Usage:
    from spice_parser import SPICEParser, SPICEModelExtractor
    
    parser = SPICEParser()
    ast = parser.parse_file("model.inc")
    
    extractor = SPICEModelExtractor(ast)
    models = extractor.get_all_models()
    for model in models:
        print(f"Model: {model.name}, Type: {model.device_type}")
        print(f"Parameters: {model.parameters}")
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Optional, Union, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class SPICEStatementType(Enum):
    """Types of SPICE statements"""
    MODEL = "model"           # .model statement
    SUBCKT = "subckt"         # .subckt statement
    ENDS = "ends"             # .ends statement
    LIB = "lib"               # .lib statement
    INCLUDE = "include"       # .include/.inc statement
    PARAM = "param"           # .param statement
    OPTION = "option"         # .option statement
    CONTROL = "control"       # .control block
    DEVICE = "device"         # Device instance (M, R, C, etc.)
    COMMENT = "comment"       # Comment line
    UNKNOWN = "unknown"       # Unknown statement


@dataclass
class SPICEParameter:
    """Represents a SPICE parameter (key=value pair)"""
    name: str
    value: Union[str, float, int]
    unit: Optional[str] = None
    
    def __repr__(self):
        if self.unit:
            return f"{self.name}={self.value}{self.unit}"
        return f"{self.name}={self.value}"


@dataclass
class SPICEModel:
    """Represents a .model statement"""
    name: str
    device_type: str  # nmos, pmos, npn, pnp, resistor, etc.
    level: Optional[int] = None
    parameters: Dict[str, SPICEParameter] = field(default_factory=dict)
    raw_line: str = ""
    line_number: int = 0
    
    def get_parameter(self, name: str) -> Optional[SPICEParameter]:
        """Get parameter by name (case-insensitive)"""
        name_lower = name.lower()
        for key, value in self.parameters.items():
            if key.lower() == name_lower:
                return value
        return None


@dataclass
class SPICESubcircuit:
    """Represents a .subckt statement"""
    name: str
    ports: List[str]  # Port names in order
    parameters: Dict[str, SPICEParameter] = field(default_factory=dict)
    internal_statements: List[Any] = field(default_factory=list)
    raw_line: str = ""
    line_number: int = 0


@dataclass
class SPICEInclude:
    """Represents an .include or .lib statement"""
    file_path: str
    section: Optional[str] = None  # For .lib statements
    statement_type: str = "include"  # "include" or "lib"
    line_number: int = 0


@dataclass
class SPICEDevice:
    """Represents a device instance (M1, R1, C1, etc.)"""
    name: str
    device_type: str  # First character: M, R, C, etc.
    nodes: List[str]
    model_name: Optional[str] = None
    parameters: Dict[str, SPICEParameter] = field(default_factory=dict)
    line_number: int = 0


@dataclass
class SPICEAST:
    """Abstract Syntax Tree for SPICE file"""
    models: List[SPICEModel] = field(default_factory=list)
    subcircuits: List[SPICESubcircuit] = field(default_factory=list)
    includes: List[SPICEInclude] = field(default_factory=list)
    devices: List[SPICEDevice] = field(default_factory=list)
    parameters: Dict[str, SPICEParameter] = field(default_factory=dict)
    comments: List[Tuple[int, str]] = field(default_factory=list)
    raw_lines: List[str] = field(default_factory=list)


class ModelFileType(Enum):
    SPICE = "spice"
    VERILOGA = "veriloga"
    DATA = "data"
    UNKNOWN = "unknown"


@dataclass
class UnifiedModel:
    backend: str
    name: str
    ports: List[str] = field(default_factory=list)
    parameters: Dict[str, SPICEParameter] = field(default_factory=dict)
    source: Optional[str] = None
    line_number: Optional[int] = None
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UnifiedParseResult:
    backend: str
    source: str
    models: List[UnifiedModel] = field(default_factory=list)
    includes: List[str] = field(default_factory=list)
    data_files: List[str] = field(default_factory=list)
    parameters: Dict[str, SPICEParameter] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)


def _strip_verilog_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"//.*?$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\(\*.*?\*\)", "", text, flags=re.DOTALL)
    return text


def _split_top_level_commas(s: str) -> List[str]:
    parts: List[str] = []
    cur: List[str] = []
    depth = 0
    for ch in s:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth = max(depth - 1, 0)
        if ch == "," and depth == 0:
            parts.append("".join(cur).strip())
            cur = []
            continue
        cur.append(ch)
    tail = "".join(cur).strip()
    if tail:
        parts.append(tail)
    return parts


def _find_string_literals(text: str) -> List[str]:
    vals: List[str] = []
    for m in re.finditer(r"\"([^\"\n]+)\"", text):
        vals.append(m.group(1))
    for m in re.finditer(r"\'([^\'\n]+)\'", text):
        vals.append(m.group(1))
    return vals


def _looks_like_spice(text: str) -> bool:
    low = text.lower()
    return any(tok in low for tok in (".model", ".subckt", ".include", ".inc", ".lib"))


def detect_model_file_type(file_path: Union[str, Path]) -> ModelFileType:
    p = Path(file_path)
    suf = p.suffix.lower()
    if suf in {".va", ".vams"}:
        return ModelFileType.VERILOGA
    if suf in {".json", ".yaml", ".yml", ".csv", ".tsv", ".tbl", ".lut", ".dat", ".txt", ".npy", ".npz"}:
        return ModelFileType.DATA
    if suf in {".sp", ".cir", ".lib", ".inc", ".scs"}:
        return ModelFileType.SPICE
    try:
        txt = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ModelFileType.UNKNOWN
    if _looks_like_spice(txt):
        return ModelFileType.SPICE
    vtxt = _strip_verilog_comments(txt)
    if re.search(r"\bmodule\b", vtxt) and (
        re.search(r"\banalog\b", vtxt) or re.search(r"\belectrical\b", vtxt)
    ):
        return ModelFileType.VERILOGA
    if suf == ".v" and (re.search(r"\banalog\b", vtxt) or re.search(r"\belectrical\b", vtxt)):
        return ModelFileType.VERILOGA
    if suf in {".json", ".yaml", ".yml"}:
        return ModelFileType.DATA
    return ModelFileType.UNKNOWN


class SPICETokenizer:
    """Tokenize SPICE file handling continuation lines and comments"""
    
    def __init__(self):
        self.lines = []
        self.current_line = 0
    
    def tokenize_file(self, file_path: Union[str, Path]) -> List[Tuple[int, str]]:
        """Read and tokenize a SPICE file
        
        Returns:
            List of (line_number, logical_line) tuples where continuation lines
            are merged into logical lines
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            raw_lines = f.readlines()
        
        return self.tokenize_lines(raw_lines)
    
    def tokenize_lines(self, raw_lines: List[str]) -> List[Tuple[int, str]]:
        """Tokenize lines handling continuation and comments
        
        Args:
            raw_lines: List of raw text lines
            
        Returns:
            List of (line_number, logical_line) tuples
        """
        logical_lines = []
        current_logical = ""
        current_line_num = 0
        
        for i, line in enumerate(raw_lines, start=1):
            # Remove inline comments (;)
            if ';' in line:
                line = line.split(';')[0]
            
            # Strip line
            line = line.rstrip('\n\r')
            
            # Skip empty lines
            if not line.strip():
                continue
            
            # Check if this is a comment line (starts with *)
            if line.lstrip().startswith('*'):
                if current_logical:
                    logical_lines.append((current_line_num, current_logical.strip()))
                    current_logical = ""
                logical_lines.append((i, line))
                continue
            
            # Check for continuation line (starts with +)
            if line.lstrip().startswith('+'):
                # Continuation line - append to current logical line
                current_logical += " " + line.lstrip()[1:].strip()
            else:
                # New statement
                if current_logical:
                    logical_lines.append((current_line_num, current_logical.strip()))
                current_logical = line.strip()
                current_line_num = i
        
        # Don't forget the last line
        if current_logical:
            logical_lines.append((current_line_num, current_logical.strip()))
        
        return logical_lines


class SPICEParser:
    """Parse SPICE files into AST"""
    
    def __init__(self):
        self.tokenizer = SPICETokenizer()
        # Regex patterns
        self.unit_pattern = re.compile(r'([0-9.eE+-]+)\s*([afpnumkMGT]|meg|MEG)?')
    
    def parse_file(self, file_path: Union[str, Path]) -> SPICEAST:
        """Parse a SPICE file and return AST"""
        tokens = self.tokenizer.tokenize_file(file_path)
        return self.parse_tokens(tokens)
    
    def parse_tokens(self, tokens: List[Tuple[int, str]]) -> SPICEAST:
        """Parse tokenized lines into AST"""
        ast = SPICEAST()
        
        i = 0
        while i < len(tokens):
            line_num, line = tokens[i]
            ast.raw_lines.append(line)
            
            # Skip empty lines
            if not line.strip():
                i += 1
                continue
            
            # Comments
            if line.startswith('*'):
                ast.comments.append((line_num, line))
                i += 1
                continue
            
            # Determine statement type
            line_lower = line.lower().strip()
            
            if line_lower.startswith('.model'):
                # Each logical line produced by the tokenizer already has
                # continuation lines (+ ...) merged in, so we can parse this
                # .model statement directly without walking subsequent lines.
                model = self._parse_model(line, line_num)
                if model:
                    ast.models.append(model)
                i += 1
                continue
            
            elif line_lower.startswith('.subckt'):
                subckt = self._parse_subcircuit(line, line_num)
                if subckt:
                    ast.subcircuits.append(subckt)
            
            elif line_lower.startswith('.lib'):
                include = self._parse_lib(line, line_num)
                if include:
                    ast.includes.append(include)
            
            elif line_lower.startswith('.inc') or line_lower.startswith('.include'):
                include = self._parse_include(line, line_num)
                if include:
                    ast.includes.append(include)
            
            elif line_lower.startswith('.param'):
                params = self._parse_param(line)
                ast.parameters.update(params)
            
            elif self._is_device_line(line):
                device = self._parse_device(line, line_num)
                if device:
                    ast.devices.append(device)
            
            i += 1
        
        return ast
    
    def _parse_model(self, line: str, line_num: int) -> Optional[SPICEModel]:
        """Parse .model statement
        
        Format: .model model_name type [level=N] [param=value ...]
        Example: .model NMOS_VTG nmos level=54 vth0=0.4
        """
        parts = line.split()
        if len(parts) < 3:
            return None
        
        # parts[0] is '.model'
        model_name = parts[1]
        device_type = parts[2].lower()
        
        # Parse parameters
        parameters = {}
        level = None
        
        # Join remaining parts and parse parameters
        param_str = ' '.join(parts[3:])
        params = self._parse_parameters(param_str)
        
        # Extract level if present
        if 'level' in params:
            try:
                level = int(params['level'].value)
            except (ValueError, AttributeError):
                pass
        
        return SPICEModel(
            name=model_name,
            device_type=device_type,
            level=level,
            parameters=params,
            raw_line=line,
            line_number=line_num
        )
    
    def _parse_subcircuit(self, line: str, line_num: int) -> Optional[SPICESubcircuit]:
        """Parse .subckt statement
        
        Format: .subckt subckt_name port1 port2 ... [param=value ...]
        Example: .subckt sky130_fd_pr__nfet_01v8 D G S B w=1u l=0.15u
        """
        parts = line.split()
        if len(parts) < 2:
            return None
        
        # parts[0] is '.subckt'
        subckt_name = parts[1]
        
        # Separate ports from parameters
        ports = []
        param_parts = []
        
        for part in parts[2:]:
            if '=' in part:
                # This is a parameter
                param_parts.append(part)
            else:
                # This is a port
                ports.append(part)
        
        # Parse parameters
        param_str = ' '.join(param_parts)
        parameters = self._parse_parameters(param_str)
        
        return SPICESubcircuit(
            name=subckt_name,
            ports=ports,
            parameters=parameters,
            raw_line=line,
            line_number=line_num
        )
    
    def _parse_lib(self, line: str, line_num: int) -> Optional[SPICEInclude]:
        """Parse .lib statement
        
        Format: .lib "filename" section_name
        Example: .lib "../models/corner.lib" tt
        """
        # Remove .lib and split
        content = line[4:].strip()
        
        # Try to extract filename (may be quoted)
        file_match = re.search(r'["\']([^"\']+)["\']|(\S+)', content)
        if not file_match:
            return None
        
        file_path = file_match.group(1) or file_match.group(2)
        
        # Try to get section name (after filename)
        remainder = content[file_match.end():].strip()
        section = remainder.split()[0] if remainder else None
        
        return SPICEInclude(
            file_path=file_path,
            section=section,
            statement_type="lib",
            line_number=line_num
        )
    
    def _parse_include(self, line: str, line_num: int) -> Optional[SPICEInclude]:
        """Parse .include or .inc statement
        
        Format: .include "filename"
        Example: .include "../models/nmos.inc"
        """
        # Remove .include/.inc and get filename
        if line.lower().startswith('.include'):
            content = line[8:].strip()
        else:
            content = line[4:].strip()
        
        # Try to extract filename (may be quoted)
        file_match = re.search(r'["\']([^"\']+)["\']|(\S+)', content)
        if not file_match:
            return None
        
        file_path = file_match.group(1) or file_match.group(2)
        
        return SPICEInclude(
            file_path=file_path,
            statement_type="include",
            line_number=line_num
        )
    
    def _parse_param(self, line: str) -> Dict[str, SPICEParameter]:
        """Parse .param statement
        
        Format: .param name=value name2=value2 ...
        """
        # Remove .param
        content = line.split(None, 1)[1] if len(line.split()) > 1 else ""
        return self._parse_parameters(content)
    
    def _parse_parameters(self, param_str: str) -> Dict[str, SPICEParameter]:
        """Parse parameter string into dict of SPICEParameter objects
        
        Args:
            param_str: String like "vth0=0.4 tox=2.5e-9 w=10u" or "vth0 = 0.4 tox = 2.5e-9"
            
        Returns:
            Dict mapping parameter names to SPICEParameter objects
        """
        parameters = {}
        
        # Use regex to handle both "key=value" and "key = value" formats
        # Pattern matches: word characters + optional spaces + = + optional spaces + value
        import re
        param_pattern = re.compile(r'(\w+)\s*=\s*([^\s=]+)')
        
        matches = param_pattern.findall(param_str)
        
        for key, value_str in matches:
            key = key.strip().lower()
            value_str = value_str.strip()
            
            # Skip empty values
            if not value_str:
                continue
            
            # Try to parse value with unit
            value, unit = self._parse_value_with_unit(value_str)
            
            parameters[key] = SPICEParameter(
                name=key,
                value=value,
                unit=unit
            )
        
        return parameters
    
    def _parse_value_with_unit(self, value_str: str) -> Tuple[Union[float, str], Optional[str]]:
        """Parse a value string that may have a unit suffix
        
        Args:
            value_str: String like "10u", "2.5e-9", "1.2V"
            
        Returns:
            (value, unit) tuple where value is float or string, unit is optional string
        """
        # Try numeric match with optional unit
        match = self.unit_pattern.match(value_str)
        if match:
            num_str = match.group(1)
            unit = match.group(2)
            
            try:
                # Convert to float
                value = float(num_str)
                
                # Apply unit multiplier if numeric
                if unit:
                    multipliers = {
                        'f': 1e-15, 'p': 1e-12, 'n': 1e-9,
                        'u': 1e-6, 'm': 1e-3, 'k': 1e3,
                        'K': 1e3, 'M': 1e6, 'meg': 1e6,
                        'MEG': 1e6, 'G': 1e9, 'T': 1e12
                    }
                    if unit in multipliers:
                        value *= multipliers[unit]
                        return value, unit
                
                return value, unit
            except ValueError:
                pass
        
        # If not numeric, return as string
        return value_str, None
    
    def _is_device_line(self, line: str) -> bool:
        """Check if line is a device instance (M1, R1, C1, etc.)"""
        if not line:
            return False
        first_char = line[0].upper()
        # Device lines start with specific letters
        return first_char in 'MRCLDQJKXVIFGHESBAT'
    
    def _parse_device(self, line: str, line_num: int) -> Optional[SPICEDevice]:
        """Parse device instance line.

        We try to be robust for the two cases we care most about:

        - MOSFETs: ``M1 drain gate source bulk model_name [params]``
        - Subcircuits: ``X1 n1 n2 ... subckt_name [params]``

        The strategy is:
        - Split the statement into tokens.
        - Separate tokens *before* the first "param" token (containing ``=``)
          from the parameter tokens.
        - For ``M...`` devices, treat the first four pre-param tokens as nodes
          and the fifth as model name when available.
        - For ``X...`` devices, treat all but the last pre-param token as
          nodes and the last one as the subcircuit name.
        """

        parts = line.split()
        if len(parts) < 2:
            return None

        device_name = parts[0]
        device_type = device_name[0].upper()

        body = parts[1:]
        pre_param: List[str] = []
        param_parts: List[str] = []

        for part in body:
            if '=' in part:
                param_parts.append(part)
            else:
                pre_param.append(part)

        nodes: List[str] = []
        model_name: Optional[str] = None

        if device_type == 'M' and len(pre_param) >= 5:
            # M1 d g s b model_name ...
            nodes = pre_param[:4]
            model_name = pre_param[4]
        elif device_type == 'X' and len(pre_param) >= 2:
            # X1 n1 n2 ... subckt_name
            nodes = pre_param[:-1]
            model_name = pre_param[-1]
        else:
            # Fallback: treat all as nodes; model name unknown
            nodes = pre_param

        # Parse parameters
        param_str = ' '.join(param_parts)
        parameters = self._parse_parameters(param_str)

        return SPICEDevice(
            name=device_name,
            device_type=device_type,
            nodes=nodes,
            model_name=model_name,
            parameters=parameters,
            line_number=line_num,
        )


class SPICEModelExtractor:
    """Extract and query information from SPICE AST"""
    
    def __init__(self, ast: SPICEAST):
        self.ast = ast
    
    def get_all_models(self) -> List[SPICEModel]:
        """Get all .model definitions"""
        return self.ast.models
    
    def get_all_subcircuits(self) -> List[SPICESubcircuit]:
        """Get all .subckt definitions"""
        return self.ast.subcircuits
    
    def get_models_by_type(self, device_type: str) -> List[SPICEModel]:
        """Get models of specific type (nmos, pmos, etc.)"""
        device_type = device_type.lower()
        return [m for m in self.ast.models if m.device_type.lower() == device_type]
    
    def get_model_by_name(self, name: str) -> Optional[SPICEModel]:
        """Get model by name (case-insensitive)"""
        name_lower = name.lower()
        for model in self.ast.models:
            if model.name.lower() == name_lower:
                return model
        return None
    
    def get_subcircuit_by_name(self, name: str) -> Optional[SPICESubcircuit]:
        """Get subcircuit by name (case-insensitive)"""
        name_lower = name.lower()
        for subckt in self.ast.subcircuits:
            if subckt.name.lower() == name_lower:
                return subckt
        return None
    
    def get_nmos_models(self) -> List[SPICEModel]:
        """Get all NMOS models"""
        return self.get_models_by_type('nmos')
    
    def get_pmos_models(self) -> List[SPICEModel]:
        """Get all PMOS models"""
        return self.get_models_by_type('pmos')
    
    def get_includes(self) -> List[SPICEInclude]:
        """Get all .include and .lib statements"""
        return self.ast.includes
    
    def suggest_default_device(self) -> Optional[Union[SPICEModel, SPICESubcircuit]]:
        """Suggest a default NMOS device for benchmarking
        
        Heuristic: prefer models/subckts with names containing:
        - 'core', '01v8', '1v8', 'nom', 'vtg', 'typ', 'tt'
        """
        # Try NMOS models first
        nmos_models = self.get_nmos_models()
        
        # Scoring heuristic
        def score_name(name: str) -> int:
            name_lower = name.lower()
            score = 0
            keywords = ['core', '01v8', '1v8', 'nom', 'vtg', 'typ', 'tt', 'standard']
            for kw in keywords:
                if kw in name_lower:
                    score += 10
            # Penalize special variants
            penalties = ['hvt', 'lvt', 'thk', 'native', 'nat', 'esd']
            for pen in penalties:
                if pen in name_lower:
                    score -= 5
            return score
        
        if nmos_models:
            best_model = max(nmos_models, key=lambda m: score_name(m.name))
            return best_model
        
        # Try NMOS subcircuits
        nmos_subckts = [s for s in self.ast.subcircuits 
                        if 'nmos' in s.name.lower() or 'nfet' in s.name.lower()]
        if nmos_subckts:
            best_subckt = max(nmos_subckts, key=lambda s: score_name(s.name))
            return best_subckt
        
        return None
    
    def infer_vdd(self) -> float:
        """Infer recommended VDD from model/subcircuit names
        
        Returns:
            Estimated VDD voltage in volts
        """
        # Check model/subcircuit names for voltage hints
        all_names = ([m.name for m in self.ast.models] + 
                     [s.name for s in self.ast.subcircuits])
        
        for name in all_names:
            name_lower = name.lower()
            # Look for voltage indicators
            if '01v8' in name_lower or '1v8' in name_lower or '1.8v' in name_lower:
                return 1.8
            if '3v3' in name_lower or '3.3v' in name_lower:
                return 3.3
            if '5v' in name_lower or '5.0v' in name_lower:
                return 5.0
            if '10v' in name_lower:
                return 10.0
        
        # Check for vth0 parameter to estimate
        nmos_models = self.get_nmos_models()
        if nmos_models:
            for model in nmos_models:
                vth_param = model.get_parameter('vth0')
                if vth_param and isinstance(vth_param.value, (int, float)):
                    vth = abs(vth_param.value)
                    # Estimate VDD as 3-4x Vth
                    estimated_vdd = vth * 3.5
                    # Round to common values
                    if estimated_vdd < 1.4:
                        return 1.2
                    elif estimated_vdd < 2.0:
                        return 1.8
                    elif estimated_vdd < 2.8:
                        return 2.5
                    else:
                        return 3.3
        
        # Default fallback
        return 1.8
    
    def export_summary(self) -> Dict[str, Any]:
        """Export a summary of parsed content"""
        return {
            'models': {
                'total': len(self.ast.models),
                'nmos': len(self.get_nmos_models()),
                'pmos': len(self.get_pmos_models()),
                'names': [m.name for m in self.ast.models]
            },
            'subcircuits': {
                'total': len(self.ast.subcircuits),
                'names': [s.name for s in self.ast.subcircuits],
                'ports': {s.name: s.ports for s in self.ast.subcircuits}
            },
            'includes': {
                'total': len(self.ast.includes),
                'files': [i.file_path for i in self.ast.includes]
            },
            'devices': {
                'total': len(self.ast.devices),
                'types': list(set(d.device_type for d in self.ast.devices))
            },
            'suggested_device': self.suggest_default_device(),
            'inferred_vdd': self.infer_vdd()
        }


class VerilogAParser:
    def __init__(self):
        self._spice = SPICEParser()

    def parse_file(self, file_path: Union[str, Path]) -> UnifiedParseResult:
        p = Path(file_path)
        text = p.read_text(encoding="utf-8", errors="ignore")
        stripped = _strip_verilog_comments(text)

        includes = self._extract_includes(stripped)
        models = self._extract_modules(stripped)
        data_files = self._extract_data_files(stripped)

        resolved_includes = [str(self._resolve_ref(p, inc)) for inc in includes]
        resolved_data = [str(self._resolve_ref(p, df)) for df in data_files]

        for m in models:
            m.source = str(p)

        return UnifiedParseResult(
            backend=ModelFileType.VERILOGA.value,
            source=str(p),
            models=models,
            includes=sorted(set(resolved_includes)),
            data_files=sorted(set(resolved_data)),
        )

    def _resolve_ref(self, base: Path, ref: str) -> Path:
        rp = Path(ref)
        if rp.is_absolute():
            return rp
        return (base.parent / rp).resolve()

    def _extract_includes(self, text: str) -> List[str]:
        bt = chr(96)
        pat = re.compile(
            re.escape(bt) + r"include\s+(?:\"([^\"]+)\"|\'([^\']+)\'|<([^>]+)>)",
            re.IGNORECASE,
        )
        out: List[str] = []
        for m in pat.finditer(text):
            out.append((m.group(1) or m.group(2) or m.group(3) or "").strip())
        return [x for x in out if x]

    def _extract_modules(self, text: str) -> List[UnifiedModel]:
        models: List[UnifiedModel] = []
        mod_pat = re.compile(r"\bmodule\s+([A-Za-z_][A-Za-z0-9_$]*)", re.IGNORECASE)
        for m in mod_pat.finditer(text):
            name = m.group(1)
            i = m.end()
            i = self._skip_ws(text, i)

            header_param_blob: Optional[str] = None
            if i < len(text) and text[i] == "#":
                i += 1
                i = self._skip_ws(text, i)
                if i < len(text) and text[i] == "(":
                    header_param_blob, i = self._extract_balanced_parens(text, i)
                    i = self._skip_ws(text, i)

            port_blob: Optional[str] = None
            if i < len(text) and text[i] == "(":
                port_blob, i = self._extract_balanced_parens(text, i)
                i = self._skip_ws(text, i)

            semi = text.find(";", i)
            if semi == -1:
                continue

            body_start = semi + 1
            body_end = text.find("endmodule", body_start)
            body = text[body_start:body_end] if body_end != -1 else text[body_start:]

            ports = self._parse_port_list(port_blob or "") if port_blob else []
            if not ports:
                ports = self._parse_port_decls(body)
            if not ports:
                ports = self._parse_electrical_decls(body)

            params = {}
            if header_param_blob:
                params.update(self._parse_parameter_list(header_param_blob))
            params.update(self._parse_parameter_decls(body))

            models.append(UnifiedModel(backend=ModelFileType.VERILOGA.value, name=name, ports=ports, parameters=params))
        return models

    def _skip_ws(self, text: str, i: int) -> int:
        while i < len(text) and text[i].isspace():
            i += 1
        return i

    def _extract_balanced_parens(self, text: str, i: int) -> Tuple[str, int]:
        if i >= len(text) or text[i] != "(":
            return "", i
        depth = 0
        start = i
        while i < len(text):
            ch = text[i]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    return text[start + 1 : i], i + 1
            i += 1
        return text[start + 1 :], len(text)

    def _parse_port_list(self, port_blob: str) -> List[str]:
        ports: List[str] = []
        for item in _split_top_level_commas(port_blob):
            tok = item.strip()
            if not tok:
                continue
            tok = re.sub(r"\[[^\]]*\]", " ", tok)
            tok = re.sub(r"\b(input|output|inout|electrical|wire|reg|integer|real)\b", " ", tok, flags=re.IGNORECASE)
            toks = [t for t in re.split(r"\s+", tok.strip()) if t]
            if not toks:
                continue
            ident = toks[-1]
            if re.match(r"^[A-Za-z_][A-Za-z0-9_$]*$", ident):
                ports.append(ident)
        return ports

    def _parse_port_decls(self, body: str) -> List[str]:
        ports: List[str] = []
        decl_pat = re.compile(r"\b(input|output|inout)\b\s+([^;]+);", re.IGNORECASE)
        for m in decl_pat.finditer(body):
            blob = m.group(2)
            blob = re.sub(r"\[[^\]]*\]", " ", blob)
            for item in _split_top_level_commas(blob):
                name = item.strip().split()[-1] if item.strip() else ""
                if name and re.match(r"^[A-Za-z_][A-Za-z0-9_$]*$", name):
                    ports.append(name)
        return ports

    def _parse_electrical_decls(self, body: str) -> List[str]:
        ports: List[str] = []
        decl_pat = re.compile(r"\b(electrical|terminal)\b\s+([^;]+);", re.IGNORECASE)
        for m in decl_pat.finditer(body):
            blob = m.group(2)
            blob = re.sub(r"\[[^\]]*\]", " ", blob)
            for item in _split_top_level_commas(blob):
                name = item.strip().split()[-1] if item.strip() else ""
                if name and re.match(r"^[A-Za-z_][A-Za-z0-9_$]*$", name):
                    ports.append(name)
        return ports

    def _parse_parameter_list(self, blob: str) -> Dict[str, SPICEParameter]:
        params: Dict[str, SPICEParameter] = {}
        decl = blob
        decl = re.sub(r"\bparameter\b", " ", decl, flags=re.IGNORECASE)
        decl = re.sub(r"\b(real|integer|int|string)\b", " ", decl, flags=re.IGNORECASE)
        decl = re.sub(r"\bfrom\b\s*(\[[^\]]*\]|\([^\)]*\))", " ", decl, flags=re.IGNORECASE)
        decl = re.sub(r"\bexclude\b\s*(\[[^\]]*\]|\([^\)]*\)|[^,\s]+)", " ", decl, flags=re.IGNORECASE)
        for item in _split_top_level_commas(decl):
            if "=" not in item:
                continue
            k, v = item.split("=", 1)
            key = k.strip().lower()
            if not key:
                continue
            expr = v.strip()
            token = expr.split()[0] if expr else expr
            val, unit = self._spice._parse_value_with_unit(token) if token else (expr, None)
            params[key] = SPICEParameter(name=key, value=val if token else expr, unit=unit)
        return params

    def _parse_parameter_decls(self, body: str) -> Dict[str, SPICEParameter]:
        params: Dict[str, SPICEParameter] = {}
        stmt_pat = re.compile(r"\bparameter\b\s+([^;]+);", re.IGNORECASE | re.DOTALL)
        for m in stmt_pat.finditer(body):
            decl = m.group(1)
            decl = re.sub(r"\b(real|integer|int|string)\b", " ", decl, flags=re.IGNORECASE)
            decl = re.sub(r"\bfrom\b\s*\([^\)]*\)", " ", decl, flags=re.IGNORECASE)
            decl = re.sub(r"\bexclude\b\s*\([^\)]*\)", " ", decl, flags=re.IGNORECASE)
            for item in _split_top_level_commas(decl):
                if "=" not in item:
                    continue
                k, v = item.split("=", 1)
                key = k.strip().lower()
                if not key:
                    continue
                expr = v.strip()
                token = expr.split()[0] if expr else expr
                val, unit = self._spice._parse_value_with_unit(token) if token else (expr, None)
                params[key] = SPICEParameter(name=key, value=val if token else expr, unit=unit)
        return params

    def _extract_data_files(self, text: str) -> List[str]:
        exts = {".dat", ".txt", ".csv", ".tsv", ".tbl", ".lut", ".npy", ".npz", ".json", ".yaml", ".yml"}
        out: List[str] = []
        for s in _find_string_literals(text):
            ext = Path(s).suffix.lower()
            if ext in exts:
                out.append(s.strip())
        return [x for x in out if x]


class DataModelParser:
    def __init__(self):
        self._spice = SPICEParser()

    def parse_file(self, file_path: Union[str, Path]) -> UnifiedParseResult:
        p = Path(file_path)
        suf = p.suffix.lower()
        if suf == ".json":
            return self._parse_json(p)
        if suf in {".yaml", ".yml"}:
            return self._parse_yaml(p)
        if suf in {".csv", ".tsv"}:
            return self._parse_delimited(p)
        if suf in {".tbl", ".lut", ".dat", ".txt"}:
            return self._parse_text_table(p)
        if suf in {".npy", ".npz"}:
            return UnifiedParseResult(
                backend=ModelFileType.DATA.value,
                source=str(p),
                models=[UnifiedModel(backend=ModelFileType.DATA.value, name=p.stem, source=str(p))],
                data_files=[str(p.resolve())],
            )
        return self._parse_yaml(p)

    def _resolve_ref(self, base: Path, ref: str) -> str:
        rp = Path(ref)
        if rp.is_absolute():
            return str(rp)
        return str((base.parent / rp).resolve())

    def _parse_json(self, p: Path) -> UnifiedParseResult:
        obj = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
        return self._from_object(obj, p)

    def _parse_yaml(self, p: Path) -> UnifiedParseResult:
        text = p.read_text(encoding="utf-8", errors="ignore")
        try:
            import yaml  # type: ignore

            obj = yaml.safe_load(text)
            if obj is None:
                obj = {}
            return self._from_object(obj, p)
        except Exception:
            simple_obj = self._parse_simple_yaml_like(text)
            if simple_obj is not None:
                return self._from_object(simple_obj, p)
            includes, data_files = self._extract_refs_from_text(text, p)
            return UnifiedParseResult(
                backend=ModelFileType.DATA.value,
                source=str(p),
                models=[UnifiedModel(backend=ModelFileType.DATA.value, name=p.stem, source=str(p))],
                includes=sorted(set(includes)),
                data_files=sorted(set(data_files)),
            )

    def _parse_simple_yaml_like(self, text: str) -> Optional[Dict[str, Any]]:
        lines = [ln.rstrip("\n") for ln in text.splitlines()]
        if not any(":" in ln for ln in lines):
            return None

        obj: Dict[str, Any] = {}

        def parse_list_val(v: str) -> Optional[List[str]]:
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                inner = v[1:-1]
                items = [x.strip().strip("\"'") for x in inner.split(",")]
                return [x for x in items if x]
            return None

        i = 0
        while i < len(lines):
            ln = lines[i]
            if not ln.strip() or ln.lstrip().startswith("#"):
                i += 1
                continue
            m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_\-]*)\s*:\s*(.*)$", ln)
            if not m:
                i += 1
                continue
            key = m.group(1).strip()
            rest = m.group(2).strip()
            if key.lower() in {"parameters", "params", "param"}:
                params: Dict[str, Any] = {}
                base_indent = len(ln) - len(ln.lstrip())
                i += 1
                while i < len(lines):
                    ln2 = lines[i]
                    if not ln2.strip() or ln2.lstrip().startswith("#"):
                        i += 1
                        continue
                    indent = len(ln2) - len(ln2.lstrip())
                    if indent <= base_indent:
                        break
                    m2 = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_\-]*)\s*:\s*(.*)$", ln2)
                    if m2:
                        pk = m2.group(1).strip()
                        pv = m2.group(2).strip().strip("\"'")
                        params[pk] = pv
                    i += 1
                obj["parameters"] = params
                continue

            if not rest:
                i += 1
                continue

            list_val = parse_list_val(rest)
            if list_val is not None:
                obj[key] = list_val
            else:
                obj[key] = rest.strip().strip("\"'")
            i += 1

        return obj if obj else None

    def _parse_delimited(self, p: Path) -> UnifiedParseResult:
        text = p.read_text(encoding="utf-8", errors="ignore")
        delim = "," if p.suffix.lower() == ".csv" else "\t"
        header = ""
        for ln in text.splitlines():
            if not ln.strip():
                continue
            if ln.lstrip().startswith("#"):
                continue
            header = ln
            break
        cols = [c.strip() for c in header.split(delim)] if header else []
        model = UnifiedModel(
            backend=ModelFileType.DATA.value,
            name=p.stem,
            source=str(p),
            meta={"columns": cols, "delimiter": delim},
        )
        return UnifiedParseResult(
            backend=ModelFileType.DATA.value,
            source=str(p),
            models=[model],
            data_files=[str(p.resolve())],
        )

    def _parse_text_table(self, p: Path) -> UnifiedParseResult:
        text = p.read_text(encoding="utf-8", errors="ignore")
        lines = [ln for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
        ncols = 0
        for ln in lines[:50]:
            parts = [x for x in re.split(r"\s+|,", ln.strip()) if x]
            if len(parts) >= 2:
                ncols = max(ncols, len(parts))
        model = UnifiedModel(
            backend=ModelFileType.DATA.value,
            name=p.stem,
            source=str(p),
            meta={"columns": ncols},
        )
        return UnifiedParseResult(
            backend=ModelFileType.DATA.value,
            source=str(p),
            models=[model],
            data_files=[str(p.resolve())],
        )

    def _extract_refs_from_text(self, text: str, p: Path) -> Tuple[List[str], List[str]]:
        includes: List[str] = []
        data_files: List[str] = []
        for s in _find_string_literals(text):
            ext = Path(s).suffix.lower()
            if ext in {".json", ".yaml", ".yml", ".va", ".vams", ".sp", ".cir", ".lib", ".inc", ".scs"}:
                includes.append(self._resolve_ref(p, s))
            if ext in {".dat", ".txt", ".csv", ".tsv", ".tbl", ".lut", ".npy", ".npz"}:
                data_files.append(self._resolve_ref(p, s))
        return includes, data_files

    def _from_object(self, obj: Any, p: Path) -> UnifiedParseResult:
        models: List[UnifiedModel] = []
        includes: List[str] = []
        data_files: List[str] = []
        params: Dict[str, SPICEParameter] = {}

        def add_params_from_mapping(d: Dict[Any, Any]):
            for k, v in d.items():
                key = str(k).strip().lower()
                if not key or key in params:
                    continue
                if isinstance(v, (int, float)):
                    params[key] = SPICEParameter(name=key, value=float(v), unit=None)
                elif isinstance(v, bool):
                    params[key] = SPICEParameter(name=key, value=str(v).lower(), unit=None)
                elif isinstance(v, str):
                    token = v.strip().split()[0] if v.strip() else v
                    val, unit = self._spice._parse_value_with_unit(token) if token else (v, None)
                    params[key] = SPICEParameter(name=key, value=val if token else v, unit=unit)

        def visit(node: Any):
            if isinstance(node, dict):
                for k, v in node.items():
                    lk = str(k).lower()
                    if lk in {"include", "includes", "files", "file"} and isinstance(v, (str, list)):
                        vals = [v] if isinstance(v, str) else v
                        for s in vals:
                            if isinstance(s, str):
                                includes.append(self._resolve_ref(p, s))
                    if lk in {"data", "data_file", "data_files", "lut", "table"} and isinstance(v, (str, list)):
                        vals = [v] if isinstance(v, str) else v
                        for s in vals:
                            if isinstance(s, str):
                                data_files.append(self._resolve_ref(p, s))
                    if lk in {"parameters", "params", "param"}:
                        if isinstance(v, dict):
                            add_params_from_mapping(v)
                        elif isinstance(v, list):
                            for it in v:
                                if isinstance(it, dict) and "name" in it and "value" in it:
                                    add_params_from_mapping({it.get("name"): it.get("value")})
                    if isinstance(v, str):
                        ext = Path(v).suffix.lower()
                        if ext in {".dat", ".txt", ".csv", ".tsv", ".tbl", ".lut", ".npy", ".npz"}:
                            data_files.append(self._resolve_ref(p, v))
                        if ext in {".json", ".yaml", ".yml", ".va", ".vams", ".sp", ".cir", ".lib", ".inc", ".scs"}:
                            includes.append(self._resolve_ref(p, v))
                    visit(v)
            elif isinstance(node, list):
                for it in node:
                    visit(it)

        visit(obj)

        root = obj if isinstance(obj, dict) else {}
        name = None
        for k in ("name", "model", "model_name", "device", "device_name"):
            v = root.get(k) if isinstance(root, dict) else None
            if isinstance(v, str) and v.strip():
                name = v.strip()
                break
        if name is None:
            name = p.stem

        ports: List[str] = []
        for k in ("ports", "terminals", "nodes", "pins"):
            v = root.get(k) if isinstance(root, dict) else None
            if isinstance(v, list) and all(isinstance(x, str) for x in v):
                ports = [x.strip() for x in v if x.strip()]
                break

        param_obj = None
        for k in ("parameters", "params", "param"):
            v = root.get(k) if isinstance(root, dict) else None
            if isinstance(v, dict):
                param_obj = v
                break
        if isinstance(param_obj, dict):
            add_params_from_mapping(param_obj)

        models.append(
            UnifiedModel(
                backend=ModelFileType.DATA.value,
                name=name,
                ports=ports,
                parameters=params,
                source=str(p),
            )
        )

        return UnifiedParseResult(
            backend=ModelFileType.DATA.value,
            source=str(p),
            models=models,
            includes=sorted(set(includes)),
            data_files=sorted(set(data_files)),
            parameters=params,
        )


class UniversalModelParser:
    def __init__(self, follow_includes: bool = False, max_include_depth: int = 3):
        self._spice = SPICEParser()
        self._va = VerilogAParser()
        self._data = DataModelParser()
        self._follow_includes = follow_includes
        self._max_include_depth = max_include_depth

    def parse_file(self, file_path: Union[str, Path]) -> UnifiedParseResult:
        p = Path(file_path)
        return self._parse_file_recursive(p.resolve(), visited=set(), depth=0)

    def _parse_file_recursive(self, p: Path, visited: set, depth: int) -> UnifiedParseResult:
        key = str(p)
        if key in visited:
            return UnifiedParseResult(backend=ModelFileType.UNKNOWN.value, source=str(p), meta={"cycle": True})
        visited.add(key)

        ftype = detect_model_file_type(p)
        if ftype == ModelFileType.SPICE:
            result = self._parse_spice_file(p)
        elif ftype == ModelFileType.VERILOGA:
            result = self._va.parse_file(p)
        elif ftype == ModelFileType.DATA:
            result = self._data.parse_file(p)
        else:
            result = UnifiedParseResult(backend=ModelFileType.UNKNOWN.value, source=str(p))

        if not self._follow_includes or depth >= self._max_include_depth:
            result.meta.setdefault("parsed_files", [str(p)])
            return result

        agg_models = list(result.models)
        agg_includes = list(result.includes)
        agg_data_files = list(result.data_files)
        agg_params = dict(result.parameters)
        parsed_files: List[str] = [str(p)]

        for inc in result.includes:
            ip = Path(inc)
            if not ip.exists() or not ip.is_file():
                continue
            sub = self._parse_file_recursive(ip.resolve(), visited=visited, depth=depth + 1)
            parsed_files.extend(sub.meta.get("parsed_files", [sub.source]) if isinstance(sub.meta.get("parsed_files"), list) else [sub.source])
            agg_models.extend(sub.models)
            agg_includes.extend(sub.includes)
            agg_data_files.extend(sub.data_files)
            for k, v in sub.parameters.items():
                if k not in agg_params:
                    agg_params[k] = v

        result.models = agg_models
        result.includes = sorted(set(agg_includes))
        result.data_files = sorted(set(agg_data_files))
        result.parameters = agg_params
        result.meta["parsed_files"] = sorted(set(parsed_files))
        return result

    def _parse_spice_file(self, p: Path) -> UnifiedParseResult:
        ast = self._spice.parse_file(p)
        extractor = SPICEModelExtractor(ast)
        models: List[UnifiedModel] = []
        for m in extractor.get_all_models():
            models.append(
                UnifiedModel(
                    backend=ModelFileType.SPICE.value,
                    name=m.name,
                    ports=[],
                    parameters=m.parameters,
                    source=str(p),
                    line_number=m.line_number,
                    meta={"device_type": m.device_type, "level": m.level},
                )
            )
        for s in extractor.get_all_subcircuits():
            models.append(
                UnifiedModel(
                    backend=ModelFileType.SPICE.value,
                    name=s.name,
                    ports=s.ports,
                    parameters=s.parameters,
                    source=str(p),
                    line_number=s.line_number,
                )
            )
        includes: List[str] = []
        for inc in extractor.get_includes():
            ip = Path(inc.file_path)
            includes.append(str(ip if ip.is_absolute() else (p.parent / ip).resolve()))
        return UnifiedParseResult(
            backend=ModelFileType.SPICE.value,
            source=str(p),
            models=models,
            includes=sorted(set(includes)),
            parameters=ast.parameters,
        )


def parse_model_file(
    file_path: Union[str, Path],
    follow_includes: bool = False,
    max_include_depth: int = 3,
) -> UnifiedParseResult:
    parser = UniversalModelParser(follow_includes=follow_includes, max_include_depth=max_include_depth)
    return parser.parse_file(file_path)


# Convenience function
def parse_spice_file(file_path: Union[str, Path]) -> Tuple[SPICEAST, SPICEModelExtractor]:
    """Parse a SPICE file and return AST and extractor
    
    Args:
        file_path: Path to SPICE model file
        
    Returns:
        (ast, extractor) tuple
        
    Example:
        ast, extractor = parse_spice_file("model.inc")
        models = extractor.get_all_models()
        summary = extractor.export_summary()
    """
    parser = SPICEParser()
    ast = parser.parse_file(file_path)
    extractor = SPICEModelExtractor(ast)
    return ast, extractor


if __name__ == "__main__":
    # Demo usage
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python spice_parser.py <spice_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    print(f"Parsing: {file_path}")
    print("=" * 60)
    
    ast, extractor = parse_spice_file(file_path)
    
    # Print summary
    summary = extractor.export_summary()
    print(json.dumps(summary, indent=2, default=str))
    
    print("\n" + "=" * 60)
    print("Models found:")
    for model in extractor.get_all_models():
        print(f"  - {model.name} ({model.device_type}, level={model.level})")
        print(f"    Parameters: {len(model.parameters)} params")
        if model.parameters:
            # Show first 3 parameters
            for i, (name, param) in enumerate(list(model.parameters.items())[:3]):
                print(f"      {param}")
    
    print("\n" + "=" * 60)
    print("Subcircuits found:")
    for subckt in extractor.get_all_subcircuits():
        print(f"  - {subckt.name}")
        print(f"    Ports: {', '.join(subckt.ports)}")
        if subckt.parameters:
            print(f"    Parameters: {list(subckt.parameters.keys())}")
