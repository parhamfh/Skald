Toy problem (of Rhythm matching for verses)
===========

Definitions
-----------
###Rhythm representation###
A vector r, of length **n** with binary values will represent the rhythm for __n__ _beats_ (the number of notes vary). 

Ex: n = 6, [0, 0, 1, 1, 0, 1]

This vector represents a (MIDI) note sequence of 6 beats with 3 notes. 

The following rules apply:

* The vector represents note onsets, **not** offsets.
* A *1* symbolizes a note **onset**. 
* if a *1* is followed by one or more _0_, the *1* sounds for the entire duration of zeroes. Example: [1, 0, 0] The first note rings for a duration 3 notes.
* Zeroes in the **beginning** of the vector are _rests_.
* The number of _1_ is the number of notes/syllables, denoted _s_.

Eg. [0,1,1,0] A vector that has one notes rest, followed by a short note and concluded with a long note.

###Rhythm tree###
The rhythm tree is a set of rhythms that share similar traits in their pattern. A rhythm tree of length **n** contains one rhythm for each length `1,..,n`

Input
-----
###Maximum length of verse###
The maximum length of a verse is denoted as the number of beats, this will be defined as **n**. `0<s<n`

###Constraints (/ verses)###
A set of constraints {C1,C2,...,Cm} each with a number of syllables in `{1,...,n}`

The constraints are in vector form and have the values _Rest_, _Long_ or _Short_, but the _Rest_ can only appear in the beginning. Example: [Rest, Rest, Long, Short]

But this excludes constraints that have `n` number syllables but total length is longer than `n` due to long notes. 
But it is my task to generate constraints that do not exceed the maximum length.

###Rhythm set###
A complete set of all rhythm vectors (as described above) of length `n` (and number of syllables between `1,..,n`)

###Rhythm transition map###
The rhythm transition map describes allowed transitions from a rhythm with _k_ syllables to either a rhythm with _k-1_ or _k+1_ syllables according to the rules:

* You can transition to a rhythm of shorter length by merging a note in the longer rhythm on the same beat as the one in the shorter. Since music notation reads left to right, you can **only merge** from __right to left__.
    * Ex1: [0, 1, 0, 1] s=2 -> [0, 1, 0, 0] s=1 (last note was merged with first long note)
    * Ex2: [1, 0, 0, 1] cannot transition to [0, 1, 0, 0] since there is no note on the second beat.
    * Ex3: [1, 0, 0, 1] cannot transition to [0, 0, 0, 1] since the note on the first beat cannot merge into the second note.
* You can transition to a longer rhythm if you can split a note on the same beat as the longer one. Since music notation reads left to right, you can **only split** from __left to right__.
    * Example: [0, 1, 0, 0] s=1 -> [0, 1, 0, 1] s=1 (splitting the real long note into one long and one short note)
    * Example: [0, 1, 0, 0] s=1 cannot transition to [1, 0, 0, 1]
    * Example: [0, 0, 0, 1] cannot transition to [1, 0, 0, 1] since the note available to split is not on the same beat as the first note in the second rhythm.

Output
------

Given the input return the valid rhythm tree, T, of length **n** with the highest probability P(c1,c2,c3,c4,T) where the rhythms are based on the set of constraints. In other words find the T that maximizes the probability P(c1,c2,c3,c4,T). (we are choosing only 4 constraints/verses for this example)

Task
----
T* = argmax P(c1,c2,c3,c4,T)

can be written as

T* = argmax P(c1,c2,c3,c4,T) = P(c1,c2,c3,c4|T)P(T)

Under the assumption that the constraints are independent of each other (an assumption that might not be true in later cases, specially considering lyric and poetry meter. E.g Haiku), this can be written as this:

P(c1,c2,c3,c4|T)P(T) = P(c1|T) * P(c2|T) * P(c3|T) * P(c4|T) * P(T)

what we do know though is that each constraint/verse only depends on the rhythm with the same number of beats and syllables. So if we let the cardinality of a constraint, |c|, denote the number of syllables and r^(x) as the rhythm for _x_ beats we can rephrase the probability as

P(c1,c2,c3,c4,T) = P(c1|r^(|c1|)) * P(c2|r^(|c2|)) * P(c3|r^(|c3|)) * P(c4|r^(|c4|)) * P(T)

P(T) can also be rewritten as 

P(T) = p(r^(0))*SeqProd{l=1, 32}(P(r^(l)|r^(l-1))) 
since each rhythm in the tree depends on the one previous to it! (Ask Fukayama to clarify... since you don't quite get this part).

The final form of the probability can therefor be written as

= SeqProd{n=1,4}( P(cn | r^(n)) ) * P(r^(0))*SeqProd{l=1, 32}( P(r^(l) | r^(l-1)) )

= fp * ft

this is the score/cost function which we wish to maximize is

S = fp * ft

argmax(T \in Tspace) S(c1,c2,c3,c4,T) 

Data to generate
----------------
###Set of probabilities P(c|r)###
These need to be generated and preferably in a way that denotes how well they match. perhaps use a deterministic heuristic to check similarity and then award a probability?

###Set of probabilities P(r^k|r^k-1)###
Due to the nature of ft these need to be evaluated "a priori". Here we must adhere to the rules of the transition map and try to award probabilities to the best of our abilities. Of course this could be a binary function but we want to allow maybe some exceptions to allow
for more interesting choices. Also, it might be help avoiding sinks, and some situations or strange sentences
might force our hand to allow a rhythm tree that is not so much a rhythm tree. Oh well.

Contact
-------
Parham in real life<parhamfh>



