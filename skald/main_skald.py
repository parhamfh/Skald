'''
Created on Jan 3, 2013

@author: parhamfh
'''
import random

from skald.pd.sounder import Sounder
from skald.lilypond.ponder import Ponder
from skald.parser import InputParser
from skald.hmm import Hmm
from skald.hmm.model.rhythm import RhythmModel
from skald.hmm.model.rhythm.elements import Syllable

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


    def __init__(self, health_model=False):
        '''
        Constructor
        '''
        if health_model:
            print 'Running Wikipedia example: Health Model.'
            from skald.hmm.model.health import HealthModel
            from skald.hmm.model.health.elements import Symptom
            observed = [Symptom('normal'), 
                        Symptom('cold'),
                        Symptom('dizzy')]
 
            self.hmm = Hmm(HealthModel, observed)
            self.hmm.find_most_likely_state_seq()
            self.hmm.print_path()
        
        else:
            print 'Running Rhythm Model calculations.'
#            self.observed = [Syllable("Tom","SHORT","UNSTRESSED"),
#                             Syllable("ten","LONG","STRESSED"),
#                             Syllable("par","SHORT","UNSTRESSED")]
            self.user_plain_text = self.query_for_input()
#            self.observed = self.convert_input()


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
    
    def query_for_input(self):
        p = InputParser()
        return p.prompt_for_input()
    
    def convert_input(self):
        pass
        
        