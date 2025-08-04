/* $Id: cfunc.tpl,v 1.1 91/03/18 19:01:04 bill Exp $ */
/*.......1.........2.........3.........4.........5.........6.........7.........8
================================================================================

FILE gain/cfunc.mod

Copyright 1991
Georgia Tech Research Corporation, Atlanta, Ga. 30332
All Rights Reserved

PROJECT A-8503-405
               

AUTHORS                      

    6 Jun 1991     Jeffrey P. Murray


MODIFICATIONS   

     2 Oct 1991    Jeffrey P. Murray
                                   

SUMMARY

    This file contains the model-specific routines used to
    functionally describe the frequency-domain gain source code model.


INTERFACES       

    FILE                 ROUTINE CALLED     

    N/A                  N/A                     


REFERENCED FILES

    Inputs from and outputs to ARGS structure.
                     

NON-STANDARD FEATURES

    NONE

===============================================================================*/

/*=== INCLUDE FILES ====================*/
#include <math.h>

                                      

/*=== CONSTANTS ========================*/




/*=== MACROS ===========================*/



  
/*=== LOCAL VARIABLES & TYPEDEFS =======*/                         


    
           
/*=== FUNCTION PROTOTYPE DEFINITIONS ===*/




                   
/*==============================================================================

FUNCTION void cm_gain()

AUTHORS                      

     2 Oct 1991     Jeffrey P. Murray

MODIFICATIONS   

    NONE

SUMMARY

    This function implements the frequency domain gain code model.

INTERFACES       

    FILE                 ROUTINE CALLED     

    N/A                  N/A


RETURNED VALUE
    
    Returns inputs and outputs via ARGS structure.

GLOBAL VARIABLES
    
    NONE

NON-STANDARD FEATURES

    NONE

==============================================================================*/

/*

Model structure:

R, L, G, C are per unit length. R and G can be frequency dependent. 

Lossy telegraph equation:

d               d
-- v(x,t) = - L -- i(x,t) - R i(x,t)
dx              dt 

d               d
-- i(x,t) = - c -- v(x,t) - G v(x,t)
dx              dt 


From lossy telegraph equation express PDE wrt x,t for v(x,t) and i(x,t). 
i(x,t) flows from left to right. Transform to frequency domain. 
  2 
 d
---- V = (R + j omega L) (G + j omega C) V
  2
dx

Equation for I is the same as for V. 

     2
Gamma  = (R + j omega L) (G + j omega C) 

  2   R + j omega L
Zk  = -------------
      G + j omega C
      

Gamma, Zk, and A are calculated as 

Gamma = sqrt(R + j omega L) sqrt(G + j omega C)

Zk = sqrt(R + j omega L) / sqrt(G + j omega C)

A = exp (-Gamma len)


Solution:

V(x) = Vfwd exp(-Gamma x) + Vrev exp(Gamma x)
I(x) = Ifwd exp(-Gamma x) + Irev exp(Gamma x)

d/dx both equations. 

Insert 

d
-- V = - j omega L I - R I
dx

d
-- I = - j omega C V - G V
dx 


V(x) = - Vfwd Gamma exp(-Gamma x) + Vrev Gamma exp(Gamma x) = - (j omega L + R) I 
     = - (j omega L + R) (Ifwd + Irev)
I(x) = - Ifwd Gamma exp(-Gamma x) + Irev Gamma exp(Gamma x) = - (j omega C + G) V
     = - (j omega C + G) (Vfwd + Vrev)
     
Vfwd and Vrev don't mix, same goes for Ifwd and Irev. Calculate connectiuon between 
Vfwd and Ifwd, Vrev and Irev. 

Vfwd =   Zk Ifwd
Vref = - Zk Irev


 i1         i2
->--       --<-
+             +
V1           V2
-             -
----       ----

V1 = Vfwd + Vrev
I1 = 1/Zk (Vfwd - Vrev)

V2 = A Vfwd + A^-1 Vrev
I2 = 1/Zk (A Vfwd - A^-1 Vrev)


Express Vfwd and Vrev from first and second pair of equations. 

  Vrev =    V1 - Zk I1  = A (V2 + Zk I2)
A Vfwd = A (V1 + Zk I1) =    V2 - Zk I2


Two internal nodes (I1 and I2). KCL at those nodes: 

   V1 - Zk I1  = A (V2 + Zk I2)
A (V1 + Zk I1) =    V2 - Zk I2

Use a VCCS at line ports to transfer internal node voltages which represent port currents. 

*/

#define PI 3.14159265358979323846

void cm_complex_magphi(Mif_Complex_t x, double *mag, double *arg) {
	*mag=sqrt(x.real*x.real+x.imag*x.imag);
	if (x.imag==0) {
		if (x.real>0) {
			*arg=PI/2;
		} else if (x.real<0) {
			*arg=-PI/2;
		} else {
			*arg=0.0;
		}
	} else {
		*arg=atan(x.imag/x.real);
		if (x.real<0) {
			*arg=*arg+PI;
		}
	}
}

Mif_Complex_t cm_complex_sqrt(Mif_Complex_t x) {
	Mif_Complex_t result;
	double mag, arg;
	
	cm_complex_magphi(x, &mag, &arg);
	mag=sqrt(mag);
	arg=arg/2;
	result.real=mag*cos(arg);
	result.imag=mag*sin(arg);
	
	return result;
}

Mif_Complex_t cm_complex_exp(Mif_Complex_t x) {
	Mif_Complex_t result;
	double mag;
	
	mag=exp(x.real);
	result.real=mag*cos(x.imag);
	result.imag=mag*sin(x.imag);
	
	return result;
}



/*=== CM_FDTABGAIN ROUTINE ===*/
                                                   

void cm_fdtabltra(ARGS)   /* structure holding parms, inputs, outputs, etc.     */
{
    Mif_Complex_t rval, gval, a1, a2, rjwl, gjwc, Gamma, Zk, GammaL, A, AZk, one, zero, negone;
    int nftable;
    double om1, om2;
    double findex;
    int index;
    double omega, omegamin, omegamax; 
    int i, j, found;

    if(ANALYSIS != MIF_AC) {
        OUTPUT(i1) = 0;
        PARTIAL(i1,p1) = 0;
        PARTIAL(i1,p2) = 0;
		PARTIAL(i1,i1) = 1;
        PARTIAL(i1,i2) = 0;
        OUTPUT(i2) = 0;
        PARTIAL(i2,p1) = 0;
        PARTIAL(i2,p2) = 0;
		PARTIAL(i2,i1) = 0;
        PARTIAL(i2,i2) = 1;
        OUTPUT(p1) = 0;
        PARTIAL(p1,p1) = 0;
        PARTIAL(p1,p2) = 0;
		PARTIAL(p1,i1) = 0;
        PARTIAL(p1,i2) = 0;
        OUTPUT(p2) = 0;
        PARTIAL(p2,p1) = 0;
        PARTIAL(p2,p2) = 0;
		PARTIAL(p2,i1) = 0;
        PARTIAL(p2,i2) = 0;
    }
    else {
		// Get frequency
		omega=RAD_FREQ;
		
		// Find index
		nftable=PARAM_SIZE(omegatab);
		omegamin=PARAM(omegatab[0]);
		j=nftable-1;
		omegamax=PARAM(omegatab[j]);
		found=0;
		
		// Look it up in freq table
		for(i=0;i<nftable-1;i++) {
			om1=PARAM(omegatab[i]);
			j=i+1;
			om2=PARAM(omegatab[j]);
			if (om1<=omega && om2>=omega) {
				findex=(omega-om1)/(om2-om1);
				index=i;
				found=1;
				break;
			}
		}
		
		// Default if no index found
		if (!found) {
			if (omega<omegamin) {
				// Extrapolate below omegamin
				index=0;
				j=index+1;
				om1=PARAM(omegatab[index]);
				om2=PARAM(omegatab[j]);
				if (om1!=om2) {
					// Extrapolate
					findex=(omega-om1)/(om2-om1); 
				} else {
					// Extrapolation not possible, use value at omegamin
					findex=0.0;
				}
			} else {
				// Extrapolate above omegamax
				index=PARAM_SIZE(omegatab)-2;
				j=index+1;
				om1=PARAM(omegatab[index]);
				om2=PARAM(omegatab[j]);
				if (om1!=om2) {
					// Extrapolate
					findex=(omega-om1)/(om2-om1); 
				} else {
					// Extrapolation not possible, use value at omegamax
					findex=1.0;
				}
			}
		} 
		
		// Get R and G
		j=index+1;
		
		// BAD: if r has a smaller length than omegatab
		if (PARAM_SIZE(r)<nftable) {
			// Uh-oh, default to maximal index of r
			int i;
			i=PARAM_SIZE(r)-1;
			rval=PARAM(r[i]);
		} else {
			a1=PARAM(r[index]);
			a2=PARAM(r[j]);
			rval.real=a1.real+(a2.real-a1.real)*findex;
			rval.imag=a1.imag+(a2.imag-a1.imag)*findex;
		}
		
		// BAD: if g has a smaller length than omegatab
		if (PARAM_SIZE(g)<nftable) {
			// Uh-oh, default to maximal index of g
			int i;
			i=PARAM_SIZE(g)-1;
			gval=PARAM(g[i]);
		} else {
			a1=PARAM(g[index]);
			a2=PARAM(g[j]);
			gval.real=a1.real+(a2.real-a1.real)*findex;
			gval.imag=a1.imag+(a2.imag-a1.imag)*findex;
		}
		
		// Calculate R+jwL
		rjwl.real=rval.real;
		rjwl.imag=rval.imag+omega*PARAM(l);
		
		// Calculate G+jwC
		gjwc.real=gval.real;
		gjwc.imag=gval.imag+omega*PARAM(c);
		
		// Square root of rjwl and gjwc
		rjwl=cm_complex_sqrt(rjwl);
		gjwc=cm_complex_sqrt(gjwc);
		
		// Calculate Gamma and Zk
		Gamma=cm_complex_multiply(rjwl, gjwc);
		Zk=cm_complex_divide(rjwl, gjwc);
		
		// Calculate A
		GammaL.real=-Gamma.real*PARAM(len);
		GammaL.imag=-Gamma.imag*PARAM(len);
		A=cm_complex_exp(GammaL);
		
		// Calculate AZk
		AZk=cm_complex_multiply(A, Zk);
		
		// One and zero
		one.real=1.0;
		one.imag=0.0;
		zero.real=0.0;
		zero.imag=0.0;
		negone.real=-1.0;
		negone.imag=0.0;
		
		// AC gain
		AC_GAIN(p1, p1)=zero;
		AC_GAIN(p1, p2)=zero;
		AC_GAIN(p1, i1)=one;
		AC_GAIN(p1, i2)=zero;
		
		AC_GAIN(p2, p1)=zero;
		AC_GAIN(p2, p2)=zero;
		AC_GAIN(p2, i1)=zero;
		AC_GAIN(p2, i2)=one; 
		
		AC_GAIN(i1, p1)=negone; 
		AC_GAIN(i1, i1)=Zk;
		AC_GAIN(i1, p2)=A;
		AC_GAIN(i1, i2)=AZk;
		
		AC_GAIN(i2, p2)=negone;
		AC_GAIN(i2, i2)=Zk;
		AC_GAIN(i2, p1)=A;
		AC_GAIN(i2, i1)=AZk;
    }
}
