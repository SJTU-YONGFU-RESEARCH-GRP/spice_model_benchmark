# MOS 大信号电容定义说明

本说明文档给出 CMOS 工艺中 MOS 管五个端口相关“大信号电容”的严格定义，供其他项目在 SPICE 仿真中提取 Ground Truth 使用。

目标电容（NMOS / PMOS 同理）：

- $C_{gs}$：栅–源大信号电容
- $C_{gd}$：栅–漏大信号电容
- $C_{db}$：漏–衬底大信号结电容
- $C_{sb}$：源–衬底大信号结电容
- $C_{gb}$：栅–衬底大信号电容

下面所有定义均基于器件四端电荷 $Q_g, Q_d, Q_s, Q_b$，与具体 SPICE 仿真器无关（Spectre / HSPICE / Ngspice 等均可通过 .op/.dc 访问端电荷或通过电流积分得到电荷变化）。

---

## 1. 总体数学框架

对任意一个 MOS 器件，假设其四端电荷为：

- $Q_g(V_g, V_d, V_s, V_b)$
- $Q_d(V_g, V_d, V_s, V_b)$
- $Q_s(V_g, V_d, V_s, V_b)$
- $Q_b(V_g, V_d, V_s, V_b)$

并满足电荷守恒：

$$
Q_g + Q_d + Q_s + Q_b = 0
$$

### 1.1 小信号与大信号的关系

- 小信号电容（微分定义）：
  $$
  C_{ij}^{\text{ss}}(\mathbf{V}_0) = \left.-\frac{\partial Q_i}{\partial V_j}\right|_{\mathbf{V} = \mathbf{V}_0}
  $$

- 大信号电容（有限差分定义）：

  给定两个偏置状态：

  - 初始：$\mathbf{V}^{(1)} = (V_g^{(1)}, V_d^{(1)}, V_s^{(1)}, V_b^{(1)})$
  - 终止：$\mathbf{V}^{(2)} = (V_g^{(2)}, V_d^{(2)}, V_s^{(2)}, V_b^{(2)})$

  若在这两者之间，**仅第 j 个端口电压发生有限变化**（其余端口电压保持不变）：

  $$
  \Delta V_j = V_j^{(2)} - V_j^{(1)}, \quad \Delta Q_i = Q_i^{(2)} - Q_i^{(1)}
  $$

  则定义：

  $$
  C_{ij}^{\text{LS}}(\mathbf{V}^{(1)} \to \mathbf{V}^{(2)}) \;\stackrel{\text{def}}{=}\; -\frac{\Delta Q_i}{\Delta V_j}
  $$

此处 "LS" 表示 large-signal / line-segment average。这个定义与小信号电容在 $\Delta V_j \to 0$ 极限下是一致的：

$$
\lim_{\Delta V_j \to 0} C_{ij}^{\text{LS}} = C_{ij}^{\text{ss}}
$$

在实际工程中，我们关心的是在一个有限电压摆幅（例如 0 → VDD）下的平均电容，因此采用有限差分形式更符合 RO 延时建模所需的“大信号”含义。

---

## 2. 栅相关大信号电容 Cgs, Cgd, Cgb

### 2.1 实验设定

以 NMOS 为例（PMOS 完全对称替换电压极性）：

- 源端 S 固定在 0 V
- 体端 B 固定在 0 V
- 漏端 D 固定在某个代表性电平（可以选 0 V 或 VDD，视具体应用而定）
- 只改变栅端电压 $V_g$：从 $V_g^{(1)}$ 扫到 $V_g^{(2)}$（例如 0 → VDD）

对这两个偏置点分别求出：

- $Q_g^{(1)}, Q_d^{(1)}, Q_s^{(1)}, Q_b^{(1)}$
- $Q_g^{(2)}, Q_d^{(2)}, Q_s^{(2)}, Q_b^{(2)}$

### 2.2 严格定义

记：

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

同时可定义：

$$
C_{gg}^{\text{LS}} = -\frac{Q_g^{(2)} - Q_g^{(1)}}{\Delta V_g}
$$

由于电荷守恒，应满足近似关系：

$$
C_{gg}^{\text{LS}} \approx C_{gs}^{\text{LS}} + C_{gd}^{\text{LS}} + C_{gb}^{\text{LS}}
$$

注：本仓库的 ngspice/AC 提取采用约定 $C=-\mathrm{Im}(i(V))/\omega$，与上面的统一符号约定一致；主链路 AC 模式也支持对 `Cgg(Vg)` 做电压积分生成 `Qg(Vg)` 与 `Cgg^{LS}`（见 docs/AC_SIMULATION_FILE_FLOW.md）。

这提供了一个可用于数值自检的关系。

---

## 3. 结大信号电容 Cdb, Csb

对结电容，更自然是从 **体端电荷 Qb** 的变化来定义。

### 3.1 漏–衬底结电容 Cdb

实验设定（NMOS）：

- 栅端 G 固定在某一电压 $V_g$（可选与 RO 工作点相关的值）
- 源端 S 固定在 0 V
- 体端 B 固定在 0 V
- 仅改变漏端电压 Vd：从 $V_d^{(1)}$ 到 $V_d^{(2)}$

在这两个偏置点下计算体端电荷：

- $Q_b^{(1)}$ 对应 $V_d^{(1)}$
- $Q_b^{(2)}$ 对应 $V_d^{(2)}$

定义：

$$
\Delta V_d = V_d^{(2)} - V_d^{(1)}, \quad C_{db}^{\text{LS}} = -\frac{Q_b^{(2)} - Q_b^{(1)}}{\Delta V_d}
$$

### 3.2 源–衬底结电容 Csb

实验设定（NMOS）：

- 栅端 G 固定在某一电压 $V_g$
- 漏端 D 固定在某一电压 $V_d$
- 体端 B 固定在 0 V
- 仅改变源端电压 Vs：从 $V_s^{(1)}$ 到 $V_s^{(2)}$

两点的体端电荷为：

- $Q_b^{(1)}$ 对应 $V_s^{(1)}$
- $Q_b^{(2)}$ 对应 $V_s^{(2)}$

定义：

$$
\Delta V_s = V_s^{(2)} - V_s^{(1)}, \quad C_{sb}^{\text{LS}} = -\frac{Q_b^{(2)} - Q_b^{(1)}}{\Delta V_s}
$$

---

## 4. 与 RO 工作偏置的对应（推荐电压路径）

在基于环形振荡器（RO）的延时提取框架中，某一级 CMOS 反相器在稳态与翻转过程中，MOS 管实际上经历的是两个逻辑电平之间的大摆幅切换。为了让在独立 SPICE 实验中提取的大信号电容与 RO 延时模型一致，推荐按以下"代表性偏置路径"选取 $\mathbf{V}^{(1)}, \mathbf{V}^{(2)}$。

### 4.1 系统 N：NMOS 在 pHL（输出下降沿）中的偏置近似

CMOS 反相器连接方式：

- NMOS：D 接输出 Vout，S 接 0 V，G 接输入 Vin，B 接 0 V
- PMOS：D 接输出 Vout，S 接 VDD，G 接输入 Vin，B 接 VDD

在 pHL 过程中（输出从高到低），NMOS 近似经历：

- 状态 A（pHL 开始前）：
  - Vin $= V_g^{(1)} \approx 0$
  - Vout $= V_d^{(1)} \approx VDD$
  - Vs = 0, Vb = 0
  - NMOS 关断

- 状态 B（pHL 结束后）：
  - Vin $= V_g^{(2)} \approx VDD$
  - Vout $= V_d^{(2)} \approx 0$
  - Vs = 0, Vb = 0
  - NMOS 强导通，将输出节点放电至 0

因此，在单独的 MOS 器件实验中，可采用如下路径来定义与 RO pHL 一致的“大信号电容” Ground Truth：

- 栅电压：$V_g$ 从 0 扫到 VDD
- 漏电压：$V_d$ 从 VDD 扫到 0
- 源电压：$V_s = 0$ 固定
- 体电压：$V_b = 0$ 固定

在此路径的起点与终点上，按第 2–3 节给出的公式计算 $C_{gs}^{\text{LS}}, C_{gd}^{\text{LS}}, C_{db}^{\text{LS}}, C_{sb}^{\text{LS}}, C_{gb}^{\text{LS}}$，即可得到与 RO 系统 N 延时分析相匹配的 NMOS 大信号电容参考值。

### 4.2 系统 P：PMOS 在 pLH（输出上升沿）中的偏置近似

PMOS 连接方式：

- D 接输出 Vout
- S 接 VDD
- G 接输入 Vin
- B 接 VDD

在 pLH 过程中（输出从低到高），PMOS 近似经历：

- 状态 A（pLH 开始前）：
  - Vin $= V_g^{(1)} \approx VDD$
  - Vout $= V_d^{(1)} \approx 0$
  - Vs = VDD, Vb = VDD
  - PMOS 关断

- 状态 B（pLH 结束后）：
  - Vin $= V_g^{(2)} \approx 0$
  - Vout $= V_d^{(2)} \approx VDD$
  - Vs = VDD, Vb = VDD
  - PMOS 强导通，将输出节点充电至 VDD

因此，在单独的 PMOS 实验中，可采用如下路径来定义与 RO pLH 一致的“大信号电容” Ground Truth：

- 栅电压：$V_g$ 从 VDD 扫到 0
- 漏电压：$V_d$ 从 0 扫到 VDD
- 源电压：$V_s = VDD$ 固定
- 体电压：$V_b = VDD$ 固定

同样在此路径的起点与终点上，按第 2–3 节的公式计算五个大信号电容，即可得到与 RO 系统 P 延时分析匹配的 PMOS 参考值。

---

## 5. 在 SPICE 中的典型操作方式（概述）

### 5.1 端电荷差分法（推荐）

1. 建立单管测试电路，设置所需的 $V_g, V_d, V_s, V_b$ 偏置和温度 T。
2. 对于某一条路径（只改变一个或两个端电压），在起点与终点分别运行 .op 或 .dc，记录四端电荷：
   - 例如在 Spectre 中可读取 `@M1[qg]`, `@M1[qd]`, `@M1[qs]`, `@M1[qb]`；
3. 代入本文件第 2、3 节给出的有限差分公式，计算对应的 $C_{gs}^{\text{LS}}, C_{gd}^{\text{LS}}, C_{db}^{\text{LS}}, C_{sb}^{\text{LS}}, C_{gb}^{\text{LS}}$。

### 5.2 电流积分法（在不方便直接读 Q 时）

1. 用受控电压源给某端口施加一个缓慢变化的电压波形（例如从 $V^{(1)}$ ramp 到 $V^{(2)}$），保证过程接近准静态。
2. 在波形全过程中记录目标端口的电流 $I_i(t)$。
3. 对电流积分得到电荷变化：
   $$
   \Delta Q_i = \int I_i(t)\,dt
   $$
4. 根据对应端电压变化 $\Delta V_j$，计算：
   $$
   C_{ij}^{\text{LS}} = -\frac{\Delta Q_i}{\Delta V_j}
   $$

在准静态条件下，电流积分法与端电荷差分法等价。

---

本说明文档可以作为在其他项目中定义和提取 MOS 五个大信号电容（Cgs/Cgd/Cdb/Csb/Cgb）的统一规范，尤其适用于与基于环形振荡器的延时–电容提取模型进行定量对比和校准。
