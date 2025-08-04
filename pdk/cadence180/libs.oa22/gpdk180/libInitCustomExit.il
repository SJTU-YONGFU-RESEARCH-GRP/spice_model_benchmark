;;
;; Set the Simulation Model Path
;;
;; This code will only add the gpdk models to the modelFiles setup if the
;; models are not already part of the setup. Also, the model file setup
;; information is appended to the existing setup so that setup defined
;; elsewhere by start-up sequence does not get removed.
prog((libPath pdkRoot pdkModels modelFiles file)
    when( isContextLoaded("schView") 
	envSetVal("asimenv.startup" "simulator" 'string "spectre")
	libPath = ddGetObjReadPath( ddGetObj( "gpdk180" ) )
	;;; Determine pdk root installation directory from pdk library path
	pdkRoot = strcat( libPath "/../.." )
	pdkModels = simplifyFilename(
		 strcat( pdkRoot "/models/spectre/gpdk.scs") 
	)
	;;; Append PDK models to existing path. This allows models to defined
	;;; in the users or project .cdsinit files
	modelFiles = asiGetEnvOptionVal(asiGetTool('spectre) "modelFiles")
	;;; Watch-out for duplicate entries
	rexCompile( "^\\$\\([a-zA-Z]+\\)\\(.*\\)" )
	modelFiles = mapcar( 
	    lambda((modelDef)
		file = car( modelDef )
		if( rexExecute( file ) then
		    list(
			simplifyFilename( 
			    strcat(
				or( getShellEnvVar( rexSubstitute( "\\1" ) ) "")
				rexSubstitute( "\\2" )
			    )
			)
			cadr( modelDef )
		    )
		else
		    modelDef
		)
	    )
	    modelFiles
	)
	 unless( member( pdkModels mapcar('car modelFiles) )
	    asiSetEnvOptionVal(asiGetTool('spectre) "modelFiles"
		append1(
		    asiGetEnvOptionVal(asiGetTool('spectre) "modelFiles")
		    list( pdkModels  "stat")
		)
	    )
	    asiSetEnvOptionVal(asiGetTool('ams) "modelFiles"
		append1(
		    asiGetEnvOptionVal(asiGetTool('ams) "modelFiles")
		    list( pdkModels  "stat")
		)
	    )
	) 
    )
)

;;
;; Set the display units variable
;;
gLabelsNumNotation = 'suffix

;;
;; Set the circuit prospector pdk defualts
;;
when( isCallable('ciRegisterDevice)
 ciRegisterDevice("fet"
			append(ciGetDeviceNames("fet")
			'( '("gpdk180" "nmos" nil)
			   '("gpdk180" "nmos3" nil)
			   '("gpdk180" "nmos3hv" nil)
			   '("gpdk180" "nmoshv" nil)
			   '("gpdk180" "nmosrf" nil)
			   '("gpdk180" "pmos" nil)
			   '("gpdk180" "pmos3" nil)
			   '("gpdk180" "pmos3hv" nil)
			   '("gpdk180" "pmoshv" nil)
			   '("gpdk180" "pmosrf" nil)
 )))
 ciRegisterDevice("nfet"
			append(ciGetDeviceNames("nfet")
			'( '("gpdk180" "nmos" nil)
			   '("gpdk180" "nmos3" nil)
			   '("gpdk180" "nmos3hv" nil)
			   '("gpdk180" "nmoshv" nil)
			   '("gpdk180" "nmosrf" nil)
 )))
 ciRegisterDevice("pfet"
 			append(ciGetDeviceNames("pfet")
		  	'( '("gpdk180" "pmos" nil)
			   '("gpdk180" "pmos3" nil)
			   '("gpdk180" "pmos3hv" nil)
			   '("gpdk180" "pmoshv" nil)
			   '("gpdk180" "pmosrf" nil)
 )))
 ciRegisterDevice("bjt"
 			append(ciGetDeviceNames("bjt")
		  	'( '("gpdk180" "npn" nil)
			   '("gpdk180" "pnp" nil)
			   '("gpdk180" "vpnp" nil)
 )))
 ciRegisterDevice("npn"
 			append(ciGetDeviceNames("npn")
		  	'( '("gpdk180" "npn" nil)
 )))
 ciRegisterDevice("pnp"
 			append(ciGetDeviceNames("pnp")
		  	'( '("gpdk180" "pnp" nil)
			   '("gpdk180" "vpnp" nil)
 )))
 ciRegisterDevice("diode"
 			append(ciGetDeviceNames("diode")
		  	'( '("gpdk180" "ndio" nil)
			   '("gpdk180" "pdio" nil)
 )))
 ciRegisterDevice("passive"
 			append(ciGetDeviceNames("passive")
			'( '("gpdk180" "mimcap" nil)
			   '("gpdk180" "m1res" nil)
			   '("gpdk180" "m2res" nil)
			   '("gpdk180" "m3res" nil)
			   '("gpdk180" "m4res" nil)
			   '("gpdk180" "m5res" nil)
			   '("gpdk180" "m6res" nil)
			   '("gpdk180" "nplusres" nil)
			   '("gpdk180" "nwellres" nil)
			   '("gpdk180" "polyhres" nil)
			   '("gpdk180" "polyres" nil)
			   '("gpdk180" "pplusres" nil)
 )))
 ciRegisterDevice("resistor"
 			append(ciGetDeviceNames("resistor")
			'( '("gpdk180" "m1res" nil)
			   '("gpdk180" "m2res" nil)
			   '("gpdk180" "m3res" nil)
			   '("gpdk180" "m4res" nil)
			   '("gpdk180" "m5res" nil)
			   '("gpdk180" "m6res" nil)
			   '("gpdk180" "nplusres" nil)
			   '("gpdk180" "nwellres" nil)
			   '("gpdk180" "polyhres" nil)
			   '("gpdk180" "polyres" nil)
			   '("gpdk180" "pplusres" nil)
 )))
 ciRegisterDevice("capacitor"
 			append(ciGetDeviceNames("capacitor")
			'( '("gpdk180" "mimcap" nil)
 )))

 ciMapParam("width"        append(ciGetParamMapping("width")        '("w")))
 ciMapParam("length"       append(ciGetParamMapping("length")       '("l")))
 ciMapParam("fingerCount"  append(ciGetParamMapping("fingerCount")  '("fingers")))
 ciMapParam("fingerWidth"  append(ciGetParamMapping("fingerWidth")  '("fw")))
 ciMapParam("mFactor"      append(ciGetParamMapping("mFactor")      '("m")))
 ciMapParam("resValue"     append(ciGetParamMapping("resValue")     '("r")))
 ciMapParam("capValue"     append(ciGetParamMapping("capValue")     '("c")))
 ciMapParam("indValue"     append(ciGetParamMapping("indValue")     '("l")))
 ciMapParam("area"         append(ciGetParamMapping("area")         '("area")))
 ciMapParam("perimeter"    append(ciGetParamMapping("perimeter")    '("perim")))

 ciMapTerm("gate"      append(ciGetTermNames("gate")      '("G")))
 ciMapTerm("source"    append(ciGetTermNames("source")    '("S")))
 ciMapTerm("drain"     append(ciGetTermNames("drain")     '("D")))
 ciMapTerm("bulk"      append(ciGetTermNames("bulk")      '("B")))
 ciMapTerm("base"      append(ciGetTermNames("base")      '("B")))
 ciMapTerm("emitter"   append(ciGetTermNames("emitter")   '("E")))
 ciMapTerm("collector" append(ciGetTermNames("collector") '("C")))
) ; when 

;;
;; Print this header in the CIW
;;
  printf("\n  *************************************************************
          \n  *              Cadence Design Systems, Inc.                 *
          \n  *                                                           *
          \n  *                    Generic 180nm PDK                      *
          \n  *                        (gpdk180)                          *
          \n  *                                                           *
          \n  *                       Version 3.2                         *
          \n  *                                                           *
          \n  *************************************************************
          \n")

