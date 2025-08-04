/* $Id: dscope_step.mod v2017.10.26 FSG $ */

#include <stdlib.h>
#include <stdio.h>

#define SAMPLING_WRITING 1
#define NONE 0

void cm_dscope_step(ARGS)  
{
  Digital_State_t inp;            /* digital input signal */

           double tstep,          /* time step */
                  nsamp,          /* number of samples */
                  *ncount,        /* sample counter */
                  *tnext;         /* next break point */
              int action;         /* action type */
             FILE *outfile;       /* output file pointer */
             char *filename;      /* output file name */
    
  inp = INPUT_STATE(inp);     /* Retriving input values */
  tstep = PARAM(tstep);       /* Retrieving parameters */
  nsamp = PARAM(nsamp);
  filename = PARAM(fname);

  if (INIT==1) { /* Static storage allocation, file header and first sample */

    ncount = malloc(sizeof(double));
    tnext = malloc(sizeof(double));
    
    outfile = fopen(filename,"w");
    if (outfile!=NULL) {
      fprintf(outfile,"Title: %s\n",filename);
      fprintf(outfile,"Date: unknown\n");
      fprintf(outfile,"Plotname: Transient Analysis\n");
      fprintf(outfile,"Flags: real\n");
      fprintf(outfile,"Sckt. naming: from bottom to top\n");
      fprintf(outfile,"No. Variables: 2\n");
      fprintf(outfile,"No. Points: %.0f\n",nsamp);
      fprintf(outfile,"Variables:\n");
      fprintf(outfile,"\t0\ttime\ttime\n");
      fprintf(outfile,"\t1\tvout\tvoltage\n");
      fprintf(outfile,"Values:\n");
      fprintf(outfile,"\t%.0f\t%.15e\t%d\n",*ncount,TIME,inp);
      fclose(outfile);
    }

    *ncount = 1;
    *tnext = tstep;
    STATIC_VAR(ncount) = ncount;
    STATIC_VAR(tnext) = tnext;
    cm_event_queue(*tnext);

  } else {
    switch (ANALYSIS) {

      case TRANSIENT: /* Transient analysis */

        ncount = STATIC_VAR(ncount);   /* Retriving previous state */
        tnext = STATIC_VAR(tnext);

        if (TIME == *tnext) { /* Multiple of time step */
          action = SAMPLING_WRITING;
        } else { /* No operation */
          action = NONE;
        }
        
        if ((action==SAMPLING_WRITING)&&(*ncount<nsamp)) { /* Writing action */
            outfile = fopen(filename,"a");
            if (outfile!=NULL) {
              fprintf(outfile,"\t%.0f\t%.15e\t%d\n",*ncount,TIME,inp);
              fclose(outfile);
              *ncount = *ncount+1;
              *tnext = *tnext+tstep;
              cm_event_queue(*tnext);
            }
        }

        STATIC_VAR(ncount) = ncount;
        STATIC_VAR(tnext) = tnext;
     
        break;
    }
  }
}


