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
    if os.path.isfile(addr_source):
        a = os.path.basename(addr_source)
        filelist.append(a)
 
    elif os.path.islink(addr_source):
        print("link")

    elif os.path.isdir(addr_source):
        inner_dir = []
        pid = os.fork()
        if pid == 0:
            inner_dir = ls(addr_source)
            #parent_dir = os.getcwd()
            for i in range(len(inner_dir)):
                inner_path = os.path.join(addr_source,inner_dir[i])
                a = lister(inner_path)
                filelist.append(a)
            sys.exit(0)
        else:
            pid_wait, status = os.waitpid(-1,0)
    else:
        pass
    return filelist
    
A = lister(SRC)
print(A)
#lister(SRC)
#print(ls(SRC))
