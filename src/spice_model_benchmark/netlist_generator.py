"""Dynamic SPICE Netlist Generator.

Synthesizes self-contained, simulator-compatible netlists on the fly for
evaluating SPICE compact models across DC, AC, Transient, Noise, and Physics
(Gummel Symmetry, Passivity, Smoothness) verification modes without relying
on external static template files.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Optional, Union

from .model_parser import DeviceSpec, ModelInfo


# Synthetic fallback PMOS model card for inverter/CMOS analysis when testing standalone NMOS
SYNTHETIC_PMOS_CARD = """
* Auto-generated fallback PMOS model for CMOS transient / inverter evaluation
.model PMOS_AUTO PMOS (
+ LEVEL=54 VERSION=4.5
+ VTH0=-0.4 TOX=1.4e-9 U0=150 VSAT=80000 RDSW=200
+ ETA0=0.08 PCLM=1.2 PDIBLC1=0.4 PDIBLC2=0.001
+ DROUT=0.5 PSCBE1=5e8 PSCBE2=1e-5 PVAG=0.01 DELTA=0.01
+ A0=1.1 AGS=0.25 A1=0 A2=1 B0=0 B1=0 K1=0.4
+ K2=0.01 K3=0 K3B=0 W0=2.5e-6 DVT0=1.5 DVT1=0.45
+ DVT2=0.02 DSUB=0.2 CIT=0 CDSC=2.4e-4 CDSCB=0 CDSCD=0
+ NFACTOR=1.5 XJ=1e-8 LINT=1e-9 WINT=1e-9 DWG=0 DWB=0
+ VOFF=-0.1 MINV=1 CKAPPA=0.6 CGDO=5e-10 CGSO=5e-10
+ CGBO=1e-12 CJ=0.001 MJ=0.5 PB=0.9 CJSW=1e-10
+ MJSW=0.33 PBSW=0.9 CF=0 PVTH0=0 PRDSW=0 PK2=0
+ TNOM=27 UTE=-1.5 KT1=-0.11 KT2=0.022 UA1=4.31e-9
+ CAPMOD=2 XPART=0.5
+ )
"""


class NetlistGenerator:
    """Generates complete simulation netlists dynamically for various simulators."""

    def __init__(self, output_dir: Union[str, Path] = "results/netlists"):
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_ngspice_netlists(
        self,
        model_file: Path,
        dut: DeviceSpec,
        pmos_dut: Optional[DeviceSpec] = None,
    ) -> Dict[str, Path]:
        """Generate all 5 ngspice benchmark netlists dynamically.

        Args:
            model_file: Path to SPICE model file to include.
            dut: Active DeviceSpec (NMOS or PMOS under test).
            pmos_dut: Optional complementary PMOS device for CMOS switching tests.

        Returns:
            Dict mapping mode name ('dc', 'ac', 'transient', 'noise', 'gummel') to file Path.
        """
        model_inc = model_file.resolve().as_posix()
        vdd = dut.default_vdd
        l_val = dut.default_l
        w_val = dut.default_w

        netlists = {}

        # -------------------------------------------------------------
        # 1. DC Analysis Netlist (dc_circuit.cir)
        # -------------------------------------------------------------
        dc_m1 = dut.format_instance("1", "drain_iv", "gate_iv", "source_iv", "bulk_iv", l=l_val, w=w_val)
        dc_m2 = dut.format_instance("2", "drain_bias", "gate_bias", "source_bias", "bulk_bias", l=l_val, w=w_val)

        dc_content = f"""* Automated MOSFET DC Benchmark
.option temp=27 tnom=27
.option gmin=1e-15 reltol=1e-4 abstol=1e-12 chgtol=1e-15 method=gear

.inc '{model_inc}'

* Device under test for IV characteristics
{dc_m1}

* Device under test for bias point analysis
{dc_m2}

* IV Characteristics Circuit Sources
Vds_iv drain_iv 0 DC 0
Vgs_iv gate_iv 0 DC 0
Vs_iv source_iv 0 DC 0
Vb_iv bulk_iv 0 DC 0

* Bias Point Analysis Circuit Sources
Vds_bias drain_bias 0 DC 0
Vgs_bias gate_bias 0 DC 0
Vs_bias source_bias 0 DC 0
Vb_bias bulk_bias 0 DC 0

.control
set filetype=ascii
set wr_vecnames
set wr_singlescale
set wr_singleprecision
set wr_formatted

* Run DC analysis with temperature sweeps
echo "Starting temperature sweep"

* Temperature -40°C
option temp=-40
dc Vds_iv 0 {vdd} 0.01 Vgs_iv 0 {vdd} {vdd/6:.3f}
let id = i(Vds_iv)
let is = i(Vs_iv)
let ig = i(Vgs_iv)
let ib = i(Vb_iv)
let kcl = abs(id + is + ig + ib)
wrdata ./iv_data_-40.txt v(drain_iv) v(gate_iv) id is ib ig kcl

* Temperature 0°C
option temp=0
dc Vds_iv 0 {vdd} 0.01 Vgs_iv 0 {vdd} {vdd/6:.3f}
let id = i(Vds_iv)
let is = i(Vs_iv)
let ig = i(Vgs_iv)
let ib = i(Vb_iv)
let kcl = abs(id + is + ig + ib)
wrdata ./iv_data_0.txt v(drain_iv) v(gate_iv) id is ib ig kcl

* Temperature 25°C
option temp=25
dc Vds_iv 0 {vdd} 0.01 Vgs_iv 0 {vdd} {vdd/6:.3f}
let id = i(Vds_iv)
let is = i(Vs_iv)
let ig = i(Vgs_iv)
let ib = i(Vb_iv)
let kcl = abs(id + is + ig + ib)
wrdata ./iv_data_25.txt v(drain_iv) v(gate_iv) id is ib ig kcl

* Temperature 50°C
option temp=50
dc Vds_iv 0 {vdd} 0.01 Vgs_iv 0 {vdd} {vdd/6:.3f}
let id = i(Vds_iv)
let is = i(Vs_iv)
let ig = i(Vgs_iv)
let ib = i(Vb_iv)
let kcl = abs(id + is + ig + ib)
wrdata ./iv_data_50.txt v(drain_iv) v(gate_iv) id is ib ig kcl

* Temperature 100°C
option temp=100
dc Vds_iv 0 {vdd} 0.01 Vgs_iv 0 {vdd} {vdd/6:.3f}
let id = i(Vds_iv)
let is = i(Vs_iv)
let ig = i(Vgs_iv)
let ib = i(Vb_iv)
let kcl = abs(id + is + ig + ib)
wrdata ./iv_data_100.txt v(drain_iv) v(gate_iv) id is ib ig kcl

* Temperature 150°C
option temp=150
dc Vds_iv 0 {vdd} 0.01 Vgs_iv 0 {vdd} {vdd/6:.3f}
let id = i(Vds_iv)
let is = i(Vs_iv)
let ig = i(Vgs_iv)
let ib = i(Vb_iv)
let kcl = abs(id + is + ig + ib)
wrdata ./iv_data_150.txt v(drain_iv) v(gate_iv) id is ib ig kcl

* Reset to 27C for bias point table
option temp=27
"""
        # Append 9 bias point evaluation loops
        bias_steps = [
            (0.0, 0.0), (0.0, vdd*0.5), (0.0, vdd),
            (vdd*0.5, 0.0), (vdd*0.5, vdd*0.5), (vdd*0.5, vdd),
            (vdd, 0.0), (vdd, vdd*0.5), (vdd, vdd)
        ]
        for vds_b, vgs_b in bias_steps:
            dc_content += f"""
alter Vds_bias = {vds_b:.3f}
alter Vgs_bias = {vgs_b:.3f}
op
let id_bias = i(Vds_bias)
let is_bias = i(Vs_bias)
let ig_bias = i(Vgs_bias)
let ib_bias = i(Vb_bias)
echo "$&v(drain_bias) $&v(gate_bias) $&id_bias $&ig_bias $&is_bias $&ib_bias" >> ./bias_point_data.txt
"""
        dc_content += """
echo "DC analysis completed"
quit
.endc
.end
"""
        dc_path = self.output_dir / "dc_circuit.cir"
        dc_path.write_text(dc_content)
        netlists["dc"] = dc_path

        # -------------------------------------------------------------
        # 2. AC Analysis Netlist (ac_circuit.cir)
        # -------------------------------------------------------------
        ac_m1 = dut.format_instance("1", "drain_1", "gate_1", "source_1", "bulk_1", l=l_val, w=w_val)
        ac_m2 = dut.format_instance("2", "drain_2", "gate_2", "0", "0", l=l_val, w=w_val)
        ac_m3 = dut.format_instance("3", "drain_3", "gate_3", "source_3", "bulk_3", l=l_val, w=w_val)

        ac_content = f"""* Automated MOSFET AC Benchmark
.option temp=27 tnom=27 gmin=1e-15
.inc '{model_inc}'

* CV test device
{ac_m1}
VG gate_1 0 DC 0 AC 1
VD drain_1 0 DC {vdd*0.8:.3f} AC 0
VS source_1 0 DC 0 AC 0
VB bulk_1 0 DC 0 AC 0

* S-parameter test device
{ac_m2}
RG gate_2 gate_in2 50
RD drain_2 drain_in2 50
VGS gate_in2 0 DC {vdd*0.8:.3f} AC 0
VDS drain_in2 0 DC {vdd} AC 0

* Charge conservation test device
{ac_m3}
VGQ gate_3 0 DC 0 PWL(0 0 1n 0 1.01n {vdd} 5n {vdd})
VDQ drain_3 0 DC {vdd}
VSQ source_3 0 DC 0
VBQ bulk_3 0 DC 0

.control
shell mkdir -p .
set filetype=ascii
set wr_vecnames=yes
set wr_singlescale=yes
set numdgt=10

* ----------------------------------------------------------
* CV Analysis
* ----------------------------------------------------------
let vg_start = -{vdd*0.8:.3f}
let vg_stop = {vdd}
let vg_step = 0.05
let num_points = floor((vg_stop - vg_start)/vg_step) + 1

echo "Vg Cgg_1kHz Cgg_10kHz Cgg_100kHz Cgg_1MHz Cgb_1MHz Cgs_1MHz Cgd_1MHz" > cv_data.txt
echo "Vg Cgg Cdg Csg Cbg Cgd Cdd Csd Cbd Cgs Cds Css Cbs Cgb Cdb Csb Cbb" > cmatrix_data.txt

let idx = 0
while idx < num_points
    let vg_bias = vg_start + idx * vg_step
    alter VG = vg_bias

    ac lin 1 1k 1k
    let cgg_val_1k = -imag(i(VG))/(2*3.14159*1e3)
    set cgg_1k_s = $&cgg_val_1k

    ac lin 1 10k 10k
    let cgg_val_10k = -imag(i(VG))/(2*3.14159*1e4)
    set cgg_10k_s = $&cgg_val_10k

    ac lin 1 100k 100k
    let cgg_val_100k = -imag(i(VG))/(2*3.14159*1e5)
    set cgg_100k_s = $&cgg_val_100k

    ac lin 1 1meg 1meg
    let cgg_val_1m = -imag(i(VG))/(2*3.14159*1e6)
    let cgb_val_1m = -imag(i(VB))/(2*3.14159*1e6)
    let cgs_val_1m = -imag(i(VS))/(2*3.14159*1e6)
    let cgd_val_1m = -imag(i(VD))/(2*3.14159*1e6)
    set cgg_1m_s = $&cgg_val_1m
    set cgb_1m_s = $&cgb_val_1m
    set cgs_1m_s = $&cgs_val_1m
    set cgd_1m_s = $&cgd_val_1m

    echo "$&vg_bias $cgg_1k_s $cgg_10k_s $cgg_100k_s $cgg_1m_s $cgb_1m_s $cgs_1m_s $cgd_1m_s" >> cv_data.txt

    * 4x4 small-signal matrix
    alter @VG[acmag] = 1
    alter @VD[acmag] = 0
    alter @VS[acmag] = 0
    alter @VB[acmag] = 0
    ac lin 1 1meg 1meg
    let cgg_m = -imag(i(VG))/(2*3.14159*1e6)
    let cdg_m = -imag(i(VD))/(2*3.14159*1e6)
    let csg_m = -imag(i(VS))/(2*3.14159*1e6)
    let cbg_m = -imag(i(VB))/(2*3.14159*1e6)
    set cgg_s = $&cgg_m
    set cdg_s = $&cdg_m
    set csg_s = $&csg_m
    set cbg_s = $&cbg_m

    alter @VG[acmag] = 0
    alter @VD[acmag] = 1
    alter @VS[acmag] = 0
    alter @VB[acmag] = 0
    ac lin 1 1meg 1meg
    let cgd_m = -imag(i(VG))/(2*3.14159*1e6)
    let cdd_m = -imag(i(VD))/(2*3.14159*1e6)
    let csd_m = -imag(i(VS))/(2*3.14159*1e6)
    let cbd_m = -imag(i(VB))/(2*3.14159*1e6)
    set cgd_s = $&cgd_m
    set cdd_s = $&cdd_m
    set csd_s = $&csd_m
    set cbd_s = $&cbd_m

    alter @VG[acmag] = 0
    alter @VD[acmag] = 0
    alter @VS[acmag] = 1
    alter @VB[acmag] = 0
    ac lin 1 1meg 1meg
    let cgs_m = -imag(i(VG))/(2*3.14159*1e6)
    let cds_m = -imag(i(VD))/(2*3.14159*1e6)
    let css_m = -imag(i(VS))/(2*3.14159*1e6)
    let cbs_m = -imag(i(VB))/(2*3.14159*1e6)
    set cgs_s = $&cgs_m
    set cds_s = $&cds_m
    set css_s = $&css_m
    set cbs_s = $&cbs_m

    alter @VG[acmag] = 0
    alter @VD[acmag] = 0
    alter @VS[acmag] = 0
    alter @VB[acmag] = 1
    ac lin 1 1meg 1meg
    let cgb_m = -imag(i(VG))/(2*3.14159*1e6)
    let cdb_m = -imag(i(VD))/(2*3.14159*1e6)
    let csb_m = -imag(i(VS))/(2*3.14159*1e6)
    let cbb_m = -imag(i(VB))/(2*3.14159*1e6)
    set cgb_s = $&cgb_m
    set cdb_s = $&cdb_m
    set csb_s = $&csb_m
    set cbb_s = $&cbb_m

    alter @VG[acmag] = 1
    alter @VD[acmag] = 0
    alter @VS[acmag] = 0
    alter @VB[acmag] = 0

    echo "$&vg_bias $cgg_s $cdg_s $csg_s $cbg_s $cgd_s $cdd_s $csd_s $cbd_s $cgs_s $cds_s $css_s $cbs_s $cgb_s $cdb_s $csb_s $cbb_s" >> cmatrix_data.txt
    let idx = idx + 1
end

* ----------------------------------------------------------
* S-parameters
* ----------------------------------------------------------
alter VGS = {vdd*0.8:.3f}
alter VDS = {vdd}
echo "# S-parameter analysis" > sparams_data.txt
echo "# freq s11_mag s11_phase s12_mag s12_phase s21_mag s21_phase s22_mag s22_phase" >> sparams_data.txt

foreach freq 1e6 1e7 1e8 1e9
    destroy all
    alter @VGS[acmag]=1
    alter @VDS[acmag]=0
    ac lin 1 $freq $freq
    let y11 = (-i(VGS)) / v(gate_in2)
    let y21 = (-i(VDS)) / v(gate_in2)

    alter @VGS[acmag]=0
    alter @VDS[acmag]=1
    ac lin 1 $freq $freq
    let y12 = (-i(VGS)) / v(drain_in2)
    let y22 = (-i(VDS)) / v(drain_in2)

    let a11 = 1 + 50*ac1.y11
    let a12 = 50*y12
    let a21 = 50*ac1.y21
    let a22 = 1 + 50*y22
    let b11 = 1 - 50*ac1.y11
    let b12 = -50*y12
    let b21 = -50*ac1.y21
    let b22 = 1 - 50*y22
    let detA = a11*a22 - a12*a21

    let s11 = (b11*a22 - b12*a21) / detA
    let s12 = (-b11*a12 + b12*a11) / detA
    let s21 = (b21*a22 - b22*a21) / detA
    let s22 = (-b21*a12 + b22*a11) / detA

    let s11_m = abs(s11)
    let s11_p = 180/3.141592653589793*ph(s11)
    let s12_m = abs(s12)
    let s12_p = 180/3.141592653589793*ph(s12)
    let s21_m = abs(s21)
    let s21_p = 180/3.141592653589793*ph(s21)
    let s22_m = abs(s22)
    let s22_p = 180/3.141592653589793*ph(s22)

    echo "$freq $&s11_m $&s11_p $&s12_m $&s12_p $&s21_m $&s21_p $&s22_m $&s22_p" >> sparams_data.txt
end

* ----------------------------------------------------------
* NQS Effects
* ----------------------------------------------------------
echo "# Non-quasi-static effects analysis - phase shifts" > nqs_effects.txt
echo "# freq vg_phase id_phase phase_diff" >> nqs_effects.txt

alter VG = {vdd*0.8:.3f}
alter VD = {vdd}

foreach fq 1e7 1e8 1e9 1e10
    ac lin 1 $fq $fq
    let vg_phase = 180/3.14159*ph(v(gate_1))
    let id_phase = 180/3.14159*ph(i(VD))
    let phase_diff = vg_phase - id_phase
    echo "$fq $&vg_phase $&id_phase $&phase_diff" >> nqs_effects.txt
end

* ----------------------------------------------------------
* Charge Conservation Test
* ----------------------------------------------------------
tran 0.01n 5n
write charge_conservation.txt time v(gate_3) i(VGQ) i(VDQ) i(VSQ) i(VBQ)

quit
.endc
.end
"""
        ac_path = self.output_dir / "ac_circuit.cir"
        ac_path.write_text(ac_content)
        netlists["ac"] = ac_path

        # -------------------------------------------------------------
        # 3. Transient Analysis Netlist (transient_circuit.cir)
        # -------------------------------------------------------------
        # For CMOS inverter and delay ring:
        # If complementary PMOS is provided, use it; otherwise use synthetic PMOS model card
        pmos_decl = ""
        if pmos_dut is not None:
            inv_p = pmos_dut.format_instance("inv_p", "out_inv", "in_inv", "vdd_inv", "vdd_inv", l=pmos_dut.default_l, w=pmos_dut.default_w)
            d1_p = pmos_dut.format_instance("d1_p", "mid1_delay", "in_delay", "vdd_delay", "vdd_delay", l=pmos_dut.default_l, w=pmos_dut.default_w)
            d2_p = pmos_dut.format_instance("d2_p", "mid2_delay", "mid1_delay", "vdd_delay", "vdd_delay", l=pmos_dut.default_l, w=pmos_dut.default_w)
            d3_p = pmos_dut.format_instance("d3_p", "out_delay", "mid2_delay", "vdd_delay", "vdd_delay", l=pmos_dut.default_l, w=pmos_dut.default_w)
            p1_p = pmos_dut.format_instance("p1_p", "out_power", "in_power", "vdd_power", "vdd_power", l=pmos_dut.default_l, w=pmos_dut.default_w)
        else:
            pmos_decl = SYNTHETIC_PMOS_CARD
            inv_p = f"M_inv_p out_inv in_inv vdd_inv vdd_inv PMOS_AUTO L={l_val:.3e} W={w_val*2:.3e}"
            d1_p = f"M_d1_p mid1_delay in_delay vdd_delay vdd_delay PMOS_AUTO L={l_val:.3e} W={w_val*2:.3e}"
            d2_p = f"M_d2_p mid2_delay mid1_delay vdd_delay vdd_delay PMOS_AUTO L={l_val:.3e} W={w_val*2:.3e}"
            d3_p = f"M_d3_p out_delay mid2_delay vdd_delay vdd_delay PMOS_AUTO L={l_val:.3e} W={w_val*2:.3e}"
            p1_p = f"M_p1_p out_power in_power vdd_power vdd_power PMOS_AUTO L={l_val:.3e} W={w_val*2:.3e}"

        tran_m = dut.format_instance("tran", "drain_tran", "gate_tran", "source_tran", "bulk_tran", l=l_val, w=w_val)
        inv_n = dut.format_instance("inv_n", "out_inv", "in_inv", "0", "0", l=l_val, w=w_val)
        d1_n = dut.format_instance("d1_n", "mid1_delay", "in_delay", "0", "0", l=l_val, w=w_val)
        d2_n = dut.format_instance("d2_n", "mid2_delay", "mid1_delay", "0", "0", l=l_val, w=w_val)
        d3_n = dut.format_instance("d3_n", "out_delay", "mid2_delay", "0", "0", l=l_val, w=w_val)
        p1_n = dut.format_instance("p1_n", "out_power", "in_power", "0", "0", l=l_val, w=w_val)
        qs_m = dut.format_instance("qs", "drain_qs", "gate_qs", "0", "0", l=l_val, w=w_val)
        charge_m = dut.format_instance("charge", "drain_charge", "gate_charge", "source_charge", "bulk_charge", l=l_val, w=w_val)

        tran_content = f"""* Automated MOSFET Transient Benchmark
.option temp=27 tnom=27 gmin=1e-15 reltol=1e-4 method=gear
.inc '{model_inc}'
{pmos_decl}

* 1. Large Signal Transient Circuit
{tran_m}
Vgs_tran gate_tran 0 PULSE(0 {vdd} 0n 0.1n 0.1n 10n 20n)
Vds_tran drain_tran 0 DC {vdd}
Vs_tran source_tran 0 DC 0
Vb_tran bulk_tran 0 DC 0
Cload drain_tran 0 1f

* 2. Inverter Switching Circuit
{inv_n}
{inv_p}
Vdd_inv vdd_inv 0 DC {vdd}
Vin_inv in_inv 0 PULSE(0 {vdd} 0n 0.1n 0.1n 10n 20n)
Cload_inv out_inv 0 1f

* 3. 3-Stage Inverter Chain (Delay Effects)
Vdd_delay vdd_delay 0 DC {vdd}
Vin_delay in_delay 0 PULSE(0 {vdd} 0n 0.1n 0.1n 10n 20n)
{d1_n}
{d1_p}
Cload_mid1 mid1_delay 0 1f
{d2_n}
{d2_p}
Cload_mid2 mid2_delay 0 1f
{d3_n}
{d3_p}
Cload_out out_delay 0 1f

* 4. Power Dissipation Circuit
Vdd_power vdd_power 0 DC {vdd}
Vin_power in_power 0 PULSE(0 {vdd} 0n 0.1n 0.1n 10n 20n)
{p1_n}
{p1_p}
Cload_power out_power 0 1f

* 5. Quasi-Static Verification Circuit
{qs_m}
Vgs_qs gate_qs 0 PWL(0 0 100n {vdd} 200n 0)
Vds_qs drain_qs 0 DC {vdd}

* 6. Charge Verification Circuit
{charge_m}
Vgs_charge gate_charge 0 PULSE(0 {vdd} 0n 0.1n 0.1n 10n 20n)
Vds_charge drain_charge 0 DC {vdd}
Vs_charge source_charge 0 DC 0
Vb_charge bulk_charge 0 DC 0

.control
set filetype=ascii
set wr_vecnames
set wr_singlescale

* Large signal transient
tran 0.02n 25n
wrdata ./tran_large_signal.txt time v(gate_tran) v(drain_tran) i(Vds_tran) i(Vgs_tran) i(Vs_tran) i(Vb_tran)

* Inverter switching
tran 0.02n 25n
let power_switching = -v(vdd_inv) * i(Vdd_inv)
wrdata ./tran_switching.txt time v(in_inv) v(out_inv) i(Vdd_inv)
wrdata ./tran_switching_power.txt time power_switching

* Inverter delay chain
tran 0.02n 25n
wrdata ./tran_delay.txt time v(in_delay) v(mid1_delay) v(mid2_delay) v(out_delay)

* Power analysis at 27C
tran 0.02n 25n
let power_diss = -v(vdd_power) * i(Vdd_power)
let energy = integ(power_diss)
wrdata ./tran_power_27C.txt time v(in_power) v(out_power) power_diss energy

* Power analysis at 100C
option temp=100
tran 0.02n 25n
let power_diss = -v(vdd_power) * i(Vdd_power)
let energy = integ(power_diss)
wrdata ./tran_power_100C.txt time v(in_power) v(out_power) power_diss energy
option temp=27

* Quasi-static
tran 0.1n 200n uic
let id_qs = -i(Vds_qs)
wrdata ./tran_quasi_static.txt time v(gate_qs) v(drain_qs) id_qs

* Dynamic charge conservation
tran 0.02n 25n
let ig_charge = -i(Vgs_charge)
let id_charge = -i(Vds_charge)
let is_charge = i(Vs_charge)
let ib_charge = i(Vb_charge)
let i_total = ig_charge + id_charge + is_charge + ib_charge
let qg_approx = integ(ig_charge)
let qd_approx = integ(id_charge)
let qs_approx = integ(is_charge)
let qb_approx = integ(ib_charge)
let q_total = qg_approx + qd_approx + qs_approx + qb_approx
wrdata ./tran_charge.txt time v(gate_charge) ig_charge id_charge is_charge ib_charge i_total qg_approx qd_approx qs_approx qb_approx q_total

quit
.endc
.end
"""
        tran_path = self.output_dir / "transient_circuit.cir"
        tran_path.write_text(tran_content)
        netlists["transient"] = tran_path

        # -------------------------------------------------------------
        # 4. Noise Analysis Netlist (noise_circuit.cir)
        # -------------------------------------------------------------
        noise_m = dut.format_instance("noise", "drain_noise", "gate_noise", "source_noise", "bulk_noise", l=l_val, w=w_val)
        flicker_m = dut.format_instance("flicker", "flicker_drain", "flicker_gate", "flicker_source", "flicker_bulk", l=l_val, w=w_val)
        shot_m = dut.format_instance("shot", "shot_drain", "shot_gate", "shot_source", "shot_bulk", l=l_val, w=w_val)

        noise_content = f"""* Automated MOSFET Noise Benchmark
.option temp=27 tnom=27 gmin=1e-15
.inc '{model_inc}'

* Thermal Noise DUT
Vdd_noise vdd_noise 0 DC {vdd}
Vin_noise in_noise 0 DC {vdd*0.5:.3f} AC 1
Rb_noise in_noise gate_noise 1k
Cb_noise in_noise gate_noise 1u
Rs_noise source_noise 0 100
Rd_noise vdd_noise drain_noise 10k
Vgs_noise gate_noise source_noise DC 0
Vds_noise drain_noise source_noise DC 0
Vbulk_noise bulk_noise 0 DC 0
{noise_m}

* Flicker Noise DUT
Vin_f flicker_in 0 DC 0 AC 1
Rin_f flicker_in flicker_gate 1k
Vbias_f flicker_vdd 0 DC {vdd}
Vgs_flicker flicker_gate_bias 0 DC {vdd*0.5:.3f}
Vgs_inp_f flicker_gate flicker_gate_bias DC 0
Rout_f flicker_drain flicker_vdd 10k
Vbulk_f flicker_bulk 0 DC 0
Vsrc_f flicker_source 0 DC 0
{flicker_m}

* Shot Noise DUT
Vdd_shot shot_vdd 0 DC {vdd} AC 1
Vgs_shot shot_gate 0 DC {vdd*0.75:.3f}
Rload_shot shot_vdd shot_drain 10k
Vbulk_shot shot_bulk 0 DC 0
Vsrc_shot shot_source 0 DC 0
{shot_m}

.control
set filetype=ascii
set wr_vecnames
set wr_singlescale

* Thermal noise sweeps across bias points
"""
        noise_bias_pts = [
            (0.3, 0.3), (0.3, 0.6), (0.3, 0.9), (0.3, min(1.2, vdd)),
            (0.6, 0.3), (0.6, 0.6)
        ]
        for vgs_n, vds_n in noise_bias_pts:
            noise_content += f"""
alter Vgs_noise = {vgs_n}
alter Vds_noise = {vds_n}
noise v(drain_noise) Vin_noise dec 20 1 1G
setplot noise1
let thermal_noise = inoise_spectrum
let freq = frequency
write ./thermal_noise_vgs{vgs_n}_vds{vds_n}.txt freq thermal_noise
"""
        noise_content += f"""
* Flicker noise
alter Vgs_flicker = {vdd*0.5:.3f}
alter Vbias_f = {vdd}
noise v(flicker_drain) Vin_f dec 20 0.1 1MEG
setplot noise1
let flicker_noise = inoise_spectrum
let freq = frequency
write ./flicker_noise.txt freq flicker_noise

* Shot noise
alter Vgs_shot = {vdd*0.75:.3f}
noise v(shot_drain) Vdd_shot dec 20 1 1G
setplot noise1
let shot_noise = inoise_spectrum
let freq = frequency
write ./shot_noise.txt freq shot_noise

* Temperature dependence
foreach t -40 0 27 50 100 150
    option temp = $t
    alter Vgs_noise = 0.6
    alter Vds_noise = 0.6
    noise v(drain_noise) Vin_noise dec 20 1 1G
    setplot noise1
    let temp_noise = inoise_spectrum
    let freq = frequency
    write ./noise_temp$t.txt freq temp_noise
end

quit
.endc
.end
"""
        noise_path = self.output_dir / "noise_circuit.cir"
        noise_path.write_text(noise_content)
        netlists["noise"] = noise_path

        # -------------------------------------------------------------
        # 5. Physics QA Netlist (gummel_circuit.cir)
        # -------------------------------------------------------------
        gst_m = dut.format_instance("gst", "d_gst_int", "g_gst", "s_gst_int", "b_gst", l=l_val, w=w_val)
        zero_m = dut.format_instance("zero", "d_zero", "g_zero", "s_zero", "b_zero", l=l_val, w=w_val)
        ac_m = dut.format_instance("ac", "d_ac_int", "g_ac", "s_ac_int", "b_ac", l=l_val, w=w_val)
        tr_m = dut.format_instance("tr", "d_tr_int", "g_tr", "s_tr", "b_tr", l=l_val, w=w_val)
        out_m = dut.format_instance("out", "d_out_int", "g_out", "s_out", "b_out", l=l_val, w=w_val)
        asymp_m = dut.format_instance("asymp", "d_asymp_int", "g_asymp", "s_asymp", "b_asymp", l=l_val, w=w_val)
        sh_m = dut.format_instance("sh", "d_sh_int", "g_sh", "s_sh", "b_sh", l=l_val, w=w_val)

        gummel_content = f"""* Automated MOSFET Physics QA Benchmark
.option temp=27 tnom=27 gmin=1e-15 reltol=1e-4 method=gear
.inc '{model_inc}'

* Gummel Symmetry Test Setup
V_x vx 0 DC 0
E_d d_gst 0 vx 0 0.5
E_s s_gst 0 vx 0 -0.5
V_g g_gst 0 DC {vdd*0.5:.3f}
V_b b_gst 0 DC 0
Vsens_d d_gst d_gst_int DC 0
Vsens_s s_gst s_gst_int DC 0
{gst_m}

* Zero-Bias Passivity
Vd_zero d_zero 0 DC 0
Vg_zero g_zero 0 DC 0
Vs_zero s_zero 0 DC 0
Vb_zero b_zero 0 DC 0
{zero_m}

* Capacitance Symmetry
V_x_ac vx_ac 0 DC 0
E_d_ac d_ac 0 vx_ac 0 0.5
E_s_ac s_ac 0 vx_ac 0 -0.5
V_g_ac g_ac 0 DC {vdd*0.5:.3f} AC 1
V_b_ac b_ac 0 DC 0
Vsens_d_ac d_ac d_ac_int DC 0
Vsens_s_ac s_ac s_ac_int DC 0
{ac_m}

* Transfer Characteristics Smoothness
Vd_tr d_tr 0 DC {vdd}
Vg_tr g_tr 0 DC 0
Vs_tr s_tr 0 DC 0
Vb_tr b_tr 0 DC 0
Vsens_d_tr d_tr d_tr_int DC 0
{tr_m}

* Output Conductance Smoothness
Vd_out d_out 0 DC 0
Vg_out g_out 0 DC {vdd}
Vs_out s_out 0 DC 0
Vb_out b_out 0 DC 0
Vsens_d_out d_out d_out_int DC 0
{out_m}

* Asymptotic Extrapolation
Vd_asymp d_asymp 0 DC {vdd}
Vg_asymp g_asymp 0 DC 0
Vs_asymp s_asymp 0 DC 0
Vb_asymp b_asymp 0 DC 0
Vsens_d_asymp d_asymp d_asymp_int DC 0
{asymp_m}

* Dynamic Self-Heating / Admittance
Vd_sh d_sh 0 DC {vdd} AC 1
Vg_sh g_sh 0 DC {vdd}
Vs_sh s_sh 0 DC 0
Vb_sh b_sh 0 DC 0
Vsens_d_sh d_sh d_sh_int DC 0
{sh_m}

.control
set filetype=ascii
set wr_vecnames
set wr_singlescale

* Zero bias
op
let id_zero = i(Vd_zero)
let ig_zero = i(Vg_zero)
let is_zero = i(Vs_zero)
let ib_zero = i(Vb_zero)
wrdata ./zero_bias_passivity.txt id_zero ig_zero is_zero ib_zero

* Gummel symmetry test
dc V_x -0.2 0.2 0.001
let vx = v(vx)
let id_gst = -i(Vsens_d)
let is_gst = i(Vsens_s)
let ix = (id_gst + is_gst) / 2
let gx = deriv(ix)
let gxx = deriv(gx)
let gxxx = deriv(gxx)
wrdata ./gummel_symmetry.txt vx ix gx gxx gxxx id_gst is_gst

* Transfer smoothness
dc Vg_tr 0 {vdd} 0.005
let vg_tr = v(g_tr)
let id_tr = -i(Vsens_d_tr)
let gm_tr = deriv(id_tr)
let gm2_tr = deriv(gm_tr)
let gm3_tr = deriv(gm2_tr)
wrdata ./transfer_data.txt vg_tr id_tr gm_tr gm2_tr gm3_tr

* Output conductance smoothness
dc Vd_out 0 {vdd} 0.005
let vd_out = v(d_out)
let id_out = -i(Vsens_d_out)
let gds_out = deriv(id_out)
let gds2_out = deriv(gds_out)
let gds3_out = deriv(gds2_out)
wrdata ./output_conductance.txt vd_out id_out gds_out gds2_out gds3_out

* Asymptotic gate extrapolation
dc Vg_asymp -2.0 2.5 0.01
let vg_asymp = v(g_asymp)
let id_asymp_vg = -i(Vsens_d_asymp)
wrdata ./asymptotic_vg.txt vg_asymp id_asymp_vg

* Asymptotic drain leakage
alter Vg_asymp = -0.5
dc Vd_asymp 0 2.5 0.02
let vd_asymp_leak = v(d_asymp)
let id_asymp_leak = -i(Vsens_d_asymp)
wrdata ./asymptotic_vd_leak.txt vd_asymp_leak id_asymp_leak

* Asymptotic drain on
alter Vg_asymp = {vdd}
dc Vd_asymp 0 2.5 0.02
let vd_asymp_on = v(d_asymp)
let id_asymp_on = -i(Vsens_d_asymp)
wrdata ./asymptotic_vd_on.txt vd_asymp_on id_asymp_on

* Dynamic self heating
ac dec 10 1 100G
let freq_sh = frequency
let y_sh = -i(Vsens_d_sh)
let go_sh = real(y_sh)
let co_sh = imag(y_sh) / (2 * 3.141592653589793 * freq_sh)
wrdata ./self_heating_ac.txt freq_sh go_sh co_sh

* Gummel CV
dc V_x_ac -0.2 0.2 0.005
wrdata ./gummel_cv.txt v(vx_ac)

quit
.endc
.end
"""
        gummel_path = self.output_dir / "gummel_circuit.cir"
        gummel_path.write_text(gummel_content)
        netlists["gummel"] = gummel_path

        return netlists

    def generate_spectre_netlists(
        self,
        model_file: Path,
        dut: DeviceSpec,
        pmos_dut: Optional[DeviceSpec] = None,
    ) -> Dict[str, Path]:
        """Generate Spectre netlists (.scs) on the fly."""
        model_inc = model_file.resolve().as_posix()
        vdd = dut.default_vdd
        l_val = dut.default_l
        w_val = dut.default_w
        mname = dut.name

        pmos_name = pmos_dut.name if pmos_dut else "PMOS_AUTO"
        pmos_decl = "" if pmos_dut else SYNTHETIC_PMOS_CARD

        netlists = {}

        # Spectre DC Netlist
        dc_scs = f"""// Spectre DC IV & Bias Point Benchmark
simulator lang=spice
.option temp=27 tnom=27 gmin=1e-15
.include '{model_inc}'

M1 (drain_iv gate_iv 0 0) {mname} L={l_val:.3e} W={w_val:.3e}
M2 (drain_bias gate_bias 0 0) {mname} L={l_val:.3e} W={w_val:.3e}

Vds_iv (drain_iv 0) vsource dc=0
Vgs_iv (gate_iv 0) vsource dc=0
Vds_bias (drain_bias 0) vsource dc={vdd}
Vgs_bias (gate_bias 0) vsource dc={vdd}

simulator lang=spectre
dc_iv sweep dev=Vds_iv start=0 stop={vdd} step=0.01 {{
    dc_iv_vgs sweep dev=Vgs_iv start=0 stop={vdd} step={vdd/6:.3f} {{
        dc
    }}
}}
bias_op dc
"""
        dc_path = self.output_dir / "dc_circuit.scs"
        dc_path.write_text(dc_scs)
        netlists["dc"] = dc_path

        # Spectre AC Netlist
        ac_scs = f"""// Spectre AC Benchmark
simulator lang=spice
.option temp=27 tnom=27 gmin=1e-15
.include '{model_inc}'

M1 (drain_1 gate_1 0 0) {mname} L={l_val:.3e} W={w_val:.3e}
VG (gate_1 0) vsource dc=0 mag=1
VD (drain_1 0) vsource dc={vdd*0.8:.3f} mag=0

simulator lang=spectre
ac_sweep ac start=1e3 stop=1e9 dec=10
"""
        ac_path = self.output_dir / "ac_circuit.scs"
        ac_path.write_text(ac_scs)
        netlists["ac"] = ac_path

        # Spectre Transient Netlist
        tran_scs = f"""// Spectre Transient Benchmark
simulator lang=spice
.option temp=27 tnom=27 gmin=1e-15
.include '{model_inc}'
{pmos_decl}

M_tran (drain_tran gate_tran 0 0) {mname} L={l_val:.3e} W={w_val:.3e}
Vgs_tran (gate_tran 0) vsource type=pulse val0=0 val1={vdd} period=20n width=10n delay=0 rise=0.1n fall=0.1n
Vds_tran (drain_tran 0) vsource dc={vdd}
Cload (drain_tran 0) capacitor c=1f

M_inv_n (out_inv in_inv 0 0) {mname} L={l_val:.3e} W={w_val:.3e}
M_inv_p (out_inv in_inv vdd_inv vdd_inv) {pmos_name} L={l_val:.3e} W={w_val*2:.3e}
Vdd_inv (vdd_inv 0) vsource dc={vdd}
Vin_inv (in_inv 0) vsource type=pulse val0=0 val1={vdd} period=20n width=10n delay=0 rise=0.1n fall=0.1n
Cload_inv (out_inv 0) capacitor c=1f

simulator lang=spectre
tran_sim tran stop=25n step=0.02n
"""
        tran_path = self.output_dir / "transient_circuit.scs"
        tran_path.write_text(tran_scs)
        netlists["transient"] = tran_path

        # Spectre Noise Netlist
        noise_scs = f"""// Spectre Noise Benchmark
simulator lang=spice
.option temp=27 tnom=27 gmin=1e-15
.include '{model_inc}'

M_noise (drain_noise gate_noise 0 0) {mname} L={l_val:.3e} W={w_val:.3e}
Vdd_n (vdd_n 0) vsource dc={vdd}
Vin_n (in_n 0) vsource dc={vdd*0.5:.3f} mag=1
Rb_n (in_n gate_noise) resistor r=1k
Rd_n (vdd_n drain_noise) resistor r=10k

simulator lang=spectre
noise_sim noise start=1 stop=1e9 dec=20 oprobe=Rd_n iprobe=Vin_n
"""
        noise_path = self.output_dir / "noise_circuit.scs"
        noise_path.write_text(noise_scs)
        netlists["noise"] = noise_path

        # Spectre Auxiliary SP Netlist
        sp_scs = f"""// Spectre S-parameter Auxiliary Netlist
simulator lang=spice
.option temp=27 tnom=27 gmin=1e-15
.include '{model_inc}'

M1 (d g 0 0) {mname} L={l_val:.3e} W={w_val:.3e}
P1 (g 0) port r=50 dc={vdd*0.8:.3f} num=1
P2 (d 0) port r=50 dc={vdd} num=2

simulator lang=spectre
sp_sim sp start=1e6 stop=10e9 dec=20 ports=[P1 P2]
"""
        sp_path = self.output_dir / "_sp.scs"
        sp_path.write_text(sp_scs)
        netlists["_sp"] = sp_path

        # Spectre Auxiliary NQS Netlist
        nqs_scs = f"""// Spectre NQS Auxiliary Netlist
simulator lang=spice
.option temp=27 tnom=27 gmin=1e-15
.include '{model_inc}'

M1 (d g 0 0) {mname} L={l_val:.3e} W={w_val:.3e}
Vgs (g 0) vsource dc={vdd*0.8:.3f} mag=1
Vds (d 0) vsource dc={vdd} mag=0

simulator lang=spectre
nqs_sim ac start=1e7 stop=10e9 dec=10
"""
        nqs_path = self.output_dir / "_nqs.scs"
        nqs_path.write_text(nqs_scs)
        netlists["_nqs"] = nqs_path

        return netlists
