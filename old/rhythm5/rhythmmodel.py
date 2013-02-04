#!/usr/local/bin/python

import viterbi, numpy
import random as ra
from itertools import izip_longest

from sounder import Sounder

class BeatPair(object):
    '''
    Hidden state.
    '''
    def __init__(self, origin, to, idx):
        self.orig = origin
        self.dest = to
        self.i = idx

    @property
    def origin(self):
        return self.orig

    @property
    def to(self):
        return self.dest

    @property
    def duration(self):
        return self.to-self.origin+1

    def __repr__(self):
        return "{0}{3}({1},{2})".format('B', self.orig, self.dest, self.i)

class Syllable(object):
    '''
    Output/emission.
    '''

    def __init__(self, syllable, duration, accent):
        self.s = syllable
        self.d = duration
        self.e = accent

    @property
    def syllable(self):
        return self.s
    
    @property
    def duration(self):
        return self.d

    @property
    def accent(self):
        return self.e

    @property
    def stress(self):
        raise RuntimeError("It is called ACCENT../")

    def __repr__(self):
        return "(\"{0}\",{1},{2})".format(self.s, self.d, self.e)

DEBUG=True

def dprint(s=""):
    if DEBUG:
        print "<DEBUG>",s

def trans_p_strange(B, goalsum=1):
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
                v = round(abs(ra.gauss(div,div/2)),4)
                T[i][j]= v
                tot -= v
                divisors -= 1
                div = tot/divisors
            else:
                T[i][j]=round(tot,4)
    return T
    
def trans_p_gauss(B,goalsum=1):
    T = numpy.zeros(shape=(len(B),len(B)))
    for i in range(len(B)):
        for j in range(i,len(B)):
            v = ra.gauss(goalsum,goalsum)
            T[i][j]= v
        s = sum(T[i])/goalsum
        T[i] = map(lambda x:x/s, T[i])
    return T

def trans_p_randnorm(B,val=1):
    '''
    generated values will have a summed value
    equal/"equal" to param sum
    '''
    T = numpy.zeros(shape=(len(B),len(B)))
    for b in B:
        for k in B:
            if b.to < k.origin:
                T[b.i][k.i] = round(ra.random(),4)
        su = sum(T[b.i])
        if su != 0:
            T[b.i] = [round((val*x)/su,4) for x in T[b.i]]

    return T

def generate_e_p(e_p, beats):
    for b in beats:
        sh = ra.random()
        e_p[b.i] = {"UNSTRESSED":sh, "STRESSED": 1-sh}

def generate_d_p(d_p, beats):
    for b in beats:
        sh = ra.random()
        d_p[b.i] = {"SHORT":sh, "LONG": 1-sh}

def accent_p(b, emission):
    return e_p[b.i][emission.accent]

def duration_p(b, emission):
    return d_p[b.i][emission.duration]


## PLAY BALL ##

num_beats=5
B=[]

#Only ring for the beats duration or this till the next designated state
idx = 0
for i in range(0,num_beats):
    for j in range (i,num_beats):
        B.append(BeatPair(i,j,idx))
        idx += 1

print B

S = [Syllable("Tom","SHORT","UNSTRESSED"), Syllable("ten","LONG","STRESSED")]

start_p = [1.0/len(B) for _ in B]
dprint("\n start p:%s\n"%start_p)

T = trans_p_randnorm(B,1)

numpy.set_printoptions(suppress=True, precision=5)
dprint("T: %s\n"%T)

dprint("Sum of T's rows:")
if DEBUG:
    for row in range(0,len(T)):
        dprint(sum(T[row]))

# LOOK HERE
e_p = range(len(B))
generate_e_p(e_p, B)
d_p = range (len(B))
generate_d_p(d_p, B)

dprint("\nProbabilities:")
if DEBUG:
    for b in B:  
        dprint("{0} \nwith e={1} and d={2}".format(b,e_p[b.i],d_p[b.i],sum(e_p[b.i].values()),sum(d_p[b.i].values())))


# print "\nSafety check:"
# print accent_p(B[7],S[1])
# print duration_p(B[7],S[0])

# Two emission functions
# xpath = viterbi.viterbi(S,B,T,start_p,accent_p,duration_p)
# One emission function
xpath = viterbi.viterbi(S,B,T,start_p, accent_p)

print "\nAnd they said, in great unison, that The Path shalt be:"

sounder = Sounder(5)
sendlist = [(-1,1,b) for b in range(0,5)]
for x in xpath:
    print x
    # print "Hidden state, transition values ",T[x.i]
    sendlist[x.origin] = (ra.randint(60,80),x.duration,x.origin)

print sendlist
sounder.set_notes(sendlist)
sounder.send_notes()
sounder.close()

