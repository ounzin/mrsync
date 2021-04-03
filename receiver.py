#!/usr/bin/env python3

import os
import time
 
write_path = "/tmp/server_in"
read_path = "/tmp/server_out"
 
wf = os.open(write_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)
rf = None
A = ['a','toto','arararara']  

for i in range(len(A)):
    msg = A[i]
    msg = str.encode(msg)
    len_send = os.write(wf,msg)
    print ("sent msg:",msg)
 
    if rf is None:
        rf = os.open(read_path, os.O_RDONLY)
 
    s = os.read(rf, 1024)
    if len(s) == 0:
        break
    print ("received msg: %s",s)
 
    time.sleep(1)
 
os.write(wf,str.encode('exit'))
os.close(rf)
os.close(wf)