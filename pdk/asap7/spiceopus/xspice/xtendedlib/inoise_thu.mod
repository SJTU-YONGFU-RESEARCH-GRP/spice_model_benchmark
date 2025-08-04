/* $Id: inoise_thu.mod v2017.03.01 MD $ */

# include <stdlib.h>

# define M1 1
# define T1 2

void cm_inoise_thu(ARGS)
{
    
    double *py;
    double y;
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
            y = 2.0*(double)rand()/(double)(RAND_MAX)-1.0;
            *py = y;
        } 
        OUTPUT(t_plus) = PARAM(i_peak)*y;
        OUTPUT(t_minus) = -PARAM(i_peak)*y; 
    }
     
} 
