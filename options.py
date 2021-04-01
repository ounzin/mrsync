#!/usr/bin/env python3
import argparse,sys

SRC = ''
DST = ''
SRC_user = ''
DST_user = ''
mode = ''
based_options = []

#Parsing...

parser = argparse.ArgumentParser(prog='mrsync', description="Here is a short summary of the options available in mrsync. Please refer "+
"to the detailed description below for a complete description.")
parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    help="increase verbosity",
)

parser.add_argument(
    "-q",
    "--quiet",
    action="store_false",
    help="suppress non-error messages",
)

parser.add_argument(
    "-a",
    "--archive",
    action="store_false",
    help=" archive mode; same as -rpt (no -H)",
)  

parser.add_argument(
    "-r",
    "--recursive",
    action="store_false",
    help=" recurse into directories",
)   

parser.add_argument(
    "-u",
    "--update",
    action="store_false",
    help=" skip files that are newer on the receiver",
)  

parser.add_argument(
    "-d",
    "--dirs",
    action="store_false",
    help=" transfer directories without recursing",
)  

parser.add_argument(
    "-H",
    "--hard-links",
    action="store_false",
    help=" preserve hard links",
)   

parser.add_argument(
    "-p",
    "--perms",
    action="store_false",
    help=" preserve permissions",
)

parser.add_argument(
    "-t",
    "--times",
    action="store_true",
    help=" preserve times",
)


parser.add_argument(
    "SRC",
    help="Adresse source",
)

parser.add_argument(
    "DST",
    help="Adresse destination",
    nargs='*'
)
args = parser.parse_args()

options_map={
    'verbose':'-v',
    'quiet':'-q',
    'archive':'-a',
    'recursive':'-r',
    'update':'-u',
    'dirs':'-d',
    'hard_links':'-H',
    'perms':'-p',
    'times':'-t',
}

#End parsing

##############################################################################################

#Values and mode Handler 

def point_finder(s):
    a = s.find(':')
    b = s.find('::')
    if a!=-1 or b!=-1:
        return True
    else:
        return False

def username_finder(s):
    a = s.split('@')
    return a[0]

""" Affectation de l'adresse source et de la destination (si définie) & verifications """
SRC = args.SRC
if args.DST:
    DST = args.DST[0]

src_point_tester = point_finder(SRC)
dst_point_tester = point_finder(DST)

if SRC and DST == '': #mrsync [OPTION]... SRC 
    print('local src')

if SRC and DST != '': #mrsync [OPTION]... SRC [SRC]... [DEST] (includes dest optional or nor)
    #Search : or :: and assign modes
    
    if src_point_tester == False and dst_point_tester == False: #source et destination sur même machine local
         mode = 'local'
    if src_point_tester == True and dst_point_tester == False: #source distante, destination local
        mode = 'pull'
        SRC_user = username_finder(SRC)
        
    if src_point_tester == False and dst_point_tester == True : #source local, destination distante
        mode = 'push'
        DST_user = username_finder(DST)
        
    if src_point_tester == True and dst_point_tester == True : #source et destination sur même machine distante
        mode = 'local'
   
for v in options_map.values():
    based_options.append(v)

#for k in args.__dict__:
 # print (k)
