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
layertype ='NO'
VIA0_count = 1
M1_width = 0.1
diff_pot = 0.1
dtype = 'DIFF_15'

def nfin(Lfin,fin_number,dtype):

# define location of  FIN 
		if typelayer == 'PIMP':
			typelayer1 = 'NIMP'
		if typelayer == 'NIMP':
			typelayer1 = 'PIMP'
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

#generate NWELL , DIOD, ESD	
	
		x1_cnwell_left = 0.02
		y1_cnwell_bot = y1_first_fin-0.02
		x2_cnwell_right = y2_last_fin - y1_first_fin+0.056+Lfin
		y2_cnwell_top = y2_last_fin+0.02
		Rect(Layer('DIOD'), Box(x1, y1_first_fin-0.018-0.02, x2, y2+0.018+0.02))	
		if typelayer == 'PIMP':
			Rect(Layer('NWELL'), Box(x1, y1_first_fin-0.018-0.02, x2, y2+0.018+0.02))
		if layertype == 'YES':
			Rect(Layer('ESD'), Box(x1, y1_first_fin-0.018-0.02, x2, y2+0.018+0.02))	

#generate left NIMP, PIMP, M1		
		
		x1_nimp_left = 0 + 2*Pfin+Tsi+0.018+0.036
		y1_nimp_bot = y1_first_fin + 2*Pfin+Tsi+0.018
		x2_nimp_right = y2_last_fin - y1_first_fin+0.036 - (2*Pfin+Tsi+0.018)+Lfin
		y2_nimp_top = y2_last_fin - (2*Pfin+Tsi+0.018)	
		Rect(Layer('M1'), Box(x1_nimp_left+Pfin, y1_nimp_bot+Pfin, x2_nimp_right-Pfin, y2_nimp_top-Pfin))
		Rect(Layer('CTM1'), Box(x1_nimp_left+Pfin, y1_nimp_bot+Pfin, x2_nimp_right-Pfin, y2_nimp_top-Pfin))
		Rect(Layer('DIFF'), Box(x1_nimp_left+Pfin, y1_nimp_bot+Pfin, x2_nimp_right-Pfin, y2_nimp_top-Pfin))
		Rect(Layer(dtype), Box(x1_nimp_left+Pfin, y1_nimp_bot+Pfin, x2_nimp_right-Pfin, y2_nimp_top-Pfin))
		Rect(Layer(typelayer), Box(x1_nimp_left, y1_nimp_bot, x2_nimp_right, y2_nimp_top))
		wid = y1_nimp_bot-y1_first_fin+0.038
		cord = [Point(x1_nimp_left-wid/2,y1_nimp_bot-wid),Point(x1_nimp_left-wid/2,y2_nimp_top+wid/2),Point(x2_nimp_right+wid/2,y2_nimp_top+wid/2),Point(x2_nimp_right+wid/2,y1_nimp_bot-wid/2),Point(x1_nimp_left,y1_nimp_bot-wid/2)]
		Path(Layer(typelayer1), width = wid, points = cord) 
		
		cord = [Point(x1_nimp_left-(diff_pot/2+M1_width/2),y1_nimp_bot-diff_pot/2-M1_width),Point(x1_nimp_left-(diff_pot/2+M1_width/2),y2_nimp_top+(diff_pot/2+M1_width/2)),Point(x2_nimp_right+(diff_pot/2+M1_width/2),y2_nimp_top+(diff_pot/2+M1_width/2)),Point(x2_nimp_right+(diff_pot/2+M1_width/2),y1_nimp_bot-(diff_pot/2+M1_width/2)),Point(x1_nimp_left-diff_pot/2,y1_nimp_bot-(diff_pot/2+M1_width/2))]
		Path(Layer('M1'), width = M1_width, points = cord)
		Path(Layer('DIFF'), width = M1_width, points = cord)
		Path(Layer(dtype), width = M1_width, points = cord)

#generate left rigth VIA0
		
		lrvia = y2_last_fin - wid/2+M1_width/2
		ff = int((lrvia-0.014)/0.074)
		lrv = lrvia - ff*0.03 - (ff-1)*0.044
		for i in range(1,ff+1):
			Rect(Layer('VIA0'), Box(x1_nimp_left-(diff_pot+M1_width)/2-co_width/2, y1_nimp_bot-wid+(wid-M1_width)/2+lrv/2 + (co_width + 0.044)*(i-1), x1_nimp_left-(diff_pot+M1_width)/2+co_width/2, y1_nimp_bot-wid+(wid-M1_width)/2+lrv/2+(co_width+0.044)*i-0.044))
			Rect(Layer('VIA0'), Box(x2_nimp_right+(diff_pot+M1_width)/2-co_width/2, y1_nimp_bot-wid+(wid-M1_width)/2+lrv/2 + (co_width + 0.044)*(i-1), x2_nimp_right+(diff_pot+M1_width)/2+co_width/2, y1_nimp_bot-wid+(wid-M1_width)/2+lrv/2+(co_width+0.044)*i-0.044))

#generate top bottom VIA0
		lrvia = x2_nimp_right+wid - M1_width - x1_nimp_left
		ff = int((lrvia-0.006)/0.074)
		lrv = lrvia - ff*0.03 - (ff-1)*0.044
		for i in range(1,ff+1):
			Rect(Layer('VIA0'), Box(x1_nimp_left-wid/2+M1_width/2+lrv/2+ (co_width + 0.044)*(i-1), y2_nimp_top+(diff_pot+M1_width)/2 - co_width/2, x1_nimp_left-wid/2+M1_width/2+lrv/2+(co_width+0.044)*i-0.044, y2_nimp_top+(diff_pot+M1_width)/2 + co_width/2))
			Rect(Layer('VIA0'), Box(x1_nimp_left-wid/2+M1_width/2+lrv/2+ (co_width + 0.044)*(i-1), y1_nimp_bot-(diff_pot+M1_width)/2 - co_width/2, x1_nimp_left-wid/2+M1_width/2+lrv/2+(co_width+0.044)*i-0.044, y1_nimp_bot-(diff_pot+M1_width)/2 + co_width/2))
		

#generate top central VIA0

		cviav = y2_nimp_top - y1_nimp_bot
		cviah = x2_nimp_right - x1_nimp_left		
		fv = int((cviav-0.01)/0.104)
		fh = int((cviah-0.01)/0.104)
		cvc = cviav - fv*0.03 - (fv-1)*0.044
		chc = cviah - fh*0.03 - (fh-1)*0.044
		for i in range(1,fv+1):
			for j in range(1,fh+1):
				Rect(Layer('VIA0'), Box(x1_nimp_left+chc/2 + (co_width + 0.044)*(j-1), y1_nimp_bot+cvc/2 + (co_width + 0.044)*(i-1), x1_nimp_left+chc/2+(co_width+0.044)*j-0.044, y1_nimp_bot+cvc/2+(co_width+0.044)*i-0.044))


class pd_TO(DloGen):
	@classmethod
	def defineParamSpecs(cls, specs):
	# define parameters and default values
    		specs('Width', fin_number)
		specs('Length', Lfin)
		specs('DIFF type', dtype,'DIFF type', ChoiceConstraint(['DIFF_15', 'DIFF_18']))

	
	def setupParams(self, params):
	# process parameter values entered by user
		self.fin_number = params['Width']
		self.length = params['Length']
		self.dtype = params['DIFF type']
		

	def genLayout(self):
	
		fin_number = self.fin_number
		Lfin = self.length 
		dtype = self.dtype
		nfin(Lfin,fin_number,dtype)


