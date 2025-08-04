from cni.dlo import *





Lfin = 0.014			# fin length or gate length
Tsi = 0.01			# fin width
po_met_dis = Tsi		# distance  between poly and metal
po_fin_h_dis = 0.05		# horisontal distance  between poly and fin
Pfin = 0.046			# distance  between fins. In ader words , Fin pitch using spacer lithography
fin_number = 2			# amount of fin
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
layertype ='PrBoundary'
VIA0_count = 1
#fettype = 'DIFF_15'

def nfin(x,Lfin,fin_number,j, nf,VIA0_count):#del layertype

# define location of  FIN 
		for i in range (1, fin_number + 1):
			x1 = - po_met_dis + 0 + x 
			y1 = 0 + (i-1)*Pfin
			x2 = Lfin + po_met_dis + 0 + x
			y2 = Tsi + (i - 1)*Pfin

			y1_first_fin = 0
			y2_last_fin = y2

			#Rect(Layer('rpo'), Box(x1, y1, x2, y2))

# generate centre POLY 

		x1 = 0 + x 
		y1 = 0 - po_fin_h_dis -0.018
		x2 = 0 + Lfin + x
		y2 = y2 + po_fin_h_dis + 0.018

		Rect(Layer('PO'), Box(x1, y1, x2, y2))


#generate right POLYS
		if Lfin > 0.014:
			po_po_dis = 0.11
		else :
			po_po_dis = 0.06
		xx1=x1
		yy1=y1
		xx2=x2
		yy2=y2
		for gg in range (0,nf):

			xx1 = xx1 + po_po_dis + Lfin
			#y1 = 0 - po_fin_h_dis
			xx2 = xx2 + po_po_dis + Lfin
			#y2 = y2 + po_fin_h_dis

			x2_right_po = xx2	
			y2_right_po = yy2

			Rect(Layer('PO'), Box(xx1, y1, xx2, y2))
		x1_dumy_po = xx2 + po_po_dis	
		x2_dumy_po = xx2 + po_po_dis + Lfin

		Rect(Layer('PO'), Box(x1_dumy_po, y1, x2_dumy_po, y2))


#generate left POLYS

		x1 = 0 - po_po_dis - Lfin + x
		#y1 = 0 - po_fin_h_dis
		x2 = 0 + Lfin - po_po_dis - Lfin + x
		#y2 = y2 + po_fin_h_dis

		x1_left_po = x1	
		x2_left_po = x2
		y1_left_po = y1
		y2_left_po = y2

		Rect(Layer('PO'), Box(x1, y1, x2, y2))
		
		if x == 0:
			x1_dumy_po = x1 - po_po_dis - Lfin
 			x2_dumy_po = x1 - po_po_dis
			Rect(Layer('PO'), Box(x1_dumy_po , y1, x2_dumy_po, y2))
#generate instnce 	

#del		Rect(Layer(layertype), Box(x1_left_po, y1_left_po, x2_right_po, y2_right_po))

#generate Fin 
		for i in range (1, fin_number + 1):
			x1 = x1_left_po - 0.14
			y1 = 0 + (i-1)*Pfin
			x2 = xx2 + 0.14 
			y2 = Tsi + (i - 1)*Pfin			
			Rect(Layer('FIN'), Box(x1, y1, x2, y2))

#generate diff

		x1 = x1_left_po
		y1 = y1_first_fin-0.018
		x2 = x2_right_po
		y2 = y2_last_fin+0.018
		Rect(Layer('DIFF'), Box(x1, y1, x2, y2))

#generate nplus 	


		x1 = x1 - 0.052 - x
		y1 = y1_left_po #y1 - 0.067
		x2 = x2 + 0.052
		y2 = y2_left_po#y2 + 0.067		
		Rect(Layer(typelayer), Box(x1, y1, x2, y2)) 
#		Rect(Layer(fettype), Box(x1, y1, x2, y2))

		#via_count = (y2_last_fin + 0.018 - (y1_first_fin - 0.018))/co_width


#generate left contact
		if typelayer == 'NIMP':
			for gg in range(0,nf+1):
				for i in range (1, VIA0_count+1 ):
					x1 = -po_po_dis/2 - co_width/2 + gg*(po_po_dis+Lfin)
					y1 = i*Tsi + j*co_fin_dis + (i-1)*co_width 
					x2 = -po_po_dis/2 + co_width/2 + gg*(po_po_dis+Lfin)
					y2 = i*Tsi + j*co_fin_dis + i*co_width
					Rect(Layer('VIA0'), Box(x1, y1, x2, y2))
					if i == VIA0_count:
						last_via0 = y2
		rev = range (1, VIA0_count+1 )
		rever = reversed(rev)
		if typelayer == 'PIMP':
			for gg in range(0,nf+1):
				for i in range (VIA0_count,0,-1):
					x1 = -po_po_dis/2 - co_width/2 + gg*(po_po_dis+Lfin)
					y1 = y2_last_fin + 0.018 - (i*Tsi + j*co_fin_dis + i*co_width )
					x2 = -po_po_dis/2 + co_width/2 + gg*(po_po_dis+Lfin)
					y2 = y2_last_fin + 0.018 - (i*Tsi + j*co_fin_dis + (i-1)*co_width)
					Rect(Layer('VIA0'), Box(x1, y1, x2, y2))
					if i == VIA0_count:
						last_via0 = y1

#generate left modiff2 
		if typelayer == 'PIMP':
			for gg in range(0,nf+1):
				x1 = -po_po_dis/2 - co_width/2 + gg*(po_po_dis+Lfin)
				y1 = last_via0-0.01
				x2 = -po_po_dis/2 + co_width/2 + gg*(po_po_dis+Lfin)
				y2 = y2_last_fin + 0.018
				Rect(Layer('CTM1'), Box(x1, y1, x2, y2))
		if typelayer == 'NIMP':
			for gg in range(0,nf+1):
				x1 = -po_po_dis/2 - co_width/2 + gg*(po_po_dis+Lfin)
				y1 = y1_first_fin-0.018
				x2 = -po_po_dis/2 + co_width/2 + gg*(po_po_dis+Lfin)
				y2 = last_via0+0.01
				Rect(Layer('CTM1'), Box(x1, y1, x2, y2))

class pfet_0(DloGen):
	@classmethod
	def defineParamSpecs(cls, specs):
	# define parameters and default values
    		specs('fin number', fin_number)
		specs('length', float(Lfin))
		specs('nf', 1)
#del		specs('yyy',layertype, 'xxx',ChoiceConstraint(['PrBoundary','HVTIMP','LVTIMP','SLVTIMP']))
		specs('VIA0_count',VIA0_count)

	
	def setupParams(self, params):
	# process parameter values entered by user
		self.fin_number = params['fin number']
		self.length = params['length']
		self.nf = params['nf']
		self.VIA0_count = params['VIA0_count']
		

	def genLayout(self):
	
		fin_number = self.fin_number
		Lfin = self.length 
		global nf
		nf = self.nf
#del		layertype = self.layertype
		VIA0_count = self.VIA0_count
		if self.length > 0.014:
			po_po_dis = 0.014
		j=1
		nfin(0,Lfin,fin_number,j,nf,VIA0_count)#del layertype













