#!/usr/local/bin/python
# coding: utf8
import socket

HOST_DOMAIN = 'u-shell.csc.kth.se'
HOST_DOMAIN = 'localhost'
HOST = socket.gethostbyname(HOST_DOMAIN)

class Sender(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    def send_message(self, message):
        # s.connect(('share-01.csc.kth.se',7777))
        self.s.sendto("A unicode message! {0} ÖÄÅäöå!".format(message), (HOST,7777))

class Receiver(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('127.0.0.1',7777))

    def receive_message(self):
        d = self.s.recv(8124)
        return d

if __name__ == '__main__':
    import sys
    if len(sys.argv) <2:
        print "Sender"
        s = Sender()
        while True:
            s.send_message(raw_input('Send it:!'))
    else:
        print "Receiver"
        r = Receiver()
        while True:
            print "Everyday we receivin'! This right here! {0}".format(r.receive_message())
