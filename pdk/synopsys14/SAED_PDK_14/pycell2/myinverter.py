__version__ = "$Revision: 13 $"

# this script is based on Ciranova PyCell's tutorial sample, esp. $CNI_ROOT/tutorial/MyTutorialPyCells/tutorial2.py
# this script aims at contructing a parameterized inverter which can be ported to different technologies
# two technologies, namely cni130 and cni180 with reduced physical rules (please see the technology file for more details) have been tested successfully with passed DRC
# LVS needed to be done with a third-party software, like Cadence Virtuoso or Calibre

from cni.dlo import *
from cni.geo import *
from cni.constants import *

class myinverter(DloGen):
# construct an inverter
	@classmethod
	def defineParamSpecs(cls, specs):

		oxide = 'thin'
		# now get the parameters of gate
		nwidth = specs.tech.getMosfetParams('nmos', oxide, 'minWidth')
		nlength = specs.tech.getMosfetParams('nmos', oxide, 'minLength')
		pwidth = specs.tech.getMosfetParams('pmos', oxide, 'minWidth')
		plength = specs.tech.getMosfetParams('pmos', oxide, 'minLength')

		# now use these default parameter values in the parameter definitions
		specs('nwidth', nwidth, 'device nwidth', RangeConstraint(nwidth, 10*nwidth, USE_DEFAULT))
		specs('nlength', nlength, 'device nlength', RangeConstraint(nlength, 10*nlength, USE_DEFAULT))
		specs('pwidth', pwidth, 'device pwidth', RangeConstraint(pwidth, 10*pwidth, USE_DEFAULT))
		specs('plength', plength, 'device plength', RangeConstraint(plength, 10*plength, USE_DEFAULT))
		specs('nsourceDiffOverlap', 0.0)
		specs('ndrainDiffOverlap', 0.0)
		specs('psourceDiffOverlap', 0.0)
		specs('pdrainDiffOverlap', 0.0)
		specs('xtorFillLayer', Layer('metal1'))
		specs('powerMetalWidth',3*specs.tech.getPhysicalRule('minWidth',Layer('metal1')))	
		# get the width for powerline metal


	def setupParams(self, params):

		# get parameters from user input
		self.nwidth = params['nwidth']
		self.nlength = params['nlength']
		self.pwidth = params['pwidth']
		self.plength = params['plength']
		self.nsourceDiffOverlap = params['nsourceDiffOverlap']
		self.ndrainDiffOverlap = params['ndrainDiffOverlap']
		self.psourceDiffOverlap = params['psourceDiffOverlap']
		self.pdrainDiffOverlap = params['pdrainDiffOverlap']
		self.xtorFillLayer = params['xtorFillLayer']	# what is it?
		self.powerMetalWidth = params['powerMetalWidth']
		if (self.powerMetalWidth < self.tech.getPhysicalRule('minWidth',Layer('metal1'))):
			self.powerMetalWidth = self.tech.getPhysicalRule('minWidth',Layer('metal1'))
			# if the user input a metal width smaller than the minimum width of physical rule, round it to the physical rule
			# b.t.w., this is how to get physical rule info out of tech file 
			
		# also snap width and length values to nearest grid points
		grid = Grid(self.tech.getGridResolution())
		self.nwidth = grid.snap(self.nwidth, SnapType.ROUND)
		self.nlength = grid.snap(self.nlength, SnapType.ROUND)
		self.pwidth = grid.snap(self.pwidth, SnapType.ROUND)
		self.plength = grid.snap(self.plength, SnapType.ROUND)

		# save layer values using class variables
		self.diffLayer = Layer('diff')
		self.gateLayer = Layer('poly1')
		self.metalLayer = Layer('metal1')

		# determine minimum extension for gate poly layer
		self.endcap = self.tech.getPhysicalRule('minExtension', self.gateLayer, self.diffLayer)
		# same for both n and p types

	def genLayout(self):
	# construct nmos first:
		# first construct the rectangle for the gate
		ngateBox = Box(-self.endcap, 0, (self.nwidth + self.endcap), self.nlength)
		# not surprisingly, self.nlength == self.plength here	

		#### UNCOMMENT FOLLOWING FOUR LINES TO REMOVE MINIMUM AREA DRC ERROR
		if self.tech.physicalRuleExists('minArea', self.gateLayer):
			minArea = self.tech.getPhysicalRule('minArea', self.gateLayer)
			grid = Grid(self.tech.getGridResolution())
			ngateBox.expandForMinArea(NORTH, minArea, grid)
		# in real tech file, this minArea constraint has been artificially removed to show in a more obvious way that the layout migration works

		ngateRect = Rect(self.gateLayer, ngateBox)

		# now construct contacts for source and drain
		# the size of contacts are not explicitly specified here, the the coordinates are floating too, since they will be done in the next
		# the contact here includes corresponding diff, contact material, and metal
		nsourceContact = Contact(self.diffLayer, self.metalLayer, 'NS')
		ndrainContact = Contact(self.diffLayer, self.metalLayer, 'ND')

		# stretch the source and drain contacts to full transistor extent
		# but the absolute coords of contacts are still floating
		nsourceBox = nsourceContact.getBBox()
		nsourceBox.setRight(ngateBox.right)
		nsourceBox.setLeft(ngateBox.left)
		nsourceContact.stretch(nsourceBox)
		ndrainBox = ndrainContact.getBBox()
		ndrainBox.setRight(ngateBox.right)
		ndrainBox.setLeft(ngateBox.left)
		ndrainContact.stretch(ndrainBox)

		# use "smart place" to place gate between source and drain
		fgPlace(nsourceContact, SOUTH, ngateRect)	# place source contact to the south of gate and use gate as a static reference
		fgPlace(ndrainContact, NORTH, ngateRect)

		# construct gate diffusion rectangle, from top of source to bottom of drain
		nbottom = nsourceContact.getBBox().top
		ntop = ndrainContact.getBBox().bottom
		ndiffBox = Box(0, nbottom, self.nwidth, ntop)
		ndiffRect = Rect(self.diffLayer, ndiffBox)

		# add any extra diffusion outside source and drain contacts
		if self.nsourceDiffOverlap > 0:
			nsBox = nsourceContact.getBBox(self.diffLayer)
			nsBox.setBottom(nsBox.bottom - self.nsourceDiffOverlap)
			Rect(self.diffLayer, nsBox)
		if self.ndrainDiffOverlap > 0:
			ndBox = ndrainContact.getBBox(self.diffLayer)
			ndBox.setTop(ndBox.top + self.ndrainDiffOverlap)
			Rect(self.diffLayer, ndBox)

		# define the enclosure rectangles on the enclosure layers for transistor
		ngroup=Grouping('ngroup')	# create ngroup, for nmos
		ngroup.add(ngateRect)
		ngroup.add(nsourceContact)
		ngroup.add(ndrainContact)
		ngroup.add(ndiffRect)
		nEnctmp = fgAddEnclosingRects(ngroup, [Layer('nimp')])	# form an enclosure layer for nmos
		nEnc = Rect(Layer('nimp'), nEnctmp.getBBox())
		nEnctmp.destroy()
		ngroup.add(nEnc)

 		# now create ptap for nmos
 		ptapContact = Contact(Layer('diff'), Layer('metal1'), 'PTAP')	# but the coords are still floating
		ptapContactBox = ptapContact.getBBox()
		if self.tech.physicalRuleExists('minArea', Layer('pimp')):
 			minArea = self.tech.getPhysicalRule('minArea', Layer('pimp'))
 			grid = Grid(self.tech.getGridResolution())
 			ptapContactBox.expandForMinArea(EAST, minArea, grid)    # expand the area to meet the minimum requirement
		ptapContact.stretch(ptapContactBox)    # adjust the size of ptap
 		ptapGroup = Grouping('ptap')
 		ptapGroup.add(ptapContact)
 		ptapEnctmp = fgAddEnclosingRects(ptapGroup, [Layer('pimp')])    # define the diffusion region inside as p type
		ptapEncBox = ptapEnctmp.getBBox()
		ptapEnctmp.destroy()
		ptapEnc = Rect(Layer('pimp'), ptapEncBox)
		ptapGroup.add(ptapEnc)
 		fgPlace(ptapGroup, SOUTH, ngroup)	# place the whole ptap in right place
		ngroup.add(ptapGroup)

########################################## 

	# then construct pmos
	# methodology here: first construct pmos with the same origin as nmos, and then horizontally move pmos to the right by some distance
		# first construct the rectangle for the gate
		pgateBox = Box(-self.endcap, 0, (self.pwidth + self.endcap), self.plength)
		####UNCOMMENT FOLLOWING FOUR LINES TO REMOVE MINIMUM AREA DRC ERROR
		if self.tech.physicalRuleExists('minArea', self.gateLayer):
			minArea = self.tech.getPhysicalRule('minArea', self.gateLayer)
			grid = Grid(self.tech.getGridResolution())
			pgateBox.expandForMinArea(NORTH, minArea, grid)
		pgateRect = Rect(self.gateLayer, pgateBox)

		# now construct contacts for source and drain
		psourceContact = Contact(self.diffLayer, self.metalLayer, 'PS')
		pdrainContact = Contact(self.diffLayer, self.metalLayer, 'PD')

		# stretch the source and drain contacts to full transistor extent
		psourceBox = psourceContact.getBBox()
		psourceBox.setRight(pgateBox.right)
		psourceBox.setLeft(pgateBox.left)
		psourceContact.stretch(psourceBox)
		pdrainBox = pdrainContact.getBBox()
		pdrainBox.setRight(pgateBox.right)
		pdrainBox.setLeft(pgateBox.left)
		pdrainContact.stretch(pdrainBox)
	
		# use "smart place" to place gate between source and drain
		fgPlace(psourceContact, SOUTH, pgateRect)
		fgPlace(pdrainContact, NORTH, pgateRect)

		# construct gate diffusion rectangle, from top of source to bottom of drain
		pbottom = psourceContact.getBBox().top
		ptop = pdrainContact.getBBox().bottom
		pdiffBox = Box(0, pbottom, self.pwidth, ptop)
		pdiffRect = Rect(self.diffLayer, pdiffBox)

		# add any extra diffusion outside source and drain contacts
		if self.psourceDiffOverlap > 0:
			psBox = psourceContact.getBBox(self.diffLayer)
			psBox.setBottom(psBox.bottom - self.psourceDiffOverlap)
			Rect(self.diffLayer, psBox)

		if self.pdrainDiffOverlap > 0:
			pdBox = pdrainContact.getBBox(self.diffLayer)
			pdBox.setTop(pdBox.top + self.pdrainDiffOverlap)
			Rect(self.diffLayer, pdBox)

		# now create ntap for pmos
		ntapContact = Contact(Layer('diff'), Layer('metal1'), 'NTAP')
		ntapContactBox = ntapContact.getBBox() 
		if self.tech.physicalRuleExists('minArea', Layer('nimp')):
			minArea = self.tech.getPhysicalRule('minArea', Layer('nimp'))
			grid = Grid(self.tech.getGridResolution())
			ntapContactBox.expandForMinArea(EAST, minArea, grid)
		ntapContact.stretch(ntapContactBox)
		ntapGroup = Grouping('ntap')
		ntapGroup.add(ntapContact)
		ntapEnctmp = fgAddEnclosingRects(ntapGroup, [Layer('nimp'), Layer('nwell')]) # floating ntap
		# the reason to generate enclosure layer with both nimp and nwell and delete nwell layer later ...
		# instead of just with nimp is that the latter will have a DRC error on the distance ...
		# between nimp enclosure layer and active region ...
		ntapEnc = Rect(Layer('nimp'), ntapEnctmp.getComp(0).getBBox())
		ntapEnctmp.destroy()
		ntapGroup.add(ntapEnc)

		# define the enclosure rectangles on the enclosure layers for transistor
		pgroup=Grouping('pgroup')	# create pgroup 
		pgroup.add(pgateRect)
		pgroup.add(psourceContact)
		pgroup.add(pdrainContact)
		pgroup.add(pdiffRect)	# group them together
		pEnctmp = fgAddEnclosingRects(pgroup, [Layer('pimp'), Layer('nwell')])     # form an enclosure
		pEncPimp = Rect(Layer('pimp'), pEnctmp.getComp(0).getBBox())    # get a copy of enclosure layer pimp
		pEnctmp.destroy()   # delete pEnc group
		# the reason not to directly assign pEnc.getComp(0) to pEncPimp is 
		# that pEnc belongs to a different class from DloGen which Group class belong to.
		# and these two classes are not communicative so it is not doable to directly assign the value

		# now create the gate contact
		gateContact=Contact(self.gateLayer, self.metalLayer,'PIN')	
		# as input of inverter, use default contact width
		# the coords of gateContact is still floating
		
		pgroup.add(pEncPimp)   # add layer pimp into pgroup
		fgPlace(gateContact, WEST, pgroup)
		pgroupContactDist = pgroup.getBBox().left - gateContact.getBBox().right   # measure the posistion of gateContact w.r.t pgroup
		fgPlace(gateContact,EAST,ngroup)
		ngroupContactDist = gateContact.getBBox().left - ngroup.getBBox().right   # measure the position of gateContact w.r.t. ngroup
		gateContactWidth = gateContact.getBBox().right - gateContact.getBBox().left
		# till now gateContact has been put to the east of nmos
		
		# now place ntap
		fgPlace(ntapGroup, SOUTH, pgroup)
		pgroup.add(ntapGroup)
		pEnctmp = fgAddEnclosingRects(pgroup, [Layer('nwell')])
		pEncNwell = Rect(Layer('nwell'), pEnctmp.getBBox())	# form nwell
		pgroup.add(pEncNwell)
		pEnctmp.destroy()
		pmoveDist = ngroup.getBBox().right + ngroupContactDist + gateContactWidth + pgroupContactDist - pEncNwell.getBBox().left
		pgroup.moveTowards(EAST,pmoveDist)   # move the pmos to a proper position


		polyGap = Rect(self.gateLayer, Box(ngateRect.getBBox().right, ngateRect.getBBox().bottom, pgateRect.getBBox().left, pgateRect.getBBox().top))    # draw poly to fill the gap between nmos and pmos gates
		
		
		npowerMetal = Rect(self.metalLayer, Box(0, 0, self.powerMetalWidth,(nEnc.getBBox().top-ptapEnc.getBBox().bottom)))	# draw nmos power metal layer (GND), but the coods are still floating
		ppowerMetal = Rect(self.metalLayer, Box(0, 0, self.powerMetalWidth,(pEncNwell.getBBox().top-pEncNwell.getBBox().bottom)))	# draw pmos power metal layer (VDD)
		
		prMetal1 = self.tech.getPhysicalRule('minSpacing', Layer('metal1'))	# get the minimum spacing of metal1
		npowerMetal.setRight(ndrainContact.getBBox().left - prMetal1.value)	
		npowerMetal.setLeft(ndrainContact.getBBox().left - prMetal1.value - self.powerMetalWidth)
		npowerMetal.setTop(nEnc.getBBox().top)
		npowerMetal.setBottom(ptapContact.getBBox().bottom)
		ppowerMetal.setLeft(pdrainContact.getBBox().right + prMetal1.value)	
		ppowerMetal.setRight(pdrainContact.getBBox().right + prMetal1.value + self.powerMetalWidth)
		ppowerMetal.setTop(pEncNwell.getBBox().top)
		ppowerMetal.setBottom(pEncNwell.getBBox().bottom)
		
		# now wire up everything
		if npowerMetal.getBBox().right < nsourceContact.getBBox().left :  # npowerMetal is in the left of nsourceContact
			npowerSourceMetal = Rect(Layer('metal1'), Box(npowerMetal.getBBox().right, nsourceContact.getBBox().bottom, nsourceContact.getBBox().right, nsourceContact.getBBox().top))   # draw metal between ground metal and nmos source contact
		if ppowerMetal.getBBox().left > psourceContact.getBBox().right :  # ppowerMetal is in the right of psourceContact
			ppowerSourceMetal = Rect(Layer('metal1'), Box(psourceContact.getBBox().left, psourceContact.getBBox().bottom, ppowerMetal.getBBox().left, psourceContact.getBBox().top))     # draw metal between vdd metal and pmos source contact
		if npowerMetal.getBBox().right < ptapContact.getBBox().left :  # npowerMetal is in the left of ptapContact
			ptapMetal = Rect(Layer('metal1'), Box(npowerMetal.getBBox().right, ptapContact.getBBox().bottom, ptapContact.getBBox().right, ptapContact.getBBox().top))  # connect ptap to ground
		if ppowerMetal.getBBox().left > ntapContact.getBBox().right :  # ppowerMetal is in the right of ntapContact
			ntapMetal = Rect(Layer('metal1'), Box(ntapContact.getBBox().left, ntapContact.getBBox().bottom, ppowerMetal.getBBox().left, ntapContact.getBBox().top))  # connect ntap to vdd
		npdrainMetal = Rect(Layer('metal1'), Box(ndrainContact.getBBox().left, ndrainContact.getBBox().bottom, pdrainContact.getBBox().right, pdrainContact.getBBox().top))         # connect the drains of nmos and pmos


		# now make sure gate contact does have contact with gate, and does not violate physical rule at the same time
		# gateContact has been horizontally put into a proper place, but not sure if vertically proper
		gateContactWidth = ( gateContact.getBBox().top - gateContact.getBBox().bottom )    # get the width of gateContact;
		polyCenter = (polyGap.getBBox().top + polyGap.getBBox().bottom) /2	# get the Y coord of poly center
		gateContact.stretch(Box(gateContact.getBBox().left, polyCenter-gateContactWidth/2, gateContact.getBBox().right, polyCenter+gateContactWidth/2))
		gateDrainMetalSpacingClear = prMetal1.value - (npdrainMetal.getBBox().bottom - gateContact.getBBox().top)
		if ( gateDrainMetalSpacingClear > 0) :
			gateContact.moveTowards(SOUTH, gateDrainMetalSpacingClear)
		
		# now create terminals
		self.addTerm('IN', TermType.INPUT)   # input pin of inverter
		self.addTerm('OUT', TermType.OUTPUT)  # output pin
		self.addTerm('VDD', TermType.INPUT)  # set vdd pin
		self.addTerm('VSS', TermType.INPUT)   # set ground pin
		
		self.setTermOrder(['IN','OUT','VDD','VSS'])
		
		self.addPin('IN','IN', gateContact.getBBox(Layer('metal1')),Layer('metal1'))
		self.addPin('OUT','OUT', npdrainMetal.getBBox(), Layer('metal1'))
		self.addPin('VDD','VDD', ppowerMetal.getBBox(), Layer('metal1'))
		self.addPin('VSS', 'VSS', npowerMetal.getBBox(), Layer('metal1'))
		

		
