# Appendix: LACI vs SAOCP (Paper Appendix E)

Compares **LACI** with **SAOCP** (Strongly Adaptive Online Conformal Prediction, Bhatnagar et al., 2023; also written SACOP / SOCAP in some file and folder names). The two methods adapt the conformal interval in different ways:

- **LACI** selects a miscoverage level α_i through an ACI-style recursion with local-error weighting.
- **SAOCP** tracks the calibration threshold (interval radius) directly in the nonconformity-score space by aggregating online learners started at different times.

To compare them on the same footing, LACI is run here with the **midpoint absolute-residual nonconformity score** (the absolute distance between the observation and the midpoint of the predicted interval), the score type used by SAOCP. The goal is to see how much local calibration is gained by adapting the threshold itself instead of selecting the level from existing conformal scores.

Corresponds to **Appendix E** of the paper.

## Files

- `LACI_SACOP.ipynb`: LACI experiment with midpoint absolute-residual scores on all nine datasets.
- `SOCAP_final.ipynb`: final code for the SAOCP baseline.
- `Final_Results.txt`: aggregated numerical output.
- `results_LACI_midpoint_absolute_*.csv`: per-group result files, split into four German grid datasets (50Hertz, Amprion, TenneTTSO, TransnetBW), two wind locations, two solar plants and Hydropower.
- `Helper_Scripts/`: metric computation, models and method implementations.
- `trajectories/`: per-dataset online trajectories of each method.

## Run

```bash
jupyter notebook LACI_SACOP.ipynb          # LACI with midpoint absolute-residual scores
jupyter notebook SOCAP_final.ipynb   # SAOCP baseline
```

Run all cells in each notebook. Results are written to `Final_Results.txt` and the CSV files.

## Experimental Setup

Same online protocol as Sec. 6.5 (LSTM quantile forecaster, T_init = 5,000, 1 fine-tuning epoch every 6 steps, seed 42).

| Parameter | Value |
|---|---|
| Target coverage (1 − α) | 0.90 |
| Local window (w) | 24 hours |
| Nonconformity score | Midpoint absolute residual |
| LACI step size (γ) | 0.001 |
| Datasets | Nine energy datasets (Table 1 of the paper) |

## Metrics

- **Local:** LPICE (lower is better), LPIA (higher is better), LMPIW (lower is better).
- **Global:** PICP (closest to 0.90 is preferred), MPIW (lower is better).

## Results

Nominal coverage 1 − α = 0.90. Best results are in bold, as in the paper table.

| Dataset | Method | LPICE ↓ | LPIA ↑ | LMPIW ↓ | PICP | MPIW ↓ |
|---|---|---|---|---|---|---|
| 50Hertz | LACI | 0.03 | 0.73 | 61.13 | **0.93** | 61.17 |
| | SAOCP | **0.01** | **0.73** | **57.35** | 0.93 | **57.25** |
| Amprion | LACI | 0.03 | 0.76 | **40.09** | **0.93** | **40.11** |
| | SAOCP | **0.01** | **0.82** | 46.85 | 0.93 | 46.79 |
| TenneTTSO | LACI | 0.03 | 0.75 | **49.65** | **0.93** | **49.70** |
| | SAOCP | **0.01** | **0.87** | 65.14 | 0.94 | 65.16 |
| TransnetBW | LACI | 0.03 | 0.74 | 14.74 | 0.93 | 14.75 |
| | SAOCP | **0.01** | **0.74** | **14.45** | **0.92** | **14.45** |
| Hydropower | LACI | 0.05 | 0.67 | 182.65 | **0.90** | 182.91 |
| | SAOCP | **0.01** | **0.84** | **166.52** | 0.94 | **167.69** |
| Location 1 | LACI | 0.03 | 0.74 | 0.05 | **0.92** | 0.05 |
| | SAOCP | **0.01** | **0.76** | **0.04** | 0.93 | **0.04** |
| Location 2 | LACI | 0.03 | 0.69 | 0.04 | **0.92** | 0.04 |
| | SAOCP | **0.01** | **0.73** | **0.03** | 0.92 | **0.03** |
| Plant 1 | LACI | 0.05 | 0.72 | 1608.13 | **0.91** | 1606.66 |
| | SAOCP | **0.00** | **0.93** | **713.07** | 0.96 | **720.38** |
| Plant 2 | LACI | 0.02 | 0.79 | 5989.54 | 0.94 | 5997.60 |
| | SAOCP | **0.01** | **0.80** | **2114.70** | **0.93** | **2121.23** |

## Summary

- SAOCP has the lower LPICE on all nine datasets (0.00 to 0.01 vs 0.02 to 0.05 for LACI).
- SAOCP has the higher LPIA on seven of nine datasets, with ties at two decimals on 50Hertz and TransnetBW; the largest gaps are on Plant 1 (0.93 vs 0.72), Hydropower (0.84 vs 0.67) and TenneTTSO (0.87 vs 0.75).
- SAOCP also gives narrower local intervals on seven of nine datasets (all except Amprion and TenneTTSO), with very large reductions on Plant 1 and Plant 2.
- LACI has PICP closer to 0.90 on several datasets, while SAOCP tends to over-cover slightly (0.92 to 0.96).
- This indicates that adapting the calibration threshold directly can give more reliable local coverage than selecting the significance level from existing conformal scores, which is the main limitation of LACI discussed in the paper. LACI remains a single-recursion modification of ACI with no expert aggregation.
- LACI numbers here use midpoint absolute-residual scores and therefore differ from the LACI results in Table 6, which use the CQR score.
