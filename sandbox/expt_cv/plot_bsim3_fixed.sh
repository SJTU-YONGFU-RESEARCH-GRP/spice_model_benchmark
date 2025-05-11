#!/bin/bash
ngspice -b cv_mos_bsim3_fixed.cir
python3 plot_bsim3_fixed.py 