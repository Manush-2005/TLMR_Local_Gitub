import torch


def quantile_loss(y_true, y_pred, q=0.5):
    """
    Quantile (pinball) loss for quantile regression.
    Loss is asymmetric: penalizes over-prediction and under-prediction differently.
    """
    y_true = y_true.view(-1)
    y_pred = y_pred.squeeze()
    errors = y_true - y_pred
    
    loss = torch.where(errors >= 0, q * errors, (q - 1) * errors)
    return loss.mean()