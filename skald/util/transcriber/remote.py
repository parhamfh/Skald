'''
Created on Jan 4, 2013

WHEN RUN ON WINDOWS:


WHEN RUN ON OS X:

@author: parhamfh
'''

import socket, threading, time, sys
from threading import Lock

class RemotePhoneticTranscriber(object):
    '''
    Uses Sockets
    '''

    def __init__(self, sock = None):
        '''
        Constructor
        '''
        if sock == None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        
    def connect(self, host=None, port=None):
        if host is None:
            host = 'localhost'
        if port is None:
            port = 7777
            
        self.sock.connect((host, port))

    def send_message(self, message="Halloj"):
        self.sock.sendall(message)
    
    def receive_transcribed_message(self):
        message = self.sock.recv(8192)
        return message
    
    def close_connection(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        
    def transcribe_message(self, message, host=None, port=None):
        self.connect(host, port)
        self.send_message(message)
        transcribed_message = self.receive_transcribed_message()
        self.close_connection()
        print "RemotePhoneticTranscriber got this message: %s"%(
                                                        transcribed_message)
        return transcribed_message
    
class RemoteWindowsPhoneticTranscriber(object):
    '''
    Remote phonetic transcriber customized to be run on windows machine
    since currently we can only run the TCL script for the CTT toolbox from
    a Windows machine.
    
    Receives connections on 7777. Listen to clients for one message containing
    the input to be transcribed. After receiving the message it is transcribed
    using a local script then sent back. Following this the communication is
    terminated and the connection shut down. 
    
    
    #TODO: CAPTURE KEYBOARD INTERUPPTS AND KILL THREADS AND CLOSE SOCKETS
    '''
    
    def __init__(self, server_sock=None, port=7777, remote_is_local=False):
        
        self.port = port
        self.remote_is_local = remote_is_local
        
        if server_sock == None:
            self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.server_sock = server_sock
                    
        self.has_setup = False
        self.listen_thread = ListenerThread(self.server_sock)
        self.listen_thread.daemon = True
        
    def start_transcoding(self):
        '''
        blocking
        '''
        if not self.has_setup:
            self.bind_port()
            self.server_sock.listen(5)
            self.has_setup = True
            print "RemoteWindowsPhoneticTranscriber: Setting up transcoding."
        
        self.listen_thread.transcode(True) # Race condition
        self.listen_thread.start()
        print "RemoteWindowsPhoneticTranscriber: Start transcoding."
        
    def stop_transcoding(self):
        if self.has_setup:
            print "RemoteWindowsPhoneticTranscriber: Stopping transcoding."
            self.listen_thread.transcode(False)
            self.listen_thread.join(7)
            return
        
        print "RemoteWindowsPhoneticTranscriber: Not running transcoder."
        
    def bind_port(self):
        if not self.remote_is_local:
            self.server_sock.bind((socket.gethostname(), self.port))
            return
        self.server_sock.bind(('127.0.0.1', self.port))

class ListenerThread(threading.Thread):
    '''
    ListenerThread
    
    is a daemon thread so when KeyboardInterrupt is received by main thread
    and it gets killed, the Listener will also go down.
    '''
    TRANSCODING = False
    thread_id = 0

    def __init__(self, server_sock):
        threading.Thread.__init__(self)
        self.server_sock = server_sock
        self.lock = Lock()
        
    def run(self):
        self.lock.acquire()
        while self.TRANSCODING:
            self.lock.release()
            (clientsocket, address) = self.server_sock.accept()
            print "ListenerThread: Client connection received on socket on"\
            " address: {0}".format(address)
            
            tt = TranscriberThread(clientsocket, self.thread_id)
            tt.daemon = True
            self.thread_id += 1
            tt.start()
            
            self.lock.acquire()
            
    def close_listener(self):
        try:
            self.server_sock.shutdown(socket.SHUT_RDWR)
        except socket.error, se:
            print type(se),se
        self.server_sock.close()
        
    def transcode(self, is_transcoding):
        # TODO use Lock or Queue???
        with self.lock:
            self.TRANSCODING = is_transcoding
        
class TranscriberThread(threading.Thread):
    '''
    TranscriberThread
    
    is a daemon thread so when KeyboardInterrupt is received by main thread
    and it gets killed, the Listener will also go down.
    '''
    def __init__(self, clientsocket, thread_id):
        threading.Thread.__init__(self)
        self.client_sock = clientsocket
        self.thread_id = thread_id
        print "Transcriber {0} initiated contact with socket on {1}".format(
                                                        self.thread_id, 
                                                        self.client_sock.getsockname())
        
    def run(self):
#        message = self.receive_message()
        message = self.client_sock.recv(8192)
        print "Transcriber {0}: received message '{2}' from socket on {1}\n"\
        "Doing some local stuff to the message".format(
                                                        self.thread_id, 
                                                        self.client_sock.getsockname(),
                                                        message)
        self.client_sock.sendall('BABYLONIANS TAKE HEED '+message+' ENDOFT')
    
    def receive_message(self):
        message = ''
        latest = self.client_sock.recv(8192)
        while latest != '':
            message += latest
            latest = self.client_sock.recv(8192)
            print 'latest now is %s\n==='%latest[0:10]
            
        print 'DONE'
        return message
        
if __name__ == '__main__':
    import platform
    
    if platform.system() == 'Darwin':
        rpt = RemotePhoneticTranscriber()
        print 'MAC ATTAC'
    
    elif platform.system() == 'Windows':
        rwpt = RemoteWindowsPhoneticTranscriber(remote_is_local=True)
        rwpt.start_transcoding()
    else:
        print("Doing nothing, unspecified platform")

#    rwpt = RemoteWindowsPhoneticTranscriber(remote_is_local=True)
#    rwpt.start_transcoding()
    try:
        print "MAIN IS BACK"
        #rwpt.listen_thread.join()
        #http://stackoverflow.com/questions/3788208/python-threading-ignores-keyboardinterrupt-exception
        while True:
            time.sleep(10)
    except KeyboardInterrupt, ke:
        print "KeyboardInterrupt received. ke: %s"%ke
        rwpt.listen_thread.close_listener()
        sys.exit(0)
