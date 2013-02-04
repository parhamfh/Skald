from skald.transcribe.remote import RemoteTranscriber

class Transcriber(object):
    '''
    Transcribes the words in a Swedish text to their phonetic representation
    '''
    
    REMOTE_TRANSCRIBE = True
    
    def __init__(self, normal_text, remote=True):
        '''
        Constructor
        '''
        self.text = normal_text
        
        if not remote:
            self.REMOTE_TRANSCRIBE = remote
    
    def transcribe(self):
        '''
        Currently we have to contact the windows machine where the tcl script
        is run and fetch the phonetic representation so here we call for
        transcribing it remotely instead of locally.
        '''
        if self.REMOTE_TRANSCRIBE:
            return self.transcribe_remotely()
        
        elif not self.REMOTE_TRANSCRIBE:
            return self.transcribe_locally()
        
        else:
            raise RuntimeError("Something is wrong with REMOTE_TRANSCRIBE "\
                               "value.\n value: %s"%self.REMOTE_TRANSCRIBE)
            
    def transcribe_remotely(self):
        '''
        Uses a network connection to a remote server that can run the
        appropriate scrip to transcribe the input
        '''
        rpt = RemoteTranscriber()
        rpt.connect()
        response = rpt.transcribe_message(self.text)
        print response
        
        return response
    
    def transcribe_locally(self):
        '''
        Cannot be done yet
        '''
        pass