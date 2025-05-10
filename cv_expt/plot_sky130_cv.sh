#!/bin/bash
ngspice -b cv_mos_sky130.cir
python3 plot_sky130_cv.py 