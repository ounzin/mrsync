#!/usr/bin/env python3

def send(fd,tag,v):
    os.write(fd,v)