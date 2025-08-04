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
