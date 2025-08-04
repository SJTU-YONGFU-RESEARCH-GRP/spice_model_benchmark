from cni.dlo import *





Lfin = 0.0			# fin length or gate length
Tsi = 0.014			# fin width
po_met_dis = Tsi		# distance  between poly and metal
po_fin_h_dis = 0.1		# horisontal distance  between poly and fin
Pfin = 0.05			# distance  between fins. In ader words , Fin pitch using spacer lithography
fin_number = 15			# amount of fin
modiff2_po_dis = 0.017  	# distance  between modiff2 and poly
modiff2_co_dis = 0.004  	# distance  between modiff2 and contact
modiff2_m1_H_dis = 0.004  	# horisontal distance  between modiff2 and M1
modiff2_m1_V_dis = 0.032  	# vertical   distance  between modiff2 and M1
co_width = 0.03        		# width and length of contact
co_fin_dis = 0.003      	# distance  between contact and fin
co_m1_enc = 0.041		# contact encloser in M1 ###
m1_width = co_width		# width of contact
po_po_dis = 0.06 		# distance between 2 thick polys
typelayer ='PIMP'
layertype ='YES'
VIA0_count = 1
M1_width = 0.1
diff_pot = 0.1
dtype = 1

def nfin(Lfin,fin_number,dtype):

# define location of  FIN 
		for i in range (1, fin_number + 1):
			x1 = - po_met_dis + 0 
			y1 = 0 + (i-1)*Pfin
			x2 = Lfin + po_met_dis + 0
			y2 = Tsi + (i - 1)*Pfin

			y1_first_fin = 0
			y2_last_fin = y2

			#Rect(Layer('rpo'), Box(x1, y1, x2, y2))

#generate Fin 
		for i in range (1, fin_number + 1):
			x1 = -0.002
			y1 = 0 + (i-1)*Pfin
			x2 = y2_last_fin - y1_first_fin+0.074+Lfin
			y2 = Tsi + (i - 1)*Pfin			
			Rect(Layer('FIN'), Box(x1, y1, x2, y2))

#generate PIMP
		wid = dtype*co_width+(dtype-1)*0.044+0.006+0.04
		cord = [Point(x1+wid/2,y1_first_fin),Point(x1+wid/2,y2_last_fin-wid/2),Point(x2-wid/2,y2_last_fin-wid/2),Point(x2-wid/2,y1_first_fin+wid/2),Point(x1+wid,y1_first_fin+wid/2)]
		Path(Layer(typelayer), width = wid, points = cord) 
		wid = dtype*co_width+(dtype-1)*0.044+0.006	
		Path(Layer('M1'), width = wid, points = cord) 
		Path(Layer('DIFF'), width = wid, points = cord)

class test(DloGen):
	@classmethod
	def defineParamSpecs(cls, specs):
	# define parameters and default values
    		specs('Width', fin_number)
		specs('Length', Lfin)
		specs('Via count', dtype)

	
	def setupParams(self, params):
	# process parameter values entered by user
		self.fin_number = params['Width']
		self.length = params['Length']
		self.dtype = params['Via count']
		

	def genLayout(self):
	
		fin_number = self.fin_number
		Lfin = self.length 
		dtype = self.dtype
		nfin(Lfin,fin_number,dtype)


