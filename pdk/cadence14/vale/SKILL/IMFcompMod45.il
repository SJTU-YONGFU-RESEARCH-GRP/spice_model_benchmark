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
   2018-04-19 JF Basic Trim insertion using LPA topological patterns
   2018-07-31 JF Updated Component Module based on MVS18.10 code efficiency 
                 enhancements: Changes 180724a 180724b 180724c 180724d 180725a
                 180725b 180725c
   2018-10-04 JF Updates for a name change from AddCut to AddTrims for V05
   2018-12-14 JF Changed the LPA run directory to VALE_RUNDIR/wd.<CM>_<cellName>
   2019-02-26 JF Converted to new LPA style using _dfmRunBatchMJobs 
   2019-06-11 JF Change 190610a, added user interrupt catch
 
*/

procedure(IMFcompMod45(
             rtDpl
          @optional 
             (debug nil)
          )
   prog((cv lpaJobList erv rv plugins foundit runDir runConf 
         streamMap lpaMap lpaJobList resultFile)

      printf("VALE INFO: Creating %L as %L %L ...\n" rtDpl->name 
         rtDpl->outputStyle rtDpl->outputLocation) 

      cv = geGetWindowCellView()
      unless(cv
         printf("VALE ERROR: Unable to find an active layout window. ")
         printf("Please locate or open a layout window and try again.\n")
         return()
      )

      ;; Install the DFM plug-in if not already
      plugins = deGetPlugins(hiGetCurrentWindow())
      foundit = nil
      foreach(plugin plugins
         when(plugin~>name_ == "DFM-Plugin" 
            foundit = t
         )
      )
      unless(foundit
         errset(deInstallPlugin(hiGetCurrentWindow() 'DFMPlugin ))
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

      ;; Set the run directory
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

      ;; 1. Stream out the data 
      when(debug
         printf("VALE DEBUG: Streaming out %s...\n" rtDpl->topCv~>cellName)
      )
      erv = errset(
         _lpa_stream_out_gds(cv runDir streamMap "INPUT.gds")
      )
      if(erv then
         if(erv == list(nil) then
            printf("VALE ERROR: Failed to stream out the cellview %s\n"
               rtDpl->topCv~>cellName)
            return()
         )
         ;; pass thru
      else
         printf("VALE ERROR: A problem occurred during stream out of the ")
         printf("cellview %s, %L\n" rtDpl->topCv~>cellName errset.errset)
         return()
      )

      ;; 2. Run LPA
      lpaJobList = list(
         list(hiGetCurrentWindow() runDir runConf lpaMap 
            strcat(runDir "/INPUT.gds"))
      )
      when(debug
         printf("VALE DEBUG: Running LPA...\n")
      )
      erv = errset(_dfmRunBatchMJobs(lpaJobList))
      unless(erv
         ;; only use unless here because _dfmRunBatchMJobs returns nil on
         ;; successful submission, so errset returns list(nil)
         printf("VALE ERROR: A problem occurred while running LPA on %s, %L\n"
            rtDpl->topCv~>cellName errset.errset)
         return()
      ) 

      ;; 3. Monitor LPA for completion
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
          
      ;; 4. Import results
      when(debug
         printf("VALE INFO: Staring in-design updates...\n")
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

      printf("VALE INFO: %s complete.\n" rtDpl->name)
      return(t)
   )
)

