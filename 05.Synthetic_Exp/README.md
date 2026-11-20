# Synthetic Experiment: LACI under Abrupt Distribution Shift (Paper Sec. 6.2)

A controlled AR(1) experiment illustrating how ACI and LACI behave under abrupt changes in the noise distribution. It shows that (i) after a variance shift most local coverage failures of ACI are "abrupt" (local error above the weighted average of past local errors), and (ii) LACI reduces local coverage error in this regime.

Corresponds to **Section 6.2, Tables 2 and 3 and Figure 2** of the paper.

## Files

- `Synethic_Experiment.ipynb`: notebook that generates the series, fits the AR(1) forecaster, runs ACI and LACI, and produces all tables and figures.
- `ar1_upward_shift_outputs/`: outputs for the upward variance shifts (trajectories, metrics).
- `ar1_upward_shift_outputs_side_by_side/`: ACI vs LACI comparison plots for a single shift.
- `ar1_all_upward_shifts_side_by_side/`: ACI vs LACI comparison plots for all upward shifts.

## Run

```bash
jupyter notebook Synethic_Experiment.ipynb
```

Run all cells. The output folders above are created automatically.

## Experimental Setup

Data-generating process:

x_t = c + φ · x_{t−1} + ε_t, ε_t ~ N(0, σ_t²), with c = 10, φ = 0.8, x_0 = 50.

| Parameter | Value |
|---|---|
| Number of observations | 7,200 |
| Variance shift times | t = 1800, 2800, 3800, 4800, 5800 |
| Noise std σ (before, then after each shift) | 0.06, 0.17, 0.09, 0.21, 0.10, 0.23 |
| Point forecaster | AR(1) fitted by OLS on the first 700 observations |
| Conformal calibration | Rolling window of 300 residual scores |
| ACI / LACI step size (γ) | 0.001 |
| Decay factor (M) | 0.95 |
| Target coverage (1 − α) | 0.90 |
| Local window (w) | 24 |

The shifts at t = 1800, 3800 and 5800 increase σ (the "upward shifts" analysed here). Local behaviour is evaluated over the first 180 observations after each such shift.

## Results

### Table 2: abrupt local coverage errors of ACI

Windows right after a shift vs a window 200 steps later. "Abrupt" means LE_s^(L) > weighted-average local error.

| Window | Coverage failures | # abrupt | % abrupt |
|---|---|---|---|
| 1800–1979 (after shift) | 54 | 36 | 66.67 |
| 2000–2179 | 11 | 1 | 9.09 |
| 3800–3979 (after shift) | 52 | 40 | 76.92 |
| 4000–4179 | 14 | 6 | 42.86 |
| 5800–5979 (after shift) | 50 | 37 | 74.00 |
| 6000–6179 | 16 | 7 | 43.75 |

### Table 3: local performance of ACI vs LACI after each shift

First 180 observations after the shift.

| Shift time | LPICP ACI | LPICP LACI | Mean LE ACI | Mean LE LACI | LMPIW ACI | LMPIW LACI |
|---|---|---|---|---|---|---|
| 1800 | 0.7000 | 0.8556 | 0.19875 | 0.07097 | 0.37307 | 0.50873 |
| 3800 | 0.7111 | 0.8556 | 0.20537 | 0.07097 | 0.48624 | 0.66982 |
| 5800 | 0.7222 | 0.8556 | 0.18421 | 0.05958 | 0.55724 | 0.69948 |

## Summary

- Right after a variance shift, 67% to 77% of ACI's coverage failures are abrupt, compared with 9% to 44% in the later window, which supports condition (23) of the paper.
- In the 180 steps after each shift, LACI raises local coverage from about 0.70 to 0.72 (ACI) to 0.8556 and cuts the mean local error by roughly 65% to 68%.
- The improvement comes with wider local intervals (LMPIW about 30% to 38% larger).
- Figure 2 shows, for one shift, the ACI prediction intervals with abrupt failures marked, the local error trajectories of ACI and LACI, and the abrupt-failure counts immediately after the shift vs 200 steps later.
