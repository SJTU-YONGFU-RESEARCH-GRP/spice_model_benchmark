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
   2018-06-15 JF Initial coding for FastXOR
   2018-07-25 JF Updated Component Module based on MVS18.10 code efficiency 
                 enhancements: Changes 180724a 180724b 180724c 180724d 180725a
                 180725b 180725c
   2018-12-14 JF Changed the PVS run directory to VALE_RUNDIR/wd.<CM>_<cellName>
   2019-06-13 JF Change 190613b, updates to remove compMod25 from the core tool

*/

procedure(IMFcompMod25(
             rtDpl
          @optional 
             (debug nil)
          ) 
   prog((cv libCellNameList libNameList imfCompMod25Fields imfCompMod25Form 
         erv okToSave msg) 

      printf("VALE INFO: Running %L ...\n" rtDpl->name) 

      cv = geGetWindowCellView()
      unless(cv
         printf("VALE ERROR: Unable to find an active layout window. ")
         printf("Please locate or open a layout window and try again.\n")
         return()
      )

      when(dbIsCellViewModified(cv)
         ;; Dialog box regarding the need to save the current cellview before 
         ;; running PVS FastXOR
         sprintf(msg "The current layout window must be saved before running ")
         sprintf(msg "%s Fast XOR. Would you like to save and continue?" msg)
         okToSave = hiDisplayAppDBox(
            ?name 'imfWaitForUserOnXOR
            ?dboxBanner "FastXOR Question"
            ?dboxText msg
            ?callback 'nil
            ?dialogType hicQuestionDialog
            ?dialogStyle 'modal
            ?buttonLayout 'YesNo
         )
         if(okToSave then
            dbSave(cv)
         else
            printf("VALE INFO: Exiting without saving.\n")
            return()
         )
      )

      ;; Turn off Layer Palette Object Markers
      leSetObjectVisible("Markers" nil)

      ;; Start Component Module Core Function
      when(rtDpl->outputLocation != "Shapes"
         printf("VALE INFO: The output location is always \"Shapes\" for ")
         printf("Component Module %L. Overriding current " rtDpl->name)
         printf("setting of %L\n" rtDpl->outputLocation)
         rtDpl->outputLocation = "Shapes"
      )

      libCellNameList = ddGetObj(cv~>libName)~>cells~>name 
      rtDpl->libNameList = libNameList = ddGetLibList()~>name 

      imfCompMod25Fields = list(
         list(hiCreateFrameField(
            ?name 'imfFrameCompMod25
            ?labelText "VALE Fast XOR Options"
            ?help 'nil
            ?invisible 'nil
            );frame field
            5:5
            390:80 25
         )
         list(hiCreateCyclicField(
            ?name 'imfcompMod25Cell1
            ?choices libCellNameList
            ?value cv~>cellName
            ?prompt "Layout 1:"
            ?callback nil 
            ) ;cyclic field
            10:25
            200:22 55
         )
         list(hiCreateCyclicField(
            ?name 'imfcompMod25Lib1
            ?choices libNameList
            ?value cv~>libName
            ?callback "IMFcompMod25FormLib1CB(hiGetCurrentForm())"
            ) ;cyclic field
            220:25
            160:22 5
         )
         list(hiCreateCyclicField(
            ?name 'imfcompMod25Cell2
            ?choices libCellNameList
            ?value car(libCellNameList)
            ?prompt "Layout 2:"
            ?callback nil 
            ) ;cyclic field
            10:48
            200:22 55
         )
         list(hiCreateCyclicField(
            ?name 'imfcompMod25Lib2
            ?choices libNameList
            ?value car(libNameList)
            ?callback "IMFcompMod25FormLib2CB(hiGetCurrentForm())"
            ) ;cyclic field
            220:48
            160:22 5
         )
      )
      hiCreateAppForm(
         ?name 'imfCompMod25Form
         ?fields imfCompMod25Fields
         ?formTitle strcat("PVS " rtDpl->name)
         ?callback "_IMFfastXORFormCB(hiGetCurrentForm() \"compMod25\" getShellEnvVar(\"CDS_MVS_IMF_DEBUG\"))"
         ?initialSize list(400 85)
         ?buttonLayout 'OKCancel
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
         )
      ) ;form

      erv = errset(hiDisplayForm(imfCompMod25Form))
      if(erv then
         if(erv == list(nil) then
            printf("VALE INFO: Complete\n")
         )
      else 
         printf("VALE ERROR: A problem occurred building the VALE framework ")
         printf("%L form.\n%L\n" rtDpl->name errset.errset)
         return()
      )

      return(t)
   )
)

procedure(IMFcompMod25FormLib1CB(form)
   form->imfcompMod25Cell1->choices =
      ddGetObj(form->imfcompMod25Lib1->value)~>cells~>name
)

procedure(IMFcompMod25FormLib2CB(form)
   form->imfcompMod25Cell2->choices =
      ddGetObj(form->imfcompMod25Lib2->value)~>cells~>name
)

