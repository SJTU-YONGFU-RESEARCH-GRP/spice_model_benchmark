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
   2019-09-24 Created by JPC 
   2019-10-16 Added move module functions by JPC
   2019-11-19 Updated syntax to correct variable scope according to sklinter
   2019-12-04 Added support for CM2 (getIMFconf*), also fixed atoi error JPC
   2019-12-05 JF Fixed missing field highlights, modified parameters for 
              VALEmoveModule to fix lint error, added check in
              _VALEgetMaxCompModNumber for element being nil
   2019-12-11 support auto menu for add modules and move module
   2019-12-12 Code cleanups plus load new skill files into memory correctly. 
              Name cleanups.
 
*/



procedure(_IMFwriteCadenceCopyrightHeader(wPort) 
   fprintf(wPort 
"/*\n\
 |-----------------------------------------------------------------------|\n\
 |                                                                       |\n\
 |      _               Copyright (c) 2019                               |\n\
 |    c a d e n c e     Cadence Design Systems, Inc.                     |\n\
 |                      Cadence VCAD IP Component                        |\n\
 |                      All Rights Reserved                              |\n\
 |                                                                       |\n\
 |                                                                       |\n\
 | THIS IS UNPUBLISHED PROPRIETARY SOURCE CODE OF CADENCE DESIGN SYSTEMS |\n\
 | The copyright notice above does not evidence any actual or intended   |\n\
 | publication of such source code.                                      |\n\
 |                                                                       |\n\
 | This source code and any other accompanying code (\"Code\") is          |\n\
 | Cadence's Intellectual Property.                                      |\n\
 |                                                                       |\n\
 | This Code remains Cadence intellectual property and may under no      |\n\
 | circumstances be given to third parties, neither in original nor in   |\n\
 | modified versions, without Cadence's explicit written permission.     |\n\
 |                                                                       |\n\
 | PROPRIETARY INFORMATION, PROPERTY OF CADENCE DESIGN SYSTEMS, INC.     |\n\
 |                                                                       |\n\
 | The code may require modification to satisfy the requirements of any  |\n\
 | user. The code and any modifications to the code may not be           |\n\
 | compatible with current or future versions of Cadence products. THE   |\n\
 | CODE IS PROVIDED \"AS IS\" AND WITH NO WARRANTIES, INCLUDING WITHOUT    |\n\
 | LIMITATION ANY EXPRESS WARRANTIES OR IMPLIED WARRANTIES OF            |\n\
 | MERCHANTABILITY OR FITNESS FOR A PARTICULAR USE.                      |\n\
 |                                                                       |\n\
 |-----------------------------------------------------------------------|\n\
 */\n" )
   )  


procedure(_IMFwriteRevision(wPort)
   fprintf(wPort 
      "\n/*\n   Revision log:   %s created by VALE\n\n*/\n\n"  
      (getCurrentTime)))



procedure(_IMFwriteLPACompmodTemplate(wPort 
      compModNumber bloat filterBloat fixHierarchically)
   fprintf(wPort 
"procedure(IMFcompMod%s(\n\
             rtDpl\n\
          @optional\n\
             (debug nil)\n\
          )\n\
   prog((cv lpaJobList erv rv plugins foundit runDir runConf \n\
         streamMap lpaMap lpaJobList resultFile)\n\n\
      printf(\"VALE INFO: Creating %s as %s %s ...\\n\" rtDpl->name \n\
         rtDpl->outputStyle rtDpl->outputLocation)\n\n\
      cv = geGetWindowCellView()\n\
      unless(cv\n\
         printf(\"VALE ERROR: Unable to find an active layout window. \")\n\
         printf(\"Please locate or open a layout window and try again.\\n\")\n\
         return()\n\
      )\n\n" compModNumber "%L" "%L" "%L")

   fprintf(wPort 
"      ;; Install the DFM plug-in if not already\n\
      plugins = deGetPlugins(hiGetCurrentWindow())\n\
      foundit = nil\n\
      foreach(plugin plugins\n\
         when(plugin~>name_ == \"DFM-Plugin\" \n\
            foundit = t\n\
         )\n\
      )\n\
      unless(foundit\n\
         errset(deInstallPlugin(hiGetCurrentWindow() 'DFMPlugin ))\n\
      )\n\n\

      ;; Turn off Layer Palette Object Markers\n\
      leSetObjectVisible(\"Markers\" nil)\n\n\

      ;; CIW Text regarding LPA output location\n\
      when(rtDpl->outputLocation != \"Shapes\"\n\
         printf(\"VALE INFO: Component Module %s requires the \" rtDpl->name)\n\
         printf(\"output location to be \\\"Shapes\\\", and the shapes \")\n\
         printf(\"will be generated in the current cell. The current \")\n\
         printf(\"output location is %s.\
 This will be \" rtDpl->outputLocation)\n\
         printf(\"changed to \\\"Shapes\\\" and\
 the run will continue. When \")\n\
         printf(\"the run completes,\
 use the VALE Options form, the Update \")\n\
         printf(\"button,\
 to move the output shapes to a different location.\\n\")\n\
         ;; Set the output location back to Shapes\n\
         rtDpl->outputLocation = \"Shapes\"\n\
         rtDpl->targetCv = rtDpl->topCv = cv\n\
         rtDpl->targetNm = cv~>cellName\n\
      )\n\n"  "%s"  "%s")


   fprintf(wPort 
"      ;; Set the run directory\n\
      when(debug\n\
         printf(\"VALE DEBUG: Setting up the LPA run directory...\\n\")\n\
      ) \n\
      erv = errset(\n\
         strcat(getWorkingDir() \"/VALE_RUNDIR/wd.\" rtDpl->name \"_\" \n\
            cv~>cellName)\n\
      )\n\
      if(erv then\n\
         if(erv == list(nil) then\n\
            printf(\"VALE ERROR:\
 Failed to set the LPA output directory.\\n\")\n\
            return()\n\
         else\n\
            runDir = car(erv)\n\
            unless(isDir(runDir)\n\
               createDirHier(runDir)\n\
            )\n\
         )\n\
      else\n\
         printf(\"VALE ERROR:\
 A problem occurred setting up the LPA output \")\n\
         printf(\"directory.\\n%s\\n\" errset.errset)\n\
         return()\n\
      )\n\n" "%L")

   fprintf(wPort 
"      ;; Remove prior results if any\n\
      resultFile = strcat(runDir \"/GUIDE/merged.hif\")\n\
      when(isFile(resultFile)\n\
         deleteFile(resultFile)\n\
      )\n\n")


   fprintf(wPort 
"      ;; Set the LPA conf file\n\
      runConf = _IMFgetIncludeFileInIncludeDir(cv rtDpl \".conf\" debug)\n\
      unless(runConf return())\n\n")

   fprintf(wPort 
"      ;; Set the LPA map file\n\
      lpaMap = _IMFgetIncludeFileInIncludeDir(cv rtDpl \".lpa_map\" debug)\n\
      unless(lpaMap return())\n\n")

   fprintf(wPort 
"      ;; Set the LPA streamout file\n\
      streamMap =\
 _IMFgetIncludeFileInIncludeDir(cv rtDpl \".streamout_map\" debug)\n\
      unless(streamMap return())\n\n")


   fprintf(wPort 
"      ;; Load LPA init file \n\
      lpaInit = _IMFgetIncludeFileInIncludeDir(cv rtDpl \".lpainit\" debug)\n\
      unless(load(lpaInit) return())\n\n")


   fprintf(wPort 
"      ;;;;;;;;;;;;;;;;;;;;;\n\
      ;; Start main flow ;;\n\
      ;;;;;;;;;;;;;;;;;;;;;\n\n")

   fprintf(wPort 
"      ;; 1. Stream out the data \n\
      when(debug\n\
         printf(\"VALE DEBUG:\
 Streaming out %s...\\n\" rtDpl->topCv~>cellName)\n\
      )\n\
      erv = errset(\n\
         _lpa_stream_out_gds(cv runDir streamMap \"INPUT.gds\")\n\
      )\n\
      if(erv then\n\
         if(erv == list(nil) then\n\
            printf(\"VALE ERROR: Failed to stream out the cellview %s\\n\"\n\
               rtDpl->topCv~>cellName)\n\
            return()\n\
         )\n\
         ;; pass thru\n\
      else\n\
         printf(\"VALE ERROR: A problem occurred during stream out of the \")\n\
         printf(\"cellview %s, %s\\n\" rtDpl->topCv~>cellName errset.errset)\n\
         return()\n\
      )\n\n" "%s"  "%s"  "%s" "%L")

   fprintf(wPort 
"      ;; 2. Run LPA\n\
      lpaJobList = list(\n\
         list(hiGetCurrentWindow() runDir runConf lpaMap \n\
            strcat(runDir \"/INPUT.gds\"))\n\
      )\n\
      when(debug\n\
         printf(\"VALE DEBUG: Running LPA...\\n\")\n\
      )\n\
      erv = errset(_dfmRunBatchMJobs(lpaJobList))\n\
      unless(erv\n\
         ;; only use unless here because _dfmRunBatchMJobs returns nil on\n\
         ;; successful submission, so errset returns list(nil)\n\
         printf(\"VALE ERROR:\
 A problem occurred while running LPA on %s, %s\\n\"\n\
            rtDpl->topCv~>cellName errset.errset)\n\
         return()\n\
      )\n\n"  "%s" "%L")

   fprintf(wPort 
"      ;; 3. Monitor LPA for completion\n\
      unless(rtDpl->timeout\n\
         rtDpl->timeout = \"300\"\n\
      )\n\
      rv = _IMFmonitorSys(resultFile evalstring(rtDpl->timeout) debug)\n\
      unless(rv\n\
         printf(\"VALE ERROR:\
 Failed to load the results file %s \" resultFile)\n\
         printf(\"in the allotted time %s. Please check the results \"\n\
            rtDpl->timeout)\n\
         printf(\"and/or update the time-out settings\
 in the config file.\\n\")\n\
         return()\n\
      )\n\
      ;; Change 190610a: Check for User Interrupt, IMFmonitorSys returns\n\
      ;; \"userInterrupt\", exit nicely\n\
      when(rv == \"userInterrupt\"\n\
         return(t) \n\
      )\n\n"  "%L"  "%L")

   fprintf(wPort 
"      ;; 4. Import results\n\
      when(debug\n\
         printf(\"VALE INFO: Staring in-design updates...\\n\")\n\
      )\n")

   fprintf(wPort 
"      ;; load Markers\n\
	 when(rtDpl->showAllMarkers\n\
             dfmDisplayABrowser(runDir))\n")


   fprintf(wPort 
"      ;; do PEGASUS error checking\n\
      if(rtDpl->doDRCChecking then\n\
      ;; Set the PEGASUS deck\n\
	     pvsLPACheckDeck =\
 _IMFgetIncludeFileInIncludeDir(cv rtDpl \".pvl\" debug)\n\
	     unless(pvsLPACheckDeck return())\n\n\
      ;; Set the pvs deck virt layer map\n\
	     pvsLPACheckDeckLayerMap =\
 _IMFgetIncludeFileInIncludeDir(cv rtDpl \".pvs_virt_layer_map\" debug)\n\
	     unless(pvsLPACheckDeckLayerMap return())\n\n\
      ;; Set the pvs deck rules file\n\
	     pvsLPACheckDeckRuleFile =\
 _IMFgetIncludeFileInIncludeDir(cv rtDpl \".pvs_rules\" debug)\n\
	     unless(pvsLPACheckDeckRuleFile return())\n\n")


   fprintf(wPort 
"	     erv = errset(_dfmPVSDRCSetupBatch(?enableDRC t \n\
				  ?deckFile pvsLPACheckDeck \n\
				  ?layerMapFile pvsLPACheckDeckLayerMap\n\
				  ?minBloatValue %s\n\
				  ?minFilterBloatValue %s\n\
				  ?abortOnLayoutError nil\n\
				  ?printViolations nil\n\
				  ?markerViolations nil\n\
				  ?enablePostFilter nil\n\
				  ?postFilterList list(\"M1\")\n\
				  ?selectedRulesFile pvsLPACheckDeckRuleFile\n\
				  )	)\n\n"  bloat  filterBloat)

   fprintf(wPort 
"	     unless(erv\n\
		    printf(\"VALE ERROR:\
 A problem occured setting up DRC checking in-design.\\n%s\\n\" errset.errset)\n\
		    return()\n\
		    )\n\
	     )\n\n"  "%L")

   if(fixHierarchically then 
      fprintf(wPort "     _dfmSetHierarchyFlag()\n"))

   fprintf(wPort 
"      erv = errset(_dfm_lpa_batch_fixing(resultFile))\n\
      unless(erv\n\
         ;; only use unless here because _dfm_lpa_batch_fixing returns nil on\n\
         ;; successful submission, so errset returns list(nil)\n\
         printf(\"VALE ERROR: A problem occurred in applying the results \")\n\
         printf(\"in-design.\\n%s\\n\" errset.errset)\n\
         return()\n\
      )\n\n"  "%L")

   if(fixHierarchically then 
      fprintf(wPort "    _dfmSetHierarchyFlag(0)\n"))

   fprintf(wPort 
"      unless(rtDpl->showAllMarkers   \n\
         geDeleteAllMarker(cv)\n\
      )\n\n\
      if(rtDpl->doDRCChecking then\n\
;;;; turn off PEGASUS DRC\n\
	     _dfmPVSDRCDisableBatch()\n\
      )\n")


   fprintf(wPort 
"      ;; Add Connectivity\n\
      if(rtDpl->addConnectivity then\n\
         erv = errset(_IMFpostpAddConn(rtDpl debug))\n\
         if(erv then\n\
            if(erv == list(nil) then\n\
               printf(\"VALE WARNING:\
 Failed to post process add connectivity \")\n\
              printf(\"to %s shapes\\n\" rtDpl->name)\n\
            )\n\
         else\n\
            printf(\"VALE ERROR:\
 A problem occurred while adding connectivity \")\n\
            printf(\"as a post process for %s\\n\" rtDpl->name)\n\
            printf(\"%s\\n\" errset.errset)\n\
         )\n\
      )\n\n\
     when(rtDpl->saveCheckpoint\n\
           VALEsaveCheckpoint(rtDpl)\n\
     )\n"  "%s"  "%s"  "%L")

   fprintf(wPort "      printf(\"VALE INFO: %s complete.\\n\" rtDpl->name)\n\
      return(t)\n   )\n)\n"  "%s")

   )



procedure(_IMFwriteIMFcompMod(fileName number  minBloat minFilterBloat 
      fixHierarchically) 
   let((outputFilePort) 

      outputFilePort = outfile(fileName)

      _IMFwriteCadenceCopyrightHeader(outputFilePort)

      _IMFwriteRevision(outputFilePort)

      _IMFwriteLPACompmodTemplate(outputFilePort 
	 number  minBloat minFilterBloat fixHierarchically)

      close(outputFilePort)
      )
   )

procedure(_IMFreturnPrimaryLayersFromXML(xmlFile) 

   prog( (element lines  matchLines  layers  line inPort)
      lines = list()
      matchLines = list()
      layers = list()
      inPort = infile(xmlFile )
      while(gets(line inPort)
	 lines=append(lines list(line))
	 )
      close(inPort)
      matchLines= rexMatchList("primary_layer=\".*\"" lines)
      rexCompile("primary_layer=\"\\([a-zA-Z0-9_]*\\)\"")
      
      foreach(match matchLines
	 rexExecute(match)
	 element = rexSubstitute("\\1")
	 if(lindex(layers element) == nil  then  
	    layers= append(layers list(element)))
	 )
      return(layers)
      )
   
   )



procedure(_IMFappendNewValeFunctionToConfigFile(configFile compModNum moduleName
      version shortName description slider showAllMarkers doPVSDRCChecking)
   let( (valeConfigPort)   
      valeConfigPort=(outfile configFile "a")
      fprintf(valeConfigPort 
"\n;;VALE created LPA module from template\n\
_IMFdat->compMod%s = list(nil)\n\
_IMFdat->compMod%s->name = \"%s\"\n\
_IMFdat->compMod%s->version = \"%s\"\n\
_IMFdat->compMod%s->shortName = \"%s\"\n\
_IMFdat->compMod%s->description = \"%s\"\n\
_IMFdat->compMod%s->slider = \"%s\"\n\
_IMFdat->compMod%s->timeout = \"120\"\n" 
	 compModNum 
	 compModNum moduleName 
	 compModNum version 
	 compModNum shortName  
	 compModNum description  
	 compModNum slider 
	 compModNum)
      
      if(showAllMarkers then 
	 fprintf( valeConfigPort 
	    "_IMFdat->compMod%s->showAllMarkers = t\n" compModNum )
	 else
	 fprintf( valeConfigPort 
	    "_IMFdat->compMod%s->showAllMarkers = nil\n" compModNum )
	 )
      if(doPVSDRCChecking then 
	 fprintf( valeConfigPort 
	    "_IMFdat->compMod%s->doDRCChecking = t\n" compModNum)
	 else
	 fprintf( valeConfigPort 
	    "_IMFdat->compMod%s->doDRCChecking = nil\n" compModNum)
	 )
      fprintf(valeConfigPort 
	 "_IMFdat->compMod%s->saveCheckpoint = nil\n\n" compModNum)
      close(valeConfigPort) 

      evalstring(strcat("_IMFdat->compMod" compModNum " =  list(nil)"))
      evalstring(strcat("_IMFdat->compMod" compModNum "->name = \"" 
	    moduleName "\""))
      evalstring(strcat("_IMFdat->compMod" compModNum "->version = \"" 
	    version "\""))
      evalstring(strcat("_IMFdat->compMod" compModNum "->shortName = \"" 
	    shortName "\""))
      evalstring(strcat("_IMFdat->compMod" compModNum "->description = \"" 
	    description "\""))
      evalstring(strcat("_IMFdat->compMod" compModNum "->slider = \"" 
	    slider "\""))
      evalstring(strcat("_IMFdat->compMod" compModNum "->timeout = \"120\""))
      if(showAllMarkers then 
	 evalstring(strcat("_IMFdat->compMod" compModNum "->showAllMarkers = t"))
	 else
	 evalstring(strcat("_IMFdat->compMod" compModNum "->showAllMarkers = nil"))
	 )
      if(doPVSDRCChecking then 
	 evalstring(strcat("_IMFdat->compMod" compModNum "->doDRCChecking = t"))
	 else
	 evalstring(strcat("_IMFdat->compMod" compModNum "->doDRCChecking = nil"))
	 )
      evalstring(strcat("_IMFdat->compMod" compModNum "->saveCheckpoint = nil"))
      )
   )


procedure(_IMFcreateLPAConfFile(file compModName compModVers 
      addPreprocess layerOrderList addMPTFile)
   let((valeLPAConfPort layerOrderString)
   valeLPAConfPort=(outfile file)

   fprintf(valeLPAConfPort 
"setConf jobName LPAJOB\n\
setConf smallLayout 1\n\
############################################################################\n\
##\n\
##  Copy from here to COPY_END, for every VALE framework LPA Component Module\n\
##  Modify the two variables below for each Component Module Name and Version\n\
##\n\
############################################################################\n\
set compModName \"%s\"\n\
set compModVers \"%s\"\n" compModName compModVers)
   
   fprintf(valeLPAConfPort 
"###########################################################################\n\
set compModMap \"${compModName}_$compModVers/${compModName}.lpa_map\" \n\
set compModRunset \"${compModName}_$compModVers/${compModName}.xml\"\n\
set compModPreprocess\
 \"${compModName}_$compModVers/${compModName}.preprocess.tcl\"\n")
   
   fprintf(valeLPAConfPort 
"\n\
## Search for the layer map in the CM, CM2, and local directories \n\
if {[info exists env(CDS_MVS_IMF_CM)]} {\n\
   ## Variable for the CM directory is defined\n\
   set compModDir $env(CDS_MVS_IMF_CM)\n\
   if {[file isdirectory $compModDir]} {\n\
      ## The variable contains a valid CM directory\n\
      if {[file exists $compModDir/Include/$compModMap]} {\n\
         ## Layer map file exists in the CM directory\n\
         set compModMapPath \"$compModDir/Include/$compModMap\"\n\
         set compModRunsetPath \"$compModDir/Include/$compModRunset\"\n\
         set compModPreprocessPath \"$compModDir/Include/$compModPreprocess\"\n\
      } else {\n\
         ## No layer map in the CM directory\n\
         if {[info exists env(CDS_MVS_IMF_CM2)]} {\n\
            ## Variable for the CM2 directory is defined\n\
            set compModDir $env(CDS_MVS_IMF_CM2)\n\
            if {[file isdirectory $compModDir]} {\n\
               ## The variable contains a valid CM2 directory\n\
               if {[file exists $compModDir/Include/$compModMap]} {\n\
                  ## Layer map file exists in the CM2 directory\n\
                  set compModMapPath \"$compModDir/Include/$compModMap\"\n\
                  set compModRunsetPath\
 \"$compModDir/Include/$compModRunset\"\n\
                  set compModPreprocessPath\
 \"$compModDir/Include/$compModPreprocess\"\n\
               } else {\n\
                  ## No layer map in the CM2 directory either,\
 set to local dir\n\
                  set compModDir \"./\"\n\
                  if {[file exists $compModDir/Include/$compModMap]} {\n\
                     ## Layer map found in the local dir\n\
                     set compModMapPath \"$compModDir/Include/$compModMap\"\n\
                     set compModRunsetPath\
 \"$compModDir/Include/$compModRunset\"\n\
                     set compModPreprocessPath\
 \"$compModDir/Include/$compModPreprocess\"\n\
                  } else {\n\
                     ## No layer map found\n\
                     puts \"VALE ERROR:\
 Failed to set the Component Module paths.\"\n\
                  }\n\
               }\n\
            } else {\n\
               ## No valid CM2 directory\n\
               set compModDir \"./\"\n\
               if {[file exists $compModDir/Include/$compModMap]} {\n\
                  ## Layer map found in the local dir\n\
                  set compModMapPath \"$compModDir/Include/$compModMap\"\n\
                  set compModRunsetPath \"$compModDir/Include/$compModRunset\"\n\
                  set compModPreprocessPath\
 \"$compModDir/Include/$compModPreprocess\"\n\
               } else {\n\
                  ## No layer map found\n\
                  puts \"VALE ERROR:\
 Failed to set the Component Module paths.\"\n\
               }\n\
            }\n\
         } else {\n\
            ## No CM2 variable defined \n\
            set compModDir \"./\"\n\
            if {[file exists $compModDir/Include/$compModMap]} {\n\
               ## Layer map found in the local dir\n\
               set compModMapPath \"$compModDir/Include/$compModMap\"\n\
               set compModRunsetPath \"$compModDir/Include/$compModRunset\"\n\
               set compModPreprocessPath\
 \"$compModDir/Include/$compModPreprocess\"\n\
            } else {\n\
               ## No layer map found\n\
               puts \"VALE ERROR: Failed to set the Component Module paths.\"\n\
            }\n\
         }\n\
      }\n\
   } else {\n\
      ## No valid CM directory \n\
      if {[info exists env(CDS_MVS_IMF_CM2)]} {\n\
         ## Variable for the CM2 directory is defined\n\
         set compModDir $env(CDS_MVS_IMF_CM2)\n\
         if {[file isdirectory $compModDir]} {\n\
            ## The variable contains a valid CM2 directory\n\
            if {[file exists $compModDir/Include/$compModMap]} {\n\
               ## Layer map file exists in the CM2 directory\n\
               set compModMapPath \"$compModDir/Include/$compModMap\"\n\
               set compModRunsetPath \"$compModDir/Include/$compModRunset\"\n\
               set compModPreprocessPath\
 \"$compModDir/Include/$compModPreprocess\"\n\
            } else {\n\
               ## No layer map in the CM2 directory either, set to local dir\n\
               set compModDir \"./\"\n\
               if {[file exists $compModDir/Include/$compModMap]} {\n\
                  ## Layer map found in the local dir\n\
                  set compModMapPath \"$compModDir/Include/$compModMap\"\n\
                  set compModRunsetPath \"$compModDir/Include/$compModRunset\"\n\
                  set compModPreprocessPath\
 \"$compModDir/Include/$compModPreprocess\"\n\
               } else {\n\
                  ## No layer map found\n\
                  puts \"VALE ERROR:\
 Failed to set the Component Module paths.\"\n\
               }\n\
            }\n")

   fprintf(valeLPAConfPort 
"         } else {\n\
            ## No valid CM2 directory\n\
            set compModDir \"./\"\n\
            if {[file exists $compModDir/Include/$compModMap]} {\n\
               ## Layer map found in the local dir\n\
               set compModMapPath \"$compModDir/Include/$compModMap\"\n\
               set compModRunsetPath \"$compModDir/Include/$compModRunset\"\n\
               set compModPreprocessPath\
 \"$compModDir/Include/$compModPreprocess\"\n\
            } else {\n\
               ## No layer map found\n\
               puts \"VALE ERROR: Failed to set the Component Module paths.\"\n\
            }\n\
         }\n\
      } else {\n\
         ## No CM2 variable defined \n\
         set compModDir \"./\"\n\
         if {[file exists $compModDir/Include/$compModMap]} {\n\
            ## Layer map found in the local dir\n\
            set compModMapPath \"$compModDir/Include/$compModMap\"\n\
            set compModRunsetPath \"$compModDir/Include/$compModRunset\"\n\
            set compModPreprocessPath\
 \"$compModDir/Include/$compModPreprocess\"\n\
         } else {\n\
            ## No layer map found\n\
            puts \"VALE ERROR: Failed to set the Component Module paths.\"\n\
         }\n\
      }\n\
   }\n\
} else {\n\
   if {[info exists env(CDS_MVS_IMF_CM2)]} {\n\
      ## Variable for the CM2 directory defined\n\
      set compModDir $env(CDS_MVS_IMF_CM2)\n\
      if {[file isdirectory $compModDir]} {\n\
         ## The variable contains a valid CM2 directory\n\
         if {[file exists $compModDir/Include/$compModMap]} {\n\
            ## Layer map file exists in the CM2 directory\n\
            set compModMapPath \"$compModDir/Include/$compModMap\"\n\
            set compModRunsetPath \"$compModDir/Include/$compModRunset\"\n\
            set compModPreprocessPath\
 \"$compModDir/Include/$compModPreprocess\"\n\
         } else {\n\
            ## No layer map in the CM2 directory either, set to local dir\n\
            set compModDir \"./\"\n\
            if {[file exists $compModDir/Include/$compModMap]} {\n\
               ## Layer map found in the local dir\n\
               set compModMapPath \"$compModDir/Include/$compModMap\"\n\
               set compModRunsetPath \"$compModDir/Include/$compModRunset\"\n\
               set compModPreprocessPath\
 \"$compModDir/Include/$compModPreprocess\"\n\
            } else {\n\
               ## No layer map found\n\
               puts \"VALE ERROR: Failed to set the Component Module paths.\"\n\
            }\n\
         }\n\
      } else {\n\
         ## No valid CM2 directory\n\
         set compModDir \"./\"\n\
         if {[file exists $compModDir/Include/$compModMap]} {\n\
            ## Layer map found in the local dir\n\
            set compModMapPath \"$compModDir/Include/$compModMap\"\n\
            set compModRunsetPath \"$compModDir/Include/$compModRunset\"\n\
            set compModPreprocessPath\
 \"$compModDir/Include/$compModPreprocess\"\n\
         } else {\n\
            ## No layer map found\n\
            puts \"VALE ERROR: Failed to set the Component Module paths.\"\n\
         }\n\
      }\n\
   } else {\n\
      ## No CM2 variable defined \n\
      set compModDir \"./\"\n\
      if {[file exists $compModDir/Include/$compModMap]} {\n\
         ## Layer map found in the local dir\n\
         set compModMapPath \"$compModDir/Include/$compModMap\"\n\
         set compModRunsetPath \"$compModDir/Include/$compModRunset\"\n\
         set compModPreprocessPath \"$compModDir/Include/$compModPreprocess\"\n\
      } else {\n\
         ## No layer map found\n\
         puts \"VALE ERROR: Failed to set the Component Module paths.\"\n\
      }\n\
   }\n\
}\n\
##########################################################################\n\
##\n\
##  COPY_END \n\
##\n\
##########################################################################\n\n")
   
   fprintf(valeLPAConfPort 
	 "## uncomment the prerocess file to enable preprecessing\n")

   unless(addPreprocess
      fprintf( valeLPAConfPort "#") 
      )


      fprintf(valeLPAConfPort 
"setConf preProcessTCL \"$compModPreprocessPath\"\n\
setConf layerMapFile \"$compModMapPath\"\n\
set patternTechFile\
 \"$env(DFMHOME)/share/lpa/techfiles/patternMatch/TechFile/lpa.tcl\"\n\
\n\
## Set layer names per Component Module\n")

      layerOrderString = ""

      foreach(item layerOrderList
	 fprintf(valeLPAConfPort "%s {\n" item)
	 fprintf(valeLPAConfPort "  setConf LPATechFile $patternTechFile\n")
	 fprintf(valeLPAConfPort "}\n")
	 layerOrderString = sprintf(nil "%s %s" layerOrderString item)
	 )
      
      fprintf(valeLPAConfPort 
"setConf patInputReplace \"$compModRunsetPath\"\n\
setConf dmcErrorLimit 90000\n\
### set the layerOrder to match your pattern matching\n\
setConf layerOrder {%s}\n\
setConf guidelineType router\n" layerOrderString)

      when(addMPTFile
	 fprintf(valeLPAConfPort 
"set outputdir [getConf outputDir]\n\
setConf mptFile \"$outputdir/preproc/INTERMEDIATE.gds\"\n\
\n\n# Uncomment and modify if MPT file has different root than\n\
# input gds file\n\
#setConf mptFileRootCell \"LPA_MERGED_TOP\"\n")
	 )
      
      close(valeLPAConfPort)
      )      
   )  



procedure(_IMFcreateLPAlpainitFile(file  lpaCPUs)
   let( (valeLPAlpainitPort)
      valeLPAlpainitPort=(outfile file)
      fprintf(valeLPAlpainitPort 
"DFM_DP_env = list('dp_env\n\
                'method \"Local\"\n\
                'jobname \"LPAJOB\"\n\
                'args sprintf(nil \"-P %s -W 2:00\" \"MYPROJ:16.20:RD:Test\")\n\
                'queue (list \"lnx64\" \"queue\")\n\
                'resource \"mem > 2048\"\n\
                'local 1\n\
                'nhost %s\n\
                'hosts (list \"localhost:%s\")\n             )\n\n"  "%s"  
	 lpaCPUs  lpaCPUs)
      (close valeLPAlpainitPort)
      )
   )
	   

procedure(_IMFcopyValeIncludeFile(file dir moduleName version extension)
   let( (filename)
      filename = sprintf(nil "%s/Include/%s_%s/%s%s" 
	 dir moduleName version moduleName  extension)
      printf("VALE INFO: copying file %s to %s\n" file filename)
      csh(strcat("cp " file " " filename))
      )	  
   )

procedure(_IMFcreateTemplateLPAXmlFile(valeDir moduleName version)
   let((filename outP)
      filename = 
      strcat( valeDir "/Include/" moduleName "_" version "/" moduleName  ".xml")
      outP = outfile(filename)
      
      fprintf(outP 
	 "<!-- Sample basic lpa squish rule deck -->\n\
<!-- Please replace with your rule deck -->\n\
<deck>\n\
<properties lpa_xml_version = \"2.0\"/>\n\
<rule>\n\
      <rulename>rule1</rulename>\n\
      <pattern_def type=\"squish\"\n\
                   signature=\"M1\n\
                              0 0 0 /\n\
                              0 1 0 /\n\
                              0 0 0 \"\n\
         x_deltas=\"1 1-200 1\"\n\
         y_deltas=\"1 1-200 1\" >\n\
         <pattern sel=\"M2\" />\n\
         <overlay_scanline_range\
 range_str=\"x1 x2 y1 y2\" output_layer=\"MARKER\" />\n\
         <properties\n\
            primary_layer=\"M2\"\n\
            hotspot_type=\"WIDTH\"\n\
            hotspot_level=\"1\" />\n\
      </pattern_def>\n\
   </rule>\n\
</deck>\n")
      close(outP)
      )
   )
    
procedure(_IMFcreateTemplateLPAlayerMapFile(valeDir moduleName version)
   let((outP)
      outP = outfile(strcat( valeDir "/Include/" moduleName "_" version "/" 
	    moduleName  ".lpa_map"))
      fprintf(outP 
"## sample lpa layer map\n\
## replace with you map\n\
M2 32:0 M2\n\
MARKER 9999:0 MARKER\n\
AOI 99999:0 AOI\n")
      close(outP)

      )
   )

procedure(_IMFcreateTemplateLPAstreamoutMapFile(valeDir moduleName version)
   let((outP)
      outP = outfile(strcat( valeDir "/Include/" moduleName "_" version "/" 
	    moduleName  ".streamout_map"))
      fprintf(outP 
"## sample virtuoso stream out  map\n\
## replace with you map\n\
M2 drawing 32 0\n")
      close(outP)
      )
   )


procedure(_IMFreturnStringOfPrimaryLayersFromXML(xmlFile) 
   prog((stringList layers)
      stringList = ""
      layers = _IMFreturnPrimaryLayersFromXML(xmlFile)
      foreach( item	
	 layers
	 stringList = strcat(stringList sprintf(nil "%s " item) )
	 )
      return(stringList)
      )
   )

procedure(_IMFCreateLPAValeModulePopulateLayerOrderFormXmlCB(form)
   when(isFile(form->XmlSelector->value) && form->copyLPAFilesToggle->value
      form->layerOrderField->value = 
      _IMFreturnStringOfPrimaryLayersFromXML(form->XmlSelector->value)
      )
   )


procedure(_IMFCreateLPAValeModulePVSCheckButtonToggleCB(form)
   if(form->doPVSCheckingButton->value 
      then 
      hiSetFieldEditable(form->pvsRunScriptField t)
      hiSetFieldEditable(form->pvsRunScriptRulesField t)
      hiSetFieldEditable(form->pvsRunScriptVirtMapField t)
      hiSetFieldEditable(form->pvsMinBloatField t)
      hiSetFieldEditable(form->pvsMinFilterBloatField t)
      else
      hiSetFieldEditable(form->pvsRunScriptField nil)
      hiSetFieldEditable(form->pvsRunScriptRulesField nil)
      hiSetFieldEditable(form->pvsRunScriptVirtMapField nil)
      hiSetFieldEditable(form->pvsMinBloatField nil)
      hiSetFieldEditable(form->pvsMinFilterBloatField nil)
      )
   )


procedure(_IMFCopyLPABaseFilesCB(form)
   if(form->copyLPAFilesToggle->value 
      then
      hiSetFieldEditable(form->XmlSelector t)
      hiSetFieldEditable(form->layerMapSelector t)
      hiSetFieldEditable(form->streamoutMapSelector t)
      hiSetFieldEditable(form->layerOrderField t)
      form->XmlSelector->value = ""
      form->layerMapSelector->value = ""
      form->streamoutMapSelector->value = ""
      else
      hiSetFieldEditable(form->XmlSelector nil)
      hiSetFieldEditable(form->layerMapSelector nil)
      hiSetFieldEditable(form->streamoutMapSelector nil)
      hiSetFieldEditable(form->layerOrderField nil)
      form->XmlSelector->value = strcat(form->newValeModuleName->value  ".xml")
      form->layerMapSelector->value = 
      strcat(form->newValeModuleName->value  ".lpa_map")
      form->streamoutMapSelector->value = 
      strcat(form->newValeModuleName->value  ".streamout_map")
      
      )
   )

procedure(_IMFCreateLPAValeModuleLPAPreprocessToggleCB(form)
   if(form->doLPAPreprocess->value 
      then 
      hiSetFieldEditable(form->lpaPreprocessingTCLField t)
      else
      hiSetFieldEditable(form->lpaPreprocessingTCLField nil)
      )
   )

procedure(_IMFgetMaxCompModNumber(ValeConfFile) 
   
   prog( (element lines matchLines maxModNumber inPort line val)
      maxModNumber = 0      
      lines = list()
      matchLines = list()

      inPort = infile(ValeConfFile)
      while(gets(line inPort)
	 lines=append(lines list(line))
	 )
      close(inPort)
      matchLines = rexMatchList("_IMFdat->compMod" lines)

      rexCompile("_IMFdat->compMod\\([0-9_]+\\)")
      
      foreach(match matchLines
	 rexExecute(match)
	 element = rexSubstitute("\\1")
         when(element
	    val = atoi(element)
	    if(val == nil then
               printf("VALE WARNING: found strange compMod number %s\n" element)
            )
	    if(val > maxModNumber then 
               maxModNumber = val
	    )
	 )
      )

      return(maxModNumber)
   )
)



procedure(_IMFCreateLPAValeModuleCB(form) 
   let((success)
      success = _IMFaddLPAValeEntry(form form->valeDir->value
         form->valeConfFile->value
         form->newValeModuleNumber->value
         form->newValeModuleName->value  
         form->newValeModuleVersion->value 			   
         form->newValeModuleName->value  
         form->newValeModuleDescription->value  
         form->newValeModuleSlider->value  
         form->copyLPAFilesToggle->value
         form->XmlSelector->value  
         form->layerMapSelector->value  
         form->streamoutMapSelector->value 
         form->showAllMarkersToggle->value 
         form->doPVSCheckingButton->value 
         form->doLPAPreprocess->value 
         form->lpaPreprocessingTCLField->value 
         form->pvsMinBloatField->value
         form->pvsMinFilterBloatField->value
         form->pvsRunScriptField->value
         form->pvsRunScriptVirtMapField->value
         form->pvsRunScriptRulesField->value
         form->lpaCPUsField->value
         form->hierarchyToggle->value
         form->addMPTFile->value
         form->layerOrderField->value
	 )
      hiSetCallbackStatus(form success)
      )
   )

;;public form creation
procedure(VALEcreateLPAItemForm(valeDirs valeConfigFile 
      @optional (debug nil)) 
   let( (f_frame  f_moduleName  f_moduleDescription  f_moduleSlider 
	 f_XmlSelector f_layerMapSelector f_moduleVersion f_streamoutMapSelector
	 f_valeDir f_valeConf f_LPAPreprocessingTCL moduleNumber 
	 f_PVSCheckingDeck f_PVSCheckingRules f_PVSMinBloat 
	 f_PVSMinFilterBloat f_PVSCheckingVirtMap f_Pegasusframe f_PreProframe 
	 f_addMPTFile f_copyBaseLPAFiles f_lpaCPUs f_layerOrder f_hierarchyToggle
	 f_doLPAPreprocessing f_doPVSChecking f_moduleNumber f_showAllMarkers 
	 myForm createLPAValeOption availSliders tipTable
	 (baseX 10)
	 (baseY 10)
	 (incrY 30)
	 (incrX 10))


      f_frame = hiCreateFrameField(
	 ?name 'valeCreateLPAVALEFrame
	 ?labelText "Create VALE Pattern Base (LPA) Module"
         ?help      'nil
         ?invisible 'nil
	 )

      f_PreProframe = hiCreateFrameField(
	 ?name 'valeCreatePreProframe
	 ?labelText "LPA PreProcessing"
         ?help      'nil
         ?invisible 'nil
	 )

      f_Pegasusframe = hiCreateFrameField(
	 ?name 'valeCreatePegasusframe
	 ?labelText "LPA Pegasus Checking"
         ?help      'nil
         ?invisible 'nil
	 )

      moduleNumber = _IMFgetMaxCompModNumber(valeConfigFile) + 10

      f_moduleNumber = hiCreateStringField(
	 ?name 'newValeModuleNumber
	 ?prompt "Module Number:"
	 ?editable t
	 ?value sprintf(nil "%d" moduleNumber))
      
      f_moduleName = hiCreateStringField(
	 ?name 'newValeModuleName
	 ?prompt "Module Name:" 
	 ?editable t)

      f_moduleVersion = hiCreateStringField( 
	 ?name 'newValeModuleVersion
	 ?prompt "Module Version: " 
	 ?editable t 
	 ?defValue "V01")

      f_moduleDescription = hiCreateStringField( 
	 ?name 'newValeModuleDescription
	 ?prompt "Module Description:" 
	 ?editable t)


      availSliders = _IMFgetVALESliders(valeConfigFile)
      availSliders = append(availSliders list("Create New Vale Slider ..."))
      f_moduleSlider = hiCreateCyclicField(
	 ?name 'newValeModuleSlider
	 ?prompt "Module Slider:" 
	 ?callback '_IMFSliderCB
	 ?choices availSliders)


      f_lpaCPUs =(hiCreateStringField 
	 ?name 'lpaCPUsField
	 ?prompt "LPA CPUs to use:" 
	 ?value "1"
	 ?defValue "1"
	 ?editable t)


      f_copyBaseLPAFiles = hiCreateBooleanButton(
	 ?name 'copyLPAFilesToggle
	 ?buttonText "Copy LPA Files"
	 ?defValue t
	 ?buttonLocation 'left
	 ?value t
	 ?callback "_IMFCopyLPABaseFilesCB(hiGetCurrentForm())"
	 )
      


      f_XmlSelector= hiCreateFileSelectorField( 
	 ?name 'XmlSelector
	 ?prompt "Pattern Xml File:"
	 ?mode 'existingFile
	 ?callback "_IMFCreateLPAValeModulePopulateLayerOrderFormXmlCB(hiGetCurrentForm())"
	 ?defValue ""
	 ?value ""
	 ?editable t)


      f_layerMapSelector= hiCreateFileSelectorField( 
	 ?name 'layerMapSelector
	 ?prompt "LPA Layer map file:"
	 ?mode 'existingFile
	 ?defValue ""
	 ?value ""
	 ?editable t)

      f_streamoutMapSelector= hiCreateFileSelectorField( 
	 ?name 'streamoutMapSelector
	 ?prompt "Virtuoso streamout map file:"
	 ?mode 'existingFile
	 ?defValue ""
	 ?value ""
	 ?editable t)

      f_layerOrder = hiCreateStringField( 
	 ?name 'layerOrderField
	 ?prompt "LPA Layer Order:" 
	 ?defValue "M2"
	 ?value "M2"
	 ?editable t)

      f_doPVSChecking = hiCreateBooleanButton(
	 ?name 'doPVSCheckingButton
	 ?buttonText "Do PEGASUS DRC Error Checking?"
	 ?defValue nil
	 ?buttonLocation 'left
	 ?value nil
	 ?callback "_IMFCreateLPAValeModulePVSCheckButtonToggleCB(hiGetCurrentForm())"
	 )

      f_showAllMarkers = hiCreateBooleanButton(
	 ?name 'showAllMarkersToggle
	 ?buttonText "Show Markers"
	 ?defValue nil
	 ?buttonLocation 'left
	 ?value nil
	 )

      f_hierarchyToggle = hiCreateBooleanButton(
	 ?name 'hierarchyToggle
	 ?buttonText "Fix Hierarchically"
	 ?defValue nil
	 ?buttonLocation 'left
	 ?value nil
	 )


      f_doLPAPreprocessing = hiCreateBooleanButton(
	 ?name 'doLPAPreprocess
	 ?buttonText "Do LPA Preprocessing"
	 ?defValue nil
	 ?buttonLocation 'left
	 ?value nil
	 ?callback "_IMFCreateLPAValeModuleLPAPreprocessToggleCB(hiGetCurrentForm())"
	 )

      f_addMPTFile = hiCreateBooleanButton(
	 ?name 'addMPTFile
	 ?buttonText "add LPA MPT file"
	 ?defValue nil
	 ?buttonLocation 'left
	 ?value nil
	 )


      f_LPAPreprocessingTCL = hiCreateFileSelectorField( 
	 ?name 'lpaPreprocessingTCLField
	 ?prompt "LPA PreProcessing TCL Script" 
	 ?mode 'existingFile
	 ?value ""
	 ?editable nil
	 ?defValue "" )


      f_PVSCheckingDeck = hiCreateFileSelectorField( 
	 ?name 'pvsRunScriptField
	 ?prompt "PEGASUS Run Script" 
	 ?mode 'existingFile
	 ?value ""
	 ?editable nil
	 ?defValue "" )


      f_PVSCheckingVirtMap = hiCreateFileSelectorField( 
	 ?name 'pvsRunScriptVirtMapField
	 ?prompt "Virtuoso Map For PEGASUS" 
	 ?mode 'existingFile
	 ?value ""
	 ?editable nil
	 ?defValue "" )

      f_PVSCheckingRules = hiCreateFileSelectorField( 
	 ?name 'pvsRunScriptRulesField
	 ?prompt "PEGASUS Applicable Rules File" 
	 ?mode 'existingFile
	 ?value ""
	 ?editable nil
	 ?defValue "" )

      f_PVSMinBloat = hiCreateStringField( 
	 ?name 'pvsMinBloatField
	 ?prompt "PEGASUS Min Bloat:" 
	 ?editable nil
	 ?value "0.2"
	 ?defValue "0.2" )

      f_PVSMinFilterBloat = hiCreateStringField(
	 ?name 'pvsMinFilterBloatField
	 ?prompt "PEGASUS Min Filter Bloat:" 
	 ?editable nil
	 ?value "0.1"
	 ?defValue "0.1" )

      f_valeDir = hiCreateCyclicField(
	 ?name 'valeDir
	 ?prompt "VALE directory:" 
	 ?choices valeDirs)	 



      f_valeConf = hiCreateStringField( 
	 ?name 'valeConfFile
	 ?prompt "VALE conf file:" 
	 ?editable nil
	 ?defValue valeConfigFile)



      myForm = hiCreateAppForm( 
	 ?name 'createLPAValeOption
	 ?formTitle "Create VALE Pattern Base (LPA) Module"
	 ?formType 'nonoptions 
	 ?unmapAfterCB t
	 ?initialSize (800:660)
	 ?callback "_IMFCreateLPAValeModuleCB(hiGetCurrentForm())"
	 ?fields list( 
	    list(f_frame               baseX:baseY 780:620 10)
	    list(f_moduleName          baseX+incrX:baseY+incrY 590:20 150)
	    list(f_moduleVersion       610:baseY+incrY 170:20 100) 
	    list(f_moduleDescription   baseX+incrX:baseY+2*incrY 760:20 150)
	    list(f_moduleSlider        baseX+incrX:baseY+3*incrY 590:20 150)
	    list(f_moduleNumber        610:baseY+3*incrY 170:20 100)
	    list(f_copyBaseLPAFiles    baseX+incrX:baseY+4*incrY 200:20)
	    list(f_showAllMarkers      180:baseY+4*incrY 150:20 )
	    list(f_hierarchyToggle    340:baseY+4*incrY 150:20 )
	    list(f_lpaCPUs             500:baseY+4*incrY 200:20 100)
	    list(f_XmlSelector         baseX+incrX:baseY+5*incrY 760:20 200)
	    list(f_layerOrder          baseX+incrX:baseY+6*incrY 760:20 200)
	    list(f_layerMapSelector    baseX+incrX:baseY+7*incrY 760:20 200)
	    list(f_streamoutMapSelector  baseX+incrX:baseY+8*incrY 760:20 200)
	    list(f_PreProframe         
	       baseX+incrX:baseY+9*incrY 760:2*incrY+20 10)
	    list(f_doLPAPreprocessing  baseX+2*incrX:baseY+9*incrY+10 200:20 )
	    list(f_addMPTFile          
	       baseX+2*incrX+200:baseY+9*incrY+10 200:20 )
	    list(f_LPAPreprocessingTCL 
	       baseX+2*incrX:baseY+10*incrY+10 740:20 200)
	    list(f_Pegasusframe        
	       baseX+incrX:baseY+11*incrY+20 760:5*incrY+50 10)
	    list(f_doPVSChecking       baseX+2*incrX:baseY+11*incrY+30 740:20)
	    list(f_PVSCheckingDeck     
	       baseX+2*incrX:baseY+12*incrY+30 740:20 200)
	    list(f_PVSCheckingVirtMap  
	       baseX+2*incrX:baseY+13*incrY+30 740:20 200)
	    list(f_PVSCheckingRules    
	       baseX+2*incrX:baseY+14*incrY+30 740:20 200)
	    list(f_PVSMinBloat         
	       baseX+2*incrX:baseY+15*incrY+30 740:20 200)
	    list(f_PVSMinFilterBloat   
	       baseX+2*incrX:baseY+16*incrY+30 740:20 200)
	    list(f_valeDir            
	       baseX+incrX:baseY+17*incrY+40 760:20 200)
	    list(f_valeConf           
	       baseX+incrX:baseY+18*incrY+40 760:20 200))
	 )

      tipTable = makeTable("LPAValeOptionToolTips")

      tipTable['newValeModuleNumber]       = 
      "VALE compModule Number recommended"

      tipTable['newValeModuleName]         = 
      "Module Name.\nAll include files will be labeled with this name"
      
      tipTable['newValeModuleVersion]      = 
      "Module Version.\n All include files will be labeled with this version."
      
      tipTable['newValeModuleDescription]  = 
      "Module Description.\n This will be the text of the Menu option"

      tipTable['newValeModuleSlider]       = 
      "Slider Name.\n Which VALE submenu will this be in"

      tipTable['copyLPAFilesToggle]        = 
      "If enabled requires you to provide input xml pattern file, lpa layer map,\
 and virtuoso stream out map.\n\
If disabled will create dummy files which you will need to replace."

      tipTable['XmlSelector]               = 
      "LPA pattern file"
      tipTable['addMPTFile]                = 
      "Adds MPT file to LPA config file. LPA assumes mptfile is\
 VALE_RUNDIR/wd.<module_name>_<topcell name>/preproc/INTERMEDIATE.gds.\
 This can be changed in the config file if necessary"

      tipTable['layerMapSelector]          = 
      "LPA layer map"
      tipTable['streamoutMapSelector]      = 
      "Virtuoso stream out map used for LPA"
      
      tipTable['layerOrderField]           = 
      "layer order used by LPA.\nThis is autodetected from the pattern file.\
 If you do pattern mappings or want to not run all the layers edit as\
 desired"
      tipTable['doPVSCheckingButton]       = 
      "Enable PEGASUS/PVS DRC checking.\nEnabling allows editing of the PEGASUS\
 fields"
      tipTable['showAllMarkersToggle]      = 
      "All markers are deleted after run unless this is enabled"
      tipTable['hierarchyToggle]           = 
      "Allow fixes in subcells. Default is to only do fixes in top cell. Not\
 enabled for all fixing types"
      tipTable['doLPAPreprocess]           = 
      "Enable adding a preprocess deck for lpa"
      tipTable['lpaPreprocessingTCLField]  = 
      "LPA preprocess file."
      tipTable['pvsRunScriptField]         = 
      "DRC PEGASUS script to use"
      tipTable['pvsRunScriptVirtMapField]  = 
      "Virtuoso map for PEGASUS DRC run"
      tipTable['pvsRunScriptRulesField]    = 
      "file containing which rules to use in the PEGASUS DRC deck"
      tipTable['pvsMinBloatField]          = 
      "Halo around pattern marker to use for PVS rule violation detection"
      tipTable['pvsMinFilterBloatField]    = 
      "The halo around the pattern marker to use to find DRC violations "
      tipTable['lpaCPUsField]              = 
      "Number of CPU's to run. This is for rsh local host\n"


      _IMFapplyTipTableForhiToolTips(tipTable createLPAValeOption)      
      hiDisplayForm(myForm)      
      )

   )


procedure(_IMFapplyTipTableForhiToolTips(table form)
      foreach(key table
	 get(form key)->hiToolTip = table[key] 
	 )
   )

procedure(_IMFcompModNameAndVersionIsUsed(defaultsFile name version) 

   prog((lines inPort number nlines nameLines nameMatches versionLines 
      stringToMatch oldVersion line)
      inPort =  infile(defaultsFile)      
      lines = list()


      ;; read in file
      while(gets(line inPort)
	 lines=append(lines list(line))
	 )
      close(inPort)

      ;; get rid of comments
      rexCompile(";.*")
      nlines = mapcar(lambda( (x) rexReplace(x "" 0) ) lines)
      
      ;; find compMod numbers
      nameLines= rexMatchList("_IMFdat->compMod\\([0-9]+\\)->name" nlines)

      nameMatches = rexMatchList(name nameLines)


      when(length(nameMatches) == 0  return(nil))

      versionLines = rexMatchList("_IMFdat->compMod\\([0-9]+\\)->version" lines)	 
      
      foreach(match nameMatches
	 
	 rexCompile("_IMFdat->compMod\\([0-9]+\\)")
	 rexExecute(match)
	 number = rexSubstitute("\\1")

	 stringToMatch = strcat( "_IMFdat->compMod" 
	    number "->version[ ]*=[ ]*\"\\([a-zA-Z0-9]+\\)\"" )
	 
	 rexCompile(stringToMatch)
	 foreach(vLine versionLines

	    when(rexExecute(vLine)
	       oldVersion = rexSubstitute("\\1") 
	       when(oldVersion == version return(t))
	       )
	    )
	 )
      
      return(nil)
      )
   )	   






procedure(_IMFcreateDocsEntry(valeDir moduleName)
   let( (filename outP)
      filename = strcat(valeDir "/SKILL/docs/" moduleName ".txt")
      outP = outfile(filename)      

      fprintf(outP 
"VALE Framework Component Module:\n\
________________________________\n\n\
Description\n\
___________\n\n\
Dependencies\n\
____________\n\n\
Input Requirements:\n\
___________________\n\n\
Output:\n\
_______\n\n\
Development Notes:\n\
__________________\n\n\
Known Issues:\n\
____________:\n\n")

      close(outP)
      printf("VALE INFO: Created documentation file %s\n" filename)
      printf("VALE INFO: Please annotate appropriately.\n")
      )
   )



procedure(_IMFaddLPAValeEntry( form valeDir valeConfigFile compModNum
      moduleName version shortName description slider copyLPAFiles 
      xmlFile layerMapFile streamoutMapFile showAllMarkers 
      doPVSChecking addPreprocess preprocessFileName  minBloat 
      minFilterBloat pvsScriptFile pvsMapFile pvsRuleFile lpaCPUs
      fixHierarchically addMPTFile layerOrder) 


   prog( (defaultsFile fields layerOrderList compModSkillFile 
	 confFileName lpaInitFileName )

      defaultsFile = valeConfigFile
      ;; reset all field highlights       
      fields = list( 'valeConfFile 'newValeModuleNumber
         'newValeModuleName 'newValeModuleVersion 'newValeModuleName 
	 'newValeModuleDescription  'XmlSelector
         'layerMapSelector 'streamoutMapSelector 'lpaPreprocessingTCLField 
	 'pvsMinBloatField 'pvsMinFilterBloatField 'pvsRunScriptField
         'pvsRunScriptVirtMapField 'pvsRunScriptRulesField 'lpaCPUsField )

      ;; reset all field highlights       
      foreach( field fields
	 hiHighlightField(form field 'background)      
	 )

      defaultsFile = valeConfigFile
      
      unless(plusp(atoi(compModNum))  
	 printf("VALE ERROR: Module number needs to be a positive integer\n")
	 hiHighlightField(form 'newValeModuleNumber 'error)
	 return(nil)
	 )	 
      when(_IMFcompModNumberIsUsed(defaultsFile compModNum)
	 printf("VALE ERROR: Module number already used\n")
  	 hiHighlightField(form 'newValeModuleNumber 'error)
	 return(nil)
	 )

      when(blankstrp(moduleName)
	 printf("VALE ERROR: Module Name blank, please provide\n")
  	 hiHighlightField(form 'newValeModuleName 'error)
	 return(nil)
	 )
      when(rexMatchp("[ \t\n]+" moduleName)
	 printf("VALE ERROR: Module Name \"%s\" must not contain white space,\n\
VALE ERROR: please remove white space from name\n" moduleName)
  	 hiHighlightField(form 'newValeModuleName 'error)
	 return(nil)
	 )

      when(blankstrp(description)
	 printf("VALE ERROR: Module Description blank, please provide\n")
  	 hiHighlightField(form 'newValeModuleDescription 'error)
	 return(nil)
	 )
      when(blankstrp(slider)
	 printf("VALE ERROR: Module Slider blank, please provide\n")
  	 hiHighlightField(form 'newValeModuleSlider 'error)
	 return(nil)
	 )
      when(blankstrp(xmlFile)
	 printf("VALE ERROR: Pattern xml file blank, please provide\n")
  	 hiHighlightField(form 'XmlSelector 'error)
	 return(nil)
	 )
      when(blankstrp(layerMapFile)
	 printf("VALE ERROR: LPA layer map file blank, please provide\n")
  	 hiHighlightField(form 'layerMapSelector 'error)
	 return(nil)
	 )
      
      when(blankstrp(streamoutMapFile)
	 printf("VALE ERROR: Stream out file blank, please provide\n")
  	 hiHighlightField(form 'streamoutMapSelector 'error)
	 return(nil)
	 )


      when(_IMFcompModNameAndVersionIsUsed(defaultsFile moduleName version)
	 printf("VALE ERROR:\
 Module name and version in use please increment version\n")
  	 hiHighlightField(form 'newValeModuleName 'error)
  	 hiHighlightField(form 'newValeModuleVersion 'error)

	 return(nil)
	 )
      when(copyLPAFiles
	 unless(isFile(xmlFile) 
	    printf("VALE ERROR: Specified LPA pattern file is not a file,\
 please provide correct path to file\n")
	    hiHighlightField(form 'XmlSelector 'error)
	    return(nil)
	    )

	 unless(isFile(layerMapFile) 
	    printf("VALE ERROR: Specified LPA layer map is not a file,\
 please provide correcte path to file\n")
	    hiHighlightField(form 'layerMapSelector 'error)
	    return(nil)
	    )

	 unless(isFile(streamoutMapFile) 
	    printf("VALE ERROR: Specified Virtuoso stream out map is not a file,\
 please provide correcte path to file\n")
	    hiHighlightField(form 'streamoutMapSelector 'error)
	    return(nil)
	    )
	 )

      
      printf("VALE INFO: IMFcompMod%s With name %s and version %s to %s\n" 
         compModNum moduleName version  valeConfigFile) 

      _IMFappendNewValeFunctionToConfigFile(defaultsFile compModNum moduleName
	 version shortName  description slider  showAllMarkers doPVSChecking )

      compModSkillFile = (strcat valeDir "/SKILL/IMFcompMod" compModNum ".il") 

      printf("VALE INFO: Creating %s\n" compModSkillFile)

      _IMFwriteIMFcompMod(compModSkillFile compModNum  
	 minBloat minFilterBloat fixHierarchically)
      
      printf("VALE INFO: Creating %s/Include/%s_%s\n" 
	 valeDir moduleName version)

      if(copyLPAFiles
	 then 

	 ;; make sure xmlFile layerMapFile and streamoutMapFile are files 
	 csh(strcat("mkdir "  valeDir "/Include/" moduleName "_" version ))
	 ;;	 layerOrderList = _IMFreturnPrimaryLayersFromXML(xmlFile)
	 unless(listp(layerOrder)
	    layerOrderList = parseString(layerOrder)	 
	    )
	 confFileName = 
	 sprintf(nil "%s/Include/%s_%s/%s%s" valeDir moduleName version moduleName ".conf")

	 printf("VALE INFO: Creating %s\n" confFileName)
	 _IMFcreateLPAConfFile(confFileName moduleName version 
	    addPreprocess layerOrderList addMPTFile)
	 lpaInitFileName = 
	 sprintf(nil "%s/Include/%s_%s/%s%s" valeDir moduleName version moduleName  ".lpainit")

	 printf("VALE INFO: Creating %s\n" lpaInitFileName)
	 _IMFcreateLPAlpainitFile(lpaInitFileName  lpaCPUs)
	 
	 _IMFcopyValeIncludeFile(xmlFile valeDir moduleName version ".xml")
	 _IMFcopyValeIncludeFile(layerMapFile valeDir moduleName version ".lpa_map")
	 _IMFcopyValeIncludeFile(streamoutMapFile 
	    valeDir moduleName version ".streamout_map")
	 
	 ;;;; place lpa template files
	 else
	 layerOrderList = list( "M2")
	 csh(strcat("mkdir "  valeDir "/Include/" moduleName "_" version ))
	 confFileName = 
	 sprintf(nil "%s/Include/%s_%s/%s%s" valeDir moduleName version moduleName ".conf")
	 printf("VALE INFO: Creating %s\n" confFileName)
	 _IMFcreateLPAConfFile(confFileName moduleName version 
	    addPreprocess layerOrderList addMPTFile)
	 lpaInitFileName = 
	 sprintf(nil "%s/Include/%s_%s/%s%s" 
	    valeDir moduleName version moduleName ".lpainit")
	 printf("VALE INFO: Creating %s\n" lpaInitFileName)
	 _IMFcreateLPAlpainitFile(lpaInitFileName lpaCPUs)
	 
	 _IMFcreateTemplateLPAXmlFile(valeDir moduleName version)
	 _IMFcreateTemplateLPAlayerMapFile(valeDir moduleName version)
	 _IMFcreateTemplateLPAstreamoutMapFile(valeDir moduleName version)
	 )

      when(addPreprocess
	 _IMFcopyValeIncludeFile(preprocessFileName 
	    valeDir moduleName version  ".preprocess.tcl")
	 )
      when(doPVSChecking 
	 _IMFcopyValeIncludeFile(pvsScriptFile 
	    valeDir moduleName version ".pvl")
	 _IMFcopyValeIncludeFile(pvsMapFile 
	    valeDir moduleName version ".pvs_virt_layer_map")
	 when(strncmp(pvsRuleFile "" 1) == 1
	    _IMFcopyValeIncludeFile(pvsRuleFile 
	       valeDir moduleName version ".pvs_rules")
	    )
	 )

      _IMFcreateDocsEntry(valeDir moduleName)
;;    Add to menu
      _IMFaddItemToPDMenu(description slider compModNum)	
;; need to source skill file
      load(compModSkillFile)      
      return(t)
      )
   )


procedure(_IMFmoveModuleCB(form)
   prog((valeConfigFilePath inPort outPort lines matchLines outFile modString
	 skillLines newString skillFile oldSkillFile cmd line matchString
         componentModule newComponentModule newLine newMatchLines 
	 moduleDescription templist tmpString updatedString)

      ;; JF 191205 removed 4 passed parameters in lieu of single form par
      ;; rebuild variables for this procedure from the form parameter
      ;; JPC 191211 changed form for being able to move slider as well
      ;;"%d Description:%s Slider:%s"
      templist = parseString(form->existingValeModuleNumber->value ":")           
      componentModule =
         car(parseString(car(templist) " "))
      matchString = " Slider"      
      rexCompile(matchString)      
      moduleDescription =  rexReplace(nth(1 templist) "" 0)   
      newComponentModule = form->newValeModuleNumber->value
      valeConfigFilePath = form->valeConfFile->value



      oldSkillFile = ""      
      foreach(pdir form->valeDir->choices
	 tmpString = 
	 sprintf(nil "%s/SKILL/IMFcompMod%s.il" pdir componentModule)
	when(isFile(tmpString) 
	    oldSkillFile = tmpString)
	 )  
      when(oldSkillFile == ""
	 printf("VALE ERROR: Module is not a SKILL component Module.\n")
	 printf("VALE ERROR:\
 Module number can be changed by just editing configuration file.\n")
	 return(nil)
	 )
      	 
      skillFile = sprintf(nil "%s/SKILL/IMFcompMod%s.il"
         form->valeDir->value newComponentModule)

      unless(plusp(atoi(newComponentModule))  
	 printf("VALE ERROR: Module number needs to be a positive integer\n")
         ;; JF 191205 form variable needed for this line
	 hiHighlightField(form 'newValeModuleNumber 'error)
	 return(nil)
	 )	 

      when(_IMFcompModNumberIsUsed(valeConfigFilePath newComponentModule) 
	 printf("VALE ERROR: Module number already used\n")
	 return(nil)
	 )

      unless(isWritable(valeConfigFilePath)
	 printf("VALE ERROR:\
 You do not have write permissions for the IMFdefaults file: %s\n"
	    valeConfigFilePath)
	 return(nil)
	 )

      unless(isWritable(oldSkillFile)
	 printf("VALE ERROR:\
 You do not have write permissions for the SKILL file: %s\n" oldSkillFile)
	 return(nil)
	 )
      

      inPort = infile(valeConfigFilePath)
      ;; Find compMod lines in defaults file
      while(gets(line inPort)
	 lines=append(lines list(line))
	 )
      close(inPort)


      matchString = sprintf(nil "^_IMFdat->compMod%s" componentModule)
      matchLines = rexMatchList(matchString lines)
      
      outFile = strcat(valeConfigFilePath ".tmp")

      outPort = outfile(outFile "w")
      modString = sprintf(nil "^_IMFdat->compMod%s" componentModule)
      
      newString = sprintf(nil ";;_IMFdat->compMod%s" componentModule)
      rexCompile(modString)

      ;; comment out those lines
      foreach(li lines
	 ;;		    printf("%s" li)
	 
	 fprintf(outPort "%s" rexReplace(li newString 1))
	 )

      ;; add lines with new component module number 
      fprintf(outPort 
	 "\n\n;;Module defined by moving compMod%s to this mod\n" 
	 componentModule)
      newString = sprintf(nil "_IMFdat->compMod%s" newComponentModule)
      newMatchLines = list()   
   
      foreach(li matchLines
	 newLine = rexReplace(li newString 1)
	 newMatchLines = append(newMatchLines list(newLine))
	 )	 
      modString = sprintf(nil "^_IMFdat->compMod%s->slider" newComponentModule)
      rexCompile(modString)      
      foreach(li newMatchLines
	 unless(rexExecute(li)
	    fprintf(outPort "%s" li))
;; setup internal memory with the moved compmod data
	 evalstring(li)	 
)
      fprintf(outPort "_IMFdat->compMod%s->slider = \"%s\"\n" 
	 newComponentModule form->newValeModuleSlider->value)
      evalstring(sprintf(nil  "_IMFdat->compMod%s->slider = \"%s\"\n" 
	 newComponentModule form->newValeModuleSlider->value))     
      close(outPort)

      ;; create new IMFcompMod<mew number> file from IMFcompMod<number>
      
      inPort = infile(oldSkillFile)
      ;; Find compMod lines in defaults file
      while(gets(line inPort)
	 skillLines=append(skillLines list(line))
	 )
      close(inPort)

      outPort = outfile(skillFile)

      ;; replace compMod<number with compMod<new number>
      modString = sprintf(nil "compMod%s" componentModule)
      rexCompile(modString)
      newString = sprintf(nil "compMod%s" newComponentModule)
      foreach(li skillLines
	 updatedString = rexReplace(li newString 0)
	 fprintf(outPort "%s" updatedString))
      close(outPort)
      
      ;; mv defaults file to .old
      cmd = sprintf(nil "mv %s %s.old\n" valeConfigFilePath valeConfigFilePath)
      printf("%s" cmd)
      csh(cmd)
      ;; mv temp defaults file to defaults file
      cmd = sprintf(nil "mv %s.tmp %s\n" valeConfigFilePath valeConfigFilePath)
      printf("%s" cmd)
      csh(cmd)
      ;; mv skill file to skill.unused
      cmd = sprintf(nil "mv %s %s.unused\n" oldSkillFile oldSkillFile)
      printf("%s" cmd)
      csh(cmd)
      ;; need to reset VALE menu
      ;; remove module from previous spot
      _IMFremovePDMenuItem(moduleDescription)
      ;; add module to new spot      
      _IMFaddItemToPDMenu(moduleDescription 
	 form->newValeModuleSlider->value newComponentModule)
      ;;load the new skill file
      load(skillFile)      
      return(t)
      )
   )



procedure(VALEmoveModule(valeDirs valeConfigFile 
      @optional (debug nil)) 
   (let (f_frame  f_valeDir f_valeConf valeConfFilePath f_existing_moduleNumber 
	 f_new_moduleNumber mvModForm moveVALEModuleForm availSliders 
	 f_moduleSlider	newValeModuleSlider tipTable
	 (baseX 10)
	 (baseY 10)
	 (incrY 30)
	 (incrX 10))

      f_frame = hiCreateFrameField(
         ?name 'valeMoveModule
         ?labelText "Move VALE Module"
         ?help      'nil
         ?invisible 'nil
         )
      valeConfFilePath = valeConfigFile



      availSliders = _IMFgetVALESliders(valeConfigFile)
      availSliders = append(availSliders list("Create New Vale Slider ..."))
      f_moduleSlider = hiCreateCyclicField(
	 ?name 'newValeModuleSlider
	 ?prompt "Module Slider:" 
	 ?callback '_IMFSliderCB
	 ?choices availSliders)

      f_existing_moduleNumber = hiCreateCyclicField(
	 ?name 'existingValeModuleNumber
	 ?value ""
	 ?prompt "Existing Module Number:"
;	 ?callback '_IMFmoveModuleModuleNumberCB	 
	 ?choices _IMFcompModNumbersUsedWithDescription(valeConfFilePath))



      f_new_moduleNumber = hiCreateStringField(
         ?name 'newValeModuleNumber
         ?prompt "New Module Number:"
         ?editable t
         ?value "")


      f_valeDir = hiCreateCyclicField(
         ?name 'valeDir
         ?prompt "VALE directory:" 
	 ?choices valeDirs)	 

      f_valeConf = hiCreateStringField(
         ?name 'valeConfFile
         ?prompt "VALE conf file:" 
         ?editable nil
         ?defValue valeConfigFile)



      mvModForm = hiCreateAppForm(
         ?name 'moveVALEModuleForm
         ?formTitle "Move VALE Module"
         ?formType 'nonoptions 
         ?unmapAfterCB t
         ?initialSize (800:240)
         ?callback "_IMFmoveVALEModuleCB(hiGetCurrentForm())"
         ?fields list( 
            list(f_frame                   baseX:baseY 780:160 10)
            list(f_existing_moduleNumber   baseX+incrX:baseY+15 340:30 160)
            list(f_moduleSlider            baseX+incrX:baseY+15+incrY 340:30 160)
            list(f_new_moduleNumber        
	       baseX+incrX:baseY+15+2*incrY 760:30 160)
            list(f_valeDir                 
	       baseX+incrX:baseY+3*incrY+15 760:30 160)
            list(f_valeConf                
	       baseX+incrX:baseY+4*incrY+15 760:30 160)))


      tipTable = makeTable("moveVALEModuleForm")

      tipTable['existingValeModuleNumber] =      
      "existing VALE compModule Number "
      tipTable['newValeModuleNumber] =       
      "new VALE compModule Number desired"
      _IMFapplyTipTableForhiToolTips(tipTable  moveVALEModuleForm)
      hiDisplayForm(mvModForm)
      )

   )

procedure(_IMFmoveVALEModuleCB(form)
   let( (success)
      ;; JF 191205 simply pass form, needed for field highlighting
      success = _IMFmoveModuleCB(form)
      hiSetCallbackStatus(form success)
      )
   )



;; Procedure to get the module numbers currently used in the vale setup
procedure(_IMFcompModNumbersUsed(defaultsFile) 


   prog((element lines  matchLines existingNumbs inPort line)
      inPort = infile(defaultsFile)      
      lines = list()
      matchLines = list()
      existingNumbs = list()
      ;; read in file
      rexCompile(";[.]*")
      while(gets(line inPort)
	 ;; need to get rid of comments -- assume none quoted
	 line = rexReplace(line "" 1)
	 lines=append(lines list(line))
	 )
      close(inPort)
      ;; find compMod numbers
      matchLines= rexMatchList("_IMFdat->compMod" lines)
      rexCompile("_IMFdat->compMod\\([0-9_]+\\)")

      foreach(match matchLines
	 rexExecute(match)
	 element = rexSubstitute("\\1")

	 if(lindex(existingNumbs atoi(element)) == nil  then  
	    existingNumbs= append(existingNumbs list(atoi(element))))
	 )

      return(existingNumbs)
      )
   )	   


procedure(_IMFcompModNumberIsUsed(defaultsFile  number) 
   prog((existingNumbs)
      existingNumbs = _IMFcompModNumbersUsed(defaultsFile)
      if(lindex(existingNumbs atoi(number)) == nil
	 then
	 return(nil)
	 else
	 return(t)
	 )
      )	   
   )

;;

procedure(_IMFcompModNumbersUsedWithDescription(defaultsFile) 


   prog((lines matchLines existingNumbs element descriptionLine line
         description inPort nline matchString numbDescPair numbDescPairList 
         slider sliderLine)
      lines = list()
      matchLines = list()
      existingNumbs = list()
      numbDescPairList = list()
      ;; read in file
      inPort = infile(defaultsFile)
      rexCompile(";.*")
      while(gets(line inPort)
	 ;; need to get rid of comments -- assume none quoted
	 nline = rexReplace(line "" 0)
	 lines = append(lines list(nline))
	 )
      close(inPort)
      ;; find compMod numbers
      matchLines= rexMatchList("_IMFdat->compMod" lines)
      rexCompile("_IMFdat->compMod\\([0-9_]+\\)")

      foreach(match matchLines
	 rexExecute(match)
	 element = rexSubstitute("\\1")

	 if(lindex(existingNumbs atoi(element)) == nil  then  
	    existingNumbs = append(existingNumbs list(atoi(element))))
	 )
      foreach(number sort(existingNumbs 'lessp)
	 matchString = 
	 sprintf(nil "_IMFdat->compMod%d->description[ \t]*=[ \t]*" number)
	 descriptionLine = rexMatchList(matchString lines)
	 description = cadr(parseString(car(descriptionLine) "\"" ))
	 matchString = 
	 sprintf(nil "_IMFdat->compMod%d->slider[ \t]*=[ \t]*" number)
	 sliderLine = rexMatchList(matchString lines)
	 slider = nth(1 parseString(car(sliderLine) "\"" ))
	 numbDescPair = 
	 sprintf(nil "%d Description:%s Slider:%s" number description slider)
	 numbDescPairList = append(numbDescPairList list(numbDescPair))
	 )
      return(numbDescPairList)
      )
   )	   




procedure(_IMFCreateVALESKILLModuleCB(form) 
   let( (success)   
      success = _IMFaddSKILLValeEntry(form->valeDir->value 
	 form->valeConfFile->value 
	 form->newValeModuleNumber->value
	 form->newValeModuleName->value  
	 form->newValeModuleVersion->value  
	 form->newValeModuleName->value  
	 form->newValeModuleDescription->value  
	 form->newValeModuleSlider->value 
	 form->newValeModuleSchemeToggle->value
	 form->newValeModuleCodeField->value
	 form)
      hiSetCallbackStatus(form success)
      )
   )




procedure(_IMFaddSKILLValeEntry(valeDir valeConfigFile compModNum moduleName
             version shortName description slider isScheme code myForm)
   prog((fields defaultsFile identicallyNamedModules compModSkillFile)

      ;; Formatting updates JF 191205
      fields = list('newValeModuleNumber
                    'newValeModuleName
                    'newValeModuleVersion
                    'newValeModuleDescription
                    )

      foreach(field fields
	 hiHighlightField(myForm field 'background)      
      )


      ;; JF 191205 This variable now contains valeDir so no strcat necessary
      defaultsFile = valeConfigFile


      unless(plusp(atoi(compModNum))  
	 printf("VALE ERROR: Module number needs to be a positive integer\n")
	 hiHighlightField(myForm 'newValeModuleNumber 'error)
	 return(nil)
      )	 

      when(_IMFcompModNumberIsUsed(defaultsFile compModNum)
	 printf("VALE ERROR: Module number already used\n")
         ;; JF 191205 changed form to myForm
	 hiHighlightField(myForm 'newValeModuleNumber 'error)
	 return(nil)
      )

      ;; Checking the module name field
      when(blankstrp(moduleName) 
	 printf("VALE ERROR: Module Name blank, please provide\n")
	 hiHighlightField(myForm 'newValeModuleName 'error)
	 return(nil)
      )

      when(rexMatchp("[ \t\n]+" moduleName)
         printf("VALE ERROR: Module Name \"%s\" must not contain " moduleName)
         printf("white space, please remove white space from name\n")
  	 hiHighlightField(myForm 'newValeModuleName 'error)
	 return(nil)
      )

      ;; Checking the module description field
      when(blankstrp(description) 
	 printf("VALE ERROR: Module Description blank, please provide\n")
	 hiHighlightField(myForm 'newValeModuleDescription 'error)
	 return(nil)
      )

      ;; Checking the module slider field
      when(blankstrp(slider) 
	 printf("VALE ERROR: Module Slider blank, please provide\n")
	 hiHighlightField(myForm 'newValeModuleSlider 'error)
	 return(nil)
      )

      when(_IMFcompModNameAndVersionIsUsed(defaultsFile moduleName version)
         printf("VALE ERROR: Module name and version are already used, ")
         printf("please increment version\n")
	 hiHighlightField(myForm 'newValeModuleNumber 'error)
	 hiHighlightField(myForm 'newValeModuleVersion 'error)
	 return(nil)
      )

      identicallyNamedModules =
         _IMFcompModNameIsUsedByModules(defaultsFile moduleName)

      when(length(identicallyNamedModules) > 0
         foreach(module identicallyNamedModules
            printf("VALE INFO: Module %s has same name as new " module)
            printf("requested module, please comment out the old version\n")
         )
      ) 

      printf("VALE INFO: IMFcompMod%s With name %s and version %s to %s\n"
         compModNum moduleName version  valeConfigFile)

      _IMFappendNewValeSKILLFunctionToConfigFile(defaultsFile compModNum
         moduleName version shortName description slider)

      if(isScheme then
         compModSkillFile =
            strcat(valeDir "/SKILL/IMFcompMod" compModNum ".ils")
      else
         compModSkillFile =
            strcat(valeDir "/SKILL/IMFcompMod" compModNum ".il")
      )

      printf("VALE INFO: Creating %s\n" compModSkillFile)

      _IMFwriteSKILLIMFcompMod(compModSkillFile compModNum code)

      _IMFcreateDocsEntry(valeDir moduleName)

;;    Add to menu
      _IMFaddItemToPDMenu(description slider compModNum)	
;; load skillFile
      load(compModSkillFile)
      return(t)

   )
)


procedure(_IMFappendNewValeSKILLFunctionToConfigFile(configFile 
      compModNum moduleName version shortName description slider)
   let((valeConfigPort)   
      valeConfigPort=(outfile configFile "a")
      fprintf(valeConfigPort 
"\n;;VALE created SKILL module from template\n\
_IMFdat->compMod%s = list(nil)\n\
_IMFdat->compMod%s->name = \"%s\"\n\
_IMFdat->compMod%s->version = \"%s\"\n\
_IMFdat->compMod%s->shortName = \"%s\"\n\
_IMFdat->compMod%s->description = \"%s\"\n\
_IMFdat->compMod%s->slider = \"%s\"\n\n\n" 
	 compModNum  compModNum  moduleName  compModNum version  compModNum 
	 shortName compModNum description compModNum slider)
      close(valeConfigPort) 
      evalstring(strcat("_IMFdat->compMod" compModNum " =  list(nil)"))
      evalstring(strcat("_IMFdat->compMod" compModNum "->name = \"" 
	    moduleName "\""))
      evalstring(strcat("_IMFdat->compMod" compModNum "->version = \"" 
	    version "\""))
      evalstring(strcat("_IMFdat->compMod" compModNum "->shortName = \"" 
	    shortName "\""))
      evalstring(strcat("_IMFdat->compMod" compModNum "->description = \"" 
	    description "\""))
      evalstring(strcat("_IMFdat->compMod" compModNum "->slider = \"" 
	    slider "\""))
      )      
   )


procedure(_IMFwriteSKILLIMFcompMod(fileName number inputCode) 

   let( (outputFilePort)
      outputFilePort = outfile(fileName)
      _IMFwriteCadenceCopyrightHeader(outputFilePort)

      _IMFwriteRevision(outputFilePort)

      _IMFwriteSKILLCompmodTemplate(outputFilePort number inputCode)
      
      close(outputFilePort)
      )
   )


procedure(_IMFwriteSKILLCompmodTemplate(outputFilePort compModNumber incCode)
   fprintf(outputFilePort 
"procedure(IMFcompMod%s(\n\
          rtDpl\n\
          @optional\n\
             (debug nil)\n\
          )\n\
   prog((win)\n\
         printf(\"VALE INFO: Starting %s\\n\" rtDpl->description)\n\
         ;; place your SKILL code here.\n%s\n\
         printf(\"VALE INFO: Finished %s\\n\" rtDpl->description)\n\
      return(t)\n   )\n)\n"  compModNumber  "%L"  incCode  "%L")
   )




procedure(_IMFcompModNameIsUsedByModules(defaultsFile name) 


   prog(( number lines existingNumbs  inPort nameLines nameMatches line nlines)
      existingNumbs = list()      
      lines = list()
      ;; read in file
      inPort = infile(defaultsFile)
      while(gets(line inPort)
	 lines=append(lines list(line))
	 )
      close(inPort)
      ;; get rid of comments
      rexCompile(";.*")
      ;nlines = mapcar( lambda( (x) rexReplace(x "" 0) ) lines)
      
      ;; find compMod numbers
      nameLines= rexMatchList("_IMFdat->compMod\\([0-9]+\\)->name" nlines)
      nameMatches = rexMatchList(name nameLines)

      when(length(nameMatches) == 0  return(list()))

      rexCompile("_IMFdat->compMod\\([0-9]+\\)")
      foreach(match nameMatches
	 
	 rexExecute(match)
	 number = rexSubstitute("\\1")
	 existingNumbs = append(existingNumbs list(number))
	 )


      
      return(existingNumbs)
      )
   )	   



procedure(VALEcreateNewVALESkillModule(valeDirs valeConfigFile 
      @optional (debug nil)) 

   let((f_frame f_moduleName  f_moduleDescription  f_moduleSlider f_valeDir 
	 f_valeConf moduleNumber f_schemeToggle f_startMacroButton 
	 f_macroSourceCode f_moduleVersion f_moduleNumber 
	 createVALESKILLModuleForm baseX baseY incrX incrY myForm 
	 f_importSKILLButton availSliders toolTip)

      f_frame = hiCreateFrameField(
	 ?name 'valeCreateLPAVALEFrame
	 ?labelText "Create VALE SKILL Module"
	 ?help      'nil
	 ?invisible 'nil
	 )
      
      moduleNumber = _IMFgetMaxCompModNumber(valeConfigFile) + 10

      f_moduleNumber = hiCreateStringField(
	 ?name 'newValeModuleNumber
	 ?prompt "Module Number:"
	 ?editable t
	 ?value sprintf(nil "%d" moduleNumber))
      
      f_moduleName = hiCreateStringField(
	 ?name 'newValeModuleName
	 ?prompt "Module Name:" 
	 ?editable t)

      f_moduleVersion = hiCreateStringField(
	 ?name 'newValeModuleVersion
	 ?prompt "Module Version: " 
	 ?editable t 
	 ?defValue "V01")

      f_moduleDescription = hiCreateStringField(
	 ?name 'newValeModuleDescription
	 ?prompt "Module Description:" 
	 ?editable t)

      availSliders = _IMFgetVALESliders(valeConfigFile)
      availSliders = append(availSliders list("Create New Vale Slider ..."))
      f_moduleSlider = hiCreateCyclicField(
	 ?name 'newValeModuleSlider
	 ?callback '_IMFSliderCB
	 ?prompt "Module Slider:" 
	 ?choices availSliders)


      f_schemeToggle = hiCreateBooleanButton(
	 ?name 'newValeModuleSchemeToggle
	 ?buttonText "SKILL++"
	 ?defValue nil
	 ?buttonLocation 'left
	 ?value nil
	 ;;	 ?callback "_IMFCopyLPABaseFilesCallback(hiGetCurrentForm())"
	 )

      ;; JF 191205 gray-ed out until implmented
      f_importSKILLButton = hiCreateButton(
	 ?name 'importSKILLButton
	 ?buttonText "Import SKILL File"
	 ?callback
            "_IMFImportSKILLintoBuildASKILLModule(hiGetCurrentForm())"
	 ?enabled nil
         )
      
      f_startMacroButton = hiCreateButtonBoxField(
	 ?name 'newValeModuleStartStopMacro
	 ?choices list("Start" "Stop")
	 ?callback list("_IMFStartMacro(hiGetCurrentForm())" 
	    "_IMFStopMacro(hiGetCurrentForm())")	 
	 ?prompt "Record Virtuoso commands" )	 

      f_macroSourceCode = hiCreateMLTextField(
	 ?name 'newValeModuleCodeField
	 ?enableWordWrap t
	 ?hasVerticalScrollbar t
	 ?hasHorizontalScrollbar t
	 ?prompt "Code to Insert:" 
	 ?editable t)

      f_valeDir = hiCreateCyclicField(
	 ?name 'valeDir
	 ?prompt "VALE directory:" 
	 ?choices valeDirs)	 


      f_valeConf = hiCreateStringField(
	 ?name 'valeConfFile
	 ?prompt "VALE conf file:" 
	 ?editable nil
	 ?defValue valeConfigFile)

      baseX = 10
      baseY = 10
      incrY = 30
      incrX = 10


      myForm = hiCreateAppForm(
	 ?name 'createVALESKILLModuleForm
	 ?formTitle "Create VALE SKILL Module"
	 ?formType 'nonoptions 
	 ?unmapAfterCB t
	 ?initialSize (800:410)
	 ?callback "_IMFCreateVALESKILLModuleCB(hiGetCurrentForm())"
	 ?fields list( 
	    list(f_frame             baseX:baseY 780:370 10)
	    list(f_moduleName        baseX+incrX:baseY+incrY 590:20 150)
	    list(f_moduleVersion     610:baseY+incrY 170:20 100) 
	    list(f_moduleDescription baseX+incrX:baseY+2*incrY 760:20 150)
	    list(f_moduleSlider      baseX+incrX:baseY+3*incrY 590:20 150)
	    list(f_moduleNumber      610:baseY+3*incrY 170:20 100)
	    list(f_schemeToggle      baseX+incrX:baseY+4*incrY 200:20)
	    list(f_startMacroButton  baseX+incrX+220:baseY+4*incrY 300:20 160) 
	    list(f_importSKILLButton baseX+incrX+520:baseY+4*incrY 200:20 160) 	    
	    list(f_macroSourceCode   baseX+incrX:baseY+5*incrY 760:120 150)    
	    list(f_valeDir           baseX+incrX:baseY+9*incrY 760:20 150)
	    list(f_valeConf          baseX+incrX:baseY+10*incrY 760:20 150)))

      toolTip = makeTable("createValeSKILLModuleFormTips")      

      toolTip['newValeModuleNumber]      = 
      "VALE compModule Number recommended"

      toolTip['newValeModuleName]        = 
      "Module Name.\nAll include files will be labeled with this name"

      toolTip['newValeModuleVersion]     = 
      "Module Version.\n All include files will be labeled with this version."

      toolTip['newValeModuleDescription] = 
      "Module Description.\n This will be the text of the Menu option"

      toolTip['newValeModuleSlider]      = 
      "Slider Name.\n Which VALE submenu will this be in"

      _IMFapplyTipTableForhiToolTips(toolTip createVALESKILLModuleForm)      

      hiDisplayForm(myForm)
      )

   )

procedure(_IMFStartMacro(form)
   prog((currentLogFile macroLogFile )   
      macroLogFile = strcat(getWorkingDir() "/VALE_RUNDIR/macro.log")

      ;; could be in a macro. 
      ;; check if current log file name is our macro log file name      
      currentLogFile = hiGetLogFileName()      
      when(strcmp(currentLogFile macroLogFile) == 0 
	 hiEndLog()	 
	 )	 
      hiStartLog(macroLogFile)      

      hiSetCallbackStatus(form t)
      )      
   )

procedure(_IMFStopMacro(form)

   prog((macroLogFile dataline commands inPort matchLines  nline  
	 codeString compat1)
      codeString = ""      
      commands = list()      
      macroLogFile = strcat(getWorkingDir() "/VALE_RUNDIR/macro.log")
      hiEndLog()   
      inPort = infile(macroLogFile)
      while(gets(dataline inPort)
	 commands = append(commands list(dataline)))

      close(inPort)    
      compat1 = pcreCompile("_IMFStopMacro")
      ;;      form->f_macroSourceCode->value = commands   
      matchLines= rexMatchList("\\a " commands)

      foreach(mli matchLines
	 nline = substring(mli 4)
	 unless(pcreExecute(compat1 nline)
	    codeString = sprintf(nil "%s%s" codeString nline)	 
	    )
	 )
      ;;      printf("%s" codeString)    
      form->newValeModuleCodeField->value = codeString      
      hiSetCallbackStatus(form t)
      )
   )  


procedure(_IMFImportSKILLintoBuildASKILLModule(form)
   printf("VALE INFO: Under development\n")   
   )


procedure(VALEremoveModule(valeDirs valeConfigFile @optional (debug nil)) 
   (let (f_frame  f_valeDir f_valeConf valeConfFilePath f_existing_moduleNumber
	 rmModForm removeVALEModuleForm	toolTips   
	 (baseX 10)
	 (baseY 10)
	 (incrY 30)
	 (incrX 10))

      f_frame = hiCreateFrameField(
         ?name 'valeMoveModule
         ?labelText "Remove a VALE Module"
         ?help      'nil
         ?invisible 'nil
         )
      valeConfFilePath = valeConfigFile


      f_existing_moduleNumber = hiCreateCyclicField(
	 ?name 'existingValeModuleNumber
	 ?value ""
	 ?prompt "Existing Module Number:"
	 ?choices _IMFcompModNumbersUsedWithDescription(valeConfFilePath))



      f_valeDir = hiCreateCyclicField(
         ?name 'valeDir
         ?prompt "VALE directory:" 
	 ?choices valeDirs)	 

      f_valeConf = hiCreateStringField(
         ?name 'valeConfFile
         ?prompt "VALE conf file:" 
         ?editable nil
         ?defValue valeConfigFile)



      rmModForm = hiCreateAppForm(
         ?name 'removeVALEModuleForm
         ?formTitle "Remove VALE Module"
         ?formType 'nonoptions 
         ?unmapAfterCB t
         ?initialSize (800:200)
         ?callback "_IMFremoveVALEModuleCB(hiGetCurrentForm() valeDirs)"
         ?fields list( 
            list(f_frame               baseX:baseY 780:160 10)
            list(f_existing_moduleNumber   baseX+incrX:baseY+15 340:30 160)
            list(f_valeDir             baseX+incrX:baseY+incrY+15 760:30 160)
            list(f_valeConf          baseX+incrX:baseY+2*incrY+15 760:30 160)))

      toolTips = makeTable("removeVALEModuleForm")      

      toolTips['existingValeModuleNumber] =      
      "existing VALE compModule Number to remove"

      toolTips['valeDir] =
      "Removed modules moved to REMOVED directory under this directory"
      _IMFapplyTipTableForhiToolTips(toolTips removeVALEModuleForm)      
      hiDisplayForm(rmModForm)
      )

   )


procedure(_IMFremoveVALEModuleCB(form dirs)
   let( (success)
      ;; JF 191205 simply pass form, needed for field highlighting
      success = _IMFremoveModuleCB(form dirs)
      hiSetCallbackStatus(form success)
      )
   )

procedure(_IMFremoveModuleCB(form dirs)
   prog((valeConfigFilePath inPort outPort lines matchLines outFile modString
   	 newString oldSkillFile cmd line matchString nameMatchLine 
	 versionMatchLine componentModule skillFilesToRemove removedDir 
	 removedSkillDir removedIncludeDir removedSkillDocsDir 
	 removedSkillCxt64bitDir moduleName moduleVersion foundDir
         descMatchLine moduleDesc)

      ;; JF 191205 removed 4 passed parameters in lieu of single form par
      ;; rebuild variables for this procedure from the form parameter
      componentModule =
         car(parseString(form->existingValeModuleNumber->value " "))
;;      newComponentModule = form->newValeModuleNumber->value
      valeConfigFilePath = form->valeConfFile->value

      unless(isWritable(form->valeDir->value)
	 printf("VALE ERROR:\
 You need write permission of the VALE directory to remove VALE modules\n")	 
	 return(nil)
	 )      

      removedDir = strcat(form->valeDir->value "/REMOVED")
      removedSkillDir = strcat(removedDir "/SKILL")
      removedSkillDocsDir = strcat(removedSkillDir "/docs")

      removedIncludeDir = strcat(removedDir "/Include")      

      removedSkillCxt64bitDir = strcat(removedSkillDir "/cxt/64bit")      
;; find old SKILL File
      skillFilesToRemove = list()
      foreach(path dirs
	 oldSkillFile = sprintf(nil "%s/SKILL/IMFcompMod%s.il"
            path componentModule)
	 when(isFile(oldSkillFile) 
	    foundDir = path	    
	    skillFilesToRemove= cons(oldSkillFile skillFilesToRemove )
	    )	    
	 )
	    


      unless(isWritable(valeConfigFilePath)
	 printf("VALE ERROR:\
 You do not have write permissions for the IMFdefaults file: %s\n" 
	    valeConfigFilePath)
	 return(nil)
	 )
      foreach(file skillFilesToRemove       
	 unless(isWritable(file)
	    printf("VALE ERROR:\
 You do not have write permissions for the SKILL file: %s\n" file)
	    return(nil)
	    )
	 )
      

      inPort = infile(valeConfigFilePath)
      ;; Find compMod lines in defaults file
      while(gets(line inPort)
	 lines=append(lines list(line))
	 )
      close(inPort)


      matchString = sprintf(nil "^_IMFdat->compMod%s" componentModule)
      matchLines = rexMatchList(matchString lines)


      
      outFile = strcat(valeConfigFilePath ".tmp")

      outPort = outfile(outFile "w")
      modString = sprintf(nil "^_IMFdat->compMod%s" componentModule)
      
      newString = sprintf(nil ";;removed\n;;_IMFdat->compMod%s" componentModule)
      rexCompile(modString)

      ;; comment out those lines
      foreach(li lines
	 ;;		    printf("%s" li)
	 
	 fprintf(outPort "%s" rexReplace(li newString 1))
	 )

      close(outPort)


      ;;find component module name and version
      matchString = sprintf(nil "^_IMFdat->compMod%s->name" componentModule)
      nameMatchLine =  rexMatchList(matchString matchLines)

      moduleName =
      nth(1 parseString(car(last(parseString(car(nameMatchLine) "="))) "\"") )


      matchString = sprintf(nil "^_IMFdat->compMod%s->version" componentModule)  
      versionMatchLine = rexMatchList(matchString matchLines)
      when( versionMatchLine      
	 moduleVersion = 
	 nth(1 parseString(car(last(parseString(car(versionMatchLine) "="))) "\""))
	 )
      ;; mv defaults file to .old

      cmd = sprintf(nil "mv %s %s.old\n" valeConfigFilePath valeConfigFilePath)
      printf("%s" cmd)
      csh(cmd)
      ;; mv temp defaults file to defaults file
      cmd = sprintf(nil "mv %s.tmp %s\n" valeConfigFilePath valeConfigFilePath)
      printf("%s" cmd)
      csh(cmd)

      ;;find component module description for removing the menu 
      matchString = 
         sprintf(nil "^_IMFdat->compMod%s->description" componentModule)
      descMatchLine = rexMatchList(matchString matchLines)

      moduleDesc =
         nth(1 parseString(
            car(last(parseString(car(descMatchLine) "="))) "\"") )

      
      ;; check that all directories exists. if not create it

      foreach(newDir list(removedSkillDocsDir removedIncludeDir 
	    removedSkillCxt64bitDir)      
	 createDirHier(newDir)
	 )	 

      foreach(file skillFilesToRemove    
	 cmd = sprintf(nil 
	    "mv %s %s\n" file 
	    sprintf(nil "%s/IMFcompMod%s.il" removedSkillDir componentModule))
	 printf("%s" cmd)
	 csh(cmd)

	 )


      ;;move all skill docs to removedSkillDocsDir
      when(isFile(sprintf(nil "%s/SKILL/docs/%s.txt" foundDir moduleName ))    
	 cmd = 
	 sprintf(nil "mv -f %s/SKILL/docs/%s.txt %s" 
	    foundDir moduleName removedSkillDocsDir)    
	 printf("VALE: moving doc files with: %s\n" cmd)
	 csh(cmd)
	 )

      ;;move all cxt files to removedSkillCxtDir      
      when(isFile(sprintf(nil "%s/SKILL/cxt/64bit/cm%s.cxt" 
	       foundDir componentModule))      
	 cmd = sprintf(nil "mv -f %s/SKILL/cxt/64bit/cm%s.cxt %s" 
	    foundDir componentModule removedSkillCxt64bitDir)    
	 printf("VALE: moving any cxt files with: %s\n" cmd)
	 csh(cmd)
	 )

      ;;move all Inlude files to removedIncludeDir      
      if( versionMatchLine     
	 then 	 
	 cmd = sprintf(nil "mv -f %s/Include/%s_%s* %s" 
	    foundDir moduleName moduleVersion removedIncludeDir)    
	 else
	 cmd = sprintf(nil "mv -f %s/Include/%s* %s" 
	    foundDir moduleName  removedIncludeDir)    
	 )
	 printf("VALE: moving any Included files with: %s\n" cmd)
      csh(cmd)

      ;;remove module from menu
      _IMFremovePDMenuItem(moduleDesc)

      return(t)
      )
   )


procedure(_IMFgetVALESliders(ValeConfFile) 
   
   prog( (lines nlines matchLines sliders inPort line slider)
      sliders = list()     
      lines = list()
      matchLines = list()

      inPort = infile(ValeConfFile)
      while(gets(line inPort)
	 lines=append(lines list(line))
	 )
      close(inPort)
      ;; get rid of comments
      rexCompile(";.*")
      nlines = mapcar( lambda( (x) rexReplace(x "" 0) ) lines)

      matchLines = rexMatchList("_IMFdat->compMod[0-9]+->slider" nlines)

      foreach(match matchLines
	 slider = nth(1 parseString(car(last(parseString(match "="))) "\""))
	 unless(lindex(sliders slider) 
	    sliders = cons(slider sliders)
	    )
	 )
      return(sliders)      
   )
)


procedure(_IMFSliderCB(myField myScope value)
   let((myPopup newSliderField)   
      when(value == "Create New Vale Slider ..."
	 ;; need a popup to get new Slider name	 

	 newSliderField = hiCreateStringField(
	    ?name  'sliderPopupNameField
	    ?prompt "New Slider Name:"
	    ?defValue ""
	    ?editable t
	    ?callback 
	    "_IMFsetSliderValueCB(newSliderField hiGetCurrentForm() myField)"	    
	    )	 

	 myPopup = hiCreateAppForm(
	    ?name 'newSliderPopup
	    ?formTitle "Enter New Slider Name"
	    ?fields list( newSliderField )
	    ?unmapAfterCB t
	    )	    
	 hiDisplayForm(myPopup)
	 )
      )
   )

procedure(_IMFsetSliderValueCB(myField myScope parentField)
   let((values)
      values = parentField->choices
      values = append(list(myField->value) values)
      parentField->choices = values
      parentField->value = myField->value
      )
   )	 


unless(isCallable('VALEgetConfigFile)
;; public VALE utility
   procedure(VALEgetConfigFile(@optional (debug nil))
      prog((conf1 conf2 confToUse)

	 conf1 = getShellEnvVar("CDS_MVS_IMF_CM")
	 conf2 = getShellEnvVar("CDS_MVS_IMF_CM2")
	 confToUse = getShellEnvVar("CDS_MVS_IMF_CONFIG")
	 when(and(confToUse isFileName(confToUse))
	    return(confToUse)
	    )
	 when(and(conf1 isDir(conf1))
	    return(strcat(conf1 "/IMFdefaults.il"))
	    )
	 when(and(conf2 isDir(conf2))       
	    return(strcat(conf2 "/IMFdefaults.il"))
	    )
	 printf("VALE ERROR:\
	    CDS_MVS_IMF_CONFIG, CDS_MVS_IMF_CM,\
 and CDS_MVS_IMF_CM2 not properly defined\n")
	 return(nil)      
	 )      
      )
   )

unless(isCallable('VALEgetConfigDirs)
   procedure(VALEgetConfigDirs(@optional (debug nil))
      prog((conf1 conf2 listOfDirs)

	 conf1 = getShellEnvVar("CDS_MVS_IMF_CM")
	 conf2 = getShellEnvVar("CDS_MVS_IMF_CM2")
	 listOfDirs = list()
	    
	 when(and(conf1 isDir(conf1))
	    listOfDirs = append(listOfDirs list(conf1))
	    )
	 when(and(conf2 isDir(conf2))       
	    listOfDirs = append(listOfDirs list(conf2))
	    )
	 return(listOfDirs)      
	 )      
      )
   )
