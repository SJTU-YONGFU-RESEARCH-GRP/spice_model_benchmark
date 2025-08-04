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


procedure(IMFcompMod172(
             rtDpl
          @optional 
             (debug nil)
          )
   prog((cv mapFile erv placementMapList name bBoxCurrent mag inst bBoxTarget
         x1o y1o x1n y1n xDelta yDelta orient tf dbuOld dbuNew)
      printf("VALE INFO: Running Component Module %s\n" rtDpl->name)

      cv = geGetWindowCellView()
      unless(cv
         printf("VALE ERROR: Unable to find an active layout window. ")
         printf("Please locate or open a layout window and try again.\n")
         return()
      )

      mapFile = strcat("./VALE_RUNDIR/placementMap.il")
      unless(isFile(mapFile)
         printf("VALE ERROR: Failed to find an existing, readable map file ")
         printf("%s. Please verify \"Save placement placement to " mapFile)
         printf("file\" has been run successfully first, and then re-run.\n")
         return()
      )

      erv = errset(load(mapFile))
      if(erv then
         if(erv == list(nil) then
            printf("VALE ERROR: Failed to load the placement map from ")
            printf("%s, please check the file an re-run.\n" mapFile)
            return()
         )
         ;; pass thru
         ;; dbuOld = NUMBER
         ;; placementMapList = list(
         ;;    list(name bBox orient)
         ;;    list(name bBox orient)
         ;; )
      else
         printf("VALE ERROR: A problem occurred while loading the placement ")
         printf("map from %s, please check the file and re-run.\n%L\n"
            mapFile errset.errset)
         return()
      )

      tf = techGetTechFile(cv~>lib)
      dbuNew = techGetDBUPerUU(tf "maskLayout")
      mag = dbuNew/dbuOld
      when(debug
         printf("VALE DEBUG: Magnification is %L\n" mag)
      )

      foreach(line placementMapList 
         name = car(line)
         bBoxTarget = nth(1 line)
         orient = nth(2 line) 
         ;xDelta = yDelta = 0.0
         
         inst = dbFindAnyInstByName(cv name)
         if(inst then
            bBoxCurrent = inst~>bBox
            x1o = caar(bBoxCurrent)
            y1o = cadar(bBoxCurrent)
            x1n = caar(bBoxTarget) * mag
            y1n = cadar(bBoxTarget) * mag
            xDelta = x1n - x1o
            if(abs(xDelta) < 0.0001 then
               xDelta = 0.0
            )
            yDelta = y1n - y1o
            if(abs(yDelta) < 0.0001 then
               yDelta = 0.0
            )
            when(debug
               printf("VALE DEBUG: Instance %s at %L, %L, needs to move to "
                  name x1o y1o)
               printf("%L, %L\n" x1n y1n)
               printf("VALE DEBUG:    xDelta is %L, yDelta is %L\n"
                  xDelta yDelta)
            )
            dbMoveFig(inst cv list(list(xDelta yDelta) "R0"))
            unless(orient == "R0"
               inst~>orient = orient
            )
         else
            printf("VALE WARNING: No instance found in the current cellview ")
            printf("with the name %s...continuing\n" name)
         )
      )

      hiZoomAbsoluteScale(hiGetCurrentWindow() 0.9)

      printf("VALE INFO: %s Complete.\n" rtDpl->name)
      return(t)
   )
)

