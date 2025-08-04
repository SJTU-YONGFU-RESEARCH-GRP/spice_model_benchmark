/* $Id: inoise_flicker.h v2017.03.01 MD $ */

# include <stdlib.h>
# include "inoise_flicker.h"

/*
    Auxiliary functions:
        ran1f -> ranh -> circular_delay 
*/

void circular_delay(int m, int *q)
{
    // Decrements the offset Q, When Q = - 1, it wraps to Q = M.
    *q = *q-1;
    if (*q<0) {*q = m;} 
    return;
}

double ranh(int d, double *u, int *q)
{
    // random generator with associated Q index array
    double y;

    if (d < 1) {d = 1;}
    y = *u; 			// Hold this sample for D calls.
    circular_delay(d-1,q); 	// Decrement Q and wrap mod D.
    if (*q == 0) 		// Every D calls, get a new U with zero mean.
    {
        *u = 2.0*(double)rand()/(double)(RAND_MAX)-1.0;
    }
    return y;
}

double ran1f(int b, double u[], int q[])
{
    int i;
    int j;
    double y;

    y = 0.0;
    j = 1;
    for (i = 0; i < b; i++)
    {
        y = y + ranh(j,u+i,q+i);
        j = j*2;
    }
    y = y/b;
    return y;
}
