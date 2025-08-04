
;; VALEdeviceTypeMarker(geGetWindowCellView() "create" "model" "pmos_hvt" 
;;                         list(list("PIMP" "drawing")) 0.02 t)
;; VALEdeviceTypeMarker(geGetWindowCellView() "remove") 

procedure(VALEdeviceTypeMarker(cv action 
             @optional (parName "par") (parValue "val") (lpp list(list("layer"
             "drawing"))) (boxWidth 0.01) (debug nil))
   prog((cdfgData parId bBox origin rv prop)
      if(action == "create" then
         foreach(inst cv~>instances
            when(inst~>libName == _IMFdat->techLib
               ;; Get CDF
               cdfgData = cdfGetInstCDF(inst)
               parId = cdfFindParamByName(cdfgData parName)
               if(parId then
                  when(debug
                     printf("VALE DEBUG: Checking parameter %L...\n" parName)
                  )
                  if(rexMatchp(parValue parId~>value) then 
                     when(debug
                        printf("VALE DEBUG: %L...\n" parId~>value)
                     )
                     ;; Create a marker
                     foreach(lyrpurp lpp
                        origin = inst~>xy
                        bBox = list(origin car(origin)+boxWidth:cadr(origin)+boxWidth)
                        rv = dbCreateRect(cv lyrpurp bBox)
                        unless(rv
                           printf("VALE ERROR: Failed to create the device ")
                           printf("marker\n")
                           return()
                        )
                        ;; Create prop
                        unless(dbCreateProp(rv "imfGenerated" 'string 
                           "DeviceMarker")
                           printf("VALE ERROR: Failed to tag the device ")
                           printf("marker\n")
                           return()
                        )
                     )
                  else
                     when(debug
                        printf("VALE DEBUG: No match, %L...\n" parId~>value)
                     )
              
                  )
               else
                  when(debug
                     printf("VALE WARNING: No CDF parameter named %L " parName)
                     printf("found on the current PCell.\n")
                  )
               )
            )
         )
      else
         if(action == "remove" then
            foreach(shape cv~>shapes
               prop = dbFindProp(shape "imfGenerated")
               when(prop
                  when(prop~>value == "DeviceMarker"
                     dbDeleteObject(shape)
                  )
               )
            )
         )
      )
      return(t)
   )
)
