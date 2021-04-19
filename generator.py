#!/usr/bin/env python3

import os,sys

def is_different(a,b): #return True if a is different from b
   
    if a['relative_path'] != b['relative_path']:
        return True
    elif a['st_size'] != b['st_size']:
        return True
    elif a['st_mtime'] != b['st_mtime']:
        return True
    else:
        return False

def compare(list_src,list_dst):
    missing = []
    a = len(list_src)
    for i in range(a):
        b = list_src[i]
        if list_src[i] in list_dst:
            pass
        else:
            missing.append(list_src[i])
    return missing


A = [{'filename':'tester','size':10},{'filename':'ahmed','size':10},{'filename':'padel','size':9}]
D = [{'filename':'aaeaeaea','size':39}]
B = [{'filename':'tester','size':10},{'filename':'ahmed','size':10},{'filename':'mshangama','size':13}]

K = {'relative_path':'tester','st_size':10,'st_mtime':10}
I = {'relative_path':'tester','st_size':110,'st_mtime':10}

C = is_different(K,I)
print(C)

            
            
