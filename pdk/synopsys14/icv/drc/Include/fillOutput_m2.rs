
fillOutput1_m2  = fill_pattern( fill_candidates_M2,
                           fill_function = my_func1,
                          output_aref = {output_aref = true}

);


fillOutput1_1_m2 = size (fillOutput1_m2 , 0.2);
fill_candidates_s_m2 = fill_candidates_M2 not fillOutput1_1_m2;


fillOutput2_m2  = fill_pattern( fill_candidates_s_m2,
                           fill_function = my_func2,
                          output_aref = {output_aref = true}

);

fillOutput2_1_m2 = size (fillOutput2_m2 , 0.2);
fill_candidates_s_1_m2 = fill_candidates_s_m2 not fillOutput2_1_m2;

fillOutput3_m2  = fill_pattern( fill_candidates_s_1_m2,
                           fill_function = my_func3,
                          output_aref = {output_aref = true}

);

fillOutput_m2 = fillOutput2_m2 or fillOutput1_m2 or fillOutput3_m2;


////////////////////////////////////////////////////

ME2D = fillOutput_m2 or M2;

ME2D_extent = layer_extent(ME2D);

sf2_global_end = density_statistics_file ("ME2.global.end");

densityEQ_single_ME2D : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.71)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}
