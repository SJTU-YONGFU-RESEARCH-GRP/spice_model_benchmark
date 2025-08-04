# CNM25 2M extraction deck
# with 2D parasitic capacitances

# Initialise boolean package 
from ui import *
ui = cvar.uiptr
cv = ui.getEditCellView()
geomBegin(cv)
libxtrpar = cv.lib()

# Parasitic capacitance density [F/um2]
e0 = 8.854187817e-12 # [F/m]
er = 3.9             # SiO2
c0 = e0 * er * 1e-6  # Normalized to 1um thickness
cpoly0sub     = c0 / 1.060
cpoly1sub     = c0 / 1.060
cmetal1poly1  = c0 / 1.300
cmetal1poly0  = c0 / 1.300
cmetal1diff   = c0 / 1.300
cmetal1sub    = c0 / 2.360
cmetal2metal1 = c0 / 1.300
cmetal2poly1  = c0 / 2.600
cmetal2poly0  = c0 / 2.600
cmetal2diff   = c0 / 3.660
cmetal2sub    = c0 / 3.660

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

# Form derived layers
bkgnd       = geomBkgnd()
pwell       = geomAndNot(bkgnd, nwell)
gate        = geomAnd(polygate, active)
ngate       = geomAnd(gate, nimp)
pgate       = geomAndNot(gate, ngate)
cpoly       = geomAnd(polygate, polycap)
diff        = geomAndNot(active, gate)
ndiff       = geomAnd(diff, nimp)
pdiff       = geomAndNot(diff, nimp)
ntap        = geomAnd(ndiff, nwell)
ptap        = geomAnd(pdiff, pwell)

# Extract pin and net names before geomConnect
geomLabel(polygate, "POLY1", "pin", 1)
geomLabel(metal1, "METAL", "pin", 1)
geomLabel(metal2, "METAL2", "pin", 1)
geomLabel(polygate, "POLY1", "net", 0)
geomLabel(metal1, "METAL", "net", 0)
geomLabel(metal2, "METAL2", "net", 0)

# Form connectivity
geomConnect( [
        [pwell, bkgnd, pwell],
		[ptap, pwell, pdiff],
		[ntap, nwell, ndiff],
		[cont, ndiff, pdiff, polygate, polycap, metal1],
		[via12, metal1, metal2]
		] )

# Save interconnect
saveInterconnect( [
		[pwell, "PWELL"],
		nwell,
		[ptap, "GASAD"],
		[ntap, "GASAD"],
		[ndiff, "GASAD"],
		[pdiff, "GASAD"],
		polycap,
		polygate,
		cont,
		metal1,
		via12,
		metal2,
		] )

# Extracting devices

if geomNumShapes(ngate) > 0 :
	print "# Extract NMOS transistors"
	extractMOS("cnm25modn", ngate, polygate, ndiff, pwell)

if geomNumShapes(pgate) > 0 :
	print "# Extract PMOS transistors"
	extractMOS("cnm25modp", pgate, polygate, pdiff, nwell)

if geomNumShapes(cpoly) > 0 :
	print "# Extract PiP capacitors"
	extractDevice("cnm25cpoly", cpoly, [[polygate, "T"], [polycap, "B"]])

# Extracting parasitics

print "# Extract Poly0 parasitics"
extractParasitic2(pwell, polycap, cpoly0sub, 0)
extractParasitic2(nwell, polycap, cpoly0sub, 0)

print "# Extract Poly1 parasitics"
extractParasitic2(pwell, polygate, cpoly1sub, 0)
extractParasitic2(nwell, polygate, cpoly1sub, 0)

print "# Extract Metal1 parasitics"
extractParasitic2(polygate, metal1, cmetal1poly1, 0)
extractParasitic2(polycap, metal1, cmetal1poly0, 0)
extractParasitic3(pdiff, metal1, cmetal1diff, 0, [polygate, polycap])
extractParasitic3(ndiff, metal1, cmetal1diff, 0, [polygate, polycap])
extractParasitic3(pwell, metal1, cmetal1sub, 0, [polygate, polycap, pdiff, ndiff])
extractParasitic3(nwell, metal1, cmetal1sub, 0, [polygate, polycap, pdiff, ndiff])

print "# Extract Metal2 parasitics"
extractParasitic2(metal1, metal2, cmetal2metal1, 0)
extractParasitic3(polygate, metal2, cmetal2poly1, 0, [metal1])
extractParasitic3(polycap, metal2, cmetal2poly0, 0, [metal1, polygate])
extractParasitic3(pdiff, metal2, cmetal2diff, 0, [metal1, polygate, polycap])
extractParasitic3(ndiff, metal2, cmetal2diff, 0, [metal1, polygate, polycap])
extractParasitic3(pwell, metal2, cmetal2sub, 0, [metal1, polygate, polycap, pdiff, ndiff])
extractParasitic3(nwell, metal2, cmetal2sub, 0, [metal1, polygate, polycap, pdiff, ndiff])

print "# Ending circuit extraction"
geomEnd()

# Opening extracted view
ui.openCellView(libxtrpar.libName(), cv.cellName(), "extracted")

