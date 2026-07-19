#!/bin/bash
# Spectre environment setup
export SPECTRE_HOME=/eda/cadence/SPECTRE241

# Include ALL lib/64bit subdirectories for runtime dependencies
LIB64_DIRS=$(find $SPECTRE_HOME/tools.lnx86 -maxdepth 4 -type d -name "64bit" 2>/dev/null | tr '\n' ':')
LIB_DIRS=$(find $SPECTRE_HOME/tools.lnx86 -maxdepth 3 -type d -name "lib" 2>/dev/null | tr '\n' ':')
TP_DIRS=$(find $SPECTRE_HOME/tools.lnx86/TPtools -maxdepth 3 -type d -name "lib64" 2>/dev/null | tr '\n' ':')

export LD_LIBRARY_PATH="${LIB64_DIRS}${LIB_DIRS}${TP_DIRS}${LD_LIBRARY_PATH}"
export PATH=$SPECTRE_HOME/tools.lnx86/spectre/bin/64bit:$SPECTRE_HOME/tools.lnx86/spectre/bin:$SPECTRE_HOME/bin:$PATH
