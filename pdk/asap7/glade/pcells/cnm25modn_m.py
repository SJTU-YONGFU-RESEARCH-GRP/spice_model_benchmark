#---------------------------------------------------------------
# CNM25 Multiple NMOS PCell
#   w  : element gate width (m)
#   l  : element gate length (m)
#   mx : number of X elements (int)
#   my : number of Y elements (int)
#   common_d : common drain? (boolean)
#   common_g : common gate? (boolean)
#   common_s : common source? (boolean)
#
# Note: Gates are R90
#---------------------------------------------------------------

from ui import *

def cnm25modn_m(cv, w=4.5e-6, l=3.0e-6, mx=1, my=1, common_d=0, common_g=0, common_s=0) :
	lib = cv.lib()
	tech = lib.tech()
	dbu = lib.dbuPerUU()
	width = abs(int(w * 1.0e6 * dbu))
	length = abs(int(l * 1.0e6 * dbu))
	xelem = abs(int(mx))
	yelem = abs(int(my))
	commd = bool(common_d)
	commg = bool(common_g)
	comms = bool(common_s)

	# Layer rules
	xygrid = int(0.25 * dbu)
	gasad_width = int(2.00 * dbu)
	gasad_space = int(4.00 * dbu)
	ntub_ov_gasad = int(5.00 * dbu)
	nplus_ov_gasad = int(2.50 * dbu)
	poly_width = int(3.0 * dbu)
	poly_space = int(3.0 * dbu)
	poly_space_gasad = int(1.25 * dbu)
	poly_ext_gasad = int(2.5 * dbu) 
	cont_size = int(2.50 * dbu)
	cont_space = int(3.00 * dbu)
	cont_space_poly = int(2.00 * dbu)
	gasad_ov_cont = int(1.00 * dbu)
	poly_ov_cont = int(1.25 * dbu)
	metal_width = int(2.50 * dbu)
	metal_space = int(3.00 * dbu)
	metal_ov_cont = int(1.25 * dbu)

	# Device rules
	min_length = poly_width
	min_width = max(gasad_width, cont_size + 2*gasad_ov_cont)
	min_xelem = 1
	min_yelem = 1

	# Checking parameters
	if length%xygrid!=0 :
		length = int(xygrid * int(length / xygrid))
		cv.dbReplaceProp("l", 1e-6 * (length / dbu))
		print "** cnm25modn WARNING: l is off-grid. Adjusting element length. **"
		cv.update()
	if width%xygrid!=0 :
		width = int(xygrid * int(width / xygrid))
		cv.dbReplaceProp("w", 1e-6 * (width / dbu))
		print "** cnm25modn WARNING: w is off-grid. Adjusting element width. **"
		cv.update()
	if length < min_length :     
		length = min_length
		cv.dbReplaceProp("l", 1e-6 * (length / dbu))
		print "** cnm25modn WARNING: l < minimum length. Resetting element length. **"
		cv.update()
	if width < min_width :     
		width = min_width
		cv.dbReplaceProp("w", 1e-6 * (width / dbu))
		print "** cnm25modn WARNING: w < minimum width. Resetting element width. **"
		cv.update()
	if xelem < min_xelem :
		xelem = min_xelem
		cv.dbReplaceProp("mx", xelem)
		print "** cnm25modn WARNING: mx == 0. Resetting number of horizontal elements to ", xelem, ". **"
		cv.update()
	if yelem < min_yelem :
		yelem = min_yelem
		cv.dbReplaceProp("my", yelem)
		print "** cnm25modn WARNING: my == 0. Resetting number of vertical elements to ", yelem, ". **"
		cv.update()

	# Calculate XY incremental offsets
	dxoffset_min = length + 2*cont_space_poly + cont_size
	dxoffset_extra = cont_size + 2*gasad_ov_cont + max(gasad_space, (metal_ov_cont-gasad_ov_cont) + metal_space)
	dxoffset_alt = [ dxoffset_min + (not commd) * dxoffset_extra, dxoffset_min + (not comms) * dxoffset_extra]
	dyoffset = width + max(gasad_space, (not commg) * (2*poly_ext_gasad + poly_space), ((not commd) or (not comms)) * (2*(metal_ov_cont-gasad_ov_cont) + metal_space))

	# 2D element array iteration
	xoffset = 0
	for x in range(xelem) :
		yoffset = 0
		for y in range(yelem) :

			# Create active
			layer = tech.getLayerNum("GASAD", "drawing")
			r = Rect(-(cont_space_poly + cont_size + gasad_ov_cont), 0, length + cont_space_poly + cont_size + gasad_ov_cont, width)
			r.offset(xoffset, yoffset)
			active = cv.dbCreateRect(r, layer)

			# Create gate
			layer = tech.getLayerNum("POLY1", "drawing")
			poly_ext_one_side = max(poly_ext_gasad, commg * max(gasad_space/2, ((not commd) or (not comms)) * ((metal_ov_cont-gasad_ov_cont) + metal_space/2)))
			r = Rect(0, -poly_ext_one_side, length, width + poly_ext_one_side)
			r.offset(xoffset, yoffset)
			poly = cv.dbCreateRect(r, layer)
			gate_net = cv.dbCreateNet("G")
			pin = cv.dbCreatePin("G", gate_net, DB_PIN_INPUT)
			cv.dbCreatePort(pin, poly)

			# Create drain and source contacts
			layer = tech.getLayerNum("WINDOW", "drawing")
			n_cont = int((width - 2*gasad_ov_cont + cont_space) / (cont_size + cont_space))
			s_cont = 0
			if (n_cont > 1) :
				 s_cont = cont_space
			for n in range(n_cont) :
				r = Rect(-cont_space_poly - cont_size, gasad_ov_cont + n * (cont_size + s_cont), -cont_space_poly, gasad_ov_cont + cont_size + n * (cont_size + s_cont))
				r.offset(xoffset, yoffset)
				contact = cv.dbCreateRect(r, layer)
				r = Rect(length + cont_space_poly, gasad_ov_cont + n * (cont_size + s_cont), length + cont_space_poly + cont_size, gasad_ov_cont + cont_size + n * (cont_size + s_cont))
				r.offset(xoffset, yoffset)
				contact = cv.dbCreateRect(r, layer)

			# Create drain and source metal
			layer = tech.getLayerNum("METAL", "drawing")
			metal_ext_one_side = max(metal_ov_cont - gasad_ov_cont, (((x%2!=0) and commd) or ((x%2==0) and (comms))) * (dyoffset - width)/2) 
			r = Rect(-(cont_space_poly + cont_size + metal_ov_cont), -metal_ext_one_side, -cont_space_poly + metal_ov_cont, width + metal_ext_one_side)
			r.offset(xoffset, yoffset)
			metal = cv.dbCreateRect(r, layer)
			source_net = cv.dbCreateNet("S")
			pin = cv.dbCreatePin("S", source_net, DB_PIN_INOUT)
			cv.dbCreatePort(pin, metal)

			metal_ext_one_side = max(metal_ov_cont - gasad_ov_cont, (((x%2==0) and (commd)) or ((x%2!=0) and (comms))) * (dyoffset - width)/2) 
			r = Rect(length + cont_space_poly - metal_ov_cont, -metal_ext_one_side, length + cont_space_poly + cont_size + metal_ov_cont, width + metal_ext_one_side)
			r.offset(xoffset, yoffset)
			metal = cv.dbCreateRect(r, layer)
			drain_net = cv.dbCreateNet("D")
			pin = cv.dbCreatePin("D", drain_net, DB_PIN_INOUT)
			cv.dbCreatePort(pin, metal)

			yoffset = yoffset + dyoffset

		xoffset = xoffset + dxoffset_alt[x%2!=0]

	# Create n-plus
	layer = tech.getLayerNum("NPLUS", "drawing")
	nplus_x_ext = cont_space_poly + cont_size + gasad_ov_cont + nplus_ov_gasad
	r = Rect(-nplus_x_ext, -nplus_ov_gasad, length + nplus_x_ext + xoffset -dxoffset_alt[x%2!=0], width + nplus_ov_gasad + yoffset - dyoffset)
	nplus = cv.dbCreateRect(r, layer)

	# Create p-well
	layer = tech.getLayerNum("backgnd", "drawing")
	ntub_x_ext = cont_space_poly + cont_size + gasad_ov_cont + ntub_ov_gasad
	r = Rect(-ntub_x_ext, -ntub_ov_gasad, length + ntub_x_ext + xoffset -dxoffset_alt[x%2!=0], width + ntub_ov_gasad + yoffset - dyoffset)
	ptub = cv.dbCreateRect(r, layer)
	bulk_net = cv.dbCreateNet("B")
	pin = cv.dbCreatePin("B", bulk_net, DB_PIN_INOUT)
	cv.dbCreatePort(pin, ptub)

	# Save results
	cv.update()

