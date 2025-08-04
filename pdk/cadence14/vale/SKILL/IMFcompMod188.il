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
   2019-04-08 JF Initial Coding for a Optimize PCell Parameters module

*/

procedure(IMFcompMod188(
             rtDpl
          @optional 
             (debug nil)
          )
   prog((cv parList toValue instList cdfgData parId)
      printf("VALE INFO: Running %s\n" rtDpl->name)

      cv = geGetEditCellView()
      unless(cv
         printf("VALE ERROR: Unable to find an active layout window. ")
         printf("Please locate or open a layout window and try again.\n")
         return()
      )

      ;; Remove Left and Right Dummy Poly
      parList = rtDpl->parList1 
      toValue = rtDpl->parValue1 

      instList = setof(i cv~>instances i~>libName == _IMFdat->techLib)
      foreach(inst instList
         cdfgData = cdfGetInstCDF(inst)
         if(cdfgData then
            foreach(par parList
               parId = cdfFindParamByName(cdfgData par)
               if(parId then
                  when(debug
                     printf("VALE DEBUG: Setting %L %L to %L\n" inst~>cellName
                        par toValue)
                  )
                  ;; Set Value
                  parId~>value = toValue
               )
            ) 
         )
      )

      printf("VALE INFO: %s complete.\n" rtDpl->name)
      return(t) 

   )
)

