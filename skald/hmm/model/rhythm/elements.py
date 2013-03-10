#!/usr/local/bin/python
# coding: utf8

from ..elements import HmmModelHiddenState, HmmModelObservation

class BeatPair(HmmModelHiddenState):
    '''
    Hidden state.
    '''
    object_counter = 0

    def __init__(self, origin, to, note_value = None, idx=-1):
        self.orig = origin
        self.dest = to
        self._note_value = note_value

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
        BeatPair.object_counter = 0
    
    @property
    def origin(self):
        return self.orig

    @property
    def to(self):
        return self.dest

    @property
    def duration(self):
        return self.to-self.origin+1

    @property
    def note_value(self):
        return self._note_value
    
    def add_syllable(self, s):
        self.syllable = s

    def __repr__(self):
        return "{0}{3}({1},{2})".format('B', self.orig, self.dest, self.i)

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
        
        def __len__(self):
            return len(self.path)
            
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

        @path.setter
        def path(self,value):
            self._path = value

        def __repr__(self):
            return 'BeatPath#{1} => {0}'.format(self.path, self.i)

class BeatPathSet(object):
    '''
    Set that contains BeatPaths as calculated by the HMM.
    Each BeatPath corresponds to one line of text from the user.
    
    Upon calling BeatPathSet[key] (with or without assignment) a 
    BeatPath will be instantiated if it is the first time referencing that key.
    
    If it also is an assignment, the BeatPath's u{set_list} method will be
    called.
    
    Due to the way BeatPathSet wraps BeatPath objects and access to them, the 
    BeatPath object will never have to be explicitly instantiated for the class.
    '''

    def __init__(self, number_of_beatpaths, paths = None):
        self._number_of_bp = number_of_beatpaths
        if paths is None:
            self._paths = [None] * number_of_beatpaths
        else:
            self._paths = paths
    
    def __getitem__(self, key):
        if type(key) == slice:
            return self.paths[key]
        elif key < self.number_of_bp and key >= 0:
            if self.paths[key] is None:
                #print '__getitem__: Creating BeatPath object for index %s'%key
                self.paths[key] = BeatPath(key)
            
            return self.paths[key]
        else:
            #print "BeatPathSet.__getitem__: Index key out of bounds."
            raise IndexError("BeatPathSet.__getitem__: Index key out of bounds. key={0}, self.number_of_bp={1}".format(key,self.number_of_bp))
    
    def __setitem__(self, key, value):
        if key < self.number_of_bp and key >= 0:
            if self.paths[key] is None:
                #print '__setitem__: Creating BeatPath object for index %s'%key
                self.paths[key] = BeatPath(key)
            
            self.paths[key].set_list(value)
        else:
            #print "BeatPathSet.__setitem__: Index key out of bounds."
            raise IndexError("BeatPathSet.__setitem__: Index key out of bounds.")
    
    def __len__(self):
        return len(self.paths)

    @property
    def number_of_bp(self):
        return self._number_of_bp
    
    @property
    def paths(self):
        return self._paths
    
    def __repr__(self):
        # should be "unambigious"
        # If paths is a container (which it is) the conataining items'
        # __repr__ method will be called instead of __str__
        return '{0}'.format(self.paths)
        
    def __str__(self):
        # should be "readable"
        return "BeatPathSet: {0}".format(self.__repr__())

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

