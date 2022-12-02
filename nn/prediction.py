import torch

from torch.autograd import Variable

from FashionCampus.nn.loader import load_image, output_label
from FashionCampus.nn.preprocessor import process_image
from FashionCampus.nn.model import model

def predict(path):
    image = load_image(path)
    image = process_image(image, to_tensor = True)
    test = Variable(image.view(1, 1, 28, 28))
    output = model(test)
    prediction = torch.max(output, 1)[1]
    label = output_label(prediction)
    return label
