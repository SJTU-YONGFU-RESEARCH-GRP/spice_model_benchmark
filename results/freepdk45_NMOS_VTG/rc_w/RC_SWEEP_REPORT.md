# RC Extraction Sweep (MVP)

Model file: `/data1/duhaochen/spice_model_benchmark/models/FreePDK45/tran_models/models_nom/NMOS_VTG.inc`
Device: `NMOS_VTG` (style: `model`)
Bias: VDS=0.6, VGS_step=1.2, TEMP=27
Rdrive=1k
Sweep mode: `w`

## Sweep points
| W | L | tau (s) | Ceff (F) | Ids_final (A) | R_equiv (ohm) |
|---|---|--------:|---------:|-------------:|--------------:|
| 1u | 0.045u | 1.67463e-12 | 1.67463e-15 | 0.00130266 | 460.595 |
| 2u | 0.045u | 2.78479e-12 | 2.78479e-15 | 0.00261376 | 229.554 |
| 5u | 0.045u | 6.15379e-12 | 6.15379e-15 | 0.00654665 | 91.6499 |
| 10u | 0.045u | 1.1723e-11 | 1.1723e-14 | 0.0131002 | 45.8008 |

## Artifacts
- `rc_sweep_results.json`
- Per-run netlists/logs under `/data1/duhaochen/spice_model_benchmark/results/freepdk45_NMOS_VTG/rc_w/runs`