# Geometry Scaling Check (MVP)

Model file: `/data1/duhaochen/spice_model_benchmark/models/FreePDK45/tran_models/models_nom/NMOS_VTG.inc`
Device: `NMOS_VTG` (style: `model`)
Bias: VDS=0.6, VGS=1.2, TEMP=27

## Checks
- Ids monotonic increasing with W: `True`
- Ids monotonic decreasing with L: `True`
- Ids near-linear with W (max/min(Id/W) <= 1.5): `True`
  - min(Id/W)=1302.69, max(Id/W)=1310.31

## W sweep (fixed L)
| W | L | Ids (A) |
|---|---|---------|
| 1u | 0.045u | 0.00130269 |
| 2u | 0.045u | 0.00261387 |
| 5u | 0.045u | 0.00654737 |
| 10u | 0.045u | 0.0131031 |

## L sweep (fixed W)
| W | L | Ids (A) |
|---|---|---------|
| 10u | 0.045u | 0.0131031 |
| 10u | 0.06u | 0.00998091 |
| 10u | 0.09u | 0.00715201 |
| 10u | 0.18u | 0.00390883 |

## Artifacts
- `geometry_results.json`
- Per-run netlists/logs under `/data1/duhaochen/spice_model_benchmark/results/freepdk45_NMOS_VTG/geometry/runs`

## Vth/DIBL/SS vs L (MVP)
- Vth_low monotonic increasing with L: `True`
- DIBL monotonic decreasing with L: `True`
- SS monotonic decreasing with L: `False`
- DIBL non-negative: `True`

| W | L | VDS_low | VDS_high | Vth_low (V) | Vth_high (V) | DIBL (V/V) | SS (mV/dec) |
|---|---|---------|----------|------------:|-------------:|-----------:|------------:|
| 10u | 0.045u | 0.05 | 0.6 | 0.280222 | 0.198072 | 0.149364 | 83.7807 |
| 10u | 0.06u | 0.05 | 0.6 | 0.297906 | 0.27014 | 0.0504838 | 83.6908 |
| 10u | 0.09u | 0.05 | 0.6 | 0.309683 | 0.295605 | 0.0255962 | 84.1457 |
| 10u | 0.18u | 0.05 | 0.6 | 0.319075 | 0.309719 | 0.0170105 | 84.5922 |

## gm/gds vs W/L (MVP)
- gm positive: `True`
- gds non-negative: `True`
- gm near-linear with W: `True`
  - min(gm/W)=1358.9999999999957, max(gm/W)=1365.5000000000005

### W sweep (fixed L)
| W | L | gm (S) | gds (S) |
|---|---|--------:|---------:|
| 1u | 0.045u | 0.001359 | 0.000503 |
| 2u | 0.045u | 0.0027255 | 0.001011 |
| 5u | 0.045u | 0.006825 | 0.002535 |
| 10u | 0.045u | 0.013655 | 0.005075 |

### L sweep (fixed W)
| W | L | gm (S) | gds (S) |
|---|---|--------:|---------:|
| 10u | 0.045u | 0.013655 | 0.005075 |
| 10u | 0.06u | 0.0119355 | 0.002668 |
| 10u | 0.09u | 0.009216 | 0.001791 |
| 10u | 0.18u | 0.005329 | 0.001104 |