# MOS 大信号电容仿真与线性度分析

本目录包含用于提取 MOS 大信号电容（Cgs, Cgd, Cgb）并分析其随 L/W 变化线性度的脚本。

核心流程：

1. 使用 DC 网表模板（按 PDK 区分）对单个 NMOS/PMOS 做偏置点分析，写出端电荷。
2. `run_cap_param_sweep.py` 扫描一系列 (L, W)，为每个点生成网表并调用 ngspice 运行，读出电荷并计算 Cgs/Cgd/Cgb。
3. `analyze_cap_linearity.py` 基于生成的 CSV，对 C–L、C–W 关系做线性拟合，评估线性度（R²），并画图。

---

## 目录结构概览

- `netlists/`
  - 顶层目录，放共用的 DC 模板网表与 `.spiceinit`。
  - 关键文件：
    - `freepdk45_dc_circuit.cir`：FreePDK45 DC 偏置 & 大信号电容提取模板。
    - `sky130_dc_circuit.cir`：Sky130 DC 偏置 & 大信号电容提取模板（结构尽量仿照 FreePDK45，仅器件更换）。
    - `test_cap_single.cir` / `test_cap_single_sky130.cir`：用于调试的单点/单器件最小网表。
  - 每次 ngspice 运行时，会在此目录生成/覆盖：
    - `ls_caps_dc.txt`：NMOS 大信号电容端点电荷文件。
    - `ls_caps_dc_pmos.txt`：PMOS 大信号电容端点电荷文件。

- `netlists/<pdk_lower>/`
  - 按 PDK 划分的**自动生成网表**目录（例如 `netlists/freepdk45/`、`netlists/sky130/`）。
  - `run_cap_param_sweep.py` 会在这里为每个 (L,W) 生成一个 DC 网表：
    - 命名示例：`freepdk45_dc_circuit_L0.045u_W0.1u.cir`。

- `test_cap_param/`
  - 本目录：脚本和结果。
  - 脚本：
    - `run_cap_param_sweep.py`：扫描 L/W，调用 ngspice，计算 Cgs/Cgd/Cgb。
    - `analyze_cap_linearity.py`：读取 CSV，对电容随 L/W 的线性度做拟合与绘图。
  - 结果：
    - `results/<pdk_lower>/cap_vs_LW.csv`：NMOS Cgs/Cgd/Cgb vs L/W。
    - `results/<pdk_lower>/cap_vs_LW_pmos.csv`：PMOS Cgs/Cgd/Cgb vs L/W。
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

## DC 模板网表与大信号电容提取方法

大信号电容提取采用文档 `docs/mos_large_signal_caps.md` 中的 **方法 5.1（端点电荷差分法）**：

1. 在两个 gate 电压端点（例如 Vg=0, Vg=VDD）下分别求解 DC 工作点。
2. 在每个工作点，读取通道四端电荷向量：`Qg, Qd, Qs, Qb`。
3. 大信号电容定义为：
   - `Cgs = -(Qs(Vg2) - Qs(Vg1)) / (Vg2 - Vg1)`
   - `Cgd = -(Qd(Vg2) - Qd(Vg1)) / (Vg2 - Vg1)`
   - `Cgb = -(Qb(Vg2) - Qb(Vg1)) / (Vg2 - Vg1)`

### FreePDK45 模板：`netlists/freepdk45_dc_circuit.cir`

- 引入模型：
  ```spice
  .inc ../models/FreePDK45/nom.inc
  ```
  其中 `NMOS_VTG` / `PMOS_VTG` 为 BSIM4 level 54 模型，`capmod=2`，使用电荷模型计算电容。

- 器件实例：
  - `M1`：IV 扫描用 NMOS。
  - `M2`：NMOS 偏置与电荷提取用。
  - `M3`：PMOS 偏置与电荷提取用。

- 大信号电容提取（节选）：
  - 通过多组 `alter + op` 定义一系列 (Vds, Vgs) 偏置点。
  - 在关键的两个点（例如 Vds=1.2, Vg=0 / 1.2）下：
    ```spice
    let qg_bias = @M2[qg]
    let qd_bias = @M2[qd]
    let qs_bias = @M2[qs]
    let qb_bias = @M2[qb]
    echo "... $&qg_bias $&qd_bias $&qs_bias $&qb_bias" >> ./ls_caps_dc.txt
    ```
  - PMOS 部分类似，写入 `ls_caps_dc_pmos.txt`。

### Sky130 模板：`netlists/sky130_dc_circuit.cir`

- 引入 Sky130 1.8V 器件模型：
  - `sky130_fd_pr__nfet_01v8`
  - `sky130_fd_pr__pfet_01v8`
  - 以及必要的 corner / mismatch / invariant 等参数文件。

- 器件实例：
  - `X1`：IV 扫描 NMOS 子电路。
  - `X2`：NMOS 偏置与电荷提取用子电路。
  - `X3`：PMOS 偏置与电荷提取用子电路。

- 内部 MOS 为 BSIM4 level 54（`sky130_fd_pr__nfet_01v8__model.3`），同样使用 `capmod=2` 的电荷模型。

- 大信号电容提取结构与 FreePDK45 尽量一致，只是层次不同：
  - 利用 `@m.x2.msky130_fd_pr__nfet_01v8[qg]` / `[...] [qd] [qs] [qb]` 访问内部 MOS 四端电荷；
  - 通过一系列 `alter + op` 设定多个 (Vds, Vgs) 偏置点，在两个 gate 端点电压下写出 `ls_caps_dc.txt` 和 `ls_caps_dc_pmos.txt`。

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
    --dc-netlist netlists/sky130_dc_circuit.cir
```

主要命令行参数：

- `--pdk PDK_NAME`
  - 用于生成网表文件名、结果目录和图标题。
  - 示例：`FreePDK45`（默认）、`Sky130`。

- `--dc-netlist PATH`
  - 指定 DC 偏置/电荷提取模板网表路径。
  - 未指定时，默认使用 `netlists/freepdk45_dc_circuit.cir`。

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

1. 在 `netlists/<pdk_lower>/` 下生成一个 DC 网表：
   - FreePDK45：修改模板中 `M2`/`M3` 的 `L=` 和 `W=`；
   - Sky130：修改模板中 `X2`/`X3` 子电路实例的 `l=` / `w=`。
2. 从 **顶层 `netlists/` 目录** 调用 ngspice：
   - 确保模板里的 `.include` 相对路径和 `wrdata` 输出路径保持一致。
   - 每次运行会覆盖 `netlists/ls_caps_dc.txt` / `ls_caps_dc_pmos.txt`。
3. 读取 `ls_caps_dc*.txt`：
   - 头一行是列名：`Vg Vd Qg Qd Qs Qb`；
   - 后面至少两行，对应两个 gate 端点偏置。
4. 使用端点电荷差分法计算：
   - `Cgs, Cgd, Cgb`（NMOS 和 PMOS 各一组）。
5. 累积所有点，输出 CSV 与绘图。

输出 CSV：

- NMOS：`test_cap_param/results/<pdk_lower>/cap_vs_LW.csv`
  - 列：`L_um, W_um, Cgs_fF, Cgd_fF, Cgb_fF`。
- PMOS：`test_cap_param/results/<pdk_lower>/cap_vs_LW_pmos.csv`
  - 列：`L_um, W_um, Cgs_p_fF, Cgd_p_fF, Cgb_p_fF`。

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

### FreePDK45：`netlists/test_cap_single.cir`

最小例子用于验证单个 FreePDK45 NMOS 的大信号电容提取：

```bash
cd netlists
ngspice test_cap_single.cir
```

- 完成后检查 `ls_caps_dc.txt` 中两行数据：
  - 确认 Vg 两个端点下的 `Qg, Qd, Qs, Qb` 有明显差异；
  - 用脚本手算 `Cgs, Cgd, Cgb` 可与 `run_cap_param_sweep.py` 的结果核对。

### Sky130：`netlists/test_cap_single_sky130.cir`

同理，用于验证 Sky130 1.8V 器件的电荷访问和偏置设置是否正确：

```bash
cd netlists
ngspice test_cap_single_sky130.cir
```

- 确认：
  - 没有 `could not find valid modelname` 或 binning 范围错误；
  - `ls_caps_dc.txt` 中的 Q 在不同 Vg 下有合理变化。

如遇仿真报错或电容为 0 的异常，可以：

1. 先在最小网表上调通电荷提取；
2. 再用 `--max-L-count / --max-W-count` 在小范围 L/W 上跑 sweep；
3. 最终回到全范围扫描与线性度分析。

---

## 小结

- DC 模板网表（FreePDK45 / Sky130）负责：偏置、调用 PDK 模型、写出端点电荷文件 `ls_caps_dc*.txt`。
- `run_cap_param_sweep.py` 负责：
  - 扫描 (L,W)；
  - 自动生成 per-PDK 网表；
  - 调用 ngspice 并从 `ls_caps_dc*.txt` 计算 Cgs/Cgd/Cgb；
  - 输出 `cap_vs_LW*.csv` 与 C–L/W 关系图。
- `analyze_cap_linearity.py` 负责：
  - 从 `cap_vs_LW*.csv` 读入电容数据；
  - 对 C–L、C–W 做线性拟合与 R² 分析；
  - 输出拟合 CSV 与线性度图。

按上述说明运行脚本，即可在不同 PDK 下系统性地评估 MOS 栅相关大信号电容随几何参数的变化规律与线性度。
