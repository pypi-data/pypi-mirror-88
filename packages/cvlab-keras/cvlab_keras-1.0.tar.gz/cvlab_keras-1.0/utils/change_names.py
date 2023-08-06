#!/usr/bin/env python
import os

if __name__ == "__main__":
    path = "C:/Users/kazek/PycharmProjects/cvlab/cvlab_keras/data/mnist.txt"

    fin = open(path, "rt")
    #read file contents to string
    data = fin.read()
    #replace all occurrences of the required string
    data = data.replace('\\', '/')
    #close the input file
    fin.close()
    #open the input file in write mode
    fin = open(path, "wt")
    #overrite the input file with the resulting data
    fin.write(data)
    #close the file
    fin.close()
