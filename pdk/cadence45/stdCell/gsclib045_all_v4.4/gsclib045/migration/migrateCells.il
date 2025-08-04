;;; CreateNewLibrary - creates a new library named "libname" associated with a tech file from library techfileLib

procedure( CreateNewLibrary( libname techfileLibName )
	let( (libId techId)
		libId = dbCreateLib( libname )
		techId = techOpenTechFile(libname "tech.db" "w")
		tcLoadTechFile(techId techfileLibName)
		techSaveTechFile(techId)
	)
)

;;; ListCellsWithView - returns list with cells in library "lib" that have the view "view"

procedure( ListCellsWithView( lib @optional (view "schematic") )
     let( ( libDDid cellDDid allCellList matchCellList)
	libDDid = ddGetObj( lib )

	;; Build list of all cells in Lib

	allCellList = libDDid~>cells~>name
	foreach( cell allCellList
		cellDDid = ddGetObj( lib cell )
		;; if cell has a view named "view", add to list
		if( rexMatchList( view cellDDid~>views~>name )
			matchCellList = cons( cell matchCellList )
		)
	)
     matchCellList
     )
)

;;; OptCellsInList - use VLM to migrate cells in "celllist" in library "lib" to library defined in
;;;                  migratemap.il using technology files q90to45.qtt, preprocess.qts and postprocess.qts

procedure( OptCellsInList(celllist libname)
		let( (cellname winId cv contextPath excludeList finalCellList)

		     ;; List of cells that need to be manually migrated

		    ;;  excludeList = list( "ANTENNA" "FILL1" "FILL2" "FILL4" "FILL8" "FILL16" "FILL32" "FILL64")
			excludeList = list( " ")

		     ;; Load routines and variables associated with VLM
		     loadContext(strcat(prependInstallPath("etc/context/") "loCore.cxt"))
		     callInitProc("loCore")

		     ;; Turn off writing data to disk which breaks multiple migrations
		     _loPref->_loPreferences->page1->_loKeepResults->value= nil
		     ;; Turn on relaxation for cells that have infeasible optimzation status
		     ;;_loPref->_loPreferences->page2->_loRelaxConstraintsByType->value= t
                     ;;_loPref->_loPreferences->page2->_loAutoRelaxTolerance->value = 5.0
		      hiFormDone(_loPref)

		     ;; Populate VLM setup form with source lib, cell and view names,
		     ;; working directory, mapping control file, and tech files
		     _loPlanner->_loPlannerLibStr->value = libname
		     _loPlanner->_loPlannerViewStr->value = "layout"
		     _loPlanner->_loWorkingDirStr->value = getWorkingDir()
                     _loPlanner->_loPlannerTechFileCyclic->value = "g90to45.qtt"
		     _loPlanner->_loPlannerGUIMapCyclic->value="migmap.il"
	             _loPlanner->_loPlannerPrepUsing->value="preprocess.qts"
		     _loPlanner->_loPlannerPostprocUsing->value="postprocess.qts"

		     ;; Do migration on each cell in list
		     foreach( cellname celllist 
			;; Check to see if on excludeList
			if(!member(cellname excludeList ) then
			printf("Loading cell %s.\n" cellname)
			;; Load source cell layout view in le window - needed so that form can sync and update
		        winId = deOpenCellView( libname cellname "layout" "maskLayout" list(list(0 0) list(500 600)) "r")
			cv = geGetWindowCellView( winId )
			
			_loPlanner->_loPlannerCellStr->value = cellname
			;; Needed to update migration map file cyclic
                        ddsUpdateSyncWithForm()
			_loWorkingDirStrCB()
			;; perform migration
			_loFullOptFlowPC()
			;; close dialog box for migration
			hiDBoxOK(OptimizeResultDBox)
		        ;; close source cell layout view le window so you don't have a large number of them
		        dbPurge(cv)
			finalCellList = cons( cellname finalCellList )
			 )
		     )
		     finalCellList

))


procedure( MoveMigrateToLayout( celllist libname ) 

   let( (cellname srcSpec destSpec)

         foreach( cellname celllist
		 srcSpec = gdmCreateSpec(libname cellname "migrate" nil "CDBA")
                 destSpec = gdmCreateSpec(libname cellname "layout" nil "CDBA")
		 ccpRename(srcSpec destSpec)
	)
   )
)

procedure( MigrateSchematics( celllist )
	let( (cellname winId cv) 
		loadContext( strcat(prependInstallPath("etc/context/") "adexl.cxt"))
		callInitProc("adexl")
		loadContext( strcat(prependInstallPath("etc/context/") "loCore.cxt"))
		callInitProc("loCore")
	        foreach( cellname celllist 
		        winId = deOpenCellView( "gsclib090" cellname "schematic" "schematic" list(list(0 0) list(500 600)) "r")
			cv = geGetWindowCellView( winId )
			_loSchematicMigrationForm->_loSchematicMigrationMapFileField->value="migratemap_sch.il"

			_loMigrateLibraries = nil
			_loMapPcellParams = nil
			_loUseSchematicLinks = nil

			_loSchematicMigrationMapFileFieldCB()
			_loSchematicMigrationFormCB()
			_loMigrateAllSchematics()
			dbPurge(cv)
		)
		celllist
	)
)
		
procedure(MakeHolding(cellList libname)
	let((winId cv cellname viewname cellcontainer xpos ypos ystepsize stepsize bBox rObj)

		xpos = 0
		ypos = 0
		mgrid = 0.005
		ystepsize = 2.00
		stepsize = 2.00
		viewname = "layout"
		winId = deOpenCellView( libname "allcells" "layout" "maskLayout" list(list(0 0) list(500 600)) "w")
		cv = geGetWindowCellView( winId )
		foreach( cellname cellList
		  cellcontainer = dbOpenCellViewByType(libname cellname viewname)
		  rObj = dbCreateInst( cv cellcontainer cellname xpos:ypos "R0" 1)
		  xpos = xpos + caadr(rObj->bBox) - caar(rObj->bBox) + stepsize
		  xpos = round(xpos/mgrid)*mgrid
		  if((xpos > 100) then
			xpos = 0
			ypos = ypos + ystepsize + stepsize
		  )
		  
		)
         )
)

;CreateNewLibrary("gsclib045" "gsclib045.tf")
;CellList = OptCellsInList( ListCellsWithView( "gsclib090" "layout" ) "gsclib090" )
;MoveMigrateToLayout( CellList "gsclib045")
;MigrateSchematics( ListCellsWithView( "gsclib090" "schematic" ))
;MakeHolding(CellList "gsclib045")
