# coding: utf8
'''
Created on 25 May, 2013

@author: parhamfh
'''

from util import InputParser, Syllabifyer, PhoneticTranscriber, SyllableSet, InputValidator

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
        # stored in self.user_input
        self.get_input()

        # STEP 1: Syllabify ortographic text

        syllabifyer = Syllabifyer(self.ortographic_text, mock = self.mock)
        syllabifyer.syllabify()
        self.syllables = syllabifyer.get_syllable_set()
        
        # STEP 1.5: VALIDATE INPUT
        self.validate_input(self.user_input, self.syllables)
            

        print
        print '\n-----\n'.join(' ||| '.join(y for y in x ) for x in self.syllables)
        
        """ SAME STEP """
        # STEP 2: Translate user input to phonetic version (maybe remotely)
        self.phonetic_text = self.transcribe_input(self.ortographic_text,
                                                mode = PhoneticTranscriber.REMOTE,
                                                protocol = 'UDP',
                                                mock = self.mock)

        # IF DEBUG
        print "\nPrinting data to validate."
        for line in self.phonetic_text:
            for w in line:
                print u"{0} == became ==> {1}".format(w[0],w[1])
        # STEP 3: Syllabify phonetic text (using external binary)
        
        """ /SAME STEP"""
        
        # STEP 4: Fuse together syllables and phoneme syllable (not syllables...) in one
        # Observation object
        return self.mark_syllables_for_stress(self.syllables, self.phonetic_text)

    def query_for_input(self, mock = None):
        p = InputParser(mock = mock)
        return p.prompt_for_input()

    def validate_input(self, input_text, syllables):
        
        validator = InputValidator(input_text, syllables)
        if not validator.validate():
            raise RuntimeError('Invalid input. '\
                    'Please check input constraints.')
    
    def transcribe_input(self, text_input = None, mode = None, protocol = None, mock = None):
        if not text_input:
            text_input = self.raw_input

        ph = PhoneticTranscriber(text_input, mode = mode, protocol = protocol, mock = mock)
        
        transcribed_input = ph.transcribe()
        return transcribed_input
    
    def mark_syllables_for_stress(self, syllables, phonemes):
        '''


        @param syllables: A list of lists of syllables; each list of syllables represents a line in the input. 
        @type syllables: u{SyllableSet}
        @param phonemes: 
        '''
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
            from hmm.model.rhythm.elements import Syllable
            WORD_INDENT = "    "
            # For each line of text of input
            line = 0
            line_list = SyllableSet()
            print '====== +++ MARKING FOR STRESS +++ ======'
            print 'Number of lines:' , len(syllables)
            print 'phonemes: ', phonemes
            print 'syllables: ', syllables
            print '========================================'
            while line < len(syllables):
                print "\nThe {0} line.".format(line+1)
                line_orto_words = syllables[line]
                print 'line_words: ', line_orto_words
                line_phonetic_words = phonemes[line]
                # print 'line_phonemes: ', line_phonetic_words

                word_list = []
                # 0. For EACH word in the line
                word = 0
                while word < len(syllables[line]):
                    # print WORD_INDENT+"Word {0}".format(word+1)
                    syllable_list = []

                    # 1. Determine which syllable has the stress for that word
                    print u"\nDEBUG: Printing syllabified ortographic word for reference: {0}".format(line_orto_words[word])
                    stressed_syllable_index = self.find_phoneme_stress(line_phonetic_words[word])
                    
                    # 2. Create Syllables objects from the ortographic syllables and mark for stress
                    # Iterate over the syllables in the word
                    orto_syllables = line_orto_words[word].split('.')
                    orto_index = 0
                    while orto_index < len(orto_syllables):
                        # print type(orto_syllables[orto_index]), type(line_orto_words[word])
                        # print orto_index
                        # print "Vad gör du inte härt."

                        # 3. Create a Syllable object and add information about the original word
                        if orto_index == stressed_syllable_index:
                            syllable_list.append(Syllable(orto_syllables[orto_index],u"SHORT",u"STRESSED", orig_word = line_orto_words[word]))
                        else:
                            syllable_list.append(Syllable(orto_syllables[orto_index],u"SHORT",u"UNSTRESSED", orig_word = line_orto_words[word]))
                        orto_index += 1

                    word_list.extend(syllable_list)
                    word += 1

                line_list.append(word_list)
                line += 1

            # IF DEBUG
            # for l in line_list:
            #     for s in l:
            #         print s
            return line_list
            
    def find_phoneme_stress(self, phonemes):
        # This algorithm should use the same way of counting syllables as the
        # Syllabifier but should also remember which one has the stress
        # print u'DEBUG: Unmassaged phonemes ',phonemes
        phoneme= self._massage_phonetic_word(phonemes[1])
        # print u'DEBUG: massaged phonemes: ', phoneme
        syllabifyer = Syllabifyer(phoneme, mock = self.mock)
        syllabifyer.syllabify()

        # WILL ALWAYS ONLY BE ONE WORD
        syllables = syllabifyer.get_syllable_set()[0][0]
        print u"DEBUG: find_phoneme_stress | Final output: {0}".format(syllables)

        i = 0 
        ss = syllables.split(".")
        while i < len(ss):
            if "'" in ss[i]:
                return i
            i += 1
        return 0

    def _massage_phonetic_word(self, phonemes):
        phoneme = phonemes.replace('{\\"}','"')
        phoneme = phoneme.replace("{\\'}","'")
        phoneme = ''.join(phoneme.split())
        return phoneme
