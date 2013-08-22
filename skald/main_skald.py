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

from skald.pd.sounder import Sounder

from skald.handler.user_input import UserInputHandler

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
        else:
            self.mock = False
        
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
            
            self.uinput_handler = UserInputHandler(self.mock)

    def run(self, no_lilypond = False, no_orpheus = False):
        if self.health_model:
            sys.exit("You cannot use run() when using the Health model. Exiting...")
        
        # List of observations (SyllableSet). One list for each row. 
        # Each row list contains lists of Syllable objects
        # representing the words.
        self.observations = self.uinput_handler.input_to_observations()
        

        # print self.observations
        # raise RuntimeError('Innan här!')
    
        if self.mock:
            if self.mock_hmm:
                self.mock_model()
        else:            
            self.run_model()
            
        if not no_lilypond:
            self.generate_lilypond_score(self.beat_paths, self.observations)
            
        if not no_orpheus:
            self.generate_orpheus_output(self.beat_paths, self.observations)

    def mock_model(self):
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
