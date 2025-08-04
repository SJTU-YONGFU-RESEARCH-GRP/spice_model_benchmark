;; Translated with ADS Netlist Translator (*) 270.day Jul 31 2004
;;
;;*************************************************************
;;   Generic PDK Resistor models                       05/17/03
;;                                              PDK Tech Center
;;*************************************************************
;
;;simulator lang=spectre
;;library gpdk

#ifdef res


;; Nplus Resistor
;;
;; nplusreslw is a spectre diffusion resistor model (rdiff) - no equivalent in ADS 2004A
model nplusreslw R_Model Rsh=50 Width=1e-6 Wdexp=1 Ldexp=1 TC1=3e-3 TC2=-2e-6

inline define gpdk180_nplusres ( PLUS MINUS B)
parameters  sl=0.6e-6 w=0.6e-6 rcont="UNDEF"
ADS_rcont_0=15/int(((w*1e6)-0.19999)/0.4)
ADS_rcont_1=if (rcont == "UNDEF") then ADS_rcont_0 else rcont endif


R:rcont1 PLUS PLUSHEAD R=ADS_rcont_1/2
  nplusreslw:gpdk180_nplusres PLUSHEAD MINUSHEAD Length=sl Width=w
R:rcont2 MINUSHEAD MINUS R=ADS_rcont_1/2

end gpdk180_nplusres


;Pplus Resistor
;;
;; pplusreslw is a spectre diffusion resistor model (rdiff) - no equivalent in ADS 2004A
model pplusreslw R_Model Rsh=158 Width=1e-6 Wdexp=1 Ldexp=1 TC1=3e-3 TC2=-4e-6

inline define gpdk180_pplusres ( PLUS MINUS B)
parameters  sl=0.6e-6 w=0.6e-6 rcont="UNDEF"
ADS_rcont_2=15/int(((w*1e6)-0.19999)/0.4)
ADS_rcont_3=if (rcont == "UNDEF") then ADS_rcont_2 else rcont endif


R:rcont1 PLUS PLUSHEAD R=ADS_rcont_3/2
  pplusreslw:gpdk180_pplusres PLUSHEAD MINUSHEAD Length=sl Width=w
R:rcont2 MINUSHEAD MINUS R=ADS_rcont_3/2
end gpdk180_pplusres



;
; Low Poly Resistor
; polyreslw is a spectre physical resistor model (phy_res) - no equivalent in ADS 2004A
model polyreslw R_Model Rsh=7.5 Width=1e-6 Wdexp=1 Ldexp=1 TC1=3e-3 TC2=-2e-6



inline define gpdk180_polyres ( PLUS MINUS)
parameters  sl=0.6e-6 w=0.6e-6 rcont="UNDEF"
etchc=0
etchlc=0
mult=1
cj=1.33e-3
cjsw=3.15e-10
ADS_rcont_4=10/int(((w*1e6)-0.19999)/0.4)
ADS_rcont_5=if (rcont == "UNDEF") then ADS_rcont_4 else rcont endif

R:rcont1 PLUS PLUSHEAD R=ADS_rcont_5/2
polyreslw:gpdk180_polyres PLUSHEAD MINUSHEAD Length=sl Width=w
R:rcont2 MINUSHEAD MINUS R=ADS_rcont_5/2


model cap_pn C_Model Width=1e-6\
   Cj=cj/2 \
   Cjsw=cjsw/2 \
   Length=sl-2*etchlc \
   Width=w-2*etchc

cap_pn:C1 PLUS 0  _M=mult
cap_pn:C2 MINUS 0 _M=mult

end gpdk180_polyres


; High Poly Resistor
;
; polyhreslw was a spectre phy_res - no equilvalent in ADS 2004A

model polyhreslw R_Model Rsh=352 Width=1e-6 Wdexp=1 Ldexp=1 TC1=3e-3 TC2=-2e-6

inline define gpdk180_polyhres ( PLUS MINUS)
parameters  sl=0.6e-6 w=0.6e-6 rend="UNDEF" rcont="UNDEF"
etchc=0
etchlc=0
mult=1
cj=1.33e-3
cjsw=3.15e-10
ADS_rend_6=15/(w*1e6)
ADS_rend_7=if (rend == "UNDEF") then ADS_rend_6 else rend endif


ADS_rcont_8=10/int(((w*1e6)-0.19999)/0.4)
ADS_rcont_9=if (rcont == "UNDEF") then ADS_rcont_8 else rcont endif


R:rcont1 PLUS PLUSHEAD R=ADS_rcont_9/2
R:rend1 PLUSHEAD PLUSEND R=ADS_rend_7/2
  polyhreslw:gpdk180_polyhres PLUSEND MINUSEND Length=sl Width=w
R:rend2 MINUSEND MINUSHEAD R=ADS_rend_7/2
R:rcont2 MINUSHEAD MINUS R=ADS_rcont_9/2

model cap_pn C_Model Width=1e-6\
   Cj=cj/2 \
   Cjsw=cjsw/2 \
   Length=sl-2*etchlc \
   Width=w-2*etchc

cap_pn:C1 PLUS 0 _M=mult
cap_pn:C2 MINUS 0 _M=mult

end gpdk180_polyhres

;


model nwellreslw R_Model Rsh=415 Width=1e-6 Wdexp=1 Ldexp=1 TC1=3e-3 TC2=-2e-6


inline define gpdk180_nwellres ( PLUS MINUS)
parameters  sl=2.0e-6 w=1.6e-6 rend="UNDEF" rcont="UNDEF"
etchc=0
etchlc=0
mult=1


ADS_rend_10=320/(w*1e6)
ADS_rend_11=if (rend == "UNDEF") then ADS_rend_10 else rend endif

ADS_rcont_12=15/int(((w*1e6)-1.199999)/0.4)
ADS_rcont_13=if (rcont == "UNDEF") then ADS_rcont_12 else rcont endif

R:rcont1 PLUS PLUSHEAD R=ADS_rcont_13/2
R:rend1 PLUSHEAD PLUSEND R=ADS_rend_11/2

nwellreslw:gpdk180_nwellres PLUSEND MINUSEND Length=sl Width=w
R:rend2 MINUSEND MINUSHEAD R=ADS_rend_11/2
R:rcont2 MINUSHEAD MINUS R=ADS_rcont_13/2

model diode_sn Diode \
	Tnom=27.0          
	

model diode_sn_sw Diode \
    	Tnom=27.0          
	
	

diode_sn:D1    0 PLUS _M=mult
diode_sn_sw:D2 0 PLUS  _M=mult
diode_sn:D3    0 MINUS _M=mult
diode_sn_sw:D4 0 MINUS _M=mult

end gpdk180_nwellres


model m1reslw R_Model Width=1e-6 Wdexp=1 Ldexp=1 Tnom=27 Rsh=0.01 TC1=3e-3 TC2=-2e-6
inline define gpdk180_m1res ( PLUS MINUS)
parameters  sl=  w= 
m1reslw:gpdk180_m1res PLUS MINUS Length=sl Width=w
end gpdk180_m1res

model m2reslw R_Model Width=1e-6 Wdexp=1 Ldexp=1 Tnom=27 Rsh=0.01 TC1=3e-3 TC2=-2e-6
inline define gpdk180_m2res ( PLUS MINUS)
parameters  sl=  w= 
m2reslw:gpdk180_m2res PLUS MINUS Length=sl Width=w
end gpdk180_m2res

model m3reslw R_Model Width=1e-6 Wdexp=1 Ldexp=1 Tnom=27 Rsh=0.01 TC1=3e-3 TC2=-2e-6
inline define gpdk180_m3res ( PLUS MINUS)
parameters  sl=  w= 
m3reslw:gpdk180_m3res PLUS MINUS Length=sl Width=w
end gpdk180_m3res

model m4reslw R_Model Width=1e-6 Wdexp=1 Ldexp=1 Tnom=27 Rsh=0.01 TC1=3e-3 TC2=-2e-6
inline define gpdk180_m4res ( PLUS MINUS)
parameters  sl=  w= 
m4reslw:gpdk180_m4res PLUS MINUS Length=sl Width=w
end gpdk180_m4res

model m5reslw R_Model Width=1e-6 Wdexp=1 Ldexp=1 Tnom=27 Rsh=0.01 TC1=3e-3 TC2=-2e-6
inline define gpdk180_m5res ( PLUS MINUS)
parameters  sl=  w= 
m5reslw:gpdk180_m5res PLUS MINUS Length=sl Width=w
end gpdk180_m5res

model m6reslw R_Model Width=1e-6 Wdexp=1 Ldexp=1 Tnom=27 Rsh=0.01 TC1=3e-3 TC2=-2e-6
inline define gpdk180_m6res ( PLUS MINUS)
parameters  sl=  w= 
m6reslw:gpdk180_m6res PLUS MINUS Length=sl Width=w
end gpdk180_m6res



#endif
;;endlibrary gpdk
;;Spectre Math Constants
#ifndef SPECTRE_MATH_CONSTANTS
;;Define a CPP variable so the constants will not be redefined
#define SPECTRE_MATH_CONSTANTS
M_E=e
M_LOG2E=1.44269504088896
M_LOG10E=log(e)
M_LN2=ln(2)
M_LN10=ln10
M_PI=pi
M_TWOPI=2*pi
M_PI_2=pi/2
M_PI_4=pi/4
M_1_PI=1/pi
M_2_PI=2/pi
M_2_SQRTPI=2/sqrt(pi)
M_SQRT1_2=sqrt(1/2)
M_DEGPERRAD=57.2957795130823208772
M_SQRT2=sqrt(2)
;End of Spectre Math Constants
#endif
;
;;Spectre Physical Constants
#ifndef SPECTRE_PHYSICAL_CONSTANTS
;;Define a CPP variable so the constants will not be redefined
#define SPECTRE_PHYSICAL_CONSTANTS
P_Q=qelectron
P_C=c0
P_K=boltzmann
P_H=planck
P_EPS0=e0
P_U0=u0
P_CELSIUS0=273.15
;End of Spectre Physical Constants
#endif
;
;Spectre boolean function replacements
#ifndef SPECTRE_BOOLEAN_EQUATIONS
;Define a value so the functions will not be included multiple times
#define SPECTRE_BOOLEAN_EQUATIONS
;Spectre Equals
ADS_SCS_EQ(x,y)=if (x == y) then 1 else 0 endif
;Spectre Not Equal
ADS_SCS_NEQ(x,y)=if (x != y) then 1 else 0 endif
;Spectre Less Than
ADS_SCS_LT(x,y)=if (x < y) then 1 else 0 endif
;Spectre Greater Than
ADS_SCS_GT(x,y)=if (x > y) then 1 else 0 endif
;Spectre Less Than or Equal To
ADS_SCS_LTE(x,y)=if (x <= y) then 1 else 0 endif
;Spectre Greater Than or Equal To
ADS_SCS_GTE(x,y)=if (x >= y) then 1 else 0 endif
;Spectre Trinary
ADS_SCS_TRINARY(z,x,y)=if (z == 1) then x else y endif
;End of the Spectre boolean function replacement block
#endif


