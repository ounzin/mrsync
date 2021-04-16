#!/usr/bin/env python3
import os,sys,time,signal
from options import *
from sender import *
import server, receiver, message

# Handle server and client 

(rf1,wf1) = os.pipe() # client to server 
(rf2,wf2) = os.pipe() # server to client 

pid = os.fork()

if pid == 0: #son, execute server
    if mode == 'push' or mode == 'local' :
        os.close(wf1)
        server.server(rf2,wf1)
    else:
        pass #server.server_push 
else: #father, execute client
    if mode == 'push' or mode == 'local' :
        A = ['bonjour','bonsoir','eaea','bonsoir','bonsoir',]
        os.close(rf1)
        message.send(wf2,mode,A)
