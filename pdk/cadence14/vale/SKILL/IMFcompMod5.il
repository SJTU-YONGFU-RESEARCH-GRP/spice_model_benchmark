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
 | This source code and any other accompanying code ("Code") is        |
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
   200312  JF  Created EM Wire Guide Tool for GPDK

*/

procedure(IMFcompMod5(
          rtDpl
          @optional
             (debug nil)
          )
   prog((compMod5Form compMod5Fields posX posY frameX frameY)
      printf("VALE INFO: Starting %L\n" rtDpl->description)

      ;; Build form
      posX = 5
      posY = 5
      frameX = 525
      frameY = 246
      compMod5Fields = list(
         list(hiCreateFrameField(
            ?name 'compMod5Frame
            ?labelText "Wire Width(s)"
            ?help 'nil
            ?invisible 'nil
            ) ;frame field
            posX:posY
            frameX:frameY 25
         )
         list(hiCreateComboField(
            ?name 'compMod5Current
            ?items rtDpl->currentExamples
            ?value car(rtDpl->currentExamples)
            ?prompt "I(dc) Estimate: "
            )
            posX+8:posY+16
            190:28 100
         )
         list(hiCreateComboField(
            ?name 'compMod5Type
            ?items rtDpl->calcType
            ?value car(rtDpl->calcType)
            ?callback "_IMFwireToolTypeCB(hiGetCurrentForm() rtDpl debug)"
            ?prompt ""
            )
            posX+215:posY+16
            140:28 80
         )
         list(hiCreateBooleanButton(
            ?name 'compMod5ShortLength
            ?value nil
            ?buttonLocation 'left
            ?buttonText "Short Length Multiplier"
            )
            posX+18:posY+50
            170:22 17
         )
         list(hiCreateReportField(
            ?name 'compMod5Report
            ?headers list(
               list("Layer" 50 'left 'string nil nil nil)
               list("Min Width/Min Via Count" 220 'center 'string nil nil nil)
               list("Irms limit" 0 'center 'string nil nil nil)
               )
            ?choices list(
               list("M1" "0.0" "n/a")
               list("V1" "0" "n/a")
               list("M2" "0.0" "n/a")
               list("V2" "0" "n/a")
               list("M3" "0.0" "n/a")
               list("V3" "0" "n/a")
               )
            )
            posX+215:posY+50
            300:130 22
         )
         list(hiCreateBooleanButton(
            ?name 'compMod5WideWire
            ?value nil
            ?buttonLocation 'left
            ?buttonText "Wide Wire Multiplier"
            )
            posX+18:posY+74
            170:22 17
         )
         list(hiCreateBooleanButton(
            ?name 'compMod5NumLines
            ?value nil
            ?buttonLocation 'left
            ?buttonText "Number of Lines Multiplier"
            )
            posX+18:posY+98
            170:22 17
         )
         list(hiCreateComboField(
            ?name 'compMod5Temp
            ?items rtDpl->temperature
            ?value "110" 
            ?prompt "Temperature: "
            ?callback "printf(\"VALE INFO: Temperature = %L\n\" hiGetCurrentForm()->compMod5Temp->value)"
            )
            posX+18:posY+148
            165:24 82
         )
         list(hiCreateComboField(
            ?name 'compMod5ViaType
            ?items rtDpl->viaType
            ?value car(rtDpl->viaType)
            ?prompt "         Via Type: "
            ?callback "printf(\"VALE INFO: Via Type = %L\n\" hiGetCurrentForm()->compMod5ViaType->value)"
            )
            posX+18:posY+178
            165:24 82
         )
         list(hiCreateBooleanButton(
            ?name 'compMod5ForceReload
            ?value nil
            ?buttonLocation 'left
            ?buttonText "Reload All Equations"
            )
            posX+18:posY+211
            172:22 17
         )
         list(hiCreateButton(
            ?name 'compMod5Calculate
            ?buttonText "Calculate"
            ?callback "_IMFwireToolCalcCB(hiGetCurrentForm() rtDpl debug)"
            ?enabled t
            )
            posX+215:posY+184
            70:28 40
         )
         list(hiCreateButton(
            ?name 'compMod5Reset
            ?buttonText "Reset"
            ?callback "_IMFwireToolResetCB(hiGetCurrentForm() debug)"
            ?enabled t
            )
            posX+290:posY+184
            70:28 40
         )
      )
      hiCreateAppForm(
         ?name 'compMod5Form
         ?fields compMod5Fields
         ?formTitle "VALE Framework EM Wire Guide"
         ?initialSize list(frameX+10 frameY+15)
         ?buttonLayout 'Close
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
         )
      )

      hiDisplayForm(compMod5Form)

      return(t)
   )
)

procedure(_IMFwireToolCalcCB(form rtDpl debug)
   prog((inputDpl eqFilePath erv results reloadEqs formattedResults
         currentResult)
      inputDpl = list(nil
         'current form->compMod5Current->value
         'wideWireX form->compMod5WideWire->value
         'shortLenX form->compMod5ShortLength->value
         'midLenX form->compMod5MidLength->value
         'temp form->compMod5Temp->value
         'viaType form->compMod5ViaType->value
         'numLinesX form->compMod5NumLines->value
      )
      when(debug
         printf("VALE DEBUG: inputDpl is %L\n" inputDpl)
      )

      when(debug
         printf("VALE DEBUG: form contents are %L\n" form->compMod5Report->value )
      )

      reloadEqs = form->compMod5ForceReload->value

      eqFilePath = _IMFgetIncludeFile(rtDpl->topCv rtDpl ".il" debug)
      unless(eqFilePath return())

      ;; Get results
      erv = errset(_IMFparseBuildEvalEqs(eqFilePath inputDpl reloadEqs debug))
      if(erv then
         if(erv == list(nil) then
            printf("VALE ERROR: Failed to calculate results\n")
         else
            results = car(erv)
            when(debug
               printf("VALE DEBUG: Finished building equations\n")
            )
         )
      else
         printf("VALE ERROR: A problem occurred while calculating results\n")
         printf("%L\n" errset.errset)
         return()
      )

      ;; Update UI
      formattedResults = nil
      foreach(layer list("M1" "V1" "M2" "V2" "M3" "V3")
         when(results[layer]
            when(debug
               printf("VALE DEBUG: data for %L is %L\n" layer results[layer])
            )
            when(results[layer] == 0
               results[layer] = list(nil 'value1 "n/a" 'value2 "n/a"
                 'layer layer)
            )
            if(rexMatchp("^M" layer) then
               when(results[layer]->value1 != "n/a"
                  results[layer]->value1 = 
                     aelSuffixNotation(1e-6*atof(results[layer]->value1))
               )
               when(results[layer]->value2 != "n/a"
                  results[layer]->value2 = 
                     aelSuffixNotation(1e-3*atof(results[layer]->value2))
               )
            )
            currentResult =
               list(layer results[layer]->value1 results[layer]->value2)
            formattedResults = append1(formattedResults currentResult)
         )
      )
      when(debug
         printf("VALE DEBUG: %L\n" formattedResults)
      )
         
      form->compMod5Report->choices = formattedResults 

      return(t)
   )
)

procedure(_IMFwireToolTypeCB(form rtDpl @optional (debug nil))
   let(()
       
         printf("VALE INFO: Updating form layout for %s\n"
            form->compMod5Type->value)
      ;; Add table structure here for each analysis type
      if(form->compMod5Type->value == "Idc width, Irms limit" then
         form->compMod5Report->headers = list(
            list("Layer" 50 'left 'string nil nil nil)
            list("Min Width/Min Via Count" 140 'center 'string nil nil nil)
            list("Irms limit" 80 'center 'string nil nil nil)
         )
         form->compMod5Report->choices = list(
            list("M1" "0.0" "0.0")
            list("V1" "0" "n/a")
            list("M2" "0.0" "0.0")
            list("V2" "0" "n/a")
            list("M3" "0.0" "0.0")
            list("V3" "0" "n/a")
         )
      else
         form->compMod5Report->headers = list(
            list("Layer" 50 'left 'string nil nil nil)
            list("Min Width/Min Via Count" 220 'center 'string nil nil nil)
            list("Irms" 0 'center 'string nil nil nil)
         )
         form->compMod5Report->choices = list(
            list("M1" "0.0" "n/a")
            list("V1" "0" "n/a")
            list("M2" "0.0" "n/a")
            list("V2" "0" "n/a")
            list("M3" "0.0" "n/a")
            list("V3" "0" "n/a")
         )
      )
   )
)

procedure(_IMFwireToolResetCB(form @optional (debug nil))
   let(()
      ;; Add table structure here for each analysis type
      if(form->compMod5Type->value == "Idc width, Irms limit" then
         form->compMod5Report->headers = list(
            list("Layer" 50 'left 'string nil nil nil)
            list("Min Width/Min Via Count" 140 'center 'string nil nil nil)
            list("Irms limit" 80 'center 'string nil nil nil)
         )
         form->compMod5Report->choices = list(
            list("M1" "0.0" "0.0")
            list("V1" "0" "n/a")
            list("M2" "0.0" "0.0")
            list("V2" "0" "n/a")
            list("M3" "0.0" "0.0")
            list("V3" "0" "n/a")
         )
      else
         form->compMod5Report->headers = list(
            list("Layer" 50 'left 'string nil nil nil)
            list("Min Width/Min Via Count" 220 'center 'string nil nil nil)
            list("Irms limit" 0 'center 'string nil nil nil)
         )
         form->compMod5Report->choices = list(
            list("M1" "0.0" "n/a")
            list("V1" "0" "n/a")
            list("M2" "0.0" "n/a")
            list("V2" "0" "n/a")
            list("M3" "0.0" "n/a")
            list("V3" "0" "n/a")
         )
      )
   )
)

procedure(_IMFdisplayNum(val)
   prog((val1b val1c val1d)
      val1b = aelEngNotation(val)
      sprintf(val1c "%4.6s" val1b)
      val1d = aelSuffixNotation(val1c)
      return(val1d)
   )
)
