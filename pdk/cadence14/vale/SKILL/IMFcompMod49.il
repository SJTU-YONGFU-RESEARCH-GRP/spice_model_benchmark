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
   190311 JF Initial Coding for the Boundary Cell Wrapper

*/


procedure(IMFcompMod49(rtDpl debug)
   prog((cv prB prBox wrapSpec wrapperData erv displayList layer
         purpose wrapIncl)

      printf("VALE INFO: Creating %L as %L %L ...\n" rtDpl->name
         rtDpl->outputStyle rtDpl->outputLocation)

      cv = geGetWindowCellView()
      unless(cv
         printf("VALE ERROR: Unable to find an active layout window. ")
         printf("Please locate or open a layout window and try again.\n")
         return()
      )
      layer = purpose = "none"

      ;; Get the wrapper specification file
      wrapIncl = _IMFgetIncludeFile(cv rtDpl ".il" debug)
      wrapSpec = buildString(hiGetExistingFile(?defaultValue wrapIncl) "/")
      if(isFile(wrapSpec) then
         printf("VALE INFO: Loading Cell Wrapper file: %s\n" wrapSpec)
         load(wrapSpec)
         ;; The variable wrapperData comes from the load of the wrapSpec
         rtDpl->wrapperData = wrapperData
      else
         printf("VALE ERROR: %s is not readable or does not " wrapSpec)
         printf("exist. Please check the file and re-run.\n")
         _IMFcmReturn(cv rtDpl "reset" debug)
      )

      if(length(wrapperData) == 1 then
         ;; Get bBox
         prB = rtDpl->topCv~>prBoundary
         if(prB then
            prBox = prB~>bBox
         else
            ;; variable useBoundaryLayerIfNoPRBoundary comes from the load of
            ;; the wrapSpec
            if(useBoundaryLayerIfNoPRBoundary then
               layer = car(parseString(useBoundaryLayerIfNoPRBoundary))
               purpose = cadr(parseString(useBoundaryLayerIfNoPRBoundary))
               prB = car(setof(shape cv~>shapes shape~>layerName == layer &&
                  shape~>purpose == purpose))
              if(prB then
                  prBox = prB~>bBox
               else
                  printf("VALE ERROR: There was no prBoundary in the current ")
                  printf("design, or a shape on %s %s " layer purpose)
                  printf("please create one of these and re-run\n")
                  _IMFcmReturn(cv rtDpl "reset" debug)
               )
            else
               printf("VALE ERROR: Please add a prBoundary to the current ")
               printf("design with Create->P&R Objects->P&R Boundary, or ")
               printf("add a \"useBoundaryLayerIfNoPRBoundary\" definition ")
               printf("and re-run\n")
               _IMFcmReturn(cv rtDpl "reset" debug)
            )
         )
         ;; Place instances
         when(debug
            printf("VALE DEBUG: Running wrapper cell placement on %L\n"
               rtDpl->targetCv)
         )
         erv = errset(
            ;; Modgen feature test
            ;_IMFwrapCellWithCellsMG(rtDpl->targetCv prBox wrapperData debug)

            ;; Basic instance wrap 
            _IMFwrapCellWithCells(rtDpl->targetCv prBox wrapperData debug layer
               purpose rtDpl->name)
         )
         if(erv then
            if(erv == list(nil) then
               printf("VALE ERROR: Failed to run wrapper cell placement\n")
               return()
            )
            ;; pass thru
         else
            printf("VALE ERROR: A problem occurred during wrapper cell ")
            printf("placement. %L\n" errset.errset)
            return()
         )

         ;; Save and open cellview if checkcell or overlay
         when(rtDpl->outputLocation == "CheckCell" || 
              rtDpl->outputLocation == "Overlay"
            dbSave(rtDpl->targetCv)
            geOpen(?lib rtDpl->targetCv~>libName
                   ?cell rtDpl->targetCv~>cellName
                   ?view rtDpl->targetCv~>viewName
            )
         )
      else
         displayList = nil
         foreach(style wrapperData
            displayList = cons(
               sprintf(nil "%s: %s" style->style style->description)
               displayList
            )
         )
         when(displayList == list(nil)
            printf("VALE ERROR: Failed to read the cell wrapper ")
            printf("specification.\n")
            _IMFcmReturn(cv rtDpl "reset" debug)
         )
         hiShowListBox(
            ?name 'valeSelectCellWrapStyle
            ?choices displayList
            ?callback '_IMFwrapDesign
            ?title "VALE Wrapper Style Selection"
            ?multipleSelect nil
            ?appData "compMod49"
         )
      )

      return(t)
   )
)

