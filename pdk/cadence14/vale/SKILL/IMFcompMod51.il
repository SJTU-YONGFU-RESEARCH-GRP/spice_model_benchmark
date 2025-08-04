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
   2019-01-11 JF Created MissingNetVia Comp Mod using LPA
   2019-06-11 JF Change 190610a, added user interrupt catch
   2019-06-12 JF Change 190612a, added connectivity
   2019-10-24 JF Change 191024a, added support for selecting and tracing any
                 shape in the visible hierarchy

*/

procedure(IMFcompMod51(
             rtDpl
          @optional 
             (debug nil)
          )
   prog((cv win plugins foundit erv rv msg netCvName netWin runDir runConf
         netCv streamMap lpaMap lpaJobList resultFile )

      printf("VALE INFO: Creating %L as %L %L ...\n" rtDpl->name 
         rtDpl->outputStyle rtDpl->outputLocation) 

      cv = geGetWindowCellView()
      unless(cv
         printf("VALE ERROR: Unable to find an active layout window. ")
         printf("Please locate or open a layout window and try again.\n")
         return()
      )

      win = hiGetCurrentWindow()
      unless(win
         printf("VALE ERROR: Failed to find the current window.\n")
         return()
      )

      ;; Install the DFM plug-in if not already
      plugins = deGetPlugins(win)
      foundit = nil
      foreach(plugin plugins
         when(plugin~>name_ == "DFM-Plugin" 
            foundit = t
         )
      )
      unless(foundit
         errset(deInstallPlugin(win 'DFMPlugin ))
      )

      ;; Turn off Layer Palette Object Markers
      leSetObjectVisible("Markers" nil)

      ;; CIW Text regarding LPA output location
      when(rtDpl->outputLocation != "Shapes"
         printf("VALE INFO: Component Module %s requires the " rtDpl->name)
         printf("output location to be \"Shapes\", and the shapes ")
         printf("will be generated in the current cell. The current ")
         printf("output location is %s. This will be " rtDpl->outputLocation)
         printf("changed to \"Shapes\" and the run will continue. When ")
         printf("the run completes, use the VALE Options form, the Update ")
         printf("button, to move the output shapes to a different location.\n")
         ;; Set the output location back to Shapes
         rtDpl->outputLocation = "Shapes"
         rtDpl->targetCv = rtDpl->topCv = cv
         rtDpl->targetNm = cv~>cellName
      )

      ;; Set up run directory 
      when(debug
         printf("VALE DEBUG: Setting up the LPA run directory...\n")
      )
      erv = errset(
         strcat(getWorkingDir() "/VALE_RUNDIR/wd." rtDpl->name "_" 
            cv~>cellName)
      )
      if(erv then
         if(erv == list(nil) then
            printf("VALE ERROR: Failed to set the LPA output directory.\n")
            return()
         else
            runDir = car(erv)
            unless(isDir(runDir)
               createDirHier(runDir)
            )
         )
      else
         printf("VALE ERROR: A problem occurred setting up the LPA output ")
         printf("directory.\n%L\n" errset.errset)
         return()
      )

      ;; Remove prior results if any
      resultFile = strcat(runDir "/GUIDE/merged.hif")
      when(isFile(resultFile)
         deleteFile(resultFile)
      )

      ;; Set the LPA conf file
      runConf = _IMFgetIncludeFile(cv rtDpl ".conf" debug)
      unless(runConf return())

      ;; Set the LPA map file
      lpaMap = _IMFgetIncludeFile(cv rtDpl ".lpa_map" debug)
      unless(lpaMap return())

      ;; Set the LPA streamout file
      streamMap = _IMFgetIncludeFile(cv rtDpl ".streamout_map" debug)
      unless(streamMap return())

      ;;;;;;;;;;;;;;;;;;;;;
      ;; Start main flow ;;
      ;;;;;;;;;;;;;;;;;;;;;

      ;; 1. Instruct the user to select a shape
      msg = "   Select any shape on a net to start tracing the net..."
      unless(VALEshowDialog1(rtDpl "Select Shape..." msg debug)
         return()
      )

      ;; 2. Save cellview for traced net by selection
      erv = errset(_IMFsaveNetBySelection(cv nil nil debug))
      if(erv then
         if(erv == list(nil) then
            printf("VALE ERROR: Failed to save aside the selected net\n")
            return()
         else
            netCvName = car(erv)
         )
      else
         printf("VALE ERROR: A problem occurred why trying to save aside ")
         printf("the selected net.\n%L\n" errset.errset)
         return()
      ) 

      ;; 3. Open the net trace cellview
      if(ddGetObj(cv~>libName netCvName cv~>viewName) then
         netCv = dbOpenCellViewByType(cv~>libName netCvName cv~>viewName 
            nil "r")
         netWin = geOpen(?lib cv~>libName ?cell netCvName ?view cv~>viewName)
      else
         printf("VALE ERROR: Failed to find the traced-net cellview %L\n"
            netCvName)
         return()
      )

      ;; LPA settings
      ;lpainitFile = _IMFgetIncludeFile(netCv rtDpl ".lpainit" debug)
      ;unless(lpainitFile return())
      ;erv = load(lpainitFile)
      ;unless(erv
      ;   printf("VALE ERROR: A problem occurred loading the LPA global ")
      ;   printf("defaults from %L.\n%L\n" lpainitFile errset.errset)
      ;   return()
      ;)

      ;; 4. Stream out the net
      when(debug
         printf("VALE DEBUG: Streaming out net traced cellview...\n")
      )
      erv = errset(
         _lpa_stream_out_gds(netCv runDir streamMap "INPUT.gds")
      )
      if(erv then
         if(erv == list(nil) then
            printf("VALE ERROR: Failed to stream out the net trace cellview\n")
            return()
         )
         ;; pass thru
      else
         printf("VALE ERROR: A problem occurred during stream out of the net ")
         printf("trace cellview.\n%L\n" errset.errset)
         return()
      )

      ;; The window object sets the conf topcell
      ;; INPUT.gds is the required name for LPA 
      lpaJobList = list(
         list(netWin runDir runConf lpaMap strcat(runDir "/INPUT.gds"))
      )

      ;; 5. Running LPA 
      when(debug
         printf("VALE DEBUG: Running LPA...\n")
      )
      erv = errset(_dfmRunBatchMJobs(lpaJobList))
      unless(erv
         ;; only use unless here because _dfmRunBatchMJobs returns nil on
         ;; successful submission, so errset returns list(nil)
         printf("VALE ERROR: A problem occurred while running LPA.\n%L\n"
            errset.errset)
         return()
      )

      ;; 6. Monitor LPA for completion
      unless(rtDpl->timeout
         rtDpl->timeout = "300"
      )
      rv = _IMFmonitorSys(resultFile evalstring(rtDpl->timeout) debug)
      unless(rv
         printf("VALE ERROR: Failed to load the results file %L " resultFile)
         printf("in the allotted time %L. Please check the results " 
            rtDpl->timeout)
         printf("and/or update the time-out settings in the config file.\n")
         return()
      )
      ;; Change 190610a: Check for User Interrupt, IMFmonitorSys returns
      ;; "userInterrupt", exit nicely
      when(rv == "userInterrupt"
         return(t)
      )

      ;; 7. Close net trace cellview
      erv = errset(hiCloseWindow(netWin))
      ;dbClose(netCv)
      ;erv = errset(ddDeleteObj(dbGetCellViewDdId(netCv)))

      ;; 8. Import results on net trace file into original cellview
      hiSetCurrentWindow(win)
      when(debug
         printf("VALE DEBUG: Importing in-design updates...\n")
      )
      erv = errset(_dfm_lpa_batch_fixing(resultFile))
      unless(erv
         ;; only use unless here because _dfm_lpa_batch_fixing returns nil on
         ;; successful submission, so errset returns list(nil)
         printf("VALE ERROR: A problem occurred in applying the results ")
         printf("in-design.\n%L\n" errset.errset)
         return()
      )

      unless(rtDpl->showAllMarkers   
         geDeleteAllMarker(cv)
      )

      ;; Add Connectivity
      if(rtDpl->addConnectivity then
         erv = errset(_IMFpostpAddConn(rtDpl debug))
         if(erv then
            if(erv == list(nil) then
               printf("VALE WARNING: Failed to post process add connectivity ")
               printf("to %s shapes\n" rtDpl->name)
            )
         else
            printf("VALE ERROR: A problem occurred while adding connectivity ")
            printf("as a post process for %s\n" rtDpl->name)
            printf("%L\n" errset.errset)
         )
      )

      ;; Remove remaining traces
      lntRemoveAll()

      errset(_IMFremoveByProp(rtDpl->topCv "RemoveAll" nil))

      printf("VALE INFO: %s complete.\n" rtDpl->name)

      return(t)
   )
)

