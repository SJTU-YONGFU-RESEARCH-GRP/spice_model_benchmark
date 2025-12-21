# 电容一致性分析报告

**日期**: 2025年12月18日  
**PDK**: FreePDK45  
**工具**: ngspice-45.2

## 1. 摘要

本项目旨在验证 MOS 管大信号电容（Large Signal Capacitance）与小信号电容（Small Signal Capacitance）的一致性。
通过对比三种提取方法：
1. **AC 小信号积分法**：对 AC 分析得到的 $C_{gg}(V)$ 进行积分。
2. **Transient 大信号法**：对瞬态仿真中的栅极电流 $I_g(t)$ 进行积分。
3. **DC 工作点法 (Method 5.1)**：基于 `op` 分析报告的端点电荷 `@M[qg]` 差分。

**结论**：
- **AC 法与 Transient 法高度一致**（误差 < 0.2%），均符合物理预期（包含氧化层电容与交叠电容）。
- **DC Method 5.1 存在严重偏差**（误差 ~70%），其计算出的电容远小于物理值。
- **原因分析**：ngspice BSIM4 模型在 `op` 分析中报告的 `@M[qg]` 似乎仅包含部分沟道电荷，缺失了交叠电容（Overlap Capacitance）和边缘电容（Fringing Capacitance）等关键分量，导致大信号电容计算偏小。

建议后续工作弃用基于 `op` `@M[qg]` 的 Method 5.1，改用 **Transient 法** 或 **AC 积分法** 作为大信号电容的标准提取手段。

补充：本仓库主链路的 AC 仿真（`python src/mosfet_simulation.py --mode ac`）已集成 **AC 积分法**，会在输出目录的 `data/` 下自动生成 AC 积分得到的大信号电容与电荷曲线（见第 5 节复现命令）。

---

## 2. 实验设置

- **器件**: NMOS_VTG (FreePDK45)
- **尺寸**: L=0.045um, W=10um
- **偏置**: Vd=1.2V, Vs=Vb=0V
- **扫描范围**: Vg 从 0V 到 1.2V

### 2.1 方法描述

#### 方法 A: AC 小信号积分 (AC Integration)
- 主链路网表：`netlists/ac_circuit.cir` 生成 `cv_data.txt`，由 Python 对 C(V) 积分得到大信号电容
- 原理: 
  $$ Q_{total} = \int_{0}^{1.2} C_{gg}(V) \, dV $$
  $$ C_{LS} = \frac{Q_{total}}{\Delta V} $$
- 仿真: AC 频率 1MHz，积分区间 0V ~ 1.2V。

#### 方法 B: Transient 大信号 (Transient Charge)
- 主链路网表：`netlists/transient_circuit.cir`
- 原理: 施加 Vg 脉冲 (0 -> 1.2V)，积分栅极电流：
  $$ Q_{total} = \int I_g(t) \, dt $$
  $$ C_{LS} = \frac{Q_{total}}{\Delta V} $$

#### 方法 C: DC 工作点差分 (Method 5.1)
- 说明：本仓库主链路不包含历史实验脚本；若要做 DC `op` 差分，可基于 `netlists/*_dc_circuit.cir` 自行扩展工作点扫描。
- 原理: 在 Vg=0 和 Vg=1.2 分别运行 `op`，读取 `@M[qg]`：
  $$ C_{LS} = \frac{Q_g(1.2V) - Q_g(0V)}{1.2V} $$

---

## 3. 实验结果

| 方法 | 提取电容 (fF) | 相对 Transient 误差 | 备注 |
| :--- | :---: | :---: | :--- |
| **AC Integration** | **11.24** | **0.13%** | 符合物理预期 (Cox + Overlap) |
| **Transient** | **11.25** | **-** | 基准值 (直接物理定义) |
| **DC Method 5.1** | **3.41** | **69.7%** | **严重偏小** |

### 3.1 详细数据分析

- **物理估算**:
  - $C_{ox} \approx 30 \text{ fF}/\mu m^2 \times 0.45 \mu m^2 = 13.5 \text{ fF}$
  - 考虑有效沟道长度 $L_{eff} \approx 17.5 \text{ nm}$ (由于 $xl=-20nm$)，则 $C_{ox,eff} \approx 5.4 \text{ fF}$。
  - 交叠电容 $C_{ov} = (C_{gso} + C_{gdo}) \times W = (0.11 + 0.11) \times 10 = 2.2 \text{ fF}$。
  - 预期总电容 $C_{total} \approx C_{ox,eff} + C_{ov} + C_{fringing}$。
  - AC 和 Transient 结果 (~11.25 fF) 包含了所有这些分量。

- **DC Method 5.1 问题**:
  - 提取值为 3.41 fF。
  - 即使只考虑 $C_{ox,eff}$ (5.4 fF) 也偏小。
  - 实验表明，当在模型中移除交叠电容参数 (`cgso=0`) 时，AC 电容减少约 6.5 fF，而 DC 电荷仅减少约 2.9 fC (对应 2.4 fF)。这说明 DC `op` 报告的电荷虽然包含部分交叠成分，但计算方式与 AC/Transient 存在巨大差异。

---

## 4. 结论与建议

1. **弃用 DC Method 5.1**: 目前基于 ngspice `op` `@M[qg]` 的提取方法不可靠，无法用于验证 AC 模型的一致性。
2. **采用 Transient 法**: 作为大信号电容的“真值”。该方法直接反映了电路在时域的大信号行为，且与 AC 小信号积分结果高度吻合。
3. **更新工具链**:
  - 在后续的 PDK 移植和测试中，优先使用 Transient 方法或 AC 积分法进行大信号电容提取。

## 5. 附录：复现脚本

运行以下命令可复现本报告结果：

```bash
# AC analysis (includes AC-integral large-signal capacitance outputs)
PYTHONPATH=src python -m spice_model_benchmark.mosfet_simulation --mode ac --output-dir results_ac_cmatrix

# Transient analysis (time-domain large-signal behavior)
PYTHONPATH=src python -m spice_model_benchmark.mosfet_simulation --mode transient --output-dir results_tran_smoke
```

主链路新增输出（`results_ac_cmatrix/data/`）：
- `ac_ls_caps_from_cv_integral.csv`
- `ac_qg_from_cv_integral.csv`
```
