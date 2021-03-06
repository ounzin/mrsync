#!/usr/bin/env python3
# Authors : ADJIBADE Ahmed - ALLOUCHE Yanis

import os,sys
import filelist
from options import *
import os.path
import message

def is_different(a,b): #return True if a is different from b
    
    #Handle options

    if args.size_only: # --size-only
        if a['st_size'] == b['st_size']:
            return False

    if args.perms:#--perm
        if a['st_mode'] == b['st_mode']:
            return False

    if args.update:#--update
        if a['relative_path'] != b['relative_path']:
            return False

    if args.times:# --times
        if a['st_mtime'] == b['st_mtime']:
            return False
    
    if args.ignore_times: # --ignore-times
        if a['st_mtime'] == b['st_mtime'] and a['st_size'] == b['st_size']:
            if a['relative_path'] == b['relative_path']:
                return False
            else:
                return True

    if a['relative_path'] != b['relative_path']:
        return True
        
    elif a['st_size'] != b['st_size']:
        return True
    
    elif a['st_mtime'] != b['st_mtime']:
        return True

    else:
        return False


def comparator(list_src,list_dst):
    
    missing = {}
    
    for k1,v1 in list_src.items():
        dest_keys = list_dst.keys()
        miss_keys = missing.keys()
        dest_keys = list(dest_keys)
        miss_keys = list(miss_keys)

        
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

def to_deletee(src,dst):
    to_del = "ok"
    to_del = comparator(dst, src)
    return to_del

def compare(src,dst,list_src,list_dst):
    
    missing = comparator(list_src, list_dst) # files and dir in src but not in dst
    missing_files = {}
    to_delete = to_deletee(list_src, list_dst)

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

    #force handler 
    if args.force:
        for k,v in to_delete.items():
            if v['type'] == 'dir':
                try:
                    os.rmdir(v['absolute_path'])
                except:
                    pass

    if(len(SRC)>=2):         
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