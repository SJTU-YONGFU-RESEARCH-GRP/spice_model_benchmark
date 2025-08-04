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


procedure(IMFcompMod18(
             rtDpl
          @optional 
             (debug nil)
          )
   prog((hifFile hifFilePath loadrv)
      printf("VALE INFO: Loading hotspots file...\n")

      hifFile = hiDisplayFileDialog(
         ?dialogName 'valeLoadHIF
         ?filter "SKILL (*.hif)" 
         ?caption "Select the hotspot (HIF) file to load"
      )
      unless(hifFile
         printf("VALE INFO: Selection of custom HIF file canceled, exiting.\n")
         return(t)
      )
      if(listp(hifFile) then
         hifFilePath = strcat(car(hifFile) "/" cadr(hifFile))
         loadrv = errset(_dfm_lpa_batch_fixing(hifFilePath))
         unless(loadrv
            printf("VALE INFO: Failed to load the custom HIF file: ")
            printf("%L, please check the selections and " hifFilePath)
            printf("re-run.\n")
            return(t)
         )
         return(t)
      else
         printf("VALE INFO: The HIF file selection dialog returned an ")
         printf("unexpected value: %L, please check the " hifFile)
         printf("selections and re-run.\n")
         return(t)
      )
   )
)
