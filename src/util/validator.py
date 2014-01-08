# coding: utf8

class InputValidator(object):

    ALPHABET = u'abcdefghijklmnopqrstuvwxyzåäö\n '

    def __init__(self, input_text, input_syllables):
        self.text = input_text
        self.syllables = input_syllables
        
    def validate(self):
        '''

        Returns True if valid input, False otherwise
        
        '''
        # Check that there is only Swedish letters
        if not self._check_letters(self.text):
            return False
        
        # Check length of each line (number of characters)
        if not self._check_length_per_line(self.text):
            return False

        # Check number of syllabls per line
        if not self._check_syllables_per_line(self.syllables):
            return False
        
        # Check number of lines
        if not self._check_dispersion(self.syllables):
            return False
        
        return True

    def _check_letters(self, text):
        for letter in text:
            if letter.lower() not in self.ALPHABET:
                print u"Letter '{0}' is not an accepted letter.\n".format(letter)
                return False
        return True

    def _check_length_per_line(self, text):
        '''
        
        len(u'norrländskornas '*10) = 160 approximately 140 chars

        '''
        for line in text.split('\n'):
            if not len(line) <= 160:
                print u"Line '{0}' is over 160 characters.\n".format(line)
                return False
        return True

    def _check_syllables_per_line(self, syllable_set):
        for line_of_syllables in syllable_set:
            num_syllables = 0
            for word in line_of_syllables:
                num_syllables += len(word.split('.'))
            if not 0 < num_syllables <= 32:
                print u'Too many syllables ({0}) in line.\n'.format(num_syllables)
                return False

        return True
    
    def _check_dispersion(self, syllabel_set):
        '''
        
        +++ OLD +++

        Each staff is a maximum of 32 syllables, each syllable representing at 
        the least a 16th note, this means that 32 syllables at most can make up
        2 bars. There is a maximum of 4 staffs. 
        
        This means that the user can specify up to 4 lines of text with a
        maximum of 32 syllables in each line. Empty staffs will be filled out
        with rest notes. 
        
        '''
        return True

class ValidationFailedException(RuntimeError):
    pass