# coding: utf8
'''
Created on Jan 4, 2013

WHEN RUN ON WINDOWS:

WHEN RUN ON OS X:

@author: parhamfh
'''

import socket, threading, time, sys, pickle, re
from threading import Lock

HOST_DOMAIN = 'u-shell.csc.kth.se'
HOST = socket.gethostbyname(HOST_DOMAIN)
PORT = 7777

class RemotePhoneticTranscriber(object):
    '''
    Uses Sockets
    '''

    def __init__(self, sock = None, host=None, port=None, protocol=None):
        '''
        Constructor
        '''
        if host is None:
            self.host = HOST
        else:
            self.host = host
        if port is None:
            self.port = PORT
        else:
            self.port = port

        if protocol is None:
            self.protocol = 'TCP'
        else:
            self.protocol = protocol
        self.sock = None

    def tcp_connect(self, host=None, port=None):
        if host is None:
            host = self.host
        if port is None:
            port = self.port
        
        print "{2} connecting to host {0} on port {1}!".format(host, port, self)
        self.sock.connect((host, port))
        print "{0}: Connected to host!".format(self)

    def tcp_disconnect(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
    
    def tcp_send_message(self, message="Halloj"):
        # print "\nTYPE OF MESSAGE IS {0}\n".format(type(message))
        print u"{0}: Sending message: '{1}'".format(self, message)
        self.sock.sendall(message.encode('utf8'))
    
    def udp_send_message(self, message="Halloj"):
        print u"{0} | 0. Sending message:\n{1}\nto host {2} through port {3}".format(self, message, self.host, self.port)
        self.sock.sendto(message.encode('utf8'),(self.host, self.port))

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
            self.udp_send_message(message)

    def disconnect(self):
        if self.protocol == 'TCP':
            self.tcp_disconnect()
        elif self.protocol == 'UDP':
            pass
        else:
            print 'Unknown protocol!'

    def transcribe_message(self, message, host=None, port=None, then_disconnect=False): 
        self.setup_socket(self.sock, host, port)
        self.send_message(message)
        transcribed_data = self.receive_transcribed_message()
        if then_disconnect:
            print "... now disconnecting"
            self.disconnect()
        # print "{0} | 5. Received the following data: {1}".format(self, transcribed_data)
        return transcribed_data

    def receive_transcribed_message(self):
        print "{0} | 1. Receiving response from transcriber server".format(self)
        response = self.sock.recv(8192)
        print "{0} | 2. Received response with payload:\n{1}".format(self,
                                            response)
        message = self._unpickle_response(response)
        # message = pickle.loads(response)
        print "{0} | 4. Message unpickled. Data contained:\n{1}".format(self, message)
        return message

    def _unpickle_response(self, response):
        pickled_data = self._extract_pickled_data(response)
        print "{0} | 3. Pickled data extracted, presented in repr form for consistency check:\n{1}".format(self, repr(pickled_data))
        return pickle.loads(pickled_data)
    
    def _extract_pickled_data(self, response):
        match = re.findall("\|===\|\\n(.*)\\n\|===\|", response, re.DOTALL)
        # print match
        return match[0]
    
    def __str__(self):
        return "RemotePhoneticTranscriber"
