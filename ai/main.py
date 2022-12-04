from preprocessing import PreProcessing
from model import MobileNetCNNModel
from postprocessing import PostProcessing
from inference import Inference

MODEL_PATH = ""

if __name__ == "__main__":
    pre_proc = PreProcessing()
    model = MobileNetCNNModel(MODEL_PATH)
    inf = Inference(model)
    post_proc = PostProcessing()

    image = None  #TODO: connect image from BE to AI
    image = pre_proc.process(image)
    result = inf.infer(image)
    prediction = post_proc.predict(result)

    print(prediction)
