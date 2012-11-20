'''
    Viterbi implementation modified for an HMM with two emissions,
    one occuring over transitions (edges) and one from a state.

    Based on algorithm on U{en.wikipedia.org<http://en.wikipedia.org/wiki/Viterbi_algorithm>}. 
'''
import numpy

def viterbi(B,p,s_observed,T, start_p, q=None):
    '''
        Run the Viterbi algorithm against our
        rhythm model which is a Mealy type HMM.

        @param B: the set of the 32 hidden states (the beats)
        @type B: list
        @param p: the duration emission probability for each state
        @type p: numpy.matrix
        @param s_observed: set of observed syllables
        @type s_observed: list
        @param T: transition matrif for hidden states
        @type T: numpy.matrix
        @param start_p: start probabilities for the states
        @type start_p: list of probabilities
        @param q: the accent emission probability for each state.
                    Default is None.
        @type q: numpy.matrix
    '''
    for b in B:
        if q is None:
            T1[b.i,1] = (start_p(b.i) *
                    p(b.i, s_observed[1].duration))

        if q is not None:
            T1[b.i,1] = (start_p(b.i) *
                    p(b.i, s_observed[1].duration) *
                    q(b.i, s_observed[1].accent))
        
        T2[b.i,1] = 0
    
    s_len = len(s_observed)
    
    for i in range(2,s_len):
        for b in B:
            (pk, k) = transition_max_k(i-1, T1, b, B, T, s_observed, p, q)
            T1[b.i,i] = pk
            T2[b.i,i] = k
    
    #experimental
    (zp, sz) = final_state_max_k(s_len, T1, B, T, s_observed)
    
    #initialize path vector
    x = [0] * s_len

    #set max
    x[s_len-1] = B[sz.i]

    for i in range(s_len-1, 2,-1):
        (zp, sz) = final_state_max_k(i-1, T1, B, T, s_observed)
        x[i-1] = B[sz.i]

    return x

def transition_max_k(j, T1, b, B, T, s_observed, p, q):
    '''
    Returns the next state which maximizes
    probability of transition to that state and
    emission probabilities.
    Returns a tuplet with index of state as well 
    as value of probability.

    @param j: the time for which the emission
                probability is calculated. Is used
                to index T1.
    @type j: int
    @param T1: 2D matrix; where first index, i, is
                state index and second, j, is time of 
                emission. Elements give probability
                of output j being emitted by state i. 
    @type T1: numpy.matrix
    @param b: The state which you are currently in.
    @type b: BeatState.
    @param B: the set of the 32 hidden states (the beats)
    @type B: list
    @param T: transition matrif for hidden states
    @type T: numpy.matrix
    @param s_observed: set of observed syllables
    @type s_observed: list
    @param p: the duration emission probability for each state
    @type p: numpy.matrix
    @param q: the accent emission probability for each state.
                Default is None.
    @type q: numpy.matrix

    @return: tuplet with two values, first being max 
                probability and second being index of state
                that gives max probability.
    @rtype: tuples
    '''
    if q is None:
        return max([(T1[k,j]*T[k.i,b.i]*p(k.i,s_observed[j].d),k) for k in B])

def final_state_max_k(j, T1, B, T, s_observed):
    '''
    Returns the state with maximum
    probability of that state being the state
    outputting the final emission.
    Returns a tuplet with index of state as well 
    as value of probability.

    @param j: the time for which the emission
                probability is calculated. Is used
                to index T1.
    @type j: int
    @param T1: 2D matrix; where first index, i, is
                state index and second, j, is time of 
                emission. Elements give probability
                of output j being emitted by state i. 
    @type T1: numpy.matrix
    @param B: the set of the 32 hidden states (the beats)
    @type B: list
    @param T: transition matrif for hidden states
    @type T: numpy.matrix
    @param s_observed: set of observed syllables
    @type s_observed: list

    @return: tuplet with two values, first being max 
                probability and second being index of state
                that gives max probability.
    @rtype: tuples
    '''