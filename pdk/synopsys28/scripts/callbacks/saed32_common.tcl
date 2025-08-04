
if [info exists limit] { unset limit }

proc metric_equal {a b} {
	set a  	[iPDK_engToSci $a]
	set b  	[iPDK_engToSci $b]	
	return [expr $a == $b]
}

proc console_log {{severity information} id message} {
	# de::sendMessage "This is an error message." -severity error
	# de::sendMessage "This is a warning message." -severity warning
	# de::sendMessage "This is an information message." -severity information
	set prefix "SAED 32/28 PDK"	
	de::sendMessage	"$prefix> $message (SAED32PDK-$id)" -severity $severity	
}

proc checkParameterValid {param value} {
	log "checkParameterValid $param $value"
	
	# 1 yes, 0 - no, 3 - error
	set is_variable [isVariable $value]
	
	if {$is_variable == 1 && [iPDK_isLayout] } {
		console_log warning 001 "Variables not allowed in layout mode."
		resetToDefault $param $value "not allowed in layout mode"
	} elseif {$is_variable == 2 } {
		resetToDefault $param $value
	} else {
		if {[catch {iPDK_engToSci $value}]} {
			resetToDefault $param $value
		}
	}
	
	return 
}

proc checkParameterLimits {device param value} {
	#log "checkParameterLimits $device $param $value"
	set max_value [iPDK_engToSci [getLimits $device $param max]]
	set min_value [iPDK_engToSci [getLimits $device $param min]]

	if {$value > $max_value} {		
		resetToMinMax $param $value $min_value $max_value  max
		return $max_value
	} elseif {$value < $min_value} {	
		resetToMinMax $param $value $min_value $max_value min
		return $min_value
	}
	
	return $value
}

proc checkMfGrid {param value grid} {
	set value 	  [iPDK_engToSci $value]
	set new_value [toMfGrid $value $grid]
	
	if {$new_value != $value} {	
			console_log warning 005 "Parameter \"$param\" with value \"[sciToU $value]\" is not multiply of [sciToU $grid ] grid. Resetting to nearest value \"[sciToU $new_value ]\"."
	} 
	return $new_value
}

proc sciToU {value} {
	return [db::sciToEng $value -suffix u ]
}

proc sciToInt {value} {
	return [expr int([db::engToSci $value ])]
}

proc toMfGrid {value grid} {
	set value 	[iPDK_engToSci $value]
	set grid  	[iPDK_engToSci $grid]
	
	set grids_in_value [expr double(round($value/$grid))]
	set new_value [iPDK_engToSci [expr $grids_in_value*$grid]]
	
	if {$new_value != $value} {	
		return $new_value
	} else {
		return $value
	}
	
}

proc resetToDefault {param incorrect_value {reason invalid}} {
		set inst  			[iPDK_getCurrentInst]
		set model 			[iPDK_getParamValue model $inst]
		set param_display 	[iPDK_getParamDef prompt $inst $param]
		set default_value 	[iPDK_getParamDef defValue $inst $param]
		
		if {[regexp {} $param_display]} { set param_display $param}
				
		set default_value [iPDK_sciToEng $default_value]
		
		console_log warning 003 "Parameter \"$param_display\" with value \"$incorrect_value\" is $reason. Resetting to default value \"$default_value\"."

	    iPDK_setParamValue $param  $default_value $inst 1
}
 
proc resetToMinMax {param incorrect_value min_value max_value {direction max}} {
		set inst  			[iPDK_getCurrentInst]
		set model 			[iPDK_getParamValue model $inst]
		set param_display 	[iPDK_getParamDef prompt $inst $param]
		
		if {[regexp {^\s*$} $param_display]} { set param_display $param}
		
		if {$direction == "min"} {
			set new_value $min_value
		} else {
			set new_value $max_value
		}
		
		set incorrect_value [iPDK_sciToEng $incorrect_value]
		set min_value [iPDK_sciToEng $min_value]
		set max_value [iPDK_sciToEng $max_value]
		set new_value [iPDK_sciToEng $new_value]
		
		console_log warning 004 "Value \"${incorrect_value}\" for parameter \"${param_display}\" is not in the allowable range \[${min_value}:${max_value}\]. Resetting \"${param_display}\" to $direction value \"$new_value\"."

	    iPDK_setParamValue $param  $new_value $inst 1
} 
 
 


proc setLimits {device param min max}  {
	global limits
	set limits($device,$param,min) $min
	set limits($device,$param,max) $max
}
 
proc getLimits {device param minmax}  {
	global limits
	return $limits($device,$param,$minmax) 
} 
 

proc log {string} {
	if 0 {
		puts $string
	}
}

proc isVariable { paramValue } {

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

proc get_param_def { attr inst param} {
    return [db::getAttr $attr -of [db::getParamDefs $param -of $inst]]
}

proc make_editable {controlParamName MODE} {
	set value     [db::getParamValue $controlParamName -of [db::getCurrentRef]]
	set paramType [get_param_def type [db::getCurrentRef] $controlParamName]
	
	if {$paramType == "boolean"} {
		if {$value} {
			return 1
		} else {
			return 0 
		}
	} else {
		if {[regexp $MODE $value]} {
			return 1
		} else {
			return 0  
		}
	}
}