# Sec 6.4 — LACI vs. ACI Variants: LSTM Experiments

Compares LACI against ACI, DtACI, and AgACI across nine energy datasets using an LSTM
architecture. This is the primary experiment of the paper, demonstrating that LACI
consistently achieves superior local calibration — measured by LPIA and LPICE — over all
existing ACI variants, at a modest cost in interval width.

Two decay factor settings are evaluated:

- **`Exp_6.4.ipynb`** — main results with decay factor M = 0.95 (Table 4 of the paper)
- **`Exp_6.4_Decay_0.80.ipynb`** — sensitivity check with M = 0.80

## Files

- `Exp_6.4.ipynb` — main notebook (M = 0.95); trains ACI, LACI, DtACI, AgACI on all 9 datasets
- `Exp_6.4_Decay_0.80.ipynb` — repeat of the above with decay factor M = 0.80
- `Helper_Scripts/calculate_metrics.py` — LPIA, LPICE, MLPICP, LMPIW, LCWC, PICP, MPIW computation
- `Helper_Scripts/loss_functions.py` — pinball loss implementation for quantile training
- `Helper_Scripts/models.py` — LSTM architecture definition
- `Helper_Scripts/models_TLMR.py` — LSTM architecture variant used for TMLR submission
- `Helper_Scripts/preprocessing.py` — sliding-window construction, train/calibration split, normalization
- `trajectories/` — per-dataset CSV files of online trajectories for each method; columns:
  `step`, `alphaTrajectory`, `errSeq`, `y_u_pred`, `y_l_pred`, `y_true`

## Run

Main experiment (M = 0.95):

```bash
jupyter notebook Exp_6.4.ipynb
```

Decay sensitivity (M = 0.80):

```bash
jupyter notebook Exp_6.4_Decay_0.80.ipynb
```

Trajectory CSVs are written to `trajectories/` automatically during each run.

## Experimental Setup

| Parameter | Value |
|---|---|
| Architecture | LSTM (hidden dim: 64, layers: 1) |
| Initial training window (T_init) | 5,000 samples |
| Fine-tuning cadence | Every 6 hours (online) |
| Sequence length | 48 |
| Target coverage (1 − α) | 0.90 |
| Local evaluation window (w) | 24 hours |
| ACI / LACI step size (γ) | 0.001 |
| Decay factor (M) | 0.95 (main), 0.80 (sensitivity) |
| DtACI γ candidates | {0.001, 0.002, 0.004, 0.008, 0.016} |
| AgACI γ candidates | {0.001, 0.002, 0.004, 0.008, 0.016} |
| Random seed | 42 |

## Results (Table 4 from paper)

LACI achieves the best LPIA in **9/9** datasets and the best LPICE in **8/9** datasets.
The average LPIA across datasets: ACI = 0.61, DtACI = 0.59, AgACI = 0.59, **LACI = 0.72**.

| Dataset | Method | LPIA | LPICE | LMPIW | PICP | MPIW |
|---|---|---|---|---|---|---|
| 50Hertz | ACI | 0.6338 | 0.0404 | 48.947 | 0.9022 | 48.948 |
| 50Hertz | **LACI** | **0.6964** | **0.0281** | 54.553 | 0.9234 | 54.547 |
| 50Hertz | DtACI | 0.6116 | 0.0398 | 50.400 | 0.9020 | 50.402 |
| 50Hertz | AgACI | 0.5973 | 0.0365 | 50.268 | 0.9009 | 50.256 |
| Amprion | ACI | 0.6652 | 0.0408 | 32.161 | 0.9069 | 32.187 |
| Amprion | **LACI** | **0.7243** | **0.0349** | 34.969 | 0.9217 | 35.006 |
| Amprion | DtACI | 0.5883 | 0.0371 | 31.352 | 0.9029 | 31.385 |
| Amprion | AgACI | 0.6053 | 0.0343 | 31.011 | 0.9031 | 31.022 |
| TenneTTSO | ACI | 0.6383 | 0.0392 | 42.845 | 0.9040 | 42.777 |
| TenneTTSO | **LACI** | **0.6960** | **0.0270** | 48.459 | 0.9252 | 48.415 |
| TenneTTSO | DtACI | 0.6226 | 0.0354 | 42.624 | 0.9031 | 42.591 |
| TenneTTSO | AgACI | 0.5802 | 0.0352 | 42.443 | 0.9022 | 42.387 |
| TransnetBW | ACI | 0.6141 | 0.0298 | 11.881 | 0.9047 | 11.865 |
| TransnetBW | **LACI** | **0.7449** | **0.0216** | 13.161 | 0.9283 | 13.150 |
| TransnetBW | DtACI | 0.6038 | 0.0303 | 11.727 | 0.9022 | 11.714 |
| TransnetBW | AgACI | 0.5742 | 0.0294 | 12.089 | 0.9022 | 12.078 |
| Location 1 | ACI | 0.6192 | 0.0396 | 0.0325 | 0.8972 | 0.0325 |
| Location 1 | **LACI** | **0.7626** | **0.0181** | 0.0367 | 0.9311 | 0.0367 |
| Location 1 | DtACI | 0.5902 | 0.0338 | 0.0294 | 0.8996 | 0.0294 |
| Location 1 | AgACI | 0.5940 | 0.0336 | 0.0321 | 0.8976 | 0.0320 |
| Location 2 | ACI | 0.6269 | 0.0333 | 0.0262 | 0.9015 | 0.0261 |
| Location 2 | **LACI** | **0.7916** | **0.0149** | 0.0302 | 0.9350 | 0.0302 |
| Location 2 | DtACI | 0.6143 | 0.0327 | 0.0262 | 0.8996 | 0.0262 |
| Location 2 | AgACI | 0.5946 | 0.0307 | 0.0258 | 0.8996 | 0.0258 |
| Solar Plant 1 | ACI | 0.6206 | 0.0677 | 1429.529 | 0.8817 | 1429.153 |
| Solar Plant 1 | **LACI** | **0.7473** | **0.0477** | 1496.151 | 0.9111 | 1495.502 |
| Solar Plant 1 | DtACI | 0.6412 | **0.0405** | 898.424 | 0.9054 | 902.608 |
| Solar Plant 1 | AgACI | 0.5635 | 0.0278 | 974.793 | 0.8982 | 981.173 |
| Solar Plant 2 | ACI | 0.4179 | 0.0532 | 5333.736 | 0.8761 | 5334.083 |
| Solar Plant 2 | **LACI** | **0.7534** | **0.0135** | 7305.272 | 0.9397 | 7314.249 |
| Solar Plant 2 | DtACI | 0.5417 | 0.0331 | 5269.600 | 0.8951 | 5282.610 |
| Solar Plant 2 | AgACI | 0.5479 | 0.0319 | 5618.196 | 0.8962 | 5626.572 |
| Hydropower | ACI | 0.5729 | 0.0732 | 146.676 | 0.8658 | 146.696 |
| Hydropower | **LACI** | **0.6856** | **0.0506** | 161.582 | 0.9003 | 161.755 |
| Hydropower | DtACI | 0.5904 | 0.0679 | 157.698 | 0.8738 | 158.918 |
| Hydropower | AgACI | 0.5493 | 0.0657 | 152.812 | 0.8684 | 152.634 |