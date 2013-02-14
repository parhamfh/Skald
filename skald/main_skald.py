'''
Created on Jan 3, 2013

@author: parhamfh
'''
import random
import sys

from skald.hmm import Hmm
from skald.hmm.model.rhythm import RhythmModel
from skald.hmm.model.rhythm.elements import BeatPathSet, BeatPair

from skald.lilypond.ponder import Ponder

from skald.parser import InputParser
from skald.util.syllabification import SyllableTokenizer, SyllableSet
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
        self.mock = mock
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

            self.raw_input = self.query_for_input(mock)

            s_tokenizer = SyllableTokenizer(self.raw_input, mock = mock)

            #returns a SyllableSet
            self.syllables = s_tokenizer.get_syllable_set()

            if not self.validate_input(self.syllables):
                raise RuntimeError('Invalid input.'\
                            'Please check input constraints.')

            ## SEE GITHUB issues! Mock stuff here anyway
            self.phonemes = self.transcribe_input(mock = mock)
            
            self.mark_syllables_for_stress(self.syllables, self.phonemes)

    def run_model(self, no_score = False):
        self.observations= self.syllables
        if isinstance(self.observations, SyllableSet):
            o_len = len(self.observations)
            self.hmm = [None] * o_len
            self.beat_paths = BeatPathSet(o_len)

            for i in range(o_len):
                self.hmm[i] = Hmm(RhythmModel, self.observations[i])
                self.beat_paths[i] = self.hmm[i].find_most_likely_state_seq()
                self.hmm[i].print_path()
                # TODO: circumventing BeatPaths lacking implementation
                # It should wrap it's list properly instead of
                # explicitly referencing the internal 'path' variable 
                self.hmm[i].model.print_beats(self.beat_paths[i].path, self.observations[i])
                # TODO: fix this, very ugly!
                BeatPair._reset_object_counter()
                
            if not no_score:
                self.generate_lilypond_score(self.beat_paths, self.observations, 32*o_len)
        else:
            self.hmm = Hmm(RhythmModel, self.observations)
            self.path = self.hmm.find_most_likely_state_seq()
            self.hmm.print_path()
            self.hmm.model.print_beats(self.path, self.observation)
        
            if not no_score:
                self.generate_lilypond_score(self.path, self.observed, 32)
    
    def generate_lilypond_score(self, xpath, observations, num_beats):
#        pon = Ponder(xpath,num_beats/16, observations)
        pon = Ponder(xpath, observations)
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
        
        sys.stdout.write('\nWARNING! Validation not implemented in Skald \n\n')
        # Check that there is only Swedish letters

        # Check length of each line (number of syllables)
#        self.check_dispersion(syllables)
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
        if self.mock:
            for i in [0,2,3,4,7,10,11,13]:
                syllables[0][i].e="STRESSED"
#            print syllables[0]
#            print
            for i in [0,2,4,5,6,7,8,11,12]:
                syllables[1][i].e="STRESSED"
#            print syllables[1]
#            print
            for i in [0,1,2,5,6,7,8,11,12]:
                syllables[2][i].e="STRESSED"
#            print syllables[2]
#            print
            for i in [0,3,5,8,10,11,12]:
                syllables[3][i].e="STRESSED"
#            print syllables[3]
#            print
#            for s in self.syllables:
#                print '---'
#                print s
            return syllables
        else:
            print 'Stress marking Not implemented yet...'
        
