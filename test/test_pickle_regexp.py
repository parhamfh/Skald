#!/usr/local/bin/python
#coding: utf8
import re, pickle

# FOR CHECKING UNPICKLING
# a ="|===|\n\x80\x02]q\x00]q\x01(X\x05\x00\x00\x00kollaq\x02X\r\x00\x00\x00K {\\\"} \xc3\x85 L Aq\x03U\x01sq\x04\x87q\x05X\x02\x00\x00\x00inq\x06X\x08\x00\x00\x00{\\\'} I Nq\x07h\x04\x87q\x08ea.\n|===|"
a= "|===|\n\x80\x02]q\x00(]q\x01(X\x05\x00\x00\x00kollaq\x02X\r\x00\x00\x00K {\\\"} \xc3\x85 L Aq\x03U\x01sq\x04\x87q\x05X\x03\x00\x00\x00p\xc3\xa5q\x06X\n\x00\x00\x00P {\\\'} \xc3\x85:q\x07h\x04\x87q\x08X\x04\x00\x00\x00minaq\tX\r\x00\x00\x00M {\\\"} I: N Aq\nh\x04\x87q\x0bX\x04\x00\x00\x00b\xc3\xa4rq\x0cX\x0c\x00\x00\x00B {\\\'} \xc3\x843 Rq\rh\x04\x87q\x0ee]q\x0f(X\x05\x00\x00\x00k\xc3\xa4raq\x10X\x0f\x00\x00\x00TJ {\\\"} \xc3\x843 R Aq\x11h\x04\x87q\x12X\x07\x00\x00\x00v\xc3\xa4nnerq\x13X\x10\x00\x00\x00V {\\\"} \xc3\x84 N E0 Rq\x14h\x04\x87q\x15e]q\x16(X\x03\x00\x00\x00hejq\x17X\n\x00\x00\x00H {\\\'} E Jq\x18h\x04\x87q\x19X\x03\x00\x00\x00d\xc3\xa5q\x1aX\n\x00\x00\x00D {\\\'} \xc3\x85:q\x1bh\x04\x87q\x1cee.\n|===|"

# FOR CHECKING REGEXP
# a = "|===|�]q]q(XadfaqX{\"} A D F {\'} AqUsq�qXaqX{\'} Aqh�ea.|===|"
# a = "|===|mamam|===|"

# a = unicode(a, encoding='utf8')
print a

def _extract_pickled_data(response):
    pattern = re.compile(u"\|===\|\\n(.*)\\n\|===\|", re.DOTALL) #re.compile(r"^(.+)\n((?:\n.+)+)", re.MULTILINE)
    return pattern.search(response)

# print re.findall("\|===\|\\n(.*)\\n\|===\|", a, re.DOTALL)
# print re.findall("\|===\|(.*)\|===\|", a)
pa = _extract_pickled_data(a)
print "\nmatching:"
print pa.groups()[0], type(pa.groups()[0])

print "unpickling:"
un = pickle.loads(pa.groups()[0])
for i in un:
    for w in i:
        print w[1]