import torch
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

def has_black_bg(img, threshold=0.6, frame_length=1):
    # treshold image to BnW
    _, image = cv.threshold(img,230,255,cv.THRESH_BINARY)

    # total_pixel = image.shape[0] * image.shape[1]
    is_rgb = False
    black_pixel = 0
    if len(image.shape) == 3: # image is rgb
      black_pixel = np.array([0, 0, 0])
      is_rgb = True

    image_length = image.shape[0] # width and height are the same
    start_row_max = start_col_max = frame_length - 1
    end_row_max   = end_col_max   = image_length - frame_length

    count = 0
    total = 0
    for row, _ in enumerate(image):
        for col in range(row):
            if    (
                  row <= start_row_max or
                  row >= end_row_max or
                  col <= start_col_max or
                  col >= end_col_max
                ):
                total += 1
                if is_rgb:
                  if np.array_equal(image[row, col], black_pixel):
                    count += 1
                else:
                  if image[row, col] == black_pixel:
                    count += 1

    percent = count / total
    # print(f"{percent}, {count}, {total}, {percent >= threshold}")
    if percent >= threshold:
        return True
    else:
        return False

def process_image(image, to_tensor=False, frame_length=1):
  height = image.shape[0]
  width = image.shape[1]

  # make it square
  if height != width:
    side = abs(int((height - width) / 2))
    if height > width:
      image = image[side:side+width , 0:width]
      height = image.shape[0]

    else: # width > height
      image = image[0:height , side:side+height]
      width = image.shape[1]

  # invert image if has white bg
  if has_black_bg(image, frame_length=frame_length) == False:
    image = cv.bitwise_not(image)

  # make it grayscale
  image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)


  # rescale to 28x28
  # resize_factor = 28/height # or width cuz its a square
  image = cv.resize(image, (28, 28), interpolation= cv2.INTER_AREA)

  # # invert image if has white bg
  # if has_black_bg(image, frame_length=frame_length) == False:
  #   image = cv.bitwise_not(image)

  if to_tensor:
    # cast into float tensor
    image = torch.from_numpy(image)
    image = image.float()

    # add 1 dim at the start
    image = torch.unsqueeze(image, dim=0)

  return image
