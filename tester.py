#!/usr/bin/env python3
import os, os.path,sys,subprocess, pickle
#from options import *

v= [['aoeiaeae','aoeiaeae'],
['aoeiaeae','aoeiaeae'],
['aoeiaeae','aoeiaeae']]

stat_table = []
A = os.stat('test/a.txt')
B = str(A).split('(')
C = B[1].split(')')
D = C[0].split(',')
for i in range(len(D)):
    inner_stat = D[i].split('=')
    stat_table.append(inner_stat[1])

print(stat_table)

