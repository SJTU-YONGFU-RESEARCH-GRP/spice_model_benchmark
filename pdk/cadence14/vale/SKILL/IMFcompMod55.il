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
   2018-04-19 JF Initial Coding for WSPFill 
   2018-07-31 JF Updated Component Module based on MVS18.10 code efficiency 
                 enhancements: Changes 180724a 180724b 180724c 180724d 180725a
                 180725b 180725c

*/


procedure(IMFcompMod55(
             rtDpl
          @optional 
             (debug nil)
          )
   prog((cv erv erv2 currentTime stamp wspToShapesCvNm wspToShapesCv instName
         selectedRules control outputDpl ruleset lyrsmap objsmap e3)

      printf("VALE INFO: Creating %L as %L %L ...\n" rtDpl->name 
         rtDpl->outputStyle rtDpl->outputLocation) 

      cv = geGetWindowCellView()
      unless(cv
         printf("VALE ERROR: Unable to find an active layout window. ")
         printf("Please locate or open a layout window and try again.\n")
         return()
      )

      ;; Turn off Layer Palette Object Markers
      leSetObjectVisible("Markers" nil)
      IMFcompMod55LayerPaletteChanges()

      ;; Start core Component Module function
      ;; Create a temporary cellview
      currentTime = parseString(getCurrentTime() " ")
      rexCompile(":")
      stamp = rexReplace(caddr(currentTime) "" 0)
      wspToShapesCvNm = strcat(cv~>cellName "_temp" stamp)
      when(debug printf("VALE DEBUG: Temporary cellview name is %s.\n"
         wspToShapesCvNm))
      wspToShapesCv = dbOpenCellViewByType(cv~>libName wspToShapesCvNm
         "layout" "maskLayout" "w")
      unless(dbobjectp(wspToShapesCv)
         printf("VALE ERROR: Failed to open a temporary %s cell.\n" rtDpl->name)
         _IMFcmReturn(cv rtDpl "reset" debug)
         return()
      )

      ;; Instantiate the current cellview in the temporary cellview
      ;; pvsCv is used to capture shapes in a CheckCell as well
      instName = strcat("I" rtDpl->topCv~>cellName)
      erv = errset(dbCreateInstByMasterName(wspToShapesCv rtDpl->topCv~>libName
         rtDpl->topCv~>cellName "layout" instName 0:0 "R0") )
      if(erv then
         when(erv == list(nil)
            printf("VALE ERROR: Failed to create the instance of the Overlay ")
            printf("cellView %s\n" rtDpl->topCv~>cellName)
            _IMFcmReturn(cv rtDpl "reset" debug)
            return()
         )
      else
         printf("VALE ERROR: A problem occurred creating an instance of the ")
         printf("Overlay cellView %s\n%L\n" rtDpl->topCv~>cellName
            errset.errset)
         _IMFcmReturn(cv rtDpl "reset" debug)
         return()
      )
         
      ;; Convert the WSP to Shapes
      ;; Use cv as the source cellview because that is where the WSPs are
      ;; If not defined, loadContext
      unless(_IMFwspToShapes(?cv cv ?outCv wspToShapesCv ?setColor nil
         ?debug debug)
         ;; Remove the temporary cellview
         errset(ddDeleteObj(
            ddGetObj(wspToShapesCv~>libName wspToShapesCv~>cellName))
         )
         _IMFcmReturn(cv rtDpl "reset" debug)
         return()
      )

      if(rtDpl->showAllMarkers then
         selectedRules = list(
            "gen-M1-TFILL-1-fill"
            "gen-M1-TFILL-2-fill"
            "gen-M1-TFILL-1-drawing"
            "gen-M1-TFILL-2-drawing"
            "mrk-M2-TFILL--jog"
            "mrk-M2-TFILL--color_conflict"
            "mrk-M2-TFILL--trim_outside_WSP_area"
            "gen-M2-TFILL-1-fill"
            "gen-M2-TFILL-2-fill"
            "gen-M2-TFILL-1-drawing"
            "gen-M2-TFILL-2-drawing"
            "mrk-M3-TFILL--jog"
            "mrk-M3-TFILL--color_conflict"
            "mrk-M3-TFILL--trim_outside_WSP_area"
            "gen-M3-TFILL-1-fill"
            "gen-M3-TFILL-2-fill"
            "gen-M3-TFILL-1-drawing"
            "gen-M3-TFILL-2-drawing"
            "gen-M4-TFILL--fill"
            "gen-M5-TFILL--fill"
         )
      else
         selectedRules = list(
            "gen-M1-TFILL-1-fill"
            "gen-M1-TFILL-2-fill"
            "gen-M1-TFILL-1-drawing"
            "gen-M1-TFILL-2-drawing"
            "gen-M2-TFILL-1-fill"
            "gen-M2-TFILL-2-fill"
            "gen-M2-TFILL-1-drawing"
            "gen-M2-TFILL-2-drawing"
            "gen-M3-TFILL-1-fill"
            "gen-M3-TFILL-2-fill"
            "gen-M3-TFILL-1-drawing"
            "gen-M3-TFILL-2-drawing"
            "gen-M4-TFILL--fill"
            "gen-M5-TFILL--fill"
         )
      )

      ;; Set up call to PVS or Pegasus
      unless(_IMFsetupPV()
         return()
      )
      outputDpl = nil
      control = list(nil 'area wspToShapesCv~>bBox
                         'enableColoring t
                         'abortOnLayoutError nil
                         'excludeCells ""
                         'ruleSet selectedRules
                    )

      ;; Get the include file paths
      ruleset = _IMFgetIncludeFile(cv rtDpl ".pvl" debug)
      unless(ruleset return())
      lyrsmap = _IMFgetIncludeFile(cv rtDpl ".lmap" debug)
      unless(lyrsmap return())
      objsmap = ""

      when(debug
         printf("VALE DEBUG: Running PVS or Pegasus on cell %s.\n"
            rtDpl->topCv~>cellName)
         printf("VALE DEBUG: Running ruleset %s...\n" ruleset)
      )

      ;; Call PVS or Pegasus
      ;; Try Pegasus
      erv = errset(pgssDRC(wspToShapesCv ruleset lyrsmap objsmap control
         lambda((shape) outputDpl=cons(shape outputDpl) t) ) ) 
      if(erv then
         when(erv == list(nil)
            ;; Try PVS
            e3 = errset(pvsApplyDRC(wspToShapesCv ruleset lyrsmap objsmap
               control lambda((shape) outputDpl=cons(shape outputDpl) t)))
            if(e3 then
               if(e3 == list(nil) then 
                  printf("VALE ERROR: The shapes analysis returned nil. No ")
                  printf("results will be generated for %s\n" rtDpl->name)
                  ;; No luck, clean up temporary cellview
                  erv2 = errset(ddDeleteObj(dbGetCellViewDdId(wspToShapesCv)))
                  if(erv2 then
                     when(erv2 == list(nil)
                        printf("VALE ERROR: Failed to delete the temporary ")
                        printf("cellview %s, please use the Library Manager "
                           wspToShapesCvNm)
                        printf("to delete this cellview.\n")
                     )
                     ;; Deletion complete
                  else
                     printf("VALE ERROR: A problem occurred deleting the ")
                     printf("temporary cellview %s, please use the Library "
                        wspToShapesCvNm)
                     printf("Manager to delete it. %L\n" errset.errset)
                  )
                  _IMFcmReturn(cv rtDpl "reset" debug)
                  return()
               )
               ;; All good pvsApplyDRC, main flow
            else
               printf("VALE ERROR: A problem occurred in the shape analysis, ")
               printf("No results were generated for %s. %L\n" rtDpl->name
                  errset.errset)
               _IMFcmReturn(cv rtDpl "reset" debug)
               return()
            )
         ) ;when pgssDRC returns nil
         ;; All good pgssDRC, main flow
      else
         printf("VALE ERROR: A problem occurred in pgssDRC. No results ")
         printf("were generated for %s. %L\n" rtDpl->name errset.errset)
         erv2 = errset(ddDeleteObj(dbGetCellViewDdId(wspToShapesCv)))
         if(erv2 then
            when(erv2 == list(nil)
               printf("VALE ERROR: Failed to delete the temporary cellview ")
               printf("%s, please use the Library Manager " wspToShapesCvNm)
               printf("to delete this cellview.\n")
            )
         else
            printf("VALE ERROR: A problem occurred deleting the temporary ")
            printf("cellview %s, please use the Library " wspToShapesCvNm)
            printf("Manager to delete this cellview.\n")
         )
         _IMFcmReturn(cv rtDpl "reset" debug)
         return()
      )

      when(debug
         printf("VALE DEBUG: PV complete.\n")
      )
      ;; Delete the temporary cellview
      erv = errset(
         ddDeleteObj(dbGetCellViewDdId(wspToShapesCv))
      )
      unless(erv
         printf("VALE ERROR: Failed to delete the temporary WSP cellview. ")
         printf("VALE will continue, but check the libarary for this cellview ")
         printf("when IMF completes: %s.\n" wspToShapesCvNm)
         ;; no return necessary
      )

      ;; Process the return shapes from PV
      erv = errset(_IMFprocessRunsetResults(cv rtDpl outputDpl nil debug))
      if(erv then
         when(erv == list(nil)
            printf("VALE ERROR: Exiting runset results processing due to ")
            printf("previous error.\n ")
            return()
         )
      else
            printf("VALE ERROR: Exiting runset results processing due to ")
            printf("previous problem.\n%L\n" errset.errset)
            _IMFcmReturn(cv rtDpl "reset" debug)
            return()
      )
     
      printf("VALE INFO: %s complete.\n" rtDpl->name)
      return(t)
   )
)

procedure(IMFcompMod55LayerPaletteChanges()
   pteShowRoutingLPP(nil)
   pteShowUsedLPP(nil)
   pteShowValidLPP(nil)
   pteSetValidity("prBoundary drawing"  t "Layers")
   pteSetValidity("prBoundary boundary" t "Layers")
   pteSetValidity("M3 fill"             t "Layers")
   pteSetValidity("M4 fill"             t "Layers")
   pteSetValidity("M5 fill"             t "Layers")
   pteSetValidity("M6 fill"             t "Layers")
   pteSetValidity("M7 fill"             t "Layers")
   pteSetValidity("MT fill"             t "Layers")
   pteShowValidLPP(t)
)
