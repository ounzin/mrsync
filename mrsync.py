#!/usr/bin/env python3
import os,sys,time,signal,pickle
from options import *
from sender import *
import server, receiver, message,sender,generator

#Alarm Handler

def alarm_handler(signal,frame):
    try:
        #print("ok")
        pass
    except:
        pass
        #print("okkk")

# Handle server and client 
if args.timeout:
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(int(args.timeout))

(rf1,wf1) = os.pipe() # client to server 
(rf2,wf2) = os.pipe() # server to client 
receive_msg = {}

pid = os.fork()

if pid == 0: #son, execute server
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
        fin = "fin d'envoi"
        os.close(wf2)
        os.close(rf1)
        message.send(wf1,mode,A)
        missing_files = message.receive(rf2) # return missing files in dst
        if(args.list_only):
            sys.exit(0)
        for k,v in missing_files[1].items():
            current_file = os.open(v['absolute_path'],os.O_RDONLY)
            file_size = int(v['st_size'])
            file_tag = "data"
            start_tag = "debut envoi"
            counter = 1

            if file_size > 16777216 :
                counter = (file_size // 16777216) + 1
                file_tag = "big_data"

            message.send(wf1,"debut envoi",counter)
            
            while counter > 0:
                cpt = 0
                to_send=b""
                while (byte := os.read(current_file,1)) and cpt <= 16777216:
                    to_send = to_send + byte
                    cpt+=1
                message.send(wf1,file_tag,to_send)
                counter -= 1   

            #print(current_file)
            #print(v['absolute_path'])
        message.send(wf1,fin,fin)
        os.waitpid(pid,0)
        #signal.alarm(0)
        
