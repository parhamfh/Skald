#!/usr/local/bin/python

from ..elements import HmmModelHiddenState, HmmModelObservation

class HealthCondition(HmmModelHiddenState):
    '''
    Hidden state
    '''

    def __init__(self,n,condition):
        self.i = n
        self.condition = condition

    def __str__(self):
        return self.condition

    def __repr__(self):
        return self.condition

class Symptom(HmmModelObservation):
    def __init__(self,observed_state):
        self.observed_state = observed_state

    @property 
    def feeling(self):
        return self.observed_state

    def __repr__(self):
        return "({0})".format(self.feeling)