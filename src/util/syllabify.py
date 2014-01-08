    # coding: utf8
'''
Created on Feb 6, 2013

@author: parhamfh
'''

import re

from hmm.model.rhythm.elements import Syllable

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
            self._syllabified_word = word.lower()
            self._original_word = word
            self._debug = debug 
            
        def repl(self, a,b):
            '''
            Replace character <a> with <b> in self.word.
            
            Ignores case.
            '''
            if self.debug:
                print u"{0}: repl(a='{1}' b='{2}')".format(self.s_word, a , b)

            self.s_word = self.s_word.replace(a,b)
        
        @property
        def final_word(self):
            try:
                return self._final._word
            except:
                self.finalize_syllabification()
                return self._final_word
        
        def finalize_syllabification(self):
            self._final_word = self.original_word
            s = self.s_word
            
            if self.debug:
                print u'Finalize Word: {0} with {1}'.format(self.original_word,
                                                             self.s_word)
                print self._final_word
                print s, "length: ", self.s_length
                print range(self.s_length)
            
            for i in range(self.s_length):
                if s[i] == '.':
                    self._final_word = self._final_word[:i]+'.'+self._final_word[i:]

                
        @property
        def original_word(self):
            return self._original_word
        
        @property
        def s_word(self):
            return self._syllabified_word
        
        @s_word.setter
        def s_word(self, x):
            self._syllabified_word = x
        
        @property
        def syllabified_word(self):
            import sys
            sys.stderr.write('WARNING! Do not use this property!'+\
                             ' Use s_word property instead.')
            return self.s_word

        @property
        def s_length(self):
            return len(self.s_word)
            
        def replace_s_word(self, new_word):
            self.s_word = new_word
    
        @property
        def debug(self):
            return self._debug

    def __init__(self, ortographic_text):
        '''
        @param ortographic_text: The ortographic text to be syllabifyed.
        @type ortographic_text: String
        '''
        self.ortographic_text = ortographic_text
        
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
                w = self.Word(word, debug=False)
                self.syllabify_word(w)
                words.append(w.final_word)
            self._syllables.append(words)

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
        sub_str = u'a i u e o y å ä ö'.split() 
        map(lambda x: word.repl(x,u"{0}.".format(x)), sub_str)
        
        # approach 2 - breaks step 2.3 and requires that Word class stores
        # self._word as a unicode string (unicode) and not byte string (str).
        
        # unicode_substr = u'aiueoyåäö'
        # map(lambda x: word.repl(x,u"{0}.".format(x)), unicode_substr)
        
        # If last letter is a vowel, last character will be a dot. Remove it.
        if word.s_word[-1] == '.':
            word.replace_s_word(word.s_word[:-1])
        
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
        last_index = word.s_length-1
        i = 0
        
        while i < last_index:
            if not skip_next:
                # Long consonant, so split consonants (rule 2.1)
                if word.s_word[i] == word.s_word[i+1]:
                    skip_next = True
                    word.replace_s_word(word.s_word[:i+1] + "." + word.s_word[i+1:])
                    # Skip the syllable boundary marker
                    i += 1
                    # Since we added an extra character the string is longer
                    last_index += 1
            elif skip_next:
                skip_next = False
            i += 1

    def _merge_consonant_clusters(self, word):
        '''
        Exercises Rule 2.2 on word
        Apply fonotactic rules.
        
        
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
        new = word.s_word.split('.')
        pattern = re.compile(u'[aiueoyåäö]', re.IGNORECASE)
        
        last_index = len(new)
        i = 0

        while i < last_index:
            if not pattern.search(new[i]):
                # isolated consonant/s
                # join with left syllable group
                new[i-1] = new[i-1]+new[i]
                new.pop(i)
                # Moving pointer left, since we removed item (list is smaller)
                i -= 1 
                last_index -= 1
            i += 1
        
        word.replace_s_word('.'.join(new))
        
    @property
    def syllables(self):
        return self._syllables

    def get_syllable_set(self):
        return self.syllables
    
class MockSyllabifyer(object):
    
    def get_syllable_set(self):
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

# SHOULD BE DICT INSTEAD - why?
class SyllableSet(list):
        pass
#    def __init__(self, length):
#        