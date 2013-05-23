# coding: utf8
'''
Created on Jan 3, 2013

@author: parhamfh
'''
import random
import sys

from skald.hmm import Hmm
from skald.hmm.model.rhythm import RhythmModel
from skald.hmm.model.rhythm.elements import BeatPathSet, BeatPair

from skald.formatter.lilypond import LilypondFormatter
from skald.formatter.orpheus import OrpheusFormatter

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
        if mock:
            if mock > 1:
                self.mock_hmm = True
            else:
                self.mock_hmm = False
            self.mock = True
        
        self.health_model = health_model
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


            '''
                THIS IS A REALLY STRANGE PROCESS
                
                should be that you take in input
                - transcribe it phonetically
                - then somehow syllabalize the phonetic (which we want only for
                    stress currently) and the normal representations
                - link them, and make sure the right syllables retain the 
                    correct stress markers/values
                    
                Also look over how data is passed
                some of it is passed to functions, like the mock
                and sometimes it is stored in global attributes
                (raw_input, phonemes, etc). Is this consistent behaviour?
                I think that they should be passed, but saved in attributes.
                Fetched when they are supplimental, and given as parameters
                when they are the object of transformation, data source etc to
                a function.
                
            '''
            s_tokenizer = SyllableTokenizer(self.raw_input, mock = mock)

            #returns a SyllableSet
            self.syllables = s_tokenizer.get_syllable_set()

            if not self.validate_input(self.syllables):
                raise RuntimeError('Invalid input.'\
                            'Please check input constraints.')

            self.phonemes = self.transcribe_input(mock = mock)
            
            self.mark_syllables_for_stress(self.syllables, self.phonemes)

    
    def run(self, no_score = False, no_orpheus = False):
        if self.health_model:
            sys.exit("You cannot use run() when using the Health model. Exiting...")

        if self.mock_hmm:
            self.mock_model()
        else:            
            self.run_model()
            
        if not no_score:
            self.generate_lilypond_score(self.beat_paths, self.observations)
            
        if not no_orpheus:
            self.generate_orpheus_output(self.beat_paths, self.observations)

    def mock_model(self):
        self.observations = self.syllables

        from skald.hmm.model.rhythm.elements import BeatPath
        
        self.beat_paths = BeatPathSet(8, paths = [
                                BeatPath(0, [BeatPair(16, 21, idx=397), BeatPair(23,23, idx=483), BeatPair(24,25, idx=493), BeatPair(26,26, idx=507), BeatPair(27,27, idx=513), BeatPair(28,28, idx=518), BeatPair(29,29, idx=522), BeatPair(30,31,idx=526)]),
                                BeatPath(1, [BeatPair(16,25, idx=401), BeatPair(26,26, idx=507), BeatPair(27,27, idx=513), BeatPair(28,28, idx=518), BeatPair(29,29, idx=522), BeatPair(30,31, idx=526)]),
                                BeatPath(2, [BeatPair(16,20, idx=396), BeatPair(22,22, idx=473), BeatPair(24,26, idx=494), BeatPair(27,27, idx=513), BeatPair(28,29, idx=519), BeatPair(30,31, idx=526)]),
                                BeatPath(3, [BeatPair(16,17, idx=393), BeatPair(20,22, idx=452), BeatPair(24,25, idx=493), BeatPair(26,26, idx=507), BeatPair(27,27, idx=513), BeatPair(28,29, idx=519), BeatPair(30,31, idx=526)]),
                                BeatPath(4, [BeatPair(16,17, idx=393), BeatPair(20,22, idx=452), BeatPair(24,25, idx=493), BeatPair(26,26, idx=507), BeatPair(27,27, idx=513), BeatPair(28,29, idx=519), BeatPair(30,31, idx=526)]),
                                BeatPath(5, [BeatPair(16,22, idx=398), BeatPair(24,25, idx=493), BeatPair(26,26, idx=507), BeatPair(27,27, idx=513 ), BeatPair(28,29, idx=519), BeatPair(30,31, idx=526)]),
                                BeatPath(6, [BeatPair(16,19, idx=395), BeatPair(21,21, idx=462), BeatPair(23,23, idx=483), BeatPair(24,25, idx=493), BeatPair(26,26, idx=507), BeatPair(27,27, idx=513), BeatPair(28,28, idx=518), BeatPair(29,29, idx=522), BeatPair(30,31, idx=526)]),
                                BeatPath(7, [BeatPair(22,22, idx=473), BeatPair(24,27, idx=495), BeatPair(28,28, idx=518), BeatPair(29,29, idx=522), BeatPair(30,31,idx=526)])]
                                         )

    def run_model(self):
        self.observations = self.syllables
        # Sets of Syllables
#        if isinstance(self.observations, SyllableSet):
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
            

    def generate_lilypond_score(self, xpaths, observations):
#        pon = LilypondFormatter(xpath,num_beats/16, observations)
        pon = LilypondFormatter(xpaths, observations)
        pon.make_ly_file()
    
    def generate_orpheus_output(self, paths, observations):
        orp = OrpheusFormatter(paths, observations, 
                               output_format=OrpheusFormatter.STDOUT)
        orp.make_rhythm_file()
        
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

#            for s in self.syllables:
#                print '---'
#                print s
            return syllables
        
        else:
            print 'Stress marking Not implemented yet...'
        