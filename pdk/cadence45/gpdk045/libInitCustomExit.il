;; Version 6.0
;; Get the Library Path
;;

  libPath = ddGetObjReadPath( ddGetObj( libName ) )

;;; Sets the specified environment variable if it hasn't been already set 
;;; differently from its default value
procedure( envSetValIfDefault( tool var type value "ttsg" )
    when( and( envIsVal( tool var ) envGetVal( tool var ) == envGetDefVal( tool var ) )
	envSetVal( tool var type value )
    )
)

printf("\tLoading Environment Settings ...\n")
envSetValIfDefault("layoutXL" "setPPConn" 'boolean nil)
envSetValIfDefault("layout" "mppTemplate" 'string "N-Tap")
envSetValIfDefault("layout" "xSnapSpacing" 'float 0.005)
envSetValIfDefault("layout" "ySnapSpacing" 'float 0.005)
envSetValIfDefault("layoutXL" "initIOPinLayer" 'string "Metal1 drawing")
envSetValIfDefault("spectre.envOpts" "useAltergroup" 'boolean nil)
envSetValIfDefault("hspiceD.envOpts" "autoDisplay" 'boolean nil)
envSetValIfDefault("layoutXL" "lxGenerateInBoundary" 'boolean t)
envSetValIfDefault("layoutXL" "lxPositionMinSep" 'float 0.12)
envSetValIfDefault("layoutXL" "extractVerifyWellSubstrateConnections" 'boolean t)
envSetValIfDefault("layoutXL" "lxEvalCDFCallbacks" 'boolean t)

when( rexMatchp("6.1.5" getVersion(t)) 
     printf("\tLoading Fluid Guard Ring Set Up ... \n")
     when(isCallable('vfoInstallFluidDeviceFiles) 
          vfoInstallFluidDeviceFiles()
     )
    )
when( rexMatchp("6.1.4" getVersion(t)) 
        isrDotNum = rindex(rindex(getVersion(t) ".") ".")
        isrNum = evalstring(substring(isrDotNum 2 strlen(isrDotNum)))
          if( (isrNum < 5) then 
             printf("\tLoading Fluid Guard Ring Set Up ... \n")
             envSetVal("layout" "enableFluidGuardRing" 'boolean t)
             when(isCallable('installFluidDeviceFiles)
                  installFluidDeviceFiles()
             )
          else 
             printf("\tLoading Fluid Guard Ring Set Up ... \n")
             envSetVal("layout" "enableFluidGuardRing" 'boolean t)
             when(isCallable('vfoInstallFluidDeviceFiles)
                  vfoInstallFluidDeviceFiles()
             )
          )
    )

;;
;; Append Simulator Model Paths
;;
when(isContextLoaded("schView") 
    file = strcat( libPath "/gpdk045_ModelMgmt.il" )
    ;;; Load required skill code
    when( and( !getd( 'gpdk045_AppendModelFile ) isReadable( file ) )
        printf("\tLoading Model Management File ...\n", file)
	load( file )
    )
    gpdk045_AppendModelFile( 
	'( "spectre" "UltraSim" "ams" )
	strcat( libPath "/../models/spectre/gpdk045.scs")
	"mc"
    )
)

;;
;; Set the Simulator Model Paths
;;
;;  if(isContextLoaded("schView") then
;;    envSetVal("asimenv.startup" "simulator" 'string "spectre")
;;      asiSetEnvOptionVal(asiGetTool('spectre) "modelFiles"
;;         list(
;;            list(strcat( libPath "/../models/spectre/gpdk045.scs") "tt")
;;      ))
;;      asiSetEnvOptionVal(asiGetTool('UltraSim) "modelFiles"
;;         list(
;;            list(strcat( libPath "/../models/spectre/gpdk045.scs") "tt")
;;     ))
;;      asiSetEnvOptionVal(asiGetTool('ams) "modelFiles"
;;         list(
;;            list(strcat( libPath "/../models/spectre/gpdk045.scs") "tt")
;;      ))
;;    )
;;
;; Set the display units variable
;;
gLabelsNumNotation = 'suffix

;;
;; Set the circuit prospector pdk defualts
;;

;; For additional detailed information about Circuit Prospector, please see
;; the Cadence online help or SourceLink:
;;
;;     Virtuoso Unified Custom Constraints User Guide, Reference Manual
;;     Virtuoso Unified Custom Constraints Reference Manual
;;     Virtuoso Unified Custom Constraints SKILL API Commands
;;       
     ;; load custom library initialization file
     when( ddObj = ddGetObj(libName nil nil "gpdk045_PDKRegistrations.il")
    printf("\tLoading %s/%s ... " libName ddObj~>name)
    if( errset(load(ddGetObjReadPath(ddObj))) then
       printf("done!\n")
    else
       success = nil
       printf("failed!\n")
    )
     ) ; ** when ddObj **

    ;;; EAD setup

    let( (libId pdkPath )
	when( ( libId = ddGetObj( libName) )
	    pdkPath = simplifyFilename( strcat( ddGetObjReadPath(libId) "/.." ) )
	    setShellEnvVar( strcat("GPDK045_PDK_PATH=" pdkPath ) )
	    when( and( isFile(strcat(pdkPath "/ead/gpdk045_setup.ini") ) envIsVal("layoutEAD" "useSetup") envGetVal("layoutEAD" "useSetup")==envGetDefVal("layoutEAD" "useSetup") )
                printf( "\tInitializing EAD\n")
		envSetVal("layoutEAD" "useSetup" 'string "$GPDK045_PDK_PATH/ead/gpdk045_setup.ini")
	    )
	    ;;; Non-GUI flow setup, such as the pre-EM flow Setup
	    when( and( envIsVal("layoutEAD" "useCorner") envGetVal("layoutEAD" "useCorner")==envGetDefVal("layoutEAD" "useCorner") )
		envSetVal("layoutEAD" "useCorner" 'string "typical" ) ;;; Corner 
	    )
	    when( and( envIsVal("layoutEAD.em" "preEMCheckLayers") envGetVal("layoutEAD.em" "preEMCheckLayers")==envGetDefVal("layoutEAD.em" "preEMCheckLayers") )
		envSetVal("layoutEAD.em" "preEMCheckLayers" 'string "Metal1,Metal2")
	    )
	    ;;; Additional variables required for the pre-EM check flow but which
	    ;;; are not considered part of the PDK process setup
	    /*
	    when( envIsVal("layoutEAD.em" "preEMDetailReport")
		envSetVal("layoutEAD.em" "preEMDetailReport" 'boolean t)
	    )
	    when( envIsVal("layoutEAD.em" "preEMLogFile" )
		envSetVal("layoutEAD.em" "preEMLogFile" 'string "preEmCheck.log")
	    )
	    when( envIsVal("layoutEAD.em" "preEMViolThresholdPercent" )
		envSetVal("layoutEAD.em" "preEMViolThresholdPercent" 'float 100.0 )
	    )
	    */
	)
    )

;;
;; Print this header in the CIW
;;
  printf("\n  *************************************************************
          \n  *              Cadence Design Systems, Inc.                 *
          \n  *                                                           *
          \n  *                    Generic 45nm PDK                       *
          \n  *                        (gpdk045)                          *
          \n  *                                                           *
          \n  *************************************************************
          \n")

fp=infile(strcat(libPath "/../docs/VERSION"))
if(fp then
    while(gets(line fp) printf("\t%s\n" line))
    close(fp)
else
    printf("\tVersion File is not available\n")
)
