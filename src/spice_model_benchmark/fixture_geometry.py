"""Model-declared geometry handling for the stock benchmark fixture.

This module only adapts device instance geometry in benchmark netlists.  It
never changes, replaces, or lowers a supplied model card.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional


def read_geometry_override(
    model_file: str | Path,
) -> Optional[tuple[str, str]]:
    """Return ``(length, width)`` when the handoff declares an override."""
    content = Path(model_file).read_text(errors="replace")
    match = re.search(
        r"(?im)^\s*\*\s*BENCHMARK_DUT_GEOMETRY_OVERRIDE:\s*"
        r"L=(\S+)\s+W=(\S+)\s*$",
        content,
    )
    return (match.group(1), match.group(2)) if match else None


def apply_primary_geometry(
    content: str,
    primary_model: str,
    geometry: Optional[tuple[str, str]],
) -> str:
    """Apply declared W/L to every instance of the exact primary model."""
    if geometry is None:
        return content
    length, width = geometry

    def update_tail(tail: str) -> str:
        values = {"l": length, "w": width}
        for name, value in values.items():
            pattern = rf"(?i)(\b{name}\s*=\s*)[^\s]+"
            tail, count = re.subn(pattern, rf"\g<1>{value}", tail)
            if count == 0:
                tail += f" {name}={value}"
        return tail

    spice = re.compile(
        r"(?im)^(\s*M\S+\s+(?:\S+\s+){4})(\S+)([^\n]*)$"
    )
    spectre = re.compile(
        r"(?im)^(\s*M\S+\s*\([^)]*\)\s+)(\S+)([^\n]*)$"
    )

    def replace(match: re.Match[str]) -> str:
        if match.group(2).lower() != primary_model.lower():
            return match.group(0)
        return match.group(1) + match.group(2) + update_tail(match.group(3))

    content = spice.sub(replace, content)
    return spectre.sub(replace, content)
