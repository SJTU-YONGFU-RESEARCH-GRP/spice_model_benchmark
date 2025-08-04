
fillOutput1_m8  = fill_pattern( fill_candidates_M8,
                           fill_function = my_func1,
                          output_aref = {output_aref = true}

);


fillOutput1_1_m8 = size (fillOutput1_m8 , 0.2);
fill_candidates_s_m8 = fill_candidates_M8 not fillOutput1_1_m8;


fillOutput2_m8  = fill_pattern( fill_candidates_s_m8,
                           fill_function = my_func2,
                          output_aref = {output_aref = true}

);

fillOutput2_1_m8 = size (fillOutput2_m8 , 0.2);
fill_candidates_s_1_m8 = fill_candidates_s_m8 not fillOutput2_1_m8;

fillOutput3_m8  = fill_pattern( fill_candidates_s_1_m8,
                           fill_function = my_func3,
                          output_aref = {output_aref = true}

);

fillOutput_m8 = fillOutput2_m8 or fillOutput1_m8 or fillOutput3_m8;
///////////////////////////////////////////////////

ME8D = fillOutput_m8 or M8;

ME8D_extent = layer_extent(ME8D);

sf8_global_end = density_statistics_file ("ME8.global.end");

densityEQ_single_ME8D : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.71)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}
