#!/usr/bin/tclsh
if { [llength $argv] < 4 || [llength $argv] > 5 } {

	puts "Usage: <Input File> <Fill> <Output Fill> <Top cell> <Type>"
	return 0
}

set design  [lindex $argv 0]
set fill    [lindex $argv 1]
set output  [lindex $argv 2]
set topcell [lindex $argv 3]
set type    [lindex $argv 4]
	
	if { [string equal "gds" $type ] || [string equal "gdsii" $type ]} {
		set type "gds"

	} elseif { [string equal "oas" $type ]} {
		set type "oas"

	} else {
		puts "Type should be \"gds\" or \"gdsii\" or \"oas\""
		return 0
	}

set str_rpl [open "merge.setup" w ]
puts $str_rpl "FILE	$fill\nPRIME	$topcell\nSNAP	0\nPLACE_MIRROR	0\nPLACE_ANGLE 	0\nPLACE_MAG 	1.0\nPLACE_X	0.0\nPLACE_Y	0.0\nENDPLACES	\n\nFILE	$design\nPRIME 	$topcell\nSNAP  0\nPLACE_MIRROR 0\nPLACE_ANGLE  0\nPLACE_MAG   1.0\nPLACE_X    0.0\nPLACE_Y    0.0\nENDPLACES \n\nENDFILES"
close $str_rpl

if { ![string match "oas" $type] } {

	set a [catch { exec k2_viewer -batch qv_gdsmerge merge.setup temp.gds $topcell } res]
	file rename -force temp.gds $output

} else {
        set a [catch { exec k2_viewer -batch qv_oasismerge merge.setup temp.oas $topcell } res]
        file rename -force temp.oas $output

}



