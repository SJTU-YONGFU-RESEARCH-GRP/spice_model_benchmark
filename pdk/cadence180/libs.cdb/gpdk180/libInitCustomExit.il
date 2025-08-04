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
;; Set the VXL chaining and folding library
;;
envSetVal("layoutXL" "compTypeRefLibs" 'string "gpdk180")

;;
;; Set the display units variable
;;
gLabelsNumNotation = 'suffix

;;
;; Set the VXL ignore parameters for 5141USR3
;;
envSetVal("layoutXL" "checkOldIgnoredParamsProps" 'boolean t)

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

