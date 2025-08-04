/*
#########################################################################################
# SAED 32/28NM 1p9m icv  density drc deck						#
#											#
# Revision History:									#
# Rev.		date			what						#
# -------------------------------------------------------------------------------------	#	
# 1.0		--/---/2011		(First draft)					#
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
VIA1		=	assign({{21}});
M2		=	assign({{12}});
M2_TEXT		=	assign_text({{12}});
M2DMY		=	assign({{12},{1}});
VIA2		=	assign({{22}});
M3		=	assign({{13}});
M3_TEXT		=	assign_text({{13}});
M3DMY		=	assign({{13},{1}});
VIA3		=	assign({{23}});
M4		=	assign({{14}});
M4_TEXT		=	assign_text({{14}});
M4DMY		=	assign({{14},{1}});
VIA4 		=	assign({{24}});
M5		=	assign({{15}});
M5_TEXT		=	assign_text({{15}});
M5DMY		=	assign({{15},{1}});
VIA5		=	assign({{25}});
M6		=	assign({{16}});
M6_TEXT		=	assign_text({{16}});
M6DMY		=	assign({{16},{1}});
VIA6		=	assign({{26}});
M7		=	assign({{17}});
M7_TEXT		=	assign_text({{27}});
M7DMY		=	assign({{17},{1}});
M8		=	assign({{18}});
M8_TEXT		=	assign_text({{18}});
M8DMY		=	assign({{18},{1}});
M9		=	assign({{19}});
M9_TEXT		=	assign_text({{19}});
M9DMY		=	assign({{19},{1}});
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
VARMARK 	=	assign({{70}});
CBMMARK 	=	assign({{71}});
INDMARK 	=	assign({{72}});
CTMMARK	        =	assign({{73}});
METDMY  	=	assign({{74}});
PWELL   	=	assign({{75}});
DIFF_33	        =	assign({{76}});



densityEQ_PO : function(void) returning void
{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (areaW > 0 && (RATIO < 0.2 || RATIO > 0.75))
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}
PO_extent = layer_extent(PO);


{ @"PO.DN.1 Density across window";
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
   if (areaW > 0 &&(RATIO < 0.15 || RATIO > 0.85))
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}
DIFF_extent = layer_extent(DIFF);


{ @"DIFF.DN.1 Density across window";
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
   if (areaW > 0 && (RATIO < 0.15 || RATIO > 0.4))
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}

sf = density_statistics_file ("PO.global.start");

PO_extent = layer_extent(PO);
{ @"PO.DN.1 Densisty across chip";
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
   if (areaW > 0 && (RATIO < 0.2 || RATIO > 0.8))
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}

sf1 = density_statistics_file ("DIFF.global.start");

DIFF_extent = layer_extent(DIFF);
{ @"DIFF.DN.1 Densisty across chip";
        density(window_layer =DIFF_extent,
                  layer_hash = { "layer1" => DIFF },
                  window_function = density_DIFF,
                
                  delta_x = 1.0,
                  delta_y = 1.0,
                  statistics_files = sf1);}



ME1 = M1DMY or M1;

ME1_extent = layer_extent(ME1);

sf1_global_start = density_statistics_file ("ME1.global.start");

densityEQ_single_ME1 : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (areaW > 0 && RATIO > 0.7)
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
   if (areaW > 0 && RATIO > 0.71)
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
   if (areaW > 0 && RATIO > 0.71)
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
   if (areaW > 0 && RATIO > 0.71)
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
   if (areaW > 0 && RATIO > 0.71)
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
   if (areaW > 0 && RATIO > 0.71)
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
   if (areaW > 0 && RATIO > 0.71)
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
   if (areaW > 0 && RATIO > 0.71)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}



{ @"M1.DN.1 Densisty across chip";


             density(window_layer = ME1_extent,
                  layer_hash = { "layer1" => ME1 },
                  window_function = densityEQ_single_ME1,
                  statistics_files = sf1_global_start 
                  ); 
}
  	     

{ @"M2.DN.1 Densisty across chip";
density(window_layer = ME2_extent,
                  layer_hash = { "layer1" => ME2 },
                  window_function = densityEQ_single_ME2,
                  statistics_files = sf2_global_start 
                  ); 
}

{ @"M3.DN.1 Densisty across chip";
	     density(window_layer = ME3_extent,
                  layer_hash = { "layer1" => ME3 },
                  window_function = densityEQ_single_ME3,
                  statistics_files = sf3_global_start 
                  ); 
}

{ @"M4.DN.1 Densisty across chip";	
	     density(window_layer = ME4_extent,
                  layer_hash = { "layer1" => ME4 },
                  window_function = densityEQ_single_ME4,
                  statistics_files = sf4_global_start 
                  );
}
{ @"M5.DN.1 Densisty across chip";
 	    density(window_layer = ME5_extent,
                  layer_hash = { "layer1" => ME5 },
                  window_function = densityEQ_single_ME5,
                  statistics_files = sf5_global_start 
                  ); 
	}
{ @"M6.DN.1 Densisty across chip";	
	     density(window_layer = ME6_extent,
                  layer_hash = { "layer1" => ME6 },
                  window_function = densityEQ_single_ME6,
                  statistics_files = sf6_global_start 
                  );
}

{ @"M7.DN.1 Densisty across chip";
       	     density(window_layer = ME7_extent,
                  layer_hash = { "layer1" => ME7 },
                  window_function = densityEQ_single_ME7,
                  statistics_files = sf7_global_start 
                  ); 
	}
{ @"M8.DN.1 Densisty across chip";	
	     density(window_layer = ME8_extent,
                  layer_hash = { "layer1" => ME8 },
                  window_function = densityEQ_single_ME8,
                  statistics_files = sf8_global_start 
                  );
}
/*
 	     density(window_layer =ME9_extent,
                  layer_hash = { "layer1" => ME9 },
                  window_function = densityEQ_single_ME9,
                  statistics_files = sf9_global_start 
                  );*/







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


w_window : double = 10;
l_window : double = 10;

///////////////////////////////////////////////////////
densityEQ_ME : function(void) returning void
{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (areaW > 0 && RATIO > 0.9)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}


{ @"M1.DN.1 Density across window";


             density(window_layer = ME1_extent,
                  layer_hash = { "layer1" => ME1 },
                  window_function = densityEQ_ME,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  statistics_files = sf1_window_start 
                  ); 
}

{ @"M2.DN.1 Density across window";	
             density(window_layer = ME2_extent,
                  layer_hash = { "layer1" => ME2 },
                  window_function = densityEQ_ME,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  statistics_files = sf2_window_start 
                  ); 
}
{ @"M3.DN.1 Density across window";
	     density(window_layer = ME3_extent,
                  layer_hash = { "layer1" => ME3 },
                  window_function = densityEQ_ME,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  statistics_files = sf3_window_start 
                  ); 
}

{ @"M4.DN.1 Density across window";
	     density(window_layer = ME4_extent,
                  layer_hash = { "layer1" => ME4 },
                  window_function = densityEQ_ME,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  statistics_files = sf4_window_start 
                  ); 
}

{ @"M5.DN.1 Density across window";
	     density(window_layer = ME5_extent,
                  layer_hash = { "layer1" => ME5 },
                  window_function = densityEQ_ME,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  statistics_files = sf5_window_start 
                  ); 
}

{ @"M6.DN.1 Density across window";
	     density(window_layer = ME6_extent,
                  layer_hash = { "layer1" => ME6 },
                  window_function = densityEQ_ME,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  statistics_files = sf6_window_start 
                  ); 

  }

{ @"M7.DN.1 Density across window";
	     density(window_layer = ME7_extent,
                  layer_hash = { "layer1" => ME7 },
                  window_function = densityEQ_ME,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  statistics_files = sf7_window_start 
                  ); 
}

{ @"M8.DN.1 Density across window";
	     density(window_layer = ME8_extent,
                  layer_hash = { "layer1" => ME8 },
                  window_function = densityEQ_ME,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  statistics_files = sf8_window_start 
                  ); 
}
   	   /*density(window_layer = ME9_extent,
                  layer_hash = { "layer1" => ME9 },
                  window_function = densityEQ_ME,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10.0,
                  delta_y = 10.0,
                  statistics_files = sf9_window_start 
                  ); */





