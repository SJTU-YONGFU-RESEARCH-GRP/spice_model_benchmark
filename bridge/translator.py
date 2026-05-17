"""
Benchmark → Translator bridge.

After benchmarking an ngspice model, translate it to other SPICE formats
(hspice, spectre) so the validated model can be used in other simulators.
"""

import argparse
from pathlib import Path


def run(context: dict, args: list[str]) -> dict:
    """B→T: translate a benchmarked ngspice model to other formats.

    context keys:
        model_file:   Path to the original ngspice model file
        output_dir:   Directory where benchmark results were written

    args (from --bridge "translate --targets hspice,spectre"):
        --targets   Comma-separated target formats (default: hspice)
    """
    parser = argparse.ArgumentParser(prog="bridge-translate")
    parser.add_argument("--targets", type=str, default="hspice",
                        help="Comma-separated target formats: hspice,spectre")
    parsed = parser.parse_args(args)

    from ._common import import_module

    translator = import_module("new-spice-translator", "src.main")
    if translator is None:
        print("[bridge:translate] new-spice-translator not found — skipping")
        return {"ok": False, "reason": "translator not found"}

    engine = translator.TranslationEngine()
    model_file = Path(context["model_file"])
    output_dir = Path(context.get("output_dir", ".")) / "translated"
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {}
    for fmt in parsed.targets.split(","):
        fmt = fmt.strip()
        if fmt == "ngspice":
            continue
        ext = {"spectre": "scs", "hspice": "lib"}.get(fmt, "lib")
        out = output_dir / f"{model_file.stem}.{ext}"
        res = engine.translate(
            input_file=model_file,
            source_format="ngspice",
            target_format=fmt,
            output_file=out,
            validate=False,
        )
        results[fmt] = {
            "ok": res.get("success", False),
            "output": str(out) if res.get("success") else None,
            "error": res.get("error"),
        }
        status = "OK" if res.get("success") else "FAIL"
        print(f"[bridge:translate] ngspice → {fmt}: {status}")

    return {"ok": True, "results": results}
