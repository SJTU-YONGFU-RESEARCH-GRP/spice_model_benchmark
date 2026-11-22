# SPICE Models & Process Corners Catalog

This directory contains clean, streamlined SPICE model cards and process corners used by the `spice_model_benchmark` verification and regression system. All non-simulation layout, DRC, LVS, and documentation files have been removed to keep the directory lightweight and focused strictly on circuit simulation.

---

## 1. FreePDK45 (45nm Bulk CMOS, BSIM4)
- **Technology:** 45nm bulk CMOS
- **Standard Model:** BSIM4.0
- **Path:** `models/FreePDK45/`
- **Process Corners:**
  - **Typical-Typical (TT):** `models/FreePDK45/nom.inc` (Nominal supply: 1.0V – 1.2V)
  - **Fast-Fast (FF):** `models/FreePDK45/ff.inc`
  - **Slow-Slow (SS):** `models/FreePDK45/ss.inc`
- **Available Devices:**
  - `NMOS_VTG` / `PMOS_VTG`: Nominal regular-threshold core transistors
  - `NMOS_VTH` / `PMOS_VTH`: High-threshold low-leakage transistors
  - `NMOS_VTL` / `PMOS_VTL`: Low-threshold high-speed transistors
  - `NMOS_THKOX` / `PMOS_THKOX`: Thick-oxide 2.5V I/O transistors

---

## 2. IHP SG13G2 (130nm BiCMOS, BSIM4 / HICUM)
- **Technology:** 130nm SiGe:C BiCMOS
- **Standard Model:** BSIM4 (MOSFETs), HICUM/L2 (HBTs)
- **Path:** `models/IHP-Open-PDK/ihp-sg13g2/libs.tech/ngspice/models/`
- **Process Corners (`cornerMOSlv.lib`):**
  - **Typical-Typical (TT):** Section `mos_tt`
  - **Fast-Fast (FF):** Section `mos_ff`
  - **Slow-Slow (SS):** Section `mos_ss`
- **Supporting Libraries:**
  - `sg13g2_moslv_mod.lib`, `sg13g2_moslv_parm.lib`: Low-voltage (1.2V/1.5V) NMOS/PMOS models
  - `cornerMOShv.lib`, `sg13g2_moshv_mod.lib`: High-voltage (3.3V) NMOS/PMOS models
  - `cornerHBT.lib`, `sg13g2_hbt_mod.lib`: High-speed SiGe heterojunction bipolar transistors

---

## 3. SkyWater SKY130 (130nm Bulk CMOS, BSIM4)
- **Technology:** 130nm bulk CMOS
- **Standard Model:** BSIM4.5
- **Path:** `models/skywater-pdk-libs-sky130_fd_pr/models/` and `models/skywater-pdk-libs-sky130_fd_pr/cells/`
- **Process Corners (`sky130.lib.spice`):**
  - **Typical-Typical (TT):** Section `tt` (Nominal supply: 1.8V)
  - **Fast-Fast (FF):** Section `ff`
  - **Slow-Slow (SS):** Section `ss`
  - **Slow-Fast (SF):** Section `sf`
  - **Fast-Slow (FS):** Section `fs`
- **Primary Core Transistors:**
  - `sky130_fd_pr__nfet_01v8`: 1.8V standard NMOS
  - `sky130_fd_pr__pfet_01v8`: 1.8V standard PMOS
  - `sky130_fd_pr__nfet_01v8_lvt`: 1.8V low-threshold NMOS
  - `sky130_fd_pr__pfet_01v8_hvt`: 1.8V high-threshold PMOS

---

## 4. ASAP7 (7nm FinFET, BSIM-CMG)
- **Technology:** 7nm FinFET Predictive Model
- **Standard Model:** BSIM-CMG (multi-gate FinFET)
- **Path:** `models/PDKs/ASAP7_7nm/spice/`
- **Process Corners:**
  - **Typical-Typical (TT):** `7nm_TT_160803.pm` (Nominal supply: 0.7V)
  - **Fast-Fast (FF):** `7nm_FF_160803.pm`
  - **Slow-Slow (SS):** `7nm_SS_160803.pm`

---

## 5. GF180MCU (180nm Bulk CMOS, BSIM4)
- **Technology:** 180nm bulk CMOS
- **Standard Model:** BSIM4
- **Path:** `models/PDKs/GF180MCU_180nm/spice/`
- **Model Includes:** `design.ngspice` (devices: `nmos_10p0_asym`, `nmos_3p3`, `nmos_6p0`, `pmos_3p3`, `pmos_6p0`)

