; Technology File johnTech
; Generated on Sep 18 15:57:40 2008
;     with @(#)$CDS: virtuoso version 6.1.2 08/28/2008 04:57 (cic612lnx) $


;********************************
; CONTROLS
;********************************
controls(
 techParams(
 ;( parameter           value             )
 ;( ----------          -----             )
  ( maskGrid       	0.005 )
  ( cadGrid        	0.005 )
  ( drcGrid        	0.005 )
  ( mfgGrid        	0.005 )
  ( scale          	1.0 )
  ( LEFDEF_MANUFACTURINGGRID	0.005 )
  ( LEFDEF_OVERLAP_LAYER_NAME	"OVERLAP"       )
 ) ;techParams

 viewTypeUnits(
 ;( viewType            userUnit       dbuperuu           )
 ;( --------            --------       --------           )
  ( maskLayout     	"micron"       	2000            )
  ( schematic      	"inch"         	160             )
  ( schematicSymbol	"inch"         	160             )
  ( netlist        	"inch"         	160             )
  ( hierDesign     	"_def_"        	2000            )
 ) ;viewTypeUnits

 mfgGridResolution(
      ( 0.005000 )
 ) ;mfgGridResolution

 refTechLibs(
; techLibName            
; -----------            
 ) ;refTechLibs

 processFamily(
 ) ;processFamily

 distanceMeasure(
 ) ;distanceMeasure

) ;controls


;********************************
; LAYER DEFINITION
;********************************
layerDefinitions(

 techPurposes(
 ;( PurposeName               Purpose#   Abbreviation )
 ;( -----------               --------   ------------ )
 ;User-Defined Purposes:
  ( GeoShare                  1          GeoShare     )
  ( port                      8          pt0          )
  ( port1                     9          pt1          )
  ( region                    10         reg          )
  ( ppath                     12         pp0          )
  ( nwell                     13         nwl          )
  ( nwelld                    14         nwld         )
  ( tpwell                    15         tpwl         )
  ( silicon                   20         si           )
  ( vlc                       21         vlc          )
  ( Metal1                    22         M1           )
  ( Metal2                    23         M2           )
  ( Metal3                    24         M3           )
  ( Metal4                    25         M4           )
  ( Metal5                    26         M5           )
  ( Metal6                    27         M6           )
 ;System-Reserved Purposes:
 ) ;techPurposes

 techLayers(
 ;( LayerName                 Layer#     Abbreviation )
 ;( ---------                 ------     ------------ )
 ;User-Defined Layers:
  ( ResWdum                   0          ResWdum      )
  ( Oxide                     1          OXIDE        )
  ( Nwell                     2          NWELL        )
  ( Poly                      3          POLY         )
  ( Nimp                      4          NIMP         )
  ( Pimp                      5          PIMP         )
  ( Cont                      6          CONT         )
  ( Metal1                    7          METAL1       )
  ( Via1                      8          VIA1         )
  ( Metal2                    9          METAL2       )
  ( Via2                      10         VIA2         )
  ( Metal3                    11         METAL3       )
  ( Capdum                    12         CAPDUM       )
  ( Resdum                    13         RESDUM       )
  ( CapMetal                  14         CAPMETA      )
  ( BJTdum                    15         BJTDUM       )
  ( INDdummy                  16         INDdumm      )
  ( IND2dummy                 17         IND2dum      )
  ( Pwell                     18         PWELL        )
  ( Nburied                   19         NBURIED      )
  ( NPNdummy                  20         NPNDUMM      )
  ( PNPdummy                  21         PNPDUMM      )
  ( DIOdummy                  22         DIODUMM      )
  ( SiProt                    23         SiProt       )
  ( ThickOxide                24         ThickOxide   )
  ( JVAR1dummy                25         JVAR1du      )
  ( JVAR2dummy                26         JVAR2du      )
  ( JVAR3dummy                27         JVAR3du      )
  ( RFdummy                   28         RFdummy      )
  ( Via3                      30         VIA3         )
  ( Metal4                    31         METAL4       )
  ( Via4                      32         VIA4         )
  ( Metal5                    33         METAL5       )
  ( Via5                      34         VIA5         )
  ( Metal6                    35         METAL6       )
  ( Bondpad                   36         Bondpad      )
  ( WellBody                  50         WELLBOD      )
  ( Psubiso                   51         PSUBISO      )
  ( scaPort                   66         scaP         )
  ( scaNwell                  67         scaNW        )
  ( scaNburied                68         scaNB        )
  ( scaSelect                 69         scaSel       )
  ( IND3dummy                 70         IND3dum      )
  ( M1dummy                   71         M1dum        )
  ( M2dummy                   72         M2dum        )
  ( M3dummy                   73         M3dum        )
  ( M4dummy                   74         M4dum        )
  ( M5dummy                   75         M5dum        )
  ( M6dummy                   76         M6dum        )
  ( SNA                       85         SNA          )
  ( allGeoShare               100        allGeo       )
  ( OVERLAP                   101        OVERLAP      )
  ( INDdumVlcRF               102        INDdumVlcRF  )
  ( vlccn                     103        vlccn        )
  ( vlcdummy                  104        vlcdummy     )
  ( PCMdummy                  105        PCMdum       )
 ;System-Reserved Layers:
 ) ;techLayers

 techLayerPurposePriorities(
 ;layers are ordered from lowest to highest priority
 ;( LayerName                 Purpose    )
 ;( ---------                 -------    )
  ( Nwell                     drawing    )
  ( Pwell                     drawing    )
  ( Nburied                   drawing    )
  ( Oxide                     drawing    )
  ( ThickOxide                drawing    )
  ( Poly                      drawing    )
  ( Poly                      track      )
  ( Nimp                      drawing    )
  ( Pimp                      drawing    )
  ( Cont                      drawing    )
  ( Cont                      grid       )
  ( Cont                      blockage   )
  ( Metal1                    drawing    )
  ( Metal1                    track      )
  ( Metal1                    grid       )
  ( Metal1                    blockage   )
  ( Via1                      drawing    )
  ( Via1                      grid       )
  ( Via1                      blockage   )
  ( Metal2                    drawing    )
  ( Metal2                    track      )
  ( Metal2                    grid       )
  ( Metal2                    blockage   )
  ( CapMetal                  drawing    )
  ( Via2                      drawing    )
  ( Via2                      grid       )
  ( Via2                      blockage   )
  ( Metal3                    drawing    )
  ( Metal3                    track      )
  ( Metal3                    grid       )
  ( Metal3                    blockage   )
  ( Via3                      drawing    )
  ( Via3                      grid       )
  ( Via3                      blockage   )
  ( Metal4                    drawing    )
  ( Metal4                    track      )
  ( Metal4                    grid       )
  ( Metal4                    blockage   )
  ( Via4                      drawing    )
  ( Via4                      grid       )
  ( Via4                      blockage   )
  ( Metal5                    drawing    )
  ( Metal5                    track      )
  ( Metal5                    grid       )
  ( Metal5                    blockage   )
  ( Via5                      drawing    )
  ( Via5                      grid       )
  ( Via5                      blockage   )
  ( Metal6                    drawing    )
  ( Metal6                    track      )
  ( Metal6                    grid       )
  ( Metal6                    blockage   )
  ( Bondpad                   drawing    )
  ( SiProt                    drawing    )
  ( Psubiso                   drawing    )
  ( text                      drawing    )
  ( text                      label      )
  ( prBoundary                drawing    )
  ( Poly                      pin        )
  ( Metal1                    pin        )
  ( Metal2                    pin        )
  ( Metal3                    pin        )
  ( Metal4                    pin        )
  ( Metal5                    pin        )
  ( Metal6                    pin        )
  ( Capdum                    drawing    )
  ( INDdummy                  drawing    )
  ( IND2dummy                 drawing    )
  ( IND3dummy                 drawing    )
  ( RFdummy                   drawing    )
  ( ResWdum                   drawing    )
  ( Resdum                    drawing    )
  ( M1dummy                   drawing    )
  ( M2dummy                   drawing    )
  ( M3dummy                   drawing    )
  ( M4dummy                   drawing    )
  ( M5dummy                   drawing    )
  ( M6dummy                   drawing    )
  ( BJTdum                    drawing    )
  ( NPNdummy                  drawing    )
  ( PNPdummy                  drawing    )
  ( DIOdummy                  drawing    )
  ( JVAR1dummy                drawing    )
  ( JVAR2dummy                drawing    )
  ( JVAR3dummy                drawing    )
  ( PCMdummy                  drawing    )
  ( vlccn                     drawing    )
  ( vlcdummy                  drawing    )
  ( INDdumVlcRF               silicon    )
  ( text                      vlc        )
  ( vlcdummy                  Metal6     )
  ( vlcdummy                  Metal5     )
  ( vlcdummy                  Metal4     )
  ( vlcdummy                  Metal3     )
  ( vlcdummy                  Metal2     )
  ( vlcdummy                  Metal1     )
  ( vlccn                     Metal6     )
  ( vlccn                     Metal5     )
  ( vlccn                     Metal4     )
  ( vlccn                     Metal3     )
  ( vlccn                     Metal2     )
  ( vlccn                     Metal1     )
  ( SNA                       nwell      )
  ( SNA                       nwelld     )
  ( SNA                       tpwell     )
  ( SNA                       region     )
  ( SNA                       port       )
  ( SNA                       port1      )
  ( SNA                       drawing9   )
  ( SNA                       drawing8   )
  ( SNA                       drawing7   )
  ( SNA                       drawing6   )
  ( SNA                       drawing5   )
  ( SNA                       drawing4   )
  ( SNA                       drawing3   )
  ( SNA                       drawing2   )
  ( SNA                       drawing1   )
  ( SNA                       drawing    )
  ( SNA                       grid       )
  ( SNA                       ppath      )
  ( SNA                       label      )
  ( Metal1                    label      )
  ( Metal1                    drawing4   )
  ( Metal1                    net        )
  ( Metal1                    boundary   )
  ( Via1                      label      )
  ( Via1                      pin        )
  ( Via1                      drawing4   )
  ( Via1                      net        )
  ( Via1                      boundary   )
  ( Metal2                    label      )
  ( Poly                      fill       )
  ( Poly                      slot       )
  ( Poly                      gapFill    )
  ( Poly                      blockage   )
  ( Poly                      grid       )
  ( Poly                      fillOPC    )
  ( Oxide                     fill       )
  ( Oxide                     slot       )
  ( Oxide                     gapFill    )
  ( Oxide                     blockage   )
  ( Oxide                     grid       )
  ( Oxide                     fillOPC    )
  ( Oxide                     pin        )
  ( Nimp                      fill       )
  ( Nimp                      slot       )
  ( Nimp                      gapFill    )
  ( Nimp                      blockage   )
  ( Nimp                      grid       )
  ( Nimp                      fillOPC    )
  ( Nimp                      pin        )
  ( Pimp                      fill       )
  ( Pimp                      slot       )
  ( Pimp                      gapFill    )
  ( Pimp                      blockage   )
  ( Pimp                      grid       )
  ( Pimp                      fillOPC    )
  ( Pimp                      pin        )
  ( Cont                      fill       )
  ( Cont                      slot       )
  ( Cont                      gapFill    )
  ( Cont                      fillOPC    )
  ( Metal1                    fill       )
  ( Metal1                    slot       )
  ( Metal1                    gapFill    )
  ( Metal1                    fillOPC    )
  ( Via1                      fill       )
  ( Via1                      slot       )
  ( Via1                      gapFill    )
  ( Via1                      fillOPC    )
  ( Metal2                    fill       )
  ( Metal2                    slot       )
  ( Metal2                    gapFill    )
  ( Metal2                    fillOPC    )
  ( Via2                      fill       )
  ( Via2                      slot       )
  ( Via2                      gapFill    )
  ( Via2                      fillOPC    )
  ( Metal3                    fill       )
  ( Metal3                    slot       )
  ( Metal3                    gapFill    )
  ( Metal3                    fillOPC    )
  ( Via3                      fill       )
  ( Via3                      slot       )
  ( Via3                      gapFill    )
  ( Via3                      fillOPC    )
  ( Metal4                    fill       )
  ( Metal4                    slot       )
  ( Metal4                    gapFill    )
  ( Metal4                    fillOPC    )
  ( Via4                      fill       )
  ( Via4                      slot       )
  ( Via4                      gapFill    )
  ( Via4                      fillOPC    )
  ( Metal5                    fill       )
  ( Metal5                    slot       )
  ( Metal5                    gapFill    )
  ( Metal5                    fillOPC    )
  ( Via5                      fill       )
  ( Via5                      slot       )
  ( Via5                      gapFill    )
  ( Via5                      fillOPC    )
  ( Metal6                    fill       )
  ( Metal6                    slot       )
  ( Metal6                    gapFill    )
  ( Metal6                    fillOPC    )
  ( OVERLAP                   fill       )
  ( OVERLAP                   slot       )
  ( OVERLAP                   gapFill    )
  ( OVERLAP                   blockage   )
  ( OVERLAP                   grid       )
  ( OVERLAP                   fillOPC    )
  ( OVERLAP                   pin        )
  ( OVERLAP                   net        )
  ( Metal2                    drawing4   )
  ( Metal2                    net        )
  ( Metal2                    boundary   )
  ( Via2                      pin        )
  ( Via2                      label      )
  ( Via2                      drawing4   )
  ( Via2                      net        )
  ( marker                    error      )
  ( marker                    warning    )
  ( Via2                      boundary   )
  ( Metal3                    label      )
  ( Metal3                    drawing4   )
  ( Metal3                    net        )
  ( Metal3                    boundary   )
  ( Via3                      pin        )
  ( Via3                      label      )
  ( Via3                      drawing4   )
  ( Via3                      net        )
  ( Via3                      boundary   )
  ( Metal4                    label      )
  ( Metal4                    drawing4   )
  ( Metal4                    net        )
  ( Metal4                    boundary   )
  ( Via4                      pin        )
  ( Via4                      label      )
  ( Via4                      drawing4   )
  ( Via4                      net        )
  ( Via4                      boundary   )
  ( Metal5                    label      )
  ( Metal5                    drawing4   )
  ( Metal5                    net        )
  ( Metal5                    boundary   )
  ( Via5                      pin        )
  ( Via5                      label      )
  ( Via5                      drawing4   )
  ( Via5                      net        )
  ( Via5                      boundary   )
  ( Metal6                    label      )
  ( Metal6                    drawing4   )
  ( Metal6                    net        )
  ( Metal6                    boundary   )
  ( CapMetal                  net        )
  ( CapMetal                  boundary   )
  ( Cont                      pin        )
  ( Cont                      net        )
  ( Cont                      boundary   )
  ( Poly                      label      )
  ( Poly                      drawing4   )
  ( Poly                      net        )
  ( Poly                      boundary   )
  ( Nwell                     net        )
  ( Nwell                     boundary   )
  ( Pwell                     net        )
  ( Pwell                     boundary   )
  ( Oxide                     net        )
  ( Oxide                     boundary   )
  ( Nburied                   net        )
  ( Nburied                   boundary   )
  ( Nimp                      boundary   )
  ( Pimp                      boundary   )
  ( Bondpad                   boundary   )
  ( WellBody                  drawing    )
  ( scaSelect                 drawing    )
  ( scaNburied                net        )
  ( scaNwell                  net        )
  ( scaPort                   net        )
  ( allGeoShare               drawing    )
  ( allGeoShare               GeoShare   )
  ( OVERLAP                   drawing    )
  ( OVERLAP                   label      )
  ( OVERLAP                   boundary   )
  ( background                drawing    )
  ( grid                      drawing    )
  ( grid                      drawing1   )
  ( annotate                  drawing    )
  ( annotate                  drawing1   )
  ( annotate                  drawing2   )
  ( annotate                  drawing3   )
  ( annotate                  drawing4   )
  ( annotate                  drawing5   )
  ( annotate                  drawing6   )
  ( annotate                  drawing7   )
  ( annotate                  drawing8   )
  ( annotate                  drawing9   )
  ( instance                  drawing    )
  ( instance                  label      )
  ( prBoundary                boundary   )
  ( prBoundary                label      )
  ( align                     drawing    )
  ( hardFence                 drawing    )
  ( softFence                 drawing    )
  ( text                      drawing1   )
  ( text                      drawing2   )
  ( border                    drawing    )
  ( device                    drawing    )
  ( device                    label      )
  ( device                    drawing1   )
  ( device                    drawing2   )
  ( device                    annotate   )
  ( wire                      drawing    )
  ( wire                      label      )
  ( wire                      flight     )
  ( pin                       label      )
  ( pin                       drawing    )
  ( pin                       annotate   )
  ( axis                      drawing    )
  ( edgeLayer                 drawing    )
  ( edgeLayer                 pin        )
  ( snap                      drawing    )
  ( snap                      boundary   )
  ( stretch                   drawing    )
  ( y0                        drawing    )
  ( y1                        drawing    )
  ( y2                        drawing    )
  ( y3                        drawing    )
  ( y4                        drawing    )
  ( y5                        drawing    )
  ( y6                        drawing    )
  ( y7                        drawing    )
  ( y8                        drawing    )
  ( y9                        drawing    )
  ( hilite                    drawing    )
  ( hilite                    drawing1   )
  ( hilite                    drawing2   )
  ( hilite                    drawing3   )
  ( hilite                    drawing4   )
  ( hilite                    drawing5   )
  ( hilite                    drawing6   )
  ( hilite                    drawing7   )
  ( hilite                    drawing8   )
  ( hilite                    drawing9   )
  ( select                    drawing    )
  ( drive                     drawing    )
  ( hiz                       drawing    )
  ( resist                    drawing    )
  ( spike                     drawing    )
  ( supply                    drawing    )
  ( unknown                   drawing    )
  ( unset                     drawing    )
  ( designFlow                drawing    )
  ( designFlow                drawing1   )
  ( designFlow                drawing2   )
  ( designFlow                drawing3   )
  ( designFlow                drawing4   )
  ( designFlow                drawing5   )
  ( designFlow                drawing6   )
  ( designFlow                drawing7   )
  ( designFlow                drawing8   )
  ( designFlow                drawing9   )
  ( changedLayer              tool0      )
  ( changedLayer              tool1      )
  ( Row                       drawing    )
  ( Row                       label      )
  ( Group                     drawing    )
  ( Group                     label      )
  ( Cannotoccupy              drawing    )
  ( Cannotoccupy              boundary   )
  ( Canplace                  drawing    )
  ( Unrouted                  drawing    )
  ( Unrouted                  drawing1   )
  ( Unrouted                  drawing2   )
  ( Unrouted                  drawing3   )
  ( Unrouted                  drawing4   )
  ( Unrouted                  drawing5   )
  ( Unrouted                  drawing6   )
  ( Unrouted                  drawing7   )
  ( Unrouted                  drawing8   )
  ( Unrouted                  drawing9   )
  ( INDdummy                  net        )
  ( JVAR1dummy                net        )
  ( Nimp                      net        )
  ( Pimp                      net        )
 ) ;techLayerPurposePriorities

 techDisplays(
 ;( LayerName    Purpose      Packet          Vis Sel Con2ChgLy DrgEnbl Valid )
 ;( ---------    -------      ------          --- --- --------- ------- ----- )
  ( Nwell        drawing      nwell            t t t t t )
  ( Pwell        drawing      pwell            t t t t nil )
  ( Nburied      drawing      npblk            t t t t nil )
  ( Oxide        drawing      tox              t t t t t )
  ( ThickOxide   drawing      thox             t t t t nil )
  ( Poly         drawing      poly1            t t t t t )
  ( Poly         track        poly1            nil nil t t nil )
  ( Nimp         drawing      nplus            t t t t t )
  ( Pimp         drawing      pplus            t t t t t )
  ( Cont         drawing      cw               t t t t t )
  ( Cont         grid         cw               t nil nil nil nil )
  ( Cont         blockage     cw               t nil t t nil )
  ( Metal1       drawing      m1               t t t t t )
  ( Metal1       track        m1               nil nil t t nil )
  ( Metal1       grid         m1               t nil nil nil nil )
  ( Metal1       blockage     m1               t nil t t nil )
  ( Via1         drawing      v1               t t t t t )
  ( Via1         grid         v1               t nil nil nil nil )
  ( Via1         blockage     v1               t nil t t nil )
  ( Metal2       drawing      m2               t t t t t )
  ( Metal2       track        m2               nil nil t t nil )
  ( Metal2       grid         m2               t nil nil nil nil )
  ( Metal2       blockage     m2               t nil t t nil )
  ( CapMetal     drawing      m4               t t t t t )
  ( Via2         drawing      v2               t t t t t )
  ( Via2         grid         v2               t nil nil nil nil )
  ( Via2         blockage     v2               t nil t t nil )
  ( Metal3       drawing      m3               t t t t t )
  ( Metal3       track        m3               nil nil t t nil )
  ( Metal3       grid         m3               t nil nil nil nil )
  ( Metal3       blockage     m3               t nil t t nil )
  ( Via3         drawing      v3               t t t t t )
  ( Via3         grid         v3               t nil nil nil nil )
  ( Via3         blockage     v3               t nil t t nil )
  ( Metal4       drawing      m4               t t t t t )
  ( Metal4       track        m4               nil nil t t nil )
  ( Metal4       grid         m4               t nil nil nil nil )
  ( Metal4       blockage     m4               t nil t t nil )
  ( Via4         drawing      v4               t t t t t )
  ( Via4         grid         v4               t nil nil nil nil )
  ( Via4         blockage     v4               t nil t t nil )
  ( Metal5       drawing      m5               t t t t t )
  ( Metal5       track        m5               nil nil t t nil )
  ( Metal5       grid         m5               t nil nil nil nil )
  ( Metal5       blockage     m5               t nil t t nil )
  ( Via5         drawing      v5               t t t t t )
  ( Via5         grid         v5               t nil nil nil nil )
  ( Via5         blockage     v5               t nil t t nil )
  ( Metal6       drawing      m6               t t t t t )
  ( Metal6       track        m6               nil nil t t nil )
  ( Metal6       grid         m6               t nil nil nil nil )
  ( Metal6       blockage     m6               t nil t t nil )
  ( Bondpad      drawing      pass             t t t t t )
  ( SiProt       drawing      siprot           t t t t t )
  ( Psubiso      drawing      Psubiso          t t t t t )
  ( text         drawing      notChg           t t t t t )
  ( text         label        notChg           t t t t t )
  ( prBoundary   drawing      prBoundary       t t nil t t )
  ( Poly         pin          poly1Pin         t t nil t nil )
  ( Metal1       pin          m1Pin            t t nil t t )
  ( Metal2       pin          m2Pin            t t nil t t )
  ( Metal3       pin          m3Pin            t t nil t t )
  ( Metal4       pin          m4Pin            t t nil t t )
  ( Metal5       pin          m5Pin            t t nil t t )
  ( Metal6       pin          m6Pin            t t nil t t )
  ( Capdum       drawing      zcap             t t t t t )
  ( INDdummy     drawing      zind             t t t t t )
  ( IND2dummy    drawing      zind2            t t t t t )
  ( IND3dummy    drawing      zind3            t t t t t )
  ( RFdummy      drawing      zrf              t t t t t )
  ( ResWdum      drawing      zrwell           t t t t t )
  ( Resdum       drawing      zrpoly           t t t t t )
  ( M1dummy      drawing      m1dum            t t t t t )
  ( M2dummy      drawing      m2dum            t t t t t )
  ( M3dummy      drawing      m3dum            t t t t t )
  ( M4dummy      drawing      m4dum            t t t t t )
  ( M5dummy      drawing      m5dum            t t t t t )
  ( M6dummy      drawing      m6dum            t t t t t )
  ( BJTdum       drawing      zbip             t t t t t )
  ( NPNdummy     drawing      znpn             t t t t t )
  ( PNPdummy     drawing      zpnp             t t t t t )
  ( DIOdummy     drawing      zdiode           t t t t t )
  ( JVAR1dummy   drawing      zjvar1           t t t t t )
  ( JVAR2dummy   drawing      zjvar2           t t t t t )
  ( JVAR3dummy   drawing      zjvar3           t t t t t )
  ( PCMdummy     drawing      PCMdummy         t t t t t )
  ( vlccn        drawing      vlccn            t t t t nil )
  ( vlcdummy     drawing      vlcdummy         t t t t nil )
  ( INDdumVlcRF  silicon      vlcbase          t t t t nil )
  ( text         vlc          text             t t nil t nil )
  ( vlcdummy     Metal6       vlcdummy         t t nil t nil )
  ( vlcdummy     Metal5       vlcdummy         t t nil t nil )
  ( vlcdummy     Metal4       vlcdummy         t t nil t nil )
  ( vlcdummy     Metal3       vlcdummy         t t nil t nil )
  ( vlcdummy     Metal2       vlcdummy         t t nil t nil )
  ( vlcdummy     Metal1       vlcdummy         t t nil t nil )
  ( vlccn        Metal6       vlccn            t t nil t nil )
  ( vlccn        Metal5       vlccn            t t nil t nil )
  ( vlccn        Metal4       vlccn            t t nil t nil )
  ( vlccn        Metal3       vlccn            t t nil t nil )
  ( vlccn        Metal2       vlccn            t t nil t nil )
  ( vlccn        Metal1       vlccn            t t nil t nil )
  ( SNA          nwell        nwell            t t nil t nil )
  ( SNA          nwelld       hilite7          t t nil t nil )
  ( SNA          tpwell       hilite9          t t nil t nil )
  ( SNA          region       SCRD             t t nil t nil )
  ( SNA          port         SCAPD            t t nil t nil )
  ( SNA          port1        SCAPD1           t t nil t nil )
  ( SNA          drawing9     SCSDD9           t t nil t nil )
  ( SNA          drawing8     SCSDD8           t t nil t nil )
  ( SNA          drawing7     SCSDD7           t t nil t nil )
  ( SNA          drawing6     SCSDD6           t t nil t nil )
  ( SNA          drawing5     SCSDD5           t t nil t nil )
  ( SNA          drawing4     SCSDD4           t t nil t nil )
  ( SNA          drawing3     SCSDD3           t t nil t nil )
  ( SNA          drawing2     SCSDD2           t t nil t nil )
  ( SNA          drawing1     SCSDD1           t t nil t nil )
  ( SNA          drawing      SCSDD0           t t nil t nil )
  ( SNA          grid         SCSGD            t t t t t )
  ( SNA          ppath        SCPPD            t t t t t )
  ( SNA          label        SCPPL            t t t t t )
  ( Metal1       label        m1               t t nil t nil )
  ( Metal1       drawing4     m1               t t nil t nil )
  ( Metal1       net          m1Net            t t nil t nil )
  ( Metal1       boundary     m1Bnd            t t nil t nil )
  ( Via1         label        v1               t t nil t nil )
  ( Via1         pin          v1               t t nil t nil )
  ( Via1         drawing4     v1               t t nil t nil )
  ( Via1         net          v1Net            t t nil t nil )
  ( Via1         boundary     v1Bnd            t t nil t nil )
  ( Metal2       label        m2               t t nil t nil )
  ( Poly         fill         Poly_fill        t t t t nil )
  ( Poly         slot         Poly_slot        t t t t nil )
  ( Poly         gapFill      Poly_gapFill     t t t t nil )
  ( Poly         blockage     Poly_blockage    t t t t nil )
  ( Poly         grid         Poly_grid        t t t t nil )
  ( Poly         fillOPC      Poly_fillOPC     t t t t nil )
  ( Oxide        fill         Oxide_fill       t t t t nil )
  ( Oxide        slot         Oxide_slot       t t t t nil )
  ( Oxide        gapFill      Oxide_gapFill    t t t t nil )
  ( Oxide        blockage     Oxide_blockage   t t t t nil )
  ( Oxide        grid         Oxide_grid       t t t t nil )
  ( Oxide        fillOPC      Oxide_fillOPC    t t t t nil )
  ( Oxide        pin          Oxide_pin        t t t t nil )
  ( Nimp         fill         Nimp_fill        t t t t nil )
  ( Nimp         slot         Nimp_slot        t t t t nil )
  ( Nimp         gapFill      Nimp_gapFill     t t t t nil )
  ( Nimp         blockage     Nimp_blockage    t t t t nil )
  ( Nimp         grid         Nimp_grid        t t t t nil )
  ( Nimp         fillOPC      Nimp_fillOPC     t t t t nil )
  ( Nimp         pin          Nimp_pin         t t t t nil )
  ( Pimp         fill         Pimp_fill        t t t t nil )
  ( Pimp         slot         Pimp_slot        t t t t nil )
  ( Pimp         gapFill      Pimp_gapFill     t t t t nil )
  ( Pimp         blockage     Pimp_blockage    t t t t nil )
  ( Pimp         grid         Pimp_grid        t t t t nil )
  ( Pimp         fillOPC      Pimp_fillOPC     t t t t nil )
  ( Pimp         pin          Pimp_pin         t t t t nil )
  ( Cont         fill         Cont_fill        t t t t nil )
  ( Cont         slot         Cont_slot        t t t t nil )
  ( Cont         gapFill      Cont_gapFill     t t t t nil )
  ( Cont         fillOPC      Cont_fillOPC     t t t t nil )
  ( Metal1       fill         Metal1_fill      t t t t nil )
  ( Metal1       slot         Metal1_slot      t t t t nil )
  ( Metal1       gapFill      Metal1_gapFill   t t t t nil )
  ( Metal1       fillOPC      Metal1_fillOPC   t t t t nil )
  ( Via1         fill         Via1_fill        t t t t nil )
  ( Via1         slot         Via1_slot        t t t t nil )
  ( Via1         gapFill      Via1_gapFill     t t t t nil )
  ( Via1         fillOPC      Via1_fillOPC     t t t t nil )
  ( Metal2       fill         Metal2_fill      t t t t nil )
  ( Metal2       slot         Metal2_slot      t t t t nil )
  ( Metal2       gapFill      Metal2_gapFill   t t t t nil )
  ( Metal2       fillOPC      Metal2_fillOPC   t t t t nil )
  ( Via2         fill         Via2_fill        t t t t nil )
  ( Via2         slot         Via2_slot        t t t t nil )
  ( Via2         gapFill      Via2_gapFill     t t t t nil )
  ( Via2         fillOPC      Via2_fillOPC     t t t t nil )
  ( Metal3       fill         Metal3_fill      t t t t nil )
  ( Metal3       slot         Metal3_slot      t t t t nil )
  ( Metal3       gapFill      Metal3_gapFill   t t t t nil )
  ( Metal3       fillOPC      Metal3_fillOPC   t t t t nil )
  ( Via3         fill         Via3_fill        t t t t nil )
  ( Via3         slot         Via3_slot        t t t t nil )
  ( Via3         gapFill      Via3_gapFill     t t t t nil )
  ( Via3         fillOPC      Via3_fillOPC     t t t t nil )
  ( Metal4       fill         Metal4_fill      t t t t nil )
  ( Metal4       slot         Metal4_slot      t t t t nil )
  ( Metal4       gapFill      Metal4_gapFill   t t t t nil )
  ( Metal4       fillOPC      Metal4_fillOPC   t t t t nil )
  ( Via4         fill         Via4_fill        t t t t nil )
  ( Via4         slot         Via4_slot        t t t t nil )
  ( Via4         gapFill      Via4_gapFill     t t t t nil )
  ( Via4         fillOPC      Via4_fillOPC     t t t t nil )
  ( Metal5       fill         Metal5_fill      t t t t nil )
  ( Metal5       slot         Metal5_slot      t t t t nil )
  ( Metal5       gapFill      Metal5_gapFill   t t t t nil )
  ( Metal5       fillOPC      Metal5_fillOPC   t t t t nil )
  ( Via5         fill         Via5_fill        t t t t nil )
  ( Via5         slot         Via5_slot        t t t t nil )
  ( Via5         gapFill      Via5_gapFill     t t t t nil )
  ( Via5         fillOPC      Via5_fillOPC     t t t t nil )
  ( Metal6       fill         Metal6_fill      t t t t nil )
  ( Metal6       slot         Metal6_slot      t t t t nil )
  ( Metal6       gapFill      Metal6_gapFill   t t t t nil )
  ( Metal6       fillOPC      Metal6_fillOPC   t t t t nil )
  ( OVERLAP      fill         OVERLAP_fill     t nil t t nil )
  ( OVERLAP      slot         OVERLAP_slot     t nil t t nil )
  ( OVERLAP      gapFill      OVERLAP_gapFill  t nil t t nil )
  ( OVERLAP      blockage     OVERLAP_blockage t nil t t nil )
  ( OVERLAP      grid         OVERLAP_grid     t nil t t nil )
  ( OVERLAP      fillOPC      OVERLAP_fillOPC  t nil t t nil )
  ( OVERLAP      pin          OVERLAP_pin      t nil t t nil )
  ( OVERLAP      net          OVERLAP_net      t nil t t nil )
  ( Metal2       drawing4     m2               t t nil t nil )
  ( Metal2       net          m2Net            t t nil t nil )
  ( Metal2       boundary     m2Bnd            t t nil t nil )
  ( Via2         pin          v2               t t nil t nil )
  ( Via2         label        v2               t t nil t nil )
  ( Via2         drawing4     v2               t t nil t nil )
  ( Via2         net          v2Net            t t nil t nil )
  ( marker       error        markerErr        t t nil t nil )
  ( marker       warning      markerWarn       t t nil t nil )
  ( Via2         boundary     v2Bnd            t t nil t nil )
  ( Metal3       label        m3               t t nil t nil )
  ( Metal3       drawing4     m3               t t nil t nil )
  ( Metal3       net          m3Net            t t nil t nil )
  ( Metal3       boundary     m3Bnd            t t nil t nil )
  ( Via3         pin          v3               t t nil t nil )
  ( Via3         label        v3               t t nil t nil )
  ( Via3         drawing4     v3               t t nil t nil )
  ( Via3         net          v3Net            t t nil t nil )
  ( Via3         boundary     v3Bnd            t t nil t nil )
  ( Metal4       label        m4               t t nil t nil )
  ( Metal4       drawing4     m4               t t nil t nil )
  ( Metal4       net          m4Net            t t nil t nil )
  ( Metal4       boundary     m4Bnd            t t nil t nil )
  ( Via4         pin          v4               t t nil t nil )
  ( Via4         label        v4               t t nil t nil )
  ( Via4         drawing4     v4               t t nil t nil )
  ( Via4         net          v4Net            t t nil t nil )
  ( Via4         boundary     v4Bnd            t t nil t nil )
  ( Metal5       label        m5               t t nil t nil )
  ( Metal5       drawing4     m5               t t nil t nil )
  ( Metal5       net          m5Net            t t nil t nil )
  ( Metal5       boundary     m5Bnd            t t nil t nil )
  ( Via5         pin          v5               t t nil t nil )
  ( Via5         label        v5               t t nil t nil )
  ( Via5         drawing4     v5               t t nil t nil )
  ( Via5         net          v5Net            t t nil t nil )
  ( Via5         boundary     v5Bnd            t t nil t nil )
  ( Metal6       label        m6               t t nil t nil )
  ( Metal6       drawing4     m6               t t nil t nil )
  ( Metal6       net          m6Net            t t nil t nil )
  ( Metal6       boundary     m6Bnd            t t nil t nil )
  ( CapMetal     net          m4               t t nil t nil )
  ( CapMetal     boundary     m4               t t nil t nil )
  ( Cont         pin          cwPin            t t nil t nil )
  ( Cont         net          cwNet            t t nil t nil )
  ( Cont         boundary     cwBnd            t t nil t nil )
  ( Poly         label        poly1            t t nil t nil )
  ( Poly         drawing4     poly1            t t nil t nil )
  ( Poly         net          poly1Net         t t nil t nil )
  ( Poly         boundary     poly1Bnd         t t nil t nil )
  ( Nwell        net          nwellNet         t t nil t nil )
  ( Nwell        boundary     nwellBnd         t t nil t nil )
  ( Pwell        net          pwellNet         t t nil t nil )
  ( Pwell        boundary     pwellBnd         t t nil t nil )
  ( Oxide        net          toxBnd           t t nil t nil )
  ( Oxide        boundary     toxBnd           t t nil t nil )
  ( Nburied      net          npblk            t t nil t nil )
  ( Nburied      boundary     npblkBnd         t t nil t nil )
  ( Nimp         boundary     nplusBnd         t t nil t nil )
  ( Pimp         boundary     pplusBnd         t t nil t nil )
  ( Bondpad      boundary     pbaseBnd         t t nil t nil )
  ( WellBody     drawing      WellBody         nil nil nil t nil )
  ( scaSelect    drawing      scaSelect        t t nil t t )
  ( scaNburied   net          scaNburied_net   t nil nil nil nil )
  ( scaNwell     net          scaNwell_net     t nil nil nil nil )
  ( scaPort      net          scaPort_net      t nil nil nil nil )
  ( allGeoShare  drawing      ovlap            nil nil nil t nil )
  ( allGeoShare  GeoShare     ovlap            t t t t t )
  ( OVERLAP      drawing      ovlap            t nil t t nil )
  ( OVERLAP      label        ovlap            t nil nil t nil )
  ( OVERLAP      boundary     ovlap            t nil nil t t )
  ( background   drawing      background       t nil nil nil nil )
  ( grid         drawing      grid             t nil nil nil nil )
  ( grid         drawing1     grid1            t nil nil nil nil )
  ( annotate     drawing      annotate         t t nil t nil )
  ( annotate     drawing1     annotate1        t t nil t nil )
  ( annotate     drawing2     annotate2        t t nil t nil )
  ( annotate     drawing3     annotate3        t t nil t nil )
  ( annotate     drawing4     annotate4        t t nil t nil )
  ( annotate     drawing5     annotate5        t t nil t nil )
  ( annotate     drawing6     annotate6        t t nil t nil )
  ( annotate     drawing7     annotate7        t t nil t nil )
  ( annotate     drawing8     annotate8        t t nil t nil )
  ( annotate     drawing9     annotate9        t t nil t nil )
  ( instance     drawing      instance         t t nil t t )
  ( instance     label        instanceLbl      t t nil t nil )
  ( prBoundary   boundary     prBoundaryBnd    t t nil t nil )
  ( prBoundary   label        prBoundaryLbl    t t nil t nil )
  ( align        drawing      align            t t nil t nil )
  ( hardFence    drawing      hardFence        t t nil t nil )
  ( softFence    drawing      softFence        t t nil t nil )
  ( text         drawing1     text1            t t nil t nil )
  ( text         drawing2     text2            t t nil t nil )
  ( border       drawing      border           t t nil t nil )
  ( device       drawing      device           t t nil t nil )
  ( device       label        deviceLbl        t t nil t nil )
  ( device       drawing1     device1          t t nil t nil )
  ( device       drawing2     device2          t t nil t nil )
  ( device       annotate     deviceAnt        t t nil t nil )
  ( wire         drawing      wire             t t nil t nil )
  ( wire         label        wireLbl          t t nil t nil )
  ( wire         flight       wireFlt          t t nil t nil )
  ( pin          label        pinLbl           t t nil t nil )
  ( pin          drawing      pin              t t nil t nil )
  ( pin          annotate     pinAnt           t t nil t nil )
  ( axis         drawing      axis             t nil nil t nil )
  ( edgeLayer    drawing      edgeLayer        t t nil t nil )
  ( edgeLayer    pin          edgeLayerPin     t t nil t nil )
  ( snap         drawing      snap             t t nil t nil )
  ( snap         boundary     snap             t t nil t nil )
  ( stretch      drawing      stretch          t t nil t nil )
  ( y0           drawing      y0               t t nil t nil )
  ( y1           drawing      y1               t t nil t nil )
  ( y2           drawing      y2               t t nil t nil )
  ( y3           drawing      y3               t t nil t nil )
  ( y4           drawing      y4               t t nil t nil )
  ( y5           drawing      y5               t t nil t nil )
  ( y6           drawing      y6               t t nil t nil )
  ( y7           drawing      y7               t t nil t nil )
  ( y8           drawing      y8               t t nil t nil )
  ( y9           drawing      y9               t t nil t nil )
  ( hilite       drawing      hilite           t t nil t nil )
  ( hilite       drawing1     hilite1          t t nil t nil )
  ( hilite       drawing2     hilite2          t t nil t nil )
  ( hilite       drawing3     hilite3          t t nil t nil )
  ( hilite       drawing4     hilite4          t t nil t nil )
  ( hilite       drawing5     hilite5          t t nil t nil )
  ( hilite       drawing6     hilite6          t t nil t nil )
  ( hilite       drawing7     hilite7          t t nil t nil )
  ( hilite       drawing8     hilite8          t t nil t nil )
  ( hilite       drawing9     hilite9          t t nil t nil )
  ( select       drawing      select           t t nil t nil )
  ( drive        drawing      drive            t t nil t nil )
  ( hiz          drawing      hiz              t t nil t nil )
  ( resist       drawing      resist           t t nil t nil )
  ( spike        drawing      spike            t t nil t nil )
  ( supply       drawing      supply           t t nil t nil )
  ( unknown      drawing      unknown          t t nil t nil )
  ( unset        drawing      unset            t t nil t nil )
  ( designFlow   drawing      designFlow       t nil nil nil nil )
  ( designFlow   drawing1     designFlow1      t nil nil nil nil )
  ( designFlow   drawing2     designFlow2      t nil nil nil nil )
  ( designFlow   drawing3     designFlow3      t nil nil nil nil )
  ( designFlow   drawing4     designFlow4      t nil nil nil nil )
  ( designFlow   drawing5     designFlow5      t nil nil nil nil )
  ( designFlow   drawing6     designFlow6      t nil nil nil nil )
  ( designFlow   drawing7     designFlow7      t nil nil nil nil )
  ( designFlow   drawing8     designFlow8      t nil nil nil nil )
  ( designFlow   drawing9     designFlow9      t nil nil nil nil )
  ( changedLayer tool0        changedLayerTl0  nil nil nil nil nil )
  ( changedLayer tool1        changedLayerTl1  nil nil nil nil nil )
  ( Row          drawing      prBoundaryLbl    t t nil t t )
  ( Row          label        RowLbl           t t nil t nil )
  ( Group        drawing      Group            t t nil t nil )
  ( Group        label        GroupLbl         t t nil t nil )
  ( Cannotoccupy drawing      Cannotoccupy     t t nil t nil )
  ( Cannotoccupy boundary     CannotoccupyBnd  t t nil t nil )
  ( Canplace     drawing      Canplace         t t nil t nil )
  ( Unrouted     drawing      Unrouted         t t nil t nil )
  ( Unrouted     drawing1     Unrouted1        t t nil t nil )
  ( Unrouted     drawing2     Unrouted2        t t nil t nil )
  ( Unrouted     drawing3     Unrouted3        t t nil t nil )
  ( Unrouted     drawing4     Unrouted4        t t nil t nil )
  ( Unrouted     drawing5     Unrouted5        t t nil t nil )
  ( Unrouted     drawing6     Unrouted6        t t nil t nil )
  ( Unrouted     drawing7     Unrouted7        t t nil t nil )
  ( Unrouted     drawing8     Unrouted8        t t nil t nil )
  ( Unrouted     drawing9     Unrouted9        t t nil t nil )
  ( INDdummy     net          zindnet          t t nil t nil )
  ( JVAR1dummy   net          zjvar1           t t nil t nil )
  ( Nimp         net          nplusBnd         t t nil t nil )
  ( Pimp         net          pplusBnd         t t nil t nil )
 ) ;techDisplays

 techLayerProperties(
 ;( PropName               Layer1 [ Layer2 ]            PropValue )
 ;( --------               ------ ----------            --------- )
  ( sheetResistance        Oxide                          300.000000 )
  ( sheetResistance        Poly                           7.500000 )
  ( areaCapacitance        Metal1                         1.320000e-04 )
  ( edgeCapacitance        Metal1                         8.800000e-05 )
  ( sheetResistance        Metal1                         0.101000 )
  ( areaCapacitance        Metal2                         7.000000e-05 )
  ( edgeCapacitance        Metal2                         8.300000e-05 )
  ( sheetResistance        Metal2                         0.101000 )
  ( areaCapacitance        Metal3                         6.300000e-05 )
  ( edgeCapacitance        Metal3                         1.000000e-04 )
  ( sheetResistance        Metal3                         0.101000 )
  ( areaCapacitance        Metal4                         5.400000e-05 )
  ( edgeCapacitance        Metal4                         8.300000e-05 )
  ( sheetResistance        Metal4                         0.101000 )
  ( areaCapacitance        Metal5                         3.100000e-05 )
  ( edgeCapacitance        Metal5                         1.020000e-04 )
  ( sheetResistance        Metal5                         0.045000 )
  ( areaCapacitance        Metal6                         3.100000e-05 )
  ( edgeCapacitance        Metal6                         1.020000e-04 )
  ( sheetResistance        Metal6                         0.045000 )
 ) ;techLayerProperties

 techDerivedLayers(
 ;( DerivedLayerName          #          composition  )
 ;( ----------------          ------     ------------ )
  ( noOverlapLayer1           10001           ( CapMetal   'and    Metal1    ))
  ( noOverlapLayer2           10002           ( Poly       'and    Resdum    ))
  ( gate                      10003           ( Poly       'and    Oxide     ))
  ( ipoly                     10004           ( Poly       'not    gate      ))
  ( gate15                    10005           ( gate       'not    ThickOxide))
  ( gate25                    10006           ( gate       'and    ThickOxide))
  ( ngate_tmp                 10007           ( gate       'and    Nimp      ))
  ( ngate                     10008           ( ngate_tmp  'not    Nwell     ))
  ( pgate_tmp                 10009           ( gate       'and    Pimp      ))
  ( pgate                     10010           ( pgate_tmp  'and    Nwell     ))
  ( ngate15                   10011           ( ngate      'not    ThickOxide))
  ( pgate15                   10012           ( pgate      'not    ThickOxide))
  ( ngate25                   10013           ( ngate      'and    ThickOxide))
  ( pgate25                   10014           ( pgate      'and    ThickOxide))
  ( ndiff                     10015           ( Oxide      'and    Nimp      ))
  ( pdiff                     10016           ( Oxide      'and    Pimp      ))
  ( ndiff25                   10017           ( ndiff      'and    ThickOxide))
  ( pdiff25                   10018           ( pdiff      'and    ThickOxide))
  ( sd_ndiff                  10019           ( ndiff      'not    Nwell     ))
  ( sd_pdiff                  10020           ( pdiff      'and    Nwell     ))
  ( ntap                      10021           ( ndiff      'and    Nwell     ))
  ( ptap                      10022           ( pdiff      'not    Nwell     ))
  ( sd_cont                   10023           ( Cont       'and    Oxide     ))
  ( CapVia2                   10024           ( Via2       'and    CapMetal  ))
 ) ;techDerivedLayers

) ;layerDefinitions


;********************************
; LAYER RULES
;********************************
layerRules(

 equivalentLayers(
 ;( list of layers )
 ;( -------------- )
 ) ;equivalentLayers

 functions(
 ;( layer                       function        [maskNumber])
 ;( -----                       --------        ------------)
  ( Nburied                  	"recognition"	1            )
  ( Nwell                    	"nwell"     	2            )
  ( Pwell                    	"pwell"     	3            )
  ( Poly                     	"poly"      	4            )
  ( Oxide                    	"diff"      	5            )
  ( Nimp                     	"nplus"     	6            )
  ( Pimp                     	"pplus"     	7            )
  ( Cont                     	"cut"       	8            )
  ( Metal1                   	"metal"     	9            )
  ( Via1                     	"cut"       	10           )
  ( Metal2                   	"metal"     	11           )
  ( Via2                     	"cut"       	12           )
  ( Metal3                   	"metal"     	13           )
  ( Via3                     	"cut"       	14           )
  ( Metal4                   	"metal"     	15           )
  ( Via4                     	"cut"       	16           )
  ( Metal5                   	"metal"     	17           )
  ( Via5                     	"cut"       	18           )
  ( Metal6                   	"metal"     	19           )
  ( OVERLAP                  	"passivationCut"	20           )
 ) ;functions

 mfgResolutions(
 ;( layer                       mfgResolution )
 ;( -----                       ------------- )
 ) ;mfgResolutions

 routingDirections(
 ;( layer                       direction     )
 ;( -----                       ---------     )
  ( Poly                     	"none"       )
  ( Metal1                   	"horizontal" )
  ( Metal2                   	"vertical"   )
  ( Metal3                   	"horizontal" )
  ( Metal4                   	"vertical"   )
  ( Metal5                   	"horizontal" )
  ( Metal6                   	"vertical"   )
 ) ;routingDirections

 incompatibleLayers(
 ;( layer                       incompatibleLayers       )
 ;( -----                       ------------------       )
 ) ;incompatibleLayers

 labelLayers(
 ;( textLayer   layers        )
 ;( ---------   ----------------------------------        )
 ) ;labelLayers

 stampLabelLayers(
 ;( textLayer   layers        )
 ;( ---------   ----------------------------------        )
  ( text      	Poly      	Metal1    	Metal2    	Metal3    	Metal4    	Metal5    	Metal6     )
 ) ;stampLabelLayers

 currentDensity(
 ;( rule                	layer1    	layer2    	value    )
 ;( ----                	------    	------    	-----    )
  ( avgDCCurrentDensity 	"Cont"			0.1	 )
  ( avgDCCurrentDensity 	"Metal1"			2.0	 )
  ( avgDCCurrentDensity 	"Via1"			0.1	 )
  ( avgDCCurrentDensity 	"Metal2"			2.0	 )
  ( avgDCCurrentDensity 	"Via2"			0.1	 )
  ( avgDCCurrentDensity 	"Metal3"			2.0	 )
  ( avgDCCurrentDensity 	"Via3"			0.1	 )
  ( avgDCCurrentDensity 	"Metal4"			2.0	 )
  ( avgDCCurrentDensity 	"Via4"			0.1	 )
  ( avgDCCurrentDensity 	"Metal5"			2.0	 )
  ( avgDCCurrentDensity 	"Via5"			0.1	 )
  ( avgDCCurrentDensity 	"Metal6"			2.0	 )
 ) ;currentDensity

 currentDensityTables(
 ;( rule                	layer1    
 ;  (( index1Definitions	[index2Definitions]) [defaultValue] )
 ;  (table))
 ;( ----------------------------------------------------------------------)
 ) ;currentDensityTables

) ;layerRules


;********************************
; VIADEFS
;********************************
viaDefs(

 standardViaDefs(
 ;( viaDefName	layer1	layer2	(cutLayer cutWidth cutHeight [resistancePerCut]) 
 ;   (cutRows	cutCol	(cutSpace)) 
 ;   (layer1Enc) (layer2Enc)	(layer1Offset)	(layer2Offset)	(origOffset) 
 ;   [implant1	 (implant1Enc)	[implant2	(implant2Enc) [well/substrate]]]) 
 ;( -------------------------------------------------------------------------- ) 
  ( M6_M5       	Metal5      Metal6      	("Via5" 0.2 0.2 6.4)
     (1 1 (0.5 0.5))
     (0.1 0.1)	(0.1 0.1)	(0.0 0.0)	(0.0 0.0)	(0.0 0.0)
  )
  ( M5_M4       	Metal4      Metal5      	("Via4" 0.2 0.2 6.4)
     (1 1 (0.5 0.5))
     (0.1 0.1)	(0.1 0.1)	(0.0 0.0)	(0.0 0.0)	(0.0 0.0)
  )
  ( M4_M3       	Metal3      Metal4      	("Via3" 0.2 0.2 6.4)
     (1 1 (0.5 0.5))
     (0.1 0.1)	(0.1 0.1)	(0.0 0.0)	(0.0 0.0)	(0.0 0.0)
  )
  ( M3_M2       	Metal2      Metal3      	("Via2" 0.2 0.2 6.4)
     (1 1 (0.5 0.5))
     (0.1 0.1)	(0.1 0.1)	(0.0 0.0)	(0.0 0.0)	(0.0 0.0)
  )
  ( M2_M1       	Metal1      Metal2      	("Via1" 0.2 0.2 6.4)
     (1 1 (0.5 0.5))
     (0.1 0.1)	(0.1 0.1)	(0.0 0.0)	(0.0 0.0)	(0.0 0.0)
  )
  ( M1_ISOPWELL 	Oxide       Metal1      	("Cont" 0.2 0.2)
     (1 1 (0.3 0.3))
     (0.2 0.2)	(0.1 0.1)	(0.0 0.0)	(0.0 0.0)	(0.0 0.0)
     Pimp        	(0.2 0.2)	Nburied     	(0.9 0.9)
  )
  ( M1_PSUB     	Oxide       Metal1      	("Cont" 0.2 0.2)
     (1 1 (0.3 0.3))
     (0.2 0.2)	(0.1 0.1)	(0.0 0.0)	(0.0 0.0)	(0.0 0.0)
     Pimp        	(0.2 0.2)
  )
  ( M1_PIMP     	Oxide       Metal1      	("Cont" 0.2 0.2)
     (1 1 (0.3 0.3))
     (0.2 0.2)	(0.1 0.1)	(0.0 0.0)	(0.0 0.0)	(0.0 0.0)
     Pimp        	(0.2 0.2)
  )
  ( M1_NWELL    	Oxide       Metal1      	("Cont" 0.2 0.2)
     (1 1 (0.3 0.3))
     (0.2 0.2)	(0.1 0.1)	(0.0 0.0)	(0.0 0.0)	(0.0 0.0)
     Nimp        	(0.2 0.2)	Nwell       	(0.6 0.6)
  )
  ( M1_NIMP     	Oxide       Metal1      	("Cont" 0.2 0.2)
     (1 1 (0.3 0.3))
     (0.2 0.2)	(0.1 0.1)	(0.0 0.0)	(0.0 0.0)	(0.0 0.0)
     Nimp        	(0.2 0.2)
  )
  ( M1_POLY1    	Poly        Metal1      	("Cont" 0.2 0.2)
     (1 1 (0.3 0.3))
     (0.2 0.2)	(0.1 0.1)	(0.0 0.0)	(0.0 0.0)	(0.0 0.0)
  )
 ) ;standardViaDefs

 customViaDefs(
 ;( viaDefName libName cellName viewName layer1 layer2 resistancePerCut)
 ;( ---------- ------- -------- -------- ------ ------ ----------------)
   ( Via56_stack_west  gpdk180 Via56_stack_west symbolic Metal5 Metal6 2.54)
   ( Via56_stack_east  gpdk180 Via56_stack_east symbolic Metal5 Metal6 2.54)
   ( Via45_stack_south  gpdk180 Via45_stack_south symbolic Metal4 Metal5 2.54)
   ( Via45_stack_north  gpdk180 Via45_stack_north symbolic Metal4 Metal5 2.54)
   ( Via34_stack_west  gpdk180 Via34_stack_west symbolic Metal3 Metal4 6.4)
   ( Via34_stack_east  gpdk180 Via34_stack_east symbolic Metal3 Metal4 6.4)
   ( Via23_stack_south  gpdk180 Via23_stack_south symbolic Metal2 Metal3 6.4)
   ( Via23_stack_north  gpdk180 Via23_stack_north symbolic Metal2 Metal3 6.4)
   ( ruleVia            gpdk180 ruleVia           symbolic Metal1 Metal2 0.0)
 ) ;customViaDefs

 standardViaVariants(
 ;( viaVariantName viaDefName (cutLayer cutWidth cutHeight) 
 ;   (cutRows	cutCol	(cutSpace)) 
 ;   (layer1Enc) (layer2Enc)	(layer1Offset)	(layer2Offset)	(origOffset) 
 ;   (implant1Enc) (implant2Enc) (cut_pattern) ) 
 ;( -------------------------------------------------------------------------- ) 
 ) ;standardViaVariants

 customViaVariants(
 ;(viaVariantName viaDefName (paramName paramValue) ...)
 ;( -------------------------------------------------------------------------- )
 ) ;customViaVariants

) ;viaDefs



;********************************
; CONSTRAINT GROUPS
;********************************
constraintGroups(

 ;( group	[override] )
 ;( -----	---------- )
  ( "default"	nil
  ) ;default

 ;( group	[override] )
 ;( -----	---------- )
  ( "virtuosoDefaultExtractorSetup"	nil

    interconnect(
     ( validLayers   (Nwell  Pwell  Oxide  Poly  Cont  Metal1  Via1  Metal2  Via2  Metal3  Via3  Metal4  Via4  Metal5  Via5  Metal6  ) )
     ( validVias     (M1_ISOPWELL  M1_PSUB  M1_PIMP  M1_NWELL  M1_NIMP  M1_POLY1  M2_M1  M3_M2  M4_M3  M5_M4  M6_M5  ) )
     ( errorLayer    noOverlapLayer1 )
     ( errorLayer    noOverlapLayer2 )
    ) ;interconnect
  ) ;virtuosoDefaultExtractorSetup

 ;( group	[override] )
 ;( -----	---------- )
  ( "virtuosoDefaultSetup"	nil

    interconnect(
     ( validLayers   (Nwell  Pwell  Oxide  Poly  Cont  Metal1  Via1  Metal2  Via2  Metal3  Via3  Metal4  Via4  Metal5  Via5  Metal6  ) )
     ( validVias     (M1_ISOPWELL  M1_PSUB  M1_PIMP  M1_NWELL  M1_NIMP  M1_POLY1  M2_M1  M3_M2  M4_M3  M5_M4  M6_M5  ) )
     ( errorLayer    noOverlapLayer1 )
     ( errorLayer    noOverlapLayer2 )
    ) ;interconnect
  ) ;virtuosoDefaultSetup

 ;( group	[override] )
 ;( -----	---------- )
  ( "VLMDefaultSetup"	nil

    interconnect(
     ( validLayers   (Nwell  Pwell  Oxide  Poly  Cont  Metal1  Via1  Metal2  Via2  Metal3  Via3  Metal4  Via4  Metal5  Via5  Metal6  ) )
     ( validVias     (M1_ISOPWELL  M1_PSUB  M1_PIMP  M1_NWELL  M1_NIMP  M1_POLY1  M2_M1  M3_M2  M4_M3  M5_M4  M6_M5  ) )
     ( errorLayer    noOverlapLayer1 )
     ( errorLayer    noOverlapLayer2 )
    ) ;interconnect
  ) ;VLMDefaultSetup

 ;( group	[override] )
 ;( -----	---------- )
  ( "LEFDefaultRouteSpec_gpdk180"	nil

    spacings(
     ( minWidth                   "Cont"	0.2 )
    ) ;spacings

    routingGrids(
     ( horizontalPitch            "Metal1"   0.6 )
     ( verticalPitch              "Metal1"   0.6 )
     ( horizontalOffset           "Metal1"   0.3 )
     ( verticalOffset             "Metal1"   0.3 )
    ) ;routingGrids

    spacings(
     ( minWidth                   "Metal1"	0.3 )
     ( minWidth                   "Via1"	0.2 )
    ) ;spacings

    routingGrids(
     ( horizontalPitch            "Metal2"   0.6 )
     ( verticalPitch              "Metal2"   0.6 )
     ( horizontalOffset           "Metal2"   0.3 )
     ( verticalOffset             "Metal2"   0.3 )
    ) ;routingGrids

    spacings(
     ( minWidth                   "Metal2"	0.3 )
     ( minWidth                   "Via2"	0.2 )
    ) ;spacings

    routingGrids(
     ( horizontalPitch            "Metal3"   0.6 )
     ( verticalPitch              "Metal3"   0.6 )
     ( horizontalOffset           "Metal3"   0.3 )
     ( verticalOffset             "Metal3"   0.3 )
    ) ;routingGrids

    spacings(
     ( minWidth                   "Metal3"	0.3 )
     ( minWidth                   "Via3"	0.2 )
    ) ;spacings

    routingGrids(
     ( horizontalPitch            "Metal4"   0.6 )
     ( verticalPitch              "Metal4"   0.6 )
     ( horizontalOffset           "Metal4"   0.3 )
     ( verticalOffset             "Metal4"   0.3 )
    ) ;routingGrids

    spacings(
     ( minWidth                   "Metal4"	0.3 )
     ( minWidth                   "Via4"	0.2 )
    ) ;spacings

    routingGrids(
     ( horizontalPitch            "Metal5"   0.6 )
     ( verticalPitch              "Metal5"   0.6 )
     ( horizontalOffset           "Metal5"   0.3 )
     ( verticalOffset             "Metal5"   0.3 )
    ) ;routingGrids

    spacings(
     ( minWidth                   "Metal5"	0.3 )
     ( minWidth                   "Via5"	0.2 )
    ) ;spacings

    routingGrids(
     ( horizontalPitch            "Metal6"   0.6 )
     ( verticalPitch              "Metal6"   0.6 )
     ( horizontalOffset           "Metal6"   0.3 )
     ( verticalOffset             "Metal6"   0.3 )
    ) ;routingGrids

    spacings(
     ( minWidth                   "Metal6"	0.3 )
    ) ;spacings

    interconnect(
     ( validLayers   (Metal1  Metal2  Metal3  Metal4  Metal5  Metal6  ) )
     ( validVias     (M2_M1  M3_M2  M4_M3  M5_M4  M6_M5  ) )
    ) ;interconnect
  ) ;LEFDefaultRouteSpec_gpdk180

 ;( group	[override] )
 ;( -----	---------- )
  ( "foundry"	nil

    spacings(
     ( minWidth                   "Nburied"	1.0  'ref  "0A"  'description  "Minimum Nburied Width" )
     ( minSpacing                 "Nburied"	1.0  'ref  "0B"  'description  "Minimum Nburied Space" )
     ( minWidth                   "Nwell"	1.0  'ref  "1A"  'description  "Minimum Nwell Width" )
     ( minSpacing                 "Nwell"	1.0  'ref  "1B"  'description  "Minimum Nwell Space" )
     ( minWidth                   "Pwell"	1.0  'ref  "1D"  'description  "Minimum Pwell Width" )
     ( minSpacing                 "Pwell"	1.0  'ref  "1E"  'description  "Minimum Pwell Space" )
     ( minWidth                   "Oxide"	0.4  'ref  "2A"  'description  "Minimum Oxide Width" )
     ( minSpacing                 "Oxide"	0.3  'ref  "2B"  'description  "Minimum Oxide Space" )
     ( minWidth                   "ThickOxide"	0.5  'ref  "2.5A"  'description  "Minimum ThickOxide Width" )
     ( minSpacing                 "ThickOxide"	0.4  'ref  "2.5B"  'description  "Minimum ThickOxide Space" )
     ( minWidth                   "Nimp"	0.4  'ref  "3A"  'description  "Minimum Nimp Width" )
     ( minSpacing                 "Nimp"	0.4  'ref  "3B"  'description  "Minimum Nimp Space" )
     ( minWidth                   "Pimp"	0.4  'ref  "4A"  'description  "Minimum Pimp Width" )
     ( minSpacing                 "Pimp"	0.4  'ref  "4B"  'description  "Minimum Pimp Space" )
     ( minWidth                   "Poly"	0.18  'ref  "5A"  'description  "Minimum Poly Width" )
     ( minSpacing                 "Poly"	0.3  'ref  "5B"  'description  "Minimum Poly Space" )
     ( minWidth                   "Cont"	0.2  'ref  "6A"  'description  "Minimum Cont Width" )
     ( minSpacing                 "Cont"	0.2  'ref  "6B"  'description  "Minimum Cont Space" )
     ( minWidth                   "Metal1"	0.3  'ref  "7A"  'description  "Minimum Metal1 Width" )
     ( minSpacing                 "Metal1"	0.3  'ref  "7B"  'description  "Minimum Metal1 Space" )
     ( minWidth                   "Via1"	0.2  'ref  "8A"  'description  "Minimum Via1 Width" )
     ( minSpacing                 "Via1"	0.3  'ref  "8B"  'description  "Minimum Via1 Space" )
     ( minWidth                   "Metal2"	0.3  'ref  "9A"  'description  "Minimum Metal2 Width" )
     ( minSpacing                 "Metal2"	0.3  'ref  "9B"  'description  "Minimum Metal2 Space" )
     ( minWidth                   "Via2"	0.2  'ref  "10A"  'description  "Minimum Via2 Width" )
     ( minSpacing                 "Via2"	0.3  'ref  "10B"  'description  "Minimum Via2 Space" )
     ( minWidth                   "Metal3"	0.3  'ref  "11A"  'description  "Minimum Metal3 Width" )
     ( minSpacing                 "Metal3"	0.3  'ref  "11B"  'description  "Minimum Metal3 Space" )
     ( minWidth                   "Via3"	0.2  'ref  "14A"  'description  "Minimum Via3 Width" )
     ( minSpacing                 "Via3"	0.3  'ref  "14B"  'description  "Minimum Via3 Space" )
     ( minWidth                   "Metal4"	0.3  'ref  "15A"  'description  "Minimum Metal4 Width" )
     ( minSpacing                 "Metal4"	0.3  'ref  "15B"  'description  "Minimum Metal4 Space" )
     ( minWidth                   "Via4"	0.2  'ref  "16A"  'description  "Minimum Via4 Width" )
     ( minSpacing                 "Via4"	0.3  'ref  "16B"  'description  "Minimum Via4 Space" )
     ( minWidth                   "Metal5"	0.3  'ref  "17A"  'description  "Minimum Metal5 Width" )
     ( minSpacing                 "Metal5"	0.3  'ref  "17B"  'description  "Minimum Metal5 Space" )
     ( minWidth                   "Via5"	0.2  'ref  "18A"  'description  "Minimum Via5 Width" )
     ( minSpacing                 "Via5"	0.3  'ref  "18B"  'description  "Minimum Via5 Space" )
     ( minWidth                   "Metal6"	0.3  'ref  "19A"  'description  "Minimum Metal6 Width" )
     ( minSpacing                 "Metal6"	0.3  'ref  "19B"  'description  "Minimum Metal6 Space" )
     ( minWidth                   "CapMetal"	0.5  'ref  "12A"  'description  "Minimum CapMetal Width" )
     ( minSpacing                 "CapMetal"	0.4  'ref  "12B"  'description  "Minimum CapMetal Space" )
     ( minWidth                   "Bondpad"	45.0  'ref  "20A"  'description  "Minimum Bondpad Width" )
     ( minSpacing                 "Bondpad"	10.0  'ref  "20B"  'description  "Minimum Bondpad Space" )
     ( minPRBoundaryInteriorHalo  "Nwell"	0.5  'coincidentAllowed )
     ( minPRBoundaryExtension     "Nwell"	0.5 )
     ( minPRBoundaryInteriorHalo  "Pwell"	0.5  'coincidentAllowed )
     ( minPRBoundaryExtension     "Pwell"	0.5 )
     ( minPRBoundaryInteriorHalo  "Oxide"	0.15 )
     ( minPRBoundaryInteriorHalo  "Poly"	0.15 )
     ( minPRBoundaryInteriorHalo  "Pimp"	0.2  'coincidentAllowed )
     ( minPRBoundaryExtension     "Pimp"	0.2 )
     ( minPRBoundaryInteriorHalo  "Nimp"	0.2  'coincidentAllowed )
     ( minPRBoundaryExtension     "Nimp"	0.2 )
     ( minPRBoundaryInteriorHalo  "Cont"	0.1 )
     ( minPRBoundaryInteriorHalo  "Metal1"	0.15  'coincidentAllowed )
     ( minPRBoundaryInteriorHalo  "Via1"	0.15 )
     ( minPRBoundaryInteriorHalo  "Metal2"	0.15 )
     ( minPRBoundaryInteriorHalo  "Via2"	0.15 )
     ( minPRBoundaryInteriorHalo  "Metal3"	0.15 )
     ( minPRBoundaryInteriorHalo  "Via3"	0.15 )
     ( minPRBoundaryInteriorHalo  "Metal4"	0.15 )
     ( minPRBoundaryInteriorHalo  "Via4"	0.15 )
     ( minPRBoundaryInteriorHalo  "Metal5"	0.15 )
     ( minPRBoundaryInteriorHalo  "Via5"	0.15 )
     ( minPRBoundaryInteriorHalo  "Metal6"	0.15 )
     ( minSpacing                 "Nwell"	"Oxide"		0.5  'ref  "2D"  'description  "Minimum Nwell to Oxide Space" )
     ( minSpacing                 "Pwell"	"Oxide"		0.5  'ref  "2D"  'description  "Minimum Pwell to Oxide Space" )
     ( minSpacing                 "ThickOxide"	"Oxide"		0.25  'ref  "2.5D"  'description  "Minimum ThickOxide to Oxide Space" )
     ( minSpacing                 "ThickOxide"	"Poly"		0.4  'ref  "2.5E"  'description  "Minimum ThickOxide to Poly Space" )
     ( minSpacing                 "Poly"	"Oxide"		0.2  'ref  "5E"  'description  "Minimum Poly to Oxide Space" )
     ( minSpacing                 "Cont"	"Poly"		0.2  'ref  "6E"  'description  "Minimum Contact to Poly Space" )
     ( minSpacing                 "Cont"	"Oxide"		0.2  'ref  "6H"  'description  "Minimum Contact to Oxide Space" )
     ( minDensity                 "Poly"	0.15  'ref  "Poly.Density"  'description  "Minimum Poly Density Full Chip is 15%" )
     ( minDensity                 "Metal1"	0.25  'ref  "Metal1.Density"  'description  "Minimum Metal1 Density Full Chip is 25%" )
     ( minDensity                 "Metal2"	0.25  'ref  "Metal2.Density"  'description  "Minimum Metal2 Density Full Chip is 25%" )
     ( minDensity                 "Metal3"	0.25  'ref  "Metal3.Density"  'description  "Minimum Metal3 Density Full Chip is 25%" )
     ( minDensity                 "Metal4"	0.25  'ref  "Metal4.Density"  'description  "Minimum Metal4 Density Full Chip is 25%" )
     ( minDensity                 "Metal5"	0.25  'ref  "Metal5.Density"  'description  "Minimum Metal5 Density Full Chip is 25%" )
     ( minDensity                 "Metal6"	0.25  'ref  "Metal6.Density"  'description  "Minimum Metal6 Density Full Chip is 25%" )
    ) ;spacings

    orderedSpacings(
     ( minEnclosure               "Nburied"	"Nwell"		0.3  'ref  "1C"  'description  "Minimum Nburied enclosure of Nwell" )
     ( minEnclosure               "Nburied"	"Pwell"		0.3  'ref  "1F"  'description  "Minimum Nburied enclosure of Pwell" )
     ( minEnclosure               "Nwell"	"Oxide"		0.5  'ref  "2C"  'description  "Minimum Nwell enclosure of Oxide" )
     ( minEnclosure               "Pwell"	"Oxide"		0.5  'ref  "2C"  'description  "Minimum Pwell enclosure of Oxide" )
     ( minEnclosure               "ThickOxide"	"Oxide"		0.25  'ref  "2.5C"  'description  "Minimum ThickOxide enclosure of Oxide" )
     ( minEnclosure               "ThickOxide"	"Poly"		0.4  'ref  "2.5F"  'description  "Minimum ThickOxide enclosure of Poly" )
     ( minEnclosure               "Nimp"	"Oxide"		0.2  'ref  "3C"  'description  "Minimum Nimp enclosure of Oxide" )
     ( minEnclosure               "Nburied"	"Nimp"		0.6  'ref  "3D"  'description  "Minimum Nburied enclosure of Nimp" )
     ( minEnclosure               "Pimp"	"Oxide"		0.2  'ref  "4C"  'description  "Minimum Pimp enclosure of Oxide" )
     ( minEnclosure               "Nburied"	"Pimp"		0.6  'ref  "4D"  'description  "Minimum Nburied enclosure of Pimp" )
     ( minExtension               "Poly"	"Oxide"		0.2  'ref  "5C"  'description  "Minimum Poly extension over Oxide" )
     ( minExtension               "Oxide"	"Poly"		0.4  'ref  "5D"  'description  "Minimum Oxide extension over Poly" )
     ( minEnclosure               "Oxide"	"Cont"		0.2  'ref  "6C"  'description  "Minimum Oxide enclosure of Contact" )
     ( minEnclosure               "Poly"	"Cont"		0.2  'ref  "6D"  'description  "Minimum Poly enclosure of Contact" )
     ( minEnclosure               "Pimp"	"Cont"		0.1  'ref  "6F"  'description  "Minimum Pimp enclosure of Contact" )
     ( minEnclosure               "Nimp"	"Cont"		0.1  'ref  "6G"  'description  "Minimum Nimp enclosure of Contact" )
     ( minEnclosure               "Metal1"	"Cont"		0.1  'ref  "7C"  'description  "Minimum Metal1 enclosure of Contact" )
     ( minEnclosure               "Metal1"	"Via1"		0.1  'ref  "8C"  'description  "Minimum Metal1 enclosure of Via1" )
     ( minEnclosure               "Metal2"	"Via1"		0.1  'ref  "9C"  'description  "Minimum Metal2 enclosure of Via1" )
     ( minEnclosure               "Metal2"	"Via2"		0.1  'ref  "10C"  'description  "Minimum Metal2 enclosure of Via2" )
     ( minEnclosure               "Metal3"	"Via2"		0.1  'ref  "11C"  'description  "Minimum Metal3 enclosure of Via2" )
     ( minEnclosure               "Metal3"	"Via3"		0.1  'ref  "14C"  'description  "Minimum Metal3 enclosure of Via3" )
     ( minEnclosure               "Metal4"	"Via3"		0.1  'ref  "15C"  'description  "Minimum Metal4 enclosure of Via3" )
     ( minEnclosure               "Metal4"	"Via4"		0.1  'ref  "16C"  'description  "Minimum Metal4 enclosure of Via4" )
     ( minEnclosure               "Metal5"	"Via4"		0.1  'ref  "17C"  'description  "Minimum Metal5 enclosure of Via4" )
     ( minEnclosure               "Metal5"	"Via5"		0.1  'ref  "18C"  'description  "Minimum Metal5 enclosure of Via5" )
     ( minEnclosure               "Metal6"	"Via5"		0.1  'ref  "19C"  'description  "Minimum Metal6 enclosure of Via5" )
     ( minEnclosure               "CapMetal"	"Via2"		0.2  'ref  "12C"  'description  "Minimum CapMetal enclosure of Via2" )
     ( minEnclosure               "Metal3"	"CapVia2"		0.1  'ref  "11D"  'description  "Minimum CapMetal enclosure of Via2" )
     ( minEnclosure               "CapMetal"	"Metal3"		0.3  'ref  "12D"  'description  "Minimum CapMetal enclosure of Metal3" )
     ( minEnclosure               "Metal1"	"Bondpad"		3.0  'ref  "20C"  'description  "Minimum Metal1 enclosure of Bondpad" )
     ( minEnclosure               "Metal2"	"Bondpad"		3.0  'ref  "20D"  'description  "Minimum Metal2 enclosure of Bondpad" )
     ( minEnclosure               "Metal3"	"Bondpad"		3.0  'ref  "20E"  'description  "Minimum Metal3 enclosure of Bondpad" )
     ( minEnclosure               "Metal4"	"Bondpad"		3.0  'ref  "20F"  'description  "Minimum Metal4 enclosure of Bondpad" )
     ( minEnclosure               "Metal5"	"Bondpad"		3.0  'ref  "20G"  'description  "Minimum Metal5 enclosure of Bondpad" )
     ( minEnclosure               "Metal6"	"Bondpad"		3.0  'ref  "20H"  'description  "Minimum Metal6 enclosure of Bondpad" )
    ) ;orderedSpacings

    spacings(
     ( stackable                  "Via1"	"Via2"		t )
     ( stackable                  "Via2"	"Via3"		t )
     ( stackable                  "Via3"	"Via4"		t )
     ( stackable                  "Via4"	"Via5"		t )
    ) ;spacings

    antennaModels(
    ;( model )
    ;( ----- )
     ( "default"
       antenna(
	( areaRatio          "Metal1"     200.0 )
       ) ;antenna
       antenna(
	( areaRatio          "Via1"     20.0 )
       ) ;antenna
       antenna(
	( areaRatio          "Metal2"     200.0 )
       ) ;antenna
       antenna(
	( areaRatio          "Via2"     20.0 )
       ) ;antenna
       antenna(
	( areaRatio          "Metal3"     200.0 )
       ) ;antenna
       antenna(
	( areaRatio          "Via3"     20.0 )
       ) ;antenna
       antenna(
	( areaRatio          "Metal4"     200.0 )
       ) ;antenna
       antenna(
	( areaRatio          "Via4"     20.0 )
       ) ;antenna
       antenna(
	( areaRatio          "Metal5"     200.0 )
       ) ;antenna
       antenna(
	( areaRatio          "Via5"     20.0 )
       ) ;antenna
       antenna(
	( areaRatio          "Metal6"     200.0 )
       ) ;antenna
     ) ;default
    ) ;antennaModels
  ) ;foundry
) ;constraintGroups


;********************************
; DEVICES
;********************************
devices(
tcCreateCDSDeviceClass()

;
; no cdsVia devices
;

;
; no cdsMos devices
;

;
; no cdsResistor devices
;
;
; no ruleContact devices
;


multipartPathTemplates(
; ( name [masterPath] [offsetSubpaths] [encSubPaths] [subRects] )
; 
;   masterPath:
;   (layer [width] [choppable] [endType] [beginExt] [endExt] [justify] [offset]
;   [connectivity])
; 
;   offsetSubpaths:
;   (layer [width] [choppable] [separation] [justification] [begOffset] [endOffset]
;   [connectivity])
; 
;   encSubPaths:
;   (layer [enclosure] [choppable] [separation] [begOffset] [endOffset]
;   [connectivity])
; 
;   subRects:
;   (layer [width] [length] [choppable] [separation] [justification] [space] [begOffset] [endOffset] [gap] 
;   [connectivity] [beginSegOffset] [endSegOffset])
; 
;   connectivity:
;   ([I/O type] [pin] [accDir] [dispPinName] [height] [ layer]
;    [layer] [justification] [font] [textOptions] [orientation]
;    [refHandle] [offset])
; 
; ( --------------------------------------------------------------------- )
  (slotbus 
    (("Metal1" "drawing")	5.0	t	nil	nil	nil	right	1.0)
    ((("Metal1" "drawing")	5.0	t	2.0	right)
    )
    nil
    ((("Metal1" "drawing")	2.0	10.0	t	nil	right	10.0)
    )
  )
  (Nguardring 
    (("Oxide" "drawing")	0.6	nil)
    ((("Metal1" "drawing")	0.4	t	nil	nil	-0.1)
     (("Nimp" "drawing")	1.0	nil	nil	nil	0.2)
     (("Nwell" "drawing")	1.6	nil	nil	nil	0.5)
    )
    nil
    ((("Cont" "drawing")	nil	nil	t	nil	nil	nil	-0.2	-0.2)
    )
  )
  (Pguardring 
    (("Oxide" "drawing")	0.6	nil)
    ((("Metal1" "drawing")	0.4	t	nil	nil	-0.1)
     (("Pimp" "drawing")	1.0	nil	nil	nil	0.2)
    )
    nil
    ((("Cont" "drawing")	nil	nil	t	nil	nil	nil	-0.2	-0.2)
    )
  )
  (bus_x8_metal1 
    (("Metal1" "drawing"))
    ((("Metal1" "drawing")	nil	t	0.6)
     (("Metal1" "drawing")	nil	t	1.2)
     (("Metal1" "drawing")	nil	t	1.8)
     (("Metal1" "drawing")	nil	t	2.4)
     (("Metal1" "drawing")	nil	t	3.0)
     (("Metal1" "drawing")	nil	t	3.6)
     (("Metal1" "drawing")	nil	t	4.2)
    )
    nil
    nil
  )
)  ;multipartPathTemplates


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; Opus Symbolic Device Class Definition
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;
; no other device classes
;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; Opus Symbolic Device Declaration
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; Device Extraction Declaration
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;extractMOS(deviceName  recLayer gateLayer sdLayer bulkLayer [spiceModel])
extractMOS("NMOS15" "ngate15" "Poly" "Oxide" "substrate" "NMOS15")

;extractMOS(deviceName  recLayer gateLayer sdLayer bulkLayer [spiceModel])
extractMOS("PMOS15" "pgate15" "Poly" "Oxide" "Nwell" "PMOS15")

;extractMOS(deviceName  recLayer gateLayer sdLayer bulkLayer [spiceModel])
extractMOS("NMOS25" "ngate25" "Poly" "Oxide" "substrate" "NMOS25")

;extractMOS(deviceName  recLayer gateLayer sdLayer bulkLayer [spiceModel])
extractMOS("PMOS25" "pgate25" "Poly" "Oxide" "Nwell" "PMOS25")


) ;devices


;********************************
; LE RULES
;********************************
leRules(

 leLswLayers(
 ;( layer               purpose         )
 ;( -----               -------         )
 ) ;leLswLayers

) ;leRules


;********************************
; SITEDEFS
;********************************
siteDefs(

 scalarSiteDefs(
 ;( siteDefName          type width  height  symInX symInY symInR90)
 ;( -----------          ---- -----  ------  ------ ------ -------)
 ) ;scalarSiteDefs

 arraySiteDefs(
 ; ( name	type
 ;  ((siteDefName     dx      dy      orientation) ...)
 ;   [symX] [symY] [symR90] )

 ) ;arraySiteDefs

) ;siteDefs


;********************************
; VIASPECS
;********************************

viaSpecs(
 ;(layer1  layer2  (viaDefName ...) 
 ;   [(        
 ;	(layer1MinWidth layer1MaxWidth layer2MinWidth layer2MaxWidth 
 ;            (viaDefName ...)) 
 ;	...         
 ;   )])       
 ;( ------------------------------------------------------------------------ ) 
   ( Metal5  Metal6  ("M6_M5")
   )
   ( Metal4  Metal5  ("M5_M4")
   )
   ( Metal3  Metal4  ("M4_M3")
   )
   ( Metal2  Metal3  ("M3_M2")
   )
   ( Metal1  Metal2  ("M2_M1")
   )
   ( Oxide   Metal1  ("M1_ISOPWELL" "M1_PSUB" "M1_PIMP" "M1_NWELL" "M1_NIMP")
   )
   ( Poly    Metal1  ("M1_POLY1")
   )
) ;viaSpecs
