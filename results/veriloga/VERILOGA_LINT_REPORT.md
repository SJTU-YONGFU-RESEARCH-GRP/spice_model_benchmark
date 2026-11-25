# Verilog-A Compact Model Physical Quality & Transpilation Report

Generated automatically by **SPICE Model Benchmark Framework**.
OpenVAF Engine: `/usr/local/bin/openvaf` | Hardware: `{'platform': 'Linux-5.14.0-611.26.1.el9_7.x86_64-x86_64-with-glibc2.34', 'processor': 'x86_64', 'cpu_model': 'Intel(R) Xeon(R) CPU E5-2678 v3 @ 2.50GHz', 'total_threads': '48', 'physical_cores': '24', 'sockets': '2', 'total_memory': '377Gi'}`.
Conforms to **IEEE TED 2025** (McAndrew et al.) and **IEEE TCAD 2026** (NeuralCM-QA).

---

## 1. Executive Quality Audit Summary

| Verilog-A File | Extracted Modules | Score | Quality Grade | Standard LRM | OpenVAF Binary |
|:---|:---|:---:|:---:|:---:|:---:|
| **`fusion_ic_nmos_lvt.va`** | nmos_lvt | 64.5/100 | **Grade C** | ⚠ Spectre AHDL | ⚠ Dialect Error |
| **`fusion_ic_pmos_lvt.va`** | pmos_lvt | 64.5/100 | **Grade C** | ⚠ Spectre AHDL | ⚠ Dialect Error |
| **`cap_cmomf.va`** | cap_cmomf | 60.5/100 | **Grade C** | ✓ Compatible | ✓ OSDI Ready |
| **`res_va.va`** | res_va | 73.8/100 | **Grade B** | ✓ Compatible | ✓ OSDI Ready |
| **`nfet_03v3_pinn.va`** | nfet_03v3_pinn | 96.2/100 | **Grade A+** | ✓ Compatible | ✓ OSDI Ready |

---

## 2. Detailed Per-Model Rule Diagnostics

### `fusion_ic_nmos_lvt.va` (Grade: C | Score: 64.5/100)

| Rule ID | Physical / Dialect Requirement | Status | Score | Diagnostic Finding |
|:---|:---|:---:|:---:|:---|
| `RULE_TEMP_DYNAMIC` | Dynamic Temperature Scaling | **✗ FAIL** | 30 | No dynamic temperature dependence found ($temperature or $vt omitted). Model operates only at fixed static temperature. |
| `RULE_INTRINSIC_NOISE` | Intrinsic Physical Noise | **✗ FAIL** | 20 | No intrinsic noise sources modeled (zero white_noise and zero flicker_noise). |
| `RULE_GUMMEL_SYMMETRY` | Gummel Symmetry Guarantee | **⚠ WARN** | 60 | Could not verify analytical Gummel symmetry decomposition from source AST. |
| `RULE_ZERO_BIAS_PASSIVITY` | Zero-Bias Passivity | **✓ PASS** | 100 | Ids is explicitly multiplied by Vds factor, guaranteeing Ids(Vds=0) == 0.0 A identically. |
| `RULE_CONTINUITY_SMOOTHNESS` | Mathematical Smoothness & C^2 Continuity | **✓ PASS** | 100 | Smooth differentiable formulations utilized (exp, ln). Zero discontinuous conditionals. |
| `RULE_CHARGE_CONSERVATION` | Dynamic Charge Conservation | **✓ PASS** | 100 | Dynamic transient and AC charges implemented with 2 ddt() formulations. |
| `RULE_DIALECT_COMPATIBILITY` | Verilog-A Standard Dialect (OpenVAF) | **⚠ WARN** | 50 | Contains non-standard Spectre AHDL extensions: Cadence Spectre attribute syntax '(* instance_parameter_list = { ... } *)'; module-level initialized real variables referencing other variables. Will compile on Cadence Spectre, but requires normalization for OpenVAF. |


### `fusion_ic_pmos_lvt.va` (Grade: C | Score: 64.5/100)

| Rule ID | Physical / Dialect Requirement | Status | Score | Diagnostic Finding |
|:---|:---|:---:|:---:|:---|
| `RULE_TEMP_DYNAMIC` | Dynamic Temperature Scaling | **✗ FAIL** | 30 | No dynamic temperature dependence found ($temperature or $vt omitted). Model operates only at fixed static temperature. |
| `RULE_INTRINSIC_NOISE` | Intrinsic Physical Noise | **✗ FAIL** | 20 | No intrinsic noise sources modeled (zero white_noise and zero flicker_noise). |
| `RULE_GUMMEL_SYMMETRY` | Gummel Symmetry Guarantee | **⚠ WARN** | 60 | Could not verify analytical Gummel symmetry decomposition from source AST. |
| `RULE_ZERO_BIAS_PASSIVITY` | Zero-Bias Passivity | **✓ PASS** | 100 | Ids is explicitly multiplied by Vds factor, guaranteeing Ids(Vds=0) == 0.0 A identically. |
| `RULE_CONTINUITY_SMOOTHNESS` | Mathematical Smoothness & C^2 Continuity | **✓ PASS** | 100 | Smooth differentiable formulations utilized (exp, ln). Zero discontinuous conditionals. |
| `RULE_CHARGE_CONSERVATION` | Dynamic Charge Conservation | **✓ PASS** | 100 | Dynamic transient and AC charges implemented with 2 ddt() formulations. |
| `RULE_DIALECT_COMPATIBILITY` | Verilog-A Standard Dialect (OpenVAF) | **⚠ WARN** | 50 | Contains non-standard Spectre AHDL extensions: Cadence Spectre attribute syntax '(* instance_parameter_list = { ... } *)'; module-level initialized real variables referencing other variables. Will compile on Cadence Spectre, but requires normalization for OpenVAF. |


### `cap_cmomf.va` (Grade: C | Score: 60.5/100)

| Rule ID | Physical / Dialect Requirement | Status | Score | Diagnostic Finding |
|:---|:---|:---:|:---:|:---|
| `RULE_TEMP_DYNAMIC` | Dynamic Temperature Scaling | **✗ FAIL** | 30 | No dynamic temperature dependence found ($temperature or $vt omitted). Model operates only at fixed static temperature. |
| `RULE_INTRINSIC_NOISE` | Intrinsic Physical Noise | **✗ FAIL** | 20 | No intrinsic noise sources modeled (zero white_noise and zero flicker_noise). |
| `RULE_GUMMEL_SYMMETRY` | Gummel Symmetry Guarantee | **⚠ WARN** | 60 | Could not verify analytical Gummel symmetry decomposition from source AST. |
| `RULE_ZERO_BIAS_PASSIVITY` | Zero-Bias Passivity | **⚠ WARN** | 75 | Passivity at Vds=0 is dependent on internal neural network evaluation rather than analytical multiplicative gating. |
| `RULE_CONTINUITY_SMOOTHNESS` | Mathematical Smoothness & C^2 Continuity | **✗ INFO** | 85 | Standard arithmetic expressions without detected discontinuity warnings. |
| `RULE_CHARGE_CONSERVATION` | Dynamic Charge Conservation | **⚠ WARN** | 70 | Only 1 ddt() charge contribution found. Terminal charge conservation across gate/drain/source may be incomplete. |
| `RULE_DIALECT_COMPATIBILITY` | Verilog-A Standard Dialect (OpenVAF) | **✓ PASS** | 100 | Complies strictly with standard IEEE 1800-AMS syntax. 100% compatible with OpenVAF and open-source simulators. |


### `res_va.va` (Grade: B | Score: 73.8/100)

| Rule ID | Physical / Dialect Requirement | Status | Score | Diagnostic Finding |
|:---|:---|:---:|:---:|:---|
| `RULE_TEMP_DYNAMIC` | Dynamic Temperature Scaling | **✓ PASS** | 100 | Dynamic temperature scaling fully modeled via $temperature or $vt. |
| `RULE_INTRINSIC_NOISE` | Intrinsic Physical Noise | **⚠ WARN** | 65 | Thermal white_noise implemented, but 1/f flicker_noise is absent. |
| `RULE_GUMMEL_SYMMETRY` | Gummel Symmetry Guarantee | **⚠ WARN** | 60 | Could not verify analytical Gummel symmetry decomposition from source AST. |
| `RULE_ZERO_BIAS_PASSIVITY` | Zero-Bias Passivity | **⚠ WARN** | 75 | Passivity at Vds=0 is dependent on internal neural network evaluation rather than analytical multiplicative gating. |
| `RULE_CONTINUITY_SMOOTHNESS` | Mathematical Smoothness & C^2 Continuity | **✗ INFO** | 85 | Standard arithmetic expressions without detected discontinuity warnings. |
| `RULE_CHARGE_CONSERVATION` | Dynamic Charge Conservation | **✗ FAIL** | 30 | Zero ddt() charge contributions found. Model supports only DC analysis and cannot run AC/Transient. |
| `RULE_DIALECT_COMPATIBILITY` | Verilog-A Standard Dialect (OpenVAF) | **✓ PASS** | 100 | Complies strictly with standard IEEE 1800-AMS syntax. 100% compatible with OpenVAF and open-source simulators. |


### `nfet_03v3_pinn.va` (Grade: A+ | Score: 96.2/100)

| Rule ID | Physical / Dialect Requirement | Status | Score | Diagnostic Finding |
|:---|:---|:---:|:---:|:---|
| `RULE_TEMP_DYNAMIC` | Dynamic Temperature Scaling | **✓ PASS** | 100 | Dynamic temperature scaling fully modeled via $temperature or $vt. |
| `RULE_INTRINSIC_NOISE` | Intrinsic Physical Noise | **✓ PASS** | 100 | Both thermal/shot noise (white_noise) and 1/f trap noise (flicker_noise) are implemented. |
| `RULE_GUMMEL_SYMMETRY` | Gummel Symmetry Guarantee | **✓ PASS** | 100 | Analytical Gummel symmetry verified via midpoint channel potential or odd/even function decomposition. |
| `RULE_ZERO_BIAS_PASSIVITY` | Zero-Bias Passivity | **⚠ WARN** | 75 | Passivity at Vds=0 is dependent on internal neural network evaluation rather than analytical multiplicative gating. |
| `RULE_CONTINUITY_SMOOTHNESS` | Mathematical Smoothness & C^2 Continuity | **✓ PASS** | 100 | Smooth differentiable formulations utilized (ln, pow). Zero discontinuous conditionals. |
| `RULE_CHARGE_CONSERVATION` | Dynamic Charge Conservation | **✓ PASS** | 100 | Dynamic transient and AC charges implemented with 3 ddt() formulations. |
| `RULE_DIALECT_COMPATIBILITY` | Verilog-A Standard Dialect (OpenVAF) | **✓ PASS** | 100 | Complies strictly with standard IEEE 1800-AMS syntax. 100% compatible with OpenVAF and open-source simulators. |


---

## 3. Scientific Modeling Recommendations for Neural Compact Models

1. **Dynamic Temperature Scaling**: Neural compact models must bind intrinsic thermal voltage `$vt = $temperature * `P_K / `P_Q` and temperature-dependent mobility rather than pinning model cards to static 300K.
2. **Intrinsic Noise Physics**: Commercial analog/RF signoff requires thermal white noise (`white_noise(4*k*T*gm)`) and flicker noise (`flicker_noise(Kf*Ids^Af/(W*L))`).
3. **OpenVAF Standard Compliance**: Avoid proprietary Cadence Spectre AHDL module-level initializers (`real a = b * c;`). Declare dependencies within `analog initial_step` or define explicit module parameters.

---
*Report automatically compiled at 2026-11-26 07:09:46*.
