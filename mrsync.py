#!/usr/bin/env python3
import os,sys,signal,pickle
import time
from options import *
from sender import *
import server, receiver, message,sender,generator

#Metadonnees
actions = os.open('action',os.O_RDWR | os.O_CREAT | os.O_TRUNC)  
send_byte = 0
received_byte = 0
duree = 0
debit = 0

#Timeout
class TimeOut(BaseException):
    pass

def alarm_handler(signal,frame):
    raise TimeOut()
    print('Timeout !')

if args.timeout:
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(args.timeout)

# Handle server and client 
def sync(SRC,DST):
    global duree
    global send_byte
    global received_byte

    os.write(actions,b'Debut de la synchronisation \n') # message pour le log

    tps1 = time.time()
    (rf1,wf1) = os.pipe() # client to server 
    (rf2,wf2) = os.pipe() # server to client 

    receive_msg = {}
    mode = mode_finder(SRC, DST)
    pid = os.fork()
    if pid == 0: #son, execute server
        os.close(wf1)
        os.close(rf2)

        if  mode == 'local' :
            os.write(actions,b'Mode de transmission de donnees : Local \n')
            
            server.server(SRC,DST,rf1,wf2)
        elif mode == 'push':
            os.write(actions,b'Mode de transmission de donnees : Push \n')
            pass
        else:
            pass #server.server_push
        sys.exit(0)    

    else: #father, execute client
        if mode == 'local' :
            A = sender.sender(SRC)
            os.write(actions,b'Creation de la liste de fichiers de(s) (la) source(s) \n') #log

            fin = "fin d'envoi"
            os.close(wf2)
            os.close(rf1)

            try:
                byte_a = message.send(wf1,mode,A)
                send_byte += byte_a
            except:
                print("Erreur envoi de la liste de fichiers",file=sys.stderr)

            os.write(actions,b'Reception de la liste de fichiers manquants \n') #log

            missing_files = message.receive(rf2) # return missing files in dst
            received_byte += missing_files.__sizeof__()
            
            if(args.list_only):
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

            os.waitpid(pid,0)
        elif mode == 'push':
            print("ssh handle")
        os.write(actions,b'Fin de la synchronisation \n')    

    tps2 = time.time()
    duree = tps2 - tps1
    
# Lancement de la synchronisation    

if len(SRC) == 1: # SRC seul est passé en paramètre
    if args.list_only:
        print(lister(SRC))
if len(SRC) >= 2:
    for i in range(len(SRC)-1):
        sync(str(SRC[i]),DST)


# Filing metafiles
send_byte = str(send_byte)
received_byte = str(received_byte)
duree = str(round(duree, 2))
log_msg = "\n\nsent : " +send_byte+ " bytes " + "received : " + received_byte + " bytes " + " speed : " + duree
log_msg = log_msg.encode('utf_8') 
os.write(actions,log_msg)

if args.quiet:
    if os.path.exists('action'):
        os.remove('action')

if args.verbose:
    if os.path.exists('action'):
        os.lseek(actions, 0, 0)
        c = os.read(actions, 2048)
        c = c.decode('ascii')
        print(c)
        os.remove('action')

try: # remove action file after making all operations if exist !
    os.remove('action')
except:
    pass
signal.alarm(0)
