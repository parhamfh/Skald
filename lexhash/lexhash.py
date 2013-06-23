#!/usr/local/bin/python
# coding: utf8

import time, string

TABLE = string.maketrans("åäö","åäö")
def find_word(word, words):
    for w in words:
        # print "is '{0}' '{1}'  ?".format(w.split()[0],word)
        if w.split()[0] == word:
            return True
    return False

def lower_and_strip(word):
    return word.translate(TABLE, string.punctuation).lower()

lexicon = open("../contrib/swe-dictionary/swe030224STA.dict")
start_time = time.time()

words=[]
for l in lexicon.readlines():
    words.append("{0}".format(l))

boye = open("../resources/mock/mockinput")
boyo = []
for b in boye:
    boyo.extend(b.split())
boyo_time = time.time()

for word in boyo:
    if not find_word(lower_and_strip(word), words):
    # if not find_word(word.lower(), words):
        print "Word \"{0}\" not found!".format(word)

end_time = time.time()
print "Execution time: {1} ({0})".format(end_time - start_time,round(end_time - start_time, 6))
print "Boye time: {1} ({0})".format(boyo_time - start_time,round(boyo_time - start_time, 6))
