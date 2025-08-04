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


procedure(VALEfilterOverlapList(cv inputList @optional (debug nil))
   prog((tmpShape object selectedObject tf cg vl transform xT yT oR
         ll ur xlo ylo xhi yhi objList coordUpd )
      selectedObject = nil

      ;; Check for a debug variable
      unless(debug
         debug = getShellEnvVar("VALE_DEBUG_OVERLAPS")
      )   

      ;; Get the valid routing layers from the techfile
      tf = techGetTechFile(cv)
      unless(tf
         printf("VALE ERROR: Failed to get the techfile for the current ")
         printf("cellview.\n")
         return()
      )
      cg = cstFindConstraintGroupIn(tf "virtuosoDefaultExtractorSetup")
      unless(cg
         printf("VALE ERROR: Failed to find the ")
         printf("virtuosoDefaultExtractorSetup contraint group.\n")
         return()
      )
      vl = car(
         setof(constraint 
            cg~>objects constraint~>defName == "validLayers")
      )
      ;vl = mapcar('car setof(lyr vl~>layers listp(lyr)))
      vl = vl~>value
      unless(vl
         printf("VALE ERROR: Failed to get the validLayers for routing\n")
         return()
      )
      when(debug printf("VALE DEBUG: valid layers = %L\n" vl))

      transform = nil
      foreach(olItem inputList
         when(debug
            printf("VALE DEBUG: Line item is %L\n" olItem)
         )
         unless(transform
            objList = nil
            objList = _IMFisTraceCandidate(olItem objList debug)
            when(debug
               printf("VALE DEBUG: Selected object is %L\n" objList)
            )
            when(objList && member(car(objList)~>layerName vl)
               transform = dbGetHierPathTransform(olItem)
               when(debug
                  printf("VALE DEBUG: Selected transform is %L\n" transform)
               )
            )      
         )
      )

      if(transform && dbobjectp(car(objList)) then
         coordUpd = t
         object = car(objList)
         ll = lowerLeft(object~>bBox)
         ur = upperRight(object~>bBox)
         
         xT = caar(transform)
         yT = cadar(transform)
         oR = cadr(transform)
         if(oR == "R0" then
            xlo = car(ll) + xT 
            ylo = cadr(ll) + yT
            xhi = car(ur) + xT
            yhi = cadr(ur) + yT
         else
            if(oR == "MX" then
               xlo = car(ll) + xT 
               ylo = yT - cadr(ur)
               xhi = car(ur) + xT
               yhi = yT - cadr(ll)
            else
               if(oR == "R180" then
                  xlo = xT - car(ur)
                  ylo = yT - cadr(ur)
                  xhi = xT - car(ll)
                  yhi = yT - cadr(ll)
               else
                  if(oR == "MY" then
                     xlo = xT - car(ur)
                     ylo = cadr(ll) + yT
                     xhi = xT - car(ll)
                     yhi = cadr(ur) + yT
                  else
                     coordUpd = xlo = ylo = xhi = yhi = nil
                     printf("VALE WARNING: Only instance orientations of ")
                     printf("R0, R180, MX and MY are currently supported by ")
                     printf("VALEfilterOverlapList.il in the $CDS_MVS_IMF_CM/")
                     printf("directory.  Please update this file if other ")
                     printf("orientations are necessary.\n")
                  )
               )
            )
         ) ;if for new coordinates

         if(coordUpd then
            when(debug
               printf("VALE DEBUG: Net tracing start shape -> (%L %L) (%L %L)\n"
                  xlo ylo xhi yhi)
            )

            tmpShape = dbCreateRect(cv
               list(object~>layerName object~>purpose)
               list(list(xlo ylo) list(xhi yhi))) 
   
            ;; Use the RemoveAll compMod to clear the shape later
            dbCreateProp(tmpShape "imfGenerated" 'string "RemoveAll")
                           
            selectedObject = tmpShape 
            when(debug
               printf("VALE DEBUG: Net trace shape found in the ")
               printf("hierarchy, created a temporary top level ")
               printf("shape to start the net trace at %L, %L\n"
                  xlo ylo)
            )
         else
            selectedObject = nil
         )
      else
         selectedObject = nil
      )

      return(selectedObject)
   )
)
