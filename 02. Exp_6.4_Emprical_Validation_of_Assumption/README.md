# Empirical Validation of the Assumption at Coverage Failures (Paper Sec. 6.4)

Checks whether the abrupt local-error condition (Eq. 23) used to motivate LACI holds in practice. ACI is run online on top of an LSTM probabilistic forecaster on nine energy datasets, and at every coverage failure we test whether the local coverage error exceeds its recency-weighted average:

LE_s^(L) > mean-LE_s^(L)  (recency-weighted average of past local errors, decay M = 0.95)

If a large share of coverage failures satisfy this, the trajectory obeys condition (23): the number of such failures is at least |F_i| / p, with p < 2 meaning more than half of all failures are "abrupt".

Corresponds to **Section 6.4 and Table 5** of the paper. The same check for other values of γ (Tables 11 to 13) is in the Appendix D experiment folder.

## Files

- `Exp_6.4_Final.ipynb`: main notebook. Runs ACI with the LSTM on all datasets and counts abrupt local coverage errors at coverage failures.
- `Final_Results.txt`: aggregated numerical output of the notebook run.
- `aci_failure_audit/`: per-dataset audit of coverage failures.
- `lemma3_results/`: results of the check supporting the theoretical analysis.
- `outputs/`: other generated outputs (trajectories, intermediate files).

## Run

```bash
jupyter notebook Exp_6.4_Final.ipynb
```

Run all cells. Results are written to `Final_Results.txt` and the output folders above.

## Experimental Setup

| Parameter | Value |
|---|---|
| Forecaster | LSTM (hidden dim 64, 2 layers, dropout 0.1), pinball loss |
| Initial training samples (T_init) | 5,000 |
| Online fine-tuning | 1 epoch every 6 steps |
| Conformal method | ACI, γ = 0.001 |
| Target coverage (1 − α) | 0.90 |
| Local window (w) | 24 hours |
| Decay factor for the weighted average of local errors (M) | 0.95 |
| Random seed | 42 |

## Results (Table 5 of the paper)

Column meanings:
- `#(err=1)`: number of coverage failures.
- `# abrupt`: failures with LE_s^(L) > weighted-average local error.
- `Mean LE_s`: mean local error at failures.
- `Mean baseline`: mean weighted-average local error at failures.
- `Δ`: mean difference.

| Dataset | #(err=1) | # abrupt | % abrupt | Mean LE_s | Mean baseline | Δ |
|---|---|---|---|---|---|---|
| 50Hertz | 388 | 233 | 60.05 | 0.09 | 0.05 | 0.04 |
| Amprion | 366 | 218 | 59.56 | 0.11 | 0.07 | 0.04 |
| Location 1 | 482 | 285 | 59.13 | 0.08 | 0.05 | 0.04 |
| Location 2 | 433 | 239 | 55.20 | 0.08 | 0.05 | 0.04 |
| Plant 1 Generation | 231 | 139 | 60.17 | 0.22 | 0.19 | 0.02 |
| Plant 2 Generation | 416 | 324 | 77.88 | 0.14 | 0.10 | 0.03 |
| TenneTTSO | 401 | 238 | 59.35 | 0.10 | 0.06 | 0.04 |
| TransnetBW | 420 | 241 | 57.38 | 0.06 | 0.03 | 0.03 |
| Hydropower | 161 | 109 | 67.70 | 0.18 | 0.10 | 0.09 |
| **Total** | **3298** | **2026** | **61.43** | **0.11** | **0.07** | **0.04** |

## Summary

- Across all datasets, about 61% of ACI coverage failures (2026 of 3298) occur with a local error above the weighted average, so the abrupt errors are the clear majority.
- Every dataset is above 50% (lowest: Location 2 at 55.20%, highest: Plant 2 at 77.88%), so condition (23) holds with p < 2 everywhere.
- The mean local error at failures is higher than the weighted-average baseline on every dataset (pooled Δ = 0.04).
- This supports the design of LACI, which gives higher weight to failures with larger local errors (Lemma 1, Proposition 2).
- The behaviour does not depend on γ; see the Appendix D folder for γ ∈ {0.004, 0.008, 0.016} (pooled 62.06%, 62.35%, 62.15%).
