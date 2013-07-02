#!/usr/bin/tclsh

# variable folder "~/kurser/exjobb/Skald/contrib/syllabify/"
variable folder "~/skald/contrib/syllabify/"

source $folder/syllabify.tcl

readsyllex lex $folder/new_nst_STA_fix.syl

# MOTEXEMPEL till varför vi måste köra ord för ord
puts [syllabify lex "O M   M A N   A P A R    S I G "]
puts [syllabify lex "P Å  J  A:   K Å M E R"]

puts [syllabify lex [lindex $argv 0]]
