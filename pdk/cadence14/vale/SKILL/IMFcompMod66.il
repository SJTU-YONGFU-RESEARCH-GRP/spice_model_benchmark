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
   2018-10-08 JF Initial Coding for V3 decomposition
   2020-05-05 JF Update to use pgssDRC or pvsApplyDRC

*/


procedure(proceduriIMFcompMod66(
             rtDpl
          @optional 
             (debug nil)
          )
   prog((cv erv e2 newBox
         selectedRules control outputDpl ruleset lyrsmap objsmap)

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

      ;; Environment Variables specific to this Component Module

      ;; Start core Component Module function
      if(rtDpl->showAllMarkers then
         selectedRules = list(
            "mrk-V3-DECOMP--link_SP2"
            "gen-V3-DECOMP-1-drawing"
            "gen-V3-DECOMP-2-drawing"
            "gen-V3-DECOMP-3-drawing"
         )
      else
         selectedRules = list(
            "gen-V3-DECOMP-1-drawing"
            "gen-V3-DECOMP-2-drawing"
            "gen-V3-DECOMP-3-drawing"
         )
      )

      ;; Set up call to PVS or Pegasus
      unless(_IMFsetupPV()
         return()
      )
      outputDpl = nil
      newBox = _IMFexpandVIPVSBox(rtDpl->topCv~>bBox 0.5)
      control = list(nil 'area newBox
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
         printf("VALE DEBUG: Running Pegasus or PVS on cell %s.\n"
            rtDpl->topCv~>cellName)
         printf("VALE DEBUG: Running ruleset %s...\n" ruleset)
      )

      ;; Call Pegasus or PVS
      erv = errset(pgssDRC(rtDpl->topCv ruleset lyrsmap objsmap control
         lambda((shape) outputDpl=cons(shape outputDpl) t)))
      if(erv then
         when(erv == list(nil)
            ;; Attempt to use pvsApplyDRC if pgssDRC is not available
            e2 = errset(pvsApplyDRC(rtDpl->topCv ruleset lyrsmap objsmap
               control lambda((shape) outputDpl=cons(shape outputDpl) t)))
            if(e2 then
               when(e2 == list(nil)
                  printf("VALE ERROR: The shapes processing failed to run, no ")
                  printf("results were generated for %s.\n" rtDpl->name)
                  _IMFcmReturn(cv rtDpl "reset" debug)
                  return()
               )
               ;; pvsApplyDRC was successful
            else
               printf("VALE ERROR: A problem occurred in pvsApplyDRC. No ")
               printf("results were generated for %s: %L\n" rtDpl->name
                  errset.errset)
               _IMFcmReturn(cv rtDpl "reset" debug)
               return()
            )
         )
         ;; pgssDRC was successful
      else
         printf("VALE ERROR: A problem occurred in pgssDRC. No results ")
         printf("will be generated for %s: %L\n" rtDpl->name errset.errset)
         _IMFcmReturn(cv rtDpl "reset" debug)
         return()
      )
      when(debug printf("VALE DEBUG: shapes processing complete.\n"))

      ;; Process the returned shapes
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

      ;; Save secondary cellviews
      when(rtDpl->outputLocation == "Overlay" ||
           rtDpl->outputLocation == "CheckCell"
         dbSave(rtDpl->targetCv)
      )

      ;; Clear environment variables for this compMod

      printf("VALE INFO: %s complete.\n" rtDpl->name)
      return(t)
   )
)

