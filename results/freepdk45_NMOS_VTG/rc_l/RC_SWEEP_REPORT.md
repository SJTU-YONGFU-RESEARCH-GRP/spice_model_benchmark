# RC Extraction Sweep (MVP)

Model file: `/data1/duhaochen/spice_model_benchmark/models/FreePDK45/tran_models/models_nom/NMOS_VTG.inc`
Device: `NMOS_VTG` (style: `model`)
Bias: VDS=0.6, VGS_step=1.2, TEMP=27
Rdrive=1k
Sweep mode: `l`

## Sweep points
| W | L | tau (s) | Ceff (F) | Ids_final (A) | R_equiv (ohm) |
|---|---|--------:|---------:|-------------:|--------------:|
| 10u | 0.045u | 1.1723e-11 | 1.1723e-14 | 0.0131002 | 45.8008 |
| 10u | 0.06u | 1.36361e-11 | 1.36361e-14 | 0.00997805 | 60.132 |
| 10u | 0.09u | 1.76096e-11 | 1.76096e-14 | 0.00714842 | 83.9346 |
| 10u | 0.18u | 2.93558e-11 | 2.93558e-14 | 0.00390411 | 153.684 |

## Artifacts
- `rc_sweep_results.json`
- Per-run netlists/logs under `/data1/duhaochen/spice_model_benchmark/results/freepdk45_NMOS_VTG/rc_l/runs`