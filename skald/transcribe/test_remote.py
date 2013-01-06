#!/usr/local/bin/python

print "SKALD - Testing remote transcriber"

import sys
print sys.version

from remote import RemotePhoneticTranscriber as RPT

rpt = RPT()
rpt.transcribe_message('Kalas')
