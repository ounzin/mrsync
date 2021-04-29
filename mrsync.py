#!/usr/bin/env python3
import os,sys,time,signal
from options import *
from sender import *
import server, receiver, message,sender,generator

#Alarm Handler

def alarm_handler(signal,frame):
    try:
        print("ok")
    except:
        print("okkk")

# Handle server and client 
if args.timeout:
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(int(args.timeout))

(rf1,wf1) = os.pipe() # client to server 
(rf2,wf2) = os.pipe() # server to client 
receive_msg = {}

pid = os.fork()

if pid == 0: #son, execute server
    """
    if args.blocking:
        os.set_blocking(wf1, False)
        os.set_blocking(rf2, False)
    else:
        os.set_blocking(wf1, True)
        os.set_blocking(rf2, True)"""
    os.close(wf1)
    os.close(rf2)
        
    if mode == 'push' or mode == 'local' :
        R = server.server(rf1,wf2)
    else:
        pass #server.server_push
    sys.exit(0)    

else: #father, execute client
    if mode == 'push' or mode == 'local' :
        A = sender.sender(SRC)

        os.close(wf2)
        os.close(rf1)
        """
        if args.blocking:
            os.set_blocking(wf2, False)
            os.set_blocking(rf1, False)
        else:
            os.set_blocking(wf2, True)
            os.set_blocking(rf1, True)"""
    
        message.send(wf1,mode,A)
        missing_files = message.receive(rf2)
        print(missing_files[1])
        os.waitpid(pid,0)
        #signal.alarm(0)
        
