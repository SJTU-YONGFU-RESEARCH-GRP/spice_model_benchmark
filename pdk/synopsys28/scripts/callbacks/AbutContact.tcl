proc getCurrentInstance {} {
	return [db::getCurrentRef]
}

proc getCurrentParam {} {
	return [db::getCurrentParam]
}

proc getCurrentParamValue {param_name} {
	return [db::getParamValue $param_name -of [getCurrentInstance]]
}

proc getLayers {} {
	return [list\
		NWELL  DNW DIFF PIMP NIMP DIFF_18 PAD ESD_25 SBLK PO\
		M1 VIA1 M2 VIA2 M3 VIA3 M4 VIA4 M5 VIA5 M6 VIA6 M7 VIA7 M8 VIA8 M9 CO HVTIMP LVTIMP\
		M1PIN M2PIN M3PIN M4PIN M5PIN M6PIN M7PIN M8PIN M9PIN MRDL VIARDL MRPIN DIOD BJTMY RNW\
		RMARK LOGO IP PrBoundary RM1 RM2 RM3 RM4 RM5 RM6 RM7 RM8 RM9 DM1EXCL DM2EXCL\
		DM3EXCL DM4EXCL DM5EXCL DM6EXCL DM7EXCL DM8EXCL DM9EXCL POEXCL \
	]
}

proc getLayerPosition {layer} {
	return [lsearch -exact [getLayers] "$layer"]
}

proc set_AbutContact_Limits {} {
	return [list [list min_width max_width min_height max_height] [list 0 100 0 100] ]
}

proc getLimitsValueByName_AC { value_name } {
	set names  [lindex [set_AbutContact_Limits] 0]
	set values [lindex [set_AbutContact_Limits] 1]
	
	for {set i 0} {$i < [llength $values]} {incr i} {
		if {[lindex $names $i] == $value_name} {
			return [lindex $values $i]
		}
	}
}

proc getDefaultValueForLayers_AC {layer_name} {
	if {$layer_name == "layer1"} {
		return "DIFF"
	} elseif {$layer_name == "layer2"} {
		return "M1"
	}
}

proc isLayer_AC {layer} {
	set layers [getLayers]
	set result 0
	
	foreach key $layers {
		if {$key == $layer} {
			set result 1
		}
	}
	
	return $result
}

proc is_variable_AC { paramValue } {

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

proc setInstanceParamValue { param value inst} {
	set formval [db::getParamValue $param -of $inst]
	
	# param is a variable
	if { [is_variable_AC $formval] || [is_variable_AC $value] } {
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

proc AbutContact32 {} {
	set layer1             [getCurrentParamValue "layer1"]
	set layer2             [getCurrentParamValue "layer2"]
	set routeDir1          [getCurrentParamValue "routeDir1"]
	set routeDir2          [getCurrentParamValue "routeDir2"]
	set width              [getCurrentParamValue "width"]
	set height             [getCurrentParamValue "height"]
	set addLayer           [getCurrentParamValue "addLayer"]
	set ruleset            [getCurrentParamValue "ruleset"]
	set deviceContext      [getCurrentParamValue "deviceContext"]
	set abutDir            [getCurrentParamValue "abutDir"]
	set abutViaSpaceFactor [getCurrentParamValue "abutViaSpaceFactor"]
	set symAddLayer        [getCurrentParamValue "symAddLayer"]
	
	set param_1 [getCurrentParam]
	
	if {$param_1 == "layer1" || $param_1== "layer2"} {
		if {$param_1 == "layer1"} {
			set param_2 "layer2"
			set value_layer_1 [getCurrentParamValue $param_1]
			set value_layer_2 [getCurrentParamValue $param_2]
		} else {
			set param_2 "layer1"
			set value_layer_1 [getCurrentParamValue $param_2]
			set value_layer_2 [getCurrentParamValue $param_1]
		}
		
		set is_layer_1 [isLayer_AC $value_layer_1]
		set is_layer_2 [isLayer_AC $value_layer_2]
		
		if {$is_layer_1 && $is_layer_2} {
			if {[getLayerPosition $value_layer_1] < [getLayerPosition $value_layer_2]} {
				setInstanceParamValue $param_1 [getCurrentParamValue $param_1] [getCurrentInstance]
			} elseif {[getLayerPosition $value_layer_1] > [getLayerPosition $value_layer_2]} {
				puts "WARNING 0003> The ${param_1} value $value_layer_1 > $value_layer_2 the ${param_2} value."
				puts "\t\tResetting ${param_1} and ${param_2} values to Default value."
				setInstanceParamValue $param_1 [getDefaultValueForLayers_AC $param_1] [getCurrentInstance]
				setInstanceParamValue $param_2 [getDefaultValueForLayers_AC $param_2] [getCurrentInstance]
			}
		} elseif {$is_layer_1 == 0} {
			puts "WARNING 0004> The value of ${param_1} \"[getCurrentParamValue $param_1]\" is not a layer..."
			puts "\t\tResetting ${param_1} and ${param_2} values to Default value."
			setInstanceParamValue $param_1 [getDefaultValueForLayers_AC $param_1] [getCurrentInstance]
			setInstanceParamValue $param_2 [getDefaultValueForLayers_AC $param_2] [getCurrentInstance]
		} elseif {$is_layer_2 == 0} {
			puts "WARNING 0004> The value of ${param_1} \"[getCurrentParamValue $param_1]\" is not a layer..."
			puts "\t\tResetting ${param_1} and ${param_2} values to Default value."
			setInstanceParamValue $param_1 [getDefaultValueForLayers_AC $param_1] [getCurrentInstance]
			setInstanceParamValue $param_2 [getDefaultValueForLayers_AC $param_2] [getCurrentInstance]
		}
	}
	
	if {$param_1 == "width"} {
		puts [getLimitsValueByName_AC "max_${param_1}"]
		
		if {$width < [getLimitsValueByName_AC "min_${param_1}"]} {
			set min [getLimitsValueByName_AC "min_${param_1}"]
			puts "WARNING 0005> The value of ${param_1} ${width} < ${min} min value..."
			puts "\t\tResetting ${param_1} value to min ${min} value."
			setInstanceParamValue $param_1 [getLimitsValueByName_AC "min_${param_1}"] [getCurrentInstance]
		} elseif {$width > [getLimitsValueByName_AC "max_${param_1}"]} {
			set max [getLimitsValueByName_AC "max_${param_1}"]
			puts "WARNING 0005> The value of ${param_1} ${width} > ${max} max value..."
			puts "\t\tResetting ${param_1} value to max ${max} value."
			setInstanceParamValue $param_1 [getLimitsValueByName_AC "max_${param_1}"] [getCurrentInstance]
		}
	}
	
	if {$param_1 == "height"} {
		puts [getLimitsValueByName_AC "max_${param_1}"]
		
		if {$height < [getLimitsValueByName_AC "min_${param_1}"]} {
			set min [getLimitsValueByName_AC "min_${param_1}"]
			puts "WARNING 0006> The value of ${param_1} ${width} < ${min} min value..."
			puts "\t\tResetting ${param_1} value to min ${min} value."
			setInstanceParamValue $param_1 [getLimitsValueByName_AC "min_${param_1}"] [getCurrentInstance]
		} elseif {$height > [getLimitsValueByName_AC "max_${param_1}"]} {
			set max [getLimitsValueByName_AC "max_${param_1}"]
			puts "WARNING 0006> The value of ${param_1} ${width} > ${max} max value..."
			puts "\t\tResetting ${param_1} value to max ${max} value."
			setInstanceParamValue $param_1 [getLimitsValueByName_AC "max_${param_1}"] [getCurrentInstance]
		}
	}
}
