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


procedure(IMFcompMod3(
             rtDpl
          @optional
             (debug nil)
          )
   prog((win)
      when(debug
         printf("VALE DEBUG: Running %L\n" rtDpl->description)
      )
      win = hiGetCurrentWindow()
      win->stopLevel = dbGetMaxHierDepth()-1
      hiZoomAbsoluteScale(win 0.9)
      pteEditLayerSetValidity()
      pteSetAllValidity(?panel "Layers")
      pteSetAllSelectable(?panel "Layers")
      pteCloseLayerSetEdition()
      pteShowUsedLPP(t)
      pteSetVisible("Grids" nil "Grids")
      pteSetVisible("Boundaries" nil "Objects")
      ;pteSetActiveLpp(rtDpl->startingLayer)
      pteSetNoneVisible(?panel "Layers")

      return(t)
   )
)
