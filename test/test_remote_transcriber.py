#!/usr/local/bin/python

print "SKALD - Testing remote transcriber"

import sys
print sys.version

from skald.transcribe.remote import RemoteTranscriber as RPT

rpt = RPT()
rpt.transcribe_message('Kalas')