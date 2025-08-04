# CNM25 2M extraction deck
# with 3D parasitic capacitances

# Initialise boolean package 
from ui import *
ui = cvar.uiptr
cv = ui.getEditCellView()
geomBegin(cv)
libxtrpar = cv.lib()

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

# Extracting 3D parasitics with Fastcap

print "# Extract 3D cap parasitics using switch values:"

if 'bulk_name' not in globals() :
	bulk_name = "vss"
print "  bulk_name = ", bulk_name

if 'ref_name' not in globals() :
	ref_name = "vss"
print "  ref_name = ", ref_name

if 'fastcap_tol' not in globals() :
	fastcap_tol = 0.01
print "  fastcap_tol = ", fastcap_tol

if 'fastcap_order' not in globals() :
	fastcap_order = 3
print "  fastcap_order = ", fastcap_order

extractParasitic3D(bulk_name, ref_name, fastcap_tol, fastcap_order)

print "# Ending circuit extraction"
geomEnd()

# Opening extracted view
ui.openCellView(libxtrpar.libName(), cv.cellName(), "extracted")

