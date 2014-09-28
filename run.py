#!/usr/bin/python
# coding: utf8

import argparse
import time
import sys
import os

# INITIALIZE env variables
# TODO: read from a .skald.conf/rc file instead

"""
lägg till så att man väljer om skald servern man startar (run.py) ska transcribe remotely elelr locally, om remotely så måste man ange protokoll samt adress för remote transcriber
"""



parser = argparse.ArgumentParser(description='Run and calculate the rhythm model for Skald.')
parser.add_argument('-m','--model', nargs='?', dest='model_choice', default='R',
                    choices=['R','H'],
                    help="the HMM model you wish to run. R for rhythm model, H for health model. (default: Skald's (R)hythm model)")
parser.add_argument('-l','--no-lilypond', dest='no_lilypond', action='store_true',
                    help="Do not generate a lilypond score.")
parser.add_argument('-o','--no-orpheus', dest='no_orpheus',action='store_true',
                    help="Do not produce output for Orpheus.")
parser.add_argument('-M','--mock', dest='mock', action='count',
                    help="Mock input. If '-M' flag is given twice also mocks "+ 
                    "calculations")
parser.add_argument('-v','--version', dest='version', action='store_true',
                    help="Print Skald version number and exit.")
parser.add_argument('-d','--directory', dest='skald_directory',
                    help='Give absolute path to Skald\'s directory on computer')
#parser.add_argument('-t',choices=['input','transcribing']
                    # help='Test only specified functionality/module.')

args = parser.parse_args()

print "------------------------------------------------"
print "|                 S K A L D                    |"
print "------------------------------------------------"


#SKALD_DIRECTORY = '/Users/pfh/skald'
if args.skald_directory:
    SKALD_DIRECTORY = args.skald_directory
else:
    SKALD_DIRECTORY = os.getcwd()
    print SKALD_DIRECTORY

os.environ['SKALD_DIRECTORY'] = SKALD_DIRECTORY

# Import Skald module
from skald import Skald

# Start timing
start_time = time.time()

if args.version:
    print Skald.__version__
    sys.exit(0)

### SKALD

if args.model_choice == 'R':
    print "Generate musical score: {0}".format("Yes" if not args.no_lilypond else "No")
    print "Generate output for Orpheus: {0}".format("Yes" if not args.no_orpheus else "No")
    print "Current version only supports "
    print ''
    s = Skald(mock = args.mock)
    s.run(no_lilypond=args.no_lilypond, no_orpheus=args.no_orpheus)
    
elif args.model_choice == 'H':
    s = Skald(health_model=True, mock = args.mock)
    #s.run()
else:
    raise RuntimeError("Unknown choice of model. (should not be possible to get this message)")

### ORPHEUS
if s:
    s.prepare_orpheus()
    s.invoke_orpheus()
else:
    raise RuntimeError("Skald not initialized, why?")
    
### FIN
end_time = time.time()
print "Execution time: {1} ({0})".format(end_time - start_time,round(end_time - start_time, 6))
# s=Skald()
