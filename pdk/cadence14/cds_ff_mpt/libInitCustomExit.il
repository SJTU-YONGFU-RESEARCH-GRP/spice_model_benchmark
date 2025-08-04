;;
;; Get the Library Path
;;
  libPath = ddGetObjReadPath( ddGetObj( "cds_ff_mpt" ) )

;;
;; Set the IVPVS Path
  vipvsPath = strcat(libPath "/..")
  setShellEnvVar("GPDK_INSTALL_DIR" vipvsPath)

;;; Sets the specified environment variable if it hasn't been already set 
;;; differently from its default value
procedure( envSetValIfDefault( tool var type value "ttsg" )
    when( and( envIsVal( tool var ) envGetVal( tool var ) == envGetDefVal( tool var ) )
	envSetVal( tool var type value )
    )
)

printf("\tLoading Environment Settings ...\n")
;; envSetValIfDefault("layoutXL" "setPPConn" 'boolean nil)
;;envSetValIfDefault("layout" "mppTemplate" 'string "N-Tap")
envSetValIfDefault("layout" "labelHeight" 'float 0.02)
envSetValIfDefault("layout" "displayPinNames" 'boolean t)
envSetValIfDefault("layout" "pinTextSameLayer" 'boolean t)
envSetValIfDefault("layout" "pinTextSamePurpose" 'boolean t)
envSetValIfDefault("layout" "xSnapSpacing" 'float 0.001)
envSetValIfDefault("layout" "ySnapSpacing" 'float 0.001)
envSetValIfDefault("layout" "extractStopLevel" 'int 1)
envSetValIfDefault("layout" "viaParamCalcMode" 'cyclic "minRules")
envSetValIfDefault("layout" "wireViaParamCalcMode" 'cyclic "minRules")
envSetValIfDefault("layoutXL" "initIOPinLayer" 'string "M1 drawing")
envSetValIfDefault("spectre.envOpts" "useAltergroup" 'boolean nil)
envSetValIfDefault("hspiceD.envOpts" "autoDisplay" 'boolean nil)
;; envSetValIfDefault("layoutXL" "lxGenerateInBoundary" 'boolean t)
envSetValIfDefault("layoutXL" "lxPositionMinSep" 'float 0.12)
envSetValIfDefault("layoutXL" "extractVerifyWellSubstrateConnections" 'boolean t)
envSetValIfDefault("layoutXL" "lxFingeringNames" 'string "nf")
envSetValIfDefault("layoutXL" "chainAbutStrategy" 'string "sdFirst")
envSetValIfDefault("layout" "keepGuardRingEndsConnected" 'boolean t)
envSetValIfDefault("layout" "fgrEnableAdvanceWrap" 'boolean t)
envSetValIfDefault("layout" "fgrPostEditPitchCorrection" 'boolean t)
setShellEnvVar("FGR_USE_MIN_SEG_LENGTH=t")
abutDebug=nil

;;; Undefine VLS XL inductor parameters so that "l" parameter on FETs
;;; is not reduced --- see solution associated with CCR 942040
envSetVal( "layoutXL" "inductanceParamNames" 'string "" )
;;-envSetVal( "layoutXL" "sfactorNames" 'string "s S ns" )

;;
;; Append Simulator Model Paths
;;
when(isContextLoaded("schView") 
    file = strcat( libPath "/cds_ff_mpt_ModelMgmt.il" )
    ;;; Load required skill code
    when( and( !getd( 'cds_ff_mpt_AppendModelFile ) isReadable( file ) )
        printf("\tLoading Model Management File ...\n", file)
	load( file )
    )
    cds_ff_mpt_AppendModelFile( 
	'( "spectre" "UltraSim" "ams" )
	strcat( libPath "/../models/spectre/cds_ff_mpt.scs")
	"tt"
    )
)

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
     when( ddObj = ddGetObj(libName nil nil "libInitCktPro.il")
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
	    setShellEnvVar( strcat("cds_ff_mpt_PDK_PATH=" pdkPath ) )
	    when( and( isFile(strcat(pdkPath "/ead/cds_ff_mpt_setup.ini") ) envIsVal("layoutEAD" "useSetup") envGetVal("layoutEAD" "useSetup")==envGetDefVal("layoutEAD" "useSetup") )
                printf( "\tInitializing EAD\n")
		envSetVal("layoutEAD" "useSetup" 'string "$cds_ff_mpt_PDK_PATH/ead/cds_ff_mpt_setup.ini")
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
          \n  *             Generic Finfet Multi Pattern PDK              *
          \n  *                     (cds_ff_mpt)                          *
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
