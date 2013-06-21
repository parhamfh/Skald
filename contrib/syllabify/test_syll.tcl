#!/usr/local/bin/tclsh
source syllabify.tcl

readsyllex lex new_nst_STA_fix.syl

# MOTEXEMPEL till varför vi måste köra ord för ord
puts [syllabify lex "O M   M A N   A P A R    S I G "]
puts [syllabify lex "P Å  J  A:   K Å M E R"]
