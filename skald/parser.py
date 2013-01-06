'''
Created on Jan 3, 2013

@author: parhamfh
'''

from transcribe import PhoneticTranscriber

class InputParser(object):
    '''
    InputParser translates the Swedish words into syllables and disperses them 
    across the staffs.
    '''

    def __init__(self, user_input):
        '''
        Constructor
        '''
        self.raw_input = user_input
        
    def generate_observations(self):    
        # Translate the input into syllables so each syllable is an entry in
        # the list
        self.syllables = self.transcribe_input()
        print self.syllables
        # Each syllable is an observation, but we can only have 32 syllables
        # per line so they must be dispersed amongst the 4 staves
        self.observation_sets = self.disperse()
        
        return self.observation_sets

    def transcribe_input(self, text_input=None):
        if not text_input:
            text_input = self.raw_input
            
        ph = PhoneticTranscriber(text_input)
        transcribed_input = ph.transcribe()
        
        return transcribed_input

    def disperse(self):
        '''
        Each staff is a maximum of 32 syllables, each syllable representing at 
        the least a 16th note, this means that 32 syllables at most can make up
        2 bars. There is a maximum of 4 staffs. 
        
        This means that the user can specify up to 4 lines of text with a
        maximum of 32 syllables in each line. Empty staffs will be filled out
        with rest notes. 
        '''
        return True

        
        