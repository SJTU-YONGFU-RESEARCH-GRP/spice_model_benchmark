/*
#########################################################################################
# SAED 32/28NM 1p9m icv metal fill drc deck						#
#											#
# Revision History:									#
# Rev.		date			what						#
# -------------------------------------------------------------------------------------	#	
# 1.0		02/Feb/2011		(First draft)					#
#########################################################################################
*/


#include "icv.rh"		
#include "math.rh"

/*
library(
	library_path = m_LIBRARY_PATH ,
	library_name  = "INLIB_TRAINING",
	format = MILKYWAY,
	cell = "FORICV"
);
*/

library(
	library_name  = "CELLNAME.gds",  
	format = GDSII,
	cell = "CELLNAME"

);

	
  
NWELL 		=	assign({{1}});
DNW		=	assign({{2}});
DIFF		=	assign({{3}});
DDMY		=	assign({{3},{1}});
PIMP		=	assign({{4}});
NIMP		=	assign({{5}});
DIFF_18		=	assign({{6}});
PAD		=	assign({{7}});
ESD_25		=	assign({{8}});
SBLK		=	assign({{9}});
PO		=	assign({{10}});
PODMY		=	assign({{10},{1}});
M1		=	assign({{11}});
M1_TEXT		=	assign_text({{11}});
M1DMY		=	assign({{11},{1}});
VIA1		=	assign({{12}});
M2		=	assign({{13}});
M2_TEXT		=	assign_text({{13}});
M2DMY		=	assign({{13},{1}});
VIA2		=	assign({{14}});
M3		=	assign({{15}});
M3_TEXT		=	assign_text({{15}});
M3DMY		=	assign({{15},{1}});
VIA3		=	assign({{16}});
M4		=	assign({{17}});
M4_TEXT		=	assign_text({{17}});
M4DMY		=	assign({{17},{1}});
VIA4 		=	assign({{18}});
M5		=	assign({{19}});
M5_TEXT		=	assign_text({{19}});
M5DMY		=	assign({{19},{1}});
VIA5		=	assign({{20}});
M6		=	assign({{21}});
M6_TEXT		=	assign_text({{21}});
M6DMY		=	assign({{21},{1}});
VIA6		=	assign({{22}});
M7		=	assign({{23}});
M7_TEXT		=	assign_text({{23}});
M7DMY		=	assign({{23},{1}});
VIA7		=	assign({{24}});
M8		=	assign({{25}});
M8_TEXT		=	assign_text({{25}});
M8DMY		=	assign({{25},{1}});
VIA8		=	assign({{26}});
M9		=	assign({{27}});
M9_TEXT		=	assign_text({{27}});
M9DMY		=	assign({{27},{1}});
CO		=	assign({{28}}); 
HVTIMP		=	assign({{29}});
LVTIMP		=	assign({{30}});
M1PIN		=	assign({{31}});
M1PIN_TEXT	=	assign_text({{31}});
M2PIN		=	assign({{32}});
M2PIN_TEXT	=	assign_text({{32}});
M3PIN		=	assign({{33}});
M3PIN_TEXT	=	assign_text({{33}});
M4PIN		=	assign({{34}});
M4PIN_TEXT	=	assign_text({{34}});
M5PIN		=	assign({{35}});
M5PIN_TEXT	=	assign_text({{35}});
M6PIN		=	assign({{36}});
M6PIN_TEXT	=	assign_text({{36}});
M7PIN		=	assign({{37}});
M7PIN_TEXT	=	assign_text({{37}});
M8PIN		=	assign({{38}});
M8PIN_TEXT	=	assign_text({{38}});
M9PIN		=	assign({{39}});
M9PIN_TEXT	=	assign_text({{39}});
MRDL		=	assign({{41}});
VIARDL		=	assign({{42}});
HOTNWL		=	assign({{44}});
DIOD		=	assign({{46}});
BJTMY		=	assign({{47}});
RNW		=	assign({{48}});
RMARK		=	assign({{49}});
LOGO		=	assign({{51}});
IP		=	assign({{52}});
RM1		=	assign({{53}});
RM2		=	assign({{54}});
RM3		=	assign({{55}});
RM4		=	assign({{56}});
RM5		=	assign({{57}});
RM6		=	assign({{58}});
RM7		=	assign({{59}});
RM8		=	assign({{60}});
RM9		=	assign({{61}});
DM1EXCL 	=	assign({{64}});
DM2EXCL 	=	assign({{65}});
DM3EXCL 	=	assign({{66}});
DM4EXCL 	=	assign({{67}});
DM5EXCL 	=	assign({{68}});
DM6EXCL 	=	assign({{69}});
DM7EXCL 	=	assign({{70}});
DM8EXCL 	=	assign({{71}});
DM9EXCL 	=	assign({{72}});
DIFFEXCL	=	assign({{73}});
POEXCL	 	=	assign({{74}});
DIFF_25		=	assign({{75}});

  
#define MilkyWay "N";
stagger : string = MilkyWay;


w_window : double = 10;
l_window : double = 10;

M1_extent = layer_extent(M1);

densityEQ_single_M1 : function(void) returning void
{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.00000000001 || RATIO < 0.1)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}

{ @"Fill candidates within window";


             density(window_layer =M1_extent,
                  layer_hash = { "layer1" => M1 },
                  window_function = densityEQ_single_M1,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  resize_delta_xy = true); 
}

candidates1 = density(window_layer =M1_extent,
                  layer_hash = { "layer1" => M1 },
                  window_function = densityEQ_single_M1,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  resize_delta_xy = true); 

sized_layer = size (M1, 0.18);
candidates = candidates1 not DM1EXCL ;
fill_candidates = candidates not sized_layer;

#include "Include/ME2_32.rs"
#include "Include/ME3_32.rs"
#include "Include/ME4_32.rs"
#include "Include/ME5_32.rs"
#include "Include/ME6_32.rs"
#include "Include/ME7_32.rs"
#include "Include/ME8_32.rs"
////#include "Include/ME9_32.rs"



if (stagger == "Y"){
my_func1: function ( void ) returning void{
   strike : polygon = fp_get_current_polygon();
   fp_generate_fill(
      polygon = strike,
      width =  0.4,
      height = 0.7, 
      space_x = 0.3,
      space_y = 0.3,
      stagger_x = 0.2,
      stagger_y = 0.2
     );
}
fillOutput1  = fill_pattern( fill_candidates,
                           fill_function = my_func1,
                          output_aref = {output_aref = true}

);

fillOutput1_1 = size (fillOutput1 , 0.2);
fill_candidates_s = fill_candidates not fillOutput1_1;

my_func2: function ( void ) returning void{
   strike : polygon = fp_get_current_polygon();
   fp_generate_fill(
      polygon = strike,
      width = 1.0,
      height = 0.75,
      space_x = 0.25,
      space_y = 0.25,
      stagger_x = 0.25,
      stagger_y = 0.25
     );
}
fillOutput2  = fill_pattern( fill_candidates_s,
                           fill_function = my_func2,
                          output_aref = {output_aref = true}

);

fillOutput2_1 = size (fillOutput2 , 0.2);
fill_candidates_s_1 = fill_candidates_s not fillOutput2_1;

my_func3: function ( void ) returning void{
   strike : polygon = fp_get_current_polygon();
   fp_generate_fill(
      polygon = strike,
      width = 0.5,
      height = 0.5,
      space_x = 0.2,
      space_y = 0.2,
      stagger_x = 0.2,
      stagger_y = 0.2
     );
}
fillOutput3  = fill_pattern( fill_candidates_s_1,
                           fill_function = my_func3,
                          output_aref = {output_aref = true}

);

fillOutput_m1 = fillOutput2 or fillOutput1 or fillOutput3;

#include "Include/fillOutput_m2.rs"
#include "Include/fillOutput_m3.rs"
#include "Include/fillOutput_m4.rs"
#include "Include/fillOutput_m5.rs"
#include "Include/fillOutput_m6.rs"
#include "Include/fillOutput_m7.rs"
#include "Include/fillOutput_m8.rs"
///#include "Include/fillOutput_m9.rs"





} else if(stagger == "N") {

my_func1: function ( void ) returning void{
   strike : polygon = fp_get_current_polygon();
   fp_generate_fill(
      polygon = strike,
      width = 0.4,
      height = 0.7,
      space_x = 0.3,
      space_y = 0.3,
      stagger_x = 0.2,
      stagger_y = 0.2
     );
}
fillOutput1  = fill_pattern( fill_candidates,
                           fill_function = my_func1,
                          output_aref = {output_aref = true}

);

fillOutput1_1 = size (fillOutput1 , 0.2);
fill_candidates_s = fill_candidates not fillOutput1_1;

my_func2: function ( void ) returning void{
   strike : polygon = fp_get_current_polygon();
   fp_generate_fill(
      polygon = strike,
      width = 1.0,
      height = 0.75,
      space_x = 0.25,
      space_y = 0.25,
      stagger_x = 0.25,
      stagger_y = 0.25
     );
}
fillOutput2  = fill_pattern( fill_candidates_s,
                           fill_function = my_func2,
                          output_aref = {output_aref = true}

);

fillOutput2_1 = size (fillOutput2 , 0.2);
fill_candidates_s_1 = fill_candidates_s not fillOutput2_1;

my_func3: function ( void ) returning void{
   strike : polygon = fp_get_current_polygon();
   fp_generate_fill(
      polygon = strike,
      width = 0.5,
      height = 0.5,
      space_x = 0.2,
      space_y = 0.2,
      stagger_x = 0.2,
      stagger_y = 0.2
     );
}
fillOutput3  = fill_pattern( fill_candidates_s_1,
                           fill_function = my_func3,
                          output_aref = {output_aref = true}

);

fillOutput_m1 = fillOutput2 or fillOutput1 or fillOutput3;


#include "Include/fillOutput_m2.rs"
#include "Include/fillOutput_m3.rs"
#include "Include/fillOutput_m4.rs"
#include "Include/fillOutput_m5.rs"
#include "Include/fillOutput_m6.rs"
#include "Include/fillOutput_m7.rs"
#include "Include/fillOutput_m8.rs"
////#include "Include/fillOutput_m9.rs"


//////////////////////////////////////////////////////////////
ME1D = fillOutput_m1 or M1;

ME1D_extent = layer_extent(ME1D);

sf1_global_end = density_statistics_file ("ME1.global.end");

densityEQ_single_ME1D : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.7)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}


gds_fh1 = gds_library ("special_testgdsout.gds");
write_gds(gds_fh1, holding_cell = "*" ,output_cell = "POANT2", merge_input_layout = true ,cell_prefix = "FD_",  

layers = {{fillOutput_m1,{11} },	
	   {fillOutput_m2,{13} },
	   {fillOutput_m3,{15} },
	   {fillOutput_m4,{17} },
	   {fillOutput_m5,{19} },
	   {fillOutput_m6,{21} },
	   {fillOutput_m7,{23} },
	   {fillOutput_m8,{25} },
      /////{fillOutput_m9,{27} }}
	
	{NWELL 		, {1}},
	{DNW		, {2}},
	{DIFF		, {3}},
	{DDMY		, {3}},
	{PIMP		, {4}},
	{NIMP		, {5}},
	{DIFF_18	, {6}},
	{PAD		, {7}},
	{ESD_25		, {8}},
	{SBLK		, {9}},
	{PO		, {10}},	
	{PODMY		, {10}},
	{M1		, {11}},
	{M1_TEXT	, {11}},
	{M1DMY		, {11}},
	{VIA1		, {12}},
	{M2		, {13}},
	{M2_TEXT	, {13}},
	{M2DMY		, {13}},
	{VIA2		, {14}},
	{M3		, {15}},
	{M3_TEXT	, {15}},
	{M3DMY		, {15}},
	{VIA3		, {16}},
	{M4		, {17}},
	{M4_TEXT	, {17}},
	{M4DMY		, {17}},
	{VIA4 		, {18}},
	{M5		, {19}},
	{M5_TEXT	, {19}},
	{M5DMY		, {19}},
	{VIA5		, {20}},
	{M6		, {21}},
	{M6_TEXT	, {21}},
	{M6DMY		, {21}},
	{VIA6		, {22}},
	{M7		, {23}},
	{M7_TEXT	, {23}},
	{M7DMY		, {23}},
	{VIA7		, {24}},
	{M8		, {25}},
	{M8_TEXT	, {25}},
	{M8DMY		, {25}},
	{VIA8		, {26}},
	{M9		, {27}},
	{M9_TEXT	, {27}},
	{M9DMY		, {27}},
	{CO		, {28}}, 
	{HVTIMP		, {29}},
	{LVTIMP		, {30}},
	{M1PIN		, {31}},
	{M1PIN_TEXT	, {31}},
	{M2PIN		, {32}},
	{M2PIN_TEXT	, {32}},
	{M3PIN		, {33}},
	{M3PIN_TEXT	, {33}},
	{M4PIN		, {34}},
	{M4PIN_TEXT	, {34}},
	{M5PIN		, {35}},
	{M5PIN_TEXT	, {35}},
	{M6PIN		, {36}},
	{M6PIN_TEXT	, {36}},
	{M7PIN		, {37}},
	{M7PIN_TEXT	, {37}},
	{M8PIN		, {38}},
	{M8PIN_TEXT	, {38}},
	{M9PIN		, {39}},
	{M9PIN_TEXT	, {39}},
	{MRDL		, {41}},
	{VIARDL		, {42}},
	{HOTNWL		, {44}},
	{DIOD		, {46}},
	{BJTMY		, {47}},
	{RNW		, {48}},
	{RMARK		, {49}},
	{LOGO		, {51}},
	{IP		, {52}},
	{RM1		, {53}},
	{RM2		, {54}},
	{RM3		, {55}},
	{RM4		, {56}},
	{RM5		, {57}},
	{RM6		, {58}},
	{RM7		, {59}},
	{RM8		, {60}},
	{RM9		, {61}},
	{DM1EXCL 	, {64}},
	{DM2EXCL 	, {65}},
	{DM3EXCL 	, {66}},
	{DM4EXCL 	, {67}},
	{DM5EXCL 	, {68}},
	{DM6EXCL 	, {69}},
	{DM7EXCL 	, {70}},
	{DM8EXCL 	, {71}},
	{DM9EXCL 	, {72}},
	{DIFFEXCL	, {73}},
	{POEXCL	 	, {74}},
	{DIFF_25	, {75}}});
 

/////////////////////////////////////////////////////ME1
ME1 = M1DMY or M1;

ME1_extent = layer_extent(ME1);

sf1_global_start = density_statistics_file ("ME1.global.start");

densityEQ_single_ME1 : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.7)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}

//////////////////////////////////////////////////////ME2
ME2 = M2DMY or M2;

ME2_extent = layer_extent(ME2);

sf2_global_start = density_statistics_file ("ME2.global.start");

densityEQ_single_ME2 : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.71)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}
///////////////////////////////////////////////////////ME3

ME3 = M3DMY or M3;

ME3_extent = layer_extent(ME3);

sf3_global_start = density_statistics_file ("ME3.global.start");

densityEQ_single_ME3 : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.71)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}
///////////////////////////////////////////////////////ME4

ME4 = M4DMY or M4;

ME4_extent = layer_extent(ME4);

sf4_global_start = density_statistics_file ("ME4.global.start");

densityEQ_single_ME4 : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.71)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}

///////////////////////////////////////////////////////ME5

ME5 = M5DMY or M5;

ME5_extent = layer_extent(ME5);

sf5_global_start = density_statistics_file ("ME5.global.start");

densityEQ_single_ME5 : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.71)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}
///////////////////////////////////////////////////////ME6

ME6 = M6DMY or M6;

ME6_extent = layer_extent(ME6);

sf6_global_start = density_statistics_file ("ME6.global.start");

densityEQ_single_ME6 : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.71)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}
///////////////////////////////////////////////////////ME7

ME7 = M7DMY or M7;

ME7_extent = layer_extent(ME7);

sf7_global_start = density_statistics_file ("ME7.global.start");

densityEQ_single_ME7 : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.71)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}


///////////////////////////////////////////////////////ME8

ME8 = M8DMY or M8;

ME8_extent = layer_extent(ME8);

sf8_global_start = density_statistics_file ("ME8.global.start");

densityEQ_single_ME8 : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.71)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}

///////////////////////////////////////////////////////ME9
/*
ME9 = M9DMY or M9;

ME9_extent = layer_extent(ME9);

sf9_global_start = density_statistics_file ("ME9.global.start");

densityEQ_single_ME9 : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.6)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}*/
///////////////////////////////////////////////////////




{ @"Densisty across chip";


             density(window_layer = ME1_extent,
                  layer_hash = { "layer1" => ME1 },
                  window_function = densityEQ_single_ME1,
                  statistics_files = sf1_global_start 
                  ); 

  	     density(window_layer = ME2_extent,
                  layer_hash = { "layer1" => ME2 },
                  window_function = densityEQ_single_ME2,
                  statistics_files = sf2_global_start 
                  ); 

	     density(window_layer = ME3_extent,
                  layer_hash = { "layer1" => ME3 },
                  window_function = densityEQ_single_ME3,
                  statistics_files = sf3_global_start 
                  ); 
		
	     density(window_layer = ME4_extent,
                  layer_hash = { "layer1" => ME4 },
                  window_function = densityEQ_single_ME4,
                  statistics_files = sf4_global_start 
                  );
 	    density(window_layer = ME5_extent,
                  layer_hash = { "layer1" => ME5 },
                  window_function = densityEQ_single_ME5,
                  statistics_files = sf5_global_start 
                  ); 
		
	     density(window_layer = ME6_extent,
                  layer_hash = { "layer1" => ME6 },
                  window_function = densityEQ_single_ME6,
                  statistics_files = sf6_global_start 
                  );

       	     density(window_layer = ME7_extent,
                  layer_hash = { "layer1" => ME7 },
                  window_function = densityEQ_single_ME7,
                  statistics_files = sf7_global_start 
                  ); 
		
	     density(window_layer = ME8_extent,
                  layer_hash = { "layer1" => ME8 },
                  window_function = densityEQ_single_ME8,
                  statistics_files = sf8_global_start 
                  );
/*
 	     density(window_layer =ME9_extent,
                  layer_hash = { "layer1" => ME9 },
                  window_function = densityEQ_single_ME9,
                  statistics_files = sf9_global_start 
                  );*/



}
//////////////////////////////////////////////////////

sf1_window_start = density_statistics_file ("ME1.window.start");
sf2_window_start = density_statistics_file ("ME2.window.start");
sf3_window_start = density_statistics_file ("ME3.window.start");
sf4_window_start = density_statistics_file ("ME4.window.start");
sf5_window_start = density_statistics_file ("ME5.window.start");
sf6_window_start = density_statistics_file ("ME6.window.start");
sf7_window_start = density_statistics_file ("ME7.window.start");
sf8_window_start = density_statistics_file ("ME8.window.start");
///sf9_window_start = density_statistics_file ("ME9.window.start");




///////////////////////////////////////////////////////
densityEQ_ME : function(void) returning void
{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.9)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}


{ @"Density across window";


             density(window_layer = ME1_extent,
                  layer_hash = { "layer1" => ME1 },
                  window_function = densityEQ_ME,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  statistics_files = sf1_window_start 
                  ); 


	
             density(window_layer = ME2_extent,
                  layer_hash = { "layer1" => ME2 },
                  window_function = densityEQ_ME,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  statistics_files = sf2_window_start 
                  ); 


	     density(window_layer = ME3_extent,
                  layer_hash = { "layer1" => ME3 },
                  window_function = densityEQ_ME,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  statistics_files = sf3_window_start 
                  ); 

	     density(window_layer = ME4_extent,
                  layer_hash = { "layer1" => ME4 },
                  window_function = densityEQ_ME,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  statistics_files = sf4_window_start 
                  ); 

	     density(window_layer = ME5_extent,
                  layer_hash = { "layer1" => ME5 },
                  window_function = densityEQ_ME,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  statistics_files = sf5_window_start 
                  ); 

	     density(window_layer = ME6_extent,
                  layer_hash = { "layer1" => ME6 },
                  window_function = densityEQ_ME,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  statistics_files = sf6_window_start 
                  ); 

  
	     density(window_layer = ME7_extent,
                  layer_hash = { "layer1" => ME7 },
                  window_function = densityEQ_ME,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  statistics_files = sf7_window_start 
                  ); 

	     density(window_layer = ME8_extent,
                  layer_hash = { "layer1" => ME8 },
                  window_function = densityEQ_ME,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  statistics_files = sf8_window_start 
                  ); 

   	   /*density(window_layer = ME9_extent,
                  layer_hash = { "layer1" => ME9 },
                  window_function = densityEQ_ME,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  statistics_files = sf9_window_start 
                  ); */

}

/*
		m_library = milkyway_library ("design_results" , ".");
write_milkyway ( 
	output_library = m_library,
	output_cell = "out",
	view ="filled_",
	mode = OVERWRITE,
	output_hierarchy = true,
	
layers = {{fillOutput_m1,{11} },	
	   {fillOutput_m2,{13} },
	   {fillOutput_m3,{15} },
	   {fillOutput_m4,{17} },
	   {fillOutput_m5,{19} },
	   {fillOutput_m6,{21} },
	   {fillOutput_m7,{23} },
	   {fillOutput_m8,{25} },
      /////{fillOutput_m9,{27} }}
	
	{NWELL 		, {1}},
	{DNW		, {2}},
	{DIFF		, {3}},
	{DDMY		, {3}},
	{PIMP		, {4}},
	{NIMP		, {5}},
	{DIFF_18	, {6}},
	{PAD		, {7}},
	{ESD_25		, {8}},
	{SBLK		, {9}},
	{PO		, {10}},	
	{PODMY		, {10}},
	{M1		, {11}},
	{M1_TEXT	, {11}},
	{M1DMY		, {11}},
	{VIA1		, {12}},
	{M2		, {13}},
	{M2_TEXT	, {13}},
	{M2DMY		, {13}},
	{VIA2		, {14}},
	{M3		, {15}},
	{M3_TEXT	, {15}},
	{M3DMY		, {15}},
	{VIA3		, {16}},
	{M4		, {17}},
	{M4_TEXT	, {17}},
	{M4DMY		, {17}},
	{VIA4 		, {18}},
	{M5		, {19}},
	{M5_TEXT	, {19}},
	{M5DMY		, {19}},
	{VIA5		, {20}},
	{M6		, {21}},
	{M6_TEXT	, {21}},
	{M6DMY		, {21}},
	{VIA6		, {22}},
	{M7		, {23}},
	{M7_TEXT	, {23}},
	{M7DMY		, {23}},
	{VIA7		, {24}},
	{M8		, {25}},
	{M8_TEXT	, {25}},
	{M8DMY		, {25}},
	{VIA8		, {26}},
	{M9		, {27}},
	{M9_TEXT	, {27}},
	{M9DMY		, {27}},
	{CO		, {28}}, 
	{HVTIMP		, {29}},
	{LVTIMP		, {30}},
	{M1PIN		, {31}},
	{M1PIN_TEXT	, {31}},
	{M2PIN		, {32}},
	{M2PIN_TEXT	, {32}},
	{M3PIN		, {33}},
	{M3PIN_TEXT	, {33}},
	{M4PIN		, {34}},
	{M4PIN_TEXT	, {34}},
	{M5PIN		, {35}},
	{M5PIN_TEXT	, {35}},
	{M6PIN		, {36}},
	{M6PIN_TEXT	, {36}},
	{M7PIN		, {37}},
	{M7PIN_TEXT	, {37}},
	{M8PIN		, {38}},
	{M8PIN_TEXT	, {38}},
	{M9PIN		, {39}},
	{M9PIN_TEXT	, {39}},
	{MRDL		, {41}},
	{VIARDL		, {42}},
	{HOTNWL		, {44}},
	{DIOD		, {46}},
	{BJTMY		, {47}},
	{RNW		, {48}},
	{RMARK		, {49}},
	{LOGO		, {51}},
	{IP		, {52}},
	{RM1		, {53}},
	{RM2		, {54}},
	{RM3		, {55}},
	{RM4		, {56}},
	{RM5		, {57}},
	{RM6		, {58}},
	{RM7		, {59}},
	{RM8		, {60}},
	{RM9		, {61}},
	{DM1EXCL 	, {64}},
	{DM2EXCL 	, {65}},
	{DM3EXCL 	, {66}},
	{DM4EXCL 	, {67}},
	{DM5EXCL 	, {68}},
	{DM6EXCL 	, {69}},
	{DM7EXCL 	, {70}},
	{DM8EXCL 	, {71}},
	{DM9EXCL 	, {72}},
	{DIFFEXCL	, {73}},
	{POEXCL	 	, {74}},
	{DIFF_25	, {75}}});
*/
}















