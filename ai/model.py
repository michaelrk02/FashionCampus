from torchvision import models
import torch
import torch.nn as nn
from collections import OrderedDict


class MobileNetCNNModel:
    def __init__(self, model_path):
        self.model_path = model_path

        self.__init_model()
        self.__load_model()
        self.__get_model()

    def __init_model(self):
        self.model = models.mobilenet_v2(pretrained=True)

        new_classifier = nn.Sequential(OrderedDict([
            ('fc1', nn.Linear(1280, 640)),
            ('relu1', nn.ReLU()),
            ('fc2', nn.Linear(640, 110)),
            ('relu2', nn.ReLU()),
            ('fc3', nn.Linear(110, 11)),
            ('output', nn.LogSoftmax(dim=1))
        ]))
        self.model.classifier = new_classifier

    def __load_model(self):
        self.model.load_state_dict(torch.load(self.model_path, map_location=torch.device('cpu')))

    def __get_model(self):
        return self.model

