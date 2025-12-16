# Sky130 单位面积栅相关电容回归结果说明

本文件说明 `test_cap_param/results/sky130_unit_area_caps.csv` 的含义与用法。

该 CSV 是在 **Sky130 大信号电容 L/W 扫描结果** 基础上，对电容与器件面积进行线性回归得到的等效单位面积电容密度。

---

## 1. CSV 文件路径

- 相对工程根目录路径：
  - `test_cap_param/results/sky130_unit_area_caps.csv`

文件示例内容：

```text
pdk,device,cap_name,slope_fF_per_um2,intercept_fF,R2,C_per_area_F_per_m2
Sky130,NMOS,Cgs,2.01065,-3.53719,1.000000,0.00201065
Sky130,NMOS,Cgd,1.34226,-2.39954,1.000000,0.00134226
Sky130,NMOS,Cgb,1.02792,16.3792,0.999963,0.00102792
Sky130,PMOS,Cgs_p,-0.575407,-4.12464,0.999995,-0.000575407
Sky130,PMOS,Cgd_p,-0.383828,-2.751,0.999995,-0.000383828
Sky130,PMOS,Cgb_p,-1.61859,-1.3979,0.999996,-0.00161859
```

---

## 2. 各列含义

- **`pdk`**  
  PDK 名称，这里固定为 `Sky130`。

- **`device`**  
  器件类型：
  - `NMOS`：`sky130_fd_pr__nfet_01v8` 的结果；
  - `PMOS`：`sky130_fd_pr__pfet_01v8` 的结果（注意符号约定）。

- **`cap_name`**  
  电容名称：
  - `Cgs`, `Cgd`, `Cgb`：NMOS 的栅-源 / 栅-漏 / 栅-体大信号电容；
  - `Cgs_p`, `Cgd_p`, `Cgb_p`：PMOS 的对应量。

- **`slope_fF_per_um2`**  
  线性回归模型中面积项的斜率，单位为 **fF/µm²**。

  回归假设为：

  \[
  C(L, W) \approx m \cdot A + b,\quad A = L \cdot W\ (\mu\text{m}^2)
  \]

  其中：

  - `m = slope_fF_per_um2`（fF/µm²），可视为 **等效单位面积电容密度**；
  - `b = intercept_fF`（fF），为小的常数偏移（主要反映重叠/周长电容等）。

- **`intercept_fF`**  
  回归截距 `b`，单位为 **fF**。在面积较大时，相对 `m·A` 比较小，一般可视为次要修正。

- **`R2`**  
  回归的决定系数（coefficient of determination）。越接近 1，说明在给定 L/W 范围内，

  - 电容与面积的线性假设越好；
  - 这里各项 R² 基本在 0.9999 以上，说明 **C ≈ m·(L·W) + b** 是非常好的近似。

- **`C_per_area_F_per_m2`**  
  将斜率从 fF/µm² 换算到 SI 单位 **F/m²**。

  换算关系：

  - 1 µm = 1e−6 m → 1 µm² = 1e−12 m²；
  - 1 fF = 1e−15 F；
  - 因此：1 fF/µm² = (1e−15 F)/(1e−12 m²) = 1e−3 F/m²。

  所以：

  \[
  C_{\text{per\_area}}(\text{F/m}^2) = \text{slope\_fF\_per\_um2} \times 10^{-3}.
  \]

---

## 3. 如何使用这些回归结果

在线性回归模型下，可以在给定 L、W（单位 µm）时，快速估算电容值：

1. **计算面积**：

   \[ A = L\cdot W\ (\mu\text{m}^2) \]

2. **查表得到对应电容的 `m` 和 `b`**（例如 NMOS Cgs）：

   - `m = slope_fF_per_um2`；
   - `b = intercept_fF`。

3. **估算电容值（fF）**：

   \[
   C(L, W) \approx m \cdot A + b\quad (\text{fF})
   \]

4. **单位面积电容（F/m²）**：

   直接使用 `C_per_area_F_per_m2` 列即可，无需再换算。

> 对 PMOS 项（`Cgs_p`/`Cgd_p`/`Cgb_p`），斜率为负号是因为大信号电荷差分中电荷方向约定不同：
> 
> - 若只关心“电容大小”，可对斜率取绝对值；
> - 若同时关心电荷方向与符号，则应保留 CSV 中的原始正负号。

---

## 4. 适用范围与注意事项

- 该回归是基于脚本 `run_cap_param_sweep.py` 对 **Sky130 1.8V 器件** 在一定 L/W 范围内的大信号电容数据拟合得到：
  - L 范围约为 0.15–98 µm；
  - W 范围约为 2–98 µm（具体范围见脚本内部设置）。
- 在上述范围内，`C ≈ m·A + b` 拟合的 R² 非常高，可认为是一个可靠的一阶近似；
- 若在明显超出该范围的 L/W 上使用，误差可能增大，需要重新跑 sweep 并拟合。

---

## 5. 与物理模型的联系（简要）

- Sky130 的 `nfet_01v8` / `pfet_01v8` 内部使用 **BSIM4 (level 54)**，`capmod=2` 的电荷模型：
  - 主导项为平行板栅氧电容：\( C \propto C_{ox} \cdot W \cdot L_{\text{eff}} \)；
  - 叠加重叠、边缘及周长相关电容项。
- 因此在给定的几何范围内，电容对面积的近似线性（R² ≈ 1）是符合模型物理预期的，
  本 CSV 给出的单位面积电容密度可以视作该 PDK 下、该偏置条件和几何范围内的
  “等效 Cox + 几何修正”的经验参数。
