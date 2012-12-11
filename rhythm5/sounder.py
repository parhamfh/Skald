#!/usr/local/bin/python

import OSC

class Sounder(object):

    def __init__(self, beats):
        self.client = OSC.OSCClient()
        self.client.connect(("127.0.0.1",8777))
        self.beats = beats
        self.data = [0 for _ in xrange(5)]
    
    def set_notes(self,tuple_list):
        for n,d,i in tuple_list:
            self.data[i] = (n, d)

    def send_notes(self):
        bundle=OSC.OSCBundle()
        for i in range(0,5):
            msg = OSC.OSCMessage("/skald/%s"%i)
            msg.append(self.data[i])
            bundle.append(msg)

        self.client.send(bundle)

    def close(self):
        self.client.close()


# opt=0
# ## 0: Play notes
# if opt == 0:
#     data[0] = (60, 1)
#     data[1] = (62, 1)
#     data[2] = (65, 1)
#     data[3] = (55, 1)
#     data[4] = (77, 1)
# ## 1: Play edge value notes
# elif opt == 1:
#     data[0] = (0, 1)
#     data[1] = (0, 1)
#     data[2] = (0, 1)
#     data[3] = (0, 1)
#     data[4] = (0, 1)
# ## 2: Play no notes
# elif opt == 2:
#     data[0] = (-1, 1)
#     data[1] = (-1, 1)
#     data[2] = (-1, 1)
#     data[3] = (-1, 1)
#     data[4] = (-1, 1)
# ## 3: Play some notes
# elif opt == 3:
#     data[0] = (60, 1)
#     data[1] = (-1, 1)
#     data[2] = (65, 1)
#     data[3] = (-1, 1)
#     data[4] = (-1, 1)
