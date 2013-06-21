set maxlen 8

proc syllabify {lexvar trans} {
    upvar $lexvar lex
   # puts [info level 0]
   # puts lexsize:[llength [array names lex]]
    set candidates [list]

    for {set i 0} {$i<$::maxlen} {incr i} {
	set p1 [lrange $trans 0 $i]
	set p2 [lrange $trans [expr $i+1] end]
	#	puts <$p1>,<$p2>

	if [info exists lex($p1)] {
	    if {[llength $p2]==0} {
		# p1 is the last syllable
		# puts "last syll: $p1"
		return $p1
	    } else {
		set rest [syllabify lex $p2]
		if {$rest!=""} {
		    set cand [concat $p1 [list --] $rest]
		    #puts "adding candidate:$cand"
		    lappend candidates $cand
		}
	    }
	}
    }
    #     puts cand:[join $candidates ,]([llength $candidates])
    if {[llength $candidates]==0} {
	return ""
    } else {
	# return shortest candidate
	set res [lindex $candidates 0]
	foreach c [lrange $candidates 1 end] {
	    if {[llength $c]<[llength $res]} {set res $c}
	}
	return $res
    }
    error "not supposed to get here"
}


proc gensyllex {lexvar file} {
    upvar $lexvar lex
    set f [open $file]
    set data [split [string trim [read $f]] \n]
    close $f

    foreach line $data {
	foreach {wrd phn} [split $line \t] break
	foreach syl [split $phn .,] {
	    regsub -all _1 $syl "" syl
	    regsub -all _2 $syl "" syl
	    regsub -all _3 $syl "" syl
	    
	    set syl [string trim $syl]
	    set lex($syl) 1
	   # puts $syl
	}
    }
    puts "[llength [array names lex]] lexicon entries"
}

proc readsyllex {lexvar file} {
    upvar $lexvar lex

    set f [open $file]
    set data [split [string trim [read $f]] \n]
    close $f

    foreach line $data {
	set lex([string trim $line]) 1
    }
}

proc writesyllex {lexvar file} {
    upvar $lexvar lex
    
    set f [open $file w]

    foreach key [lsort -dictionary [array names lex]] {
	puts $f $key
    }
    close $f
}
