snaDefaultRegionBias = '( )
;
snaGeneration = '(
   ( "TIE" nil (( "P1" )) "default" "contact"  "Resistive"  "metal1"  "Unique" 1e1 -1 1 0  "inline" )

   ( "pcapacitor" ( ( "model" "snacapacitor" ) ) (( "MINUS" )( "PLUS" )) "default" "default"  "Resistive"  "device"  "Unique" 1e4 -1 0 0  "new" )

)
;
snaSelection = '(
   ( "nmos" nil (( "B" )( "S"  "D" )( "G" )) "default" "channel"  "Resistive"  "device"  "Unique" 1e4 -1 0 0  "parallel" )
   ( "nmoshv" nil (( "B" )( "S"  "D" )( "G" )) "default" "channel"  "Resistive"  "device"  "Unique" 1e4 -1 0 0  "parallel" )
   ( "pmos" nil (( "B" )( "S"  "D" )( "G" )) "nwell" "channel"  "Resistive"  "device"  "Unique" 1e4 -1 0 0  "parallel" )
   ( "pmoshv" nil (( "B" )( "S"  "D" )( "G" )) "nwell" "channel"  "Resistive"  "device"  "Unique" 1e4 -1 0 0  "parallel" )
   ( "nplusres" nil (( "B" )( "MINUS" )( "PLUS" )) "default" "source_drain"  "Resistive" "device"  "Unique" 1e4 -1 0 0 "new" )
   ( "pplusres" nil (( "B" )( "MINUS" )( "PLUS" )) "nwell" "source_drain"  "Resistive" "device"  "Unique" 1e4 -1 0 0 "new" )
   ( "nmoscap" nil (( "B" )( "S"  "D" )( "G" )) "default" "channel"  "Resistive"  "device"  "Unique" 1e4 -1 0 0  "new" )
   ( "pmoscap" nil (( "B" )( "S"  "D" )( "G" )) "nwell" "channel"  "Resistive"  "device"  "Unique" 1e4 -1 0 0  "new" )
   ( "polyres" nil (( "PLUS" )( "MINUS" )) "default" "default"  "Capacitive"  "poly"  "Unique" 1e4 -1 0 0  "inline" )
   ( "mimcap" nil (( "MINUS" )( "PLUS" )) "default" "default"  "Capacitive"  "metal2"  "Unique" 1e4 -1 0 0  "inline" )
   ( "xjvar_w40" nil (( "BULK" )( "CATHODE" )( "ANODE" )) "default" "deep_device"  "Resistive" "device"  "Unique" 1e4 -1 0 0 "new" )
   ( "xjvar_nf36" nil (( "BULK" )( "CATHODE" )( "ANODE" )) "default" "deep_device"  "Resistive" "device"  "Unique" 1e4 -1 0 0 "new" )
)
;

snaRegions = '(
   ( ( "SNA"  "nwell" ) "nwell" ( (1.8 "VDD") ) )
   ( ( "SNA"  "nwelld" ) "deep_nwell" ( (1.8 "VDD") ) )
   ( ( "SNA"  "tpwell" ) "triple_well" ( (0.0 "VSS" ) (1.8 "VDD") ) )
)
;
snaViewSelection = '(
( "Instances"
)

( "Layout"
)

( "Substrate Abstract View" 
)

( "Surface Mesh" 
)

( "Surface Distribution" 
)

( "Perturbing Path" 
)

)
;

snaLayersAndPurposes = '(
  ( "SNA"   "region"  )  ; this LPP is used to display REGIONS
  ( "SNA"  "port"  )  ; this LPP is used to display ACCESS PORTS
  ( "SNA"  "port1" )  ; this LPP is used to HIGHLIGHT ACCESS PORTS
  ( "SNA"  "drawing"  )  ; this LPP is used to display SURFACE NOISE DISTRIBUTION for LEVEL 0 ( low noise )
  ( "SNA"  "drawing1" )  ; this LPP is used to display SURFACE NOISE DISTRIBUTION for LEVEL 1
  ( "SNA"  "drawing2" )  ; this LPP is used to display SURFACE NOISE DISTRIBUTION for LEVEL 2
  ( "SNA"  "drawing3" )  ; this LPP is used to display SURFACE NOISE DISTRIBUTION for LEVEL 3
  ( "SNA"  "drawing4" )  ; this LPP is used to display SURFACE NOISE DISTRIBUTION for LEVEL 4
  ( "SNA"  "drawing5" )  ; this LPP is used to display SURFACE NOISE DISTRIBUTION for LEVEL 5
  ( "SNA"  "drawing6" )  ; this LPP is used to display SURFACE NOISE DISTRIBUTION for LEVEL 6
  ( "SNA"  "drawing7" )  ; this LPP is used to display SURFACE NOISE DISTRIBUTION for LEVEL 7
  ( "SNA"  "drawing8" )  ; this LPP is used to display SURFACE NOISE DISTRIBUTION for LEVEL 8
  ( "SNA"  "drawing9" )  ; this LPP is used to display SURFACE NOISE DISTRIBUTION for LEVEL 9 ( high noise )
  ( "SNA"  "ppath"  )  ; this LPP is used to display PERTURBING PATH at substrate SURFACE
  ( "y0"  "drawing" )  ; this LPP is used to display PERTURBING PATH in substrate DEPTH
  ( "SNA"  "label"    )  ; this LPP is used to display the NOISE level VALUES
  ( "SNA"  "grid"  )  ; this LPP is used to display substrate surface MESH
  ( "y1" "drawing"  )  ; this LPP is used to display the MACRO port MASK
)

;After Saving SAV:
snaPostProcessingGenerateSAV = '("hooknoiseport" t nil )
;snaPostProcessingSaveSAV = '("mysnaHookPostSaveSAV" t nil )
;snaPostProcessingSaveSAV = '("snaHookCheckScaleFactor" t nil )
; Before Substrate Model Extraction:
; Note: the following hook is editable in GUI. If you do not want the user
; to be able to edit it, replace first field 't' with  'nil' .
;snaPreProcessingExtract = '("snaHookCopySubstrateSubckt" t  nil )

; After Substrate Model Extraction:
; Note: the following hook is not editable in GUI. If you want the user
; to be able to edit it, replace first field 'nil' with  't' .
;snaPostProcessingExtract = '("snaHookCompareDate" nil  nil )
;snaPostProcessingExtract = '("snaHookDisplaySubstrateSubckt" t  nil )
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; The following section enables the user to attach a Recognition ;
; Shape to an instance in Extracted View that does not have any  ;
;   Recognition Shape by default ( Application: ASSURA flow )    ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;snaRecognitionShapeLayer = list( "device" "net" )



