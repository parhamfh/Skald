

class BeatPair(object):
    '''
    Hidden state.
    '''
    object_counter = 0

    def __init__(self, origin, to, idx=-1):
        self.orig = origin
        self.dest = to
        if idx == -1:
            self.i = self._get_index()
        else:
            self.i = idx
        self.syllable = None

    def _get_index(self):
        BeatPair.object_counter += 1
        return BeatPair.object_counter-1
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
