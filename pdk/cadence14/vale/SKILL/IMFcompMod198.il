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
   2019-04-29 VA Initial Coding to remove inactive Gate WSSPs
*/

procedure(IMFcompMod198(
        rtDpl
     @optional 
        (debug nil)
     )
   prog((cv polyLayer allWSPs activeWSPs)
      printf("VALE INFO: Running %s\n" rtDpl->name)

      cv = rtDpl->topCv 

      polyLayer = _IMFdat->polyLayer
      unless(polyLayer
         polyLayer = "Poly"
      )

      activeWSPs = wspWSSPDefGetEnabledOverrides(cv)
      foreach(reg wspRegionFindByLayer(cv polyLayer)
         unless(member(wspRegionGetWSSPDef(reg) activeWSPs)
            activeWSPs = cons(wspRegionGetWSSPDef(reg) activeWSPs)
         )
      )

      allWSPs = wspWSSPDefFind(cv polyLayer)

      foreach(wssp allWSPs
         unless(member(wssp activeWSPs)
            dbDeleteWidthSpacingSnapPatternDef(wssp)
         )
      )
      
      printf("VALE INFO: %s complete.\n" rtDpl->name)
      return(t)
   )
)

