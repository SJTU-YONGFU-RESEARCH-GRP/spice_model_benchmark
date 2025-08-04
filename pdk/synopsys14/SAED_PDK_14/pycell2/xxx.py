from cni.dlo import *





Lfin = 0.014			# fin length or gate length
Tsi = 0.01			# fin width
po_met_dis = Tsi		# distance  between poly and metal
po_fin_h_dis = 0.1		# horisontal distance  between poly and fin
Pfin = 0.048			# distance  between fins. In ader words , Fin pitch using spacer lithography
fin_number = 2			# amount of fin
modiff2_po_dis = 0.017  	# distance  between modiff2 and poly
modiff2_co_dis = 0.004  	# distance  between modiff2 and contact
modiff2_m1_H_dis = 0.004  	# horisontal distance  between modiff2 and M1
modiff2_m1_V_dis = 0.032  	# vertical   distance  between modiff2 and M1
co_width = 0.032        	# width and length of contact
co_fin_dis = 0.003      	# distance  between contact and fin
co_m1_enc = 0.041		# contact encloser in M1 ###
m1_width = co_width		# width of contact
po_po_dis = 0.06 		# distance between 2 thick polys
typelayer ='PIMP'
layertype ='PrBoundary'

def nfin1(x,Lfin,fin_number,j,typelayer,layertype, nf):

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
		y1 = 0 - po_fin_h_dis
		x2 = 0 + Lfin + x
		y2 = y2 + po_fin_h_dis

		Rect(Layer('PO'), Box(x1, y1, x2, y2))


#generate right POLYS
		if Lfin > 0.014:
			po_po_dis = 0.11
		else :
			po_po_dis = 0.06 

		for x in range (0,nf):

			x1 = 0 + po_po_dis + Lfin + x
			#y1 = 0 - po_fin_h_dis
			x2 = 0 + Lfin + po_po_dis + Lfin + x
			#y2 = y2 + po_fin_h_dis

			x2_right_po = x2	
			y2_right_po = y2

			Rect(Layer('PO'), Box(x1, y1, x2, y2))

		
		x1_dumy_po = x2 + po_po_dis	
		x2_dumy_po = x2 + po_po_dis + Lfin

		Rect(Layer('PO'), Box(x1_dumy_po, y1, x2_dumy_po, y2))


#generate left POLYS

		x1 = 0 - po_po_dis - Lfin + x
		#y1 = 0 - po_fin_h_dis
		x2 = 0 + Lfin - po_po_dis - Lfin + x
		#y2 = y2 + po_fin_h_dis

		x1_left_po = x1	
		y1_left_po = y1

		Rect(Layer('PO'), Box(x1, y1, x2, y2))
		
		if x == 0:
			x1_dumy_po = x1 - po_po_dis - Lfin
 			x2_dumy_po = x1 - po_po_dis
			Rect(Layer('PO'), Box(x1_dumy_po , y1, x2_dumy_po, y2))

#generate instnce 	



		Rect(Layer(layertype), Box(x1_left_po, y1_left_po, x2_right_po, y2_right_po))

#generate Fin 
		for i in range (1, fin_number + 1):
			x1 = x1_left_po - 0.14
			y1 = 0 + (i-1)*Pfin
			x2 = x2_right_po + 0.14
			y2 = Tsi + (i - 1)*Pfin


			
			Rect(Layer('FIN'), Box(x1, y1, x2, y2))

#generate diff

		x1 = x1_left_po
		y1 = y1_first_fin
		x2 = x2_right_po
		y2 = y2_last_fin


		Rect(Layer('DIFF'), Box(x1, y1, x2, y2))

#generate nplus 	


		x1 = x1 - 0.052 - x
		y1 = y1 - 0.067
		x2 = x2 + 0.052
		y2 = y2 + 0.067

		
		Rect(Layer(typelayer), Box(x1, y1, x2, y2)) 


#generate left contact
		j=1
		for i in range (1, fin_number ):

			x1 = -modiff2_po_dis - modiff2_co_dis - co_width + x
			y1 = i*Tsi + j*co_fin_dis + (i-1)*co_width  
			x2 = -modiff2_po_dis - modiff2_co_dis + x
			y2 = i*Tsi + j*co_fin_dis + i*co_width
			j=j+2
			Rect(Layer('VIA0'), Box(x1, y1, x2, y2))

#generate left M1 

		x1 = -(modiff2_po_dis + modiff2_co_dis + m1_width ) + x
		global metal_modul_x1
		metal_modul_x1= modiff2_po_dis + modiff2_co_dis + m1_width
		y1 = Tsi + co_fin_dis - co_m1_enc
		x2 = -(modiff2_po_dis + modiff2_co_dis) + x
		y2 = y2 + co_m1_enc
		Rect(Layer('M1'), Box(x1, y1, x2, y2))

#generate left modiff2 

		x1 = -(modiff2_po_dis + 2*modiff2_m1_H_dis + m1_width ) + x
		y1 = Tsi + co_fin_dis - modiff2_m1_V_dis
		x2 = -(modiff2_po_dis) + x
		y2 = y2 - co_m1_enc + modiff2_m1_V_dis
		Rect(Layer('M2'), Box(x1, y1, x2, y2))


#generate right contact
		j=1
		for i in range (1, fin_number ):

			x1 = modiff2_po_dis + modiff2_co_dis + Lfin + x
			y1 = i*Tsi + j*co_fin_dis + (i-1)*co_width 
			x2 = modiff2_po_dis + modiff2_co_dis + co_width + Lfin + x
			y2 = i*Tsi + j*co_fin_dis + i*co_width
			j=j+2
			Rect(Layer('VIA0'), Box(x1, y1, x2, y2))

#generate right M1 

		x1 = (modiff2_po_dis + modiff2_co_dis + Lfin ) + x 
		global M1_po_dis 
		M1_po_dis = modiff2_po_dis + modiff2_co_dis
		y1 = Tsi + co_fin_dis - co_m1_enc
		x2 = modiff2_po_dis + modiff2_co_dis + m1_width + Lfin + x
		y2 = y2 + co_m1_enc
		Rect(Layer('M1'), Box(x1, y1, x2, y2))

#generate left modiff2 

		x1 = (modiff2_po_dis + Lfin ) + x 
		y1 = Tsi + co_fin_dis - modiff2_m1_V_dis
		x2 = modiff2_po_dis + 2*modiff2_m1_H_dis + m1_width + Lfin + x
		y2 = y2 - co_m1_enc + modiff2_m1_V_dis
		Rect(Layer('M2'), Box(x1, y1, x2, y2))





class n_fin(DloGen):
	@classmethod
	def defineParamSpecs(cls, specs):
	# define parameters and default values
    		specs('fin number', fin_number)
		specs('length', Lfin)
		specs('nf', 1)
		specs('type',typelayer, 'FinFET type',ChoiceConstraint(['PIMP', 'NIMP']))
		specs('yyy',layertype, 'xxx',ChoiceConstraint(['PrBoundary','HVTIMP','LVTIMP','SLVTIMP']))

	
	def setupParams(self, params):
	# process parameter values entered by user
		self.fin_number = params['fin number']
		self.length = params['length']
		self.nf = params['nf']
		self.typelayer = params['type']
		self.layertype = params['yyy']
		

	def genLayout(self):
	
		fin_number = self.fin_number
		Lfin = self.length 
		global nf
		nf = self.nf
		typelayer = self.typelayer
		layertype = self.layertype
		if self.length > 0.014:
			po_po_dis = 0.014






		j = 1
		nfin1(0,Lfin,fin_number,j,typelayer,layertype,nf)

		
		for j in range (2, nf + 1):
			x=(j-1)*(metal_modul_x1 + Lfin + M1_po_dis)
			nfin1(0,Lfin,fin_number,j,typelayer,layertype,nf)













