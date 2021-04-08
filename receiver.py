#!/usr/bin/env python3

import os
import time
import pickle
from filelist import *
from options import *
import message
 
write_path = "/tmp/server_in"
read_path = "/tmp/server_out"
 
wf = os.open(write_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)
rf = os.open(read_path,os.O_RDONLY)

A = ['bonjour','bonsoir','bonsoir','bonsoir','bonsoir',]
B = lister(SRC)

message.send(wf,'size',1211) 

os.close(rf)
os.close(wf)