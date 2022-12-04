import torch
from torch.autograd import Variable


class Inference:
    def __init__(self, model):
        self.model = model
        self.model.eval()

    def infer(self, image):
        #with torch.no_grad:
        var_image = Variable(image.view(1, 3, 28, 28)) # expected shape
        result = self.model(var_image)

        return result
    
