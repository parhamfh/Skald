
from abc import ABCMeta, abstractmethod, abstractproperty
def blaj():
    print 'ko'
class HmmModel(object):
    __metaclass__ = ABCMeta 
    
    DEBUG = False
        
    def _set_debug(self, debug):
        self.DEBUG = debug

    def dprint(self, s=""):
        if self.DEBUG:
            print "<DEBUG>",s
    
    @abstractproperty
    def start_probabilities(self):
        '''
        Return's the start probabilities for the model's hidden states.
        Used for the first timestep (t=0) in the Viterbi algorithm.
        '''
        
    @abstractproperty
    def emission_probabilities(self):
        '''
        Returns the model's hidden states emission probabilities.
        '''
    
    @abstractproperty
    def transition_probabilities(self):
        '''
        Returns the transition probabilities between the model's hidden states.
        '''
    
    @abstractproperty
    def hidden_states(self):
        '''
        Returns the hidden states of this model
        '''

    @abstractmethod
    def emission_p_of_state(self, state, emission):
        '''
        Return the probability that this state emits this observation
        
        @param state: The hidden state whose emission probability you seek 
        @type state: L{HmmModelHiddenState}
        '''
        