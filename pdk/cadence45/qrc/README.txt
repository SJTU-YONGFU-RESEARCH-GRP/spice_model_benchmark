GPDK045 QUANTUS QRC Corner Technology Files
===========================================
Compiled using EXT 19.12-s160

CORNERS:
	typical
	rcbest	- min r, min c
	rcworst	- max r, max c


These technology files can be used with Virtuoso custom and 
Innovus digital implementation flows.

-----------------------------------------------------------------
RECOMMENDED USAGE - Technology Library Method
-----------------------------------------------------------------
1. Create a "pvtech.lib" file in your Virtuoso run directory and 
add the following technology library definition:

	DEFINE gpdk045_pvs <GPDK045_INSTALL_PATH>/pvs

...where <GPDK045_INSTALL_PATH> is the local directory where the 
GPDK045 PDK has been installed. The associated pvs/techRuleSets
file defines default PVS rule decks as well as the available QRC
technology file corners for this process.

2. Ensure that the QUANTUS EXT QRC package installation is in your
$PATH environment setup before starting virtuoso.


-----------------------------------------------------------------
QRC Technology File Generation Flow
-----------------------------------------------------------------
Instructions for re-generating the QRC technology files for each corner. 

1. Environment Setup: Edit setup.csh file as specify the EXT/QRC local
installation directory path.

2. Run the <corner_name>/Techgen_cmd_S (Simulation Step) script for
each corner. This will take the following input files and re-create the
following output files. NOTE: This is the most time-consuming step
(approx. 16hours). The Techgen_cmd_S script assumes the number of
available cpus to be 8. 

    INPUT(S):
	<corner_name>.ict (link to ../ict/GPDK045_<CORNER>.ict)
    OUTPUT(S):
	Mbb_data.analog
	Mbb_data.digital
	p2lvsfile
	procfile
	qrcTechFile

3. Run the <corner_name>/Techgen_cmd_C (Compilation Step) script for
each corner. This will take the following input files and produce the
following output files:
    INPUT(S):
	layer_setup
	lvsfile
	qrcTechFile
    OUTPUT(S):
	cap_coeff.dat
	caps2d
	capsw3d
	auxinfo
	paxfile_coeff
	RCXspiceINIT
	RCXdspfINIT
	rcxfs.dat
	qrcTechFile
