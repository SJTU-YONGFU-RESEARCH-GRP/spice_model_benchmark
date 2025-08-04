procedure( avExtractedCellViewCallProc( layID )
let( (mbulkvalue updateflag str_to_int_value check_inst str_to_int_flag)
  ;printf("\nApplying Post process update on %s %s %s\n" layID~>libName layID~>cellName layID~>viewName)
  foreach( inst layID~>instances
      if(inst~>viewName == "ivpcell" then
        if(inst~>cellName != "npn" then
	      printf("Deleting model property for instance %s.\n" inst~>name)
	      dbDeletePropByName(inst "model")
        );if
      );if
  );foreach
);let
);procedure

