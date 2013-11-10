#!/usr/local/bin/python

# coding: utf8

'''
    This module takes in the sample.pk and generates a template which we
    can use to create our own sample.pk and pass to orpheus.

    The orpheus_template.json will be used by the actual module 
    outputting the sample.pk to be used.

    So, to clarify: this module is not to be used with Skald
    but ONLY to generate the orpheus_template.json

    Most of this code will be/is lifted to the actual module that does the
    sample.pk generation.
'''

import json
import collections

import unicodecsv

def is_int(int_candidate):
    try:
        int(int_candidate)
        return True
    except ValueError:
        return False

def has_second_part(candidate):
    try:
        candidate[1]
        return True
    except IndexError:
        return False

with open('sample.pk') as csv_f:

    # Read in the sample.pk origina file Fukayama gave you
    red = unicodecsv.UnicodeReader(csv_f, delimiter=',')
    dic = {}

    for row in red:
        if len(row) < 1:
            continue

        if row[0] in dic:
            print 'what', row[0],'already in dict! ABORT'
            assert False 

        dic[row[0]] = row[1]

    if 'div' not in dic:
        raise RuntimeError('Why no div bro?')
    
    # Break out the 'div' keys and prepare a new dict where
    # the div key contains a dict with proper key-values
    num_div = int(dic['div'][0])
    fin_dic = {}

    # SPLIT the DIV KEYS and add to new fin_dic
    for key in dic:
        
        # MAJOR ASSUMPTION THAT IF
        # WE SPLIT KEY AND:
        # A) IT IS AN INTEGER
        # B) IT IS LESS THAN OR EQUAL TO DIV
        # C) IT HAS A SECOND PART
        # 
        # IT IS A DIVISION

        split_key = key.split(':')

        if is_int(split_key[0]) and has_second_part(split_key):
            if int(split_key[0]) <= num_div:
                k = int(split_key[0])
                if k not in fin_dic:
                    fin_dic[k] = {}
                
                fin_dic[k][split_key[1]] = dic[key]
                continue

        # NOT a division so proceed without fancyness

        # Only one value associated to key
        fin_dic[key] = dic[key]

    # Dump our new dictionary to JSON as orpheus_template.json
    with open('orpheus_template.json','w') as orp_dump:
        json.dump(fin_dic, orp_dump, sort_keys=True, indent=4)

    ############
    ### EVERYTHIN BELOW HERE IS JUST FOR CHECKING THAT
    ### THE FILES AND PROCESS ARE CORRECT
    ############
    
    # Check that we can read in the json and put it into csv format
    
    # ORP_JSON IS A DICT
    with open('orpheus_template.json', 'r') as json_dump:
        orp_json = json.load(json_dump)

    # Sorted() on a dict returns the key set sorted
    for shit in sorted(orp_json):
        print shit, type(orp_json[shit]), len(orp_json[shit])

    # Write back the loaded JSON template in CSV with changes 
    # we want orpheus to respect included
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

    # Trust that it is done properly
    # But you could always compare sample.pk and csvsampleexample.pk
