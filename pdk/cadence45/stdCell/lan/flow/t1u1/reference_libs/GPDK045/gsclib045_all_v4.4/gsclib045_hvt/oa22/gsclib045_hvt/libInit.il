procedure(gsclib045_stretch(spcInfo)
    let((paramValue increment newValue )

	    paramValue = spcInfo->paramVal
	    increment  = spcInfo->increment

	    newValue = gsclib045_round((paramValue + increment) 0.001)
	    when( newValue < abs(increment)
		newValue = abs(increment)
	    )

	    newValue ;<--- return
	
    )
)

procedure( gsclib045_round( value grid )
      float(round(value/grid)*grid)
)

procedure( gsclib045_cellTmplCB( paramSym )
    let(( width height xpGrid ypGrid )

	xpGrid = cdfgData->xpGrid->value
	ypGrid = cdfgData->ypGrid->value
	width = cdfgData->width->value
	height = cdfgData->height->value

	when( gsclib045_round( width xpGrid ) != width
	    width = gsclib045_round( width xpGrid )
	    warn( "Cell Width must be a multiple of the horizontal placement grid (%g) - changed to %g" xpGrid width )
	    cdfgData->width->value = width
	)
	when( gsclib045_round( height ypGrid ) != height
	    height = gsclib045_round( height ypGrid )
	    warn( "Cell Height must be a multiple of the vertical placement grid (%g) - changed to %g" ypGrid height )
	    cdfgData->height->value = height
	)

    )
)
