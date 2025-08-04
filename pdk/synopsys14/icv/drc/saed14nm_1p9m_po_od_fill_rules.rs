/*
#########################################################################################
# SAED 14NM 1p9m icv poly od fill deck							#
#											#
# Revision History:									#
# Rev.		date			what						#
# -------------------------------------------------------------------------------------	#	
# 1.0		24/Sep/2017		(First draft)					#
#											#
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


FIN             =	 assign({{1}});
FINCUT          =	 assign({{2}});
NWELL           =	 assign({{3}});
DNW             =	 assign({{4}});
DIFF            =	 assign({{5}});
DDMY            =	 assign({{5},{1}});
PIMP            =	 assign({{6}});
NIMP            =	 assign({{7}});
DIFF_15         =	 assign({{8}});
DIFF_18         =	 assign({{9}});
PAD             =	 assign({{10}});
ESD             =	 assign({{11}});
SBLK            =	 assign({{12}});
PO              =	 assign({{13}});
POCUT      	=	 assign({{14}});
PODMY           =	 assign({{13,1}});
TSLCO           =	 assign({{15}});
TSLCB           =	 assign({{16}});
CTM1            =	 assign({{17}});
CTM1_1      	=	 assign({{17}, {1}});
CTM1_2      	=	 assign({{17}, {2}});
CPO             =	 assign({{18}});
CPO_1       	=	 assign({{18}, {1}});
CPO_2       	=	 assign({{18}, {2}});
VIA0            =	 assign({{81}});
M1              =	 assign({{19}});
M1_3            =	 assign({{90}});
M1DMY           =	 assign({{19},{1}});
M1_text         =	 assign_text({{19}});
VIA1            =	 assign({{20}});
M2              =	 assign({{21}});
M2_3            =	 assign({{91}});
M2_text         =	 assign_text({{21}});
VIA2            =	 assign({{22}});
M2DMY           =	 assign({{21},{1}});
M3              =	 assign({{23}});
M3_3            =	 assign({{92}});
M3_text         =	 assign_text({{23}});
M3DMY           =	 assign({{23},{1}});
VIA3            =	 assign({{24}});
M4              =	 assign({{25}});
M4_text         =	 assign_text({{25}});
M4DMY           =	 assign({{25},{1}});
VIA4            =	 assign({{26}});
M5              =	 assign({{27}});
M5_text         =	 assign_text({{27}});
VIA5            =	 assign({{28}});
M6              =	 assign({{29}});
M6_text         =	 assign_text({{29}});
M6DMY           =	 assign({{29},{1}});
VIA6            =	 assign({{30}});
M7              =	 assign({{31}});
M7_text         =	 assign_text({{31}});
M7DMY           =	 assign({{31},{1}});
VIA7            =	 assign({{32}});
M8              =	 assign({{33}});
M8_text         =	 assign_text({{33}});
M8DMY           =	 assign({{33},{1}});
VIA8            =	 assign({{34}});
M9              = 	 assign({{35}});
M9_text         = 	 assign({{35}});
M9DMY           = 	 assign({{35},{1}});
HVTIMP          = 	 assign({{36}});
LVTIMP          = 	 assign({{37}});
M1PIN           = 	 assign({{38}});
M1PIN_text      = 	 assign_text({{38}});
M2PIN           = 	 assign({{39}});
M2PIN_text      = 	 assign_text({{39}});
M3PIN           = 	 assign({{40}});
M3PIN_text      = 	 assign_text({{40}});
M4PIN           = 	 assign({{41}});
M4PIN_text      = 	 assign_text({{41}});
M5PIN           = 	 assign({{42}});
M5PIN_text      = 	 assign_text({{42}});
M6PIN           = 	 assign({{43}});
M6PIN_text      = 	 assign_text({{43}});
M7PIN           = 	 assign({{44}});
M7PIN_text      = 	 assign_text({{44}});
M8PIN           =	 assign({{45}});
M8PIN_text      =	 assign_text({{45}});
M9PIN           =	 assign({{46}});
M9PIN_text      =	 assign_text({{46}});
MRDL            =	 assign({{47}});
VIARDL          =	 assign({{48}});
MRPIN           =	 assign({{49}});
HOTNWL          =	 assign({{50}});
DIOD            =	 assign({{51}});
BJTMY           =	 assign({{52}});
RNW             =	 assign({{53}});
RMARK           =	 assign({{54}});
LOGO            =	 assign({{56}});
IP              =	 assign({{57}});
RM1             =	 assign({{58}});
RM2             =	 assign({{59}});
RM3             =	 assign({{60}});
RM4             =	 assign({{61}});
RM5             =	 assign({{62}});
RM6             =	 assign({{63}});
RM7             =	 assign({{64}});
RM8             =	 assign({{65}});
RM9             =	 assign({{66}});
DIFFCUT    	=	 assign({{82}});
AXPOLY      	=	 assign({{83}});
SLVTIMP     	=	 assign({{84}});
FGATE           =	 assign({{85}});
B_VIA0      	=	 assign({{86}});



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
sized_layer = size (PO,  distance = 0.33, processing_mode = CELL_LEVEL ); 
navs1 = size (DIFF,  distance = 0.33, processing_mode = CELL_LEVEL ); 
navs = navs1 or PO;
candidates = candidates1 ;// not PO_FM;
//syzed_layer = size (PO,  distance = 0.2,processing_mode = CELL_LEVEL ); 
fill_candidates2 = candidates not sized_layer;

fill_candidates =  fill_candidates2 not navs; 
//bad_fill = fill_candidates1 interacting blockage;
// fill_candidates =  fill_candidates1 not bad_fill;



my_func1: function ( void ) returning void{
   strike : polygon = fp_get_current_polygon();
   fp_generate_fill(
      polygon = strike,
      width = 0.05,
      height = 0.2,
      space_x = 0.2,
      space_y = 0.2,
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
      width = 0.05,
      height = 0.4,
      space_x = 0.2,
      space_y = 0.2,
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
      width = 0.1,
      height = 0.1,
      space_x = 0.1,
      space_y = 0.1,
      stagger_x = 0.05,
      stagger_y = 0.05
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
      width = 0.1,
      height = 0.3,
      space_x = 0.1,
      space_y = 0.1,
      stagger_x = 0.06,
      stagger_y = 0.06
     );
}


PO_FILL = copy (fillOutput_PO) ;
POD = PO_FILL or PO;












od_fill_rect_1   = fill_pattern( fillOutput2,
                           fill_function = my_func4,
                          output_aref = {output_aref = true}

);

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
sized_layer_1 = size (DIFF,  distance = 0.33, processing_mode = CELL_LEVEL ); 
navs1_1 = size (PO,  distance = 0.33, processing_mode = CELL_LEVEL ); 
navs2 = size (PODMY,  distance = 0.33,processing_mode = CELL_LEVEL );
navs3 = size (DDMY,  distance =0.33,processing_mode = CELL_LEVEL );
navs_1 =  (navs1_1 or navs2 or navs3);
candidates_1 =  candidates1_1; //not DIFF_FM;
fill_candidates2_1 =  candidates_1 not sized_layer_1;
fill_candidates1_1 =  fill_candidates2_1 not navs_1; 
bad_fill_1 = fill_candidates1_1 interacting blockage_1;
//fill_candidates3_1 =  fill_candidates1 not bad_fill_1;
syzed_PODMY_1 = size (fillOutput_PO,  distance = 0.33,processing_mode = CELL_LEVEL ); 
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
      width = 0.05,
      height = 0.5,
      space_x = 0.1,
      space_y = 0.1,
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
write_gds(gds_fh1, holding_cell = "*" ,output_cell = "POANT2",merge_input_layout = true, cell_prefix = "kkkt",  layers = {{PO_FILL,{14} },{DIFF_FILL,{5}},
       
	{FIN      	,{1}},
	{FINCUT      	,{2}},
	{NWELL      	,{3}},
	{DNW		,{4}},
	{DIFF		,{5}},
	{DDMY		,{5}},
	{PIMP		,{6}},
	{NIMP		,{7}},
	{DIFF_15	,{8}},
	{DIFF_18  	,{9}},
	{PAD		,{10}},
	{ESD		,{11}},
	{SBLK		,{12}},
	{PO		,{13}},
	{POCUT		,{14}},
	{PODMY		,{14}},
	{TSLCO		,{15}},
	{TSLCB		,{16}},
	{CTM1		,{17}},
	{CTM1_1		,{17}},
	{CTM1_2		,{17}},
	{CPO		,{18}},
	{CPO_1		,{18}},
	{CPO_2		,{18}},
	{VIA0		,{81}},
	{M1		,{19}},
	{M1_3		,{90}},
	{M1_text	,{19}},
	{M1DMY		,{19}},
	{VIA1		,{20}},
	{M2		,{21}},
	{M2_3		,{91}},
	{M2_text	,{21}},
	{M2DMY		,{21}},
	{VIA2		,{22}},
	{M3		,{23}},
	{M3_3		,{92}},
	{M3_text	,{23}},
	{M3DMY		,{23}},
	{VIA3		,{24}},
	{M4		,{25}},
	{M4_text	,{25}},
	{M4DMY		,{25}},
	{VIA4 		,{26}},
	{M5		,{27}},
	{M5_text	,{27}},
//	{M5DMY		,{27}},
	{VIA5		,{28}},
	{M6		,{29}},
	{M6_text	,{29}},
	{M6DMY		,{29}},
	{VIA6		,{30}},
	{M7		,{31}},
	{M7_text	,{31}},
	{M7DMY		,{31}},
	{VIA7		,{32}},
	{M8		,{33}},
	{M8_text	,{33}},
	{M8DMY		,{33}},
	{VIA8		,{34}},
	{M9		,{35}},
	{M9_text	,{35}},
	{M9DMY		,{35}},
	{HVTIMP		,{36}},
	{LVTIMP		,{37}},
	{M1PIN		,{38}},
	{M1PIN_text	,{38}},
	{M2PIN		,{39}},
	{M2PIN_text	,{39}},
	{M3PIN		,{40}},
	{M3PIN_text	,{40}},
	{M4PIN		,{41}},
	{M4PIN_text	,{41}},
	{M5PIN		,{42}},
	{M5PIN_text	,{42}},
	{M6PIN		,{43}},
	{M6PIN_text	,{43}},
	{M7PIN		,{44}},
	{M7PIN_text	,{44}},
	{M8PIN		,{45}},
	{M8PIN_text	,{45}},
	{M9PIN		,{46}},
	{M9PIN_text	,{46}},
	{MRDL		,{47}},
	{VIARDL		,{48}},
	{MRPIN		,{49}},
	{HOTNWL		,{50}},
	{DIOD		,{51}},
	{BJTMY		,{52}},
	{RNW		,{53}},
	{RMARK		,{54}},
	{LOGO		,{56}},
	{IP		,{57}},
	{RM1	 	,{58}},
	{RM2	 	,{59}},
	{RM3	 	,{60}},
	{RM4	 	,{61}},
	{RM5	 	,{62}},
	{RM6	 	,{63}},
	{RM7	 	,{64}},
	{RM8	 	,{65}},
	{RM9	 	,{66}},
	{DIFFCUT	,{82}},
	{AXPOLY		,{83}},
	{SLVTIMP	,{84}},
	{FGATE	 	,{85}},
	{B_VIA0		,{86}}});
}elif(stagger == "Y"){
milkyway_fh1 = milkyway_library("special_testgdsout");
write_milkyway(milkyway_fh1, holding_cell = "*" ,output_cell = "POANT2",  layers = {{PO_FILL,{14} },{DIFF_FILL,{5}},
	

        {FIN            ,{1}},
        {FINCUT         ,{2}},
        {NWELL          ,{3}},
        {DNW            ,{4}},
        {DIFF           ,{5}},
        {DDMY           ,{5}},
        {PIMP           ,{6}},
        {NIMP           ,{7}},
        {DIFF_15        ,{8}},
        {DIFF_18        ,{9}},
        {PAD            ,{10}},
        {ESD            ,{11}},
        {SBLK           ,{12}},
        {PO             ,{13}},
        {POCUT          ,{14}},
        {PODMY          ,{14}},
        {TSLCO          ,{15}},
        {TSLCB          ,{16}},
        {CTM1           ,{17}},
        {CTM1_1         ,{17}},
        {CTM1_2         ,{17}},
        {CPO            ,{18}},
        {CPO_1          ,{18}},
        {CPO_2          ,{18}},
        {VIA0           ,{81}},
        {M1             ,{19}},
        {M1_3           ,{90}},
        {M1_text        ,{19}},
        {M1DMY          ,{19}},
        {VIA1           ,{20}},
        {M2             ,{21}},
        {M2_3           ,{91}},
        {M2_text        ,{21}},
        {M2DMY          ,{21}},
        {VIA2           ,{22}},
        {M3             ,{23}},
        {M3_3           ,{92}},
        {M3_text        ,{23}},
        {M3DMY          ,{23}},
        {VIA3           ,{24}},
        {M4             ,{25}},
        {M4_text        ,{25}},
        {M4DMY          ,{25}},
        {VIA4           ,{26}},
        {M5             ,{27}},
        {M5_text        ,{27}},
//      {M5DMY          ,{27}},
        {VIA5           ,{28}},
        {M6             ,{29}},
        {M6_text        ,{29}},
        {M6DMY          ,{29}},
        {VIA6           ,{30}},
        {M7             ,{31}},
        {M7_text        ,{31}},
        {M7DMY          ,{31}},
        {VIA7           ,{32}},
        {M8             ,{33}},
        {M8_text        ,{33}},
        {M8DMY          ,{33}},
        {VIA8           ,{34}},
        {M9             ,{35}},
        {M9_text        ,{35}},
        {M9DMY          ,{35}},
        {HVTIMP         ,{36}},
        {LVTIMP         ,{37}},
        {M1PIN          ,{38}},
        {M1PIN_text     ,{38}},
        {M2PIN          ,{39}},
        {M2PIN_text     ,{39}},
        {M3PIN          ,{40}},
        {M3PIN_text     ,{40}},
        {M4PIN          ,{41}},
        {M4PIN_text     ,{41}},
        {M5PIN          ,{42}},
        {M5PIN_text     ,{42}},
        {M6PIN          ,{43}},
        {M6PIN_text     ,{43}},
        {M7PIN          ,{44}},
        {M7PIN_text     ,{44}},
        {M8PIN          ,{45}},
        {M8PIN_text     ,{45}},
        {M9PIN          ,{46}},
        {M9PIN_text     ,{46}},
        {MRDL           ,{47}},
        {VIARDL         ,{48}},
        {MRPIN          ,{49}},
        {HOTNWL         ,{50}},
        {DIOD           ,{51}},
        {BJTMY          ,{52}},
        {RNW            ,{53}},
        {RMARK          ,{54}},
        {LOGO           ,{56}},
        {IP             ,{57}},
        {RM1            ,{58}},
        {RM2            ,{59}},
        {RM3            ,{60}},
        {RM4            ,{61}},
        {RM5            ,{62}},
        {RM6            ,{63}},
        {RM7            ,{64}},
        {RM8            ,{65}},
        {RM9            ,{66}},
        {DIFFCUT        ,{82}},
        {AXPOLY         ,{83}},
        {SLVTIMP        ,{84}},
        {FGATE          ,{85}},
        {B_VIA0         ,{86}}});

}

