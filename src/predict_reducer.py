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
    member_dict=dict()

    for line in sys.stdin:
        lines = line.strip().split("\t")
        ID = lines[0]
        vector = json.loads(lines[1])
        did = lines[2]
        if ID != tmp_ID and tmp_ID != None:
            member_dict[tmp_ID] = members
            num=1
            members=[did]
            tmp_ID = ID
        elif ID == tmp_ID:
            num+=1
            members.append(did)
        elif tmp_ID == None:
            tmp_ID = ID
            num+=1
            members.append(did)

    member_dict[tmp_ID] = members
    #print (member_dict.keys())
    ####预测结果
    for key in member_dict.keys():
        if key != None:
            print(key+"\t"+json.dumps(member_dict[key]))

if __name__ == "__main__":
    main()
