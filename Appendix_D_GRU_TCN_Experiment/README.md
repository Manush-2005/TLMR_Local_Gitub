# Appendix: LACI with GRU and TCN Forecasters (Paper Appendix C)

Repeats the LACI vs ACI, DtACI and AgACI comparison of Sec. 6.5 with two other neural forecasters, **GRU** and **TCN**, to check that LACI's advantage does not depend on the LSTM architecture.

Corresponds to **Appendix C, Tables 8 (hyperparameters), 9 (GRU) and 10 (TCN)** of the paper.

## Files

- `Appedix_D_Exp_GRU.ipynb`: GRU experiment (ACI, LACI, DtACI, AgACI on all nine datasets).
- `Appedix_D_Exp_TCN.ipynb`: TCN experiment (same methods and datasets).
- `Final_Results.txt`: aggregated numerical output.
- `results_all_methods_all_datasets.csv`: metrics for every method and dataset.
- `results_hydropower.csv`, `results_locations_1_2.csv`, `results_plants_1_2.csv`: per-group result files.
- `Helper_Scripts/`: metric computation, GRU and TCN models, preprocessing and method implementations.
- `trajectories/`: per-dataset online trajectories of each method.

## Run

```bash
jupyter notebook Appedix_D_Exp_GRU.ipynb
jupyter notebook Appedix_D_Exp_TCN.ipynb
```

Run all cells in each notebook.

## Experimental Setup

Same online protocol as Sec. 6.5 (T_init = 5,000, 1 fine-tuning epoch every 6 steps, 1 − α = 0.90, w = 24, γ = 0.001, seed 42, sequence length 48, Adam with lr 0.001, batch size 32, 200 initial epochs). Only the forecaster changes:

| Architecture | Configuration |
|---|---|
| GRU | 2 layers, hidden dim 64, Linear(64, 1) head |
| TCN | channels [32, 32, 32, 32], kernel size 2, dropout 0.2, Linear(32, 1) head |

## Results

Target coverage 1 − α = 0.90. Local metrics: LPIA (higher is better), LPICE, LMPIW. Global metrics: PICP, MPIW.

### Table 9: GRU

| Dataset | Method | LPIA | LPICE | LMPIW | PICP | MPIW |
|---|---|---|---|---|---|---|
| 50Hertz | ACI | 0.62 | 0.04 | 49.55 | 0.90 | 49.57 |
| | LACI | **0.74** | **0.02** | 57.05 | 0.93 | 57.05 |
| | DtACI | 0.58 | 0.04 | 48.91 | 0.90 | 48.91 |
| | AgACI | 0.57 | 0.04 | 49.43 | 0.90 | 49.44 |
| Amprion | ACI | 0.66 | 0.04 | 32.47 | 0.91 | 32.49 |
| | LACI | **0.73** | **0.03** | 36.40 | 0.93 | 36.42 |
| | DtACI | 0.65 | 0.04 | 30.56 | 0.90 | 30.59 |
| | AgACI | 0.62 | 0.04 | 32.97 | 0.90 | 32.98 |
| TransnetBW | ACI | 0.66 | 0.03 | 12.36 | 0.90 | 12.34 |
| | LACI | **0.78** | **0.02** | 13.47 | 0.93 | 13.45 |
| | DtACI | 0.62 | 0.03 | 12.20 | 0.90 | 12.18 |
| | AgACI | 0.62 | 0.03 | 12.83 | 0.90 | 12.81 |
| TenneTTSO | ACI | 0.62 | 0.04 | 43.58 | 0.90 | 43.55 |
| | LACI | **0.74** | **0.02** | 50.34 | 0.94 | 50.28 |
| | DtACI | 0.59 | 0.04 | 42.27 | 0.90 | 42.24 |
| | AgACI | 0.58 | 0.04 | 42.45 | 0.90 | 42.42 |
| Location 1 | ACI | 0.56 | 0.03 | 0.26 | 0.90 | 0.26 |
| | LACI | **0.79** | **0.01** | 0.33 | 0.93 | 0.33 |
| | DtACI | 0.54 | 0.03 | 0.26 | 0.90 | 0.26 |
| | AgACI | 0.57 | 0.03 | 0.26 | 0.90 | 0.26 |
| Location 2 | ACI | 0.55 | 0.04 | 0.19 | 0.89 | 0.19 |
| | LACI | **0.74** | **0.02** | 0.24 | 0.93 | 0.24 |
| | DtACI | 0.53 | 0.03 | 0.19 | 0.90 | 0.19 |
| | AgACI | 0.56 | 0.03 | 0.20 | 0.90 | 0.20 |
| Solar Plant 1 | ACI | 0.66 | 0.06 | 628.20 | 0.90 | 627.59 |
| | LACI | **0.72** | **0.04** | 910.52 | 0.92 | 909.01 |
| | DtACI | 0.58 | **0.04** | 634.90 | 0.90 | 633.71 |
| | AgACI | 0.63 | **0.04** | 795.57 | 0.91 | 793.95 |
| Solar Plant 2 | ACI | 0.56 | 0.05 | 5226.78 | 0.89 | 5230.68 |
| | LACI | **0.71** | **0.02** | 6783.43 | 0.93 | 6785.30 |
| | DtACI | 0.58 | 0.03 | 4895.05 | 0.90 | 4905.16 |
| | AgACI | 0.56 | 0.04 | 5370.65 | 0.90 | 5379.70 |
| Hydropower | ACI | 0.66 | 0.07 | 150.97 | 0.87 | 151.49 |
| | LACI | **0.70** | 0.06 | 157.72 | 0.89 | 158.15 |
| | DtACI | 0.60 | **0.04** | 141.34 | 0.90 | 142.04 |
| | AgACI | 0.65 | **0.04** | 172.13 | 0.91 | 172.31 |

### Table 10: TCN

| Dataset | Method | LPIA | LPICE | LMPIW | PICP | MPIW |
|---|---|---|---|---|---|---|
| 50Hertz | ACI | 0.55 | 0.03 | 43.07 | 0.90 | 43.05 |
| | LACI | **0.76** | **0.01** | 49.91 | 0.93 | 49.91 |
| | DtACI | 0.55 | 0.03 | 42.99 | 0.90 | 42.97 |
| | AgACI | 0.56 | 0.03 | 43.15 | 0.90 | 43.14 |
| Amprion | ACI | 0.59 | 0.03 | 25.85 | 0.90 | 25.85 |
| | LACI | **0.75** | **0.02** | 29.56 | 0.93 | 29.55 |
| | DtACI | 0.58 | 0.03 | 26.08 | 0.90 | 26.09 |
| | AgACI | 0.59 | 0.03 | 26.16 | 0.90 | 26.16 |
| TenneTTSO | ACI | 0.59 | 0.03 | 36.54 | 0.90 | 36.50 |
| | LACI | **0.77** | **0.01** | 41.43 | 0.94 | 41.38 |
| | DtACI | 0.59 | 0.03 | 36.05 | 0.90 | 36.01 |
| | AgACI | 0.58 | 0.03 | 36.05 | 0.90 | 36.01 |
| TransnetBW | ACI | 0.61 | 0.03 | 11.24 | 0.90 | 11.23 |
| | LACI | **0.78** | **0.01** | 12.22 | 0.93 | 12.21 |
| | DtACI | 0.57 | 0.03 | 11.28 | 0.90 | 11.26 |
| | AgACI | 0.58 | 0.03 | 11.30 | 0.90 | 11.29 |
| Location 1 | ACI | 0.57 | 0.03 | 0.26 | 0.90 | 0.26 |
| | LACI | **0.81** | **0.01** | 0.32 | 0.94 | 0.32 |
| | DtACI | 0.54 | 0.02 | 0.26 | 0.90 | 0.26 |
| | AgACI | 0.56 | 0.03 | 0.26 | 0.90 | 0.26 |
| Location 2 | ACI | 0.54 | 0.03 | 0.18 | 0.90 | 0.18 |
| | LACI | **0.74** | **0.01** | 0.21 | 0.93 | 0.21 |
| | DtACI | 0.54 | 0.02 | 0.18 | 0.90 | 0.18 |
| | AgACI | 0.55 | 0.03 | 0.18 | 0.90 | 0.18 |
| Solar Plant 1 | ACI | 0.60 | 0.04 | 564.00 | 0.90 | 562.88 |
| | LACI | **0.78** | **0.02** | 678.77 | 0.94 | 677.37 |
| | DtACI | 0.58 | 0.04 | 586.90 | 0.90 | 585.86 |
| | AgACI | 0.63 | 0.04 | 604.85 | 0.91 | 603.58 |
| Solar Plant 2 | ACI | 0.59 | 0.06 | 4789.80 | 0.89 | 4799.47 |
| | LACI | **0.76** | **0.02** | 7224.34 | 0.94 | 7227.63 |
| | DtACI | 0.58 | 0.03 | 4593.01 | 0.90 | 4601.81 |
| | AgACI | 0.58 | 0.03 | 5199.46 | 0.91 | 5208.07 |
| Hydropower | ACI | 0.57 | 0.05 | 134.14 | 0.88 | 135.58 |
| | LACI | **0.62** | **0.04** | 146.56 | 0.91 | 148.10 |
| | DtACI | 0.53 | **0.04** | 130.12 | 0.89 | 131.60 |
| | AgACI | 0.59 | **0.04** | 137.62 | 0.90 | 139.23 |

## Summary

- With both GRU and TCN, LACI has the highest LPIA on all nine datasets (GRU 0.70 to 0.79, TCN 0.62 to 0.81), compared with about 0.53 to 0.66 for ACI, DtACI and AgACI.
- LACI has the lowest LPICE on most datasets (7 of 9 for GRU; for TCN it is lowest or tied-lowest on all nine at two decimals). Hydropower with GRU is the exception, where DtACI and AgACI reach 0.04.
- As in the LSTM experiment, LACI's gains come with wider intervals and a PICP slightly above target (0.89 to 0.94).
- The improvement is therefore not tied to a specific forecasting architecture.
