#!/usr/local/bin/python

import argparse
import time

from skald import Skald

parser = argparse.ArgumentParser(description='Run and calculate the rhythm model for Skald.')
parser.add_argument('-m','--model', nargs='?', dest='model_choice', default='R',
                    choices=['R','H'],
                    help="the HMM model you wish to run. R for rhythm model, H for health model. (default: Skald's (R)hythm model)")
parser.add_argument('-l','--no-lilypond', dest='no_lilypond', action='store_true',
                    help="Do not generate a lilypond score.")
parser.add_argument('-o','--orpheus', dest='no_orpheus',action='store_true',
                    help="Do not produce output for Orpheus.")
parser.add_argument('-M','--mock', dest='mock', action='count',
                    help="Mock input. If '-M' flag is given twice also mocks "+ 
                    "calculations")
#parser.add_argument('-t',choices=['input','transcribing']
                    # help='Test only specified functionality/module.')

args = parser.parse_args()

print "------------------------------------------------"
print "|                 S K A L D                    |"
print "------------------------------------------------"

start_time = time.time()

if args.model_choice == 'R':
    print "Generate musical score: {0}".format("Yes" if not args.no_lilypond else "No")
    print "Generate output for Orpheus: {0}".format("Yes" if not args.no_orpheus else "No")
    print ''
#    print args.mock
    s = Skald(mock = args.mock)
    s.run(no_score=args.no_lilypond, no_orpheus=args.no_orpheus)
    
elif args.model_choice == 'H':
    s = Skald(health_model=True, mock = args.mock)
    #s.run()
    
else:
    raise RuntimeError("Unknown choice of model. (should not be possible to get this message)")

end_time = time.time()
print "Execution time: {1} ({0})".format(end_time - start_time,round(end_time - start_time, 6))
# s=Skald()
