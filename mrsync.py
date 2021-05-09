#!/usr/bin/env python3
# Authors : ADJIBADE Ahmed - ALLOUCHE Yanis

import os,sys,signal,pickle,time
from options import *
from sender import *
import server, receiver, message,sender,generator

#Data for log

actions = os.open('log',os.O_RDWR | os.O_CREAT | os.O_TRUNC)  
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

#Archive 

if args.archive:
    args.recursive = True
    args.dirs = True


# Handle server and client 

def sync(SRC,DST): #Synchronisation function

    global duree
    global send_byte
    global received_byte

    os.write(actions,b'Debut de la synchronisation \n') # log

    tps1 = time.time() #sync start time

    (rf1,wf1) = os.pipe() # client to server 
    (rf2,wf2) = os.pipe() # server to client 

    receive_msg = {}
    mode = mode_finder(SRC, DST) #get sync mode

    pid = os.fork()
    if pid == 0: #son, execute server

        os.close(wf1)
        os.close(rf2)

        if  mode == 'local' : # local mode
            os.write(actions,b'Mode de transmission de donnees : Local \n')
            server.server(SRC,DST,rf1,wf2)
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
            
            if args.list_only: # exit to avoid errors
                sys.exit(0)

            os.write(actions,b'Envoi des fichers manquants \n') #log

            # start sending files
                
            for k,v in missing_files[1].items():
                try:
                    current_file = os.open(v['absolute_path'],os.O_RDONLY)
                except:
                    print("Erreur d'ouverture du fichier",file=sys.stderr)

                file_size = int(v['st_size'])
                file_tag = "data"
                start_tag = "debut envoi"
                counter = 1

                if file_size > 16777216 : # verify if message is bigger than 16Mo then get how many times we read
                    counter = (file_size // 16777216) + 1
                    file_tag = "big_data"

                try: # sending data
                    byte_b = message.send(wf1,"debut envoi",counter)
                    send_byte += byte_b
                except:
                    print("Erreur d'envoi du message pour signaler le début d'envoi",file=sys.stderr)
                
                while counter > 0: #sending big data : bigger than 16Mo
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
            
            # end of sending files

            os.waitpid(pid,0)

    ###################### SSH HANDLER (en cours d'implementation)
        
        if mode == 'push': #mode SSH 
            (rf3,wf3) = os.pipe() #client to server ssh
            (rf4,wf4) = os.pipe() #server to client ssh
            
            if args.server:
                os.close(rf4)
                os.close(wf3)
                server.server(SRC, DST, rf3, wf4)       
            
            if not args.server:
                pid = os.fork()
                if pid == 0:

                    #os.execvp() handler
                    exec_args = ['ssh','-e','none','-l','distant','localhost','--']
                    exec_args.append(sys.argv[0])
                    exec_args.append('--server')
                    for i in range(1,len(sys.argv)):
                        exec_args.append(sys.argv[i])
            
                    try:
                        os.execvp(exec_args[0],exec_args[0:])
                    except:
                        os.write(actions, "Erreur lancement ssh")
                    #end
                
                else:
                    os.waitpid(pid,0)

        os.write(actions,b'Fin de la synchronisation \n')

    tps2 = time.time()
    duree = tps2 - tps1
    
#### Main program ####


# Start sync 

if len_SRC == 1: # SRC, only one parameter then launch list-only
    if os.path.exists(SRC):
        a = subprocess.run(['ls',SRC],capture_output=True, text=True).stdout
        print(a)
        if args.list_only:
            print(a)
            sys.exit(0)
        pass
    else:
        print("Fatal error, dir doesn't exist")
        
if len_SRC >= 2: # SRC[s] and DST synchronisation
    for i in range(len(SRC)-1):
        if os.path.exists(SRC[i]) and os.path.exists(DST):
            sync(str(SRC[i]),DST)
        else:
            print("Fatal error, dir doesn't exist")


# Filing metafile for log

send_byte = str(send_byte)
received_byte = str(received_byte)
duree = str(round(duree, 2))
log_msg = "\n\nsent : " +send_byte+ " bytes " + "received : " + received_byte + " bytes " + " speed : " + duree
log_msg = log_msg.encode('utf_8') 
os.write(actions,log_msg)

if args.quiet: # option : --quiet
    if os.path.exists('log'):
        os.remove('log')

if args.verbose: # option : --verbose
    if os.path.exists('log'):
        os.lseek(actions, 0, 0)
        c = os.read(actions, 2048)
        c = c.decode('ascii')
        print(c)

if args.timeout:
    signal.alarm(0) # take of alarm 

#End
