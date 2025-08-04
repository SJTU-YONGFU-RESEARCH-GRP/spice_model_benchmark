================================================================================
		GPDK045 Virtuoso EAD Corner Technology Files
				Version 6.0
================================================================================

The EAD corner technology files are not included in the gpdk045_v_6_0.tar.gz
file due to their size.  They are available in a separate download tar file
named gpdk045_ead_v_6_0.tar.gz at support.cadence.com.

After installing the gpdk045_v_6_0.tar.gz file, follow these steps to install
the EAD corner technology files:

1:  Download the gpdk045_ead_v_6_0.tar.gz file from support.cadence.com

2:  Place the file in the previously installed gpdk045_v_6_0/ead directory.
    (the directory where this README.txt is located).

3:  Install the gpdk045_ead_v_6_0.tar.gz file.  This will place the EAD corner
    technology files and configuration files in the 'ead' directory.

Any open IC6.1.8 sessions should be restarted to initialize EAD with these new
files.

After installation, the gpdk045_ead_v_6_0.tar.gz file can be removed.

================================================================================

Details of the files contained in gpdk045_ead_v_6_0.tar.gz:

   Compiled using Virtuoso IC618 ISR5 (gpdk045_ead_v_6_0)

   CORNERS:
         typical/eadTechfile    - typ r, typ c
         rcbest/eadTechfile	- min r, max c
         rcworst/eadTechfile	- max r, min c

================================================================================


The user can also regenerate the files using the EAD Technology File Generation
Flow described here.  Please follow all instructions below to properly configure
GPDK files to support EAD with the regenerated files.

--------------------------------------------------------------------------------
EAD Technology File Generation Flow
--------------------------------------------------------------------------------
Instructions for re-generating the technology files for each corner. 

1. Environment Setup: Edit the eadModelGen_cmd file and specify the
local Virtuoso IC package installation directory path.

2. Change directories into each corner directory and execute the 
following command:
	eadModelGen_cmd

** Approximate execution time (8 cpus) is 15 hours per corner **

    INPUT(S):
	<corner_name>.ict (link to ../ict/GPDK045_<CORNER>.ict)
    OUTPUT(S):
	eadModelGen.log
	eadTechFile

--------------------------------------------------------------------------------
Virtuoso Environment Setup
--------------------------------------------------------------------------------
1. The gpdk045 libInitCustomExit.il file defines the following Virtuoso
environment variables:

    envSetVal( "layoutEAD" "useSetup" 'string
	    "<GPDK045_INSTALL_PATH>/ead/gpdk045_setup.ini"
    )
    ...where <GPDK045_INSTALL_PATH> is the path to the local GPDK045 PDK
    installation directory

    ;;; Default corner for non-GUI flows
    envSetVal("layoutEAD" "useCorner" 'string "typical" )
    ;;; Default check layers for the pre-layout EM flow
    envSetVal("layoutEAD.em" "preEMCheckLayers" 'string "Metal1,Metal2")

*******************************************************************************
			IMPORTANT NOTE:-
*******************************************************************************
Please edit gpdk045_process.ini to modify the path of EAD technology files
for each corner. 
Below lines are located in gpdk045_process.ini and that has the path to EAD
technology file
*******************************************************************************
1\ICTModelFile=$GPDK045_PDK_PATH/ead/typical/eadTechFile
1\name=typical
2\ICTModelFile=$GPDK045_PDK_PATH/ead/rcbest/eadTechFile
2\name=rcbest
3\ICTModelFile=$GPDK045_PDK_PATH/ead/rcworst/eadTechFile
3\name=rcworst
*******************************************************************************
