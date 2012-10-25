Toy problem (of Rhythm matching for verses)
===========

Input
-----
A vector of length **n** with binary values will be given. 

Ex: n = 6, [0, 0, 1, 1, 0, 1]

This vector represents a MIDI note sequence. The following rules apply:

* The vector represents vector onsets, **not** offsets.
* A *1* means a note onset. 
* if a *1* is followed by one or more *0*s, the *1* sounds for the entire duration of *0*s. Example: [1,0,0] The first note rings for a duration 3 notes.
* Zeroes in the beginning of the vector are _rests_.

Eg. [0,1,1,0] A vector that has one notes rest, followed by a short note and concluded with a long note.