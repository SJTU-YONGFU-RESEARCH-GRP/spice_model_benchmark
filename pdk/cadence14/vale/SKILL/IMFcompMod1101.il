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
   2019-09-04 Created by JPC 
 
*/

procedure(IMFcompMod1101(
             rtDpl
          @optional 
             (debug nil)
          )
   prog((cv erv plugins foundit runDir streamMap cmd
         DFMHOME ECLAIR_HOME K2_CPA_MACRO K2_EDITOR MC_HOME PATH
         PVSHOME QV_HOME)
         

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



      ;; Set the LPA streamout file

      streamMap = _IMFgetIncludeFile(cv rtDpl ".streamout_map" debug)
      printf("VALE INFO: Using virtuoso stream out map %s for CPA Studio launch\n" streamMap)
      printf("VALE INFO: If you want another map replace it with your desired mapping\n")
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
      ;; 2. launch k2_viewer

      ;; has to be defined
      DFMHOME =  getShellEnvVar("DFMHOME")
      ECLAIR_HOME = getShellEnvVar("ECLAIR_HOME")
      if(ECLAIR_HOME == nil then 
		     ECLAIR_HOME = DFMHOME
		     setShellEnvVar(sprintf(nil "ECLAIR_HOME=%s" ECLAIR_HOME))
		     )

      K2_EDITOR = getShellEnvVar("K2_EDITOR")
      if(K2_EDITOR == nil then 
		   K2_EDITOR = "1"
		   setShellEnvVar(sprintf(nil "K2_EDITOR=%s" K2_EDITOR))
		   )

      K2_CPA_MACRO = getShellEnvVar("K2_CPA_MACRO")
      if(K2_CPA_MACRO == nil then 
		      K2_CPA_MACRO = strcat(DFMHOME "/share/qv/cpa.mac")
		      setShellEnvVar(sprintf(nil "K2_CPA_MACRO=%s" K2_CPA_MACRO))
		      )
      PVSHOME = getShellEnvVar("PVSHOME")
      if(PVSHOME == nil then
		 printf("PVSHOME is not defined. Unable to launch CPA Studio because environment not setup corectly\n")
		 return()
		 )
      QV_HOME = getShellEnvVar("QV_HOME")
      if(QV_HOME == nil then
		 QV_HOME = strcat(PVSHOME "/tools.lnx86/K2/Viewer")
		 setShellEnvVar(sprintf(nil "QV_HOME=%s" QV_HOME))
		 )

      MC_HOME = getShellEnvVar("MC_HOME")
      if(MC_HOME == nil then
		 MC_HOME = strcat(PVSHOME "/tools.lnx86/K2/MaskCompose")
		 setShellEnvVar(sprintf(nil "MC_HOME=%s" MC_HOME))
		 )
      PATH = getShellEnvVar("PATH")
      
      PATH = strcat(PVSHOME "/bin:" QV_HOME "/bin:" QV_HOME "/../../bin:" ECLAIR_HOME "/bin:" PATH)
      setShellEnvVar(sprintf(nil "PATH=%s" PATH))

      (sprintf cmd "k2_cdsviewer -data %s/%s -post %s/share/qv/lpa_quickstart.mac &" runDir "INPUT.gds" ECLAIR_HOME)
      (system cmd)

      printf("VALE INFO: %s complete.\n" rtDpl->name)
      return(t)
   )
)

