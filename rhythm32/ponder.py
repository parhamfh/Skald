#!/usr/local/bin/python
# coding: utf8

from os import path

from skaldmodel import BeatPair

class Ponder(object):

    FILE_EXTENSION = ".ly"
    STD_G = "g"

    def __init__(self, beats, 
        number_of_bars, 
        time_signature=(4,4),
        clef='treble',
        score_name="skald"):
        self.beats = beats
        self.bars = number_of_bars
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

    def generate_ly_file(self):
        notes = self.calculate_notes()

    def calculate_notes(self):
        notes = []
        prev_note_index = 0
        for b in self.beats: 
            print "Note at 16th beat %s is %s long"%(b.origin, b.duration)
            # append rests leading up to this beta
            notes.append(self.calculate_rest_note(prev_note_index, b.origin))
            # append actual marked beat
            prev_note_index = b.origin+b.duration

    def calculate_rest_note(self, start, next_start):
        length = abs(next_start - start)
        print 'Length of rest before: %s'%length
        durations = self.get_duration(length)
    
    def get_duration(self, length):

        # How many whole
        note_length = 16
        num_notes = length/note_length
        duration = num_notes*note_length
        left = length-duration
        print "nr of notes: %s"%num_notes
        print "length in 16th: %s"%duration
        print "notes left: %s"%left
        
        #is dotted?
        if self.is_dotted(left, note_length):
            left -= note_length/2
            output_notes = self.format_output_notes(num_notes, note_length, last_is_dotted=True)
        else:
            output_notes = self.format_output_notes(num_notes, note_length)

        print output_notes
        # How many halves

        # How many quarters

        # How many eights

        # How many 16ths?

        print
    def is_dotted(self, left, note_length):
        print left, note_length/2 
        if left >= note_length/2:
            print "TRUE JU"
            return True
        else:
            return False

    def format_output_notes(self, num_notes, note_length, last_is_dotted=False):
        st = ""
        for n in range(num_notes):
            if n == 0:
                st += self.STD_G+str(note_length)+' '
            elif n <num_notes-1:
                st += self.STD_G+' '
            elif last_is_dotted:
                st += self.STD_G+'.'
            else:
                st += self.STD_G
        return st

    def generate_pdf(self):
        pass

    def format_string(self):
        pass
    
    def execute_binary(self):
        pass

# When testing Ponder
if __name__ == '__main__':
    test = [BeatPair(29,30),BeatPair(31,31)]
    print test
    p = Ponder(test,2)
    p.generate_ly_file()