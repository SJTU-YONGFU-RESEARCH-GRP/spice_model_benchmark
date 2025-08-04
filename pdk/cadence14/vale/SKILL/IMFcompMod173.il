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


procedure(IMFcompMod173(
             rtDpl
          @optional 
             (debug nil)
          )
   prog((tgtCv ttf tLayersList lppStr allLibList sCellList tgtOpts1 
         posX posY frame1X frame2X 
         frameY valeLayerMigFields valeLyrMigForm)

      when(debug
         printf("VALE DEBUG: Running %s\n" rtDpl->name)
      )

      tgtCv = geGetWindowCellView()
      unless(tgtCv
         printf("VALE ERROR: Unable to find an active layout window. ")
         printf("Please locate or open a layout window and try again.\n")
         return()
      )
      ttf = techGetTechFile(ddGetObj(tgtCv~>libName))
      tLayersList = nil
      foreach(lpp ttf~>lps
         when(lpp~>layer~>name
            lppStr = strcat(lpp~>layer~>name ":" lpp~>purpose)
            if(tLayersList then
               tLayersList = cons(lppStr tLayersList)
            else
               tLayersList = list(lppStr)
            )
         )
      )

      ;; Save user setting
      rtDpl->var1 = envGetVal("cdba" "copyMPAttributes")
      envSetVal("cdba" "copyMPAttributes" 'boolean t)

      tgtOpts1 = list("Make a selection..." "Create New...")
      allLibList = ddGetLibList()~>name
      allLibList = sort(allLibList nil)
      sCellList = ddGetObj(car(allLibList))~>cells~>name
      sCellList = sort(sCellList nil)

      posX = 5
      posY = 8
      frame1X = 290
      frame2X = 590
      frameY = 155
      valeLayerMigFields = list(
         list(hiCreateFrameField(
            ?name 'valeFrame1compMod173
            ?labelText "Source"
            ?help 'nil
            ?invisible 'nil
            ) ;frame field
            posX:posY
            frame1X:frameY 25
         )
         list(hiCreateFrameField(
            ?name 'valeFrame2compMod173
            ?labelText "Target"
            ?help 'nil
            ?invisible 'nil
            ) ;frame field
            frame1X+10:posY
            frame1X:frameY 25
         )
         list(hiCreateCyclicField(
            ?name 'valecompMod173SrcLibSel
            ?choices allLibList
            ?value car(allLibList)
            ?prompt "Library:"
            ?callback "_IMFlyrMigSrcLibSelCB(hiGetCurrentForm())"
            ) ;cyclic field
            posX+8:posY+20
            270:22 50
         )
         list(hiCreateCyclicField(
            ?name 'valecompMod173SrcCellSel
            ?choices sCellList 
            ?value car(sCellList)
            ?prompt "Cell Name:"
            ?callback "_IMFlyrMigSrcCellSelCB(hiGetCurrentForm())"
            ) ;cyclic field +30
            posX+8:posY+50
            270:22 65
         )
         list(hiCreateCyclicField(
            ?name 'valecompMod173SrcViewSel
            ?choices list("layout")
            ?value "layout"
            ?prompt "View Name:"
            ?callback "_IMFlyrMigSrcViewSelCB(hiGetCurrentForm())"
            ) ;cyclic field +30
            posX+8:posY+80
            270:22 65
         )
         list(hiCreateCyclicField(
            ?name 'valecompMod173SrcLyrSel
            ?choices list("Select Layer...")
            ?value "Select Layer..."
            ?prompt "Layer:"
            ?callback nil 
            ) ;cyclic field
            posX+8:posY+110
            270:22 50
         )
         list(hiCreateBooleanButton(
            ?name 'valecompMod173DoMulti
            ?value nil
            ?buttonLocation 'left
            ?buttonText "Use Layer Map File"
            ?callback "_IMFlyrMigUseLayerMapCB(hiGetCurrentForm())"
            ) ; string field +28
            posX+8:posY+158 
            170:22 17
         )
         list(hiCreateStringField(
            ?name 'valecompMod173LyrFile
            ?value ""
            ?prompt "Layer Migration Map:"
            ?editable t
            ?enabled nil
            ) ;string field +30
            posX+8:posY+183
            frame2X-70:22 120
         )
         list(hiCreateButton(
            ?name 'valecompMod173BrowseBtn
            ?buttonText "Browse"
            ?callback "_IMFlyrMigFileBrowserCB(hiGetCurrentForm())" 
            ?enabled nil
            ) ;string field +30
            frame2X-50:posY+181
            50:30 40
         )
         list(hiCreateBooleanButton(
            ?name 'valecompMod173DoHier
            ?value nil
            ?callback nil 
            ?buttonLocation 'left
            ?buttonText "Run Hierarchically"
            ?enabled nil
            ) ; string field +28
            posX+8:posY+210 
            170:22 17
         )
         list(hiCreateCyclicField(
            ?name 'valecompMod173TgtLibSel
            ?choices append(tgtOpts1 allLibList)
            ?value tgtCv~>libName
            ?prompt "Library:"
            ?enabled nil
            ?callback "_IMFlyrMigTgtLibSelCB(hiGetCurrentForm())"
            ) ;cyclic field
            frame1X+18:posY+20
            270:22 50
         )
         list(hiCreateCyclicField(
            ?name 'valecompMod173TgtCellSel
            ?choices ddGetObj(tgtCv~>libName)~>cells~>name
            ?value tgtCv~>cellName
            ?prompt "Cell Name:"
            ?enabled nil
            ?callback "_IMFlyrMigTgtCellSelCB(hiGetCurrentForm())"
            ) ;cyclic field +30
            frame1X+18:posY+50
            270:22 65
         )
         list(hiCreateCyclicField(
            ?name 'valecompMod173TgtViewSel
            ?choices list(tgtCv~>viewName)
            ?value tgtCv~>viewName
            ?prompt "View Name:"
            ?enabled nil
            ?callback nil
            ) ;cyclic field +30
            frame1X+18:posY+80
            270:22 65
         )
         list(hiCreateCyclicField(
            ?name 'valecompMod173TgtLyrSel
            ?choices append(list("Select Layer...") tLayersList)
            ?value "Select Layer..."
            ?prompt "Layer:"
            ?callback nil 
            ) ;cyclic field +30
            frame1X+18:posY+110
            270:22 50
         )
      )
      hiCreateAppForm(
         ?name 'valeLyrMigForm
         ?fields valeLayerMigFields
         ?formTitle "VALE Component Module for Layer Migration" 
         ?callback "_IMFlayerMigFormCB(hiGetCurrentForm() \"compMod173\")" 
         ?initialSize list(frame2X+10 frameY+85)
         ?buttonLayout 'OKCancelApply
         ?attachmentList list(
            bor(hicTopPercentSet hicLeftPercentSet hicRightPercentSet
               hicBottomPercentSet)
            bor(hicTopPercentSet hicLeftPercentSet hicRightPercentSet
               hicBottomPercentSet)
            bor(hicTopPercentSet hicLeftPercentSet hicRightPercentSet
               hicBottomPercentSet)
            bor(hicTopPercentSet hicLeftPercentSet hicRightPercentSet
               hicBottomPercentSet)
            bor(hicTopPercentSet hicLeftPercentSet hicRightPercentSet
               hicBottomPercentSet)
            bor(hicTopPercentSet hicLeftPercentSet hicRightPercentSet
               hicBottomPercentSet)
            bor(hicTopPercentSet hicLeftPercentSet hicRightPercentSet
               hicBottomPercentSet)
            bor(hicTopPercentSet hicLeftPercentSet hicRightPercentSet
               hicBottomPercentSet)
            bor(hicTopPercentSet hicLeftPercentSet hicRightPercentSet
               hicBottomPercentSet)
            bor(hicTopPercentSet hicLeftPercentSet hicRightPercentSet
               hicBottomPercentSet)
            bor(hicTopPercentSet hicLeftPercentSet hicRightPercentSet
               hicBottomPercentSet)
            bor(hicTopPercentSet hicLeftPercentSet hicRightPercentSet
               hicBottomPercentSet)
            bor(hicTopPercentSet hicLeftPercentSet hicRightPercentSet
               hicBottomPercentSet)
            bor(hicTopPercentSet hicLeftPercentSet hicRightPercentSet
               hicBottomPercentSet)
         )
      )

      hiDisplayForm(valeLyrMigForm)

      return(t)
   )
)
procedure(_IMFlyrMigSrcLibSelCB(form)
   let((srcLib cells stf sLayersList lppStr)
      srcLib = ddGetObj(form->valecompMod173SrcLibSel->value)
      cells = srcLib~>cells~>name
      cells = sort(cells nil)
      ;; Set the forms cell name list
      form->valecompMod173SrcCellSel->choices = cells
      form->valecompMod173SrcCellSel->value = car(cells)

      stf = techGetTechFile(srcLib)
      sLayersList = nil
      foreach(lpp stf~>lps
         lppStr = strcat(lpp~>layer~>name ":" lpp~>purpose)
         if(sLayersList then
            sLayersList = cons(lppStr sLayersList)
         else
            sLayersList = list(lppStr)
         )
      )
      form->valecompMod173SrcLyrSel->choices = 
         cons("Select Layer..." sLayersList)
      form->valecompMod173SrcLyrSel->value = "Select Layer..." 
   )
)

procedure(_IMFlyrMigTgtLibSelCB(form)
   prog((cells index timeCode maxTimeCode maxIndex tgtLib tLayersList lppStr
         ttf)
      if(form->valecompMod173TgtLibSel->value == "Make a selection..." ||
         form->valecompMod173TgtLibSel->value == "Create New..." then
         when(form->valecompMod173TgtLibSel->value == "Create New..."
            ;; Create New Library Form
            unless(ddsHiCreateLibrary()
               printf("VALE ERROR: A problem occurred creating a target ")
               printf("library for the Layer Migration.\n")
               return()
            )
            ;; In order to update the Layer Migration form, query the last
            ;; library created
            index = maxTimeCode = maxIndex = 0
            foreach(timeString ddGetLibList()~>lastModify
               index++
               timeCode = stringToTime(timeString)
               when(timeCode > maxTimeCode
                  maxTimeCode = timeCode
                  maxIndex = index
               )
            )
            tgtLib = nthelem(maxIndex ddGetLibList())

            ;; Update the form with the new library name
            form->valecompMod173TgtLibSel->choices = append(
               list(tgtLib~>name) form->valecompMod173TgtLibSel->choices)
            form->valecompMod173TgtLibSel->value = tgtLib~>name

            ;; Update the form with the new library cell list
            cells = sort(tgtLib~>cells~>name nil)
            form->valecompMod173TgtCellSel->choices = cells 
            form->valecompMod173TgtCellSel->value = car(cells) 
         )
      else
         tgtLib = ddGetObj(form->valecompMod173TgtLibSel->value)
         cells = tgtLib~>cells~>name
         cells = sort(cells nil)
         ;; Set the form's cell name list
         form->valecompMod173TgtCellSel->choices = cells
         form->valecompMod173TgtCellSel->value = car(cells) 
      )
 
      ttf = techGetTechFile(tgtLib)
      tLayersList = nil
      foreach(lpp ttf~>lps
         lppStr = strcat(lpp~>layer~>name ":" lpp~>purpose)
         if(tLayersList then
            tLayersList = cons(lppStr tLayersList)
         else
            tLayersList = list(lppStr)
         )
      )
      form->valecompMod173TgtLyrSel->choices = 
         cons("Select Layer..." tLayersList)
      form->valecompMod173TgtLyrSel->value = "Select Layer..." 
   )
)

procedure(_IMFlyrMigSrcCellSelCB(form)
   let((srcLib srcCell srcView viewList cv lpListNew)
      srcLib = form->valecompMod173SrcLibSel->value
      srcCell = form->valecompMod173SrcCellSel->value
      viewList = dbAllCellViews(ddGetObj(srcLib) srcCell)
      viewList = sort(viewList nil)
      form->valecompMod173SrcViewSel->choices = viewList
      srcView = car(viewList)
      form->valecompMod173SrcViewSel->value = srcView

      if(ddGetObj(srcLib srcCell srcView) then
         cv = dbOpenCellViewByType(srcLib srcCell srcView nil "r")
         if(dbobjectp(cv) then
            lpListNew = _IMFbuildLayerPurposeList(cv)
            if(lpListNew then
               form->valecompMod173SrcLyrSel->choices = lpListNew
               form->valecompMod173SrcLyrSel->value = car(lpListNew)
            else
               form->valecompMod173SrcLyrSel->choices =
                  list("No layers available")
               form->valecompMod173SrcLyrSel->value = "No layers available"
            )
         else
            printf("VALE WARNING: Failed to open the source cellview to ")
            printf("filter the layer selection list.\n")
            form->valecompMod173SrcLyrSel->choices =
               list("No layers available")
            form->valecompMod173SrcLyrSel->value = "No layers available"
         )
         dbClose(cv)
      else
         printf("VALE WARNING: Failed to open the source cellview to ")
         printf("filter the layer selection list.\n")
         form->valecompMod173SrcLyrSel->choices = list("No layers available")
         form->valecompMod173SrcLyrSel->value = "No layers available"
      )
   )
)

procedure(_IMFlyrMigSrcViewSelCB(form)
   let((srcLib srcCell srcView cv lpListNew)
      srcLib = form->valecompMod173SrcLibSel->value
      srcCell = form->valecompMod173SrcCellSel->value
      srcView = form->valecompMod173SrcViewSel->value

      if(ddGetObj(srcLib srcCell srcView) then
         cv = dbOpenCellViewByType(srcLib srcCell srcView nil "r")
         if(dbobjectp(cv) then
            lpListNew = _IMFbuildLayerPurposeList(cv)
            if(lpListNew then
               form->valecompMod173SrcLyrSel->choices = lpListNew
               form->valecompMod173SrcLyrSel->value = car(lpListNew)
            else
               form->valecompMod173SrcLyrSel->choices =
                  list("No layers available")
               form->valecompMod173SrcLyrSel->value = "No layers available"
            )
         else
            printf("VALE WARNING: Failed to open the source cellview to ")
            printf("filter the layer selection list.\n")
            form->valecompMod173SrcLyrSel->choices =
               list("No layers available")
            form->valecompMod173SrcLyrSel->value = "No layers available"
         )
         dbClose(cv)
      else
         printf("VALE WARNING: Failed to open the source cellview to ")
         printf("filter the layer selection list.\n")
         form->valecompMod173SrcLyrSel->choices = list("No layers available")
         form->valecompMod173SrcLyrSel->value = "No layers available"
      )
   )
)

procedure(_IMFlyrMigTgtCellSelCB(form)
   let((tgtLib tgtCell viewList)
      tgtLib = form->valecompMod173TgtLibSel->value
      tgtCell = form->valecompMod173TgtCellSel->value
      viewList = dbAllCellViews(ddGetObj(tgtLib) tgtCell)
      viewList = sort(viewList nil)
      form->valecompMod173TgtViewSel->choices = viewList
      form->valecompMod173TgtViewSel->value = car(viewList)
   )
)

procedure(_IMFlyrMigUseLayerMapCB(form)
   if(form->valecompMod173DoMulti->value then
      form->valecompMod173LyrFile->enabled = t
      form->valecompMod173BrowseBtn->enabled = t
      form->valecompMod173SrcLyrSel->enabled = nil
      form->valecompMod173TgtLyrSel->enabled = nil
   else
      form->valecompMod173LyrFile->enabled = nil 
      form->valecompMod173BrowseBtn->enabled = nil
      form->valecompMod173SrcLyrSel->enabled = t
      form->valecompMod173TgtLyrSel->enabled = t
   )
)

procedure(_IMFlyrMigFileBrowserCB(form)
   let((layerFileList layerFile)
      layerFileList = hiDisplayFileDialog(
         ?dialogName 'valecompMod173FileBrowser 
         ?filter "SKILL (*.il)" 
         ?caption "Select the layer map list to load"
      )
      layerFile = buildString(layerFileList "/")
      printf("%L\n" layerFile)
      if(isFile(layerFile) then
         form->valecompMod173LyrFile->value = layerFile
      else
         form->valecompMod173LyrFile->value = layerFile
         printf("VALE ERROR: Failed to find or access the layer map list ")
         printf("file %L.\n" layerFile)
      )
   )
)
