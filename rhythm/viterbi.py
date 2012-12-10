'''
    Viterbi implementation modified for an HMM with two emissions,
    one occuring over transitions (edges) and one from a state.

    Based on algorithm on U{en.wikipedia.org<http://en.wikipedia.org/wiki/Viterbi_algorithm>}. 
'''
import numpy

DEBUG=True

def dprint(s):
    if DEBUG:
        print "<DEBUG>",s

def viterbi(observed, B, T, start_p, p, q=None):
    '''
        Run the Viterbi algorithm against our
        rhythm model which is a Mealy type HMM.

        @param B: the set of the 32 hidden states (the beats)
        @type B: list
        @param p: the duration emission probability for each state
        @type p: numpy.matrix
        @param observed: set of observed syllables
        @type observed: list
        @param T: transition matrix for hidden states
        @type T: numpy.matrix
        @param start_p: start probabilities for the states
        @type start_p: list of probabilities
        @param q: the accent emission probability for each state.
                    Default is None.
        @type q: numpy.matrix
    '''
    o_len = len(observed)

    T1 = numpy.matrix( [ [y for y in numpy.zeros(o_len)] for x in numpy.zeros(len(B)) ] )
    T2 = numpy.matrix( [ [y for y in numpy.zeros(o_len)] for x in numpy.zeros(len(B)) ] )
    
    if q is None:
        dprint("q is: None")
    else:
        # dprint("q is: %s\n"%q.__name__)
        raise RuntimeError
    dprint("For observations %s: %s \n"%(0, observed[0]))
    for b in B:
        if q is None:
            dprint(start_p[b.i] * p(b, observed[0]))
            T1[b.i,0] = (start_p[b.i] *
                    p(b, observed[0])) 
            dprint(T1[b.i,0])
        elif q is not None:
            raise RuntimeError
            # T1[b.i,0] = (start_p[b.i] *
            #         p(b, observed[0]) *
            #         q(b, observed[0]))
            # dprint(T1[b.i,0])
        else:
            raise RuntimeError("What is wrong with q?")
        
        T2[b.i,0] = 0

    for i in range(1,o_len):
        dprint("For observations %s: %s "%(i, observed[i]))
        for b in B:
            (pk, k) = transition_max_k(i, T1, b, B, T, observed, p, q)
            T1[b.i,i] = pk
            T2[b.i,i] = k.i
        
    #experimental
    (zp, sz) = final_state_max_k(o_len-1, T1, B)

    #initialize path vector
    x = [0] * o_len

    #set max
    x[o_len-1] = B[sz.i]
    dprint("\n final round shows this yo state %s (p=%s)"%(sz,zp))
        
    # Range generated is not inclusive right value!
    # Last item in list is 1 not 0! ARGH!
    for i in range(o_len-1, 0,-1):
        # print 'round',i
        (zp, sz) = final_state_max_k(i-1, T1, B)
        dprint("\n final round shows this yo state %s (p=%s)"%(sz,zp))
        # print zp, sz
        x[i-1] = B[sz.i]

    return x

def transition_max_k(j, T1, b, B, T, observed, p, q):
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
    @param observed: set of observed syllables
    @type observed: list
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
    dprint("Finding likely hidden state for time %s to state %s\n"%(j,b))
    if q is None:
        tmpmax = -1
        tmpk = -1
        for k in B:
            # dprint("\n%s\n%s\n%s\n"%
            #     (T1[k.i,j-1],
            #     T[k.i,b.i],
            #     p(b,observed[j])))
            val=T1[k.i,j-1] * T[k.i,b.i]*p(b,observed[j])
            if val>tmpmax:
                tmpmax = val
                tmpk = k
        dprint("MAX prob to %s for time %s given by state %s with %s\n---\n"%(b,j,tmpk,tmpmax))
        return (tmpmax, tmpk)
        # return max([(T1[k.i,j-1] * T[k.i,b.i]*p(b,observed[j]),k) for k in B])
    elif q is not None:
        raise RuntimeError
        # return max([(T1[k.i,j-1] * T[k.i,b.i]*p(b,observed[j])*q(b,observed[j]),k) for k in B])
    else:
        raise RuntimeError("What is wrong with q?")

def final_state_max_k(j, T1, B):
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

    @return: tuplet with two values, first being max 
                probability and second being index of state
                that gives max probability.
    @rtype: tuples
    '''
    return max( [ (T1[k.i,j],k) for k in B] )