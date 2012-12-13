from os import path

class Ponder(object):

    FILE_EXTENSION = ".ly"

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
        print 'select',score_name
        if self.unused_filename(score_name):
            self.name = score_name
        else:
            self.name = self.increment_score_name(score_name, score_name, 2)

    def unused_filename(self, fn):
        print 'unused',fn
        # Fancy stackoverflow answer
        # try:
        #     with open(path.join(self.subfolder,fn)) as f: return False
        # except IOError as e:
        #     return True
        if path.isfile(path.join(self.subfolder,fn+self.FILE_EXTENSION)):
            return False
        else:
            return True

    def increment_score_name(self, score_name, stem, order):
        '''
        We assume that since it exists it either has a 
        number or not, between the score name and the file
        extension .ly.
        '''
        print 'inc',score_name, stem, order
        if score_name == stem:
            print "What"
            return self.increment_score_name(score_name+str(order), stem, order)
        elif self.unused_filename(stem+str(order)):
            print "YES"
            return stem+str(order)
        else:
            return self.increment_score_name(score_name+str(order), stem, order+1)

    def generate_ly_file(self):
        pass

    def generate_pdf(self):
        pass

    def format_string(self):
        pass
    
    def execute_binary(self):
        pass
