;----------------------------------
;  Assura 3.2 LVS RF PDK setup 
;----------------------------------

vuiLVSOptions = '(
     (( ?avrpt ) 
             ( "view" t )
             ( "edit" t )
             ( "use" t )
             ( avrpt t )
             ( spacer "  " )
             ( spacer2 "  " )
             ( printError nil )
             ( useOption nil )
             ( maxErrorShapesPerCell 1000 )
     )
     (( ?blackBoxCell ) 
             ( "view" t )
             ( "edit" t )
             ( "use" t )
             ( label "Black Box Cells" )
             ( standardCell nil )
             ( blackBoxCell "Cells" )
             ( blackBoxCellList "" )
             ( blackBoxCellFile "" )
     )
)

