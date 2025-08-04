/*
 |-----------------------------------------------------------------------|
 |                                                                       |
 |      _               Copyright (c) 2018                               |
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
   2018-09-06 JF Initial Coding for StdFill 
   2019-11-19 JF Updated how the PDK fill deck is called 
   2020-03-24 JF Scripting simplification reorganization
   2020-05-05 JF Changed PV call to _IMFrunPV() helper function

*/


procedure(IMFcompMod95(rtDpl @optional (debug nil))
   prog((cv erv fillLayers selectedRules fillLayerSwitch) 

      printf("VALE INFO: Creating %L as %L %L ...\n" rtDpl->name 
         rtDpl->outputStyle rtDpl->outputLocation) 

      cv = rtDpl->topCv 

      VALEcompMod95LayerPaletteChanges()
      VALEcompMod95EnvVars(rtDpl)

      fillLayers = parseString(rtDpl->envVars->VALE_FILL_LAYERS)
      unless(fillLayers
         fillLayers = list("Poly" "M1" "M2" "M3" "M4" "M5" "M6" "M7" "MT")
      )

      foreach(layer fillLayers 
         fillLayerSwitch = strcat("FILL_" layer)
         setShellEnvVar(fillLayerSwitch "YES")
      )

      ;; Setup Layers to bring back from the deck 
      if(rtDpl->showAllMarkers then
         selectedRules = list(
            "mrk-Poly-FILL--initialSizing"
            "mrk-PolyALL-FILL--fillArea1"
            "mrk-PolyALL-FILL--fillArea2"
            "mrk-M2color1-FILL--fillArea1"
            "mrk-M2color2-FILL--fillArea1"
            "mrk-M2color1-FILL--fillArea2"
            "mrk-M2color2-FILL--fillArea2"
            "mrk-M1-FILL--NoColor"
            "mrk-M2-FILL--NoColor"
            "mrk-M3-FILL--NoColor"
            "gen-Poly-FILL--dummy"
            "mrk-Poly-FILL--fillcell_n1"
            "mrk-Poly-FILL--fillcell_p1"
            "gen-M1-FILL-1-fill"
            "gen-M1-FILL-2-fill"
            "gen-M2-FILL-1-fill"
            "gen-M2-FILL-2-fill"
            "gen-M3-FILL-1-fill"
            "gen-M3-FILL-2-fill"
            "gen-M4-FILL--fill"
            "gen-M5-FILL--fill"
            "gen-M6-FILL--fill"
            "gen-M7-FILL--fill"
            "gen-MT-FILL--fill"
         )
      else
         selectedRules = list(
            "mrk-M1-FILL--NoColor"
            "mrk-M2-FILL--NoColor"
            "mrk-M3-FILL--NoColor"
            "gen-Poly-FILL--dummy"
            "mrk-Poly-FILL--fillcell_n1"
            "mrk-Poly-FILL--fillcell_p1"
            "gen-M1-FILL-1-fill"
            "gen-M1-FILL-2-fill"
            "gen-M2-FILL-1-fill"
            "gen-M2-FILL-2-fill"
            "gen-M3-FILL-1-fill"
            "gen-M3-FILL-2-fill"
            "gen-M4-FILL--fill"
            "gen-M5-FILL--fill"
            "gen-M6-FILL--fill"
            "gen-M7-FILL--fill"
            "gen-MT-FILL--fill"
         )
      )

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

      ;; Post-process step
      erv = errset(IMFcompMod95PostProcess(cv rtDpl debug))
      if(erv then
         if(erv == list(nil) then
            printf("VALE ERROR: Post-processing failed for %s, " rtDpl->name)
            printf("partial results may exist in the design.\n")
         else
            when(debug
                printf("VALE INFO: Post-processing completed successfully.\n")
            )
         )
      else
         printf("VALE ERROR: A problem occurred in post-processing, ")
         printf("partial results may exist in the design.\n%L\n" errset.errset)
      )

      ;; Clear environment variables for this compMod
      unsetShellEnvVar("SELECT_IN_DESIGN_FLOW")
      unsetShellEnvVar("BEOL_STACK")
      unsetShellEnvVar("SELECT_PRBOUNDARY")
      ;unsetShellEnvVar("SELECT_EXTERNAL_INST_FILL")
      unsetShellEnvVar("SELECT_INST_FILL")
      unsetShellEnvVar("SELECT_CRITICAL_NET_FEATURE")
      ;unsetShellEnvVar("DESIGN_TYPE")
      ;unsetShellEnvVar("LAYOUT_SYSTEM")
      ;unsetShellEnvVar("OUTPUT_LAYOUT")
      ;unsetShellEnvVar("CRITICAL_NET_FILE") 
      unsetShellEnvVar("CRITICAL_NET_FILE")
      unsetShellEnvVar("FILL_EDGE_HALO")

      foreach(layer fillLayers 
         fillLayerSwitch = strcat("FILL_" layer)
         unsetShellEnvVar(fillLayerSwitch)
      )

      printf("VALE INFO: %s complete.\n" rtDpl->name)
      return(t)
   )
)

procedure(IMFcompMod95PostProcess(cv rtDpl debug)
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

procedure(VALEcompMod95LayerPaletteChanges()
   pteShowRoutingLPP(nil)
   pteShowUsedLPP(nil)
   pteShowValidLPP(nil)
   pteSetValidity("prBoundary drawing"  t "Layers")
   pteSetValidity("prBoundary boundary" t "Layers")
   pteSetValidity("designFlow drawing"  t "Layers")
   pteSetValidity("designFlow drawing2" t "Layers")
   pteSetValidity("M3 fill"             t "Layers")
   pteSetValidity("M4 fill"             t "Layers")
   pteSetValidity("M5 fill"             t "Layers")
   pteSetValidity("M6 fill"             t "Layers")
   pteSetValidity("M7 fill"             t "Layers")
   pteSetValidity("MT fill"             t "Layers")
   pteShowValidLPP(t)

   ;; Turn off Layer Palette Object Markers
   leSetObjectVisible("Markers" nil)
)


procedure(VALEcompMod95EnvVars(rtDpl)
   
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

