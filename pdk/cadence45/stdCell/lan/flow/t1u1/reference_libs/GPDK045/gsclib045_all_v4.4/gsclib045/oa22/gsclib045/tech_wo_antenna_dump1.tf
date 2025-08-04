; Technology File gsclib045
; Generated on Aug  3 10:07:34 2010
;     with @(#)$CDS: virtuoso version 6.1.4 05/20/2010 23:55 (sjfnl005) $


;********************************
; CONTROLS
;********************************
controls(

 refTechLibs(
; techLibName            
; -----------            
  "gpdk045" 
 ) ;refTechLibs

) ;controls


;********************************
; LAYER DEFINITION
;********************************
layerDefinitions(

) ;layerDefinitions


;********************************
; VIADEFS
;********************************
viaDefs(

 customViaDefs(
 ;( viaDefName libName cellName viewName layer1 layer2 resistancePerCut)
 ;( ---------- ------- -------- -------- ------ ------ ----------------)
  ( M2_M1_HV   gsclib045  M2_M1_HV   via        Metal1     Metal2     0.0)
  ( M2_M1_VV   gsclib045  M2_M1_VV   via        Metal1     Metal2     0.0)
  ( M2_M1_VH   gsclib045  M2_M1_VH   via        Metal1     Metal2     0.0)
  ( M2_M1_HH   gsclib045  M2_M1_HH   via        Metal1     Metal2     0.0)
   ( M2_M1_2x1_HV_E  gsclib045 M2_M1_2x1_HV_E via Metal1 Metal2 0.0)
   ( M2_M1_2x1_HV_W  gsclib045 M2_M1_2x1_HV_W via Metal1 Metal2 0.0)
   ( M2_M1_1x2_HV_N  gsclib045 M2_M1_1x2_HV_N via Metal1 Metal2 0.0)
   ( M2_M1_1x2_HV_S  gsclib045 M2_M1_1x2_HV_S via Metal1 Metal2 0.0)
   ( M3_M2_VH        gsclib045 M3_M2_VH       via Metal2 Metal3 0.0)
   ( M3_M2_HH        gsclib045 M3_M2_HH       via Metal2 Metal3 0.0)
   ( M3_M2_HV        gsclib045 M3_M2_HV       via Metal2 Metal3 0.0)
   ( M3_M2_VV        gsclib045 M3_M2_VV       via Metal2 Metal3 0.0)
   ( M3_M2_M_NH      gsclib045 M3_M2_M_NH     via Metal2 Metal3 0.0)
   ( M3_M2_M_SH      gsclib045 M3_M2_M_SH     via Metal2 Metal3 0.0)
   ( M3_M2_2x1_VH_E  gsclib045 M3_M2_2x1_VH_E via Metal2 Metal3 0.0)
   ( M3_M2_2x1_VH_W  gsclib045 M3_M2_2x1_VH_W via Metal2 Metal3 0.0)
   ( M3_M2_1x2_VH_N  gsclib045 M3_M2_1x2_VH_N via Metal2 Metal3 0.0)
   ( M3_M2_1x2_VH_S  gsclib045 M3_M2_1x2_VH_S via Metal2 Metal3 0.0)
   ( M4_M3_HV        gsclib045 M4_M3_HV       via Metal3 Metal4 0.0)
   ( M4_M3_VV        gsclib045 M4_M3_VV       via Metal3 Metal4 0.0)
   ( M4_M3_VH        gsclib045 M4_M3_VH       via Metal3 Metal4 0.0)
   ( M4_M3_HH        gsclib045 M4_M3_HH       via Metal3 Metal4 0.0)
   ( M4_M3_M_EV      gsclib045 M4_M3_M_EV     via Metal3 Metal4 0.0)
   ( M4_M3_M_WV      gsclib045 M4_M3_M_WV     via Metal3 Metal4 0.0)
   ( M4_M3_2x1_HV_E  gsclib045 M4_M3_2x1_HV_E via Metal3 Metal4 0.0)
   ( M4_M3_2x1_HV_W  gsclib045 M4_M3_2x1_HV_W via Metal3 Metal4 0.0)
   ( M4_M3_1x2_HV_N  gsclib045 M4_M3_1x2_HV_N via Metal3 Metal4 0.0)
   ( M4_M3_1x2_HV_S  gsclib045 M4_M3_1x2_HV_S via Metal3 Metal4 0.0)
   ( M5_M4_VH        gsclib045 M5_M4_VH       via Metal4 Metal5 0.0)
   ( M5_M4_HH        gsclib045 M5_M4_HH       via Metal4 Metal5 0.0)
   ( M5_M4_HV        gsclib045 M5_M4_HV       via Metal4 Metal5 0.0)
   ( M5_M4_VV        gsclib045 M5_M4_VV       via Metal4 Metal5 0.0)
   ( M5_M4_M_NH      gsclib045 M5_M4_M_NH     via Metal4 Metal5 0.0)
   ( M5_M4_M_SH      gsclib045 M5_M4_M_SH     via Metal4 Metal5 0.0)
   ( M5_M4_2x1_VH_E  gsclib045 M5_M4_2x1_VH_E via Metal4 Metal5 0.0)
   ( M5_M4_2x1_VH_W  gsclib045 M5_M4_2x1_VH_W via Metal4 Metal5 0.0)
   ( M5_M4_1x2_VH_N  gsclib045 M5_M4_1x2_VH_N via Metal4 Metal5 0.0)
   ( M5_M4_1x2_VH_S  gsclib045 M5_M4_1x2_VH_S via Metal4 Metal5 0.0)
   ( M6_M5_HV        gsclib045 M6_M5_HV       via Metal5 Metal6 0.0)
   ( M6_M5_VV        gsclib045 M6_M5_VV       via Metal5 Metal6 0.0)
   ( M6_M5_VH        gsclib045 M6_M5_VH       via Metal5 Metal6 0.0)
   ( M6_M5_HH        gsclib045 M6_M5_HH       via Metal5 Metal6 0.0)
   ( M6_M5_M_EV      gsclib045 M6_M5_M_EV     via Metal5 Metal6 0.0)
   ( M6_M5_M_WV      gsclib045 M6_M5_M_WV     via Metal5 Metal6 0.0)
   ( M6_M5_2x1_HV_E  gsclib045 M6_M5_2x1_HV_E via Metal5 Metal6 0.0)
   ( M6_M5_2x1_HV_W  gsclib045 M6_M5_2x1_HV_W via Metal5 Metal6 0.0)
   ( M6_M5_1x2_HV_N  gsclib045 M6_M5_1x2_HV_N via Metal5 Metal6 0.0)
   ( M6_M5_1x2_HV_S  gsclib045 M6_M5_1x2_HV_S via Metal5 Metal6 0.0)
   ( M7_M6_VH        gsclib045 M7_M6_VH       via Metal6 Metal7 0.0)
   ( M7_M6_HH        gsclib045 M7_M6_HH       via Metal6 Metal7 0.0)
   ( M7_M6_HV        gsclib045 M7_M6_HV       via Metal6 Metal7 0.0)
   ( M7_M6_VV        gsclib045 M7_M6_VV       via Metal6 Metal7 0.0)
   ( M7_M6_M_NH      gsclib045 M7_M6_M_NH     via Metal6 Metal7 0.0)
   ( M7_M6_M_SH      gsclib045 M7_M6_M_SH     via Metal6 Metal7 0.0)
   ( M7_M6_2x1_VH_E  gsclib045 M7_M6_2x1_VH_E via Metal6 Metal7 0.0)
   ( M7_M6_2x1_VH_W  gsclib045 M7_M6_2x1_VH_W via Metal6 Metal7 0.0)
   ( M7_M6_1x2_VH_N  gsclib045 M7_M6_1x2_VH_N via Metal6 Metal7 0.0)
   ( M7_M6_1x2_VH_S  gsclib045 M7_M6_1x2_VH_S via Metal6 Metal7 0.0)
   ( M8_M7_HV        gsclib045 M8_M7_HV       via Metal7 Metal8 0.0)
   ( M8_M7_VV        gsclib045 M8_M7_VV       via Metal7 Metal8 0.0)
   ( M8_M7_VH        gsclib045 M8_M7_VH       via Metal7 Metal8 0.0)
   ( M8_M7_HH        gsclib045 M8_M7_HH       via Metal7 Metal8 0.0)
   ( M8_M7_M_EV      gsclib045 M8_M7_M_EV     via Metal7 Metal8 0.0)
   ( M8_M7_M_WV      gsclib045 M8_M7_M_WV     via Metal7 Metal8 0.0)
   ( M8_M7_2x1_HV_E  gsclib045 M8_M7_2x1_HV_E via Metal7 Metal8 0.0)
   ( M8_M7_2x1_HV_W  gsclib045 M8_M7_2x1_HV_W via Metal7 Metal8 0.0)
   ( M8_M7_1x2_HV_N  gsclib045 M8_M7_1x2_HV_N via Metal7 Metal8 0.0)
   ( M8_M7_1x2_HV_S  gsclib045 M8_M7_1x2_HV_S via Metal7 Metal8 0.0)
   ( M9_M8_VH        gsclib045 M9_M8_VH       via Metal8 Metal9 0.0)
   ( M9_M8_HH        gsclib045 M9_M8_HH       via Metal8 Metal9 0.0)
   ( M9_M8_HV        gsclib045 M9_M8_HV       via Metal8 Metal9 0.0)
   ( M9_M8_VV        gsclib045 M9_M8_VV       via Metal8 Metal9 0.0)
   ( M9_M8_M_NH      gsclib045 M9_M8_M_NH     via Metal8 Metal9 0.0)
   ( M9_M8_M_SH      gsclib045 M9_M8_M_SH     via Metal8 Metal9 0.0)
   ( M9_M8_2x1_VH_E  gsclib045 M9_M8_2x1_VH_E via Metal8 Metal9 0.0)
   ( M9_M8_2x1_VH_W  gsclib045 M9_M8_2x1_VH_W via Metal8 Metal9 0.0)
   ( M9_M8_1x2_VH_N  gsclib045 M9_M8_1x2_VH_N via Metal8 Metal9 0.0)
   ( M9_M8_1x2_VH_S  gsclib045 M9_M8_1x2_VH_S via Metal8 Metal9 0.0)
   ( M10_M9_HV       gsclib045 M10_M9_HV      via Metal9 Metal10 0.0)
   ( M10_M9_VV       gsclib045 M10_M9_VV      via Metal9 Metal10 0.0)
   ( M10_M9_VH       gsclib045 M10_M9_VH      via Metal9 Metal10 0.0)
   ( M10_M9_HH       gsclib045 M10_M9_HH      via Metal9 Metal10 0.0)
   ( M10_M9_2x1_HV_E  gsclib045 M10_M9_2x1_HV_E via Metal9 Metal10 0.0)
   ( M10_M9_2x1_HV_W  gsclib045 M10_M9_2x1_HV_W via Metal9 Metal10 0.0)
   ( M10_M9_1x2_HV_N  gsclib045 M10_M9_1x2_HV_N via Metal9 Metal10 0.0)
   ( M10_M9_1x2_HV_S  gsclib045 M10_M9_1x2_HV_S via Metal9 Metal10 0.0)
   ( M11_M10_VH       gsclib045 M11_M10_VH      via Metal10 Metal11 0.0)
   ( M11_M10_HH       gsclib045 M11_M10_HH      via Metal10 Metal11 0.0)
   ( M11_M10_HV       gsclib045 M11_M10_HV      via Metal10 Metal11 0.0)
   ( M11_M10_VV       gsclib045 M11_M10_VV      via Metal10 Metal11 0.0)
   ( M11_M10_M_NH  gsclib045 M11_M10_M_NH via Metal10 Metal11 0.0)
   ( M11_M10_M_SH  gsclib045 M11_M10_M_SH via Metal10 Metal11 0.0)
   ( M11_M10_2x1_VH_E  gsclib045 M11_M10_2x1_VH_E via Metal10 Metal11 0.0)
   ( M11_M10_2x1_VH_W  gsclib045 M11_M10_2x1_VH_W via Metal10 Metal11 0.0)
   ( M11_M10_1x2_VH_N  gsclib045 M11_M10_1x2_VH_N via Metal10 Metal11 0.0)
   ( M11_M10_1x2_VH_S  gsclib045 M11_M10_1x2_VH_S via Metal10 Metal11 0.0)
 ) ;customViaDefs

) ;viaDefs



;********************************
; CONSTRAINT GROUPS
;********************************
constraintGroups(

 ;( group	[override] )
 ;( -----	---------- )
  ( "LEFSpecialRouteSpec"	nil    "LEFSpecialRouteSpec"

    interconnect(
     ( validVias     (M2_M1  M3_M2  M4_M3  M5_M4  M6_M5  M7_M6  M8_M7  M9_M8  M10_M9  M11_M10  M2_M1_HV  M2_M1_VV  M2_M1_VH  M2_M1_HH  M2_M1_2x1_HV_E  M2_M1_2x1_HV_W  M2_M1_1x2_HV_N  M2_M1_1x2_HV_S  M3_M2_VH  M3_M2_HH  M3_M2_HV  M3_M2_VV  M3_M2_M_NH  M3_M2_M_SH  M3_M2_2x1_VH_E  M3_M2_2x1_VH_W  M3_M2_1x2_VH_N  M3_M2_1x2_VH_S  M4_M3_HV  M4_M3_VV  M4_M3_VH  M4_M3_HH  M4_M3_M_EV  M4_M3_M_WV  M4_M3_2x1_HV_E  M4_M3_2x1_HV_W  M4_M3_1x2_HV_N  M4_M3_1x2_HV_S  M5_M4_VH  M5_M4_HH  M5_M4_HV  M5_M4_VV  M5_M4_M_NH  M5_M4_M_SH  M5_M4_2x1_VH_E  M5_M4_2x1_VH_W  M5_M4_1x2_VH_N  M5_M4_1x2_VH_S  M6_M5_HV  M6_M5_VV  M6_M5_VH  M6_M5_HH  M6_M5_M_EV  M6_M5_M_WV  M6_M5_2x1_HV_E  M6_M5_2x1_HV_W  M6_M5_1x2_HV_N  M6_M5_1x2_HV_S  M7_M6_VH  M7_M6_HH  M7_M6_HV  M7_M6_VV  M7_M6_M_NH  M7_M6_M_SH  M7_M6_2x1_VH_E  M7_M6_2x1_VH_W  M7_M6_1x2_VH_N  M7_M6_1x2_VH_S  M8_M7_HV  M8_M7_VV  M8_M7_VH  M8_M7_HH  M8_M7_M_EV  M8_M7_M_WV  M8_M7_2x1_HV_E  M8_M7_2x1_HV_W  M8_M7_1x2_HV_N  M8_M7_1x2_HV_S  M9_M8_VH  M9_M8_HH  M9_M8_HV  M9_M8_VV  M9_M8_M_NH  M9_M8_M_SH  M9_M8_2x1_VH_E  M9_M8_2x1_VH_W  M9_M8_1x2_VH_N  M9_M8_1x2_VH_S  M10_M9_HV  M10_M9_VV  M10_M9_VH  M10_M9_HH  M10_M9_2x1_HV_E  M10_M9_2x1_HV_W  M10_M9_1x2_HV_N  M10_M9_1x2_HV_S  M11_M10_VH  M11_M10_HH  M11_M10_HV  M11_M10_VV  M11_M10_M_NH  M11_M10_M_SH  M11_M10_2x1_VH_E  M11_M10_2x1_VH_W  M11_M10_1x2_VH_N  M11_M10_1x2_VH_S  ) )
    ) ;interconnect
  ) ;LEFSpecialRouteSpec

 ;( group	[override] )
 ;( -----	---------- )
  ( "LEFDefaultRouteSpec"	nil    "LEFDefaultRouteSpec"

    spacings(
     ( minWidth                   "Cont"	0.06 )
    ) ;spacings

    routingGrids(
     ( horizontalPitch            "Metal1"   0.19 )
     ( verticalPitch              "Metal1"   0.19 )
     ( horizontalOffset           "Metal1"   0.095 )
     ( verticalOffset             "Metal1"   0.095 )
    ) ;routingGrids

    spacings(
     ( minWidth                   "Metal1"	0.06 )
     ( minWidth                   "Via1"	0.07 )
    ) ;spacings

    routingGrids(
     ( horizontalPitch            "Metal2"   0.2 )
     ( verticalPitch              "Metal2"   0.2 )
     ( horizontalOffset           "Metal2"   0.1 )
     ( verticalOffset             "Metal2"   0.1 )
    ) ;routingGrids

    spacings(
     ( minWidth                   "Metal2"	0.08 )
     ( minWidth                   "Via2"	0.07 )
    ) ;spacings

    routingGrids(
     ( horizontalPitch            "Metal3"   0.2 )
     ( verticalPitch              "Metal3"   0.2 )
     ( horizontalOffset           "Metal3"   0.1 )
     ( verticalOffset             "Metal3"   0.1 )
    ) ;routingGrids

    spacings(
     ( minWidth                   "Metal3"	0.08 )
     ( minWidth                   "Via3"	0.07 )
    ) ;spacings

    routingGrids(
     ( horizontalPitch            "Metal4"   0.2 )
     ( verticalPitch              "Metal4"   0.2 )
     ( horizontalOffset           "Metal4"   0.1 )
     ( verticalOffset             "Metal4"   0.1 )
    ) ;routingGrids

    spacings(
     ( minWidth                   "Metal4"	0.08 )
     ( minWidth                   "Via4"	0.07 )
    ) ;spacings

    routingGrids(
     ( horizontalPitch            "Metal5"   0.2 )
     ( verticalPitch              "Metal5"   0.2 )
     ( horizontalOffset           "Metal5"   0.1 )
     ( verticalOffset             "Metal5"   0.1 )
    ) ;routingGrids

    spacings(
     ( minWidth                   "Metal5"	0.08 )
     ( minWidth                   "Via5"	0.07 )
    ) ;spacings

    routingGrids(
     ( horizontalPitch            "Metal6"   0.2 )
     ( verticalPitch              "Metal6"   0.2 )
     ( horizontalOffset           "Metal6"   0.1 )
     ( verticalOffset             "Metal6"   0.1 )
    ) ;routingGrids

    spacings(
     ( minWidth                   "Metal6"	0.08 )
     ( minWidth                   "Via6"	0.07 )
    ) ;spacings

    routingGrids(
     ( horizontalPitch            "Metal7"   0.2 )
     ( verticalPitch              "Metal7"   0.2 )
     ( horizontalOffset           "Metal7"   0.1 )
     ( verticalOffset             "Metal7"   0.1 )
    ) ;routingGrids

    spacings(
     ( minWidth                   "Metal7"	0.08 )
     ( minWidth                   "Via7"	0.07 )
    ) ;spacings

    routingGrids(
     ( horizontalPitch            "Metal8"   0.2 )
     ( verticalPitch              "Metal8"   0.2 )
     ( horizontalOffset           "Metal8"   0.1 )
     ( verticalOffset             "Metal8"   0.1 )
    ) ;routingGrids

    spacings(
     ( minWidth                   "Metal8"	0.08 )
     ( minWidth                   "Via8"	0.07 )
    ) ;spacings

    routingGrids(
     ( horizontalPitch            "Metal9"   0.33 )
     ( verticalPitch              "Metal9"   0.33 )
     ( horizontalOffset           "Metal9"   0.165 )
     ( verticalOffset             "Metal9"   0.165 )
    ) ;routingGrids

    spacings(
     ( minWidth                   "Metal9"	0.08 )
     ( minWidth                   "Via9"	0.18 )
    ) ;spacings

    routingGrids(
     ( horizontalPitch            "Metal10"   0.48 )
     ( verticalPitch              "Metal10"   0.48 )
     ( horizontalOffset           "Metal10"   0.24 )
     ( verticalOffset             "Metal10"   0.24 )
    ) ;routingGrids

    spacings(
     ( minWidth                   "Metal10"	0.22 )
     ( minWidth                   "Via10"	0.18 )
    ) ;spacings

    routingGrids(
     ( horizontalPitch            "Metal11"   0.48 )
     ( verticalPitch              "Metal11"   0.48 )
     ( horizontalOffset           "Metal11"   0.24 )
     ( verticalOffset             "Metal11"   0.24 )
    ) ;routingGrids

    spacings(
     ( minWidth                   "Metal11"	0.22 )
    ) ;spacings

    interconnect(
     ( validLayers   (Metal1  Metal2  Metal3  Metal4  Metal5  Metal6  Metal7  Metal8  Metal9  Metal10  Metal11  ) )
     ( validVias     (M2_M1  M3_M2  M4_M3  M5_M4  M6_M5  M7_M6  M8_M7  M9_M8  M10_M9  M11_M10  M2_M1_HV  M2_M1_VV  M2_M1_VH  M2_M1_HH  M2_M1_2x1_HV_E  M2_M1_2x1_HV_W  M2_M1_1x2_HV_N  M2_M1_1x2_HV_S  M3_M2_VH  M3_M2_HH  M3_M2_HV  M3_M2_VV  M3_M2_M_NH  M3_M2_M_SH  M3_M2_2x1_VH_E  M3_M2_2x1_VH_W  M3_M2_1x2_VH_N  M3_M2_1x2_VH_S  M4_M3_HV  M4_M3_VV  M4_M3_VH  M4_M3_HH  M4_M3_M_EV  M4_M3_M_WV  M4_M3_2x1_HV_E  M4_M3_2x1_HV_W  M4_M3_1x2_HV_N  M4_M3_1x2_HV_S  M5_M4_VH  M5_M4_HH  M5_M4_HV  M5_M4_VV  M5_M4_M_NH  M5_M4_M_SH  M5_M4_2x1_VH_E  M5_M4_2x1_VH_W  M5_M4_1x2_VH_N  M5_M4_1x2_VH_S  M6_M5_HV  M6_M5_VV  M6_M5_VH  M6_M5_HH  M6_M5_M_EV  M6_M5_M_WV  M6_M5_2x1_HV_E  M6_M5_2x1_HV_W  M6_M5_1x2_HV_N  M6_M5_1x2_HV_S  M7_M6_VH  M7_M6_HH  M7_M6_HV  M7_M6_VV  M7_M6_M_NH  M7_M6_M_SH  M7_M6_2x1_VH_E  M7_M6_2x1_VH_W  M7_M6_1x2_VH_N  M7_M6_1x2_VH_S  M8_M7_HV  M8_M7_VV  M8_M7_VH  M8_M7_HH  M8_M7_M_EV  M8_M7_M_WV  M8_M7_2x1_HV_E  M8_M7_2x1_HV_W  M8_M7_1x2_HV_N  M8_M7_1x2_HV_S  M9_M8_VH  M9_M8_HH  M9_M8_HV  M9_M8_VV  M9_M8_M_NH  M9_M8_M_SH  M9_M8_2x1_VH_E  M9_M8_2x1_VH_W  M9_M8_1x2_VH_N  M9_M8_1x2_VH_S  M10_M9_HV  M10_M9_VV  M10_M9_VH  M10_M9_HH  M10_M9_2x1_HV_E  M10_M9_2x1_HV_W  M10_M9_1x2_HV_N  M10_M9_1x2_HV_S  M11_M10_VH  M11_M10_HH  M11_M10_HV  M11_M10_VV  M11_M10_M_NH  M11_M10_M_SH  M11_M10_2x1_VH_E  M11_M10_2x1_VH_W  M11_M10_1x2_VH_N  M11_M10_1x2_VH_S  ) )
    ) ;interconnect
  ) ;LEFDefaultRouteSpec
) ;constraintGroups


;********************************
; SITEDEFS
;********************************
siteDefs(

 scalarSiteDefs(
 ;( siteDefName          type width  height  symInX symInY symInR90)
 ;( -----------          ---- -----  ------  ------ ------ -------)
  ( CoreSite             core 0.2  1.71  nil nil nil)
 ) ;scalarSiteDefs

) ;siteDefs
