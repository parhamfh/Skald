# coding: utf8

# import sys

print "\n### OPTION 1 (unicode type) ###\n"

a = u'change these letters äöå'

la = (lambda x: a.replace(x, u'{0}.'.format(x)))

bb = map(la, u'åäö')

for c in bb:
    print c

print "\n### OPTION 2 (list of vowels) ###\n"

a = 'change these letters äöå'
fn = (lambda x: a.replace(x, '{0}.'.format(x)))
bb  = map(fn, 'å ä ö'.split())

for c in bb:
    print c
# for letter in unicode('åäö',encoding='utf8'):
#     print letter
