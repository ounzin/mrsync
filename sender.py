#!/usr/bin/env python3

import os, sys
from options import *
from filelist import *

def sender(source):
    liste = lister(source)
    return liste