
if [info exists limit] { unset limit }

proc Mos32 {} {
	setLimits_MOS
	set GRID {0.001u}
	set inst  			[iPDK_getCurrentInst]
	set model 			[iPDK_getParamValue model $inst]
	
	set edited_param 	   [getCurrentParam]	
	set edited_param_value [iPDK_getParamValue $edited_param $inst]
	

	## define parameter lists
	
	set pycell_metric_params [list diffContactLeftBottomOffset   diffContactLeftTopOffset      diffContactCenterTopOffset    diffContactCenterBottomOffset diffContactRightBottomOffset  diffContactRightTopOffset     gateContactLeftOffset   gateContactRightOffset  cgSpacingAdd  leftDiffAdd   rightDiffAdd  ]
	set geometric_params [list w l wtot ]
	set integer_params [list nf m  ]
	
	set all_string_params [list guardRing guardRingVertical guardRingHorizontal ]
	set all_option_params [list model entryMode]
	set all_metric_params [concat $geometric_params $pycell_metric_params ]
	set all_numeric_params [concat $integer_params $all_metric_params ]
	
	set all_params [concat $all_option_params $all_numeric_params $all_string_params]

	# check validity of numeric values, can be either variable or valid number
	foreach param $all_numeric_params {
		checkParameterValid $param [iPDK_getParamValue $param $inst] 
	} 

	#fetch parameter values
	log "-----------"
	log "$edited_param = $edited_param_value"
	
	if [info exists value] { unset value }
	if [info exists initial_value] { unset initial_value }
	foreach param $all_params {
		set value($param) [getCurrentParamValue $param]		
		set initial_value($param) [getCurrentParamValue $param]	
		log "$param	-> $value($param)"
	}
	
	# check limiting ranges and convert to Scientific representation
	foreach param $all_numeric_params {
		if {!([isVariable $value($param)]==1)} {	
			
			if {[lsearch $all_metric_params $param]>-1 && [regexp {^[0-9\.]+$} $value($param)]==1} {
				#no prefixes just plain value
				#then multiply by 1e-6
				
				set _value [iPDK_engToSci $value($param)]
				set _value [expr $_value*1e-6]
			} else {
				set _value [iPDK_engToSci $value($param)]
			}
			
			
			set value($param) [checkParameterLimits $model $param $_value ]
		} 
	}
	
	#check manufacturing grid
	foreach param $all_metric_params {
		set value($param) [checkMfGrid $param $value($param) $GRID]
	}
	
	# do recalculations
	
	set nf $value(nf)
	set wpf $value(w)
	set wtot $value(wtot)
	
	set no_varibles [expr [isVariable nf]==1 || [isVariable wpf]==1 || [isVariable wtot]==1 ]
	if { ($edited_param == "nf" || $edited_param == "w" || $edited_param == "wtot")  &&  $no_varibles} {
		
			if {$edited_param == "nf" || $edited_param == "w"} {			
				set wtot [expr $nf*$wpf]
				
				if { $wtot != $value(wtot) } {
					if {$nf >1} {
					console_log information 001 "Calculated Total Width = [sciToU $wtot] using Width Per Finger = [sciToU $wpf], Number of Fingers = [sciToInt $nf] "
					}
					set wtot [checkMfGrid "Total Width" $wtot $GRID]
				}
								
			} elseif {$edited_param == "wtot"} {
				set wpf [expr $wtot/$nf]
				
				if { (![metric_equal $wpf $value(w)]) } {
					if {$nf >1} {
						console_log information 002 "Calculated Width Per Finger = [sciToU $wpf] using Total Width = [sciToU $wtot], Number of Fingers = [sciToInt $nf]"
					}

					set wpf [checkMfGrid "Width Per Finger" $wpf $GRID]				
					set new_wpf [checkParameterLimits $model w $wpf]
					
					if {$new_wpf != $wpf} {
						set wpf $new_wpf
						
						#adjust
						if {$edited_param == "wtot"} {
							set wtot [expr $nf*$wpf]							
							console_log information 003 "Adjusting Total Width to [sciToU $wtot] using formula 'Width Per Finger' x 'Number of Fingers'" 
						} elseif {$edited_param == "nf"} {
							set nf [expr $wtot/$wpf]							
							console_log information 003 "Adjusting Number of Fingers to [sciToInt $nf] using formula 'Total Width' / 'Width Per Finger'" 							
						}
					}				
				}

			}				
	}
	
	if { $edited_param == "guardRingVertical" || $edited_param == "guardRingHorizontal" } {
		set guardRing "$value(guardRingVertical),$value(guardRingHorizontal)"
		set guardRing [ regsub {,none} $guardRing {}]
		set guardRing [ regsub {none,} $guardRing {}]
		set value(guardRing)  $guardRing

		log "$value(guardRing) = $value(guardRingVertical),$value(guardRingHorizontal)"
	}
	
	set  value(nf) 		$nf
	set  value(w) 		$wpf
	set  value(wtot) 	$wtot
	
	# set new values
	foreach param $all_metric_params {
		log "final $param changed from $initial_value($param) -> $value($param)"
				
		if { ! [metric_equal $initial_value($param) $value($param)]} {
			log "set!"
# this works only in J-2014, thus removed			
#			set val [db::sciToEng $value($param) -suffix u ]
			set val [iPDK_sciToEng $value($param)]
			iPDK_setParamValue $param $val $inst 1
		}
	}
	
	foreach param [concat $all_string_params $integer_params] {
		if {$initial_value($param) != $value($param)} {
			iPDK_setParamValue $param  $value($param) $inst 1
		}
	}

}


proc setLimits_MOS {} {
	# limit(device,param,min) 
	
	
	foreach dev {n18 p18 n25 p25 n105 p105 n105_lvt p105_lvt n105_hvt p105_hvt} { setLimits $dev nf 1 999 }
	foreach dev {n18 p18 n25 p25 n105 p105 n105_lvt p105_lvt n105_hvt p105_hvt} { setLimits $dev m 1 999 }
	
	
	foreach dev {n18 p18} { setLimits $dev l 0.15u 3.5u }
	foreach dev {n18 p18} { setLimits $dev w 0.16u 3.5u }
	
	foreach dev {n25 p25} { setLimits $dev l 0.26u 3.5u }
	foreach dev {n25 p25} { setLimits $dev w 0.36u 3.5u }
		
	foreach dev {n105 p105 n105_lvt p105_lvt n105_hvt p105_hvt} { setLimits $dev w 0.1u 3.5u }
	foreach dev {n105 p105 n105_lvt p105_lvt n105_hvt p105_hvt} { setLimits $dev l 0.03u 3.5u }
	
	foreach dev {n18 p18}  { setLimits $dev wtot 0.16u 250m }
	foreach dev {n25 p25 } { setLimits $dev wtot 0.36u 250m }
	foreach dev {n105 p105 n105_lvt p105_lvt n105_hvt p105_hvt} { setLimits $dev wtot 0.1u 250m }
	
	set params [list diffContactLeftBottomOffset   diffContactLeftTopOffset      diffContactCenterTopOffset    diffContactCenterBottomOffset diffContactRightBottomOffset  diffContactRightTopOffset     gateContactLeftOffset   gateContactRightOffset  cgSpacingAdd  leftDiffAdd   rightDiffAdd  ]
	set devices [list n18 p18 n25 p25 n105 p105 n105_lvt p105_lvt n105_hvt p105_hvt]
	
	foreach param  $params { 
		foreach dev $devices { 
			setLimits $dev $param -3.5u 0 
		}
	}
	
	# foreach dev {n18 p18 n25 p25} { setLimits $dev diffContactLeftBottomOffset 0 1 }
	# foreach dev {n18 p18 n25 p25} { setLimits $dev diffContactLeftTopOffset 0 1 }
	# foreach dev {n18 p18 n25 p25} { setLimits $dev diffContactCenterTopOffset 0 1 }
	# foreach dev {n18 p18 n25 p25} { setLimits $dev diffContactCenterBottomOffset 0 1 }
	# foreach dev {n18 p18 n25 p25} { setLimits $dev diffContactRightBottomOffset 0 1 }
	# foreach dev {n18 p18 n25 p25} { setLimits $dev diffContactRightTopOffset 0 1 }
	# foreach dev {n18 p18 n25 p25} { setLimits $dev gateContactLeftOffset 0 1 }
	# foreach dev {n18 p18 n25 p25} { setLimits $dev gateContactRightOffset 0 1 }
	# foreach dev {n18 p18 n25 p25} { setLimits $dev cgSpacingAdd 0 1 }
	# foreach dev {n18 p18 n25 p25} { setLimits $dev leftDiffAdd 0 1 }
	# foreach dev {n18 p18 n25 p25} { setLimits $dev rightDiffAdd 0 1 }
	
	# foreach dev {n105 p105 n105_lvt p105_lvt n105_hvt p105_hvt} { setLimits $dev diffContactLeftBottomOffset 0 1 }
	# foreach dev {n105 p105 n105_lvt p105_lvt n105_hvt p105_hvt} { setLimits $dev diffContactLeftTopOffset 0 1 }
	# foreach dev {n105 p105 n105_lvt p105_lvt n105_hvt p105_hvt} { setLimits $dev diffContactCenterTopOffset 0 1 }
	# foreach dev {n105 p105 n105_lvt p105_lvt n105_hvt p105_hvt} { setLimits $dev diffContactCenterBottomOffset 0 1 }
	# foreach dev {n105 p105 n105_lvt p105_lvt n105_hvt p105_hvt} { setLimits $dev diffContactRightBottomOffset 0 1 }
	# foreach dev {n105 p105 n105_lvt p105_lvt n105_hvt p105_hvt} { setLimits $dev diffContactRightTopOffset 0 1 }
	# foreach dev {n105 p105 n105_lvt p105_lvt n105_hvt p105_hvt} { setLimits $dev gateContactLeftOffset 0 1 }
	# foreach dev {n105 p105 n105_lvt p105_lvt n105_hvt p105_hvt} { setLimits $dev gateContactRightOffset 0 1 }
	# foreach dev {n105 p105 n105_lvt p105_lvt n105_hvt p105_hvt} { setLimits $dev cgSpacingAdd 0 1 }
	# foreach dev {n105 p105 n105_lvt p105_lvt n105_hvt p105_hvt} { setLimits $dev leftDiffAdd 0 1 }
	# foreach dev {n105 p105 n105_lvt p105_lvt n105_hvt p105_hvt} { setLimits $dev rightDiffAdd 0 1 }
	
}



