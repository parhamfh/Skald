#!/usr/bin/tclsh

package require tts

# create a tts object
set t [tts::create -language sw]

while {![eof stdin]} {
    # read next line
    set line [gets stdin]
    # transcribe line
    set trans [tts::transcribe $t "$line"]
    # split transcription
    set trans [tts::tsplit-sw $trans 1]
    puts $trans
}
