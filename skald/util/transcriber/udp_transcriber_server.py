#!/usr/local/bin/python
# coding: utf8


import socket, threading, time, sys
from threading import Lock

HOST_DOMAIN = 'u-shell.csc.kth.se'
HOST = socket.gethostbyname(HOST_DOMAIN)

class UDPTranscriberServer(object):
    '''

    INSPIRATION: 

    http://wiki.python.org/moin/UdpCommunication

    '''    
    def __init__(self, server_sock=None, port=7777, remote_is_local=False):
        
        self.port = port
        self.remote_is_local = remote_is_local
        
        if server_sock == None:
            self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.server_sock = server_sock
                    
        self.has_setup = False
        self.IS_TRANSCODING = False
        
    def start_transcoding(self):
        '''
        blocking
        '''
        if not self.has_setup:
            self.bind_port()
            self.has_setup = True
            print "{0}: Setting up transcoding.".format(self)

        print "{0}: Start transcoding.".format(self)
        self.IS_TRANSCODING = True
        self.transcode()
        
    def stop_transcoding(self):
        if self.has_setup:
            print "{0}: Stopping transcoding.".format(self)
            self.IS_TRANSCODING = False
            try:
                self.server_sock.shutdown(socket.SHUT_RDWR)
            except socket.error, se:
                print type(se),se
            
            self.server_sock.close()
        print "{0}: Not running transcoder.".format(self)
        
    def bind_port(self):
        if not self.remote_is_local:
            print "{0} binding on {1}".format(self, HOST)
            self.server_sock.bind((HOST, self.port))
            return
        print "{0} binding on localhost".format(self)
        self.server_sock.bind(('127.0.0.1', self.port))

    def transcode(self):
        while self.IS_TRANSCODING:
            data, address = self.server_sock.recvfrom(8192)
            print '{0} | Received the following data from address {2}:\n|{1}|'.format(self, data, address)
            self.server_sock.sendto('Received your message:\n{0}\nThank you!\n'.format(data), address)

    def __str__(self):
        return 'RemoteTCPPhoneticTranscriber'

if __name__ == '__main__':

    rwpt = UDPTranscriberServer(remote_is_local=True)
    rwpt.start_transcoding()
    
    try:
        print "Main process going idle until threads terminate."
        #http://stackoverflow.com/questions/3788208/python-threading-ignores-keyboardinterrupt-exception
        #rwpt.listen_thread.join()
        while True:
            time.sleep(10)
    except KeyboardInterrupt, ke:
        print "KeyboardInterrupt received. ke: %s"%ke
        rwpt.stop_transcoding()
        sys.exit(0)
        
