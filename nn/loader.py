import cv2
import os
import re
import torch

def load_image(path):
  return cv2.imread(os.path.join(path))

def load_images_from_folder(folder):
    images = []
    filenames = []
    for filename in os.listdir(folder):
        filenames.append(filename)
        img = load_image(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
        else:
            print(f"{filename} failed to be read" )
    return images, filenames

def label_mapping(label):
  label_mapping = {
    "T-shirt": 0,
    "Trouser": 1,
    "Pullover": 2,
    "Dress": 3,
    "Coat": 4,
    "Sandal": 5,
    "Shirt": 6,
    "Sneakers": 7,
    "Bag": 8,
    "Ankle Boot": 9,
    "Hat": 10 # new class
  }
  input = (label.item() if type(label) == torch.Tensor else label)
  return label_mapping[input]

def extract_label(filename):
  result = re.search("(T-shirt|Pullover|Dress|Trouser|Shirt|Ankle Boot|Sneakers|Sandal|Coat|Bag).*", filename).group(1)
  return result

def output_label(label):
    output_mapping = {
      0: "T-shirt",
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
    input = (label.item() if type(label) == torch.Tensor else label)
    return output_mapping[input]
