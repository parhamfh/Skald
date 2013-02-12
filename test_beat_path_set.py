#!/usr/local/bin/python

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
            return 'BeatPath: {0}'.format(self.path)

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
                # print '__getitem__: Creating BeatPath object for index %s'%key
                self.paths[key] = BeatPath()
            
            return self.paths[key]
        else:
            # print "BeatPathSet.__getitem__: Index key out of bounds. key=%s"%key
            raise IndexError("BeatPathSet.__getitem__: Index key out of bounds.")
    
    def __setitem__(self, key, value):
        if key < self.number_of_bp and key >= 0:
            if self.paths[key] is None:
                # print '__setitem__: Creating BeatPath object for index %s'%key
                self.paths[key] = BeatPath()
            
            self.paths[key].set_list(value)
        else:
            # print "BeatPathSet.__setitem__: Index key out of bounds. key=%s"%key
            raise IndexError("BeatPathSet.__setitem__: Index key out of bounds.")

    @property
    def paths(self):
        return self._paths


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