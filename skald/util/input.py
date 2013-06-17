# coding: utf8
'''
Created on Jan 3, 2013

@author: parhamfh
'''
import sys
from os.path import expanduser

class MetaMock(type):
    '''
    I actually wanted this functionality, together with
    the __new__() function in the InputParser class to be broken out
    into a separate module (skald.misc.mock) but I have not currently been
    successful in getting this to work.
    
    See the following Github issue for a discussion regarding the current and 
    desired solution for mocking:
    
    https://github.com/parhamfh/Skald/issues/17
    '''
    def __call__(self, *args, **kwargs):
        obj = self.__new__(self, *args, **kwargs)
        if "mock" in kwargs:
            del kwargs["mock"]
        obj.__init__(*args, **kwargs)
        return obj

class InputParser(object):
    '''
    InputParser translates the Swedish words into syllables and disperses them 
    across the staffs.
    '''
    MAX_CHARS_LINE =  160
    
    __metaclass__=MetaMock
    
    def __new__(cls, *args, **kwargs):
        if kwargs.pop('mock', None):
            mock_cls = eval('{0}{1}'.format('Mock',cls.__name__))
            return super(mock_cls, mock_cls).__new__(mock_cls)
        return super(cls, cls).__new__(cls,*args, **kwargs)
    
    def __init__(self, user_input = None):
        '''
        Constructor
        '''
        self.raw_user_input = user_input
    
    def prompt_for_input(self, custom_text = None, read_from_file=False):
        
        # Prompt sysin for the text. should be able to pipe in text file
        # via terminal
        inp = self.read_from_stdin('Please enter text to be cadenced.\n'+\
                                   'You can jump to the next line by pressing'+\
                                   ' Enter.\nPress Enter twice to finish.\n')
        return inp
    
    def _read_from_file(self):
        fp = open(expanduser('~/skald/unicode_text'))
        print fp
        with fp as f:
            for l in f.readlines():
                print l

    def read_from_stdin(self, prompt):
        second_newline = False        
        string_buffer = raw_input(prompt).strip()
        
        while not second_newline:
            inpu = raw_input().strip()
            if inpu != '':
                string_buffer += "\n{0}".format(inpu)
            else:
                second_newline = True

        #print "string buffer contains: '{0}'".format(unicode(string_buffer).encode('utf8'))

        print "System stdin encoding is",sys.stdin.encoding
        return unicode(string_buffer, encoding=sys.stdin.encoding)

class MockInputParser(object):

    def prompt_for_input(self, custom_text = None, read_from_file=None):
        with open('resources/mock/mockinput_shortverses') as fp:
            return fp.read()

if __name__ == '__main__':

    ip = InputParser()
    inpu = ip.prompt_for_input()
    print inpu

#    s = raw_input('\n')
#    print s
#    import sys
#    print sys.stdin.encoding
#    import locale
#    print locale.getpreferredencoding()
#    import readline
#    print readline.__doc__