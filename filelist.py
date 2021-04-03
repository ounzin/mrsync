#!/usr/bin/env python3

import os, os.path,sys,subprocess
from options import *

def ls(a):
    ls_out = []
    a = subprocess.run(['ls',a],capture_output=True, text=True).stdout
    b = a.split('\n')
    for i in range(len(b)):
        if b[i] != '':
            ls_out.append(b[i])
    return ls_out

def lister(addr_source):
    filelist = []
    current = ls(addr_source)
    for i in range(len(current)):
        inner_path = os.path.join(addr_source,current[i])
        #print (inner_path)
        if os.path.isfile(inner_path):
            a = os.path.basename(inner_path)  
            filelist.append(a)
        elif os.path.islink(inner_path): # a verifier avec le prof
            realink = os.path.realpath(inner_path)
            print(realink)
            subdir1 = lister(realink)
            for i in range(len(subdir1)):
                filelist.append(subdir1[i])

        elif os.path.isdir(inner_path):
            subdir2 = lister(inner_path)
            for i in range(len(subdir2)):
                filelist.append(subdir2[i])
        else:
            pass
    return filelist