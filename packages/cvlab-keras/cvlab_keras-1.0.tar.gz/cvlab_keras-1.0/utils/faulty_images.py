#!/usr/bin/env python
import os
import matplotlib.pyplot as plt

if __name__ == "__main__":
    input_path = "C:/Users/kazek/PycharmProjects/cvlab/cvlab_keras/data/test"

    for root, dirs, files in os.walk(input_path):
        for dir in dirs:
            # label = root.split("\\")[1]
            # f.write(os.path.join(root, file) + " " + label + "\n")
            # try:
            #     plt.imread(os.path.join(root, file))
            # except SyntaxError:
            #     print(os.path.join(root, file))
            print(dir)

    lista = ['a1', 'a2', '1', 'a12', 'a13']
    lista.sort()
    print(lista)