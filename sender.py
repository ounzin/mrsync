#!/usr/bin/env python3
# Authors : ADJIBADE Ahmed - ALLOUCHE Yanis

import os, sys
from options import *
from filelist import *

def sender(source):
    liste = lister(source,source)
    return liste