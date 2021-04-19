#!/usr/bin/env python3

import os, sys, os.path, time, pickle
import message
import receiver
from filelist import *
from options import *

def server(rf): # mode local : server == receiver
    list_dst = receiver.receiver(DST)

    list_rec = message.receive(rf) # ici je recupere (lecture) la liste grace à ma fonction message.receive
    a = list_rec[0]
    b = list_rec[1]
    return a,b


    
    
