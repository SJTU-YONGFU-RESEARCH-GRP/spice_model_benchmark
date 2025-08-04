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
   Revision Log:
   200428  JF  Created new version for removing WSP shapes and figGroups

*/

procedure(IMFcompMod199(
             rtDpl
          @optional 
             (debug nil)
          )
   prog((cm199LB cm199form)
      printf("VALE INFO: Running %s\n" rtDpl->name)

      cm199LB = hiCreateListBoxField(
         ?name 'VALEcm199LB
         ?prompt "Multi-select Layer(s)\nto Deleting WSP Templates:"
         ?choices _IMFdat->wspLayers
         ?defValue _IMFdat->wspLayers
         ?multipleSelect t
      )
      cm199form = hiCreateAppForm(
         ?name 'VALEcm199App
         ?fields list(list(cm199LB 10:10 260:270 120))
         ?formTitle "Delete WSP Templates"
         ?attachmentList list(
            bor(hicTopPercentSet hicLeftPercentSet hicRightPercentSet
               hicBottomPercentSet)
         )
         ?callback strcat("VALEcompMod199CB(rtDpl "
            "VALEcm199App->VALEcm199LB->value debug)")
         ?initialSize list(270 290)
      )
      hiDisplayForm(cm199form)

      return(t)
   )
)
procedure(VALEcompMod199CB(rtDpl layerList debug)
   prog((deleteList erv lpp ddList)

      deleteList = dbGetWidthSpacingPatterns(rtDpl->topCv)
      foreach(wsp deleteList
         erv = errset(dbDeleteObject(wsp))
         if(erv then
            if(erv == list(nil) then
               printf("VALE WARNING: Failed to delete WSP %L in %s\n"
                  wsp~>name rtDpl->topCv~>cellName)
            )
         else
            printf("VALE ERROR: A problem occurred while attempting to ")
            printf("delete WSP %L in %s: %L\n" wsp~>name rtDpl->topCv~>cellName
               errset.errset)
         )
      )
      foreach(lyr layerList
         if(member(lyr _IMFdat->wspLayers) then
            foreach(purp _IMFdat->wspPurposes
               lpp = list(lyr purp)
               ddList = dbGetWidthSpacingSnapPatternDefsByLP(rtDpl->topCv lpp)
               when(ddList
                  foreach(wspDef ddList
                     when(wspDef
                        erv = errset(dbDeleteWidthSpacingSnapPatternDef(wspDef))
                        if(erv then
                           if(erv == list(nil) then
                              printf("VALE WARNING: Failed to delete wsspDef ")
                              printf("%L in %s for lpp: %L\n" wspDef~>name
                                 rtDpl->topCv~>cellName lpp)
                           )
                        else
                           printf("VALE ERROR: A problem occurred while ")
                           printf("attempting to delete wsspDef ")
                           printf("%L in %s for lpp %L: %L\n" wsp~>name
                              rtDpl->topCv~>cellName lpp errset.errset)
                        )
                     )
                  )
               )
            )
         else
            printf("VALE WARNING: Layer %s was not found in the _IMFdat" lyr)
            printf("->wspLayers, please update the config file if necessary\n")
         )
      )

      printf("VALE INFO: %s complete.\n" rtDpl->name)
      return(t)
   )
)

