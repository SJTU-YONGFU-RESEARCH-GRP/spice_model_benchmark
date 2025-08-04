#!/bin/tcsh -f

set defaultRunset = "StdFill_V05.pvl"

echo "Starting PVS Batch Fill ..."

## Check that env var PVS_TECHDIR_FILL is set
if ( ! ($?PVS_TECHDIR_FILL) ) then
   echo 'INFO: Please set PVS_TECHDIR_FILL and re-run'
   exit
else
   if ( ! -d $PVS_TECHDIR_FILL ) then
      echo 'INFO: Please check that PVS_TECHDIR_FILL is correct and re-run'
      exit
   else
      if ( ! -f $PVS_TECHDIR_FILL/$defaultRunset ) then
         echo 'INFO: Please check that the fill deck exists in PVS_TECHDIR_FILL'
         exit
      endif
   endif
endif

## Check for a PVS installation
set pvsPath=`which cdnspvs`
if ( $? == 1 ) then
   echo 'INFO: Please add Cadence PVS to the path and re-run'
   exit
endif

## Input fill deck
if ( $#argv > 3 ) then
   if ( -f $argv[4] ) then
      set runset = $argv[4]
      echo "INFO: Running the fill runset $runset"
   else
      echo 'INFO: Please check the runset and re-run'
      echo 'Usage: $argv[0] <layout> <topcell> [<outputDir>] [<runset>]'
      exit
   endif
else
   set runset = "$PVS_TECHDIR_FILL/$defaultRunset"
   echo "INFO: Running the fill runset $runset"
endif

## Input layout file
if ( $#argv < 1 ) then
   echo 'INFO: Please specify a layout file and re-run'
   echo 'Usage: $argv[0] <layout> <topcell> [<outputDir>] [<runset>]'
   exit
else
   if ( -f $argv[1] ) then
      set layout = $argv[1]
      if ( $layout =~ *gds ) then
         echo 'INFO: Using layout format GDSII'
         set layoutType = "gds"
         if ( ! ($?LAYOUT_SYSTEM) ) then
            setenv LAYOUT_SYSTEM "GDSII"
         endif
      else
         echo 'INFO: Using layout format OASIS'
         set layoutType = "oas"
         if ( ! ($?LAYOUT_SYSTEM) ) then
            setenv LAYOUT_SYSTEM "OASIS"
         endif
   else
      echo 'INFO: Please check the layout location and access and re-run'
      echo 'Usage: $argv[0] <layout> <topcell> [<outputDir>] [<runset>]'
      exit
   endif
endif

## Output Directory Location
if ( $#argv > 2 ) then
   if ( ! -d $argv[3] ) then
      echo 'INFO: Please check the output directory path and re-run'
      echo 'Usage: $argv[0] <layout> <topcell> [<outputDir>] [<runset>]'
      exit
   else
      set outputDir = $argv[3]
   endif
else
   set outputDir = `pwd` 
endif 

## Get the layout top cell name
if ( $#argv > 1 ) then
   set topcell = $argv[2]
else
   echo 'INFO: Please specify the top cell name and re-run'
   echo 'Usage: $argv[0] <layout> <topcell> [<outputDir>] [<runset>]'
   exit
endif

 
## Main Fill Flow

## First, run the fill deck
if ( $layoutType == "oas" ) then
   pvs -drc -oasis $layout -tc $topcell -run_dir $outputDir $runset | tee \
      $outputDir/run_pvs_fill_${topcell}_${layoutType}.log
else
   pvs -drc -gds $layout -tc $topcell -run_dir $outputDir $runset | tee \
      $outputDir/run_pvs_fill_${topcell}_${layoutType}.log
endif

## Second, add any fill instances
$PVS_TECHDIR_FILL/merge_fillcell.tcl \
   $outputDir/output.$layoutType \
   ${topcell}_fillcell.$layoutType \
   $topcell $layoutType

## Third, merge the results into a final layout file
$PVS_TECHDIR_FILL/merge.tcl \
   $layout \
   ${topcell}_fillcell.$layoutType \
   ${topcell}_merged.$layoutType \
   $topcell $layoutType


echo "All Done. Fill output is generated in ${outputDir}"

