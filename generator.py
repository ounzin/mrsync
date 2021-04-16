#!/usr/bin/env python3

import os,sys

def compare(list_src,list_dst):
    missing = []
    counter = 0
    out = 0
    a = len(list_src)

    for i in range(a):
        if list_src[i] in list_dst:
            pass
        else:
            missing.append(list_src[i])
    return missing


A = [{'filename':'tester','size':10},{'filename':'ahmed','size':10},{'filename':'padel','size':9}]
D = [{'filename':'aaeaeaea','size':39}]
B = [{'filename':'tester','size':10},{'filename':'ahmed','size':10},{'filename':'mshangama','size':13}]

C = compare(A,B)
print(C)

            
            
