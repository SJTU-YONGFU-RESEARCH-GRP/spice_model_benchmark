;;; COMPLETE: Add support for decimal value inputs
;;; COMPLETE: Support unlimited number of bits - presently max == 8

/****************************************************/
 LIBRARY = "gsclib045_tech"
 CELL    = "cellTmpl"
/****************************************************/

let( ( libId cellId cdfId )
    unless( cellId = ddGetObj( LIBRARY CELL )
        error( "Could not get cell %s." CELL )
    )
    when( cdfId = cdfGetBaseCellCDF( cellId )
        cdfDeleteCDF( cdfId )
    )
    cdfId  = cdfCreateBaseCellCDF( cellId )

    ;;; Parameters
    cdfCreateParam( cdfId
        ?name           "width"
        ?prompt         "Cell Width"
        ?defValue       1.0
        ?type           "float"
    )
    cdfCreateParam( cdfId
        ?name           "height"
        ?prompt         "Cell Height"
        ?defValue       1.71
        ?type           "float"
    )
    cdfCreateParam( cdfId
        ?name           "xpGrid"
        ?prompt         "Horizontal Placement Grid"
        ?defValue       0.2
        ?type           "float"
    )
    cdfCreateParam( cdfId
        ?name           "ypGrid"
        ?prompt         "Vertical Placement Grid"
        ?defValue       1.71
        ?type           "float"
    )
    cdfCreateParam( cdfId
        ?name           "drawNwell"
        ?type           "boolean"
        ?prompt         "Draw Nwell"
        ?defValue       t
    )
    cdfCreateParam( cdfId
        ?name           "drawNTAP"
        ?type           "boolean"
        ?prompt         "Draw NTAP"
        ?defValue       t
    )
     cdfCreateParam( cdfId
        ?name           "drawPTAP"
        ?type           "boolean"
        ?prompt         "Draw PTAP"
        ?defValue       t
    ) 
    cdfCreateParam( cdfId
        ?name           "drawMiddleNimp"
        ?type           "boolean"
        ?prompt         "Draw Core N-Implant"
        ?defValue       t
    )
    cdfCreateParam( cdfId
        ?name           "drawMiddlePimp"
        ?type           "boolean"
        ?prompt         "Draw Core P-Implant"
        ?defValue       t
    )
    cdfCreateParam( cdfId
        ?name           "vt"
        ?type           "cyclic"
        ?prompt         "Vt"
        ?defValue       "svt"
        ?choices         '( "lvt" "svt" "hvt" )
    )
    cdfCreateParam( cdfId
        ?name           "drawMiddleMetal"
        ?type           "boolean"
        ?prompt         "Draw Middle Metal Strip"
        ?defValue       t
    )
    cdfCreateParam( cdfId
        ?name           "drawMiddleImplant"
        ?type           "boolean"
        ?prompt         "Draw Middle N-Implant"
        ?defValue       t
    )
    cdfCreateParam( cdfId
        ?name           "drawPinGrid"
        ?type           "boolean"
        ?prompt         "Draw Routing Grid"
        ?defValue       nil
    )
    cdfCreateParam( cdfId
        ?name           "xPinGrid"
        ?type           "float"
        ?prompt         "Horizontal Track Pitch"
        ?defValue       0.2
	?use		"cdfgData->drawPinGrid->value"
    )
    cdfCreateParam( cdfId
        ?name           "yPinGrid"
        ?type           "float"
        ?prompt         "Vertical Track Pitch"
        ?defValue       0.19
	?use		"cdfgData->drawPinGrid->value"
    )
    cdfCreateParam( cdfId
        ?name           "xGridOffset"
        ?type           "float"
        ?prompt         "Horizontal Track Offset"
        ?defValue       0.1
	?use		"cdfgData->drawPinGrid->value"
    )
    cdfCreateParam( cdfId
        ?name           "yGridOffset"
        ?type           "float"
        ?prompt         "Vertical Track Offset"
        ?defValue       0.19
	?use		"cdfgData->drawPinGrid->value"
    )
    cdfCreateParam( cdfId
        ?name           "drawDummyVias"
        ?type           "boolean"
        ?prompt         "Draw Dummy Vias"
        ?defValue       nil
    )
    cdfCreateParam( cdfId
        ?name           "dummyViaWidth"
        ?type           "float"
        ?prompt         "Dummy Via Width"
        ?defValue       0.08
	?use		"cdfgData->drawDummyVias->value"
    )
    cdfCreateParam( cdfId
        ?name           "dummyViaHeight"
        ?type           "float"
        ?prompt         "Dummy Via Height"
        ?defValue       0.13
	?use		"cdfgData->drawDummyVias->value"
    )

    ;;; Simulator Information
    cdfId->simInfo = list( nil )

    ;;; Properties
    cdfId->formInitProc            = ""
    cdfId->doneProc                = ""
    cdfId->buttonFieldWidth        = 340
    cdfId->fieldHeight             = 35
    cdfId->fieldWidth              = 350
    cdfId->promptWidth             = 175
    cdfId->paramLabelSet           = "numbits vbit0 vbit1"
    cdfSaveCDF( cdfId )
)
