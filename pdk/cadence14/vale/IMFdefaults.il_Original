_IMFdat = list(nil)

;; VALE Framework Global Flow Options
_IMFdat->menuTitle = "VALE"
;_IMFdat->windowList = list("layout" "schematic" "CIW")
_IMFdat->windowList = list("layout" "schematic")
_IMFdat->useCustomMenu = t
_IMFdat->defaultNetNamePrefix = "valenet"

;; Technology Setup
_IMFdat->techLib = "cds_ff_mpt"
_IMFdat->polyLayer = "Poly"
_IMFdat->sadpLayers = list("M1" "M2" "M3")
_IMFdat->mpLayers   = list("M1" "M2" "M3" "V1" "V2" "V3")
_IMFdat->mpPurposes = list("drawing" "fill")
_IMFdat->wspLayers   = list("Poly" "M1" "M2" "M3")
_IMFdat->wspPurposes = list("track")
_IMFdat->mpExcludePurpose = list("blockage" "pin")
_IMFdat->noConnectivityLayer  = list("CutM1" "CutM1Mask1" "CutM1Mask2"
                                     "CutM2" "CutM2Mask1" "CutM2Mask2"
                                     "CutM3" "CutM3Mask1" "CutM3Mask2"
                                     "CutPoly" "NWell" "Active"
                                     "Psvt" "Nsvt" "Phvt" "Nhvt" "Plvt" "Nlvt"
                                     "CutActive" "PPitch" "ThickOx"
                                    )
_IMFdat->rectangleLayers  = list("CutM1" "CutM1Mask1" "CutM1Mask2"
                                 "CutM2" "CutM2Mask1" "CutM2Mask2"
                                 "CutM3" "CutM3Mask1" "CutM3Mask2"
                                 "Psvt" "Nsvt" "Phvt" "Nhvt" "Plvt" "Nlvt"
                                 "CutPoly" "NWell" "Active" "ThickOx"
                                )
_IMFdat->rectanglePurposes = list("blockage" "pin" "track")
_IMFdat->horizontalLayers  = list("M2" "M4" "M6" "MT")

;; Row-based Placement key layers
_IMFdat->dummyRowLpp = list("designFlow" "drawing5")
_IMFdat->tapRowLpp = list("designFlow" "drawing6")
_IMFdat->instRowLpp = list("designFlow" "drawing7")
_IMFdat->nRowLpp = list("designFlow" "drawing8")
_IMFdat->pRowLpp = list("designFlow" "drawing9")

;; VF Options related to Component Module Dependencies and Output
;; Do NOT remove opt1 through opt5 parameters
_IMFdat->opt1 = list(nil)
_IMFdat->opt1->title = "Generated Shapes Output Location"
_IMFdat->opt1->name = "outputLocation"
_IMFdat->opt1->type = "cyclic"
_IMFdat->opt1->choices = list("Shapes" "figGroup" "Overlay" "CheckCell")
_IMFdat->opt1->value = "Shapes"
_IMFdat->opt1->defaultValue = "Shapes"

_IMFdat->opt2 = list(nil)
_IMFdat->opt2->title = "Generated Shapes Output Style"
_IMFdat->opt2->name = "outputStyle"
_IMFdat->opt2->type = "cyclic"
_IMFdat->opt2->choices = list("Separate" "Merged")
_IMFdat->opt2->value = "Separate"

_IMFdat->opt3 = list(nil)
_IMFdat->opt3->title = "Use Custom Output Name Extension"
_IMFdat->opt3->name = "useCustomNameExt"
_IMFdat->opt3->type = "boolean"
_IMFdat->opt3->value = nil

_IMFdat->opt4 = list(nil)
_IMFdat->opt4->title = "Custom Output Name Extension" 
_IMFdat->opt4->name = "customNameExt" 
_IMFdat->opt4->type = "entry"
_IMFdat->opt4->value = "GEN"

_IMFdat->opt5 = list(nil)
_IMFdat->opt5->title = "Merged Output Name Extension" 
_IMFdat->opt5->name = "mergedNameExt" 
_IMFdat->opt5->type = "entry"
_IMFdat->opt5->value = "IMF"

_IMFdat->opt6 = list(nil)
_IMFdat->opt6->title = "Waive Dependency" 
_IMFdat->opt6->name = "waiveDependency"
_IMFdat->opt6->type = "boolean"
_IMFdat->opt6->value = nil

_IMFdat->opt7 = list(nil)
_IMFdat->opt7->title = "Add Connectivity" 
_IMFdat->opt7->name = "addConnectivity"
_IMFdat->opt7->type = "boolean"
_IMFdat->opt7->value = nil

;; COMPONENT MODULE DEFINITIONS
;; The compModN name, where N is a number, implies an order.  The names
;; below are intentionally spaced to provide flexibility when adding more
;; Component Modules. 

;; Component Module 1 Definition
_IMFdat->compMod1 = list(nil)
_IMFdat->compMod1->name = "RemoveAll"
_IMFdat->compMod1->shortName = "RemoveAll"
_IMFdat->compMod1->description = "Remove All Generated"
_IMFdat->compMod1->slider = "Utilities"

;; Component Module 2 Definition
_IMFdat->compMod2 = list(nil)
_IMFdat->compMod2->name = "RemoveProps"
_IMFdat->compMod2->shortName = "RemoveProps"
_IMFdat->compMod2->description = "Remove VALEfw Properties..."
_IMFdat->compMod2->slider = "Utilities"

;; Component Module 3 Definition
_IMFdat->compMod3 = list(nil)
_IMFdat->compMod3->name = "ResetView"
_IMFdat->compMod3->shortName = "ResetView"
_IMFdat->compMod3->description = "Reset View with Selected Layer"
_IMFdat->compMod3->slider = "Utilities"

;; Component Module 5 Definition
_IMFdat->compMod5 = list(nil)
_IMFdat->compMod5->name = "EMWireGuide"
_IMFdat->compMod5->version = "V01"
_IMFdat->compMod5->shortName = "EMWireGuide"
_IMFdat->compMod5->description = "EM Wire Guide"
_IMFdat->compMod5->currentExamples = list("10u" "50u" "100u")
_IMFdat->compMod5->temperature = list("100" "105" "110" "115" "120" "125" "130" "135" "140")
_IMFdat->compMod5->calcType = list("Idc width" "Idc width, Irms limit")
_IMFdat->compMod5->viaType = list("square" "bar" "large")
_IMFdat->compMod5->slider = "Utilities"

;; Component Module 7 Definition
_IMFdat->compMod7 = list(nil)
_IMFdat->compMod7->name = "GridTool"
_IMFdat->compMod7->shortName = "GridTool"
_IMFdat->compMod7->description = "Grid Tool"
_IMFdat->compMod7->xGridSizes = list("0.001" "0.086" "0.090" "0.094" "0.102" "0.104" "0.344" "0.344" "0.688")
_IMFdat->compMod7->yGridSizes = list("0.001" "0.048" "0.048" "0.048" "0.048" "0.048" "0.528" "1.056" "1.056")
_IMFdat->compMod7->xOffsets = list("0.000" "0.043" "0.052" "0.043" "0.052")
_IMFdat->compMod7->yOffsets = list("0.000" "0.000" "0.000" "0.024" "0.024")
_IMFdat->compMod7->slider = "Utilities"

;; Component Module 9 Definition
_IMFdat->compMod9 = list(nil)
_IMFdat->compMod9->name = "SnapToPolyWSP"
_IMFdat->compMod9->shortName = "PolySnap"
_IMFdat->compMod9->description = "Snap Instances to Poly WSP Grid"
_IMFdat->compMod9->slider = "Utilities"

;; Component Module 16 Definition
_IMFdat->compMod16 = list(nil)
_IMFdat->compMod16->name = "DeleteWSPRegions"
_IMFdat->compMod16->version = "V05"
_IMFdat->compMod16->shortName = "DeleteWSPRegions"
_IMFdat->compMod16->description = "Delete WSP Regions"
_IMFdat->compMod16->slider = "Utilities"

;; Component Module 17 Definition
_IMFdat->compMod17 = list(nil)
_IMFdat->compMod17->name = "DeleteRowTemplates"
_IMFdat->compMod17->version = "V05"
_IMFdat->compMod17->shortName = "DelRowTempl"
_IMFdat->compMod17->description = "Delete Row Templates"
_IMFdat->compMod17->slider = "Utilities"

;; Component Module 18 Definition
_IMFdat->compMod18 = list(nil)
_IMFdat->compMod18->name = "LoadHIF"
_IMFdat->compMod18->shortName = "LoadHIF"
_IMFdat->compMod18->description = "Load DFM Hotpots File"
_IMFdat->compMod18->slider = "Utilities"

;; Component Module 26 Definition
_IMFdat->compMod26 = list(nil)
_IMFdat->compMod26->name = "InspectProps"
_IMFdat->compMod26->version = "V05"
_IMFdat->compMod26->shortName = "InspProps"
_IMFdat->compMod26->description = "Inspect Schematic Instance Properties"
_IMFdat->compMod26->menuDisplay = list("schematic")
_IMFdat->compMod26->slider = "Migration"

;; Component Module 88 Definition
_IMFdat->compMod88 = list(nil)
_IMFdat->compMod88->name = "SchMig"
_IMFdat->compMod88->shortName = "SchMig"
_IMFdat->compMod88->description = "Schematic Migration"
_IMFdat->compMod88->envVars = list(nil)
_IMFdat->compMod88->envVars->IMF_USE_CSV_INFILE = "TRUE"
_IMFdat->compMod88->envVars->IMF_MIG_MAP_FILE = "/home/jfales/Public/GPDK/pre_cds_ff_mpt_v_1.0_042220/vale/Include/SchMig_V05.csv"
_IMFdat->compMod88->envVars->IMF_RUN_CHECK_TO_SPEC = "FALSE"
_IMFdat->compMod88->envVars->IMF_RUN_CLEAN_PROPS = "TRUE"
_IMFdat->compMod88->envVars->IMF_MIG_IGNORE_LIBS = "basic analogLib US_8ths borders"
_IMFdat->compMod88->envVars->IMF_MIG_SOURCE_TECH = "cds_ff_mpt"
_IMFdat->compMod88->envVars->IMF_MIG_TARGET_TECH = "gpdk045"
;_IMFdat->compMod88->envVars->IMF_MIG_SOURCE_TECH = "gpdk045"
;_IMFdat->compMod88->envVars->IMF_MIG_TARGET_TECH = "cds_ff_mpt"
_IMFdat->compMod88->envVars->IMF_MIG_REF_PAR_PREFIX = "cc_"
_IMFdat->compMod88->envVars->IMF_MIG_EXCL_VIEWS = "layout abstract"
_IMFdat->compMod88->envVars->IMF_MIG_TERM_MAP = "/home/jfales/Public/GPDK/pre_cds_ff_mpt_v_1.0_042220/vale/Include/SchMig_V05_termMap.il"
_IMFdat->compMod88->envVars->IMF_MIG_ORIENT_MAP = "/home/jfales/Public/GPDK/pre_cds_ff_mpt_v_1.0_042220/vale/Include/SchMig_V05_orientMap.il"
_IMFdat->compMod88->setPCellDefaultsAndRunAllCBs = t
_IMFdat->compMod88->pinSearchDeltaDivisor = 2
_IMFdat->compMod88->menuDisplay = list("schematic")
_IMFdat->compMod88->slider = "Migration"

;; Component Module 34 Definition
_IMFdat->compMod34 = list(nil)
_IMFdat->compMod34->name = "MinArea"
_IMFdat->compMod34->version = "V05"
_IMFdat->compMod34->shortName = "MinArea"
_IMFdat->compMod34->description = "Fix Min Area"
_IMFdat->compMod34->slider = "Layout Toolbox"

;; Component Module 35 Definition
_IMFdat->compMod35 = list(nil)
_IMFdat->compMod35->name = "MinAreaOpt1"
_IMFdat->compMod35->version = "V01"
_IMFdat->compMod35->shortName = "MinAreaOpt1"
_IMFdat->compMod35->description = "Optimize 1x Minimum Area"
_IMFdat->compMod35->timeout = "90"
_IMFdat->compMod35->slider = "Layout Toolbox"

;; Component Module 36 Definition
_IMFdat->compMod36 = list(nil)
_IMFdat->compMod36->name = "AddExt"
_IMFdat->compMod36->version = "V05"
_IMFdat->compMod36->shortName = "EXT"
_IMFdat->compMod36->description = "Extend Via Overlaps"
_IMFdat->compMod36->slider = "Layout Toolbox"

;; Component Module 38 Definition
_IMFdat->compMod38 = list(nil)
_IMFdat->compMod38->name = "AlignEnds"
_IMFdat->compMod38->version = "V05"
_IMFdat->compMod38->shortName = "AlignLE"
_IMFdat->compMod38->description = "Align Line Ends"
_IMFdat->compMod38->slider = "Layout Toolbox"

;; Component Module 45 Definition
_IMFdat->compMod45 = list(nil)
_IMFdat->compMod45->name = "AddTrims"
_IMFdat->compMod45->version = "V05"
_IMFdat->compMod45->shortName = "Trims"
_IMFdat->compMod45->description = "Add Trim Shapes"
_IMFdat->compMod45->outputLocation = "Shapes"
_IMFdat->compMod45->outputStyle = "Separate"
_IMFdat->compMod45->slider = "Layout Toolbox"

;; Component Module 46 Definition
_IMFdat->compMod46 = list(nil)
_IMFdat->compMod46->name = "AddTrims2"
_IMFdat->compMod46->version = "V05"
_IMFdat->compMod46->shortName = "Trims2"
_IMFdat->compMod46->description = "Add Trim Shapes 2"
_IMFdat->compMod46->outputLocation = "Shapes"
_IMFdat->compMod46->outputStyle = "Separate"
_IMFdat->compMod46->slider = "Layout Toolbox"

;; Component Module 51 Definition
_IMFdat->compMod51 = list(nil)
_IMFdat->compMod51->name = "MissingNetVia"
_IMFdat->compMod51->version = "V05"
_IMFdat->compMod51->shortName = "MissingNetVia"
_IMFdat->compMod51->description = "Insert Missing Via(s) on Net"
_IMFdat->compMod51->outputLocation = "Shapes"
_IMFdat->compMod51->outputStyle = "Separate"
_IMFdat->compMod51->timeout = "90"
_IMFdat->compMod51->slider = "Layout Toolbox"

;; Component Module 70 Definition
_IMFdat->compMod70 = list(nil)
_IMFdat->compMod70->name = "SaveAsideNets"
_IMFdat->compMod70->version = "V05"
_IMFdat->compMod70->shortName = "SaveAsideNets"
_IMFdat->compMod70->description = "Save Aside Net(s)"
_IMFdat->compMod70->slider = "Utilities"

;; Component Module 95 Definition
_IMFdat->compMod95 = list(nil)
_IMFdat->compMod95->name = "StdFill"
_IMFdat->compMod95->version = "V05"
_IMFdat->compMod95->shortName = "FILL"
_IMFdat->compMod95->description = "Run Standard Fill"
_IMFdat->compMod95->outputLocation = "figGroup"
_IMFdat->compMod95->outputStyle = "Separate"
_IMFdat->compMod95->stampStreamInCellNames = nil
_IMFdat->compMod95->envVars = list(nil)
_IMFdat->compMod95->envVars->VALE_FILL_LAYERS = "Poly M1 M2 M3 M4 M5 M6 M7 MT"
_IMFdat->compMod95->envVars->VALE_BEOL_STACK = "8M_7Mx_MT"
_IMFdat->compMod95->envVars->VALE_FILL_RUNSET = "/home/jfales/Public/GPDK/pre_cds_ff_mpt_v_1.0_042220/fill/StdFill_V05.pvl"
_IMFdat->compMod95->envVars->VALE_FILL_LMAP = "/home/jfales/Public/GPDK/pre_cds_ff_mpt_v_1.0_042220/fill/StdFill_V05.lmap"
_IMFdat->compMod95->envVars->VALE_FILL_INST = "/home/jfales/Public/GPDK/pre_cds_ff_mpt_v_1.0_042220/fill/Include"
_IMFdat->compMod95->envVars->VALE_SELECT_PRBOUNDARY = "YES"
_IMFdat->compMod95->envVars->VALE_SELECT_INST_FILL = "YES"
_IMFdat->compMod95->envVars->VALE_SELECT_CRITICAL_NET_FEATURE = "YES"
_IMFdat->compMod95->envVars->VALE_FILL_EDGE_HALO = "0.120"
;_IMFdat->compMod95->envVars->VALE_CRITICAL_NET_FILE = "/path/to/custom/file"
_IMFdat->compMod95->slider = "In-design Fill"

;; Component Module 96 Definition
_IMFdat->compMod96 = list(nil)
_IMFdat->compMod96->name = "StdFillPerLyr"
_IMFdat->compMod96->version = "V05"
_IMFdat->compMod96->shortName = "FILL"
_IMFdat->compMod96->description = "Run Standard Fill per Layer"
_IMFdat->compMod96->outputLocation = "figGroup"
_IMFdat->compMod96->outputStyle = "Separate"
_IMFdat->compMod96->stampStreamInCellNames = nil
_IMFdat->compMod96->envVars = list(nil)
_IMFdat->compMod96->envVars->VALE_FILL_LAYERS = "Poly M1 M2 M3 M4 M5 M6 M7 MT"
_IMFdat->compMod96->envVars->VALE_BEOL_STACK = "8M_7Mx_MT"
_IMFdat->compMod96->envVars->VALE_FILL_LMAP = "/home/jfales/Public/GPDK/pre_cds_ff_mpt_v_1.0_042220/fill/StdFill_V05.lmap"
_IMFdat->compMod96->envVars->VALE_FILL_INST = "/home/jfales/Public/GPDK/pre_cds_ff_mpt_v_1.0_042220/fill/Include"
_IMFdat->compMod96->envVars->VALE_SELECT_PRBOUNDARY = "YES"
_IMFdat->compMod96->envVars->VALE_SELECT_INST_FILL = "YES"
_IMFdat->compMod96->envVars->VALE_SELECT_CRITICAL_NET_FEATURE = "YES"
_IMFdat->compMod96->envVars->VALE_FILL_EDGE_HALO = "0.120"
;_IMFdat->compMod96->envVars->VALE_CRITICAL_NET_FILE = "/path/to/custom/file"
_IMFdat->compMod96->slider = "In-design Fill"

;; Component Module 55 Definition
_IMFdat->compMod55 = list(nil)
_IMFdat->compMod55->name = "WSPFill"
_IMFdat->compMod55->version = "V05"
_IMFdat->compMod55->shortName = "TFILL"
_IMFdat->compMod55->description = "Insert WSP Fill"
_IMFdat->compMod55->outputLocation = "Shapes"
_IMFdat->compMod55->outputStyle = "Separate"
_IMFdat->compMod55->dependency = list("compMod45")
_IMFdat->compMod55->waiveDependency = nil
_IMFdat->compMod55->slider = "In-design Fill"

;; Component Module 25 Definition
_IMFdat->compMod25 = list(nil)
_IMFdat->compMod25->name = "FastXOR"
_IMFdat->compMod25->version = "V05"
_IMFdat->compMod25->shortName = "XOR"
_IMFdat->compMod25->description = "Layout FastXOR"
_IMFdat->compMod25->outputLocation = "Shapes"
_IMFdat->compMod25->outputStyle = "Separate"
_IMFdat->compMod25->dependency = nil 
_IMFdat->compMod25->waiveDependency = nil
_IMFdat->compMod25->envVars = list(nil)
_IMFdat->compMod25->envVars->IMF_XOR_RUNDIR = "./VALE_RUNDIR/wd.fastXOR"
_IMFdat->compMod25->envVars->IMF_XOR_TMPLIB = "FastXORImportLib"
_IMFdat->compMod25->slider = "Utilities"

;; Component Module 61 Definition
_IMFdat->compMod61 = list(nil)
_IMFdat->compMod61->name = "M1Decomp"
_IMFdat->compMod61->version = "V05"
_IMFdat->compMod61->shortName = "ColorM1"
_IMFdat->compMod61->description = "M1 Coloring"
_IMFdat->compMod61->outputLocation = "figGroup"
_IMFdat->compMod61->showAllMarkers = nil
_IMFdat->compMod61->slider = "Decomposition"

;; Component Module 62 Definition
_IMFdat->compMod62 = list(nil)
_IMFdat->compMod62->name = "V1Decomp"
_IMFdat->compMod62->version = "V05"
_IMFdat->compMod62->shortName = "ColorV1"
_IMFdat->compMod62->description = "V1 Coloring"
_IMFdat->compMod62->outputLocation = "figGroup"
_IMFdat->compMod62->showAllMarkers = nil
_IMFdat->compMod62->slider = "Decomposition"

;; Component Module 63 Definition
_IMFdat->compMod63 = list(nil)
_IMFdat->compMod63->name = "M2Decomp"
_IMFdat->compMod63->version = "V05"
_IMFdat->compMod63->shortName = "ColorM2"
_IMFdat->compMod63->description = "M2 Coloring"
_IMFdat->compMod63->outputLocation = "figGroup"
_IMFdat->compMod63->showAllMarkers = nil
_IMFdat->compMod63->slider = "Decomposition"

;; Component Module 64 Definition
_IMFdat->compMod64 = list(nil)
_IMFdat->compMod64->name = "V2Decomp"
_IMFdat->compMod64->version = "V05"
_IMFdat->compMod64->shortName = "ColorV2"
_IMFdat->compMod64->description = "V2 Coloring"
_IMFdat->compMod64->outputLocation = "figGroup"
_IMFdat->compMod64->showAllMarkers = nil
_IMFdat->compMod64->slider = "Decomposition"

;; Component Module 65 Definition
_IMFdat->compMod65 = list(nil)
_IMFdat->compMod65->name = "M3Decomp"
_IMFdat->compMod65->version = "V05"
_IMFdat->compMod65->shortName = "ColorM3"
_IMFdat->compMod65->description = "M3 Coloring"
_IMFdat->compMod65->outputLocation = "figGroup"
_IMFdat->compMod65->showAllMarkers = nil
_IMFdat->compMod65->slider = "Decomposition"

;; Component Module 66 Definition
_IMFdat->compMod66 = list(nil)
_IMFdat->compMod66->name = "V3Decomp"
_IMFdat->compMod66->version = "V05"
_IMFdat->compMod66->shortName = "ColorV3"
_IMFdat->compMod66->description = "V3 Coloring"
_IMFdat->compMod66->slider = "Decomposition"

;; Component Module 67 Definition
_IMFdat->compMod67 = list(nil)
_IMFdat->compMod67->name = "ColorAll"
_IMFdat->compMod67->version = "V05"
_IMFdat->compMod67->shortName = "ColorAll"
_IMFdat->compMod67->description = "Color All Vias"
_IMFdat->compMod67->flowList = list("compMod62" "compMod64" "compMod66")
_IMFdat->compMod67->slider = "Decomposition"

;; Component Module 60 Definition
_IMFdat->compMod60 = list(nil)
_IMFdat->compMod60->name = "AutoColor"
_IMFdat->compMod60->version = "V05"
_IMFdat->compMod60->shortName = "AutoColor"
_IMFdat->compMod60->description = "Virtuoso Color Selected Layer"
_IMFdat->compMod60->slider = "Decomposition"

;; Component Module 200 Definition
_IMFdat->compMod200 = list(nil)
_IMFdat->compMod200->name = "CreateDummyRow"
_IMFdat->compMod200->version = "V05"
_IMFdat->compMod200->shortName = "CreateDummyRow"
_IMFdat->compMod200->description = "Mark Region as Dummy Row"
_IMFdat->compMod200->slider = "Region-driven Design Flow"

;; Component Module 201 Definition
_IMFdat->compMod201 = list(nil)
_IMFdat->compMod201->name = "CreateTapRow"
_IMFdat->compMod201->version = "V05"
_IMFdat->compMod201->shortName = "CreateTapRow"
_IMFdat->compMod201->description = "Mark Region as Tap Row"
_IMFdat->compMod201->slider = "Region-driven Design Flow"

;; Component Module 202 Definition
_IMFdat->compMod202 = list(nil)
_IMFdat->compMod202->name = "RowBasedFill"
_IMFdat->compMod202->version = "V05"
_IMFdat->compMod202->shortName = "RBF"
_IMFdat->compMod202->outputLocation = "Shapes"
_IMFdat->compMod202->description = "Row-based Fill"
_IMFdat->compMod202->resizeRowAndPRB = t
_IMFdat->compMod202->skipAutoRegionResize = nil
_IMFdat->compMod202->slider = "Region-driven Design Flow"

;; Component Module 206 Definition
_IMFdat->compMod206 = list(nil)
_IMFdat->compMod206->name = "RowBasedTx"
_IMFdat->compMod206->version = "V05"
_IMFdat->compMod206->shortName = "RBTX"
_IMFdat->compMod206->outputLocation = "Shapes"
_IMFdat->compMod206->description = "Row-based Transition"
_IMFdat->compMod206->slider = "Region-driven Design Flow"

;; Component Module 212 Definition
_IMFdat->compMod212 = list(nil)
_IMFdat->compMod212->name = "RowBasedTap"
_IMFdat->compMod212->version = "V05"
_IMFdat->compMod212->shortName = "RBT"
_IMFdat->compMod212->outputLocation = "Shapes"
_IMFdat->compMod212->description = "Row-based Tap Insertion"
_IMFdat->compMod212->showAllMarkers = nil
_IMFdat->compMod212->slider = "Region-driven Design Flow"

;; Component Module 216 Definition
_IMFdat->compMod216 = list(nil)
_IMFdat->compMod216->name = "RowTermination"
_IMFdat->compMod216->version = "V05"
_IMFdat->compMod216->shortName = "RBTERM"
_IMFdat->compMod216->outputLocation = "Shapes"
_IMFdat->compMod216->description = "Row-based Termination"
_IMFdat->compMod216->slider = "Region-driven Design Flow"

;; Component Module 171 Definition
_IMFdat->compMod171 = list(nil)
_IMFdat->compMod171->name = "GetPlacement"
_IMFdat->compMod171->version = "V05"
_IMFdat->compMod171->shortName = "GetPlacement"
_IMFdat->compMod171->description = "Save Instance Placement to File"
_IMFdat->compMod171->slider = "Migration"

;; Component Module 172 Definition
_IMFdat->compMod172 = list(nil)
_IMFdat->compMod172->name = "SetPlacement"
_IMFdat->compMod172->version = "V05"
_IMFdat->compMod172->shortName = "SetPlacement"
_IMFdat->compMod172->description = "Read Instance Placement from File"
_IMFdat->compMod172->slider = "Migration"

;; Component Module 173 Definition
_IMFdat->compMod173 = list(nil)
_IMFdat->compMod173->name = "GetShapes"
_IMFdat->compMod173->version = "V05"
_IMFdat->compMod173->shortName = "MigShapes"
_IMFdat->compMod173->description = "Get Shapes from Other Cell"
_IMFdat->compMod173->slider = "Migration"

;; Component Module 175 Definition
_IMFdat->compMod175 = list(nil)
_IMFdat->compMod175->name = "ReStepObjects"
_IMFdat->compMod175->version = "V05"
_IMFdat->compMod175->shortName = "ReStepObjects"
_IMFdat->compMod175->description = "Re-Step Selected Objects"
_IMFdat->compMod175->slider = "Migration"

;; Component Module 179 Definition
_IMFdat->compMod179 = list(nil)
_IMFdat->compMod179->name = "InitRBPSettings"
_IMFdat->compMod179->version = "V05"
_IMFdat->compMod179->shortName = "RBPSetup"
_IMFdat->compMod179->description = "Initialize Region-driven Design Flow"
_IMFdat->compMod179->envVars = list(nil)
_IMFdat->compMod179->envVars->RBP_N_COMPONENTS = "n1hvt_finfet n1hvt_s_finfet n1lvt_finfet n1lvt_s_finfet n1svt_finfet n1svt_s_finfet n2svt_finfet n2svt_s_finfet"
_IMFdat->compMod179->envVars->RBP_P_COMPONENTS = "p1hvt_finfet p1hvt_s_finfet p1lvt_finfet p1lvt_s_finfet p1svt_finfet p1svt_s_finfet p2svt_finfet p2svt_s_finfet"
_IMFdat->compMod179->slider = "Region-driven Design Flow"

;; Component Module 180 Definition
_IMFdat->compMod180 = list(nil)
_IMFdat->compMod180->name = "GenFromSource"
_IMFdat->compMod180->version = "V05"
_IMFdat->compMod180->shortName = "GenFromSource"
_IMFdat->compMod180->description = "Generate All from Source"
_IMFdat->compMod180->slider = "Region-driven Design Flow"

;; Component Module 182 Definition
_IMFdat->compMod182 = list(nil)
_IMFdat->compMod182->name = "LoadRowTemplates"
_IMFdat->compMod182->version = "V05"
_IMFdat->compMod182->shortName = "LoadRowTemplates"
_IMFdat->compMod182->description = "Load Row Templates"
_IMFdat->compMod182->slider = "Region-driven Design Flow"

;; Component Module 184 Definition
_IMFdat->compMod184 = list(nil)
_IMFdat->compMod184->name = "LoadGateWSPs"
_IMFdat->compMod184->version = "V05"
_IMFdat->compMod184->shortName = "LoadGateWSPs"
_IMFdat->compMod184->description = "Load Gate WSP Templates"
_IMFdat->compMod184->slider = "Region-driven Design Flow"

;; Component Module 188 Definition
_IMFdat->compMod188 = list(nil)
_IMFdat->compMod188->name = "PCellOpt"
_IMFdat->compMod188->version = "V05"
_IMFdat->compMod188->shortName = "PCellOpt"
_IMFdat->compMod188->description = "Optimize PCell Parameters"
_IMFdat->compMod188->parList1 = list("ldummy" "rdummy")
_IMFdat->compMod188->parValue1 = "None"
_IMFdat->compMod188->slider = "Region-driven Design Flow"

;; Component Module 190 Definition
_IMFdat->compMod190 = list(nil)
_IMFdat->compMod190->name = "CreateRows"
_IMFdat->compMod190->version = "V05"
_IMFdat->compMod190->shortName = "CreateRows"
_IMFdat->compMod190->description = "Create Row Regions"
_IMFdat->compMod190->slider = "Region-driven Design Flow"

;; Component Module 192 Definition
_IMFdat->compMod192 = list(nil)
_IMFdat->compMod192->name = "CreateWSPRegions"
_IMFdat->compMod192->version = "V05"
_IMFdat->compMod192->shortName = "CreateWSPRegions"
_IMFdat->compMod192->description = "Create Gate WSP Regions"
_IMFdat->compMod192->slider = "Region-driven Design Flow"

;; Component Module 194 Definition
_IMFdat->compMod194 = list(nil)
_IMFdat->compMod194->name = "Place"
_IMFdat->compMod194->version = "V05"
_IMFdat->compMod194->shortName = "Place"
_IMFdat->compMod194->description = "Run Placement"
_IMFdat->compMod194->slider = "Region-driven Design Flow"

;; Component Module 195 Definition
_IMFdat->compMod195 = list(nil)
_IMFdat->compMod195->name = "AbutInsts"
_IMFdat->compMod195->version = "V05"
_IMFdat->compMod195->shortName = "AbutInsts"
_IMFdat->compMod195->description = "Abut Selected Instances"
_IMFdat->compMod195->slider = "Region-driven Design Flow"

;; Component Module 220 Definition
_IMFdat->compMod220 = list(nil)
_IMFdat->compMod220->name = "LoadMetalWSPs"
_IMFdat->compMod220->version = "V05"
_IMFdat->compMod220->shortName = "LoadMetalWSPs"
_IMFdat->compMod220->description = "Load Metal WSP Templates"
_IMFdat->compMod220->slider = "Region-driven Design Flow"

;; Component Module 197 Definition
_IMFdat->compMod197 = list(nil)
_IMFdat->compMod197->name = "DeleteRows"
_IMFdat->compMod197->version = "V05"
_IMFdat->compMod197->shortName = "DeleteRows"
_IMFdat->compMod197->description = "Delete Row Regions"
_IMFdat->compMod197->slider = "Utilities"

;; Component Module 198 Definition
_IMFdat->compMod198 = list(nil)
_IMFdat->compMod198->name = "DeleteInactiveGateWSPs"
_IMFdat->compMod198->version = "V05"
_IMFdat->compMod198->shortName = "DeleteInactiveGateWSPs"
_IMFdat->compMod198->description = "Delete Inactive Poly WSPs"
_IMFdat->compMod198->slider = "Region-driven Design Flow"

;; Component Module 199 Definition
_IMFdat->compMod199 = list(nil)
_IMFdat->compMod199->name = "DeleteWSPTemplates"
_IMFdat->compMod199->shortName = "DelWSPs"
_IMFdat->compMod199->version = "V05"
_IMFdat->compMod199->description = "Delete WSP Templates"
_IMFdat->compMod199->slider = "Utilities"

;; Component Module 150 Definition
_IMFdat->compMod150 = list(nil)
_IMFdat->compMod150->name = "FillFlow1"
_IMFdat->compMod150->version = "V05"
_IMFdat->compMod150->shortName = "FillFlow1"
_IMFdat->compMod150->flowList = list("compMod45" "compMod55" "compMod61" "compMod95" "compMod61")
_IMFdat->compMod150->description = "Run Trim, Color and Fill"
_IMFdat->compMod150->slider = "Custom Flows"

;; Component Module 80 Definition
_IMFdat->compMod80 = list(nil)
_IMFdat->compMod80->name = "SchDesignInventory"
_IMFdat->compMod80->version = "V05"
_IMFdat->compMod80->shortName = "SchDesignInventory"
_IMFdat->compMod80->description = "Schematic Design Inventory"
_IMFdat->compMod80->menuDisplay = list("schematic")
_IMFdat->compMod80->slider = "Migration"

;; Component Module 81 Definition
_IMFdat->compMod81 = list(nil)
_IMFdat->compMod81->name = "LayDesignInventory"
_IMFdat->compMod81->version = "V05"
_IMFdat->compMod81->shortName = "LayDesignInventory"
_IMFdat->compMod81->description = "Design Inventory: Layout"
_IMFdat->compMod81->slider = "Design Inventory"

;; Component Module 82 Definition
_IMFdat->compMod82 = list(nil)
_IMFdat->compMod82->name = "DevDesignInventory"
_IMFdat->compMod82->version = "V05"
_IMFdat->compMod82->shortName = "DevDesignInventory"
_IMFdat->compMod82->description = "Design Inventory: PDK Device"
_IMFdat->compMod82->slider = "Design Inventory"

;; Component Module 83 Definition
_IMFdat->compMod83 = list(nil)
_IMFdat->compMod83->name = "cdfDesignInventory"
_IMFdat->compMod83->version = "V05"
_IMFdat->compMod83->shortName = "cdfDesignInventory"
_IMFdat->compMod83->description = "Design Inventory: CDF Dump"
_IMFdat->compMod83->slider = "Design Inventory"

;; Component Module 49 Definition
_IMFdat->compMod49 = list(nil)
_IMFdat->compMod49->name = "CellWrapper"
_IMFdat->compMod49->version = "V05"
_IMFdat->compMod49->shortName = "WRAP"
_IMFdat->compMod49->description = "Wrap Cell with Cells"
_IMFdat->compMod49->outputLocation = "CheckCell"
_IMFdat->compMod49->outputStyle = "Separate"
_IMFdat->compMod49->slider = "Layout Toolbox"

;; Component Module 1101 Definition
_IMFdat->compMod1101 = list(nil)
_IMFdat->compMod1101->name = "LaunchQuickview"
_IMFdat->compMod1101->version = "V01"
_IMFdat->compMod1101->shortName = "LaunchQuickview"
_IMFdat->compMod1101->description = "Launch CPA Studio"
_IMFdat->compMod1101->slider = "VALE Module Utilities"

;; Component Module 1102 Definition
_IMFdat->compMod1102 = list(nil)
_IMFdat->compMod1102->name = "CreateLPAModule"
_IMFdat->compMod1102->version = "V01"
_IMFdat->compMod1102->shortName = "CreateLPAModule"
_IMFdat->compMod1102->description = "Create a Pattern (LPA) Module"
_IMFdat->compMod1102->slider = "VALE Module Utilities"

;; New module to create SKILL modules
_IMFdat->compMod401 = list(nil)
_IMFdat->compMod401->name = "CreateSKILLModule"
_IMFdat->compMod401->version = "V01"
_IMFdat->compMod401->shortName = "CreateSKILLModule"
_IMFdat->compMod401->description = "Create a SKILL Module"
_IMFdat->compMod401->slider = "VALE Module Utilities"

;; Module defined by moving compMod2055 to this mod
_IMFdat->compMod440 = list(nil)
_IMFdat->compMod440->name = "MoveModule"
_IMFdat->compMod440->version = "V01"
_IMFdat->compMod440->shortName = "MoveModule"
_IMFdat->compMod440->description = "Move a Module to new Module Number"
_IMFdat->compMod440->slider = "VALE Module Utilities"

;; VALE created LPA module 50 from template
_IMFdat->compMod50 = list(nil)
_IMFdat->compMod50->name = "ViaInterxOpt"
_IMFdat->compMod50->version = "V01"
_IMFdat->compMod50->shortName = "ViaInterxOpt"
_IMFdat->compMod50->description = "Optimize Via Intersection"
_IMFdat->compMod50->slider = "Layout Toolbox"
_IMFdat->compMod50->timeout = "300"
_IMFdat->compMod50->showAllMarkers = nil
_IMFdat->compMod50->doDRCChecking = nil
_IMFdat->compMod50->saveCheckpoint = nil

;;VALE created SKILL module from template
_IMFdat->compMod441 = list(nil)
_IMFdat->compMod441->name = "RemoveAVALEModule"
_IMFdat->compMod441->version = "V01"
_IMFdat->compMod441->shortName = "RemoveAVALEModule"
_IMFdat->compMod441->description = "Remove a VALE Module"
_IMFdat->compMod441->slider = "VALE Module Utilities"

;;VALE created SKILL module from template
;;removed
;;_IMFdat->compMod1112 = list(nil)
;;removed
;;_IMFdat->compMod1112->name = "ResetGrids"
;;removed
;;_IMFdat->compMod1112->version = "V01"
;;removed
;;_IMFdat->compMod1112->shortName = "ResetGrids"
;;removed
;;_IMFdat->compMod1112->description = "Reset Display Grids"
;;removed
;;_IMFdat->compMod1112->slider = "Custom Flows"


