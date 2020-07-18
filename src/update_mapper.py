#!/usr/bin/env python
#coding:utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import json
import sys
import os
import numpy as np

def cosine(v1,v2):
    vector1 = np.array(v1)
    vector2 = np.array(v2)
    op7= 1-np.dot(vector1,vector2)/(np.linalg.norm(vector1)*(np.linalg.norm(vector2)))
    return op7


def main():
    center_dict = dict()
    f1 = open("centers","r")
    #f1 = open("./init_cluster","r")
    for line in f1:
        lines = line.strip().split("\t")
        ID = lines[0]
        value = lines[1]
        center_dict[ID] = value

    for line in sys.stdin:

        center_index=None
        min_dis = float(sys.maxsize) 

        lines = line.strip().split("\t")
        did = lines[0]
        vector = json.loads(lines[1])
        for key in center_dict.keys():
            center = json.loads(center_dict[key])
            dis = cosine(center,vector)
            #print (dis)
            if dis < min_dis:
                min_dis=dis
                center_index = key

        vector = json.dumps(vector)
        #print (center_index)
        print (center_index+"\t"+vector+"\t"+did)

            

if __name__=="__main__":
    main()
