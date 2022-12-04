from torchvision import models
import torch
import torch.nn as nn
from collections import OrderedDict


class MobileNetCNNModel:
    def __init__(self, model_path):
        self.model_path = model_path

        self.__load_model()
        self.__get_model()

    def __load_model(self):
        self.model = torch.load(self.model_path, map_location=torch.device('cpu'))

    def __get_model(self):
        return self.model

