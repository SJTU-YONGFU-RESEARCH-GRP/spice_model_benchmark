import unittest

from spice_model_benchmark.hspice_runner import (
    _parameterize_transient_analyses,
)


class HspiceTransientControlTest(unittest.TestCase):
    def test_each_alter_inherits_its_ast_transient_controls(self):
        lines = [
            ".ALTER AST_CASE_0",
            ".tran 1e-11 1e-7",
            ".ALTER AST_CASE_1",
            ".tran 1e-10 5e-7 2e-9",
            ".END",
        ]

        rendered = _parameterize_transient_analyses(lines)

        self.assertIn(
            ".TRAN AST_TRAN_STEP AST_TRAN_STOP AST_TRAN_START",
            rendered,
        )
        self.assertIn(
            ".PARAM AST_TRAN_STEP=1e-11 AST_TRAN_STOP=1e-7 "
            "AST_TRAN_START=0",
            rendered,
        )
        self.assertIn(
            ".PARAM AST_TRAN_STEP=1e-10 AST_TRAN_STOP=5e-7 "
            "AST_TRAN_START=2e-9",
            rendered,
        )
        self.assertFalse(
            any(line.lower().startswith(".tran 1e-") for line in rendered)
        )

    def test_mixed_startup_flags_fail_instead_of_changing_physics(self):
        with self.assertRaisesRegex(ValueError, "startup flags"):
            _parameterize_transient_analyses(
                [
                    ".ALTER AST_CASE_0",
                    ".tran 1n 10n",
                    ".ALTER AST_CASE_1",
                    ".tran 1n 20n uic",
                ]
            )

    def test_single_analysis_is_left_verbatim(self):
        lines = [".tran 1n 20n 5n uic", ".end"]
        self.assertEqual(_parameterize_transient_analyses(lines), lines)


if __name__ == "__main__":
    unittest.main()
