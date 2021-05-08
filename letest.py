#!/usr/bin/python3

import os, sys
from options import *

a = ['ssh','-e','none', '-l','distant','localhost','--','./letest.py','--server','SRC','DST' ]

(rf,wf) = os.pipe()

if not args.server:
    pid = os.fork()
    if pid == 0:
        os.execvp(a[0], a[0:])
        print("after")
    else:
        os.close(rf)
        os.set_blocking(wf, True)
        os.write(wf, b'message')
        os.wait()
else:
    os.close(wf)
    b = os.read(rf,3)
    print(b)
    #print("bonsoir")
