import re
import sys
class TranscriberServer(object):

    def __init__(self):
        pass


    def transcribe(self, message):
        transcribed = []
        for line in message.split('\n'):
            lst = re.findall(u"[\w']+", message)
            
            for i in range(0,len(lst)):
                p = self.phonetize(lst[i])
                s = self.syllabify(p)
                lst[i] = (lst[i],p,s)
            transcribed.append(lst)
        return transcribed

    def phonetize(self, word):
        return "phonem{0}".format(word)
        # run local files

    def syllabify(self, phonetic):
        return "syllables{0}".format(phonetic)
        # run local files
if __name__ == '__main__':

    t = TranscriberServer()
    print t.transcribe(sys.argv[1].decode(encoding='utf8'))
    s = 'de ljuva orden i mitt liv'+\
        'behöver inte säga att det är över'+
        'inte heller att det tar slut'+
        'utan ljud, utanför bild'+
        'det kommer ta tid, men sen är jag din'+
        'på din brits'