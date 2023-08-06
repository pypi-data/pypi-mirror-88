#!/usr/bin/env python
import os
import time

if __name__ == "__main__":
    input_path = "C:/Users/kazek/PycharmProjects/cvlab/cvlab_keras/data/mnist/training"
    output_path = "C:/Users/kazek/PycharmProjects/cvlab/cvlab_keras/data/mnist.txt"

    start = time.clock()
    images_list = []
    subdirectories_paths = [f.path for f in os.scandir(input_path) if f.is_dir()]
    for path in subdirectories_paths:
        dir = os.path.basename(path)
        for root, dirs, files in os.walk(path):
            for file in files:
                label = root.split("\\")[1]
                images_list.append([os.path.join(root, file), label])
    print(time.clock() - start)
    a = images_list
    # input_path = "E:/Studia/inz/cvlab/cvlab_keras/data/mnist/training/"
    # output_path = "E:/Studia/inz/cvlab/cvlab_keras/data/cats_and_dogs.txt"
    #
    # f = open(output_path, "w")
    #
    # filenames = os.listdir("./dogs-vs-cats/train")
    # categories = []
    # for f_name in filenames:
    #     label = f_name.split('.')[0]
    #     f.write(f_name + " " + label + "\n")
    #
    # f.close()
