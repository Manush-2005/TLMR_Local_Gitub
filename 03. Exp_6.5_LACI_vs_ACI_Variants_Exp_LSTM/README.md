# LACI vs ACI and ACI Variants, LSTM (Paper Sec. 6.5)
 
Compares the proposed **LACI** (Locally Adaptive Conformal Inference) with standard **ACI**, **Weighted ACI**, **DtACI** and **AgACI** on energy datasets. All methods run on top of the same LSTM quantile forecaster, so the comparison isolates how each method updates the miscoverage level α_i.
 
Corresponds to **Section 6.5, Table 6 and Figure 4** of the paper. The same comparison with GRU and TCN forecasters is in the Appendix C folder (`Appendix_D_GRU_TCN_Experiment`).
 
## Files
 
- `Exp_6.5_Final.ipynb`: **final code** for this experiment. Trains the LSTM, runs ACI, LACI, DtACI and AgACI online, and computes all local and global metrics reported in Table 6 and Figure 4.
- `Weighted_ACI_and_Corrected_LACI.ipynb`: code for the **Weighted ACI** baseline (recency-weighted ACI update, Eq. 18 in the paper), used for the Weighted ACI rows of Table 6.
- `Final_Results.txt`: aggregated numerical output of the final run.
- `results_all_methods_all_datasets.csv`: metrics for every method and dataset.
- `results_hydropower.csv`, `results_locations_1_2.csv`, `results_plants_1_2.csv`: per-group result files for Hydropower, Locations 1 and 2, and Solar Plants 1 and 2.
- `Helper_Scripts/`: metric computation, pinball loss, LSTM model, preprocessing and method implementations.
- `trajectories/`: per-dataset online trajectories of each method.
- `outputs/`: generated plots and intermediate outputs.
- `Exp_6.5_Decay_0.80.ipynb`, `Exp_6.5.ipynb`, `Test.ipynb`: earlier and exploratory versions (decay-factor trial, development, testing). They are not needed to reproduce the paper results.
## Run
 
```bash
jupyter notebook Exp_6.5_Final.ipynb               # ACI, LACI, DtACI, AgACI
jupyter notebook Weighted_ACI_and_Corrected_LACI.ipynb   # Weighted ACI
```
 
Run all cells in each notebook. Results are written to `Final_Results.txt` and the CSV files.
 
## Experimental Setup
 
| Parameter | Value |
|---|---|
| Forecaster | LSTM (hidden dim 64, 2 layers, dropout 0.1), pinball loss |
| Initial training window (T_init) | 5,000 samples |
| Initial epochs / online fine-tuning | 200 / 1 epoch every 6 steps |
| Sequence length | 48 |
| Train/calibration split | 0.5 |
| Target coverage (1 − α) | 0.90 |
| Local window (w) | 24 hours |
| ACI, Weighted ACI, LACI step size (γ) | 0.001 |
| LACI decay factor | 0.85 |
| LACI weighting epsilon | 1e-4 |
| DtACI γ candidates / interval size | {0.001, 0.002, 0.004, 0.008, 0.016} / 500 |
| AgACI γ candidates / epsilon | {0.001, 0.002, 0.004, 0.008, 0.016} / 0.001 |
| Optimizer / learning rate | Adam / 0.001 |
| Batch size / seed | 32 / 42 |
 
LACI replaces the recency weights of ACI with weights proportional to recency × local coverage error (Eq. 24 and 25), so that coverage failures during severe local under-coverage dominate the update of α_i.
 
## Metrics
 
- **Local:** LPICE (lower is better), LPIA (higher is better), LMPIW.
- **Global:** PICP, MPIW.
## Results (Table 6 of the paper)
 
LSTM, target coverage 1 − α = 0.90. Best LPICE and LPIA per dataset are in bold.
 
| Dataset | Method | LPICE ↓ | LPIA ↑ | LMPIW | PICP | MPIW |
|---|---|---|---|---|---|---|
| Amprion | ACI | 0.04 | 0.68 | 32.03 | 0.91 | 32.05 |
| | Weighted ACI | 0.04 | 0.66 | 31.83 | 0.91 | 31.85 |
| | **LACI** | **0.03** | **0.75** | 36.33 | 0.93 | 36.33 |
| | DtACI | 0.04 | 0.66 | 30.88 | 0.90 | 30.89 |
| | AgACI | 0.04 | 0.67 | 34.16 | 0.91 | 34.15 |
| TenneTTSO | ACI | 0.04 | 0.62 | 39.99 | 0.90 | 39.99 |
| | Weighted ACI | 0.04 | 0.62 | 42.06 | 0.90 | 42.04 |
| | **LACI** | **0.03** | **0.71** | 44.44 | 0.92 | 44.43 |
| | DtACI | 0.04 | 0.59 | 39.60 | 0.90 | 39.60 |
| | AgACI | 0.04 | 0.60 | 43.06 | 0.90 | 43.04 |
| TransnetBW | ACI | 0.03 | 0.62 | 11.82 | 0.90 | 11.81 |
| | Weighted ACI | 0.03 | 0.62 | 11.92 | 0.90 | 11.91 |
| | **LACI** | **0.01** | **0.80** | 13.28 | 0.94 | 13.26 |
| | DtACI | 0.03 | 0.62 | 11.79 | 0.90 | 11.78 |
| | AgACI | 0.03 | 0.61 | 12.79 | 0.90 | 12.77 |
| Hydropower | ACI | 0.06 | 0.54 | 202.22 | 0.88 | 202.91 |
| | Weighted ACI | 0.07 | 0.58 | 147.09 | 0.87 | 147.11 |
| | LACI | 0.05 | 0.59 | 211.04 | 0.90 | 211.60 |
| | DtACI | **0.04** | 0.54 | 192.49 | 0.90 | 193.30 |
| | AgACI | 0.05 | **0.60** | 204.11 | 0.90 | 204.76 |
| Location 1 | ACI | 0.03 | 0.58 | 0.28 | 0.90 | 0.28 |
| | Weighted ACI | 0.04 | 0.62 | 0.03 | 0.90 | 0.03 |
| | **LACI** | **0.02** | **0.74** | 0.33 | 0.93 | 0.33 |
| | DtACI | 0.03 | 0.55 | 0.28 | 0.90 | 0.28 |
| | AgACI | 0.03 | 0.57 | 0.28 | 0.90 | 0.28 |
| Location 2 | ACI | 0.04 | 0.55 | 0.20 | 0.89 | 0.20 |
| | Weighted ACI | 0.04 | 0.61 | 0.03 | 0.90 | 0.03 |
| | **LACI** | **0.01** | **0.76** | 0.25 | 0.93 | 0.25 |
| | DtACI | 0.03 | 0.56 | 0.20 | 0.90 | 0.20 |
| | AgACI | 0.03 | 0.56 | 0.21 | 0.90 | 0.21 |
| Plant 1 | ACI | 0.05 | 0.66 | 749.16 | 0.90 | 751.75 |
| | Weighted ACI | 0.07 | 0.62 | 1435.14 | 0.88 | 1434.73 |
| | **LACI** | **0.04** | **0.73** | 837.24 | 0.92 | 840.13 |
| | DtACI | **0.04** | 0.60 | 687.07 | 0.90 | 688.99 |
| | AgACI | **0.04** | 0.60 | 886.86 | 0.91 | 888.70 |
| Plant 2 | ACI | 0.05 | 0.60 | 4752.39 | 0.89 | 4755.29 |
| | Weighted ACI | 0.05 | 0.41 | 5630.51 | 0.88 | 5637.40 |
| | **LACI** | **0.03** | **0.75** | 7462.30 | 0.93 | 7456.76 |
| | DtACI | **0.03** | 0.56 | 4534.31 | 0.90 | 4541.26 |
| | AgACI | **0.03** | 0.61 | 5047.83 | 0.90 | 5051.95 |
 
## Summary
 
- ACI, DtACI and AgACI reach the global target (PICP about 0.90) but only meet the local target in about 54% to 68% of 24-hour windows.
- LACI has the best LPIA on 7 of 8 datasets in Table 6 (Hydropower is the exception, where AgACI is best at 0.60 vs 0.59).
- LACI has the lowest LPICE on 6 of 8 datasets (based on unrounded values; several are ties at two decimals).
- The gain is largest on TransnetBW, Location 1, Location 2 and Plant 2 (LPIA 0.74 to 0.80).
- The cost is wider intervals: LMPIW and MPIW are larger for LACI, and its PICP is slightly above the target (0.92 to 0.94 on most datasets).
- Weighted ACI performs similarly to ACI, so the improvement comes from the local-error weighting, not from recency weighting alone.
- Figure 4 in the paper plots the percentage LPIA gain and LPICE reduction of LACI over ACI per dataset.
 