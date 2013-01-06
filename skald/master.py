'''
Created on Jan 3, 2013

@author: parhamfh
'''

class Master(object):
    '''
    Connects the dots.
    
    Takes in input from user. Converts input to observations
    Loads the model.
    Runs Viterbi algorithm.
    Adjusts probabilities.
    Generates and outputs score sheet.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        