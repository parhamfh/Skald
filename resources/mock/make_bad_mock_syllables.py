with open('mockinput') as fp:
    lines = fp.read().splitlines()

final = []
for s in lines:
    final.append([x for x in s.split()])

print final

for s in final:
    print "\n========"
    for x in s:
        print "Syllable('{0}','{1}','{2}'),".format(x,"SHORT","UNSTRESSED")
    