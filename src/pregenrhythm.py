#!/usr/bin/python
# coding: utf-8

import sys

def genmellist_python( s, e, skald_format ):
    rhythminfo = []

    for i in range(s,e): # loop for each verse
        f = open("sweedish/orpheus/{0}/verse_".format(skald_format)+str(i)+".orp", "r")
        c = f.read()
        f.close()
        
        melodyinfo_verse = c.split("[")[1].split("]")[0]
        # print melodyinfo_verse
        for noteinfo in melodyinfo_verse.split("{"):
            onset, offset, syllable = parse_python_format_line(noteinfo,i,s)
            if onset and offset and syllable:
                rhythminfo.append( {"volume":100,
                                    "onset":onset,
                                    "lyric":syllable,
                                    "restriction":"",
                                    "prosody-abs":0,
                                    "pitch":0,
                                    "velocity":0,
                                    "offset":offset,
                                    "prosody":"flat_up"
                                    }
                                   )

    return rhythminfo
###

def parse_python_format_line(noteinfo,i,s):
    onset = None
    offset = None
    syllable = None
    for line in noteinfo.strip().split("\n"):
        # print line
        if "onset" in line:
            onset  = int( line.split(":")[1].split(",")[0] ) + 3840 * (i-s)
        elif "offset" in line:
            offset = int( line.split(":")[1].split(",")[0] ) + 3840 * (i-s)
        elif "syllable" in line:
            syllable = line.split(":")[1].replace("\'","")
        else:
            pass
    return onset, offset, syllable

def genmellist_stdout(verse_number, skald_format ):
    rhythminfo = []

    
    f = open("sweedish/orpheus/{0}/verse_".format(skald_format)+str(verse_number)+".orp", "r")
    c = f.read()
    f.close()
        
    
    # print melodyinfo_verse
    for noteinfo in c.split("\n"):
        print noteinfo
        onset, offset, syllable = parse_stdout_format_line(noteinfo)
        if onset and offset and syllable:
            rhythminfo.append( {"volume":100,
                                "onset":onset,
                                "lyric":syllable,
                                "restriction":"",
                                "prosody-abs":0,
                                "pitch":0,
                                "velocity":0,
                                "offset":offset,
                                "prosody":"flat_up"
                                }
                               )

    return rhythminfo
###
def parse_stdout_format_line(line):
    if len(line) == 0:
        return (None, None, None)
    if "#" == line[0]:
        return (None, None, None)
    else:
        onset, offset, pitch, syllable = line.split()
        return int(onset), int(offset), syllable

def prepare( params, n ):

    if params['skald_format'] == 'python':
        if n == 2:
            r = genmellist_python( 1, 2, 'python')
            return r
        elif n == 4:
            r = genmellist_python( 2, 3, 'python' )
            return r
        else:
            return False
    elif params['skald_format'] == 'stdout':
        if n == 2:
            r = genmellist_stdout(1, 'stdout')
            return r
        elif n == 4:
            r = genmellist_stdout(2, 'stdout' )
            return r
        else:
            return False
    else:
        raise RuntimeError("UNKNOWN SKALD FORMAT SPECIFIED")
