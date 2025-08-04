

proc getCurrentInstance_C {} {
	return [db::getCurrentRef]
}

proc getCurrentParam_C {} {
	return [db::getCurrentParam]
}


proc getCurrentParamValue_C {param_name} {
	return [db::getParamValue $param_name -of [getCurrentInstance_C]]
}

proc setInstanceParamValue_C { param value inst} {
	db::setParamValue $param -value "${value}" -of $inst -evalCallbacks 0
}

proc Ccap {} {
	puts "==============================="
	puts "Ccap callback has no checks. Be careful when setting values"
	puts "Please align with capacitance provided by LVS in schematic."
	puts "==============================="
	
	set m  [to_user [getCurrentParamValue_C "m"]]
	set nf  [to_user [getCurrentParamValue_C "nf"]]
	set l  [to_user [getCurrentParamValue_C "l"]]
	set w  [to_user [getCurrentParamValue_C "w"]]
	set startmetal [getCurrentParamValue_C "startmetal"]
	set endmetal   [getCurrentParamValue_C "endmetal"]
	
	set Cf 0.114e-17
	set Ca 3.83e-17
	
	set layers [expr $endmetal - $startmetal]

	set l [ expr $l + 0.3]
	set perim [expr 2*($l+$w)]
	set area  [expr $l*$w]	
	 
	set cval [expr $layers * $nf * ($Ca*$area + $Cf*$perim*2.8e-7 )]

	
#	set perim [expr 2*$l+$nf*$w]
#	set area  [expr $nf*$l*$w]	
	
#	set cval [expr $Ca*$area + $Cf*$perim*2.8e-7]
	
	setInstanceParamValue_C "cval" [db::sciToEng $cval]  [getCurrentInstance_C]
	
}
