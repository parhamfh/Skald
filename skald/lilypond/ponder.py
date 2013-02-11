#!/usr/local/bin/python
# coding: utf8

from os import path
from subprocess import call

from skald.hmm.model.rhythm import BeatPair, Syllable
from skald.util.syllabification import SyllableSet

class Ponder(object):

    FILE_EXTENSION = ".ly"
    STD_G = "g"
    STD_R = "r"
    lyrics = None

    def __init__(self, beats, 
        number_of_bars,
        observations=None, 
        time_signature=(4,4),
        clef='"treble"',        #The quotes are IN the string
        score_name="skald",
        syllables=[]):
        
        if isinstance(observations,SyllableSet):
            print beats
            print number_of_bars
            print observations
            self.beats = [b for bt in beats for b in bt] 
            self.bars = number_of_bars * len(observations)
            self.lyrics = [o for ob in observations for o in ob]
        else:
            self.beats = beats
            self.bars = number_of_bars
            self.lyrics = observations

        self.t_s = "%s/%s"%(time_signature[0],time_signature[1])
        self.clef = clef

        self.subfolder = "score"
        self.select_score_name(score_name)

        print self.pathname

    @property
    def pathname(self):
        return path.join(self.subfolder,self.filename)

    @property
    def filename(self):
        return self.name+self.FILE_EXTENSION

    def select_score_name(self, score_name):
        if self.unused_filename(score_name):
            self.name = score_name
        else:
            self.name = self.increment_score_name(score_name, 1)

    def unused_filename(self, fn):
        # Fancy stackoverflow answer
        # try:
        #     with open(path.join(self.subfolder,fn)) as f: return False
        # except IOError as e:
        #     return True
        if path.isfile(path.join(self.subfolder,fn+self.FILE_EXTENSION)):
            return False
        else:
            return True

    def increment_score_name(self, stem, order):
        '''
        We assume that since it exists it either has a 
        number or not, between the score name and the file
        extension .ly.
        '''

        # Special case: first check: name without number, recurse
        if order == 1:
            return self.increment_score_name(stem, order+1)
        # Does it exist?
        elif self.unused_filename(stem+str(order)):
            return stem+str(order)
        # Try higher number
        else:
            return self.increment_score_name(stem, order+1)

    def make_ly_file(self):
        print "\n====== Ponder: Calculating note values ======\n"
        notes = self.calculate_notes()
        print notes,"\n\n====== Ponder: Generating .ly/.pdf ======\n"
        self.generate_pdf(notes)
        print "\n====== Ponder: Process completed ======\n"

    def calculate_notes(self):
        notes = []
        prev_note_index = 0
        for b in self.beats: 
            print "Note at 16th beat %s is %s long"%(b.origin, b.duration)
            # append rests leading up to this beta
            print "REST:"
            notes.append(["REST"]+self.calculate_rest_notes(prev_note_index, b.origin))
            # append actual marked beat
            prev_note_index = b.origin+b.duration
            print "ACTUAL:"
            notes.append(["ACTUAL"]+self.calculate_actual_notes(b.duration))

        return notes

    def calculate_actual_notes(self, note_duration):
        nd = note_duration
        note_list = []
        for i in [16, 8, 4, 2, 1]:
            output, left = self.fit_notes(nd, i)
            if output is not None:
                note_list.extend(output)
                nd = left

        return note_list

    def fit_notes(self, rest_length, note_length):
        num_notes = rest_length/note_length
        duration = num_notes*note_length
        left = rest_length-duration
        # print "nr of notes that fit: %s"%num_notes
        # print "duration of fitted notes in 16ths: %s"%duration
        # print "notes left that did not fit: %s"%left
        
        if num_notes > 0:
            print note_length, ':', num_notes, duration, left

            # Is it dotted?
            if self.is_dotted(left, note_length):
                print "dotted last note"
                left -= note_length/2
                output_notes = self.format_output_notes(num_notes, note_length, last_is_dotted=True)

            else:
                output_notes = self.format_output_notes(num_notes, note_length)

            return output_notes, left
        else:
            return None, None

    def format_output_notes(self, num_notes, note_length, last_is_dotted=False):
        st = []
        note_value = 16/note_length
        for n in range(num_notes):
            # First note also describes note length
            if n == 0:
                # Is it also last note
                if n == num_notes-1:
                    # Dotted last note?
                    if last_is_dotted:
                        st.append(self.STD_G+str(note_value)+'.')
                    else:
                        st.append(self.STD_G+str(note_value))
                # First note
                else:
                    st.append(self.STD_G+str(note_value)+' ')
            
            # then add right amount of notes until...
            elif n <num_notes-1:
                st.append(self.STD_G+' ')

            # ...last note that might be dotted
            elif last_is_dotted:
                st.append(self.STD_G+'.')
            else:
                st.append(self.STD_G)
        return st

    def calculate_rest_notes(self, start, next_start):
        rl = abs(next_start - start)
        print 'Length of rest before: %s'%rl
        rest_list = []
        
        # Whole, half, quarters, eigths, sixteens
        for i in [16, 8 , 4, 2, 1]:
            #print "\nTrying to fit note of %s length"%i
            output, left = self.fit_rest_notes(rl, i)
            if output is not None:
                rest_list.extend(output)
                rl = left

        return rest_list

    def fit_rest_notes(self, rest_length, note_length):
        num_notes = rest_length/note_length
        duration = num_notes*note_length
        left = rest_length-duration
        # print "nr of notes that fit: %s"%num_notes
        # print "duration of fitted notes in 16ths: %s"%duration
        # print "notes left that did not fit: %s"%left
        
        if num_notes > 0:
            print note_length, ':', num_notes, duration, left
            
            # Is it dotted?
            if self.is_dotted(left, note_length):
                print "dotted last note"
                left -= note_length/2
                output_notes = self.format_rest_notes(num_notes, note_length, last_is_dotted=True)

            else:
                output_notes = self.format_rest_notes(num_notes, note_length)

            return output_notes, left
        else:
            return None, None

    def is_dotted(self, left, note_length):
        
        if left >= note_length/2 and note_length>1:
            return True
        else:
            return False

    def format_rest_notes(self, num_notes, note_length, last_is_dotted=False):
        st = []
        note_value = 16/note_length
        for n in range(num_notes):
            # First note also describes note length
            if n == 0:
                # Is it also last note
                if n == num_notes-1:
                    # Dotted last note?
                    if last_is_dotted:
                        st.append(self.STD_R+str(note_value)+'.')
                    else:
                        st.append(self.STD_R+str(note_value))
                # First note
                else:
                    st.append(self.STD_R+str(note_value)+' ')
            
            # then add right amount of notes until...
            elif n <num_notes-1:
                st.append(self.STD_R+' ')

            # ...last note that might be dotted
            elif last_is_dotted:
                st.append(self.STD_R+'.')
            else:
                st.append(self.STD_R)
        return st

    def generate_pdf(self, output_list):
        output = self.format_string(output_list)
        self.write_to_ly_file(output)
        self.execute_binary()

    def format_string(self, output_list):
        output = "% This .ly-file is generated by Skald.\n"+\
                "\\version \"2.16.1\"\n"+\
                "\\relative c'' {\n"+\
                "\\clef {0}\n".format(self.clef)+\
                "\\time {0}\n".format(self.t_s)
        
        for o in output_list:
            # is not empty
            if len(o) > 1:
                if o[0] == "REST":
                    output += "  {0}\n".format(' '.join(o[1:]))
                elif o[0] == "ACTUAL":
                    output += "  {0}\n".format('~'.join(o[1:]))
                else:
                    raise RuntimeError("What is this?")

        output += "}\n"

        # Are there lyrics too?
        if self.lyrics is not None:
            output += "\\addlyrics {\n  "
            for l in self.lyrics:
                output += "{0} ".format(l.syllable)
            output += "\n}"
        return output

    def write_to_ly_file(self, output):
        output_file = open(self.pathname,"w")
        output_file.write(output)
        output_file.close()

    def execute_binary(self):
        call(["lilypond","-o",self.subfolder,self.pathname])

# When testing Ponder
if __name__ == '__main__':
    
    # REAL EXAMPLES from rhythm32
    # WORKS
    # [B172(5,27), B519(28,29), B526(30,31)]
    # WORKS
    # [B509(26,28), B523(29,30), B527(31,31)]
    # WORKS
    # test = [BeatPair(29,30),BeatPair(31,31)]
    # WORKS
    test = [BeatPair(18,29, 434), BeatPair(30,30,525),BeatPair(31,31,527)]
    # WORKS
    # test = [BeatPair(9,28, 271), BeatPair(29,30,523),BeatPair(31,31,527)]

    S = [Syllable("Tom","SHORT","UNSTRESSED"), Syllable("ten","LONG","STRESSED"), Syllable("par","SHORT","UNSTRESSED")]
    print test
    p = Ponder(test,2, S)
    p.make_ly_file()