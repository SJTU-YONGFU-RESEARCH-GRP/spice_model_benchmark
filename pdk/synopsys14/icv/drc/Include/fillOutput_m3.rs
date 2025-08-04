
fillOutput1_m3  = fill_pattern( fill_candidates_M3,
                           fill_function = my_func1,
                          output_aref = {output_aref = true}

);


fillOutput1_1_m3 = size (fillOutput1_m3 , 0.2);
fill_candidates_s_m3 = fill_candidates_M3 not fillOutput1_1_m3;


fillOutput2_m3  = fill_pattern( fill_candidates_s_m3,
                           fill_function = my_func2,
                          output_aref = {output_aref = true}

);

fillOutput2_1_m3 = size (fillOutput2_m3 , 0.2);
fill_candidates_s_1_m3 = fill_candidates_s_m3 not fillOutput2_1_m3;

fillOutput3_m3  = fill_pattern( fill_candidates_s_1_m3,
                           fill_function = my_func3,
                          output_aref = {output_aref = true}

);

fillOutput_m3 = fillOutput2_m3 or fillOutput1_m3 or fillOutput3_m3;



/////////////////////////////////////////////
ME3D = fillOutput_m3 or M3;

ME3D_extent = layer_extent(ME3D);

sf3_global_end = density_statistics_file ("ME3.global.end");

densityEQ_single_ME3D : function(void) returning void

{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.71)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}
