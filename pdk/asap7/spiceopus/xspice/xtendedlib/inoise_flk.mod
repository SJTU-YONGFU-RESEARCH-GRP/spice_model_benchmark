/* $Id: inoise_flk.mod v2017.03.01 MD $ */

# include <stdlib.h>
# include "inoise_flicker.h"

# define UU 1
# define QQ 2
# define YY 3
# define T1 4

void cm_inoise_flk(ARGS)
{
      
    int b;
    int *q;
    double *u;
    double *py;
    double y;
    double *t1;
    double time1;
    double t_next;

    b = 31; // number of random generators = number of octaves of 1/f law
            // b must be > 0 and < 32
            // in future implementations this variable should be internally
            // calculated or given as a model parameter
    
    if (INIT==1) { 
        /* Static storage allocation */
        cm_analog_alloc(UU,b*sizeof(double));       // geneators' sample array
        cm_analog_alloc(QQ,b*sizeof(int));          // generators' sample counter
        py = cm_analog_alloc(YY, sizeof(double));   // final noise sample
        t1 = cm_analog_alloc(T1, sizeof(double));   // last sample time
        *t1 = PARAM(t_generation_step);
	    cm_analog_set_temp_bkpt(PARAM(t_generation_step));
	    srand(PARAM(seed));
    }

    switch (ANALYSIS) {
    case TRANSIENT: /* Transient analysis */
	py = cm_analog_get_ptr(YY,0);
        t1 = cm_analog_get_ptr(T1,0);
        time1 = *t1;       
        if (T(1)<time1) {
            y = *py;
        } else {
	    t_next = T(1)+PARAM(t_generation_step);
	    *t1 = t_next;
            cm_analog_set_temp_bkpt(t_next);
            /* Retriving previous state and generate the new noise sample*/
            u = cm_analog_get_ptr(UU,0);
            q = cm_analog_get_ptr(QQ,0);
            y = ran1f(b, u, q);
            *py = y;
        } 
        OUTPUT(t_plus) = PARAM(i_peak)*y*16;
        OUTPUT(t_minus) = -PARAM(i_peak)*y*16; 
    }

}

/*
References:

https://people.sc.fsu.edu/~jburkardt/c_src/pink_noise/pink_noise.html
http://www.firstpr.com.au/dsp/pink-noise/allan-2/spectrum2.html

*/
