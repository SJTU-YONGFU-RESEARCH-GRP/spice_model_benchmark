
fillOutput1_m9  = fill_pattern( fill_candidates_M9,
                           fill_function = my_func1,
                          output_aref = {output_aref = true}

);


fillOutput1_1_m9 = size (fillOutput1_m9 , 0.2);
fill_candidates_s_m9 = fill_candidates_M9 not fillOutput1_1_m9;


fillOutput2_m9  = fill_pattern( fill_candidates_s_m9,
                           fill_function = my_func2,
                          output_aref = {output_aref = true}

);

fillOutput2_1_m9 = size (fillOutput2_m9 , 0.2);
fill_candidates_s_1_m9 = fill_candidates_s_m9 not fillOutput2_1_m9;

fillOutput3_m9  = fill_pattern( fill_candidates_s_1_m9,
                           fill_function = my_func3,
                          output_aref = {output_aref = true}

);

fillOutput_m9 = fillOutput2_m9 or fillOutput1_m9 or fillOutput3_m9;
//////////////////////////////////////////////


ME9D = fillOutput_m9 or M9;

ME9D_extent = layer_extent(ME9D);

sf9_global_end = density_statistics_file ("ME9.global.end");

densityEQ_single_ME9D : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.6)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}
