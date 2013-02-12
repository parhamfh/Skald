#!/usr/local/bin/python
# coding: utf8

from ..elements import HmmModelHiddenState, HmmModelObservation

class BeatPair(HmmModelHiddenState):
    '''
    Hidden state.
    '''
    object_counter = 0

    def __init__(self, origin, to, idx=-1):
        self.orig = origin
        self.dest = to
        
        if idx > -1:
            self.i = idx
        else:
            self.i = self._get_index()
            
        
        self.syllable = None

    def _get_index(self):
        BeatPair.object_counter += 1
        return BeatPair.object_counter-1
    
    @staticmethod
    def _reset_object_counter():
        BeatPath.object_counter = 0
    
    @property
    def origin(self):
        return self.orig

    @property
    def to(self):
        return self.dest

    @property
    def duration(self):
        return self.to-self.origin+1

    def add_syllable(self, s):
        self.syllable = s

    def __repr__(self):
        return "{0}{3}({1},{2})".format('B', self.orig, self.dest, self.i)

class BeatPath():
        '''
        A list that represents a path of Beats as calculated by the HMM.
        each entry in the list is a BeatPair. 
        '''
        def __init__(self, list_of_beat_pairs = []):
            self._path = list_of_beat_pairs
        
        def set_list(self, value):
            self.path = value

        @property
        def path(self):
            return self._path

        def __repr__(self):
            return '{0}'.format(self.path)

class BeatPathSet(object):
    '''
    Set that contains BeatPaths as calculated by the HMM.
    Each BeatPath corresponds to one line of text from the user.
    '''

    def __init__(self, number_of_beatpaths):
        self.number_of_bp = number_of_beatpaths
        self._paths = [None] * number_of_beatpaths
    
    def __getitem__(self, key):
        if key < self.number_of_bp and key >= 0:
            if self.paths[key] is None:
                #print '__getitem__: Creating BeatPath object for index %s'%key
                self.paths[key] = BeatPath()
            
            return self.paths[key]
        else:
            #print "BeatPathSet.__getitem__: Index key out of bounds."
            raise IndexError("BeatPathSet.__getitem__: Index key out of bounds.")
    
    def __setitem__(self, key, value):
        if key < self.number_of_bp and key >= 0:
            if self.paths[key] is None:
                #print '__setitem__: Creating BeatPath object for index %s'%key
                self.paths[key] = BeatPath()
            
            self.paths[key].set_list(value)
        else:
            #print "BeatPathSet.__setitem__: Index key out of bounds."
            raise IndexError("BeatPathSet.__setitem__: Index key out of bounds.")

    @property
    def paths(self):
        return self._paths
class Syllable(HmmModelObservation):
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

