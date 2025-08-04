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
   2019-04-08 JF Initial Coding for opening Placement Planning

*/

procedure(IMFcompMod190(
             rtDpl
          @optional 
             (debug nil)
          )
   prog((toAppTier win rSpecs winTitle toAppStr)
      ;; appType
      printf("VALE INFO: Running %s\n" rtDpl->name)

      if(rexMatchp("ICADV12" getVersion(t)) then
         toAppTier = "VLS-EAD"
         toAppStr = "EAD"
      else
         toAppTier = "VLS-EXL"
         toAppStr = "EXL"
      ) 

      win = hiGetCurrentWindow()
      unless(win
         printf("VALE ERROR: Unable to find an active layout window. ")
         printf("Please locate or open a layout window and try again.\n")
         return()
      )

      ;; This incorrectly reports Virtuoso-XL for ICADV12.3 when it is in EAD
      ;appType = hiGetAppType(win)
      ;printf("VALE INFO: Current Virtuoso application tier is %L\n" appType)
      ;when(appType != toAppTier 
      ;   deInstallApp(win toAppTier) 
      ;   printf("VALE INFO: Launching %s for Row Region creation.\n" toAppTier) 
      ;) 

      ;; Alternate
      winTitle = hiGetWindowName(win)
      
      when(!rexMatchp(toAppStr winTitle)
         deInstallApp(win toAppTier) 
         printf("VALE INFO: Launching %s for Row Region creation.\n" toAppTier) 
      ) 

      ;; Add Component Module code here
      lxEditPlacementStyle()

      rSpecs = dbGetCellViewRowRegionSpecs(geGetWindowCellView())
      unless(rSpecs
         printf("VALE WARNING: No Row Templates exist in the current cellview")
         printf(", please define one interactively, or use the \"Load Row ")
         printf("Templates\" Component Module on the VALE Framework menu.\n")
      )

      return(t) 

   )
)

