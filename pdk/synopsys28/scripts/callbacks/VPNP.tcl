proc getCurrentInstance_VPNP {} {
	return [db::getCurrentRef]
}

proc getCurrentParam_VPNP {} {
	return [db::getCurrentParam]
}

proc getCurrentParamValue_VPNP {param_name} {
	return [db::getParamValue $param_name -of [getCurrentInstance_VPNP]]
}

proc getLayers_VPNP {} {
	return [list\
		NWELL  DNW DIFF PIMP NIMP DIFF_18 PAD ESD_25 SBLK PO\
		M1 VIA1 M2 VIA2 M3 VIA3 M4 VIA4 M5 VIA5 M6 VIA6 M7 VIA7 M8 VIA8 M9 CO HVTIMP LVTIMP\
		M1PIN M2PIN M3PIN M4PIN M5PIN M6PIN M7PIN M8PIN M9PIN MRDL VIARDL MRPIN DIOD BJTMY RNW\
		RMARK LOGO IP PrBoundary RM1 RM2 RM3 RM4 RM5 RM6 RM7 RM8 RM9 DM1EXCL DM2EXCL\
		DM3EXCL DM4EXCL DM5EXCL DM6EXCL DM7EXCL DM8EXCL DM9EXCL POEXCL \

	]
}

proc getLayerPosition_VPNP {layer} {
	return [lsearch -exact [getLayers_VPNP] "$layer"]
}

proc set_Limits_VPNP {} {
	return [list [list min_fr max_fr min_rw max_rw min_m] [list 1 50 1 50 1] ]
}

proc getLimitsValueByName_VPNP { value_name } {
	set names  [lindex [set_Limits_VPNP] 0]
	set values [lindex [set_Limits_VPNP] 1]
	
	for {set i 0} {$i < [llength $values]} {incr i} {
		if {[lindex $names $i] == $value_name} {
			return [lindex $values $i]
		}
	}
}

proc isLayer_VPNP {layer} {
	set layers [getLayers_VPNP]
	set result 0
	foreach key $layers {
		if {$key == $layer} {
			set result 1
		}
	}
	return $result
}

proc is_variable_VPNP { paramValue } {

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

proc setInstanceParamValue_VPNP { param value inst} {
	set formval [db::getParamValue $param -of $inst]
	
	# param is a variable
	if { [is_variable_VPNP $formval] || [is_variable_VPNP $value] } {
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

proc VPNP32 {} {
	set emitterSize [getCurrentParamValue_VPNP "emitterSize"]
	set area        [getCurrentParamValue_VPNP "area"]
	set m           [getCurrentParamValue_VPNP "m"]
	set rw          [getCurrentParamValue_VPNP "rw"]
	set fr          [getCurrentParamValue_VPNP "fr"]
	set ruleset     [getCurrentParamValue_VPNP "ruleset"]
	
	set edited_param [getCurrentParam_VPNP]
	
	if {$edited_param == "emitterSize"} {
		if {$emitterSize == "2x2"} {
			setInstanceParamValue_VPNP ${edited_param} ${emitterSize} [getCurrentInstance_VPNP]
			setInstanceParamValue_VPNP "area" 4 [getCurrentInstance_VPNP]
		} elseif {$emitterSize == "5x5"} {
			setInstanceParamValue_VPNP ${edited_param} ${emitterSize} [getCurrentInstance_VPNP]
			setInstanceParamValue_VPNP "area" 25 [getCurrentInstance_VPNP]
		} elseif {$emitterSize == "10x10"} {
			setInstanceParamValue_VPNP ${edited_param} ${emitterSize} [getCurrentInstance_VPNP]
			setInstanceParamValue_VPNP "area" 100 [getCurrentInstance_VPNP]
		}
	} elseif {$edited_param == "rw"} {
		set max_value_of_rw [getLimitsValueByName_VPNP "max_${edited_param}"]
		set min_value_of_rw [getLimitsValueByName_VPNP "min_${edited_param}"]
		
		if {$rw > $max_value_of_rw} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${rw}\" > ${max_value_of_rw} max value..."
			puts "\t\tResetting \"${edited_param}\"  to max value."
			
			setInstanceParamValue_VPNP "${edited_param}" $max_value_of_rw [getCurrentInstance_VPNP]
			
		} elseif {$rw < $min_value_of_rw} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${rw}\" < ${min_value_of_rw} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			
			setInstanceParamValue_VPNP "${edited_param}" $min_value_of_rw [getCurrentInstance_VPNP]
			
		}
	} elseif {$edited_param == "fr"} {
		set max_value_of_fr [getLimitsValueByName_VPNP "max_${edited_param}"]
		set min_value_of_fr [getLimitsValueByName_VPNP "min_${edited_param}"]
		
		if {$fr > $max_value_of_fr} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${fr}\" > ${max_value_of_fr} max value..."
			puts "\t\tResetting \"${edited_param}\"  to max value."
			
			setInstanceParamValue_VPNP "${edited_param}" $max_value_of_fr [getCurrentInstance_VPNP]
			
		} elseif {$fr < $min_value_of_fr} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${fr}\" < ${min_value_of_fr} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			
			setInstanceParamValue_VPNP "${edited_param}" $min_value_of_fr [getCurrentInstance_VPNP]
			
		}
	} elseif {$edited_param == "m"} {
		set min_value_of_m [getLimitsValueByName_VPNP "min_${edited_param}"]
		
		if {$m < $min_value_of_m} {
			puts "WARNING 0009> The value of \"${edited_param}\" \"${m}\" < ${min_value_of_m} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			
			setInstanceParamValue_VPNP "${edited_param}" $min_value_of_m [getCurrentInstance_VPNP]
		}	
	} elseif {$edited_param == "ruleset"} {
		setInstanceParamValue_VPNP "${edited_param}" "construction" [getCurrentInstance_VPNP]
	}
}
