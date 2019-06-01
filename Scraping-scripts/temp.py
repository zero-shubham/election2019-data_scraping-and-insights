import os
import re
import csv


pathToStates ="./data/pageDetails/state.txt"

with open(pathToStates, "r") as states:
    for state in states:
        path = "./data/constituencyWise/"
        dirName = '_'.join((state.split('-')[0]).split(' '))
        path = path+dirName+'/'
        for file in os.listdir(path):
            with open(path+file, "r") as f:
                print(f.readlines(), '\n\n=============\n')