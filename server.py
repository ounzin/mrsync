#!/usr/bin/env python3

import os, sys, os.path, time, pickle
import message
import receiver
from filelist import *
from options import *
from generator import *

def server(rf,wf): # mode local : server == receiver
    list_dst = receiver.receiver(DST)
    list_rec = message.receive(rf) # ici je recupere (lecture) la liste grace à ma fonction message.receive
    a = list_rec[0]
    b = list_rec[1]
    pid = os.fork()
    if pid == 0:
        generated = compare(SRC,DST,b,list_dst)
        tag = "missing"
        message.send(wf, tag, generated)
        for k,v in generated.items():
             # création du fichier dans la destination
             file_split_value = str(os.path.realpath(SRC)+'/')
             to_create = str(v['absolute_path'])
             to_create_tab = to_create.split(file_split_value)
             file_create_path = str(os.path.join(DST,to_create_tab[1]))
             
             starter = message.receive(rf)
             if starter[0] == "debut envoi":
                file_des = os.open(file_create_path,os.O_WRONLY | os.O_CREAT | os.O_TRUNC) 
                counter = int(starter[1])
                if counter < 2:
                    recu = message.receive(rf)
                    os.write(file_des,recu[1])
                else:
                    final = b""
                    while counter > 0:
                        recu = message.receive(rf) 
                        final += recu   
                os.close(file_des)     
        sys.exit(0)