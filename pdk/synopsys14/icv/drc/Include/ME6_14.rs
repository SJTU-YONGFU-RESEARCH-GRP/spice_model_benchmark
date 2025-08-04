
M6_extent = layer_extent(M6);

densityEQ_single_M6 : function(void) returning void
{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.00000000001 || RATIO < 0.14)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}

{ @"Fill candidates within window";


             density(window_layer =M6_extent,
                  layer_hash = { "layer1" => M6 },
                  window_function = densityEQ_single_M6,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10,
                  delta_y = 10,
                  resize_delta_xy = true); 
}

candidates1_m6 = density(window_layer =M6_extent,
                  layer_hash = { "layer1" => M6 },
                  window_function = densityEQ_single_M6,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10,
                  delta_y = 10,
                  resize_delta_xy = true); 

//layer_d :polygon_layer;
//blockage = cell_extent (cell_list = {});
sized_layer6 = size (M6, 0.085);
candidates_m6 = candidates1_m6 not M6DMY ;
fill_candidates_M6 = candidates_m6 not sized_layer6;
//bad_fill = interacting (fill_candidates1_m6,blockage);
//fill_candidates = fill_candidates1_m6 not bad_fill;
