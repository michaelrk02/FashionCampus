import torch
import cv2 as cv
import numpy as np
# import opencv-python as cv


class PreProcessing:
    def __init__(self):
        self.to_tensor = True  # model take input in tensor
        self.grayscale_to_rgb = True  # mobilenet v2 take image input in 3 channels (rgb)
        self.resize_to = 28  # MNIST size
        self.threshold = 0.6  # for black bg checking
        self.frame_length = 1  # for black bg checking

    def __has_black_bg(self, image):
        _, image = cv.threshold(image, 230, 255, cv.THRESH_BINARY)

        is_rgb = False
        black_pixel = 0
        if len(image.shape) == 3:  # image is rgb
            black_pixel = np.array([0, 0, 0])
            is_rgb = True

        image_length = image.shape[0]  # width and height are the same
        start_row_max = start_col_max = self.frame_length - 1
        end_row_max = end_col_max = image_length - self.frame_length

        count = 0
        total = 0
        for row, _ in enumerate(image):
            for col in range(row):
                if (
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
        if percent >= self.threshold:
            return True
        else:
            return False

    def process(self, image):
        height = image.shape[0]
        width = image.shape[1]

        # make it square
        if height != width:
            side = abs(int((height - width) / 2))
            if height > width:
                image = image[side:side + width, 0:width]
            else:  # width > height
                image = image[0:height, side:side + height]

        # invert image if doesnt have black bg
        if not self.__has_black_bg(image):
            image = cv.bitwise_not(image)

        # make it grayscale
        image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

        image = cv.resize(image, (self.resize_to, self.resize_to), interpolation=cv.INTER_AREA)

        if self.to_tensor:
            # cast into float tensor
            image = torch.from_numpy(image)
            image = image.float()

            # add 1 dim at the start
            image.unsqueeze_(0)
            if self.grayscale_to_rgb:
                image = image.repeat(3, 1, 1)

        return image
