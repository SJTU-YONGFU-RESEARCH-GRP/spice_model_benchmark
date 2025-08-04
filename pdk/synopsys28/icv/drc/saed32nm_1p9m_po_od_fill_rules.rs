/*
#########################################################################################
# SAED 32/28NM 1p9m icv poly od fill deck						#
#											#
# Revision History:									#
# Rev.		date			what						#
# -------------------------------------------------------------------------------------	#	
# 1.0		02/Feb/2011		(First draft)					#
# 1.1		--/---/2011		(First draft)					#
#########################################################################################
*/


#include "icv.rh"
#include "math.rh"


#ifndef m_LIBRARY_PATH
#define m_LIBRARY_PATH "/remote/home/stud121/Desktop/antenna_icv/"
#endif



library(
	library_name  = m_LIBRARY_PATH + "CELLNAME.gds",
	format = GDSII,
	cell = "POANT1"

);


NWELL 		= 	assign({{1}});
DNW		=	assign({{2}});
DIFF		=	assign({{3}});
DDMY		=	assign({{3},{1}});
PIMP		=	assign({{4}});
NIMP		=	assign({{5}});
DIFF_25		=	assign({{6}});
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
M8		=	assign({{24}});
M8_TEXT		=	assign_text({{24}});
M8DMY		=	assign({{24},{1}});
M9		=	assign({{25}});
M9_TEXT		=	assign_text({{25}});
M9DMY		=	assign({{25},{1}});
CO		=	assign({{26}}); 
VIA7		=	assign({{27}});
VIA8		=	assign({{28}});
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
HOTNWL		=	assign({{41}});
DIODMARK	=	assign({{43}});
BJTMARK		=	assign({{44}});
RNW		=	assign({{45}});
RMARKER		=	assign({{46}});
LOGO		=	assign({{48}});
IP		=	assign({{49},{49}});
DM1EXCL 	= 	assign({{61}});
DM2EXCL 	=	assign({{62}});
DM3EXCL 	=	assign({{63}});
DM4EXCL 	=	assign({{64}});
DM5EXCL 	=	assign({{65}});
DM6EXCL 	=	assign({{66}});
DM7EXCL 	=	assign({{67}});
DM8EXCL 	=	assign({{68}});
DM9EXCL 	=	assign({{69}});
DIFF_FM 	=	assign({{100}});
PO_FM 		=	assign({{101}});


#define MilkyWay "N";
stagger : string = MilkyWay;
PO_extent = layer_extent(PO);

densityEQ_single_PO : function(void) returning void
{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.00000000001 || RATIO < 0.1)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}

{ @"Fill candidates within window";


             density(window_layer =PO_extent,
                  layer_hash = { "layer1" => PO },
                  window_function = densityEQ_single_PO,
                  delta_window = {5,5},
                  delta_x = 1.0,
                  delta_y = 1.0,
                  resize_delta_xy = true); 
}






candidates1 = density(window_layer =PO_extent,
                  layer_hash = { "layer1" => PO },
                  window_function = densityEQ_single_PO,
                  delta_x = 1.0,
                  delta_y = 1.0,
                  resize_delta_xy = true,
                  statistics_file_modes = APPEND);



//candidates1 = PO;
blockage = cell_extent (
   cell_list = {}
);
//chip_extents = chip_extent();
sized_layer = size (PO,  distance = 0.63, processing_mode = CELL_LEVEL ); 
navs1 = size (DIFF,  distance = 0.63, processing_mode = CELL_LEVEL ); 
navs = navs1 or PO;
candidates = candidates1 not PO_FM;
//syzed_layer = size (PO,  distance = 0.2,processing_mode = CELL_LEVEL ); 
fill_candidates2 = candidates not sized_layer;

fill_candidates =  fill_candidates2 not navs; 
//bad_fill = fill_candidates1 interacting blockage;
// fill_candidates =  fill_candidates1 not bad_fill;



my_func1: function ( void ) returning void{
   strike : polygon = fp_get_current_polygon();
   fp_generate_fill(
      polygon = strike,
      width = 0.19,
      height = 0.19,
      space_x = 0.19,
      space_y = 0.19,
      stagger_x = 0.2,
      stagger_y = 0.2
     );
}
fillOutput1  = fill_pattern( fill_candidates,
                           fill_function = my_func1,
                          output_aref = {output_aref = true}

);


my_func2: function ( void ) returning void{
   strike : polygon = fp_get_current_polygon();
   fp_generate_fill(
      polygon = strike,
      width = 0.19,
      height = 0.19,
      space_x = 0.1,
      space_y = 0.1,
      stagger_x = 0.025,
      stagger_y = 0.025
     );
}
od_fill_rect  = fill_pattern( fillOutput1,
                           fill_function = my_func2,
                          output_aref = {output_aref = true}

);

fillOutput_1 = size (fillOutput1,  distance = 0.2);
fill_candidates_1 = fill_candidates not fillOutput_1;

my_func3: function ( void ) returning void{
   strike : polygon = fp_get_current_polygon();
   fp_generate_fill(
      polygon = strike,
      width = 0.14,
      height = 0.14,
      space_x = 0.1,
      space_y = 0.1,
      stagger_x = 0.025,
      stagger_y = 0.025
     );
}
fillOutput2  = fill_pattern( fill_candidates_1,
                           fill_function = my_func3,
                          output_aref = {output_aref = true}

);

fillOutput_PO = fillOutput1 or fillOutput2; 



my_func4: function ( void ) returning void{
   strike : polygon = fp_get_current_polygon();
   fp_generate_fill(
      polygon = strike,
      width = 0.095,
      height = 0.095,
      space_x = 0.06,
      space_y = 0.06,
      stagger_x = 0.06,
      stagger_y = 0.06
     );
}
od_fill_rect_1   = fill_pattern( fillOutput2,
                           fill_function = my_func4,
                          output_aref = {output_aref = true}

);









        



PO_FILL = copy (fillOutput_PO) ;
POD = PO_FILL or PO;






densityEQ_single_DIFF : function(void) returning void
{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.00000000001 || RATIO < 0.1)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}



DIFF_extent = layer_extent(DIFF);

candidates1_1 = density(window_layer =DIFF_extent,
                  layer_hash = { "layer1" => DIFF },
                  window_function = densityEQ_single_DIFF,
                  delta_x = 1.0,
                  delta_y = 1.0,
                  resize_delta_xy = true,
                  statistics_file_modes = APPEND);


//candidates1_1 = DIFF;

blockage_1 = cell_extent (
   cell_list = {}
);
sized_layer_1 = size (DIFF,  distance = 0.2, processing_mode = CELL_LEVEL ); 
navs1_1 = size (PO,  distance = 0.2, processing_mode = CELL_LEVEL ); 
navs2 = size (PODMY,  distance = 0.2,processing_mode = CELL_LEVEL );
navs3 = size (DDMY,  distance =0.2,processing_mode = CELL_LEVEL );
navs_1 =  (navs1_1 or navs2 or navs3);
candidates_1 =  candidates1_1 not DIFF_FM;
fill_candidates2_1 =  candidates_1 not sized_layer_1;
fill_candidates1_1 =  fill_candidates2_1 not navs_1; 
bad_fill_1 = fill_candidates1_1 interacting blockage_1;
//fill_candidates3_1 =  fill_candidates1 not bad_fill_1;
syzed_PODMY_1 = size (fillOutput_PO,  distance = 0.2,processing_mode = CELL_LEVEL ); 
//fill_candidates_1 =  fill_candidates3_1 not syzed_PODMY_1;
fill_candidates_1 =  fill_candidates1_1 not syzed_PODMY_1;
{ @"Fill candidates within window";

density(window_layer =DIFF_extent,
                  layer_hash = { "layer1" => DIFF },
                  window_function = densityEQ_single_DIFF,
                  delta_window = {5,5},
                  delta_x = 1.0,
                  delta_y = 1.0);

        


}






my_func_15: function ( void ) returning void{
   strike : polygon = fp_get_current_polygon();
   fp_generate_fill(
      polygon = strike,
      width = 0.13,
      height = 0.13,
      space_x = 0.13,
      space_y = 0.13,
      stagger_x = 0.025,
      stagger_y = 0.025
     );
}
fillOutput_DIFF  = fill_pattern( fill_candidates_1,
                           fill_function = my_func_15,
                          output_aref = {output_aref = true}

);










fillOutput_all_DIFF = od_fill_rect or fillOutput_DIFF or od_fill_rect_1;
DIFF_FILL = copy (fillOutput_all_DIFF); 
DIFFD = DIFF_FILL or DIFF; 


density_DIFFD : function(void) returning void
{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if ( RATIO <= 0.2 || RATIO >= 0.8)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}

sf3 = density_statistics_file ("DIFF.global.end");

DIFFD_extent = layer_extent(DIFFD);
{ @"Densisty across chip";
        candidates1 = density(window_layer =DIFFD_extent,
                  layer_hash = { "layer1" => DIFFD },
                  window_function = density_DIFFD,
                  delta_x = 1.0,
                  delta_y = 1.0,
                  statistics_files = sf3);}


densityEQ_DIFFD : function(void) returning void
{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if ( RATIO <= 0.15 || RATIO >= 0.85)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}
//DIFF_extent = layer_extent(DIFF);


{ @"Density across window";
        candidates1 = density(window_layer =DIFFD_extent,
                  layer_hash = { "layer1" => DIFFD },
                  window_function = densityEQ_DIFFD,
                  delta_window = {130,130},
                  delta_x = 75,
                  delta_y = 75,
                  statistics_files = {});}




density_POD : function(void) returning void
{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if ( RATIO <= 0.15 || RATIO >= 0.4)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}

sf4 = density_statistics_file ("PO.global.end");

POD_extent = layer_extent(POD);
{ @"Densisty across chip";
        candidates1 = density(window_layer =POD_extent,
                  layer_hash = { "layer1" => POD },
                  window_function = density_POD,
                 
                  delta_x = 1.0,
                  delta_y = 1.0,
                  statistics_files = sf4);}


densityEQ_POD1 : function(void) returning void
{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if ( RATIO >= 0.2 || RATIO >= 0.75)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}


{ @"Density across window";
        candidates1 = density(window_layer =POD_extent,
                  layer_hash = { "layer1" => POD },
                  window_function = densityEQ_POD1,
                  delta_window = {5,5},
                  delta_x = 1.0,
                  delta_y = 1.0,
                  statistics_files = {});}






densityEQ_PO : function(void) returning void
{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO >= 0.2 || RATIO >= 0.75)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}
PO_extent = layer_extent(PO);


{ @"Density across window";
        density(window_layer =PO_extent,
                  layer_hash = { "layer1" => PO },
                  window_function = densityEQ_PO,
                  delta_window = {5,5},
                  delta_x = 1.0,
                  delta_y = 1.0,
                  statistics_files = {});}


densityEQ_DIFF : function(void) returning void
{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO <= 0.15 || RATIO >= 0.85)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}
DIFF_extent = layer_extent(DIFF);


{ @"Density across window";
        density(window_layer =DIFF_extent,
                  layer_hash = { "layer1" => DIFF },
                  window_function = densityEQ_DIFF,
                  delta_window = {130,130},
                  delta_x = 75,
                  delta_y = 75,
                  statistics_files = {});}


density_PO : function(void) returning void
{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO <= 0.15 || RATIO >= 0.4)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}

sf = density_statistics_file ("PO.global.start");

PO_extent = layer_extent(PO);
{ @"Densisty across chip";
        density(window_layer =PO_extent,
                  layer_hash = { "layer1" => PO },
                  window_function = density_PO,
                  delta_x = 1.0,
                  delta_y = 1.0,
                  statistics_files = sf);}




density_DIFF : function(void) returning void
{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if ( RATIO <= 0.2 || RATIO >= 0.8)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}

sf1 = density_statistics_file ("DIFF.global.start");

DIFF_extent = layer_extent(DIFF);
{ @"Densisty across chip";
        density(window_layer =DIFF_extent,
                  layer_hash = { "layer1" => DIFF },
                  window_function = density_DIFF,
                
                  delta_x = 1.0,
                  delta_y = 1.0,
                  statistics_files = sf1);}


//PO_FILL1 : polygon_layer = PO_FILL;
//DIFF_FILL1 : polygon_layer = DIFF_FILL ;


if (stagger == "N"){
gds_fh1 = gds_library("special_testgdsout.gds");
write_gds(gds_fh1, holding_cell = "*" ,output_cell = "POANT2",merge_input_layout = true, cell_prefix = "kkkt",  layers = {{PO_FILL,{10} },{DIFF_FILL,{3}},
        {NWELL      	,{1}},
	{DNW		,{2}},
	{DIFF		,{3}},
	{DDMY		,{3}},
	{PIMP		,{4}},
	{NIMP		,{5}},
	{DIFF_25	,{6}},
	{PAD		,{7}},
	{ESD_25		,{8}},
	{SBLK		,{9}},
	{PO		,{10}},
	{PODMY		,{10}},
	{M1		,{11}},
	{M1_TEXT	,{11}},
	{M1DMY		,{11}},
	{VIA1		,{12}},
	{M2		,{13}},
	{M2_TEXT	,{13}},
	{M2DMY		,{13}},
	{VIA2		,{14}},
	{M3		,{15}},
	{M3_TEXT	,{15}},
	{M3DMY		,{15}},
	{VIA3		,{16}},
	{M4		,{17}},
	{M4_TEXT	,{17}},
	{M4DMY		,{17}},
	{VIA4 		,{18}},
	{M5		,{19}},
	{M5_TEXT	,{19}},
	{M5DMY		,{19}},
	{VIA5		,{20}},
	{M6		,{21}},
	{M6_TEXT	,{21}},
	{M6DMY		,{21}},
	{VIA6		,{22}},
	{M7		,{23}},
	{M7_TEXT	,{23}},
	{M7DMY		,{23}},
	{M8		,{24}},
	{M8_TEXT	,{24}},
	{M8DMY		,{24}},
	{M9		,{25}},
	{M9_TEXT	,{25}},
	{M9DMY		,{25}},
	{CO		,{26}}, 
	{VIA7		,{27}},
	{VIA8		,{28}},
	{HVTIMP		,{29}},
	{LVTIMP		,{30}},
	{M1PIN		,{31}},
	{M1PIN_TEXT	,{31}},
	{M2PIN		,{32}},
	{M2PIN_TEXT	,{32}},
	{M3PIN		,{33}},
	{M3PIN_TEXT	,{33}},
	{M4PIN		,{34}},
	{M4PIN_TEXT	,{34}},
	{M5PIN		,{35}},
	{M5PIN_TEXT	,{35}},
	{M6PIN		,{36}},
	{M6PIN_TEXT	,{36}},
	{M7PIN		,{37}},
	{M7PIN_TEXT	,{37}},
	{M8PIN		,{38}},
	{M8PIN_TEXT	,{38}},
	{M9PIN		,{39}},
	{M9PIN_TEXT	,{39}},
	{HOTNWL		,{41}},
	{DIODMARK	,{43}},
	{BJTMARK	,{44}},
	{RNW		,{45}},
	{RMARKER	,{46}},
	{LOGO		,{48}},
	{IP		,{49}},
	{DM1EXCL 	,{61}},
	{DM2EXCL 	,{62}},
	{DM3EXCL 	,{63}},
	{DM4EXCL 	,{64}},
	{DM5EXCL 	,{65}},
	{DM6EXCL 	,{66}},
	{DM7EXCL 	,{67}},
	{DM8EXCL 	,{68}},
	{DM9EXCL 	,{69}},
	{DIFF_FM 	,{100}},
	{PO_FM 		,{101}}});
}elif(stagger == "Y"){
milkyway_fh1 = milkyway_library("special_testgdsout");
write_milkyway(milkyway_fh1, holding_cell = "*" ,output_cell = "POANT2",  layers = {{PO_FILL,{10} },{DIFF_FILL,{3}},

        {NWELL      	,{1}},
	{DNW		,{2}},
	{DIFF		,{3}},
	{DDMY		,{3}},
	{PIMP		,{4}},
	{NIMP		,{5}},
	{DIFF_25	,{6}},
	{PAD		,{7}},
	{ESD_25		,{8}},
	{SBLK		,{9}},
	{PO		,{10}},
	{PODMY		,{10}},
	{M1		,{11}},
	{M1_TEXT	,{11}},
	{M1DMY		,{11}},
	{VIA1		,{12}},
	{M2		,{13}},
	{M2_TEXT	,{13}},
	{M2DMY		,{13}},
	{VIA2		,{14}},
	{M3		,{15}},
	{M3_TEXT	,{15}},
	{M3DMY		,{15}},
	{VIA3		,{16}},
	{M4		,{17}},
	{M4_TEXT	,{17}},
	{M4DMY		,{17}},
	{VIA4 		,{18}},
	{M5		,{19}},
	{M5_TEXT	,{19}},
	{M5DMY		,{19}},
	{VIA5		,{20}},
	{M6		,{21}},
	{M6_TEXT	,{21}},
	{M6DMY		,{21}},
	{VIA6		,{22}},
	{M7		,{23}},
	{M7_TEXT	,{23}},
	{M7DMY		,{23}},
	{M8		,{24}},
	{M8_TEXT	,{24}},
	{M8DMY		,{24}},
	{M9		,{25}},
	{M9_TEXT	,{25}},
	{M9DMY		,{25}},
	{CO		,{26}}, 
	{VIA7		,{27}},
	{VIA8		,{28}},
	{HVTIMP		,{29}},
	{LVTIMP		,{30}},
	{M1PIN		,{31}},
	{M1PIN_TEXT	,{31}},
	{M2PIN		,{32}},
	{M2PIN_TEXT	,{32}},
	{M3PIN		,{33}},
	{M3PIN_TEXT	,{33}},
	{M4PIN		,{34}},
	{M4PIN_TEXT	,{34}},
	{M5PIN		,{35}},
	{M5PIN_TEXT	,{35}},
	{M6PIN		,{36}},
	{M6PIN_TEXT	,{36}},
	{M7PIN		,{37}},
	{M7PIN_TEXT	,{37}},
	{M8PIN		,{38}},
	{M8PIN_TEXT	,{38}},
	{M9PIN		,{39}},
	{M9PIN_TEXT	,{39}},
	{HOTNWL		,{41}},
	{DIODMARK	,{43}},
	{BJTMARK	,{44}},
	{RNW		,{45}},
	{RMARKER	,{46}},
	{LOGO		,{48}},
	{IP		,{49}},
	{DM1EXCL 	,{61}},
	{DM2EXCL 	,{62}},
	{DM3EXCL 	,{63}},
	{DM4EXCL 	,{64}},
	{DM5EXCL 	,{65}},
	{DM6EXCL 	,{66}},
	{DM7EXCL 	,{67}},
	{DM8EXCL 	,{68}},
	{DM9EXCL 	,{69}},
	{DIFF_FM 	,{100}},
	{PO_FM 		,{101}}});
}


