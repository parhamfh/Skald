#!/usr/local/bin/python

import argparse

from skald import Skald

parser = argparse.ArgumentParser(description='Run and calculate the rhythm model for Skald.')
parser.add_argument('-m','--model', nargs='?', dest='model_choice', default='R',
                    choices=['R','H'],
                    help="the HMM model you wish to run. R for rhythm model, H for health model. (default: Skald's (R)hythm model)")
parser.add_argument('-n','--no-score', dest='no_score', action='store_true',
                    help="Do not generate a lilypond score.")
parser.add_argument('-M','--mock', dest='mock', action='store_true',
                    help="Mock input")
#parser.add_argument('-t',choices=['input','transcribing']
                    # help='Test only specified functionality/module.')

args = parser.parse_args()

if args.model_choice == 'R':
    s = Skald(mock = args.mock)
#    s.run_model(no_score=args.no_score)
    
elif args.model_choice == 'H':
    s = Skald(health_model=True, mock = args.mock)

else:
    raise RuntimeError("Unknown choice of model. (should not be possible to get this message)")

# s=Skald()
