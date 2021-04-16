#!/usr/bin/env python3
import os, sys, pickle,time

def send(fd,tag,v): # fd : file descriptor, tag : nature of message
    info_out = [] 
    #        
    info_out.append(tag)
    info_out.append(v)
    #
    size_m = info_out.__sizeof__()
    info_out = pickle.dumps(info_out)
    size_m = len(info_out)
    size_m = size_m.to_bytes(3,byteorder='little')
    to_send = size_m + info_out
    #os.write(fd,size_m)
    #os.write(fd,info_out)
    os.write(fd,to_send)


def receive(fd):
    tag = ''
    msg = []
    size_m = os.read(fd,3)
    size_buff = int.from_bytes(size_m,byteorder='little')

    if size_buff > 16777216 :
        buffer_overflow = []
        buffer_overflow_out = [] #a completer
        while size_buff > 16777216:
            buffer_overflow.append(os.read(fd,size_buff))
            size_m -= 16777216

    elif size_buff != 0:
        receive_out = os.read(fd,size_buff)
        s = pickle.loads(receive_out)
        tag = s[0]
        msg = s[1]
    return tag,msg

            