#!/usr/bin/tclsh
if { [llength $argv] < 3 || [llength $argv] > 4 } {

        puts "Usage: <Input File> <Output Fill> <Top cell> <Type>"
        return 0
}

set design  [lindex $argv 0]
set output  [lindex $argv 1]
set topcell [lindex $argv 2]
set type    [lindex $argv 3]
if {[info exists env(PVS_TECHDIR_FILL)]} { 
   set incldir "$env(PVS_TECHDIR_FILL)/Include"
} else {
   set incldir "./"
}

        if { [string equal "gds" $type ] || [string equal "gdsii" $type ]} {
                set type "gds"
		set a [ catch { exec k2_viewer -batch qv_gdssize $design fillcell_n1 fillcell_p1 > qv_gdssize.log } res ]
		set f1 [ open qv_gdssize.log ]
		set lines [ read $f1 ]
                close $f1
		
		set lines [ split $lines "\n" ]
		file copy -force $design __$output
                foreach line $lines {

			if {[regexp {fillcell_n1} $line match ] } {
			set str_rpl [open "stream_replace.setup" w ]
			puts $str_rpl "INPUT_FILE __$output\nINPUT_TOPSTR $topcell\nHOLD_FILE $incldir/fillcell_n1.gds\nOUTPUT_FILE temp.gds\nfillcell_n1 fillcell_n1"
			close $str_rpl
			set a [catch { exec k2_viewer -batch qv_strmreplace stream_replace.setup | tee qv_strmreplace.log } res ]
			file rename -force temp.gds __$output 
			}

			if {[regexp {fillcell_p1} $line match ] } {
			set str_rpl [open "stream_replace.setup1" w ]
			puts $str_rpl "INPUT_FILE __$output\nINPUT_TOPSTR $topcell\nHOLD_FILE $incldir/fillcell_p1.gds\nOUTPUT_FILE temp.gds\nfillcell_p1 fillcell_p1"
			close $str_rpl
			set a [catch { exec k2_viewer -batch qv_strmreplace stream_replace.setup1 | tee qv_strmreplace1.log } res ]
			file rename -force temp.gds __$output 
			}
		}
		file rename -force __$output $output

        } elseif { [string equal "oas" $type ]} {
                set type "oas"
                set a [ catch { exec k2_viewer -batch qv_oasissize $design fillcell_n1 fillcell_p1 > qv_oasissize.log } res ]
                set f1 [ open qv_oasissize.log ]
                set lines [ read $f1 ]
                close $f1

                set lines [ split $lines "\n" ]
                file copy -force $design __$output
                foreach line $lines {

                        if {[regexp {fillcell_n1} $line match ] } {
                        set str_rpl [open "stream_replace.setup" w ]
                        puts $str_rpl "INPUT_FILE __$output\nINPUT_TOPSTR $topcell\nHOLD_FILE $incldir/fillcell_n1.oas\nOUTPUT_FILE temp.oas\nfillcell_n1 fillcell_n1"
                        close $str_rpl
                        set a [catch { exec k2_viewer -batch qv_oasisreplace stream_replace.setup | tee log } res ]
                        file rename -force temp.oas __$output
                        }

                        if {[regexp {fillcell_p1} $line match ] } {
                        set str_rpl [open "stream_replace.setup1" w ]
                        puts $str_rpl "INPUT_FILE __$output\nINPUT_TOPSTR $topcell\nHOLD_FILE $incldir/fillcell_p1.oas\nOUTPUT_FILE temp.oas\nfillcell_p1 fillcell_p1"
                        close $str_rpl
                        set a [catch { exec k2_viewer -batch qv_oasisreplace stream_replace.setup1 | tee log1 } res ]
                        file rename -force temp.oas __$output
                        }
		}
                file rename -force __$output $output


        } else {
                puts "Type should be \"gds\" or \"gdsii\" or \"oas\""
                return 0
        }

