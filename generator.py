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
    missing = {}
    for k1,v1 in list_src.items():
        """
        dest_keys = list_dst.keys()
        miss_keys = missing.keys()
        if k1 in dest_keys:
            if k1 not in miss_keys:
                missing[k1] = list_src[k1]"""
        for k2,v2 in list_dst.items():
            if k1 == k2:
                test = is_different(v1,v2)
                if test:
                    missing[k1] = v1
                else:
                    pass
    return missing

"""A = [{'filename':'tester','size':10},{'filename':'ahmed','size':10},{'filename':'padel','size':9}]
D = [{'filename':'aaeaeaea','size':39}]
B = [{'filename':'tester','size':10},{'filename':'ahmed','size':10},{'filename':'mshangama','size':13}]

K = {'a': {'relative_path':'tester','st_size':11110,'st_mtime':10},'b': {'relative_path':'ahmed','st_size':0,'st_mtime':110}}
I = {'b': {'relative_path':'tester','st_size':110,'st_mtime':10}}"""
            
            
