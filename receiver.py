#!/usr/bin/env python3

import os
import time
import pickle
import os.path
from filelist import *
from options import *
import message

def receiver(source):
    rep = os.path.realpath(source)
    liste = lister(rep)
    return liste

def receive(wf1,rf2,A,mode,actions):
            try:
                print("ici")
                byte_a = message.send(wf1,mode,A)
                send_byte += byte_a
            except:
                print("Erreur envoi de la liste de fichiers",file=sys.stderr)

            os.write(actions,b'Reception de la liste de fichiers manquants \n') #log

            missing_files = message.receive(rf2) # return missing files in dst
            received_byte += missing_files.__sizeof__()
            
            if args.list_only:
                sys.exit(0)

            os.write(actions,b'Envoi des fichers manquants \n') #log    
            for k,v in missing_files[1].items():
                try:
                    current_file = os.open(v['absolute_path'],os.O_RDONLY)
                except:
                    print("Erreur d'ouverture du fichier",file=sys.stderr)

                file_size = int(v['st_size'])
                file_tag = "data"
                start_tag = "debut envoi"
                counter = 1

                if file_size > 16777216 :
                    counter = (file_size // 16777216) + 1
                    file_tag = "big_data"

                try:
                    byte_b = message.send(wf1,"debut envoi",counter)
                    send_byte += byte_b
                except:
                    print("Erreur d'envoi du message pour signaler le début d'envoi",file=sys.stderr)
                
                while counter > 0:
                    cpt = 0
                    to_send=b""
                    while (byte := os.read(current_file,1)) and cpt <= 16777216:
                        to_send = to_send + byte
                        cpt+=1
                    try:
                        byte_c = message.send(wf1,file_tag,to_send)
                        send_byte += byte_c
                    except:
                        print("Erreur d'envoi de données",file=sys.stderr)

                    counter -= 1
            try:           
                byte_d = message.send(wf1,fin,fin)
                os.write(actions,b'Fin d\'envoi des fichiers manquants \n')
                send_byte += byte_d
            except:
                print("Erreur d'envoi du message signalant la fin de transmission")