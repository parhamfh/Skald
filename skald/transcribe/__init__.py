from skald.transcribe.remote import RemoteTranscriber

class PhoneticTranscriber(object):
    '''
    Transcribes the words in a Swedish text to their phonetic representation.
    
    Accepts a list of inputs as an input.
    '''
    
    REMOTE = 0
    LOCAL = 1
    MOCK = 2
#    TRANSCRIBE_MODE = True
    
    def __init__(self, raw_text_or_list, mode=None):
        '''
        Constructor
        '''
        self.raw_text = raw_text_or_list
        self.raw_text_is_list = isinstance(raw_text_or_list, list)
        
        if not self.raw_text_is_list:
            assert isinstance(raw_text_or_list, str)
        
        if mode is None:
            self.TRANSCRIBE_MODE = PhoneticTranscriber.REMOTE
        else:
            self.TRANSCRIBE_MODE = mode

    def transcribe(self):
        '''
        Currently we have to contact the windows machine where the tcl script
        is run and fetch the phonetic representation so here we call for
        transcribing it remotely instead of locally.
        '''
        if self.TRANSCRIBE_MODE == PhoneticTranscriber.REMOTE:
            # TODO: handle if list
            return self.transcribe_remotely()
        
        elif self.TRANSCRIBE_MODE == PhoneticTranscriber.LOCAL:
            return self.transcribe_locally()
        
        elif self.TRANSCRIBE_MODE == PhoneticTranscriber.MOCK:
            return self.transcribe_mockingly()
        
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
        # TODO: Handle if list
        pass

    def transcribe_mockingly(self):
        '''
        Uses a Mock transcriber.
        '''
        return self.raw_text
        
class PhonemeSet(object):
    def __init__(self):
        pass