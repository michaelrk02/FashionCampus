import torch


class PostProcessing:
    def __init__(self):
        self.label_map = {
          0: "T-shirt/Top",
          1: "Trouser",
          2: "Pullover",
          3: "Dress",
          4: "Coat",
          5: "Sandal",
          6: "Shirt",
          7: "Sneaker",
          8: "Bag",
          9: "Ankle Boot",
          10: "Hat"
        }

    def predict(self, result, with_id=False):
        prediction_id = torch.max(result, 1)[1]  # highest score from 11 classifier neuron
        prediction_label = self.label_map[prediction_id]
        if with_id:
            return prediction_id, prediction_label
        else:
            return prediction_label

    def get_label_map(self):
        return self.label_map
    