# coding: utf8
import re
import os
import subprocess

class TranscriberServer(object):

    def __init__(self):
        # Add necessary external scripts to path
        os.environ['PATH'] += os.pathsep + ("/afs/nada.kth.se/home/2/u1weowl2/kurser/exjobb/Skald/scripts/")
        os.environ['PATH'] += os.pathsep + ("/afs/nada.kth.se/home/2/u1weowl2/kurser/exjobb/Skald/contrib/syllabify/")

    def transcribe(self, message):
        transcribed = []
        if type(message) == str:
            message = unicode(message, encoding='utf8')
        for line in message.split('\n'):
            print u"Processing line: \"{0}\"\n...".format(line)
            lst = re.findall("[\w']+", line, re.UNICODE)
            for i in range(0,len(lst)):
                p = self.phonetize(lst[i])
                # IF DEBUG
                #s = None # self.syllabify(p)
                lst[i] = (lst[i],p)
            transcribed.append(lst)
        print
        return transcribed

    def phonetize(self, word):
        phonetize_proc = subprocess.Popen(['test_tts.tcl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        phonem, err = phonetize_proc.communicate(word.encode(encoding='utf8'))
        return u"{0}".format(phonem.decode(encoding='utf8').rstrip('\n'))

    def syllabify(self, phonetic):
        print "Syllabify says..."
        print phonetic
        print subprocess.check_output(["syll.tcl",self._massage_phonetic(phonetic)])
        print "Syllabify ended."

    def _massage_phonetic(self, phonetic):
        """
            Betoningsmarkeringen ser lite annorlunda ut än i wavesurfer: istället för ' och "
            och ` så sitter det ett suffix på betonade vokaler som är antingen
            _1 (akut accent/accent I)
            _2 (grav accent/accent II)
            _3 (sammansättningsbetoning)
        """
        massaged = phonetic.replace(' {\\\'}', '_1').replace(' {\\"}', '_2').replace(' {\\`}', '_3')
        # If first letter is a stress too
        if massaged[0:4] == '{\\\'}':
            massaged = massaged.replace('{\\\'}', '_1')
        elif massaged[0:4] ==  '{\\"}':
            massaged = massaged.replace('{\\"}', '_2')
        elif massaged[0:4] == '{\\`}':
            massaged = massaged.replace('{\\`}', '_3')

        print massaged
        return massaged

if __name__ == '__main__':

    print "FOR THIS TO BE ABLE TO RUN ON KTH MACHINE test_tts.tcl has to be in the path, make sure to perform:\n{0}\nto avoid crashing server".format('export PATH=$PATH:/afs/nada.kth.se/home/2/u1weowl2/kurser/exjobb/Skald/scripts/')
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
