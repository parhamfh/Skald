#!/usr/local/bin/python
# coding: utf8

import socket, threading, time, sys
from threading import Lock

from transcriber_server import TranscriberServer

HOST_DOMAIN = 'u-shell.csc.kth.se'
HOST = socket.gethostbyname(HOST_DOMAIN)

class TCPTranscriberServer(TranscriberServer):
    '''
    Remote phonetic transcriber customized to be run on windows machine
    since currently we can only run the TCL script for the CTT toolbox from
    a Windows machine.
    
    Receives connections on 7777. Listen to clients for one message containing
    the input to be transcribed. After receiving the message it is transcribed
    using a local script then sent back. Following this the communication is
    terminated and the connection shut down. 
    
    If Server is local, please specify remote_is_local flag
    #TODO: CAPTURE KEYBOARD INTERUPPTS AND KILL THREADS AND CLOSE SOCKETS

    INSPIRATION

    http://wiki.python.org/moin/TcpCommunication
    
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
            print "{0}: Setting up transcoding.".format(self)
        
        self.listen_thread.transcode(True) # Race condition
        self.listen_thread.start()
        print "{0}: Start transcoding.".format(self)
        
    def stop_transcoding(self):
        if self.has_setup:
            print "{0}: Stopping transcoding.".format(self)
            self.listen_thread.transcode(False)
            self.listen_thread.join(7)
            return
        
        print "{0}: Not running transcoder.".format(self)
        
    def bind_port(self):
        if not self.remote_is_local:
            print "{0} binding on {1}".format(self, HOST)
            self.server_sock.bind((HOST, self.port))
            return
        print "{0} binding on localhost".format(self)
        self.server_sock.bind(('127.0.0.1', self.port))

    def __str__(self):
        return 'TCPTranscriberServer'

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
        self.status_lock = Lock()
        
    def run(self):

        self.status_lock.acquire()
        while self.TRANSCODING:
            self.status_lock.release()
            (clientsocket, address) = self.server_sock.accept()
            print "ListenerThread: Client connection received on socket on"\
            " address: {0}".format(address)
            
            tt = TranscriberThread(clientsocket, self.thread_id)
            tt.daemon = True
            self.thread_id += 1
            tt.start()
            
            self.status_lock.acquire()
            
    def close_listener(self):
        try:
            self.server_sock.shutdown(socket.SHUT_RDWR)
        except socket.error, se:
            print type(se),se
        self.server_sock.close()
        
    def transcode(self, is_transcoding):
        # TODO use Lock or Queue???

        # Acquire lock before changing Transcoding variable
        with self.status_lock:
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
        self.client_sock.sendall('| START OF TRANSMISSION | Sending back message: '+message+' | END OF TRANSMISSION |\n')
    
    # def receive_message(self):
    #     message = ''
    #     latest = self.client_sock.recv(8192)
    #     while latest != '':
    #         message += latest
    #         latest = self.client_sock.recv(8192)
    #         print 'latest now is %s\n==='%latest[0:10]
            
    #     print 'DONE'
    #     return message


if __name__ == '__main__':

    rwpt = TCPTranscriberServer(remote_is_local=True)
    rwpt.start_transcoding()
    
    try:
        print "Main process going idle until threads terminate."
        #http://stackoverflow.com/questions/3788208/python-threading-ignores-keyboardinterrupt-exception
        #rwpt.listen_thread.join()
        while True:
            time.sleep(10)
    except KeyboardInterrupt, ke:
        print "KeyboardInterrupt received. ke: %s"%ke
        rwpt.listen_thread.close_listener()
        sys.exit(0)
