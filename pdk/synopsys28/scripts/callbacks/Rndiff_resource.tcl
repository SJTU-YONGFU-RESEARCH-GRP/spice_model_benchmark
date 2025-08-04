proc getCurrentInstance_RNDIFF {} {
	return [db::getCurrentRef]
}

proc getCurrentParam_RNDIFF {} {
	return [db::getCurrentParam]
}

proc getCurrentParamValue_RNDIFF {param_name} {
	return [db::getParamValue $param_name -of [getCurrentInstance_RNDIFF]]
}

proc getLayers_RNDIFF {} {
	return [list\
		NWELL  DNW DIFF PIMP NIMP DIFF_25 PAD ESD_25 SBLK PO\
		M1 VIA1 M2 VIA2 M3 VIA3 M4 VIA4 M5 VIA5 M6 VIA6 M7 VIA7 M8 VIA8 M9 CO HVTIMP LVTIMP\
		M1PIN M2PIN M3PIN M4PIN M5PIN M6PIN M7PIN M8PIN M9PIN HOTNWL DIODMARK BJTMARK RNW\
		RPOLY RDIFF LOGO IP PrBoundary RM1 RM2 RM3 RM4 RM5 RM6 RM7 RM8 RM9 DM1EXCL DM2EXCL\
		DM3EXCL DM4EXCL DM5EXCL DM6EXCL DM7EXCL DM8EXCL DM9EXCL VARMARK CBMMARK IPDMARK CTMMARK METDMY PWELL\
	]
}

proc getLayerPosition_RNDIFF {layer} {
	return [lsearch -exact [getLayers_RNDIFF] "$layer"]
}

proc set_Limits_RNDIFF {} {
	set limit 300
	return [list \
		[list min_fr max_fr min_rw max_rw min_m max_m  min_r max_r  min_wbar max_wbar min_wf max_wf min_lf max_lf min_lcontact max_lcontact] \
		[list 1      50     1      50     1     $limit 0     1e100  0.28     $limit   0.39   $limit 0.87   $limit 0.39         $limit] \
	]
}

proc getLimitsValueByName_RNDIFF { value_name } {
	set names  [lindex [set_Limits_RNDIFF] 0]
	set values [lindex [set_Limits_RNDIFF] 1]
	
	for {set i 0} {$i < [llength $values]} {incr i} {
		if {[lindex $names $i] == $value_name} {
			return [lindex $values $i]
		}
	}
}

proc isLayer_RNDIFF {layer} {
	set layers [getLayers_RNDIFF]
	set result 0
	foreach key $layers {
		if {$key == $layer} {
			set result 1
		}
	}
	return $result
}

proc is_variable_RNDIFF { paramValue } {

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

proc setInstanceParamValue_RNDIFF { param value inst} {
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
		if {$param == "wf" || $param == "l" || $param == "lf"} {
			db::setParamValue $param -value "${value}u" -of $inst -evalCallbacks 0
		} else {
			db::setParamValue $param -value "${value}" -of $inst -evalCallbacks 0
		}
	}
}

proc get_param_def_RNDFF { attr inst param} {
    return [db::getAttr $attr -of [db::getParamDefs $param -of $inst]]
}

proc make_editable_RNDIFF {controlParamName MODE} {
	set value     [getCurrentParamValue_RNDIFF $controlParamName]
	set paramType [get_param_def_RNDFF type [getCurrentInstance_RNDIFF] $controlParamName]
	
	if {$paramType == "boolean"} {
		if {$value} {
			return 1
		} else {
			return 0 
		}
	} else {
		if { [regexp $MODE $value]} {
			return 1
		} else {
			return 0  
		} 
	}
}

proc check_for_min_or_max_RNDIFF {param_name param_value} {
	set max_value [getLimitsValueByName_RNDIFF "max_${param_name}"]
	set min_value [getLimitsValueByName_RNDIFF "min_${param_name}"]
	
	if {$param_value > $max_value} {
		puts "WARNING 0009> The value of \"${param_name}\" [db::sciToEng ${param_value}] > ${max_value} max value..."
		puts "\t\tResetting \"${param_name}\"  to max value."
		
		setInstanceParamValue_RNDIFF "${param_name}" $max_value [getCurrentInstance_RNDIFF]
		
		return $max_value
	} elseif {$param_value < $min_value} {
		puts "WARNING 0009> The value of \"${param_name}\" [db::sciToEng ${param_value}] < ${min_value} min value..."
		puts "\t\tResetting \"${param_name}\"  to min value."
		
		setInstanceParamValue_RNDIFF "${param_name}" $min_value [getCurrentInstance_RNDIFF]
		
		return $min_value
	} else {
		return $param_value
	}
}

proc check_grid_RNDIFF {value grid} {
	set first [lindex [split $value "."] 0]
	set second [lindex [split $value "."] 1]
	#puts "value = ${value}"
	if {$second == 0} {
		return $value
	} else {
		set temp [expr round(double($value)/double($grid))]
	}
	return [expr double($temp*$grid)]
}

proc get_sheet_resistance_RNDIFF {resistance_type} {
	if {$resistance_type == "rnpoly"} {
		return 700
	} elseif {$resistance_type == "rppoly"} {
		return 800
	} elseif {$resistance_type == "rndiff"} {
		return 25
	} elseif {$resistance_type == "rpdiff"} {
		return 40
	} elseif {$resistance_type == "rnpoly_wos"} {
		return 402.1
	} elseif {$resistance_type == "rppoly_wos"} {
		return 390.0
	}
}

proc get_rend_RNDIFF {resistance_type} {
	if {$resistance_type == "rnpoly"} {
		return [expr 0*1e-6]
	} elseif {$resistance_type == "rppoly"} {
		return [expr 0*1e-6]
	} elseif {$resistance_type == "rndiff"} {
		return [expr 0*1e-6]
	} elseif {$resistance_type == "rpdiff"} {
		return [expr 0*1e-6]
	} elseif {$resistance_type == "rnpoly_wos"} {
		return [expr 2.0*1e-6]
	} elseif {$resistance_type == "rppoly_wos"} {
		return [expr 3.0*1e-6]
	}
}

proc get_dl_RNDIFF {resistance_type} {
	if {$resistance_type == "rnpoly"} {
		return [expr 0*1e-6]
	} elseif {$resistance_type == "rppoly"} {
		return [expr 0*1e-6]
	} elseif {$resistance_type == "rndiff"} {
		return [expr 0*1e-6]
	} elseif {$resistance_type == "rpdiff"} {
		return [expr 0*1e-6]
	} elseif {$resistance_type == "rnpoly_wos"} {
		return [expr 0.04*1e-6]
	} elseif {$resistance_type == "rppoly_wos"} {
		return [expr 0.04*1e-6]
	}
}

proc get_dw_RNDIFF {resistance_type} {
	if {$resistance_type == "rnpoly"} {
		return [expr -0.02*1e-6]
	} elseif {$resistance_type == "rppoly"} {
		return [expr -0.03*1e-6]
	} elseif {$resistance_type == "rndiff"} {
		return [expr -0.01*1e-6]
	} elseif {$resistance_type == "rpdiff"} {
		return [expr -0.03*1e-6]
	} elseif {$resistance_type == "rnpoly_wos"} {
		return [expr 0.02*1e-6]
	} elseif {$resistance_type == "rppoly_wos"} {
		return [expr 0.03*1e-6]
	}
}

proc get_r {resistance_type l w fr rw} {
	set sheetR [get_sheet_resistance_RNDIFF $resistance_type]
	set rend   [get_rend_RNDIFF $resistance_type]
	set dl     [get_dl_RNDIFF $resistance_type]
	set dw     [get_dw_RNDIFF $resistance_type]
	#return [check_grid_RNDIFF [expr $fr*$rw*($sheetR*($l-$dl) + 2*$rend) / ($w - $dw)] 0.0001]
	return [expr round($fr*$rw*($sheetR*($l-$dl) + 2*$rend) / ($w - $dw))]
}

proc get_w {resistance_type l r fr rw} {
	set sheetR [get_sheet_resistance_RNDIFF $resistance_type]
	set rend [get_rend_RNDIFF $resistance_type]
	set dl   [get_dl_RNDIFF $resistance_type]
	set dw   [get_dw_RNDIFF $resistance_type]
	
	return [check_grid_RNDIFF [check_for_min_or_max_RNDIFF "wf" [expr $fr*$rw*($sheetR*($l-$dl) + 2*$rend) / $r + $dw]] 0.01]
}

proc get_l {resistance_type w r fr rw} {
	set sheetR [get_sheet_resistance_RNDIFF $resistance_type]
	set rend [get_rend_RNDIFF $resistance_type]
	set dl   [get_dl_RNDIFF $resistance_type]
	set dw   [get_dw_RNDIFF $resistance_type]
	
	return [check_grid_RNDIFF [check_for_min_or_max_RNDIFF "lf" [expr ($r*($w-$dw) - 2*$rend*$fr*$rw) / $sheetR + $dl]] 0.005]
}

proc to_user {value} {
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

proc Rndiff32 {} {
	set r  [getCurrentParamValue "r"]

	set l [to_user [getCurrentParamValue_RNDIFF "l"]]
	set wf [check_for_min_or_max_RNDIFF "wf" [to_user [getCurrentParamValue_RNDIFF "wf"]]]
	set lf [check_for_min_or_max_RNDIFF "lf" [to_user [getCurrentParamValue_RNDIFF "lf"]]]
	
	set rw [check_for_min_or_max_RNDIFF "r"  [getCurrentParamValue_RNDIFF "rw"]]
	set fr [check_for_min_or_max_RNDIFF "fr" [getCurrentParamValue_RNDIFF "fr"]]
	
	set entryMode [getCurrentParamValue_RNDIFF "entryMode"]
	set m         [getCurrentParamValue_RNDIFF "m"]
	set lcontact  [getCurrentParamValue_RNDIFF "lcontact"]
	set wbar      [getCurrentParamValue_RNDIFF "wbar"]
	set connect   [getCurrentParamValue_RNDIFF "connect"]
	set resistance_type [getCurrentParamValue_RNDIFF "model"]

	set edited_param [getCurrentParam_RNDIFF]
	
	if {$entryMode == "r & w"} {
		if {$edited_param == "r"} {
			set l [get_l $resistance_type $wf $r $fr $rw]
			set lf [check_grid_RNDIFF [expr $l/($fr*$rw)] 0.005]
			set l [expr $lf * $fr * $rw]
			set r [get_r $resistance_type $l $wf $fr $rw]
			
		} elseif {$edited_param == "wf"} {
			set r [get_r $resistance_type $l $wf $fr $rw]
		
		}
	} elseif {$entryMode == "r & l"} {
		if {$edited_param == "r"} {
			set wf [get_w $resistance_type $l $r $fr $rw]
			set r  [get_r $resistance_type $l $wf $fr $rw]
			
		} elseif {$edited_param == "lf"} {
			set r  [get_r $resistance_type $l $wf $fr $rw]
			set l  [expr $lf * $fr * $rw]
			
		}
	} elseif {$entryMode == "l & w"} {
		if {$edited_param == "wf"} {
			set r  [get_r $resistance_type $l $wf $fr $rw]
		}
		if {$edited_param == "lf"} {
			set l [expr $lf * $fr * $rw]
			set r [get_r $resistance_type $l $wf $fr $rw]
		}
	}
	
	if {$edited_param == "m"} {
		setInstanceParamValue_RNDIFF "m" [check_for_min_or_max_RNDIFF "m" $m] [getCurrentInstance_RNDIFF]
	} elseif {$edited_param == "wbar"} {
		setInstanceParamValue_RNDIFF "wbar" [check_for_min_or_max_RNDIFF "wbar" $wbar] [getCurrentInstance_RNDIFF]
	} elseif {$edited_param == "lcontact"} {
		setInstanceParamValue_RNDIFF "lcontact" [check_for_min_or_max_RNDIFF "lcontact" $lcontact] [getCurrentInstance_RNDIFF]
	} 
	
	if {$edited_param == "rw"} {
		set rw [check_for_min_or_max_RNDIFF "rw" $rw]
		set r  [get_r $resistance_type $l $wf $fr $rw]
		set l  [expr $lf * $fr * $rw]
		#setInstanceParamValue_RNDIFF "rw" $rw [getCurrentInstance_RNDIFF]
	} elseif {$edited_param == "fr"} {
		set fr [check_for_min_or_max_RNDIFF "fr" $fr]
		set r  [get_r $resistance_type $l $wf $fr $rw]
		set l  [expr $lf * $fr * $rw]
		#setInstanceParamValue_RNDIFF "fr" $fr [getCurrentInstance_RNDIFF]
	}
	
	
	setInstanceParamValue_RNDIFF "lf" $lf [getCurrentInstance_RNDIFF]
	setInstanceParamValue_RNDIFF "wf" $wf [getCurrentInstance_RNDIFF]
	setInstanceParamValue_RNDIFF "r"  $r  [getCurrentInstance_RNDIFF]
	setInstanceParamValue_RNDIFF "fr" $fr [getCurrentInstance_RNDIFF]
	setInstanceParamValue_RNDIFF "rw" $rw [getCurrentInstance_RNDIFF]
	setInstanceParamValue_RNDIFF "l"  $l  [getCurrentInstance_RNDIFF]
	
}
