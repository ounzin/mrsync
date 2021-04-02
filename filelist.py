#!/usr/bin/env python3

import os, os.path,sys,subprocess
from options import *

def ls():
    a = subprocess.run(['ls'],capture_output=True, text=True).stdout
    b = a.split('\n')
    return b

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
            inner_dir = ls()
            #parent_dir = os.getcwd()
            for i in range(len(inner_dir)):
                inner_path = os.path.join(addr_source,inner_dir[i])
                print(inner_path)
                #lister(inner_path)
            sys.exit(0)
        else:
            pid_wait, status = os.waitpid(-1,0)
    else:
        pass
    return filelist

print(lister(SRC))
