#---------------------------------------------------------------
# CNM25 PMOSFET PCell for extraction
#---------------------------------------------------------------

from ui import *

def cnm25modp(cv, ptlist=[[0,0],[3000,0],[3000,4500],[0,4500]]) :
	lib = cv.lib()
	dbu = lib.dbuPerUU()

	# Create the recognition region shape
	npts = len(ptlist)
	xpts = intarray(npts)
	ypts = intarray(npts)
	for i in range (npts) :
		xpts[i] = ptlist[i][0]
		ypts[i] = ptlist[i][1]
	cv.dbCreatePolygon(xpts, ypts, npts, TECH_Y0_LAYER);

	# Create pins
	gate_net = cv.dbCreateNet("G")
	cv.dbCreatePin("G", gate_net, DB_PIN_INPUT)
	source_net = cv.dbCreateNet("S")
	cv.dbCreatePin("S", source_net, DB_PIN_INPUT)
	drain_net = cv.dbCreateNet("D")
	cv.dbCreatePin("D", drain_net, DB_PIN_INPUT)	
	bulk_net = cv.dbCreateNet("B")
	cv.dbCreatePin("B", bulk_net, DB_PIN_INPUT)

	# Setting device type to mosfet
	cv.dbAddProp("type", "mos")

	# Set the device modelName property for netlisting
	cv.dbAddProp("modelName", "cnm25modp")

	# Set the NLP property for netlisting
	cv.dbAddProp("NLPDeviceFormat", "m[@instName] [|D:%] [|G:%] [|S:%] [|B:%] [@modelName] [@w:w=%:w=4.5u] [@l:l=%:l=3u] [@ad:ad=%:ad=24.75e-12] [@as:as=%:as=24.75e-12] [@pd:pd=%:pd=20.0e-6] [@ps:ps=%:ps=20.0e-6] [@m:m=%:m=1]")
	cv.dbAddProp("NLPDeviceFormatCDL", "x[@instName] [|D:%] [|G:%] [|S:%] [|B:%] [@modelName] [@w:w=%:w=4.5u] [@l:l=%:l=3u] [@ad:ad=%:ad=24.75e-12] [@as:as=%:as=24.75e-12] [@pd:pd=%:pd=20.0e-6] [@ps:ps=%:ps=20.0e-6] [@m:m=%:m=1]")

	# Update the bounding box
	cv.update()

