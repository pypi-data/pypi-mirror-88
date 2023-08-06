import os.path
from multiprocessing import Pool
import sys
import time
import matplotlib.pyplot as plt

def process_file(file):
    """ Process one file: count number of lines and words """
    image = plt.imread(file[0])
    label = file[1]
    return image, label


def process_files_parallel(images):
    """ Process each file in parallel via Poll.map() """
    pool=Pool()
    results=pool.map(process_file, images)
    return results


def process_files(images):
    """ Process each file in via map() """
    results=[process_file(file) for file in images]
    return results


if __name__ == '__main__':
    with open('E:/Studia/inz/cvlab/cvlab_keras/data/mnist.txt') as file:
        images = [line.rstrip().split(" ") for line in file]

    for i in range(250):
        start=time.clock()
        results1 = process_files(images[i*128:(i+1)*128])
        print("process_files()", i, ": ", time.clock()-start)

    # start2=time.clock()
    # results2 = process_files_parallel(images[:100])
    # print("process_files_parallel()", time.clock()-start2)