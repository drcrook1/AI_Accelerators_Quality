import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import numpy as np


def score_anomaly(model, data):
    dl = DataLoader(data)
    return score_anomaly_dl(model, dl)

def score_anomaly_dl(model, dataloader):
    model.eval()
    losses = []
    with torch.set_grad_enabled(False):
      for inputs in dataloader:
          outputs = model(inputs)
          criterion = nn.MSELoss()
          loss = criterion(outputs, inputs).data.item()
          losses.append(loss)

    return np.array(losses)

class AutoencoderModel(nn.Module):

  def __init__(self):

    super(AutoencoderModel, self).__init__()
    self.encoder = nn.Sequential(
      nn.Linear(5, 4),
      nn.Tanh(),
      nn.Linear(4, 3),
      nn.ReLU()
      )

    self.decoder = nn.Sequential(
      nn.Linear(3, 3),
      nn.Tanh(),
      nn.Linear(3, 5),
      nn.ReLU()
      )

  def forward(self, x):
    x = self.encoder(x)
    x = self.decoder(x)
    return x
