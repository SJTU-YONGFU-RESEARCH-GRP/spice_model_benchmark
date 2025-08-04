proc getCurrentInstance_BG {} {
	return [db::getCurrentRef]
}

proc getCurrentParam_BG {} {
	return [db::getCurrentParam]
}

proc getCurrentParamValue_BG {param_name} {
	return [db::getParamValue $param_name -of [getCurrentInstance_BG]]
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

proc set_Limits_BG {} {
	return [list [list min_we max_we min_he max_he] [list 2 50 2 50] ]
}

proc getLimitsValueByName_BG { value_name } {
	set names  [lindex [set_Limits_BG] 0]
	set values [lindex [set_Limits_BG] 1]
	
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

proc setInstanceParamValue_BG { param value inst} {
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


proc BandGap {} {



	set edited_param [getCurrentParam_BG]
	
	if {[IsLayoutEditor]} {
		set we [getCurrentParamValue "we"]
		set he [getCurrentParamValue "he"]
		set we [lindex [split [db::sciToEng $we] "u"] 0]
		set he [lindex [split [db::sciToEng $he] "u"] 0]
	} else {
		set we [getCurrentParamValue "we"]
		if {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $we] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $we]} {
			set we [lindex [split [db::sciToEng $we] "u"] 0]
		}
		set l [getCurrentParamValue "he"]
		if {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $he] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $he]}  {
			set he [lindex [split [db::sciToEng $he] "u"] 0]
		}
	}
	if {$edited_param == "we"} {
		set max_value_of_we [getLimitsValueByName_BG "max_${edited_param}"]
		set min_value_of_we [getLimitsValueByName_BG "min_${edited_param}"]
		
		if {$we > $max_value_of_we && ([regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $we] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $we])} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${we}\" > ${max_value_of_we} max value..."
			puts "\t\tResetting \"${edited_param}\"  to max value."
			
			setInstanceParamValue_BG "${edited_param}" $max_value_of_we [getCurrentInstance_BG]	
		} elseif {$we < $min_value_of_we && ([regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $we] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $we])} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${we}\" < ${min_value_of_we} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			
			setInstanceParamValue_BG "${edited_param}" $min_value_of_we [getCurrentInstance_BG]
		} elseif {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $we] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $we]} {
			setInstanceParamValue_BG "${edited_param}" $we [getCurrentInstance_BG]
		} else {
			setInstanceParamValue_BG "${edited_param}" $we [getCurrentInstance_BG]
		}
	} elseif {$edited_param == "he"} {
		set max_value_of_he [getLimitsValueByName_BG "max_${edited_param}"]
		set min_value_of_he [getLimitsValueByName_BG "min_${edited_param}"]
		
		if {$he > $max_value_of_he && ([regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $he] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $he])} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${he}\" > ${max_value_of_he} max value..."
			puts "\t\tResetting \"${edited_param}\"  to max value."
			
			setInstanceParamValue_BG "${edited_param}" $max_value_of_he [getCurrentInstance_BG]
		} elseif {$he < $min_value_of_he && ([regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $he] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $he])} {
		
			puts "WARNING 0009> The value of \"${edited_param}\" \"${he}\" < ${min_value_of_he} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			
			setInstanceParamValue_BG "${edited_param}" $min_value_of_he [getCurrentInstance_BG]
		} elseif {[regexp {^\d+\.\d+[kMGTPEZYmunpfay]?$} $he] || [regexp {^\d+[kMGTPEZYmunpfay]?$} $he]} {
			setInstanceParamValue_BG "${edited_param}" $he [getCurrentInstance_BG]
		} else {
			setInstanceParamValue_BG "${edited_param}" $l [getCurrentInstance_BG]
		}
	} 
}
