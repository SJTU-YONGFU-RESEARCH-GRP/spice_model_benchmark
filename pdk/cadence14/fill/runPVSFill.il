/*******************************************************************************
* DISCLAIMER: The following code is provided for Cadence customers             *
* to use at their own risk. The code may require modification to               *
* satisfy the requirements of any user. The code and any modifications         *
* to the code may not be compatible with current or future versions of         *
* Cadence products.                                                            *
* THE CODE IS PROVIDED "AS IS" AND WITH NO WARRANTIES,                         *
* INCLUDING WITHOUT LIMITATION ANY EXPRESS WARRANTIES OR IMPLIED               *
* WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR USE.               *
*******************************************************************************/
/*
This SKILL code generates a pvsRunFill Pull-down menu in Layout L and XL.
USAGE:
load("runPVSFill.il")
*/

procedure(ipvsRunFill(lib cell outLib rule_File ruleMap_File layerMap_File 
                      objectMap_File useInstFill fillCell1 fillCell2
                      designType prBoundary critNet critNetFile fillEdgeHalo
                      beolStack)
   prog((cvv fill cellId fillCvName inst instXY fillCV w l point x y lppShapes1
        lppShapes2 instId instName n point_cv fillInstId fillInst evDesignType
        evBoundary evBeolStack evUseInstFill evUseCritNet evCritNetFile 
        evFillEdgeHalo)

      ;; Initialize cellview
      cellId = geGetWindowCellView()
      unless(cellId
         ;; no cellview open, only possible if the user runs ipvsRunFill
         ;; on the command line
         cvv = geOpen(?lib lib ?cell cell ?view "layout")
         hiRaiseWindow(cvv)
         cellId = geGetEditCellView(cvv)
      )

      unless(isFile(rule_File)
         printf("ERROR: Rule file does not exist or is not readable.")
         printf(" %L\n" rule_File)
         return()
      )

      ;; Set runset switches
      evDesignType = getShellEnvVar("DESIGN_TYPE")
      setShellEnvVar("DESIGN_TYPE" designType)
      
      evBoundary = getShellEnvVar("SELECT_PRBOUNDARY")
      if(prBoundary == "prBoundary" then
         setShellEnvVar("SELECT_PRBOUNDARY" "YES")
      else
         setShellEnvVar("SELECT_PRBOUNDARY" "NO")
      )

      evBeolStack = getShellEnvVar("BEOL_STACK")
      setShellEnvVar("BEOL_STACK" beolStack)

      evUseInstFill = getShellEnvVar("SELECT_INST_FILL")
      setShellEnvVar("SELECT_INST_FILL" useInstFill)
   
      evUseCritNet = getShellEnvVar("SELECT_CRITICAL_NET_FEATURE")
      setShellEnvVar("SELECT_CRITICAL_NET_FEATURE" critNet)

      evCritNetFile = getShellEnvVar("CRITICAL_NET_FILE")
      if(critNetFile != "" then
         setShellEnvVar("CRITICAL_NET_FILE" critNetFile)
      )

      evFillEdgeHalo = getShellEnvVar("FILL_EDGE_HALO")
      setShellEnvVar("FILL_EDGE_HALO" fillEdgeHalo)         

      ;; Run ipvsCreateFill
      if(outLib == "" then
         fill = ipvsCreateFill(rule_File ruleMap_File ?layerMap layerMap_File
            ?objectMap objectMap_File ?libName lib ?cellName cell)
         when(fill == ""
            printf("PVSFill: ipvsCreateFill returned \"\".  Please verify ")
            printf("the runset options are correct and re-run.\n")
            return()
         )
         fillCvName = get_string(concat(fill "_" cell))
         inst = setof(inst cellId~>instances inst~>cellName == fillCvName )
         when(inst && inst != list(nil)
            instXY = car(inst)~>xy 
            dbDeleteObject(car(inst))
         )
         fillCV = dbOpenCellViewByType(lib fillCvName "layout")
      else
         fill = ipvsCreateFill(rule_File ruleMap_File ?layerMap layerMap_File
            ?objectMap objectMap_File ?fillLibName outLib )
         when(fill == ""
            printf("PVSFill: ipvsCreateFill returned \"\".  Please verify ")
            printf("the runset options are correct and re-run.\n")
            return()
         )
         fillCvName = get_string(concat(fill "_" cell))
         inst = setof(inst cellId~>instances inst~>cellName == fillCvName )
         when(inst && inst != list(nil)
            instXY = car(inst)~>xy 
            dbDeleteObject(car(inst))
         )
         fillCV = dbOpenCellViewByType(outLib fillCvName "layout")
      ) ;if 

      ;  point_cv = centerBox(cellId~>bBox)
      ;  dbSave(fillCV)

      n = 1

      lppShapes1 = car(setof(lpp fillCV~>layerPurposePairs
         lpp~>layerName == "designFlow" && lpp~>purpose == "drawing" ))~>shapes

      foreach(shp lppShapes1
         w = xCoord(upperRight(shp~>bBox)) - xCoord(lowerLeft(shp~>bBox))
         l = yCoord(upperRight(shp~>bBox)) - yCoord(lowerLeft(shp~>bBox))
         point = centerBox(shp~>bBox)
         x = xCoord(point) - (w/2)
         y = yCoord(point) - (l/2)
         instId = dbOpenCellViewByType(lib fillCell1 "layout" nil "r") 
         unless(instId
            ;; No fill cell in the current library
            printf("PVSFill: Fill cell %s does not exist in " fillCell1)
            printf("library %s, please copy the fill cells to this " lib)
            printf("library and re-run.\n")
            return()
         )
         instName = get_string(concat("I_" n))
         inst = dbCreateInst(fillCV instId instName list(x y) "R0") 
         n = n + 1
         ;dbDeleteObject(shp)
      ) ; foreach

      if(fillCell2 != "" then
         lppShapes2 = car( setof( lpp fillCV~>layerPurposePairs
            lpp~>layerName == "designFlow" && 
            lpp~>purpose == "drawing2" ))~>shapes
         foreach(shp lppShapes2
            w = xCoord(upperRight(shp~>bBox)) - xCoord(lowerLeft(shp~>bBox))
            l = yCoord(upperRight(shp~>bBox)) - yCoord(lowerLeft(shp~>bBox))
            point = centerBox(shp~>bBox)
            x = xCoord(point) - (w/2)
            y = yCoord(point) - (l/2)
            instId = dbOpenCellViewByType(lib fillCell2 "layout" nil "r")
            unless(instId
               ;; No fill cell in the current library
               printf("PVSFill: Fill cell %s does not exist in " fillCell2)
               printf("library %s, please copy the fill cells to this " lib)
               printf("library and re-run.\n")
               return()
            )
            instName = get_string(concat("I_" n))
            inst = dbCreateInst(fillCV instId instName list(x y) "R0") 
            n = n + 1
            ;dbDeleteObject(shp)
         ) ; foreach
      ); if

      dbSave(fillCV)
      point_cv = centerBox(cellId~>bBox)
      if(outLib == "" then
         fillInstId = dbOpenCellViewByType(lib fillCvName "layout" nil "r")
      else
         fillInstId = dbOpenCellViewByType(outLib fillCvName "layout" nil "r")
      )
      fillInst = dbCreateInst(cellId fillInstId instName point_cv "R0")
      fillInst~>xy = instXY 
      ;dbSave(cellId)
      dbClose(fillInstId)

      ;; Reset environment variables
      if(evDesignType then
         setShellEnvVar("DESIGN_TYPE" evDesignType)
      else
         unsetShellEnvVar("DESIGN_TYPE")
      )
      if(evBoundary   then
         setShellEnvVar("SELECT_PRBOUNDARY" evBoundary) 
      else
         unsetShellEnvVar("SELECT_PRBOUNDARY")
      )
      if(evBeolStack then
         setShellEnvVar("BEOL_STACK" evBeolStack)
      else
         unsetShellEnvVar("BEOL_STACK")
      )
      if(evUseInstFill then
         setShellEnvVar("SELECT_INST_FILL" evUseInstFill)
      else
         unsetShellEnvVar("SELECT_INST_FILL")
      )
      if(evUseCritNet  then
         setShellEnvVar("SELECT_CRITICAL_NET_FEATURE" evUseCritNet)
      else
         unsetShellEnvVar("SELECT_CRITICAL_NET_FEATURE")
      ) 
      if(evCritNetFile then
         setShellEnvVar("CRITICAL_NET_FILE" evCritNetFile)
      else
         unsetShellEnvVar("CRITICAL_NET_FILE")
      ) 
      if(evFillEdgeHalo then
         setShellEnvVar("FILL_EDGE_HALO" evFillEdgeHalo)
      else
         unsetShellEnvVar("FILL_EDGE_HALO")
      ) 
         
   ); prog
); procedure

;; Procedure to create Application form
procedure(VCADGenPvsRunFillForm()
   let((cv libName_Fill cellName_Fill outLib_Fill pathRuleFile_Fill 
        pathMapFile_Fill pathOMapFile_Fill fillcell1_Fill fillcell2_Fill 
        designType prBoundary instFill critNet critNetFile fillEdgeHalo 
        beolStack pathRuleMapFile_Fill libName cellName ruleFile ruleMap
        lmapFile omapFile gpdkInstallDir pvsRunFillForm)

      cv = geGetWindowCellView()
      if(cv then
         libName = cv~>libName
         cellName = cv~>cellName
      else
         libName = ""
         cellName = ""
      )

      gpdkInstallDir = getShellEnvVar("GPDK_INSTALL_DIR")
      if(gpdkInstallDir then
         ruleFile = strcat(gpdkInstallDir "/fill/StdFill_V05.pvl")
         ruleMap  = strcat(gpdkInstallDir "/fill/Include/fill_rule.map")
         lmapFile = strcat(gpdkInstallDir "/fill/StdFill_V05.lmap")
         omapFile = strcat(gpdkInstallDir "/fill/StdFill_V05.omap")
      else
         ruleFile = "" 
         ruleMap  = "" 
         lmapFile = "" 
         omapFile = "" 
      )

      if(!boundp('pvsRunFillForm) || (pvsRunFillForm == nil) then
         libName_Fill = hiCreateStringField(
            ?name     'libName_Fill
            ?prompt   "Input Library:"
            ?value    libName 
            )
         cellName_Fill = hiCreateStringField(
            ?name     'cellName_Fill
            ?prompt   "Cell Name:"
            ?value    cellName
            )
         outLib_Fill = hiCreateStringField(
            ?name 'outLib_Fill
            ?prompt "Output Library:"
            ?value ""
            )
         pathRuleFile_Fill = hiCreateStringField(
            ?name     'pathRuleFile_Fill
            ?prompt   "Path to PVS FILL rule file:"
            ?value    ruleFile
            )
         pathRuleMapFile_Fill = hiCreateStringField(
            ?name     'pathRuleMapFile_Fill
            ?prompt   "Path to Rule Map File:"
            ?value    ruleMap
            )
         pathMapFile_Fill = hiCreateStringField(
            ?name     'pathMapFile_Fill
            ?prompt   "Path to Layer Map file:"
            ?value    lmapFile
            )
         pathOMapFile_Fill = hiCreateStringField(
            ?name     'pathOMapFile_Fill
            ?prompt   "Path to Object Map file:"
            ?value    omapFile
            )
         instFill = hiCreateCyclicField(
            ?name     'instFill
            ?prompt   "Use Instance Fill"
            ?choices  list("YES" "NO")
            ?value    "YES"
            )
         fillcell1_Fill = hiCreateStringField(
            ?name     'fillcell1_Fill
            ?prompt   "Fill Cell1:"
            ?value    "fillcell_n1"
            )
         fillcell2_Fill = hiCreateStringField(
            ?name     'fillcell2_Fill
            ?prompt   "Fill Cell2:"
            ?value    "fillcell_p1"
            )
         designType = hiCreateCyclicField(
            ?name     'designType
            ?prompt   "Design Type:"
            ?choices  list("CHIP" "CELL")
            ?value    "CELL"
            )
         prBoundary = hiCreateCyclicField(
            ?name     'prBoundary
            ?prompt   "Boundary:"
            ?choices  list("prBoundary" "data extents")
            ?value    "prBoundary"
            )
         fillEdgeHalo = hiCreateStringField(
            ?name     'fillEdgeHalo
            ?prompt   "Fill Edge Halo:"
            ?value    "0.0" 
            )
         critNet = hiCreateCyclicField(
            ?name     'critNet
            ?prompt   "Use Critical Net Feature"
            ?choices  list("YES" "NO")
            ?value    "YES"
            )
         critNetFile = hiCreateStringField(
            ?name     'critNetFile
            ?prompt   "Critical Net Spacings:"
            ?value    "" 
            )
         beolStack = hiCreateCyclicField(
            ?name     'beolStack
            ?prompt   "Metal Stack:"
            ?choices  list("8M_7Mx_MT" "10M_9Mx_MT")
            ?value    "8M_7Mx_MT"
            )
         pvsRunFillForm =  hiCreateAppForm(
            ?name 'pvsRunFillForm
            ?formTitle "Cadence PVS: ipvsCreateFill Form"
            ?fields list(
               list(libName_Fill         0:0   300:30 150)
               list(cellName_Fill        0:30  300:30 150)
               list(outLib_Fill          0:60  300:30 150)
               list(pathRuleFile_Fill    0:90  300:30 150)
               list(pathRuleMapFile_Fill 0:120 300:30 150)
               list(pathMapFile_Fill     0:150 300:30 150)
               list(pathOMapFile_Fill    0:180 300:30 150)
               list(instFill             0:210 300:30 150)
               list(fillcell1_Fill       0:240 300:30 150)
               list(fillcell2_Fill       0:270 300:30 150)
               list(designType           0:300 300:30 150)
               list(prBoundary           0:330 300:30 150)
               list(critNet              0:360 300:30 150)
               list(critNetFile          0:390 300:30 150)
               list(fillEdgeHalo         0:420 300:30 150)
               list(beolStack            0:450 300:30 150)
               )
            ?callback "ipvsRunFill(libName_Fill->value cellName_Fill->value outLib_Fill->value pathRuleFile_Fill->value pathRuleMapFile_Fill->value pathMapFile_Fill->value pathOMapFile_Fill->value instFill->value fillcell1_Fill->value fillcell2_Fill->value designType->value prBoundary->value critNet->value critNetFile->value fillEdgeHalo->value beolStack->value )"
            )
      ) ;if

      pvsRunFillForm 
      hiDisplayForm(pvsRunFillForm 375:475)

   ) ;let
) ;procedure_VCADGenPvsRunFillForm

procedure(VCADCreateFillPDMenu()
   if(boundp('CCSLayoutPulldownMenu) then 
      CCSLayoutPulldownMenu
   else
      hiCreatePulldownMenu(
         'CCSLayoutPulldownMenu
         "ipvsCreateFill"
         list(hiCreateMenuItem(
            ?name 'pvsRunFill
            ?itemText "Run Standard Fill"
            ?callback  "VCADGenPvsRunFillForm()" 
            )
         ) ;list
      ) ;hiCreatePulldownMenu
   ) ;if
) ;procedure

procedure(CCSUserPostInstallTrigger(args)
   hiInsertBannerMenu(
      args->window
      VCADCreateFillPDMenu()
      length(hiGetBannerMenus(args->window))
   ) ;hiInsertBannerMenu
) ;procedure

;; Triggers for adding it to layout and VXL window
deRegUserTriggers("maskLayout" nil nil 'CCSUserPostInstallTrigger)
deRegUserTriggers("maskLayoutXL" nil nil 'CCSUserPostInstallTrigger)
