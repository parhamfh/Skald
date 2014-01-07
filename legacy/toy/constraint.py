import sys

class Constraint(object):
    LONG="l"
    SHOT="s"
    REST="r"
    RING="g"

    def __init__(self, sequence):
        (beats, syllables) = self._verify(sequence)

        if beats >= 0:
            self.sequence = sequence
            self.syllables = syllables
            self.beats = beats
        else:
            raise RuntimeError("Invalid sequence")

    def _verify(self, seq):
        no_rest = False
        ringing = False
        syllables = 0
        beat = 0
        
        for c in seq:
            if beat == 32:
                raise RuntimeError("Sequence too long. Maximum length 32 beats.\nchar='%s' b=%s s=%s"%(c,beat,syllables))
            
            if c == 'r':
                if no_rest:
                    raise RuntimeError("Rests are only allowed in the beginning of the sequence.\nchar='%s' b=%s s=%s"%(c,beat,syllables))
            
            elif c == 'l':
                if not no_rest:
                    no_rest = True

                syllables += 1
                if not ringing:
                    ringing = True
            
            elif c == 's':
                if not no_rest:
                    no_rest = True
                if ringing:
                    ringing = False

                syllables += 1

            elif c == 'g':
                if not ringing:
                    raise RuntimeError("RINGING marker with no previous LONG note marker.\nchar='%s' b=%s s=%s"%(c,beat,syllables))
            else:
                beat = -1
                break
            beat += 1

        return (beat, syllables)
        
    def __str__(self):
        return "Constraint(sequence={0}, beats={1}, syllables={2}".format(self.sequence,
                                                                   self.beats, 
                                                                   self.syllables)

def main():
    print 'halleliuja'
    first = True
    c = []
    for a in sys.argv:
        if first:
            first = False
            continue
        c.append(a)

    con = Constraint(c)
    print con
if __name__=='__main__':
    main()

