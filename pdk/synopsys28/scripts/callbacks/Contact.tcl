proc getCurrentInstance_CONTACT {} {
	return [db::getCurrentRef]
}

proc getCurrentParam_CONTACT {} {
	return [db::getCurrentParam]
}

proc getCurrentParamValue_CONTACT {param_name} {
	return [db::getParamValue $param_name -of [getCurrentInstance_CONTACT]]
}

proc getLayers_CONTACT {} {
	return [list\
		NWELL  DNW DIFF PIMP NIMP DIFF_18 PAD ESD_25 SBLK PO\
		M1 VIA1 M2 VIA2 M3 VIA3 M4 VIA4 M5 VIA5 M6 VIA6 M7 VIA7 M8 VIA8 M9 CO HVTIMP LVTIMP\
		M1PIN M2PIN M3PIN M4PIN M5PIN M6PIN M7PIN M8PIN M9PIN MRDL VIARDL MRPIN DIOD BJTMY RNW\
		RMARK LOGO IP PrBoundary RM1 RM2 RM3 RM4 RM5 RM6 RM7 RM8 RM9 DM1EXCL DM2EXCL\
		DM3EXCL DM4EXCL DM5EXCL DM6EXCL DM7EXCL DM8EXCL DM9EXCL POEXCL \

	]
}

proc getLayerPosition_CONTACT {layer} {
	return [lsearch -exact [getLayers_CONTACT] "$layer"]
}

proc set_Limits_CONTACT {} {
	return [list [list min_width max_width min_height max_height] [list 0 100 0 100] ]
}

proc getLimitsValueByName_CONTACT { value_name } {
	set names  [lindex [set_Limits_CONTACT] 0]
	set values [lindex [set_Limits_CONTACT] 1]
	
	for {set i 0} {$i < [llength $values]} {incr i} {
		if {[lindex $names $i] == $value_name} {
			return [lindex $values $i]
		}
	}
}

proc isLayer_CONTACT {layer} {
	set layers [getLayers_CONTACT]
	set result 0
	foreach key $layers {
		if {$key == $layer} {
			set result 1
		}
	}
	return $result
}

proc is_variable_CONTACT { paramValue } {

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

proc setInstanceParamValue_CONTACT { param value inst} {
	set formval [db::getParamValue $param -of $inst]
	
	# param is a variable
	if { [is_variable_CONTACT $formval] || [is_variable_CONTACT $value] } {
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

proc Contact32 {} {
	set layer1             [getCurrentParamValue_CONTACT "layer1"]
	set layer2             [getCurrentParamValue_CONTACT "layer2"]
	set routeDir1          [getCurrentParamValue_CONTACT "routeDir1"]
	set routeDir2          [getCurrentParamValue_CONTACT "routeDir2"]
	set width              [getCurrentParamValue_CONTACT "width"]
	set height             [getCurrentParamValue_CONTACT "height"]
	set addLayers          [getCurrentParamValue_CONTACT "addLayers"]
	set ruleset            [getCurrentParamValue_CONTACT "ruleset"]
	set deviceContext      [getCurrentParamValue_CONTACT "deviceContext"]

	set edited_param [getCurrentParam_CONTACT]
	
	if {$edited_param == "layer1"} {
		if {[isLayer_CONTACT $layer1]} {
			set position_layer_1 [getLayerPosition_CONTACT $layer1]
			set position_layer_2 [getLayerPosition_CONTACT $layer2]
			
			if {$position_layer_1 < $position_layer_2} {
			} elseif {$position_layer_1 >= $position_layer_2} {
				puts "WARNING 0008> The value of \"layer1\" ${layer1} >\[=\] \"layer2\" ${layer2} value..."
				puts "\t\tResetting \"layer1\"  and \"layer2\" to default value."
				setInstanceParamValue_CONTACT "layer1" "DIFF" [getCurrentInstance_CONTACT]
				setInstanceParamValue_CONTACT "layer2" "M1"   [getCurrentInstance_CONTACT]
			}
		} else {
			puts "WARNING 0008> The value of \"layer1\" \"${layer1}\" is not a layer value..."
			puts "\t\tResetting \"layer1\"  to default value."
			setInstanceParamValue_CONTACT "layer1" "DIFF" [getCurrentInstance_CONTACT]
		}
	} elseif {$edited_param == "layer2"} {
		if {[isLayer_CONTACT $layer2]} {
			set position_layer_1 [getLayerPosition_CONTACT $layer1]
			set position_layer_2 [getLayerPosition_CONTACT $layer2]
			
			if {$position_layer_2 > $position_layer_1} {
			} elseif {$position_layer_2 <= $position_layer_1} {
				puts "WARNING 0008> The value of \"layer2\" ${layer2} <\[=\] \"layer1\" ${layer1} value..."
				puts "\t\tResetting \"layer1\"  and \"layer2\" to default value."
				setInstanceParamValue_CONTACT "layer1" "DIFF" [getCurrentInstance_CONTACT]
				setInstanceParamValue_CONTACT "layer2" "M1"   [getCurrentInstance_CONTACT]
			}
		} else {
			puts "WARNING 0008> The value of \"layer2\" \"${layer2}\" is not a layer value..."
			puts "\t\tResetting \"layer2\"  to default value."
			setInstanceParamValue_CONTACT "layer2" "M1" [getCurrentInstance_CONTACT]
		}
	} elseif {$edited_param == "width"} {
		set max_value_of_width [getLimitsValueByName_CONTACT "max_${edited_param}"]
		set min_value_of_width [getLimitsValueByName_CONTACT "min_${edited_param}"]
		if {$width > $max_value_of_width} {
			puts "WARNING 0009> The value of \"${edited_param}\" \"${width}\" >\[=\] ${max_value_of_width} max value..."
			puts "\t\tResetting \"${edited_param}\"  to max value."
			setInstanceParamValue_CONTACT "${edited_param}" $max_value_of_width [getCurrentInstance_CONTACT]
		} elseif {$width < $min_value_of_width} {
			puts "WARNING 0009> The value of \"width\" \"${width}\" <\[=\] ${min_value_of_width} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			setInstanceParamValue_CONTACT "${edited_param}" $min_value_of_width [getCurrentInstance_CONTACT]
		}
	} elseif {$edited_param == "height"} {
		set max_value_of_height [getLimitsValueByName_CONTACT "max_${edited_param}"]
		set min_value_of_height [getLimitsValueByName_CONTACT "min_${edited_param}"]
		if {$height > $max_value_of_height} {
			puts "WARNING 0010> The value of \"${edited_param}\" \"${height}\" >\[=\] ${max_value_of_height} max value..."
			puts "\t\tResetting \"${edited_param}\"  to max value."
			setInstanceParamValue_CONTACT "${edited_param}" $max_value_of_height [getCurrentInstance_CONTACT]
		} elseif {$height < $min_value_of_height} {
			puts "WARNING 0010> The value of \"${edited_param}\" \"${height}\" <\[=\] ${min_value_of_height} min value..."
			puts "\t\tResetting \"${edited_param}\"  to min value."
			setInstanceParamValue_CONTACT "${edited_param}" $min_value_of_height [getCurrentInstance_CONTACT]
		}
	} elseif {$edited_param == "addLayers"} {
		if {[isLayer_CONTACT $addLayers]} {
			
		} else {
			puts "WARNING 0011> The value of \"${edited_param}\" \"${addLayers}\" is not a layer..."
			puts "\t\tResetting \"${edited_param}\"  to default value."
			setInstanceParamValue_CONTACT "${edited_param}" "" [getCurrentInstance_CONTACT]
		}
	} elseif {$edited_param == "ruleset"} {
		setInstanceParamValue_CONTACT "${edited_param}" "default" [getCurrentInstance_CONTACT]
	} elseif {$edited_param == "deviceContext"} {
		setInstanceParamValue_CONTACT "${edited_param}" "" [getCurrentInstance_CONTACT]
	}
}
