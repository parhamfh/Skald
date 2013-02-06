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
    
    def prompt_for_input(self, custom_text = None, read_from_file=False):
        
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