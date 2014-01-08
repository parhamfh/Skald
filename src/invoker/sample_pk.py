# coding: utf8

import os
import json
import tempfile

import skald.util.assets as assets
from skald.util import merge_dicts, is_int
from skald.util.unicodecsv import UnicodeWriter

class SamplePKFormatter(object):
    '''
    Uses the .json template to generate the sample_pk .csv file which Orpheus
    reads song settings from.

    Converts .json to Python dict and merges it with user input, outputting the
    resulting dict as a comma-separated CSV file.

    '''

    # ORPHEUS_JSON_TEMPLATE = 'orpheus_template.json'
    ORPHEUS_JSON_TEMPLATE = 'test_orp_temp.json'
    
    def __init__(self, settings, number_of_verses, user_choices=None):
        self.settings = settings
        self.number_of_verses = number_of_verses
        self.user_choices = user_choices

    def generate_sample_pk(self):

        template = self._read_in_json_template()

        choices = self._user_choices_to_dict(self.user_choices)

        new_sample = self._inject_choices_into_template(template, choices)

        return self._write_out_csv(new_sample)


    def _read_in_json_template(self):
        f = assets.get_my_file(self.ORPHEUS_JSON_TEMPLATE)
        return f

    def _user_choices_to_dict(self, choices):
        # TODO: Add attribute for telling Orpheus which sections are verses and which are not
        # for pregenrhythm.py in Orpheus, so we can skip the if's in prepare(params, n)
        
        # Mock user input, lyrics, rhythm pattern, key and stuff
        return {'name':'"Sam the Ham"'}

    def _template_to_dict(self,template_json_file):
        with template_json_file as template_json:
             template_dict = json.load(template_json)
        return template_dict


    def _merge_dictionaries(self, a, b):
        '''
        Override any values in dict a that also exist in
        dict b. 

        Respect dicts in dicts and merges recursively.
        '''

        return merge_dicts(a, b)

    def _inject_choices_into_template(self, template_file, user_choices_json=None):
        template_dict = self._template_to_dict(template_file)
        # The latter will override existing variables in the former
        merged_dict = self._merge_dictionaries(template_dict, user_choices_json)
        return merged_dict

    def _write_out_csv(self, sample_pk_dict):
        div_int = int(sample_pk_dict['div'])

        tmp_sample_pk = os.path.join(tempfile.mkdtemp(prefix='skald_tmp_'),'sample.pk')
        
        with open(tmp_sample_pk,'w+') as tmp_sp:
            shitwriter = UnicodeWriter(tmp_sp, delimiter=',',lineterminator='\n')
            # For all the divs, merge the keys in the dict with the div number
            # To create the crappy <div number>:<key>,<value> format
            for crap in sorted(sample_pk_dict):
                if is_int(crap) and int(crap) in range(1,div_int+1):
                    di = int(crap)
                    # This is one of the divs (divisions)
                    # These contain dicts
                    div_dict = sample_pk_dict[crap]
                    for key in div_dict:
                        # print div_dict[key]
                        shitwriter.writerow(["{0}:{1}".format(di,key),div_dict[key]])
                else:
                    # Not divs, just write it, bruh
                    shitwriter.writerow([crap,sample_pk_dict[crap]])

        return tmp_sample_pk