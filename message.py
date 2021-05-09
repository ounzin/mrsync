#!/usr/bin/env python3
# Authors : ADJIBADE Ahmed - ALLOUCHE Yanis

import os, sys, pickle,time

def byte_writer(a,fd):
    rel = ''
    size = os.read(fd, 1024)
    #rel = size.decode('ascii')
    if rel == '':
        size = 0
    else:
        size = int(rel)
    size += a
    size = str(size)
    size = size.encode('utf-8')
    os.write(fd,size)

def send(fd,tag,v): # fd : file descriptor, tag : nature of message
    info_out = [] 
    #        
    info_out.append(tag)
    info_out.append(v)
    #
    size_m = info_out.__sizeof__()
    
    info_out = pickle.dumps(info_out)
    size_m = len(info_out)
    
    size_to_write = int(size_m) + 3

    size_m = size_m.to_bytes(3,byteorder='little')
    os.write(fd,size_m)
    os.write(fd,info_out)
    return int(size_to_write)

def receive(fd):
    tag = ''
    msg = []
    size_m = os.read(fd,3)
    size_buff = int.from_bytes(size_m,byteorder='little')

    if size_buff != 0:
        tag = ""
        msg = ""
    
        if size_buff > 16777216 :
            while size_buff > 16777216:
                receive_out = os.read(fd, 16777216)
                s = pickle.loads(receive_out)
                msg += s[1]
                tag = s[0]

        else :
            receive_out = os.read(fd,size_buff)
            s = pickle.loads(receive_out)
            tag = s[0]
            msg = s[1]
        return tag,msg