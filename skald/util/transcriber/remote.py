# coding: utf8
'''
Created on Jan 4, 2013

WHEN RUN ON WINDOWS:


WHEN RUN ON OS X:

@author: parhamfh
'''

import socket, threading, time, sys
from threading import Lock

HOST_DOMAIN = 'u-shell.csc.kth.se'
HOST_DOMAIN = 'localhost'
HOST = socket.gethostbyname(HOST_DOMAIN)

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
    
        
        self.port = port
        self.remote_is_local = remote_is_local
        
        if server_sock == None:
            self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:


    def disconnect(self):
        if self.protocol == 'TCP':
            self.tcp_disconnect()
        elif self.protocol == 'UDP':
            pass
        else:
            print 'Unknown protocol!'

    def transcribe_message(self, message, host=None, port=None, then_disconnect=False): 
        self.setup_socket(self.sock, host, port)
        print "{0}: Connected to host!".format(self)
        self.send_message(message)
        transcribed_message = self.receive_transcribed_message()
        if then_disconnect:
            print "... then disconnecting"
            self.disconnect()
        print "{0} received this message: {1}".format(self, transcribed_message)
        return transcribed_message

    def receive_transcribed_message(self):
        print "{0}: Receiving response message".format(self)
        message = self.sock.recv(8192)
        print "{0}: Message received.".format(self)
        return message

