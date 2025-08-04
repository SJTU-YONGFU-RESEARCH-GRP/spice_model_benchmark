/* $Id: inoise_thn.mod v2017.03.01 MD $ */

# include <stdlib.h>
# include <math.h>
# ifndef M_TWO_PI
# define M_TWO_PI 6.283185307179586
# endif
# define M1 1
# define T1 2

void cm_inoise_thn(ARGS)
{
    
    double *py;
    double y;
    double yu;
    double yv;
    double *t1;
    double time1;
    double t_next;

    if(INIT==1) {
        py = cm_analog_alloc(M1, sizeof(double));
        t1 = cm_analog_alloc(T1, sizeof(double));
        *t1 = PARAM(t_generation_step);
	cm_analog_set_temp_bkpt(PARAM(t_generation_step));
	srand(PARAM(seed));
    }

    switch (ANALYSIS) {
    case TRANSIENT: 			/* Transient analysis */
	py = cm_analog_get_ptr(M1,0);
        t1 = cm_analog_get_ptr(T1,0);
        time1 = *t1;
        if (T(1)<time1) {
            y = *py;
        } else {
	    t_next = T(1)+PARAM(t_generation_step);
	    *t1 = t_next;
            cm_analog_set_temp_bkpt(t_next);
	    /* Box-Muller method: */
        yu = (rand()+1.0)/(RAND_MAX+1.0); /* uniform distribution, (0, 1] */
        yv = (rand()+1.0)/(RAND_MAX+1.0);
	    y = sqrt(-2*log(yu))*cos(M_TWO_PI*yv);
            *py = y;
        } 
        OUTPUT(t_plus) = PARAM(i_sigma)*y;
        OUTPUT(t_minus) = -PARAM(i_sigma)*y; 
    }
     

} 

/* References:

https://en.wikipedia.org/wiki/Normal_distribution#Generating_values_from_normal_distribution
http://people.sc.fsu.edu/~jburkardt/c_src/normal/normal.html
http://rosettacode.org/wiki/Random_numbers#C

*/
