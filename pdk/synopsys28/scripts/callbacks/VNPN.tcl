proc getCurrentInstance_VNPN {} {
	return [db::getCurrentRef]
}

proc getCurrentParam_VNPN {} {
	return [db::getCurrentParam]
}

proc getCurrentParamValue_VNPN {param_name} {
	return [db::getParamValue $param_name -of [getCurrentInstance_VNPN]]
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

proc getLayerPosition_VNPN {layer} {
	return [lsearch -exact [getLayers_VNPN] "$layer"]
}

proc set_Limits_VNPN {} {
	return [list [list min_he max_he min_we max_we min_m] [list 1 200 1 200 1] ]
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
proc check_grid_VNPN {value grid} {
	set first [lindex [split $value "."] 0]
	set second [lindex [split $value "."] 1]
	
	if {$second == 0} {
		return $value
	} else {
		set temp [expr round($value/$grid)]
	}
	return [expr $temp*$grid]
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
		} elseif {[regexp {^\d+\.\d+$} $value] || [regexp {^\d+$} $value]} {
			db::setParamValue $param -value "${value}u" -of $inst -evalCallbacks 0
		} else {
			db::setParamValue $param -value "${value}" -of $inst -evalCallbacks 0			
		}	
	}
}

proc is_word {value} {
	if {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $value] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $value] || [regexp {^\d+e-?\d+} $value] } {
		return 0
	} elseif {[regexp {\{|\}|\[|\]|\`|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\_|\-|\+|\=|\||\"|\'|\/|\\|\,|\;|\<|\>| +|^$} $value] } {
		return 2
	} else {
		return 1
	}
}

proc get_Area_BJT {w l} {
	return [expr $l*$w]
}


proc to_user_BJT {value value_name} {
	if {[is_word $value] == 0} {
		if {[regexp {^\d+\.?\d+$} $value] && $value_name != "m"} {
			set value [append value "u"]
			set value [db::sciToEng $value]
			set return_value 0
		} else {
			set value [db::sciToEng $value]
			set return_value 0
		}
		if {[regexp {\d+k} $value]} {
			set return_value  [expr double([lindex [split [db::sciToEng $value] "k"] 0] * pow(10, 9))]
		} elseif {[regexp {\d+M} $value]} {
			set return_value  [expr double([lindex [split [db::sciToEng $value] "M"] 0] * pow(10, 12))]
		} elseif {[regexp {\d+G} $value]} {
			set return_value  [expr double([lindex [split [db::sciToEng $value] "G"] 0] * pow(10, 15))]
		} elseif {[regexp {\d+T} $value]} {
			set return_value  [expr double([lindex [split [db::sciToEng $value] "T"] 0] * pow(10, 18))]
		} elseif {[regexp {\d+P} $value]} {
			set return_value  [expr double([lindex [split [db::sciToEng $value] "P"] 0] * pow(10, 21))]
		} elseif {[regexp {\d+E} $value]} {
			set return_value  [expr double([lindex [split [db::sciToEng $value] "E"] 0] * pow(10, 24))]
		} elseif {[regexp {\d+Z} $value]} {
			set return_value  [expr double([lindex [split [db::sciToEng $value] "Z"] 0] * pow(10, 27))]
		} elseif {[regexp {\d+Y} $value]} {
			set return_value  [expr double([lindex [split [db::sciToEng $value] "Y"] 0] * pow(10, 30))]
		} elseif {[regexp {\d+m} $value]} {
			set return_value  [expr double([lindex [split [db::sciToEng $value] "m"] 0] * pow(10, 3))]
		} elseif {[regexp {\d+u} $value]} {
			set return_value  [expr double([lindex [split [db::sciToEng $value] "u"] 0] * pow(10, 0))]
		} elseif {[regexp {\d+n} $value]} {
			set return_value  [expr double([lindex [split [db::sciToEng $value] "n"] 0] * pow(10, -3))]
		} elseif {[regexp {\d+p} $value]} {
			set return_value  [expr double([lindex [split [db::sciToEng $value] "p"] 0] * pow(10, -6))]
		} elseif {[regexp {\d+f} $value]} {
			set return_value  [expr double([lindex [split [db::sciToEng $value] "f"] 0] * pow(10, -9))]
		} elseif {[regexp {\d+a} $value]} {
			set return_value  [expr double([lindex [split [db::sciToEng $value] "a"] 0] * pow(10, -12))]
		} elseif {[regexp {\d+z} $value]} {
			set return_value  [expr double([lindex [split [db::sciToEng $value] "z"] 0] * pow(10, -15))]
		} elseif {[regexp {\d+y} $value]} {
			set return_value  [expr double([lindex [split [db::sciToEng $value] "y"] 0] * pow(10, -18))]
		} else {
			set return_value $value
		}
		return $return_value
	} elseif { [is_word $value] == 2 } {
		puts "WARNING 0003> The value \"${value}\" is incorrect, type only letters or/and numbers" 
		puts "\t \t Reseting  \"$value_name\" to correct param value "
		set value "param"
		return $value
	} else {
		return $value
	}	
}



proc VNPN32 {} {
	set area        [getCurrentParamValue_VNPN "area"]
	set m           [getCurrentParamValue_VNPN "m"]
	set we          [to_user_BJT [getCurrentParamValue_VNPN "we"] "we"]
	set he          [to_user_BJT [getCurrentParamValue_VNPN "he"] "he"]
	set ruleset     [getCurrentParamValue_VNPN "ruleset"]
	set edited_param [getCurrentParam_VNPN]
	

	if {$edited_param == "we"} {
		if {![is_word $we]} {
			set max_value_of_we [getLimitsValueByName_VNPN "max_${edited_param}"]
			set min_value_of_we [getLimitsValueByName_VNPN "min_${edited_param}"]
		
			if {$we > $max_value_of_we && ([regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $we] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $we])} {
		
				puts "WARNING 0009> The value of \"${edited_param}\" \"${we}\" > ${max_value_of_we} max value..."
				puts "\t\tResetting \"${edited_param}\"  to max value."
				setInstanceParamValue_VNPN "${edited_param}" $max_value_of_we [getCurrentInstance_VNPN]
				set we $max_value_of_we 
				if {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $he] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $he]} {
					setInstanceParamValue_VNPN "area" [db::sciToEng [get_Area_BJT [expr $max_value_of_we*1e-6] [expr $he*1e-6]]] [getCurrentInstance_VNPN]
				}	

			} elseif {$we < $min_value_of_we && ([regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $we] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $we])} {
		
				puts "WARNING 0009> The value of \"${edited_param}\" \"${we}\" < ${min_value_of_we} min value..."
				puts "\t\tResetting \"${edited_param}\"  to min value."	
				setInstanceParamValue_VNPN "${edited_param}" $min_value_of_we [getCurrentInstance_VNPN]
				set we $min_value_of_we
				if {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $he] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $he]} {
					setInstanceParamValue_VNPN "area" [db::sciToEng [get_Area_BJT [expr $min_value_of_we*1e-6] [expr $he*1e-6]]] [getCurrentInstance_VNPN]
				}				
			} elseif {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $we] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $we]} {
				set we [check_grid_VNPN $we 0.001]
				setInstanceParamValue_VNPN "${edited_param}" $we [getCurrentInstance_VNPN]
				if {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $he] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $he]} {
					setInstanceParamValue_VNPN "area" [db::sciToEng [get_Area_BJT [expr $we*1e-6] [expr $he*1e-6]]] [getCurrentInstance_VNPN]
				}	
			} else {
				set we [check_grid_VNPN $we 0.001]
				setInstanceParamValue_VNPN "${edited_param}" $we [getCurrentInstance_VNPN]
			}
		} else {
			setInstanceParamValue_VNPN "${edited_param}" $we [getCurrentInstance_VNPN]
			setInstanceParamValue_VNPN "area" $area [getCurrentInstance_VNPN]
		}
	} elseif {$edited_param == "he"} {
		if {![is_word $he]} {
			set max_value_of_he [getLimitsValueByName_VNPN "max_${edited_param}"]
			set min_value_of_he [getLimitsValueByName_VNPN "min_${edited_param}"]
		
			if {$he > $max_value_of_he && ([regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $he] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $he])} {
		
				puts "WARNING 0009> The value of \"${edited_param}\" \"${he}\" > ${max_value_of_he} max value..."
				puts "\t\tResetting \"${edited_param}\"  to max value."
				setInstanceParamValue_VNPN "${edited_param}" $max_value_of_he [getCurrentInstance_VNPN]
				set he $max_value_of_he 
				if {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $we] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $we]} {
					setInstanceParamValue_VNPN "area" [db::sciToEng [get_Area_BJT [expr $max_value_of_he*1e-6] [expr $we*1e-6]]] [getCurrentInstance_VNPN]
				}
			} elseif {$he < $min_value_of_he} {		
				puts "WARNING 0009> The value of \"${edited_param}\" \"${he}\" < ${min_value_of_he} min value..."
				puts "\t\tResetting \"${edited_param}\"  to min value."			
				setInstanceParamValue_VNPN "${edited_param}" $min_value_of_he [getCurrentInstance_VNPN]			
				set he $min_value_of_he
				if {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $we] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $we]} {
					setInstanceParamValue_VNPN "area" [db::sciToEng [get_Area_BJT [expr $min_value_of_he*1e-6] [expr $we*1e-6]]] [getCurrentInstance_VNPN]
				}			
			} elseif {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $he] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $he]} {
				set he [check_grid_VNPN $he 0.001]
				setInstanceParamValue_VNPN "${edited_param}" $he [getCurrentInstance_VNPN]
				if {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $we] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $we]} {
					setInstanceParamValue_VNPN "area" [db::sciToEng [get_Area_BJT [expr $we*1e-6] [expr $he*1e-6]]] [getCurrentInstance_VNPN]
				}	
			} else {
				set he [check_grid_VNPN $he 0.001]
				setInstanceParamValue_VNPN "${edited_param}" $he [getCurrentInstance_VNPN]
			}
		} else {
			setInstanceParamValue_VNPN "${edited_param}" $he [getCurrentInstance_VNPN]
			setInstanceParamValue_VNPN "area" $area [getCurrentInstance_VNPN]
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
	#setInstanceParamValue_VNPN "we"    $we  [getCurrentInstance]
	
}
