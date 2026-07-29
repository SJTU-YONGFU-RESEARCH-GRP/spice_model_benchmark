import logging
import tempfile
import unittest
from pathlib import Path

from spice_model_benchmark.spectre_post_processor import (
    SpectrePostProcessor,
)


class _Logger:
    logger = logging.getLogger("spectre-post-processor-test")


class SpectrePostProcessorTest(unittest.TestCase):
    def test_scalar_operating_point_psf_is_measured_data(self):
        psf = """HEADER
"analysis type" "dc"
TYPE
"V" FLOAT DOUBLE
"I" FLOAT DOUBLE
VALUE
"drain_bias" "V" -6.000000000000000e-01
"gate_bias" "V" -1.200000000000000e+00
"vds_bias:p" "I" 9.849545655700000e-04
"vgs_bias:p" "I" 0.000000000000000e+00
"vs_bias:p" "I" -9.849545649700000e-04
"vb_bias:p" "I" -6.000000000000000e-13
END
"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "op.dc"
            path.write_text(psf)
            processor = SpectrePostProcessor(_Logger(), root)
            parsed = processor._parse_psf_dc_groups(path)
            self.assertEqual(parsed["n_steps"], 1)
            self.assertEqual(parsed["values"]["drain_bias"].tolist(), [-0.6])
            self.assertEqual(parsed["values"]["gate_bias"].tolist(), [-1.2])
            self.assertEqual(
                parsed["values"]["vds_bias:p"].tolist(),
                [9.8495456557e-4],
            )

    def test_bias_output_preserves_psf_source_current_direction(self):
        psf = """HEADER
"analysis type" "dc"
TYPE
"V" FLOAT DOUBLE
"I" FLOAT DOUBLE
VALUE
"drain_bias" "V" 6.000000000000000e-01
"gate_bias" "V" 1.200000000000000e+00
"Vds_bias:p" "I" -9.849545655700000e-04
"Vgs_bias:p" "I" 0.000000000000000e+00
"Vs_bias:p" "I" 9.849545649700000e-04
"Vb_bias:p" "I" 6.000000000000000e-13
END
"""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            raw = root / "raw"
            raw.mkdir()
            (raw / "benchmark_op.dc").write_text(psf)
            processor = SpectrePostProcessor(_Logger(), root)

            processor._process_dc_bias(raw)

            values = [
                float(item)
                for item in (root / "bias_point_data.txt")
                .read_text()
                .splitlines()[1]
                .split()
            ]
            self.assertEqual(values[2], -9.8495456557e-4)
            self.assertEqual(values[4], 9.8495456497e-4)


if __name__ == "__main__":
    unittest.main()
