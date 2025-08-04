/* $Id: zinteg2lim.mod v2014.04.21 FSG $ */

#include <math.h>

#define SAMPLING_INTEGRATION 1
#define HOLDING 0
#define sign(x) (( x > 0 ) - ( x < 0 ))

void cm_zinteg2sc(ARGS)  
{
           double inp,       /* analog voltage input */
                  out,       /* analog voltage output */
                  *inp_mem,  /* sampled input */
                  *out_mem,  /* integrated output */
                  *time_mem, /* previous integration time */
                  delta_v,   /* output voltage increment */
                  delta_t,   /* time increment */
                  out_ic,    /* output initial condition */
                  kgain,     /* input gain factor */
                  out_min,   /* minimum output limit */
                  out_max,   /* maximum output limit */
                  G,         /* open loop gain */
                  GBW,       /* gain bandwidth product */
                  SR,        /* slew-rate */
                  tau;       /* settling time constant */
  Digital_State_t clk,       /* current clock level */
                  *clk_mem,  /* previous clock level*/
                  pos_edge;  /* L->H edge clock output? */
              int action;    /* action type */
             char *error;    /* error message */ 
    
  inp = INPUT(inp);            /* Retriving input values */
  clk = INPUT_STATE(clk);
  kgain = PARAM(kgain);        /* Retriving parameters */  
  pos_edge = PARAM(pos_edge);
  out_ic = PARAM(out_ic);
  out_min = PARAM(out_min);
  out_max = PARAM(out_max);
  G = PARAM(G);
  GBW = PARAM(GBW);
  SR = PARAM(SR);
  tau = 1/(2*M_PI*GBW);

  if (INIT==1) { /* Static storage allocation and checking */

    cm_analog_alloc(1,sizeof(double));
    cm_analog_alloc(2,sizeof(double));
    cm_analog_alloc(3,sizeof(double));
    cm_event_alloc(4,sizeof(Digital_State_t));
    
    if (out_min>out_max) {
      error = "\n*** zinteg2lim error: out_min>out_max !\n";
      cm_message_send(error);
    }
    if ((out_ic>out_max)||(out_ic<out_min)) {
      error = "\n*** zinteg2lim error: out_ic exceeds [out_min,out_max] !\n";
      cm_message_send(error);
    }

  }

  switch (ANALYSIS) {

    case TRANSIENT: /* Transient analysis */

      inp_mem = cm_analog_get_ptr(1,0); /* Retriving previous state */
      out_mem = cm_analog_get_ptr(2,0);
      time_mem = cm_analog_get_ptr(3,0);
      clk_mem = cm_event_get_ptr(4,0);

      if (TIME==0) { /* Initialization */

        *inp_mem = inp;
        *out_mem = out_ic;
        *time_mem = 0;
        out = out_ic;

      } else { /* Regular operation */

        if ((*clk_mem==ONE)&&(clk==ZERO)) { /* Negative clk edge */
          if (pos_edge==FALSE)               
            action = SAMPLING_INTEGRATION;
          
        } else {
          if ((*clk_mem==ZERO)&&(clk==ONE)) { /* Positive clk edge */
            if (pos_edge==TRUE)                
              action = SAMPLING_INTEGRATION;
            
          } else {  /* No clock edge */ 
              action = HOLDING;
          }
        }

        switch (action) {
           case SAMPLING_INTEGRATION: /* Sampling and integration */
            *inp_mem = inp;            
            delta_t = (TIME-*time_mem)/2;

            /* finite open loop gain effect */
            out = (1/(kgain/(1+G)+1))*(*out_mem)+(kgain/(1+1/G+kgain/G))*(*inp_mem);
            delta_v = out-*out_mem;

            /********** TO BE COMPLETED **********/

            if (out<out_min) { out = out_min; } /* Limiter */
            if (out>out_max) { out = out_max; }

            *out_mem = out;
            *time_mem = TIME;
            break;
          case HOLDING:    /* Holding */
            out = *out_mem;
        }
      } 

      *clk_mem = clk;
      OUTPUT(out) = out;

      break;

    case DC:        /* DC analysis */
      OUTPUT(out) = out_ic;
      break;

    default:        /* Analysis not supported */
      error = "\n*** zinteg2sc error: analysis not supported !\n";
      cm_message_send(error);
  }
}

