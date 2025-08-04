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
   190529 JF Initial Coding for Finish Device Row 
   190902 JF Renamed to Row-based Fill
   190912 JF New handling for removing xRowLpp marker layers 
   2020-05-05 JF Changed PV call to _IMFrunPV() helper function

*/

procedure(IMFcompMod202(
             rtDpl
          @optional 
             (debug nil)
          )
   prog((cv erv selectedRules vll) 

      printf("VALE INFO: Creating %L as %L %L ...\n" rtDpl->name 
         rtDpl->outputStyle rtDpl->outputLocation) 

      cv = geGetWindowCellView()
      unless(cv
         printf("VALE ERROR: Unable to find an active layout window. ")
         printf("Please locate or open a layout window and try again.\n")
         return()
      )

      ;; Create Device Type Markers
      VALEdeviceTypeMarker(cv "create" "model" "_n1hvt"
         list(list("Nhvt" "drawing")))
      VALEdeviceTypeMarker(cv "create" "model" "_p1hvt"
         list(list("Phvt" "drawing")))
      VALEdeviceTypeMarker(cv "create" "model" "_n1svt"
         list(list("Nsvt" "drawing")))
      VALEdeviceTypeMarker(cv "create" "model" "_p1svt"
         list(list("Psvt" "drawing")))
      VALEdeviceTypeMarker(cv "create" "model" "_n1lvt"
         list(list("Nlvt" "drawing")))
      VALEdeviceTypeMarker(cv "create" "model" "_p1lvt"
         list(list("Plvt" "drawing")))
      VALEdeviceTypeMarker(cv "create" "model" "_n2hvt"
         list(list("Nhvt" "drawing") list("ThickOx" "drawing")))
      VALEdeviceTypeMarker(cv "create" "model" "_p2hvt"
         list(list("Phvt" "drawing") list("ThickOx" "drawing")))
      VALEdeviceTypeMarker(cv "create" "model" "_n2svt"
         list(list("Nsvt" "drawing") list("ThickOx" "drawing")))
      VALEdeviceTypeMarker(cv "create" "model" "_p2svt"
         list(list("Psvt" "drawing") list("ThickOx" "drawing")))
      VALEdeviceTypeMarker(cv "create" "model" "_n2lvt"
         list(list("Nlvt" "drawing") list("ThickOx" "drawing")))
      VALEdeviceTypeMarker(cv "create" "model" "_p2lvt"
         list(list("Plvt" "drawing") list("ThickOx" "drawing")))

      ;; Environment Variables specific to this Component Module

      ;; Preprocess the Poly WSP Regions, with Row Region and prBoundary
      ;; auto update
      unless(rtDpl->skipAutoRegionResize
         erv = errset(_IMFputRegionOnGrid(cv nil list("Poly" "track")
               rtDpl->resizeRowAndPRB debug))
         unless(erv
            printf("VALE ERROR: Failed to resize the region for %s\n"
               rtDpl->name)
            _IMFcmReturn(cv rtDpl "reset" debug)
            return()
         )
      )

      ;; Start core Component Module function
      if(rtDpl->showAllMarkers then
         selectedRules = list(
            "gen-NWell-RBF--drawing"
            "gen-Poly-RBF--drawing"
            "gen-Poly-RBF--edge"
            "gen-Poly-RBF--dummy"
            "gen-Nhvt-RBF--drawing"
            "gen-Phvt-RBF--drawing"
            "gen-Nsvt-RBF--drawing"
            "gen-Psvt-RBF--drawing"
            "gen-Nlvt-RBF--drawing"
            "gen-Plvt-RBF--drawing"
            "gen-CutPoly-RBF--drawing"
            "gen-LiAct-RBF--drawing"
         )
      else
         selectedRules = list(
            "gen-NWell-RBF--drawing"
            "gen-Poly-RBF--drawing"
            "gen-Poly-RBF--edge"
            "gen-Poly-RBF--dummy"
            "gen-Nhvt-RBF--drawing"
            "gen-Phvt-RBF--drawing"
            "gen-Nsvt-RBF--drawing"
            "gen-Psvt-RBF--drawing"
            "gen-Nlvt-RBF--drawing"
            "gen-Plvt-RBF--drawing"
            "gen-CutPoly-RBF--drawing"
            "gen-LiAct-RBF--drawing"
         )
      )

      ;; Preprocess
      erv = errset(_IMFmapRowsToLayers(cv rtDpl->name))
      unless(erv
         printf("VALE ERROR: Failed to run preprocessing for %s\n"
            rtDpl->name)
         _IMFcmReturn(cv rtDpl "reset" debug)
         return()
      )

      ;; Call PVS or Pegasus
      erv = errset(_IMFrunPV(rtDpl cv selectedRules debug))
      if(erv then
         when(erv == list(nil)
            printf("VALE ERROR: Failed to run PV.\n")
            _IMFcmReturn(cv rtDpl "reset" debug)
            return()
         )
      else
         printf("VALE ERROR: A problem occurred running PV:\n%s\n" 
            errset.errset)
         _IMFcmReturn(cv rtDpl "reset" debug)
         return()
      )

      ;; Clear environment variables for this compMod

      ;; Clear Device Type Markers
      VALEdeviceTypeMarker(cv "remove")

      ;; Remove any temporary row layers from VALEmapRowsToLayers or other
      ;; compMods
      when(_IMFdat->pRowLpp
         vll = cons(_IMFdat->pRowLpp vll)
      )
      when(_IMFdat->nRowLpp
         vll = cons(_IMFdat->nRowLpp vll)
      )
      when(_IMFdat->instRowLpp
         vll = cons(_IMFdat->instRowLpp vll)
      )
      when(_IMFdat->dummyRowLpp
         vll = cons(_IMFdat->dummyRowLpp vll)
      )
      when(_IMFdat->tapRowLpp
         vll = cons(_IMFdat->tapRowLpp vll)
      ) 
      foreach(rs setof(shp cv~>shapes 
                    exists(lyr vll car(lyr) == shp~>layerName) && 
                    exists(pur vll cadr(pur) == shp~>purpose))
         dbDeleteObject(rs)
      )


      printf("VALE INFO: %s complete.\n" rtDpl->name)
      return(t)
   )
)


