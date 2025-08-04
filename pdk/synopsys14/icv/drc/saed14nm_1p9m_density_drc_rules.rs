/*
#########################################################################################
# SAED 14NM 1p9m icv  density drc deck						#
#											#
# Revision History:									#
# Rev.		date			what						#
# -------------------------------------------------------------------------------------	#	
# 1.0		16/Aug/2017		(First draft)					#
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


FIN    		=	 assign({{1}});
FINCUT    	=	 assign({{2}});
NWELL    	=	 assign({{3}});
DNW	  	=	 assign({{4}});
DIFF	  	=	 assign({{5}});	
DDMY     	=	 assign({{5},{1}});
PIMP	  	=	 assign({{6}});
NIMP	  	=	 assign({{7}});
DIFF_15  	=	 assign({{8}});
DIFF_18  	=	 assign({{9}});
PAD	  	=	 assign({{10}});
ESD	  	=	 assign({{11}});
SBLK	  	=	 assign({{12}});
PO       	=	 assign({{13}});
POCUT  		=	 assign({{14}});
PODMY    	=	 assign({{13,1}});
TSLCO    	=	 assign({{15}});
TSLCB    	=	 assign({{16}});
CTM1       	=	 assign({{17}});
CTM1_1     	=	 assign({{17}, {1}});
CTM1_2      	=	 assign({{17}, {2}});
CPO       	=	 assign({{18}});
CPO_1       	=	 assign({{18}, {1}});
CPO_2       	=	 assign({{18}, {2}});
VIA0     	=	 assign({{81}});
M1       	=	 assign({{19}});
M1_3	  	=	 assign({{90}});		
M1DMY    	=	 assign({{19},{1}});
M1_text  	=	 assign_text({{19}});
VIA1     	=	 assign({{20}});
M2       	=	 assign({{21}});
M2_3	  	=	 assign({{91}});		
M2_text  	=	 assign_text({{21}});
VIA2    	=	 assign({{22}});
M2DMY    	=	 assign({{21},{1}});
M3       	=	 assign({{23}});
M3_3       	=	 assign({{92}});		
M3_text  	=	 assign_text({{23}});
M3DMY    	=	 assign({{23},{1}});
VIA3    	=	 assign({{24}});
M4       	=	 assign({{25}});
M4_text  	=	 assign_text({{25}}); 
M4DMY    	=	 assign({{25},{1}});      
VIA4    	=	 assign({{26}});
M5       	=	 assign({{27}}); 
M5_text  	=	 assign_text({{27}});   
VIA5    	=	 assign({{28}});
M6       	=	 assign({{29}});    
M6_text  	=	 assign_text({{29}});
M6DMY    	=	 assign({{29},{1}});
VIA6     	=	 assign({{30}});
M7       	=	 assign({{31}});
M7_text  	=	 assign_text({{31}});   
M7DMY    	=	 assign({{31},{1}}); 
VIA7     	=	 assign({{32}});
M8       	=	 assign({{33}});
M8_text  	=	 assign_text({{33}});
M8DMY    	=	 assign({{33},{1}});
VIA8     	=	 assign({{34}});    
M9       	=	 assign({{35}});   
M9_text  	=	 assign({{35}});
M9DMY    	=	 assign({{35},{1}});  
HVTIMP  	=	 assign({{36}});
LVTIMP   	=	 assign({{37}});
M1PIN     	=	 assign({{38}});
M1PIN_text 	=	 assign_text({{38}});
M2PIN     	=	 assign({{39}});
M2PIN_text 	=	 assign_text({{39}});
M3PIN     	=	 assign({{40}});
M3PIN_text 	=	 assign_text({{40}});
M4PIN     	=	 assign({{41}});
M4PIN_text 	=	 assign_text({{41}});
M5PIN     	=	 assign({{42}});
M5PIN_text 	=	 assign_text({{42}});
M6PIN     	=	 assign({{43}});
M6PIN_text 	=	 assign_text({{43}});
M7PIN     	=	 assign({{44}});
M7PIN_text 	=	 assign_text({{44}});
M8PIN     	=	 assign({{45}});
M8PIN_text 	=	 assign_text({{45}});
M9PIN     	=	 assign({{46}});
M9PIN_text 	=	 assign_text({{46}});
MRDL      	=	 assign({{47}});
VIARDL	   	=	 assign({{48}});
MRPIN      	=	 assign({{49}});
HOTNWL    	=	 assign({{50}});
DIOD      	=	 assign({{51}});
BJTMY     	=	 assign({{52}});
RNW      	=	 assign({{53}});
RMARK     	=	 assign({{54}});
LOGO      	=	 assign({{56}});
IP        	=	 assign({{57}});
RM1      	=	 assign({{58}});
RM2      	=	 assign({{59}});
RM3      	=	 assign({{60}});
RM4      	=	 assign({{61}});
RM5      	=	 assign({{62}});
RM6      	=	 assign({{63}});
RM7      	=	 assign({{64}});	
RM8      	=	 assign({{65}});
RM9      	=	 assign({{66}});
DIFFCUT  	=	 assign({{82}});
AXPOLY      	= 	 assign({{83}});
SLVTIMP    	=	 assign({{84}});
FGATE		=	 assign({{85}});
B_VIA0     	= 	 assign({{86}});


densityEQ_PO : function(void) returning void
{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (areaW > 0 && (RATIO < 0.1 || RATIO > 0.45))
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
   if (areaW > 0 &&(RATIO < 0.1 || RATIO > 0.7))
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
   if (areaW > 0 && (RATIO < 0.025 || RATIO > 0.35))
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




