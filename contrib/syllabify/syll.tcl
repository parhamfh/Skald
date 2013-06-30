#!/usr/bin/tclsh

variable folder "~/kurser/exjobb/Skald/contrib/syllabify/"

source $folder/syllabify.tcl

readsyllex lex $folder/new_nst_STA_fix.syl

puts [syllabify lex [lindex $argv 0]]
