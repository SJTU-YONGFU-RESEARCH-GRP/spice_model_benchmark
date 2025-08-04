; Technology File wsp_cds_ff_mpt
; Generated on Feb 21 14:29:29 2019
;     with @(#)$CDS: virtuoso version ICADV12.3-64b 12/16/2018 07:18 (sjfhw317) $


;********************************
; CONTROLS
;********************************
controls(
 techVersion("1.0")

 refTechLibs(
; techLibName            
; -----------            
  "cds_ff_mpt" 
 ) ;refTechLibs

 processFamily(
      "cds_ff_mpt"
 ) ;processFamily

) ;controls


;********************************
; LAYER DEFINITION
;********************************
layerDefinitions(

 techLayerPurposePriorities(
 ;layers are ordered from lowest to highest priority
 ;( LayerName                 Purpose    )
 ;( ---------                 -------    )
  ( BuriedNWell               drawing    )
  ( NWell                     drawing    )
  ( NWell                     net        )
  ( NWell                     boundary   )
  ( ThickOx                   drawing    )
  ( Active                    drawing    )
  ( Active                    net        )
  ( Active                    boundary   )
  ( Active                    fin        )
  ( Active                    SADPEnds   )
  ( Active                    dummy      )
  ( CutActive                 drawing    )
  ( TrimFin                   drawing    )
  ( CellBoundary              global     )
  ( FinArea                   fin48      )
  ( Psvt                      drawing    )
  ( Psvt                      net        )
  ( Psvt                      boundary   )
  ( Plvt                      drawing    )
  ( Plvt                      net        )
  ( Plvt                      boundary   )
  ( Phvt                      drawing    )
  ( Phvt                      net        )
  ( Phvt                      boundary   )
  ( Nsvt                      drawing    )
  ( Nsvt                      net        )
  ( Nsvt                      boundary   )
  ( Nlvt                      drawing    )
  ( Nlvt                      net        )
  ( Nlvt                      boundary   )
  ( Nhvt                      drawing    )
  ( Nhvt                      net        )
  ( Nhvt                      boundary   )
  ( CutPoly                   drawing    )
  ( Poly                      drawing    )
  ( Poly                      net        )
  ( Poly                      boundary   )
  ( Poly                      dummy      )
  ( Poly                      edge       )
  ( PPitch                    poly86     )
  ( PPitch                    poly90     )
  ( PPitch                    poly94     )
  ( PPitch                    poly102    )
  ( PPitch                    poly104    )
  ( M1                        localWSP   )
  ( M2                        localWSP   )
  ( M3                        localWSP   )
  ( M4                        localWSP   )
  ( M5                        localWSP   )
  ( SaB                       drawing    )
  ( LiPo                      drawing    )
  ( LiPo                      track      )
  ( LiPo                      net        )
  ( LiPo                      boundary   )
  ( LiPo                      grid       )
  ( LiPo                      blockage   )
  ( LiAct                     drawing    )
  ( LiAct                     track      )
  ( LiAct                     net        )
  ( LiAct                     boundary   )
  ( LiAct                     grid       )
  ( LiAct                     blockage   )
  ( V0                        drawing    )
  ( V0                        net        )
  ( V0                        boundary   )
  ( V0                        grid       )
  ( V0                        blockage   )
  ( V0                        fill       )
  ( M1                        drawing    )
  ( M1                        net        )
  ( M1                        boundary   )
  ( M1                        track      )
  ( M1                        pin        )
  ( M1                        grid       )
  ( M1                        blockage   )
  ( M1                        fill       )
  ( M1                        gapFill    )
  ( M1                        exclude    )
  ( M1                        critexcl   )
  ( M1                        vdd1p8     )
  ( CutM1                     drawing    )
  ( V1                        drawing    )
  ( V1                        net        )
  ( V1                        boundary   )
  ( V1                        grid       )
  ( V1                        blockage   )
  ( V1                        fill       )
  ( M2                        drawing    )
  ( M2                        net        )
  ( M2                        boundary   )
  ( M2                        track      )
  ( M2                        pin        )
  ( M2                        grid       )
  ( M2                        blockage   )
  ( M2                        fill       )
  ( M2                        gapFill    )
  ( M2                        exclude    )
  ( M2                        critexcl   )
  ( M2                        vdd1p8     )
  ( CutM2                     drawing    )
  ( V2                        drawing    )
  ( V2                        net        )
  ( V2                        boundary   )
  ( V2                        grid       )
  ( V2                        blockage   )
  ( V2                        fill       )
  ( M3                        drawing    )
  ( M3                        net        )
  ( M3                        boundary   )
  ( M3                        track      )
  ( M3                        pin        )
  ( M3                        grid       )
  ( M3                        blockage   )
  ( M3                        fill       )
  ( M3                        gapFill    )
  ( M3                        exclude    )
  ( M3                        critexcl   )
  ( M3                        vdd1p8     )
  ( CutM3                     drawing    )
  ( V3                        drawing    )
  ( V3                        net        )
  ( V3                        boundary   )
  ( V3                        grid       )
  ( V3                        blockage   )
  ( V3                        fill       )
  ( M4                        drawing    )
  ( M4                        net        )
  ( M4                        boundary   )
  ( M4                        track      )
  ( M4                        pin        )
  ( M4                        grid       )
  ( M4                        blockage   )
  ( M4                        fill       )
  ( M4                        gapFill    )
  ( M4                        exclude    )
  ( M4                        critexcl   )
  ( M4                        vdd1p8     )
  ( V4                        drawing    )
  ( V4                        net        )
  ( V4                        boundary   )
  ( V4                        grid       )
  ( V4                        fill       )
  ( V4                        blockage   )
  ( M5                        drawing    )
  ( M5                        net        )
  ( M5                        boundary   )
  ( M5                        track      )
  ( M5                        pin        )
  ( M5                        grid       )
  ( M5                        blockage   )
  ( M5                        fill       )
  ( M5                        gapFill    )
  ( M5                        exclude    )
  ( M5                        critexcl   )
  ( M5                        vdd1p8     )
  ( V5                        drawing    )
  ( V5                        net        )
  ( V5                        boundary   )
  ( V5                        grid       )
  ( V5                        fill       )
  ( V5                        blockage   )
  ( M6                        drawing    )
  ( M6                        net        )
  ( M6                        boundary   )
  ( M6                        track      )
  ( M6                        pin        )
  ( M6                        grid       )
  ( M6                        blockage   )
  ( M6                        fill       )
  ( M6                        gapFill    )
  ( M6                        exclude    )
  ( M6                        critexcl   )
  ( M6                        vdd1p8     )
  ( V6                        drawing    )
  ( V6                        net        )
  ( V6                        boundary   )
  ( V6                        grid       )
  ( V6                        fill       )
  ( V6                        blockage   )
  ( M7                        drawing    )
  ( M7                        net        )
  ( M7                        boundary   )
  ( M7                        track      )
  ( M7                        pin        )
  ( M7                        grid       )
  ( M7                        blockage   )
  ( M7                        fill       )
  ( M7                        gapFill    )
  ( M7                        exclude    )
  ( M7                        critexcl   )
  ( M7                        vdd1p8     )
  ( CMT                       drawing    )
  ( CMT                       grid       )
  ( CMT                       blockage   )
  ( VT                        drawing    )
  ( VT                        net        )
  ( VT                        boundary   )
  ( VT                        grid       )
  ( VT                        fill       )
  ( VT                        blockage   )
  ( MT                        drawing    )
  ( MT                        net        )
  ( MT                        boundary   )
  ( MT                        track      )
  ( MT                        pin        )
  ( MT                        grid       )
  ( MT                        blockage   )
  ( MT                        fill       )
  ( MT                        gapFill    )
  ( MT                        exclude    )
  ( MT                        critexcl   )
  ( MT                        vdd1p8     )
  ( m1res                     drawing    )
  ( m2res                     drawing    )
  ( m3res                     drawing    )
  ( m4res                     drawing    )
  ( m5res                     drawing    )
  ( m6res                     drawing    )
  ( m7res                     drawing    )
  ( mtres                     drawing    )
  ( nwstires                  drawing    )
  ( nwodres                   drawing    )
  ( diffres                   drawing    )
  ( pcres                     drawing    )
  ( diodmy                    drawing    )
  ( NPNdummy                  drawing    )
  ( mimW                      drawing    )
  ( mimL                      drawing    )
  ( text                      drawing    )
 ) ;techLayerPurposePriorities

 techDisplays(
 ;( LayerName    Purpose      Packet          Vis Sel Con2ChgLy DrgEnbl Valid )
 ;( ---------    -------      ------          --- --- --------- ------- ----- )
  ( BuriedNWell  drawing      DNWELLD          t t t t t )
  ( NWell        drawing      nwell            t t t t t )
  ( NWell        net          nwell_net        t t t nil nil )
  ( NWell        boundary     nwell_boundary   t t t nil nil )
  ( ThickOx      drawing      thox             t t t t t )
  ( Active       drawing      active           t t t t t )
  ( Active       net          Oxide_net        t t t nil nil )
  ( Active       boundary     Oxide_boundary   t t t nil nil )
  ( Active       fin          fin              nil nil nil nil nil )
  ( Active       SADPEnds     SADPEnds         nil nil nil nil nil )
  ( Active       dummy        active           t t t t t )
  ( CutActive    drawing      cutActive        t t t t t )
  ( TrimFin      drawing      cutFin           nil nil nil nil nil )
  ( CellBoundary global       GFG              t t t t t )
  ( FinArea      fin48        FB               t t t t t )
  ( Psvt         drawing      PP               t t t t t )
  ( Psvt         net          pplus_net        t t t nil nil )
  ( Psvt         boundary     Pimp_boundary    t t t nil nil )
  ( Plvt         drawing      plvt             t t t t t )
  ( Plvt         net          plvt_net         t t t nil nil )
  ( Plvt         boundary     plvt_boundary    t t t nil nil )
  ( Phvt         drawing      phvt             t t t t t )
  ( Phvt         net          phvt_net         t t t nil nil )
  ( Phvt         boundary     phvt_boundary    t t t nil nil )
  ( Nsvt         drawing      NP               t t t t t )
  ( Nsvt         net          nplus_net        t t t nil nil )
  ( Nsvt         boundary     Nimp_boundary    t t t nil nil )
  ( Nlvt         drawing      nlvt             t t t t t )
  ( Nlvt         net          nlvt_net         t t t nil nil )
  ( Nlvt         boundary     nlvt_boundary    t t t nil nil )
  ( Nhvt         drawing      nhvt             t t t t t )
  ( Nhvt         net          nhvt_net         t t t nil nil )
  ( Nhvt         boundary     nhvt_boundary    t t t nil nil )
  ( CutPoly      drawing      cutPoly          t t t t t )
  ( Poly         drawing      poly             t t t t t )
  ( Poly         net          Poly_net         t t t nil nil )
  ( Poly         boundary     Poly_boundary    t t t nil nil )
  ( Poly         dummy        polyDummy        t t t t t )
  ( Poly         edge         polyEdge         t t t t t )
  ( PPitch       poly86       CPP              t t t t t )
  ( PPitch       poly90       CPP              t t t t t )
  ( PPitch       poly94       CPP              t t t t t )
  ( PPitch       poly102      CPP              t t t t t )
  ( PPitch       poly104      CPP              t t t t t )
  ( M1           localWSP     m1WSP            t t nil t t )
  ( M2           localWSP     m2WSP            t t nil t t )
  ( M3           localWSP     m3WSP            t t nil t t )
  ( M4           localWSP     m4WSP            t t nil t t )
  ( M5           localWSP     m5WSP            t t nil t t )
  ( SaB          drawing      sab              t t t t t )
  ( LiPo         drawing      lipo             t t t t t )
  ( LiPo         track        lipo             nil nil t t nil )
  ( LiPo         net          lipo_net         t t t nil nil )
  ( LiPo         boundary     lipo_boundary    t t t nil nil )
  ( LiPo         grid         lipo             t nil nil nil nil )
  ( LiPo         blockage     lipo             t nil t t nil )
  ( LiAct        drawing      liact            t t t t t )
  ( LiAct        track        liact            nil nil t t nil )
  ( LiAct        net          liact_net        t t t nil nil )
  ( LiAct        boundary     liact_boundary   t t t nil nil )
  ( LiAct        grid         liact            t nil nil nil nil )
  ( LiAct        blockage     liact            t nil t t nil )
  ( V0           drawing      v0               t t t t t )
  ( V0           net          v0_net           t t t nil nil )
  ( V0           boundary     v0_boundary      t t t nil nil )
  ( V0           grid         defaultPacket    t t t t t )
  ( V0           blockage     defaultPacket    t t t t t )
  ( V0           fill         defaultPacket    t t t t t )
  ( M1           drawing      m1               t t t t t )
  ( M1           net          m1_net           t t t nil nil )
  ( M1           boundary     m1_boundary      t t t nil nil )
  ( M1           track        m1               nil nil t t nil )
  ( M1           pin          m1               t t t t t )
  ( M1           grid         m1               t t nil t t )
  ( M1           blockage     m1               t t nil t t )
  ( M1           fill         m1               t t nil t t )
  ( M1           gapFill      m1               t t nil t t )
  ( M1           exclude      m1_exc           t t t t t )
  ( M1           critexcl     m1_crit          t t t t t )
  ( M1           vdd1p8       m1_1p8           t t t t t )
  ( CutM1        drawing      cutM1            t t t t t )
  ( V1           drawing      v1               t t t t t )
  ( V1           net          v1_net           t t t nil nil )
  ( V1           boundary     v1_boundary      t t t nil nil )
  ( V1           grid         defaultPacket    t t t t t )
  ( V1           blockage     v1               t t nil t t )
  ( V1           fill         v1               t t nil t t )
  ( M2           drawing      m2               t t t t t )
  ( M2           net          m2_net           t t t nil nil )
  ( M2           boundary     m2_boundary      t t t nil nil )
  ( M2           track        m2               nil nil t t nil )
  ( M2           pin          m2               t t t t t )
  ( M2           grid         m2               t t nil t t )
  ( M2           blockage     m2               t t nil t t )
  ( M2           fill         m2               t t nil t t )
  ( M2           gapFill      m2               t t nil t t )
  ( M2           exclude      m2_exc           t t t t t )
  ( M2           critexcl     m2_crit          t t t t t )
  ( M2           vdd1p8       m2_1p8           t t t t t )
  ( CutM2        drawing      cutM2            t t t t t )
  ( V2           drawing      v2               t t t t t )
  ( V2           net          v2_net           t t t nil nil )
  ( V2           boundary     v2_boundary      t t t nil nil )
  ( V2           grid         v2               t nil nil nil nil )
  ( V2           blockage     v2               t nil nil t nil )
  ( V2           fill         v2               t t nil t t )
  ( M3           drawing      m3               t t t t t )
  ( M3           net          m3_net           t t t nil nil )
  ( M3           boundary     m3_boundary      t t t nil nil )
  ( M3           track        m3               nil nil t t nil )
  ( M3           pin          m3               t t t t t )
  ( M3           grid         m3               t nil nil nil nil )
  ( M3           blockage     m3               t nil nil t nil )
  ( M3           fill         m3               t t nil t nil )
  ( M3           gapFill      m3               t t nil t t )
  ( M3           exclude      m3_exc           t t t t t )
  ( M3           critexcl     m3_crit          t t t t t )
  ( M3           vdd1p8       m3_1p8           t t t t t )
  ( CutM3        drawing      cutM3            t t t t t )
  ( V3           drawing      v3               t t t t t )
  ( V3           net          v3_net           t t t nil nil )
  ( V3           boundary     v3_boundary      t t t nil nil )
  ( V3           grid         v3               t nil nil nil nil )
  ( V3           blockage     v3               t nil nil t nil )
  ( V3           fill         v3               t t nil t t )
  ( M4           drawing      m4               t t t t t )
  ( M4           net          m4_net           t t t nil nil )
  ( M4           boundary     m4_boundary      t t t nil nil )
  ( M4           track        m4               nil nil t t nil )
  ( M4           pin          m4               t t t t t )
  ( M4           grid         m4               t nil nil nil nil )
  ( M4           blockage     m4               t nil nil t nil )
  ( M4           fill         m4               t t nil t nil )
  ( M4           gapFill      m4               t t nil t t )
  ( M4           exclude      m4_exc           t t t t t )
  ( M4           critexcl     m4_crit          t t t t t )
  ( M4           vdd1p8       m4_1p8           t t t t t )
  ( V4           drawing      v4               t t t t t )
  ( V4           net          v4_net           t t t nil nil )
  ( V4           boundary     v4_boundary      t t t nil nil )
  ( V4           grid         v4               t nil nil nil nil )
  ( V4           fill         defaultPacket    t t t t t )
  ( V4           blockage     v4               t nil nil t nil )
  ( M5           drawing      m5               t t t t t )
  ( M5           net          m5_net           t t t nil nil )
  ( M5           boundary     m5_boundary      t t t nil nil )
  ( M5           track        m5               nil nil t t nil )
  ( M5           pin          m5               t t t t t )
  ( M5           grid         m5               t nil nil nil nil )
  ( M5           blockage     m5               t nil nil t nil )
  ( M5           fill         m5               t t nil t nil )
  ( M5           gapFill      m5               t t nil t t )
  ( M5           exclude      m5_exc           t t t t t )
  ( M5           critexcl     m5_crit          t t t t t )
  ( M5           vdd1p8       m5_1p8           t t t t t )
  ( V5           drawing      v5               t t t t t )
  ( V5           net          v5_net           t t t nil nil )
  ( V5           boundary     v5_boundary      t t t nil nil )
  ( V5           grid         v5               t nil nil nil nil )
  ( V5           fill         v5               t t nil t nil )
  ( V5           blockage     v5               t nil nil t nil )
  ( M6           drawing      m6               t t t t t )
  ( M6           net          m6_net           t t t nil nil )
  ( M6           boundary     m6_boundary      t t t nil nil )
  ( M6           track        m6               nil nil t t nil )
  ( M6           pin          m6               t t t t t )
  ( M6           grid         m6               t nil nil nil nil )
  ( M6           blockage     m6               t nil nil t nil )
  ( M6           fill         m6               t t nil t nil )
  ( M6           gapFill      m6               t t nil t t )
  ( M6           exclude      m6_exc           t t t t t )
  ( M6           critexcl     m6_crit          t t t t t )
  ( M6           vdd1p8       m6_1p8           t t t t t )
  ( V6           drawing      v6               t t t t t )
  ( V6           net          v6_net           t t t nil nil )
  ( V6           boundary     v6_boundary      t t t nil nil )
  ( V6           grid         v6               t nil nil nil nil )
  ( V6           fill         v6               t t nil t nil )
  ( V6           blockage     v6               t nil nil t nil )
  ( M7           drawing      mx               t t t t t )
  ( M7           net          m7_net           t t t nil nil )
  ( M7           boundary     m7_boundary      t t t nil nil )
  ( M7           track        m7               nil nil t t nil )
  ( M7           pin          mx               t t t t t )
  ( M7           grid         m7               t nil nil nil nil )
  ( M7           blockage     m7               t nil nil t nil )
  ( M7           fill         m7               t t nil t nil )
  ( M7           gapFill      m7               t t nil t t )
  ( M7           exclude      m7_exc           t t t t t )
  ( M7           critexcl     m7_crit          t t t t t )
  ( M7           vdd1p8       m7_1p8           t t t t t )
  ( CMT          drawing      defaultPacket    t t t t t )
  ( CMT          grid         defaultPacket    t nil nil nil nil )
  ( CMT          blockage     defaultPacket    t nil t t nil )
  ( VT           drawing      v7               t t t t t )
  ( VT           net          v7_net           t t t nil nil )
  ( VT           boundary     v7_boundary      t t t nil nil )
  ( VT           grid         v7               t nil nil nil nil )
  ( VT           fill         v7               t t nil t nil )
  ( VT           blockage     v7               t nil nil t nil )
  ( MT           drawing      m8               t t t t t )
  ( MT           net          m8_net           t t t nil nil )
  ( MT           boundary     m8_boundary      t t t nil nil )
  ( MT           track        m8               nil nil t t nil )
  ( MT           pin          m8               t t t t t )
  ( MT           grid         m8               t nil nil nil nil )
  ( MT           blockage     m8               t nil nil t nil )
  ( MT           fill         m8               t t nil t nil )
  ( MT           gapFill      m8               t t nil t t )
  ( MT           exclude      m8_exc           t t t t t )
  ( MT           critexcl     m8_crit          t t t t t )
  ( MT           vdd1p8       m8_1p8           t t t t t )
  ( m1res        drawing      resm1            t t t t t )
  ( m2res        drawing      resm2            t t t t t )
  ( m3res        drawing      resm3            t t t t t )
  ( m4res        drawing      resm4            t t t t t )
  ( m5res        drawing      resm5            t t t t t )
  ( m6res        drawing      resm6            t t t t t )
  ( m7res        drawing      resm7            t t t t t )
  ( mtres        drawing      resmt            t t t t t )
  ( nwstires     drawing      resnwsti         t t t t t )
  ( nwodres      drawing      resnwod          t t t t t )
  ( diffres      drawing      resdiff          t t t t t )
  ( pcres        drawing      respc            t t t t t )
  ( diodmy       drawing      dmydio           t t t t t )
  ( NPNdummy     drawing      dmynpn           t t t t t )
  ( mimW         drawing      dmymimw          t t t t t )
  ( mimL         drawing      dmymiml          t t t t t )
  ( text         drawing      text             t t t t t )
 ) ;techDisplays

 techDerivedLayers(
 ;( DerivedLayerName          #          composition  )
 ;( ----------------          ------     ------------ )
  ( M2WSP                     40000      ( M2         'select  localWSP  ))
  ( M3WSP                     40010      ( M3         'select  localWSP  ))
  ( M4WSP                     40020      ( M4         'select  localWSP  ))
  ( M5WSP                     40030      ( M5         'select  localWSP  ))
  ( M1WSP                     40040      ( M1         'select  localWSP  ))
 ) ;techDerivedLayers

) ;layerDefinitions


;********************************
; LAYER RULES
;********************************
layerRules(

 widthSpacingPatterns(
; (t_name
;   ['offset           g_offset
;    ['repeatOffset]]
;   ['startingColor    g_color | 'shiftColor]
;   ['allowedRepeatMode {"none" | "steppedOnly" | "flippedOnly" }
;    ['defaultRepeatMode {"stepped" | "flippedStartsWithOdd"
;                         "defaultFlippedStartsWithEven"}]
;   ]
;   'pattern           (
;      (['repeat       g_repeat
;        ['wireTypes    (l_wireTypes)]
;        ['colors       (l_colors)]]
;       'spec          (('width g_width 'space g_space ['color t_color] ['wireType wireType]) ...)
;      ) ...
;    )
; )
; ( -------------------------------------------------------------------------- )
  (minWidth    
    'offset             0.016
    'startingColor      "mask1Color"
    'pattern            (
       ('repeat         12
        'spec           (('width 0.032 'space 0.064 'wireType "1X" ))
       )
     )
  )

  (minWidthHalf
    'offset             0.016
    'startingColor      "mask1Color"
    'pattern            (
       ('repeat         6
        'spec           (('width 0.032 'space 0.064 'wireType "1X" ))
       )
     )
  )

  (minWidthDouble
    'offset             0.016
    'startingColor      "mask1Color"
    'pattern            (
       ('repeat         24
        'spec           (('width 0.032 'space 0.064 'wireType "1X" ))
       )
     )
  )

  ("2XWidth"   
    'offset             0.032
    'startingColor      "mask1Color"
    'pattern            (
       ('repeat         8
        'spec           (('width 0.064 'space 0.096 'wireType "2X" ))
       )
     )
  )

  (stdCell     
    'startingColor      "mask1Color"
    'pattern            (
       ('spec           (('width 0.096 'space 0.096 'wireType "3X" ))
       )
       ('repeat         9
        'spec           (('width 0.032 'space 0.064 'wireType "1X" ))
       )
       ('spec           (('width 0.032 'space 0.096 'wireType "1X" ))
       )
     )
  )

  (stdCellMultiWidth
    'shiftColor        
    'pattern            (
       ('spec           (('width 0.096 'space 0.12 'color "mask1Color" 'wireType "3X" ))
       )
       ('repeat         3
        'spec           (('width 0.032 'space 0.0 'color "mask2Color" 'wireType "1X" )
                         ('width 0.048 'space 0.088 'color "mask2Color" 'wireType "1.5X" )
                         ('width 0.032 'space 0.0 'color "mask1Color" 'wireType "1X" )
                         ('width 0.048 'space 0.0 'color "mask1Color" 'wireType "1.5X" )
                         ('width 0.064 'space 0.088 'color "mask1Color" 'wireType "2X" ))
       )
       ('spec           (('width 0.032 'space 0.0 'color "mask2Color" 'wireType "1X" )
                         ('width 0.048 'space 0.072 'color "mask2Color" 'wireType "1.5X" ))
       )
     )
  )

  (stdCellHalf 
    'startingColor      "mask1Color"
    'pattern            (
       ('spec           (('width 0.096 'space 0.096 'wireType "3X" ))
       )
       ('repeat         3
        'spec           (('width 0.032 'space 0.064 'wireType "1X" ))
       )
       ('spec           (('width 0.032 'space 0.096 'wireType "1X" ))
       )
     )
  )

  (stdCellDouble
    'startingColor      "mask1Color"
    'pattern            (
       ('spec           (('width 0.096 'space 0.096 'wireType "3X" ))
       )
       ('repeat         21
        'spec           (('width 0.032 'space 0.064 'wireType "1X" ))
       )
       ('spec           (('width 0.032 'space 0.096 'wireType "1X" ))
       )
     )
  )

  (stdCellFlipped
    'offset             0.048
    'startingColor      "mask1Color"
    'allowedRepeatMode  "flippedOnly"
    'defaultRepeatMode  "flippedStartsWithOdd"
    'pattern            (
       ('spec           (('width 0.096 'space 0.096 'wireType "3X" ))
       )
       ('repeat         9
        'spec           (('width 0.032 'space 0.064 'wireType "1X" ))
       )
       ('spec           (('width 0.032 'space 0.096 'wireType "1X" ))
       )
     )
  )

  (diffTrackTopBottom
    'startingColor      "mask1Color"
    'allowedRepeatMode  "flippedOnly"
    'defaultRepeatMode  "flippedStartsWithOdd"
    'pattern            (
       ('spec           (('width 0.096 'space 0.096 'wireType "3X" ))
       )
       ('repeat         3
        'spec           (('width 0.032 'space 0.064 'wireType "1X" ))
       )
       ('spec           (('width 0.032 'space 0.48 'wireType "1X" ))
       )
       ('spec           (('width 0.048 'space 0.0 'wireType "1X" ))
       )
     )
  )

  (stdCellStepped
    'offset             0.048
    'startingColor      "mask1Color"
    'allowedRepeatMode  "steppedOnly"
    'defaultRepeatMode  "stepped"
    'pattern            (
       ('spec           (('width 0.096 'space 0.096 'wireType "3X" ))
       )
       ('repeat         9
        'spec           (('width 0.032 'space 0.064 'wireType "1X" ))
       )
       ('spec           (('width 0.032 'space 0.096 'wireType "1X" ))
       )
     )
  )

  (stdCellSingleHigh
    'offset             0.048
    'startingColor      "mask1Color"
    'allowedRepeatMode  "none"
    'pattern            (
       ('spec           (('width 0.096 'space 0.096 'wireType "3X" ))
       )
       ('repeat         9
        'spec           (('width 0.032 'space 0.064 'wireType "1X" ))
       )
       ('spec           (('width 0.032 'space 0.048 'wireType "1X" ))
       )
     )
  )

  (WSP1        
    'offset             0.016
    'repeatOffset      
    'pattern            (
       ('spec           (('width 0.032 'space 0.072 'color "mask1Color" 'wireType "1X" )
                         ('width 0.048 'space 0.088 'color "mask2Color" ))
       )
       ('repeat         3
        'spec           (('width 0.064 'space 0.088 'color "mask1Color" 'wireType "2X" )
                         ('width 0.048 'space 0.088 'color "mask2Color" ))
       )
       ('spec           (('width 0.032 'space 0.064 'color "mask1Color" 'wireType "2X" ))
       )
     )
  )

  (WSP2        
    'offset             0.032
    'repeatOffset      
    'pattern            (
       ('spec           (('width 0.064 'space 0.088 'wireType "2X" ))
       )
       ('repeat         3
        'spec           (('width 0.048 'space 0.072 )
                         ('width 0.032 'space 0.072 'wireType "1X" ))
       )
       ('spec           (('width 0.048 'space 0.072 )
                         ('width 0.032 'space 0.08 'wireType "1X" )
                         ('width 0.064 'space 0.064 'wireType "2X" ))
       )
     )
  )

  (WSP_32_48    
    'startingColor      "mask1Color"
    'pattern            (
       ('spec           (('width 0.064 'space 0.12 'wireType "2X" ))
       )
       ('repeat         7
        'spec           (('width 0.032 'space 0.08 'wireType "1X" ))
       )
       ('spec           (('width 0.032 'space 0.12 'wireType "1X" ))
       )
     )
  )

  (WSP_58_126    
    'offset             0.063
    'startingColor      "mask1Color"
    'pattern            (
       ('repeat         6
        'spec           (('width 0.058 'space 0.126 'wireType "1X" ))
       )
     )
  )

 ) ;widthSpacingPatterns

 widthSpacingPatternGroups(
; (t_name
;   'members           (l_patternNames)
; )
; ( -------------------------------------------------------------------------- )
  (basic       
    'members            ("minWidth" "2XWidth")
  )

  (multiWSP    
    'members            ("WSP1" "WSP2")
  )

 ) ;widthSpacingPatternGroups

 widthSpacingSnapPatternDefs(
; (t_name (tx_layer tx_purpose)
;   'period            g_period
;   'direction         {"horizontal" | "vertical"}
;   ['offset           g_offset]
;   'snappingLayers    (('layer tx_layer ['purposes l_purposes]) ... )
;   ['patterns         (l_patterns)]
;   ['patternGroups    (l_patternGroups)]
;   'defaultActive     t_defaultActivePatternName
;   ['orthogonalGrid   t_gridType]
; )
; ( -------------------------------------------------------------------------- )
  (M1WSSPD      ("M1"  "localWSP")
    'period             0.768
    'direction          "horizontal"
    'snappingLayers     (('layer "M1" ))
    'patterns           ("minWidth")
    'defaultActive      "minWidth"
  )

  (M2WSSPD      ("M2"  "localWSP")
    'period             0.768
    'direction          "vertical"
    'snappingLayers     (('layer "M2" ))
    'patterns           ("stdCell" "stdCellFlipped" "stdCellStepped" "stdCellSingleHigh" "diffTrackTopBottom" "stdCellMultiWidth")
    'patternGroups      ("basic" "multiWSP")
    'defaultActive      "minWidth"
  )

  (M2WSSPD_half ("M2"  "localWSP")
    'period             0.384
    'direction          "vertical"
    'snappingLayers     (('layer "M2" ))
    'patterns           ("minWidthHalf" "stdCellHalf")
    'defaultActive      "minWidthHalf"
  )

  (M2WSSPD_double ("M2"  "localWSP")
    'period             1.536
    'direction          "vertical"
    'snappingLayers     (('layer "M2" ))
    'patterns           ("minWidthDouble" "stdCellDouble")
    'defaultActive      "minWidthDouble"
  )

  (M3WSSPD      ("M3"  "localWSP")
    'period             0.768
    'direction          "horizontal"
    'snappingLayers     (('layer "M3" ))
    'patternGroups      ("basic" "multiWSP")
    'defaultActive      "minWidth"
  )

  (M3WSSPD_double ("M3"  "localWSP")
    'period             1.536
    'direction          "horizontal"
    'snappingLayers     (('layer "M3" ))
    'patterns           ("minWidthDouble" "stdCellDouble")
    'defaultActive      "minWidthDouble"
  )

  (M4WSSPD      ("M4"  "localWSP")
    'period             0.8
    'direction          "vertical"
    'snappingLayers     (('layer "M4" ))
    'patterns           ("WSP_32_48") 
    'defaultActive      "WSP_32_48"
  )

  (M5WSSPD      ("M5"  "localWSP")
    'period             0.756
    'direction          "horizontal"
    'snappingLayers     (('layer "M5" ))
    'patterns           ("WSP_58_126")
    'defaultActive      "WSP_58_126"
  )

 ) ;widthSpacingSnapPatternDefs

 relatedSnapPatterns(
; (t_name
;   'snapPatternDefs     (
;     (t_snapPatternDefName
;       ['patterns       (l_patterns)]
;       ['patternGroups  (l_patternGroups)]
;     )
;   )
; )
; ( -------------------------------------------------------------------------- )
  (minWidthStack
    'snapPatternDefs    (
       (M2WSSPD         'patterns ("minWidth")
       )
       (M3WSSPD         'patterns ("minWidth")
       )
     )
  )

  ("1X_2X_Stack"
    'snapPatternDefs    (
       (M2WSSPD         'patternGroups ("basic")
       )
       (M3WSSPD         'patterns ("minWidth" "2XWidth")
       )
     )
  )

 ) ;relatedSnapPatterns

) ;layerRules


;********************************
; CONSTRAINT GROUPS
;********************************
constraintGroups(

 ;( group	[override]	[definition]	[operator] )
 ;( -----	----------	------------	---------- )
  ( "wspRegions"	nil    nil    'and

    spacings(
     ( allowedWidthRanges         "M1WSP"	'measureHorizontal	'stepSize  0.768 	(">= 0.768") )
     ( allowedWidthRanges         "M1WSP"	'measureVertical	(">= 0.032") )
     ( allowedWidthRanges         "M2WSP"	'measureVertical	'stepSize  0.384	(">= 0.384") )
     ( allowedWidthRanges         "M2WSP"	'measureHorizontal	(">= 0.032") )
     ( allowedWidthRanges         "M3WSP"	'measureHorizontal	'stepSize  0.768	(">= 0.768") )
     ( allowedWidthRanges         "M3WSP"	'measureVertical	(">= 0.032") )
     ( allowedWidthRanges         "M4WSP"	'measureVertical	'stepSize  0.8  	(">= 0.8") )
     ( allowedWidthRanges         "M4WSP"	'measureHorizontal	(">= 0.032") )
     ( allowedWidthRanges         "M5WSP"	'measureHorizontal	'stepSize  0.756	(">= 0.756") )
     ( allowedWidthRanges         "M5WSP"	'measureVertical	(">= 0.058") )
    ) ;spacings
  ) ;wspRegions

 ;( group	[override]	[definition]	[operator] )
 ;( -----	----------	------------	---------- )
  ( "foundry"	nil
	memberConstraintGroups(
 	; listed in order of precedence
 	; -----------------------------
       "wspRegions"
	); memberConstraintGroups

    spacings(
     ( snapGridVertical           ("GFG" "M2WSSPD" "M4WSSPD") )
     ( snapGridHorizontal         ("GPG86" "GPG90" "M1WSSPD" "M3WSSPD" "M5WSSPD") )
    ) ;spacings
  ) ;foundry
) ;constraintGroups

