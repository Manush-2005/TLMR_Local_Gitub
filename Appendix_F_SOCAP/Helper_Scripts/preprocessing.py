import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler

def pad(arr, length):
    arr = np.array(arr, dtype=np.float32)
    if len(arr) < length:
        arr = np.concatenate([arr, np.full(length - len(arr), np.nan)])
    return arr

class SeqDataset(Dataset):
    def __init__(self, series, seq_len):
        self.X, self.y = [], []
        for i in range(len(series) - seq_len):
            self.X.append(series[i:i+seq_len])
            self.y.append(series[i+seq_len])
        self.X, self.y = np.array(self.X), np.array(self.y)
    def __len__(self): return len(self.X)
    def __getitem__(self, idx):
        return torch.tensor(self.X[idx], dtype=torch.float32), torch.tensor(self.y[idx], dtype=torch.float32)

def load_data(filepath, seq_len=24, train_split=0.8):
    df = pd.read_csv(filepath)
    y = df.iloc[:, 1:].sum(axis=1).values.astype(float)

    scaler = StandardScaler()
    y_scaled = scaler.fit_transform(y.reshape(-1, 1)).flatten()

    split_idx = int(len(y_scaled) * train_split)
    train_series = y_scaled[:split_idx]
    test_series = y_scaled[split_idx - seq_len:]

    train_dataset = SeqDataset(train_series, seq_len)
    test_dataset = SeqDataset(test_series, seq_len)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    return train_loader, test_dataset, scaler, y, y_scaled, split_idx
def load_data_1(filepath, seq_len=24):
    df = pd.read_csv(filepath)
    y = df.iloc[:, 1:].sum(axis=1).values.astype(float)
    scaler = StandardScaler()
    y_scaled = scaler.fit_transform(y.reshape(-1, 1)).flatten()
    full_dataset = SeqDataset(y_scaled, seq_len)
    return full_dataset, scaler, y, y_scaled


def load_data_long(filepath, seq_len=96):
    """
    Converts the 15-min stamp CSV into a single long univariate time series 
    by flattening the daily 15-minute values into one sequence.
    """
    # Load the dataset
    df = pd.read_csv(filepath)

    df = df[:500]
    
    # Select all columns except 'Date' (iloc[:, 1:])
    # .values returns a 2D array (Days, 96)
    # .flatten() converts it into a 1D array of (Days * 96) values
    y = df.iloc[:, 1:].values.flatten().astype(float)
    y=y[::4]
    
    
    # Scale the data
    scaler = StandardScaler()
    y_scaled = scaler.fit_transform(y.reshape(-1, 1)).flatten()
    
    # Initialize your Dataset class
    # Note: seq_len here represents the number of 15-minute points (e.g., 96 = 1 day)
    full_dataset = SeqDataset(y_scaled, seq_len)
    
    return full_dataset, scaler, y, y_scaled