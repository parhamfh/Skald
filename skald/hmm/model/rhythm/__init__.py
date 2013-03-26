#!/usr/local/bin/python
# coding: utf8

import numpy
import random

from skald.hmm.model import HmmModel
from skald.hmm.model.rhythm.elements import BeatPair, Syllable
from skald.hmm.model.rhythm.exception import BeatTypeException
'''
    Det är konstigt att __init__ tar emot obs, för en HMM ska inte göra det
    implementera ny eller döp om HMMModel till InputOutputModel. 
    För nu måste också u{HealthModel} ta emot den, utan att den använder den.
    eller?

'''
class RhythmModel(HmmModel):
    
    # Prime numbers
    SHORT_BEAT = 7
    GOOD_BEAT = 11
    LONG_BEAT = 2
    BAD_BEAT = 5
    
    def __init__(self, num_beats=32, start_p = None, debug = False, obs = None):        
        
        # Print debug messages?
        self.set_debug(False)
        
        # Number of beats / hidden states
        self.num_beats = num_beats

        # The hidden states
        self.B=[]
        #Only ring for the beats duration or this till the next designated state
        for i in range(0,num_beats):
            for j in range (i,num_beats):
                self.B.append(BeatPair(i,j))
        
        ###################
        
        # The start probabilities for the hidden states
        # (used by viterbi at t=0)
        if start_p is not None:
            self.start_p = start_p
        else:
            # self.start_p = [1.0/len(self.B) for _ in self.B]
            a = [1.0/x for x in range(1,33)]
            self.start_p = [aa/sum(a) for aa in a]

        # The transition probabilities between each hidden state
#        self.T = self.trans_p_input(self.B, len(obs))
#        self.T = self.trans_p_randnorm(self.B, 1)
        self.T = self.trans_p_static(self.B)

        # Generate emission probabilities
        self.emission_p = range(len(self.B))
        self.generate_e_p_static(self.emission_p, self.B)
#        self.generate_e_p_random(self.emission_p, self.B)
        self.dprint("Finished setup of Rhythm model.")
    
    def trans_p_static(self, B):
        '''
        Transition probabilities are deterministically decided for any 
        given number of observations. This equals a true Hidden Markov Model.
        
        Does not model rest and the notes are connected.
        '''
        T = numpy.zeros(shape=(len(B),len(B)))
        for b in B:
            for k in B:
                # STEP 0: Only notes that connect
                if b.to == k.origin-1:
                    self.dprint("connect between {0} and {1}".format(b,k))
                    #STEP 1: Categorize beat pair
                    score = self.beat_score(k)
                    T[b.i][k.i] = score
            su = sum(T[b.i])
            # Normalize to 1
            if su != 0:
                T[b.i] = [round(x/su,7) for x in T[b.i]]
#        numpy.set_printoptions(threshold=numpy.nan)
#        print T
        return T

    def beat_score(self, b):
        '''
        This calculates the score for a beat pair for the static probability
        model. It assumes this note is connected to the previous note (i.e it
        starts right after the previous note, meaning no rests in between).
        
        It gives a score based on the length of the note, premiering notes of
        medium length. If the note is also considered to be "syncopating" it
        will reduce that score.
        
        ===
        
        OLD:
        om den börjar på jämn och slutar på jämn (d.v.s nästa blir udda) 
        så är det en jämn synkoperande not. osv
        
        regel:
        
        jämn/udda beskriver på vilket slag den börjar (d.v.s vilken 
        not den börjar på, i.e b.origin).
        och synkoperande/icke-synkoperande beskriver om nästa börjar på
        jämn eller udda (d.v.s beroende av längden).
        '''
        
        is_syncopating = self.is_syncopating_beat(b)
        length = self.length_of_beat(b)
        
        score = length * (0.7 if is_syncopating else 1)
         
#        if self.is_on_beat(b):
#            return self.ON_BEAT
#        
#        elif self.is_even_beat(b):
#            return self.EVEN_BEAT
#        
#        elif self.is_odd_beat(b):
#            return self.ODD_BEAT
#        
#        elif self.syncopating_beat(b):
#            return self.SYNCOPATED_BEAT
#        else:
#            raise BeatTypeException("Cannot determine type of beat. {0}".format
#                                    (b))
        return score
    
#    def is_on_beat(self, b):
#                
#        # 0, 4, 8 and 12 respectively refer to beat 1, 2, 3 and 4 in 4/4
#        on_beat_range = [i+(16*x) for x in [0, 1] for i in [0,4,8,12]]
#        if b.origin in on_beat_range:
#            if 
#    def is_even_beat(self, b):
#        
#    def is_odd_beat(self, b):
    
    def length_of_beat(self, b):
        '''
        We prefer quarters (crotchets) and eights (quavers), then short beats,
        then long beats, then last comes the bad, quirky and strange beats.
        '''
        # Sixteenths or eighths
        if b.duration <=2:
            return self.SHORT_BEAT
        # Quarter or Half
        elif b.duration in [4,8]:
            return self.GOOD_BEAT
        elif b.duration > 8:
            return self.LONG_BEAT
        else:
            return self.BAD_BEAT

    def is_syncopating_beat(self, b):
        '''
        If the beat ends before a downbeat (a quarter note, crotchet) it means
        that the next beat will be on beat, meaning this beat does not 
        syncopate the rhythm.
        '''
        before_on_beat_range = [i+(16*x)-1 for x in [0, 1] for i in [0,4,8,12]]
        if b.to in before_on_beat_range:
            return False
        else:
            return True

    def trans_p_input(self, B, num_obs):
        '''
        Transition probabilities will vary depending on the number of observations
        meaning this makes the model not a true Hidden Markov Model, instead
        referred to as an Input Output Model in this case.
        
        Also models rest, the notes are not necessarily connected (no spaces 
        in between.)
        '''
        T = numpy.zeros(shape=(len(B),len(B)))
        ratio = round(32.0 / num_obs) # global probability peak
#        print '\nratio: ',ratio, num_obs
        relative_ratio = ratio/ 32
#        print "relative ratio (of global peak): ", relative_ratio,'\n'
        nogo_counter = 0
        go_counter = 0
        for b in B:
            dist = 31 - b.to
            self.dprint('{0}| b.to ({1}) distance to last note: {2}'.format(b,b.to, dist))
            relative_peak = numpy.ceil(dist*relative_ratio)
            self.dprint('rel_peak: %s'%relative_peak)
#            prob_range2 = range(31, b.to+int(relative_peak)-1,-1)
#            self.dprint("{0} {1}".format(prob_range2, len(prob_range2)))
            prob_range = range(dist-int(relative_peak), -1, -1)
            self.dprint('prob range: {0} (length: {1})'.format(prob_range,
                                                                len(prob_range)))
            for k in B:
                if b.to < k.origin:
                    go_counter +=1
                    diff = k.origin - b.to 
                    #print 'diff', diff, b.to, k.origin
                    if diff < relative_peak:
                        T[b.i][k.i] = 0
                    else:
                        T[b.i][k.i] = prob_range[diff-int(relative_peak)]
                else:
                    nogo_counter +=1
            su = sum(T[b.i])
            # Normalize to 1
            if su != 0:
                T[b.i] = [round(x/su,7) for x in T[b.i]]
#            self.dprint("Prob vector looks like: %s"%T[b.i])
        self.dprint("\n\nNOGOs: %s"%nogo_counter)
        self.dprint("GOs: %s"%go_counter)
        self.dprint("SUM: %s\n"%(nogo_counter+go_counter))
        
#        numpy.set_printoptions(threshold=numpy.nan)
#        print T
        return T
    
    def trans_p_strange(self, B, goalsum=1):
        '''
        Strange distribution
        ===
    
        Starts out (round 1) by assuming equal distribution amongst the transitions
        to receive probabilities, calculates probability based on sum of probabilities 
        being 1. After this round
        it assumes equal distribution between remaining transitions to receive
        probabilities, and calculates probability from 1-`previous probability`. 
        And goes on till final transition probability remains which is given the 
        remainder of what is left of 1. 
    
        Is this anything real mathematical?
        '''
        T = numpy.zeros(shape=(len(B),len(B)))
        for i in range(len(B)):
            r = (range(i,len(B)))
            tot = goalsum
            divisors = len(r)
            div = round(tot/divisors,4)
            for j in r:
                if divisors>1:
                    v = round(abs(random.gauss(div,div/2)),4)
                    T[i][j]= v
                    tot -= v
                    divisors -= 1
                    div = tot/divisors
                else:
                    T[i][j]=round(tot,4)
        return T
        
    def trans_p_gauss(self, B,goalsum=1):
        T = numpy.zeros(shape=(len(B),len(B)))
        for i in range(len(B)):
            for j in range(i,len(B)):
                v = random.gauss(goalsum,goalsum)
                T[i][j]= v
            s = sum(T[i])/goalsum
            T[i] = map(lambda x:x/s, T[i])
        return T
    
    def trans_p_randnorm(self, B, val=1):
        '''
        generated values will have a summed value
        equal/"equal" to param sum
        '''
        T = numpy.zeros(shape=(len(B),len(B)))
        for b in B:
            for k in B:
                if b.to < k.origin:
                    T[b.i][k.i] = round(random.random(),4)
            su = sum(T[b.i])
            if su != 0:
                T[b.i] = [round((val*x)/su,4) for x in T[b.i]]
    
        return T
    
    def generate_e_p_static(self, emission_p, beats):
#        raise RuntimeError('NOT IMPLEMENTED STATIC Emission_P')
        for b in beats:
            if b.origin in [0, 16]:
                # DOWNBEAT
                emission_p[b.i] = {"UNSTRESSED":0.1, "STRESSED": 0.9}
            elif b.origin in [8, 24]:
                # ON-BEATS
                emission_p[b.i] = {"UNSTRESSED":0.25, "STRESSED": 0.75}
            elif b.origin in [4,12,20,28]:
                # OFF-BEATS 
                emission_p[b.i] = {"UNSTRESSED":0.4, "STRESSED": 0.6}
            else:
                emission_p[b.i] = {"UNSTRESSED":0.9, "STRESSED": 0.1}
    
    def generate_e_p_random(self, emission_p, beats):
        for b in beats:
            sh = random.random()
            emission_p[b.i] = {"UNSTRESSED":sh, "STRESSED": 1-sh}
    
#    def generate_d_p(self, d_p, beats):
#        for b in beats:
#            sh = random.random()
#            d_p[b.i] = {"SHORT":sh, "LONG": 1-sh}
    
    def accent_p(self, b, emission):
        return self.emission_probabilities[b.i][emission.accent]
    
#    def duration_p(self, b, emission):
#        return self.d_p[b.i][emission.duration]

    def print_beats(self, x, obs):
        st = ''
        bl = [0 for _ in range(self.num_beats)]
    
        for i in range(len(x)):
            bl[x[i].origin] = obs[i].syllable
        # 16 beat chunks
        bars = self.num_beats/16
    
        for bar in range(bars):
            part=bl[16*bar:16*( bar+1)]
            part.insert(0,"||")
            st += ' '+' '.join([str(lol) for lol in part])
    
        # Print it pretty, sir
        st += " ||"
        st = st.replace("0","x").strip()
        import re
        spaces = re.sub('[^\|\|]', ' ',st)
        topbar = ''.join(['-' for _ in range(len(spaces))])+'\n'+spaces
        botbar = spaces+'\n'+''.join(['-' for _ in range(len(spaces))])
        print topbar+'\n'+st+'\n'+botbar

    @property
    def hidden_states(self):
        return self.B
    
    @property
    def start_probabilities(self):
        return self.start_p
    
    @property
    def transition_probabilities(self):
        return self.T
    
    @property
    def emission_probabilities(self):
        return self.emission_p

    @property
    def emission_function(self):
        return self.accent_p

#    #Number of total 16th note beats 
#    num_beats=32
#    B=[]
#    
#    #Only ring for the beats duration or this till the next designated state
#    for i in range(0,num_beats):
#        for j in range (i,num_beats):
#            B.append(BeatPair(i,j))
#    
#    dprint(B)
#    
#    S = [Syllable("Tom","SHORT","UNSTRESSED"), Syllable("ten","LONG","STRESSED"), Syllable("par","SHORT","UNSTRESSED")]
#    
#    start_p = [1.0/len(B) for _ in B]
#    dprint("\n start p:%s\n"%start_p)
#    
#    T = trans_p_randnorm(B,1)
#    
#    numpy.set_printoptions(suppress=True, precision=5)
#    dprint("T: %s\n"%T)
#    
#    dprint("Sum of T's rows:")
#    if DEBUG:
#        for row in range(0,len(T)):
#            dprint(sum(T[row]))
#    
#    # Before these refered to the accEnt and Duration of the Syllables
#    e_p = range(len(B))
#    generate_e_p(e_p, B)
#    d_p = range (len(B))
#    generate_d_p(d_p, B)
#    
#    dprint("\nProbabilities:")
#    if DEBUG:
#        for b in B:  
#            dprint("{0} \nwith e={1} and d={2}".format(b,e_p[b.i],d_p[b.i],sum(e_p[b.i].values()),sum(d_p[b.i].values())))

