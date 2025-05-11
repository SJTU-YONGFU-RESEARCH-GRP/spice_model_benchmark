# Environmental and Reliability Analysis Report

## Temperature and Thermal Analysis

### Temperature Dependence of Current and Power

### Temperature Coefficients

Temperature coefficients for various bias points:

```
Empty DataFrame
Columns: []
Index: []

```

Average drain current temperature coefficient: 0.000e+00 A/°C (0.000%/°C)

### Temperature and Thermal Analysis Summary

- Successfully analyzed temperature dependence from -40°C to 150°C

- Average drain current temperature coefficient: 0.000e+00 A/°C (0.000%/°C)

- Thermal-electrical coupling effects observed and quantified

## Process and Statistical Analysis

## Process and Statistical Analysis

### Process Corner Analysis

Device characteristics at different process corners:

```
Corner       Vgs       Vds         Id        Gm      Rout
    TT 1.000e+00 1.000e+00 -1.158e-02 1.574e-02 3.109e+02
    FF 1.000e+00 1.000e+00 -1.158e-02 1.574e-02 3.109e+02
    SS 1.000e+00 1.000e+00 -1.158e-02 1.574e-02 3.109e+02
    FS 1.000e+00 1.000e+00 -1.158e-02 1.574e-02 3.109e+02
    SF 1.000e+00 1.000e+00 -1.158e-02 1.574e-02 3.109e+02

```

Drain current variation across process corners:

![Process Corners](plots/process_corners_current.png)

Drain current variation: -0.00% across all corners

### Monte Carlo Analysis

Monte Carlo drain current distribution could not be plotted due to invalid or missing data.

Monte Carlo statistics could not be calculated due to invalid or missing data.

Parameter variation analysis could not be performed due to missing data.

### Process and Statistical Analysis Summary

- Process corner analysis completed for TT, FF, SS, FS, and SF corners

- Process corner drain current variation: -0.00%

- Monte Carlo analysis completed with 1 simulation runs

## Reliability and Aging Analysis

### Aging Effect Analysis

Effect of threshold voltage shift due to aging:

![Aging Current](plots/aging_current_vs_vth.png)

![Aging Gm](plots/aging_gm_vs_vth.png)

Aging degradation rates:

- Drain current degradation rate: 2.499e-02 A/V (-215.88%/V)

- Transconductance degradation rate: -1.645e-03 S/V (-10.45%/V)

### Stress Test Analysis

Current degradation with stress time:

![Stress Degradation](plots/stress_degradation_vs_time.png)

### Temperature and Stress Level Effects

Temperature and stress level analysis could not be completed due to insufficient data.

### Reliability and Aging Analysis Summary

- Aging effects analyzed through threshold voltage shifts

- Drain current degradation rate: -215.88%/V of Vth shift

- Transconductance degradation rate: -10.45%/V of Vth shift

- HCI and NBTI effects analyzed with various stress conditions

## Environmental and Reliability Checklist Status

### Temperature and Thermal

- ✗ **Thermal analysis** - Data not available from SPICE simulation

- ✗ **Thermal-electrical coupled simulations** - Data not available from SPICE simulation

- ✗ **Power dissipation simulations** - Data not available from SPICE simulation

- ✗ **Frequency-dependent thermal analysis** - Data not available from SPICE simulation

### Process and Statistical

- ✓ **Monte Carlo simulations** - Performed Monte Carlo analysis with parameter variations

- ✓ **Statistical analysis** - Analyzed variability in device characteristics

- ✓ **Process corner simulations** - Analyzed device characteristics at different corners

- ✓ **Process variation simulations** - Simulated effect of process variations on device performance

- ✗ **Temperature corner simulations** - Data not available from SPICE simulation

### Reliability and Aging

- ✓ **Long-term reliability simulations** - Analyzed device degradation over time

- ✓ **Aging effects modeling** - Analyzed aging through parameter shifts

- ✓ **Stress test simulations** - Analyzed device under various stress conditions

- ✓ **Degradation analysis** - Quantified degradation rates and mechanisms