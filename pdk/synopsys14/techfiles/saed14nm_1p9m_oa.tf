
;#################################################################
;# SAED 14nm 1p9m CustomCompiler technology file		 #
;#								 #
;# Revision History:						 #
;# Rev.		date		what				 #
;# --------------------------------------------------------------#	
;# 1.0		10/Nov/2016	(First draft)                    #
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
	) ;techParams
	
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
		( 0.001 )
	) ;mfgGridResolution

	colors (
		(red blue)
	)
	


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
leMPPMasterPath 	("defaultPath" 		"M1" 		drawing		0.05 		extend	 	t   	t
userParams (name width layer purpose conn chop )
) ; Master Path

;             		name 	            	layer 		purpose 	enclosure 	path-style 	conn    chop
leMPPEnclosedPath 	("diffEncPath"	 	"DIFF"		drawing 	0.006          	extend	 	t       nil
userParams (name layer purpose enclosure conn chop)
) ; Enclosed Path

;             		name 	            	layer 		purpose 	enclosure 	path-style 	conn    chop
leMPPEnclosedPath 	("pplusEncPath" 	"PIMP"		drawing 	0.06          	extend	 	t  	nil
userParams (name layer purpose enclosure conn chop)
) ; Enclosed Path

;             		name 	            	layer 		purpose 	enclosure 	path-style 	conn    chop
leMPPEnclosedPath 	("nplusEncPath" 	"NIMP"		drawing 	0.06         	extend	 	t 	nil
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
leMPPSubRect (defaultContacts CTM1 drawing 0.05 0.03 t t 0.004 0.035 0.045 fit 1
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
	( FIN	 1 FIN )
	( FINCUT	 2 FINCUT )
	( NWELL	 3 NWELL )
	( DNW	 4 DNW   )
	( DIFF	 5 DIFF  )
	( PIMP	 6 PIMP  )
	( NIMP	 7 NIMP  )
	( DIFF_15 8 DIFF_15 )
	( DIFF_18 9 DIFF_18 )
	( PAD	 10 PAD      )
	( ESD 11 ESD   )
	( SBLK	 12  SBLK    )
	( PO	 13 PO      )
	( POCUT	 14 POCUT      )
	( TSLCO	 15 TSLCO      )
	( TSLCB	 16 TSLCB      )
	( CTM1	 17 CTM1      )
	( CPO	 18 CPO      )
	( M1	 19 M1      )
	( M1_3	 90 M1_3    ) 	
	( VIA0	 81 VIA0    )
	( VIA1	 20 VIA1    )
	( M2	 21 M2      )
	( M2_3	 91 M2_3    )	
	( VIA2	 22 VIA2    )
	( M3	 23 M3      )
	( M3_3	 92 M3_3    )	
	( VIA3	 24 VIA3    )
	( M4	 25 M4      )
	( VIA4	 26 VIA4    )
	( M5	 27 M5      )
	( VIA5	 28 VIA5    )
	( M6	 29 M6      )
	( VIA6	 30 VIA6    )
	( M7	 31 M7      )
	( VIA7	 32 VIA7 )
	( M8	 33 M8      )
	( VIA8	 34 VIA8  )
	( M9	 35 M9      )	
	( HVTIMP 36 HVTIMP )
	( LVTIMP 37 LVTIMP )
	( M1PIN	 38 M1PIN )
	( M2PIN	 39 M2PIN )
	( M3PIN	 40 M3PIN )
	( M4PIN	 41 M4PIN )
	( M5PIN	 42 M5PIN )
	( M6PIN	 43 M6PIN )
	( M7PIN	 44 M7PIN )
	( M8PIN	 45 M8PIN )	
	( M9PIN	 46 M9PIN )
	( MRDL   47 MRDL  ) 
	( VIARDL 48 VIARDL ) 
	( MRPIN  49 MRPIN ) 
	( HOTNWL 50 HOTNWL ) ; removal may be needed
	( DIOD	 51 DIOD )
	( BJTMY  52 BJTMY )
	( RNW	 53 RNW )
	( RMARK	 54 RMARK )
	( PrBoundary	55 PrBoundary )
	( LOGO	 56 LOGO )
	( IP	 57 IP )
	( RM1	 58 RM1 )
	( RM2	 59 RM2 )
	( RM3	 60 RM3 )
	( RM4	 61 RM4 )
	( RM5	 62 RM5 )
	( RM6	 63 RM6 )
	( RM7	 64 RM7 )
	( RM8	 65 RM8 )
	( RM9	 66 RM9 )
	( DM1EXCL 67 DM1EXCL )
	( DM2EXCL 68 DM2EXCL )
	( DM3EXCL 69 DM3EXCL )
	( DM4EXCL 70 DM4EXCL )
	( DM5EXCL 71 DM5EXCL )
	( DM6EXCL 72 DM6EXCL )
	( DM7EXCL 73 DM7EXCL )
	( DM8EXCL 74 DM8EXCL )
	( DM9EXCL 75 DM9EXCL )
	( DIFFEXCL 76 DIFFEXCL )
	( POEXCL   77 POEXCL )	
	( CBMMARK	78   CBMM)
	( CTMMARK      79   CTMM)
 	( METDMY       80   MDMY)
	(DIFFCUT 82 DIFFCUT) 
	(AXPOLY 83 AXPOLY) 
	(SLVTIMP 84 SLVTIMP) 
	(FGATE 85 FGATE) 
	(B_VIA0 86 B_VIA0)

)

techLayerPurposePriorities(
	;layers are ordered from lowest to highest priority
	;( LayerName                 Purpose    )
	;( ---------                 -------    )
	( FIN	drawing )
	( FINCUT	drawing )
	( NWELL	drawing )
	( DNW	drawing )
	( DIFF	drawing )
	( PIMP	drawing )
	( NIMP	drawing )
	( DIFFCUT drawing)	;sh
	( DIFF_15	drawing )
	( DIFF_18	drawing )
	( PAD	drawing )	
	( ESD	drawing )
	( SBLK	drawing )
	( PO	drawing )
	( POCUT	drawing )
	( TSLCO	drawing )
	( TSLCB	drawing )
	( CPO	drawing )
	( M1	drawing )
	( M1	pin )
	( M1_3	drawing )
	( M2	drawing )
	( M2	pin )
	( M2_3	drawing )
	( M3	drawing )
	( M3	pin )
	( M3_3	drawing )
	( M4	drawing )
	( M4	pin )
	( M5	drawing )
	( M5	pin )
	( M6	drawing )
	( M6	pin )
	( M7	drawing )
	( M7	pin )
	( M8	drawing )
	( M8	pin )
	( M9	drawing )
	( M9	pin )
	( VIA0	drawing )
	( VIA1	drawing )
	( VIA2	drawing )
	( VIA3	drawing )
	( VIA4	drawing )
	( VIA5	drawing )
	( VIA6	drawing )
	( VIA7	drawing )
	( VIA8	drawing )
 	( SLVTIMP       drawing   )
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
	( MRDL	text )
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
	( MRDL		pin )
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
	( CBMMARK	drawing   )
 ( CTMMARK      drawing   )
 ( METDMY       drawing   )
 ( AXPOLY       drawing   )

 ( FGATE       drawing   )
 ( B_VIA0       drawing   )

) ;techLayerPurposePriorities
	
techDisplays(
	;( LayerName    Purpose      Packet          Vis Sel Con2ChgLy DrgEnbl Valid )
	;( ---------    -------      ------          --- --- --------- ------- ----- )
	( FIN         drawing         FIN           t t nil t t  )
	( FINCUT         drawing         FINCUT           t t nil t t  )
	( NWELL		drawing		NWELL		t t nil t t  )
	( DNW		drawing		DNW		t t nil t t  )
	( DIFF		drawing		DIFF		t t nil t t  )
	( PIMP		drawing		PIMP		t t nil t t  )
	( NIMP		drawing		NIMP		t t nil t t  )
	( DIFF_18	drawing		DIFF_18		t t nil t t  )
	( PAD		drawing		PAD		t t nil t t  )
	( ESD		drawing		ESD		t t nil t t  )
	( SBLK		drawing		SBLK		t t nil t t  )
	( PO		drawing		PO		t t nil t t  )
	( CPO		drawing		CPO		t t nil t t  )
	( POCUT		drawing		POCUT		t t nil t t  )
	( TSLCO		drawing		TSLCO		t t nil t t  )
	( TSLCB		drawing		TSLCB		t t nil t t  )
	( CTM1		drawing		CTM1		t t nil t t  )
	( M1		drawing		M1		t t nil t t  )
	( M1_3		drawing		M1_3		t t nil t t  )
	( M2		drawing		M2		t t nil t t  )
	( M2_3		drawing		M2_3		t t nil t t  )
	( M3		drawing		M3		t t nil t t  )
	( M3_3		drawing		M3_3		t t nil t t  )
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
	( MRDL		text		MRPIN		t t nil t t  )
; kh :	( CO		drawing		CO		t t nil t t  )
	( VIA0		drawing		VIA0		t t nil t t  ) 
	( DIFFCUT	drawing		DIFFCUT		t t nil t t  ) 
	( AXPOLY	drawing		AXPOLY		t t nil t t  ) 
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
        ( DIFF_15		drawing 	DIFF_15         t t nil t t  )
        ( CBMMARK		drawing 	CBMMARK         t t nil t t    )
        ( CTMMARK		drawing 	CTMMARK         t t nil t t    )
        ( METDMY 		drawing 	METDMY         t t nil t t    )
        ( SLVTIMP 		drawing 	SLVTIMP         t t nil t t    )
        ( FGATE 		drawing 	FGATE         t t nil t t    )
        ( B_VIA0 		drawing 	B_VIA0         t t nil t t    )

);techDisplays

	techLayerProperties(
		;( PropName               Layer1 [ Layer2 ]           PropValue )
		;( --------               ------ ----------           --------- )
		( sheetResistance        DIFF                       0.001 )
		( sheetResistance        PO                         15    )	
		( sheetResistance        M1                         0.1	  )
		( sheetResistance        M1_3                       0.1	  )
		( sheetResistance        M2                         0.1	  )
		( sheetResistance        M2_3                       0.1	  )
		( sheetResistance        M3                         0.1	  )
		( sheetResistance        M3_3                       0.1	  )
		( sheetResistance        M4                         0.1	  )
		( sheetResistance        M5                         0.1	  )
		( sheetResistance        M6                         0.1	  )
		( sheetResistance        M7                         0.1	  )
		( sheetResistance        M8                         0.1	  )
		( sheetResistance        M9                         0.28	)
		( sheetResistance	 MRDL			    0.35	)
		( sheetResistance        VIA0 			1.5   	)	
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

									 ;sh added DerivedLayers to use in rules at line 1086+
	techDerivedLayers(
		;( DerivedLayerName          #          composition  )
		(gate 10007 (AND DIFF PO))
		(imp 10005 (OR PIMP NIMP))				 ;sh
		(ndiff 10001 (AND DIFF NIMP))				 ;sh
		(pdiff 10002 (AND PIMP DIFF))				 ;sh
		(npl_act 10003 (NOT NWELL ndiff))			 ;sh can we put (not nwell ndiff) insted of (and PWELL ndiff)?
		(ppl_act 10004 (AND NWELL pdiff))			 ;sh
		(DNW_O_1 10006 (AND NWELL DNW))				 ;sh
		;(ppl_act_inNwell 10007 (AND NWELL ppl_act))		 ;sh P+Act and P+ACT in NWell not same thing?  RULE NIMP.S.3 used line 1133
		;(npl_act_inPwell 10008 (AND PWELL npl_act))		 ;sh N+Act and N+ACT in PWell not same thing?  RULE PIMP.S.3 used line 1142
		(DIFF_15_18 10009 (OR DIFF_15 DIFF_18))
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
 ;( layer                       function        [maskNumber]		[numberOfColorMasks]		[defaultColor])
 ;( -----                       --------        ------------)
;( DNWELL            nWell          7            )
( NWELL             nWell          8            )
( DIFF              diffusion      9            )
( NIMP	            nImplant       5            )
( PIMP             pImplant       6            )
( PO              poly           10           )
;( CONT              cut            14           )
( M1                metal          15           )
( VIA1             cut            16           )
( M2                metal          17           )
( VIA2             cut            18           )
( M3                metal          19           )
( VIA3             cut            20           )
( M4                metal          21           )
( VIA4             cut            22           )
( M5                metal          23           )
( VIA5             cut            24           )
( M6                metal          25           )
( VIA6             cut            26           )
( M7                metal          27           )
( VIA7             cut            28           )
( M8                metal          29           )
( VIA8             cut            30           )
( M9                metal          31           )
;( VIA9            cut            32           )
( MRDL               metal          33           )
( VIARDL            cut            34           )
;( RDL               metal          35           )
;( POLY_CUT          recognition    50           )
( POCUT         recognition    50           )
; VIATOP            cut            32           )
;( MTOP-1            metal          31           )
;( VIATOP-1          cut            30           )
( CPO            contactlessMetal 11           )
( CTM1           contactlessMetal 12           )
;( M0DIFF2           contactlessMetal 13           )
( VIA0              cut            14           )
;( M0DIFF_CUT        recognition    51           )
( DIFFCUT          recognition    52           )
;( M1_CUT            recognition    53           )
;( POLY_WIDE         poly           10           )
;( VIA1213           cut            38           )
;( M13               metal          39           )

;	( FIN  other        1 )
;	( FINCUT  other        2 )
;	( NWELL  nWell        3 )
;	( DIFF 	diffusion 	4 )
;	( DIFFCUT other       2) ;sh
;	( DIFF_18 diffusion 	5 )
;	( PIMP 	pImplant 	6 )
;	( NIMP 	nImplant 	7 )
;	( M1 	metal 	8 		2		blue)
;	( M1_3 	metal 	87 		2		)
;	( VIA0 	cut 	        9 )
;	( VIA1 	cut 	        9 )
;	( M2 	metal 	10		2		blue)
;	( M2_3 	metal 	88 		2		)
;	( VIA2 	cut 	        11 )
;	( M3 	metal 	12 		2		blue)
;	( M3_3 	metal 	89 		2		)
;	( VIA3 	cut 	        13 )
;	( M4 	metal 	14 		2		blue)
;	( VIA4 	cut 	        15 )
;	( M5 	metal 	16 		2 		blue)
;	( VIA5 	cut 	        17 )
;	( M6 	metal 	18 		2 		blue)
;	( VIA6 	cut 	        19 )
;	( M7 	metal 	20 		2 		blue)
;	( M8 	metal 	21 		2 		blue)
;	( M9 	metal 	22 		2 		blue)
;	( MRDL  metal		23 ) 
;	( VIARDL cut		24 )
;	( VIA7 	cut 	25 )
;	( VIA8 	cut 	26 )
;	( BJTMY 	other 	27 )
;	( DIOD	 	other 	28 )
;	( DM1EXCL 	other 	29 )
;	( DM2EXCL 	other 	30 )
;	( DM3EXCL 	other 	31 )
;	( DM4EXCL 	other 	32 )
;	( DM5EXCL 	other 	33 )
;	( DM6EXCL 	other 	34 )
;	( DM7EXCL 	other 	35 )
;	( DM8EXCL 	other 	36 )
;	( DM9EXCL 	other 	37 )
;	( DNW 		other 	38 )
;	( ESD 	other 	39 )
;	( HOTNWL 	other 	40 )
;	( HVTIMP 	other 	41 )
;	( IP 		other 	42 )
;	( LOGO 		other 	43 )
;	( LVTIMP 	other 	44 )
;	( M1PIN 	other 	45 )
;	( M2PIN 	other 	46 )
;	( M3PIN 	other 	47 )
;	( M4PIN 	other 	48 )
;	( M5PIN 	other 	49 )
;	( M6PIN 	other 	50 )
;	( M7PIN 	other 	51 )
;	( M8PIN 	other 	52 )
;	( M9PIN 	other 	53 )
;	( MRPIN		other		54 )
;	( PAD 		other 	55 )
;	( PO 		poly 	56 )
;	( RM1 		other 	57 )
;	( RM2 		other 	58 )
;	( RM3 		other 	59 )
;	( RM4 		other 	60 )
;	( RM5 		other 	61 )
;	( RM6 		other 	62 )
;	( RM7 		other 	63 )
;	( RM8 		other 	64 )
;	( RM9 		other 	65 )
;	( RNW 		other 	66 )
;	( RMARK 	other 	67 )
;	( SBLK 		other 	69 )
;	( PrBoundary 	other 	70 )
;	( CBMMARK	other		71   )
;       ( CTMMARK     	other		72   )
;      ( METDMY       	other		73   )
;     ( POCUT       	recognition		74   )
;    ( CTM1       	contactlessMetal		76   )
;   ( CPO       	contactlessMetal		75   )
;        ( AXPOLY       	other		83   )
;        ( SLVTIMP       	other		84   )
;        ( FGATE       	other		85   )
;        ( B_VIA0       	other		86   )
;
	
  
 ) ;functions

 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


 mfgResolutions(
 ;( layer                       mfgResolution )
 ;( -----                       ------------- )
	( BJTMY  	0.001)
	( DIFF  	0.001)
	( DIFFCUT	0.001) ;sh
	( DIFF_15  	0.001)
	( DIFF_18	0.001)
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
	( HOTNWL  	0.001)
	( HVTIMP  	0.001)
	( IP  		0.001)
	( LOGO  	0.001)
	( LVTIMP  	0.001)
	( M1  	0.001)
	( M1_3 	0.001)
	( M2  	0.001)
	( M2_3 	0.001)
	( M3  	0.001)
	( M3_3 	0.001)
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
	( VIA0  	0.001)
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
	( SLVTIMP       0.001   )
	( FGATE       0.001   )
	( B_VIA0       0.001   )

 ) ;mfgResolutions

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  
  
 routingDirections(
 ;( layer                       direction     )
 ;( -----                       ---------     )
  ( M1 horizontal )
  ( M1_3 horizontal )
  ( M2 vertical   )
  ( M2_3 vertical )
  ( M3 horizontal )
  ( M3_3 horizontal )
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

; kh :  ( DIFFCON      DIFF   M1
;    ("CO" 0.042 0.042 ) (1 1 (0.05 0.05)) 
;    (0.02 0.01)(0.035 0.004)	
;    (0.0 0.0) (0.0 0.0) (0.0 0.0)
;  )

;  ( DIFFCONC      DIFF   M1
;    ("CO" 0.042 0.042 ) (1 1 (0.05 0.05)) 
;    (0.01 0.02)(0.035 0.004)	
;    (0.0 0.0) (0.0 0.0) (0.0 0.0)
;  )
  
;  ( POLYCON1      PO   M1
;    ("CO" 0.042 0.042 )    (1 1 (0.05 0.05)) 
;    (0.05 0.02)(0.035 0.004)
;    (0.0 0.0) (0.0 0.0) (0.0 0.0)
;  )

;  ( POLYCON1C      PO   M1
;    ("CO" 0.042 0.042 )    (1 1 (0.05 0.05)) 
;    (0.02 0.05)(0.035 0.004)
;    (0.0 0.0) (0.0 0.0) (0.0 0.0)
;  )

;  ( POLYCON2      PO   M1
;    ("CO" 0.042 0.042 )    (1 1 (0.05 0.05)) 
;    (0.034 0.02)(0.035 0.004)
;    (0.0 0.0) (0.0 0.0) (0.0 0.0)
;  )

;  ( POLYCON2C      PO   M1
;    ("CO" 0.042 0.042 )    (1 1 (0.05 0.05)) 
;    (0.02 0.034)(0.035 0.004)
;    (0.0 0.0) (0.0 0.0) (0.0 0.0)
;  )

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
     ( validRoutingLayers ( 
                            MRDL M9 M8 M7 M6 M5 M4 M3 M2 M1 CPO CTM1 PO
                            ))
     ( validRoutingVias	(  
    		    VIA12 VIA12C 
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
  ( foundry	t
( constraintGroup 	 connectLayers ) 
    spacings(
;Other
     ;( minWidth        "CTM1"    	0.03 -spacingDirection horizontal)
     ( minHight		"CTM1"	  	0.05 )
     ( minSpacing	"gate"  "CTM1"  0.04 )				 ;sh spacing of new Contact fo PO
     ;( maxLength	"CTM1"	  	0.03 )
     ( minSpacing       "CTM1"	  	0.045)
     ( minSpacing       "FIN"		0.045)
     ( minSpacing       "ndiff"	"NWELL"	0.05 ) 				 ;sh should be nact to nwell

;NWELL
     ( minWidth                   "NWELL"	0.23  )
     ( minSpacing                 "NWELL"	0.23  )
     ( minDiffPotentialSpacing    "NWELL"       0.4  )			;sh 0.46
     ( minArea			  "NWELL"	0.2  )			;sh 0.45
     ( minEnclosedArea		  "NWELL"       0.2  )			;sh 0.45
     ( layerShapeAngle		  "NWELL" 	orthogonalOnly) 	;sh Not Working, but should
;DNW
     ( minSpacing                 "DNW"		3.3   )			;sh 3.5 CHECK
     ( minWidth                   "DNW"		1.8   )			;sh 3 CHECK
     ;(minSpacing 		  "DNW"		"uNWELL"	1.7)	;sh unrelated NWELL layer	 DNW.S.2
     ;(minSpacing 		  "DNW"		"ex_npl_NWELL"	1.5)	;sh external N+Active to DNW 	 DNW.S.3
     (minWidth			  "DNW_O_1"	0.4)			;sh DNW.O.1
     ;( minEnclosure  		  "DNW" 	"DIFF" 		0.5)    ;sh not working
     
;DIFF
     ( minWidth                   "DIFF"	0.044 )			;sh Value updated. What`s DIFF not DIFFCUT? Change DIFF by that layer
     ( maxWidth                   "DIFF"	23 )			;sh Value updated. What`s DIFF not DIFFCUT? Change DIFF by that layer
     ( minSpacing                 "DIFF"	0.08  )			;sh 0.05
     ;( minSpacing                 "DIFF" 	"FIN"	0.02  )		;sh NEW rule, check required
     ( minArea                    "DIFF"	0.009  )		;sh 0.02
     ( minEnclosedArea		  "DIFF"        0.03  )			;sh should this be REMOVE?
;DIFF_15
     ( minWidth                   "DIFF_15"	0.5  )			;sh 0.33 
     ( minSpacing                 "DIFF_15"	0.5  )			;sh 0.33
     ( minArea                    "DIFF_15"	0.2   )			;sh 0.4 
     ( minEnclosedArea		  "DIFF_15"     0.2   )			;sh 0.4 CHECK IF MIN/MAX ?
;    ( minSpacing                 "DIFF_15"	"ex_DIFF"	0.2 )	;sh DIFF_18.S.2 external DIFF layer?
;DIFF_18
     ( minWidth                   "DIFF_18"	0.5  )			;sh 0.33
     ( minSpacing                 "DIFF_18"	0.5  )			;sh 0.33
     ( minArea                    "DIFF_18"	0.2   )			;sh 0.4
     ( minEnclosedArea		  "DIFF_18"     0.2   )			;sh 0.4 CHECK IF MIN/MAX?
;    ( minSpacing                 "DIFF_15"	"ex_DIFF"	0.2 )	;sh DIFF_18.S.2 external DIFF layer?
;PO
     ( minWidth                   "PO"		0.014  )		;sh 0.03
     ( minSpacing                 "PO"		0.07 ) 			;sh ask for standart and C-space
     ( minArea                    "PO"		0.005 )			;sh 0.012
     ( minSpacing                 "PO"		"DIFF"		0.03 ) 	;sh
;PIMP
     ( minWidth                   "PIMP"  	0.17 )			;sh 0.102
     ( minSpacing                 "PIMP"       	0.17  )			;sh val updated
     ( minArea			  "PIMP"	0.07  )			;sh NEW rule, check required
;    ( minSpacing                 "PIMP" "npl_act_inPwell"    0.05 )	;sh npl_act_inPwell-> derivedLayers section
     ( minSpacing                 "PIMP"    "NWELL"   	0.3  )		;sh NEW rule, check required
;    ( minSpacing                 "PIMP"   	"npl_act"    	0.05 )	;sh N+ACT layer issue

;NIMP
     ( minWidth                   "NIMP"       	0.17 )			;sh 0.102
     ( minSpacing                 "NIMP"       	0.17 )
     ( minArea			  "NIMP"	0.07  )			;sh NEW rule, check required  
;    ( minSpacing                 "NIMP" "ppl_act_inNwell"    0.05 )	;sh ppl_act_inNwell-> derivedLayers section
     ( minSpacing                 "NIMP"    "NWELL"   	0.3  )		;sh NEW rule, check required
;    ( minSpacing                 "NIMP"   	"b_ppl_act"    	0 )	;sh layer butted P+ Active (P+ Active is ppl_act layer) also check value

;M1
     ( minWidth                   "M1"	        0.03  )			;sh 0.05
     ( maxWidth                   "M1"	        0.45  )			;sh 5
     ( minSpacing                 "M1"	        0.05  )			;sh should this exist? No M1 anymore.
    ;( minSpacing                 "M1_1"	  "M1_2"    0.03  )	;sh M1_1 and M1_2 not defined
     ( minArea			  "M1"		0.005  )		;sh 0.01
     ( minEnclosedArea            "M1"		0.04   )		;sh 0.2
;VIA1
     ( minWidth                   "VIA1"	0.05  )
     ( maxLength		  "VIA1"	0.1   )
     ( maxWidth 		  "VIA1"	0.1   )
     ( minSpacing                 "VIA1"	0.07  )
;M2
     ( minWidth                   "M2"		0.03  )			;sh 0.056 
     ( maxWidth                   "M2"	        0.45  )			;sh 5
     ( minSpacing                 "M2"		0.06  )			;sh 0.056
     ( minArea			  "M2"		0.009 )			;sh 0.016
     ( minEnclosedArea            "M2"		0.05   )		;sh 0.2
     ( minSpacing                 "M2"	"VIA2"	0.08  )			;sh 	
;VIA2
     ( minWidth                   "VIA2"	0.05  )
     ( maxLength		  "VIA2"	0.1   )
     ( maxWidth 		  "VIA2"	0.1   )
     ( minSpacing                 "VIA2"	0.07  )
;M3
     ( minWidth                   "M3"		0.03  )			;sh 0.056 
     ( maxWidth                   "M3"	        0.45  )			;sh 5
     ( minSpacing                 "M3"		0.06  )			;sh 0.056
     ( minArea			  "M3"		0.009 )			;sh 0.016
     ( minEnclosedArea            "M3"		0.05   )		;sh 0.2
     ( minSpacing                 "M3"	"VIA3"	0.08  )			;sh 	
;VIA3
     ( minWidth                   "VIA3"	0.05  )
     ( maxLength		  "VIA3"	0.1   )
     ( maxWidth 		  "VIA3"	0.1   )
     ( minSpacing                 "VIA3"	0.07  )
;M4
    ( minWidth                   "M4"		0.03  )			;sh 0.056 
     ( maxWidth                   "M4"	        0.45  )			;sh 5
     ( minSpacing                 "M4"		0.06  )			;sh 0.056
     ( minArea			  "M4"		0.009 )			;sh 0.016
     ( minEnclosedArea            "M4"		0.05   )		;sh 0.2
     ( minSpacing                 "M4"	"VIA4"	0.08  )			;sh 	
;VIA4
     ( minWidth                   "VIA4"	0.05  )
     ( maxLength		  "VIA4"	0.1   )
     ( maxWidth 		  "VIA4"	0.1   )
     ( minSpacing                 "VIA4"	0.07  )
;M5
     ( minWidth                   "M5"		0.03  )			;sh 0.056 
     ( maxWidth                   "M5"	        0.45  )			;sh 5
     ( minSpacing                 "M5"		0.06  )			;sh 0.056
     ( minArea			  "M5"		0.009 )			;sh 0.016
     ( minEnclosedArea            "M5"		0.05   )		;sh 0.2
     ( minSpacing                 "M5"	"VIA5"	0.08  )			;sh 	
;VIA5
     ( minWidth                   "VIA5"	0.05  )
     ( maxLength		  "VIA5"	0.1   )
     ( maxWidth 		  "VIA5"	0.1   )
     ( minSpacing                 "VIA5"	0.07  )
;M6
     ( minWidth                   "M6"		0.03  )			;sh 0.056 
     ( maxWidth                   "M6"	        0.45  )			;sh 5
     ( minSpacing                 "M6"		0.06  )			;sh 0.056
     ( minArea			  "M6"		0.009 )			;sh 0.016
     ( minEnclosedArea            "M6"		0.05   )		;sh 0.2
     ( minSpacing                 "M6"	"VIA6"	0.08  )			;sh 	
;VIA6
     ( minWidth                   "VIA6"	0.05  )
     ( maxLength		  "VIA6"	0.1   )
     ( maxWidth 		  "VIA6"	0.1   )
     ( minSpacing                 "VIA6"	0.07  )
;M7
      ( minWidth                   "M7"		0.03  )			;sh 0.056 
     ( maxWidth                   "M7"	        0.45  )			;sh 5
     ( minSpacing                 "M7"		0.06  )			;sh 0.056
     ( minArea			  "M7"		0.009 )			;sh 0.016
     ( minEnclosedArea            "M7"		0.05   )		;sh 0.2
     ( minSpacing                 "M7"	"VIA7"	0.08  )			;sh 	
;VIA7
     ( minWidth                   "VIA7"	0.05  )
     ( maxLength		  "VIA7"	0.1   )
     ( maxWidth 		  "VIA7"	0.1   )
     ( minSpacing                 "VIA7"	0.07  )
;M8
      ( minWidth                   "M8"		0.03  )			;sh 0.056 
     ( maxWidth                   "M8"	        0.45  )			;sh 5
     ( minSpacing                 "M8"		0.06  )			;sh 0.056
     ( minArea			  "M8"		0.009 )			;sh 0.016
     ( minEnclosedArea            "M8"		0.05   )		;sh 0.2
     ( minSpacing                 "M8"	"VIA8"	0.08  )			;sh 	
;VIA8
     ( minWidth                   "VIA8"	0.13  )
     ( maxLength		  "VIA8"	0.13  )
     ( maxWidth 		  "VIA8"	0.13  )
     ( minSpacing                 "VIA8"	0.12  )
;M9
     ( minWidth                   "M9"		0.03  )			;sh 0.16 
     ( maxWidth                   "M9"	        0.45  )			;sh 10
     ( minSpacing                 "M9"		0.06  )			;sh 0.16
     ( minArea			  "M9"		0.009 )			;sh 0.055
     ( minEnclosedArea            "M9"		0.05   )		;sh 0.2
     ;( minSpacing                 "M9"	"VIAT"	0.08  )			;sh spacing to what Via?	

;     ( minWidth                   "MT"		0.16  )			;sh 0.16 
;     ( maxWidth                   "MT"	       10  )			;sh 10
;     ( minSpacing                 "MT"		0.16  )			;sh 0.16
;     ( minArea			  "MT"		0.055 )			;sh 0.055
;     ( minEnclosedArea            "MT"		0.2   )			;sh 0.2

;CTM1
	( minSpacing                 "CTM1"		0.045  )	;sh New rule
	;( minSpacing                "CTM1"	"TSLO"	0.02 )		;sh TSLO layer not defined
        ( minArea		     "CTM1"		0.0008 )	;sh New rule
;CPO

	( minSpacing                 "CPO"		0.04  )		;sh New rule
	( minSpacing                 "CPO"	"DIFF_15_18"	0.03  ) ;sh New rule
	
;MRDL
     ( minWidth                   "MRDL"	2     )
     ( maxWidth                   "MRDL"	30    )
     ( minSpacing                 "MRDL"	2     )
;VIARDL
     ( minWidth                   "VIARDL"	2     )
     ( maxLength		  "VIARDL"	2     )
     ( maxWidth 		  "VIARDL"	2     )
     ( minSpacing                 "VIARDL"	2     )
;HVTIMP
     ( minWidth			  "HVTIMP"	0.85  )
     ( minSpacing		  "HVTIMP"	0.85  )
;LVTIMP
     ( minWidth			  "LVTIMP"	0.85  )
     ( minSpacing		  "LVTIMP"	0.85  )
;SBLK
     ( minWidth                   "SBLK"	0.07  )			;sh 0.33
     ( minSpacing                 "SBLK"	0.02  )			;sh 0.33
;rest
     ( minSpacing                 "NWELL"	"DIFF"		0.065 )	;sh might be removed
     ( minSpacing                 "PIMP"	"DIFF"		0.02  )
     ( minSpacing                 "NIMP"	"DIFF"		0.02  )
     ( minSpacing                 "DIFF_18"	"DIFF"		0.15  )
     ( minSpacing                 "DIFF_15"	"DIFF"		0.15  )
     ( minSpacing                 "M1"		"VIA1"		0.08  )
     ( minSpacing                 "M2"		"VIA2"		0.08  )
     ( minSpacing                 "M3"		"VIA3"		0.08  )
     ( minSpacing                 "M4"		"VIA4"		0.08  )
     ( minSpacing                 "M5"		"VIA5"		0.08  )
     ( minSpacing                 "M6"		"VIA6"		0.08  )
     ( minSpacing                 "M7"		"VIA7"		0.08  )
     ( minSpacing                 "M8"		"VIA8"		0.08  )
     ( minSpacing                 "DIFF"	"PO"		0.02  )
     ( minSpacing                 "NIMP"	"PIMP"		0.00  )
     ( minEnclosure  		  "PO" 		"DIFF" 		0.08  )
     ( minEnclosure  		  "DIFF_18" 	"DIFF" 		0.15  )



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
;	( minEnclosure  "DIFF" "CO"   0.01 )
;	( minEnclosure  "M1" "CO" 0.002 )
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
;	( endOfLineEnclosure  "DIFF" "CO" 0.01 )
;	( endOfLineEnclosure  "M1" "CO" 0.02 )
  ) ;orderedSpacings

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;	
  
  
    spacings(
    ;( constraint		layer1		[layer2]	value  )
    ;( ----------		------		--------	-----  )
;	( defWidth  "CO" 0.042 )	
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
	
	 
     ( validLayers   (DIFF DIFF_18 M1 M1PIN M2 M2PIN M3 M3PIN M4 M4PIN M5 M5PIN M6 M6PIN M7 M7PIN M8 M8PIN M9 M9PIN MRDL MRPIN PO VIA1 VIA2 VIA3 VIA4 VIA5 VIA6 VIA7 VIA8 VIARDL CPO CTM1 ) )
	 
    ) ;interconnect

  ) ;foundry
 
( connectLayers   -operator and
( leConnectingLayers	( PO CPO CTM1 ) )
( leConnectingLayers	( CTM1 CPO ) )
( leConnectingLayers	( VIA0 CTM1 CPO ) )
( leConnectingLayers	( DIFF CTM1 ) )
 );connectLayers
 ( "LEFDefaultRouteSpec"   nil
;     ( minWidth         		CO      	      	 0.042 )
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
     ( validRoutingVias 	 (VIA12 VIA12BAR VIA12LG VIA12C VIA12BARC VIA12LGC  VIA23 VIA23BAR VIA23LG VIA23C VIA23BARC VIA23LGC VIA34 VIA34BAR VIA34LG VIA34C VIA34BARC VIA34LGC VIA45 VIA45BAR VIA45LG  VIA56 VIA56BAR VIA56LG VIA67 VIA67BAR VIA67LG  VIA78 VIA78BAR VIA78LG VIA89 )
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

