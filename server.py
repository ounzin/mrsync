#!/usr/bin/env python3

import os, sys, os.path, time

read_path = "/tmp/server_in"
write_path = "/tmp/server_out"

if os.path.exists(read_path):
    os.remove(read_path)
if os.path.exists(write_path):
    os.remove(write_path)

os.mkfifo(read_path)
os.mkfifo(write_path)


rf = os.open(read_path, os.O_RDONLY)
wf = os.open(write_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)
 
while True:
    s = os.read(rf, 1024)
    s = s.decode('utf-8')
    print ("received msg: %s",s)
    if len(s) == 0:
        time.sleep(1)
        continue
 
    if "exit" in s:
        break
    s = str.encode(s)
    os.write(wf, s)
 
os.close(rf)
os.close(wf)