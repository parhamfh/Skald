'''
Created on Feb 6, 2013

@author: parhamfh
'''

class SyllableTokenizer(object):
    def __new__(cls, *args, **kwargs):
        if kwargs.pop('mock', None):
            return MockSyllableTokenizer()
        
        return RealSyllableTokenizer(*args, **kwargs)
       
class RealSyllableTokenizer(object):
    
    def __init__(self, list_per_newline = True):
        pass
    
    def get_syllable_set(self):
        pass
    
class MockSyllableTokenizer(object):
    def get_syllable_set(self):
        return 'MOCKENIZER'
    
class SyllableSet(list):
    pass