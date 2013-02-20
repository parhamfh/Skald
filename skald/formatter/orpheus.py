# coding: utf8

import os.path

class OrpheusFormatter(object):

    SUBFOLDER_NAME = 'orpheus'
    FILENAME_STEM = 'verse'
    FILENAME_EXTENSION = 'orp'
    TICKS_PER_16TH = 120
    BEAT_INFO_INDENT = "    "

    def __init__(self, beat_path_set, observations_list):
        self.beat_path_set = beat_path_set
        self.observations_list = observations_list

    def make_rhythm_file(self):
        file_index = 1
        for i in range(len(self.bps)):
#            for bp in self.bps:
            with open(self.path_to_file(file_index),'w') as fp:
                self.write_out_header(fp)
                mergedlist = map(lambda x,y,z :(x,y,z),self.bps[i], self.obs[i], range(len(self.bps[i])))
                for b, o, idx in mergedlist:
                    if idx ==  len(self.bps[i])-1:
                        self.write_out_beat(b, o, fp, last = True)
                        continue
                    self.write_out_beat(b, o, fp)
                self.write_out_footer(fp)
            file_index += 1
            
    @property
    def bps(self):
        return self.beat_path_set
    
    @property
    def obs(self):
        return self.observations_list
    
    @property
    def subfolder(self):
        return self.SUBFOLDER_NAME
    
    @property
    def file_extension(self):
        return ".{0}".format(self.FILENAME_EXTENSION)
    
    def filename(self, index=None):
        if index is None:
            return "{0}{1}".format(self.FILENAME_STEM,self.FILENAME_EXTENSION)
        
        return "{0}_{1}{2}".format(self.FILENAME_STEM, index, self.file_extension)
        
    def path_to_file(self, file_index):
        return os.path.join(self.subfolder,self.filename(file_index))
        
    def write_out_header(self, fp):
        HEADER = "# THIS FILE HAS BEEN AUTOMATICALL GENERATED BY SKALD\n"+\
            "#\n"+\
            "# This file describes a rhythm pattern to be used in Orpheus\n"+\
            "# The timings are given in MIDI ticks\n"+\
            "# The default pitch is 385 Hz which is a G4\n"+\
            "\n"+\
            "Rhythm = [\n"
        
        fp.write(HEADER)
        
    def write_out_footer(self, fp):
        FOOTER = "]\n"
        
        fp.write(FOOTER)
    
    def write_out_beat(self, beat, observation, fp, last = False):
        write_str = \
        "\n{0}# Beat from index {1} through {2}\n".format(self.BEAT_INFO_INDENT,
                                                          beat.origin,
                                                          beat.to)+\
        "{0}{{\n".format(self.BEAT_INFO_INDENT)+\
        "{0}'onset': {1},\n".format(self.BEAT_INFO_INDENT*2,
                                self.calculate_onset(beat))+\
        "{0}'offset': {1},\n".format(self.BEAT_INFO_INDENT*2,
                                  self.calculate_offset(beat))+\
        "{0}'pitch': {1},\n".format(self.BEAT_INFO_INDENT*2,
                                  self.calculate_pitch(beat))+\
        "{0}'syllable': '{1}'\n".format(self.BEAT_INFO_INDENT*2,
                                  observation.syllable)+\
        "{0}}}{1}\n".format(self.BEAT_INFO_INDENT, ',' if not last else '')
        
        fp.write(write_str)
        
    def calculate_onset(self, beat):
        return beat.origin*self.TICKS_PER_16TH
    
    def calculate_offset(self, beat):
        return (1+beat.to) * self.TICKS_PER_16TH
    
    def calculate_pitch(self, beat):
        if beat.note_value is not None:
            return beat.note_value
        
        return str(385) # G4
        