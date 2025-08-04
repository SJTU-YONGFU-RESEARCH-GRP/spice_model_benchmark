pcDefinePCell(list(ddGetObj("gsclib045_tech") "cellTmpl" "layout" "maskLayout")
    (
	(width float 1.0)
	(height float 1.71)
	(vt  string "svt" )
	(xpGrid float 0.2)
	(ypGrid float 1.71)
	(drawPinGrid boolean nil)
	(xPinGrid float 0.20)
	(yPinGrid float 0.19)
	(xGridOffset float 0.10)
	(yGridOffset float 0.19)
	(drawNwell boolean t)
	(drawMiddleNimp boolean t)
	(drawMiddlePimp boolean t)
	(drawNTAP boolean t)
	(drawPTAP boolean t)
	(drawMiddleMetal boolean t)
	(drawMiddleImplant boolean t)
	(drawDummyVias boolean nil)
	(dummyViaWidth float 0.08)
	(dummyViaHeight float 0.13)
    )
    prog((shape x y n pts y1 y2  )

	unless( pcCellView
	    return()
	)

	shape = rodCreateRect( 
		?layer "text"
		?length height
		?width width
		?origin 0:0
	)
	n = y = 0
	if( ypGrid == height 
	    y2 = 0.83
	    y2 = 0.82
	)
	while( y <= height
	    unless( and( !drawMiddleMetal oddp(n) ) 
		if( or( and( drawPTAP evenp(n) ) and( drawNTAP oddp(n) ) ) then
		    rodCreatePath( 
			    ?layer "Metal1"
			    ?width 0.12
			    ?pts list( 0:y width:y )
			    ?subRect list(
				list( 
				    ?layer "Cont"
				    ?width	0.06
				    ?length	0.06
				    ?space 0.14
				    ?endOffset -0.07
				)
			    )
		    )
		else
		    rodCreatePath( 
			    ?layer "Metal1"
			    ?width 0.12
			    ?pts list( 0:y width:y )
		    )
		)
	    )
	    n = n + 1
	    when( !and( evenp( n ) !drawMiddleMetal )
		  dbCreateRect( pcCellView '( "Oxide" "drawing" )
		    	      list( 0:y-0.06 width:y+0.06 )
			     )
	         )
	    cond( 
		( y == 0 
		    pts = list( -0.06:y-0.07 width+0.06:y+0.08 )
		)
		( y == height 
		    pts = list( -0.06:y-0.08 width+0.06:y+0.07 )
		)
		( t
		    pts = list( -0.06:y-0.09 width+0.06:y+0.09 )
		)
	    )
	    y1 = yCoord(cadr(pts))
	
	    if( evenp( n ) then
		when( drawMiddleImplant
		    dbCreateRect( pcCellView '( "Nimp" "drawing" ) pts )
		)
		if( y < height  then
		    when( drawMiddlePimp
			dbCreateRect( pcCellView '( "Pimp" "drawing" ) 
			    list( -0.06:y1 width+0.06:y1+y2 )
			)
			case( vt
			    ( "lvt" 
				dbCreateRect( pcCellView '( "Plvt" "drawing" ) 
				    list( -0.06:y1 width+0.06:y1+y2 )
				)
			    )
			    ( "hvt" 
				dbCreateRect( pcCellView '( "Phvt" "drawing" ) 
				    list( -0.06:y1 width+0.06:y1+y2 )
				)
			    )
			    ( t	t )
			)
		    )
		    when( drawMiddleNimp
			dbCreateRect( pcCellView '( "Nimp" "drawing" ) 
			    list( -0.06:y1+y2 width+0.06:y1+0.72+y2 )
			)
			case( vt
			    ( "lvt" 
				dbCreateRect( pcCellView '( "Nlvt" "drawing" ) 
				    list( -0.06:y1+y2 width+0.06:y1+0.72+y2 )
				)
			    )
			    ( "hvt" 
				dbCreateRect( pcCellView '( "Nhvt" "drawing" ) 
				    list( -0.06:y1+y2 width+0.06:y1+0.72+y2 )
				)
			    )
			    ( t	t )
			)
		    )
		    when( drawNwell
			dbCreateRect( pcCellView '( "Nwell" "drawing" ) 
			    list( -0.06:y-0.89 width+0.06:y+0.89 )
			)
		    )
		else
		    when( drawNwell
			dbCreateRect( pcCellView '( "Nwell" "drawing" ) 
			    list( -0.06:y-0.89 width+0.06:y+0.12 )
			)
		    )
		)
	    else
		dbCreateRect( pcCellView '( "Pimp" "drawing" ) pts )
		when( y < height 
		    when( drawMiddleNimp
			dbCreateRect( pcCellView '( "Nimp" "drawing" ) 
			    list( -0.06:y1 width+0.06:y1+0.72 )
			)
			case( vt
			    ( "lvt" 
				dbCreateRect( pcCellView '( "Nlvt" "drawing" ) 
				    list( -0.06:y1 width+0.06:y1+0.72 )
				)
			    )
			    ( "hvt" 
				dbCreateRect( pcCellView '( "Nhvt" "drawing" ) 
				    list( -0.06:y1 width+0.06:y1+0.72 )
				)
			    )
			    ( t    t )
			)
		    )
		    when( drawMiddlePimp
			dbCreateRect( pcCellView '( "Pimp" "drawing" ) 
			    list( -0.06:y1+0.72 width+0.06:y1+0.72+y2 )
			)
			case( vt
			    ( "lvt" 
				dbCreateRect( pcCellView '( "Plvt" "drawing" ) 
				    list( -0.06:y1+0.74 width+0.06:y1+0.72+y2 )
				)
			    )
			    ( "hvt" 
				dbCreateRect( pcCellView '( "Phvt" "drawing" ) 
				    list( -0.06:y1+0.74 width+0.06:y1+0.72+y2 )
				)
			    )
			    ( t    t )
			)
		    )
		)
	    )

	    y = y + ypGrid
	)

	when( drawPinGrid
	    x = xGridOffset
	    while( x < width
		dbCreateLine( pcCellView '( "text" "drawing1" ) 
		    list( x:0 x:height )
		)
		x = x + xPinGrid
	    )
	    y = yGridOffset
	    while( y < height
		dbCreateLine( pcCellView '( "text" "drawing1" ) 
		    list( 0:y width:y )
		)
		y = y + yPinGrid
	    )
	)

	when( drawDummyVias
	    x = xGridOffset
	    while( x < width
		y = yGridOffset
		while( y < height-0.001
		    dbCreateRect( pcCellView '( "y0" "drawing" )
			list( 
			    x-dummyViaWidth/2.0:y-dummyViaHeight/2.0
			    x+dummyViaWidth/2.0:y+dummyViaHeight/2.0
			)
		    )
		    y = y + yPinGrid
		)
		x = x + xPinGrid
	    )
	)

	rodAssignHandleToParameter(
                ?parameter       'width
		?displayName	"width"
                ?rodObj          shape
                ?handleName      list( "centerLeft"  "centerRight" )
                ?stretchType     "relative"
		?stretchDir	'x
		?moveOrigin t
                ?userFunction    "gsclib045_stretch"
                ?updateIncrement xpGrid
	)
	rodAssignHandleToParameter(
                ?parameter       'height
		?displayName	"height"
                ?rodObj          shape
                ?handleName      list( "lowerCenter"  "upperCenter" )
                ?stretchType     "relative"
		?stretchDir	'y
		?moveOrigin t
                ?userFunction    "gsclib045_stretch"
                ?updateIncrement ypGrid
	)


	return(t)
    )
)
