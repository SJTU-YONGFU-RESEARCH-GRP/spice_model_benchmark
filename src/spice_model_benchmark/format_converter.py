"""
Format converter for SPICE model files.

Provides automatic format detection and conversion from hspice/spectre
to ngspice format using the new-spice-translator project's TranslationEngine.
"""

import os
import re
import sys
import shutil
import logging
from pathlib import Path
from typing import Optional, Tuple, List

logger = logging.getLogger(__name__)


class FormatConverter:
    """Converts SPICE model files from hspice/spectre to ngspice format."""

    EXTENSION_MAP = {
        '.scs': 'spectre',
        '.sp': 'hspice',
        '.spice': 'hspice',
        '.lib': 'hspice',
        '.inc': 'ngspice',
        '.cir': 'ngspice',
        '.model': 'ngspice',
    }

    SPECTRE_KEYWORDS = ['simulator lang', 'section ', 'endsection', 'statistics',
                        'inline ', 'subckt ', 'ends ', 'model ', 'parameters ']

    HSPICE_KEYWORDS = ['.lib ', '.alter', '.protect', '.unprotect',
                       'llevel=', 'level =', '$ ']

    # Patterns that strongly indicate hspice format
    HSPICE_INCLUDE_PATTERN = re.compile(r'^\s*\.include\s+\'', re.MULTILINE)

    def __init__(self, translator_path: Optional[str] = None):
        """
        Initialize FormatConverter.

        Args:
            translator_path: Path to new-spice-translator project root.
                             If None, auto-detected from known locations.
        """
        self.translator_path = self._resolve_translator_path(translator_path)
        self._engine = None

    def _resolve_translator_path(self, translator_path: Optional[str]) -> Optional[Path]:
        """Find the translator project root.

        Search order:
          1. Explicit --translator-path argument
          2. SPICE_TRANSLATOR_PATH environment variable
          3. pip-installed spice-translator-ir package
          4. Sibling directory ../new-spice-translator
        """
        # 1. Explicit argument
        if translator_path:
            p = Path(translator_path)
            if (p / 'src' / 'main.py').exists():
                return p
            raise FileNotFoundError(f"Translator not found at: {translator_path}")

        # 2. Environment variable
        env_path = os.environ.get('SPICE_TRANSLATOR_PATH')
        if env_path:
            p = Path(env_path)
            if (p / 'src' / 'main.py').exists():
                return p
            logger.warning(f"SPICE_TRANSLATOR_PATH={env_path} does not contain src/main.py, ignoring")

        # 3. pip-installed package
        try:
            import importlib.util
            spec = importlib.util.find_spec('src.main')
            if spec and spec.origin:
                # Found a pip-installed src.main — derive project root
                root = Path(spec.origin).resolve().parents[1]  # src/main.py -> project root
                if (root / 'src' / 'main.py').exists():
                    return root
        except (ModuleNotFoundError, ValueError):
            pass

        # 4. Sibling directory
        candidates = [
            Path.cwd().parent / 'new-spice-translator',
            Path(__file__).resolve().parents[4] / 'new-spice-translator',
        ]
        for c in candidates:
            if (c / 'src' / 'main.py').exists():
                return c
        return None

    def _get_engine(self):
        """Lazily import and instantiate TranslationEngine."""
        if self._engine is not None:
            return self._engine

        if self.translator_path is None:
            raise RuntimeError(
                "Translator not found. Set it up via one of:\n"
                "  1. --translator-path /path/to/new-spice-translator\n"
                "  2. export SPICE_TRANSLATOR_PATH=/path/to/new-spice-translator\n"
                "  3. pip install spice-translator-ir\n"
                "  4. Place new-spice-translator as a sibling directory"
            )

        root_dir = str(self.translator_path)
        if root_dir not in sys.path:
            sys.path.insert(0, root_dir)

        # Our package's src/ (registered via .pth) shadows the
        # translator's src/ directory.  Replace 'src' in sys.modules
        # with a synthetic package pointing at the translator's src/.
        import importlib, types

        saved_src = {}
        src_keys = [k for k in list(sys.modules) if k == 'src' or k.startswith('src.')]
        for k in src_keys:
            saved_src[k] = sys.modules.pop(k)

        # Create a synthetic 'src' package for the translator
        src_pkg = types.ModuleType('src')
        src_pkg.__path__ = [str(self.translator_path / 'src')]
        src_pkg.__package__ = 'src'
        sys.modules['src'] = src_pkg

        try:
            src_main = importlib.import_module('src.main')
            TranslationEngine = src_main.TranslationEngine
        finally:
            # Restore original 'src' module(s)
            for k in src_keys:
                if k in sys.modules:
                    del sys.modules[k]
            for k, v in saved_src.items():
                sys.modules[k] = v
        self._engine = TranslationEngine()
        return self._engine

    def detect_format(self, file_path: Path) -> str:
        """
        Detect SPICE format from file extension and content.

        Returns:
            'spectre', 'hspice', or 'ngspice'
        """
        file_path = Path(file_path)
        ext = file_path.suffix.lower()

        # Extension-based detection
        if ext in ('.scs',):
            return 'spectre'
        if ext in ('.sp', '.spice'):
            return 'hspice'
        if ext in ('.inc', '.cir', '.model'):
            return 'ngspice'

        # .lib is ambiguous (both hspice and ngspice use it)
        if ext == '.lib':
            return self._detect_format_from_content(file_path)

        # Fallback: content-based
        return self._detect_format_from_content(file_path)

    def _detect_format_from_content(self, file_path: Path) -> str:
        """Detect format by reading file content."""
        try:
            text = file_path.read_text(errors='ignore')[:4096]
        except Exception:
            return 'ngspice'

        lower = text.lower()
        spectre_score = sum(1 for kw in self.SPECTRE_KEYWORDS if kw in lower)
        hspice_score = sum(1 for kw in self.HSPICE_KEYWORDS if kw in lower)
        ngspice_score = sum(1 for kw in ['.subckt ', '.ends'] if kw in lower)

        # HSPICE uses .include with single quotes; ngspice uses .inc or .include without quotes
        if self.HSPICE_INCLUDE_PATTERN.search(text):
            hspice_score += 2

        # Both hspice and ngspice use .model — use it as tiebreaker only
        has_model = '.model ' in lower
        if has_model:
            if hspice_score > 0:
                hspice_score += 1
            else:
                ngspice_score += 1

        if spectre_score > max(hspice_score, ngspice_score):
            return 'spectre'
        if hspice_score > ngspice_score:
            return 'hspice'
        return 'ngspice'

    def convert_to_ngspice(
        self,
        input_file: Path,
        source_format: Optional[str] = None,
        output_dir: Optional[Path] = None,
    ) -> Path:
        """
        Convert a SPICE model file to ngspice format.

        Args:
            input_file: Source model file path
            source_format: 'spectre', 'hspice', or None (auto-detect)
            output_dir: Directory for output file (default: temp dir)

        Returns:
            Path to converted ngspice model file

        Raises:
            RuntimeError: If conversion fails
        """
        input_file = Path(input_file)

        if source_format is None:
            source_format = self.detect_format(input_file)

        if source_format == 'ngspice':
            logger.info(f"File is already ngspice format: {input_file}")
            return input_file

        if output_dir is None:
            output_dir = input_file.parent / '_converted'
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"{input_file.stem}_ngspice.lib"

        engine = self._get_engine()
        result = engine.translate(
            input_file=input_file,
            source_format=source_format,
            target_format='ngspice',
            output_file=output_file,
            validate=False,
            use_organized_output=False,
            follow_includes=True,
        )

        if not result.get('success'):
            raise RuntimeError(
                f"Translation failed at {result.get('stage', 'unknown')}: "
                f"{result.get('error', 'Unknown error')}"
            )

        logger.info(
            f"Converted {source_format} -> ngspice: {input_file} -> {output_file} "
            f"({result.get('models_translated', '?')} models)"
        )
        return output_file

    def extract_model_names(self, model_file: Path) -> List[str]:
        """Extract .model names from a ngspice model file."""
        names = []
        pattern = re.compile(r'\.model\s+(\S+)\s+(nmos|pmos)', re.IGNORECASE)
        try:
            text = model_file.read_text(errors='ignore')
            for m in pattern.finditer(text):
                names.append(m.group(1))
        except Exception:
            pass
        return names

    def generate_adapted_circuits(
        self,
        original_circuit_dir: Path,
        converted_model_path: Path,
        model_names: List[str],
        output_dir: Path,
        source_format: str,
    ) -> dict:
        """
        Generate adapted circuit files that reference the converted model.

        Replaces `.inc` paths and model names in circuit files to match the
        converted ngspice model.

        Args:
            original_circuit_dir: Directory containing original .cir files
            converted_model_path: Path to the converted ngspice model file
            model_names: List of model names in the converted file
            output_dir: Directory for adapted circuit files
            source_format: Original source format

        Returns:
            Dict mapping circuit type to adapted circuit file path
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Find a suitable NMOS and PMOS model name from the converted file
        nmos_name = None
        pmos_name = None
        for name in model_names:
            lower = name.lower()
            if nmos_name is None and 'nmos' in lower:
                nmos_name = name
            if pmos_name is None and 'pmos' in lower:
                pmos_name = name
            if nmos_name and pmos_name:
                break

        # Fallback: use first and second model names
        if nmos_name is None and model_names:
            nmos_name = model_names[0]
        if pmos_name is None and len(model_names) > 1:
            pmos_name = model_names[1]

        # Compute relative path from circuit dir to model file
        try:
            rel_model_path = os.path.relpath(converted_model_path, output_dir)
        except ValueError:
            rel_model_path = str(converted_model_path)

        circuit_map = {}
        circuit_files = {
            'dc': 'dc_circuit.cir',
            'transient': 'transient_circuit.cir',
            'ac': 'ac_circuit.cir',
            'noise': 'noise_circuit.cir',
        }

        for mode, filename in circuit_files.items():
            src = original_circuit_dir / filename
            if not src.exists():
                continue

            adapted = self._adapt_circuit_file(
                src, output_dir / filename, rel_model_path,
                nmos_name, pmos_name,
            )
            circuit_map[mode] = str(adapted)

        return circuit_map

    def _adapt_circuit_file(
        self,
        src: Path,
        dst: Path,
        model_include_path: str,
        nmos_name: Optional[str],
        pmos_name: Optional[str],
    ) -> Path:
        """
        Adapt a circuit file: replace include paths and model names.
        """
        text = src.read_text(errors='ignore')

        # Remove all .inc/.include lines that reference model files
        text = re.sub(
            r'^[ \t]*\.(inc|include)\s+.*$',
            f'.inc {model_include_path}',
            text,
            flags=re.MULTILINE,
        )

        # Only keep the first .inc line if multiple were collapsed
        first_inc = True
        lines = text.split('\n')
        new_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('.inc ') and not first_inc:
                continue
            if stripped.startswith('.inc '):
                first_inc = False

            # Replace model names in MOSFET instance lines (Mxxx ...)
            if re.match(r'^m\w+\b', stripped, re.IGNORECASE):
                if nmos_name:
                    line = re.sub(r'\bNMOS_VTG\b', nmos_name, line)
                    line = re.sub(r'\bNMOS_VTL\b', nmos_name, line)
                    line = re.sub(r'\bNMOS_VTH\b', nmos_name, line)
                    line = re.sub(r'\bNMOS_THKOX\b', nmos_name, line)
                if pmos_name:
                    line = re.sub(r'\bPMOS_VTG\b', pmos_name, line)
                    line = re.sub(r'\bPMOS_VTL\b', pmos_name, line)
                    line = re.sub(r'\bPMOS_VTH\b', pmos_name, line)
                    line = re.sub(r'\bPMOS_THKOX\b', pmos_name, line)

            new_lines.append(line)

        dst.write_text('\n'.join(new_lines))
        return dst