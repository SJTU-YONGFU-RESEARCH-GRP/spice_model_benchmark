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


procedure(IMFcompMod175(
             rtDpl
          @optional 
             (debug nil)
          )
   prog((cv shapeList lppList valecompMod175Form valecompMod175Fields
         posX posY frame1X frameY)

      when(debug
         printf("VALE DEBUG: Running %s\n" rtDpl->name)
      )

      cv = geGetWindowCellView()
      unless(cv
         printf("VALE ERROR: Unable to find an active layout window. ")
         printf("Please locate or open a layout window and try again.\n")
         return()
      )

      shapeList = geGetSelSet()
      shapeList = setof(s1 shapeList dbobjectp(s1))
      shapeList = setof(s2 shapeList s2~>objType != "ruler")
      lppList = _IMFbuildLayerPurposeList2(shapeList) 

      posX = 5
      posY = 8
      frame1X = 290
      frameY = 125
      valecompMod175Fields = list(
         list(hiCreateFrameField(
            ?name 'valeFrame1compMod175
            ?labelText "Re-Step Objects"
            ?help 'nil
            ?invisible 'nil
            ) ;frame field
            posX:posY
            frame1X:frameY 25
         )
         list(hiCreateCyclicField(
            ?name 'valecompMod175LyrSel
            ?choices lppList 
            ?value car(lppList)
            ?prompt "Layer filter:"
            ?callback nil 
            ) ;cyclic field
            posX+8:posY+20
            270:22 70
         )
         list(hiCreateStringField(
            ?name 'valecompMod175StepDelta
            ?value "0.001"
            ?prompt "Step Delta:"
            ?editable t
            ) ;string field +30
            posX+8:posY+50
            270:22 70
         )
         list(hiCreateCyclicField(
            ?name 'valecompMod175StepDir
            ?choices list("x+" "x-" "y+" "y-")
            ?value "x+"
            ?prompt "Direction:"
            ?callback nil 
            ) ;cyclic field +30
            posX+8:posY+80
            270:22 70
         )
      )
      hiCreateAppForm(
         ?name 'valecompMod175Form
         ?fields valecompMod175Fields
         ?formTitle "VALE Component Module"
         ?callback "_IMFreStepObjectsFormCB(hiGetCurrentForm() \"175\")" 
         ?initialSize list(frame1X+10 frameY+5)
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
         )
      )

      hiDisplayForm(valecompMod175Form)

      return(t)
   )
)

