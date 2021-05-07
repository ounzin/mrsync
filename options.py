#!/usr/bin/env python3
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
    action="store_true",
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

len_SRC = len(SRC)

if len(SRC) >= 2:
    DST = SRC[-1]
elif len(SRC) == 1:
    SRC = SRC[0]
else:
    pass


def mode_finder(SRC,DST):
    global mode
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
    return mode