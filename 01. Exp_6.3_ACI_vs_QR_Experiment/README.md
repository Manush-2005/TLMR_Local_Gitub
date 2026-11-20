# ACI vs Quantile Regression (Paper Sec. 6.3)

Compares Adaptive Conformal Inference (ACI) with a plain Quantile Regression baseline (`Normal_QR`) on nine energy datasets using an LSTM forecaster. Local and global calibration metrics are reported to check whether ACI improves local calibration under the distribution shifts common in energy forecasting.

Corresponds to **Section 6.3, Table 4 and Figure 3** of the paper.

## Files

- `Exp_6.3_final.ipynb`: main notebook. Trains QR and ACI on all 9 datasets and computes all metrics.
- `Final_Results.txt`: aggregated numerical output of the notebook run.
- `results_all_methods_all_datasets.csv`: per-method, per-dataset metric table.
- `Helper_Scripts/`
  - `calculate_metrics.py`: LPIA, LPICE, MLPICP, LMPIW, LCWC, PICP, MPIW.
  - `loss_functions.py`: pinball loss for quantile training.
  - `models.py`, `models_TLMR.py`: LSTM architecture definitions.
  - `preprocessing.py`: sliding-window construction, train/calibration split, normalization.
- `trajectories/LSTM/`: per-dataset CSVs of the online trajectories for each method. Columns: `step`, `alphaTrajectory`, `errSeq`, `y_u_pred`, `y_l_pred`, `y_true`.

## Run

```bash
jupyter notebook Exp_6.3_final.ipynb
```

Run all cells. Trajectory CSVs are written to `trajectories/LSTM/` and the aggregated results to `Final_Results.txt`.

## Experimental Setup

| Parameter | Value |
|---|---|
| Architecture | LSTM (hidden dim 64, 2 layers, dropout 0.1, Linear(64, 1) head) |
| Loss | Pinball loss at quantiles α/2 and 1 − α/2 |
| Initial training window (T_init) | 5,000 samples |
| Initial epochs | 200 |
| Online fine-tuning | 1 epoch every 6 steps (6 hours) |
| Train/calibration split | 0.5 |
| Sequence length | 48 |
| Target coverage (1 − α) | 0.90 (α = 0.1) |
| Local evaluation window (w) | 24 hours |
| ACI step size (γ) | 0.001 |
| Optimizer / learning rate | Adam / 0.001 |
| Batch size | 32 |
| Random seed | 42 |

ACI uses the CQR nonconformity score (Romano et al., 2019) at the adaptively updated level α_i, with the update α_{i+1} = α_i + γ(α − err_i).

## Metrics

- **Local:** LPIA (fraction of 24-hour windows meeting target coverage, higher is better), LPICE (average local coverage error, lower is better), LMPIW (local interval width).
- **Global:** PICP, MPIW.

The notebook also computes MLPICP and LCWC; the paper table reports the subset below.

## Results (Table 4 of the paper)

LSTM, target coverage 1 − α = 0.90.

| Dataset | Method | LPIA ↑ | LPICE ↓ | LMPIW | PICP | MPIW |
|---|---|---|---|---|---|---|
| 50Hertz | Normal_QR | 0.16 | 0.16 | 31.46 | 0.75 | 31.48 |
| 50Hertz | ACI | **0.67** | **0.04** | 49.10 | 0.90 | 49.12 |
| TransnetBW | Normal_QR | **0.71** | **0.02** | 12.23 | 0.92 | 12.22 |
| TransnetBW | ACI | 0.62 | 0.03 | 11.82 | 0.90 | 11.81 |
| TenneTTSO | Normal_QR | 0.22 | 0.12 | 28.87 | 0.79 | 28.85 |
| TenneTTSO | ACI | **0.62** | **0.04** | 39.99 | 0.90 | 39.99 |
| Amprion | Normal_QR | 0.30 | 0.12 | 21.78 | 0.79 | 21.79 |
| Amprion | ACI | **0.68** | **0.04** | 32.03 | 0.91 | 32.05 |
| Location 1 | Normal_QR | **0.66** | **0.04** | 0.03 | 0.89 | 0.03 |
| Location 1 | ACI | 0.62 | **0.04** | 0.03 | 0.90 | 0.03 |
| Location 2 | Normal_QR | **0.74** | **0.03** | 0.03 | 0.92 | 0.03 |
| Location 2 | ACI | 0.65 | **0.03** | 0.03 | 0.90 | 0.03 |
| Hydropower | Normal_QR | 0.35 | 0.30 | 116.75 | 0.62 | 115.66 |
| Hydropower | ACI | **0.64** | **0.06** | 184.77 | 0.88 | 184.92 |
| Solar Plant 1 | Normal_QR | 0.24 | 0.33 | 225.69 | 0.59 | 225.72 |
| Solar Plant 1 | ACI | **0.62** | **0.07** | 1442.91 | 0.88 | 1442.47 |
| Solar Plant 2 | Normal_QR | 0.11 | 0.47 | 1451.34 | 0.43 | 1454.35 |
| Solar Plant 2 | ACI | **0.48** | **0.05** | 5350.74 | 0.88 | 5359.85 |

## Summary

- ACI brings global coverage (PICP) close to the 0.90 target on all datasets (0.88 to 0.91), whereas Normal_QR falls as low as 0.43 to 0.62 on Hydropower and the solar datasets.
- ACI has higher LPIA than Normal_QR on 6 of 9 datasets (50Hertz, TenneTTSO, Amprion, Hydropower, Solar Plant 1, Solar Plant 2) and lower LPICE on 6 of 9, with ties on Location 1 and Location 2.
- The largest gains are on Hydropower and the solar datasets, where QR under-covers badly (e.g. Solar Plant 2 LPICE 0.47 to 0.05).
- Normal_QR is better on TransnetBW and slightly better on LPIA for Location 1 and Location 2, where its global coverage is already near or above target.
- ACI achieves better calibration with wider intervals, most clearly on the solar datasets.
- Figure 3 in the paper shows the LPICE distribution (QR vs ACI) and the per-dataset percentage improvement heatmap.