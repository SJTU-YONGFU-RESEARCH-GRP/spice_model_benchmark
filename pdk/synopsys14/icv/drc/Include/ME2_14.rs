
M2_extent = layer_extent(M2);

densityEQ_single_M2 : function(void) returning void
{
   areaL : double = den_polygon_area("layer1");
   areaW : double = den_window_area();
   RATIO : double = areaL / areaW;
   if (RATIO > 0.00000000001 || RATIO < 0.25)
   den_save_window (error_names = { "RATIO", "area" },
                            values = { RATIO, areaL });
}

{ @"Fill candidates within window";


             density(window_layer =M2_extent,
                  layer_hash = { "layer1" => M2 },
                  window_function = densityEQ_single_M2,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10,
                  delta_y = 10,
                  resize_delta_xy = true); 
}

candidates1_m2 = density(window_layer =M2_extent,
                  layer_hash = { "layer1" => M2 },
                  window_function = densityEQ_single_M2,
                  delta_window = {w_window ,  l_window},
                  delta_x = 10,
                  delta_y = 10,
                  resize_delta_xy = true); 

//layer_d :polygon_layer;
//blockage = cell_extent (cell_list = {});
sized_layer2 = size (M2, 0.085);
candidates_m2 = candidates1_m2 not M2DMY ;
fill_candidates_M2 = candidates_m2 not sized_layer2;
//bad_fill = interacting (fill_candidates1_m2,blockage);
//fill_candidates = fill_candidates1_m2 not bad_fill;
