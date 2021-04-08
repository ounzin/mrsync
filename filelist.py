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
            inner_tab_file = []
            a = os.path.basename(inner_path)

            # Getting file name and file stats ...

            inner_tab_file.append(a) # file name
            inner_tab_file.append(os.stat(inner_path).st_mode) #st_mode
            inner_tab_file.append(os.stat(inner_path).st_ino) #st_ino
            inner_tab_file.append(os.stat(inner_path).st_dev) #st_dev
            inner_tab_file.append(os.stat(inner_path).st_nlink) #st_nlink
            inner_tab_file.append(os.stat(inner_path).st_uid) #st_uid
            inner_tab_file.append(os.stat(inner_path).st_gid) #st_gid
            inner_tab_file.append(os.stat(inner_path).st_size) #st_size
            inner_tab_file.append(os.stat(inner_path).st_atime) #st_atime
            inner_tab_file.append(os.stat(inner_path).st_mtime) #st_mtime
            inner_tab_file.append(os.stat(inner_path).st_ctime) #st_ctime

            # End of getting file info

            filelist.append(inner_tab_file)

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