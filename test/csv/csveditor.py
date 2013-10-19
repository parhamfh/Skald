#!/usr/local/bin/python

# coding: utf8

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
    red = unicodecsv.UnicodeReader(csv_f, delimiter=',')
    dic = {}

    for row in red:

        if len(row) < 1:
            continue

        if row[0] not in dic:
            dic[row[0]] = []

        # print row[0]
        dic[row[0]].append(row[1])

    if 'div' not in dic:
        raise RuntimeError('Why no div bro?')

    num_div = int(dic['div'][0])
    fin_dic = {}
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
        if len(dic[key]) == 1:
            fin_dic[key] = dic[key][0]
        # List of values associated with key
        else:
            fin_dic[key] = dic[key]

    # for key in sorted(fin_dic.keys()):
    #     print key
    #     print fin_dic[key]
    #     print '\n==================='

    # Dump our crap to make the orpheus_template.json
    json_dump = json.dumps(fin_dic, sort_keys=True, indent=4)
    print json_dump

    # Check that we can read in the json and put it into csv format
    orp_json = json.loads(json_dump)
    for shit in orp_json:
        print shit, type(orp_json[shit]), len(orp_json[shit])

    # Write back the loaded JSON template in CSV with changes 
    # we want orpheus to respect included

    with open('csvsampleexample.pk','wb') as csvsamplepk:
        shitwriter = unicodecsv.UnicodeWriter(csvsamplepk, delimiter=',')
        # For all the divs, merge the keys in the dict with the div number
        # To create the crappy <div number>:<key>,<value> format
        for crap in orp_json:
            assert False
            shitwriter.writerow([crap,orp_json[crap]])

    # Read in the csv again and jsonify check the keys against the json orp_json
    # Here below
    assert False