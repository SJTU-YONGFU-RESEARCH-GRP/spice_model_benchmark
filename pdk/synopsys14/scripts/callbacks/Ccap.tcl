

proc getCurrentInstance_C {} {
	return [db::getCurrentRef]
}

proc getCurrentParam_C {} {
	return [db::getCurrentParam]
}


proc getCurrentParamValue_C {param_name} {
	return [db::getParamValue $param_name -of [getCurrentInstance_C]]
}

proc setInstanceParamValue_C { param value inst} {
	db::setParamValue $param -value "${value}" -of $inst -evalCallbacks 0
}

proc is_digit_C {param_name param_val} {
	set value [regsub -all {[^\.0-9]} $param_val ""]
	if {$value == ""} {
	  set value [check_for_min_or_max_C "$param_name" 0]
	}
	return $value
}

proc to_user {value} {
	set value [db::sciToEng $value]

	if {[regexp {\d+k} $value]} {
		return [expr [lindex [split [db::sciToEng $value] "k"] 0] * pow(10, 3)] 
	} elseif {[regexp {\d+M} $value]} {
		return [expr [lindex [split [db::sciToEng $value] "M"] 0] * pow(10, 6)] 
	} elseif {[regexp {\d+G} $value]} {
		return [expr [lindex [split [db::sciToEng $value] "G"] 0] * pow(10, 9)] 
	} elseif {[regexp {\d+T} $value]} {
		return [expr [lindex [split [db::sciToEng $value] "T"] 0] * pow(10, 12)] 
	} elseif {[regexp {\d+P} $value]} {
		return [expr [lindex [split [db::sciToEng $value] "P"] 0] * pow(10, 15)] 
	} elseif {[regexp {\d+E} $value]} {
		return [expr [lindex [split [db::sciToEng $value] "E"] 0] * pow(10, 18)] 
	} elseif {[regexp {\d+Z} $value]} {
		return [expr [lindex [split [db::sciToEng $value] "Z"] 0] * pow(10, 21)] 
	} elseif {[regexp {\d+Y} $value]} {
		return [expr [lindex [split [db::sciToEng $value] "Y"] 0] * pow(10, 24)] 
	} elseif {[regexp {\d+m} $value]} {
		return [expr [lindex [split [db::sciToEng $value] "m"] 0] * pow(10, -3)] 
	} elseif {[regexp {\d+u} $value]} {
		return [expr [lindex [split [db::sciToEng $value] "u"] 0] * pow(10, 0)] 
	} elseif {[regexp {\d+n} $value]} {
		return [expr [lindex [split [db::sciToEng $value] "n"] 0] * pow(10, -9)] 
	} elseif {[regexp {\d+p} $value]} {
		return [expr [lindex [split [db::sciToEng $value] "p"] 0] * pow(10, -12)] 
	} elseif {[regexp {\d+f} $value]} {
		return [expr [lindex [split [db::sciToEng $value] "f"] 0] * pow(10, -15)] 
	} elseif {[regexp {\d+a} $value]} {
		return [expr [lindex [split [db::sciToEng $value] "a"] 0] * pow(10, -18)] 
	} elseif {[regexp {\d+z} $value]} {
		return [expr [lindex [split [db::sciToEng $value] "z"] 0] * pow(10, -21)] 
	} elseif {[regexp {\d+y} $value]} {
		return [expr [lindex [split [db::sciToEng $value] "y"] 0] * pow(10, -24)] 
	} else {
		return $value
	}
}

proc set_Limits_C {} {
	set limit 20
	return [list \
		[list min_sm max_sm min_em max_em min_m max_m   min_w max_w min_l max_l min_nf max_nf ] \
		[list    1      5     1      50     1   $limit   0.28  2     0.45    2     1   $limit ] \
	]
}

proc getLimitsValueByName_C { value_name } {
	set names  [lindex [set_Limits_C] 0]
	set values [lindex [set_Limits_C] 1]
	
	for {set i 0} {$i < [llength $values]} {incr i} {
		if {[lindex $names $i] == $value_name} {
			return [lindex $values $i]
		}
	}
}

proc check_for_min_or_max_C {param_name param_value} {
	set max_value [getLimitsValueByName_C "max_${param_name}"]
	set min_value [getLimitsValueByName_C "min_${param_name}"]
	
	if {$param_value > $max_value} {
		puts "WARNING 0009> The value of \"${param_name}\" [db::sciToEng ${param_value}] > ${max_value} max value..."
		puts "\t\tResetting \"${param_name}\"  to max value."
		
		setInstanceParamValue_Rndiff_resource "${param_name}" $max_value [getCurrentInstance_Rndiff_resource]
		
		return $max_value
	} elseif {$param_value < $min_value} {
		puts "WARNING 0009> The value of \"${param_name}\" [db::sciToEng ${param_value}] < ${min_value} min value..."
		puts "\t\tResetting \"${param_name}\"  to min value."
		
		setInstanceParamValue_Rndiff_resource "${param_name}" $min_value [getCurrentInstance_Rndiff_resource]
		
		return $min_value
	} else {
		return $param_value
	}
}

proc Ccap14 {} { 
	set m  		[to_user [check_for_min_or_max_C "m" [getCurrentParamValue_C "m"]]]
	set nf  	[to_user [check_for_min_or_max_C "nf" [getCurrentParamValue_C "nf"]]]
	set l  		[is_digit_C "l" [to_user [check_for_min_or_max_C "l" [is_digit_C "l" [getCurrentParamValue_C "l"]]]]]
	setInstanceParamValue_C "l" [db::sciToEng $l] [getCurrentInstance_C]
	set w  		[is_digit_C "w" [to_user [check_for_min_or_max_C "w" [is_digit_C "w" [getCurrentParamValue_C "w"]]]]]
	setInstanceParamValue_C "w" [db::sciToEng $w] [getCurrentInstance_C]
	set startmetal  [check_for_min_or_max_C "sm" [getCurrentParamValue_C "startmetal"]]
	set endmetal    [check_for_min_or_max_C "em" [getCurrentParamValue_C "endmetal"]]
	
	set Cf 0.114e-17
	set Ca 3.83e-17
	
	set layers [expr $endmetal - $startmetal]

	set l     [expr $l + 0.3]
	set perim [expr 2*($l+$w)]
	set area  [expr $l*$w]
	 
	set cval [expr $layers * $nf * ($Ca*$area + $Cf*$perim*2.8e-7 )]

	
#	set perim [expr 2*$l+$nf*$w]
#	set area  [expr $nf*$l*$w]	
	
#	set cval [expr $Ca*$area + $Cf*$perim*2.8e-7]
	
	setInstanceParamValue_C "cval" [db::sciToEng $cval] [getCurrentInstance_C]
	
}
