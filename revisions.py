#!/usr/bin/env python3
import os,sys,signal,time, socket

def question_un():
    for i in range(3):
        pid = os.fork()
        if pid == 0:
            sys.exit(0)
        else:
            print("fils %d créé",i)
    input('Entrez un texte ...')
    for i in range(3):
        pid,status = os.wait()
        print("Mort du fils %d",pid)

def handler_sigusr(int,frame):
    pid = os.fork()
    if pid==0:
        time.sleep(2)
        sys.exit(0)
def handler_alarm(int,frame):
    print("fin")
    sys.exit(0)
        
def question_deux():
    signal.signal(signal.SIGUSR1,handler_sigusr)
    signal.signal(signal.SIGALRM,handler_alarm)
    signal.alarm(60)

    while True :
        os.kill(os.getpid(),signal.SIGUSR1.value)
        pid,status = os.wait()
        print("Le fils %d est mort",pid)

def question_six():
    clicsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    addr = ("http://deptinfo.unice.fr/~stouati/index.html",80)
    cnt = clicsock.connect(("www.deptinfo.unice.fr/~stouati/index.html",80))
    if cnt == 0: #connexion ok
        get_file = open('index.html','w')
        get_file = clicsock.recv(1024)
    else:
        print("echec connexion")
if __name__ == "__main__":
    question_six()