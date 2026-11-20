# Appendix E — Empirical Validation of the Local-Error Assumption Across Different ACI Settings

Verifies that the core local-error assumption — E[LE⁽ᴸ⁾ᵢ − LEᵢ | errᵢ = 1] > 0 — holds
consistently across a range of ACI step sizes γ. The main Sec 6.3 experiment uses γ = 0.001;
this appendix repeats the validation at γ ∈ {0.004, 0.008, 0.016} to confirm the assumption
is not sensitive to the choice of γ and therefore provides a robust motivation for LACI.

## Files

- `Appendix_E_gamma_0.004.ipynb` — local-error assumption validation at γ = 0.004 (Table 9)
- `Appendix_E_gamma_0.008.ipynb` — local-error assumption validation at γ = 0.008 (Table 10)
- `Appendix_E_gamma_0.016.ipynb` — local-error assumption validation at γ = 0.016 (Table 11)
- `Helper_Scripts/` — shared metrics, models, loss functions, and preprocessing (same as Sec 6.3)

## Run

```bash
jupyter notebook Appendix_E_gamma_0.004.ipynb
jupyter notebook Appendix_E_gamma_0.008.ipynb
jupyter notebook Appendix_E_gamma_0.016.ipynb
```

Each notebook is self-contained and writes its results to a corresponding output file.

## Experimental Setup

All settings match Sec 6.3 exactly except for the step size γ:

| Parameter | Value |
|---|---|
| Architecture | LSTM (hidden dim: 64, layers: 1) |
| Initial training window (T_init) | 5,000 samples |
| Target coverage (1 − α) | 0.90 |
| Local evaluation window (w) | 24 hours |
| Decay factor (M) | 0.95 |
| γ values tested | 0.004, 0.008, 0.016 |
| Random seed | 42 |

## Results Summary (Tables 9–11 from paper)

The condition LE⁽ᴸ⁾ᵢ > LEᵢ holds at the majority of coverage-failure points for every
dataset and every γ value tested. The mean difference Δ = Mean(LE⁽ᴸ⁾ᵢ) − Mean(LEᵢ)
remains strictly positive throughout, and the percentage of qualifying failure points
stays above 55% in all cases.

| γ | Total #(errᵢ = 1) | Total qualifying | Overall % | Mean Δ |
|---|---|---|---|---|
| 0.004 | 3,447 | 2,244 | 65.10 | 0.041745 |
| 0.008 | 3,439 | 2,227 | 64.76 | 0.038739 |
| 0.016 | 3,441 | 2,180 | 63.35 | 0.033521 |

As γ increases, the overall percentage and mean Δ decrease slightly — consistent with more
aggressive adaptation partially correcting local errors before they accumulate — but the
assumption remains empirically valid across all settings, providing robust justification
for LACI's severity-weighted update.