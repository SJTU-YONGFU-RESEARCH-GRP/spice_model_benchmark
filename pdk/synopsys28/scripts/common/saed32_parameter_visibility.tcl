#########################################################################################
# SAED 32/28NM parameter visibility script						#
#											#
# Revision History:									#
# Rev.		date			what			who			#
# -------------------------------------------------------------------------------------	#	
# 1.0		10/07/2015		(First draft)		meruzha			#
#########################################################################################


set name_of_param gateContact
set value_of_param none 

set name_of_param1 connect
set value_of_param1 series 

proc show_cmos_param {} {
	global name_of_param
	global value_of_param
	
	set ipdk [iPDK_isLayout]
	set inst [iPDK_getCurrentInst]
	set name [iPDK_getParamValue $name_of_param $inst]
	
	if {$ipdk == 1} {
		if {$name == $value_of_param} {
			return 0 
		} else { 
			return 1 
		} 
	} else {
		return 0
	}
}

proc show_res_param {} {
	global name_of_param1
	global value_of_param1
	
	set ipdk [iPDK_isLayout]
	set inst [iPDK_getCurrentInst]
	set name [iPDK_getParamValue $name_of_param1 $inst]
	
	if {$ipdk == 1} {
	    if {$name == $value_of_param1} {
		return 0 
	    } else { 
		return 1 
	    } 
	} else {
	    return 0
	}
}
		
