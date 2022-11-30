import torch

from torch.autograd import Variable

from FashionCampus.nn.loader import extract_label, label_mapping, load_images_from_folder, output_label
from FashionCampus.nn.preprocessor import process_image
from FashionCampus.nn.model import model

ext_images, ext_filenames = load_images_from_folder("./nn/data/external_fashion_dataset")

preprocessed_ext_images_tensor = []
for image in ext_images:
  image = process_image(image, to_tensor=True)
  preprocessed_ext_images_tensor.append(image)

print(f"loaded {len(preprocessed_ext_images_tensor)} images")

correct_count = 0
for i in range(len(preprocessed_ext_images_tensor)):
  test = Variable(preprocessed_ext_images_tensor[i].view(1, 1, 28, 28))
  output = model(test)
  prediction = torch.max(output, 1)[1]
  label_name = extract_label(ext_filenames[i])

  label = label_mapping( label_name )

  print("=====================")
  for idx, (val) in enumerate(output[0]):
    print(f"{output_label(idx)}: {val:.3f}")

  if(prediction == int(label)): correct_count+=1

  print(f"[{i}] prediction: {output_label(prediction)}, actual: {label_name}")
  print("=====================")

print(f"==> Correct: {correct_count}/{len(ext_filenames)}")
