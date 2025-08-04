
fillOutput1_m7  = fill_pattern( fill_candidates_M7,
                           fill_function = my_func1,
                          output_aref = {output_aref = true}

);


fillOutput1_1_m7 = size (fillOutput1_m7 , 0.2);
fill_candidates_s_m7 = fill_candidates_M7 not fillOutput1_1_m7;


fillOutput2_m7  = fill_pattern( fill_candidates_s_m7,
                           fill_function = my_func2,
                          output_aref = {output_aref = true}

);

fillOutput2_1_m7 = size (fillOutput2_m7 , 0.2);
fill_candidates_s_1_m7 = fill_candidates_s_m7 not fillOutput2_1_m7;

fillOutput3_m7  = fill_pattern( fill_candidates_s_1_m7,
                           fill_function = my_func3,
                          output_aref = {output_aref = true}

);

fillOutput_m7 = fillOutput2_m7 or fillOutput1_m7 or fillOutput3_m7;
////////////////////////////////////////

ME7D = fillOutput_m7 or M7;

ME7D_extent = layer_extent(ME7D);

sf7_global_end = density_statistics_file ("ME7.global.end");

densityEQ_single_ME7D : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.71)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}
