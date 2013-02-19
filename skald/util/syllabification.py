# coding: utf8

'''
Created on Feb 6, 2013

@author: parhamfh
'''
from skald.hmm.model.rhythm.elements import Syllable

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
#            self.observed = [Syllable("Tom","SHORT","UNSTRESSED"),
#                             Syllable("ten","LONG","STRESSED"),
#                             Syllable("par","SHORT","UNSTRESSED")]
        ss = SyllableSet()
        ss.append([Syllable('Vo','SHORT','UNSTRESSED'),
                    Syllable('re','SHORT','UNSTRESSED'),
                    
                    Syllable('mig','SHORT','UNSTRESSED'),
                    
                    Syllable('det','SHORT','UNSTRESSED'),
                    
                    Syllable('för','SHORT','UNSTRESSED'),
                    Syllable('un','SHORT','UNSTRESSED'),
                    Syllable('nat','SHORT','UNSTRESSED'),
                    Syllable('att','SHORT','UNSTRESSED'),
                    
                    Syllable('hög','SHORT','UNSTRESSED'),
                    Syllable('tids','SHORT','UNSTRESSED'),
                    Syllable('stolt','SHORT','UNSTRESSED'),
                    
                    Syllable('som','SHORT','UNSTRESSED'),
                    
                    Syllable('des','SHORT','UNSTRESSED'),
                    Syllable('sa','SHORT','UNSTRESSED')])
        
        ss.append([Syllable('kun','SHORT','UNSTRESSED'),
                    Syllable('na','SHORT','UNSTRESSED'),
                    
                    Syllable('lyft','SHORT','UNSTRESSED'),
                    Syllable('a','SHORT','UNSTRESSED'),
                    
                    Syllable('mig','SHORT','UNSTRESSED'),
                    
                    Syllable('upp,','SHORT','UNSTRESSED'),
                    
                    Syllable('dit','SHORT','UNSTRESSED'),
                    
                    Syllable('ej','SHORT','UNSTRESSED'),
                    
                    Syllable('värld','SHORT','UNSTRESSED'),
                    Syllable('ar','SHORT','UNSTRESSED'),
                    Syllable('nas','SHORT','UNSTRESSED'),
                    
                    Syllable('jäkt','SHORT','UNSTRESSED'),
                    
                    Syllable('når','SHORT','UNSTRESSED')])
        
        ss.append([Syllable('och','SHORT','UNSTRESSED'),
                   
                    Syllable('hur','SHORT','UNSTRESSED'),
                    
                    Syllable('vred','SHORT','UNSTRESSED'),
                    Syllable('gat','SHORT','UNSTRESSED'),
                    
                    Syllable('om','SHORT','UNSTRESSED'),
                    Syllable('kring','SHORT','UNSTRESSED'),
                    
                    Syllable('mig','SHORT','UNSTRESSED'),
                    
                    Syllable('än','SHORT','UNSTRESSED'),
                    
                    Syllable('storm','SHORT','UNSTRESSED'),
                    Syllable('ar','SHORT','UNSTRESSED'),
                    Syllable('nas','SHORT','UNSTRESSED'),
                    
                    Syllable('brus','SHORT','UNSTRESSED'),
                    
                    Syllable('går','SHORT','UNSTRESSED')])
        
        ss.append([Syllable('bä','SHORT','UNSTRESSED'),
                    Syllable('ra','SHORT','UNSTRESSED'),
                   
                    Syllable('sol','SHORT','UNSTRESSED'),
                    Syllable('skim','SHORT','UNSTRESSED'),
                    Syllable('rets','SHORT','UNSTRESSED'),
                    
                    Syllable('gyll','SHORT','UNSTRESSED'),
                    Syllable('e','SHORT','UNSTRESSED'),
                    Syllable('ne','SHORT','UNSTRESSED'),
                    
                    Syllable('krans','SHORT','UNSTRESSED'),
                    
                    Syllable('om','SHORT','UNSTRESSED'),
                    Syllable('kring','SHORT','UNSTRESSED'),
                    
                    Syllable('min','SHORT','UNSTRESSED'),
                    
                    Syllable('hjäss','SHORT','UNSTRESSED'),
                    Syllable('a','SHORT','UNSTRESSED')])
        return ss

# SHOULD BE DICT INSTEAD
class SyllableSet(list):
        pass
#    def __init__(self, length):
#        