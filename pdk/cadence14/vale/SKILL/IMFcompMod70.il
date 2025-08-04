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


procedure(IMFcompMod70(
             rtDpl
          @optional 
             (debug nil)
          )
   prog((cv win appType plugins foundit netNameList netList 
         )

      printf("VALE INFO: Creating %L as %L %L ...\n" rtDpl->name 
         rtDpl->outputStyle rtDpl->outputLocation) 

      cv = geGetWindowCellView()
      unless(cv
         printf("VALE ERROR: Unable to find an active layout window. ")
         printf("Please locate or open a layout window and try again.\n")
         return()
      )

      win = hiGetCurrentWindow()
      unless(win
         printf("VALE ERROR: Failed to find the current window.\n")
         return()
      )
      appType = hiGetAppType(win)
      when(appType == "Layout"
         deInstallApp(win "Virtuoso XL")
      )

      ;; Install the DFM plug-in if not already
      plugins = deGetPlugins(win)
      foundit = nil
      foreach(plugin plugins
         when(plugin~>name_ == "DFM-Plugin" 
            foundit = t
         )
      )
      unless(foundit
         errset(deInstallPlugin(win 'DFMPlugin ))
      )

      ;; Turn off Layer Palette Object Markers
      leSetObjectVisible("Markers" nil)

      ;; Filter for the nets that have pin figures or shapes at the top level
      netList = netNameList = nil
      foreach(netObj cv~>nets
         traceShape = car(netObj~>pins)~>fig
         when(traceShape
            netNameList = cons(netObj~>name netNameList)
            netList = cons(list(netObj~>name traceShape) netList)
         )
      )
         
      if(netNameList then
         hiShowListBox(
            ?name 'valecompMod70Sel
            ?choices netNameList     
            ?callback 'VALErunTraceAndOpenCB
            ?title "Select one or more net names to open"
            ?appData netList
            ?multipleSelect t
         )
      else
         printf("VALE WARNING: No net objects were found in the current ")
         printf("design (geGetWindowCellView()~>nets). Please check and ")
         printf("re-run.\n")
         return() 
      )

      printf("VALE INFO: %s complete.\n" rtDpl->name)

      return(t)
   )
)

procedure(VALErunTraceAndOpenCB(enable formData)
   prog((cv debug newCellName count maxCount)
      debug = nil
      cv = geGetWindowCellView()

      if(enable then
         printf("VALE INFO: Opening new cellviews for traced nets %L...\n"
            formData->value)
         count = 0
         maxCount = 5
         foreach(namedNet formData->value
            foreach(netSet appData
               when(namedNet == car(netSet) && count < maxCount
                  when(debug
                     printf("VALE DEBUG: Sending %s to tracer...\n" namedNet)
                  )
                  newCellName = _IMFsaveNetBySelection(cv t netSet debug)
                  if(newCellName then
                     geOpen(?lib cv~>libName ?cell newCellName ?view 
                        cv~>viewName)
                     count++
                  else
                     printf("VALE ERROR: Failed to trace the net ")
                     printf("%s, continuing to next net.\n" namedNet)
                  )
               )
            )
         )
         return(t)
      else
         when(debug
            printf("VALE ERROR: Net selection list box not enabled.\n")
         )
         return()
      )
   )
)
