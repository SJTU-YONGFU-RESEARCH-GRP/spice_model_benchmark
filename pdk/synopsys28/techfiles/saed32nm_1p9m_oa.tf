
;#################################################################
;# SAED 32/28NM 1p9m CustomDesigner technology file		 #
;#								 #
;# Revision History:						 #
;# Rev.		date		what				 #
;# --------------------------------------------------------------#	
;# 1.0		02/Feb/2011	(First draft)                    #
;# 1.1		31/Jan/2012	Added (Mx text) layers           #
;#################################################################


;********************************
; FROLS
;********************************
controls(
	techParams(
		;( parameter           value )
		;( ----------          ----- )
		( maskGrid       	0.001 )
		( cadGrid        	0.001 )
		( drcGrid        	0.001 )
		( mfgGrid        	0.001 )
		( scale          	1.0 )
		( MPPS           	(list (list 
		nil (quote cwW) 0.09 (quote cwL) 0.09 (quote cwSp) 0.10 (quote cwRowSp) 0.15 (quote Cw) "CO" (quote M1) "M1" (quote M1CwEnc) 0.005 )
		 (list nil (quote name) "NWELL" (quote pathLayer) "DIFF" (quote pathWidth) 0.09 (quote pathCwEnc) 0.05 (quote enclosureLayers) (list)
		  (quote spacings) (list nil)) (list nil (quote name) "sub" (quote pathLayer) "DIFF" (quote pathWidth) 0.09 (quote pathCwEnc) 0.05 (quote enclosureLayers)
		   (list) (quote spacings) (list nil)))	 )
	) ;techParams
	
	techPermissions(
		;( class               (read-only users)  (read & write users)           )
		;( ----------          -----------------  --------------------           )
	) ;techPermissions
	
	techPermissions(
		;( class               (read-only users)  (read & write users)           )
		;( ----------          -----------------  --------------------           )
	) ;techPermissions

	viewTypeUnits(
		;( viewType            userUnit       dbuperuu           )
		;( --------            --------       --------           )
		( maskLayout     	"micron"       	1000            )
		( schematic      	"inch"         	160             )
		( schematicSymbol	"inch"         	160             )
		( netlist        	"inch"         	160             ) 
	) ;viewTypeUnits

	mfgGridResolution(
		( 0.001000 )
	) ;mfgGridResolution



;;;;; MPP Definitions ############################


leMPPControls (
; P type guard ring    	name    	obj-list 		spacings	master-index
leMPPDefinition 	(psubGR		("ptypeGuardRing")      (1)  		0
) ; MPP Definition 
; MPP Ring Object

; N type guard ring    	name   		obj-list 		spacings	master-index
leMPPDefinition 	(nwellGR 	("ntypeGuardRing")      (1)  		0
) ; MPP Definition 
; MPP Ring Object

; P type inside Pwell	name 		MasterPathName  EnclosedPathNames    OffsetPathNames 	SubRectangleNames  EncShapeNames
leMPPRingObject (  ptypeGuardRing	"defaultPath"   (diffEncPath pplusEncPath )  nil	(defaultContacts)  nil
;  net name  ExposedParameters
 vss userParams (name netName)
) ; MPP Ring Object


; N type inside Nwell	name 		MasterPathName  	EnclosedPathNames  	OffsetPathNames SubRectangleNames  EncShapeNames
leMPPRingObject (  ntypeGuardRing	"defaultPath"   (diffEncPath nplusEncPath nwellEncPath)   nil	(defaultContacts)  nil
;  net name  ExposedParameters
 vdd userParams (name netName)
) ; MPP Ring Object

;            		name        		layer 		purpose		width		path-style	conn    chop
leMPPMasterPath 	("defaultPath" 		"M1" 		drawing		0.05  		extend	 	t   	t
userParams (name width layer purpose conn chop )
) ; Master Path

;             		name 	            	layer 		purpose 	enclosure 	path-style 	conn    chop
leMPPEnclosedPath 	("diffEncPath"	 	"DIFF"		drawing 	0.006          	extend	 	t       nil
userParams (name layer purpose enclosure conn chop)
) ; Enclosed Path

;             		name 	            	layer 		purpose 	enclosure 	path-style 	conn    chop
leMPPEnclosedPath 	("pplusEncPath" 	"PIMP"		drawing 	0.026          	extend	 	t  	nil
userParams (name layer purpose enclosure conn chop)
) ; Enclosed Path

;             		name 	            	layer 		purpose 	enclosure 	path-style 	conn    chop
leMPPEnclosedPath 	("nplusEncPath" 	"NIMP"		drawing 	0.026         	extend	 	t 	nil
userParams (name layer purpose enclosure conn chop)
) ; Enclosed Path

;             		name 	            	layer 		purpose 	enclosure 	path-style 	conn    chop
leMPPEnclosedPath 	("nwellEncPath" 	"NWELL"		drawing 	0.09          	extend	 	t   	nil
userParams (name layer purpose enclosure conn chop)
) ; Enclosed Path

;             		name 	            	layer 		purpose 	enclosure 	path-style 	conn    chop
;leMPPEnclosedPath 	("pwellEncPath" 	"PWELL"		drawing 	0.09          	extend	 	t   	nil
;userParams (name layer purpose enclosure conn chop)
;) ; Enclosed Path


;Sub Rectangles - contacts
;             name layer purpose width height conn chop enc EOL spa spaType numRows
leMPPSubRect (defaultContacts CO drawing 0.042 0.042 t t 0.004 0.035 0.05 fit 1
userParams (name layer purpose width height conn chop minEnclosure eol spacing spaceType numRows)
)

;Enclosed shape  name layer purpose leESEnclosure conn-flag leESExposedParameters
;leMPPEnclosedShape (encNWELL nwell drawing 0.245 t )
) ; leMPPControls


;;;;; MPP Definitions ############################



) ;controls

;********************************
; LAYER DEFINITION
;********************************
layerDefinitions(

	techPurposes(
		;( PurposeName               Purpose#   Abbreviation )
		;( -----------               --------   ------------ )
		;User-Defined Purposes:
		( dmy0                      0          dmy0         )
		( dmy1                      1          dmy1         )
		( dmy2                      2          dmy2         )
		( dmy3                      3          dmy3         )
		( dmy4                      4          dmy4         )
		( waterMark                 63         waterMark    )
		( dummy                     127        dummy        )
		( text                      220        text         )
		( subnode		    221	       subnode      )
		( extract		    222        extract      )
		;System-Reserved Purposes:
		( redundant                 -8         red          )
		( gapFill                   -7         gap          )
		( annotation                -6         ann          )
		( OPCAntiSerif              -5         opa          )
		( OPCSerif                  -4         ops          )
		( slot                      -3         slt          )
		( fill                      -2         fil          )
		( drawing                   -1         drw          )
		( fatal                     223        fat          )
		( critical                  224        crt          )
		( soCritical                225        scr          )
		( soError                   226        ser          )
		( ackWarn                   227        ack          )
		( info                      228        inf          )
		( track                     229        trk          )
		( blockage                  230        blk          )
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
		( net                       253        net          )
		( cell                      254        cel          )
		( all                       255        all          )
	) ;techPurposes
	
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

techLayers(
	;( LayerName                 Layer#     Abbreviation )
	;( ---------                 ------     ------------ )
	;User-Defined Layers:
	( NWELL	 1 NWELL )
	( DNW	 2 DNW   )
	( DIFF	 3 DIFF  )
	( PIMP	 4 PIMP  )
	( NIMP	 5 NIMP  )
	( DIFF_18 6 DIFF_18 )
	( PAD	 7 PAD      )
	( ESD_25 8 ESD_25   )
	( SBLK	 9  SBLK    )
	( PO	 10 PO      )
	( M1	 11 M1      )
	( VIA1	 12 VIA1    )
	( M2	 13 M2      )
	( VIA2	 14 VIA2    )
	( M3	 15 M3      )
	( VIA3	 16 VIA3    )
	( M4	 17 M4      )
	( VIA4	 18 VIA4    )
	( M5	 19 M5      )
	( VIA5	 20 VIA5    )
	( M6	 21 M6      )
	( VIA6	 22 VIA6    )
	( M7	 23 M7      )
	( VIA7	 24 VIA7 )
	( M8	 25 M8      )
	( VIA8	 26 VIA8  )
	( M9	 27 M9      )
	( CO	 28 CO      )
	( HVTIMP 29 HVTIMP )
	( LVTIMP 30 LVTIMP )
	( M1PIN	 31 M1PIN )
	( M2PIN	 32 M2PIN )
	( M3PIN	 33 M3PIN )
	( M4PIN	 34 M4PIN )
	( M5PIN	 35 M5PIN )
	( M6PIN	 36 M6PIN )
	( M7PIN	 37 M7PIN )
	( M8PIN	 38 M8PIN )	
	( M9PIN	 39 M9PIN )
	( MRDL   41 MRDL  ) 
	( VIARDL 42 VIARDL ) 
	( MRPIN  43 MRPIN ) 
	( HOTNWL 44 HOTNWL )
	( DIOD	 46 DIOD )
	( BJTMY  47 BJTMY )
	( RNW	 48 RNW )
	( RMARK	 49 RMARK )
	( PrBoundary	50 PrBoundary )
	( LOGO	 51 LOGO )
	( IP	 52 IP )
	( RM1	 53 RM1 )
	( RM2	 54 RM2 )
	( RM3	 55 RM3 )
	( RM4	 56 RM4 )
	( RM5	 57 RM5 )
	( RM6	 58 RM6 )
	( RM7	 59 RM7 )
	( RM8	 60 RM8 )
	( RM9	 61 RM9 )
	( DM1EXCL 64 DM1EXCL )
	( DM2EXCL 65 DM2EXCL )
	( DM3EXCL 66 DM3EXCL )
	( DM4EXCL 67 DM4EXCL )
	( DM5EXCL 68 DM5EXCL )
	( DM6EXCL 69 DM6EXCL )
	( DM7EXCL 70 DM7EXCL )
	( DM8EXCL 71 DM8EXCL )
	( DM9EXCL 72 DM9EXCL )
	( DIFFEXCL 73 DIFFEXCL )
	( POEXCL   74 POEXCL )
	( DIFF_25  75 DIFF_25 )
 ( CBMMARK	76   )
 ( CTMMARK      77   )
 ( METDMY       78   )

)

techLayerPurposePriorities(
	;layers are ordered from lowest to highest priority
	;( LayerName                 Purpose    )
	;( ---------                 -------    )
	( NWELL	drawing )
	( DNW	drawing )
	( DIFF	drawing )
	( PIMP	drawing )
	( NIMP	drawing )
	( DIFF_18	drawing )
	( PAD	drawing )
	( ESD_25	drawing )
	( SBLK	drawing )
	( PO	drawing )
	( M1	drawing )
	( M2	drawing )
	( M3	drawing )
	( M4	drawing )
	( M5	drawing )
	( M6	drawing )
	( M7	drawing )
	( M8	drawing )
	( M9	drawing )
	( CO	drawing )
	( VIA1	drawing )
	( VIA2	drawing )
	( VIA3	drawing )
	( VIA4	drawing )
	( VIA5	drawing )
	( VIA6	drawing )
	( VIA7	drawing )
	( VIA8	drawing )
	( HVTIMP	drawing )
	( LVTIMP	drawing )
	( M1	text )
	( M2	text )
	( M3	text )
	( M4	text )
	( M5	text )
	( M6	text )
	( M7	text )
	( M8	text )
	( M9	text )
	( M1PIN		drawing )
	( M2PIN		drawing )
	( M3PIN		drawing )
	( M4PIN		drawing )
	( M5PIN		drawing )
	( M6PIN		drawing )
	( M7PIN		drawing )
	( M8PIN		drawing ) 
	( M9PIN		drawing )
	( MRDL		drawing )
	( VIARDL	drawing )
	( MRPIN		drawing )
	( HOTNWL	drawing )
	( DIOD		drawing )
	( BJTMY		drawing )
	( RNW		drawing )
	( RMARK		drawing )
	( LOGO		drawing )
	( IP		drawing )
	( PrBoundary	drawing )
	( RM1	drawing )
	( RM2	drawing )
	( RM3	drawing )
	( RM4	drawing )
	( RM5	drawing )
	( RM6	drawing )
	( RM7	drawing )
	( RM8	drawing )
	( RM9	drawing )
	( DM1EXCL	drawing )
	( DM2EXCL	drawing )
	( DM3EXCL	drawing )
	( DM4EXCL	drawing )
	( DM5EXCL	drawing )
	( DM6EXCL	drawing )
	( DM7EXCL	drawing )
	( DM8EXCL	drawing )
	( DM9EXCL	drawing )
	( DIFFEXCL 	drawing )
	( POEXCL	drawing )
	( DIFF_25	drawing )
	( CBMMARK	drawing   )
 ( CTMMARK      drawing   )
 ( METDMY       drawing   )

) ;techLayerPurposePriorities
	
techDisplays(
	;( LayerName    Purpose      Packet          Vis Sel Con2ChgLy DrgEnbl Valid )
	;( ---------    -------      ------          --- --- --------- ------- ----- )
	( NWELL		drawing		NWELL		t t nil t t  )
	( DNW		drawing		DNW		t t nil t t  )
	( DIFF		drawing		DIFF		t t nil t t  )
	( PIMP		drawing		PIMP		t t nil t t  )
	( NIMP		drawing		NIMP		t t nil t t  )
	( DIFF_18	drawing		DIFF_18		t t nil t t  )
	( PAD		drawing		PAD		t t nil t t  )
	( ESD_25	drawing		ESD_25		t t nil t t  )
	( SBLK		drawing		SBLK		t t nil t t  )
	( PO		drawing		PO		t t nil t t  )
	( M1		drawing		M1		t t nil t t  )
	( M2		drawing		M2		t t nil t t  )
	( M3		drawing		M3		t t nil t t  )
	( M4		drawing		M4		t t nil t t  )
	( M5		drawing		M5		t t nil t t  )
	( M6		drawing		M6		t t nil t t  )
	( M7		drawing		M7		t t nil t t  )
	( M8		drawing		M8		t t nil t t  )
	( M9		drawing		M9		t t nil t t  )
	( M1		text		M1PIN		t t nil t t  )
	( M2		text		M2PIN		t t nil t t  )
	( M3		text		M3PIN		t t nil t t  )
	( M4		text		M4PIN		t t nil t t  )
	( M5		text		M5PIN		t t nil t t  )
	( M6		text		M6PIN		t t nil t t  )
	( M7		text		M7PIN		t t nil t t  )
	( M8		text		M8PIN		t t nil t t  )
	( M9		text		M9PIN		t t nil t t  )
	( CO		drawing		CO		t t nil t t  )
	( VIA1		drawing		VIA1		t t nil t t  )
	( VIA2		drawing		VIA2		t t nil t t  )
	( VIA3		drawing		VIA3		t t nil t t  )
	( VIA4		drawing		VIA4		t t nil t t  )
	( VIA5		drawing		VIA5		t t nil t t  )
	( VIA6		drawing		VIA6		t t nil t t  )
	( VIA7		drawing		VIA7		t t nil t t  )
	( VIA8		drawing		VIA8		t t nil t t  )
	( HVTIMP	drawing		HVTIMP		t t nil t t  )
	( LVTIMP	drawing		LVTIMP		t t nil t t  )
	( M1PIN		drawing		M1PIN		t t nil t t  )
	( M2PIN		drawing		M2PIN		t t nil t t  )
	( M3PIN		drawing		M3PIN		t t nil t t  )
	( M4PIN		drawing		M4PIN		t t nil t t  )
	( M5PIN		drawing		M5PIN		t t nil t t  )
	( M6PIN		drawing		M6PIN		t t nil t t  )
	( M7PIN		drawing		M7PIN		t t nil t t  )
	( M8PIN		drawing		M8PIN		t t nil t t  )
	( M9PIN		drawing		M9PIN		t t nil t t  )
	( MRDL		drawing		MRDL		t t nil t t  )
	( VIARDL	drawing		VIARDL		t t nil t t  )
	( MRPIN		drawing		MRPIN		t t nil t t  )
	( HOTNWL	drawing		HOTNWL		t t nil t t  )
	( DIOD		drawing		DIOD		t t nil t t  )
	( BJTMY		drawing		BJTMY		t t nil t t  )
	( RNW		drawing		RNW		t t nil t t  )
	( RMARK		drawing		RMARK		t t nil t t  )
	( LOGO		drawing		LOGO		t t nil t t  )
	( IP		drawing		IP		t t nil t t  )
	( PrBoundary		drawing		PrBoundary		t t nil t t  )
	( RM1		drawing		RM1		t t nil t t  )
	( RM2		drawing		RM2		t t nil t t  )
	( RM3		drawing		RM3		t t nil t t  )
	( RM4		drawing		RM4		t t nil t t  )
	( RM5		drawing		RM5		t t nil t t  )
	( RM6		drawing		RM6		t t nil t t  )
	( RM7		drawing		RM7		t t nil t t  )
	( RM8		drawing		RM8		t t nil t t  )
	( RM9		drawing		RM9		t t nil t t  )
	( DM1EXCL		drawing		DM1EXCL		t t nil t t  )
	( DM2EXCL		drawing		DM2EXCL		t t nil t t  )
	( DM3EXCL		drawing		DM3EXCL		t t nil t t  )
	( DM4EXCL		drawing		DM4EXCL		t t nil t t  )
	( DM5EXCL		drawing		DM5EXCL		t t nil t t  )
	( DM6EXCL		drawing		DM6EXCL		t t nil t t  )
	( DM7EXCL		drawing		DM7EXCL		t t nil t t  )
	( DM8EXCL		drawing		DM8EXCL		t t nil t t  )
	( DM9EXCL		drawing		DM9EXCL		t t nil t t  )
	( DIFFEXCL 		drawing 	DIFFEXCL        t t nil t t  )
        ( POEXCL		drawing 	POEXCL          t t nil t t  )
        ( DIFF_25		drawing 	DIFF_25         t t nil t t  )
        ( CBMMARK		drawing 	CBMMARK         t t nil t t    )
        ( CTMMARK		drawing 	CTMMARK         t t nil t t    )
        ( METDMY 		drawing 	METDMY         t t nil t t    )

);techDisplays

	techLayerProperties(
		;( PropName               Layer1 [ Layer2 ]           PropValue )
		;( --------               ------ ----------           --------- )
		( sheetResistance        DIFF                       0.001 )
		( sheetResistance        PO                         15    )	
		( sheetResistance        M1                         0.1	  )
		( sheetResistance        M2                         0.1	  )
		( sheetResistance        M3                         0.1	  )
		( sheetResistance        M4                         0.1	  )
		( sheetResistance        M5                         0.1	  )
		( sheetResistance        M6                         0.1	  )
		( sheetResistance        M7                         0.1	  )
		( sheetResistance        M8                         0.1	  )
		( sheetResistance        M9                         0.28	)
		( sheetResistance	 MRDL			    0.35	)
		( sheetResistance        VIA1 			1.5   	)
		( sheetResistance        VIA2 			1.5   	)
		( sheetResistance        VIA3 			1.5   	)
		( sheetResistance        VIA4 			1.5   	)
		( sheetResistance        VIA5 			1.5   	)
		( sheetResistance        VIA6 			1.5   	)
		( sheetResistance        VIA7 			1.5   	)
		( sheetResistance        VIA8 			0.1   	)
		( sheetResistance	 VIARDL			0.05		)
		
	) ;techLayerProperties

	
	techDerivedLayers(
		;( DerivedLayerName          #          composition  )
		;( ----------------          ------     ------------ )
	) ;techDerivedLayers

) ;layerDefinitions

;********************************
; LAYER RULES
;********************************


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
layerRules(

 equivalentLayers(
 ;( list of layers )
 ;( -------------- )
 ) ;equivalentLayers

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
 
 
 functions(
 ;( layer                       function        [maskNumber])
 ;( -----                       --------        ------------)
	( NWELL  "nWell"        1 )
	( DIFF 	"diffusion" 	2 )
	( DIFF_18 "diffusion" 	3 )
	( DIFF_25 "diffusion" 	4 )
	( PIMP 	"pImplant" 	5 )
	( NIMP 	"nImplant" 	6 )
	( M1 	"metal" 	7 )
	( VIA1 	"cut" 	        8 )
	( M2 	"metal" 	9 )
	( VIA2 	"cut" 	        10 )
	( M3 	"metal" 	11 )
	( VIA3 	"cut" 	        12 )
	( M4 	"metal" 	13 )
	( VIA4 	"cut" 	        14 )
	( M5 	"metal" 	15 )
	( VIA5 	"cut" 	        16 )
	( M6 	"metal" 	17 )
	( VIA6 	"cut" 	        18 )
	( M7 	"metal" 	19 )
	( M8 	"metal" 	20 )
	( M9 	"metal" 	21 )
	( MRDL  "metal"		22 ) 
	( VIARDL "cut"		23 )
	( VIA7 	"cut" 	24 )
	( VIA8 	"cut" 	25 )
	( CO 	"cut" 	26 )
	( BJTMY 	"other" 	27 )
	( DIOD	 	"other" 	28 )
	( DM1EXCL 	"other" 	29 )
	( DM2EXCL 	"other" 	30 )
	( DM3EXCL 	"other" 	31 )
	( DM4EXCL 	"other" 	32 )
	( DM5EXCL 	"other" 	33 )
	( DM6EXCL 	"other" 	34 )
	( DM7EXCL 	"other" 	35 )
	( DM8EXCL 	"other" 	36 )
	( DM9EXCL 	"other" 	37 )
	( DNW 		"other" 	38 )
	( ESD_25 	"other" 	39 )
	( HOTNWL 	"other" 	40 )
	( HVTIMP 	"other" 	41 )
	( IP 		"other" 	42 )
	( LOGO 		"other" 	43 )
	( LVTIMP 	"other" 	44 )
	( M1PIN 	"other" 	45 )
	( M2PIN 	"other" 	46 )
	( M3PIN 	"other" 	47 )
	( M4PIN 	"other" 	48 )
	( M5PIN 	"other" 	49 )
	( M6PIN 	"other" 	50 )
	( M7PIN 	"other" 	51 )
	( M8PIN 	"other" 	52 )
	( M9PIN 	"other" 	53 )
	( MRPIN		"other"		54 )
	( PAD 		"other" 	55 )
	( PO 		"other" 	56 )
	( RM1 		"other" 	57 )
	( RM2 		"other" 	58 )
	( RM3 		"other" 	59 )
	( RM4 		"other" 	60 )
	( RM5 		"other" 	61 )
	( RM6 		"other" 	62 )
	( RM7 		"other" 	63 )
	( RM8 		"other" 	64 )
	( RM9 		"other" 	65 )
	( RNW 		"other" 	66 )
	( RMARK 	"other" 	67 )
	( SBLK 		"other" 	69 )
	( PrBoundary 	"other" 	70 )
	( CBMMARK	"other"		71   )
        ( CTMMARK     	"other"		72   )
        ( METDMY       	"other"		73   )

	
  
 ) ;functions

 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


 mfgResolutions(
 ;( layer                       mfgResolution )
 ;( -----                       ------------- )
	( BJTMY  	0.001)
	( CO  		0.001)
	( DIFF  	0.001)
	( DIFF_18  	0.001)
	( DIFF_25	0.001)
	( DIOD  	0.001)
	( DM1EXCL  	0.001)
	( DM2EXCL  	0.001)
	( DM3EXCL  	0.001)
	( DM4EXCL  	0.001)
	( DM5EXCL  	0.001)
	( DM6EXCL  	0.001)
	( DM7EXCL  	0.001)
	( DM8EXCL  	0.001)
	( DM9EXCL  	0.001)
	( DNW  		0.001)
	( ESD_25  	0.001)
	( HOTNWL  	0.001)
	( HVTIMP  	0.001)
	( IP  		0.001)
	( LOGO  	0.001)
	( LVTIMP  	0.001)
	( M1  	0.001)
	( M2  	0.001)
	( M3  	0.001)
	( M4  	0.001)
	( M5  	0.001)
	( M6  	0.001)
	( M7  	0.001)
	( M8  	0.001)
	( M9  	0.001)
	( MRDL  0.001)
	( NIMP  0.001)
	( NWELL 0.001)
	( PAD  	0.001)
	( PIMP  0.001)
	( PO  	0.001)
	( RM1  	0.001)
	( RM2  	0.001)
	( RM3  	0.001)
	( RM4  	0.001)
	( RM5  	0.001)
	( RM6  	0.001)
	( RM7  	0.001)
	( RM8  	0.001)
	( RM9  	0.001)
	( RNW  	0.001)
	( RMARK  	0.001)
	( SBLK  	0.001)
	( VIA1  	0.001)
	( VIA2  	0.001)
	( VIA3  	0.001)
	( VIA4  	0.001)
	( VIA5  	0.001)
	( VIA6  	0.001)
	( VIA7  	0.001)
	( VIA8  	0.001)
	( VIARDL	0.001)
	( PrBoundary  	0.001)
	( CBMMARK	0.001   )
	( CTMMARK      0.001   )
	( METDMY       0.001   )

 ) ;mfgResolutions

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  
  
 routingDirections(
 ;( layer                       direction     )
 ;( -----                       ---------     )
  ( M1 horizontal )
  ( M2 vertical   )
  ( M3 horizontal )
  ( M4 vertical   )
  ( M5 horizontal )
  ( M6 vertical   )
  ( M7 horizontal )
  ( M8 vertical   )
  ( M9 horizontal )
  ( MRDL vertical )
 ) ;routingDirections
 
 
  
 currentDensity(
 ;( rule                	layer1    	layer2    	value    )
 ;( ----                	------    	------    	-----    )
 ) ;currentDensity

 currentDensityTables(
 ;( rule                	layer1    
 ;  (( index1Definitions	[index2Definitions]) [defaultValue] )
 ;  (table))
 ;( ----------------------------------------------------------------------)
 ) ;currentDensityTables

) ;layerRules

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;********************************
; VIADEFS
;********************************

viaDefs(

 standardViaDefs(
 ;( viaDefName	layer1	layer2	(cutLayer cutWidth cutHeight [resistancePerCut]) 
 ;   (cutRows	cutCol	(cutSpace)) 
 ;   (layer1Enc) (layer2Enc)	(layer1Offset)	(layer2Offset)	(origOffset) 
 ;   [implant1	 (implant1Enc)	[implant2	(implant2Enc)]]) 
 ;( -------------------------------------------------------------------------- ) 

  ( DIFFCON      DIFF   M1
    ("CO" 0.042 0.042 ) (1 1 (0.05 0.05)) 
    (0.02 0.01)(0.035 0.004)	
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( DIFFCONC      DIFF   M1
    ("CO" 0.042 0.042 ) (1 1 (0.05 0.05)) 
    (0.01 0.02)(0.035 0.004)	
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )
  
  ( POLYCON1      PO   M1
    ("CO" 0.042 0.042 )    (1 1 (0.05 0.05)) 
    (0.05 0.02)(0.035 0.004)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( POLYCON1C      PO   M1
    ("CO" 0.042 0.042 )    (1 1 (0.05 0.05)) 
    (0.02 0.05)(0.035 0.004)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( POLYCON2      PO   M1
    ("CO" 0.042 0.042 )    (1 1 (0.05 0.05)) 
    (0.034 0.02)(0.035 0.004)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( POLYCON2C      PO   M1
    ("CO" 0.042 0.042 )    (1 1 (0.05 0.05)) 
    (0.02 0.034)(0.035 0.004)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA12      M1   M2
    ("VIA1" 0.05 0.05 1.5)    (1 1 (0.07 0.07)) 
    (0.03 0.005) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA12C      M1   M2
    ("VIA1" 0.05 0.05 1.5)    (1 1 (0.07 0.07)) 
    (0.005 0.03) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )
  
  ( VIA12BAR      M1   M2
    ("VIA1" 0.05 0.1 1.0)    (1 1 (0.085 0.085)) 
    (0.03 0.005) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA12BARC      M1   M2
    ("VIA1" 0.05 0.1 1.0)    (1 1 (0.085 0.085)) 
    (0.005 0.03) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA12LG      M1   M2
    ("VIA1" 0.1 0.1 0.5)    (1 1 (0.085 0.085)) 
    (0.03 0.005) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA12LGC      M1   M2
    ("VIA1" 0.1 0.1 0.5)    (1 1 (0.085 0.085)) 
    (0.005 0.03) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )
  
;----------------------------------------------------  
  ( VIA23      M2   M3
    ("VIA2" 0.05 0.05 1.5)    (1 1 (0.07 0.07)) 
    (0.03 0.005)(0.03 0.005)	
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA23C      M2   M3
    ("VIA2" 0.05 0.05 1.5)    (1 1 (0.07 0.07)) 
    (0.005 0.03)(0.03 0.005)	
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA23BAR      M2   M3
    ("VIA2" 0.05 0.1 1.0)    (1 1 (0.085 0.085)) 
    (0.03 0.005) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA23BARC      M2   M3
    ("VIA2" 0.05 0.1 1.0)    (1 1 (0.085 0.085)) 
    (0.005 0.03) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA23LG      M2   M3
    ("VIA2" 0.1 0.1 0.5)    (1 1 (0.085 0.085)) 
    (0.03 0.005) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )
  
  ( VIA23LGC      M2   M3
    ("VIA2" 0.1 0.1 0.5)    (1 1 (0.085 0.085)) 
    (0.005 0.03) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )
  
;-----------------------------------------------------  
  
  ( VIA34      M3   M4
    ("VIA3" 0.05 0.05 1.5)    (1 1 (0.07 0.07)) 
    (0.03 0.005)(0.03 0.005)	
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA34C      M3   M4
    ("VIA3" 0.05 0.05 1.5)    (1 1 (0.07 0.07)) 
    (0.005 0.03)(0.03 0.005)	
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )
  
  ( VIA34BAR      M3   M4
    ("VIA3" 0.05 0.1 1.0)    (1 1 (0.085 0.085)) 
    (0.03 0.005) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA34BARC      M3   M4
    ("VIA3" 0.05 0.1 1.0)    (1 1 (0.085 0.085)) 
    (0.005 0.03) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA34LG      M3   M4
    ("VIA3" 0.1 0.1 0.5)    (1 1 (0.085 0.085)) 
    (0.03 0.005) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )
  
  ( VIA34LGC      M3   M4
    ("VIA3" 0.1 0.1 0.5)    (1 1 (0.085 0.085)) 
    (0.005 0.03) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  
;------------------------------------------------------  
  ( VIA45      M4   M5
    ("VIA4" 0.05 0.05 1.5)    (1 1 (0.07 0.07)) 
    (0.03 0.005)(0.03 0.005)	
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA45C      M4   M5
    ("VIA4" 0.05 0.05 1.5)    (1 1 (0.07 0.07)) 
    (0.005 0.03)(0.03 0.005)	
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA45BAR      M4   M5
    ("VIA4" 0.05 0.1 1.0)    (1 1 (0.085 0.085)) 
    (0.03 0.005) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA45BARC      M4   M5
    ("VIA4" 0.05 0.1 1.0)    (1 1 (0.085 0.085)) 
    (0.005 0.03) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA45LG      M4   M5
    ("VIA4" 0.1 0.1 0.5)    (1 1 (0.085 0.085)) 
    (0.03 0.005) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA45LGC      M4   M5
    ("VIA4" 0.1 0.1 0.5)    (1 1 (0.085 0.085)) 
    (0.005 0.03) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )
  
;-------------------------------------------------------
  ( VIA56      M5   M6
    ("VIA5" 0.05 0.05 1.5)    (1 1 (0.07 0.07)) 
    (0.03 0.005)(0.03 0.005)	
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA56C      M5   M6
    ("VIA5" 0.05 0.05 1.5)    (1 1 (0.07 0.07)) 
    (0.005 0.03)(0.03 0.005)	
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA56BAR      M5   M6
    ("VIA5" 0.05 0.1 1.0)    (1 1 (0.085 0.085)) 
    (0.03 0.005) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA56BARC      M5   M6
    ("VIA5" 0.05 0.1 1.0)    (1 1 (0.085 0.085)) 
    (0.005 0.03) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA56LG      M5   M6
    ("VIA5" 0.1 0.1 0.5)    (1 1 (0.085 0.085)) 
    (0.03 0.005) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )
  
  ( VIA56LGC      M5   M6
    ("VIA5" 0.1 0.1 0.5)    (1 1 (0.085 0.085)) 
    (0.005 0.03) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )
  
;-------------------------------------------------------
  ( VIA67      M6   M7
    ("VIA6" 0.05 0.05 1.5)    (1 1 (0.07 0.07)) 
    (0.03 0.005)(0.03 0.005)	
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA67C      M6   M7
    ("VIA6" 0.05 0.05 1.5)    (1 1 (0.07 0.07)) 
    (0.005 0.03)(0.03 0.005)	
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )
  
  ( VIA67BAR      M6   M7
    ("VIA6" 0.05 0.1 1.0)    (1 1 (0.085 0.085)) 
    (0.03 0.005) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA67BARC      M6   M7
    ("VIA6" 0.05 0.1 1.0)    (1 1 (0.085 0.085)) 
    (0.005 0.03) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA67LG      M6   M7
    ("VIA6" 0.1 0.1 0.5)    (1 1 (0.085 0.085)) 
    (0.03 0.005) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA67LGC      M6   M7
    ("VIA6" 0.1 0.1 0.5)    (1 1 (0.085 0.085)) 
    (0.005 0.03) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )
  
  
;---------------------------------------------------------  
  ( VIA78      M7   M8
    ("VIA7" 0.05 0.05 1.5)    (1 1 (0.07 0.07)) 
    (0.03 0.005)(0.03 0.005)	
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA78C      M7   M8
    ("VIA7" 0.05 0.05 1.5)    (1 1 (0.07 0.07)) 
    (0.005 0.03)(0.03 0.005)	
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )
  
  ( VIA78BAR      M7   M8
    ("VIA7" 0.05 0.1 1.0)    (1 1 (0.085 0.085)) 
    (0.03 0.005) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA78BARC      M7   M8
    ("VIA7" 0.05 0.1 1.0)    (1 1 (0.085 0.085)) 
    (0.005 0.03) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA78LG      M7   M8
    ("VIA7" 0.1 0.1 0.5)    (1 1 (0.085 0.085)) 
    (0.03 0.005) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )
  

  ( VIA78LGC      M7   M8
    ("VIA7" 0.1 0.1 0.5)    (1 1 (0.085 0.085)) 
    (0.005 0.03) (0.03 0.005)
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )
  
  
;---------------------------------------------------------  
  ( VIA89      M8   M9
    ("VIA8" 0.13 0.13 0.1)    (1 1 (0.12 0.12)) 
    (0.03 0.015)(0.03 0.015)	
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

  ( VIA89C      M8   M9
    ("VIA8" 0.13 0.13 0.1)    (1 1 (0.12 0.12)) 
    (0.015 0.03)(0.03 0.015)	
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )


  ( VIARDL      M9   MRDL
    ("VIARDL" 2 2 0.05)    (1 1 ( 2 2 )) 
    (0.05 0.05)(0.05 0.05)	
    (0.0 0.0) (0.0 0.0) (0.0 0.0)
  )

 ) ;standardViaDefs

 customViaDefs(
 ;( viaDefName libName cellName viewName layer1 layer2 resistancePerCut)
 ;( ---------- ------- -------- -------- ------ ------ ----------------)
 
 ) ;customViaDefs

) ;viaDefs;********************************
; CONSTRAINT GROUPS
;********************************

constraintGroups(

 ; Connectivity
 ( leCEConstraintGroup nil
     ( validRoutingLayers (VIARDL VIA8 VIA7 VIA6 VIA5 VIA4 VIA3 VIA2  VIA1 
                            MRDL M9 M8 M7 M6 M5 M4 M3 M2 M1 
                            CO PO DIFF))
     ( validRoutingVias	( DIFFCON DIFFCONC POLYCON1 POLYCON1C 
    		    POLYCON2 POLYCON2C VIA12 VIA12C 
    		    VIA12BAR VIA12BARC VIA12LG VIA12LGC 
    		    VIA23 VIA23C VIA23BAR VIA23BARC 
    		    VIA23LG VIA23LGC 
    		    VIA34 VIA34C VIA34BAR VIA34BARC VIA34LG 
    		    VIA34LGC 
    		    VIA45 VIA45C VIA45BAR VIA45BARC 
    		    VIA45LG VIA45LGC 
    		    VIA56 VIA56C VIA56BAR VIA56BARC VIA56LG 
    		    VIA56LGC VIA67 VIA67C VIA67BAR VIA67BARC 
    		    VIA67LG VIA67LGC VIA78 VIA78C VIA78BAR 
    		    VIA78BARC VIA78LG VIA78LGC VIA89 VIA89C 
    		    VIARDL   ) 
     )
 ) ;leCEConstraintGroup


 ;( group	[override] )
 ;( -----	---------- )
  ( "foundry"	t
  
    spacings(
    
     ( minWidth                   "NWELL"	0.23  )
     ( minSpacing                 "NWELL"	0.23  )
     ( minDiffPotentialSpacing    "NWELL"       0.46  )
     ( minArea			  "NWELL"	0.45  )
     ( minEnclosedArea		  "NWELL"       0.45  )
     ( minSpacing                 "DNW"		3.5   )
     ( minWidth                   "DNW"		3     )
     ( minWidth                   "DIFF"	0.044 )
     ( minSpacing                 "DIFF"	0.05  )
     ( minArea                    "DIFF"	0.02  )
     ( minEnclosedArea		  "DIFF"        0.03  )
     ( minWidth                   "DIFF_18"	0.33  )
     ( minSpacing                 "DIFF_18"	0.33  )
     ( minArea                    "DIFF_18"	0.4   )
     ( minEnclosedArea		  "DIFF_18"     0.4   )
     ( minWidth                   "PO"		0.03  )
     ( minSpacing                 "PO"		0.086 )
     ( minArea                    "PO"		0.012 )
     ( minWidth                   "PIMP"  	0.102 )
     ( minSpacing                 "PIMP"       	0.17  )
     ( minWidth                   "NIMP"       	0.102 )
     ( minSpacing                 "NIMP"       	0.17  )
     ( minWidth                   "CO"		0.042 )
     ( maxLength		  "CO"  	0.042 )
     ( maxWidth 		  "CO"  	0.042 )
     ( minSpacing                 "CO"		0.05  )
     ( minWidth                   "M1"	        0.05  )
     ( maxWidth                   "M1"	        5     )
     ( minSpacing                 "M1"	        0.05  )
     ( minArea			  "M1"		0.01  )
     ( minEnclosedArea            "M1"		0.2   )
     ( minWidth                   "VIA1"	0.05  )
     ( maxLength		  "VIA1"	0.1   )
     ( maxWidth 		  "VIA1"	0.1   )
     ( minSpacing                 "VIA1"	0.07  )
     ( minWidth                   "M2"		0.056 )
     ( maxWidth                   "M2"	        5     )
     ( minSpacing                 "M2"		0.056 )
     ( minArea			  "M2"		0.016 )
     ( minEnclosedArea            "M2"		0.2   )
     ( minWidth                   "VIA2"	0.05  )
     ( maxLength		  "VIA2"	0.1   )
     ( maxWidth 		  "VIA2"	0.1   )
     ( minSpacing                 "VIA2"	0.07  )
     ( minWidth                   "M3"		0.056 )
     ( maxWidth                   "M3"	        5     )
     ( minSpacing                 "M3"		0.056 )
     ( minArea			  "M3"		0.016 )
     ( minEnclosedArea            "M3"		0.2   )
     ( minWidth                   "VIA3"	0.05  )
     ( maxLength		  "VIA3"	0.1   )
     ( maxWidth 		  "VIA3"	0.1   )
     ( minSpacing                 "VIA3"	0.07  )
     ( minWidth                   "M4"		0.056 )
     ( maxWidth                   "M4"	        5     )
     ( minSpacing                 "M4"		0.056 )
     ( minArea			  "M4"		0.016 )
     ( minEnclosedArea            "M4"		0.2   )
     ( minWidth                   "VIA4"	0.05  )
     ( maxLength		  "VIA4"	0.1   )
     ( maxWidth 		  "VIA4"	0.1   )
     ( minSpacing                 "VIA4"	0.07  )
     ( minWidth                   "M5"		0.056 )
     ( maxWidth                   "M5"	        5     )
     ( minSpacing                 "M5"		0.056 )
     ( minArea			  "M5"		0.016 )
     ( minEnclosedArea            "M5"		0.2   )
     ( minWidth                   "VIA5"	0.05  )
     ( maxLength		  "VIA5"	0.1   )
     ( maxWidth 		  "VIA5"	0.1   )
     ( minSpacing                 "VIA5"	0.07  )
     ( minWidth                   "M6"		0.056 )
     ( maxWidth                   "M6"	        5     )
     ( minSpacing                 "M6"		0.056 )
     ( minArea			  "M6"		0.016 )
     ( minEnclosedArea            "M6"		0.2   )
     ( minWidth                   "VIA6"	0.05  )
     ( maxLength		  "VIA6"	0.1   )
     ( maxWidth 		  "VIA6"	0.1   )
     ( minSpacing                 "VIA6"	0.07  )
     ( minWidth                   "M7"		0.056 )
     ( maxWidth                   "M7"	        5     )
     ( minSpacing                 "M7"		0.056 )
     ( minArea			  "M7"		0.016 )
     ( minEnclosedArea            "M7"		0.2   )
     ( minWidth                   "VIA7"	0.05  )
     ( maxLength		  "VIA7"	0.1   )
     ( maxWidth 		  "VIA7"	0.1   )
     ( minSpacing                 "VIA7"	0.07  )
     ( minWidth                   "M8"		0.056 )
     ( maxWidth                   "M8"	        5     )
     ( minSpacing                 "M8"		0.056 )
     ( minArea			  "M8"		0.016 )
     ( minEnclosedArea            "M8"		0.2   )
     ( minWidth                   "VIA8"	0.13  )
     ( maxLength		  "VIA8"	0.13  )
     ( maxWidth 		  "VIA8"	0.13  )
     ( minSpacing                 "VIA8"	0.12  )
     ( minWidth                   "M9"		0.16  )
     ( maxWidth                   "M9"	        10    )
     ( minSpacing                 "M9"		0.16  )
     ( minArea			  "M9"		0.055 )
     ( minEnclosedArea            "M9"		0.2   )
     ( minWidth                   "MRDL"	2     )
     ( maxWidth                   "MRDL"	30    )
     ( minSpacing                 "MRDL"	2     )
     ( minWidth                   "VIARDL"	2     )
     ( maxLength		  "VIARDL"	2     )
     ( maxWidth 		  "VIARDL"	2     )
     ( minSpacing                 "VIARDL"	2     )
     ( minWidth			  "HVTIMP"	0.85  )
     ( minSpacing		  "HVTIMP"	0.85  )
     ( minWidth			  "LVTIMP"	0.85  )
     ( minSpacing		  "LVTIMP"	0.85  )
     ( minWidth                   "SBLK"	0.33  )
     ( minSpacing                 "SBLK"	0.33  )
     ( minWidth                   "DIFF_25"	0.33  )
     ( minSpacing                 "DIFF_25"	0.33  )
     ( minArea                    "DIFF_25"	0.4   )
     ( minEnclosedArea		  "DIFF_25"     0.4   )
     ( minSpacing                 "NWELL"	"DIFF"		0.065 )
     ( minSpacing                 "PIMP"	"DIFF"		0.02  )
     ( minSpacing                 "NIMP"	"DIFF"		0.02  )
     ( minSpacing                 "DIFF_18"	"DIFF"		0.15  )
     ( minSpacing                 "DIFF_25"	"DIFF"		0.15  )
     ( minSpacing                 "M1"		"VIA1"		0.08  )
     ( minSpacing                 "M2"		"VIA2"		0.08  )
     ( minSpacing                 "M3"		"VIA3"		0.08  )
     ( minSpacing                 "M4"		"VIA4"		0.08  )
     ( minSpacing                 "M5"		"VIA5"		0.08  )
     ( minSpacing                 "M6"		"VIA6"		0.08  )
     ( minSpacing                 "M7"		"VIA7"		0.08  )
     ( minSpacing                 "M8"		"VIA8"		0.08  )
     ( minSpacing                 "CO"		"PO"		0.04  )
     ( minSpacing                 "CO"		"DIFF"		0.04  )
     ( minSpacing                 "CO"		"SBLK"		0.13  )
     ( minSpacing                 "DIFF"	"PO"		0.02  )
     ( minSpacing                 "NIMP"	"PIMP"		0.00  )
     ( minEnclosure  		  "PO" 		"DIFF" 		0.08  )
     ( minEnclosure  		  "DIFF_18" 	"DIFF" 		0.15  )
     ( minEnclosure  		  "DIFF_25" 	"DIFF" 		0.15  )



	( minSpacing  "NWELL" "DNW" 2.5 )
	( minSpacing  "DNW"  "DIFF" 1.5 )
	( minSpacing  "SBLK" "DIFF" 0.18 )
	( minSpacing  "SBLK" "PO" 0.3 )   

    ) ;spacings

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


  orderedSpacings(
	( minEnclosure  "NWELL" "DIFF" 0.065 )
	( minEnclosure  "M1" "VIA1" 0.005 )
	( minEnclosure  "M2" "VIA1" 0.005 )
	( minEnclosure  "M2" "VIA2" 0.005 )
	( minEnclosure  "M3" "VIA2" 0.005 )
	( minEnclosure  "M3" "VIA3" 0.005 )
	( minEnclosure  "M4" "VIA3" 0.005 )
	( minEnclosure  "M4" "VIA4" 0.005 )
	( minEnclosure  "M5" "VIA4" 0.005 )
	( minEnclosure  "M5" "VIA5" 0.005 )
	( minEnclosure  "M6" "VIA5" 0.005 )
	( minEnclosure  "M6" "VIA6" 0.005 )
	( minEnclosure  "M7" "VIA6" 0.005 )
	( minEnclosure  "M7" "VIA7" 0.005 )
	( minEnclosure  "M8" "VIA7" 0.005 )
	( minEnclosure  "NWELL" "DNW" 1 )
	( minEnclosure  "M8" "VIA8" 0.015 )
	( minEnclosure  "M9" "VIA8" 0.015 )
	( minEnclosure  "MRDL" "VIARDL" 0.5 )
	( minEnclosure  "PIMP" "DIFF" 0.02  )
	( minEnclosure  "NIMP" "DIFF" 0.02  )
	( minEnclosure  "HVTIMP" "DIFF" 0.05 )
	( minEnclosure  "LVTIMP" "DIFF" 0.05 )
	( minEnclosure  "SBLK" "DIFF" 0.18 )
	( minEnclosure  "PO" "SBLK"   0.18 )
	( minEnclosure  "PO" "DIFF"   0.08 )
	( minEnclosure  "DIFF" "CO"   0.01 )
	( minEnclosure  "M1" "CO" 0.002 )
	( endOfLineEnclosure  "M1" "VIA1" 0.005 )
	( endOfLineEnclosure  "M2" "VIA1" 0.005 )
	( endOfLineEnclosure  "M2" "VIA2" 0.005 )
	( endOfLineEnclosure  "M3" "VIA2" 0.005 )
	( endOfLineEnclosure  "M3" "VIA3" 0.005 )
	( endOfLineEnclosure  "M4" "VIA3" 0.005 )
	( endOfLineEnclosure  "M4" "VIA4" 0.005 )
	( endOfLineEnclosure  "M5" "VIA4" 0.005 )
	( endOfLineEnclosure  "M5" "VIA5" 0.005 )
	( endOfLineEnclosure  "M6" "VIA5" 0.005 )
	( endOfLineEnclosure  "M6" "VIA6" 0.005 )
	( endOfLineEnclosure  "M7" "VIA6" 0.005 )
	( endOfLineEnclosure  "M7" "VIA7" 0.005 )
	( endOfLineEnclosure  "M8" "VIA7" 0.005 )
	( endOfLineEnclosure  "M8" "VIA8" 0.03 )
	( endOfLineEnclosure  "M9" "VIA8" 0.03 )
	( endOfLineEnclosure  "DIFF" "CO" 0.01 )
	( endOfLineEnclosure  "M1" "CO" 0.02 )
  ) ;orderedSpacings

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;	
  
  
    spacings(
    ;( constraint		layer1		[layer2]	value  )
    ;( ----------		------		--------	-----  )
	( defWidth  "CO" 0.042 )	
	( defWidth  "DIFF" 0.12 )
	( defWidth  "DIFF_18" 0.33 )
	( defWidth  "DM1EXCL" 0.45 )
	( defWidth  "DM2EXCL" 0.45 )
	( defWidth  "DM3EXCL" 0.45 )
	( defWidth  "DM4EXCL" 0.45 )
	( defWidth  "DM5EXCL" 0.45 )
	( defWidth  "DM6EXCL" 0.45 )
	( defWidth  "DM7EXCL" 0.45 )
	( defWidth  "DM8EXCL" 0.45 )
	( defWidth  "DM9EXCL" 0.45 )
	( defWidth  "DNW" 3  )
	( defWidth  "HVTIMP" 0.85 )
	( defWidth  "IP" 0.1 )
	( defWidth  "LOGO" 0.45 )
	( defWidth  "LVTIMP" 0.85 )
	( defWidth  "M1" 0.05 )
	;( defWidth  "M1DMY" 0.1 )
	( defWidth  "M2" 0.056 )
	;( defWidth  "M2DMY" 0.1 )
	( defWidth  "M3" 0.056 )
	;( defWidth  "M3DMY" 0.1 )
	( defWidth  "M4" 0.056 )
	;( defWidth  "M4DMY" 0.1 )
	( defWidth  "M5" 0.056 )
	;( defWidth  "M5DMY" 0.1 )
	( defWidth  "M6" 0.056 )
	;( defWidth  "M6DMY" 0.1 )
	( defWidth  "M7" 0.056 )
	;( defWidth  "M7DMY" 0.1 )
	( defWidth  "M8" 0.056 )
	;( defWidth  "M8DMY" 0.1 )
	( defWidth  "M9" 0.16 )
	;( defWidth  "M9DMY" 0.1 )
	( defWidth    "MRDL" 2 ) 
	( defWidth  "NIMP" 0.102 )
	( defWidth  "NWELL" 0.65 )
	( defWidth  "PAD" 30 )
	( defWidth  "PIMP" 0.102 )
	( defWidth  "PO" 0.03 )
	( defWidth  "SBLK" 0.33 )
	( defWidth  "VIA1" 0.05 )
	( defWidth  "VIA2" 0.05 )
	( defWidth  "VIA3" 0.05 )
	( defWidth  "VIA4" 0.05 )
	( defWidth  "VIA5" 0.05 )
	( defWidth  "VIA6" 0.05 )
	( defWidth  "VIA7" 0.05 )
	( defWidth  "VIA8" 0.13 )
	( defWidth  "VIARDL" 2  )
	( defWidth  "PrBoundary" 0.45 )

    ) ;spacings

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;	
	
    interconnect(
	
	 
     ( validLayers   (CO DIFF DIFF_18 M1 M1PIN M2 M2PIN M3 M3PIN M4 M4PIN M5 M5PIN M6 M6PIN M7 M7PIN M8 M8PIN M9 M9PIN MRDL PO VIA1 VIA2 VIA3 VIA4 VIA5 VIA6 VIA7 VIA8 VIARDL ) )
	 
    ) ;interconnect

  ) ;foundry
 
 ( "LEFDefaultRouteSpec"   nil
     ( minWidth         		CO      	      	 0.042 )
     ( horizontalRouteGridPitch 	M1              	 0.2 )
     ( verticalRouteGridPitch 		M1              	 0.2 )
     ( horizontalRouteGridOffset 	M1              	 0.1 )
     ( verticalRouteGridOffset 		M1              	 0.1 )
     ( minWidth         		M1              	 0.05 )
     ( minWireExtension 		M1              	 0.105 )
     ( minWidth         		VIA1              	 0.05 )
     ( horizontalRouteGridPitch 	M2              	 0.3 )
     ( verticalRouteGridPitch 		M2              	 0.3 )
     ( horizontalRouteGridOffset 	M2			 0.15 )
     ( verticalRouteGridOffset 		M2			 0.15 )
     ( minWidth         		M2			 0.056 )
     ( minWireExtension 		M2			 0.105 )
     ( minWidth         		VIA2              	 0.05 )
     ( horizontalRouteGridPitch 	M3			 0.3 )
     ( verticalRouteGridPitch 		M3			 0.3 )
     ( horizontalRouteGridOffset 	M3			 0.15 )
     ( verticalRouteGridOffset 		M3			 0.15 )
     ( minWidth         		M3			 0.056 )
     ( minWireExtension 		M3			 0.105 )
     ( minWidth         		VIA3              	 0.05 )
     ( horizontalRouteGridPitch 	M4			 0.3 )
     ( verticalRouteGridPitch 		M4			 0.3 )
     ( horizontalRouteGridOffset 	M4			 0.15 )
     ( verticalRouteGridOffset 		M4			 0.15 )
     ( minWidth         		M4			 0.056 )
     ( minWireExtension 		M4			 0.105 )
     ( validRoutingLayers 	 (PO M1   M2   M3   M4 M5 M6 M7 M8 M9 MRDL  )
      )
     ( validRoutingVias 	 (VIA12 VIA12BAR VIA12LG VIA12C VIA12BARC VIA12LGC  VIA23 VIA23BAR VIA23LG VIA23C VIA23BARC VIA23LGC VIA34 VIA34BAR VIA34LG VIA34C VIA34BARC VIA34LGC POLYCON1 POLYCON1C POLYCON2 POLYCON2C DIFFCON VIA45 VIA45BAR VIA45LG  VIA56 VIA56BAR VIA56LG VIA67 VIA67BAR VIA67LG  VIA78 VIA78BAR VIA78LG VIA89 )
      )
  );LEFDefaultRouteSpec
 
 
 
) ;constraintGroups;********************************
; DEVICES
;********************************
devices(
tcCreateCDSDeviceClass()
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

