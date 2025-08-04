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

procedure(IMFcompMod16(
             rtDpl
          @optional 
             (debug nil)
          )
   prog((cm16LB cm16form)
      printf("VALE INFO: Running %s\n" rtDpl->name)

      cm16LB = hiCreateListBoxField(
         ?name 'VALEcm16LB
         ?prompt "Multi-select Layer(s)\nto Deleting WSPs:"
         ?choices _IMFdat->wspLayers
         ?defValue _IMFdat->wspLayers
         ?multipleSelect t
      )
      cm16form = hiCreateAppForm(
         ?name 'VALEcm16App
         ?fields list(list(cm16LB 10:10 260:270 120))
         ?formTitle "Delete WSPs"
         ?attachmentList list(
            bor(hicTopPercentSet hicLeftPercentSet hicRightPercentSet
               hicBottomPercentSet)
         )
         ?callback strcat("VALEcompMod16CB(rtDpl "
            "VALEcm16App->VALEcm16LB->value debug)")
         ?initialSize list(270 290)
      )
      hiDisplayForm(cm16form)

      return(t)
   )
)
procedure(VALEcompMod16CB(rtDpl layerList debug)
   prog((figList erv)
      foreach(grp rtDpl->topCv~>figGroups
         figList = setof(fig grp~>figs member(fig~>layerName layerList) && 
            fig~>purpose == "track")

         ;; Delete track shapes
         foreach(fig figList 
            erv = errset(dbDeleteObject(fig))
            if(erv then
               if(erv == list(nil) then
                  printf("VALE WARNING: Failed to delete ")
                  printf("%L %L in figGroup " fig~>layerName fig~>purpose)
                  printf("%L\n" grp~>name)
               )
            else
               printf("VALE ERROR: A problem occurred while deleting ") 
               printf("%L %L in figGroup " fig~>layerName fig~>purpose)
               printf("%L: %L\n" grp~>name errset.errset)
            )
         )

         ;; If that was the only shape, delete the group
         unless(grp~>figs
            erv = errset(dbDeleteObject(grp))
            if(erv then
               if(erv == list(nil) then
                  printf("VALE WARNING: Failed to delete figGroup ")
                  printf("%L\n" grp~>name)
               )
            else
               printf("VALE ERROR: A problem occurred while deleting ") 
               printf("figGroup %L: %L\n" grp~>name errset.errset)
            )
         )

      )
      printf("VALE INFO: %s complete.\n" rtDpl->name)
      return(t)
   )
)

