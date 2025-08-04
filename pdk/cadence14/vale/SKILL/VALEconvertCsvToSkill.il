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


;; VALEconvertCsvToSkill takes a CSV file saved from a spreadsheet, with a 
;; specific format, and converts it to a SKILL data structure that the
;; Schematic Migration Component Module can use.
;;
;; Revision log:
;; 190906 JF Removed check for cc_ or gf_,
;;           using _IMFdat->compMod88->IMF_MIG_REF_PAR_PREFIX
;; 190911 JF Enhanced VALEschTrDpl->libMap to enable more migration libraries
;;           at the same time, where the first set is still the primary
;;           source and target tech
;; 200211 JF Added a custom orientation map file
;; 200330 JF Improve handling of parameter reference prefix 

procedure(VALEconvertCsvToSkill(file ofile verbose)
   prog((fh ofh line lineNumber lineList skip deviceFlag wrappedFlag dMap
         prevLine previousFlag col0 knownKeywords erv pStr pVal printHeaderFlag)
         
      fh = infile(file)
      ofh = outfile(ofile "w")
      unless(fh
         printf("VALE ERROR: Failed to open file %L.\n" file)
         return()
      )
      unless(ofh
         printf("VALE ERROR: Failed to open file for writing %L.\n" ofile)
         return()
      )

      knownKeywords = list("Keyword" 
                           "device" 
                           "match parameter"
                           "display parameter")
      lineNumber = 0
      deviceFlag = nil
      wrappedFlag = nil
      printHeaderFlag = t
      prevLine = ""
      dMap = list(nil 'spl list(nil) 'tpl list(nil) 'comment "" 'showSp nil)

      ;; Process each line
      while(gets(line fh)
         lineNumber++

         previousFlag = nil
         skip = nil

         when(verbose
            printf("\nSTART NEWLINE:\n--> line %d: %s\n" lineNumber line)
            printf("--> previous line %d: %s\n" lineNumber-1 prevLine)
         )
         
         ;; 1. Empty Line 
         when(rexMatchp("^,,,,,,,,," line)
            skip = t
            when(wrappedFlag
               ;; Previous line complete, fetch comment
               erv = errset(VALEgatherCommentLines(prevLine verbose))
               if(erv then
                  if(erv == list(nil) then
                     printf("VALE ERROR: Failed to process comments on line ")
                     printf("%L\n" prevLine)
                     dMap->comment = "Failed to collect comments, see CSV.\n"
                  else
                     dMap->comment = car(erv)
                  )
               else
                  printf("VALE ERROR: A problem occurred while processing ")
                  printf("comments on line %L\n%L\n" prevLine errset.errset)
                  dMap->comment = "Failed to collect comments, see CSV.\n"
               )
               wrappedFlag = nil
            )
            prevLine = ""
         )

         unless(skip
            lineList = parseString(line "," t)
            col0 = car(lineList)
            
            if(member(col0 knownKeywords) then
               when(verbose 
                  printf("VALE MSG: Section 1: known keyword %s\n" col0)
               )

               ;; 2. DEVICE LINE
               when(col0 == "device"

                  ;; Print header once
                  when(lineNumber < 4 && printHeaderFlag == t
                     printHeaderFlag = nil
                     ;; Print Header
                     erv = errset(
                        ;VALEprintSchMigMapHeader(ofh nth(1 lineList))
                        VALEprintSchMigMapHeader(ofh)
                     )
                     if(erv then
                        if(erv == list(nil) then
                           return()
                        )
                     else
                        return()
                     ) 
                  )

                  when(verbose printf("VALE MSG: Section 2: device line\n"))
                  ;; First take care of a previous wrapped line
                  when(wrappedFlag
                     when(verbose printf("VALE MSG: Section 2: wrapped\n"))

                     ;; Previous line complete, fetch comment
                     erv = errset(
                        VALEgatherCommentLines(prevLine verbose))
                     if(erv then
                        if(erv == list(nil) then
                           printf("VALE ERROR: Failed to process comments on ")
                           printf("line %L\n" prevLine)
                           dMap->comment = 
                              "Failed to collect comments, see CSV.\n"
                        else
                           dMap->comment = car(erv)
                        )
                     else
                        printf("VALE ERROR: A problem occurred while ")
                        printf("processing comments on line %L\n%L\n" 
                           prevLine errset.errset)
                        dMap->comment = 
                           "Failed to collect comments, see CSV.\n"
                     )
                     wrappedFlag = nil
                  )

                  ;; Next print the previous device map
                  when(deviceFlag
                     when(verbose 
                        printf("VALE MSG: *** OUTPUTTING DEVICE ***\n")
                     )
                     ;; Output Device Data 
                     erv = errset(
                        VALEprintSchMigMapItem(ofh dMap verbose)
                     )
                     unless(erv
                        printf("VALE ERROR: A problem occurred while ")
                        printf("translating the CSV to SKILL for ")
                        printf("device %L\n%L\n" dMap->sCellName errset.errset)
                     )

                     ;; reset map var
                     dMap = list(nil 'spl list(nil) 'tpl list(nil) 'comment ""
                        'showSp nil)
                  )

                  ;; Gathering the info of the next device
                  deviceFlag = t
                  dMap->sLibName = nth(1 lineList)
                  dMap->sCellName = nth(2 lineList)
                  dMap->tLibName = nth(5 lineList)
                  dMap->tCellName = nth(6 lineList)

                  ;; Add libs to VALEschTrDpl->libMap list
                  unless(
                     exists(lm VALEschTrDpl->libMap car(lm) == dMap->sLibName &&
                        cadr(lm) == dMap->tLibName)
                     ;; if the sLibName is not in libMap, then add it
                     VALEschTrDpl->libMap = cons(
                        list(dMap->sLibName dMap->tLibName)
                        VALEschTrDpl->libMap)
                  )
               )
               
               ;; 3. MATCH PARAMETER
               when(col0 == "match parameter" && deviceFlag
                  when(verbose 
                     printf("VALE MSG: Section 3: match parameter\n")
                  )

                  ;; Previous line comments complete, fetch comment
                  when(wrappedFlag
                     erv = errset(
                        VALEgatherCommentLines(prevLine verbose))
                     if(erv then
                        if(erv == list(nil) then
                           printf("VALE ERROR: Failed to process comments on ")
                           printf("line %L\n" prevLine)
                           dMap->comment = 
                              "Failed to collect comments, see CSV.\n"
                        else
                           dMap->comment = car(erv)
                        )
                     else
                        printf("VALE ERROR: A problem occurred while ")
                        printf("processing comments on line %L\n%L\n" 
                           prevLine errset.errset)
                        dMap->comment = 
                           "Failed to collect comments, see CSV.\n"
                     )
                     wrappedFlag = nil
                  )

                  ;; A source match parameter
                  ;; If the match parameter line has source parameters
                  if(nth(1 lineList) != "" && nth(1 lineList) then
                     pStr = strcat("dMap->spl->" nth(1 lineList))
                     if(rexMatchp("|" nth(3 lineList)) then
                        ;; This is a conditional match
                        erv = errset(evalstring(
                           strcat(pStr " = \"" nth(3 lineList) "\"")
                        ))
                        unless(erv
                           printf("VALE ERROR: A problem occurred parsing ")
                           printf("the CSV file for source parameter %L\n%L\n"
                              nth(1 lineList) errset.errset)
                        )
                     else
                        ;; This is an exact match
                        pVal = evalstring(pStr)
                        if(pVal && pVal != nth(3 lineList) then
                           ;; Parameter already exists, skip
                           printf("VALE WARNING: Found duplicate parameter ")
                           printf("on line %d, for " lineNumber)
                           printf("%s --> %s." dMap->sCellName dMap->tCellName)
                           printf("Please correct the mapping file.\n")
                        else
                           ;; Parameter does not exist yet in the DPL
                           erv = errset(evalstring(
                              strcat(pStr " = \"" nth(3 lineList) "\"")
                           ))
                           unless(erv
                              printf("VALE ERROR: A problem occurred parsing ")
                              printf("the CSV file for source parameter %L\n%L\n"
                                 nth(1 lineList) errset.errset)
                           )
                        )
                     )

                     ;; Add parameter name to showSp list
                     when(nth(4 lineList) == "parameter&value"
                        dMap->showSp = 
                           cons(list(nth(1 lineList) nth(3 lineList)) 
                              dMap->showSp)
                     )

                     ;; A target match parameter
                     ;; If the match parameter line also has target parameters
                     if(nth(5 lineList) != "" && nth(5 lineList) then
                        pStr = strcat("dMap->tpl->" nth(5 lineList))
                        pVal = evalstring(pStr)
                        if(pVal && pVal != nth(7 lineList) then
                           ;; Parameter already exists, append value 
                           ;; This is for the situation of a conditional calc
                           ;; line with multiple options 
                           erv = errset(evalstring(
                              strcat(pStr " = \"" pVal "|" nth(7 lineList) "\"")
                           ))
                           unless(erv
                              printf("VALE ERROR: A problem occurred parsing ")
                              printf("the CSV file for target parameter %L, "
                                 nth(5 lineList))
                              printf("line number %d\n" lineNumber)
                              printf("%L\n" errset.errset)
                           )
                        else
                           ;; Parameter does not exist yet in the DPL
                           erv = errset(evalstring(
                              strcat(pStr " = \"" nth(7 lineList) "\"")
                           ))
                           unless(erv
                              printf("VALE ERROR: A problem occurred parsing ")
                              printf("the CSV file for target parameter %L %L, "
                                 nth(5 lineList) nth(7 lineList))
                              printf("line number %d\n" lineNumber)
                              printf("%L\n" errset.errset)
                           )
                        )
                     )
                  else
                     ;; If the match parameter line has only target parameters
                     if(nth(5 lineList) != "" && nth(5 lineList) then
                        pStr = strcat("dMap->tpl->" nth(5 lineList))
                        pVal = evalstring(pStr)
                        if(pVal && pVal != nth(7 lineList) then
                           ;; Parameter already exists, append value
                           ;; This is for the situation of a conditional calc
                           ;; line with multiple options 
                           erv = errset(evalstring(
                              strcat(pStr " = \"" pVal "|" nth(7 lineList) "\"")
                           ))
                           unless(erv
                              printf("VALE ERROR: A problem occurred parsing ")
                              printf("the CSV file for target parameter %L, "
                                 nth(5 lineList))
                              printf("line number %d\n" lineNumber)
                              printf("%L\n" errset.errset)
                           )
                        else
                           ;; Parameter does not exist yet in the DPL
                           erv = errset(evalstring(
                              strcat(pStr " = \"" nth(7 lineList) "\"")
                           ))
                           unless(erv
                              printf("VALE ERROR: A problem occurred parsing ")
                              printf("the CSV file for target parameter %L %L\n"
                                 nth(5 lineList) nth(7 lineList))
                              printf("%L\n" errset.errset)
                           )
                        ) 
                     )
                  )
               )

               ;; 4. DISPLAY PARAMETER
               when(col0 == "display parameter" && deviceFlag
                  when(verbose 
                     printf("VALE MSG: Section 4: display parameter\n")
                  )

                  when(wrappedFlag
                     ;; Previous line complete, fetch comment
                     erv = errset(
                        VALEgatherCommentLines(prevLine verbose))
                     if(erv then
                        if(erv == list(nil) then
                           printf("VALE ERROR: Failed to process comments on ")
                           printf("line %L\n" prevLine)
                           dMap->comment = 
                              "Failed to collect comments, see CSV.\n"
                        else
                           dMap->comment = car(erv)
                        )
                     else
                        printf("VALE ERROR: A problem occurred while ")
                        printf("processing comments on line %L\n%L\n" 
                           prevLine errset.errset)
                        dMap->comment = 
                           "Failed to collect comments, see CSV.\n"
                     )
                     wrappedFlag = nil
                  )

                  ;; display parameter with source parameters and 
                  ;; show parameter and value if not "none"
                  if(nth(1 lineList) != "" && nth(1 lineList) then
                     if(dMap->tCellName == "none" then
                        ;; Map to none, then display all display parameters
                        dMap->showSp = 
                           cons(list(nth(1 lineList) nth(3 lineList)) 
                              dMap->showSp)
                     else
                        ;; Mapped to new cell, display only parameter&value
                        ;; tagged parameters
                        when(nth(4 lineList) == "parameter&value"
                           dMap->showSp = 
                              cons(list(nth(1 lineList) nth(3 lineList))
                                 dMap->showSp)
                        )
                     )
                  )
               )

            else
               ;; Not a known keyword
               when(verbose printf("VALE MSG: No keyword found, in else \n"))
               if(col0 == "" || col0 == " " || col0 == nil ||
                  col0 == "\n" then
                  
                  when(verbose
                     printf("VALE MSG: Found empty or white space, ignoring ")
                     printf("line %d, %L\n" lineNumber line)
                  )
               else
                  ;; Not whitespace
                  if(rexMatchp("^,,,,,[a-z]" line) then
                     ;; mislabeled, but continuation of match parameters
                     printf("VALE ERROR: Line %d appears to be " lineNumber)
                     printf("missing a keyword. Please add it to the CSV ")
                     printf("file and rerun.\n")
                     return()
                  else
                     ;; Found wrapped line
                     wrappedFlag = t
                     line = buildString(parseString(line ","))
                     previousFlag = t
                     prevLine = strcat(prevLine ". " line)
                     when(verbose
                        printf("VALE MSG: Found wrapped line %d: %L\n" 
                           lineNumber line)
                     )
                  )
               )
            )
         ) ;unless skip

         unless(previousFlag
            prevLine = line
         )
      ) ;while lines in the input file

      when(verbose printf("VALE MSG: *** OUTPUTTING LAST DEVICE ***\n"))

      ;; Print Last Device
      VALEprintSchMigMapItem(ofh dMap verbose)
      fprintf(ofh ")\n")

      ;; Reverse the list to make the original techLibs first
      VALEschTrDpl->libMap = reverse(VALEschTrDpl->libMap)

      VALEprintSchMigMapFooter(ofh VALEschTrDpl->libMap)

      close(fh)
      close(ofh)

      return(t)
   )
)


procedure(VALEprintSchMigMapFooter(ofh libList)
   prog(()
      fprintf(ofh "VALEschTrDpl->libMap = list(\n")
      foreach(item libList
         fprintf(ofh "   list(\"%s\" \"%s\")\n" car(item) cadr(item))
      )
      fprintf(ofh ")\n")
   )
)
      

procedure(VALEprintSchMigMapHeader(ofh)
   prog((ignoreLibsList)
      fprintf(ofh ";; Generated mapping file from CSV for VALE Framework ")
      fprintf(ofh "Schematic Migration tool\n\n")

      ;; Print the ignoreLibList
      fprintf(ofh "VALEschTrDpl->ignoreLibList = list(\n")
      when(_IMFdat->compMod88->envVars->IMF_MIG_IGNORE_LIBS
         ignoreLibsList = parseString(
            _IMFdat->compMod88->envVars->IMF_MIG_IGNORE_LIBS
         )
         fprintf(ofh "   ")
         foreach(lib ignoreLibsList 
            fprintf(ofh "\"%s\" " lib)
         )
         fprintf(ofh "\n)\n")
      )

      ;; Print the reference parameter prefix
      if(_IMFdat->compMod88->envVars->IMF_MIG_REF_PAR_PREFIX then
         fprintf(ofh "VALEschTrDpl->parameterIdentifier = \"%s\"\n\n"
            _IMFdat->compMod88->envVars->IMF_MIG_REF_PAR_PREFIX)
      else
         printf("VALE ERROR: Please set %s in the IMFdefaults.il or other "
             strcat("_IMFdat->compMod88->envVars->IMF_MIG_REF_PAR_PREFIX"))
         printf("custom VALE framework configuration file and re-run.\n")
         return()
      )

      ;; Print the libMap
      if(_IMFdat->compMod88->envVars->IMF_MIG_SOURCE_TECH &&
         _IMFdat->compMod88->envVars->IMF_MIG_TARGET_TECH then
         fprintf(ofh ";; libMap is re-printed, updated, at the end of file\n")
         fprintf(ofh "VALEschTrDpl->libMap = list(\n")
         fprintf(ofh "   list(\"%s\" \"%s\")\n)\n"
            _IMFdat->compMod88->envVars->IMF_MIG_SOURCE_TECH
            _IMFdat->compMod88->envVars->IMF_MIG_TARGET_TECH)
      else
         printf("VALE ERROR: Please set %s and %s in the IMFdefaults.il or "
            strcat("_IMFdat->compMod88->envVars->IMF_MIG_SOURCE_TECH")
            strcat("_IMFdat->compMod88->envVars->IMF_MIG_TARGET_TECH"))
         printf("other custom VALE framework configuration file and ")
         printf("re-run.\n")
         return()
      )

      ;; Import the term Map
      when(_IMFdat->compMod88->envVars->IMF_MIG_TERM_MAP
         if(isFile(_IMFdat->compMod88->envVars->IMF_MIG_TERM_MAP) then
            erv = errset(load(_IMFdat->compMod88->envVars->IMF_MIG_TERM_MAP))
            if(erv then
               if(erv == list(nil) then
                  printf("VALE ERROR: Failed to load the VALEschTrDpl->")
                  printf("termMap file from %s, please check the syntax "
                     _IMFdat->compMod88->envVars->IMF_MIG_TERM_MAP)
                  printf("and location of the file and re-run\n")
                  return()
               else
                  when(verbose
                      printf("VALE MSG: VALEschTrDpl->termMap loaded.\n")
                  )
               )
            else
               printf("VALE ERROR: A problem occurred while loading the ")
               printf("VALEschTrDpl->termMap file from %s, please check the "
                  _IMFdat->compMod88->envVars->IMF_MIG_TERM_MAP)
               printf("syntax and location of the file and re-run\n")
               return()
            )
         else
            printf("VALE ERROR: Failed to find the VALEschTrDpl->termMap ")
            printf("file at %s, please check the location and re-run.\n"
               _IMFdat->compMod88->envVars->IMF_MIG_TERM_MAP)
            return()
         )
      )

      ;; Import the custom orientations Map
      when(_IMFdat->compMod88->envVars->IMF_MIG_ORIENT_MAP
         if(isFile(_IMFdat->compMod88->envVars->IMF_MIG_ORIENT_MAP) then
            erv = errset(load(_IMFdat->compMod88->envVars->IMF_MIG_ORIENT_MAP))
            if(erv then
               if(erv == list(nil) then
                  printf("VALE ERROR: Failed to load the VALEschTrDpl->")
                  printf("orientMap file from %s, please check the syntax "
                     _IMFdat->compMod88->envVars->IMF_MIG_ORIENT_MAP)
                  printf("and location of the file and re-run\n")
                  return()
               else
                  when(verbose
                      printf("VALE MSG: VALEschTrDpl->orientMap loaded.\n")
                  )
               )
            else
               printf("VALE ERROR: A problem occurred while loading the ")
               printf("VALEschTrDpl->orientMap file from %s, please check the "
                  _IMFdat->compMod88->envVars->IMF_MIG_ORIENT_MAP)
               printf("syntax and location of the file and re-run\n")
               return()
            )
         else
            printf("VALE ERROR: Failed to find the VALEschTrDpl->orientMap ")
            printf("file at %s, please check the location and re-run.\n"
               _IMFdat->compMod88->envVars->IMF_MIG_ORIENT_MAP)
            return()
         )
      )

      ;; Start of the Cell Parameter Map section
      fprintf(ofh "VALEschTrDpl->cpm = list(\n")

      return(t)
   )
)

procedure(VALEprintSchMigMapItem(ofh dMap verbose)
   let((pStr pVal splStr tplStr pmpStr pValList pValue pVal2 pValList2
        sCount erv)
      dMap->comment = buildString(parseString(dMap->comment "\n") "\n   ;; ") 
      fprintf(ofh "   ;; Mapping %s --> %s\n" dMap->sCellName dMap->tCellName) 
      fprintf(ofh "   ;; Comments: %s\n" dMap->comment)
      fprintf(ofh "   list(nil\n")
      fprintf(ofh "      'sn %L\n" dMap->sCellName)
      fprintf(ofh "      'sl %L\n" dMap->sLibName)
      fprintf(ofh "      'tn %L\n" dMap->tCellName)
      fprintf(ofh "      'tl %L\n" dMap->tLibName)

      splStr = "      'spl list(nil\n"
      tplStr = "      'tpl list(nil\n"
      pmpStr = "      'pMap list(\n"

      ;; Source Parameter List
      foreach(key dMap->spl->?
         pStr = strcat("dMap->spl->" key) 
         pVal = evalstring(pStr)
         if(listp(pVal) then
            ;; Process each list parameter, build string for pMap
            ;; for dMap->spl, these parameters are no-ops 
            t
         else
            if(rexMatchp("[\\+\\-\\*\\/]" pVal) || rexMatchp("sqrt" pVal) then
               pVal = strcat("eq|" pVal)
               splStr = strcat(splStr "              '" key " \"" 
                  pVal "\"\n") 
            else
               if(rexMatchp(_IMFdat->compMod88->envVars->IMF_MIG_REF_PAR_PREFIX pVal) then
                  ;; for dMap->spl, these parameters are no-ops 
                  t
               else
                  ;; build string for spl
                  splStr = strcat(splStr "              '" key " \"" 
                     pVal "\"\n")
               )
            )
         )
      )
      splStr = strcat(splStr "            )\n")
      fprintf(ofh "%s" splStr)

      ;; Target Parameter List and pMap list
      foreach(key dMap->tpl->?
         pStr = strcat("dMap->tpl->" key) 
         pVal = evalstring(pStr)
         if(listp(pVal) then
            ;; Process each list parameter, build string for pMap
            t
         else
            if(rexMatchp("^calc" pVal) then
               rexCompile("|calc")
               pVal = rexReplace(pVal "#" 0)
               pValList = parseString(pVal "#")
               foreach(item pValList
                  rexCompile(" ")
                  pVal2 = rexReplace(item "" 0)
                  pValList2 = parseString(pVal2 "[]")
                  pValue = ""
                  foreach(val pValList2
                     pValue = strcat(pValue " \"" val "\"")
                  )
                  unless(rexMatchp("calc" pValue)
                     pValue = strcat(" \"calc\"" pValue)
                  )
                  pmpStr = strcat(pmpStr "         list(nil 'par \"" key 
                     "\" 'vmap list(" pValue "))\n")
               )
            else
               if(rexMatchp("[\\+\\-\\*\\/]" pVal) || 
                  rexMatchp("sqrt" pVal) then
                  pVal = strcat("eq|" pVal)
                  ;; Remove any spaces
                  rexCompile(" ")
                  pVal = rexReplace(pVal "" 0)
                  tplStr = strcat(tplStr "              '" key " \"" 
                     pVal "\"\n") 
               else
                  if(rexMatchp(_IMFdat->compMod88->envVars->IMF_MIG_REF_PAR_PREFIX pVal) then
                     ;; Change 200330
                     ;printf("VALE DEBUG: pVal = %L\n" pVal)
                     erv = errset(_IMFgetParStart(pVal))
                     if(erv then
                        if(erv == list(nil) then
                           return()
                        )
                        sCount = car(erv)
                     else
                        return()
                     )
                     pVal = substring(pVal sCount)
                     pmpStr = strcat(pmpStr "         list(nil 'par \"" key 
                        "\" 'vmap list(\"same\" \"" pVal "\"))\n")
                  else
                     ;; build string for tpl
                     tplStr = strcat(tplStr "              '" key " \"" pVal 
                        "\"\n")
                  )
               )
            )
         )
      )
      tplStr = strcat(tplStr "            )\n")
      fprintf(ofh "%s" tplStr)

      pmpStr = strcat(pmpStr "      )\n")
      fprintf(ofh "%s" pmpStr)

      ;; Print show parameters
      fprintf(ofh "      'showSp list(\n")
      foreach(ssp dMap->showSp
         fprintf(ofh "                 list(\"%s\" \"%s\")\n" car(ssp) 
            cadr(ssp))
      )
      fprintf(ofh "      )\n")

      ;; close current map dpl
      fprintf(ofh "   )\n")

      when(verbose
         printf("VALE MSG: Finished printing %L to map file\n"
            dMap->sCellName)
      )
      t
   )
)

procedure(VALEgatherCommentLines(line verbose)
   prog((lineList index max mergedCols col)
      ;printf("VALE MSG: In comments ... %L\n" line)
      lineList = parseString(line "," t)
      index = 8
      max = length(lineList)
      mergedCols = ""
      while(index < max
         col = nth(index lineList)
         ;printf("VALE MSG: col = %L\n" col)
         when(col
            rexCompile("^ ")
            col = rexReplace(col "" 0)
            rexCompile("[ ]+")
            col = rexReplace(col " " 0)
            rexCompile("\"")
            col = rexReplace(col "" 0)
            rexCompile("[ ]+$")
            col = rexReplace(col "" 0)
            rexCompile(" $")
            col = rexReplace(col "" 0)
            rexCompile("\n\\. ")
            col = rexReplace(col "\n" 0)
            ;printf("VALE MSG: col = %L\n" col)
            if(mergedCols == "" then
               mergedCols = strcat(col " ")
            else
               mergedCols = strcat(mergedCols col " ")
            )
         ) 
         index++
      )
      when(verbose && mergedCols
         printf("VALE MSG: Merged text for this line: %L\n" mergedCols)
      )
      if(mergedCols then
         return(mergedCols)
      else
         return()
      )
   )
)


