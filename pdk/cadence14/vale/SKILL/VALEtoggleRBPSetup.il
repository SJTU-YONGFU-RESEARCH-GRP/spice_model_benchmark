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
   2019-04-05 VA Initial Coding for toggling the RBP setup variables
   2019-05-17 JF Syntax and organization updates
*/

procedure(VALEtoggleRBPSetup(cv)
   prog((tf cg viaopts tlist)
      tf = techGetTechFile(cv)
      cg = cstFindConstraintGroupIn(tf "virtuosoDefaultSetup")
      viaopts = viaGetViaOptions(cg)
      tlist = car(viaFindTransitions(viaopts~>constraintGroupSetup "M2" "M1"))
      
      if(_IMFdat->toggleRBP == nil then
         _IMFdat->toggleRBP = t 
         printf("VALE INFO: Enabling row-based placement and WSP-aware ")
         printf(" Virtuoso environment variables\n")

         printf("VALE INFO: Setting Cut Class \"Default\" for ")
         printf("V1 V2 V3\n")
         viaSetDefaultCutClasses(_IMFdat->techLib "virtuosoDefaultSetup"
            list(
               list("M1" "M2" "Default")
               list("M2" "M3" "Default")
               list("M3" "M4" "Default")
            )
         )
         envSetVal("layout" "viaCutClassInAuto" 'string "Default")

         printf("VALE INFO: Setting Virtuoso environment variables ")
         printf("weAutoDropViaForOverlaps to simplify wiring connections ")
         printf("with Create Wire\n")
         envSetVal("layout" "weAutoDropViaForOverlaps" 'boolean t)

         printf("VALE INFO: Setting wire snapping to snap (snapWireGrid) to ")
         printf("snap pattern\n")
         envSetVal("layout" "snapWireGrid" 'cyclic "Snap Pattern")

         printf("VALE INFO: Setting Virtuoso environment variables for ")
         printf("Gen from Source form defaults and Poly WSP inst snapping\n")
         envSetVal("layoutXL.APAssist" "WSPAware" 'boolean t)
         envSetVal("layoutXL.placement" "vcpCellBoundaryLPPs" 
            'string "(Active drawing)")
         envSetVal("layoutXL" "lxGenerateInBoundary" 'boolean nil)
         envSetVal("layoutXL" "lxGenerateInBoundary" 'boolean nil)
         envSetVal("layoutXL" "initCreatePins" 'boolean nil)
         envSetVal("layoutXL" "initEstimateArea" 'boolean t)
         envSetVal("layoutXL" "initCreateSnapBoundary" 'boolean nil)
         envSetVal("layoutXL" "initCreateBoundary" 'boolean t)
         envSetVal("layoutXL" "initDoFolding" 'boolean nil)
         envSetVal("layoutXL" "initDoStacking" 'boolean nil)
         envSetVal("layoutXL" "initCreateMTM" 'boolean nil)
         envSetVal("layoutXL" "initAspectRatioOption" 'string "Height")
         envSetVal("layoutXL" "initAspectRatio" 'float 1)
         envSetVal("layoutXL" "initPrBoundaryH" 'float 1)
         envSetVal("layoutXL" "initUtilization" 'float 35.0)
         envSetVal("layout" "snapPatternDrawingStyle" 'cyclic "tracks")
         hiGetCurrentWindow()~>snapPatternDrawingStyle = "tracks"

         ;; In ICADVM18.1 vsrLoadPreset has a path option
         ;vsrLoadPreset("via_default" 
         ;   ?path strcat(getShellEnvVar("CDS_MVS_IMF_CM") "/Include/"))
         foreach(viaform 
            setof(form hiFormList() rexMatchp("le[0-9]+ViaForm" form))
            eval(viaform)~>globalCutClassAuto~>value = "Default"
         )
      else
         _IMFdat->toggleRBP = nil
         printf("VALE INFO: Turning off RBP and WSPaware variables\n")

         printf("VALE INFO: Resetting Via Cut Classes to Auto.\n")
         viaSetDefaultCutClasses(_IMFdat->techLib "virtuosoDefaultSetup"
            list())
         envSetVal("layout" "viaCutClassInAuto" 'string "Auto")

         envSetVal("layout" "weAutoDropViaForOverlaps" 'boolean nil)

         printf("VALE INFO: Resetting wire snapping to manufacturing grid.\n")
         envSetVal("layout" "snapWireGrid" 'cyclic "Manufacturing Grid")

         printf("VALE INFO: Resetting placement variables\n")
         envSetVal("layoutXL.APAssist" "WSPAware" 'boolean nil)
         envSetVal("layoutXL.placement" "vcpCellBoundaryLPPs" 'string "")
         envSetVal("layoutXL" "lxGenerateInBoundary" 'boolean t) 
         foreach(viaform
            setof(form hiFormList() rexMatchp("le[0-9]+ViaForm" form))
            eval(viaform)~>globalCutClassAuto~>value = "Auto"
         )
      )

      return(t)
   )
)

