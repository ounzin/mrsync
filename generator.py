#!/usr/bin/env python3

import os,sys
import filelist
from options import *
import os.path
import message

def is_different(a,b): #return True if a is different from b
    if args.size_only:
        if a['st_size'] == b['st_size']:
            return False

    if a['relative_path'] != b['relative_path']:
        return True
    elif a['st_size'] != b['st_size']:
        return True
    elif a['st_mtime'] != b['st_mtime']:
        return True
    else:
        return False

def to_delete(list_src,list_dst):
    to_del = compare(list_dst, list_src)
    return to_del

def comparator(list_src,list_dst):
    missing = {}
    for k1,v1 in list_src.items():
        dest_keys = list_dst.keys()
        miss_keys = missing.keys()
        if k1 not in dest_keys:        
            if k1 not in miss_keys:
                missing[k1] = list_src[k1]
        for k2,v2 in list_dst.items():
            if k1 == k2:
                test = is_different(v1,v2)
                if test:
                    missing[k1] = v1
                else:
                    pass
    return missing

def compare(src,dst,list_src,list_dst):
    missing = comparator(list_src, list_dst) # files and dir in src but not in dst
    missing_files = {}
    to_delete = comparator(list_dst, list_src)
    # delete handler 
    if args.delete:
        for k,v in to_delete.items():
            for k1,v1 in v.items():
                to_del_path = v['absolute_path']
                try:
                    os.remove(to_del_path)
                except:
                    pass
                break
    #list-only handler
    if args.list_only:
        print(missing)
        sys.exit(0)
            
    # create missing dirs
    for key,value in missing.items():
        for key1,value1 in value.items():
            if key1 == "type":
                if value1 == "dir": # creating dirs, split absolute path by src absolute_path to get only relative
                    dos_split_value = str(os.path.realpath(src)+'/')
                    to_create = str(value['absolute_path'])
                    to_create_tab = to_create.split(dos_split_value)
                    create_path = str(os.path.join(dst,to_create_tab[1]))
                    if os.path.exists(create_path):
                        pass
                    else:
                        os.mkdir(create_path)
    # missing dir created

    # make list of missing files only

    for key2,value2 in missing.items():
        for key3,value3 in value2.items():
            if value3 == "file":
                missing_files[key2] = value2
                pass
    return missing_files
