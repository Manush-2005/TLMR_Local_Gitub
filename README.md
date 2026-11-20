
# Local Matters: Calibration Requirements in Online Conformal Forecasting
 
Code and datasets for the paper **"Local Matters: Calibration Requirements in Online Conformal Forecasting"** (submitted to TMLR).
 
## Overview
 
Probabilistic forecasts in energy systems are usually evaluated with global metrics (PICP, MPIW), which can hide long stretches where prediction intervals repeatedly fail to cover observations. This work:
 
- formalises calibration at different granularities and highlights the **Local Calibration Requirement (LCR)** for sequential forecasting;
- proposes local metrics: **LPICP, LPICE, LPIA, LMPIW, LCWC**;
- shows that Quantile Regression (QR) does not reliably meet global calibration, and that ACI meets global calibration but only partially meets local calibration (exact identity linking local coverage error to the drift of the miscoverage level);
- proposes **LACI (Locally Adaptive Conformal Inference)**, a variant of ACI that weights past coverage errors by their local coverage error;
- evaluates LACI on nine energy datasets and in an imbalance-cost case study.
## Repository Structure
 
Folder names follow the experiment order in this repository; the table maps each folder to the corresponding section of the paper.
 
| Folder | Paper section | Description |
|---|---|---|
| `05.Synthetic_Exp` | Sec. 6.2 | AR(1) synthetic experiment with abrupt variance shifts (t = 1800, 2800, 3800, 4800, 5800) comparing ACI vs LACI local behaviour (Tables 2, 3; Figure 2). |
| `01. Exp_6.2_ACI_vs_QR_Experiment` | Sec. 6.3 | ACI vs Quantile Regression on local and global metrics, LSTM, nine datasets (Table 4; Figure 3). |
| `02. Exp_6.3_Emprical_Validation_of_Assumption` | Sec. 6.4 | Empirical check of the abrupt local-error assumption, condition (23), for ACI (Table 5). |
| `03. Exp_6.4_LACI_vs_ACI_Variants_Exp_LSTM` | Sec. 6.5 | LACI vs ACI, Weighted ACI, DtACI and AgACI with LSTM (Table 6; Figure 4). |
| `04. Case_Study_Experiment` | Sec. 7 | Imbalance-cost case study with P_mis = 200, λ = 0.1 (Table 7). |
| `Appendix_D_GRU_TCN_Experiment` | Appendix C | Repeat of Sec. 6.5 with GRU and TCN architectures (Tables 9, 10). |
| `Appendix_E_Different_ACI_Settings_Assumption` | Appendix D | Condition (23) checked for γ ∈ {0.004, 0.008, 0.016} (Tables 11–13). |
| `Appendix_F_SOCAP` | Appendix E | LACI vs SACOP (threshold-adaptation baseline), (Table 14). |
| `Datasets` | Table 1 | Datasets used in all experiments. |

 
## Datasets
 
All datasets are univariate, hourly (except Hydropower, daily).
 
| Type | Dataset | Points | Source |
|---|---|---|---|
| Wind | 50Hertz, TransnetBW, TenneT TSO, Amprion | 9,957 each | Germany, Netztransparenz (Kaggle) |
| Wind | Location 1, Location 2 | 9,929 each | Beijing, China (Kaggle) |
| Hydro | HydroPower (daily) | 1,782 | Kaptai, Bangladesh (Kaggle) |
| Solar | Solar Plant 1, Solar Plant 2 | 9,308 / 9,561 | India (Kaggle) |
 


## Metrics
 
- **Global:** PICP, MPIW.
- **Local (window w = 24):** LPICP (local coverage), LPICE (average local coverage error), LPIA (fraction of windows meeting target coverage), LMPIW (local interval width), LCWC (local coverage-width criterion).
## Methods Compared
 
- QR (no conformal correction)
- ACI and Weighted ACI (Gibbs & Candès, 2021)
- DtACI (Gibbs & Candès, 2024)
- AgACI (Zaffran et al., 2022)
- SACOP / SAOCP (Bhatnagar et al., 2023), appendix comparison
- **LACI (proposed)**
## Reproducing the Experiments
 
1. Clone the repository:
```bash
git clone https://github.com/Manush-2005/TLMR_Local_Gitub.git
cd TLMR_Local_Gitub
```
2. Install dependencies (Python 3, PyTorch, NumPy, pandas, scikit-learn, matplotlib).
3. Make sure the data files are in `Datasets/`.
4. Open the notebooks/scripts inside the experiment folder you want (see the table above) and run them in order. Each folder contains the code and outputs for the tables and figures of its paper section.
## Key Results (summary)
 
- QR does not consistently meet global calibration; ACI reaches ~0.90 PICP but only about 61% LPIA on average.
- LACI raises average LPIA to about 68%, achieving the best LPIA in most datasets at a modest cost in interval width.
- The gains hold across LSTM, GRU and TCN forecasters.
- In the imbalance-cost case study, LACI gives the lowest cost in 5 of 8 cases.
## Citation
 
```bibtex
@article{laci2026,
  title   = {Local Matters: Calibration Requirements in Online Conformal Forecasting},
  author  = {Anonymous},
  journal = {Transactions on Machine Learning Research (under review)},
  year    = {2026}
}
```
 
## License
 
Add a license of your choice (e.g., MIT) before making the repository public.
