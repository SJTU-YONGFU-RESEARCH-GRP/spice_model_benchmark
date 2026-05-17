"""
Shared utilities for bridge modules.

Auto-discovers sibling projects (new-spice-translator, spice_model_benchmark,
spice_model_reduction) and provides safe importlib-based module loading.
"""

import sys
from pathlib import Path
from typing import Optional


# Project discovery markers: (canonical_name, marker_relative_path)
_PROJECT_MARKERS = [
    ("new-spice-translator", "src/main.py"),
    ("spice_model_benchmark", "src/spice_model_benchmark/__init__.py"),
    ("spice_model_reduction", "bmr/__init__.py"),
]


def _find_siblings() -> list[Path]:
    """Return list of known sibling project root directories."""
    here = Path(__file__).resolve()
    # Walk up from bridge/ to project root, then to parent
    own_root = here.parent.parent
    parent = own_root.parent
    siblings = []
    for name, _ in _PROJECT_MARKERS:
        candidate = parent / name
        if candidate.is_dir():
            siblings.append(candidate)
    return siblings


def find_project(name: str) -> Optional[Path]:
    """Locate a sibling project by its canonical directory name.

    Search order:
      1. Parent directory of the current project (../<name>)
      2. Explicit environment variable <NAME>_PATH
      3. Walk known sibling directories
    """
    import os

    env_key = name.upper().replace("-", "_") + "_PATH"
    env_path = os.environ.get(env_key)
    if env_path:
        p = Path(env_path)
        if p.is_dir():
            return p

    here = Path(__file__).resolve()
    own_root = here.parent.parent
    parent = own_root.parent
    candidate = parent / name
    if candidate.is_dir():
        return candidate

    # Walk siblings from current project root
    for sib in _find_siblings():
        if sib.name == name:
            return sib

    return None


def import_module(project_name: str, module_path: str):
    """Safely import a module from a sibling project.

    For projects with uniquely-named packages (``bmr``, ``spice_model_benchmark``)
    this simply adds the right paths and imports.  For projects that collide on
    the ``src/`` namespace (``new-spice-translator``) it temporarily isolates
    sys.path and sys.modules to avoid conflicts.

    Args:
        project_name: Canonical directory name (e.g. "new-spice-translator")
        module_path: Dot-separated import path (e.g. "src.main", "bmr.core.config")

    Returns:
        The imported module, or None if the project cannot be found.
    """
    import importlib

    root = find_project(project_name)
    if root is None:
        return None

    _PATH_CONFIG = {
        "new-spice-translator": [str(root)],
        "spice_model_benchmark": [str(root / "src")],
        "spice_model_reduction": [str(root)],
    }

    top_name = module_path.split(".")[0]

    # Only the translator's ``src/`` namespace conflicts with the benchmark's
    # ``src/`` (which has an __init__.py and takes ownership).  Projects with
    # unique package names (bmr, spice_model_benchmark) don't need isolation.
    needs_isolation = (project_name == "new-spice-translator")

    saved_modules = {}
    saved_path = list(sys.path)

    if needs_isolation:
        # Evict any cached ``src`` (and sub-modules) belonging to the importer
        for key in list(sys.modules):
            if key == top_name or key.startswith(top_name + "."):
                saved_modules[key] = sys.modules.pop(key)

        # Remove sys.path entries that own ``src/`` via an __init__.py from a
        # different project (e.g. the benchmark's)
        own_top = root / top_name
        clean_path = []
        for p in saved_path:
            candidate = Path(p) / top_name
            if candidate.is_dir() and (candidate / "__init__.py").exists():
                if candidate.resolve() != own_top.resolve():
                    continue
            clean_path.append(p)
        sys.path[:] = clean_path

    # Ensure needed paths are first
    for p in reversed(_PATH_CONFIG.get(project_name, [str(root)])):
        if p in sys.path:
            sys.path.remove(p)
        sys.path.insert(0, p)

    try:
        return importlib.import_module(module_path)
    except ImportError:
        return None
    finally:
        if needs_isolation:
            sys.path[:] = saved_path
            for key in list(sys.modules):
                if key == top_name or key.startswith(top_name + "."):
                    if key not in saved_modules:
                        del sys.modules[key]
            for key, mod in saved_modules.items():
                sys.modules[key] = mod
