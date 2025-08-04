proc getCurrentInstance_RESISTOR {} {
	return [db::getCurrentRef]
}

proc getCurrentParam_RESISTOR {} {
	return [db::getCurrentParam]
}

proc getCurrentParamValue_RESISTOR {param_name} {
	return [db::getParamValue $param_name -of [getCurrentInstance_RESISTOR]]
}

proc getLayers_RESISTOR {} {
	return [list\
		NWELL  DNW DIFF PIMP NIMP DIFF_25 PAD ESD_25 SBLK PO\
		M1 VIA1 M2 VIA2 M3 VIA3 M4 VIA4 M5 VIA5 M6 VIA6 M7 VIA7 M8 VIA8 M9 CO HVTIMP LVTIMP\
		M1PIN M2PIN M3PIN M4PIN M5PIN M6PIN M7PIN M8PIN M9PIN HOTNWL DIODMARK BJTMARK RNW\
		RPOLY RDIFF LOGO IP PrBoundary RM1 RM2 RM3 RM4 RM5 RM6 RM7 RM8 RM9 DM1EXCL DM2EXCL\
		DM3EXCL DM4EXCL DM5EXCL DM6EXCL DM7EXCL DM8EXCL DM9EXCL VARMARK CBMMARK INDMARK CTMMARK METDMY PWELL\
	]
}

proc getLayerPosition_RESISTOR {layer} {
	return [lsearch -exact [getLayers_RESISTOR] "$layer"]
}

proc set_Limits_RESISTOR {} {
	return [list [list min_width max_width min_length max_length min_contactLength max_contactLength] [list 0.39 100 0.39 100 0.39 100] ]
}

proc getLimitsValueByName_RESISTOR { value_name } {
	set names  [lindex [set_Limits_RESISTOR] 0]
	set values [lindex [set_Limits_RESISTOR] 1]
	
	for {set i 0} {$i < [llength $values]} {incr i} {
		if {[lindex $names $i] == $value_name} {
			return [lindex $values $i]
		}
	}
}

proc isLayer_RESISTOR {layer} {
	set layers [getLayers_RESISTOR]
	set result 0
	foreach key $layers {
		if {$key == $layer} {
			set result 1
		}
	}
	return $result
}

proc is_variable_RESISTOR { paramValue } {

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

proc setInstanceParamValue_RESISTOR { param value inst} {
	set formval [db::getParamValue $param -of $inst]
	
	if {[IsLayoutEditor]} {
		# param is a variable
		if { [is_variable_RESISTOR $formval] || [is_variable_RESISTOR $value] } {
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
		db::setParamValue $param -value "${value}u" -of $inst -evalCallbacks 0
	}
}

proc check_for_min_or_max_RESISTOR {param_name param_value} {
	set max_value [getLimitsValueByName_RESISTOR "max_${param_name}"]
	set min_value [getLimitsValueByName_RESISTOR "min_${param_name}"]
	
	if {$param_value > $max_value} {
		puts "WARNING 0009> The value of \"${param_name}\" \"${param_value}\" > ${max_value} max value..."
		puts "\t\tResetting \"${param_name}\"  to max value."
		
		setInstanceParamValue_RNDIFF "${param_name}" $max_value [getCurrentInstance_RNDIFF]
		
		return $max_value
	} elseif {$param_value < $min_value} {
		puts "WARNING 0009> The value of \"${param_name}\" \"${param_value}\" < ${min_value} min value..."
		puts "\t\tResetting \"${param_name}\"  to min value."
		
		setInstanceParamValue_RNDIFF "${param_name}" $min_value [getCurrentInstance_RNDIFF]
		
		return $min_value
	} else {
		return $param_value
	}
}

proc Resistor32 {} {
	
	set width  [lindex [split [db::sciToEng [getCurrentParamValue "width"]] "u"] 0]
	set length [lindex [split [db::sciToEng [getCurrentParamValue "length"]] "u"] 0]
	set contactLength [lindex [split [db::sciToEng [getCurrentParamValue "contactLength"]] "u"] 0]

	set width  [check_for_min_or_max_RESISTOR "width" [db::engToSci $width]]
	set length [check_for_min_or_max_RESISTOR "length" [db::engToSci $length]]
	set contactLength [check_for_min_or_max_RESISTOR "contactLength"  [db::engToSci $contactLength]]
	
	
	set edited_param [getCurrentParam_RESISTOR]
	
	if {$edited_param == "width"} {
		set max_value_of_width [getLimitsValueByName_RESISTOR "max_${edited_param}"]
		set min_value_of_width [getLimitsValueByName_RESISTOR "min_${edited_param}"]
		if {$width > $max_value_of_width} {
			puts "WARNING 0009> The value of \"${edited_param}\" \"${width}\" >\[=\] ${max_value_of_width} max value..."
			puts "\t\tResetting \"${edited_param}\"  to max value."
			setInstanceParamValue_RESISTOR "${edited_param}" $max_value_of_width [getCurrentInstance_RESISTOR]
		} elseif {$width < $min_value_of_width} {
			puts "WARNING 0009> The value of \"${edited_param}\" \"${width}\" <\[=\] ${min_value_of_width} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			setInstanceParamValue_RESISTOR "${edited_param}" $min_value_of_width [getCurrentInstance_RESISTOR]
		}
	} elseif {$edited_param == "length"} {
		set max_value_of_length [getLimitsValueByName_RESISTOR "max_${edited_param}"]
		set min_value_of_length [getLimitsValueByName_RESISTOR "min_${edited_param}"]
		if {$length > $max_value_of_length} {
			puts "WARNING 0010> The value of \"${edited_param}\" \"${length}\" >\[=\] ${max_value_of_length} max value..."
			puts "\t\tResetting \"${edited_param}\"  to max value."
			setInstanceParamValue_RESISTOR "${edited_param}" $max_value_of_length [getCurrentInstance_RESISTOR]
		} elseif {$length < $min_value_of_length} {
			puts "WARNING 0010> The value of \"${edited_param}\" \"${length}\" <\[=\] ${min_value_of_length} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			setInstanceParamValue_RESISTOR "${edited_param}" $min_value_of_length [getCurrentInstance_RESISTOR]
		}
	} elseif {$edited_param == "contactLength"} {
		set max_value_of_length_contact [getLimitsValueByName_RESISTOR "max_${edited_param}"]
		set min_value_of_length_contact [getLimitsValueByName_RESISTOR "min_${edited_param}"]
		if {$contactLength > $max_value_of_length_contact} {
			puts "WARNING 0010> The value of \"${edited_param}\" \"${contactLength}\" >\[=\] ${max_value_of_length_contact} max value..."
			puts "\t\tResetting \"${edited_param}\"  to max value."
			setInstanceParamValue_RESISTOR "${edited_param}" $max_value_of_length_contact [getCurrentInstance_RESISTOR]
		} elseif {$contactLength < $min_value_of_length_contact} {
			puts "WARNING 0010> The value of \"${edited_param}\" \"${contactLength}\" <\[=\] ${min_value_of_length_contact} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			setInstanceParamValue_RESISTOR "${edited_param}" $min_value_of_length_contact [getCurrentInstance_RESISTOR]
		}
	}
}
