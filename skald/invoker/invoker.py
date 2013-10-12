# coding: utf8
import os

import skald.orpheus as orpheus

ORPHEUS_SUB_DIR = ['skald','orpheus'] 

    
class OrpheusInvoker(object):
    
    def __init__(self):
        pass

    def invoke(self):
        # Save current directory
        cur_dir = os.getcwd()

        # Path for Orpheus submodule
        orpheus_dir = os.path.join(cur_dir, *ORPHEUS_SUB_DIR)
        
        # Change dir to Orpheus's directory
        os.chdir(orpheus_dir)
        
        # Invoke Orpheus 
        orpheus._main()
        
        # Jump back to original directory
        os.chdir(cur_dir)


    def prepare_input(self, skald_filename_stem=None):
        '''
        Takes Skalds output and prepares it for Orpheus, as valid input.
        Also sets up Orpheus' samples.pk with the users choices.
        '''
        if not skald_filename_stem:
            raise RuntimeError("Filename stem needs to be specified. skald_filename_stem was None.")
        self.copy_skald_output(skald_filename_stem)
        self.setup_samplespk()

    def copy_skald_output(self, skald_filename_stem):
        print skald_filename_stem

    def setup_samplespk(self):
        assert False