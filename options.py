#!/usr/bin/env python3
# Authors : ADJIBADE Ahmed - ALLOUCHE Yanis

import argparse,sys,subprocess

SRC = ''
len_SRC = 0
DST = ''
SRC_user = ''
DST_user = ''
mode = ''
based_options = []

#Parsing...

parser = argparse.ArgumentParser(prog='mrsync', description="Here is a short summary of the options available in mrsync. Please refer "+
"to the detailed description below for a complete description.",usage="Mrsync is used to make a synchronisation between"+
"one or many source and only one destination. This version is powered by Ahmed ADJIBADE and Yanis Allouche")

parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    help="increase verbosity",
)

parser.add_argument(
    "-q",
    "--quiet",
    action="store_true",
    help="suppress non-error messages",
)

parser.add_argument(
    "-a",
    "--archive",
    action="store_true",
    help=" archive mode; same as -rpt (no -H)",
)  

parser.add_argument(
    "-r",
    "--recursive",
    action="store_true",
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
    action="store_true",
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
    "--existing",
    action="store_true",
    help="skip creating new files on receiver",
)

parser.add_argument(
    "--ignore-existing",
    action="store_true",
    help="skip updating files that exist on receiver",
)

parser.add_argument(
    "--delete",
    action="store_true",
    help="delete extraneous files from dest dirs",
)

parser.add_argument(
    "--force",
    action="store_true",
    help="force deletion of dirs even if not empty",
)


parser.add_argument(
    "--timeout=TIME",
    help="set I/O timeout in seconds",
    type=int,
    default=0,
    dest="timeout"
)

parser.add_argument(
    "--blocking-io",
    action="store_true",
    help="use blocking I/O for the remote shell",
    dest="blocking"
)

parser.add_argument(
    "-I",
    "--ignore-times",
    action="store_true",
    help=" don't skip files that match size and time",
)

parser.add_argument(
    "--size-only",
    action="store_true",
    help="skip files that match in size",
)

parser.add_argument(
    "--address=ADDRESS",
    action="store_true",
    help="bind address for outgoing socket to daemon",
)

parser.add_argument(
    "--port=PORT",
    action="store_true",
    help="specify double-colon alternate port number",
)

parser.add_argument(
    "--list-only",
    action="store_true",
    help="list the files instead of copying them",
)
parser.add_argument(
    "--server",
    action="store_true",
    help="used in ssh mode, don't type it in commande line"
)

parser.add_argument(
    "SRC",
    help="Adresse source",
    nargs="+"
)

parser.add_argument(
    "DST",
    help="Adresse destination",
    nargs='*'
)
args = parser.parse_args()


#End parsing

##############################################################################################

#Values and mode Handler 

def point_finder(s): # a function to detect if a str contains : or ::
    a = s.find(':')
    b = s.find('::')
    if a!=-1 or b!=-1:
        return True
    else:
        return False

def username_finder(s): # a function to detect user name 
    a = s.split('@')
    return a[0]

# Affectation de l'adresse source et de la destination (si définie) & verifications 

SRC = args.SRC

len_SRC = len(SRC)

if len(SRC) >= 2:
    DST = SRC[-1]
elif len(SRC) == 1:
    SRC = SRC[0]
else:
    pass


def mode_finder(SRC,DST): # a function to detect mode
    global mode
    src_point_tester = point_finder(SRC)
    dst_point_tester = point_finder(DST)

    if SRC and DST == '': # mrsync [OPTION]... SRC 
        print('local src')

    if SRC and DST != '': 

        # Search : or :: and assign modes
        
        if src_point_tester == False and dst_point_tester == False: # local source and dest
            mode = 'local'

        if src_point_tester == True and dst_point_tester == False: # distant source, local dest
            mode = 'pull'
            SRC_user = username_finder(SRC)
            
        if src_point_tester == False and dst_point_tester == True : # local source, distant dest
            mode = 'push'
            DST_user = username_finder(DST)

        if src_point_tester == True and dst_point_tester == True : # source and dest local
            mode = 'local'
    return mode