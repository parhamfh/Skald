# coding: utf8

import skald.util.assets as assets

class SamplePKFormatter(object):

    ORPHEUS_JSON_TEMPLATE = 'orpheus_template.json'
    
    def __init__(self, settings, number_of_verses):
        self.settings = settings
        self.number_of_verses = number_of_verses

    def generate_sample_pk(self, f=None):
        self._read_in_json_template()
        # if f is None:
        #     f = open('sample.pk', 'w')
        # with f:
        #     f.write('div,%s\n'%self.number_of_verses)

    ## TAKE stuff from csveditor.py

    def _read_in_json_template(self):
        f = assets.get_my_file(self.ORPHEUS_JSON_TEMPLATE)
        
    def _settings_to_json(self):
        pass

    def _inject_settings_in_template(self):
        pass

    def _write_out_csv(self):
        pass