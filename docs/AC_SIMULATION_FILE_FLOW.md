# AC 仿真文件流转说明（现状）

更新时间：2025-12-20

本文档聚焦“AC 仿真在文件层面的流程”，说明：
- 入口脚本/网表文件分别做什么
- ngspice 运行时在哪个目录生成哪些结果文件
- 结果如何被 Python 解析、绘图并汇总到报告
- 与 AC 相关的两个旁路脚本：4×4 矩阵分量绘图、TRAN 大信号 vs AC 积分一致性验证

> 说明：本仓库有多种 PDK/网表变体（例如 netlists/freepdk45_ac_circuit.cir 等）。本文以默认主链路 netlists/ac_circuit.cir 为核心描述。

---

## 1. 主链路：基准系统的 AC 仿真（CV + 4×4 矩阵 + S 参数 + NQS + 电荷守恒）

### 1.1 入口脚本与运行方式

主入口是 src/mosfet_simulation.py（类 MOSFETSimulation）。

典型运行命令（只跑 AC）：

```bash
python src/mosfet_simulation.py --mode ac --output-dir results_ac_cmatrix
```

参数含义（摘自命令行解析）：
- --mode：选择仿真模式，可选 ac/dc/transient/noise；只想跑 AC 用 --mode ac
- --ac-circuit：AC 网表路径，默认 netlists/ac_circuit.cir
- --output-dir：结果输出目录（建议用 results_ac_cmatrix 之类专用目录避免覆盖）

### 1.2 仿真执行器：src/simulation_runner.py

关键类：src/simulation_runner.py 中的 SimulationRunner。

它做两件事：
1) 调用 ngspice 批处理运行网表
- 实际命令类似：ngspice -b <netlist>
- 执行时会 cd 到网表所在目录（例如 netlists/）

2) 运行完成后，把网表目录里生成的结果文件搬运到输出目录
- 目标目录：<output-dir>/data/
- 通过 OUTPUT_FILE_PATTERNS 里的模式匹配决定要搬哪些文件
  - 包含：cv_data.txt、cmatrix_data.txt、charge_conservation.txt、sparams_data.txt、nqs_effects.txt 等

因此：
- ngspice 首先把文件写在 netlists/ 下
- SimulationRunner 再把匹配的文件移动到 results_xxx/data/ 下

### 1.3 AC 网表：netlists/ac_circuit.cir

netlists/ac_circuit.cir 在 .control 里按以下顺序生成数据文件：

#### 1) CV（随 Vg 扫描）
输出文件：cv_data.txt

- 表头（第一行）类似：
  - Vg
  - Cgg_1kHz / Cgg_10kHz / Cgg_100kHz / Cgg_1MHz
  - Cgb_1MHz / Cgs_1MHz / Cgd_1MHz

- C 的定义：对电压源电流取导纳虚部换算
  - 例如（1MHz）：C = -Im(i(Vx)) / (2πf)

特别注意：这里的 Cgs/Cgd/Cgb 的“命名约定”是“Gate 激励 (VG AC=1) 下，分别用 i(VS)/i(VD)/i(VB) 反推的电容”，也就是矩阵的 (row, col) 视角：
- Cgs = -Im(i(VS))/ω（row s, col g）
- Cgd = -Im(i(VD))/ω（row d, col g）
- Cgb = -Im(i(VB))/ω（row b, col g）

#### 2) 4×4 小信号电容矩阵（同一个 Vg bias 点）
输出文件：cmatrix_data.txt

- 表头（第一行）是 17 列：
  - Vg + 16 个 Cij（按 {g,d,s,b} 电流行 × {g,d,s,b} 激励列展平）

- 生成方式：对每个 Vg bias 点，分别把某一个端口的 AC 幅度设为 1（其它端口 0），跑一次 ac lin 1 f f，并记录四个端口电流得到一列。重复 4 次得到 4 列，从而得到 4×4。

- 矩阵定义（网表注释中已写清）：
  - I = j·ω·C·V
  - C_ij = -Im(Y_ij)/ω

#### 3) S 参数（高频小信号）
输出文件：sparams_data.txt

- 文件有两行注释头，然后是若干频点数据。
- 当前网表里 S 参数部分有“占位写入”（echo 固定数字）逻辑：
  - 它会进行 ac 分析并计算一些中间量，但最终写入文件的数值目前是 placeholder。
  - 因此：如果你在意 S 参数真实数值，需要单独校正这一段的写文件方式。

#### 4) NQS（非准静态）相位差
输出文件：nqs_effects.txt

- 主要记录不同频点下：
  - vg_phase、id_phase、phase_diff

#### 5) 电荷守恒（瞬态）
输出文件：charge_conservation.txt

- 虽然该段属于 tran，但被放在 ac_circuit.cir 的最后一段一起跑，用于验证端口电流/电荷一致性。

### 1.4 数据解析：src/data_reader.py

关键类：src/data_reader.py 的 DataReader。

AC 相关读取接口（在 src/mosfet_simulation.py 的 AC 分支中调用）：
- read_cv_data(output_dir) → 读取 <output-dir>/data/cv_data.txt
- read_capacitance_matrix_data(output_dir) → 读取 <output-dir>/data/cmatrix_data.txt
- read_sparameter_data(output_dir) → 读取 <output-dir>/data/sparams_data.txt
- read_nqs_effects_data(output_dir) → 读取 <output-dir>/data/nqs_effects.txt
- read_charge_conservation_data(output_dir) → 读取 <output-dir>/data/charge_conservation.txt

DataReader 的 _find_file 逻辑会优先找 <output-dir>/data/，找不到时会回退到 output_dir 或 netlists/。

### 1.5 绘图：src/plot_generator.py

关键类：src/plot_generator.py 的 PlotGenerator。

AC 相关图通常输出到：
- <output-dir>/plots/

从 results_ac_cmatrix/REPORT.md 可见，典型产物包括：
- plots/ac_cv_characteristics.png
- plots/ac_cv_components.png
- plots/ac_cv_sparameter_analysis.png
- plots/ac_cv_nqs_effects.png
- plots/ac_charge_conservation.png

### 1.6 报告：src/verification_manager.py

关键类：src/verification_manager.py 的 VerificationManager。

流程：
- src/mosfet_simulation.py 在完成仿真、读取数据、绘图后，调用 update_verification_checklist
- 该函数生成 <output-dir>/REPORT.md
- 报告会引用 <output-dir>/plots/ 下的图片并给出关键数值摘要

例子：results_ac_cmatrix/REPORT.md（该目录就是一次只跑 AC 的输出目录）。

### 1.7 AC 积分得到“大信号电容/电荷”（新增）

主链路 `--mode ac` 现在会在读取 `cv_data.txt` 后，**对小信号 C(V) 做电压积分**，得到沿 Vg 扫描路径的等效“大信号电容”（Large-Signal / line-segment average）。

实现位置：
- `src/mosfet_simulation.py` 的 AC 分支（读取完 CV 后执行积分并写文件）
- `src/data_reader.py` 新增 `read_cv_table_data()` 用于解析 `cv_data.txt` 的列格式

输出文件（<OUT>/data/）：
- `ac_ls_caps_from_cv_integral.csv`：由 AC C(V) 积分得到的 `Cgg/Cgs/Cgd/Cgb` 等效大信号电容（单位同时给出 F 与 fF）
- `ac_qg_from_cv_integral.csv`：由 `Cgg(Vg)` 积分得到的 `Qg(Vg)` 曲线（单位 Coulomb）

报告（<OUT>/REPORT.md）中会增加 `AC-Integral Large-Signal Capacitance` 小节，给出 `Cgg_ls` 等摘要并引用上述输出文件。

---

## 2. 旁路 1：4×4 电容矩阵分量 C–V 绘图（每个 Cij 一张图）

用途：把主链路生成的 cmatrix_data.txt（17 列）画成 16 条 C(Vg) 曲线图，每个分量单独一张 PNG。

相关文件：
- test_cap_param/plot_cmatrix_caps.py

输入：
- <input-dir>/data/cmatrix_data.txt
  - input-dir 通常是一次 AC 仿真的输出目录，例如 results_ac_cmatrix

输出（默认）：
- <input-dir>/plots/cmatrix_caps/
  - cgg.png、cgd.png、…、cbb.png（共 16 张）

常用命令：
```bash
# 默认从 results_ac_cmatrix 读，并写到 results_ac_cmatrix/plots/cmatrix_caps/
python test_cap_param/plot_cmatrix_caps.py

# 只画部分分量
python test_cap_param/plot_cmatrix_caps.py --cap cgg cgs cgd

# 指定输入目录
python test_cap_param/plot_cmatrix_caps.py --input-dir results_ac_cmatrix --cap cgg cgs
```

---

## 3. 旁路 2：TRAN 大信号电容提取 vs AC 小信号积分验证（Cgs/Cgd/Cgb/Csb/Cdb）

用途：验证“TRAN 通过电流积分得到的等效大信号电容”与“AC 小信号 C(V) 沿电压路径积分得到的等效电容”一致。

相关文件：
- test_cap_param/verify_ls_caps_vs_ac_integral.py

### 3.1 它用到的网表/临时文件

该脚本会在 netlists/temp_ls_caps_vs_ac/ 下生成并运行 4 个临时网表：
- ac_sweep_vg.cir：扫 VG，输出 Cgs/Cgd/Cgb 随 Vg
- ac_sweep_vb.cir：扫 VB，输出 Csb/Cdb 随 Vb
- tran_step_vg.cir：VG 做阶跃（0→0.8 之类），通过积分 i(VS)/i(VD)/i(VB) 得到等效大信号电容
- tran_step_vb.cir：VB 做阶跃（0→-0.8 之类），通过积分 i(VS)/i(VD) 得到等效大信号电容

补充：该旁路脚本也会输出 `Cgg`（通过 `i(VG)`）并在对比表中给出 `cgg` 行。

注意：脚本里已经避免在 ngspice 网表中使用字符串 if（ngspice 不支持），而是在 Python 侧生成不同的 .control 片段。

### 3.2 输出文件

默认输出目录：test_cap_param/results/ls_caps_vs_ac/

主要产物：
- ac_sweep_vg.txt / ac_sweep_vb.txt：AC sweep 表格
- tran_step_vg.cir.log.txt / tran_step_vb.cir.log.txt：ngspice 输出日志（包含 meas 值）
- cap_compare.csv：汇总 TRAN 与 AC 积分对比（tran_fF / ac_int_fF / rel_err）

### 3.3 可调参数（速度/精度相关）

- --ac-step：AC 扫描的电压步长（V）
  - 步长越大 → 点数越少 → 越快，但 AC 积分误差可能变大
  - 例如：--ac-step 0.2 很快，--ac-step 0.01 更精细但更慢

- --ac-freq：AC 单点频率（Hz），默认 1e6

---

## 4. “AC 仿真结果文件”速查表

当你运行：
```bash
python src/mosfet_simulation.py --mode ac --output-dir <OUT>
```

通常会得到：

数据（<OUT>/data/）：
- cv_data.txt：CV（多频 Cgg + 1MHz 的 Cgb/Cgs/Cgd）
- cmatrix_data.txt：4×4 小信号电容矩阵随 Vg
- sparams_data.txt：S 参数（当前网表内含 placeholder 写入逻辑）
- nqs_effects.txt：NQS 相位差
- charge_conservation.txt：电荷守恒（tran）

（新增）AC 积分大信号结果（<OUT>/data/）：
- ac_ls_caps_from_cv_integral.csv：AC C(V) 积分得到的大信号等效电容
- ac_qg_from_cv_integral.csv：由 Cgg(Vg) 积分得到的 Qg(Vg)

图（<OUT>/plots/）：
- ac_cv_characteristics.png、ac_cv_components.png 等 AC 相关图

报告（<OUT>/REPORT.md）：
- 汇总表 + 图引用 + 关键指标

---

## 5. 常见定位技巧（按文件找问题）

- “结果文件没生成”
  - 先看 ngspice 是否在 netlists/ 下生成了 txt
  - 再看 SimulationRunner 是否把它 move 到 <OUT>/data/

- “DataReader 读不到文件”
  - 检查 <OUT>/data/ 是否存在对应 txt
  - DataReader 会回退到 netlists/，但主链路期望文件被搬运到 data 目录

- “只想调 VG 扫描步长/速度”
  - 主链路：改 netlists/ac_circuit.cir 里的 let vg_step
  - 旁路验证：直接改命令行 --ac-step
