
procedure(VALEgetComponentTypes(cv)
   prog((cfg regDeviceName tmpConfigFlag)

      cfg = cphFindOpenConfig(cv~>libName cv~>cellName "physConfig")
      if(cfg then
         regDeviceNames = ctGetCompTypeNames(cfg)
      else
         if(ddGetObj(cv~>libName cv~>cellName "schematic") then
            cfg = cphCreatePhysConfig(cv~>libName cv~>cellName "rbpConfigTmp"
               cv~>libName cv~>cellName "schematic")
            regDeviceNames = ctGetCompTypeNames(cfg)
            tmpConfigFlag = t
         else
            regDeviceNames = list("n1hvt_finfet" "n1lvt_finfet" 
               "n1svt_finfet" "n2svt_finfet" "p1hvt_finfet" "p1lvt_finfet" 
               "p1svt_finfet" "p2svt_finfet"
            )
            printf("VALE WARNING: No registered device names found, ")
            printf("using the default from the Advanced Node Generic PDK, ")
            printf("%L\n" regDeviceNames)
         )
      )
      when(tmpConfigFlag
         cphCloseConfig(cfg)
      )

      return(regDeviceNames)
   )
) 
