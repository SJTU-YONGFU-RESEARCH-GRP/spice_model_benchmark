;; Get the Library Path
libPath = ddGetObjReadPath( ddGetObj( "gpdk090" ) )

printf("\tLoading Environment Settings ...\n")
if(!envIsVal("layoutXL" "setPPConn") then
    envSetVal("layoutXL" "setPPConn" 'boolean nil)
)
if(!envIsVal("layout" "mppTemplate") then
    envSetVal("layout" "mppTemplate" 'string "N-Tap")
)
if(!envIsVal("layout" "xSnapSpacing") then
    envSetVal("layout" "xSnapSpacing" 'float 0.005)
)
if(!envIsVal("layout" "ySnapSpacing") then
    envSetVal("layout" "ySnapSpacing" 'float 0.005)
)
if(!envIsVal("layout" "extractVerifySubstrate") then
    envSetVal("layout" "extractVerifySubstrate" 'boolean t)
)
if(!envIsVal("layoutXL" "initIOPinLayer") then
    envSetVal("layoutXL" "initIOPinLayer" 'string "Metal1 drawing")
)
if(!envIsVal("spectre.envOpts" "useAltergroup") then
    envSetVal("spectre.envOpts" "useAltergroup" 'boolean nil)
)
if(!envIsVal("hspiceD.envOpts" "autoDisplay") then
    envSetVal("hspiceD.envOpts" "autoDisplay" 'boolean nil)
)


;; Append Simulator Model Paths
when(isContextLoaded("schView") 
    file = strcat( libPath "/gpdk090_ModelMgmt.il" )
    ;;; Load required skill code
    when( and( !getd( 'gpdk090_AppendModelFile ) isReadable( file ) )
        printf("\tLoading Model Management File ...\n", file)
	load( file )
    )
    gpdk090_AppendModelFile( 
	'( "spectre" "UltraSim" "ams" )
	strcat( libPath "/../../models/spectre/gpdk090.scs")
	"NN"
    )
)

;; Set the display units variable
gLabelsNumNotation = 'suffix

;; For additional detailed information about Circuit Prospector, please see
;; the Cadence online help or SourceLink:
;;
;;     Virtuoso Unified Custom Constraints User Guide, Reference Manual
;;     Virtuoso Unified Custom Constraints Reference Manual
;;     Virtuoso Unified Custom Constraints SKILL API Commands
;;
     ;; load custom library initialization file
     when( ddObj = ddGetObj(libName nil nil "gpdk090_PDKRegistrations.il")
    printf("\tLoading %s/%s ... " libName ddObj~>name)
    if( errset(load(ddGetObjReadPath(ddObj))) then
       printf("done!\n")
    else
       success = nil
       printf("failed!\n")
    )
     ) ; ** when ddObj **


;; Print this header in the CIW
  printf("\n  *************************************************************
          \n  *              Cadence Design Systems, Inc.                 *
          \n  *                                                           *
          \n  *                    Generic 90nm PDK                       *
          \n  *                        (gpdk090)                          *
          \n  *                                                           *
          \n  *************************************************************
          \n")

fp=infile(strcat(libPath "/../../docs/VERSION"))
if(fp then
    while(gets(line fp) printf("\t%s\n" line))
    close(fp)
else
    printf("\tVersion File is not available\n")
)
