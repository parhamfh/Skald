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

    def __init__(self, sock = None, host=None, port=None, protocol=None):
        '''
        Constructor
        '''
        self.host = host
        self.port = port
        print 'MY PROTOCOL! {0}'.format(protocol)
        self.protocol = protocol
        self.sock = None

    def tcp_connect(self, host=None, port=None):
        if host is None:
            if self.host is None:
                host = 'localhost'
            else:
                host = self.host
        if port is None:
            if self.port is None:
                port = 7777
            else:
                port = self.port
        
        print "{2} connecting to host {0} on port {1}!".format(host, port, self)
        self.sock.connect((host, port))

    def tcp_send_message(self, message="Halloj"):
        print "\nTYPE OF MESSAGE IS {0}\n".format(type(message))
        print u"{0}: Sending message: '{1}'".format(self, message)
        self.sock.sendall(message.encode('utf8'))
    
    def tcp_disconnect(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        
    def setup_socket(self, sock, host, port):
        
        if self.protocol == 'TCP':
            if sock == None:
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                self.sock = sock
            self.tcp_connect(host, port)
        elif self.protocol == 'UDP':
            if sock == None:
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                self.sock = sock
        else:
            raise RuntimeError('Unknown protocol for remote connection! protocol = {0}'.format(self.protocol))

    def send_message(self, message):
        if self.protocol == 'TCP':
            self.tcp_send_message(message)
        elif self.protocol == 'UDP':
            self.udp_sendmessage(message)

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

    def __str__(self):
        return "RemotePhoneticTranscriber"
