
from abc import ABCMeta, abstractmethod, abstractproperty
def blaj():
    print 'ko'
class HmmModel(object):
    __metaclass__ = ABCMeta 
    
    DEBUG = False
        
    def set_debug(self, debug):
        self.DEBUG = debug

    def dprint(self, s=""):
        if self.DEBUG:
            print "<DEBUG>",s

    
    @abstractproperty
    def hidden_states(self):
        '''
        Returns the hidden states of this model
        '''

    @abstractproperty
    def start_probabilities(self):
        '''
        Return's the start probabilities for the model's hidden states.
        Used for the first timestep (t=0) in the Viterbi algorithm.
        '''

    @abstractproperty
    def transition_probabilities(self):
        '''
        Returns the transition probabilities between the model's hidden states.
        '''

    @abstractproperty
    def emission_probabilities(self):
        '''
        Returns the model's hidden states emission probabilities.
        '''

    @abstractproperty
    def emission_function(self):
        '''
        Returns the function that given a state and an emission calculates
        the probability of that state emitting that particular emission.
        '''

    def emission_p_of_state(self, state, emission):
        '''
        Return the probability that given state emits given observation.
        
        @param state: The hidden state whose emission probability you seek 
        @type state: L{HmmModelHiddenState}
        '''
        return self.emission_function(state, emission)