'''
Created on Jan 3, 2013

@author: parhamfh
'''
import random


from skald.hmm import Hmm
from skald.hmm.model.rhythm import RhythmModel
#from skald.hmm.model.rhythm.elements import Syllable

from skald.lilypond.ponder import Ponder

from skald.parser import InputParser
from skald.util.syllabification import SyllableTokenizer
from skald.transcribe import PhoneticTranscriber
from skald.pd.sounder import Sounder

class Skald(object):
    '''
    Connects the dots. 
    
    Takes in input from user. Converts input to observations
    Loads the model.
    Runs Viterbi algorithm.
    Adjusts probabilities.
    Generates and outputs score sheet.
    
    Unless you set health_example as True which will try the model math
    against the trivial example on Wikipedia. 
    '''


    def __init__(self, health_model=False, mock = None):
        '''
        Constructor
        '''
        if health_model:
            print 'Running Wikipedia example: Health model.'
            from skald.hmm.model.health import HealthModel
            from skald.hmm.model.health.elements import Symptom
            self.observations = [Symptom('normal'), 
                        Symptom('cold'),
                        Symptom('dizzy')]
 
            self.hmm = Hmm(HealthModel, self.observations)
            self.hmm.find_most_likely_state_seq()
            self.hmm.print_path()
        
        else:
            print 'Running Rhythm model calculations.'
#            self.observed = [Syllable("Tom","SHORT","UNSTRESSED"),
#                             Syllable("ten","LONG","STRESSED"),
#                             Syllable("par","SHORT","UNSTRESSED")]
            self.raw_input = self.query_for_input(mock)
            print self.raw_input
#            s_tokenizer = SyllableTokenizer(self.raw_input, mock = mock)
#
#            #returns a SyllableSet
#            self.syllables = s_tokenizer.get_syllable_set()
#            
#            if not self.validate_input(self.syllables):
#                raise RuntimeError('Invalid input.'\
#                            'Please check input constraints.')
#
#            ## SEE GITHUB issues! Mock stuff here anyway
#            self.phonemes = self.transcribe_input(self.raw_input, mock)
#            
#            self.observations = self.mark_syllables_for_stress(self.syllables, self.phonemes)
#            
#            print self.observations

    def run_model(self, no_score = False):
        self.hmm = Hmm(RhythmModel, self.observed)
        self.path = self.hmm.find_most_likely_state_seq()
        self.hmm.print_path()
        self.hmm.model.print_beats(self.path, self.observed)
        
        if not no_score:
            self.generate_lilypond_score(self.path, self.observed, 32)
    
    def generate_lilypond_score(self, xpath, observations, num_beats):
        pon = Ponder(xpath,num_beats/16, observations)
        pon.make_ly_file()
    
    def send_to_pd(self, xpath, num_beats):
        # print "\nAnd they said, in great unison, that The Path shalt be:"
        sendlist = [(-1,1,b) for b in range(0,num_beats)]
        for x in xpath:
            sendlist[x.origin] = (random.randint(60,80),x.duration,x.origin)
    
        # print sendlist
        sounder = Sounder(num_beats)
        sounder.set_notes(sendlist)
        sounder.send_notes()
    
    def query_for_input(self, mock = None):
        p = InputParser(mock = mock)
        return p.prompt_for_input()
    
    def validate_input(self, syllables):
        # Check that there is only Swedish letters
        
        # Check length of each line (number of syllables)
        self.check_dispersion(syllables)
        return True
    
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

    def transcribe_input(self, text_input = None, mock = None):
        if not text_input:
            text_input = self.raw_input
        
        ph = PhoneticTranscriber(text_input, mock = mock)
        
        transcribed_input = ph.transcribe()
        return transcribed_input
    
    def mark_syllables_for_stress(self, syllables, phonemes):
        pass
        
