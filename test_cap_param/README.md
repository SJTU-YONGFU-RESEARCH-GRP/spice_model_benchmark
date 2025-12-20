# MOS 大信号电容仿真与线性度分析

本目录包含用于提取 MOS 大信号电容并分析其随 L/W 变化线性度的脚本。

核心流程：

1. 使用 transient（TRAN）网表模板（按 PDK 区分）对单个 NMOS/PMOS 做 gate 电压阶跃。
2. `run_cap_param_sweep.py` 扫描一系列 (L, W)，为每个点生成 transient 网表并调用 ngspice 运行，通过积分 gate 电流得到总电荷并计算 Cgg。
3. `analyze_cap_linearity.py` 基于生成的 CSV，对 C–L、C–W 关系做线性拟合，评估线性度（R²），并画图。

---

## 目录结构概览

- `netlists/`
  - 顶层目录，放共用的 transient 模板网表与 `.spiceinit`。
  - 关键文件：
    - `freepdk45_tran_cap_template.cir`：FreePDK45 NMOS transient 电荷积分模板。
    - `freepdk45_tran_cap_template_pmos.cir`：FreePDK45 PMOS transient 电荷积分模板。
    - `sky130_tran_cap_template.cir`：Sky130 NMOS transient 电荷积分模板。
    - `sky130_tran_cap_template_pmos.cir`：Sky130 PMOS transient 电荷积分模板。

- `netlists/<pdk_lower>/`
  - 按 PDK 划分的**自动生成网表**目录（例如 `netlists/freepdk45/`、`netlists/sky130/`）。
  - `run_cap_param_sweep.py` 会在这里为每个 (L,W) 生成一个 transient 网表：
    - 命名示例：`freepdk45_tran_cap_template_L0.045u_W0.1u.cir`。

- `test_cap_param/`
  - 本目录：脚本和结果。
  - 脚本：
    - `run_cap_param_sweep.py`：扫描 L/W，调用 ngspice（TRAN），计算大信号等效 `Cgg`。
    - `analyze_cap_linearity.py`：读取 CSV，对电容随 L/W 的线性度做拟合与绘图。
  - 结果：
    - `results/<pdk_lower>/cap_vs_LW.csv`：NMOS Cgg vs L/W（列：`L_um,W_um,Cgg_fF`）。
    - `results/<pdk_lower>/cap_vs_LW_pmos.csv`：PMOS Cgg vs L/W（列：`L_um,W_um,Cgg_fF`，可选）。
    - `results/<pdk_lower>/plots/*.png`：线性度分析图。

---

## 依赖环境

- ngspice（命令行可执行 `ngspice`）。
- Python 3.x。
  - 依赖包：`numpy`、`matplotlib`。
- PDK 模型已就绪：
  - FreePDK45：`models/FreePDK45` 目录中的 BSIM4 模型（`NMOS_VTG.inc` / `PMOS_VTG.inc` 等）。
  - Sky130：`models/skywater-pdk-libs-sky130_fd_pr` 中的 BSIM4 模型及 corner/参数文件。

项目根目录 `netlists/.spiceinit` 中设置了适配 ngspice 的选项（如 `ngbehavior=hsa`），`run_cap_param_sweep.py` 会把它复制到 per-PDK 网表目录以保持一致行为。

---

## Transient 模板网表与大信号电容提取方法

当前大信号电容提取使用 transient（TRAN）方式：对 gate 施加 0→VDD（或 VDD→0）的电压阶跃，并对 gate 电流积分得到总电荷：

- $Q_{total} = \int I_g(t)\,dt$
- $C_{gg,LS} = |Q_{total}|/VDD$

该方法与 AC/TRAN 定义一致，避免使用 ngspice `op` 报告器件电荷时可能出现的缺失/不一致问题。

### FreePDK45 模板

- NMOS：`netlists/freepdk45_tran_cap_template.cir`
- PMOS：`netlists/freepdk45_tran_cap_template_pmos.cir`

- 引入模型：
  ```spice
  .inc ../models/FreePDK45/nom.inc
  ```
  其中 `NMOS_VTG` / `PMOS_VTG` 为 BSIM4 level 54 模型，`capmod=2`，使用电荷模型计算电容。

- 器件实例：
  - NMOS：单管瞬态仿真，gate 做阶跃，测 `i(Vgs)`。
  - PMOS：source/bulk 置 VDD，gate 做 VDD→0 阶跃。

- 大信号电容提取（节选）：
  - transient 运行后在控制台输出 `q_total = ...`（由 `meas tran q_total INTEG i(Vgs)` 得到）；
  - Python 侧用 `Cgg = |q_total| / VDD` 计算大信号电容。

### Sky130 模板

- NMOS：`netlists/sky130_tran_cap_template.cir`
- PMOS：`netlists/sky130_tran_cap_template_pmos.cir`

- 引入 Sky130 1.8V 器件模型：
  - `sky130_fd_pr__nfet_01v8`
  - `sky130_fd_pr__pfet_01v8`
  - 以及必要的 corner / mismatch / invariant 等参数文件。

- 器件实例：
  - 使用 `sky130_fd_pr__nfet_01v8` / `sky130_fd_pr__pfet_01v8` 子电路；
  - 通过 gate 阶跃 + `INTEG i(Vgs)` 提取 `q_total`。

- 内部 MOS 为 BSIM4 level 54（`sky130_fd_pr__nfet_01v8__model.3`），同样使用 `capmod=2` 的电荷模型。

- corner 切换通过替换 include 文件名实现（`__tt.corner.spice` → `__{corner}.corner.spice`），由 corner/temp sweep 脚本自动生成。

---

## 参数扫描脚本：`run_cap_param_sweep.py`

### 基本用法

在项目根目录（包含 `test_cap_param/` 与 `netlists/` 的目录）执行：

```bash
python test_cap_param/run_cap_param_sweep.py \
    --pdk FreePDK45
```

或针对 Sky130：

```bash
python test_cap_param/run_cap_param_sweep.py \
    --pdk Sky130 \
  --tran-netlist netlists/sky130_tran_cap_template.cir
```

主要命令行参数：

- `--pdk PDK_NAME`
  - 用于生成网表文件名、结果目录和图标题。
  - 示例：`FreePDK45`（默认）、`Sky130`。

- `--tran-netlist PATH`
  - 指定 NMOS transient 电荷积分模板网表路径。
  - 未指定时，默认使用 `netlists/freepdk45_tran_cap_template.cir`（Sky130 则默认 `netlists/sky130_tran_cap_template.cir`）。

- `--tran-netlist-pmos PATH`
  - （可选）指定 PMOS transient 模板网表路径。

- `--L-scale` / `--W-scale` / `--W-step-scale`
  - 针对 FreePDK45 默认 L/W 扫描范围的缩放因子，用于做工艺节点缩放或减小点数。

- `--max-L-count N` / `--max-W-count M`
  - **仅使用 L、W 列表的前 N / M 个点**，用于快速在小子集上调试。
  - 示例：`--max-L-count 2 --max-W-count 3` 只跑前 2 个 L × 前 3 个 W 的 6 个点。

- `--fresh`
  - 默认脚本会尝试从已有的 `cap_vs_LW*.csv` 中复用已经算好的点，避免重复仿真。
  - 指定 `--fresh` 时：
    - 不复用旧结果；
    - 仅按当前 L/W 网格重新仿真并重写 CSV（适合精确控制测试子集）。

### L/W 扫描范围

#### Sky130（`--pdk Sky130`）

脚本内部针对 Sky130 1.8V 器件设置了适配 binning 的 L/W 范围（单位 µm）：

- L 范围：`0.15` – `98.0`；
- W 范围：`2.0` – `98.0`；
- 步长：约为全范围的 2%，即：
  - `L_step = 0.02 * (L_max - L_min)`
  - `W_step = 0.02 * (W_max - W_min)`

可结合 `--max-L-count` / `--max-W-count` 只选前若干个点进行快速调试。

#### FreePDK45（默认）

- L：对数分布，`0.045 µm` – `10 µm`，共 30 个点。
- W：线性分布，`0.1 µm` – `50 µm`，步长 `0.1 µm`。
- 可用 `--L-scale` / `--W-scale` / `--W-step-scale` 调整。

### 执行过程概述

对每个 (L_um, W_um)：

1. 在 `netlists/<pdk_lower>/` 下生成一个 transient 网表：
  - FreePDK45：替换模板中的 `L_dut` / `W_dut` 参数；
  - Sky130：替换模板中的 `L_dut` / `W_dut` 参数（配合 `scale=1e-6`）。
2. 从 **顶层 `netlists/` 目录** 调用 ngspice：
  - 确保模板里的 `.include` 相对路径保持一致。
3. 从 ngspice stdout 解析 `q_total = ...`（模板中 `meas tran q_total INTEG i(Vgs)` 输出）。
4. 计算大信号电容：
  - `Cgg = |q_total| / VDD`（NMOS；PMOS 可选）。
5. 累积所有点，输出 CSV 与绘图。

输出 CSV：

- NMOS：`test_cap_param/results/<pdk_lower>/cap_vs_LW.csv`
  - 列：`L_um, W_um, Cgg_fF`。
- PMOS：`test_cap_param/results/<pdk_lower>/cap_vs_LW_pmos.csv`
  - 列：`L_um, W_um, Cgg_fF`。

---

## 线性度分析脚本：`analyze_cap_linearity.py`

### 基本用法

在项目根目录执行：

```bash
python test_cap_param/analyze_cap_linearity.py --pdk FreePDK45
```

或：

```bash
python test_cap_param/analyze_cap_linearity.py --pdk Sky130
```

该脚本会在 `test_cap_param/results/<pdk_lower>/` 下读取之前生成的 `cap_vs_LW*.csv`，并输出：

1. 各种线性拟合的 CSV（斜率、截距、R²）。
2. 对应的 R²–L 或 R²–W 曲线图，存放在 `plots/` 子目录中。

### 线性度评价方法

对 NMOS / PMOS，分别进行四类拟合：

1. **固定 L，看 C(W) 的线性度：**
   - 对每个 `L`，拟合
     \( C(W) = m_W(L) \cdot W + b_W(L) \)，得到 slope/intercept/R²；
   - 输出到 `*_linfit_C_vs_W_per_L.csv`，并生成 `R2_*_C_vs_W_over_L.png`。

2. **固定 W，看 C(L) 的线性度：**
   - 对每个 `W`，拟合
     \( C(L) = m_L(W) \cdot L + b_L(W) \)；
   - 输出到 `*_linfit_C_vs_L_per_W.csv`，并生成 `R2_*_C_vs_L_over_W.png`。

这里的 `C` 可以是 `Cgs`、`Cgd`、`Cgb`（NMOS）、或 `Cgs_p`、`Cgd_p`、`Cgb_p`（PMOS）。

### 典型现象与解释

- 对于使用 BSIM4 `capmod=2` 的 MOS 器件（FreePDK45、Sky130）：
  - 主导项是面积型电容：\( C \propto \text{Cox} \cdot W \cdot L_\text{eff} \)；
  - 加上一些与周长和重叠电容相关的线性校正项；
  - 因此在合理的 (L,W) 范围内，`C(L)`、`C(W)` 常表现出 **极高的线性度（R² ~ 1）**。

线性度脚本的输出可以用来：

- 检查 PDK 模型的几何缩放是否大致符合物理预期；
- 与简单宏模型（例如 2D 线性/多项式 C(L,W)）做拟合对比；
- 比较不同 PDK 间的相对电容密度和线性行为差异。

---

## 调试与最小网表示例

建议直接运行 transient 模板并检查 stdout 是否包含 `q_total = ...`：

### FreePDK45：`netlists/freepdk45_tran_cap_template.cir`

```bash
cd netlists
ngspice freepdk45_tran_cap_template.cir
```

- 完成后检查控制台输出：
  - 存在 `q_total = ...`；
  - `c_ls_vec`/`q_total` 的数量级随 W 增大而增大。

### Sky130：`netlists/sky130_tran_cap_template.cir`

```bash
cd netlists
ngspice sky130_tran_cap_template.cir
```

- 确认：
  - 没有 `could not find valid modelname` 或 binning 范围错误；
  - 控制台输出中存在 `q_total = ...`。

如遇仿真报错或电容为 0 的异常，可以：

1. 先在最小网表上调通电荷提取；
2. 再用 `--max-L-count / --max-W-count` 在小范围 L/W 上跑 sweep；
3. 最终回到全范围扫描与线性度分析。

---

## 小结

- transient 模板网表（FreePDK45 / Sky130）负责：包含模型、定义 gate 阶跃、`meas tran q_total INTEG i(Vgs)`。
- `run_cap_param_sweep.py` 负责：
  - 扫描 (L,W)；
  - 自动生成 per-PDK transient 网表；
  - 调用 ngspice 并从 stdout 解析 `q_total` 计算 Cgg；
  - 输出 `cap_vs_LW*.csv` 与 Cgg–L/W 关系图。
- `analyze_cap_linearity.py` 负责：
  - 从 `cap_vs_LW*.csv` 读入电容数据；
  - 对 C–L、C–W 做线性拟合与 R² 分析；
  - 输出拟合 CSV 与线性度图。

按上述说明运行脚本，即可在不同 PDK 下系统性地评估 MOS 栅相关大信号电容随几何参数的变化规律与线性度。
