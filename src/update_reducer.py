#!/usr/bin/env python
#coding:utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import json
import sys
import os
import numpy as np

def main():
    center_dict = dict()
    f1 = open("centers","r")
    #f1 = open("init_cluster","r")
    for line in f1:
        lines = line.strip().split("\t")
        ID = lines[0]
        value = lines[1]
        center_dict[ID] = value
    num = 0
    members=[]
    tmp_ID=None
    newcenter_dict=dict()

    for line in sys.stdin:
        lines = line.strip().split("\t")
        ID = lines[0]
        vector = json.loads(lines[1])

        if ID != tmp_ID and tmp_ID != None:
            center_value = np.sum(members,axis=0)/float(num)            
            newcenter_dict[tmp_ID] = center_value
            num=1
            members=[vector]
            tmp_ID = ID
        elif ID == tmp_ID:
            num+=1
            members.append(vector)
        elif tmp_ID == None:
            tmp_ID = ID
            num+=1
            members.append(vector) 

    ####最后一个
    center_value = np.sum(members,axis=0)/float(num)            
    newcenter_dict[tmp_ID] = center_value
    ####更新聚类中心
    for key in center_dict.keys():
        #print(key+"\t"+json.dumps(newcenter_dict[key].tolist()))
        if key in newcenter_dict.keys():
            print(key+"\t"+json.dumps(newcenter_dict[key].tolist()))
if __name__ == "__main__":
    main()
