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