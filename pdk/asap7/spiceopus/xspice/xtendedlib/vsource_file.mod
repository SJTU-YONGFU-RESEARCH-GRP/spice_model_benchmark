/* $Id: vsource_file.mod v2017.10.26 FSG $ */

#include <stdlib.h>
#include <stdio.h>

void cm_vsource_file(ARGS)  
{
           double out,            /* analog voltage signal */
                  *tnext,         /* next breakpoint time */
                  *vnext,         /* next breakpoint voltage */
                  *vprev;         /* previous breakpoint voltage */
               int n;             /* auxiliar counter */
             FILE *infile;        /* input file pointer */
             char *filename,      /* input file name */
                  buffer[128];    /* input file buffer */
    
  filename = PARAM(fname);     /* Retrieving parameters */

  if (INIT==1) { /* Static storage allocation, file header and first breakpoint */

    tnext = malloc(sizeof(double));
    vnext = malloc(sizeof(double));
    vprev = malloc(sizeof(double));
    
    infile = fopen(filename,"r");
    if (infile!=NULL) {
      for (n=1;n<13;n=n+1) {
        if (fgets(buffer,128,infile)==NULL) {
          fclose(infile);
          break;
        }
      }
    } else { fclose(infile); }
    sscanf(buffer,"%*d %lf %lf",tnext,vnext);
    *vprev = *vnext;

    if (*tnext==0) { /* First breakpoint is at time = 0 !*/
      OUTPUT(out) = *vnext;
      if (fgets(buffer,128,infile)==NULL) {
        fclose(infile);
      } else { /* Second breakpoint */
        sscanf(buffer,"%*d %lf %lf",tnext,vnext);
      }
    }
      
    cm_analog_set_perm_bkpt(*tnext);
    STATIC_VAR(infile) = infile;
    STATIC_VAR(tnext) = tnext;
    STATIC_VAR(vnext) = vnext;
    STATIC_VAR(vprev) = vprev;
    
  } else {
    switch (ANALYSIS) {

      case TRANSIENT: /* Transient analysis */

        infile = STATIC_VAR(infile);  /* Retriving previous state */
        tnext = STATIC_VAR(tnext);  
        vnext = STATIC_VAR(vnext);
        vprev = STATIC_VAR(vprev);

        if (TIME == *tnext) { /* New sample */ 
          OUTPUT(out) = *vnext;
          *vprev = *vnext;
          if (fgets(buffer,128,infile)==NULL) {
            fclose(infile);
          } else {
            sscanf(buffer,"%*d %lf %lf",tnext,vnext);
            cm_analog_set_perm_bkpt(*tnext);
            STATIC_VAR(tnext) = tnext;
            STATIC_VAR(vnext) = vnext;
            STATIC_VAR(vprev) = vprev;
          }
        } else { /* Old sample */
          OUTPUT(out) = *vprev;
        }
     
        break;
    }
  }
}


