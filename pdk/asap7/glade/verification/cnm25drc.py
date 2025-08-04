# CNM25 2M DRC deck

def printErrors(msg) :
	n = geomGetCount()
	if n > 0 :
		print n, msg

# Initialise DRC package. 
from ui import *
cv = ui().getEditCellView()
geomBegin(cv)

# Get raw layers
nwell     = geomGetShapes("NTUB", "drawing")
active    = geomGetShapes("GASAD", "drawing")
polygate  = geomGetShapes("POLY1", "drawing")
polycap   = geomGetShapes("POLY0", "drawing")
nimp      = geomGetShapes("NPLUS", "drawing")
cont      = geomGetShapes("WINDOW", "drawing")
metal1    = geomGetShapes("METAL", "drawing")
via12     = geomGetShapes("VIA", "drawing")
metal2    = geomGetShapes("METAL2", "drawing")
pad       = geomGetShapes("CAPS", "drawing")

# Form derived layers
gate        = geomAnd(polygate, active)
ngate       = geomAnd(gate, nimp)
pgate       = geomAndNot(gate, ngate)
cpoly       = geomAnd(polygate, polycap)
polygatecont= geomAnd(polygate, cont)
polycapcont = geomAnd(polycap, cont)
activecont  = geomAnd(active, cont)
allcon      = geomOr(geomOr(polygatecont, polycapcont),activecont)
badcon      = geomAndNot(allcon, metal1)
metal1via   = geomAnd(metal1, via12)
badvia      = geomAndNot(metal1via, metal2)
diff        = geomAndNot(active, gate)
ndiff       = geomAnd(diff, nimp)
pdiff       = geomAndNot(diff, nimp)
ntap        = geomAnd(ndiff, nwell)
ptap        = geomAndNot(pdiff, nwell)

# Form connectivity
geomConnect( [
              [ntap, nwell, ndiff],
			  [cont, ndiff, metal1],
			  [cont, pdiff, metal1],
			  [cont, polygate, metal1],
			  [cont, polycap, metal1],
              [via12, metal1, metal2]
	     ] )

# Start design rule checking

print "0.0. Checking off-grid..."
geomOffGrid(nwell, 0.25, 1, "0.0. Design grid is 0.25um x 0.25um")
geomOffGrid(active, 0.25, 1, "0.0. Design grid is 0.25um x 0.25um")
geomOffGrid(polygate, 0.25, 1, "0.0. Design grid is 0.25um x 0.25um")
geomOffGrid(polycap, 0.25, 1, "0.0. Design grid is 0.25um x 0.25um")
geomOffGrid(nimp, 0.25, 1, "0.0. Design grid is 0.25um x 0.25um")
geomOffGrid(cont, 0.25, 1, "0.0. Design grid is 0.25um x 0.25um")
geomOffGrid(metal1, 0.25, 1, "0.0. Design grid is 0.25um x 0.25um")
geomOffGrid(via12, 0.25, 1, "0.0. Design grid is 0.25um x 0.25um")
geomOffGrid(metal2, 0.25, 1, "0.0. Design grid is 0.25um x 0.25um")
geomOffGrid(pad, 0.25, 1, "0.0. Design grid is 0.25um x 0.25um")

print "1.X. Checking N-well..."
geomWidth(nwell, 8, "1.1. N-well width >= 8um")
geomSpace(nwell, 8, samenet, "1.2. N-well spacing (same net) >= 8um")
geomSpace(nwell, 8, diffnet, "1.2. N-well spacing (different net) >= 8um")
geomNotch(nwell, 8, "1.2. N-well notch >= 8um")

print "2.X. Checking GASAD..."
geomWidth(active, 2, "2.1. GASAD width >= 2um")
geomSpace(active, 4, samenet, "2.2. GASAD spacing (same net) >= 4um")
geomSpace(active, 4, diffnet, "2.2. GASAD spacing (different net) >= 4um")
geomNotch(active, 4, "2.2. GASAD notch >= 4um")
geomEnclose(nwell, pdiff, 5, "2.3. N-well enclosure of P-plus active >= 5um")
geomSpace(nwell, ndiff, 5, samenet, "2.4. N-well spacing to N-plus active (same net) >= 5um")
geomSpace(nwell, ndiff, 5, diffnet, "2.4. N-well spacing to N-plus active (different net) >= 5um")

print "3.X. Checking Poly0..."
geomWidth(polycap, 2.5, "3.1. Poly0 width >= 2.5um")
geomSpace(polycap, 6, samenet, "3.2. Poly0 spacing (same net) >= 6um")
geomSpace(polycap, 6, diffnet, "3.2. Poly0 spacing (different net) >= 6um")
geomNotch(polycap, 6, "3.2. Poly0 notch >= 6um")
geomSpace(polycap, active, 6, samenet, "3.3. Poly0 spacing to GASAD (same net) >= 6um")
geomSpace(polycap, active, 6, diffnet, "3.3. Poly0 spacing to GASAD (different net) >= 6um")

print "4.X. Checking Poly1..."
geomWidth(gate, 3, "4.1.a. Poly1 width inside GASAD >= 3um")
geomWidth(geomAndNot(polygate, gate), 2.5, "4.1.b. Poly1 width outside GASAD >= 2.5um")
geomSpace(polygate, 3, samenet, "4.2. Poly1 spacing (same net) >= 3um")
geomSpace(polygate, 3, diffnet, "4.2. Poly1 spacing (different net) >= 3um")
geomNotch(polygate, 3, "4.2. Poly1 notch >= 3um")
geomExtension(active, polygate, 3 , "4.3. GASAD extension of Poly1 >= 3um")
geomExtension(polygate, active, 2.5, "4.4. Poly1 extension of GASAD >= 2.5um")
geomSpace(polygate, active, 1.25, samenet, "4.5. Poly1 spacing to GASAD (same net) >= 1.25um")
geomSpace(polygate, active, 1.25, diffnet, "4.5. Poly1 spacing to GASAD (different net) >= 1.25um")
geomEnclose(polycap, cpoly, 3, "4.6. Poly0 enclosure of Poly1 >= 3um")

print "5.X. Checking N-plus..."
geomEnclose(nimp, active, 2.5, "5.1. N-plus enclosure of GASAD >= 2.5um")
geomSpace(nimp, pdiff, 2.5, samenet, "5.2. N-plus spacing to P-plus active (same net) >= 2.5um")
geomSpace(nimp, pdiff, 2.5, diffnet, "5.2. N-plus spacing to P-plus active (different net) >= 2.5um")
geomSpace(nimp, pgate, 2, samenet, "5.3. N-plus spacing to Poly1 inside P-plus active (same net) >= 2um")
geomSpace(nimp, pgate, 2, diffnet, "5.3. N-plus spacing to Poly1 inside P-plus active (different net) >= 2um")
geomExtension(nimp, ngate, 1.5, "5.4. N-plus extension of Poly1 inside N-plus active >= 1.5um")
geomWidth(nimp, 2.5, "5.5. N-plus width >= 2.5um")
geomSpace(nimp, 2.5, samenet, "5.6. N-plus spacing (same net) >= 2.5um")
geomSpace(nimp, 2.5, diffnet, "5.6. N-plus spacing (different net) >= 2.5um")
geomNotch(nimp, 2.5, "5.6. N-plus notch >= 2.5um")

print "6.X. Checking contact..."
saveDerived(badcon, "6.0. Contact requires Metal1")
geomArea(cont, 6.25, 6.25, "6.1. Exact contact size = 2.5um x 2.5um")
geomWidth(cont, 2.5, "6.1. Exact contact size = 2.5um x 2.5um")
geomSpace(cont, 3, samenet, "6.2. Contact spacing (same net) >= 3um")
geomSpace(cont, 3, diffnet, "6.2. Contact spacing (different net) >= 3um")
geomNotch(cont, 3, "6.2. Contact notch >= 3um")
geomEnclose(active, cont, 1, "6.3. GASAD enclosure of Contact >= 1um")
geomEnclose(polygate, cont, 1.25, "6.4. Poly1 enclosure of Contact >= 1.25um")
geomSpace(polygatecont, 2.5, samenet, "6.5. Poly1 Contact spacing to GASAD (same net) >= 2.5um")
geomSpace(polygatecont, 2.5, diffnet, "6.5. Poly1 Contact spacing to GASAD (different net) >= 2.5um")
geomSpace(cont, gate, 2, samenet, "6.6. Contact spacing to Poly1 inside GASAD (same net) >= 2um")
geomSpace(cont, gate, 2, diffnet, "6.6. Contact spacing to Poly1 inside GASAD (different net) >= 2um")
# 6.7 and 6.8 not implemented!
geomEnclose(polycap, cont, 4, "6.9. Poly0 enclosure of Contact >= 4um")
geomSpace(cont, cpoly, 4, diffnet, "6.10. Contact spacing to Poly1 & Poly0 (different net) >= 4um")

print "7.X. Checking Metal1..."
geomWidth(metal1, 2.5, "7.1. Metal1 width >= 2.5um")
geomSpace(metal1, 3, samenet, "7.2. Metal1 spacing (same net) >= 3um")
geomSpace(metal1, 3, diffnet, "7.2. Metal1 spacing (different net) >= 3um")
geomNotch(metal1, 3, "7.2. Metal1 notch >= 3um")
geomEnclose(metal1, cont, 1.25, "7.3. Metal1 enclosure of Contact >= 1.25um")

print "8.X. Checking Via..."
saveDerived(badvia, "8.0. Via requires Metal2")
geomArea(via12, 9, 9, "8.1. Exact via size = 3um x 3um")
geomWidth(via12, 3, "8.1. Exact via size = 3um x 3um")
geomSpace(via12, 3.5, samenet, "8.2. Via spacing (same net) >= 3.5um")
geomSpace(via12, 3.5, diffnet, "8.2. Via spacing (different net) >= 3.5um")
geomNotch(via12, 3.5, "8.2. Via notch >= 3.5um")
geomEnclose(metal1, via12, 1.25, "8.3. Metal1 enclosure of Via >= 1.25um")
geomSpace(via12, cont, 2.5, samenet, "8.4. Via spacing to contact (same net) >= 2.5um")
geomSpace(via12, cont, 2.5, diffnet, "8.4. Via spacing to contact (different net) >= 2.5um")
geomSpace(via12, polygate, 2.5, samenet, "8.5. Via spacing to Poly1 (same net) >= 2.5um")
geomSpace(via12, polygate, 2.5, diffnet, "8.5. Via spacing to Poly1 (different net) >= 2.5um")

print "9.X. Checking Metal2..."
geomWidth(metal2, 3.5, "9.1. Metal2 width >= 3.5um")
geomSpace(metal2, 3.5, samenet, "9.2. Metal2 spacing (same net) >= 3.5um")
geomSpace(metal2, 3.5, diffnet, "9.2. Metal2 spacing (different net) >= 3.5um")
geomNotch(metal2, 3.5, "9.2. Metal2 notch >= 3.5um")
geomEnclose(metal2, via12, 1.25, "9.3. Metal2 enclosure of Via >= 1.25um")

print "10.X. Checking Pad..."
geomArea(pad, 10000, 10000, "10.1. Exact passivation size = 100um x 100um")
geomWidth(pad, 100, "10.1. Exact passivation size = 100um x 100um")

num_err = geomGetTotalCount()
print "** Total error count = ", num_err

# Exit DRC package, freeing memory
geomEnd()

ui().winRedraw()

