

import numpy as np

WINDOW = 24          
CWC_ETA = 50.0        



def _window_bounds(w):
    if w % 2 == 0:
        l = w // 2 - 1
    else:
        l = w // 2
    r = w // 2
    return l, r


def _iter_windows(n, w):
    l, r = _window_bounds(w)
    for i in range(n):
        start = i - l
        end = i + r  # inclusive
        if start < 0 or end >= n:
            continue
        yield i, start, end

# ------------------------------------------------------------------
def find_picp(lower, upper, predictions):
    """Eq. (1): global PICP."""
    lower = np.asarray(lower, dtype=np.float64)
    upper = np.asarray(upper, dtype=np.float64)
    predictions = np.asarray(predictions, dtype=np.float64)
    inside = (predictions >= lower) & (predictions <= upper)
    return float(np.mean(inside))


def find_mpiw(lower, upper, predictions=None):
    """Eq. (2): global MPIW."""
    lower = np.asarray(lower, dtype=np.float64)
    upper = np.asarray(upper, dtype=np.float64)
    return float(np.mean(upper - lower))


def find_local_picp(lower, upper, predictions, w=WINDOW):
    """Returns the list of per-index LPICP_i values (Eq. 11). The mean
    of this list is MLPICP / LPICP as defined in Eq. (12)."""
    lower = np.asarray(lower, dtype=np.float64)
    upper = np.asarray(upper, dtype=np.float64)
    predictions = np.asarray(predictions, dtype=np.float64)
    n = len(lower)

    covered = (predictions >= lower) & (predictions <= upper)

    local_picp = []
    for i, start, end in _iter_windows(n, w):
        cur = float(np.mean(covered[start:end + 1]))
        local_picp.append(cur)
    return local_picp


def find_mlpicp(local_picp):
    """Eq. (12): MLPICP = mean of LPICP_i over all valid windows."""
    if len(local_picp) == 0:
        return float("nan")
    return float(np.mean(local_picp))


def find_local_mpiw(lower, upper, predictions=None, w=WINDOW):
    """Returns the list of per-index LMPIW_i values (Eq. 16), using the
    SAME window convention as find_local_picp so the two align index
    for index (required for LCWC)."""
    lower = np.asarray(lower, dtype=np.float64)
    upper = np.asarray(upper, dtype=np.float64)
    n = len(lower)
    widths = upper - lower

    local_mpiw = []
    for i, start, end in _iter_windows(n, w):
        cur = float(np.mean(widths[start:end + 1]))
        local_mpiw.append(cur)
    return local_mpiw


def find_lmpiw(local_mpiw):
    """Eq. (17): LMPIW = mean of LMPIW_i over all valid windows."""
    if len(local_mpiw) == 0:
        return float("nan")
    return float(np.mean(local_mpiw))



def find_lpice(local_picp, req_cov):
    """Eq. (13): LE_i = max((1-alpha) - LPICP_i, 0).
    Eq. (14): LPICE = mean(LE_i) over all windows.
    NOTE: the paper defines LPICE as a plain mean of the shortfalls,
    NOT a root-mean-square. Use find_local_error_std separately if a
    dispersion measure of LE_i is wanted."""
    local_picp = np.asarray(local_picp, dtype=np.float64)
    if len(local_picp) == 0:
        return float("nan")
    le = np.maximum(req_cov - local_picp, 0.0)
    return float(np.mean(le))


def find_local_errors(local_picp, req_cov):
    """Helper: returns the raw per-window LE_i array (Eq. 13), useful
    for statistical tests or plotting error-severity distributions
    (e.g. Fig. 4/5/12 style analyses)."""
    local_picp = np.asarray(local_picp, dtype=np.float64)
    return np.maximum(req_cov - local_picp, 0.0)


def find_local_error_std(local_picp, req_cov):
    """Dispersion (population std) of LE_i -- NOT part of the paper's
    core five metrics, but retained as a diagnostic (matches the
    paper's remark under Eq. 14 that 'a more practical approach ...
    is through LPICE and the variance of LE_i')."""
    le = find_local_errors(local_picp, req_cov)
    if len(le) == 0:
        return float("nan")
    return float(np.std(le))


# ------------------------------------------------------------------
# LPIA (Eq. 15): fraction of windows meeting the LCR
# ------------------------------------------------------------------
def find_accuracy(local_picp, req_cov):
    """Eq. (15): LPIA = fraction of indices i with LPICP_i >= (1-alpha).
    (This is what the paper calls LPIA; in the empirical section this
    quantity is also reported under the column header 'Acc'.)"""
    local_picp = np.asarray(local_picp, dtype=np.float64)
    if len(local_picp) == 0:
        return float("nan")
    return float(np.mean(local_picp >= req_cov))


def find_lipce_mean(local_picp, req_cov):
    return 1.0 - find_accuracy(local_picp, req_cov)



def find_local_range(predictions, w=WINDOW):
    """R_i = max_{j in N_w(h_i)} x_j - min_{j in N_w(h_i)} x_j, computed
    over the true observations, using the same window convention as
    LPICP/LMPIW so indices line up (needed for Eq. 18)."""
    predictions = np.asarray(predictions, dtype=np.float64)
    n = len(predictions)
    r_list = []
    for i, start, end in _iter_windows(n, w):
        window_vals = predictions[start:end + 1]
        r_list.append(float(np.max(window_vals) - np.min(window_vals)))
    return r_list


def find_lcwc(lower, upper, predictions, req_cov, w=WINDOW, eta=CWC_ETA):

    lower = np.asarray(lower, dtype=np.float64)
    upper = np.asarray(upper, dtype=np.float64)
    predictions = np.asarray(predictions, dtype=np.float64)
    n = len(lower)

    covered = (predictions >= lower) & (predictions <= upper)
    widths = upper - lower

    lcwc_list = []
    for i, start, end in _iter_windows(n, w):
        lpicp_i = float(np.mean(covered[start:end + 1]))
        lmpiw_i = float(np.mean(widths[start:end + 1]))
        window_vals = predictions[start:end + 1]
        r_i = float(np.max(window_vals) - np.min(window_vals))

        if r_i > 0:
            nlmpiw_i = lmpiw_i / r_i
        else:
            nlmpiw_i = 0.0  # degenerate (constant) window

        gamma_i = 1.0 if lpicp_i < req_cov else 0.0
        lcwc_i = nlmpiw_i * (1.0 + gamma_i * np.exp(-eta * (lpicp_i - req_cov)))
        lcwc_list.append(lcwc_i)

    if len(lcwc_list) == 0:
        return float("nan")
    return float(np.mean(lcwc_list))


def summarize_all_metrics(y_true, y_lower, y_upper, alpha, w=WINDOW, eta=CWC_ETA,
                           time_taken=None):
    req_cov = 1.0 - alpha

    picp = find_picp(y_lower, y_upper, y_true)
    mpiw = find_mpiw(y_lower, y_upper, y_true)

    local_picp = find_local_picp(y_lower, y_upper, y_true, w=w)
    local_mpiw = find_local_mpiw(y_lower, y_upper, y_true, w=w)

    mlpicp = find_mlpicp(local_picp)
    lmpiw = find_lmpiw(local_mpiw)
    lpice = find_lpice(local_picp, req_cov)
    lpia = find_accuracy(local_picp, req_cov)
    lcwc = find_lcwc(y_lower, y_upper, y_true, req_cov, w=w, eta=eta)
    le_std = find_local_error_std(local_picp, req_cov)

    metrics = {
        "PICP": picp,
        "MPIW": mpiw,
        "MLPICP": mlpicp,
        "LPICE": lpice,
        "LPIA": lpia,
        "LMPIW": lmpiw,
        "LCWC": lcwc,
        "STD_LE": le_std,
        "n_local_windows": len(local_picp),
    }
    if time_taken is not None:
        metrics["time_sec"] = time_taken
    return metrics