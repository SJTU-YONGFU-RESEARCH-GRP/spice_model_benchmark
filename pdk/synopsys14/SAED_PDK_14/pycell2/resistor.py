from cni.dlo import *


po_h=0.3
po_v=0.5	
po_nimp = 0.034			# po to nimp distancein = 0.0	
Tsi = 0.01			# fin width
po_met_dis = Tsi		# distance  between poly and metal
modiff2_po_dis = 0.017  	# distance  between modiff2 and poly
modiff2_co_dis = 0.004  	# distance  between modiff2 and contact
modiff2_m1_H_dis = 0.004  	# horisontal distance  between modiff2 and M1
modiff2_m1_V_dis = 0.032  	# vertical   distance  between modiff2 and M1
co_width = 0.03        		# width and length of contact
co_fin_dis = 0.003      	# distance  between contact and fin
co_m1_enc = 0.041		# contact encloser in M1 ###
m1_width = co_width		# width of contact
po_po_dis = 0.06 		# distance between 2 thick polys
typelayer ='NIMP'
layertype ='NO'
VIA0_countv = 1
VIA0_counth = 3
M1_width = 0.05

def nfin(po_v,po_h,VIA0_counth):
		
#generate PO 
		x1 = -po_h/2
		y1 = 0 
		x2 = po_h/2
		y2 = po_v		
		Rect(Layer('PO'), Box(x1, y1, x2, y2))





#generate VIA0
		
				
		lcvia = po_h
		#fh = int((lcvia-0.01)/0.04)
		lcv = lcvia -VIA0_counth*0.03 - (VIA0_counth - 1)*0.044 -0.04
		for j in range(1,VIA0_counth+1):		
			Rect(Layer('VIA0'), Box(x1 +0.02 + lcv/(VIA0_counth+1)+(co_width + lcv/(VIA0_counth+1)+ 0.044)*(j-1), y1 +0.003, x1 + 0.02 + lcv/(VIA0_counth+1) + (co_width + lcv/(VIA0_counth+1) + 0.044)*j-0.044-lcv/(VIA0_counth+1), y1+co_width+0.003))
			y_bots = y1 - (co_width+0.003)
			
			Rect(Layer('VIA0'), Box(x1 + 0.02 + lcv/(VIA0_counth+1) + (co_width + lcv/(VIA0_counth+1) + 0.044)*(j-1), y2 -co_width- 0.003, x1 + 0.02 +lcv/(VIA0_counth+1)+ (co_width + lcv/(VIA0_counth+1) + 0.044)*j-0.044-lcv/(VIA0_counth+1), y2 -0.003))
			y_tops = y2 + (co_width+0.003)

#generate M1 bot	
	
		x1_m1_bot = x1
		y1_m1_bot = 0
		x2_m1_bot = x2
		y2_m1_bot = 0.04
		Rect(Layer('M1'), Box(x1_m1_bot, y1_m1_bot, x2_m1_bot, y2_m1_bot))

#generate M1 top	
	
		x1_m1_top = x1
		y1_m1_top = po_v-0.04
		x2_m1_top = x2
		y2_m1_top = po_v
		Rect(Layer('M1'), Box(x1_m1_top, y1_m1_top, x2_m1_top, y2_m1_top))

#denerate imlants

		Rect(Layer(typelayer), Box(x1 - po_nimp, y1_m1_bot - po_nimp, x2 + po_nimp, y2_m1_top + po_nimp))

#generate RMARK
		Rect(Layer('RMARK'), Box(x1 - po_nimp, y1, x2 + po_nimp, y2))
#gererate CPO
		Rect(Layer('CPO'), Box(x1_m1_bot, y1_m1_bot, x2_m1_bot, y2_m1_bot))
		Rect(Layer('CPO'), Box(x1_m1_top, y1_m1_top, x2_m1_top, y2_m1_top))

		
class resistor(DloGen):
	@classmethod
	def defineParamSpecs(cls, specs):
	# define parameters and default values
    		specs('PO Width', po_h)
		specs('PO Length', po_v)
		specs('VIA0 horizonal count',VIA0_counth)

	
	def setupParams(self, params):
	# process parameter values entered by user
		self.po_h = params['PO Width']
		self.length = params['PO Length']
		self.VIA0_counth = params['VIA0 horizonal count']
		

	def genLayout(self):
	
		po_h = self.po_h
		po_v = self.length 
		VIA0_counth = self.VIA0_counth
		nfin(po_v,po_h, VIA0_counth)


