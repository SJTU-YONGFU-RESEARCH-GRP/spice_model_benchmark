
fillOutput1_m5  = fill_pattern( fill_candidates_M5,
                           fill_function = my_func1,
                          output_aref = {output_aref = true}

);


fillOutput1_1_m5 = size (fillOutput1_m5 , 0.2);
fill_candidates_s_m5 = fill_candidates_M5 not fillOutput1_1_m5;


fillOutput2_m5  = fill_pattern( fill_candidates_s_m5,
                           fill_function = my_func2,
                          output_aref = {output_aref = true}

);

fillOutput2_1_m5 = size (fillOutput2_m5 , 0.2);
fill_candidates_s_1_m5 = fill_candidates_s_m5 not fillOutput2_1_m5;

fillOutput3_m5  = fill_pattern( fill_candidates_s_1_m5,
                           fill_function = my_func3,
                          output_aref = {output_aref = true}

);

fillOutput_m5 = fillOutput2_m5 or fillOutput1_m5 or fillOutput3_m5;



////////////////////////////////////
ME5D = fillOutput_m5 or M5;

ME5D_extent = layer_extent(ME5D);

sf5_global_end = density_statistics_file ("ME5.global.end");

densityEQ_single_ME5D : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.71)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}
