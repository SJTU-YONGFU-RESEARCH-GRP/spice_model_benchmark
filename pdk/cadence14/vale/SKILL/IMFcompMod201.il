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
   2019-09-12 JF Initial Coding for the Create Tap Row Component Module

*/

procedure(IMFcompMod201(
             rtDpl
          @optional 
             (debug nil)
          )
   prog((bBox rowBox shape)
      printf("VALE INFO: Running %s\n" rtDpl->name)

      ;; Get the row template bounding box around a user selected point
      erv = errset(_IMFgetRowTemplateBox(rtDpl->topCv "tap" debug))
      if(erv then
         if(erv == list(nil) then
            printf("VALE WARNING: No row was found at the current point, ")
            printf("please check that a row region exists and try again.\n")
            return()
         else
            bBox = car(erv)
         )
      else
         printf("VALE ERROR: A problem occurred while querying for the row ")
         printf("in the current cellview.  %L\n" errset.errset)
         return()
      )

      ;; Create a marker layer
      ;; No need to tag with a property because the Row-based Fill compMod
      ;; will clear all the _IMFdat->xRowLpp layers
      rowBox = list(list(car(lowerLeft(bBox)) cadr(lowerLeft(bBox))+0.001)
                    list(car(upperRight(bBox)) cadr(upperRight(bBox))-0.001))
      shape = dbCreateRect(rtDpl->topCv _IMFdat->tapRowLpp rowBox)
      unless(shape
         printf("VALE ERROR: A problem occurred creating a Tap Row Marker ")
         printf("shape.\n")
         return()
      )

      printf("VALE INFO: %s complete\n" rtDpl->name)
      return(t) 

   )
)

