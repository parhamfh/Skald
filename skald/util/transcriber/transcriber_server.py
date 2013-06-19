# coding: utf8
import re
import sys
import subprocess

class TranscriberServer(object):

    def __init__(self):
        pass


    def transcribe(self, message):
        transcribed = []
        for line in message.split('\n'):
	    print u"Processing line: \"{0}\"\n...".format(line)
	    lst = re.findall("[\w']+", line, re.UNICODE)
            for i in range(0,len(lst)):
                p = self.phonetize(lst[i])
                s = self.syllabify(p)
                lst[i] = (lst[i],p,s)
            transcribed.append(lst)
        return transcribed

    def phonetize(self, word):
    	sys.path.append("/afs/nada.kth.se/home/2/u1weowl2/kurser/exjobb/Skald/scripts/")
	phonetize_proc = subprocess.Popen(['test_tts.tcl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	phonem, err = phonetize_proc.communicate(word.encode(encoding='utf8'))
        return u"{0}".format(phonem.decode(encoding='utf8').rstrip('\n'))
        # run local files

    def syllabify(self, phonetic):
        return "s"

        # run local files
if __name__ == '__main__':

    t = TranscriberServer()
    # print t.transcribe(sys.argv[1].decode(encoding='utf8'))
    s = 'En liten gåva till D.\n'\
    	+'de "ljuva" orden i mitt liv\n'\
        +'behöver inte säga att det är över\n'\
        +'inte heller att det tar slut\n'\
        +'utan ljud, utanför bild\n'\
	+'det kommer ta tid, men sen är jag din\n'\
        +'på din brits'
    s = unicode(s, encoding='utf8')
    response = t.transcribe(s)
    for line in response:
    	print '\n',"|".join(map(lambda (x,y,z):x, line))
	for (a,b,c) in line:
		print u'    {0} : {1}'.format(a,b)
