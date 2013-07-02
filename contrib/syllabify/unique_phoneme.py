#!/usr/local/bin/python
#coding utf8


f = open("new_nst_STA_fix.syl", "r")
i = 1

unique_list= []
for l in f.readlines():
    print i
    i += 1
    for phoneme in l.split():
        if phoneme not in unique_list:
            unique_list.append(phoneme)

print " ".join(unique_list)
print len(unique_list)