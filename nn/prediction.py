import cv2

from FashionCampus.nn.preprocessing import PreProcessing
from FashionCampus.nn.model import MobileNetCNNModel
from FashionCampus.nn.postprocessing import PostProcessing
from FashionCampus.nn.inference import Inference

MODEL_PATH = "./nn/data/MobileNetCNN_epo5_model.pth"

def predict(path):
    pre_proc = PreProcessing()
    model = MobileNetCNNModel(MODEL_PATH)
    inf = Inference(model.model)
    post_proc = PostProcessing()

    image = cv2.imread(path)
    image = pre_proc.process(image)
    result = inf.infer(image)
    prediction = post_proc.predict(result)

    return prediction
