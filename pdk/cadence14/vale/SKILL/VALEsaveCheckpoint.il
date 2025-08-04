
unless(isCallable('VALEsaveCheckpoint)
   procedure(VALEsaveCheckpoint(
	 rtDpl
	 @optional 
	 (debug nil)
	 )
		  
      prog((cv)
		 
	 cv = geGetWindowCellView()
		 
	 checkpointViewName = sprintf(nil "%s_%s"  cv->viewName rtDpl->name) 
		 ;; save cell to new cell with new view name
	 printf("VALE INFO: Saving cell %s into viewName %s\n" cv->cellName checkpointViewName)
	 savedCellID = dbCopyCellView(cv cv->libName cv->cellName checkpointViewName 
	    nil nil t)

	 unless(savedCellID  
	    printf("VALE ERROR: Could not save database to\n Library: %s\n Cell Name: %s\n View Name %s\n" 
	       cv->libName cv->cellName checkpointViewName)
	    return()
	    )
	 return(t)
	 )
      )
   )