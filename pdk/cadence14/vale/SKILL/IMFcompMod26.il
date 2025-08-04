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


procedure(IMFcompMod26(
             rtDpl
          @optional
             (debug nil)
          )
   prog((cellList label labelList)
      when(debug
         printf("VALE DEBUG: Running %L\n" rtDpl->description)
      )

      cellList = setof(cell dbGetOpenCellViews() 
         cell~>cellViewType == "schematic" && 
         cell~>libName == rtDpl->topCv~>libName)
      if(cellList then
         foreach(cvObj cellList
            label = strcat(cvObj~>libName ":" cvObj~>cellName)
            labelList = cons(label labelList)
         )
         hiShowListBox(
            ?name 'valeOpenCellSelector
            ?choices labelList
            ?callback 'VALEinspectCellInstPropsCB
            ?title "Select a Cell to Inspect"
            ?appData nil 
            ?multipleSelect nil
         )
      else
         printf("VALE WARNING: No schematic is open to inspect instance ")
         printf("properties. Please open a schematic and re-run.\n")
         schHiOpenCellView()
         return(t)
      )

      return(t)
   )
)

procedure(VALEinspectCellInstPropsCB(enable formData)
   prog((cv selList libName cellName propList appData)
      when(enable
         selList = parseString(car(formData->value) ":")
         libName = car(selList)
         cellName = cadr(selList)
         appData = list(libName cellName)

         if(ddGetObj(libName cellName "schematic") then
            cv = dbOpenCellViewByType(libName cellName "schematic" nil "a")
            unless(cv
               printf("VALE ERROR: Failed to open %L/%L/%L\n" libName
                  cellName "schematic")
               return()
            )
            unless(_IMFisCellAnOpenWindow(cv)
               geOpen(?lib cv~>libName ?cell cv~>cellName ?view cv~>viewName
                  ?mode "a")
            )
         else
            printf("VALE ERROR: Failed to find and open %L/%L/%L\n" libName
               cellName "schematic")
            return()
         )

         propList = nil
         foreach(inst cv~>instances
            when(inst~>libName == cv~>libName ||
                 inst~>libName == 
                    _IMFdat->compMod88->envVars->IMF_MIG_TARGET_TECH 
               foreach(prop inst~>prop
                  cdfgData = cdfGetInstCDF(inst)
                  parId = cdfFindParamByName(cdfgData prop~>name)
                  if(parId then
                     if(parId->defValue == parId->value then
                        propList = cons(strcat(inst~>cellName "," inst~>name
                           ":" prop~>name) propList)
                     )
                  else
                     propList = cons(strcat(inst~>cellName "," inst~>name 
                        ":" prop~>name) propList)
                  )
               )
            )
         )
         if(propList then
            hiShowListBox(
               ?name 'valePropInspector
               ?choices propList
               ?callback 'VALErmSelInstPropsCB
               ?title "Select one or more for deletion"
               ?appData appData 
               ?multipleSelect t
            )
         else
            printf("VALE INFO: No instance properties found in the current ")
            printf("cellview %s.\n" cellName)
         )
   
         return(t)
      )
      return(t)
   )
)

procedure(VALErmSelInstPropsCB(enable formData)
   prog((lib cell cv itemList nameList pname cellName instName selInst)
      when(enable
         
         lib = car(formData~>appData)
         cell = cadr(formData~>appData)
         cv = dbOpenCellViewByType(lib cell "schematic" nil "a")
         unless(cv
            printf("VALE ERROR: Unable to find the selected schematic ")
            printf("%s/%s/%s\n" lib cell "schematic")
            return()
         )

         foreach(lineItem formData->value
            itemList = parseString(lineItem ":")
            pname = cadr(itemList)
            nameList = parseString(car(itemList) ",")
            cellName = car(nameList)
            instName = cadr(nameList)
            
            selInst = dbFindAnyInstByName(cv instName)
            if(selInst then
               if(dbGetPropByName(selInst pname) then
                  if(dbDeletePropByName(selInst pname) then
                     printf("VALE INFO: Removed %s %s property %s.\n" cellName
                        instName pname)
                  else
                     printf("VALE INFO: Failed to remove %s %s property %s\n"
                        cellName instName pname)
                  )
               else
                  printf("VALE INFO: Property %s not found on instance %s\n"
                     pname instName)
               )
            else
               printf("VALE INFO: Instance %s not found in cellview %s\n"
                  instName cellName)
            )
         )
         ;; Close the most recent dbOpen...
         dbClose(cv)
      )
   )
)
            
