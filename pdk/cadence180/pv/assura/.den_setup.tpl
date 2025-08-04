;----------------------------
; Assura 3.2 DEN PDK setup
;----------------------------

vuiDRCOptions = '(
     (( ?avrpt ) 
             ( "view" t )
             ( "edit" t )
             ( "use" t )
             ( avrpt t )
             ( spacer "  " )
             ( spacer2 "  " )
             ( useOption nil )
             ( maxErrorShapesPerCell 1000 )
     )
     (( ?dbuPerUU ) 
             ( "view" t )
             ( "edit" t )
             ( "use" t )
             ( dbuPerUU 2000.0 )
     )
     (( ?userUnits ) 
             ( "view" t )
             ( "edit" t )
             ( "use" t )
             ( userUnits "micron" )
     )
)

