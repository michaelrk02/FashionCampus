import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
from torch.autograd import Variable

import torchvision
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import confusion_matrix

import time
import os

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
device

class NewCNN(nn.Module):
  def __init__(self):
    super(NewCNN, self).__init__()

    self.layer1 = nn.Sequential(
        # 28x28x1
        nn.Conv2d(in_channels=1, out_channels=64, kernel_size=5, padding=2),
        nn.BatchNorm2d(64),
        nn.ReLU(),
        nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1),
        nn.BatchNorm2d(64),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2, stride=2)
        # 14x14x64
    )

    self.layer2 = nn.Sequential(
        # 14x14x64
        nn.Conv2d(in_channels=64, out_channels=32, kernel_size=5, padding=2),
        nn.BatchNorm2d(32),
        nn.ReLU(),
        nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, padding=1),
        nn.BatchNorm2d(32),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2, stride=2)
        # 7x7x32
    )

    self.fc1 = nn.Linear(in_features=7*7*32, out_features=110)
    self.fc2 = nn.Linear(in_features=110, out_features=11) # out_features from 10 to 11

  def forward(self, x):
    x = self.layer1(x)
    x = self.layer2(x)
    x = x.view(x.size(0), -1)
    x = self.fc1(x)
    x = self.fc2(x)

    return x

def get_filename(model):
  if isinstance(model, NewCNN):
    return "./nn/data/NewCNN_checkpoint_extended_dataset.pth.tor"

def load_model(model, optimizer):
  filename = get_filename(model)
  if os.path.exists(filename) == False:
    print("=> load model failed!")
    return
  checkpoint = torch.load(filename)
  model.load_state_dict(checkpoint['state_dict'])
  optimizer.load_state_dict(checkpoint['optimizer'])
  print("=> model loaded!")

model = NewCNN()
learning_rate = 0.001
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

load_model(model, optimizer)
