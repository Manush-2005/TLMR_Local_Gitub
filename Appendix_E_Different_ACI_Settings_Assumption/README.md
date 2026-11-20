# Appendix: Local-Error Assumption under Different ACI Step Sizes (Paper Appendix D)

Repeats the empirical check of Sec. 6.4 for other values of the ACI step size γ. The goal is to show that the abrupt local-error behaviour of ACI at coverage failures (condition (23)) does not depend on the choice of γ.

Corresponds to **Appendix D, Tables 11 to 13** of the paper. The main experiment (γ = 0.001, Table 5) is in the Sec. 6.4 folder.

## Files

- `Exp_ACI_final_gamma_0.004.ipynb`: ACI with γ = 0.004 (Table 11).
- `Exp_ACI_final_gamma_0.008.ipynb`: ACI with γ = 0.008 (Table 12).
- `Exp_ACI_final_gamma_0.016.ipynb`: ACI with γ = 0.016 (Table 13).
- `Final_Results.txt`: aggregated numerical output.
- `results_all_methods_all_datasets.csv`: results for every γ and dataset.
- `aci_failure_audit/`: per-dataset audit of coverage failures.
- `trajectories/`: per-dataset online ACI trajectories.
- `Helper_Scripts/`: metric computation, models and ACI implementation.

## Run

```bash
jupyter notebook Exp_ACI_final_gamma_0.004.ipynb
jupyter notebook Exp_ACI_final_gamma_0.008.ipynb
jupyter notebook Exp_ACI_final_gamma_0.016.ipynb
```

Run all cells in each notebook.

## Experimental Setup

Same as Sec. 6.4 (LSTM forecaster, T_init = 5,000, 1 − α = 0.90, w = 24, decay factor M = 0.95 for the weighted average of local errors, seed 42). Only γ changes: **γ ∈ {0.004, 0.008, 0.016}**.

At each coverage failure s, the check is whether LE_s^(L) exceeds the recency-weighted average local error. Columns:
- `#(err=1)`: number of coverage failures.
- `# abrupt`: failures with LE_s^(L) > weighted-average local error.
- `Mean LE_s`: mean local error at failures.
- `Mean baseline`: mean weighted-average local error at failures.
- `Δ`: mean difference.

## Results

### Table 11: γ = 0.004

| Dataset | #(err=1) | # abrupt | % abrupt | Mean LE_s | Mean baseline | Δ |
|---|---|---|---|---|---|---|
| 50Hertz | 409 | 259 | 63.33 | 0.08 | 0.04 | 0.04 |
| Amprion | 401 | 247 | 61.60 | 0.11 | 0.06 | 0.04 |
| Location 1 | 476 | 272 | 57.14 | 0.08 | 0.04 | 0.04 |
| Location 2 | 439 | 241 | 54.90 | 0.06 | 0.04 | 0.03 |
| Plant 1 Generation | 198 | 127 | 64.14 | 0.09 | 0.07 | 0.03 |
| Plant 2 Generation | 348 | 272 | 78.16 | 0.10 | 0.07 | 0.03 |
| TenneTTSO | 420 | 258 | 61.43 | 0.10 | 0.06 | 0.04 |
| TransnetBW | 434 | 251 | 57.83 | 0.06 | 0.03 | 0.03 |
| Hydropower | 149 | 105 | 70.47 | 0.16 | 0.08 | 0.07 |
| **Total** | **3274** | **2032** | **62.06** | **0.09** | **0.05** | **0.04** |

### Table 12: γ = 0.008

| Dataset | #(err=1) | # abrupt | % abrupt | Mean LE_s | Mean baseline | Δ |
|---|---|---|---|---|---|---|
| 50Hertz | 430 | 263 | 61.16 | 0.08 | 0.04 | 0.04 |
| Amprion | 417 | 266 | 63.79 | 0.10 | 0.05 | 0.04 |
| Location 1 | 464 | 263 | 56.68 | 0.07 | 0.04 | 0.04 |
| Location 2 | 460 | 259 | 56.30 | 0.06 | 0.03 | 0.03 |
| Plant 1 Generation | 259 | 183 | 70.66 | 0.07 | 0.04 | 0.03 |
| Plant 2 Generation | 366 | 284 | 77.60 | 0.10 | 0.07 | 0.03 |
| TenneTTSO | 435 | 257 | 59.08 | 0.09 | 0.05 | 0.04 |
| TransnetBW | 438 | 259 | 59.13 | 0.06 | 0.03 | 0.03 |
| Hydropower | 147 | 96 | 65.31 | 0.13 | 0.07 | 0.06 |
| **Total** | **3416** | **2130** | **62.35** | **0.08** | **0.05** | **0.03** |

### Table 13: γ = 0.016

| Dataset | #(err=1) | # abrupt | % abrupt | Mean LE_s | Mean baseline | Δ |
|---|---|---|---|---|---|---|
| 50Hertz | 438 | 263 | 60.05 | 0.07 | 0.03 | 0.04 |
| Amprion | 433 | 269 | 62.12 | 0.08 | 0.04 | 0.04 |
| Location 1 | 467 | 264 | 56.53 | 0.06 | 0.03 | 0.03 |
| Location 2 | 467 | 257 | 55.03 | 0.05 | 0.03 | 0.02 |
| Plant 1 Generation | 288 | 219 | 76.04 | 0.05 | 0.03 | 0.03 |
| Plant 2 Generation | 360 | 286 | 79.44 | 0.07 | 0.04 | 0.03 |
| TenneTTSO | 437 | 260 | 59.50 | 0.07 | 0.04 | 0.03 |
| TransnetBW | 444 | 254 | 57.21 | 0.05 | 0.03 | 0.02 |
| Hydropower | 148 | 92 | 62.16 | 0.10 | 0.05 | 0.05 |
| **Total** | **3482** | **2164** | **62.15** | **0.07** | **0.04** | **0.03** |

## Summary

- The pooled share of abrupt coverage failures is about 62% for every γ (62.06%, 62.35% and 62.15%), almost identical to the 61.43% at γ = 0.001 in the main experiment.
- Every dataset stays above 50% for every γ (lowest: Location 2 at 54.90% to 56.30%), so condition (23) holds with p < 2 across all values of γ considered.
- The mean local error at coverage failures is larger than the weighted-average baseline for every γ and dataset (positive Δ).
- This suggests that recent local miscalibration carries information about imminent coverage failures, which supports using local error information in LACI.
