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
   190913 JF Created for Row-based Termination (Boundary Fill) 

*/

procedure(IMFcompMod216(
             rtDpl
          @optional 
             (debug nil)
          )
   prog((cv erv selectedRules msg) 

      printf("VALE INFO: Creating %L as %L %L ...\n" rtDpl->name 
         rtDpl->outputStyle rtDpl->outputLocation) 

      cv = geGetWindowCellView()
      unless(cv
         printf("VALE ERROR: Unable to find an active layout window. ")
         printf("Please locate or open a layout window and try again.\n")
         return()
      )

      ;; Call LPA for Tap Insertion
      erv = errset(_IMFrunLPA1(rtDpl debug))
      if(erv then
         when(erv == list(nil)
            printf("VALE ERROR: Failed to run LPA for %s\n" rtDpl->name)
            _IMFcmReturn(cv rtDpl "reset" debug)
            return()
         )
      else
         printf("VALE ERROR: A problem occurred running LPA:\n%s\n" 
            errset.errset)
         _IMFcmReturn(cv rtDpl "reset" debug)
         return()
      )

      ;; Wait for LPA to complete
      sprintf(msg "   Please wait for the %s process to finish in the CIW "
         rtDpl->name)
      sprintf(msg "%sbefore leaving\n   the current window.\n" msg)
      VALEshowDialog1(rtDpl "OK" msg debug)

      ;; Flow continues in the post proc of _IMFrunLPA1

      return(t)
   )
)


