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
        choices = self._user_choices_to_json()
        new_sample = self._inject_choices_into_template(f, choices)
        self._write_out_csv(new_sample)

    def _user_choices_to_json(self):
        pass

    def _inject_choices_into_template(self, template_file, user_choices_json):
        pass

    def _write_out_csv(self):
        div_int = int(orp_json['div'])

        with open('comparison_sample.pk','w+') as csvsamplepk:
            shitwriter = unicodecsv.UnicodeWriter(csvsamplepk, delimiter=',')
            # For all the divs, merge the keys in the dict with the div number
            # To create the crappy <div number>:<key>,<value> format
            for crap in sorted(orp_json):
                if is_int(crap) and int(crap) in range(1,div_int+1):
                    di = int(crap)
                    # This is one of the divs (divisions)
                    # These contain dicts
                    div_dict = orp_json[crap]
                    for key in div_dict:
                        # print div_dict[key]
                        shitwriter.writerow(["{0}:{1}".format(di,key),div_dict[key]])
                else:
                    # Not divs, just write it, bruh
                    shitwriter.writerow([crap,orp_json[crap]])