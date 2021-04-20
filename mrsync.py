#!/usr/bin/env python3
import os,sys,time,signal
from options import *
from sender import *
import server, receiver, message,sender,generator

# Handle server and client 

(rf1,wf1) = os.pipe() # client to server 
(rf2,wf2) = os.pipe() # server to client 

receive_msg = {}

pid = os.fork()

if pid == 0: #son, execute server
    os.close(wf1)
    if mode == 'push' or mode == 'local' :
        R = server.server(rf1)
        #list_src = R[1]   
        #pid_g = os.fork()
        #if pid_g == 0: # server son, fork generator to compare files
        #    generator.compare()
    else:
        pass #server.server_push
    sys.exit(0)    

else: #father, execute client
    if mode == 'push' or mode == 'local' :
        A = sender.sender(SRC)
        os.close(rf1)
        message.send(wf1,mode,A)
        os.waitpid(pid,0)
        
        
