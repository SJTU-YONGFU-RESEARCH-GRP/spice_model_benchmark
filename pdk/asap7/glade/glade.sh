#! /bin/bash

#export GLADE_USE_OPENGL=NO
export GLADE_HOME=path_to_glade
export PATH=${GLADE_HOME}/bin:${PATH}
export LD_LIBRARY_PATH=${GLADE_HOME}/lib:${LD_LIBRARY_PATH}
export PYTHONPATH=.:./pcells:./verification:${GLADE_HOME}/bin:${PYTHONPATH}
export GLADE_LOGFILE_DIR=.
export GLADE_DRC_WORK_DIR=.
export GLADE_DRC_FILE=./verification/cnm25drc.py
export GLADE_EXT_FILE=./verification/cnm25xtr_lvs.py
export GLADE_FASTCAP_WORK_DIR=.
#export GLADE_NO_DELETE_TMPFILES=1

rm ./glade*.log
glade -script ./glade_init.py &

