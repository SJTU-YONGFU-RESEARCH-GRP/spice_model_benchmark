proc getCurrentInstance_VNPN {} {
	return [db::getCurrentRef]
}

proc getCurrentParam_VNPN {} {
	return [is_digit_VNPN [db::getCurrentParam]]
}

proc getCurrentParamValue_VNPN {param_name} {
	return [is_digit_VNPN [db::getParamValue $param_name -of [getCurrentInstance_VNPN]]]
}

proc getLayers_VNPN {} {
	return [list\
		NWELL  DNW DIFF PIMP NIMP DIFF_18 PAD ESD_25 SBLK PO\
		M1 VIA1 M2 VIA2 M3 VIA3 M4 VIA4 M5 VIA5 M6 VIA6 M7 VIA7 M8 VIA8 M9 CO HVTIMP LVTIMP\
		M1PIN M2PIN M3PIN M4PIN M5PIN M6PIN M7PIN M8PIN M9PIN MRDL VIARDL MRPIN DIOD BJTMY RNW\
		RMARK LOGO IP PrBoundary RM1 RM2 RM3 RM4 RM5 RM6 RM7 RM8 RM9 DM1EXCL DM2EXCL\
		DM3EXCL DM4EXCL DM5EXCL DM6EXCL DM7EXCL DM8EXCL DM9EXCL POEXCL \

	]
}

proc is_digit_VNPN {param_name param_val} {
	set value [regsub -all {[^\.0-9]} $param_val ""]
	if {$value == ""} {
	  set value [check_for_min_or_max_VNPN "$param_name" 0]
	}
	return $value
}
proc getLayerPosition_VNPN {layer} {
	return [lsearch -exact [getLayers_VNPN] "$layer"]
}

proc set_Limits_VNPN {} {
	return [list [list min_fr max_fr min_rw max_rw min_m] [list 1 50 1 50 1] ]
}

proc getLimitsValueByName_VNPN { value_name } {
	set names  [lindex [set_Limits_VNPN] 0]
	set values [lindex [set_Limits_VNPN] 1]
	
	for {set i 0} {$i < [llength $values]} {incr i} {
		if {[lindex $names $i] == $value_name} {
			return [lindex $values $i]
		}
	}
}

proc isLayer_VNPN {layer} {
	set layers [getLayers_VNPN]
	set result 0
	foreach key $layers {
		if {$key == $layer} {
			set result 1
		}
	}
	return $result
}

proc is_variable_VNPN { paramValue } {

    if { [regexp {([i][n][s][t])|([p][a][r][e][n][t])|([l][i][n][e][a][g][e])|([P][a][r])} $paramValue match] } {
        return 1
    } elseif { [regexp {(^\[+)}  $paramValue ] } {
        return 1
    } elseif { [regexp {(^[a-zA-Z]+$)|(^[a-zA-Z]+)} $paramValue ]} {
        if { [regexp {(^[a-zA-Z]+)((\*+)|(\/+)|(\-+)|(\++) \
          |(\%+))(([a-zA-Z]+$)|([0-9]+$))} $paramValue ] && ![regexp {(\@+)|(\^+)|(\&+)|(\(+)|(\)+)|(\|+)|(\{+)|(\}+)|(\<+) \
          |(\>+)|(\?+)|(\:+)|(\;+)|(\"+)|(\'+)|(\=+)|(\`+)|(\~+)|(\,+)} $paramValue ]} {
            return 1

         } elseif { [regexp {(^[a-zA-Z]+$)|(^[a-zA-Z]+)} $paramValue ] && ![regexp {(\@+)|(\^+)|(\&+)|(\(+)|(\)+)|(\|+)|(\{+)|(\}+)| \
             (\<+)|(\>+)|(\?+)|(\:+)|(\;+)|(\"+)|(\'+)|(\=+)|(\`+)|(\~+)|(\,+)} $paramValue ]} {
             return 1

         } else {
            
            # input error
             return 2

         }

    # if input begins with a number
    } elseif { ([regexp {(^[0-9]+$)|(^[0-9]+\.[0-9]+$)|(^\.[0-9]+$)} $paramValue ] \
       || [regexp {((^[0-9]+)|(^[0-9]+\.[0-9]+)|(^\.[0-9]+))([a-zA-Z]+$)} $paramValue ] \
       || [regexp {((^[0-9]+)|(^[0-9]+\.[0-9]+)|(^\.[0-9]+))(([a-zA-Z]+)|(\++)|(\!+)| \
        (\#+)|(\$+)|(\%+)|(\[+)|(\]+)|(\_+)|(\/+)|(\*+)|(\-+))} $paramValue ]) && ![regexp { } $paramValue] } {

        if { [regexp {(^[0-9]+)|(^[0-9]+\.[0-9]+)|(^\.[0-9]+)} $paramValue match] } {
            if { [regexp {(^[0-9]+$)|(^[0-9]+\.[0-9]+$)|(^\.[0-9]+$)} $paramValue ] } {
                return 0
            } else {
                  
                  set sample_value [string trimleft $paramValue $match]
                  if {[regexp {^([y]|[z]|[a]|[f]|[p]|[n]|[u]|[m]|[c]|[k]|[M]|(^[m][e][g])|[X]|[G]|[T]|[P]|[E]|[Z]|[Y])$} $sample_value] \
                  && ![regexp {[0-9]$} $sample_value ]} {
                      return 0
 
                  } elseif {[regexp {(^[eE][0-9]+$)|(^[eE]([\-]|[\+])[0-9]+$)} $sample_value check ] || [regexp {(^[0-9]+$)|(^[0-9]+\.[0-9]+$)} \
                    $sample_value check ]} {
                      return 0
              
                  } elseif { [regexp {((\*+)|(\/+)|(\-+)|(\++)|(\%+))(([a-zA-Z]+)|([0-9]+))} $sample_value ] \
                    || [regexp {([a-zA-Z]+)((\*+)|(\/+)|(\-+)|(\++)|(\%+))(([a-zA-Z]+$)|([0-9]+$))} $sample_value ] \
                    && ![regexp {(\@+)|(\^+)|(\&+)|(\(+)|(\)+)|(\|+)|(\{+)|(\}+)|(\<+)|(\>+)|(\?+)|(\:+)|(\;+)| \
                    (\"+)|(\'+)|(\=+)|(\`+)|(\~+)|(\,+)} $sample_value ] } {
                      return 1

                  } elseif { [regexp {(\@+)|(\^+)|(\&+)|(\(+)|(\)+)|(\|+)|(\{+)|(\}+)|(\<+)|(\>+)|(\?+)|(\:+) \
                    |(\;+)|(\"+)|(\'+)|(\=+)|(\`+)|(\~+)|(\,+)} $sample_value ]} {   
                     # input error
                      return 2

                  } else {
                      # input error
                      return 2

                  }
              }
        }
        
    } else {
        return 3

    }

}

proc setInstanceParamValue_VNPN { param value inst} {
	set formval [db::getParamValue $param -of $inst]
	
	# param is a variable
	if { [is_variable_VNPN $formval] || [is_variable_VNPN $value] } {
		set old_val $formval
		set new_val $value
		if { [string compare $old_val $new_val] != 0 } {
			db::setParamValue $param -value $value -of $inst -evalCallbacks 0
		}
	# param is NOT a variable
	} else {
		set old_val [db::engToSci $formval]
		set new_val [db::engToSci $value]
		if { [expr $old_val] != [expr $new_val] } {
			db::setParamValue $param -value $value -of $inst -evalCallbacks 0
		}
	}
}

proc VNPN14 {} { 
	set emitterSize [getCurrentParamValue_VNPN "emitterSize"]
	set area        [is_digit_VNPN [getCurrentParamValue_VNPN "area"]]
	set m           [is_digit_VNPN [getCurrentParamValue_VNPN "m"]]
	set rw          [is_digit_VNPN [getCurrentParamValue_VNPN "rw"]]
	set fr          [is_digit_VNPN [getCurrentParamValue_VNPN "fr"]]
	set ruleset     [is_digit_VNPN [getCurrentParamValue_VNPN "ruleset"]]
	
	set edited_param [getCurrentParam_VNPN]
	
	if {$edited_param == "emitterSize"} {
		if {$emitterSize == "2x2"} {
			setInstanceParamValue_VNPN ${edited_param} ${emitterSize} [getCurrentInstance_VNPN]
			setInstanceParamValue_VNPN "area" 4 [getCurrentInstance_VNPN]
		} elseif {$emitterSize == "5x5"} {
			setInstanceParamValue_VNPN ${edited_param} ${emitterSize} [getCurrentInstance_VNPN]
			setInstanceParamValue_VNPN "area" 25 [getCurrentInstance_VNPN]
		} elseif {$emitterSize == "10x10"} {
			setInstanceParamValue_VNPN ${edited_param} ${emitterSize} [getCurrentInstance_VNPN]
			setInstanceParamValue_VNPN "area" 100 [getCurrentInstance_VNPN]
		}
	} elseif {$edited_param == "rw"} {
		set max_value_of_rw [getLimitsValueByName_VNPN "max_${edited_param}"]
		set min_value_of_rw [getLimitsValueByName_VNPN "min_${edited_param}"]
		
		if {$rw > $max_value_of_rw} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${rw}\" > ${max_value_of_rw} max value..."
			puts "\t\tResetting \"${edited_param}\"  to max value."
			
			setInstanceParamValue_VNPN "${edited_param}" $max_value_of_rw [getCurrentInstance_VNPN]
			
		} elseif {$rw < $min_value_of_rw} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${rw}\" < ${min_value_of_rw} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			
			setInstanceParamValue_VNPN "${edited_param}" $min_value_of_rw [getCurrentInstance_VNPN]
			
		}
	} elseif {$edited_param == "fr"} {
		set max_value_of_fr [getLimitsValueByName_VNPN "max_${edited_param}"]
		set min_value_of_fr [getLimitsValueByName_VNPN "min_${edited_param}"]
		
		if {$fr > $max_value_of_fr} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${fr}\" > ${max_value_of_fr} max value..."
			puts "\t\tResetting \"${edited_param}\"  to max value."
			
			setInstanceParamValue_VNPN "${edited_param}" $max_value_of_fr [getCurrentInstance_VNPN]
			
		} elseif {$fr < $min_value_of_fr} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${fr}\" < ${min_value_of_fr} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			
			setInstanceParamValue_VNPN "${edited_param}" $min_value_of_fr [getCurrentInstance_VNPN]
			
		}
	} elseif {$edited_param == "m"} {
		set min_value_of_m [getLimitsValueByName_VNPN "min_${edited_param}"]
		
		if {$m < $min_value_of_m} {
			puts "WARNING 0009> The value of \"${edited_param}\" \"${m}\" < ${min_value_of_m} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			
			setInstanceParamValue_VNPN "${edited_param}" $min_value_of_m [getCurrentInstance_VNPN]
		}	
	} elseif {$edited_param == "ruleset"} {
		setInstanceParamValue_VNPN "${edited_param}" "construction" [getCurrentInstance_VNPN]
	}
}
