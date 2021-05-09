#!/usr/bin/env python3
# Authors : ADJIBADE Ahmed - ALLOUCHE Yanis

import os, os.path,sys,subprocess
from options import *
import itertools

#filelist return an array of dictionnary

def ls(a):
    ls_out = []
    if a == "*":
        a = subprocess.run(['ls'],capture_output=True, text=True).stdout
    else:
        a = subprocess.run(['ls',a],capture_output=True, text=True).stdout
    b = a.split('\n')
    for i in range(len(b)):
        if b[i] != '':
            ls_out.append(b[i])
    return ls_out


def get_stats(path):
    stat_table = []
    A = os.stat(path)
    B = str(A).split('(')
    C = B[1].split(')')
    D = C[0].split(',')
    for i in range(len(D)):
        inner_stat = D[i].split('=')
        stat_table.append(inner_stat[1])
    return stat_table


def lister(addr_source,src):

    filelist = {}
    current = ls(addr_source)

    if addr_source == "*":
        addr_source = os.getcwd()

    for i in range(len(current)):
        inner_path = ""

        if os.path.isfile(addr_source) :
            inner_path = addr_source
        else:
            inner_path = os.path.join(addr_source,current[i])


        if os.path.isdir(inner_path):
            #Dir is also a file
            aa = os.path.dirname(addr_source)
            inner_tab_file = {} 
            a = os.path.basename(inner_path)
                
            absolute_path = os.path.realpath(inner_path)     
            relative_path = ""

            if not os.path.isfile(addr_source):
                r = os.path.relpath(inner_path)
                re = r.split(src)
                for i in range(1,len(re)):
                    relative_path += re[i]
                if relative_path == "":
                    r = absolute_path.split(src+'/')
                    relative_path = r[1]
            else:
                relative_path = addr_source
                    
            stat_table = get_stats(inner_path) 

            # Getting dir name and dir stats ...

            inner_tab_file['type'] = 'dir'
            inner_tab_file['filename'] = relative_path
            inner_tab_file['origin'] = src
            inner_tab_file['absolute_path'] = absolute_path
            inner_tab_file['relative_path'] = relative_path
            inner_tab_file['st_mode'] = stat_table[0] # st_mode
            inner_tab_file['st_ino'] = stat_table[1] # st_ino
            inner_tab_file['st_dev'] = stat_table[2] # st_mode
            inner_tab_file['st_nlink'] = stat_table[3] # st_nlink
            inner_tab_file['st_uid'] = stat_table[4] # st_uid
            inner_tab_file['st_gid'] = stat_table[5] # st_gid
            inner_tab_file['st_size'] = stat_table[6] # st_size
            inner_tab_file['st_atime'] = stat_table[7] # st_atime
            inner_tab_file['st_mtime'] = stat_table[8] # st_mtime
            inner_tab_file['st_ctime'] = stat_table[9] # st_ctime

            # End of getting dir info
            if args.recursive: # recurse into directories
                filelist[relative_path] = inner_tab_file
                subdir2 = lister(inner_path,src)
                filelist.update(subdir2)

            if args.dirs:
                filelist[relative_path] = inner_tab_file
                

        elif os.path.isfile(inner_path):
            inner_tab_file = {} 
            a = os.path.basename(inner_path)
        
            absolute_path = os.path.realpath(inner_path)
            relative_path = ""

            if not os.path.isfile(addr_source):
                r = os.path.relpath(inner_path)
                re = r.split(src)

                for i in range(1,len(re)):
                    relative_path += re[i]
                if relative_path == "":
                    r = absolute_path.split(src+'/')
                    relative_path = r[1]
            else:
                relative_path = addr_source
            
            stat_table = get_stats(inner_path) 

            # Getting file name and file stats ...

            inner_tab_file['type'] = 'file'
            inner_tab_file['filename'] = relative_path
            inner_tab_file['origin'] = src
            inner_tab_file['absolute_path'] = absolute_path
            inner_tab_file['relative_path'] = relative_path
            inner_tab_file['st_mode'] = stat_table[0] # st_mode
            inner_tab_file['st_ino'] = stat_table[1] # st_ino
            inner_tab_file['st_dev'] = stat_table[2] # st_mode
            inner_tab_file['st_nlink'] = stat_table[3] # st_nlink
            inner_tab_file['st_uid'] = stat_table[4] # st_uid
            inner_tab_file['st_gid'] = stat_table[5] # st_gid
            inner_tab_file['st_size'] = stat_table[6] # st_size
            inner_tab_file['st_atime'] = stat_table[7] # st_atime
            inner_tab_file['st_mtime'] = stat_table[8] # st_mtime
            inner_tab_file['st_ctime'] = stat_table[9] # st_ctime

            # End of getting file info

            filelist[relative_path] = inner_tab_file 

        elif os.path.islink(inner_path): # a verifier avec le prof
            inner_tab_link = {} 
            a = os.path.basename(inner_path)
        
            absolute_path = os.path.realpath(inner_path)
            r = os.path.relpath(inner_path)
            re = r.split(src)
                
            relative_path = ""
            for i in range(1,len(re)):
                relative_path += re[i]
            if relative_path == "":
                r = absolute_path.split(src+'/')
                relative_path = r[1]
            stat_table = get_stats(inner_path)

            # Getting link name and link stats ...

            inner_tab_link['type'] = 'file'
            inner_tab_link['filename'] = relative_path
            inner_tab_link['origin'] = src
            inner_tab_link['absolute_path'] = absolute_path
            inner_tab_link['relative_path'] = relative_path
            inner_tab_link['st_mode'] = stat_table[0] # st_mode
            inner_tab_link['st_ino'] = stat_table[1] # st_ino
            inner_tab_link['st_dev'] = stat_table[2] # st_mode
            inner_tab_link['st_nlink'] = stat_table[3] # st_nlink
            inner_tab_link['st_uid'] = stat_table[4] # st_uid
            inner_tab_link['st_gid'] = stat_table[5] # st_gid
            inner_tab_link['st_size'] = stat_table[6] # st_size
            inner_tab_link['st_atime'] = stat_table[7] # st_atime
            inner_tab_link['st_mtime'] = stat_table[8] # st_mtime
            inner_tab_link['st_ctime'] = stat_table[9] # st_ctime

            # End of getting link info

            filelist[relative_path] = inner_tab_link
        else:
            pass
    return filelist