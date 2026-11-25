"""Unit tests for Verilog-A Compact Model Linter & OpenVAF Compiler."""

import pytest
from pathlib import Path
from spice_model_benchmark.veriloga_linter_and_compiler import (
    VerilogALinter,
    OpenVAFCompiler,
    LintRuleResult,
    VerilogALintReport
)


def test_veriloga_linter_gold_model(tmp_path):
    va_code = """
`include "disciplines.vams"
`include "constants.vams"

module nmos_pinn(d, g, s, b);
  inout d, g, s, b;
  electrical d, g, s, b;

  parameter real W = 1.0e-6;
  parameter real L = 0.045e-6;

  analog begin
    real Vds, Vgs, Vbs, Vt, Ids, Qg, Qd;
    Vds = V(d, s);
    Vgs = V(g, s);
    Vbs = V(b, s);

    Vt = $temperature * `P_K / `P_Q;

    // Smooth tanh activation with odd Gummel symmetry
    Ids = Vds * (1.0e-3 * tanh(Vgs / Vt));
    Qg = 1.0e-15 * Vgs;
    Qd = 0.5e-15 * Vds;

    I(d, s) <+ Ids;
    I(g, s) <+ ddt(Qg);
    I(d, s) <+ ddt(Qd);

    // Intrinsic noise
    I(d, s) <+ white_noise(4.0 * `P_K * $temperature * 1e-3, "thermal");
    I(d, s) <+ flicker_noise(1e-24 * pow(abs(Ids), 1.0) / (W * L), 1.0, "flicker");
  end
endmodule
"""
    test_va = tmp_path / "nmos_test.va"
    test_va.write_text(va_code, encoding="utf-8")

    linter = VerilogALinter()
    report = linter.lint_file(test_va)

    assert report.total_score >= 85.0
    assert report.grade in ("A+", "A")
    assert report.openvaf_compatible is True

    rule_map = {r.rule_id: r.status for r in report.results}
    assert rule_map["RULE_TEMP_DYNAMIC"] == "PASS"
    assert rule_map["RULE_INTRINSIC_NOISE"] == "PASS"
    assert rule_map["RULE_ZERO_BIAS_PASSIVITY"] == "PASS"
    assert rule_map["RULE_CHARGE_CONSERVATION"] == "PASS"


def test_veriloga_linter_spectre_dialect_warning(tmp_path):
    va_code = """
module nmos_spectre(d, g, s, b);
  inout d, g, s, b;
  electrical d, g, s, b;

  (* instance_parameter_list = {L, W} *)

  real MEL = 9.11e-31;
  real mx = 0.916 * MEL;

  analog begin
    temp = 300.0;
    I(d, s) <+ 1e-3 * V(d, s);
  end
endmodule
"""
    test_va = tmp_path / "spectre_dialect.va"
    test_va.write_text(va_code, encoding="utf-8")

    linter = VerilogALinter()
    report = linter.lint_file(test_va)

    rule_map = {r.rule_id: r.status for r in report.results}
    assert rule_map["RULE_DIALECT_COMPATIBILITY"] == "WARN"
    assert rule_map["RULE_INTRINSIC_NOISE"] == "FAIL"
    assert report.openvaf_compatible is False


def test_openvaf_compiler_availability():
    compiler = OpenVAFCompiler()
    assert compiler.is_available() is True
