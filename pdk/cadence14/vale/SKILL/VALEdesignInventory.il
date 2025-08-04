;;; (C) Copyright Cadence Design Systems Inc. 2019
;;; All Rights Reserved
;;; Licensed Materials - Property of Cadence Design Systems
;;;
;;; No part of this file may be reproduced, stored in a retrieval system,
;;; or transmitted in any form or by any means --- electronic, mechanical,
;;; photocopying, recording, or otherwise --- without prior written permission
;;; of Cadence Design Systems, Inc.
;;;
;;; WARRANTY:
;;; Use all material in this file at your own risk.  Cadence Design Systems
;;; makes no claims about any material contained in this file.
;;;
;;; $Revision: 2.02 $
;;; $Date: Aug 12 2019 $
;;;
;;; ADAPTATIONS by M Sridhar Reddy
;;;    1. Integration with VALE Framework, major changes for displaying CDF
;;;       parameter tables.
;;;    2. Reformatted for improved readability 
;;;    3. Updates by Jonathan Fales for VALE Framework
;;; $Date: Fri Apr 25 2019 $
;;;
;;; $Revision: 2.01 $
;;; $Date: Fri Jun 15 2018 $
;;;
;;; ADAPTATIONS by Kent Lewallen
;;; Modifications for a specific customer's application
;;;
;;;
;;; $Previous Revision: 1.12 $
;;; $Date: Mon Aug  7 16:01:54 2017 $

;;; Functionality: Traverse the schematic/layout and report these items:
;;;                1. Design tree
;;;                2. Design inventory (cells being used)
;;;                3. Parameters that impact to layout (Eg: l, nfin, fingers, vt) in advance nodes.
;;; Usage: (a) Set .cdsinit file to load this program,
;;;        (b) In SE/LE window, access to menu: View -> 'Design Inventory'.
;;; Owner: Cadence IC Flow Solutions Team (Contributor: Ray Viranam)
;;; Note: _di* = Cadence internal Skill function for 'Design Inventory'



;------------------------------------------------------------------------;
; Main program: Design Inventory (Tree, Cells used, Parameters)
;------------------------------------------------------------------------;
procedure(VALEdesignInventory(
          @key 
             (cvId geGetWindowCellView())
             (tab "   ;") 
             (traverseView "nil") 
             (checkLayout nil)
             (rtDpl nil)
          )
   prog((erv runDir logfile title port sum_inst_count cUsedCount 
         refLibList refLibCellList cellList refLibCellTable)  

      ;list("l" "nfin" "nf" "fw")  
      ;rtDpl->parameterList = nil
 
      ;list("pd2svt");'("p1hvt_s");
      ;rtDpl->deviceList = nil

      erv = errset(
         strcat(getWorkingDir() "/VALE_RUNDIR")
      )
      if(erv then
         if(erv == list(nil) then
            printf("VALE ERROR: Failed to set the VALE_RUNDIR output ")
            printf("directory.\n")
            return()
         else
            runDir = car(erv)
            unless(isDir(runDir)
               createDirHier(runDir)
            )
            logfile = strcat(runDir "/designInventory.log")
            port = outfile(logfile)
         )
      else
         printf("VALE ERROR: A problem occurred setting up the VALE_RUNDIR ")
         printf("directory.\n%L\n" errset.errset)
         return()
      )


      if(checkLayout then
         if(cvId~>cellViewType == "schematic" then
            fprintf(port "\n\n   VALE ERROR: The current window is not ")
            fprintf(port "a layout window.  Please open a layout window ")
            fprintf(port "and rerun.\n")
            drain(port)
            sprintf(title "Design Inventory: %s/%s/%s" cvId~>libName 
               cvId~>cellName cvId~>viewName)
            view(logfile list(25:25 750:400) title)
            return()
         else
      	    traverseView = "layout"
         )
      else
         if(cvId~>cellViewType == "maskLayout" then
            fprintf(port "\n\n   VALE ERROR: The current window is not ")
            fprintf(port "a schematic window.  Please open a schematic window ")
            fprintf(port "and rerun.\n")
            fprintf(port "\n   It may be necessary to edit the VALE Framework ")
            fprintf(port "configuration file (IMFdefaults.il) to enable this ")
            fprintf(port "\n   feature on a schematic window.\n")
            drain(port)
            sprintf(title "Design Inventory: %s/%s/%s" cvId~>libName 
               cvId~>cellName cvId~>viewName)
            view(logfile list(25:25 750:400) title)
            return()
         else
       	    traverseView = "schematic cmos_sch symbol"
         )
      )
         
      refLibList= VALEdiCreateRefLibList( cvId ?traverseView traverseView )

      ;; (A) Print design tree 
         fprintf(port "\
            \n1. Design Tree (%s)\
            \n   ******************************************************************************\
            \n   Library : %s\
            \n   Cell    : %s\
            \n   View    : %s\
            \n   ******************************************************************************\n"
            getCurrentTime()
            cvId~>libName
            cvId~>cellName
            cvId~>viewName
         )

         VALEdiTravInstTree(cvId 
            ?tab tab
            ?traverseView traverseView 
            ?port port
            ?printTree t 
            ?refLibName "nil" 
            ?refLibCellList refLibCellList
            ?refLibCellTable refLibCellTable
         )
         fprintf(port "   ---------------------------------------------------------------------------\n\n\n")

         ;; (B) Generate inventory
         fprintf(port "2. Design Inventory")

         foreach(refLib refLibList
            refLibCellList  = ddGetObj(refLib)~>cells~>name
            refLibCellTable = makeTable("refLibCellTable" 0)
            VALEdiTravInstTree(cvId 
               ?tab strcat("       " tab)
               ?traverseView traverseView 
               ?port port
               ?printTree nil
               ?refLibName refLib 
               ?refLibCellList refLibCellList
               ?refLibCellTable refLibCellTable            
            )     
            sum_inst_count = 0
            cellList=list()
            cUsedCount = 0
            fprintf( port "\n   --------------------------------------------------------------------------\n")
            fprintf( port "   Reference Lib = %s (Lib Contents: %n cells)\n" refLib length(refLibCellList) )
            fprintf( port "   --------------------------------------------------------------------------")

            foreach(key refLibCellTable 
                 when(refLibCellTable[key] > 0  
                  cellList = cons(key cellList)
               ) 
            )
            foreach(key sort(cellList nil)
               fprintf(port "\n            %-34s = %10d" key refLibCellTable[key] )
            )
            foreach(key refLibCellTable 
               when(refLibCellTable[key] > 0  
                  cUsedCount = cUsedCount+1
               )
            )
            forall(key refLibCellTable  
               sum_inst_count =  sum_inst_count + refLibCellTable[key]  
            )
            fprintf( port "\n   ========================================================================\
               \n            Sum                       : %10d instances (from %n cells)\
               \n   " sum_inst_count cUsedCount
            )  
         );foreach refLib

         ;; (C) Device Parameter Inventory
         fprintf(port "\n\n3. Device CDF Parameters\n") 
         fprintf(port "   --> Set Device List in the config file: ")
         fprintf(port "_IMFdat->compModN->deviceList = ")
         fprintf(port "list(\"name1\" \"name2\")\n")
         fprintf(port "   --> Set CDF Parameters in the config file: ")
         fprintf(port "_IMFdat->compModN->parameterList = ")
         fprintf(port "list(\"par1\" \"par2\")\n")
         cellList = rtDpl->deviceList
         unless(cellList cellList="All")
         if(rtDpl->parameterList then
            fprintf(port   "\n       --------    : Device List: %L   " 
               cellList ) 
            fprintf(port   "\n       --------    : CDF Parameters: %L  "
               rtDpl->parameterList)
         else
            fprintf( port   "\n       --------    : Device List: %L   " 
               cellList) 
            fprintf( port   "\n       --------    : CDF Parameters: All" ) 
         )
         fprintf( port   "\n\n   A. Top Cell: %s/%s/%s"  
            cvId~>libName cvId~>cellName cvId~>viewName
         )
         VALEdiTravCvCreateParTbl(cvId port traverseView rtDpl)

      drain(port)
      sprintf( title "Device Inventory: %s/%s/%s" cvId~>libName cvId~>cellName 
         cvId~>viewName )
      view(logfile list(25:25 900:800) title ) 
      ;deleteFile(file)

      return(t)
   )
)

procedure(VALEdiTravInstTree(
             cvId
          @key (tab  "    ;")
             (traverseView "schematic symbol layout")
             (port nil)
             (printTree t ) 
             (refLibName "analogLib")
             (mfactor 1) 
             (refLibCellList nil) 
             (refLibCellTable  makeTable("refLibCellTable" 0))
          )
   let((inst tmp)
      foreach(hdr cvId~>instHeaders
         if((length(hdr~>instances) > 0) 
            && (inst = car(hdr~>instances)) 
            && (tmp = dbGetAnyInstSwitchMaster(inst traverseView)) then
            when(printTree == t    
               fprintf(port "%s%s %s %s (%d) \n" tab hdr->libName 
                  hdr->cellName hdr->viewName length(hdr~>instances))
            )
            unless(refLibName   == "nil"     
               when(rexMatchList(hdr->cellName refLibCellList )
                  refLibCellTable[hdr->cellName] = 
                     refLibCellTable[hdr->cellName] + length(hdr~>instances) *
                        mfactor
               )
            )
            unless(tmp->cellViewType == "schematicSymbol" || 
               hdr~>viewName == "abstract"
               VALEdiTravInstTree(tmp 
                  ?tab strcat("   ;    " tab)
                  ?traverseView traverseView 
                  ?port port
                  ?printTree printTree
                  ?mfactor length(hdr~>instances) 
                  ?refLibCellList refLibCellList
                  ?refLibCellTable refLibCellTable				      
               )
            )
         )
      )
      ;drain( port )
   )
)

procedure(VALEdiCreateRefLibList(
             cvId 
          @key 
             (traverseView "schematic cmos_sch symbol layout") 
             (refLibListTable makeTable("tableOfReferenceLibraries" 0))
          )
   let((refLibList) 
      VALEdiTravInstCreateRefLibTbl( cvId ?traverseView traverseView 
         ?refLibListTable refLibListTable)
      foreach(key refLibListTable 
         refLibList = cons(key refLibList)
      )
      sort(refLibList nil)
   )	 
)

procedure(VALEdiTravInstCreateRefLibTbl(
             cvId 
          @key 
             (traverseView "schematic cmos_sch symbol layout") 
             (refLibListTable makeTable("tableOfReferenceLibraries" 0))
          ) 
   let((inst tmp (refLibList list()) ) 
      foreach(hdr cvId~>instHeaders
         if((length(hdr~>instances) > 0)
            && (inst = car( hdr~>instances )) 
            && (tmp = dbGetAnyInstSwitchMaster( inst traverseView )) then
       	    when(!member(hdr->libName refLibList) 
               refLibList = cons(hdr->libName refLibList)
      	    )
   	    refLibListTable[hdr->libName] = refLibListTable[hdr->libName]+1
  	    unless(tmp->cellViewType == "schematicSymbol" || 
                   hdr~>viewName == "abstract"
    	       VALEdiTravInstCreateRefLibTbl(tmp ?traverseView traverseView 
                  ?refLibListTable refLibListTable)
       	    )
         )
      )
   )
)

procedure(VALEdiTravCvCreateParTbl(cvId port traverseView rtDpl) 
   let((pdkCellList)
      pdkCellList = ddGetObj(VALEdiGetTechLibName(cvId))~>cells~>name 
      foreach(hdr cvId~>instHeaders
         if(member(hdr~>cellName pdkCellList) then
            fprintf(port   "\n                  %s/%s/%s"  
                hdr~>libName hdr~>cellName hdr~>viewName
            )
         )
         VALEdiTravInstCreateParTbl(cvId port hdr traverseView rtDpl) 
      )
   )
)

procedure(VALEdiTravInstCreateParTbl(cvId port headerInst traverseView rtDpl) 
   let((pdkCellList tmp propVal dev_allparamList targetId)
      pdkCellList = ddGetObj(VALEdiGetTechLibName(cvId))~>cells~>name 

      foreach(inst headerInst~>instances
         tmp = dbGetAnyInstSwitchMaster( inst traverseView )
  	 ;printf("\nDebug2a: cellName = %s" inst~>cellName)
         if(!rtDpl->parameterList then
            targetId = cdfGetCellCDF(ddGetObj(inst~>libName inst~>cellName))
            dev_allparamList=targetId~>parameters~>name
         else
            dev_allparamList=rtDpl->parameterList
         )

  	 foreach(prop inst~>prop
  	    case(type(prop~>value)
  	       (fixnum   sprintf(propVal "%n" prop~>value ))
  	       (flonum   sprintf(propVal "%f" prop~>value ))
  	       (t	   propVal = prop~>value)
  	    )
  	    when(member(prop~>name dev_allparamList) && (!rtDpl->deviceList 
                        || rexMatchList(inst~>cellName rtDpl->deviceList)) 
               fprintf(port   "\n                     %s : %s(%L) :  %L"
                  inst~>name inst~>cellName prop~>name propVal) 
  	    )
         )
         if(!member(inst~>cellName pdkCellList) then
               unless((tmp->cellViewType == "schematicSymbol" || 
                  inst~>viewName == "abstract")    
                  fprintf(port   "\n                  %s/%s/%s"  
                     inst~>libName inst~>cellName inst~>viewName
                  )
                  VALEdiTravInstCreateParTbl(cvId port tmp traverseView rtDpl)
               )
         else
            fprintf(port
               "\n                     ----------------------------------")
                  
         )
      ); foreach inst
   )
)

procedure(VALEdiAscentSortList(listOfStrings)
   ;; Sort list of string to numerical ascend
   ;; Caution: This function removes identical elements
   ;; (eg: 338.0n, 338.0e-9) from the given list.
   prog((numList threshold_un)
      numList      = nil
      threshold_un = 501.0n
      foreach(listElement listOfStrings
         ;; Eliminate identical element
         when(!member(car(errsetstring(listElement)) numList) 
	    numList = append( numList errsetstring(listElement) )
	 )
      )
      ;; sort it to the numerical ascend.
      numList = sort( numList 'lessp )
      ;; reset to an empty list
      listOfStrings = nil
      foreach(listElement numList
         case(type(listElement)
	    (fixnum  listOfStrings = 
               append(listOfStrings parseString(sprintf(nil "%n" listElement)))
            )
	    (flonum
               when(listElement >= threshold_un 
	          listOfStrings = append(listOfStrings 
                     parseString(cdfFormatFloatString(
                        sprintf(nil "%g" listElement) "u"))
                  ) 
               )
	       when(listElement < threshold_un
	          listOfStrings = append(listOfStrings 
                     parseString(cdfFormatFloatString(
                        sprintf(nil "%g" listElement) "n"))
                  ) 
               )
	    )
	 ); case
      )        
      return(listOfStrings)
   )
)

procedure(VALEdiGetTechLibName( cvId )
   ; Identify the associated techLib:
   let((baseTechLibName refLibId refLibIdList tfId )
      foreach(libProp ddGetObj(cvId~>libName)~>prop 
         ;Case of 'techLibName' specified to a none-ITDB:
         when(libProp~>name == "techLibName" &&
              !techGetTechFile(ddGetObj(cvId->libName ))~>refs
	    baseTechLibName = libProp~>value
         )
         ;Case of 'techLibName' specified to ITDB:
   	 when(libProp~>name == "techLibName" ||
              techGetTechFile(ddGetObj(cvId->libName ))~>refs 
   	    tfId = techGetTechFile(ddGetObj(cvId->libName ))
   	    refLibIdList = tfId~>refs
   	    while(and( !baseTechLibName refLibIdList )
               refLibId = car( refLibIdList )
               refLibIdList = cdr( refLibIdList )
   	       if(refLibId~>refs then
                  baseTechLibName = VALEdiGetTechLibName( refLibId )
   	       else
   	          when( member( "foundry" refLibId~>constraintGroups~>name )
                     baseTechLibName = refLibId~>libName
   		  )
   	       )
            );end while 
   	 );end when		
      );end foreach
      baseTechLibName ;<-- return
   )
)
;-------------------------------------------------------------------------------

; Traverse design tree and return the technology cell list
procedure(VALEdiGetTechCellList(@key (cvId geGetEditCellView()) 
                                     (display nil             ))  
   let((logfile title port traverseView refLib refLibCellList refLibCellTable
        cellList sum_inst_count erv runDir)
      case(cvId~>cellViewType
         ("schematic" traverseView = "schematic cmos_sch symbol")
         (("maskLayout" || "maskLayoutXL") traverseView = "layout")
      )
      refLib          = VALEdiGetTechLibName(cvId )
      refLibCellList  = ddGetObj(refLib)~>cells~>name
      refLibCellTable = makeTable("refLibCellTable" 0)
      VALEdiTravInstTree(cvId 
         ?tab "    ;"
         ?traverseView traverseView 
         ?port nil
         ?printTree nil
         ?refLibName refLib 
         ?refLibCellList refLibCellList
         ?refLibCellTable refLibCellTable            
      )     
      cellList = list()
      foreach(cell refLibCellTable 
         when(refLibCellTable[cell] > 0  && 
              ddGetObj(refLib cell "layout" nil nil "r")
	    cellList = cons( cell cellList ) 
	 ) 
      )
      when(display == t
         erv = errset(
            strcat(getWorkingDir() "/VALE_RUNDIR")
         )
         if(erv then
            if(erv == list(nil) then
               printf("VALE ERROR: Failed to set the VALE_RUNDIR output ")
               printf("directory.\n")
               return()
            else
               runDir = car(erv)
               unless(isDir(runDir)
                  createDirHier(runDir)
               )
               logfile = strcat(runDir "/designInventory.log")
               port = outfile(logfile)
            )
         else
            printf("VALE ERROR: A problem occurred setting up the VALE_RUNDIR ")
            printf("directory.\n%L\n" errset.errset)
            return()
         )

	 fprintf(port "\n\
		   \n   PDK Technology Cells Used in Full Hierarchy (%s)\
		   \n   **************************************************************************\
		   \n   Library : %s\
		   \n   Cell    : %s\
		   \n   View    : %s\
		   \n   **************************************************************************"
            getCurrentTime() cvId~>libName cvId~>cellName cvId~>viewName  
         )
	 fprintf(port "\n   PDK Technology Library: %s" 
            VALEdiGetTechLibName(cvId) )
	 sum_inst_count = 0
	 foreach(cell sort( cellList nil)
	    fprintf(port
               "\n            %-34s = %10d" cell refLibCellTable[cell] )
	    sum_inst_count =  sum_inst_count + refLibCellTable[cell]
         )
	 fprintf(port "\n   --------------------------------------------------------------------------\
	         	\n            Sum            = %10d instances in the full hierarchy\
   			\n   --------------------------------------------------------------------------\n"
			sum_inst_count )
	 drain(port)
         sprintf( title "Techology cells used in: %s/%s/%s" 
            cvId~>libName cvId~>cellName cvId~>viewName )
         view(logfile list(25:25 800:600) title ) 	
      )
      ;; Return value	
      sort(cellList nil)
   )
)

; Dump CDF of each technology cell
procedure(VALEdiCdfDump(
          @key 
             (cvId geGetEditCellView())
          )
   prog((techLib techCellList cdfDumpFile erv runDir)
      techLib      = VALEdiGetTechLibName( cvId )
      techCellList = VALEdiGetTechCellList( ?cvId cvId ?display nil)

      erv = errset(
         strcat(getWorkingDir() "/VALE_RUNDIR")
      )
      if(erv then
         if(erv == list(nil) then
            printf("VALE ERROR: Failed to set the VALE_RUNDIR directory.\n")
            return()
         else
            runDir = car(erv)
            unless(isDir(runDir)
               createDirHier(runDir)
            )
         )
      else
         printf("VALE ERROR: A problem occurred setting up the VALE_RUNDIR ")
         printf("directory.\n%L\n" errset.errset)
         return()
      )

     sprintf(cdfDumpFile "%s/diUsingCdf_%s.cdf" runDir techLib)
     when(isFile(cdfDumpFile) 
        shell(sprintf(nil "rm -f %s" cdfDumpFile))
     )
     foreach(cell techCellList
        cdfDump(techLib 
           sprintf(nil "/tmp/diUsingCdf_%s_%s" techLib cell)
           ?cellName cell ?level 'base ?edit nil
        )
	shell(
           sprintf(nil "cat /tmp/diUsingCdf_%s_%s >> %s" techLib cell 
              cdfDumpFile)
        )
     )
     view(cdfDumpFile list(25:25 800:600))
     return(t) 
  )
)


