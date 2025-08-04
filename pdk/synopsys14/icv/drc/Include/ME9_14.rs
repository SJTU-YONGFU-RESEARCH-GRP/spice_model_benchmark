
M9_extent = layer_extent(M9);

densityEQ_single_M9 : function(void) returning void
{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.00000000001 || RATIO < 0.14)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}

{ @"Fill candidates within window";


             density(window_layer =M9_extent,
                  layer_hash = { "layer1" => M9 },
                  window_function = densityEQ_single_M9,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10,
                  delta_y = 10,
                  resize_delta_xy = true); 
}

candidates1_m9 = density(window_layer =M9_extent,
                  layer_hash = { "layer1" => M9 },
                  window_function = densityEQ_single_M9,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10,
                  delta_y = 10,
                  resize_delta_xy = true); 

//layer_d :polygon_layer;
//blockage = cell_extent (cell_list = {});
sized_layer9 = size (M9, 0.085);
candidates_m9 = candidates1_m9 not M9DMY ;
fill_candidates_M9 = candidates_m9 not sized_layer9;
//bad_fill = interacting (fill_candidates1_m9,blockage);
//fill_candidates = fill_candidates1_m9 not bad_fill;
