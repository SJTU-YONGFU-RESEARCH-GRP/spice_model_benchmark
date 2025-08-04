#---------------------------------------------------------------
# CNM25 PiP Capacitor PCell for extraction
#---------------------------------------------------------------

from ui import *

def cnm25cpoly(cv, ptlist=[[0,0],[30000,0],[30000,30000],[0,30000]]) :
	lib = cv.lib()
	dbu = float(lib.dbuPerUU())
	npts = len(ptlist)

	# Calculate total area an perimeter for arbitrary Manhattan shapes
	asum = 0.0
	perimeter = 0.0
	i = npts-1
	j = 0
	while (j < npts) :
		dx  = float(ptlist[i][0]) / dbu
		dy  = float(ptlist[i][1]) / dbu
		dx1 = float(ptlist[j][0]) / dbu
		dy1 = float(ptlist[j][1]) / dbu
		# compute perimeter
		perimeter = perimeter + ((dx1 - dx) * (dx1 - dx) + (dy1 - dy) * (dy1 - dy))**0.5
		# compute area
		asum = asum + (dx + dx1) * (dy1 - dy)

		# increment vertex
		i = j
		j = j + 1
	area = asum / 2.0

	# Derive rectangular w and l properties:
	# area = w*l
	# perimeter = 2*(w+l)
	a = 1.0
	b = -perimeter / 2.0
	c = area
	l = float((-b+(b**2-4*a*c)**0.5)/(2*a))
	w = float(area/l)

	# Update the master pcell property.
	cv.dbAddProp("w", w*1e-6)
	cv.dbAddProp("l", l*1e-6)

	# Create the recognition region shape
	xpts = intarray(npts)
	ypts = intarray(npts)
	for i in range (npts) :
		xpts[i] = ptlist[i][0]
		ypts[i] = ptlist[i][1]
	cv.dbCreatePolygon(xpts, ypts, npts, TECH_Y0_LAYER);

	# Create pins
	top_net = cv.dbCreateNet("T")
	cv.dbCreatePin("T", top_net, DB_PIN_INPUT)
	bot_net = cv.dbCreateNet("B")
	cv.dbCreatePin("B", bot_net, DB_PIN_INPUT)

	# Setting device type to capacitor
	cv.dbAddProp("type", "cap")

	# Set the device modelName property for netlisting
	cv.dbAddProp("modelName", "cnm25cpoly")

	# Set the NLP property for netlisting
	cv.dbAddProp("NLPDeviceFormat", "c[@instName] [|T:%] [|B:%] [@modelName] [@w:w=%:w=30u] [@l:l=%:l=30u] [@m:m=%:m=1]")
	cv.dbAddProp("NLPDeviceFormatCDL", "x[@instName] [|T:%] [|B:%] [@modelName] [@w:w=%:w=30u] [@l:l=%:l=30u] [@m:m=%:m=1]")

	# Update the bounding box
	cv.update()

