#!/usr/local/bin/python
#coding: utf8
import re, pickle

a ="|===|\n�]q]q(XadfaqX{\"} A D F {\'} AqUsq�qXaqX{\'} Aqh�ea.\n|===|"

a = "|===|�]q]q(XadfaqX{\"} A D F {\'} AqUsq�qXaqX{\'} Aqh�ea.|===|"

a = "|===|mamam|===|"

# a = unicode(a, encoding='utf8')
print a

def _extract_pickled_data(response):
    pattern = re.compile("^([=|].*)", re.MULTILINE)#re.compile(r"^(.+)\n((?:\n.+)+)", re.MULTILINE)
    return pattern.search(response, re.MULTILINE)

pa = _extract_pickled_data(a)
print "matching:"
print pa.groups()

print "unpickling:"
un = pickle.loads(pa)