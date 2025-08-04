proc getCurrentInstance_GR {} {
	return [db::getCurrentRef]
}

proc getCurrentParam_GR {} {
	return [db::getCurrentParam]
}

proc getCurrentParamValue_GR {param_name} {
	return [db::getParamValue $param_name -of [getCurrentInstance_GR]]
}

proc set_Limits_GR {} {
	return [list [list min_width max_width min_height max_height] [list 0.044 50 0.044 50] ]
}

proc getLimitsValueByName_GR { value_name } {
	set names  [lindex [set_Limits_GR] 0]
	set values [lindex [set_Limits_GR] 1]
	
	for {set i 0} {$i < [llength $values]} {incr i} {
		if {[lindex $names $i] == $value_name} {
			return [lindex $values $i]
		}
	}
}

proc is_digit_GR {param_val} {
	set value [regsub -all {[^\.0-9]} $param_val "" ]
 	if {$value == "" || $value < 0.044} {
		set value 0.044
	} elseif {$value > 50} {
		set value 50
	}
	return $value
}

proc is_variable_GR { paramValue } {

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

proc setInstanceParamValue_GR { param value inst} {
	set formval [db::getParamValue $param -of $inst]
	
	if {[IsLayoutEditor]} {
		# param is a variable
		if { [is_variable_GR $formval] || [is_variable_GR $value] } {
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
				db::setParamValue $param -value $new_val -of $inst -evalCallbacks 0
			}
		}
	} else {
		 if {[regexp {^\d+\.\d+$} $value] || [regexp {^\d+$} $value]} {
			db::setParamValue $param -value "${value}u" -of $inst -evalCallbacks 0
		} else {
			db::setParamValue $param -value "${value}" -of $inst -evalCallbacks 0
		}	
	}
}


proc GuardRing14 {} {
	
	 
	set edited_param [getCurrentParam_GR]
	
	if {[IsLayoutEditor]} {
		set width  [is_digit_GR [getCurrentParamValue "width"]]
		setInstanceParamValue_GR "witdh" $width [getCurrentInstance_GR]
		set height [is_digit_GR [getCurrentParamValue "height"]]
		setInstanceParamValue_GR  "height" $height [getCurrentInstance_GR]
		set width  [lindex [split [db::sciToEng [is_digit_GR $width]] "u"] 0]
		set height [lindex [split [db::sciToEng [is_digit_GR $height]] "u"] 0]
	} else {
		set width [is_digit_GR [getCurrentParamValue "width"]]
		setInstanceParamValue_GR "width"  $width [getCurrentInstance_GR]
		if {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $width] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $width]} {
			set width [lindex [split [db::sciToEng $width] "u"] 0]
		}
		#set l [getCurrentParamValue "height"]
		if {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $height] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $height]}  {
			
	set height [lindex [split [db::sciToEng $height] "u"] 0]
		}
	}
	if {$edited_param == "width"} {
		set max_value_of_width [getLimitsValueByName_GR "max_${edited_param}"]
		set min_value_of_width [getLimitsValueByName_GR "min_${edited_param}"]
		
		if {$width > $max_value_of_width && ([regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $width] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $width])} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${width}\" > ${max_value_of_width} max value..."
			puts "\t\tResetting \"${edited_param}\"  to max value."
			$max_value_of_width
			setInstanceParamValue_GR "${edited_param}" $max_value_of_width [getCurrentInstance_GR]	
		} elseif {$width < $min_value_of_width && ([regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $width] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $width])} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${width}\" < ${min_value_of_width} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			
			setInstanceParamValue_GR "${edited_param}" $min_value_of_width [getCurrentInstance_GR]
		} elseif {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $width] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $width]} {
			setInstanceParamValue_GR "${edited_param}" $width [getCurrentInstance_GR]
		} else {
			setInstanceParamValue_GR "${edited_param}" $we [getCurrentInstance_GR]
		}
	} elseif {$edited_param == "height"} {
		set max_value_of_height [getLimitsValueByName_GR "max_${edited_param}"]
		set min_value_of_height [getLimitsValueByName_GR "min_${edited_param}"]
		
		if {$height > $max_value_of_height && ([regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $height] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $height])} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${height}\" > ${max_value_of_height} max value..."
			puts "\t\tResetting \"${edited_param}\"  to max value."
			
			setInstanceParamValue_GR "${edited_param}" $max_value_of_height [getCurrentInstance_GR]
		} elseif {$height < $min_value_of_height && ([regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $height] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $height])} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${height}\" < ${min_value_of_height} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			
			setInstanceParamValue_GR "${edited_param}" $min_value_of_height [getCurrentInstance_GR]
		} elseif {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $height] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $height]} {
			setInstanceParamValue_GR "${edited_param}" $height [getCurrentInstance_GR]
		} else {
			setInstanceParamValue_GR "${edited_param}" $l [getCurrentInstance_GR]
		}
	} elseif {$edited_param == "sides"} {
		set side [getCurrentParamValue_GR "sides"]
		set side_values [list "top" "bottom" "left" "right"]
		set new_side [split $side ","]
		set ind 0
		foreach i $side_values {
			foreach j $new_side {
				if {$i == $j} {
					incr ind
					break
				}
			}
		}
		if {$ind == [llength $new_side] && $ind <= 4 && $ind!=0} {
			setInstanceParamValue_GR "${edited_param}"  $side [getCurrentInstance_GR]
		} else {
			puts "WARNING 0020> Side paramater input error."
			puts "Side parameter is \"top, bottom, left, right\""
			puts "\t\tPlease enter any combination of above mentioned options, splited only by \",\"..."
			setInstanceParamValue_GR "sides"  "top,bottom,left,right" [getCurrentInstance_GR]
		}
	}

}
