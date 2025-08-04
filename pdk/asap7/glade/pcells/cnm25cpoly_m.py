#---------------------------------------------------------------
# CNM25 Multiple PiP Capacitor PCell
#   w  : element gate width (m)
#   l  : element gate length (m)
#   mx : number of X elements (int)
#   my : number of Y elements (int)
#   common_p0 : common bottom plate? (boolean)
#   common_p1 : common top plate? (boolean)
#---------------------------------------------------------------

from ui import *

def cnm25cpoly_m(cv, w=30.0e-6, l=30.0e-6, mx=1, my=1, common_p0=0, common_p1=0) :
	lib = cv.lib()
	tech = lib.tech()
	dbu = lib.dbuPerUU()
	width = abs(int(w * 1.0e6 * dbu))
	length = abs(int(l * 1.0e6 * dbu))
	xelem = abs(int(mx))
	yelem = abs(int(my))
	commp0 = bool(common_p0)
	commp1 = bool(common_p1)

	# Layer rules
	xygrid = int(0.25 * dbu)
	poly1_width = int(2.5 * dbu)
	poly1_space = int(3.0 * dbu)
	poly0_width = int(2.5 * dbu)
	poly0_space = int(6.0 * dbu)
	poly0_ov_poly1 = int(3.0 * dbu)
	cont_size = int(2.50 * dbu)
	cont_space_cpoly = int(4.00 * dbu)
	poly1_ov_cont = int(1.25 * dbu)
	metal_width = int(2.50 * dbu)
	metal_space = int(3.00 * dbu)
	metal_ov_cont = int(1.25 * dbu)

	# Device rules
	min_length = 4 * poly1_ov_cont + 2 * cont_size + max(poly0_width, poly1_space, metal_ov_cont - poly1_ov_cont + metal_space)
	min_width = min_length
	min_xelem = 1
	min_yelem = 1

	# Checking parameters
	if length%(2*xygrid)!=0 :
		length = int(2 * xygrid * int(length / xygrid / 2))
		cv.dbReplaceProp("l", 1e-6 * (length / dbu))
		print "** cnm25cpoly WARNING: l is off-grid. Adjusting element length. **"
		cv.update()
	if width%(2*xygrid)!=0 :
		width = int(2 * xygrid * int(width / xygrid / 2))
		cv.dbReplaceProp("w", 1e-6 * (width / dbu))
		print "** cnm25cpoly WARNING: w is off-grid. Adjusting element width. **"
		cv.update()
	if length < min_length :     
		length = min_length
		cv.dbReplaceProp("l", 1e-6 * (length / dbu))
		print "** cnm25cpoly WARNING: l < minimum length. Resetting element length. **"
		cv.update()
	if width < min_width :     
		width = min_width
		cv.dbReplaceProp("w", 1e-6 * (width / dbu))
		print "** cnm25cpoly WARNING: w < minimum width. Resetting element width. **"
		cv.update()
	if xelem < min_xelem :
		xelem = min_xelem
		cv.dbReplaceProp("mx", xelem)
		print "** cnm25cpoly WARNING: mx == 0. Resetting number of horizontal elements to ", xelem, ". **"
		cv.update()
	if yelem < min_yelem :
		yelem = min_yelem
		cv.dbReplaceProp("my", yelem)
		print "** cnm25cpoly WARNING: my == 0. Resetting number of vertical elements to ", yelem, ". **"
		cv.update()

	# Calculate XY incremental offsets
	dxoffset = length + max(2 * (poly0_ov_poly1 + cont_space_cpoly + cont_size + poly1_ov_cont), poly0_space)
	dyoffset = width + max(2 * (poly0_ov_poly1 + cont_space_cpoly + cont_size + poly1_ov_cont), poly0_space)

	# 2D element array iteration
	xoffset = 0
	for x in range(xelem) :
		yoffset = 0
		for y in range(yelem) :

			# Create bottom plate
			bot_net = cv.dbCreateNet("B")
			pin = cv.dbCreatePin("B", bot_net, DB_PIN_INOUT)
			layer = tech.getLayerNum("POLY0", "drawing")
			r = Rect(-poly0_ov_poly1, -poly0_ov_poly1, length + poly0_ov_poly1, width + poly0_ov_poly1)
			r.offset(xoffset, yoffset)
			poly0 = cv.dbCreateRect(r, layer)
			cv.dbCreatePort(pin, poly0)

			# If common_p0 create bottom stubs 
			if (commp0) :
					layer = tech.getLayerNum("POLY0", "drawing")
					r = Rect(-poly0_ov_poly1, (width - poly0_width) / 2, -(dxoffset - length) / 2, (width + poly0_width) / 2)
					r.offset(xoffset, yoffset)
					poly0 = cv.dbCreateRect(r, layer)
					r = Rect(length + poly0_ov_poly1, (width - poly0_width) / 2, length + (dxoffset - length) / 2, (width + poly0_width) / 2)
					r.offset(xoffset, yoffset)
					poly0 = cv.dbCreateRect(r, layer)
					r = Rect((length - poly0_ov_poly1) / 2, -poly0_ov_poly1, (length + poly0_ov_poly1) / 2, -(dyoffset - width) / 2)
					r.offset(xoffset, yoffset)
					poly0 = cv.dbCreateRect(r, layer)
					r = Rect((length - poly0_ov_poly1) / 2, width + poly0_ov_poly1, (length + poly0_ov_poly1) / 2, width + (dyoffset - width) / 2)
					r.offset(xoffset, yoffset)
					poly0 = cv.dbCreateRect(r, layer)

			# Create top plate
			layer = tech.getLayerNum("POLY1", "drawing")
			r = Rect(0, 0, length, width)
			r.offset(xoffset, yoffset)
			poly1 = cv.dbCreateRect(r, layer)

			# Create top stubs
			stub_length = poly0_ov_poly1 + cont_space_cpoly + cont_size + poly1_ov_cont
			stub_width = cont_size + 2*poly1_ov_cont
			r = Rect(0 , 0, -stub_length, stub_width)
			r.offset(xoffset, yoffset)
			poly1 = cv.dbCreateRect(r, layer)
			r = Rect(length , width, length + stub_length, width - stub_width)
			r.offset(xoffset, yoffset)
			poly1 = cv.dbCreateRect(r, layer)
			r = Rect(length , 0, length - stub_width, -stub_length)
			r.offset(xoffset, yoffset)
			poly1 = cv.dbCreateRect(r, layer)
			r = Rect(0 , width, stub_width, width + stub_length)
			r.offset(xoffset, yoffset)
			poly1 = cv.dbCreateRect(r, layer)

			# Create top stubs contacts
			layer = tech.getLayerNum("WINDOW", "drawing")
			r = Rect(-poly0_ov_poly1 - cont_space_cpoly, poly1_ov_cont, -poly0_ov_poly1 - cont_space_cpoly - cont_size, poly1_ov_cont + cont_size)
			r.offset(xoffset, yoffset)
			window = cv.dbCreateRect(r, layer)
			r = Rect(length + poly0_ov_poly1 + cont_space_cpoly, width - poly1_ov_cont - cont_size, length + poly0_ov_poly1 + cont_space_cpoly + cont_size, width - poly1_ov_cont)
			r.offset(xoffset, yoffset)
			window = cv.dbCreateRect(r, layer)
			r = Rect(length - poly1_ov_cont, -poly0_ov_poly1 - cont_space_cpoly , length - poly1_ov_cont - cont_size, -poly0_ov_poly1 - cont_space_cpoly - cont_size)
			r.offset(xoffset, yoffset)
			window = cv.dbCreateRect(r, layer)
			r = Rect(poly1_ov_cont, width + poly0_ov_poly1 + cont_space_cpoly , poly1_ov_cont + cont_size, width + poly0_ov_poly1 + cont_space_cpoly + cont_size)
			r.offset(xoffset, yoffset)
			window = cv.dbCreateRect(r, layer)

			# Create top stubs metal
			top_net = cv.dbCreateNet("T")
			pin = cv.dbCreatePin("T", top_net, DB_PIN_INOUT)
			layer = tech.getLayerNum("METAL", "drawing")
			r = Rect(-poly0_ov_poly1 - cont_space_cpoly + metal_ov_cont, poly1_ov_cont - metal_ov_cont, -poly0_ov_poly1 - cont_space_cpoly - cont_size - metal_ov_cont, poly1_ov_cont + cont_size + metal_ov_cont)
			r.offset(xoffset, yoffset)
			metal = cv.dbCreateRect(r, layer)
			cv.dbCreatePort(pin, metal)
			r = Rect(length + poly0_ov_poly1 + cont_space_cpoly - metal_ov_cont, width - poly1_ov_cont - cont_size - metal_ov_cont , length + poly0_ov_poly1 + cont_space_cpoly + cont_size + metal_ov_cont, width - poly1_ov_cont + metal_ov_cont)
			r.offset(xoffset, yoffset)
			metal = cv.dbCreateRect(r, layer)
			cv.dbCreatePort(pin, metal)
			r = Rect(length - poly1_ov_cont + metal_ov_cont, -poly0_ov_poly1 - cont_space_cpoly + metal_ov_cont, length - poly1_ov_cont - cont_size - metal_ov_cont, -poly0_ov_poly1 - cont_space_cpoly - cont_size - metal_ov_cont)
			r.offset(xoffset, yoffset)
			metal = cv.dbCreateRect(r, layer)
			cv.dbCreatePort(pin, metal)
			r = Rect(poly1_ov_cont - metal_ov_cont, width + poly0_ov_poly1 + cont_space_cpoly - metal_ov_cont, poly1_ov_cont + cont_size + metal_ov_cont, width + poly0_ov_poly1 + cont_space_cpoly + cont_size + metal_ov_cont)
			r.offset(xoffset, yoffset)
			metal = cv.dbCreateRect(r, layer)
			cv.dbCreatePort(pin, metal)

			# If common_p1 connect top stubs metals
			if (commp1) :
				layer = tech.getLayerNum("METAL", "drawing")
				r = Rect((-dxoffset - metal_width) / 2 , (-dyoffset - metal_width) /2, (-dxoffset + metal_width) / 2 , (dyoffset + metal_width) /2)
				r.offset(length/2, width/2)
				r.offset(xoffset, yoffset)
				metal = cv.dbCreateRect(r, layer)
				r = Rect((dxoffset - metal_width) / 2 , (-dyoffset - metal_width) /2, (dxoffset + metal_width) / 2 , (dyoffset + metal_width) /2)
				r.offset(length/2, width/2)
				r.offset(xoffset, yoffset)
				metal = cv.dbCreateRect(r, layer)
				r = Rect((-dxoffset - metal_width) / 2 , (-dyoffset - metal_width) /2, (dxoffset + metal_width) / 2 , (-dyoffset + metal_width) /2)
				r.offset(length/2, width/2)
				r.offset(xoffset, yoffset)
				metal = cv.dbCreateRect(r, layer)
				r = Rect((-dxoffset - metal_width) / 2 , (dyoffset - metal_width) /2, (dxoffset + metal_width) / 2 , (dyoffset + metal_width) /2)
				r.offset(length/2, width/2)
				r.offset(xoffset, yoffset)
				metal = cv.dbCreateRect(r, layer)

			yoffset = yoffset + dyoffset

		xoffset = xoffset + dxoffset

	# Save results
	cv.update()

