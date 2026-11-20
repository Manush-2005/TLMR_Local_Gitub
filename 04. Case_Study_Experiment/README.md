# Case Study: Economic Implications of Local Calibration (Paper Sec. 7)

Simulates the financial effect of local coverage failures for a power generation company that must meet its scheduled generation over each 24-hour operating window. Prediction intervals from ACI, DtACI, AgACI and LACI are converted into an imbalance penalty cost, so that better local calibration can be compared in money terms.

Corresponds to **Section 7 and Table 7** of the paper.

## Cost Model

Hourly net revenue: R_t = p_t^(g) · E_t^(g) − C_t^imb

Imbalance penalty at hour i:

C_i^imb = P_mis · LE_i + λ · LMPIW_i

- `LE_i`: local coverage error over the 24-hour window (violation of the energy commitment).
- `LMPIW_i`: local interval width, penalised at a lower rate through λ (cost of holding flexible reserve).

Average penalty over the evaluation period:

C = P_mis · LPICE + λ · LMPIW

Parameters used: **P_mis = 200**, **λ = 0.1**. The cost structure follows the equivalent-cost approach to reserve setting under probabilistic wind forecasts (Matos & Bessa, 2011).

## Files

- `Case_studyExp.ipynb`: main notebook. Runs ACI, DtACI, AgACI and LACI, computes LPICE, LPIA, LMPIW, the average cost C and the total composite cost for each dataset.
- `Final_Results.txt`: aggregated numerical output.
- `results_all_methods_all_datasets.csv`: metrics and costs for every method and dataset.
- `predictions.csv`: forecasts and prediction intervals used for the cost computation.
- `local_calibration_imbalance_results/`, `local_calibration_penalty_results/`: per-dataset imbalance and penalty cost outputs.
- `trajectories/`: per-dataset online trajectories of each method.
- `Helper_Scripts/`: metric computation, models and method implementations.

## Run

```bash
jupyter notebook Case_studyExp.ipynb
```

Run all cells. Results are written to `Final_Results.txt` and the CSV and output folders above.

## Experimental Setup

| Parameter | Value |
|---|---|
| Forecaster | LSTM quantile model (same setup as Sec. 6.5) |
| Target coverage (1 − α) | 0.90 |
| Local window (w) | 24 hours |
| Penalty coefficient (P_mis) | 200 |
| Reserve cost coefficient (λ) | 0.1 |
| ACI / LACI step size (γ) | 0.001 |
| Compared methods | ACI, DtACI, AgACI, LACI |

## Results (Table 7 of the paper)

Average imbalance cost C̄ (Eq. 28) and total composite cost, P_mis = 200, λ = 0.1. Lower cost is better; the lowest cost per dataset is in bold.

| Dataset | Method | LPICE ↓ | LPIA ↑ | LMPIW ↓ | Cost C̄ ↓ | Total Composite Cost ↓ |
|---|---|---|---|---|---|---|
| 50Hertz | ACI | 0.04 | 0.67 | 49.14 | 12.87 | 57354.14 |
| | DtACI | 0.04 | 0.63 | 48.10 | 12.58 | 56087.83 |
| | AgACI | 0.04 | 0.63 | 49.64 | 12.26 | 54639.35 |
| | LACI | 0.03 | 0.73 | 55.12 | **10.78** | **48062.00** |
| Amprion | ACI | 0.04 | 0.68 | 32.07 | 11.61 | 51740.82 |
| | DtACI | 0.04 | 0.66 | 30.89 | 10.96 | 48858.61 |
| | AgACI | 0.04 | 0.67 | 34.17 | 10.49 | 46768.42 |
| | LACI | 0.03 | 0.75 | 36.35 | **9.42** | **41998.42** |
| Location 1 | ACI | 0.03 | 0.58 | 0.28 | 6.40 | 37342.30 |
| | DtACI | 0.03 | 0.55 | 0.28 | 5.68 | 33110.13 |
| | AgACI | 0.03 | 0.57 | 0.28 | 5.71 | 33317.04 |
| | LACI | 0.02 | 0.74 | 0.33 | **3.15** | **18381.23** |
| Location 2 | ACI | 0.04 | 0.55 | 0.20 | 7.03 | 41020.21 |
| | DtACI | 0.03 | 0.56 | 0.20 | 5.59 | 32614.99 |
| | AgACI | 0.03 | 0.56 | 0.21 | 5.98 | 34885.78 |
| | LACI | 0.01 | 0.76 | 0.25 | **3.01** | **17570.54** |
| Plant 1 | ACI | 0.05 | 0.66 | 749.16 | 85.69 | 503939.92 |
| | DtACI | 0.04 | 0.60 | 687.07 | **76.78** | **451546.70** |
| | AgACI | 0.04 | 0.60 | 886.86 | 96.40 | 566952.84 |
| | LACI | 0.04 | 0.73 | 837.24 | 91.68 | 539169.39 |
| TenneTTSO | ACI | 0.04 | 0.62 | 40.00 | 12.04 | 53651.14 |
| | DtACI | 0.04 | 0.59 | 39.61 | 11.87 | 52912.20 |
| | AgACI | 0.04 | 0.60 | 43.06 | 11.46 | 51058.34 |
| | LACI | 0.03 | 0.71 | 44.45 | **10.27** | **45777.83** |
| TransnetBW | ACI | 0.03 | 0.62 | 11.82 | 7.08 | 31541.34 |
| | DtACI | 0.03 | 0.62 | 11.79 | 6.69 | 29818.32 |
| | AgACI | 0.03 | 0.61 | 12.79 | 6.58 | 29314.38 |
| | LACI | 0.01 | 0.80 | 13.28 | **3.98** | **17734.68** |
| Hydropower | ACI | 0.06 | 0.54 | 202.22 | 32.85 | 47304.91 |
| | DtACI | 0.04 | 0.54 | 192.49 | **26.97** | **38839.77** |
| | AgACI | 0.05 | 0.60 | 204.11 | 29.73 | 42818.17 |
| | LACI | 0.05 | 0.59 | 211.04 | 30.75 | 44273.67 |

## Summary

- LACI gives the lowest imbalance cost on 6 of the 8 datasets (50Hertz, Amprion, Location 1, Location 2, TenneTTSO, TransnetBW); DtACI is lowest on Plant 1 and Hydropower.
- The largest savings are on TransnetBW, Location 1 and Location 2, where LACI roughly halves the cost of ACI (e.g. Location 2: 7.03 to 3.01).
- LACI lowers the local-error term (LPICE) at the price of wider intervals; with P_mis = 200 and λ = 0.1 the reduction in local coverage failures outweighs the extra reserve cost on most datasets.
- On Plant 1 and Hydropower, where LACI's intervals are much wider and its LPICE gain is small, the width term dominates and DtACI is cheaper.
