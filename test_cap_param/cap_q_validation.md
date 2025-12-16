# MOS 大信号电容 Q 提取与数值验证说明

本文件记录当前工程中 **5.1 端电荷差分法** 提取栅相关大信号电容（Cgs、Cgd、Cgb）时，
端电荷 `Q` 的来源，以及如何通过手算验证 `Q` 与计算出来的电容是一致且正确的。

---

## 1. 理论定义回顾（文档 mos_large_signal_caps.md）

对于 MOS 器件四端电荷：

- $Q_g(V_g, V_d, V_s, V_b)$
- $Q_d(V_g, V_d, V_s, V_b)$
- $Q_s(V_g, V_d, V_s, V_b)$
- $Q_b(V_g, V_d, V_s, V_b)$

在仅栅电压变化、其他端固定的情况下（文档第 2 节）：

给定两偏置点：

- 初始：$\mathbf{V}^{(1)} = (V_g^{(1)}, V_d^{(1)}, V_s^{(1)}, V_b^{(1)})$
- 终止：$\mathbf{V}^{(2)} = (V_g^{(2)}, V_d^{(2)}, V_s^{(2)}, V_b^{(2)})$

若仅 $V_g$ 发生变化：

$$
\Delta V_g = V_g^{(2)} - V_g^{(1)}
$$

则三类栅相关大信号电容定义为：

$$
\begin{aligned}
C_{gs}^{\text{LS}} &= -\frac{Q_s^{(2)} - Q_s^{(1)}}{\Delta V_g} \\
C_{gd}^{\text{LS}} &= -\frac{Q_d^{(2)} - Q_d^{(1)}}{\Delta V_g} \\
C_{gb}^{\text{LS}} &= -\frac{Q_b^{(2)} - Q_b^{(1)}}{\Delta V_g}
\end{aligned}
$$

这是本工程 DC 端电荷法（5.1）严格遵循的数学定义。

---

## 2. SPICE 中 Q 的提取方式（5.1 端电荷法）

### 2.1 Netlist 与仿真设置

Netlist：`netlists/freepdk45_dc_circuit.cir`，Bias Point Analysis 段中对器件 `M2`：

```spice
* MOSFET device under test for bias point analysis
M2 drain_bias gate_bias source_bias bulk_bias NMOS_VTG L=0.045u W=10u
...
* Initialize large-signal capacitance DC charge file (for method 5.1)
echo "Vg Vd Qg Qd Qs Qb" > ./ls_caps_dc.txt

* Seventh bias point (1.2, 0.0)
alter Vds_bias = 1.2
alter Vgs_bias = 0.0
op
let qg_bias = @M2[qg]
let qd_bias = @M2[qd]
let qs_bias = @M2[qs]
let qb_bias = @M2[qb]
echo "$&v(gate_bias) $&v(drain_bias) $&qg_bias $&qd_bias $&qs_bias $&qb_bias" >> ./ls_caps_dc.txt
...
* Ninth bias point (1.2, 1.2)
alter Vds_bias = 1.2
alter Vgs_bias = 1.2
op
let qg_bias = @M2[qg]
let qd_bias = @M2[qd]
let qs_bias = @M2[qs]
let qb_bias = @M2[qb]
echo "$&v(gate_bias) $&v(drain_bias) $&qg_bias $&qd_bias $&qs_bias $&qb_bias" >> ./ls_caps_dc.txt
```

仿真条件：

- 工艺：FreePDK45，`../models/FreePDK45/nom.inc`（nominal/TT）
- 器件：`NMOS_VTG`，L=0.045µm，W=10µm
- 偏置：
  - $V_s = 0$, $V_b = 0$
  - $V_d = 1.2\,\text{V}$
  - $V_g$：在 5.1 中采用两个静态点 $0 \to 1.2\,\text{V}$
- 温度：$T = 27 ^\circ\text{C}$

### 2.2 数据文件 ls_caps_dc.txt

ngspice 运行 `freepdk45_dc_circuit.cir` 后，在 `src/results/data/ls_caps_dc.txt` 中得到：

```text
Vg Vd Qg Qd Qs Qb
0   1.2  1.38694E-15  -6.86686E-21  -1.02958E-20  -1.38692E-15
1.2 1.2  5.47816E-15  -1.09965E-15  -1.64847E-15  -2.73003E-15
```

对应两偏置点：

- 状态 1：$V_g^{(1)} = 0$, $V_d^{(1)} = 1.2$
  - $Q_g^{(1)} = 1.38694\times10^{-15}\,\mathrm{C}$
  - $Q_d^{(1)} = -6.86686\times10^{-21}\,\mathrm{C}$
  - $Q_s^{(1)} = -1.02958\times10^{-20}\,\mathrm{C}$
  - $Q_b^{(1)} = -1.38692\times10^{-15}\,\mathrm{C}$

- 状态 2：$V_g^{(2)} = 1.2$, $V_d^{(2)} = 1.2$
  - $Q_g^{(2)} = 5.47816\times10^{-15}\,\mathrm{C}$
  - $Q_d^{(2)} = -1.09965\times10^{-15}\,\mathrm{C}$
  - $Q_s^{(2)} = -1.64847\times10^{-15}\,\mathrm{C}$
  - $Q_b^{(2)} = -2.73003\times10^{-15}\,\mathrm{C}$

---

## 3. 手算验证 ΔQ/ΔV 得到 Cgs/Cgd/Cgb

记：

$$
\Delta V_g = V_g^{(2)} - V_g^{(1)} = 1.2 - 0 = 1.2\,\mathrm{V}
$$

### 3.1 Cgs 的手算

$$
\begin{aligned}
Q_s^{(1)} &= -1.02958\times10^{-20}\,\mathrm{C}\\
Q_s^{(2)} &= -1.64847\times10^{-15}\,\mathrm{C}\\
\Delta Q_s &= Q_s^{(2)} - Q_s^{(1)} \\
&\approx -1.64847\times10^{-15} - (-1.02958\times10^{-20}) \\
&\approx -1.64846\times10^{-15}\,\mathrm{C}
\end{aligned}
$$

代入定义：

$$
C_{gs}^{\text{LS}} = -\frac{\Delta Q_s}{\Delta V_g}
= -\frac{-1.64846\times10^{-15}}{1.2}
\approx 1.37372\times10^{-15}\,\mathrm{F}
$$

换算为 fF：

$$
C_{gs}^{\text{LS}} \approx 1.37372\times10^{-15}\,\mathrm{F}
\approx 1.374\,\mathrm{fF}
$$

与 `src/results/large_signal_caps.txt` 中的 5.1 结果：

```text
cgs_dc: 1.373716e-15 F (1.374 fF)
```
完全一致（仅数值截断误差）。

### 3.2 Cgd 的手算

$$
\begin{aligned}
Q_d^{(1)} &= -6.86686\times10^{-21}\,\mathrm{C}\\
Q_d^{(2)} &= -1.09965\times10^{-15}\,\mathrm{C}\\
\Delta Q_d &= Q_d^{(2)} - Q_d^{(1)} \\
&\approx -1.09965\times10^{-15} - (-6.86686\times10^{-21}) \\
&\approx -1.09964\times10^{-15}\,\mathrm{C}
\end{aligned}
$$

$$
C_{gd}^{\text{LS}} = -\frac{\Delta Q_d}{\Delta V_g}
= -\frac{-1.09964\times10^{-15}}{1.2}
\approx 9.1637\times10^{-16}\,\mathrm{F}
$$

fF：

$$
C_{gd}^{\text{LS}} \approx 0.916\,\mathrm{fF}
$$

与 `large_signal_caps.txt` 中：

```text
cgd_dc: 9.163693e-16 F (0.916 fF)
```
一致。

### 3.3 Cgb 的手算

$$
\begin{aligned}
Q_b^{(1)} &= -1.38692\times10^{-15}\,\mathrm{C}\\
Q_b^{(2)} &= -2.73003\times10^{-15}\,\mathrm{C}\\
\Delta Q_b &= Q_b^{(2)} - Q_b^{(1)} \\
&= -2.73003\times10^{-15} - (-1.38692\times10^{-15}) \\
&= -1.34311\times10^{-15}\,\mathrm{C}
\end{aligned}
$$

$$
C_{gb}^{\text{LS}} = -\frac{\Delta Q_b}{\Delta V_g}
= -\frac{-1.34311\times10^{-15}}{1.2}
\approx 1.11926\times10^{-15}\,\mathrm{F}
$$

fF：

$$
C_{gb}^{\text{LS}} \approx 1.119\,\mathrm{fF}
$$

对应 `large_signal_caps.txt` 中：

```text
cgb_dc: 1.119258e-15 F (1.119 fF)
```
数值完全吻合。

---

## 4. 其他一致性检验

### 4.1 电荷守恒检验

对每个偏置点，可计算：

$$
Q_\text{tot} = Q_g + Q_d + Q_s + Q_b
$$

以状态 1 为例：

$$
\begin{aligned}
Q_\text{tot}^{(1)} &\approx 1.38694\times10^{-15} + (-6.87\times10^{-21}) \\
&\quad + (-1.03\times10^{-20}) + (-1.38692\times10^{-15}) \\
&\approx  (1.38694 - 1.38692)\times10^{-15} + O(10^{-20}) \\
&\approx 2\times10^{-20}\,\mathrm{C}
\end{aligned}
$$

量级远小于单个端电荷（10⁻¹⁵ C），说明数值上满足

$$
Q_g + Q_d + Q_s + Q_b \approx 0
$$

这是端电荷向量的一致性检验。

### 4.2 与 transient 方法的对比（特别是 Cgb）

在 transient 电流积分法（5.2）中，从 `tran_charge.txt` 重新积分 $i_b(t)$ 得到 $Q_b(t)$，再按同样的 -ΔQ/ΔVg 公式计算 Cgb，得到的数值约为：

- $|C_{gb}^{\text{rise}}| \approx 1.12\,\mathrm{fF}$
- $|C_{gb}^{\text{fall}}| \approx 1.08\,\mathrm{fF}$

与 5.1 方法的 \(C_{gb}^{\text{LS}} \approx 1.119\,\mathrm{fF}\) 高度一致，仅有积分/选点带来的微小偏差，进一步说明：

- 端电荷 \(Q_b\) 的提取与符号约定是稳定且自洽的；
- DC 端电荷法（5.1）与 transient 积分法（5.2）在 **bulk 端电容** 上等价。

（相比之下，Cgs/Cgd 在 5.2 中受导通电流影响较大，数值上出现一大正一大负但总和很小的情况，这属于“电荷在 S/D 之间如何分配”的工程问题，而不是 5.1 路径的错误。）

---

## 5. 结论

1. 当前 5.1 端电荷差分法中使用的 Q 值来自 ngspice/BSIM4 内部端电荷向量 `@M2[qg]`, `@M2[qd]`, `@M2[qs]`, `@M2[qb]`，通过 `freepdk45_dc_circuit.cir` 写入 `ls_caps_dc.txt`。
2. 按文档定义 $C_{ij}^{\text{LS}} = -\Delta Q_i/\Delta V_j$ 手算得到的 Cgs/Cgd/Cgb，与代码自动计算并写入 `large_signal_caps.txt` 中的 `cgs_dc/cgd_dc/cgb_dc` 完全一致（数值到 1e-18 量级精度）。
3. 电荷守恒关系 $Q_g+Q_d+Q_s+Q_b \approx 0$ 在每个偏置点都成立，进一步证明 Q 向量的一致性。
4. 与 transient 电流积分法在 Cgb 上的交叉验证表明，两种方法在“端电荷→大信号电容”的映射上是一致的；因此，可以将 5.1 提取到的 Cgs/Cgd/Cgb 视为符合文档定义的 **Ground Truth**。

后续在 `test_cap_param/` 中的 L/W 扫描与 unit-width 电容拟合，均基于上述经过验证的 5.1 端电荷差分法结果。
