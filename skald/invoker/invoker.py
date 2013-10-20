# coding: utf8
import os
import shutil

import skald.orpheus as orpheus
from skald.formatter.orpheus import OrpheusFormatter
from skald.invoker import SamplePKFormatter

type_to_string = OrpheusFormatter.type_to_string

ORPHEUS_SUB_DIR = ['skald','orpheus']
ORPHEUS_INPUT_DIR = ['sweedish', 'orpheus']
OUTPUT_SUB_DIR =  ['output','orpheus']

class OrpheusInvoker(object):

    def __init__(self, number_of_verses, skald_filename_stem=None, skald_output_type=None, user_settings=None):
        if not skald_filename_stem:
            raise RuntimeError("Filename stem needs to be specified. skald_filename_stem was None.")
        self.skald_filename_stem = skald_filename_stem

        if not skald_output_type:
            raise RuntimeError("Skald output type needs to be specified. skald_output_type was None.")
        self.skald_output_type = skald_output_type

        # Save current directory
        self.running_directory = os.getcwd()
        # Path for Orpheus submodule
        self.orpheus_running_directory = os.path.join(self.running_directory, *ORPHEUS_SUB_DIR)
        
        output_type_name = type_to_string(self.skald_output_type)
        
        # Path for Orpheus input
        self.input_directory = os.path.join(self.orpheus_running_directory,
                                            os.path.join(*ORPHEUS_INPUT_DIR),
                                            output_type_name)
        
        # Path to Skald's output
        self.skald_output_directory = os.path.join(self.running_directory,
                                                   os.path.join(*OUTPUT_SUB_DIR),
                                                   output_type_name)

        # print self.running_directory
        # print self.orpheus_running_directory
        # print self.input_directory
        # print self.skald_output_directory
        self.number_of_verses = number_of_verses
        self.settings = user_settings

    def invoke(self):
        
        # Change dir to Orpheus's directory
        os.chdir(self.orpheus_running_directory)
        
        # Invoke Orpheus 
        orpheus._main()
        
        # Jump back to original directory
        os.chdir(self.running_directory)

    def prepare_input(self):
        '''
        Takes Skalds output and prepares it for Orpheus, as valid input.
        Also sets up Orpheus' samples.pk with the users choices.
        '''

        self._copy_skald_output(self.skald_filename_stem)
        self._setup_samplespk(self.number_of_verses)

    def _copy_skald_output(self, skald_filename_stem):
        files = os.listdir(self.skald_output_directory)
        
        # Which are the files
        skald_files = [f for f in files if f.startswith(skald_filename_stem)]
        
        # How many Skald output files
        num_skald_files = len(skald_files)

        # Copy files over
        for f in skald_files:
            src = os.path.join(self.skald_output_directory, f)
            
            # f[f.find('_')+1:]: remove index prefix for dst
            dst = os.path.join(self.input_directory, f[f.find('_')+1:])
            shutil.copyfile(src, dst)

        return num_skald_files

    def _setup_samplespk(self, number_of_verses):
        sample_formatter = SamplePKFormatter(self.settings, number_of_verses)
        sample_formatter.generate_sample_pk()