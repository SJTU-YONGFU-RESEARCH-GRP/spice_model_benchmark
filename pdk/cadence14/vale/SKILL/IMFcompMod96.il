/*
 |-----------------------------------------------------------------------|
 |                                                                       |
 |      _               Copyright (c) 2019                               |
 |    c a d e n c e     Cadence Design Systems, Inc.                     |
 |                      Cadence VCAD IP Component                        |
 |                      All Rights Reserved                              |
 |                                                                       |
 |                                                                       |
 | THIS IS UNPUBLISHED PROPRIETARY SOURCE CODE OF CADENCE DESIGN SYSTEMS |
 | The copyright notice above does not evidence any actual or intended   |
 | publication of such source code.                                      |
 |                                                                       |
 | This source code and any other accompanying code ("Code") is          |
 | Cadence's Intellectual Property.                                      |
 |                                                                       |
 | This Code remains Cadence intellectual property and may under no      |
 | circumstances be given to third parties, neither in original nor in   |
 | modified versions, without Cadence's explicit written permission.     |
 |                                                                       |
 | PROPRIETARY INFORMATION, PROPERTY OF CADENCE DESIGN SYSTEMS, INC.     |
 |                                                                       |
 | The code may require modification to satisfy the requirements of any  |
 | user. The code and any modifications to the code may not be           |
 | compatible with current or future versions of Cadence products. THE   |
 | CODE IS PROVIDED "AS IS" AND WITH NO WARRANTIES, INCLUDING WITHOUT    |
 | LIMITATION ANY EXPRESS WARRANTIES OR IMPLIED WARRANTIES OF            |
 | MERCHANTABILITY OR FITNESS FOR A PARTICULAR USE.                      |
 |                                                                       |
 |-----------------------------------------------------------------------|
*/

/*
   Revision log:
   190613 JF New GPDK Standard Fill Flow with Layer Selection
   191119 JF Updated how the PDK fill deck is called
   200324 JF Scripting simplifications 
   2020-05-05 JF Changed PV call to _IMFrunPV() helper function

*/

procedure(VALEcompMod96LayerMapping(layer)
   prog((ruleNames)
      ruleNames = case(layer
         ("Poly"      list("gen-Poly-FILL--fill" 
                           "mrk-Poly-FILL--fillcell_n1"
                           "mrk-Poly-FILL--fillcell_p1"))
         ("M1"        list("gen-M1-FILL-1-fill" "gen-M1-FILL-2-fill"))
         ("M2"        list("gen-M2-FILL-1-fill" "gen-M2-FILL-2-fill"))
         ("M3"        list("gen-M3-FILL-1-fill" "gen-M3-FILL-2-fill"))
         ("M4"        list("gen-M4-FILL--fill"))
         ("M5"        list("gen-M5-FILL--fill"))
         ("M6"        list("gen-M6-FILL--fill"))
         ("M7"        list("gen-M7-FILL--fill"))
         ("MT"        list("gen-MT-FILL--fill"))
         (t           list("gen-M1-FILL-1-fill" "gen-M1-FILL-2-fill"))
      )
      return(ruleNames)
   )
)

procedure(IMFcompMod96(rtDpl @optional (debug nil))
   prog((fillLayers form96)

      printf("VALE INFO: Creating %L as %L %L ...\n" rtDpl->name 
         rtDpl->outputStyle rtDpl->outputLocation) 

      ;; Environment Variables specific to this Component Module
      VALEcompMod96EnvVars(rtDpl)

      ;; Set default fill layers if NOT set in the config file
      fillLayers = parseString(rtDpl->envVars->VALE_FILL_LAYERS)
      unless(fillLayers
         fillLayers = list("Poly" "M1" "M2" "M3" "M4" "M5" "M6" "M7" "MT")
      )

      ;; Create Layer Selection UI
      form96 = hiCreateAppForm(
         ?name 'VALEcm96ListBoxForm
         ?fields list(
            list(hiCreateListBoxField(
               ?name 'VALEcm96ListBox
               ?prompt "Multi-select Layer(s)\nfor Standard Fill:"
               ?choices fillLayers 
               ?multipleSelect t
            )
            10:10 260:270 120)
         )
         ?formTitle "Create Standard Fill"
         ?attachmentList list(
            bor(hicTopPercentSet hicLeftPercentSet hicRightPercentSet
               hicBottomPercentSet)
         )
         ?callback strcat("VALEcompMod96CB(rtDpl " 
            "VALEcm96ListBoxForm->VALEcm96ListBox->value debug)")
         ?initialSize list(270 290)
      )
      hiDisplayForm(form96)

      return(t)
   )
)

procedure(VALEcompMod96CB(rtDpl selectedLayers debug)
   prog((cv erv fillLayerSwitch selectedRules ruleNames)

      cv = rtDpl->topCv

      ;; Enable switches in the deck from layer selection in the UI
      foreach(layer selectedLayers
         fillLayerSwitch = strcat("FILL_" layer)
         setShellEnvVar(fillLayerSwitch "YES")
         ruleNames = VALEcompMod96LayerMapping(layer)
         selectedRules = append(ruleNames selectedRules)
      )

      ;; PART 1 Run
      ;; RUN PVS or PEGASUS depending on which technology node
      erv = errset(_IMFrunPV(rtDpl cv selectedRules debug))
      if(erv then
         when(erv == list(nil)
            printf("VALE ERROR: Failed to run PV.\n")
            _IMFcmReturn(cv rtDpl "reset" debug)
            return()
         )
      else
         printf("VALE ERROR: A problem occurred running PV:\n%s\n"
            errset.errset)
         _IMFcmReturn(cv rtDpl "reset" debug)
         return()
      )

      ;; PART 2 Post process
      ;; Post-process step for instance-based fill
      erv = errset(VALEcompMod96PostProcess(cv rtDpl debug))
      if(erv then
         if(erv == list(nil) then
            printf("VALE ERROR: Post-processing failed for %s, " rtDpl->name)
            printf("partial results may exist in the design.\n")
         else
            when(debug
                printf("VALE DEBUG: Post-processing completed successfully.\n")
            )
         )
      else
         printf("VALE ERROR: A problem occurred in post-processing, ")
         printf("partial results may exist in the design.\n%L\n" errset.errset)
      )

      ;; PART 3 Clean-up
      ;; Clear environment variables for this compMod
      unsetShellEnvVar("SELECT_IN_DESIGN_FLOW")
      unsetShellEnvVar("BEOL_STACK")
      unsetShellEnvVar("SELECT_PRBOUNDARY")
      unsetShellEnvVar("SELECT_EXTERNAL_INST_FILL")
      unsetShellEnvVar("SELECT_INST_FILL")
      unsetShellEnvVar("SELECT_CRITICAL_NET_FEATURE")
      ;unsetShellEnvVar("DESIGN_TYPE")
      ;unsetShellEnvVar("LAYOUT_SYSTEM")
      ;unsetShellEnvVar("OUTPUT_LAYOUT")
      ;unsetShellEnvVar("CRITICAL_NET_FILE")
      unsetShellEnvVar("CRITICAL_NET_FILE")
      unsetShellEnvVar("FILL_EDGE_HALO")

      foreach(layer selectedLayers 
         fillLayerSwitch = strcat("FILL_" layer)
         unsetShellEnvVar(fillLayerSwitch)
      ); foreach

      printf("VALE INFO: %s complete.\n" rtDpl->name)
      return(t)
   )
)

procedure(VALEcompMod96EnvVars(rtDpl)
   ;; Turn off Layer Palette Object Markers
   leSetObjectVisible("Markers" nil)
   
   ;; Default for SELECT_IN_DESIGN_FLOW is FALSE
   setShellEnvVar("SELECT_IN_DESIGN_FLOW" "TRUE")

   if(rtDpl->envVars->VALE_BEOL_STACK then
      setShellEnvVar("BEOL_STACK" rtDpl->envVars->VALE_BEOL_STACK)
   else
      ;; Default for BEOL_STACK is 8M_7Mx_MT
      setShellEnvVar("BEOL_STACK" "8M_7Mx_MT")
   )

   if(rtDpl->envVars->VALE_SELECT_PRBOUNDARY then
      setShellEnvVar("SELECT_PRBOUNDARY"
         rtDpl->envVars->VALE_SELECT_PRBOUNDARY)
   else
      ;; Default for SELECT_PRBOUNDARY is TRUE
      setShellEnvVar("SELECT_PRBOUNDARY" "TRUE")
   )

   if(rtDpl->envVars->VALE_SELECT_INST_FILL then
      setShellEnvVar("SELECT_INST_FILL"
         rtDpl->envVars->VALE_SELECT_INST_FILL)
   else
      ;; Default for SELECT_INST_FILL is FALSE
      unsetShellEnvVar("SELECT_INST_FILL")
   )

   ;; Default for DESIGN_TYPE is CELL
   ;;setShellEnvVar("DESIGN_TYPE"       "CELL")
   ;; Default for LAYOUT_SYSTEM is GDSII
   ;;setShellEnvVar("LAYOUT_SYSTEM"     "GDSII")
   ;; Default for OUTPUT_LAYOUT is GDSII
   ;;setShellEnvVar("OUTPUT_LAYOUT"     "GDSII")

   if(rtDpl->envVars->VALE_SELECT_CRITICAL_NET_FEATURE then
      setShellEnvVar("SELECT_CRITICAL_NET_FEATURE"
         rtDpl->envVars->VALE_SELECT_CRITICAL_NET_FEATURE)
      ;; Default for CRITICAL_NET_FILE is unset
      when(rtDpl->envVars->VALE_CRITICAL_NET_FILE
         setShellEnvVar("CRITICAL_NET_FILE"
            rtDpl->envVars->VALE_CRITICAL_NET_FILE)
      )
   else
      ;; Default for SELECT_CRITICAL_NET_FEATURE is FALSE
      unsetShellEnvVar("SELECT_CRITICAL_NET_FEATURE")
   )
   when(rtDpl->envVars->VALE_FILL_EDGE_HALO
      setShellEnvVar("FILL_EDGE_HALO"
         rtDpl->envVars->VALE_FILL_EDGE_HALO)
   )
)

procedure(VALEcompMod96PostProcess(cv rtDpl debug)
   prog((cellPath lmapPath libCellNameList ppList lDataSet cellName
         markerDpl markerNameList type streamInFile strmInFlag
         streamInMap erv index instObjName)

      ;; Path to include files
      cellPath = _IMFgetIncludeFile(cv rtDpl "VALE_FILL_INST" debug)
      unless(cellPath return())
      lmapPath = _IMFgetIncludeFile(cv rtDpl "VALE_FILL_LMAP" debug)
      unless(lmapPath return())

      ppList = setof(mrkr cv~>markers mrkr~>objType != "ruler" &&
         rexMatchp("fillcell" mrkr~>shortMsg) )
      when(ppList == list(nil)
         return()
      )

      lDataSet = strmInFlag = nil

      foreach(marker ppList
         markerDpl = list(nil)
         markerNameList = parseString(marker~>shortMsg "-" t)
         markerDpl->orient = "R0"
         markerDpl->propTag = rtDpl->name
         cellName  = nth(4 markerNameList)
         unless(cellName
            printf("VALE ERROR: The cellName table does not have a match for ")
            printf("%s, please contact the IMF enablement owner update " type)
            printf("the Component Module post-process SKILL procedure.\n")
            return()
         )

         markerDpl->location = nth(0 marker~>points)
         unless(markerDpl->location
            printf("VALE ERROR: The location table does not have a match for ")
            printf("%s, please contact the IMF enablement owner update " type)
            printf("the Component Module post-process SKILL procedure.\n")
            return()
         )
         markerDpl->origName = cellName
         streamInFile = strcat(cellPath "/" cellName ".gds")
         streamInMap = strcat(lmapPath)

         ;; When the cell already exists, this will be non-nil
         libCellNameList = ddGetObj(cv~>libName)~>cells~>name
         if(rtDpl->stampStreamInCellNames then
            markerDpl->cellName =
               car(rexMatchList(strcat(cellName "_") libCellNameList))
         else
            markerDpl->cellName =
               car(rexMatchList(cellName libCellNameList))
         )
         when(debug
            printf("VALE DEBUG: Found cellName %L " markerDpl->cellName)
            printf("matching %s\n" cellName)
         )

         ;; Import the cell when it is not found  
         unless(markerDpl->cellName
            ;; Stream In
            strmInFlag = t
            erv = errset(
               _IMFstreamInCell(cellName cv~>libName streamInFile streamInMap
                  debug rtDpl->stampStreamInCellNames)
            )
            if(erv then
               if(erv == list(nil) then
                  printf("VALE ERROR: Failed to stream in %s.\n" streamInFile)
                  _IMFcmReturn(cv rtDpl "reset" debug)
                  return()
               else
                  markerDpl->cellName = car(erv)
                  when(debug
                     printf("VALE DEBUG: Cell now named to %s\n" car(erv))
                  )
              )
            else
               printf("VALE ERROR: A problem occurred during stream in.\n")
               printf("%L\n" errset.errset)
               _IMFcmReturn(cv rtDpl "reset" debug)
               return()
            )
         )

         ;; Update the loop list var 
         lDataSet = cons(markerDpl lDataSet)
      )

      when(debug
         printf("VALE DEBUG: Ready to place instances.\n")
      )

      ;; Create instances
      index = 0
      foreach(mdpl lDataSet
         ;; Get the cell dbObject to place
         erv = errset(
            dbOpenCellViewByType(cv~>libName mdpl->cellName "layout"
               "maskLayout" "r")
         )
         if(erv then
            if(erv == list(nil) then
               printf("VALE ERROR: Failed to get the cellview ")
               printf("%s for placement.\n" mdpl->cellName)
               return()
            else
               mdpl->obj = car(erv)
               when(debug
                  printf("VALE DEBUG: Opened %s for read.\n" mdpl->cellName)
               )
            )
         else
            printf("VALE ERROR: A problem occurred accessing the cellview to ")
            printf("place for read - %L\n" mdpl->cellName)
            printf("%L\n" errset.errset)
            _IMFcmReturn(cv rtDpl "reset" debug)
            return()
         )
         when(debug
            printf("VALE DEBUG: dbObject = %L\n" mdpl->obj)
         )

         ;; Create the instance name and call the instance add proc
         when(debug printf("VALE DEBUG: targetCv = %L\n" rtDpl->targetCv))
         sprintf(instObjName "I%s_%d" mdpl->origName index)
         erv = errset(
            _IMFaddInstance(mdpl->cellName mdpl->obj instObjName
               rtDpl->targetCv mdpl->location mdpl->orient mdpl->propTag debug)
         )
         if(erv then
            if(erv == list(nil) then
               printf("VALE ERROR: Failed to add instance %L to " instObjName)
               printf("%L near %L. " rtDpl->targetNm mdpl->location)
               printf("Processing will attempt to continue for any other ")
               printf("instances.\n")
            else
               when(debug
                  printf("VALE DEBUG: Instance %s added to %s\n" instObjName
                     rtDpl->targetNm)
               )
            )
         else
            printf("VALE ERROR: A problem occurred adding instance ")
            printf("%L to %L\n" instObjName rtDpl->targetNm)
            printf("%L\n" errset.errset)
            _IMFcmReturn(cv rtDpl "reset" debug)
            return()
         )
         when(strmInFlag
            dbClose(mdpl->obj)
         )
         index = index + 1
      )

      return(t)
   )
)

