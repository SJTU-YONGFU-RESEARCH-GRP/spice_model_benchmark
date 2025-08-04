;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;   SubstrateStorm Version 3.5.x       ;
; 28 Oct 2003, Cadence Design Systems  ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Bias Potential of region 'Default'
; To be defined when region 'Default'
; includes at least one p-n transition
; Example: snaDefaultRegionBias = '( ( 5.0 "VDD" ) )
snaDefaultRegionBias = '( )

; The following section is applied with
; menu 'AbstractView->Generate'
snaGeneration = '(
   ( "TIE" nil ( ( "P1" ) ) "default" "contact"  "Resistive"  "metal1"  "Unique" 1 -1 0 0  "inline" )
)
 

; The following section is applied with
; menu 'Define Access Ports' and mouse selection
; 'nil' could be replaced by a device property list.
; Example ( "nmos4" ( ( "model" "nfet" ) ( "w" 30.0e-6 ) ( "l" 5e-6 ) ) (( "B" ) ... "new" )
snaSelection = '(
  ( "nmos1v"       nil ( ( "B" ) ( "S" "D" ) ( "G" ) )  "default"  "channel"       "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "nmos1v_hvt"   nil ( ( "B" ) ( "S" "D" ) ( "G" ) )  "default"  "channel"       "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
; ( "nmos1v_iso"   nil ( ( "B" ) ( "S" "D" ) ( "G" ) )  "default"  "channel"       "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "nmos1v_nat"   nil ( ( "B" ) ( "S" "D" ) ( "G" ) )  "default"  "channel"       "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "nmos2v"       nil ( ( "B" ) ( "S" "D" ) ( "G" ) )  "default"  "channel"       "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "nmos2v_nat"   nil ( ( "B" ) ( "S" "D" ) ( "G" ) )  "default"  "channel"       "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "pmos1v"       nil ( ( "B" ) ( "S" "D" ) ( "G" ) )  "nwell"    "channel"       "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "pmos1v_hvt"   nil ( ( "B" ) ( "S" "D" ) ( "G" ) )  "nwell"    "channel"       "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "pmos2v"       nil ( ( "B" ) ( "S" "D" ) ( "G" ) )  "nwell"    "channel"       "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "pmoscap1v"    nil ( ( "B" ) ( "S" "D" ) ( "G" ) )  "nwell"    "channel"       "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "pmoscap2v"    nil ( ( "B" ) ( "S" "D" ) ( "G" ) )  "nwell"    "channel"       "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "pmoscap1v3"   nil ( ( "B" ) ( "S" "D" ) ( "G" ) )  "nwell"    "channel"       "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "pmoscap2v3"   nil ( ( "B" ) ( "S" "D" ) ( "G" ) )  "nwell"    "channel"       "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "nmoscap1v"    nil ( ( "B" ) ( "S" "D" ) ( "G" ) )  "default"  "channel"       "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "nmoscap2v"    nil ( ( "B" ) ( "S" "D" ) ( "G" ) )  "default"  "channel"       "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "nmoscap1v3"   nil ( ( "B" ) ( "S" "D" ) ( "G" ) )  "default"  "channel"       "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "nmoscap2v3"   nil ( ( "B" ) ( "S" "D" ) ( "G" ) )  "default"  "channel"       "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "ressndiff"    nil ( ( "B" ) ( "PLUS" "MINUS" ) )   "default"  "source_drain"  "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "resnsndiff"   nil ( ( "B" ) ( "PLUS" "MINUS" ) )   "default"  "source_drain"  "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "ressnpoly"    nil ( ( "B" ) ( "PLUS" "MINUS" ) )   "default"  "source_drain"  "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "resnsnpoly"   nil ( ( "B" ) ( "PLUS" "MINUS" ) )   "default"  "source_drain"  "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "resspdiff"    nil ( ( "B" ) ( "PLUS" "MINUS" ) )   "nwell"    "source_drain"  "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "resnspdiff"   nil ( ( "B" ) ( "PLUS" "MINUS" ) )   "nwell"    "source_drain"  "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "ressppoly"    nil ( ( "B" ) ( "PLUS" "MINUS" ) )   "nwell"    "source_drain"  "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "resnsppoly"   nil ( ( "B" ) ( "PLUS" "MINUS" ) )   "nwell"    "source_drain"  "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "resnwsti"     nil ( ( "B" ) ( "PLUS" "MINUS" ) )   "default"  "deep_device"   "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
  ( "resnwoxide"   nil ( ( "B" ) ( "PLUS" "MINUS" ) )   "default"  "deep_device"   "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )

; The following devices have been commented because there is an overlap between the device recognition and the nwell tie associated
;  with the device. Since the tie is of greater significance, the device selection has been commented.

; ( "ndio"         nil ( ( "PLUS" ) ( "MINUS" ) )       "default"  "source_drain"  "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )
; ( "pdio"         nil ( ( "MINUS" ) ( "PLUS" ) )       "nwell"    "source_drain"  "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )

; The following device definitions have been commented since the better way to consider these is to use the ties associated around
; them instead of the device itself

; ( "vpnp"         nil ( ( "E" ) ( "B" ) ( "C" ) )      "nwell"    "channel"       "Resistive"  "device"  "Unique" 1e4 -1 0 0 "new" )

; The following device definitions have been commented since there is no bulk node from the device to connect to the substrate. 
; If a device model is available with the appropriate bulk nodes, these devices could be considered for study

)
;

snaRegions = '(
   ( ( "SNA"  "nwell" ) "nwell" ( (1.2 "VDD") ) )
   ( ( "SNA"  "dnwell" ) "deep_nwell" ( (1.2 "VDD") ) )
   ( ( "SNA"  "ipwell" ) "triple_well" ( (0.0 "VSS" ) (1.2 "VDD") ) )
)
;
snaViewSelection = '(
( "Instances"
( "instance"  "drawing" )
( "device"    "drawing" )
)

( "Layout"
)

( "Substrate Abstract View" 
( "SNA"  "port" )
( "SNA"  "port1" )
( "SNA"  "region" )
( "SNA"  "macro" )
)

( "Surface Mesh" 
( "SNA" "macro" )
)

( "Surface Distribution" 
( "SNA"  "drawing" )
( "SNA"  "drawing1" )
( "SNA"  "drawing2" )
( "SNA"  "drawing3" )
( "SNA"  "drawing4" )
( "SNA"  "drawing5" )
( "SNA"  "drawing6" )
( "SNA"  "drawing7" )
( "SNA"  "drawing8" )
( "SNA"  "drawing9" )
)

( "Perturbing Path" 
( "SNA"  "drawing" )
( "SNA"  "drawing1" )
( "SNA"  "label" )
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
  ( "SNA"  "ppath1" )  ; this LPP is used to display PERTURBING PATH in substrate DEPTH
  ( "SNA"  "label"    )  ; this LPP is used to display the NOISE level VALUES
  ( "SNA"  "grid"  )  ; this LPP is used to display substrate surface MESH
  ( "SNA" "macro"  )  ; this LPP is used to display the MACRO port MASK
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; The following section enables the user to launch pre-defined   ;
; skill functions ( HOOKS ) at different stages inside sna flow  ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; You must write your skill procedure name between quotes.
; There are two boolean fields after the procedure name:
; - first one specifies whether or not the hook is editable in SubstrateStormCDS form.
; - second one is reserved for future usage.

; Before SAV Generation:
;snaPreProcessingGenerateSAV = '("mysnaHookPreGenerateSAV" t nil )

; After SAV Generation:
;snaPostProcessingGenerateSAV = '("mysnaHookPostGenerateSAV" t nil )

; Before Saving SAV:
;snaPreProcessingSaveSAV = '("mysnaHookPreSaveSAV" t nil )

; After Saving SAV:
;snaPostProcessingSaveSAV = '("mysnaHookPostSaveSAV" t nil )

; Before Substrate Model Extraction:
snaPreProcessingExtract = '("mysnaHookPreExtractNetlist" t  nil )

; After Substrate Model Extraction:
; snaPostProcessingExtract = '("mysnaHookPostExtractNetlist" nil  nil )


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; The following section enables the user to attach a Recognition ;
; Shape to an instance in Extracted View that does not have any  ;
;   Recognition Shape by default                                 ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;snaRecognitionShapeLayer = list( "device" "net" )





