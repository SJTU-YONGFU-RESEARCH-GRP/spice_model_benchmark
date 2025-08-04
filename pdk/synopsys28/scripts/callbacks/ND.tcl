proc getCurrentInstance_ND {} {
	return [db::getCurrentRef]
}

proc getCurrentParam_ND {} {
	return [db::getCurrentParam]
}

proc getCurrentParamValue_ND {param_name} {
	return [db::getParamValue $param_name -of [getCurrentInstance_ND]]
}

proc getLayers_ND {} {
	return [list\
		NWELL  DNW DIFF PIMP NIMP DIFF_18 PAD ESD_25 SBLK PO\
		M1 VIA1 M2 VIA2 M3 VIA3 M4 VIA4 M5 VIA5 M6 VIA6 M7 VIA7 M8 VIA8 M9 CO HVTIMP LVTIMP\
		M1PIN M2PIN M3PIN M4PIN M5PIN M6PIN M7PIN M8PIN M9PIN MRDL VIARDL MRPIN DIOD BJTMY RNW\
		RMARK LOGO IP PrBoundary RM1 RM2 RM3 RM4 RM5 RM6 RM7 RM8 RM9 DM1EXCL DM2EXCL\
		DM3EXCL DM4EXCL DM5EXCL DM6EXCL DM7EXCL DM8EXCL DM9EXCL POEXCL \

	]
}

proc getLayerPosition_ND {layer} {
	return [lsearch -exact [getLayers_ND] "$layer"]
}

proc check_grid_ND {value grid} {
	set first [lindex [split $value "."] 0]
	set second [lindex [split $value "."] 1]
	
	if {$second == 0} {
		return $value
	} else {
		set temp [expr round($value/$grid)]
	}
	return [expr $temp*$grid]
}


proc set_Limits_ND {} {
	return [list [list min_m min_w max_w min_l max_l] [list 1 0.3 50 0.3 50] ]
}

proc getLimitsValueByName_ND { value_name } {
	set names  [lindex [set_Limits_ND] 0]
	set values [lindex [set_Limits_ND] 1]
	
	for {set i 0} {$i < [llength $values]} {incr i} {
		if {[lindex $names $i] == $value_name} {
			return [lindex $values $i]
		}
	}
}

proc isLayer_ND {layer} {
	set layers [getLayers_ND]
	set result 0
	foreach key $layers {
		if {$key == $layer} {
			set result 1
		}
	}
	return $result
}

proc is_variable_ND { paramValue } {

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

proc IsLayoutEditor { } {
    set inst  [db::getCurrentRef]
    set viewType [oa::getName [oa::getViewType [oa::getDesign $inst]]]
    set viewName [oa::getViewName $inst] 
    if { $viewName == "layout" } {return 1} else {return 0}
}


proc setInstanceParamValue_ND { param value inst} {
	set formval [db::getParamValue $param -of $inst]
	if {[IsLayoutEditor]} {
		# param is a variable
		if { [is_variable_MOS $formval] || [is_variable_MOS $value] } {
			set old_val $formval
			set new_val $value
			if { [string compare $old_val $new_val] != 0 } {
				set value [lindex [split $value "u"] 0]
				db::setParamValue $param -value $new_val -of $inst -evalCallbacks 0
			}
		# param is NOT a variable
		} else {
			set old_val [db::engToSci $formval]
			set new_val [db::engToSci $value]
			if { [expr $old_val] != [expr $new_val] } {
				set value [lindex [split $value "u"] 0]				
				set new_val [db::sciToEng $new_val]
				db::setParamValue $param -value $new_val -of $inst -evalCallbacks 0
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


proc get_Area_ND {w l} {
	return [expr $l*$w]
}



proc to_user_ND {value value_name} {
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



proc ND32 {} {

	set area    [getCurrentParamValue_ND "area"]
	set m       [getCurrentParamValue_ND "m"]
	set edited_param [getCurrentParam_ND]	
	set w [to_user_ND [getCurrentParamValue "w"] "w"]
	set l [to_user_ND [getCurrentParamValue "l"] "l"]
	
	if {$edited_param == "w"} {
		if {![is_word $w]} {
			set max_value_of_w [getLimitsValueByName_ND "max_${edited_param}"]
			set min_value_of_w [getLimitsValueByName_ND "min_${edited_param}"]
			
			if {$w > $max_value_of_w && ([regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $w] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $w])} {
		
				puts "WARNING 0009> The value of \"${edited_param}\" \"${w}\" > ${max_value_of_w} max value..."
				puts "\t\tResetting \"${edited_param}\"  to max value."
				
				setInstanceParamValue_ND "${edited_param}" $max_value_of_w [getCurrentInstance_ND]
				if {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $l] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $l]} {
					setInstanceParamValue_ND "area" [db::sciToEng [get_Area_ND [expr $max_value_of_w*1e-6] [expr $l*1e-6]]] [getCurrentInstance_ND]
				}	
			} elseif {$w < $min_value_of_w && ([regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $w] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $w])} {
		
				puts "WARNING 0009> The value of \"${edited_param}\" \"${w}\" < ${min_value_of_w} min value..."
				puts "\t\tResetting \"${edited_param}\"  to min value."
				
				setInstanceParamValue_ND "${edited_param}" $min_value_of_w [getCurrentInstance_ND]
				if {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $l] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $l]} {
					setInstanceParamValue_ND "area" [db::sciToEng [get_Area_ND [expr $min_value_of_w*1e-6] [expr $l*1e-6]]] [getCurrentInstance_ND]
				}	
			} elseif {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $w] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $w]} {
				set w [check_grid_ND $w 0.001]
				setInstanceParamValue_ND "${edited_param}" $w [getCurrentInstance_ND]
				if {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $l] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $l]} {
					setInstanceParamValue_ND "area" [db::sciToEng [get_Area_ND [expr $w*1e-6] [expr $l*1e-6]]] [getCurrentInstance_ND]
				}	
			} else {
				set w [check_grid_ND $w 0.001]
				setInstanceParamValue_ND "${edited_param}" $w [getCurrentInstance_ND]
			}
		} else {
			setInstanceParamValue_ND "${edited_param}" $w [getCurrentInstance_ND]
			setInstanceParamValue_ND "area" $area [getCurrentInstance_ND]
		}	
	} elseif {$edited_param == "l"} {
		if {![is_word $l]} {
			set max_value_of_l [getLimitsValueByName_ND "max_${edited_param}"]
			set min_value_of_l [getLimitsValueByName_ND "min_${edited_param}"]
		
			if {$l > $max_value_of_l && ([regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $l] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $l])} {
		
				puts "WARNING 0009> The value of \"${edited_param}\" \"${l}\" > ${max_value_of_l} max value..."
				puts "\t\tResetting \"${edited_param}\"  to max value."
			
				setInstanceParamValue_ND "${edited_param}" $max_value_of_l [getCurrentInstance_ND]
				if {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $w] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $w]} {
					setInstanceParamValue_ND "area" [db::sciToEng [get_Area_ND [expr $w*1e-6] [expr $max_value_of_l*1e-6] ]] [getCurrentInstance_ND]
				}	
			} elseif {$l < $min_value_of_l && ([regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $l] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $l])} {
		
				puts "WARNING 0009> The value of \"${edited_param}\" \"${l}\" < ${min_value_of_l} min value..."
				puts "\t\tResetting \"${edited_param}\"  to min value."
			
				setInstanceParamValue_ND "${edited_param}" $min_value_of_l [getCurrentInstance_ND]
				if {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $w] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $w]} {
					setInstanceParamValue_ND "area" [db::sciToEng [get_Area_ND [expr $w*1e-6] [expr $min_value_of_l*1e-6] ]] [getCurrentInstance_ND]
				}	
			} elseif {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $l] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $l]} {
				set l [check_grid_ND $l 0.001]			
				setInstanceParamValue_ND "${edited_param}" $l [getCurrentInstance_ND]
				if {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $w] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $w]} {
					setInstanceParamValue_ND "area" [db::sciToEng [get_Area_ND [expr $w*1e-6] [expr $l*1e-6]]] [getCurrentInstance_ND]
				}
			} else {
				set l [check_grid_ND $l 0.001]
				setInstanceParamValue_ND "${edited_param}" $l [getCurrentInstance_ND]
			} 
		} else {
			setInstanceParamValue_ND "${edited_param}" $l [getCurrentInstance_ND]
			setInstanceParamValue_ND "area" $area [getCurrentInstance_ND]
		}		
	} elseif {$edited_param == "m"} {
	
		set min_value_of_m [getLimitsValueByName_ND "min_m"]
		
		if {$m < $min_value_of_m } {
			puts "WARNING 0009> The value of \"${edited_param}\" \"${m}\" < ${min_value_of_m} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			setInstanceParamValue_ND "${edited_param}" $min_value_of_m [getCurrentInstance_ND]
		}
	}
}
