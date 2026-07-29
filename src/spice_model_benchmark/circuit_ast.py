"""Simulator-neutral AST and translators for benchmark test circuits.

The module deliberately models the *physical* part of a test deck (devices,
sources and analyses) separately from simulator presentation.  It is not a
model-card parser: model cards remain external includes and are handled by the
existing model pipeline.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union


class CircuitSyntaxError(ValueError):
    """Raised when a circuit cannot be represented without losing meaning."""


class Dialect(str, Enum):
    NGSPICE = "ngspice"
    HSPICE = "hspice"
    SPECTRE = "spectre"


_NUMBER_SUFFIXES = {
    "t": 1e12,
    "g": 1e9,
    "meg": 1e6,
    "k": 1e3,
    "m": 1e-3,
    "u": 1e-6,
    "n": 1e-9,
    "p": 1e-12,
    "f": 1e-15,
    "a": 1e-18,
}


def _number(value: str) -> Union[float, str]:
    value = value.strip().strip("{}")
    match = re.fullmatch(
        r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?)"
        r"(meg|[tgkmunpfa])?",
        value,
        re.IGNORECASE,
    )
    if not match:
        return value.lower()
    result = float(match.group(1))
    suffix = match.group(2)
    if suffix:
        result *= _NUMBER_SUFFIXES[suffix.lower()]
    return float(format(result, ".15g"))


def _value_text(value: Union[float, str]) -> str:
    if isinstance(value, float):
        return format(value, ".15g")
    return value


def _tokens(text: str) -> List[str]:
    """SPICE-aware tokenization retaining parenthesized source expressions."""
    return re.findall(
        r"\w+=\[[^\]]*\]|'[^']*'|\"[^\"]*\"|\([^)]*\)|\[[^\]]*\]|[^\s,]+",
        text,
    )


def _params(tokens: Sequence[str]) -> Tuple[List[str], Dict[str, str]]:
    positional: List[str] = []
    values: Dict[str, str] = {}
    for token in tokens:
        if "=" in token and not token.startswith("="):
            key, value = token.split("=", 1)
            values[key.lower()] = value
        else:
            positional.append(token)
    return positional, values


@dataclass
class Element:
    name: str
    kind: str
    nodes: List[str]
    value: Optional[str] = None
    model: Optional[str] = None
    parameters: Dict[str, str] = field(default_factory=dict)
    source: List[str] = field(default_factory=list)

    def semantic(self) -> Dict[str, object]:
        return {
            "name": self.name.lower(),
            "kind": self.kind.lower(),
            "nodes": [node.lower() for node in self.nodes],
            "value": _number(self.value) if self.value is not None else None,
            "model": self.model.lower() if self.model else None,
            "parameters": {
                key.lower(): _number(value)
                for key, value in sorted(self.parameters.items())
            },
            "source": [_number(token) for token in self.source],
        }


@dataclass
class Analysis:
    kind: str
    arguments: List[str]
    name: Optional[str] = None
    parameters: Dict[str, str] = field(default_factory=dict)
    temperature: Optional[str] = None
    temperature_values: List[str] = field(default_factory=list)
    alterations: Dict[str, str] = field(default_factory=dict)

    def semantic(self) -> Dict[str, object]:
        arguments: List[Union[float, str]] = [
            _number(arg) for arg in self.arguments
        ]
        parameters: Dict[str, Union[float, str]] = {
            key.lower(): _number(value)
            for key, value in sorted(self.parameters.items())
            if key.lower() != "temp"
        }
        for presentation_key in (
            "oppoint", "annotate", "maxiters", "errpreset", "cmin",
            "minstep", "method", "lteratio",
        ):
            parameters.pop(presentation_key, None)

        def normalize_values(key: str, suffix: str = "") -> None:
            raw = parameters.pop(key, None)
            if not isinstance(raw, str):
                return
            values = [_number(item) for item in _tokens(raw.strip("[]"))]
            if not values:
                return
            parameters.setdefault("start" + suffix, values[0])
            parameters.setdefault("stop" + suffix, values[-1])
            if len(values) > 1 and all(isinstance(item, float) for item in values):
                parameters.setdefault("step" + suffix, values[1] - values[0])
            else:
                parameters.setdefault("values" + suffix, raw)
        # Normalize the positional SPICE syntax and Spectre's named syntax to
        # one shape.  This makes equality independent of the source language.
        if self.kind == "tran":
            if "maxstep" in parameters:
                parameters.setdefault("step", parameters.pop("maxstep"))
            if arguments:
                parameters.setdefault("step", arguments[0])
            if len(arguments) > 1:
                parameters.setdefault("stop", arguments[1])
            if len(arguments) > 2:
                tail = arguments[2:]
                if tail and isinstance(tail[0], float):
                    parameters.setdefault("start", tail.pop(0))
                if tail:
                    parameters.setdefault("flags", " ".join(map(str, tail)))
            parameters.setdefault("start", 0.0)
            arguments = []
        elif self.kind == "ac":
            if len(arguments) >= 4:
                parameters.setdefault("sweeptype", arguments[0])
                parameters.setdefault("points", arguments[1])
                parameters.setdefault("start", arguments[2])
                parameters.setdefault("stop", arguments[3])
                arguments = arguments[4:]
            for sweep_kind in ("dec", "oct", "lin", "log"):
                if sweep_kind in parameters:
                    parameters.setdefault("sweeptype", sweep_kind)
                    parameters.setdefault("points", parameters.pop(sweep_kind))
                    break
            values = parameters.pop("values", None)
            if isinstance(values, str) and values.startswith("[") and values.endswith("]"):
                bounds = _tokens(values[1:-1])
                if bounds:
                    parameters.setdefault("start", _number(bounds[0]))
                    parameters.setdefault("stop", _number(bounds[-1]))
                    if len(bounds) == 1:
                        parameters.setdefault("sweeptype", "lin")
                        parameters.setdefault("points", 1.0)
        elif self.kind == "dc":
            if len(arguments) >= 4:
                parameters.setdefault("source", arguments[0])
                parameters.setdefault("start", arguments[1])
                parameters.setdefault("stop", arguments[2])
                parameters.setdefault("step", arguments[3])
                if len(arguments) >= 8:
                    parameters.setdefault("source2", arguments[4])
                    parameters.setdefault("start2", arguments[5])
                    parameters.setdefault("stop2", arguments[6])
                    parameters.setdefault("step2", arguments[7])
                arguments = arguments[8:]
            if "dev" in parameters:
                parameters.setdefault("source", parameters.pop("dev"))
            if "dev2" in parameters:
                parameters.setdefault("source2", parameters.pop("dev2"))
            normalize_values("values")
            normalize_values("values2", "2")
        elif self.kind == "noise" and len(arguments) >= 6:
            parameters.setdefault("output", arguments[0])
            parameters.setdefault("input", arguments[1])
            parameters.setdefault("sweeptype", arguments[2])
            parameters.setdefault("points", arguments[3])
            parameters.setdefault("start", arguments[4])
            parameters.setdefault("stop", arguments[5])
            arguments = arguments[6:]
        if self.kind == "noise":
            if "oprobe" in parameters:
                parameters.setdefault("output", parameters.pop("oprobe"))
            if "iprobe" in parameters:
                parameters.setdefault("input", parameters.pop("iprobe"))
            for sweep_kind in ("dec", "oct", "lin", "log"):
                if sweep_kind in parameters:
                    parameters.setdefault("sweeptype", sweep_kind)
                    parameters.setdefault("points", parameters.pop(sweep_kind))
            output = parameters.get("output")
            if isinstance(output, str):
                parameters["output"] = re.sub(
                    r"(?i),\s*0\s*\)$", ")", output
                )
        if self.kind == "tran" and parameters.pop("skipdc", None) == "yes":
            parameters.setdefault("flags", "uic")
        return {
            "kind": self.kind.lower(),
            "arguments": arguments,
            "parameters": parameters,
            "alterations": {
                key.lower(): _number(value)
                for key, value in sorted(self.alterations.items())
            },
        }


@dataclass
class Directive:
    kind: str
    arguments: List[str]


@dataclass
class CircuitAST:
    title: str = "Translated benchmark circuit"
    source_dialect: Dialect = Dialect.NGSPICE
    elements: List[Element] = field(default_factory=list)
    analyses: List[Analysis] = field(default_factory=list)
    directives: List[Directive] = field(default_factory=list)
    temperatures: List[str] = field(default_factory=list)
    default_temperature: Optional[str] = None
    comments: List[str] = field(default_factory=list)

    def semantic_data(self) -> Dict[str, object]:
        """Canonical physical meaning; output formatting is intentionally absent."""
        analyses: List[Dict[str, object]] = []
        source_defaults: Dict[str, Dict[str, Union[float, str]]] = {}
        for element in self.elements:
            if element.kind not in {"vsource", "isource"}:
                continue
            fields: Dict[str, Union[float, str]] = {"dc": 0.0, "ac": 0.0}
            for index, token in enumerate(element.source[:-1]):
                if token.lower() in {"dc", "ac"}:
                    fields[token.lower()] = _number(element.source[index + 1])
            source_defaults[element.name.lower()] = fields
        for analysis in self.analyses:
            temperatures: List[Optional[str]]
            if analysis.temperature_values:
                temperatures = list(analysis.temperature_values)
            else:
                temperatures = [analysis.temperature]
            for temperature in temperatures:
                item = analysis.semantic()
                normalized_alterations = dict(item["alterations"])
                for key, value in list(normalized_alterations.items()):
                    field_match = re.match(r"@([^[]+)\[([^]]+)\]", key)
                    if field_match:
                        device = field_match.group(1).lower()
                        field_name = (
                            "ac"
                            if field_match.group(2).lower() in {"ac", "acmag", "mag"}
                            else field_match.group(2).lower()
                        )
                    else:
                        device, field_name = key.lower(), "dc"
                    if (
                        device in source_defaults
                        and source_defaults[device].get(field_name) == value
                    ):
                        normalized_alterations.pop(key)
                item["alterations"] = normalized_alterations
                item["temperature"] = (
                    _number(
                        temperature
                        if temperature is not None
                        else self.default_temperature
                    )
                    if temperature is not None or self.default_temperature is not None
                    else None
                )
                analyses.append(item)
        return {
            "elements": [item.semantic() for item in self.elements],
            "analyses": analyses,
        }

    def semantic_fingerprint(self) -> str:
        payload = json.dumps(
            self.semantic_data(), sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


def detect_dialect(text: str, path: Optional[Union[str, Path]] = None) -> Dialect:
    lower = text.lower()
    suffix = Path(path).suffix.lower() if path else ""
    if (
        "simulator lang=spectre" in lower
        or re.search(r"(?m)^\s*\w+\s*\([^)]*\)\s+(?:mos|vsource|isource)\b", lower)
        or suffix == ".scs"
    ):
        return Dialect.SPECTRE
    if (
        suffix in {".sp", ".hsp", ".hspice"}
        or re.search(r"(?im)^\s*\.alter\b|^\s*\.option\s+post\b", text)
    ):
        return Dialect.HSPICE
    return Dialect.NGSPICE


def _logical_lines(text: str) -> List[str]:
    lines: List[str] = []
    current = ""
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped:
            if current:
                lines.append(current)
                current = ""
            continue
        if stripped.startswith("+"):
            current += " " + stripped[1:].strip()
        elif current.endswith("\\"):
            current = current[:-1].rstrip() + " " + stripped
        else:
            if current:
                lines.append(current)
            current = stripped
    if current:
        lines.append(current)
    return lines


def _scalar_expression(expression: str, variables: Dict[str, float]) -> Optional[float]:
    expression = expression.strip()
    if not re.fullmatch(r"[\w\s.+*/()<>-]+", expression):
        return None
    try:
        value = eval(  # noqa: S307 - grammar and globals are deliberately restricted
            expression,
            {"__builtins__": {}, "floor": math.floor},
            dict(variables),
        )
    except (NameError, SyntaxError, TypeError, ValueError, ZeroDivisionError):
        return None
    return float(value) if isinstance(value, (int, float)) else None


def _parse_alter_command(
    command: List[str],
) -> Optional[Tuple[str, str]]:
    """Return the target/value pair for all accepted ngspice alter spellings.

    ngspice accepts both whitespace-separated forms (``alter V1 = 1``) and
    compact source-parameter forms (``alter @V1[acmag]=1``).  Treating the
    latter as a two-token presentation command silently dropped the physical
    excitation from translated HSPICE/Spectre decks.
    """
    if not command or command[0].lower() != "alter":
        return None
    remainder = " ".join(command[1:]).strip()
    match = re.fullmatch(r"(\S+?)\s*=\s*(\S+)", remainder)
    if match:
        return match.group(1), match.group(2)
    if len(command) >= 3:
        return command[1], command[2]
    return None


def _expand_control_program(lines: List[str]) -> List[str]:
    """Statically expand ngspice scalar ``while`` and ``foreach`` programs."""
    variables: Dict[str, float] = {}

    def matching_end(items: List[str], start: int) -> int:
        depth = 1
        for index in range(start + 1, len(items)):
            command = _tokens(items[index])
            head = command[0].lower() if command else ""
            if head in {"while", "foreach"}:
                depth += 1
            elif head == "end":
                depth -= 1
                if depth == 0:
                    return index
        raise CircuitSyntaxError("unterminated ngspice control loop")

    def substitute(line: str) -> str:
        for name, value in variables.items():
            rendered = _value_text(value)
            line = re.sub(r"\$" + re.escape(name) + r"\b", rendered, line)
        command = _tokens(line)
        parsed_alter = _parse_alter_command(command)
        if parsed_alter:
            target, value = parsed_alter
            if value in variables:
                line = "alter %s = %s" % (
                    target, _value_text(variables[value])
                )
        return line

    def expand(items: List[str]) -> List[str]:
        output: List[str] = []
        index = 0
        while index < len(items):
            line = items[index].split(";", 1)[0].rstrip()
            command = _tokens(line)
            head = command[0].lower() if command else ""
            if head == "let" and "=" in command:
                equals = command.index("=")
                if equals == 2 and "[" not in command[1]:
                    value = _scalar_expression(
                        " ".join(command[equals + 1 :]), variables
                    )
                    if value is not None:
                        variables[command[1]] = value
                index += 1
                continue
            if head in {"while", "foreach"}:
                end = matching_end(items, index)
                body = items[index + 1 : end]
                if head == "foreach" and len(command) >= 3:
                    name = command[1]
                    for raw_value in command[2:]:
                        value = _number(raw_value)
                        if isinstance(value, float):
                            variables[name] = value
                            output.extend(expand(body))
                elif head == "while":
                    condition = " ".join(command[1:])
                    iterations = 0
                    while _scalar_expression(condition, variables):
                        output.extend(expand(body))
                        iterations += 1
                        if iterations > 10000:
                            raise CircuitSyntaxError(
                                "ngspice control loop exceeds 10000 iterations"
                            )
                index = end + 1
                continue
            if head == "end":
                index += 1
                continue
            output.append(substitute(line))
            index += 1
        return output

    return expand(lines)


def _expand_control_sections(lines: List[str]) -> List[str]:
    output: List[str] = []
    index = 0
    while index < len(lines):
        if lines[index].lower() != ".control":
            output.append(lines[index])
            index += 1
            continue
        end = index + 1
        while end < len(lines) and lines[end].lower() != ".endc":
            end += 1
        if end == len(lines):
            raise CircuitSyntaxError("unterminated .control section")
        output.append(lines[index])
        output.extend(_expand_control_program(lines[index + 1 : end]))
        output.append(lines[end])
        index = end + 1
    return output


def _parse_spice_element(line: str) -> Optional[Element]:
    tokens = _tokens(line)
    if not tokens:
        return None
    name = tokens[0]
    kind = name[0].upper()
    if kind == "M" and len(tokens) >= 6:
        positional, parameters = _params(tokens[6:])
        if positional:
            parameters["_extra"] = " ".join(positional)
        return Element(name, "mos", tokens[1:5], model=tokens[5], parameters=parameters)
    if kind in {"R", "C", "L"} and len(tokens) >= 4:
        _, parameters = _params(tokens[4:])
        return Element(
            name,
            {"R": "resistor", "C": "capacitor", "L": "inductor"}[kind],
            tokens[1:3],
            value=tokens[3],
            parameters=parameters,
        )
    if kind in {"V", "I"} and len(tokens) >= 3:
        source = tokens[3:]
        joined = " ".join(source)
        waveform = re.search(r"(?i)\b(pulse|sin|pwl)\s*\(([^)]*)\)", joined)
        if waveform:
            prefix = source[:]
            for index, token in enumerate(prefix):
                if waveform.group(1).lower() in token.lower():
                    prefix = prefix[:index]
                    break
            values = _tokens(waveform.group(2))
            keys = {
                "pulse": ["val0", "val1", "delay", "rise", "fall", "width", "period"],
                "sin": ["offset", "amplitude", "frequency", "delay", "damping"],
                "pwl": [],
            }[waveform.group(1).lower()]
            source = prefix + ["type", waveform.group(1).lower()]
            if keys:
                for key, value in zip(keys, values):
                    source.extend([key, value])
            else:
                source.extend(values)
        return Element(
            name,
            "vsource" if kind == "V" else "isource",
            tokens[1:3],
            source=source,
        )
    if kind == "D" and len(tokens) >= 4:
        _, parameters = _params(tokens[4:])
        return Element(name, "diode", tokens[1:3], model=tokens[3], parameters=parameters)
    if kind == "Q" and len(tokens) >= 5:
        _, parameters = _params(tokens[5:])
        return Element(name, "bjt", tokens[1:4], model=tokens[4], parameters=parameters)
    if kind == "X" and len(tokens) >= 3:
        split = len(tokens) - 1
        while split > 1 and "=" in tokens[split]:
            split -= 1
        _, parameters = _params(tokens[split + 1 :])
        return Element(name, "subckt", tokens[1:split], model=tokens[split], parameters=parameters)
    return None


def _parse_spectre_element(line: str) -> Optional[Element]:
    match = re.match(r"(\S+)\s*\(([^)]*)\)\s*(\S+)(?:\s+(.*))?$", line)
    if not match:
        return None
    name, node_text, primitive, tail = match.groups()
    nodes = node_text.split()
    positional, parameters = _params(_tokens(tail or ""))
    primitive_lower = primitive.lower()
    if primitive_lower in {"vsource", "isource"}:
        source = []
        for key in (
            "dc", "ac", "mag", "type", "val0", "val1", "delay", "rise", "fall",
            "width", "period", "offset", "amplitude", "frequency", "damping",
        ):
            if key in parameters:
                source.extend([
                    "ac" if key == "mag" else key,
                    parameters.pop(key),
                ])
        if "wave" in parameters:
            source.extend(_tokens(parameters.pop("wave").strip("[]")))
        source.extend(positional)
        return Element(name, primitive_lower, nodes, parameters=parameters, source=source)
    if primitive_lower in {"resistor", "capacitor", "inductor"}:
        value_key = {"resistor": "r", "capacitor": "c", "inductor": "l"}[
            primitive_lower
        ]
        value = parameters.pop(value_key, positional[0] if positional else None)
        return Element(name, primitive_lower, nodes, value=value, parameters=parameters)
    # Spectre MOS instances use the model name in the primitive position.
    if len(nodes) == 4:
        return Element(name, "mos", nodes, model=primitive, parameters=parameters)
    return Element(name, "subckt", nodes, model=primitive, parameters=parameters)


_ANALYSIS_KINDS = {"dc", "ac", "tran", "transient", "noise", "op"}


def _parse_analysis(line: str, dialect: Dialect) -> Optional[Analysis]:
    stripped = line.strip()
    if dialect != Dialect.SPECTRE:
        stripped = stripped.lstrip(".")
        tokens = _tokens(stripped)
        if tokens and tokens[0].lower() in _ANALYSIS_KINDS:
            kind = "tran" if tokens[0].lower() == "transient" else tokens[0].lower()
            if kind == "dc" and dialect == Dialect.HSPICE:
                tokens = [
                    token for token in tokens
                    if token.lower() != "sweep"
                ]
            positional, parameters = _params(tokens[1:])
            return Analysis(kind, positional, parameters=parameters)
        return None

    tokens = _tokens(stripped.rstrip("{").strip())
    if (
        len(tokens) >= 3
        and tokens[1].startswith("(")
        and tokens[2].lower() == "noise"
    ):
        positional, parameters = _params(tokens[3:])
        output_nodes = tokens[1].strip("()").split()
        if output_nodes:
            parameters.setdefault("oProbe", "v(%s)" % ",".join(output_nodes))
        return Analysis("noise", positional, name=tokens[0], parameters=parameters)
    if len(tokens) >= 2 and tokens[1].lower() in _ANALYSIS_KINDS:
        kind = "tran" if tokens[1].lower() == "transient" else tokens[1].lower()
        if (
            kind == "dc"
            and (
                tokens[0].lower().startswith("benchmark_op_")
                or re.fullmatch(r"op\d+", tokens[0].lower())
            )
        ):
            kind = "op"
        positional, parameters = _params(tokens[2:])
        return Analysis(kind, positional, name=tokens[0], parameters=parameters)
    return None


def parse_circuit(
    source: Union[str, Path],
    dialect: Optional[Union[str, Dialect]] = None,
    analysis_hint: Optional[str] = None,
) -> CircuitAST:
    """Parse a circuit path or string into the simulator-neutral representation."""
    if isinstance(source, Path):
        path: Optional[Path] = source
        text = source.read_text(errors="replace")
    elif "\n" not in source and Path(source).exists():
        path = Path(source)
        text = path.read_text(errors="replace")
    else:
        path = None
        text = str(source)
    selected = Dialect(dialect) if dialect else detect_dialect(text, path)
    current_language = selected
    ast = CircuitAST(source_dialect=selected)
    in_control = False
    active_temperature: Optional[str] = None
    active_temperature_values: List[str] = []
    active_alterations: Dict[str, str] = {}
    in_hspice_alter = False
    hspice_ac_template: Optional[Analysis] = None
    hspice_case_name: Optional[str] = None
    hspice_case_frequency: Optional[str] = None
    hspice_case_analyses: List[Analysis] = []
    sweep_stack: List[Dict[str, str]] = []
    saw_content = False

    def finish_hspice_case() -> None:
        nonlocal hspice_case_name
        nonlocal hspice_case_frequency
        nonlocal hspice_case_analyses
        if hspice_case_name is None:
            return
        if hspice_case_analyses:
            ast.analyses.extend(hspice_case_analyses)
        elif hspice_ac_template is not None:
            if hspice_case_frequency is None:
                raise CircuitSyntaxError(
                    f"{hspice_case_name} has no AST_AC_FREQUENCY"
                )
            arguments = [
                hspice_case_frequency
                if str(value).lower() == "ast_ac_frequency"
                else value
                for value in hspice_ac_template.arguments
            ]
            parameters = {
                key: (
                    hspice_case_frequency
                    if str(value).lower() == "ast_ac_frequency"
                    else value
                )
                for key, value in hspice_ac_template.parameters.items()
            }
            ast.analyses.append(
                Analysis(
                    kind=hspice_ac_template.kind,
                    arguments=arguments,
                    name=hspice_case_name,
                    parameters=parameters,
                    temperature=active_temperature,
                    temperature_values=list(active_temperature_values),
                    alterations=dict(active_alterations),
                )
            )
        hspice_case_name = None
        hspice_case_frequency = None
        hspice_case_analyses = []

    for line in _expand_control_sections(_logical_lines(text)):
        if ";" in line:
            line = line.split(";", 1)[0].rstrip()
            if not line:
                continue
        lower = line.lower()
        if line.startswith("*") or line.startswith("//"):
            ast.comments.append(line.lstrip("*/ "))
            continue
        if not saw_content and not line.startswith(".") and selected != Dialect.SPECTRE:
            ast.title = line
            saw_content = True
            continue
        saw_content = True
        if lower == ".control":
            in_control = True
            continue
        if lower.startswith(".alter"):
            case_match = re.match(
                r"(?i)^\.alter\s+(ast_case_\d+)\s*$",
                line,
            )
            if case_match:
                candidates = [
                    item
                    for item in ast.analyses
                    if item.kind == "ac"
                    and any(
                        str(value).lower() == "ast_ac_frequency"
                        for value in (
                            list(item.arguments)
                            + list(item.parameters.values())
                        )
                    )
                ]
                if hspice_ac_template is not None or candidates:
                    finish_hspice_case()
                    if hspice_ac_template is None:
                        if len(candidates) != 1:
                            raise CircuitSyntaxError(
                                "parameterized HSPICE AC deck has no unique "
                                "AST_AC_FREQUENCY template"
                            )
                        hspice_ac_template = candidates[0]
                        ast.analyses.remove(hspice_ac_template)
                    hspice_case_name = case_match.group(1)
                    hspice_case_frequency = None
                    hspice_case_analyses = []
                    active_temperature = None
                    active_temperature_values = []
            in_hspice_alter = True
            active_alterations = {}
            continue
        if lower == ".endc":
            in_control = False
            continue
        if lower == "simulator lang=spice":
            current_language = Dialect.NGSPICE
            continue
        if lower == "simulator lang=spectre":
            current_language = Dialect.SPECTRE
            continue
        if lower in {".end", "}"}:
            if lower == ".end":
                finish_hspice_case()
            if lower == "}":
                if sweep_stack:
                    sweep_stack.pop()
            continue
        if lower.startswith(("simulatoroptions ", "global ")):
            if lower.startswith("simulatoroptions "):
                match = re.search(r"(?i)\btemp\s*=\s*(\S+)", line)
                if match:
                    ast.default_temperature = match.group(1)
            continue
        if lower.startswith((".temp ", "temp ")):
            values = _tokens(line)[1:]
            for value in values:
                if value not in ast.temperatures:
                    ast.temperatures.append(value)
            active_temperature = values[0] if len(values) == 1 else None
            active_temperature_values = values
            continue
        if in_control and lower.startswith("option temp"):
            match = re.search(r"=\s*(\S+)", line)
            if match:
                active_temperature = match.group(1)
                active_temperature_values = [active_temperature]
                if active_temperature not in ast.temperatures:
                    ast.temperatures.append(active_temperature)
            continue
        if current_language == Dialect.SPECTRE:
            sweep_match = re.match(r"\S+\s+sweep\s+(.*?)(?:\s*\{)?$", line, re.I)
            if sweep_match:
                _, sweep = _params(_tokens(sweep_match.group(1)))
                sweep_stack.append(sweep)
                if sweep.get("param", "").lower() == "temp" and "values" in sweep:
                    values = _tokens(sweep["values"].strip("[]"))
                    for value in values:
                        if value not in ast.temperatures:
                            ast.temperatures.append(value)
                continue
        analysis = _parse_analysis(
            line, current_language if not in_control else Dialect.NGSPICE
        )
        if analysis:
            if (
                selected == Dialect.HSPICE
                and analysis.kind == "noise"
                and len(analysis.arguments) == 3
                and ast.analyses
                and ast.analyses[-1].kind == "ac"
            ):
                ac_analysis = ast.analyses.pop()
                analysis.arguments = (
                    analysis.arguments[:2] + ac_analysis.arguments
                )
            if analysis.kind == "dc":
                dc_sweeps = [
                    sweep for sweep in sweep_stack
                    if sweep.get("param", "").lower() == "dc"
                ]
                if dc_sweeps:
                    outer = dc_sweeps[-1]
                    if "dev" in outer:
                        analysis.parameters["dev2"] = outer["dev"]
                    for key in ("start", "stop", "step", "values"):
                        if key in outer:
                            analysis.parameters[key + "2"] = outer[key]
            if "temp" in analysis.parameters:
                analysis.temperature = analysis.parameters.pop("temp")
                analysis.temperature_values = [analysis.temperature]
                if analysis.temperature not in ast.temperatures:
                    ast.temperatures.append(analysis.temperature)
            else:
                analysis.temperature = active_temperature
                analysis.temperature_values = list(active_temperature_values)
            for sweep in sweep_stack:
                if sweep.get("param", "").lower() == "temp" and "values" in sweep:
                    analysis.temperature_values = _tokens(
                        sweep["values"].strip("[]")
                    )
                    analysis.temperature = (
                        analysis.temperature_values[0]
                        if len(analysis.temperature_values) == 1
                        else None
                    )
            analysis.alterations = dict(active_alterations)
            for sweep in sweep_stack:
                sweep_param = sweep.get("param", "").lower()
                if sweep_param != "temp" and "dev" in sweep and "values" in sweep:
                    values = _tokens(sweep["values"].strip("[]"))
                    if len(values) == 1:
                        key = (
                            "@%s[acmag]" % sweep["dev"]
                            if sweep_param in {"mag", "ac", "acmag"}
                            else sweep["dev"]
                        )
                        analysis.alterations[key] = values[0]
            if hspice_case_name is not None:
                hspice_case_analyses.append(analysis)
            else:
                ast.analyses.append(analysis)
            continue
        if line.startswith("."):
            tokens = _tokens(line)
            kind = tokens[0].lstrip(".").lower()
            if kind == "param" and hspice_case_name is not None:
                frequency_match = re.search(
                    r"(?i)\bAST_AC_FREQUENCY\s*=\s*(\S+)",
                    line,
                )
                if frequency_match:
                    hspice_case_frequency = frequency_match.group(1)
            if kind in {
                "inc", "include", "lib", "option", "options", "param",
                "save", "print", "probe", "measure", "meas", "ic", "nodeset",
            }:
                ast.directives.append(Directive(kind, tokens[1:]))
                if kind in {"option", "options"}:
                    match = re.search(r"(?i)\btemp\s*=\s*(\S+)", line)
                    if match:
                        ast.default_temperature = match.group(1)
            # Output/control statements have no effect on the physical fingerprint.
            continue
        if in_control:
            # Commands such as write/plot/let only select presentation.  Alter is
            # retained as a directive so emitters never silently execute it as a
            # device statement.
            command = _tokens(line)
            if command:
                parsed_alter = _parse_alter_command(command)
                if parsed_alter:
                    target, value = parsed_alter
                    active_alterations[target] = value
                ast.directives.append(Directive("control_" + command[0].lower(), command[1:]))
            continue
        element = (
            _parse_spectre_element(line)
            if current_language == Dialect.SPECTRE
            else _parse_spice_element(line)
        )
        if element:
            if in_hspice_alter:
                existing = next(
                    (
                        item for item in ast.elements
                        if item.name.lower() == element.name.lower()
                    ),
                    None,
                )
                if existing and element.kind in {"vsource", "isource"}:
                    def source_fields(item: Element) -> Dict[str, str]:
                        fields: Dict[str, str] = {}
                        for source_index, token in enumerate(item.source[:-1]):
                            if token.lower() in {"dc", "ac"}:
                                fields[token.lower()] = item.source[source_index + 1]
                        return fields

                    old_fields = source_fields(existing)
                    new_fields = source_fields(element)
                    if new_fields.get("dc") != old_fields.get("dc"):
                        if "dc" in new_fields:
                            active_alterations[element.name] = new_fields["dc"]
                    if new_fields.get("ac") != old_fields.get("ac"):
                        if "ac" in new_fields:
                            active_alterations[
                                "@%s[acmag]" % element.name
                            ] = new_fields["ac"]
                    continue
            ast.elements.append(element)

    finish_hspice_case()
    if not ast.elements:
        raise CircuitSyntaxError("circuit contains no supported physical elements")
    if analysis_hint:
        expected = "tran" if analysis_hint == "transient" else analysis_hint
        if not any(item.kind == expected for item in ast.analyses):
            raise CircuitSyntaxError(
                "circuit does not contain the requested %s analysis" % analysis_hint
            )
    if not ast.analyses:
        raise CircuitSyntaxError("circuit contains no supported analysis")
    return ast


def _spice_source(element: Element) -> str:
    if not element.source:
        return ""
    source = list(element.source)
    pairs: Dict[str, str] = {}
    positional: List[str] = []
    index = 0
    known = {
        "dc", "ac", "type", "val0", "val1", "delay", "rise", "fall",
        "width", "period", "offset", "amplitude", "frequency", "damping",
    }
    while index < len(source):
        key = source[index].lower()
        if key in known and index + 1 < len(source):
            pairs[key] = source[index + 1]
            index += 2
        else:
            positional.append(source[index])
            index += 1
    rendered: List[str] = []
    for key in ("dc", "ac"):
        if key in pairs:
            rendered.extend([key.upper(), pairs[key]])
    waveform = pairs.get("type")
    if waveform in {"pulse", "sin"}:
        keys = (
            ["val0", "val1", "delay", "rise", "fall", "width", "period"]
            if waveform == "pulse"
            else ["offset", "amplitude", "frequency", "delay", "damping"]
        )
        values = [pairs[key] for key in keys if key in pairs]
        rendered.append("%s(%s)" % (waveform.upper(), " ".join(values)))
    elif waveform == "pwl":
        rendered.append("PWL(%s)" % " ".join(positional))
        positional = []
    elif waveform:
        rendered.append(waveform.upper())
    rendered.extend(positional)
    return " ".join(rendered)


def _emit_spice_element(element: Element) -> str:
    params = " ".join(
        "%s=%s" % (key, value)
        for key, value in element.parameters.items()
        if not key.startswith("_")
    )
    if element.kind == "mos":
        body = "%s %s %s" % (
            element.name, " ".join(element.nodes), element.model
        )
    elif element.kind in {"resistor", "capacitor", "inductor"}:
        prefix = {"resistor": "R", "capacitor": "C", "inductor": "L"}[element.kind]
        name = element.name if element.name[0].upper() == prefix else prefix + element.name
        body = "%s %s %s" % (name, " ".join(element.nodes), element.value)
    elif element.kind in {"vsource", "isource"}:
        prefix = "V" if element.kind == "vsource" else "I"
        name = element.name if element.name[0].upper() == prefix else prefix + element.name
        body = "%s %s %s" % (name, " ".join(element.nodes), _spice_source(element))
    else:
        body = "%s %s %s" % (
            element.name, " ".join(element.nodes), element.model or ""
        )
    return " ".join(piece for piece in (body, params) if piece).strip()


def _emit_spice_analysis(
    analysis: Analysis, dialect: Dialect = Dialect.NGSPICE
) -> str:
    semantic = analysis.semantic()
    params = semantic["parameters"]
    args = list(semantic["arguments"])
    if analysis.kind == "dc":
        args = [
            params["source"], params["start"], params["stop"], params["step"]
        ]
        if "source2" in params:
            args.extend([
                params["source2"], params["start2"], params["stop2"],
                params["step2"],
            ])
    elif analysis.kind == "ac":
        args = [
            params.get("sweeptype", "dec"), params["points"],
            params["start"], params["stop"],
        ]
    elif analysis.kind == "tran":
        args = [params.get("step", params["stop"] / 1000.0), params["stop"]]
        if params.get("start", 0.0) != 0.0:
            args.append(params["start"])
        if params.get("flags") == "uic":
            args.append("uic")
    elif analysis.kind == "noise":
        if dialect == Dialect.HSPICE:
            ac_line = ".AC %s %s %s %s" % (
                params.get("sweeptype", "dec"),
                _value_text(params["points"]),
                _value_text(params["start"]),
                _value_text(params["stop"]),
            )
            noise_line = ".NOISE %s %s 1" % (
                params["output"], params["input"]
            )
            return ac_line + "\n" + noise_line
        args = [
            params["output"], params["input"], params.get("sweeptype", "dec"),
            params["points"], params["start"], params["stop"],
        ]
    return ".%s%s" % (
        analysis.kind,
        (" " + " ".join(_value_text(item) for item in args)) if args else "",
    )


def _source_with_dc(element: Element, value: str) -> Element:
    source = list(element.source)
    for index, token in enumerate(source[:-1]):
        if token.lower() == "dc":
            source[index + 1] = value
            break
    else:
        source = ["dc", value] + source
    return Element(
        element.name,
        element.kind,
        list(element.nodes),
        value=element.value,
        model=element.model,
        parameters=dict(element.parameters),
        source=source,
    )


def _emit_hspice_alterations(
    ast: CircuitAST, alterations: Dict[str, str]
) -> List[str]:
    changed: Dict[str, Element] = {}
    for target, value in alterations.items():
        source_name = re.sub(r"^@|\[.*\]$", "", target)
        element = next(
            (
                item for item in ast.elements
                if item.name.lower() == source_name.lower()
                and item.kind in {"vsource", "isource"}
            ),
            None,
        )
        if element is not None:
            modified = changed.get(element.name.lower(), element)
            field_match = re.search(r"\[([^]]+)\]$", target)
            field_name = field_match.group(1).lower() if field_match else "dc"
            source = list(modified.source)
            source_key = "ac" if field_name in {"ac", "acmag", "mag"} else "dc"
            for index, token in enumerate(source[:-1]):
                if token.lower() == source_key:
                    source[index + 1] = value
                    break
            else:
                source.extend([source_key, value])
            changed[element.name.lower()] = Element(
                modified.name,
                modified.kind,
                list(modified.nodes),
                value=modified.value,
                model=modified.model,
                parameters=dict(modified.parameters),
                source=source,
            )
    return [_emit_spice_element(item) for item in changed.values()]


def _baseline_alteration(ast: CircuitAST, target: str) -> str:
    source_name = re.sub(r"^@|\[.*\]$", "", target)
    element = next(
        (
            item for item in ast.elements
            if item.name.lower() == source_name.lower()
            and item.kind in {"vsource", "isource"}
        ),
        None,
    )
    if element is None:
        return "0"
    field_match = re.search(r"\[([^]]+)\]$", target)
    field_name = field_match.group(1).lower() if field_match else "dc"
    source_key = "ac" if field_name in {"ac", "acmag", "mag"} else "dc"
    for index, token in enumerate(element.source[:-1]):
        if token.lower() == source_key:
            return element.source[index + 1]
    return "0"


def _spectre_source(element: Element) -> str:
    tokens = element.source
    if not tokens:
        return ""
    rendered: List[str] = []
    index = 0
    known = {
        "dc", "ac", "type", "val0", "val1", "delay", "rise", "fall",
        "width", "period", "offset", "amplitude", "frequency", "damping",
    }
    while index < len(tokens):
        key = tokens[index].lower()
        if key in known and index + 1 < len(tokens):
            rendered.append(
                "%s=%s"
                % ("mag" if key == "ac" else key, tokens[index + 1])
            )
            index += 2
        elif index == 0 and _number(tokens[index]) != tokens[index].lower():
            rendered.append("dc=%s" % tokens[index])
            index += 1
        else:
            rendered.append(tokens[index])
            index += 1
    if "type=pwl" in rendered:
        keywords = tuple(item + "=" for item in known)
        waveform_values = [
            item for item in rendered
            if not item.lower().startswith(keywords)
        ]
        rendered = [
            item for item in rendered
            if item.lower().startswith(keywords)
        ]
        if waveform_values:
            rendered.append("wave=[%s]" % " ".join(waveform_values))
    return " ".join(rendered)


def _emit_spectre_element(element: Element) -> str:
    params = dict(element.parameters)
    if element.kind == "mos":
        primitive = element.model or "mos"
    elif element.kind in {"vsource", "isource"}:
        primitive = element.kind
    elif element.kind in {"resistor", "capacitor", "inductor"}:
        primitive = element.kind
        key = {"resistor": "r", "capacitor": "c", "inductor": "l"}[element.kind]
        if element.value is not None:
            params[key] = element.value
    else:
        primitive = element.model or element.kind
    tail = " ".join(
        "%s=%s" % (key.lower(), value)
        for key, value in params.items()
        if not key.startswith("_")
    )
    if element.kind in {"vsource", "isource"}:
        tail = " ".join(piece for piece in (_spectre_source(element), tail) if piece)
    return "%s (%s) %s%s" % (
        element.name.lower(),
        " ".join(node.lower() for node in element.nodes),
        primitive,
        (" " + tail) if tail else "",
    )


def _emit_spectre_analysis(analysis: Analysis, index: int) -> str:
    semantic = analysis.semantic()
    params = {
        key: _value_text(value)
        for key, value in semantic["parameters"].items()
    }
    emitted_kind = "dc" if analysis.kind == "op" else analysis.kind
    if analysis.kind == "dc":
        params["dev"] = params.pop("source")
        if "source2" in params:
            params["dev2"] = params.pop("source2")
    elif analysis.kind == "ac":
        sweep_type = params.pop("sweeptype", "dec")
        points = params.pop("points")
        if params.get("start") == params.get("stop"):
            frequency = params.pop("start")
            params.pop("stop")
            params["values"] = f"[{frequency}]"
        else:
            params[sweep_type] = points
    elif analysis.kind == "tran":
        params.update(
            {
                "errpreset": "conservative",
                "method": "gear2only",
                "maxiters": "50",
                "minstep": "1e-18",
                "cmin": "1e-18",
            }
        )
    elif analysis.kind == "noise":
        output = params.pop("output")
        input_probe = params.pop("input").lower()
        sweep_type = params.pop("sweeptype", "dec")
        points = params.pop("points")
        params["iprobe"] = input_probe
        params[sweep_type] = points
        match = re.match(r"(?i)v\(([^,()]+)(?:,([^()]+))?\)", output)
        if match:
            output_terminals = "(%s %s)" % (
                match.group(1).lower(),
                (match.group(2) or "0").lower(),
            )
        else:
            params["oprobe"] = output.lower()
            output_terminals = ""
    elif analysis.kind == "tran" and "step" in params:
        params["maxstep"] = params.pop("step")
    if analysis.kind == "tran" and str(params.pop("flags", "")).lower() == "uic":
        params.setdefault("skipdc", "yes")
    if analysis.kind == "dc" and "dev2" in params:
        outer = {
            "dev": params.pop("dev2"),
            "start": params.pop("start2"),
            "stop": params.pop("stop2"),
            "step": params.pop("step2"),
        }
        inner = " ".join("%s=%s" % item for item in params.items())
        outer_text = " ".join("%s=%s" % item for item in outer.items())
        base_name = analysis.name or "x%d" % index
        return (
            "%s_outer sweep param=dc %s {\n"
            "  %s dc %s\n}"
        ) % (base_name, outer_text, base_name, inner)
    tail = " ".join(
        "%s=%s" % item if item[0] != "_args" else item[1]
        for item in params.items()
    )
    if analysis.kind == "noise" and output_terminals:
        return "%s %s noise%s" % (
            analysis.name or "x%d" % index,
            output_terminals,
            (" " + tail) if tail else "",
        )
    default_name = (
        "op%d" % index if analysis.kind == "op" else "x%d" % index
    )
    return "%s %s%s" % (
        analysis.name or default_name,
        emitted_kind,
        (" " + tail) if tail else "",
    )


def emit_circuit(ast: CircuitAST, dialect: Union[str, Dialect]) -> str:
    target = Dialect(dialect)
    lines = ["* " + ast.title, "* semantic-sha256: " + ast.semantic_fingerprint()]
    if target == Dialect.SPECTRE:
        lines.extend([
            "simulator lang=spectre",
            "global 0",
            # Permit difficult compact models to spend more iterations near
            # Spectre's minimum transient step before declaring failure.
            # This changes only the numerical solver policy, not the circuit.
            "benchmarkNumerics options max_approach_minstep=10000 "
            "max_minstep_nonconv=10000",
        ])
        if ast.default_temperature is not None:
            lines.append(
                "simulatorOptions options temp=%s" % ast.default_temperature
            )
        for directive in ast.directives:
            if directive.kind in {"inc", "include"}:
                include_path = " ".join(directive.arguments).strip("'\"")
                lines.extend([
                    "simulator lang=spice",
                    ".include '%s'" % include_path,
                    "simulator lang=spectre",
                ])
            elif directive.kind in {"option", "options"}:
                normalized_options: List[str] = []
                for argument in directive.arguments:
                    key, separator, value = argument.partition("=")
                    lower_key = key.lower()
                    if lower_key in {"chgtol", "tempscale"}:
                        continue
                    if lower_key == "abstol":
                        normalized_options.append("iabstol=" + value)
                    elif lower_key == "method" and value.lower() == "gear":
                        normalized_options.append("method=gear2only")
                    elif lower_key == "gmin":
                        normalized_options.append("gmin=1e-12")
                    elif lower_key == "reltol":
                        normalized_options.append("reltol=1e-3")
                    else:
                        normalized_options.append(argument)
                if normalized_options:
                    lines.append(
                        "simulatorOptions options "
                        + " ".join(normalized_options)
                    )
            elif directive.kind in {"param"}:
                lines.append("parameters " + " ".join(directive.arguments))
        lines.extend(_emit_spectre_element(item) for item in ast.elements)
        for index, analysis in enumerate(ast.analyses):
            emitted = _emit_spectre_analysis(analysis, index)
            for alter_index, (device, value) in enumerate(
                reversed(list(analysis.alterations.items()))
            ):
                field_match = re.match(r"@([^[]+)\[([^]]+)\]", device)
                if field_match:
                    alter_device = field_match.group(1).lower()
                    alter_param = (
                        "mag"
                        if field_match.group(2).lower() == "acmag"
                        else field_match.group(2).lower()
                    )
                else:
                    alter_device = device.lower()
                    alter_param = "dc"
                emitted = (
                    "a%d_%d sweep param=%s dev=%s values=[%s] {\n"
                    "  %s\n}"
                ) % (
                    index, alter_index, alter_param, alter_device, value, emitted
                )
            temperatures = analysis.temperature_values or (
                [analysis.temperature] if analysis.temperature is not None else []
            )
            if temperatures:
                values = " ".join(temperatures)
                lines.append(
                    "t%d sweep param=temp values=[%s] {\n"
                    "  %s\n}" % (index, values, emitted)
                )
            else:
                lines.append(emitted)
        lines.append("")
        return "\n".join(lines)

    lines.append(".TITLE " + ast.title)
    for directive in ast.directives:
        if directive.kind in {
            "inc", "include", "lib", "option", "options", "param",
            "ic", "nodeset",
        }:
            kind = "option" if directive.kind == "options" else directive.kind
            arguments = list(directive.arguments)
            if kind == "option" and target == Dialect.HSPICE:
                arguments = [
                    item for item in arguments
                    if not re.match(r"(?i)^temp\s*=", item)
                ]
            if arguments:
                lines.append(".%s %s" % (kind, " ".join(arguments)))
    lines.extend(_emit_spice_element(item) for item in ast.elements)
    if target == Dialect.NGSPICE:
        lines.append(".CONTROL")
        all_alterations = sorted({
            device
            for analysis in ast.analyses
            for device in analysis.alterations
        })
        for analysis in ast.analyses:
            temperatures = (
                analysis.temperature_values
                or (
                    [analysis.temperature]
                    if analysis.temperature is not None
                    else [ast.default_temperature]
                )
            )
            for temperature in temperatures:
                if temperature is not None:
                    lines.append("option temp = %s" % temperature)
                for device in all_alterations:
                    value = analysis.alterations.get(
                        device, _baseline_alteration(ast, device)
                    )
                    lines.append("alter %s = %s" % (device, value))
                lines.append(
                    _emit_spice_analysis(
                        analysis, Dialect.NGSPICE
                    ).lstrip(".")
                )
        lines.append(".ENDC")
    else:
        for index, analysis in enumerate(ast.analyses):
            lines.append(".ALTER AST_CASE_%d" % index)
            lines.extend(
                _emit_hspice_alterations(ast, analysis.alterations)
            )
            temperatures = analysis.temperature_values or (
                [analysis.temperature]
                if analysis.temperature is not None
                else (
                    [ast.default_temperature]
                    if ast.default_temperature is not None
                    else []
                )
            )
            if temperatures:
                lines.append(".TEMP " + " ".join(temperatures))
            lines.append(_emit_spice_analysis(analysis, Dialect.HSPICE))
    lines.append(".END")
    lines.append("")
    return "\n".join(lines)


_PRIMARY_BIAS_SOURCES = {
    "vds_iv", "vgs_iv", "vds_bias", "vgs_bias",
    "vg", "vd", "vgs", "vds", "vgq", "vdq",
    "vgs_tran", "vds_tran", "vg_charge", "vd_charge",
    "vgs_qs", "vds_qs", "vgs_noise", "vds_noise",
    "vdd_noise", "vin_noise", "vbias_f", "vgs_flicker",
    "vdd_shot", "vgs_shot",
}


def _negative_magnitude(token: str) -> str:
    """Return a numeric token with negative polarity, preserving zero."""
    match = re.fullmatch(
        r"\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)"
        r"([a-zA-Z]*)\s*",
        token,
    )
    if not match:
        return token
    value = float(match.group(1))
    if value == 0.0:
        return token
    return f"{-abs(value):g}{match.group(2)}"


def _opposite_polarity(token: str) -> str:
    """Mirror a signed numeric token around zero, preserving its suffix."""
    match = re.fullmatch(
        r"\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)"
        r"([a-zA-Z]*)\s*",
        token,
    )
    if not match:
        return token
    value = float(match.group(1))
    if value == 0.0:
        return token
    return f"{-value:g}{match.group(2)}"


def _model_has_pmos_primary(model_file: Union[str, Path]) -> bool:
    text = Path(model_file).read_text(errors="replace")
    cards = [
        (match.group(1), match.group(2).lower())
        for match in re.finditer(
            r"(?i)\.model\s+(\S+)\s+(nmos|pmos)\b",
            text,
        )
        if not match.group(1).lower().startswith("__fixture_")
    ]
    return bool(cards) and not any(kind == "nmos" for _, kind in cards) and any(
        kind == "pmos" for _, kind in cards
    )


def _adapt_primary_polarity(
    ast: CircuitAST,
    model_file: Optional[Union[str, Path]],
) -> None:
    """Apply PMOS single-device biasing once at the shared AST boundary."""
    if model_file is None or not _model_has_pmos_primary(model_file):
        return

    for element in ast.elements:
        if (
            element.kind not in {"vsource", "isource"}
            or element.name.lower() not in _PRIMARY_BIAS_SOURCES
        ):
            continue
        source = list(element.source)
        waveform = None
        positional_start = len(source)
        index = 0
        while index < len(source):
            key = source[index].lower()
            if key == "type" and index + 1 < len(source):
                waveform = source[index + 1].lower()
                index += 2
                continue
            if key in {
                "dc", "ac", "val0", "val1", "delay", "rise", "fall",
                "width", "period", "offset", "amplitude", "frequency",
                "damping",
            } and index + 1 < len(source):
                if key in {"dc", "val0", "val1", "offset", "amplitude"}:
                    source[index + 1] = _opposite_polarity(source[index + 1])
                index += 2
                continue
            positional_start = min(positional_start, index)
            index += 1
        if waveform == "pwl" and positional_start < len(source):
            for value_index in range(positional_start + 1, len(source), 2):
                source[value_index] = _opposite_polarity(source[value_index])
        element.source = source

    for analysis in ast.analyses:
        if analysis.kind == "dc":
            arguments = list(analysis.arguments)
            index = 0
            while index + 3 < len(arguments):
                source_name = arguments[index].lower()
                if source_name in _PRIMARY_BIAS_SOURCES:
                    for value_index in range(index + 1, index + 4):
                        arguments[value_index] = _opposite_polarity(
                            arguments[value_index]
                        )
                index += 4
            analysis.arguments = arguments
        for target, value in list(analysis.alterations.items()):
            source_name = re.sub(r"^@|\[.*\]$", "", target).lower()
            field = re.search(r"\[([^]]+)\]$", target)
            if (
                source_name in _PRIMARY_BIAS_SOURCES
                and not field
            ):
                analysis.alterations[target] = _opposite_polarity(value)


def translate_circuit(
    source: Union[str, Path],
    target: Union[str, Dialect],
    output: Optional[Union[str, Path]] = None,
    source_dialect: Optional[Union[str, Dialect]] = None,
    analysis_hint: Optional[str] = None,
    model_file: Optional[Union[str, Path]] = None,
) -> Tuple[CircuitAST, str]:
    ast = parse_circuit(source, source_dialect, analysis_hint)
    target_dialect = Dialect(target)
    # Native ngspice decks retain their control/wrdata program and are
    # polarity-normalized by the ngspice runner while being copied.  The
    # cross-dialect emitters must normalize the AST here so HSPICE and
    # Spectre receive the same physical PMOS bias.
    if not (
        ast.source_dialect == Dialect.NGSPICE
        and target_dialect == Dialect.NGSPICE
    ):
        _adapt_primary_polarity(ast, model_file)
    source_path: Optional[Path] = None
    if isinstance(source, Path):
        source_path = source
    elif "\n" not in str(source) and Path(str(source)).is_file():
        source_path = Path(str(source))
    if model_file is not None:
        model_argument = "'%s'" % Path(model_file).resolve()
        include = next(
            (
                item for item in ast.directives
                if item.kind in {"inc", "include", "lib"}
            ),
            None,
        )
        if include is None:
            ast.directives.insert(0, Directive("inc", [model_argument]))
        else:
            include.kind = "inc"
            include.arguments = [model_argument]
    # Keeping a deck in its native language preserves simulator-specific
    # result commands (wrdata/.print/save) while the AST still verifies its
    # physical meaning. Cross-dialect paths always use the normalized emitter.
    if source_path is not None and ast.source_dialect == target_dialect:
        rendered = source_path.read_text(errors="replace")
        if model_file is not None:
            absolute_model = str(Path(model_file).resolve())
            if target_dialect == Dialect.SPECTRE:
                replacement = (
                    "simulator lang=spice\n"
                    ".include '%s'\n"
                    "simulator lang=spectre"
                ) % absolute_model
                rendered, count = re.subn(
                    r"(?im)^\s*(?:\.(?:inc|include|lib)|include)\s+.*$",
                    replacement,
                    rendered,
                    count=1,
                )
            else:
                rendered, count = re.subn(
                    r"(?im)^\s*\.(?:inc|include|lib)\s+.*$",
                    ".include '%s'" % absolute_model,
                    rendered,
                    count=1,
                )
            if count == 0:
                rendered = ".include '%s'\n%s" % (
                    absolute_model,
                    rendered,
                )
    else:
        rendered = emit_circuit(ast, target_dialect)
    if output is not None:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered)
    return ast, rendered


def translate_circuit_set(
    circuits: Dict[str, Union[str, Path]],
    output_dir: Union[str, Path],
    targets: Iterable[Union[str, Dialect]] = tuple(Dialect),
    model_file: Optional[Union[str, Path]] = None,
) -> Dict[str, Dict[str, str]]:
    """Translate DC/AC/transient/noise inputs for all requested simulators."""
    root = Path(output_dir)
    result: Dict[str, Dict[str, str]] = {}
    target_fingerprints: Dict[str, Dict[str, str]] = {}
    source_asts = {
        mode: parse_circuit(source, analysis_hint=mode)
        for mode, source in circuits.items()
    }
    extension = {
        Dialect.NGSPICE: ".cir",
        Dialect.HSPICE: ".sp",
        Dialect.SPECTRE: ".scs",
    }
    for target_value in targets:
        target = Dialect(target_value)
        result[target.value] = {}
        target_fingerprints[target.value] = {}
        for mode, source in circuits.items():
            path = root / target.value / (mode + extension[target])
            original, rendered = translate_circuit(
                source,
                target,
                output=path,
                analysis_hint=mode,
                model_file=model_file,
            )
            reparsed = parse_circuit(rendered, target, analysis_hint=mode)
            original_fingerprint = original.semantic_fingerprint()
            target_fingerprint = reparsed.semantic_fingerprint()
            if original_fingerprint != target_fingerprint:
                raise CircuitSyntaxError(
                    "%s -> %s changed physical semantics (%s != %s)"
                    % (
                        mode,
                        target.value,
                        original_fingerprint,
                        target_fingerprint,
                    )
                )
            result[target.value][mode] = str(path)
            target_fingerprints[target.value][mode] = target_fingerprint
    manifest = {
        "schema": 1,
        "circuits": result,
        "semantic_fingerprints": {
            mode: ast.semantic_fingerprint()
            for mode, ast in source_asts.items()
        },
        "target_fingerprints": target_fingerprints,
        "equivalent": True,
    }
    root.mkdir(parents=True, exist_ok=True)
    (root / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    return result
