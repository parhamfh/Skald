#!/usr/local/bin/python

class BeatPath(object):
        '''
        A list that represents a path of Beats as calculated by the HMM.
        each entry in the list is a BeatPair.
        
        Due to the way BeatPathSet wraps this class and access to it, this
        will never have to be explicitly instantiated for the BeatPathSet.
        '''
        def __init__(self, idx, list_of_beat_pairs = []):
            self._path = list_of_beat_pairs
            self._index = idx 
        
        def set_list(self, value):
            self.path = value

        def __iter__(self):
            return self.path_gen()

        def path_gen(self):
            for i in self.path:
                yield i

        @property
        def i(self):
            return self._index
        
        @property
        def path(self):
            return self._path

        def __repr__(self):
            return 'BeatPath #{0}'.format(self.path)

class BeatPathSet(object):
    '''
    Set that contains BeatPaths as calculated by the HMM.
    Each BeatPath corresponds to one line of text from the user.
    
    Upon calling BeatPathSet[key] (with or without assignment) a 
    BeatPath will be instantiated if it is the first time referencing that key.
    
    If it also is an assignment, the BeatPath's u{set_value} method will be
    called.
    
    Due to the way BeatPathSet wraps BeatPath objects and access to them, the 
    BeatPath object will never have to be explicitly instantiated for the class.
    '''

    def __init__(self, number_of_beatpaths):
        self._number_of_bp = number_of_beatpaths
        self._paths = [None] * number_of_beatpaths
    
    def __getitem__(self, key):
        if key < self.number_of_bp and key >= 0:
            if self.paths[key] is None:
                #print '__getitem__: Creating BeatPath object for index %s'%key
                self.paths[key] = BeatPath(key)
            
            return self.paths[key]
        else:
            #print "BeatPathSet.__getitem__: Index key out of bounds."
            raise IndexError("BeatPathSet.__getitem__: Index key out of bounds.")
    
    def __setitem__(self, key, value):
        if key < self.number_of_bp and key >= 0:
            if self.paths[key] is None:
                #print '__setitem__: Creating BeatPath object for index %s'%key
                self.paths[key] = BeatPath(key)
            
            self.paths[key].set_list(value)
        else:
            #print "BeatPathSet.__setitem__: Index key out of bounds."
            raise IndexError("BeatPathSet.__setitem__: Index key out of bounds.")
    @property
    def number_of_bp(self):
        return self._number_of_bp
    
    @property
    def paths(self):
        return self._paths


if False:
    print '====='
    bps = BeatPathSet(4)
    print bps
    print type(bps[0])
    bps[0] = [2222,3,41,2]
    print '====='
    print bps[0]
    print type(bps[0])
    print isinstance(bps[0],BeatPath)
    print bps[3]
    print bps[3]
    print '====='
    # print bps[667]

    for b in bps:
        print isinstance(b, BeatPath)

    for a in bps[0]:
        print a,a

[
[['REST', 'r4'], ['ACTUAL', 'g4.', 'g16'], ['REST'], ['ACTUAL', 'g4', 'g16'], ['REST'], ['ACTUAL', 'g8'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g8'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST', 'r16'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g8'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST', 'r4.'], ['ACTUAL', 'g8'], ['REST', 'r8'], ['ACTUAL', 'g4'], ['REST', 'r2.', 'r8.'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST', 'r2.'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g8'], ['REST', 'r16'], ['ACTUAL', 'g16'], ['REST', 'r16'], ['ACTUAL', 'g16'], ['REST', 'r2.'], ['ACTUAL', 'g16'], ['REST', 'r2'], ['ACTUAL', 'g8.'], ['REST', 'r16'], ['ACTUAL', 'g8.'], ['REST', 'r1'], ['ACTUAL', 'g16']],
[['REST', 'r4'], ['ACTUAL', 'g4.', 'g16'], ['REST'], ['ACTUAL', 'g4', 'g16'], ['REST'], ['ACTUAL', 'g8'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g8'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST', 'r16'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g8'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST', 'r4.'], ['ACTUAL', 'g8'], ['REST', 'r8'], ['ACTUAL', 'g4'], ['REST', 'r2.', 'r8.'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST', 'r2.'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g8'], ['REST', 'r16'], ['ACTUAL', 'g16'], ['REST', 'r16'], ['ACTUAL', 'g16'], ['REST', 'r2.'], ['ACTUAL', 'g16'], ['REST', 'r2'], ['ACTUAL', 'g8.'], ['REST', 'r16'], ['ACTUAL', 'g8.'], ['REST', 'r1'], ['ACTUAL', 'g16']],
[['REST', 'r4'], ['ACTUAL', 'g4.', 'g16'], ['REST'], ['ACTUAL', 'g4', 'g16'], ['REST'], ['ACTUAL', 'g8'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g8'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST', 'r16'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g8'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST', 'r4.'], ['ACTUAL', 'g8'], ['REST', 'r8'], ['ACTUAL', 'g4'], ['REST', 'r2.', 'r8.'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST', 'r2.'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g8'], ['REST', 'r16'], ['ACTUAL', 'g16'], ['REST', 'r16'], ['ACTUAL', 'g16'], ['REST', 'r2.'], ['ACTUAL', 'g16'], ['REST', 'r2'], ['ACTUAL', 'g8.'], ['REST', 'r16'], ['ACTUAL', 'g8.'], ['REST', 'r1'], ['ACTUAL', 'g16']],
[['REST', 'r4'], ['ACTUAL', 'g4.', 'g16'], ['REST'], ['ACTUAL', 'g4', 'g16'], ['REST'], ['ACTUAL', 'g8'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g8'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST', 'r16'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g8'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST', 'r4.'], ['ACTUAL', 'g8'], ['REST', 'r8'], ['ACTUAL', 'g4'], ['REST', 'r2.', 'r8.'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g16'], ['REST', 'r2.'], ['ACTUAL', 'g16'], ['REST'], ['ACTUAL', 'g8'], ['REST', 'r16'], ['ACTUAL', 'g16'], ['REST', 'r16'], ['ACTUAL', 'g16'], ['REST', 'r2.'], ['ACTUAL', 'g16'], ['REST', 'r2'], ['ACTUAL', 'g8.'], ['REST', 'r16'], ['ACTUAL', 'g8.'], ['REST', 'r1'], ['ACTUAL', 'g16']]
]
