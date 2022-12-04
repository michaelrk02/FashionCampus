import os

from FashionCampus.nn.prediction import predict

if __name__ == '__main__':
    image_file = input('Enter image file name: ')
    print('Predicting ...')
    prediction = predict(os.path.join('./nn/data/external_fashion_dataset', image_file))
    print('Result: %s' % (prediction))
