'''
Created on Feb 6, 2013

@author: parhamfh
'''

class SyllableTokenizer(object):
    
    
    def __init__(self, list_per_newline = True, mock = False):
        self.MOCK_MODE = mock 
        
    def get_syllable_set(self):
        if self.MOCK_MODE:
            return self._mock_get_syllable_set()
    
    def _mock_get_syllable_set(self):
        return 

class SyllableSet(list):
    pass