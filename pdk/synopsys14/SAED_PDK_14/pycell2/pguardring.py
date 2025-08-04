from cni.dlo import *
import re




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
side = 'top,right,bottom,left'

def nfin(Lfin,fin_number,dtype,side):

# define location of  FIN 

		top = re.match( r'.*(top)', side, re.M|re.I)
		rigth = re.match( r'.*(right)', side, re.M|re.I)
		bottom = re.match( r'.*(bottom)', side, re.M|re.I)
		left = re.match( r'.*(left)', side, re.M|re.I)
		fin_number+=2
		for i in range (1, fin_number + 1):
			x1 = - po_met_dis + 0 
			y1 = 0 + (i-1)*Pfin
			x2 = Lfin + po_met_dis + 0
			y2 = Tsi + (i - 1)*Pfin

			y1_first_fin = 0
			y2_last_fin = y2

			#Rect(Layer('rpo'), Box(x1, y1, x2, y2))

#generate Fin 
		for i in range (2, fin_number):
			x1 = -0.002
			y1 = 0 + (i-1)*Pfin
			x2 = y2_last_fin - y1_first_fin-0.002+Lfin
			y2 = Tsi + (i - 1)*Pfin			
			#Rect(Layer('FIN'), Box(x1, y1, x2, y2))

#generate PIMP,	M1 and DIFF

		wid = Pfin*dtype
		x_1=x1+(wid+Tsi+Pfin)/2
		y_1=y1_first_fin+(Tsi+Pfin)/2
		x_2=x1+(wid+Tsi+Pfin)/2
		y_2=y2_last_fin-(wid+Tsi+Pfin)/2 
		x_3=x2-(wid+Tsi+Pfin)/2
		y_3=y2_last_fin-(wid+Tsi+Pfin)/2 
		x_4=x2-(wid+Tsi+Pfin)/2
		y_4=y1_first_fin+(wid+Tsi+Pfin)/2
		x_5=x_1+wid/2
		y_5=y1_first_fin+(wid+Tsi+Pfin)/2		
		cord = [Point(x_1,y_1),Point(x_2,y_2),Point(x_3,y_3),Point(x_4,y_4),Point(x_5,y_5)]
		wid1= Pfin*dtype+0.04
		y_1=y_1-0.02
		x_5=x_1+wid1/2
		cord = [Point(x_1,y_1),Point(x_2,y_2),Point(x_3,y_3),Point(x_4,y_4),Point(x_5,y_5)]
		wi=(wid1-wid)/2
		if left or bottom:
			Rect(Layer('PIMP'), Box(x_1-wid1/2, y_1, x_1+wid1/2, y_1+wid1))
			Rect(Layer('M1'), Box(x_1-wid/2, y_1+wi, x_1+wid/2, y_1+wid1-wi))
			Rect(Layer('DIFF'), Box(x_1-wid/2, y_1+wi, x_1+wid/2, y_1+wid1-wi))
		if left:
			Rect(Layer('PIMP'), Box(x_1-wid1/2, y_1+wid1, x_1+wid1/2, y_2-wid1/2))
			Rect(Layer('M1'), Box(x_1-wid/2, y_1+wid1-wi, x_1+wid/2, y_2-wid1/2+wi))
			Rect(Layer('DIFF'), Box(x_1-wid/2, y_1+wid1-wi, x_1+wid/2, y_2-wid1/2+wi))
		if left or top:
			Rect(Layer('PIMP'), Box(x_1-wid1/2, y_2-wid1/2, x_1+wid1/2, y_2+wid1/2))
			Rect(Layer('M1'), Box(x_1-wid/2, y_2-wid1/2+wi, x_1+wid/2, y_2+wid1/2-wi))
			Rect(Layer('DIFF'), Box(x_1-wid/2, y_2-wid1/2+wi, x_1+wid/2, y_2+wid1/2-wi))
		if top:
			Rect(Layer('PIMP'), Box(x_1+wid1/2, y_2-wid1/2, x_3-wid1/2, y_2+wid1/2))
			Rect(Layer('M1'), Box(x_1+wid1/2-wi, y_2-wid1/2+wi, x_3-wid1/2+wi, y_2+wid1/2-wi))
			Rect(Layer('DIFF'), Box(x_1+wid1/2-wi, y_2-wid1/2+wi, x_3-wid1/2+wi, y_2+wid1/2-wi))
		if top or rigth:
			Rect(Layer('PIMP'), Box(x_3-wid1/2, y_2-wid1/2, x_3+wid1/2, y_2+wid1/2))
			Rect(Layer('M1'), Box(x_3-wid1/2+wi, y_2-wid1/2+wi, x_3+wid1/2-wi, y_2+wid1/2-wi))
			Rect(Layer('DIFF'), Box(x_3-wid1/2+wi, y_2-wid1/2+wi, x_3+wid1/2-wi, y_2+wid1/2-wi))
		if rigth:
			Rect(Layer('PIMP'), Box(x_3-wid1/2, y_4+wid1/2, x_3+wid1/2, y_3-wid1/2))
			Rect(Layer('M1'), Box(x_3-wid1/2+wi, y_4+wid1/2-wi, x_3+wid1/2-wi, y_3-wid1/2+wi))
			Rect(Layer('DIFF'), Box(x_3-wid1/2+wi, y_4+wid1/2-wi, x_3+wid1/2-wi, y_3-wid1/2+wi))
		if rigth or bottom:
			Rect(Layer('PIMP'), Box(x_4-wid1/2, y_1, x_4+wid1/2, y_1+wid1))
			Rect(Layer('M1'), Box(x_4-wid/2, y_1+wi, x_4+wid/2, y_1+wid1-wi))
			Rect(Layer('DIFF'), Box(x_4-wid/2, y_1+wi, x_4+wid/2, y_1+wid1-wi))
		if bottom:
			Rect(Layer('PIMP'), Box(x_1+wid1/2, y_1, x_3-wid1/2, y_1+wid1))
			Rect(Layer('M1'), Box(x_1+wid1/2-wi, y_1+wi, x_3-wid1/2+wi, y_1+wid1-wi))
			Rect(Layer('DIFF'), Box(x_1+wid1/2-wi, y_1+wi, x_3-wid1/2+wi, y_1+wid1-wi))
#generate edge VIA0
		y_1=y_1+0.02

		lrcia = wid - 0.004
		lrci = lrcia - 0.03
		fx = int(lrci/0.074)
		fx = fx +1
		lrc = lrcia - fx*0.03 - (fx-1)*0.044



		lrvia = y2_last_fin - Tsi - Pfin-2*(x_1-wid/2+0.002+lrc/(fx+1))-wid
		lrvi = lrvia - 0.03
		ff = int(lrvi/0.074)
		ff = ff+1
		lrv = lrvia - ff*0.03 - (ff-1)*0.044



		for i in range(1,fx+1):
			for j in range (1,fx+1):
				if left or bottom:
					Rect(Layer('VIA0'), Box(x_1-wid/2+0.002+lrc/(fx+1)+(co_width +lrc/(fx+1)+ 0.044)*(j-1), y_1+lrc/(fx+1)+0.002+(co_width +lrc/(fx+1)+ 0.044)*(i-1),x_1-wid/2+0.002+lrc/(fx+1)+(co_width+lrc/(fx+1)+0.044)*j-0.044-lrc/(fx+1), y_1+0.002+lrc/(fx+1)+(co_width+lrc/(fx+1)+0.044)*i-0.044-lrc/(fx+1)))
				if rigth or bottom:
					Rect(Layer('VIA0'), Box(x_4-wid/2+0.002+lrc/(fx+1)+(co_width +lrc/(fx+1)+ 0.044)*(j-1), y_1+lrc/(fx+1)+0.002+(co_width +lrc/(fx+1)+ 0.044)*(i-1),x_4-wid/2+0.002+lrc/(fx+1)+(co_width+lrc/(fx+1)+0.044)*j-0.044-lrc/(fx+1), y_1+0.002+lrc/(fx+1)+(co_width+lrc/(fx+1)+0.044)*i-0.044-lrc/(fx+1)))
				if left or top:
					Rect(Layer('VIA0'), Box(x_1-wid/2+0.002+lrc/(fx+1)+(co_width +lrc/(fx+1)+ 0.044)*(j-1), y_2-wid/2+lrc/(fx+1)+0.002+(co_width +lrc/(fx+1)+ 0.044)*(i-1),x_1-wid/2+0.002+lrc/(fx+1)+(co_width+lrc/(fx+1)+0.044)*j-0.044-lrc/(fx+1), y_2-wid/2+0.002+lrc/(fx+1)+(co_width+lrc/(fx+1)+0.044)*i-0.044-lrc/(fx+1)))
				if rigth or top:
					Rect(Layer('VIA0'), Box(x_4-wid/2+0.002+lrc/(fx+1)+(co_width +lrc/(fx+1)+ 0.044)*(j-1), y_2-wid/2+lrc/(fx+1)+0.002+(co_width +lrc/(fx+1)+ 0.044)*(i-1),x_4-wid/2+0.002+lrc/(fx+1)+(co_width+lrc/(fx+1)+0.044)*j-0.044-lrc/(fx+1), y_2-wid/2+0.002+lrc/(fx+1)+(co_width+lrc/(fx+1)+0.044)*i-0.044-lrc/(fx+1)))
		
				xx_1=x_1-wid/2+0.002+lrc/(fx+1)+(co_width+lrc/(fx+1)+0.044)*j-0.044-lrc/(fx+1)+ 0.044
				yy_bot = y_1+0.002+lrc/(fx+1)+(co_width+lrc/(fx+1)+0.044)*i-0.044-lrc/(fx+1)+0.044
		yy_top = y_2-wid/2+lrc/(fx+1)+0.002-0.044
#generate left and rigth VIA0	

		xx_1_left=x_1-wid/2+0.002+lrc/(fx+1)
		xx_2 = x_4-wid/2+0.002+lrc/(fx+1)- 0.044
		yy_2 =  y_1+0.002+lrv/(ff+1)+(co_width+lrv/(ff+1)+0.044)*i-0.044-lrv/(ff+1)
		lrvia_2 = yy_top-yy_bot
		lrvi_2 = lrvia_2 - 0.03
		ff_2 = int(lrvi_2/0.074)
		ff_2 = ff_2+1
		lrv_2 = lrvia_2 - ff_2*0.03 - (ff_2-1)*0.044
		for j in range(1,fx+1):
			for i in range(1,ff_2+1):
				if left:
					Rect(Layer('VIA0'), Box(x_1-wid/2+0.002+lrc/(fx+1)+(co_width +lrc/(fx+1)+ 0.044)*(j-1), yy_bot+lrv_2/(ff_2+1)+0.002+(co_width +lrv_2/(ff_2+1)+ 0.044)*(i-1),x_1-wid/2+0.002+lrc/(fx+1)+(co_width +lrc/(fx+1)+ 0.044)*j-0.044-lrc/(fx+1), yy_bot+0.002+lrv_2/(ff_2+1)+(co_width+lrv_2/(ff_2+1)+0.044)*i-0.044-lrv_2/(ff_2+1)))
				if rigth:
					Rect(Layer('VIA0'), Box(x_4-wid/2+0.002+lrc/(fx+1)+(co_width +lrc/(fx+1)+ 0.044)*(j-1), yy_bot+lrv_2/(ff_2+1)+0.002+(co_width +lrv_2/(ff_2+1)+ 0.044)*(i-1),x_4-wid/2+0.002+lrc/(fx+1)+(co_width +lrc/(fx+1)+ 0.044)*j-0.044-lrc/(fx+1), yy_bot+0.002+lrv_2/(ff_2+1)+(co_width+lrv_2/(ff_2+1)+0.044)*i-0.044-lrv_2/(ff_2+1)))
#(co_width+lrv/(ff+1)+0.044)*i+0.044+lrv/(ff+1)


#generate top and bottom VIA0
		lrvia_1 = xx_2-xx_1
		lrvi_1 = lrvia_1 - 0.03
		ff_1 = int(lrvi_1/0.074)
		ff_1 = ff_1 + 1
		lrv_1 = lrvia_1 - ff_1*0.03 - (ff_1-1)*0.044
		for j in range(1,ff_1+1):
			for i in range(1,fx+1):
				if bottom:
					Rect(Layer('VIA0'), Box(xx_1+lrv_1/(ff_1+1)+(co_width +lrv_1/(ff_1+1)+ 0.044)*(j-1), y_1+lrc/(fx+1)+0.002+(co_width +lrc/(fx+1)+ 0.044)*(i-1),xx_1+lrv_1/(ff_1+1)+(co_width+lrv_1/(ff_1+1)+0.044)*j-0.044-lrv_1/(ff_1+1), y_1+0.002+lrc/(fx+1)+(co_width+lrc/(fx+1)+0.044)*i-0.044-lrc/(fx+1)))
				if top:
					Rect(Layer('VIA0'), Box(xx_1+lrv_1/(ff_1+1)+(co_width +lrv_1/(ff_1+1)+ 0.044)*(j-1), y_2-wid/2+lrc/(fx+1)+0.002+(co_width +lrc/(fx+1)+ 0.044)*(i-1),xx_1+lrv_1/(ff_1+1)+(co_width+lrv_1/(ff_1+1)+0.044)*j-0.044-lrv_1/(ff_1+1), y_2-wid/2+0.002+lrc/(fx+1)+(co_width+lrc/(fx+1)+0.044)*i-0.044-lrc/(fx+1)))
#(co_width+lrv/(ff+1)+0.044)*i+0.044+lrv/(ff+1)

class pguardring(DloGen):
	@classmethod
	def defineParamSpecs(cls, specs):
	# define parameters and default values
    		specs('Width', fin_number)
		specs('Length', Lfin)
		specs('Wire Width', dtype)
		specs('Sides', side)
	
	def setupParams(self, params):
	# process parameter values entered by user
		self.fin_number = params['Width']
		self.length = params['Length']
		self.dtype = params['Wire Width']
		self.side = params['Sides']	

	def genLayout(self):
	
		fin_number = self.fin_number
		Lfin = self.length 
		dtype = self.dtype
		side = self.side
		nfin(Lfin,fin_number,dtype,side)


