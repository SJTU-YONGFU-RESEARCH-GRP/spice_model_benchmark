/*
#########################################################################################
# SAED 14NM 1p9m icv metal fill drc deck						#
#											#
# Revision History:									#
# Rev.		date			what						#
# -------------------------------------------------------------------------------------	#	
# 1.0		10/Jan/2018		(First draft)					#
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
FIN    		= assign({{1}});
FINCUT    	= assign({{2}});
NWELL    	= assign({{3}});
DNW	  		= assign({{4}});
DIFF	  	= assign({{5}});	
DDMY     	= assign({{5},{1}});
PIMP	  	= assign({{6}});
NIMP	  	= assign({{7}});
DIFF_15  	= assign({{8}});
DIFF_18  	= assign({{9}});
PAD	  		= assign({{10}});
ESD	  		= assign({{11}});
SBLK	  	= assign({{12}});
PO       	= assign({{13}});
POCUT       = assign({{14}});
PODMY    	= assign({{13,1}});
TSLCO    	= assign({{15}});
TSLCB    	= assign({{16}});
CTM1       	= assign({{17}});
CTM1_1      = assign({{17}, {1}});
CTM1_2      = assign({{17}, {2}});
CPO       	= assign({{18}});
CPO_1       = assign({{18}, {1}});
CPO_2       = assign({{18}, {2}});
VIA0     	= assign({{81}});
M1       	= assign({{19}});
M1_3	  	= assign({{90}});		
M1DMY    	= assign({{19},{1}});
M1_text  	= assign_text({{19}});
VIA1     	= assign({{20}});
M2       	= assign({{21}});
M2_3	  	= assign({{91}});		
M2_text  	= assign_text({{21}});
VIA2    	= assign({{22}});
M2DMY    	= assign({{21},{1}});
M3       	= assign({{23}});
M3_3       	= assign({{92}});		
M3_text  	= assign_text({{23}});
M3DMY    	= assign({{23},{1}});
VIA3    	= assign({{24}});
M4       	= assign({{25}});
M4_text  	= assign_text({{25}}); 
M4DMY    	= assign({{25},{1}});      
VIA4    	= assign({{26}});
M5       	= assign({{27}}); 
M5_text  	= assign_text({{27}});   
VIA5    	= assign({{28}});
M6       	= assign({{29}});    
M6_text  	= assign_text({{29}});
M6DMY    	= assign({{29},{1}});
VIA6     	= assign({{30}});
M7       	= assign({{31}});
M7_text  	= assign_text({{31}});   
M7DMY    	= assign({{31},{1}}); 
VIA7     	= assign({{32}});
M8       	= assign({{33}});
M8_text  	= assign_text({{33}});
M8DMY    	= assign({{33},{1}});
VIA8     	= assign({{34}});    
M9       	= assign({{35}});   
M9_text  	= assign({{35}});
M9DMY    	= assign({{35},{1}});  
HVTIMP  	= assign({{36}});
LVTIMP   	= assign({{37}});
M1PIN     	= assign({{38}});
M1PIN_text 	= assign_text({{38}});
M2PIN     	= assign({{39}});
M2PIN_text 	= assign_text({{39}});
M3PIN     	= assign({{40}});
M3PIN_text 	= assign_text({{40}});
M4PIN     	= assign({{41}});
M4PIN_text 	= assign_text({{41}});
M5PIN     	= assign({{42}});
M5PIN_text 	= assign_text({{42}});
M6PIN     	= assign({{43}});
M6PIN_text 	= assign_text({{43}});
M7PIN     	= assign({{44}});
M7PIN_text 	= assign_text({{44}});
M8PIN     	= assign({{45}});
M8PIN_text 	= assign_text({{45}});
M9PIN     	= assign({{46}});
M9PIN_text 	= assign_text({{46}});
MRDL      	= assign({{47}});
VIARDL	   	= assign({{48}});
MRPIN      	= assign({{49}});
HOTNWL    	= assign({{50}});
DIOD      	= assign({{51}});
BJTMY     	= assign({{52}});
RNW      	= assign({{53}});
RMARK     	= assign({{54}});
LOGO      	= assign({{56}});
IP        	= assign({{57}});
RM1      	= assign({{58}});
RM2      	= assign({{59}});
RM3      	= assign({{60}});
RM4      	= assign({{61}});
RM5      	= assign({{62}});
RM6      	= assign({{63}});
RM7      	= assign({{64}});	
RM8      	= assign({{65}});
RM9      	= assign({{66}});
DIFFCUT     = assign({{82}});
AXPOLY      = assign({{83}});
SLVTIMP     = assign({{84}});
FGATE		= assign({{85}});
B_VIA0      = assign({{86}});

	
  
#define MilkyWay "N";
stagger : string = MilkyWay;


w_window : double = 10;
l_window : double = 10;
M1_all = M1 or M1_3;
M1_extent = layer_extent(M1_all);

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
                  layer_hash = { "layer1" => M1_all },
                  window_function = densityEQ_single_M1,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  resize_delta_xy = true); 
}

candidates1 = density(window_layer =M1_extent,
                  layer_hash = { "layer1" => M1_all },
                  window_function = densityEQ_single_M1,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  resize_delta_xy = true); 

sized_layer = size (M1_all, 0.085);
candidates = candidates1 not M1DMY ;
fill_candidates = candidates not sized_layer;

#include "Include/ME2_14.rs"
#include "Include/ME3_14.rs"
#include "Include/ME4_14.rs"
#include "Include/ME5_14.rs"
#include "Include/ME6_14.rs"
#include "Include/ME7_14.rs"
#include "Include/ME8_14.rs"
////#include "Include/ME9_14.rs"



if (stagger == "Y"){
my_func1: function ( void ) returning void{
   strike : polygon = fp_get_current_polygon();
   fp_generate_fill(
      polygon = strike,
      width =  0.06,
      height = 0.1, 
      space_x = 0.04,
      space_y = 0.04,
      stagger_x = 0.01,
      stagger_y = 0.01
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
      width = 0.12,
      height = 0.48,
      space_x = 0.08,
      space_y = 0.08,
      stagger_x = 0.02,
      stagger_y = 0.02
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
      width = 0.2,
      height = 0.2,
      space_x = 0.1,
      space_y = 0.1,
      stagger_x = 0.05,
      stagger_y = 0.05
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
      width = 0.06,
      height = 0.1,
      space_x = 0.04,
      space_y = 0.04,
      stagger_x = 0.01,
      stagger_y = 0.01
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
      width = 0.12,
      height = 0.48,
      space_x = 0.08,
      space_y = 0.08,
      stagger_x = 0.08,
      stagger_y = 0.08
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
      width = 0.2,
      height = 0.2,
      space_x = 0.1,
      space_y = 0.1,
      stagger_x = 0.05,
      stagger_y = 0.05
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
ME1D = (fillOutput_m1 or M1) or M1_3;

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

layers = {{fillOutput_m1,{19} },	
	   {fillOutput_m2,{21} },
	   {fillOutput_m3,{23} },
	   {fillOutput_m4,{25} },
	   {fillOutput_m5,{27} },
	   {fillOutput_m6,{29} },
	   {fillOutput_m7,{31} },
	   {fillOutput_m8,{33} },
      /////{fillOutput_m9,{35} }}
				


	{FIN		, {1}},
	{FINCUT		, {2}},
	{NWELL 		, {3}},
	{DNW		, {4}},
	{DIFF		, {5}},
	{DDMY		, {5}},
	{PIMP		, {6}},
	{NIMP		, {7}},
	{DIFF_15	, {8}},
	{DIFF_18	, {9}},
	{PAD		, {10}},
	{ESD		, {11}},
	{SBLK		, {12}},
	{PO		, {13}},
	{POCUT		, {14}},	
	{PODMY		, {13}},
	{TSLCO		, {15}},
	{TSLCB		, {16}},
	{CTM1		, {17}},
	{CTM1_1		, {17}},
	{CTM1_2		, {17}},
	{CPO		, {18}},
	{CPO_1		, {18}},
	{CPO_2		, {18}},
	{VIA0		, {81}},
	{M1			, {19}},
	{M1_3		, {90}},
	{M1DMY		, {19}},
	{M1_text	, {19}},
	{VIA1		, {20}},
	{M2			, {21}},
	{M2_3		, {91}},
	{M2_text	, {21}},
	{M2DMY		, {21}},
	{VIA2		, {22}},
	{M3			, {23}},
	{M3_3		, {92}},
	{M3_text	, {23}},
	{M3DMY		, {23}},
	{VIA3		, {24}},
	{M4			, {25}},
	{M4_text	, {25}},
	{M4DMY		, {25}},
	{VIA4 		, {26}},
	{M5			, {27}},
	{M5_text	, {27}},
//	{M5DMY		, {19}},	chka
	{VIA5		, {28}},
	{M6			, {29}},
	{M6_text	, {29}},
	{M6DMY		, {29}},
	{VIA6		, {30}},
	{M7			, {31}},
	{M7_text	, {31}},
	{M7DMY		, {31}},
	{VIA7		, {32}},
	{M8			, {33}},
	{M8_text	, {33}},
	{M8DMY		, {33}},
	{VIA8		, {34}},
	{M9			, {35}},
	{M9_text	, {35}},
	{M9DMY		, {35}},
	{HVTIMP		, {36}},
	{LVTIMP		, {37}},
	{M1PIN		, {38}},
	{M1PIN_text	, {38}},
	{M2PIN		, {39}},
	{M2PIN_text	, {39}},
	{M3PIN		, {40}},
	{M3PIN_text	, {40}},
	{M4PIN		, {41}},
	{M4PIN_text	, {41}},
	{M5PIN		, {42}},
	{M5PIN_text	, {42}},
	{M6PIN		, {43}},
	{M6PIN_text	, {43}},
	{M7PIN		, {44}},
	{M7PIN_text	, {44}},
	{M8PIN		, {45}},
	{M8PIN_text	, {45}},
	{M9PIN		, {46}},
	{M9PIN_text	, {46}},
	{MRDL		, {47}},
	{VIARDL		, {48}},
	{MRPIN		, {49}},
	{HOTNWL		, {50}},
	{DIOD		, {51}},
	{BJTMY		, {52}},
	{RNW		, {53}},
	{RMARK		, {54}},
	{LOGO		, {56}},
	{IP		, {57}},
	{RM1		, {58}},
	{RM2		, {59}},
	{RM3		, {60}},
	{RM4		, {61}},
	{RM5		, {62}},
	{RM6		, {63}},
	{RM7		, {64}},
	{RM8		, {65}},
	{RM9		, {66}},
	{DIFFCUT	, {82}},
	{AXPOLY		, {83}},
	{SLVTIMP	, {84}},
	{FGATE		, {85}},
	{B_VIA0		, {86}}});	

/////////////////////////////////////////////////////ME1
ME1 = (M1DMY or (M1 or M1_3));

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
ME2 = (M2DMY or (M2 or M2_3));

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

ME3 = (M3DMY or (M3 or M3_3));

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

ME5 = M5;

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
}
