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
   2019-02-20 JF Initial Coding for automatic coloring

*/

procedure(IMFcompMod60(
             rtDpl
          @optional
             (verbose nil)
          )
   prog((erv lppList layer cv autoColorList erv failFlag)

      erv = errset(leGetEntryLayer())
      if(erv then
         if(erv == list(nil) then
            printf("VALE WARNING: Failed to find the active/selected layer. ")
            printf("Please select a layer in the Layer Palette and re-run.\n")
            return(t)
         else
            lppList = car(erv)
            layer = car(lppList)
            purpose = cadr(lppList)
            when(!member(layer   _IMFdat->mpLayers) ||
                 !member(purpose _IMFdat->mpPurposes)
               printf("VALE WARNING: The selected LPP in the Layer Palette ")
               printf("is not one of multiple patterning layers listed in ")
               printf("the VALE Framework configuration file: %L. " 
                  _IMFdat->mpLayers )
               printf("Please verify the configuration file is correct, or ")
               printf("select a different layer and re-run.\n")
               return(t)
            )
            ;; pass through
         )
      else
         printf("VALE WARNING: Failed to find the active/selected layer. ")
         printf("Please select a layer in the Layer Palette and re-run.\n")
         return(t)
      )
      
      cv = geGetWindowCellView()
      unless(cv
         printf("VALE ERROR: Unable to find an active layout window. ")
         printf("Please locate or open a layout window and try again.\n")
         return()
      )
 
      printf("VALE INFO: Running Virtuoso Coloring for layer %s " layer)
      printf("on the current level of hierarchy only.\n") 

      ;; Store the user's env var settings in autoColorList
      autoColorList = list(
         list(nil 'name "coloringEngineEnabled"   'type "boolean" 
                  'cat "mpt"  'cmValue nil)
         list(nil 'name "defaultColoringMethod"   'type "cyclic"  
                  'cat "mpt"  'cmValue "managed")
         list(nil 'name "reColorReadOnlyCellView" 'type "boolean"
                  'cat "dpt"  'cmValue nil)
         list(nil 'name "unclusteredShapeColor"   'type "cyclic"
                  'cat "mpt"  'cmValue "random")
         list(nil 'name "hideStitchingTools"      'type "boolean" 
                  'cat "dpt"  'cmValue t)
         list(nil 'name "copyMPAttributes"        'type "boolean"
                  'cat "cdba" 'cmValue t)
      )
     
      ;; Save each env var into an originalValue 
      foreach(acDpl autoColorList
         acDpl->originalValue = envGetVal(acDpl->cat acDpl->name)
         erv = envSetVal(acDpl->cat acDpl->name stringToSymbol(acDpl->type)
            acDpl->cmValue)
         if(erv then
            if(erv == list(nil) then
               printf("VALE WARNING: Failed to set %s to " acDpl->name)
               printf("%L\n" acDpl->cmValue)
            )
            ;; pass through
         else
            printf("VALE ERROR: A problem occurred while setting ")
            printf("%s to %L\n%L\n" acDpl->name acDpl->cmValue errset.errset)
            return()
         )
      )

      ;; Color the layer
      if(member(layer _IMFdat->mpLayers) then
         erv = errset(mptReColor(cv list(layer) 0))
         unless(erv
            printf("VALE ERROR: A problem occurred during Automatic Coloring ")
            printf("for layer %s\n" layer)
            failFlag = t 
         )
         mptLockAll(cv list(layer))
      else
         if(layer == "ALL" then
            erv = errset(mptReColor(cv _IMFdat->mpLayers) 0)
            unless(erv
               printf("VALE ERROR: A problem occurred during Automatic ")
               printf("Coloring for layer %s\n" layer)
               failFlag = t 
            )
         else
            printf("VALE INFO: Layer %s is not colorable through the " layer)
            printf("VALE framework Auto Color component modules.  Enabled ")
            printf("layers are %L\n" _IMFdat->mpLayers)
         )
      )

      ;; Reset env vars
      foreach(acDpl autoColorList
         erv = envSetVal(acDpl->cat acDpl->name stringToSymbol(acDpl->type)
            acDpl->originalValue)
         if(erv then
            if(erv == list(nil) then
               printf("VALE WARNING: Failed to reset %s to " acDpl->name)
               printf("%L\n" acDpl->originalValue)
            )
            ;; pass through
         else
            printf("VALE ERROR: A problem occurred while resetting ")
            printf("%s to %L\n%L\n" acDpl->name acDpl->originalValue errset.errset)
            return()
         )
      )

      if(failFlag then
         return()
      else
         return(t)
      )
   )
)
