from cni.dlo import *





Lfin = 0.014			# fin length or gate length
Tsi = 0.01			# fin width
po_met_dis = Tsi		# distance  between poly and metal
po_fin_h_dis = 0.1		# horisontal distance  between poly and fin
Pfin = 0.048			# distance  between fins. In ader words , Fin pitch using spacer lithography
fin_number = 2			# amount of fin
modiff2_po_dis = 0.017  	# distance  between modiff2 and poly
modiff2_co_dis = 0.004  	# distance  between modiff2 and contact
modiff2_m1_H_dis = 0.004  	# horisontal distance  between modiff2 and metal1
modiff2_m1_V_dis = 0.032  	# vertical   distance  between modiff2 and metal1
co_width = 0.032        	# width and length of contact
co_fin_dis = 0.003      	# distance  between contact and fin
co_m1_enc = 0.041		# contact encloser in metal1 ###
m1_width = co_width		# width of contact
po_po_dis = 0.074 		# distance between 2 polys
pmet_nmet_h_dis_po = 0.022	# horisontal distance between po and pmet or nwell
pmet_nmet_v_dis_po = 0.012	# vertical distance between po and pmet or nwell


def pfinlvt(x,Lfin,fin_number,k):

# define location of  FIN 
		for i in range (1, fin_number + 1):
			x1 = - po_met_dis + 0 + x 
			y1 = 0 + (i-1)*Pfin
			x2 = Lfin + po_met_dis + 0 + x
			y2 = Tsi + (i - 1)*Pfin

			y1_first_fin = 0
			y2_last_fin = y2

			#Rect(Layer('rpo'), Box(x1, y1, x2, y2))

		y1lvtn = 0
		y2lvtn = y2

# generate centre POLY 




		x1 = 0 + x 
		y1 = 0 - po_fin_h_dis
		x2 = 0 + Lfin + x
		y2 = y2 + po_fin_h_dis

		Rect(Layer('poly1'), Box(x1, y1, x2, y2))


#generate right POLYS


		x1 = 0 + po_po_dis + Lfin + x
		#y1 = 0 - po_fin_h_dis
		x2 = 0 + Lfin + po_po_dis + Lfin + x
		#y2 = y2 + po_fin_h_dis

		x2_right_po = x2	
		y2_right_po = y2

		Rect(Layer('poly1'), Box(x1, y1, x2, y2))


		if k == nf:
			x1_dumy_po = x2 + po_po_dis	
			x2_dumy_po = x2 + po_po_dis + Lfin

			x2_po_coord = x2_dumy_po
			y2_po_coord = y2

			Rect(Layer('poly1'), Box(x1_dumy_po, y1, x2_dumy_po, y2))


#generate left POLYS

		x1 = 0 - po_po_dis - Lfin + x
		#y1 = 0 - po_fin_h_dis
		x2 = 0 + Lfin - po_po_dis - Lfin + x
		#y2 = y2 + po_fin_h_dis

		x1_left_po = x1	
		y1_left_po = y1


		Rect(Layer('poly1'), Box(x1, y1, x2, y2))
		
		if x == 0:
			x1_dumy_po = x1 - po_po_dis - Lfin
 			x2_dumy_po = x1 - po_po_dis
			
			global x1_po_coord
			global y1_po_coord

			x1_po_coord = x1_dumy_po
			y1_po_coord = y1			

			Rect(Layer('poly1'), Box(x1_dumy_po , y1, x2_dumy_po, y2))

#generate instnce 	



		Rect(Layer('dpnw'), Box(x1_left_po, y1_left_po, x2_right_po, y2_right_po))

#generate lvtn
 
		Rect(Layer('metal3'), Box(x1_left_po, y1lvtn, x2_right_po, y2lvtn))

#generate Fin 
		for i in range (1, fin_number + 1):
			x1 = x1_left_po - 0.14
			y1 = 0 + (i-1)*Pfin
			x2 = x2_right_po + 0.14
			y2 = Tsi + (i - 1)*Pfin


			
			Rect(Layer('rpo'), Box(x1, y1, x2, y2))

#generate diff

		x1 = x1_left_po
		y1 = y1_first_fin
		x2 = x2_right_po
		y2 = y2_last_fin


		Rect(Layer('diff'), Box(x1, y1, x2, y2))

#generate pplus 	


		x1 = x1 - 0.052 - x
		y1 = y1 - 0.067
		x2 = x2 + 0.052
		y2 = y2 + 0.067

		
		Rect(Layer('pwell'), Box(x1, y1, x2, y2)) 


#generate left contact
		j=1
		for i in range (1, fin_number ):

			x1 = -modiff2_po_dis - modiff2_co_dis - co_width + x
			y1 = i*Tsi + j*co_fin_dis + (i-1)*co_width  
			x2 = -modiff2_po_dis - modiff2_co_dis + x
			y2 = i*Tsi + j*co_fin_dis + i*co_width
			j=j+2
			Rect(Layer('contact'), Box(x1, y1, x2, y2))

#generate left metal1 

		x1 = -(modiff2_po_dis + modiff2_co_dis + m1_width ) + x
		global metal_modul_x1
		metal_modul_x1= modiff2_po_dis + modiff2_co_dis + m1_width
		y1 = Tsi + co_fin_dis - co_m1_enc
		x2 = -(modiff2_po_dis + modiff2_co_dis) + x
		y2 = y2 + co_m1_enc
		Rect(Layer('metal1'), Box(x1, y1, x2, y2))

#generate left modiff2 

		x1 = -(modiff2_po_dis + 2*modiff2_m1_H_dis + m1_width ) + x
		y1 = Tsi + co_fin_dis - modiff2_m1_V_dis
		x2 = -(modiff2_po_dis) + x
		y2 = y2 - co_m1_enc + modiff2_m1_V_dis
		Rect(Layer('metal2'), Box(x1, y1, x2, y2))


#generate right contact
		j=1
		for i in range (1, fin_number ):

			x1 = modiff2_po_dis + modiff2_co_dis + Lfin + x
			y1 = i*Tsi + j*co_fin_dis + (i-1)*co_width 
			x2 = modiff2_po_dis + modiff2_co_dis + co_width + Lfin + x
			y2 = i*Tsi + j*co_fin_dis + i*co_width
			j=j+2
			Rect(Layer('contact'), Box(x1, y1, x2, y2))

#generate right metal1 

		x1 = (modiff2_po_dis + modiff2_co_dis + Lfin ) + x 
		global metal1_po_dis 
		metal1_po_dis = modiff2_po_dis + modiff2_co_dis
		y1 = Tsi + co_fin_dis - co_m1_enc
		x2 = modiff2_po_dis + modiff2_co_dis + m1_width + Lfin + x
		y2 = y2 + co_m1_enc
		Rect(Layer('metal1'), Box(x1, y1, x2, y2))

#generate left modiff2 

		x1 = (modiff2_po_dis + Lfin ) + x 
		y1 = Tsi + co_fin_dis - modiff2_m1_V_dis
		x2 = modiff2_po_dis + 2*modiff2_m1_H_dis + m1_width + Lfin + x
		y2 = y2 - co_m1_enc + modiff2_m1_V_dis
		Rect(Layer('metal2'), Box(x1, y1, x2, y2))

#generate pmet & nwell



		if k == nf:
		

			
			x1_po_coord = x1_po_coord - pmet_nmet_h_dis_po
			y1_po_coord = y1_po_coord - pmet_nmet_v_dis_po
			x2_po_coord = x2_po_coord + pmet_nmet_h_dis_po
			y2_po_coord = y2_po_coord + pmet_nmet_v_dis_po
			


			Rect(Layer('nwell'), Box(x1_po_coord, y1_po_coord , x2_po_coord, y2_po_coord))
			Rect(Layer('metal6'), Box(x1_po_coord, y1_po_coord , x2_po_coord, y2_po_coord))


class p_fin_lvt(DloGen):
	@classmethod
	def defineParamSpecs(cls, specs):
	# define parameters and default values
    		specs('fin number', fin_number)
		specs('length', Lfin)
		specs('nf', 1)
	
	def setupParams(self, params):
	# process parameter values entered by user
		self.fin_number = params['fin number']
		self.length = params['length']
		self.nf = params['nf']
		

	def genLayout(self):
	
		fin_number = self.fin_number
		Lfin = self.length 
		global nf
		nf = self.nf


		j = 1
		pfinlvt(0,Lfin,fin_number,j)

		
		for j in range (2, nf + 1):
			x=(j-1)*(metal_modul_x1 + Lfin + metal1_po_dis)
			pfinlvt(x,Lfin,fin_number,j)













