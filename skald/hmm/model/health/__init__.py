#!/usr/local/bin/python

import numpy

from skald.hmm.model import HmmModel
from skald.hmm.model.health.elements import HealthCondition, Symptom

class HealthModel(HmmModel):
    '''
    Model 
    Copy of the wikipedia example on the Viterbi algorithm.
    '''
    def __init__(self, debug = False):
#        super(HealthModel,self).__init__(debug)
        # Init
        self._set_debug(debug)
        
        # Set model probabilities
        self._hidden_states = [HealthCondition(0,'Healthy'), 
                              HealthCondition(1,'Fever')]

        self.start_p = [0.6, 0.4]  # index: 0 'Healthy', 1 'Fever'
        
        self.emission_p = [{'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
                           {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}]
        
        self.trans_p = numpy.matrix([[0.7, 0.3], [0.4, 0.6]])
        
        self.T = numpy.matrix([[0.7, 0.3],[0.4, 0.6]])
    
    def health_p(self, state, emission):
        return self.emission_probabilities[state.i][emission.feeling]
    
    @property
    def hidden_states(self):
        return self._hidden_states
    @property
    def start_probabilities(self):
        return self.start_p
    @property
    def transition_probabilities(self):
        return self.trans_p
    @property
    def emission_probabilities(self):
        return self.emission_ps
    @property
    def emission_function(self):
        return self.health_p
