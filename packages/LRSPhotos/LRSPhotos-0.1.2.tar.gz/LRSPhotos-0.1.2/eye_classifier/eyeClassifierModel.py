import numpy as np
import torch
from torch import nn
import torch.nn.functional as F

class EyeClassifierModel(torch.nn.Module):
  """A simple convolutional network.
  
  Map from inputs with shape [batch_size, 1, height, width] to
  outputs with shape [batch_size, 1].
  """
  
  def __init__(self):
    super().__init__()
    self.conv1=nn.Conv2d(3,96,5,3,2)
    self.conv2=nn.Conv2d(96,192,5,padding=2)
    self.conv3=nn.Conv2d(192,256,3,padding=1)
    self.conv4=nn.Conv2d(256,256,3,padding=1)
    self.conv5=nn.Conv2d(256,128,3,padding=1)
    self.fc = nn.Sequential(
            nn.Dropout(p=0.1),
            nn.Linear(8192, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.1),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, 2),
            nn.LogSoftmax(dim=1)
    )
    
  def forward(self, x):
    out = self.conv1(x)
    out = F.relu(out)
    out = F.max_pool2d(out, 3, 2)
    out = self.conv2(out)
    out = F.relu(out)
    out = F.max_pool2d(out, 3, 2)
    out = self.conv3(out)
    out = F.relu(out)
    out = self.conv4(out)
    out = F.relu(out)
    out = self.conv5(out)
    out = F.relu(out)
    out = F.max_pool2d(out, 3, 2)
    out = torch.flatten(out, 1)
    out = self.fc(out)
    return out
