#!/usr/bin/python3

import os, sys

"""print ("The child will write text to a pipe and ")
print ("the parent will read the text written by child...")

# file descriptors r, w for reading and writing
r, w = os.pipe() 

processid = os.fork()
if processid:
   # This is the parent process 
   # Closes file descriptor w
   os.close(w)
   r = os.fdopen(r)
   print ("Parent reading")
   str = r.read()
   print ("text =", str)   
   sys.exit(0)
else:
   # This is the child process
   os.close(r)
   w = os.fdopen(w, 'w')
   print ("Child writing")
   w.write("Text written by aeaea...")
   w.close()
   print ("Child closing")
   sys.exit(0)"""

"""def ARRSUM(L,n):
   tiptop = n-1
   somme = 0
   if n == 1: 
      return L[0]
   somme = ARRSUM(L,n-1) + L[tiptop]
   return somme

L = [1,2,3,4]

n = len(L)
print(ARRSUM(L,n))"""

A = {'a':{'taille':2,'crea':1212},'b':{'taille':122,'crea':112}}
B = {'a':{'taille':23,'crea':887},'DQ':{'taille':57,'crea':3131}}

A.update(B)
