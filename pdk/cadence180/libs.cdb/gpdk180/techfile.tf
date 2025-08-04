; Technology File gpdk180
; Generated on Aug 15 16:19:38 2005
;     with @(#)$CDS: icfb.exe version 5.1.0 06/29/2005 18:27 (cds125839) $


;********************************
; CONTROLS
;********************************
controls(
 techParams(
 ;( parameter           value             )
 ;( ----------          -----             )
  ( _0A            	1.0 )
  ( _0B            	1.0 )
  ( _1A            	1.0 )
  ( _1B            	1.0 )
  ( _1C            	0.3 )
  ( _1D            	1.0 )
  ( _1E            	1.0 )
  ( _1F            	0.3 )
  ( _2A            	0.4 )
  ( _2B            	0.3 )
  ( _2C            	0.5 )
  ( _2D            	0.5 )
  ( _25A           	0.5 )
  ( _25B           	0.4 )
  ( _25D           	0.25 )
  ( _25E           	0.4 )
  ( _25F           	0.4 )
  ( _25C           	0.25 )
  ( _3A            	0.4 )
  ( _3B            	0.4 )
  ( _3C            	0.2 )
  ( _3D            	0.6 )
  ( _4A            	0.4 )
  ( _4B            	0.4 )
  ( _4C            	0.2 )
  ( _4D            	0.6 )
  ( _5A            	0.18 )
  ( _5B            	0.3 )
  ( _5C            	0.2 )
  ( _5D            	0.4 )
  ( _5E            	0.2 )
  ( _6B            	0.2 )
  ( _6A            	0.2 )
  ( _6C            	0.2 )
  ( _6E            	0.2 )
  ( _6G            	0.1 )
  ( _6H            	0.2 )
  ( _6D            	0.2 )
  ( _6F            	0.1 )
  ( _7A            	0.3 )
  ( _7B            	0.3 )
  ( _7C            	0.1 )
  ( _9A            	0.3 )
  ( _9B            	0.3 )
  ( _9C            	0.1 )
  ( _11A           	0.3 )
  ( _11B           	0.3 )
  ( _11C           	0.1 )
  ( _15A           	0.3 )
  ( _15B           	0.3 )
  ( _15C           	0.1 )
  ( _17A           	0.3 )
  ( _17B           	0.3 )
  ( _17C           	0.1 )
  ( _19A           	0.3 )
  ( _19B           	0.3 )
  ( _19C           	0.1 )
  ( _8B            	0.3 )
  ( _8A            	0.2 )
  ( _8C            	0.1 )
  ( _10B           	0.3 )
  ( _10A           	0.2 )
  ( _10C           	0.1 )
  ( _14B           	0.3 )
  ( _14A           	0.2 )
  ( _14C           	0.1 )
  ( _16B           	0.3 )
  ( _16A           	0.2 )
  ( _16C           	0.1 )
  ( _18B           	0.3 )
  ( _18A           	0.2 )
  ( _18C           	0.1 )
  ( _12D           	0.3 )
  ( _12A           	0.5 )
  ( _12B           	0.4 )
  ( _12C           	0.2 )
  ( _11D           	0.1 )
  ( _20C           	3.0 )
  ( _20D           	3.0 )
  ( _20E           	3.0 )
  ( _20F           	3.0 )
  ( _20G           	3.0 )
  ( _20H           	3.0 )
  ( _20A           	45.0 )
  ( _20B           	10.0 )
  ( _13A1          	10.0 )
  ( _13A2          	10.0 )
  ( _13A3          	10.0 )
  ( maskGrid       	0.005 )
  ( cadGrid        	0.005 )
  ( drcGrid        	0.005 )
  ( mfgGrid        	0.005 )
  ( scale          	1.0 )
  ( LEFDEF_MANUFACTURINGGRID	0.005 )
  ( iccHeader      	"; Translation Rules 2.0 ; Title: icc.rules ; Technology File: gpdk180 ; Creator: Rules Editor 4.4.6.100.101 ; Creation Date: Jul 25 15:22:21 2003 ; From: @(#)$CDS: icfb.exe version 4.4.6 12/20/2002 13:46 (cds11612) $  " )
  ( iccRevision    	"2.0"           )
  ( iccLayers      	((("Oxide" "drawing") "n_diffusion" "off" 0.6 0.3 nil t) (("Poly" "drawing") "polysilicon" "vertical" 0.18 0.3 nil t) (("Cont" "drawing") "cut" "off" 0.2 0.2 nil t) (("Metal1" "drawing") "metal" "orthogonal" 0.3 0.3 nil t) (("Via1" "drawing") "cut" "off" 0.2 0.1 nil t) (("Metal2" "drawing") "metal" "orthogonal" 0.3 0.3 nil t) (("Via2" "drawing") "cut" "off" 0.2 0.1 nil t) (("Metal3" "drawing") "metal" "orthogonal" 0.3 0.3 nil t) (("Via3" "drawing") "cut" "off" 0.2 0.1 nil t) (("Metal4" "drawing") "metal" "orthogonal" 0.3 0.3 nil t) (("Via4" "drawing") "cut" "off" 0.2 0.1 nil t) (("Metal5" "drawing") "metal" "orthogonal" 0.3 0.3 nil t) (("Via5" "drawing") "cut" "off" 0.2 0.1 nil t) (("Metal6" "drawing") "metal" "orthogonal" 0.3 0.3 nil t))	 )
  ( iccVias        	((("gpdk180" "M1_POLY1" "symbolic") t) (("gpdk180" "M2_M1" "symbolic") t) (("gpdk180" "M3_M2" "symbolic") t) (("gpdk180" "M4_M3" "symbolic") t) (("gpdk180" "M5_M4" "symbolic") t) (("gpdk180" "M6_M5" "symbolic") t))	 )
  ( iccEquivalentLayers	((("Poly" "drawing") ("Poly" "boundary") ("Poly" "pin")) (("Cont" "drawing") ("Cont" "boundary")) (("Metal1" "drawing") ("Metal1" "boundary") ("Metal1" "pin")) (("Via1" "drawing") ("Via1" "boundary")) (("Metal2" "drawing") ("Metal2" "boundary") ("Metal2" "pin")) (("Via2" "drawing") ("Via2" "boundary")) (("Metal3" "drawing") ("Metal3" "boundary") ("Metal3" "pin")) (("Via3" "drawing") ("Via3" "boundary")) (("Metal4" "drawing") ("Metal4" "boundary") ("Metal4" "pin")) (("Via4" "drawing") ("Via4" "boundary")) (("Metal5" "drawing") ("Metal5" "boundary") ("Metal5" "pin")) (("Via5" "drawing") ("Via5" "boundary")) (("Metal6" "drawing") ("Metal6" "boundary") ("Metal6" "pin")))	 )
  ( iccBoundaryLayers	((("Oxide" "drawing") ("prBoundary" "drawing") 0.0) (("Poly" "drawing") ("prBoundary" "drawing") 0.0) (("Cont" "drawing") ("prBoundary" "drawing") 0.0) (("Metal1" "drawing") ("prBoundary" "drawing") 0.0) (("Via1" "drawing") ("prBoundary" "drawing") 0.0) (("Metal2" "drawing") ("prBoundary" "drawing") 0.0) (("Via2" "drawing") ("prBoundary" "drawing") 0.0) (("Metal3" "drawing") ("prBoundary" "drawing") 0.0) (("Via3" "drawing") ("prBoundary" "drawing") 0.0) (("Metal4" "drawing") ("prBoundary" "drawing") 0.0) (("Via4" "drawing") ("prBoundary" "drawing") 0.0) (("Metal5" "drawing") ("prBoundary" "drawing") 0.0) (("Via5" "drawing") ("prBoundary" "drawing") 0.0) (("Metal6" "drawing") ("prBoundary" "drawing") 0.0))	 )
  ( iccScopes      	nil	 )
  ( iccKeepouts    	((nil (("or" (("Oxide" "drawing") ("Poly" "drawing")) ("Poly" "drawing") "routing" t) ("=>" (("INDdummy" "drawing")) ("Metal6" "drawing") "routing" t) ("=>" (("INDdummy" "drawing")) ("Metal5" "drawing") "routing" t) ("=>" (("INDdummy" "drawing")) ("Metal4" "drawing") "routing" t) ("=>" (("INDdummy" "drawing")) ("Metal3" "drawing") "routing" t) ("=>" (("INDdummy" "drawing")) ("Metal2" "drawing") "routing" t) ("=>" (("INDdummy" "drawing")) ("Metal1" "drawing") "routing" t) ("=>" (("INDdummy" "drawing")) ("Poly" "drawing") "routing" t) ("=>" (("Capdum" "drawing")) ("Via1" "drawing") "routing" t)) 32))	 )
  ( iccConductors  	((nil (("and" (("Poly" "drawing") ("Oxide" "drawing")) ("Poly" "drawing") "MOSFET" t)) 5))	 )
 ) ;techParams

 viewTypeUnits(
 ;( viewType            userUnit       dbuperuu           )
 ;( --------            --------       --------           )
  ( maskLayout          "micron"        2000            )
  ( schematic           "inch"          160             )
  ( schematicSymbol     "inch"          160             )
  ( netlist             "inch"          160             )
 ) ;viewTypeUnits

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
  ( grid                      11         grd          )
  ( ppath                     12         pp0          )
  ( nwell                     13         nwl          )
  ( nwelld                    14         nwld         )
  ( tpwell                    15         tpwl         )
  ( fill                      16         fil          )
  ( silicon                   20         si           )
  ( vlc                       21         vlc          )
  ( Metal1                    22         M1           )
  ( Metal2                    23         M2           )
  ( Metal3                    24         M3           )
  ( Metal4                    25         M4           )
  ( Metal5                    26         M5           )
  ( Metal6                    27         M6           )
 ;System-Reserved Purposes:
  ( warning                   234        wng          )
  ( tool1                     235        tl1          )
  ( tool0                     236        tl0          )
  ( label                     237        lbl          )
  ( flight                    238        flt          )
  ( error                     239        err          )
  ( annotate                  240        ant          )
  ( drawing1                  241        dr1          )
  ( drawing2                  242        dr2          )
  ( drawing3                  243        dr3          )
  ( drawing4                  244        dr4          )
  ( drawing5                  245        dr5          )
  ( drawing6                  246        dr6          )
  ( drawing7                  247        dr7          )
  ( drawing8                  248        dr8          )
  ( drawing9                  249        dr9          )
  ( boundary                  250        bnd          )
  ( pin                       251        pin          )
  ( drawing                   252        drw          )
  ( net                       253        net          )
  ( cell                      254        cel          )
  ( all                       255        all          )
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
  ( Unrouted                  200        Unroute      )
  ( Row                       201        Row          )
  ( Group                     202        Group        )
  ( Cannotoccupy              203        noOcupy      )
  ( Canplace                  204        Canplac      )
  ( hardFence                 205        hardFnc      )
  ( softFence                 206        softFnc      )
  ( y0                        207        y0           )
  ( y1                        208        y1           )
  ( y2                        209        y2           )
  ( y3                        210        y3           )
  ( y4                        211        y4           )
  ( y5                        212        y5           )
  ( y6                        213        y6           )
  ( y7                        214        y7           )
  ( y8                        215        y8           )
  ( y9                        216        y9           )
  ( designFlow                217        dsnFlow      )
  ( stretch                   218        stretch      )
  ( edgeLayer                 219        edgeLyr      )
  ( changedLayer              220        chngLyr      )
  ( unset                     221        unset        )
  ( unknown                   222        unknown      )
  ( spike                     223        spike        )
  ( hiz                       224        hiz          )
  ( resist                    225        resist       )
  ( drive                     226        drive        )
  ( supply                    227        supply       )
  ( wire                      228        wire         )
  ( pin                       229        pin          )
  ( text                      230        text         )
  ( device                    231        device       )
  ( border                    232        border       )
  ( snap                      233        snap         )
  ( align                     234        align        )
  ( prBoundary                235        prBndry      )
  ( instance                  236        instnce      )
  ( annotate                  237        anotate      )
  ( marker                    238        marker       )
  ( select                    239        select       )
  ( grid                      251        grid         )
  ( axis                      252        axis         )
  ( hilite                    253        hilite       )
  ( background                254        bkground     )
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
  ( Nimp                      drawing    )
  ( Pimp                      drawing    )
  ( Cont                      drawing    )
  ( Metal1                    drawing    )
  ( Via1                      drawing    )
  ( Metal2                    drawing    )
  ( CapMetal                  drawing    )
  ( Via2                      drawing    )
  ( Metal3                    drawing    )
  ( Via3                      drawing    )
  ( Metal4                    drawing    )
  ( Via4                      drawing    )
  ( Metal5                    drawing    )
  ( Via5                      drawing    )
  ( Metal6                    drawing    )
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
  ( Metal1                    fill       )
  ( Metal2                    fill       )
  ( Metal3                    fill       )
  ( Metal4                    fill       )
  ( Metal5                    fill       )
  ( Metal6                    fill       )
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
  ( Metal2                    drawing4   )
  ( Metal2                    net        )
  ( Metal2                    boundary   )
  ( Via2                      pin        )
  ( Via2                      label      )
  ( Via2                      drawing4   )
  ( Via2                      net        )
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
  ( marker                    warning    )
  ( marker                    error      )
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
  ( Nimp         drawing      nplus            t t t t t )
  ( Pimp         drawing      pplus            t t t t t )
  ( Cont         drawing      cw               t t t t t )
  ( Metal1       drawing      m1               t t t t t )
  ( Via1         drawing      v1               t t t t t )
  ( Metal2       drawing      m2               t t t t t )
  ( CapMetal     drawing      m4               t t t t t )
  ( Via2         drawing      v2               t t t t t )
  ( Metal3       drawing      m3               t t t t t )
  ( Via3         drawing      v3               t t t t t )
  ( Metal4       drawing      m4               t t t t t )
  ( Via4         drawing      v4               t t t t t )
  ( Metal5       drawing      m5               t t t t t )
  ( Via5         drawing      v5               t t t t t )
  ( Metal6       drawing      m6               t t t t t )
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
  ( Metal1       fill         Metal1_fill      t t t t nil )
  ( Metal2       fill         Metal2_fill      t t t t nil )
  ( Metal3       fill         Metal3_fill      t t t t nil )
  ( Metal4       fill         Metal4_fill      t t t t nil )
  ( Metal5       fill         Metal5_fill      t t t t nil )
  ( Metal6       fill         Metal6_fill      t t t t nil )
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
  ( Metal2       drawing4     m2               t t nil t nil )
  ( Metal2       net          m2Net            t t nil t nil )
  ( Metal2       boundary     m2Bnd            t t nil t nil )
  ( Via2         pin          v2               t t nil t nil )
  ( Via2         label        v2               t t nil t nil )
  ( Via2         drawing4     v2               t t nil t nil )
  ( Via2         net          v2Net            t t nil t nil )
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
  ( marker       warning      markerWarn       t t nil t nil )
  ( marker       error        markerErr        t t nil t nil )
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
 ( iccMaskNumber          (Poly              drawing )   0 )
 ( iccMaskNumber          (Cont              drawing )   0 )
 ( iccMaskNumber          (Metal1            drawing )   0 )
 ( iccMaskNumber          (Via1              drawing )   0 )
 ( iccMaskNumber          (Metal2            drawing )   0 )
 ( iccMaskNumber          (Via2              drawing )   0 )
 ( iccMaskNumber          (Metal3            drawing )   0 )
 ( iccMaskNumber          (Via3              drawing )   0 )
 ( iccMaskNumber          (Metal4            drawing )   0 )
 ( iccMaskNumber          (Via4              drawing )   0 )
 ( iccMaskNumber          (Metal5            drawing )   0 )
 ( iccMaskNumber          (Via5              drawing )   0 )
 ( iccMaskNumber          (Metal6            drawing )   0 )
)

) ;layerDefinitions


;********************************
; LAYER RULES
;********************************
layerRules(

 streamLayers(
 ;( layer       streamNumber    dataType        translate )
 ;( -----       ------------    --------        --------- )
  ( ("Metal1" "label")	7         	3       	t	 )
  ( ("Metal1" "drawing4")	7         	4       	t	 )
  ( ("Metal1" "fill")	7         	5       	t	 )
  ( ("Metal1" "drawing")	7         	0       	t	 )
  ( ("Metal1" "pin")	7         	1       	t	 )
  ( ("Metal1" "net")	7         	2       	t	 )
  ( ("Via1" "label")	8         	3       	t	 )
  ( ("Via1" "pin")	8         	1       	t	 )
  ( ("Via1" "drawing4")	8         	4       	t	 )
  ( ("Via1" "drawing")	8         	0       	t	 )
  ( ("Metal2" "label")	9         	3       	t	 )
  ( ("Metal2" "drawing4")	9         	4       	t	 )
  ( ("Metal2" "fill")	9         	5       	t	 )
  ( ("Metal2" "drawing")	9         	0       	t	 )
  ( ("Metal2" "pin")	9         	1       	t	 )
  ( ("Metal2" "net")	9         	2       	t	 )
  ( ("Via2" "pin")	10        	1       	t	 )
  ( ("Via2" "label")	10        	3       	t	 )
  ( ("Via2" "drawing4")	10        	4       	t	 )
  ( ("Via2" "drawing")	10        	0       	t	 )
  ( ("Metal3" "label")	11        	3       	t	 )
  ( ("Metal3" "drawing4")	11        	4       	t	 )
  ( ("Metal3" "fill")	11        	5       	t	 )
  ( ("Metal3" "drawing")	11        	0       	t	 )
  ( ("Metal3" "pin")	11        	1       	t	 )
  ( ("Metal3" "net")	11        	2       	t	 )
  ( ("Via3" "pin")	30        	1       	t	 )
  ( ("Via3" "label")	30        	3       	t	 )
  ( ("Via3" "drawing4")	30        	4       	t	 )
  ( ("Via3" "drawing")	30        	0       	t	 )
  ( ("Metal4" "label")	31        	3       	t	 )
  ( ("Metal4" "drawing4")	31        	4       	t	 )
  ( ("Metal4" "fill")	31        	5       	t	 )
  ( ("Metal4" "drawing")	31        	0       	t	 )
  ( ("Metal4" "pin")	31        	1       	t	 )
  ( ("Metal4" "net")	31        	2       	t	 )
  ( ("Via4" "pin")	32        	1       	t	 )
  ( ("Via4" "label")	32        	3       	t	 )
  ( ("Via4" "drawing4")	32        	4       	t	 )
  ( ("Via4" "drawing")	32        	0       	t	 )
  ( ("Metal5" "label")	33        	3       	t	 )
  ( ("Metal5" "drawing4")	33        	4       	t	 )
  ( ("Metal5" "fill")	33        	5       	t	 )
  ( ("Metal5" "drawing")	33        	0       	t	 )
  ( ("Metal5" "pin")	33        	1       	t	 )
  ( ("Metal5" "net")	33        	2       	t	 )
  ( ("Via5" "pin")	34        	1       	t	 )
  ( ("Via5" "label")	34        	3       	t	 )
  ( ("Via5" "drawing4")	34        	4       	t	 )
  ( ("Via5" "drawing")	34        	0       	t	 )
  ( ("Metal6" "label")	35        	3       	t	 )
  ( ("Metal6" "drawing4")	35        	4       	t	 )
  ( ("Metal6" "fill")	35        	5       	t	 )
  ( ("Metal6" "drawing")	35        	0       	t	 )
  ( ("Metal6" "pin")	35        	1       	t	 )
  ( ("Metal6" "net")	35        	2       	t	 )
  ( ("CapMetal" "drawing")	14        	0       	t	 )
  ( ("Cont" "drawing")	6         	0       	t	 )
  ( ("Poly" "label")	3         	3       	t	 )
  ( ("Poly" "drawing4")	3         	4       	t	 )
  ( ("Poly" "drawing")	3         	0       	t	 )
  ( ("Poly" "pin")	3         	1       	t	 )
  ( ("Poly" "net")	3         	2       	t	 )
  ( ("Nwell" "drawing")	2         	0       	t	 )
  ( ("Pwell" "drawing")	18        	0       	t	 )
  ( ("Oxide" "drawing")	1         	0       	t	 )
  ( ("ThickOxide" "drawing")	24        	0       	t	 )
  ( ("Nburied" "drawing")	19        	0       	t	 )
  ( ("Nimp" "drawing")	4         	0       	t	 )
  ( ("Pimp" "drawing")	5         	0       	t	 )
  ( ("SiProt" "drawing")	72        	0       	t	 )
  ( ("Bondpad" "drawing")	36        	0       	t	 )
  ( ("Capdum" "drawing")	12        	0       	t	 )
  ( ("INDdummy" "drawing")	16        	0       	t	 )
  ( ("IND2dummy" "drawing")	17        	0       	t	 )
  ( ("IND3dummy" "drawing")	70        	0       	t	 )
  ( ("RFdummy" "drawing")	69        	0       	t	 )
  ( ("ResWdum" "drawing")	71        	0       	t	 )
  ( ("Resdum" "drawing")	13        	0       	t	 )
  ( ("M1dummy" "drawing")	37        	0       	t	 )
  ( ("M2dummy" "drawing")	38        	0       	t	 )
  ( ("M3dummy" "drawing")	39        	0       	t	 )
  ( ("M4dummy" "drawing")	40        	0       	t	 )
  ( ("M5dummy" "drawing")	41        	0       	t	 )
  ( ("M6dummy" "drawing")	42        	0       	t	 )
  ( ("BJTdum" "drawing")	15        	0       	t	 )
  ( ("NPNdummy" "drawing")	20        	0       	t	 )
  ( ("PNPdummy" "drawing")	21        	0       	t	 )
  ( ("DIOdummy" "drawing")	22        	0       	t	 )
  ( ("Psubiso" "drawing")	51        	0       	t	 )
  ( ("allGeoShare" "drawing")	100       	1       	t	 )
  ( ("allGeoShare" "GeoShare")	100       	0       	t	 )
  ( ("OVERLAP" "drawing")	101       	0       	t	 )
  ( ("OVERLAP" "label")	101       	3       	t	 )
  ( ("OVERLAP" "boundary")	101       	5       	t	 )
  ( ("prBoundary" "drawing")	235       	0       	t	 )
  ( ("prBoundary" "boundary")	235       	5       	t	 )
  ( ("text" "drawing")	230       	0       	t	 )
  ( ("text" "label")	230       	3       	t	 )
  ( ("JVAR1dummy" "drawing")	43        	0       	t	 )
  ( ("JVAR2dummy" "drawing")	44        	0       	t	 )
  ( ("JVAR3dummy" "drawing")	48        	0       	t	 )
  ( ("SNA" "nwelld")	0         	0       	t	 )
  ( ("SNA" "tpwell")	0         	0       	t	 )
  ( ("text" "vlc")	116       	0       	t	 )
  ( ("INDdumVlcRF" "silicon")	102       	0       	t	 )
  ( ("vlcdummy" "drawing")	104       	0       	t	 )
  ( ("vlccn" "drawing")	103       	0       	t	 )
  ( ("vlcdummy" "Metal1")	104       	1       	t	 )
  ( ("vlccn" "Metal1")	103       	1       	t	 )
  ( ("vlcdummy" "Metal2")	104       	2       	t	 )
  ( ("vlccn" "Metal2")	103       	2       	t	 )
  ( ("vlcdummy" "Metal3")	104       	3       	t	 )
  ( ("vlccn" "Metal3")	103       	3       	t	 )
  ( ("vlcdummy" "Metal4")	104       	4       	t	 )
  ( ("vlccn" "Metal4")	103       	4       	t	 )
  ( ("vlcdummy" "Metal5")	104       	5       	t	 )
  ( ("vlccn" "Metal5")	103       	5       	t	 )
  ( ("vlcdummy" "Metal6")	104       	6       	t	 )
  ( ("vlccn" "Metal6")	103       	6       	t	 )
 ) ;streamLayers

 viaLayers(
 ;( layer1      viaLayer        layer2     )
 ;( ------      --------        ------     )
  ( Poly      	Cont      	Metal1     )
  ( Oxide     	Cont      	Metal1     )
  ( Metal1    	Via1      	Metal2     )
  ( Metal2    	Via2      	Metal3     )
  ( Metal3    	Via3      	Metal4     )
  ( Metal4    	Via4      	Metal5     )
  ( Metal5    	Via5      	Metal6     )
 ) ;viaLayers

 layerFunctions(
 ;( layer                       function        [maskNumber])
 ;( -----                       --------        ------------)
  ( Oxide                    	"ndiff"      )
  ( Poly                     	"poly"       )
  ( Cont                     	"cut"        )
  ( Metal1                   	"metal"      )
  ( Via1                     	"cut"        )
  ( Metal2                   	"metal"      )
  ( Via2                     	"cut"        )
  ( Metal3                   	"metal"      )
  ( Via3                     	"cut"        )
  ( Metal4                   	"metal"      )
  ( Via4                     	"cut"        )
  ( Metal5                   	"metal"      )
  ( Via5                     	"cut"        )
  ( Metal6                   	"metal"      )
  ( Nwell                    	"nwell"      )
  ( Pwell                    	"pwell"      )
  ( Nburied                  	"nplus"      )
 ) ;layerFunctions

) ;layerRules


;********************************
; PHYSICAL RULES
;********************************
physicalRules(

 spacingRules(
 ;( rule                	layer1    	layer2    	value    )
 ;( ----                	------    	------    	-----    )
  ( minWidth            	("Metal1" "drawing")			0.3	 )
  ( minNotch            	("Metal1" "drawing")			0.3	 )
  ( minSpacing          	("Metal1" "drawing")			0.3	 )
  ( minWidth            	("Via1" "drawing")			0.2	 )
  ( minNotch            	("Via1" "drawing")			0.3	 )
  ( minSpacing          	("Via1" "drawing")			0.3	 )
  ( minWidth            	("Metal2" "drawing")			0.3	 )
  ( minNotch            	("Metal2" "drawing")			0.3	 )
  ( minSpacing          	("Metal2" "drawing")			0.3	 )
  ( minWidth            	("Via2" "drawing")			0.2	 )
  ( minNotch            	("Via2" "drawing")			0.3	 )
  ( minSpacing          	("Via2" "drawing")			0.3	 )
  ( minWidth            	("Metal3" "drawing")			0.3	 )
  ( minNotch            	("Metal3" "drawing")			0.3	 )
  ( minSpacing          	("Metal3" "drawing")			0.3	 )
  ( minWidth            	("Via3" "drawing")			0.2	 )
  ( minNotch            	("Via3" "drawing")			0.3	 )
  ( minSpacing          	("Via3" "drawing")			0.3	 )
  ( minWidth            	("Metal4" "drawing")			0.3	 )
  ( minNotch            	("Metal4" "drawing")			0.3	 )
  ( minSpacing          	("Metal4" "drawing")			0.3	 )
  ( minWidth            	("Via4" "drawing")			0.2	 )
  ( minNotch            	("Via4" "drawing")			0.3	 )
  ( minSpacing          	("Via4" "drawing")			0.3	 )
  ( minWidth            	("Metal5" "drawing")			0.3	 )
  ( minNotch            	("Metal5" "drawing")			0.3	 )
  ( minSpacing          	("Metal5" "drawing")			0.3	 )
  ( minWidth            	("Via5" "drawing")			0.2	 )
  ( minNotch            	("Via5" "drawing")			0.3	 )
  ( minSpacing          	("Via5" "drawing")			0.3	 )
  ( minWidth            	("Metal6" "drawing")			0.3	 )
  ( minNotch            	("Metal6" "drawing")			0.3	 )
  ( minSpacing          	("Metal6" "drawing")			0.3	 )
  ( minWidth            	("CapMetal" "drawing")			0.5	 )
  ( minWidth            	("Cont" "drawing")			0.2	 )
  ( minNotch            	("Cont" "drawing")			0.2	 )
  ( minSpacing          	("Cont" "drawing")			0.2	 )
  ( minWidth            	("Poly" "drawing")			0.18	 )
  ( minNotch            	("Poly" "drawing")			0.3	 )
  ( minSpacing          	("Poly" "drawing")			0.3	 )
  ( minWidth            	("Nwell" "drawing")			1.0	 )
  ( minNotch            	("Nwell" "drawing")			1.0	 )
  ( minSpacing          	("Nwell" "drawing")			1.0	 )
  ( minWidth            	("Pwell" "drawing")			1.0	 )
  ( minNotch            	("Pwell" "drawing")			1.0	 )
  ( minSpacing          	("Pwell" "drawing")			1.0	 )
  ( minWidth            	("Oxide" "drawing")			0.4	 )
  ( minNotch            	("Oxide" "drawing")			0.3	 )
  ( minSpacing          	("Oxide" "drawing")			0.3	 )
  ( minWidth            	("ThickOxide" "drawing")			0.5	 )
  ( minNotch            	("ThickOxide" "drawing")			0.4	 )
  ( minSpacing          	("ThickOxide" "drawing")			0.4	 )
  ( minWidth            	("Nburied" "drawing")			1.0	 )
  ( minNotch            	("Nburied" "drawing")			1.0	 )
  ( minSpacing          	("Nburied" "drawing")			1.0	 )
  ( minWidth            	("Nimp" "drawing")			0.4	 )
  ( minNotch            	("Nimp" "drawing")			0.4	 )
  ( minSpacing          	("Nimp" "drawing")			0.4	 )
  ( minWidth            	("Pimp" "drawing")			0.4	 )
  ( minNotch            	("Pimp" "drawing")			0.4	 )
  ( minSpacing          	("Pimp" "drawing")			0.4	 )
  ( minWidth            	("Bondpad" "drawing")			45.0	 )
  ( minNotch            	("Bondpad" "drawing")			10.0	 )
  ( minSpacing          	("Bondpad" "drawing")			10.0	 )
  ( minWidth            	"CapMetal"			0.5	 )
  ( minSpacing          	"Cont"			0.2	 )
  ( minWidth            	"Cont"			0.2	 )
  ( minSpacingRange     	"Metal1"			("0.600 RANGE   10.000 100000.000")	 )
  ( minSpacing          	"Metal1"			0.3	 )
  ( minWidth            	"Metal1"			0.3	 )
  ( offset              	"Metal1"			0.33	 )
  ( minSpacingRange     	"Metal2"			("0.600 RANGE   10.000 100000.000")	 )
  ( minSpacing          	"Metal2"			0.3	 )
  ( minWidth            	"Metal2"			0.3	 )
  ( offset              	"Metal2"			0.33	 )
  ( minSpacingRange     	"Metal3"			("0.600 RANGE   10.000 100000.000")	 )
  ( minSpacing          	"Metal3"			0.3	 )
  ( minWidth            	"Metal3"			0.3	 )
  ( offset              	"Metal3"			0.33	 )
  ( minSpacingRange     	"Metal4"			("0.600 RANGE   10.000 100000.000")	 )
  ( minSpacing          	"Metal4"			0.3	 )
  ( minWidth            	"Metal4"			0.3	 )
  ( offset              	"Metal4"			0.33	 )
  ( minSpacingRange     	"Metal5"			("0.600 RANGE   10.000 100000.000")	 )
  ( minSpacing          	"Metal5"			0.3	 )
  ( minWidth            	"Metal5"			0.3	 )
  ( offset              	"Metal5"			0.33	 )
  ( minSpacingRange     	"Metal6"			("0.600 RANGE   10.000 100000.000")	 )
  ( minSpacing          	"Metal6"			0.3	 )
  ( minWidth            	"Metal6"			0.3	 )
  ( offset              	"Metal6"			0.33	 )
  ( minSpacing          	"Nimp"			0.4	 )
  ( minWidth            	"Nimp"			0.4	 )
  ( minSpacing          	"Nwell"			1.0	 )
  ( minWidth            	"Nwell"			1.0	 )
  ( minSpacing          	"Pwell"			1.0	 )
  ( minWidth            	"Pwell"			1.0	 )
  ( minNotch            	"Oxide"			0.3	 )
  ( minSpacing          	"Oxide"			0.3	 )
  ( minWidth            	"Oxide"			0.4	 )
  ( minSpacing          	"Pimp"			0.4	 )
  ( minWidth            	"Pimp"			0.4	 )
  ( minWidth            	"Poly"			0.18	 )
  ( minExtension        	"Poly"			0.2	 )
  ( minNotch            	"Poly"			0.3	 )
  ( minSpacing          	"Poly"			0.3	 )
  ( minWidth            	"Via1"			0.2	 )
  ( minSpacing          	"Via1"			0.3	 )
  ( minWidth            	"Via2"			0.2	 )
  ( minSpacing          	"Via2"			0.3	 )
  ( minWidth            	"Via3"			0.2	 )
  ( minSpacing          	"Via3"			0.3	 )
  ( minWidth            	"Via4"			0.2	 )
  ( minSpacing          	"Via4"			0.3	 )
  ( minWidth            	"Via5"			0.2	 )
  ( minSpacing          	"Via5"			0.3	 )
  ( minSpacing          	("Cont" "drawing")		("Poly" "drawing")		0.2	 )
  ( minSpacing          	("Cont" "drawing")		("Oxide" "drawing")		0.2	 )
  ( minSpacing          	("Poly" "drawing")		("Oxide" "drawing")		0.2	 )
  ( minSpacing          	("Poly" "drawing")		("ThickOxide" "drawing")		0.4	 )
  ( minSpacing          	("Nwell" "drawing")		("Oxide" "drawing")		0.5	 )
  ( minSpacing          	("Pwell" "drawing")		("Oxide" "drawing")		0.5	 )
  ( minSpacing          	("Oxide" "drawing")		("ThickOxide" "drawing")		0.25	 )
  ( sameNet             	"Metal1"		"Metal1"		0.3	 )
  ( sameNet             	"Metal2"		"Metal2"		0.3	 )
  ( sameNet             	"Metal3"		"Metal3"		0.3	 )
  ( sameNet             	"Metal4"		"Metal4"		0.3	 )
  ( sameNet             	"Metal5"		"Metal5"		0.3	 )
  ( sameNet             	"Metal6"		"Metal6"		0.3	 )
  ( minSpacing          	"Oxide"		"Poly"		0.2	 )
  ( minSpacing          	"Poly"		"Cont"		0.2	 )
  ( minOverlap          	"Poly"		"Oxide"		0.2	 )
  ( sameNet             	"Via1"		"Via2"		0.0	 )
  ( sameNet             	"Via1"		"Via1"		0.3	 )
  ( sameNet             	"Via2"		"Via3"		0.0	 )
  ( sameNet             	"Via2"		"Via2"		0.3	 )
  ( sameNet             	"Via3"		"Via4"		0.0	 )
  ( sameNet             	"Via3"		"Via3"		0.3	 )
  ( sameNet             	"Via4"		"Via5"		0.0	 )
  ( sameNet             	"Via4"		"Via4"		0.3	 )
  ( sameNet             	"Via5"		"Via5"		0.3	 )
 ) ;spacingRules

 mfgGridResolution(
      ( 0.005000 )
 ) ;mfgGridResolution

 orderedSpacingRules(
 ;( rule                	layer1    	layer2    	value    )
 ;( ----                	------    	------    	-----    )
  ( minEnclosure        	"Nwell"		"Oxide"		0.5	 )
  ( minEnclosure        	"Oxide"		"Poly"		0.4	 )
  ( minEnclosure        	"Oxide"		"Cont"		0.2	 )
  ( minEnclosure        	"Nimp"		"Oxide"		0.2	 )
  ( minEnclosure        	"Pimp"		"Oxide"		0.2	 )
  ( minEnclosure        	"CapMetal"		"Via2"		0.2	 )
  ( minEnclosure        	"Poly"		"Oxide"		0.2	 )
  ( minEnclosure        	"Poly"		"Cont"		0.2	 )
  ( minEnclosure        	"Metal1"		"Cont"		0.1	 )
  ( minEnclosure        	"Metal1"		"Via1"		0.1	 )
  ( minEnclosure        	"Metal2"		"Via1"		0.1	 )
  ( minEnclosure        	"Metal2"		"Via2"		0.1	 )
  ( minEnclosure        	"Metal3"		"Via2"		0.1	 )
  ( minEnclosure        	"Metal3"		"Via3"		0.1	 )
  ( minEnclosure        	"Metal4"		"Via3"		0.1	 )
  ( minEnclosure        	"Metal4"		"Via4"		0.1	 )
  ( minEnclosure        	"Metal5"		"Via4"		0.1	 )
  ( minEnclosure        	"Metal5"		"Via5"		0.1	 )
  ( minEnclosure        	"Metal6"		"Via5"		0.1	 )
 ) ;orderedSpacingRules

) ;physicalRules


;********************************
; ELECTRICAL RULES
;********************************
electricalRules(

 characterizationRules(
 ;( rule                	layer1    	layer2    	value    )
 ;( ----                	------    	------    	-----    )
  ( sheetRes            	"Nimp"			300	 )
  ( sheetRes            	"Poly"			7.5	 )
  ( contactRes          	"Poly"			0	 )
  ( contactRes          	"Oxide"			0	 )
  ( sheetRes            	"Oxide"			300	 )
  ( sheetRes            	"Metal1"			0.101	 )
  ( areaCap             	"Metal1"			0.000132	 )
  ( edgeCapacitance     	"Metal1"			0.0	 )
  ( edgeCap             	"Metal1"			8.8e-05	 )
  ( sheetRes            	"Metal2"			0.101	 )
  ( areaCap             	"Metal2"			7e-05	 )
  ( edgeCapacitance     	"Metal2"			0.0	 )
  ( edgeCap             	"Metal2"			8.3e-05	 )
  ( sheetRes            	"Metal3"			0.101	 )
  ( areaCap             	"Metal3"			6.3e-05	 )
  ( edgeCapacitance     	"Metal3"			0.0	 )
  ( edgeCap             	"Metal3"			0.0001	 )
  ( sheetRes            	"Metal4"			0.101	 )
  ( areaCap             	"Metal4"			5.4e-05	 )
  ( edgeCapacitance     	"Metal4"			0.0	 )
  ( edgeCap             	"Metal4"			8.3e-05	 )
  ( sheetRes            	"Metal5"			0.045	 )
  ( areaCap             	"Metal5"			3.1e-05	 )
  ( edgeCapacitance     	"Metal5"			0.0	 )
  ( edgeCap             	"Metal5"			0.000102	 )
  ( sheetRes            	"Metal6"			0.045	 )
  ( areaCap             	"Metal6"			3.1e-05	 )
  ( edgeCapacitance     	"Metal6"			0.0	 )
  ( edgeCap             	"Metal6"			0.000102	 )
 ) ;characterizationRules

 orderedCharacterizationRules(
 ;( rule                	layer1    	layer2    	value    )
 ;( ----                	------    	------    	-----    )
  ( areaCap             	"Poly"		"Nwell"		100	 )
  ( edgeCapacitance     	"Poly"		"Nwell"		50	 )
  ( areaCap             	"Metal1"		"Nwell"		30	 )
  ( edgeCapacitance     	"Metal1"		"Nwell"		35	 )
  ( edgeCapacitance     	"Metal1"		"Oxide"		45	 )
  ( areaCap             	"Metal1"		"Oxide"		40	 )
  ( areaCap             	"Metal1"		"Poly"		65	 )
  ( edgeCapacitance     	"Metal1"		"Poly"		60	 )
  ( areaCap             	"Metal2"		"Nwell"		15	 )
  ( edgeCapacitance     	"Metal2"		"Nwell"		25	 )
  ( edgeCapacitance     	"Metal2"		"Oxide"		27	 )
  ( areaCap             	"Metal2"		"Oxide"		18	 )
  ( areaCap             	"Metal2"		"Poly"		17.5	 )
  ( edgeCapacitance     	"Metal2"		"Poly"		30	 )
  ( edgeCapacitance     	"Metal2"		"Metal1"		45	 )
  ( areaCap             	"Metal2"		"Metal1"		35	 )
  ( edgeCapacitance     	"Metal3"		"Nwell"		20	 )
  ( areaCap             	"Metal3"		"Nwell"		10	 )
  ( areaCap             	"Metal3"		"Oxide"		12.5	 )
  ( edgeCapacitance     	"Metal3"		"Oxide"		22.5	 )
  ( edgeCapacitance     	"Metal3"		"Metal1"		25.5	 )
  ( areaCap             	"Metal3"		"Metal1"		15.5	 )
  ( areaCap             	"Metal3"		"Metal2"		35.5	 )
  ( edgeCapacitance     	"Metal3"		"Metal2"		45.5	 )
  ( areaCap             	"Metal4"		"Nwell"		5	 )
  ( areaCap             	"Metal4"		"Oxide"		6.5	 )
  ( areaCap             	"Metal4"		"Poly"		7	 )
  ( areaCap             	"Metal4"		"Metal1"		9	 )
  ( areaCap             	"Metal4"		"Metal2"		15	 )
  ( areaCap             	"Metal4"		"Metal3"		40	 )
  ( areaCap             	"Metal5"		"Nwell"		5	 )
  ( areaCap             	"Metal5"		"Oxide"		5.5	 )
  ( areaCap             	"Metal5"		"Poly"		5.5	 )
  ( areaCap             	"Metal5"		"Metal1"		8	 )
  ( areaCap             	"Metal5"		"Metal2"		9.5	 )
  ( areaCap             	"Metal5"		"Metal3"		15	 )
  ( areaCap             	"Metal5"		"Metal4"		40.5	 )
  ( areaCap             	"Metal6"		"Nwell"		4.5	 )
  ( areaCap             	"Metal6"		"Oxide"		6	 )
  ( areaCap             	"Metal6"		"Poly"		6.5	 )
  ( areaCap             	"Metal6"		"Metal1"		8	 )
  ( areaCap             	"Metal6"		"Metal2"		10	 )
  ( areaCap             	"Metal6"		"Metal3"		17	 )
  ( areaCap             	"Metal6"		"Metal4"		18	 )
  ( areaCap             	"Metal6"		"Metal5"		50	 )
  ( edgeCapacitance     	"Metal4"		"Nwell"		20	 )
  ( edgeCapacitance     	"Metal4"		"Oxide"		32.5	 )
  ( edgeCapacitance     	"Metal4"		"Poly"		18.5	 )
  ( edgeCapacitance     	"Metal4"		"Metal1"		46	 )
  ( edgeCapacitance     	"Metal4"		"Metal2"		47.5	 )
  ( edgeCapacitance     	"Metal4"		"Metal3"		60	 )
  ( edgeCapacitance     	"Metal5"		"Nwell"		18.5	 )
  ( edgeCapacitance     	"Metal5"		"Oxide"		28	 )
  ( edgeCapacitance     	"Metal5"		"Poly"		17	 )
  ( edgeCapacitance     	"Metal5"		"Metal1"		47.5	 )
  ( edgeCapacitance     	"Metal5"		"Metal2"		49	 )
  ( edgeCapacitance     	"Metal5"		"Metal3"		52	 )
  ( edgeCapacitance     	"Metal5"		"Metal4"		63.5	 )
  ( edgeCapacitance     	"Metal6"		"Nwell"		17	 )
  ( edgeCapacitance     	"Metal6"		"Oxide"		21.5	 )
  ( edgeCapacitance     	"Metal6"		"Poly"		16.5	 )
  ( edgeCapacitance     	"Metal6"		"Metal1"		48	 )
  ( edgeCapacitance     	"Metal6"		"Metal2"		50	 )
  ( edgeCapacitance     	"Metal6"		"Metal3"		50.5	 )
  ( edgeCapacitance     	"Metal6"		"Metal4"		52	 )
  ( edgeCapacitance     	"Metal6"		"Metal5"		67.5	 )
 ) ;orderedCharacterizationRules

) ;electricalRules


;********************************
; DEVICES
;********************************
devices(
tcCreateCDSDeviceClass()

;
; no syEnhancement devices
;

;
; no syDepletion devices
;

symContactDevice(
; (name viaLayer viaPurpose layer1 purpose1 layer2 purpose2
;  w l (row column xPitch yPitch xBias yBias) encByLayer1 encByLayer2 legalRegion)

  (M1_POLY1 Cont drawing Poly drawing Metal1 drawing
  0.2 0.2 (1 1 0.5 0.5 center center) 0.2 0.1 _NA_)

  (M1_NIMP Cont drawing Oxide drawing (Nimp drawing 0.2) Metal1 drawing
  0.2 0.2 (1 1 0.5 0.5 center center) 0.2 0.1 _NA_)

  (M1_NWELL Cont drawing Oxide drawing (Nimp drawing 0.2) Metal1 drawing (Nwell drawing 0.6)
  0.2 0.2 (1 1 0.5 0.5 center center) 0.2 0.1 _NA_)

  (M1_PIMP Cont drawing Oxide drawing (Pimp drawing 0.2) Metal1 drawing
  0.2 0.2 (1 1 0.5 0.5 center center) 0.2 0.1 _NA_)

  (M1_PSUB Cont drawing Oxide drawing (Pimp drawing 0.2) Metal1 drawing
  0.2 0.2 (1 1 0.5 0.5 center center) 0.2 0.1 _NA_)

  (M1_ISOPWELL Cont drawing Oxide drawing (Pimp drawing 0.2) Metal1 drawing (Nburied drawing 0.9)
  0.2 0.2 (1 1 0.5 0.5 center center) 0.2 0.1 _NA_)

  (M2_M1 Via1 drawing Metal1 drawing Metal2 drawing
  0.2 0.2 (1 1 0.7 0.7 center center) 0.1 0.1 _NA_)

  (M3_M2 Via2 drawing Metal2 drawing Metal3 drawing
  0.2 0.2 (1 1 0.7 0.7 center center) 0.1 0.1 _NA_)

  (M4_M3 Via3 drawing Metal3 drawing Metal4 drawing
  0.2 0.2 (1 1 0.7 0.7 center center) 0.1 0.1 _NA_)

  (M5_M4 Via4 drawing Metal4 drawing Metal5 drawing
  0.2 0.2 (1 1 0.7 0.7 center center) 0.1 0.1 _NA_)

  (M6_M5 Via5 drawing Metal5 drawing Metal6 drawing
  0.2 0.2 (1 1 0.7 0.7 center center) 0.1 0.1 _NA_)
)

tfcDefineDeviceProp(
; (viewName        deviceName        propName          propValue)
  (symbolic        M2_M1             res               6.400000)
  (symbolic        M3_M2             res               6.400000)
  (symbolic        M4_M3             res               6.400000)
  (symbolic        M5_M4             res               6.400000)
  (symbolic        M6_M5             res               6.400000)
)

;
; no cdsVia devices
;

;
; no cdsMos devices
;

symPinDevice(
; (name maskable layer1 purpose1 w1 layer2 purpose2 w2 legalRegion)
  (poly1_T t Poly drawing 0.18 _NA_ _NA_ _NA_ _NA_)
  (nwell_T t Nwell drawing 1 _NA_ _NA_ _NA_ _NA_)
  (m1_T t Metal1 drawing 0.3 _NA_ _NA_ _NA_ _NA_)
  (m2_T t Metal2 drawing 0.3 _NA_ _NA_ _NA_ _NA_)
  (m3_T t Metal3 drawing 0.3 _NA_ _NA_ _NA_ _NA_)
  (m4_T t Metal4 drawing 0.3 _NA_ _NA_ _NA_ _NA_)
  (m5_T t Metal5 drawing 0.3 _NA_ _NA_ _NA_ _NA_)
  (m6_T t Metal6 drawing 0.3 _NA_ _NA_ _NA_ _NA_)
  (Metal1_T nil Metal1 drawing 0.3 _NA_ _NA_ _NA_ _NA_)
  (Metal2_T nil Metal2 drawing 0.3 _NA_ _NA_ _NA_ _NA_)
  (Metal3_T nil Metal3 drawing 0.3 _NA_ _NA_ _NA_ _NA_)
  (Metal4_T nil Metal4 drawing 0.3 _NA_ _NA_ _NA_ _NA_)
  (Metal5_T nil Metal5 drawing 0.3 _NA_ _NA_ _NA_ _NA_)
  (Metal6_T nil Metal6 drawing 0.3 _NA_ _NA_ _NA_ _NA_)
)

;
; no syRectPin devices
;

ruleContactDevice(
; ( viaName (layer1 purpose1 layer1BBox1 [layer1BBox2 ...])
;           (viaLayer viaPurpose viaLayerBBox1 [viaLayerBBox2 ...])
;           (layer2 purpose2 layer2BBox1 [layer2BBox2 ...])
; )
  ( ruleVia
    ( Metal1 drawing
       ( -1.500000 -0.900000 1.500000 0.900000 )
    )
    ( Via1 drawing
       ( -0.900000 -0.300000 -0.300000 0.300000 )
       ( 0.300000 -0.300000 0.900000 0.300000 )
    )
    ( Metal2 drawing
       ( -1.500000 -0.900000 1.500000 0.900000 )
    )
  )
)


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; Opus Symbolic Device Class Definition
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

tcCreateDeviceClass( "symbolic" "syEnhContact"
    ; class parameters
    ( (viaLayer "cont") (viaLayer2 "sl") (encByVia 0.2) 
      (layer1 "ndiff") (layer1Implant "") (layer1ImpEnc 1.2) 
      (layer2 "metal1") (layer2Implant "") (layer2ImpEnc 0.0) 
      (encByLayer1 0.7) (encByLayer2 0.7) (layer1XEnc 0.7) 
      (layer1YEnc 0.7) (layer2XEnc 0.7) (layer2YEnc 0.7) )
    ; formal parameters
    ( (w 1.4) (l 1.4) (row 1) 
      (column 1) (xPitch 3.3) (yPitch 3.3) 
      (offset 0.0) (side "center") (xBias "center") 
      (yBias "center") (layer1Dir "") (layer2Dir "") 
      (leakLength 1.4) (areaPin "") )
    ; IL codes specifying geometry
    
    (setq layer1X 
	(case layer1Dir 
	    (("x" "xy" "xt" "xb") layer1XEnc) 
	    (t encByLayer1)
	)
    )
    (setq layer1Y 
	(case layer1Dir 
	    (("y" "yx" "yl" "yr") layer1YEnc) 
	    (t encByLayer1)
	)
    )
    (setq layer2X 
	(case layer2Dir 
	    (("x" "xy" "xt" "xb") layer2XEnc) 
	    (t encByLayer2)
	)
    )
    (setq layer2Y 
	(case layer2Dir 
	    (("y" "yx" "yl" "yr") layer2YEnc) 
	    (t encByLayer2)
	)
    )
    (setq direction1 
	(case layer1Dir 
	    ("x" 
		(list "left" "right")
	    ) 
	    ("xt" 
		(list "left" "right" "top")
	    ) 
	    ("xb" 
		(list "left" "right" "bottom")
	    )
	    ("y" 
		(list "top" "bottom")
	    ) 
	    ("yl" 
		(list "top" "bottom" "left")
	    ) 
	    ("yr" 
		(list "top" "bottom" "right")
	    ) 
	    (t 
		(list "left" "right" "top" "bottom")
	    )
	)
    )
    (setq direction2 
	(case layer2Dir 
	    ("x" 
		(list "left" "right")
	    ) 
	    ("xt" 
		(list "left" "right" "top")
	    ) 
	    ("xb" 
		(list "left" "right" "bottom")
	    )
	    ("y" 
		(list "top" "bottom")
	    ) 
	    ("yl" 
		(list "top" "bottom" "left")
	    ) 
	    ("yr" 
		(list "top" "bottom" "right")
	    ) 
	    (t 
		(list "left" "right" "top" "bottom")
	    )
	)
    )
    (case side 
	(("left-leak" "right-leak") 
	    (setq orientation "vertical") 
	    (setq layer1X encByLayer1) 
	    (setq layer2X encByLayer2)
	) 
	(("top-leak" "bottom-leak") 
	    (setq orientation "horizontal") 
	    (setq layer1X layer1Y) 
	    (setq layer2X layer2Y) 
	    (setq layer1Y encByLayer1)
	    (setq layer2Y encByLayer2) 
	    (setq x xPitch) 
	    (setq xPitch yPitch) 
	    (setq yPitch x) 
	    (setq x w)
	    (setq w l) 
	    (setq l x)
	) 
	(t 
	    (setq orientation side)
	)
    )
    (case orientation 
	("top" 
	    (setq llY offset) 
	    (setq urY 
		(plus 
		    (times yPitch 
			(difference row 1.0)
		    ) l llY
		)
	    ) 
	    (setq lleftY 
		(minus urY)
	    ) 
	    (setq urightY urY)
	    (setq centerY offset) 
	    (setq n 1)
	) 
	("bottom" 
	    (setq urY 
		(minus offset)
	    ) 
	    (setq llY 
		(difference urY 
		    (times yPitch 
			(difference row 1.0)
		    ) l
		)
	    ) 
	    (setq urightY 
		(minus llY)
	    ) 
	    (setq lleftY llY)
	    (setq centerY 
		(minus offset)
	    ) 
	    (setq n 1)
	) 
	("both" 
	    (setq llY offset) 
	    (setq urY 
		(plus 
		    (times yPitch 
			(difference row 1.0)
		    ) l llY
		)
	    ) 
	    (setq lleftY 
		(minus urY)
	    ) 
	    (setq urightY urY)
	    (setq centerY offset) 
	    (setq n 2)
	)
	("vertical" 
	    (setq offset 0.0) 
	    (setq urightY 
		(quotient 
		    (plus 
			(times yPitch 
			    (difference row 1.0)
			) l
		    ) 2.0
		)
	    ) 
	    (setq urY urightY) 
	    (setq lleftY 
		(minus urightY)
	    )
	    (setq llY lleftY) 
	    (setq centerY 0.0) 
	    (setq row 1) 
	    (setq column 1) 
	    (setq n 1)
	) 
	("horizontal" 
	    (setq offset 0.0) 
	    (setq urightY 
		(quotient 
		    (plus 
			(times yPitch 
			    (difference row 1.0)
			) l
		    ) 2.0
		)
	    ) 
	    (setq urY urightY) 
	    (setq lleftY 
		(minus urightY)
	    )
	    (setq llY lleftY) 
	    (setq centerY 0.0) 
	    (setq row 1) 
	    (setq column 1) 
	    (setq n 1)
	) 
	(t 
	    (setq orientation "center") 
	    (setq offset 0.0) 
	    (setq urightY 
		(quotient 
		    (plus 
			(times yPitch 
			    (difference row 1.0)
			) l
		    ) 2.0
		)
	    ) 
	    (setq urY urightY)
	    (setq lleftY 
		(minus urightY)
	    ) 
	    (setq llY lleftY) 
	    (setq centerY 0.0) 
	    (setq n 1)
	)
    )
    (setq urightX 
	(quotient 
	    (plus 
		(times xPitch 
		    (difference column 1)
		) w
	    ) 2.0
	)
    )
    (setq lleftX 
	(minus urightX)
    )
    (setq moveX 
	(case xBias 
	    ("right" 
		(quotient 
		    (times 
			(difference 1 column) xPitch
		    ) 2.0
		)
	    ) 
	    ("left" 
		(quotient 
		    (times 
			(difference column 1) xPitch
		    ) 2.0
		)
	    ) 
	    (t 0.0)
	)
    )
    (setq moveY 
	(case yBias 
	    ("top" 
		(quotient 
		    (times 
			(difference 1 row) yPitch
		    ) 2.0
		)
	    ) 
	    ("bottom" 
		(quotient 
		    (times 
			(difference row 1) yPitch
		    ) 2.0
		)
	    ) 
	    (t 0.0)
	)
    )
    (setq net 
	(dbMakeNet tcCellView "ppd")
    )
    (setq x1 
	(case side 
	    ("left-leak" 
		(plus 
		    (difference lleftX layer1X leakLength) encByLayer1
		)
	    ) 
	    ("right-leak" 
		(difference 
		    (plus urightX layer1X) encByLayer1
		)
	    ) 
	    (t 
		(difference lleftX layer1X)
	    )
	)
    )
    (setq x2 
	(case side 
	    ("left-leak" 
		(plus 
		    (difference lleftX layer1X) encByLayer1
		)
	    ) 
	    ("right-leak" 
		(plus 
		    (difference 
			(plus urightX layer1X) encByLayer1
		    ) leakLength
		)
	    ) 
	    (t 
		(plus urightX layer1X)
	    )
	)
    )
    (setq layer1AreaPin 
	(or 
	    (equal areaPin "all") 
	    (equal areaPin "layer1") 
	    (equal areaPin "layer12")
	)
    )
    (setq layer2AreaPin 
	(or 
	    (equal areaPin "all") 
	    (equal areaPin "layer2") 
	    (equal areaPin "layer12")
	)
    )
    (setq viaAreaPin 
	(or 
	    (equal areaPin "via") 
	    (equal areaPin "all")
	)
    )
    (setq via2AreaPin 
	(or 
	    (equal areaPin "via2") 
	    (equal areaPin "all")
	)
    )
    (when 
	(lessp x1 x2) 
	(setq y1 
	    (case side 
		("bottom-leak" 
		    (difference 
			(plus 
			    (difference lleftY layer1Y) encByLayer1
			) leakLength
		    )
		) 
		("top-leak" 
		    (difference 
			(plus urightY layer1Y) encByLayer1
		    )
		) 
		(t 
		    (difference lleftY layer1Y)
		)
	    )
	) 
	(setq y2 
	    (case side 
		("bottom-leak" 
		    (plus 
			(difference lleftY layer1Y) encByLayer1
		    )
		) 
		("top-leak" 
		    (plus 
			(difference 
			    (plus urightY layer1Y) encByLayer1
			) leakLength
		    )
		) 
		(t 
		    (plus urightY layer1Y)
		)
	    )
	) 
	(when 
	    (lessp y1 y2) 
	    (setq rect 
		(dbCreateRect tcCellView layer1 
		    (list 
			(range x1 y1) 
			(range x2 y2)
		    )
		)
	    ) 
	    (dbMoveFig rect tcCellView 
		(list 
		    (range moveX moveY) "R0"
		)
	    ) 
	    (dbAddFigToNet rect net)
	    (when layer1AreaPin 
		(setq pin 
		    (dbCreatePin net rect)
		) 
		(dbSetq pin direction1 accessDir)
	    ) 
	    (unless 
		(equal layer1Implant "") 
		(setq x1 
		    (difference x1 layer1ImpEnc)
		) 
		(setq x2 
		    (plus x2 layer1ImpEnc)
		) 
		(when 
		    (lessp x1 x2) 
		    (setq y1 
			(difference y1 layer1ImpEnc)
		    ) 
		    (setq y2 
			(plus y2 layer1ImpEnc)
		    ) 
		    (setq rect 
			(dbCreateRect tcCellView layer1Implant 
			    (list 
				(range x1 y1) 
				(range x2 y2)
			    )
			)
		    )
		    (dbMoveFig rect tcCellView 
			(list 
			    (range moveX moveY) "R0"
			)
		    ) 
		    (dbAddFigToNet rect net)
		)
	    )
	)
    )
    (unless layer1AreaPin 
	(setq dot 
	    (dbCreateDot tcCellView layer1 
		(range 0.0 0.0)
	    )
	) 
	(setq pin 
	    (dbCreatePin net dot)
	) 
	(dbSetq pin direction1 accessDir)
    )
    (unless via2AreaPin 
	(when 
	    (and 
		(nequal viaLayer viaLayer2) 
		(nequal viaLayer2 "")
	    ) 
	    (setq dot 
		(dbCreateDot tcCellView viaLayer2 
		    (range 0.0 0.0)
		)
	    ) 
	    (setq pin 
		(dbCreatePin net dot)
	    ) 
	    (dbSetq pin 
		(list "right" "left" "top" "bottom") accessDir
	    )
	)
    )
    (for i 1 n 
	(for c 1 column 
	    (if 
		(equal side "horizontal") then 
		(setq lX 
		    (difference 
			(plus lleftX 
			    (times 
				(difference c 1.0) xPitch
			    )
			) layer1X
		    )
		) 
		(setq uX 
		    (plus lX w 
			(times 2.0 layer1X)
		    )
		)
		else 
		(setq lX 
		    (plus lleftX 
			(times 
			    (difference c 1.0) xPitch
			)
		    )
		) 
		(setq uX 
		    (plus lX w)
		)
	    )
	    (for r 1 row 
		(if 
		    (equal side "vertical") then 
		    (setq lY 
			(difference 
			    (plus llY 
				(times 
				    (difference r 1.0) yPitch
				)
			    ) layer1Y
			)
		    ) 
		    (setq uY 
			(plus lY l 
			    (times 2.0 layer1Y)
			)
		    )
		    else 
		    (setq lY 
			(plus llY 
			    (times 
				(difference r 1.0) yPitch
			    )
			)
		    ) 
		    (setq uY 
			(plus lY l)
		    )
		)
		(when 
		    (and 
			(lessp lX uX) 
			(lessp lY uY)
		    ) 
		    (setq rect 
			(dbCreateRect tcCellView viaLayer 
			    (list 
				(range lX lY) 
				(range uX uY)
			    )
			)
		    ) 
		    (dbMoveFig rect tcCellView 
			(list 
			    (range moveX moveY) "R0"
			)
		    ) 
		    (dbAddFigToNet rect net)
		) 
		(when 
		    (and 
			(nequal viaLayer viaLayer2) 
			(nequal viaLayer2 "")
		    ) 
		    (case side 
			("vertical" 
			    (setq x1 
				(plus lX encByVia)
			    ) 
			    (setq x2 
				(difference uX encByVia)
			    ) 
			    (when 
				(and 
				    (lessp x1 x2) 
				    (lessp lY uY)
				) 
				(setq rect 
				    (dbCreateRect tcCellView viaLayer2 
					(list 
					    (range x1 lY) 
					    (range x2 uY)
					)
				    )
				) 
				(dbMoveFig rect tcCellView 
				    (list 
					(range moveX moveY) "R0"
				    )
				) 
				(dbAddFigToNet rect net)
			    )
			) 
			("horizontal" 
			    (setq y1 
				(plus lY encByVia)
			    ) 
			    (setq y2 
				(difference uY encByVia)
			    ) 
			    (when 
				(and 
				    (lessp y1 y2) 
				    (lessp lX uX)
				) 
				(setq rect 
				    (dbCreateRect tcCellView viaLayer2 
					(list 
					    (range lX y1) 
					    (range uX y2)
					)
				    )
				) 
				(dbMoveFig rect tcCellView 
				    (list 
					(range moveX moveY) "R0"
				    )
				) 
				(dbAddFigToNet rect net)
			    )
			) 
			(t 
			    (setq x1 
				(plus lX encByVia)
			    ) 
			    (setq x2 
				(difference uX encByVia)
			    ) 
			    (when 
				(lessp x1 x2) 
				(setq y1 
				    (plus lY encByVia)
				) 
				(setq y2 
				    (difference uY encByVia)
				) 
				(when 
				    (lessp y1 y2) 
				    (setq rect 
					(dbCreateRect tcCellView viaLayer2 
					    (list 
						(range x1 y1) 
						(range x2 y2)
					    )
					)
				    ) 
				    (dbMoveFig rect tcCellView 
					(list 
					    (range moveX moveY) "R0"
					)
				    ) 
				    (dbAddFigToNet rect net)
				)
			    )
			)
		    )
		)
	    )
	)
	(unless 
	    (or viaAreaPin 
		(equal viaLayer layer2)
	    ) 
	    (setq dot 
		(dbCreateDot tcCellView viaLayer 
		    (range 0.0 centerY)
		)
	    ) 
	    (setq pin 
		(dbCreatePin net dot)
	    ) 
	    (dbSetq pin 
		(list "right" "left" "top" "bottom") accessDir
	    )
	) 
	(unless 
	    (equal layer2 "") 
	    (setq x1 
		(difference lleftX layer2X)
	    ) 
	    (setq x2 
		(plus urightX layer2X)
	    ) 
	    (when 
		(lessp x1 x2) 
		(setq y1 
		    (difference llY layer2Y)
		) 
		(setq y2 
		    (plus urY layer2Y)
		) 
		(when 
		    (lessp y1 y2) 
		    (setq rect 
			(dbCreateRect tcCellView layer2 
			    (list 
				(range x1 y1) 
				(range x2 y2)
			    )
			)
		    ) 
		    (dbMoveFig rect tcCellView 
			(list 
			    (range moveX moveY) "R0"
			)
		    ) 
		    (dbAddFigToNet rect net)
		    (when layer2AreaPin 
			(setq pin 
			    (dbCreatePin net rect)
			) 
			(dbSetq pin direction2 accessDir)
		    ) 
		    (when 
			(nequal layer2Implant "") 
			(setq x1 
			    (difference x1 layer2ImpEnc)
			) 
			(setq x2 
			    (plus x2 layer2ImpEnc)
			) 
			(when 
			    (lessp x1 x2) 
			    (setq y1 
				(difference y1 layer2ImpEnc)
			    ) 
			    (setq y2 
				(plus y2 layer2ImpEnc)
			    ) 
			    (when 
				(lessp y1 y2) 
				(setq rect 
				    (dbCreateRect tcCellView layer2Implant 
					(list 
					    (range x1 y1) 
					    (range x2 y2)
					)
				    )
				) 
				(dbMoveFig rect tcCellView 
				    (list 
					(range moveX moveY) "R0"
				    )
				) 
				(dbAddFigToNet rect net)
			    )
			)
		    )
		)
	    )
	    (unless layer2AreaPin 
		(setq dot 
		    (dbCreateDot tcCellView layer2 
			(range 0.0 centerY)
		    )
		) 
		(setq pin 
		    (dbCreatePin net dot)
		) 
		(dbSetq pin direction2 accessDir)
	    ) 
	    (when 
		(and 
		    (null layer2AreaPin) 
		    (equal viaLayer layer2)
		) 
		(if 
		    (equal i 1) then 
		    (case orientation 
			(("both" "top") 
			    (setq dot 
				(dbCreateDot tcCellView layer2 
				    (range 0.0 
					(plus centerY l)
				    )
				)
			    ) 
			    (setq pin 
				(dbCreatePin net dot)
			    ) 
			    (dbSetq pin direction2 accessDir)
			) 
			("bottom" 
			    (setq dot 
				(dbCreateDot tcCellView layer2 
				    (range 0.0 
					(difference centerY l)
				    )
				)
			    ) 
			    (setq pin 
				(dbCreatePin net dot)
			    ) 
			    (dbSetq pin direction2 accessDir)
			) 
			(t 
			    (setq dot 
				(dbCreateDot tcCellView layer2 
				    (range 0.0 
					(difference centerY 
					    (quotient l 2.0)
					)
				    )
				)
			    ) 
			    (setq pin 
				(dbCreatePin net dot)
			    ) 
			    (dbSetq pin direction2 accessDir) 
			    (setq dot 
				(dbCreateDot tcCellView layer2 
				    (range 0.0 
					(plus centerY 
					    (quotient l 2.0)
					)
				    )
				)
			    )
			    (setq pin 
				(dbCreatePin net dot)
			    ) 
			    (dbSetq pin direction2 accessDir)
			)
		    ) else
		    (setq dot 
			(dbCreateDot tcCellView layer2 
			    (range 0.0 
				(difference centerY l)
			    )
			)
		    ) 
		    (setq pin 
			(dbCreatePin net dot)
		    ) 
		    (dbSetq pin direction2 accessDir)
		)
	    )
	) 
	(setq Y llY) 
	(setq llY 
	    (minus urY)
	) 
	(setq urY 
	    (minus Y)
	)
	(setq centerY 
	    (minus centerY)
	)
    )
    (case side 
	("left-leak" 
	    (setq x2 
		(quotient 
		    (minus w) 2.0
		)
	    ) 
	    (setq x1 
		(difference x2 leakLength)
	    ) 
	    (setq y1 x2) 
	    (setq y2 
		(minus x2)
	    )
	) 
	("right-leak" 
	    (setq x1 
		(quotient w 2.0)
	    ) 
	    (setq x2 
		(plus x1 leakLength)
	    ) 
	    (setq y1 
		(minus x1)
	    ) 
	    (setq y2 x1)
	) 
	("top-leak" 
	    (setq x2 
		(quotient l 2.0)
	    ) 
	    (setq x1 
		(minus x2)
	    ) 
	    (setq y1 x2) 
	    (setq y2 
		(plus y2 leakLength)
	    )
	)
	("bottom-leak" 
	    (setq x1 
		(quotient 
		    (minus l) 2.0
		)
	    ) 
	    (setq x2 
		(minus x1)
	    ) 
	    (setq y2 x1) 
	    (setq y1 
		(difference y2 leakLength)
	    )
	) 
	(t 
	    (setq x1 0.0) 
	    (setq x2 0.0) 
	    (setq y1 0.0) 
	    (setq y2 0.0)
	)
    )
    (when 
	(and 
	    (lessp x1 x2) 
	    (lessp y1 y2)
	) 
	(setq rect 
	    (dbCreateRect tcCellView viaLayer 
		(list 
		    (range x1 y1) 
		    (range x2 y2)
		)
	    )
	) 
	(dbMoveFig rect tcCellView 
	    (list 
		(range moveX moveY) "R0"
	    )
	) 
	(dbAddFigToNet rect net)
    )
)
;
;
tfcDefineDeviceClassProp(
; (viewName        devClassName      propName          propValue)
  (symbolic        syEnhContact      function          "contact")
)


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; Opus Symbolic Device Declaration
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;; device class "syEnhContact":
tcDeclareDevice( "symbolic" "syEnhContact" "Via23_stack_north"
    ( (viaLayer "Via2") (viaLayer2 "") (encByVia 0.000000) 
      (layer1 "Metal2") (layer1Implant "") (layer1ImpEnc 0.000000) 
      (layer2 "Metal3") (layer2Implant "") (layer2ImpEnc 0.000000) 
      (encByLayer1 0.150000) (encByLayer2 0.100000) (layer1XEnc 0.100000) 
      (layer1YEnc 0.000000) (layer2XEnc 0.000000) (layer2YEnc 0.000000) )
    ( (w 0.200000) (l 0.200000) (row 1) 
      (column 1) (xPitch 1.000000) (yPitch 1.000000) 
      (offset 0.000000) (side "center") (xBias "center") 
      (yBias "center") (layer1Dir "xy") (layer2Dir "") 
      (leakLength 0.000000) (areaPin "layer1") )
)
;

tfcDefineDeviceProp(
; (viewName        deviceName        propName          propValue)
  (symbolic        Via23_stack_north res               6.400000)
  (symbolic        Via23_stack_north topstack          t)
)

tcDeclareDevice( "symbolic" "syEnhContact" "Via23_stack_south"
    ( (viaLayer "Via2") (viaLayer2 "") (encByVia 0.000000) 
      (layer1 "Metal2") (layer1Implant "") (layer1ImpEnc 0.000000) 
      (layer2 "Metal3") (layer2Implant "") (layer2ImpEnc 0.000000) 
      (encByLayer1 0.150000) (encByLayer2 0.100000) (layer1XEnc 0.100000) 
      (layer1YEnc 0.000000) (layer2XEnc 0.000000) (layer2YEnc 0.000000) )
    ( (w 0.200000) (l 0.200000) (row 1) 
      (column 1) (xPitch 1.000000) (yPitch 1.000000) 
      (offset 0.000000) (side "center") (xBias "center") 
      (yBias "center") (layer1Dir "xy") (layer2Dir "") 
      (leakLength 0.000000) (areaPin "layer1") )
)
;

tfcDefineDeviceProp(
; (viewName        deviceName        propName          propValue)
  (symbolic        Via23_stack_south res               6.400000)
  (symbolic        Via23_stack_south topstack          t)
)

tcDeclareDevice( "symbolic" "syEnhContact" "Via34_stack_east"
    ( (viaLayer "Via3") (viaLayer2 "") (encByVia 0.000000) 
      (layer1 "Metal3") (layer1Implant "") (layer1ImpEnc 0.000000) 
      (layer2 "Metal4") (layer2Implant "") (layer2ImpEnc 0.000000) 
      (encByLayer1 0.100000) (encByLayer2 0.100000) (layer1XEnc 0.150000) 
      (layer1YEnc 0.000000) (layer2XEnc 0.000000) (layer2YEnc 0.000000) )
    ( (w 0.200000) (l 0.200000) (row 1) 
      (column 1) (xPitch 1.000000) (yPitch 1.000000) 
      (offset 0.000000) (side "center") (xBias "center") 
      (yBias "center") (layer1Dir "xy") (layer2Dir "") 
      (leakLength 0.000000) (areaPin "layer1") )
)
;

tfcDefineDeviceProp(
; (viewName        deviceName        propName          propValue)
  (symbolic        Via34_stack_east  res               6.400000)
  (symbolic        Via34_stack_east  topstack          t)
)

tcDeclareDevice( "symbolic" "syEnhContact" "Via34_stack_west"
    ( (viaLayer "Via3") (viaLayer2 "") (encByVia 0.000000) 
      (layer1 "Metal3") (layer1Implant "") (layer1ImpEnc 0.000000) 
      (layer2 "Metal4") (layer2Implant "") (layer2ImpEnc 0.000000) 
      (encByLayer1 0.100000) (encByLayer2 0.100000) (layer1XEnc 0.150000) 
      (layer1YEnc 0.000000) (layer2XEnc 0.000000) (layer2YEnc 0.000000) )
    ( (w 0.200000) (l 0.200000) (row 1) 
      (column 1) (xPitch 1.000000) (yPitch 1.000000) 
      (offset 0.000000) (side "center") (xBias "center") 
      (yBias "center") (layer1Dir "xy") (layer2Dir "") 
      (leakLength 0.000000) (areaPin "layer1") )
)
;

tfcDefineDeviceProp(
; (viewName        deviceName        propName          propValue)
  (symbolic        Via34_stack_west  res               6.400000)
  (symbolic        Via34_stack_west  topstack          t)
)

tcDeclareDevice( "symbolic" "syEnhContact" "Via45_stack_north"
    ( (viaLayer "Via4") (viaLayer2 "") (encByVia 0.000000) 
      (layer1 "Metal4") (layer1Implant "") (layer1ImpEnc 0.000000) 
      (layer2 "Metal5") (layer2Implant "") (layer2ImpEnc 0.000000) 
      (encByLayer1 0.150000) (encByLayer2 0.100000) (layer1XEnc 0.100000) 
      (layer1YEnc 0.000000) (layer2XEnc 0.000000) (layer2YEnc 0.000000) )
    ( (w 0.200000) (l 0.200000) (row 1) 
      (column 1) (xPitch 1.000000) (yPitch 1.000000) 
      (offset 0.000000) (side "center") (xBias "center") 
      (yBias "center") (layer1Dir "xy") (layer2Dir "") 
      (leakLength 0.000000) (areaPin "layer1") )
)
;

tfcDefineDeviceProp(
; (viewName        deviceName        propName          propValue)
  (symbolic        Via45_stack_north res               2.540000)
  (symbolic        Via45_stack_north topstack          t)
)

tcDeclareDevice( "symbolic" "syEnhContact" "Via45_stack_south"
    ( (viaLayer "Via4") (viaLayer2 "") (encByVia 0.000000) 
      (layer1 "Metal4") (layer1Implant "") (layer1ImpEnc 0.000000) 
      (layer2 "Metal5") (layer2Implant "") (layer2ImpEnc 0.000000) 
      (encByLayer1 0.150000) (encByLayer2 0.100000) (layer1XEnc 0.100000) 
      (layer1YEnc 0.000000) (layer2XEnc 0.000000) (layer2YEnc 0.000000) )
    ( (w 0.200000) (l 0.200000) (row 1) 
      (column 1) (xPitch 1.000000) (yPitch 1.000000) 
      (offset 0.000000) (side "center") (xBias "center") 
      (yBias "center") (layer1Dir "xy") (layer2Dir "") 
      (leakLength 0.000000) (areaPin "layer1") )
)
;

tfcDefineDeviceProp(
; (viewName        deviceName        propName          propValue)
  (symbolic        Via45_stack_south res               2.540000)
  (symbolic        Via45_stack_south topstack          t)
)

tcDeclareDevice( "symbolic" "syEnhContact" "Via56_stack_east"
    ( (viaLayer "Via5") (viaLayer2 "") (encByVia 0.000000) 
      (layer1 "Metal5") (layer1Implant "") (layer1ImpEnc 0.000000) 
      (layer2 "Metal6") (layer2Implant "") (layer2ImpEnc 0.000000) 
      (encByLayer1 0.100000) (encByLayer2 0.100000) (layer1XEnc 0.150000) 
      (layer1YEnc 0.000000) (layer2XEnc 0.000000) (layer2YEnc 0.000000) )
    ( (w 0.200000) (l 0.200000) (row 1) 
      (column 1) (xPitch 1.000000) (yPitch 1.000000) 
      (offset 0.000000) (side "center") (xBias "center") 
      (yBias "center") (layer1Dir "xy") (layer2Dir "") 
      (leakLength 0.000000) (areaPin "layer1") )
)
;

tfcDefineDeviceProp(
; (viewName        deviceName        propName          propValue)
  (symbolic        Via56_stack_east  res               2.540000)
  (symbolic        Via56_stack_east  topstack          t)
)

tcDeclareDevice( "symbolic" "syEnhContact" "Via56_stack_west"
    ( (viaLayer "Via5") (viaLayer2 "") (encByVia 0.000000) 
      (layer1 "Metal5") (layer1Implant "") (layer1ImpEnc 0.000000) 
      (layer2 "Metal6") (layer2Implant "") (layer2ImpEnc 0.000000) 
      (encByLayer1 0.100000) (encByLayer2 0.100000) (layer1XEnc 0.150000) 
      (layer1YEnc 0.000000) (layer2XEnc 0.000000) (layer2YEnc 0.000000) )
    ( (w 0.200000) (l 0.200000) (row 1) 
      (column 1) (xPitch 1.000000) (yPitch 1.000000) 
      (offset 0.000000) (side "center") (xBias "center") 
      (yBias "center") (layer1Dir "xy") (layer2Dir "") 
      (leakLength 0.000000) (areaPin "layer1") )
)
;

tfcDefineDeviceProp(
; (viewName        deviceName        propName          propValue)
  (symbolic        Via56_stack_west  res               2.540000)
  (symbolic        Via56_stack_west  topstack          t)
)

) ;devices


;********************************
; COMPACTOR RULES
;********************************
compactorRules(

 compactorLayers(
 ;( layer                    	usage      )
 ;( -----                    	-----      )
  ( Metal1                   	"conduction" )
  ( Via1                     	"via"      )
  ( Metal2                   	"conduction" )
  ( Via2                     	"via"      )
  ( Metal3                   	"conduction" )
  ( Via3                     	"via"      )
  ( Metal4                   	"conduction" )
  ( Via4                     	"via"      )
  ( Metal5                   	"conduction" )
  ( Via5                     	"via"      )
  ( Metal6                   	"conduction" )
  ( Cont                     	"via"      )
  ( Poly                     	"conduction" )
  ( Nwell                    	"well"     )
  ( Pwell                    	"well"     )
  ( Oxide                    	"diffusion" )
  ( Nimp                     	"implant"  )
  ( Pimp                     	"implant"  )
 ) ;compactorLayers

) ;compactorRules


;********************************
; LX RULES
;********************************
lxRules(

 lxExtractLayers(
 ;( list of layers or layer/purpose pairs  )
 ;( -------------------------------------  )
  ( Pwell     	Nwell     	Oxide     	Poly      	Cont      	Metal1    	Via1      	Metal2    	Via2      	Metal3    	Via3      	Metal4    	Via4      	Metal5    	Via5      	Metal6    	Bondpad    )
 ) ;lxExtractLayers

 lxNoOverlapLayers(
 ;( forbidden overlaps in LX )
 ;( ------------------------ )
  ( Poly      	Oxide      )
  ( Poly      	Resdum     )
 ) ;lxNoOverlapLayers

 lxMPPTemplates(
 ;( name [masterPath] [offsetSubpaths] [encSubPaths] [subRects] )
 ;
 ;  masterPath:
 ;  (layer [width] [choppable] [endType] [beginExt] [endExt] [justify] [offset]
 ;  [connectivity])
 ;
 ;  offsetSubpaths:
 ;  (layer [width] [choppable] [separation] [justification] [begOffset] [endOffset]
 ;  [connectivity])
 ;
 ;  encSubPaths:
 ;  (layer [enclosure] [choppable] [separation] [begOffset] [endOffset]
 ;  [connectivity])
 ;
 ;  subRects:
 ;  (layer [width] [length] [choppable] [separation] [justification] [space] [begOffset] [endOffset] [gap] 
 ;  [connectivity] [beginSegOffset] [endSegOffset])
 ;
 ;  connectivity:
 ;  ([I/O type] [pin] [accDir] [dispPinName] [height] [ layer]
 ;   [layer] [justification] [font] [textOptions] [orientation]
 ;   [refHandle] [offset])
 ;
 ;( --------------------------------------------------------------------- )
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
 ) ;lxMPPTemplates

) ;lxRules


;********************************
; P&R RULES
;********************************
prRules(

 prRoutingLayers(
 ;( layer                       preferredDirection  )
 ;( -----                       ------------------  )
  ( Metal1                   	"horizontal" )
  ( Metal2                   	"vertical" )
  ( Metal3                   	"horizontal" )
  ( Metal4                   	"vertical" )
  ( Metal5                   	"horizontal" )
  ( Metal6                   	"vertical" )
 ) ;prRoutingLayers

 prViaTypes(
 ;( device viewName             viaType    )
 ;( ---------------             -------    )
  ( ("M1_POLY1" "symbolic")	"default"  )
  ( ("M2_M1" "symbolic")	"default"  )
  ( ("M3_M2" "symbolic")	"default"  )
  ( ("M4_M3" "symbolic")	"default"  )
  ( ("M5_M4" "symbolic")	"default"  )
  ( ("M6_M5" "symbolic")	"default"  )
  ( ("Via23_stack_north" "symbolic")	"default"  )
  ( ("Via23_stack_south" "symbolic")	"default"  )
  ( ("Via34_stack_east" "symbolic")	"default"  )
  ( ("Via34_stack_west" "symbolic")	"default"  )
  ( ("Via45_stack_north" "symbolic")	"default"  )
  ( ("Via45_stack_south" "symbolic")	"default"  )
  ( ("Via56_stack_east" "symbolic")	"default"  )
  ( ("Via56_stack_west" "symbolic")	"default"  )
 ) ;prViaTypes

 prRoutingPitch(
 ;( layer                pitch )
 ;( -----                ----- )
  ( Metal1               0.66 )
  ( Metal2               0.66 )
  ( Metal3               0.66 )
  ( Metal4               0.66 )
  ( Metal5               0.66 )
  ( Metal6               0.66 )
 ) ;prRoutingPitch

 prRoutingOffset(
 ;( layer                offset )
 ;( -----                ------ )
  ( Metal1               0.33 )
  ( Metal2               0.33 )
  ( Metal3               0.33 )
  ( Metal4               0.33 )
  ( Metal5               0.33 )
  ( Metal6               0.33 )
 ) ;prRoutingOffset

 prMastersliceLayers(
 ;( layers : listed in order of lowest (closest to substrate) to highest )
 ;( -------------------------------------------------------------------- )
  ( Poly       )
 ) ;prMastersliceLayers

 prOverlapLayer(
 ;( list of layers or layer/purpose pairs )
 ;( ------------------------------------- )
  ( OVERLAP )
 ) ;prOverlapLayer

 prStackVias(
 ;( viaLayerPairList    stackable )
 ;( ----------------    --------- )
  ( Metal2	Metal2 )
  ( Metal3	Metal3 )
  ( Metal4	Metal4 )
  ( Metal5	Metal5 )
  ( Via1	Via2 )
  ( Via2	Via3 )
  ( Via3	Via4 )
  ( Via4	Via5 )
 ) ;prStackVias

 prGenViaRules(
 ;( ViaRuleName         viaLayer     (lowerPt upperPt xPitch yPitch resistence) 
 ;    Layer1            Direction|(overhang1 overhang2)    (wMin wMax overHang metalOverHang) 
 ;    Layer2            Direction|(overhang1 overhang2)    (wMin wMax overHang metalOverHang) 
 ;    (properties)
 ;) 
 ;( ---------------------------------------------------------------------- ) 
  ( Via12Array  	"Via1"	( (range -0.1 -0.1) (range 0.1 0.1) 0.5 0.5 _NA_ )
      Metal1         	"horizontal"	( _NA_ _NA_ 0.1 0.0 )
      Metal2         	"vertical"	( _NA_ _NA_ 0.1 0.0 )
  )
  ( Via23Array  	"Via2"	( (range -0.1 -0.1) (range 0.1 0.1) 0.5 0.5 _NA_ )
      Metal2         	"vertical"	( _NA_ _NA_ 0.1 0.0 )
      Metal3         	"horizontal"	( _NA_ _NA_ 0.1 0.0 )
  )
  ( Via34Array  	"Via3"	( (range -0.1 -0.1) (range 0.1 0.1) 0.5 0.5 _NA_ )
      Metal3         	"horizontal"	( _NA_ _NA_ 0.1 0.0 )
      Metal4         	"vertical"	( _NA_ _NA_ 0.1 0.0 )
  )
  ( Via45Array  	"Via4"	( (range -0.1 -0.1) (range 0.1 0.1) 0.5 0.5 _NA_ )
      Metal4         	"vertical"	( _NA_ _NA_ 0.1 0.0 )
      Metal5         	"horizontal"	( _NA_ _NA_ 0.1 0.0 )
  )
  ( Via56Array  	"Via5"	( (range -0.1 -0.1) (range 0.1 0.1) 0.5 0.5 _NA_ )
      Metal5         	"horizontal"	( _NA_ _NA_ 0.1 0.0 )
      Metal6         	"vertical"	( _NA_ _NA_ 0.1 0.0 )
  )
  ( TURNMetal1  	nil	( _NA_ _NA_ _NA_ _NA_ _NA_ )
      Metal1         	"vertical"	( _NA_ _NA_ _NA_ _NA_ )
      Metal1         	"horizontal"	( _NA_ _NA_ _NA_ _NA_ )
  )
  ( TURNMetal2  	nil	( _NA_ _NA_ _NA_ _NA_ _NA_ )
      Metal2         	"vertical"	( _NA_ _NA_ _NA_ _NA_ )
      Metal2         	"horizontal"	( _NA_ _NA_ _NA_ _NA_ )
  )
  ( TURNMetal3  	nil	( _NA_ _NA_ _NA_ _NA_ _NA_ )
      Metal3         	"vertical"	( _NA_ _NA_ _NA_ _NA_ )
      Metal3         	"horizontal"	( _NA_ _NA_ _NA_ _NA_ )
  )
  ( TURNMetal4  	nil	( _NA_ _NA_ _NA_ _NA_ _NA_ )
      Metal4         	"vertical"	( _NA_ _NA_ _NA_ _NA_ )
      Metal4         	"horizontal"	( _NA_ _NA_ _NA_ _NA_ )
  )
  ( TURNMetal5  	nil	( _NA_ _NA_ _NA_ _NA_ _NA_ )
      Metal5         	"vertical"	( _NA_ _NA_ _NA_ _NA_ )
      Metal5         	"horizontal"	( _NA_ _NA_ _NA_ _NA_ )
  )
  ( TURNMetal6  	nil	( _NA_ _NA_ _NA_ _NA_ _NA_ )
      Metal6         	"vertical"	( _NA_ _NA_ _NA_ _NA_ )
      Metal6         	"horizontal"	( _NA_ _NA_ _NA_ _NA_ )
  )
 ) ;prGenViaRules

) ;prRules
