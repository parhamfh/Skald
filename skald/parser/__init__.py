# coding: utf8'
'''
Created on Jan 3, 2013

@author: parhamfh
'''
from os.path import expanduser

from skald.transcribe import Transcriber

class InputParser(object):
    '''
    InputParser translates the Swedish words into syllables and disperses them 
    across the staffs.
    '''
    MAX_CHARS_LINE =  160

    def __init__(self, user_input = None):
        '''
        Constructor
        '''
        self.raw_user_input = user_input
    
    def prompt_for_input(self, custom_text = None):
        
        # Prompt sysin for the text. should be able to pipe in text file
        # via terminal
        inp = self.read_from_stdin('Please enter text to be cadenced.\n')
        return inp
    
    def _read_from_file(self):
        fp = open(expanduser('~/skald/unicode_text'))
        print fp 
        with fp as f:
            for l in f.readlines():
                print l

    def read_from_stdin(self, prompt):
        second_newline = False        
        string_buffer = raw_input(prompt)
        
        while not second_newline:
            inpu = raw_input()
            if inpu != '':
                string_buffer += "\n{0}".format(inpu)
            else:
                second_newline = True
        print "string buffer contains: '{0}'".format(
                                        unicode(string_buffer).encode('utf8'))
        return string_buffer

    def generate_observations(self, syllables):    

        # Translate the input into syllables so each syllable is an entry in
        # the list
#        self.syllables = self.transcribe_input()
#        print syllables

        # Each syllable is an observation, but we can only have 32 syllables
        # per line so they must be dispersed amongst the 4 staves
        observation_sets = syllables if self.check_dispersion(syllables) else "kalas"
        
        ## GENERATE SYLLABLE OBJECTS FROM SYLLABLES
        return observation_sets

    def transcribe_input(self, text_input=None):
        if not text_input:
            text_input = self.raw_input
            
        ph = Transcriber(text_input)
#        transcribed_input = ph.transcribe()
        transcribed_input = 'bolo/{0}'.format(text_input)
        return transcribed_input

    def check_dispersion(self, syllabel_set):
        '''
        Each staff is a maximum of 32 syllables, each syllable representing at 
        the least a 16th note, this means that 32 syllables at most can make up
        2 bars. There is a maximum of 4 staffs. 
        
        This means that the user can specify up to 4 lines of text with a
        maximum of 32 syllables in each line. Empty staffs will be filled out
        with rest notes. 
        '''
        return True


if __name__ == '__main__':

    ip = InputParser()
    inpu = ip.prompt_for_input()
    trans_inpu = ip.transcribe_input(inpu)
    gen_obs = ip.generate_observations(trans_inpu)
    print gen_obs

#    s = raw_input('\n')
#    print s
#    import sys
#    print sys.stdin.encoding
#    import locale
#    print locale.getpreferredencoding()
#    import readline
#    print readline.__doc__