#!/usr/bin/env python3
# Authors : ADJIBADE Ahmed - ALLOUCHE Yanis

import os, sys, os.path, time, pickle
import message
import receiver
from filelist import *
from options import *
from generator import *

def server(SRC,DST,rf,wf): # mode local : server == receiver
    
    list_dst = receiver.receiver(DST)
    list_rec = message.receive(rf) # getting filelist with message.receive()
    a = list_rec[0] #tag
    b = list_rec[1] #message

    pid = os.fork()
    if pid == 0: # fork a generator to compare file and then send missing filelist to mrsync
        generated = compare(SRC,DST,b,list_dst) 
        tag = "missing"        
        message.send(wf, tag, generated)
    
        for k,v in generated.items(): # creating missing files on dst and fill them with data

             file_split_value = str(os.path.realpath(SRC)+'/')
             to_create = str(v['absolute_path'])
             to_create_tab = to_create.split(file_split_value)
             if not os.path.isfile(SRC):
                file_create_path = str(os.path.join(DST,to_create_tab[1]))
             else:
                 c = to_create.split('/')
                 d = c[-1]
                 file_create_path = str(os.path.join(DST,d))
             starter = message.receive(rf) 

             if starter[0] == "debut envoi": # we are about to receive data 
                
                file_des = os.open(file_create_path,os.O_WRONLY | os.O_CREAT | os.O_TRUNC) 
                counter = int(starter[1])

                if counter < 2: # data: lower than 16Mo
                    recu = message.receive(rf)
                    os.write(file_des,recu[1])

                else: # data: bigger than 16Mo
                    final = b""
                    while counter > 0:
                        recu = message.receive(rf) 
                        final += recu[1]
                    os.write(file_des,final)   
                os.close(file_des) #end 