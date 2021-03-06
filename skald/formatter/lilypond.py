#!/usr/local/bin/python
# coding: utf8

from os import path, makedirs

from subprocess import call

from skald.hmm.model.rhythm.elements import BeatPair, Syllable, BeatPathSet, BeatPath
from skald.util.syllabify import SyllableSet

class LilypondFormatter(object):

    FILENAME_EXTENSION = ".ly"
    STD_G = "g"
    STD_R = "r"
    BARLINE = "|"
    BARLINE_WITH_REST = "~ |"
    lyrics = None

    class LilypondStaff(object):
        
        def __init__(self, notes):
            self.notes = notes
            
        def __repr__(self):
            return self.notes
        
        
    def __init__(self, beat_path_set, 
#        number_of_bars,
        observations, 
        time_signature=(4,4),
        clef='"treble"',        #The quotes are IN the string
        score_name="skald",
        syllables=[]):
        
        if isinstance(beat_path_set, BeatPathSet) and isinstance(observations,SyllableSet):
            print "=== BeatPairSet & SyllableSet received"\
                    " by Lilypond Score generator ==="
            for b in beat_path_set:
                assert isinstance(b, BeatPath)
#            print beats
##            print number_of_bars
#            print observations
#            self.beats = [b for bt in beats for b in bt] 
##            self.bars = number_of_bars * len(observations)
#            self.lyrics = [o for ob in observations for o in ob]
        else:
            raise RuntimeError('Received input of invalid type. beats = {0}'\
                               ' and observations = {1}'.format(
                                            type(beat_path_set), type(observations)))
        self.beat_path_set = beat_path_set
#            self.bars = number_of_bars
        self.lyrics = observations

        self.t_s = "%s/%s"%(time_signature[0],time_signature[1])
        self.clef = clef

        self.default_subfolder_stem = "output"
        self.subfolder = "lilypond"
        self.select_score_name(score_name)

#        print self.pathname

    @property
    def pathname(self):
        return path.join(self.default_subfolder_stem,
                         self.subfolder,self.filename)

    @property
    def folder_path(self):
        return path.join(self.default_subfolder_stem,
                         self.subfolder)
    @property
    def filename(self):
        return self.name+self.FILENAME_EXTENSION

    def ensure_path_exists(self, directory):
        if not path.exists(directory):
            makedirs(directory)

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
        if path.isfile(path.join(self.folder_path,fn+self.FILENAME_EXTENSION)):
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
    
    def format_note_string(self, note):
        '''
        escapes tildes (~) around bar sign (|)
        '''
        if '|' not in note:
            # Handles note variable with both single and multiple values.
            return '~'.join(note)
        else:
            # Assume it is bigger than one note and contains bar sign
            note_str = note[0]
            skip_next_tilde = False
            
            self.reformat_middle_bars(note)
            for n in note[1:]:
                if n == "|" or n == "~ |":
                    note_str+=" {0}\n".format(n)
                    skip_next_tilde = True
                elif skip_next_tilde:
                    # This clause is true when the barline is the first
                    # element and the preceeding note must not tie to
                    # preceeding note list
                    note_str+="  {0}".format(n)
                    skip_next_tilde = False
                else:
                    note_str+="~{0}".format(n)
            return note_str
    
    def reformat_middle_bars(self, note):
        '''
        We want to tie notes across the barline that occurs
        in the middle of a note list. We don't want to
        do this for barlines that occur as the first or last
        element in the note list since that would wrongfully tie
        the notes together with notes from other note lists (i.e from 
        other syllables' note list)
        '''
        i = 0
        while i<len(note):
            if not i == 0 and not i == len(note)-1:
                if note[i] == '|':
                    note[i] = '~ |'
            i += 1
    def format_rest_string(self, note):
        '''
        formats around bar sign (|)
        '''
        if '|' not in note:
            # Handles note variable with both single and multiple values.
            return ' '.join(note)
        else:
            # Assume it is bigger than one note and contains bar sign
            note_str = note[0]
            for n in note[1:]:
                post_bar_extra_space = True
                if n == "|":
                    note_str+=" {0}\n".format(n)
                    post_bar_extra_space = True
                else:
                    if post_bar_extra_space:
                        note_str += ' '
                        post_bar_extra_space = False
                    note_str+=" {0}".format(n)
            return note_str

    def format_string(self, output_note_lists):
        output = "% This .ly-file is generated by Skald.\n"+\
                "\\version \"2.16.1\"\n\n"

        staff_header = "\\relative c'' {\n"+\
                "\\clef {0}\n".format(self.clef)+\
                "\\time {0}\n".format(self.t_s)
        lyrics_i = 0
        for note_list in output_note_lists:
            note_staff = ""
            note_staff += staff_header
            for o in note_list:
                # is not empty
                if len(o) > 1:
                    if o[0] == "REST":
                        note_staff += "  {0}".format(self.format_rest_string(o[1:]))
                    elif o[0] == "ACTUAL":
                        note_staff += "  {0}".format(self.format_note_string(o[1:]))
                    else:
                        raise RuntimeError("What is this?")
            
            #TODO: ugly to use variable meant for other thing. rename
            if lyrics_i == len(output_note_lists)-1:
                note_staff += ' \\bar "|." \n}\n'
            else:
                note_staff += " |\n}\n"
            
            output +=note_staff
            #Are there lyrics too?
            if self.lyrics is not None:
                output += "\\addlyrics {\n  "
                for l in self.lyrics[lyrics_i]:
                    output += "{0} ".format(l.syllable.encode(encoding='utf8'))
                output += "\n}\n\n"
                lyrics_i+=1
        return output
    
    def write_to_ly_file(self, output):
        with open(self.pathname,"w") as output_file: 
            output_file.write(output)


    def execute_binary(self):
        # for checking if lilypond is in path
        #import os
        #print os.environ['PATH']
        print ["lilypond","-o",self.folder_path,self.pathname]
        call(["lilypond","-o",self.folder_path,self.pathname])
    
    def generate_pdf(self, output_note_list):
        output = self.format_string(output_note_list)
        self.ensure_path_exists(self.folder_path)
        self.write_to_ly_file(output)
        self.execute_binary()
    
    def make_ly_file(self):
        print "\n====== LilypondFormatter: Calculating note values ======\n"
        note_lists = self.calculate_notes()
        print "====== LilypondFormatter: Generating .ly/.pdf ======"
        self.generate_pdf(note_lists)
        print "\n====== LilypondFormatter: Process completed ======\n"

    def note_across_bar(self,start_index,end_index, bar_tuples):
        '''
        Check if a range representing a duration of notes (rest or actual)
        crosses over bar lines. 
        
        The bars are represented as a tuple with the index of the preceeding
        and following index. If both are present in the range, that means that
        the rest or note will cross the bar line. 
        '''
        bar_index = bar_tuples
        index_before_bar = [b for (a,b) in bar_index if a and b in range(start_index,end_index)] 
        if index_before_bar != []: 
            return True, index_before_bar
        else:
            return False, -1

    def calculate_notes(self):
        note_lists = [[] for _ in range(self.beat_path_set.number_of_bp)]
        for bp in self.beat_path_set:
            prev_note_index=0
            barlines = [(15,16)]
            for b in bp:  
                #print "Note at 16th beat %s is %s long"%(b.origin, b.duration)
        
                # Append rests leading up to this beat
                rnote = self.calculate_preceeding_rest_notes(prev_note_index, b.origin, barlines)
                #print "REST PRECEEDING: %s"%rnote
                note_lists[bp.i].append(["REST"]+rnote)
                
                # Append actual marked beat
                prev_note_index = b.origin+b.duration
                

                anote=self.calculate_actual_notes(b.duration, b.origin, barlines)
                #print "ACTUAL FOLLOWING: %s"%anote
                note_lists[bp.i].append(["ACTUAL"]+anote)
                
                
            #print "NOTE LIST DONE === %s\n"%note_lists[bp.i]

            
        return note_lists

    def calculate_actual_notes(self, note_duration, note_start, barlines):
        nd = note_duration
        note_list = []
        # CHECK IF REST GOES OVER BAR LINES
        is_across, next_bar_indexes = self.note_across_bar(note_start, note_start+note_duration+1, barlines)
        
        if is_across:
#            print note_start, note_start+note_duration
#            print is_across, next_bar_indexes
            # if we cross bar boundaries...
            s = note_start
            for i in next_bar_indexes:
                if i == note_start:
                    # if the note starts on the same note as the bar "ends"
                    # assume that preceeding rest adds bar.
                    # Addendum 26 march: Don't I mean "if it starts on
                    # the first note of the next bar"? Since if next_bar_indexes
                    # contains [16], which it usually does, 16 represents
                    # the first note of the second bar...
                    continue
                #for each bar fill out with rests
                note_list.extend(self.fill_duration_with_notes(i-s))
                nd -= (i-s)
                s = i+1
                note_list.append("|")
                barlines.remove((i-1,i))
        
        # Big notes -> Smaller notes. Whole -> 16th
        for i in [16, 8, 4, 2, 1]:
            output, left = self.fit_notes(nd, i)
            if output is not None:
                note_list.extend(output)
                nd = left

        return note_list
    

    def fill_duration_with_notes(self, duration):
        return_list = []
        # Whole, half, quarters, eigths, sixteens
        for i in [16, 8 , 4, 2, 1]:
#            print "\nTrying to fit note of %s length"%i
            output, left = self.fit_notes(duration, i)
            if output is not None:
                return_list.extend(output)
                duration = left
        return return_list
    
    def fit_notes(self, rest_length, note_length):
        num_notes = rest_length/note_length
        duration = num_notes*note_length
        left = rest_length-duration
        
        if num_notes > 0:
#            print "nr of notes that fit: %s"%num_notes
#            print "duration of fitted notes in 16ths: %s"%duration
#            print "notes left that did not fit: %s"%left
#            print note_length, ':', num_notes, duration, left

            # Is it dotted?
            if self.is_dotted(left, note_length):
                #print "dotted last note"
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
            
            # then add right amount of notes until... (observe that it is < not <=)
            elif n <num_notes-1:
                st.append(self.STD_G+' ')

            # ...last note that might be dotted
            elif last_is_dotted:
                st.append(self.STD_G+'.')
            else:
                st.append(self.STD_G)
                raise RuntimeError()
        return st

    def calculate_preceeding_rest_notes(self, start, next_start, barlines):

        rest_length = abs(next_start - start)
        rest_list = []

#        print 'Length of rest before: %s'%rl

        # CHECK IF REST GOES OVER BAR LINES
        is_across, next_bar_indexes = self.note_across_bar(start, next_start, barlines)
        if is_across:
            # if we cross bar boundaries...
            s = start
            for i in next_bar_indexes:
                #for each bar fill out with rests
                rest_list.extend(self.fill_duration_with_rest_notes(i-s))
                rest_length -= (i-s)
                s = i+1
                rest_list.append("|")
                barlines.remove((i-1,i))
        
        rest_list.extend(self.fill_duration_with_rest_notes(rest_length))
        
        # TODO: TIRED
        # Shouldn't be needed? Looks at note_across_bar in calculate_actual_note
        # there it calculated, and puts bar in the end.. why___??? tired ><
        
        # Does the actual note begin after the barline?
        if [a for a in barlines if next_start == a[1]] != []:
            # If so. add a barline
            rest_list.append('|')
        return rest_list
    
    def fill_duration_with_rest_notes(self, duration):
        return_list = []
        # Whole, half, quarters, eigths, sixteens
        for i in [16, 8 , 4, 2, 1]:
            #print "\nTrying to fit note of %s length"%i
            output, left = self.fit_rest_notes(duration, i)
            if output is not None:
                return_list.extend(output)
                duration = left
        return return_list
    
    def fit_rest_notes(self, rest_length, note_length):
        num_notes = rest_length/note_length
        duration = num_notes*note_length
        left = rest_length-duration
        
        if num_notes > 0:
#            print "nr of notes that fit: %s"%num_notes
#            print "duration of fitted notes in 16ths: %s"%duration
#            print "notes left that did not fit: %s"%left
#            print note_length, ':', num_notes, duration, left
            
            # Is it dotted?
            if self.is_dotted(left, note_length):
#                print "dotted last note"
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


# When testing LilypondFormatter
if __name__ == '__main__':
    '''
    
    THIS IS FOR TESTING JUST THE LILYPOND FORMATTER
    
    '''
    # REAL EXAMPLES from rhythm32
    # WORKS
    # [B172(5,27), B519(28,29), B526(30,31)]
    # WORKS
    # [B509(26,28), B523(29,30), B527(31,31)]
    # WORKS
    # test = [BeatPair(29,30),BeatPair(31,31)]
    # WORKS
#    test = [BeatPair(18,29, 434), BeatPair(30,30,525),BeatPair(31,31,527)]
    # WORKS
    # test = [BeatPair(9,28, 271), BeatPair(29,30,523),BeatPair(31,31,527)]

#    S = [Syllable("Tom","SHORT","UNSTRESSED"), Syllable("ten","LONG","STRESSED"), Syllable("par","SHORT","UNSTRESSED")]
#    print test
#    p = LilypondFormatter(test,2, S)
#    p.make_ly_file()
    obs = SyllableSet()
    obs.append([Syllable('Vo','SHORT','UNSTRESSED'),
                Syllable('re','SHORT','UNSTRESSED'),
                
                Syllable('mig','SHORT','UNSTRESSED'),
                
                Syllable('det','SHORT','UNSTRESSED'),
                
                Syllable('för','SHORT','UNSTRESSED'),
                Syllable('un','SHORT','UNSTRESSED'),
                Syllable('nat','SHORT','UNSTRESSED'),
                Syllable('att','SHORT','UNSTRESSED'),
                
                Syllable('hög','SHORT','UNSTRESSED'),
                Syllable('tids','SHORT','UNSTRESSED'),
                Syllable('stolt','SHORT','UNSTRESSED'),
                
                Syllable('som','SHORT','UNSTRESSED'),
                
                Syllable('des','SHORT','UNSTRESSED'),
                Syllable('sa','SHORT','UNSTRESSED')])
    
    obs.append([Syllable('kun','SHORT','UNSTRESSED'),
                Syllable('na','SHORT','UNSTRESSED'),
                
                Syllable('lyft','SHORT','UNSTRESSED'),
                Syllable('a','SHORT','UNSTRESSED'),
                
                Syllable('mig','SHORT','UNSTRESSED'),
                
                Syllable('upp,','SHORT','UNSTRESSED'),
                
                Syllable('dit','SHORT','UNSTRESSED'),
                
                Syllable('ej','SHORT','UNSTRESSED'),
                
                Syllable('värld','SHORT','UNSTRESSED'),
                Syllable('ar','SHORT','UNSTRESSED'),
                Syllable('nas','SHORT','UNSTRESSED'),
                
                Syllable('jäkt','SHORT','UNSTRESSED'),
                
                Syllable('når','SHORT','UNSTRESSED')])
    
    obs.append([Syllable('och','SHORT','UNSTRESSED'),
               
                Syllable('hur','SHORT','UNSTRESSED'),
                
                Syllable('vred','SHORT','UNSTRESSED'),
                Syllable('gat','SHORT','UNSTRESSED'),
                
                Syllable('om','SHORT','UNSTRESSED'),
                Syllable('kring','SHORT','UNSTRESSED'),
                
                Syllable('mig','SHORT','UNSTRESSED'),
                
                Syllable('än','SHORT','UNSTRESSED'),
                
                Syllable('storm','SHORT','UNSTRESSED'),
                Syllable('ar','SHORT','UNSTRESSED'),
                Syllable('nas','SHORT','UNSTRESSED'),
                
                Syllable('brus','SHORT','UNSTRESSED'),
                
                Syllable('går','SHORT','UNSTRESSED')])
    
    obs.append([Syllable('bä','SHORT','UNSTRESSED'),
                Syllable('ra','SHORT','UNSTRESSED'),
               
                Syllable('sol','SHORT','UNSTRESSED'),
                Syllable('skim','SHORT','UNSTRESSED'),
                Syllable('rets','SHORT','UNSTRESSED'),
                
                Syllable('gyll','SHORT','UNSTRESSED'),
                Syllable('e','SHORT','UNSTRESSED'),
                Syllable('ne','SHORT','UNSTRESSED'),
                
                Syllable('krans','SHORT','UNSTRESSED'),
                
                Syllable('om','SHORT','UNSTRESSED'),
                Syllable('kring','SHORT','UNSTRESSED'),
                
                Syllable('min','SHORT','UNSTRESSED'),
                
                Syllable('hjäss','SHORT','UNSTRESSED'),
                Syllable('a','SHORT','UNSTRESSED')])

    bps = BeatPathSet(4)
    bps[0] = [BeatPair(4,10,128),
                BeatPair(11,15,301),
                BeatPair(16,17,393),
                BeatPair(18,18,423),
                BeatPair(19,20,438),
                BeatPair(21,21,462),
                BeatPair(22,22,473),
                BeatPair(23,23,483),
                BeatPair(25,25,500),
                BeatPair(26,27,508),
                BeatPair(28,28,518),
                BeatPair(29,29,522),
                BeatPair(30,30,525),
                BeatPair(31,31,527)]
    
    bps[1] = [BeatPair(6,7,178),
                BeatPair(10,13,278),
                BeatPair(14,14,357),
                BeatPair(15,17,377),
                BeatPair(18,20,425),
                BeatPair(21,22,463),
                BeatPair(23,24,484),
                BeatPair(25,26,501),
                BeatPair(27,27,513),
                BeatPair(28,28,518),
                BeatPair(29,29,522),
                BeatPair(30,30,525),
                BeatPair(31,31,527)]
    
    bps[2] = [BeatPair(12,12,318),
                BeatPair(13,14,339),
                BeatPair(16,16,392),
                BeatPair(18,18,423),
                BeatPair(20,20,450),
                BeatPair(21,21,462),
                BeatPair(22,22,473),
                BeatPair(23,24,484),
                BeatPair(25,27,502),
                BeatPair(28,28,518),
                BeatPair(29,29,522),
                BeatPair(30,30,525),
                BeatPair(31,31,527)]
    
    bps[3] = [BeatPair(8,10,230),
                BeatPair(12,14,320),
                BeatPair(17,17,408),
                BeatPair(18,18,423),
                BeatPair(19,21,439),
                BeatPair(22,22,439),
                BeatPair(23,23,483),
                BeatPair(24,24,492),
                BeatPair(25,25,492),
                BeatPair(27,27,513),
                BeatPair(28,28,518),
                BeatPair(29,29,522),
                BeatPair(30,30,525),
                BeatPair(31,31,527)]
    
#    obs = SyllableSet()
#    bps = BeatPathSet(1)
#    obs.append([Syllable('än','SHORT','UNSTRESSED'),
#                
#                Syllable('storm','SHORT','UNSTRESSED'),
#                Syllable('ar','SHORT','UNSTRESSED'),
#                Syllable('nas','SHORT','UNSTRESSED'),
#                
#                Syllable('brus','SHORT','UNSTRESSED'),
#                
#                Syllable('går','SHORT','UNSTRESSED'), Syllable('SUN', 'SHORT', 'UNSTRESSED')])
#    bps[0] = [BeatPair(0,3,3),          # 4 long
#                BeatPair(4,11,129),     # 8 long
#                BeatPair(12,19,325),    # 8 long
#                BeatPair(20,23,452),    # 4 long
#                BeatPair(24,27,495),    # 4 long 
#                BeatPair(28,31,521)]    # 4 long

    p = LilypondFormatter(bps, obs)
    p.make_ly_file()
