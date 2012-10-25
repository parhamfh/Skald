Toy problem (of Rhythm matching for verses)
===========

Definitions
-----------
#Rhythm representation#
A vector r, of length **n** with binary values will represent the rhythm for __n__ notes. 

Ex: n = 6, [0, 0, 1, 1, 0, 1]

This vector represents a MIDI beat sequence. The following rules apply:

* The vector represents note onsets, **not** offsets.
* A *1* means a note onset. 
* if a *1* is followed by one or more *0*s, the *1* sounds for the entire duration of *0*s. Example: [1,0,0] The first note rings for a duration 3 notes.
* Zeroes in the beginning of the vector are _rests_.
* The number of ones is the number of notes/syllables, denoted _s_.

Eg. [0,1,1,0] A vector that has one notes rest, followed by a short note and concluded with a long note.

#Rhythm tree#
The rhythm tree is a set of rhythms that share similar traits in their pattern. A rhythm tree of length **n** contains one rhythm for each length 1,..,n

Input
-----
#Maximum length of verse#
The maximum length of a verse is denotd as the number of syllables, this will be defined as **n**. `0<s<n`

#Constraints (/ verses)#
A set of constraints {C1,C2,...,Cm} of length Cl \in {0,...,n}

The constraints are in vector form and have the values _Rest_, _Long_ or _Short_, but the _Rest_ can only appear in the beginning. Example: [Rest, Rest, Long, Short]

#Rhythm Tree#
A complete set of rhythm vectors as described above, for vector lengths `0,..,n`

The rhythm transition tree describes allowed transitions from a rhythm with _k_ syllbales to either a rhythm with _k-1_ or _k+1_ syllables according to the rules:

* You can transition to a rhythm of shorter length by merging a note in the longer rhythm on the same beat as the one in the shorter. Since music notation is left to right, you can **only merge** from __left to right__.
Ex1: [0, 1, 0, 1] s=2 -> [0, 1, 0, 0] s=1 (last note was merged with first long note)
Ex2: [1, 0, 0, 1] cannot transition to [0, 1, 0, 0] since there is no note on the second beat.
Ex3: [1, 0, 0, 1] cannot transition to [0, 0, 0, 1] since the note on the first beat cannot merge into the second note.
* You can transition to a longer rhythm if you can split a note on the same beat as the longer one. Since music notation is left to right, you can **only split** from __right to left__.
Example: [0, 1, 0, 0] s=1 -> [0, 1, 0, 1] s=1 (splitting the real long note into one long and one short note)
Example: [0, 1, 0, 0] s=1 cannot transition to [1, 0, 0, 1]
Example: [0, 0, 0, 1] cannot transition to [1, 0, 0, 1] since the note available to split is not on the same beat as the first note in the second rhythm.

#Set of probabilities P(r|c)#
Given a constraint/verse of length _l_ and the set of all rhythms with _l_ syllables, _r_ ({r0,..,r2^{l}} it is less than 2^l but i forgot what the formula is??), P(r|c) is the probability that the rhythm matches that constraint/verse well.

#Set of probabilities P_{T}(r1,...,rm)#
Given a rhythm tree, _T_ with the rhythms r1,...rm, P_{T}(r1,...,rm) is the likelihood of seeing that rhythm tree in real life.

Output
------
Given the input return the valid rhythm tree, T, of length **n** with the highest probability P_{T}.


