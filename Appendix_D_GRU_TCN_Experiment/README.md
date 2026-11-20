# Appendix D — LACI vs. ACI Variants: GRU and TCN Architecture Experiments

Repeats the Sec 6.4 comparison (LACI vs. ACI, DtACI, AgACI) using GRU and TCN architectures
in place of LSTM. Demonstrates that LACI's local calibration improvements are
architecture-independent and are not an artefact of the LSTM backbone used in the main results.

## Files

- `Appedix_D_Exp_GRU.ipynb` — full experiment with GRU architecture (Table 7 of the paper)
- `Appedix_D_Exp_TCN.ipynb` — full experiment with TCN architecture (Table 8 of the paper)
- `Helper_Scripts/calculate_metrics.py` — LPIA, LPICE, MLPICP, LMPIW, LCWC, PICP, MPIW computation
- `Helper_Scripts/loss_functions.py` — pinball loss implementation for quantile training
- `Helper_Scripts/models.py` — GRU and TCN architecture definitions
- `Helper_Scripts/models_TLMR.py` — architecture variants used for TMLR submission
- `Helper_Scripts/preprocessing.py` — sliding-window construction, train/calibration split, normalization

## Run

GRU experiment:

```bash
jupyter notebook Appedix_D_Exp_GRU.ipynb
```

TCN experiment:

```bash
jupyter notebook Appedix_D_Exp_TCN.ipynb
```

## Architecture Specifications

| Parameter | GRU | TCN |
|---|---|---|
| Input dimension | 1 | 1 |
| Hidden dim / Channels | 64 | [32, 32, 32, 32] |
| Layers | 2 | — |
| Kernel size | — | 2 |
| Dropout | — | 0.2 |
| Output head | Linear(64, 1) | Linear(32, 1) |

All other settings (T_init, fine-tuning cadence, target coverage, window size, γ, seed)
match the main Sec 6.4 setup exactly — see `03. Exp_6.4` README for full hyperparameter table.

## Key Results

**GRU (Table 7):** LACI achieves the best LPIA in **8/9** datasets and best LPICE in **7/9**
datasets over ACI, DtACI, and AgACI. Average LPIA: ACI = 0.63, DtACI = 0.60,
AgACI = 0.59, **LACI = 0.66**.

**TCN (Table 8):** Results are more mixed due to the TCN's shorter effective receptive field,
but LACI still achieves the best LPIA in **6/9** datasets and remains competitive on LPICE,
confirming that the local calibration advantage generalises beyond recurrent architectures.