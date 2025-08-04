proc getCurrentInstance_Mos {} {
	return [db::getCurrentRef]
}

proc getCurrentParam_Mos {} {
	return [db::getCurrentParam]
}

proc getCurrentParamValue_Mos {param_name} {
	return [db::getParamValue $param_name -of [getCurrentInstance_Mos]]
}

proc set_Limits_Mos {} {
	set limit 1000
	set limit_l 0.2
	set limit_w 0.5
	return [list \
		[list min_nfin max_nfin min_nf max_nf min_m max_m   min_l    max_l   min_area max_area min_w  max_w  ] \
		[list 	1       $limit     1   $limit   1   $limit  0.014   $limit_l    1     $limit   0.16   $limit_w] \
	]
}

proc getLimitsValueByName_Mos { value_name } {
	set names  [lindex [set_Limits_Mos] 0]
	set values [lindex [set_Limits_Mos] 1]
	
	for {set i 0} {$i < [llength $values]} {incr i} {
		if {[lindex $names $i] == $value_name} {
			return [lindex $values $i]
		}
	}
}

proc is_variable_Mos { paramValue } {

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
proc check_for_min_or_max_Mos {param_name param_value} {
	set max_value [getLimitsValueByName_Mos "max_${param_name}"]
	set min_value [getLimitsValueByName_Mos "min_${param_name}"]
	if {$param_value > $max_value} {
		puts "WARNING 0009> The value of \"${param_name}\" [db::sciToEng ${param_value}] > ${max_value} max value..."
		puts "\t\tResetting \"${param_name}\"  to max value."
		
		setInstanceParamValue_Mos "${param_name}" $max_value [getCurrentInstance_Mos]
		return $max_value
	} elseif {$param_value < $min_value} {
		puts "WARNING 0009> The value of \"${param_name}\" [db::sciToEng ${param_value}] < ${min_value} min value..."
		puts "\t\tResetting \"${param_name}\"  to min value."
		
		setInstanceParamValue_Mos "${param_name}" $min_value [getCurrentInstance_Mos]
		return $min_value
	} else {
		return $param_value
	}
}


proc is_digit_Mos {param_name param_val} {
	set value [regsub -all {[^\.0-9]} $param_val ""]
	if {$value == ""} {
	  set value [getLimitsValueByName_Mos "min_${param_name}"]
	}
	return $value
}


proc to_user_Mos {value} {
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

proc log_Mos {string} {
	if 0 {
		puts $string
	}
}

proc isVariable_Mos { paramValue } {

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

proc checkParameterValid_Mos {param value} {
	log "checkParameterValid_Mos $param $value"
	set value [is_digit_Mos "$param" $value]
	# 1 yes, 0 - no, 3 - error
	set is_variable_Mos [isVariable_Mos $value]
	
	if {$is_variable_Mos == 1 && [iPDK_isLayout] } {
		console_log warning 001 "Variables not allowed in layout mode."
		check_for_min_or_max_Mos $param $value "not allowed in layout mode"
	} elseif {$is_variable_Mos == 2 } {
		check_for_min_or_max_Mos $param $value
	} else {
		if {[catch {iPDK_engToSci $value}]} {
			check_for_min_or_max_Mos $param $value
		}
	}
	
	return 
}

proc IsLayoutEditor_Mos { } {
    set inst  [db::getCurrentRef]
    set viewType [oa::getName [oa::getViewType [oa::getDesign $inst]]]
    set viewName [oa::getViewName $inst] 
    if { $viewName == "layout" } {return 1} else {return 0}
}

proc setInstanceParamValue_Mos { param value inst} {
	set formval [db::getParamValue $param -of $inst]
	
	if {[IsLayoutEditor_Mos]} {
		# param is a variable
		if { [is_variable_Mos $formval] || [is_variable_Mos $value] } {
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
		if {$param == "wf" || $param == "l" || $param == "lf"} {
			db::setParamValue $param -value "${value}u" -of $inst -evalCallbacks 0
		} else {
			db::setParamValue $param -value "${value}" -of $inst -evalCallbacks 0
		}
	}
}


proc Mos14 {} {
	 
	set inst [getCurrentInstance_Mos]
	set pycell_metric_params [list diffContactLeftBottomOffset   diffContactLeftTopOffset      diffContactCenterTopOffset    				diffContactCenterBottomOffset 				 diffContactRightBottomOffset  diffContactRightTopOffset     			gateContactLeftOffset   gateContactRightOffset  cgSpacingAdd  leftDiffAdd   rightDiffAdd  ]
	set geometric_params [list w wtot]
	set integer_params [list nf nfin ]
	set float_params [list l ]
	set all_option_params [list model entryMode]
	set all_string_params [list guardRing guardRingVertical guardRingHorizontal ]
	set all_metric_params [concat $geometric_params $pycell_metric_params ]
	set all_numeric_params [concat $integer_params $float_params $all_metric_params $float_params ]
	set all_params [concat $all_option_params $all_numeric_params $all_string_params]
	foreach param $all_numeric_params {
		checkParameterValid_Mos $param [iPDK_getParamValue $param $inst] 
	} 
	foreach param $all_params {
		set value($param) [getCurrentParamValue_Mos $param]		
		set initial_value($param) [getCurrentParamValue_Mos $param]	
	}
	
	set l 	 [is_digit_Mos "l" [getCurrentParamValue_Mos "l"]]
	set l    [to_user_Mos [check_for_min_or_max_Mos "l" $l]]
	setInstanceParamValue_Mos "l"  $l  [getCurrentInstance_Mos]
	set w    [to_user_Mos [check_for_min_or_max_Mos "w" [is_digit_Mos "w" [getCurrentParamValue_Mos "w"]]]]
	setInstanceParamValue_Mos "w" $w [getCurrentInstance_Mos]
	set nfin [getCurrentParamValue_Mos "nfin"]
	set nf   [getCurrentParamValue_Mos "nf"]
	set m    [getCurrentParamValue_Mos "m"]
	set edited_param [getCurrentParam_Mos]
	if {$edited_param == "l"} {
			set l [check_for_min_or_max_Mos "l" $l]
	} elseif {$edited_param == "nfin"} {
			set nfin [check_for_min_or_max_Mos "nfin" $nfin]
	} elseif {$edited_param == "nf"} {
			set nf [check_for_min_or_max_Mos "nf" $nf]
	} elseif {$edited_param == "m"} {
			set m [check_for_min_or_max_Mos "m" $m]
	}	





	#set new variebles in mos 
	setInstanceParamValue_Mos "m" $m [getCurrentInstance_Mos]
	setInstanceParamValue_Mos "nf"  $nf  [getCurrentInstance_Mos]
	setInstanceParamValue_Mos "nfin" $nfin [getCurrentInstance_Mos]
	setInstanceParamValue_Mos "l"  $l  [getCurrentInstance_Mos]
	
}
