#!/usr/bin/env python3

import os
import time
import pickle
 
write_path = "/tmp/server_in"
read_path = "/tmp/server_out"
 
wf = os.open(write_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)
rf = os.open(read_path,os.O_RDONLY)
A = ['a','toto','arararara']  

for i in range(3):
    msg = A[i]
    msg = str.encode(msg)
    send_A = pickle.dumps(A)
    os.write(wf,send_A)

    if rf is None:
        rf = os.open(read_path, os.O_RDONLY)

    s = os.read(rf, 16777216)
    s = pickle.loads(s)
    if len(s) == 0:
        break
    print ("received msg: %s",s)
 
    time.sleep(1)
end = ['exit'] 
end = pickle.dumps(end)
os.write(wf,end)
os.close(rf)
os.close(wf)