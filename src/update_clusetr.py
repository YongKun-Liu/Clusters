#!/usr/bin/env python
# coding:utf-8


from __future__ import print_function


import json
import sys
import os

def main():
    f1 = open(sys.argv[1])
    new_cluster = dict((i.strip().split("\t")[0],i) for i in f1)

    f2 = open(sys.argv[2])
    init_cluster = dict((i.strip().split("\t")[0],i) for i in f2)
    
    K = int(sys.argv[3])
    if len(new_cluster) == K:
        for key in new_cluster:
            print (new_cluster[key].strip())
    else:
        for key in init_cluster:
            if key in new_cluster:
                print (new_cluster[key].strip())
            else:
                print (init_cluster[key].strip())

if __name__ == "__main__":
    main()
