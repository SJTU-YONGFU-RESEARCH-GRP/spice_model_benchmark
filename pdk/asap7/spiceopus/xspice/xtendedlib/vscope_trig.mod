/* $Id: vscope_trig.mod v2017.10.26 FSG $ */

#include <stdlib.h>
#include <stdio.h>

#define SAMPLING_WRITING 1
#define NONE 0

void cm_vscope_trig(ARGS)  
{
  Digital_State_t strb,           /* digital strobe */
                  *strb_mem,      /* previous strobe level */
                  pos_edge;       /* L->H edge strobe? */

           double inp,            /* analog voltage signal */
                  nsamp,          /* number of samples */
                  *ncount;        /* sample counter */
              int action;         /* action type */
             FILE *outfile;       /* output file pointer */
             char *filename;      /* output file name */
    
  inp = INPUT(inp);           /* Retriving input values */
  strb = INPUT_STATE(strb);
  pos_edge = PARAM(pos_edge); /* Retrieving parameters */
  nsamp = PARAM(nsamp);
  filename = PARAM(fname);

  if (INIT==1) { /* Static storage allocation and file header */

    cm_event_alloc(1,sizeof(Digital_State_t));
    ncount = malloc(sizeof(double));
    STATIC_VAR(ncount) = ncount;
    
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
      fclose(outfile);
    }

  } else {
    switch (ANALYSIS) {

      case TRANSIENT: /* Transient analysis */

        strb_mem = cm_event_get_ptr(1,0); /* Retriving previous state */
        ncount = STATIC_VAR(ncount);

        if (TIME==0) { /* Initialization */

          *strb_mem = strb;
          *ncount = 0;
 
        } else { /* Regular operation */

          if ((*strb_mem==ONE)&&(strb==ZERO)) { /* Negative strobe edge */
            if (pos_edge==FALSE)
            {              
              action = SAMPLING_WRITING;
            }
          } else {
            if ((*strb_mem==ZERO)&&(strb==ONE)) { /* Positive strobe edge */
              if (pos_edge==TRUE)
              {               
                action = SAMPLING_WRITING;
              }
            } else {  /* No strobe edge */ 
                action = NONE;
            }
          }  
          if ((action==SAMPLING_WRITING)&&(*ncount<nsamp)) { /* Writing action */
            outfile = fopen(filename,"a");
            if (outfile!=NULL) {
              fprintf(outfile,"\t%.0f\t%.15e\t%.15e\n",*ncount,TIME,inp);
              fclose(outfile);
              *ncount = *ncount+1;
            }
          }
          *strb_mem = strb;
          STATIC_VAR(ncount) = ncount;
        }
        break;
    }
  }
}

