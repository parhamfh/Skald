
# Decorator just because Pydev is stupid
import viterbi as vtb

class Hmm(object):
    
    DEBUG=False

    def __init__(self, Model, observations):
        self._model = Model()
        self.observations = observations
    
    @property
    def path(self):
        return self._path
    @property
    def model(self):
        return self._model
        
    def find_most_likely_state_seq(self, use_viterbi = True):
        if use_viterbi:
            self._path = vtb.viterbi_w_model(self.observations, self.model)
            return self._path
        else:
            raise RuntimeError('It has to be Viterbi!')

    def print_path(self):
        try:
            if self.path is None:
                print "No sequence found."
                return
            for x in self.path:
                print x
        except AttributeError:
            print "No path exists. State sequence has not been calculated yet."
        except TypeError, te:
            print "Print what check this out: {0}".format(te)
    
    def dprint(self, s=""):
        if self.DEBUG:
            print "<DEBUG>",s

