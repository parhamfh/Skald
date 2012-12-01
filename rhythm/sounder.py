#!/usr/local/bin/python

import OSC

client = OSC.OSCClient()

client.connect(("127.0.0.1",8777))

bundle=OSC.OSCBundle()
bundle.append

data = [0 for _ in xrange(5)]
data[0] = (60, 1)
data[1] = (62, 1)
data[2] = (65, 1)
data[3] = (55, 1)
data[4] = (77, 1)
for i in range(0,5):
    msg = OSC.OSCMessage("/skald/%s"%i)
    msg.append(data[i])
    bundle.append(msg)

client.send(bundle)

client.close()