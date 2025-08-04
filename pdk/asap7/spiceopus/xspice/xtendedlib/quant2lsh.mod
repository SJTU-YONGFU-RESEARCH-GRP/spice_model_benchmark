/* $Id: quant2lsh.mod v2014.01.27 FSG $ */

#define SAMPLING_QUANTIZATION 1
#define HOLDING 0

void cm_quant2lsh(ARGS)  
{
           double inp,      /* analog voltage input */
                  *inp_mem, /* sampled input */
                  inp_th,   /* input threshold */
                  t_rise,   /* output rise time */
                  t_fall;   /* output fall time */
                  
  Digital_State_t out,      /* digital output */
                  *out_mem, /* holded output */ 
                  clk,      /* current clock level */
                  *clk_mem, /* previous clock level*/
                  out_ic,   /* output initial condition */
                  pos_edge; /* L->H edge clock output? */
              int action;   /* action type */
             char *error;   /* error message */ 
    
  inp = INPUT(inp);            /* Retriving input values */
  clk = INPUT_STATE(clk);
  inp_th = PARAM(inp_th);      /* Retrieving parameters */
  t_rise = PARAM(t_rise);
  t_fall = PARAM(t_fall);
  out_ic = PARAM(out_ic);  
  pos_edge = PARAM(pos_edge);

  if (INIT==1) { /* Static storage allocation and checking */

    cm_analog_alloc(1,sizeof(double));
    cm_event_alloc(2,sizeof(Digital_State_t));
    cm_event_alloc(3,sizeof(Digital_State_t));


    if (t_rise<1e-12) {
      error = "\n*** quant2lsh error: t_rise<1ps !\n";
      cm_message_send(error);
    }
    if (t_fall<1e-12) {
      error = "\n*** quant2lsh error: t_fall<1ps !\n";
      cm_message_send(error);
    }

  }

  switch (ANALYSIS) {

    case TRANSIENT: /* Transient analysis */

      inp_mem = cm_analog_get_ptr(1,0); /* Retriving previous state */
      out_mem = cm_event_get_ptr(2,0); 
      clk_mem = cm_event_get_ptr(3,0);

      if (TIME==0) { /* Initialization */

        *inp_mem = inp;
        *out_mem = out_ic;
        out = out_ic;
        OUTPUT_CHANGED(out) = TRUE;
        OUTPUT_STATE(out) = out;
        OUTPUT_STRENGTH(out) = STRONG;
 
      } else { /* Regular operation */

        if ((*clk_mem==ONE)&&(clk==ZERO)) { /* Negative clk edge */
          if (pos_edge==FALSE)
          {              
            action = SAMPLING_QUANTIZATION;
          }
        } else {
          if ((*clk_mem==ZERO)&&(clk==ONE)) { /* Positive clk edge */
            if (pos_edge==TRUE)
            {               
              action = SAMPLING_QUANTIZATION;
            }
          } else {  /* No clock edge */ 
              action = HOLDING;
          }
        }  

        switch (action) {
          case SAMPLING_QUANTIZATION: /* Quantization action */
            OUTPUT_CHANGED(out) = TRUE;
            *inp_mem = inp;
            if (*inp_mem>inp_th) {
              out = ONE;
              OUTPUT_DELAY(out) = t_rise;
            } else {
              out = ZERO;
              OUTPUT_DELAY(out) = t_fall;
            }
            OUTPUT_STATE(out) = out;
            OUTPUT_STRENGTH(out) = STRONG;
            *out_mem = out;
            break;
          case HOLDING:            /* Holding action */
            OUTPUT_CHANGED(out) = FALSE;
        }
      }

      *clk_mem = clk;

      break;

    case DC:        /* DC analysis */
      OUTPUT_STATE(out) = out_ic;
      OUTPUT_STRENGTH(out) = STRONG;
      break;

    default:        /* Analysis not supported */
      error = "\n*** quant2lsh error: analysis not supported !\n";
      cm_message_send(error);
  }
}

