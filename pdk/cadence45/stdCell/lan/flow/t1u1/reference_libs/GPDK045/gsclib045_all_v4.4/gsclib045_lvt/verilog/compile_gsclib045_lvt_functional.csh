#!/bin/csh -f
#
# Functionality: Run "ncvlog" for creating the 'functional' view
# 
# Prerequisite: (a) Verilog file (Eg: slow.v )
#               (b) cds.lib file (for define library, Eg: gsclib045_lvt)
#
# Syntax: compile_gsclib045_lvt_functional.csh
#---------------------------------------------------------------------------------
#
set verilogFile = slow_vdd1v0_basicCells_lvt.v
set libName     = gsclib045_lvt
set libPath     = $PROJECT/LIBS/GPDK045/gsclib045/oa22
set logfile     = ./compile_${libName}_functional.log
#

echo "Start: `date`"
if ( ! -e `which verilog | awk -F" " '{print $1}'` ) then
   echo "Error: The executable 'verilog' is not found (Eg: which verilog).";  exit (1)
endif
if ( ! -e  ${libPath}/../verilog/$verilogFile ) then
   echo "Error: The '${libPath}/../verilog/${verilogFile}' is not found.";  exit (1)
endif
#
echo "(a) Delete the existing Verilog pak file"
find $PROJECT/LIBS/GPDK045/gsclib045/oa22/${libName} -name "*.pak" | xargs \rm -f
echo "(b) Delete all existing '${libName}/<allCells>functional' view"
find $PROJECT/LIBS/GPDK045/gsclib045/oa22/${libName} -name "functional" | xargs rm -rf
#---------------------------------------------
echo "(c) Run ncvlog for creating: ${libName}/<allCells>/functional "
echo "                             (Link to: ${verilogFile})"
ncvlog \
 -use5x \
 -nocopyright \
 -work $libName \
 -view functional \
 ${libPath}/../verilog/$verilogFile > $logfile
#--------------------------------------------
echo "Done: `date`"
echo "FYI: Please review the log file for any warnings/errors."
if (-f $logfile ) nedit $logfile &
#---------------------- End of file ----------------------------------
