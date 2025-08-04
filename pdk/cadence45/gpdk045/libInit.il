
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;;  libInit.il
;;
;;  PDK Automation System (PAS)
;;  Cadence Design Systems
;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

let( ( ddObj (success t) (libName "gpdk045") )

  printf("Loading %s/libInit.il ...\n" libName)

  if( ddGetObj(libName) then
    
     ;; load custom library initialization file
     when( ddObj = ddGetObj(libName nil nil "libInitCustomEnter.il")
	printf("\tLoading %s/%s ... " libName ddObj~>name)
	if( errset(load(ddGetObjReadPath(ddObj))) then
	   printf("done!\n")
	else
	   success = nil
	   printf("failed!\n")
	)
     ) ; ** when ddObj **


     ;; load loadCxt.ile
     unless( fboundp('PasLoadLibContext)
	when( ddObj = ddGetObj(libName nil nil "loadCxt.ile")
	   printf("\tLoading %s/%s ... " libName ddObj~>name)
	   if( errset(load(ddGetObjReadPath(ddObj))) then
	      printf("done!\n")
	   else
	      success = nil
	      printf("failed!\n")
	   ) ; ** if errset **
	) ; ** when ddObj **
     ) ; ** unless fboundp **
     
     ;; load library context files
     if(  fboundp('PasLoadLibContext) then
	unless( PasLoadLibContext(libName libName)
	   success = nil
	)
	unless( PasLoadLibContext(libName "pdkUtils")
	   success = nil
	)
     else
	success = nil
     ) ; ** if fboundp **
     
     
;;  load library display resource file
;;     when(  fboundp(`drLoadDrf)     
;;	when( ddObj = ddGetObj(libName nil nil "display.drf")
;;	   printf("\tLoading %s/%s ... " libName ddObj~>name)
;;	   if( errset(drLoadDrf(ddGetObjReadPath(ddObj) nil)) then
;;	      printf("done!\n")
;;	   else
;;	      success = nil
;;	      printf("failed!\n")
;;	   )
;;	) ; ** when ddObj **
;;     ) ; ** when fboundp **

;;  This modification done based on CCR 1237646
;;  set the default library display resource file 
     when( and( isCallable('hiGraphicMode) hiGraphicMode())
        unless( and( 
                    filePath = or( envGetVal("graphic" "drfPath") ddGetStartup("display.drf") )
                    !blankstrp(filePath)
                )
            when( ( ddObj = ddGetObj(libName nil nil "display.drf") )
                filePath = ddGetObjReadPath( ddObj )
                when( isReadable( filePath )
                    envSetVal( "graphic" "drfPath" 'string filePath )
                )
            ) ; ** when ddObj **
        ) ; ** unless filePath **
     ) ; ** when callable **
     
     ;; set the number of digits to be displayed to 6
     when( fboundp('aelPushSignifDigits)
	aelPushSignifDigits(6)
     )

     ;; load custom filter settings
     when( ddObj = ddGetObj(libName nil nil "gpdk045_customFilter.il")
	printf("\tLoading %s/%s ... " libName ddObj~>name)
	if( errset(load(ddGetObjReadPath(ddObj))) then
	   printf("done!\n")
	else
	   success = nil
	   printf("failed!\n")
	)
     ) ; ** when ddObj **
     

     ;; load custom library initialization file (exit)
     when( ddObj = ddGetObj(libName nil nil "libInitCustomExit.il")
	printf("\tLoading %s/%s ... \n" libName ddObj~>name)
	if( errset(load(ddGetObjReadPath(ddObj))) then
	   printf("done!\n")
	else
	   success = nil
	   printf("failed!\n")
	)
     ) ; ** when ddObj **
  else
     success = nil
  ) ; ** if ddGetObj **

  if( success then
     printf("Loaded %s/libInit.il successfully!\n" libName)
  else
     printf("Failed to load %s/libInit.il successfully!" libName)
  )
  
  t
  
) ; ** let **
