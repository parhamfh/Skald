#!/usr/local/bin/python
# coding: utf8

import numpy
import random

from skald.hmm.model import HmmModel
from skald.hmm.model.rhythm.elements import BeatPair, Syllable

class RhythmModel(HmmModel):
    
    def __init__(self, num_beats, debug):
        super(RhythmModel,self).__init__(debug)
        
        self.num_beats = num_beats
        

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
    
    def trans_p_randnorm(self, B,val=1):
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
    
    def generate_e_p(self, e_p, beats):
        for b in beats:
            sh = random.random()
            e_p[b.i] = {"UNSTRESSED":sh, "STRESSED": 1-sh}
    
    def generate_d_p(self, d_p, beats):
        for b in beats:
            sh = random.random()
            d_p[b.i] = {"SHORT":sh, "LONG": 1-sh}
    
    def accent_p(self, b, emission):
        return self.e_p[b.i][emission.accent]
    
    def duration_p(self, b, emission):
        return self.d_p[b.i][emission.duration]
    
    
    def print_beats(self, x,obs):
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
    
#    
#    
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
#    # LOOK HERE
#    e_p = range(len(B))
#    generate_e_p(e_p, B)
#    d_p = range (len(B))
#    generate_d_p(d_p, B)
#    
#    dprint("\nProbabilities:")
#    if DEBUG:
#        for b in B:  
#            dprint("{0} \nwith e={1} and d={2}".format(b,e_p[b.i],d_p[b.i],sum(e_p[b.i].values()),sum(d_p[b.i].values())))
