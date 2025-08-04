
fillOutput1_m6  = fill_pattern( fill_candidates_M6,
                           fill_function = my_func1,
                          output_aref = {output_aref = true}

);


fillOutput1_1_m6 = size (fillOutput1_m6 , 0.2);
fill_candidates_s_m6 = fill_candidates_M6 not fillOutput1_1_m6;


fillOutput2_m6  = fill_pattern( fill_candidates_s_m6,
                           fill_function = my_func2,
                          output_aref = {output_aref = true}

);

fillOutput2_1_m6 = size (fillOutput2_m6 , 0.2);
fill_candidates_s_1_m6 = fill_candidates_s_m6 not fillOutput2_1_m6;

fillOutput3_m6  = fill_pattern( fill_candidates_s_1_m6,
                           fill_function = my_func3,
                          output_aref = {output_aref = true}

);

fillOutput_m6 = fillOutput2_m6 or fillOutput1_m6 or fillOutput3_m6;


////////////////////////////////////////////////////////////

ME6D = fillOutput_m6 or M6;

ME6D_extent = layer_extent(ME6D);

sf6_global_end = density_statistics_file ("ME6.global.end");

densityEQ_single_ME6D : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.71)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}
