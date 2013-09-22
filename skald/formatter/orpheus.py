# coding: utf8

import os, os.path

class OrpheusFormatter(object):

    # Format types
    PYTHON = 0
    STDOUT = 1
    
    DEFAULT_SUBFOLDER_STEM = 'output'
    SUBFOLDER_NAME = 'orpheus'
    FILENAME_STEM = 'verse'
    FILENAME_EXTENSION = 'orp'
    TICKS_PER_16TH = 120
    TICKS_OFFSET = 32 * TICKS_PER_16TH
    BEAT_INFO_INDENT = "    "
    

    def __init__(self, beat_path_set, observations_list, output_format=None):
        self.beat_path_set = self.group_paths_in_fours(beat_path_set)
        self.observations_list = observations_list

        if output_format == None:
            self.output_format = OrpheusFormatter.PYTHON
        else:
            self.output_format = output_format

#        for p in self.bps:
#            for i in p:
#                print i
    
        self.output_filename_stem = None
    
    def ensure_path_exists(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def make_rhythm_file(self):
        self.ensure_path_exists(self.folderpath)
        if self.output_format == OrpheusFormatter.PYTHON:
            self.make_python_file()
        elif self.output_format == OrpheusFormatter.STDOUT:
            self.make_stdout_file()

    @property
    def bps(self):
        return self.beat_path_set
    
    @property
    def obs(self):
        return self.observations_list
    
    @property
    def folderpath(self):
        if self.output_format == OrpheusFormatter.PYTHON:
            return os.path.join(self.DEFAULT_SUBFOLDER_STEM,
                                self.SUBFOLDER_NAME, 'python')
        elif self.output_format == OrpheusFormatter.STDOUT:
            return os.path.join(self.DEFAULT_SUBFOLDER_STEM,
                                self.SUBFOLDER_NAME, 'stdout')

    @property
    def file_extension(self):
        return ".{0}".format(self.FILENAME_EXTENSION)
    
    def group_paths_in_fours(self, paths):
        # num_files = math.ceil(len(paths)/4.0)
        tmp = []
        for i in xrange(0,len(paths),4):
            tmp.append(paths[i:i+4])
        print tmp
        return tmp
        
    def make_python_file(self):
        verse_index = 1
        for eight in self.bps:
            with open(self.path_to_file(verse_index),'w+') as fp:
                self.python_write_out_header(fp)
                offset=0
                for bp in eight:
                    self.python_write_out_path_info(fp, offset)
                    mergedlist = map(lambda x,y,z :(x,y,z), 
                                     bp,
                                     self.obs[bp.i], 
                                     range(len(bp)))
                    for b, o, idx in mergedlist:
                        if idx ==  len(bp)-1:
                            self.python_write_out_beat(b, o, fp, ticks_offset=offset, 
                                                last = True)
                            continue
                        self.python_write_out_beat(b, o, fp, ticks_offset=offset)
                    offset += 1
                self.python_write_out_footer(fp)
            verse_index += 1

    def make_stdout_file(self):
        file_index = 1
        for four in self.bps:
            with open(self.path_to_file(file_index),'w+') as fp:
                self.stdout_write_out_header(fp)
                offset=0
                for bp in four:
                    self.stdout_write_out_path_info(fp, offset)
                    mergedlist = map(lambda x,y,z :(x,y,z), 
                                     bp,
                                     self.obs[bp.i], 
                                     range(len(bp)))
                    for b, o, _ in mergedlist:
                        self.stdout_write_out_beat(b, o, fp, ticks_offset=offset)
                    offset += 1
            file_index += 1
    
    def _check_file_index(self, verse_index, file_index):
        if verse_index:
            filename="{0}_{1}_{2}{3}".format(
                file_index,
                self.FILENAME_STEM,
                verse_index,
                self.file_extension)
                   
        else:
            filename = "{0}_{1}{2}".format(
                file_index,
                self.FILENAME_STEM,
                self.file_extension)

        print os.path.join(self.folderpath,filename)
        filepath = os.path.join(self.folderpath,filename)
        print os.path.isfile(filepath)
        return os.path.isfile(filepath)

    def _find_filename_stem(self,verse_index, file_index=0):
        # Actual filename
        if self._check_file_index(verse_index, file_index):
            print 'here'
            return self._find_filename_stem(verse_index, file_index=file_index+1)
        else:
            print 'i like it'
            return "{0}_{1}".format(file_index,self.FILENAME_STEM)

    def filename_stem(self, verse_index=None):
        if self.output_filename_stem:
            return self.output_filename_stem

        # Check if file already exists
        self.output_filename_stem = self._find_filename_stem(verse_index)
        return self.output_filename_stem

    def filename(self, verse_index=None):
        if verse_index is None:
            return "{0}{1}".format(self.FILENAME_STEM,self.FILENAME_EXTENSION)
        
        return "{0}_{1}{2}".format(self.filename_stem(verse_index), verse_index, self.file_extension)
        
    def path_to_file(self, verse_index):
        return os.path.join(self.folderpath,self.filename(verse_index))
        
    def python_write_out_header(self, fp):
        HEADER = "# THIS FILE HAS BEEN AUTOMATICALL GENERATED BY SKALD\n"+\
            "#\n"+\
            "# This file describes a rhythm pattern to be used in Orpheus\n"+\
            "# The timings are given in MIDI ticks\n"+\
            "# The default pitch is 385 Hz which is a G4\n"+\
            "\n"+\
            "Rhythm = [\n"
        
        fp.write(HEADER)
        
    def python_write_out_footer(self, fp):
        FOOTER = "]\n"
        
        fp.write(FOOTER)
    
    def python_write_out_path_info(self, fp, ticks_offset):
        write_str = \
        "\n{0}#################################################".format(self.BEAT_INFO_INDENT)+\
        "\n{0}# BEAT PATH WITH TICKS OFFSET BY {1} ({2} bars)".format(self.BEAT_INFO_INDENT, 
                                                         self.TICKS_OFFSET*
                                                         ticks_offset,
                                                         ticks_offset*2)+\
        "\n{0}#################################################\n".format(self.BEAT_INFO_INDENT)
        fp.write(write_str)
        
    def python_write_out_beat(self, beat, observation, fp, ticks_offset=0, last = False):
        write_str = \
        "\n{0}# Beat from index {1} through {2}\n".format(self.BEAT_INFO_INDENT,
                                                          beat.origin,
                                                          beat.to)+\
        "{0}{{\n".format(self.BEAT_INFO_INDENT)+\
        "{0}'onset': {1},\n".format(self.BEAT_INFO_INDENT*2,
                                self.calculate_onset(beat, ticks_offset))+\
        "{0}'offset': {1},\n".format(self.BEAT_INFO_INDENT*2,
                                  self.calculate_offset(beat, ticks_offset))+\
        "{0}'pitch': {1},\n".format(self.BEAT_INFO_INDENT*2,
                                  self.calculate_pitch(beat))+\
        "{0}'syllable': '{1}'\n".format(self.BEAT_INFO_INDENT*2,
                                  observation.syllable)+\
        "{0}}}{1}\n".format(self.BEAT_INFO_INDENT, ',' if not last else '')

        fp.write(write_str)
    
    def stdout_write_out_header(self, fp):
        fp.write("### AUTOMATICALLY GENERATED BY SKALD ###\n")
        
    def stdout_write_out_path_info(self, fp, ticks_offset):
        fp.write("#{0} bars offset. {1} ticks.\n".format(ticks_offset*2,
                                                       ticks_offset*self.TICKS_OFFSET))
    
    def stdout_write_out_beat(self, beat, observation, fp, ticks_offset=0):
        fp.write("{0} {1} {2} '{3}'\n".format(self.calculate_onset(beat, ticks_offset),
        self.calculate_offset(beat, ticks_offset),
        self.calculate_pitch(beat),
        observation.syllable.encode(encoding='utf8')))
    
    def calculate_onset(self, beat, ticks_offset):
        return beat.origin*self.TICKS_PER_16TH+self.TICKS_OFFSET*ticks_offset
    
    def calculate_offset(self, beat, ticks_offset):
        return (1+beat.to) * self.TICKS_PER_16TH+self.TICKS_OFFSET*ticks_offset
    
    def calculate_pitch(self, beat):
        if beat.note_value is not None:
            return beat.note_value
        
        return str(385) # G4
        