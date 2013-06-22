# coding: utf8
'''
Created on 25 May, 2013

@author: parhamfh
'''

from skald.util import InputParser, Syllabifyer, PhoneticTranscriber

class UserInputHandler(object):
    
    def __init__(self, mock):
        self.mock = mock
    
    def get_input(self):
        self.user_input = self.query_for_input(self.mock)
    
    @property
    def ortographic_text(self):
        '''
        Basically the user input, maybe in the future
        we might want to change the format, object type or anything else.
        '''
        return self.user_input
    
    def input_to_observations(self):
        
        # STEP 0: Get input from user
        self.get_input()
        # STEP 1: Syllabify ortographic text

        syllabifyer = Syllabifyer(self.ortographic_text, mock = self.mock)
        syllabifyer.syllabify()
        self.syllables = syllabifyer.get_syllable_set()
        
        print
        print '\n-----\n'.join(' ||| '.join(y for y in x ) for x in self.syllables)
        

        
        """ SAME STEP"""
        # STEP 2: Translate user input to phonetic version (maybe remotely)
        self.phonetic_text = self.transcribe_input(self.ortographic_text,
                                                mode = PhoneticTranscriber.REMOTE,
                                                protocol = 'UDP',
                                                mock = self.mock)

        # IF DEBUG
        print len(self.phonetic_text)
        for line in self.phonetic_text:
            for w in line:
                print u"{0} == became ==> {1}".format(w[0],w[1])
        assert False
        # STEP 3: Syllabify phonetic text (using external binary)
        
        """ /SAME STEP"""
        
        # STEP 4: Fuse together syllables and phoneme syllable in one
        # Observation object
        return self.mark_syllables_for_stress(self.syllables, self.phonetic_text)
        
    
        # STEP 5: Validate input
        if not self.validate_input(self.syllables):
            raise RuntimeError('Invalid input.'\
                        'Please check input constraints.')

    def query_for_input(self, mock = None):
        p = InputParser(mock = mock)
        return p.prompt_for_input()

    def validate_input(self, syllables):
        
        raise NotImplementedError('\nWARNING! Validation not implemented in Skald \n\n')
        # Check that there is only Swedish letters

        # Check length of each line (number of syllables)
#        self.check_dispersion(syllables)
        
    
    def transcribe_input(self, text_input = None, mode = None, protocol = None, mock = None):
        if not text_input:
            text_input = self.raw_input

        ph = PhoneticTranscriber(text_input, mode = mode, protocol = protocol, mock = mock)
        
        transcribed_input = ph.transcribe()
        return transcribed_input
    
    def mark_syllables_for_stress(self, syllables, phonemes):
        if self.mock:
            for i in [0,2,3,5,7]:
                syllables[0][i].e="STRESSED"
            
            for i in [0,3,4]:
                syllables[1][i].e="STRESSED"
            
            for i in [0,2,4,5]:
                syllables[2][i].e="STRESSED"
            
            for i in [0, 1, 2,5,6]:
                syllables[3][i].e="STRESSED"
            
            for i in [0,1,2,5,6]:
                syllables[4][i].e="STRESSED"
            
            for i in [0,1,4,5]:
                syllables[5][i].e="STRESSED"
            
            for i in [0,3,5,8]:
                syllables[6][i].e="STRESSED"
            
            for i in [1,2,3]:
                syllables[7][i].e="STRESSED"

            return syllables
        
        else:
            raise NotImplementedError('Stress marking Not implemented yet...')