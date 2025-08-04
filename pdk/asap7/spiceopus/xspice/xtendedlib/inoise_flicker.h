/* $Id: inoise_flicker.h v2017.03.01 MD $ */

# include <stdlib.h>

/*
    Auxiliary functions:
        ran1f -> ranh -> circular_delay 
*/

void circular_delay(int m, int *q);
double ranh(int d, double *u, int *q);
double ran1f(int b, double u[], int q[]);
