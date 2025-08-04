proc getCurrentInstance_PD {} {
	return [db::getCurrentRef]
}

proc getCurrentParam_PD {} {
	return [db::getCurrentParam]
}

proc getCurrentParamValue_PD {param_name} {
	return [db::getParamValue $param_name -of [getCurrentInstance_PD]]
}

proc getLayers_PD {} {
	return [list\
		NWELL  DNW DIFF PIMP NIMP DIFF_25 PAD ESD_25 SBLK PO\
		M1 VIA1 M2 VIA2 M3 VIA3 M4 VIA4 M5 VIA5 M6 VIA6 M7 VIA7 M8 VIA8 M9 CO HVTIMP LVTIMP\
		M1PIN M2PIN M3PIN M4PIN M5PIN M6PIN M7PIN M8PIN M9PIN HOTNWL DIODMARK BJTMARK RNW\
		RPOLY RDIFF LOGO IP PrBoundary RM1 RM2 RM3 RM4 RM5 RM6 RM7 RM8 RM9 DM1EXCL DM2EXCL\
		DM3EXCL DM4EXCL DM5EXCL DM6EXCL DM7EXCL DM8EXCL DM9EXCL VARMARK CBMMARK IPDMARK CTMMARK METDMY PWELL\
	]
}

proc getLayerPosition_PD {layer} {
	return [lsearch -exact [getLayers_PD] "$layer"]
}

proc set_Limits_PD {} {
	return [list [list min_m min_w max_w min_l max_l] [list 1 0.23 50 0.23 50] ]
}

proc getLimitsValueByName_PD { value_name } {
	set names  [lindex [set_Limits_PD] 0]
	set values [lindex [set_Limits_PD] 1]
	
	for {set i 0} {$i < [llength $values]} {incr i} {
		if {[lindex $names $i] == $value_name} {
			return [lindex $values $i]
		}
	}
}

proc isLayer_PD {layer} {
	set layers [getLayers_PD]
	set result 0
	foreach key $layers {
		if {$key == $layer} {
			set result 1
		}
	}
	return $result
}

proc is_variable_PD { paramValue } {

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

proc setInstanceParamValue_PD { param value inst} {
	set formval [db::getParamValue $param -of $inst]
	
	if {[IsLayoutEditor]} {
		# param is a variable
		if { [is_variable_MOS $formval] || [is_variable_MOS $value] } {
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
	} else {
		if {$param == "area" || $param == "m"} {
			db::setParamValue $param -value "${value}" -of $inst -evalCallbacks 0
		} else {
			db::setParamValue $param -value "${value}u" -of $inst -evalCallbacks 0
		}
	}
}

proc get_Area_PD {w l} {
	return [expr $l*$w]
}

proc PD32 {} {
	set area    [getCurrentParamValue_ND "area"]
	set m       [getCurrentParamValue_ND "m"]
	
	if {[IsLayoutEditor]} {
		set w [getCurrentParamValue "w"]
		set l [getCurrentParamValue "l"]
	} else {
		set w [lindex [split [db::sciToEng [getCurrentParamValue "w"]] "u"] 0]
		set l [lindex [split [db::sciToEng [getCurrentParamValue "l"]] "u"] 0]
	}

		
	set edited_param [getCurrentParam_PD]
	
	if {$edited_param == "w"} {
		set max_value_of_w [getLimitsValueByName_PD "max_${edited_param}"]
		set min_value_of_w [getLimitsValueByName_PD "min_${edited_param}"]
		
		if {$w > $max_value_of_w} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${w}\" > ${max_value_of_w} max value..."
			puts "\t\tResetting \"${edited_param}\"  to max value."
			
			setInstanceParamValue_PD "${edited_param}" $max_value_of_w [getCurrentInstance_PD]
			setInstanceParamValue_PD "area" [db::sciToEng [get_Area_PD [expr $max_value_of_w*1e-6] [expr $l*1e-6]]] [getCurrentInstance_PD]
		} elseif {$w < $min_value_of_w} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${w}\" < ${min_value_of_w} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			
			setInstanceParamValue_PD "${edited_param}" $min_value_of_w [getCurrentInstance_PD]
			setInstanceParamValue_PD "area" [db::sciToEng [get_Area_PD [expr $min_value_of_w*1e-6] [expr $l*1e-6]]] [getCurrentInstance_PD]
		} else {
			setInstanceParamValue_PD "area" [db::sciToEng [get_Area_PD [expr $w*1e-6] [expr $l*1e-6]]] [getCurrentInstance_PD]
			setInstanceParamValue_ND "${edited_param}" $w [getCurrentInstance_ND]
		}
	} elseif {$edited_param == "l"} {
		set max_value_of_l [getLimitsValueByName_PD "max_${edited_param}"]
		set min_value_of_l [getLimitsValueByName_PD "min_${edited_param}"]
		
		if {$l > $max_value_of_l} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${l}\" > ${max_value_of_l} max value..."
			puts "\t\tResetting \"${edited_param}\"  to max value."
			
			setInstanceParamValue_PD "${edited_param}" $max_value_of_l [getCurrentInstance_PD]
			setInstanceParamValue_PD "area" [db::sciToEng [get_Area_PD [expr $w*1e-6] [expr $max_value_of_l*1e-6] ]] [getCurrentInstance_PD]
		} elseif {$l < $min_value_of_l} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${l}\" < ${min_value_of_l} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			
			setInstanceParamValue_PD "${edited_param}" $min_value_of_l [getCurrentInstance_PD]
			setInstanceParamValue_PD "area" [db::sciToEng [get_Area_PD [expr $w*1e-6] [expr $min_value_of_l*1e-6] ]] [getCurrentInstance_PD]
		} else {
			setInstanceParamValue_PD "area" [db::sciToEng [get_Area_PD [expr $w*1e-6] [expr $l*1e-6]]] [getCurrentInstance_PD]
			setInstanceParamValue_ND "${edited_param}" $l [getCurrentInstance_ND]
		}
	} elseif {$edited_param == "m"} {
	
		set min_value_of_m [getLimitsValueByName_PD "min_m"]
		
		if {$m < $min_value_of_m} {
			puts "WARNING 0009> The value of \"${edited_param}\" \"${m}\" < ${min_value_of_m} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			
			setInstanceParamValue_PD "${edited_param}" $min_value_of_m [getCurrentInstance_PD]
		}
	}
}