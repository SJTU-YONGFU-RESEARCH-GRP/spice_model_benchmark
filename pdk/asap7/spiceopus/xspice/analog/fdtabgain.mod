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


/*=== CM_FDTABGAIN ROUTINE ===*/

#define PI 3.14159265358979323846                                                   

void cm_fdtabgain(ARGS)   /* structure holding parms, inputs, outputs, etc.     */
{
    Mif_Complex_t ac_gain, cx1, cx2;
    int nftable;
    double om1, om2;
    double findex;
    int index;
    double a1, a2;
    double omega, omegamin, omegamax; 
    int i, j, found;
    int logscale;

    if(ANALYSIS != MIF_AC) {
        OUTPUT(out) = 0.0;
        PARTIAL(out,in) = 1.0;
    }
    else {
		// Get frequency
		omega=RAD_FREQ;
		
		// Log scale
		if (PARAM(logscale))
			logscale=1;
		else
			logscale=0;
		
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
				if (!logscale) {
					findex=(omega-om1)/(om2-om1);
				} else {
					findex=log(omega/om1)/log(om2/om1);
				}
				index=i;
				found=1;
				break;
			}
		}
		
		// Default if no index found
		if (!found) {
			if (omega<omegamin) {
				// No extrapolation
				/*
				// Extrapolate below omegamin
				index=0;
				j=index+1;
				om1=PARAM(omegatab[index]);
				om2=PARAM(omegatab[j]);
				if (om1!=om2) {
					// Extrapolate
					if (!logscale) {
						findex=(omega-om1)/(om2-om1); 
					} else {
						findex=log(omega/om1)/log(om2/om1);
					}
				} else {
					// Extrapolation not possible, use value at omegamin
					findex=0.0;
				}
				*/
				index=0;
				findex=0.0;
			} else {
				// No extrapolation
				/*
				// Extrapolate above omegamax
				index=PARAM_SIZE(omegatab)-2;
				j=index+1;
				om1=PARAM(omegatab[index]);
				om2=PARAM(omegatab[j]);
				if (om1!=om2) {
					// Extrapolate
					if (!logscale) {
						findex=(omega-om1)/(om2-om1); 
					} else {
						findex=log(omega/om1)/log(om2/om1);
					}
				} else {
					// Extrapolation not possible, use value at omegamax
					findex=1.0;
				}
				*/
				index=PARAM_SIZE(omegatab)-2;
				findex=1.0;
			}
		} 
		
		// Do we have a cxgaintab
		if (!PARAM_NULL(cxmagtab)) {
			// Interpolate complex gain
			
			if (PARAM_SIZE(cxmagtab)<nftable) {
				// Uh-oh, default to maximal index of cxmagtab
				index=PARAM_SIZE(cxmagtab)-2;
				findex=1.0;
			}
			
			j=index+1;
			cx1=PARAM(cxmagtab[index]);
			cx2=PARAM(cxmagtab[j]);
			
			ac_gain=cm_complex_subtract(cx2, cx1);
			ac_gain.real*=findex;
			ac_gain.imag*=findex;
			ac_gain=cm_complex_add(ac_gain, cx1);
		} else {
			double rmag, rphase;
			
			// Interpolate magnitude
			if (!PARAM_NULL(magtab)) {
				if (PARAM_SIZE(magtab)<nftable) {
					// Uh-oh, default to maximal index of magtab
					index=PARAM_SIZE(magtab)-2;
					findex=1.0;
				}
				
				j=index+1;
				a1=PARAM(magtab[index]);
				a2=PARAM(magtab[j]);
				rmag=(a2-a1)*findex+a1;
			} else if (!PARAM_NULL(dbtab)) {
				if (PARAM_SIZE(dbtab)<nftable) {
					// Uh-oh, default to maximal index of dbtab
					index=PARAM_SIZE(dbtab)-2;
					findex=1.0;
				}
				
				j=index+1;
				a1=PARAM(dbtab[index]);
				a2=PARAM(dbtab[j]);
				rmag=pow(10.0, ((a2-a1)*findex+a1)/20.0);
			} else {
				// Fixed gain of 1.0
				rmag=1.0;
			}
			
			// Interpolate phase
			if (!PARAM_NULL(degtab)) {
				if (PARAM_SIZE(degtab)<nftable) {
					// Uh-oh, default to maximal index of degtab
					index=PARAM_SIZE(degtab)-2;
					findex=1.0;
				}
				
				j=index+1;
				a1=PARAM(degtab[index]);
				a2=PARAM(degtab[j]);
				rphase=((a2-a1)*findex+a1)*PI/180.0;
			} else {
				// Fixed phase of 0.0
				rphase=0.0;
			}
			
			// AC gain
			ac_gain.real=rmag*cos(rphase);
			ac_gain.imag=rmag*sin(rphase);
		}
		
		// Set interpolated gain
        AC_GAIN(out,in) = ac_gain;
		
    }
}
