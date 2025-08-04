
fillOutput1_m4  = fill_pattern( fill_candidates_M4,
                           fill_function = my_func1,
                          output_aref = {output_aref = true}

);


fillOutput1_1_m4 = size (fillOutput1_m4 , 0.2);
fill_candidates_s_m4 = fill_candidates_M4 not fillOutput1_1_m4;


fillOutput2_m4  = fill_pattern( fill_candidates_s_m4,
                           fill_function = my_func2,
                          output_aref = {output_aref = true}

);

fillOutput2_1_m4 = size (fillOutput2_m4 , 0.2);
fill_candidates_s_1_m4 = fill_candidates_s_m4 not fillOutput2_1_m4;

fillOutput3_m4  = fill_pattern( fill_candidates_s_1_m4,
                           fill_function = my_func3,
                          output_aref = {output_aref = true}

);

fillOutput_m4 = fillOutput2_m4 or fillOutput1_m4 or fillOutput3_m4;



///////////////////////////////////////////////////////ME4

ME4D = fillOutput_m4 or M4;

ME4D_extent = layer_extent(ME4D);

sf4_global_end = density_statistics_file ("ME4.global.end");

densityEQ_single_ME4D : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.71)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}
