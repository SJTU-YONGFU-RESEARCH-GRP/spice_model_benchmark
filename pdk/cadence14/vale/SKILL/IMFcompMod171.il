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


procedure(IMFcompMod171(
             rtDpl
          @optional 
             (debug nil)
          )
   prog((cv mapFile fh tf dbuOld name bBox x1 y1 x2 y2 orient)
      printf("VALE INFO: Running Component Module %s\n" rtDpl->name)

      cv = geGetWindowCellView()
      unless(cv
         printf("VALE ERROR: Unable to find an active layout window. ")
         printf("Please locate or open a layout window and try again.\n")
         return()
      )

      unless(isDir("./VALE_RUNDIR")
         createDirHier("./VALE_RUNDIR")
      )
      mapFile = strcat("./VALE_RUNDIR/placementMap.il")

      ;; placementMapList = list(
      ;;    list(name bBox orient)
      ;;    list(name bBox orient)
      ;; )

      fh = outfile(mapFile "w")

      tf = techGetTechFile(cv~>lib)
      dbuOld = techGetDBUPerUU(tf "maskLayout")

      fprintf(fh "dbuOld = %L\n" dbuOld)
      fprintf(fh "placementMapList = list(\n")

      foreach(inst cv~>instances
         name = inst~>name
         bBox = inst~>bBox
         x1 = caar(bBox)
         y1 = cadar(bBox)
         x2 = caadr(bBox)
         y2 = cadadr(bBox) 
         orient = inst~>orient
         fprintf(fh "   list(%L list(%L:%L %L:%L) %L)\n" name x1 y1 x2 y2
            orient)
      )

      fprintf(fh ")\n")
      close(fh)

      printf("VALE INFO: %s Complete.\n" rtDpl->name)
      return(t)
   )
)

