# coding: utf8

'''
Created on Feb 6, 2013

@author: parhamfh
'''
import re

from skald.hmm.model.rhythm.elements import Syllable

class Syllabifyer(object):
    '''
    See the following Github issue for a discussion regarding the current and 
    desired solution for mocking:
    
    https://github.com/parhamfh/Skald/issues/17
    '''
    def __new__(cls, *args, **kwargs):
        if kwargs.pop('mock', None):
            return MockSyllabifyer()
        
        return RealSyllabifyer(*args, **kwargs)
       
class RealSyllabifyer(object):
    
    class Word(object):
        '''
        Help class for manipulating words when syllabifying them
        '''
        def __init__(self,word, debug = False):
            self._word = word
            self._debug = debug 
        def repl(self, a,b):
            '''
            Replace character <a> with <b> in self.word.
            
            Ignores case.
            '''
            if self._debug:
                print "{0}: repl(a='{1}' b='{2}')".format(self._word, a , b)
            self._word = self._word.replace(a,b)
        @property
        def word(self):
            return self._word
        
        @property
        def length(self):
            return len(self.word)
            
        def replace_word(self, new_word):
            self._word = new_word

    def __init__(self, ortographic_text, list_per_newline = True):
        '''
        If list_per_newline is true all syllables will be put in one list,
        meaning that the entire purpose of dividing up the syllables by sentence
        which is needed for using them as input to the model is disregarded.
        Why this functionality exists is not clear. Debugging?
        
        @param ortographic_text: The ortographic text to be syllabifyed.
        @type ortographic_text: String
        @param list_per_newline: Put all syllables in one list or per sentence.
        @type list_per_newline: bool
        '''
        self.ortographic_text = ortographic_text
        self.list_per_newline = list_per_newline
        
    def syllabify(self):
        '''
        Returns a list of syllables per sentence. The syllables are grouped in
        lists per word. 
        
        Example:
        
        Input:
            'Min fader är här."
        
        Output:
            [['Min'],['Fa','der'],['är'],['här']]
        '''
        self._syllables = []
        for sentence in self.ortographic_text.split('\n'):
            words = []
            for word in sentence.split():
                w = self.Word(word)
                self.syllabify_word(w)
                words.append(w.word)
            self._syllables.append(words)
        print self.syllables

    def syllabify_word(self, word):
        '''
        Syllabify word according to Bannerts 2 rules.
        
        Rule 1. Insert a syllable boundary (.):
                    (a) after each vowel (between V and C)
                    (b) between vowels

        Rule 2. Adjust to the following structural conditions: 
            2.1 Long consonants: split the long C: into two C, 
                the first one becomes coda
            2.2 Consonant cluster: move syllable boundary to the right as 
                phonotactic constraints permit. 
            2.3 Isolated consonants or clusters (left overs): adjoin to the 
                left (delete syllable boundary according to Rule 1)
        '''
        # RULE 1 (Basically a dot after each vowel)
        
        # approach 1 (preferred)
        sub_str = 'a i u e o y å ä ö'.split() 
        map(lambda x: word.repl(x,"{0}.".format(x)), sub_str)
        
        # approach 2 - breaks step 2.3 and requires that Word class stores
        # self._word as a unicode string (unicode) and not byte string (str).
        
        # unicode_substr = u'aiueoyåäö'
        # map(lambda x: word.repl(x,u"{0}.".format(x)), unicode_substr)
        
        # If last letter is a vowel, last character will be a dot. Remove it.
        if word.word[-1] == '.':
            word.replace_word(word.word[:-1])
        
        # RULE 2
        ## 2.1
        self._split_long_consonants(word)
        ## 2.2
        self._merge_consonant_clusters(word)
        ## 2.3
        self._ljoin_isolated_consonants(word)
         
        
    def _split_long_consonants(self, word):
        '''
        Exercises Rule 2.1 on word
        '''
        skip_next = False
        last_index = word.length-1
        i = 0
        
        while i < last_index:
            if not skip_next:
                # Long consonant, so split consonants (rule 2.1)
                if word.word[i] == word.word[i+1]:
                    skip_next = True
                    word.replace_word(word.word[:i+1] + "." + word.word[i+1:])
                    # Skip the syllable boundary marker
                    i += 1
                    # since we added an extra character the string is longer
                    last_index += 1
            elif skip_next:
                skip_next = False
            i += 1

    def _merge_consonant_clusters(self, word):
        '''
        Exercises Rule 2.2 on word
        
        
        
        http://www.liu.se/ikk/ssa/ssa1/powerpoint/1.362742/Powerpoint3fonetikSSA.pdf
        Så fonotaxiska regler gäller även för stavelser? så klart?
        
        t.ex word before isolation: o.m.ma.na.pa.rsi.g
        ??
        
        <rs> är inte tillåten enligt fonotaxiska regler i svenskan så vi flyttar
        in en gräns? behöver lista av tillåtna 
        
        så vad ska jag göra?
        
        move syllable boundary to the right as 
                phonotactic constraints permit.
                
        är lite luddigt.
        
        ett kluster av konsonanter ser väl ut så här .kskw. och då ska jag
        _lägga_ ut nya gränser? finns ju inga gränser att flytta på eller hur?
        kommer ju aldrig titta på en grupp som t.ex .l.ls.
        
        eller ska jag flytta?
        
        ['nor', 'rla', 'ndska']

        i det har fallet ska r:et i 'rla' till vänster eller hur? och
        nd ska till vänster i 'ndska'
        
        DETTA FUNKAR för det som står i vägen är dubbel konsonanter, och de
        har vi tagit hand om då vi bestämt att den vänstra konsonanten i ett
        sådant par blir en koda. Vi ska med andra ord inte flytta in den igen
        genom att flytta gränsen över det högra paret igen.
        
        t.ex det ovan
        
        nor rla 
        
        ska vi inte titta på 'rrla' utan 'rla' för vänstra äret är redan bundet
        till 'no'
        
        men 2.1 och 2.2 kanske kan slås ihop för det sker samtidigt när vi
        programmerar det?
        
        
        BEHOVER LISTA PA FONOTAKTISKT TILLÅTNA KOMBINATIONER
        
        dessutom... jag använder ju grafem, medan fonotaktiska regler
        beskriver hur det funkar för _fonem_ så ... vi blundar för det bara?
        vad kan jag skriva i rapporten? :)
         
        '''
        pass
    
    def _ljoin_isolated_consonants(self, word):
        '''
        Exercises Rule 2.3 on word
        '''
        new = word.word.split('.')
        pattern = re.compile('[aiueoyåäö]')
        
        last_index = len(new)
        i = 0
        while i < last_index:
            if not pattern.search(new[i]):
                # isolated consonants
                # join with left syllable group
                new[i-1] = new[i-1]+new[i]
                new.pop(i)
                # Moving pointer left, since we removed item (list is smaller)
                i -= 1 
                last_index -= 1
            i += 1
        
        word.replace_word('.'.join(new))
        
    @property
    def syllables(self):
        return self._syllables

    def get_syllable_set(self):
        return self.syllables
    
class MockSyllabifyer(object):
    
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
                    Syllable('att','SHORT','UNSTRESSED')])
                    
        ss.append([Syllable('hög','SHORT','UNSTRESSED'),
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
                    
                    Syllable('upp,','SHORT','UNSTRESSED')])
                    
        ss.append([Syllable('dit','SHORT','UNSTRESSED'),
                    
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
                    
                    Syllable('mig','SHORT','UNSTRESSED')])
                    
        ss.append([Syllable('än','SHORT','UNSTRESSED'),
                    
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
                    
                    Syllable('krans','SHORT','UNSTRESSED')])
                    
        ss.append([Syllable('om','SHORT','UNSTRESSED'),
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