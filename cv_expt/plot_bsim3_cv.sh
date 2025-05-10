#!/bin/bash
ngspice -b cv_mos_bsim3.cir
python3 plot_bsim3_cv.py 