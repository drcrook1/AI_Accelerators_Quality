from torch import nn

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
