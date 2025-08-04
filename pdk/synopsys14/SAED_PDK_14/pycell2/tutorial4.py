from cni.dlo import *

CTEN = 0.05 
CT  = 0.042
class res(DloGen):
	@classmethod
	def defineParamSpecs(cls, specs):
	# define parameters and default values
    		specs('width', 0.11)
		specs('height', 0.37)
		specs('layer', Layer('poly1'))
		specs('layer2', Layer('metal2'))
    		specs('layer3', Layer('nimp'))
		specs('layer4', Layer('metal1'))
		specs('layer5', Layer('contact'))

	def setupParams(self, params):
	# process parameter values entered by user
		self.width = params['width']
		self.height = params['height']
		self.layer = params['layer']
		self.layer2 = params['layer2']
		self.layer3 = params['layer3']
		self.layer4 = params['layer4']
		#self.layer5 = params['layer5']
		self.layer5 = params['layer5']
		#self.layer7 = params['layer7']
	def genLayout(self):
	
		gate_l = self.width
		gate_w = self.height 

	
    # generate rectangle layout
	#poly rmark
		x1 = 0.0
		y1 = 0.0
		x2 = gate_l
		y2 = 0.096 + gate_w + 0.096

		Rect(self.layer, Box(x1, y1, x2, y2))
    














