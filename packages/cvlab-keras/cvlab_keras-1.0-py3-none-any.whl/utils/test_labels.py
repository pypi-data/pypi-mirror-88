#!/usr/bin/env python
from tensorflow import keras

if __name__ == "__main__":
    labels = ["kot", "pies", "mysz"]

    dataset = keras.preprocessing.image_dataset_from_directory("E:/Studia/inz/cvlab/cvlab_keras/data/mnist/testing",
                                                               image_size=(28,28),
                                                               color_mode="grayscale",
                                                               batch_size=128)

    labels_categorical = keras.utils.to_categorical(labels)
    print(labels_categorical)
