from remote import RemotePhoneticTranscriber

class PhoneticTranscriber(object):
    '''
    See the following Github issue for a discussion regarding the current and 
    desired solution for mocking:
    
    https://github.com/parhamfh/Skald/issues/17
    '''
    def __new__(cls, *args, **kwargs):
        if kwargs.pop('mock', None):
            return MockPhoneticTranscriber(*args, **kwargs)
        
        return RealPhoneticTranscriber(*args, **kwargs)

    REMOTE = 0
    LOCAL = 1

class RealPhoneticTranscriber(object):
    '''
    Transcribes the words in a Swedish text to their phonetic representation.
    
    Accepts a list of inputs as an input.
    '''

    #TRANSCRIBE_MODE = True

    def __init__(self, text_input_or_list, mode=None, protocol=None, mock=None):
        '''
        Constructor
        
        @param mode: Decide 
        '''
        self.text_input = text_input_or_list
        self.text_input_in_list = isinstance(text_input_or_list, list)
        
        if not self.text_input_in_list:
            assert isinstance(self.text_input, unicode)
        
        if mode is None:
            self.TRANSCRIBE_MODE = PhoneticTranscriber.LOCAL
        else:
            self.TRANSCRIBE_MODE = mode

        if protocol is None:
            self.protocol = 'TCP'
        else:
            self.protocol = protocol

    def transcribe(self):
        '''
        Currently we have to contact the windows machine where the tcl script
        is run and fetch the phonetic representation so here we call for
        transcribing it remotely instead of locally.
        '''
        if self.TRANSCRIBE_MODE == PhoneticTranscriber.REMOTE:
            # TODO: handle if list
            return self._transcribe_remotely(protocol = self.protocol)
        
        elif self.TRANSCRIBE_MODE == PhoneticTranscriber.LOCAL:
            return self._transcribe_locally()
        
        else:
            raise RuntimeError("Something is wrong with REMOTE_TRANSCRIBE "\
                               "value.\n value: %s"%self.REMOTE_TRANSCRIBE)
            
    def _transcribe_remotely(self, host=None, port=None, protocol=None):
        '''
        Uses a network connection to a remote server that can run the
        appropriate scrip to transcribe the input
        '''
        if protocol is None:
            rpt = RemotePhoneticTranscriber(host=host, port=port, protocol=self.protocol)
        else:
            rpt = RemotePhoneticTranscriber(host=host, port=port, protocol=protocol)
        response = rpt.transcribe_message(self.text_input, then_disconnect=True)
        print response
        return response
    
    def _transcribe_locally(self):
        '''
        Cannot be done yet
        '''
        # TODO: Handle if list
        raise NotImplementedError('Local transcribing is not implemented yet..')
        
class MockPhoneticTranscriber(object):

    def __init__(self, text_input_or_list, mode=None):
        self.text_input = text_input_or_list
        self.text_input_in_list = isinstance(text_input_or_list, list)
        
        if not self.text_input_in_list:
            assert isinstance(text_input_or_list, unicode)
        
    def transcribe(self):
        '''
        Uses a Mock transcriber.
        '''

        print "MOCK TRANSCRIBING THIS:\n"
        print self.text_input

class PhonemeSet(object):
    def __init__(self):
        pass