#!/usr/local/bin/python
#coding: utf8


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

spl ='A B D S F T G J L N R RN K M P V NG O RS RD RT SJ A: rA E E: I TJ I: O: U U: Y: Ä Ä3 Ä4 Ä: Ö3 Ö4 Ö: Y Å Å: Ö bA dA lA fA RL gA H hA jA kA mA nA s pA tA sA vA'
print spl, len(spl.split())