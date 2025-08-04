#! /bin/tcsh -f
# Fucntionality:  Combine <cellName>.cdl into a single file
# Usage: gsclib045_cdl_cat.csh <libDirName>
# -----------------------------------------------------
#
if ( "$1" == "" || ! -d ./$1 ) then
   echo "Error: Invalid argument '$1'"
   exit 1
endif
#  
# Set output file:   
set outputFilePGcdl   = $1.cdl # With supply pins on subckt line.
set outputFilePGspi   = $1.spi # With supply pins on subckt line and '*.NETEXPR' included
#
echo "FYI: Start (`date`)"
if (-f $outputFilePGcdl ) \rm $outputFilePGcdl
if (-f $outputFilePGspi ) \rm $outputFilePGspi

# Generate a cell list (from .cdl files in specified dir):
\ls $1/*.cdl | sort | sed -e "/^$1\/_gsclib045_/d" -e "/^temp/d" > ./temp_cellList_$1.txt

# Create file header into the combined file:
head -9 `head -1 ./temp_cellList_$1.txt` | sed -e "/^\* Top Cell Name\:/d" > ./$outputFilePGcdl
head -9 `head -1 ./temp_cellList_$1.txt` | sed -e "/^\* Top Cell Name\:/d" > ./$outputFilePGspi

# ----------------------------------------------------------------------------------------------
#Concaternate CDL files:
foreach cdlFile (`cat ./temp_cellList_$1.txt`)
        sed  /\.SUBCKT/,/\.ENDS/\!d $cdlFile > ./temp1a #Delete the rest outside of .SUBCKT/ENDS
        more ./temp1a >> ./$outputFilePGspi
        echo ""       >> ./$outputFilePGspi
	more ./temp1a | sed -e /^\*.NETEXPR/d  -e /^\*.POWERSEN/d -e /^\*.GROUNDSEN/d >> ./$outputFilePGcdl
	echo ""                                >> ./$outputFilePGcdl 
	echo  -n "+"
end
# ----------------------------------------------------------------------------------------------
# Clean up the local tempolary files
if (-f ./temp1a) \rm -f ./temp1a
if (-f ./temp_cellList_$1.txt) \rm -f ./temp_cellList_$1.txt
#
# Delete the none-needed file: .spi
  if (-f ./$outputFilePGspi ) \rm -f ./$outputFilePGspi
#
echo ""
echo "FYI: Done (`date`)"
# ----------------------------------------------------------------------------------------------
if (-f ./$outputFilePGcdl ) nedit ./$outputFilePGcdl &
if (-f ./$outputFilePGspi ) nedit ./$outputFilePGspi &
#
