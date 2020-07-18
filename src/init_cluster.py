#!/usr/bin/env python
# coding:utf-8


from __future__ import print_function


import json
import sys
import os
import random

"""
def select_inital(infos):
    centers =[]
    infos = [i for i in f1]
    total_list = [i for i in range(len(infos))]
    sampled = random.sample(total_list, clas_num)

    centers.append(sampled)
"""



def main():
    f1 = open(sys.argv[1])
    clas_num = int(sys.argv[2])
    infos = [i for i in f1]
    total_list = [i for i in range(len(infos))]
    sampled = random.sample(total_list, clas_num)
    #print (sampled)
    for i in range(len(sampled)):
        lines = infos[sampled[i]].strip().split("\t")
        value = lines[1]
        print (str(i)+"\t"+value)
if __name__ == "__main__":
    main()
