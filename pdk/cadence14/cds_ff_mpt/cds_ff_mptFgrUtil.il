;rules table
;===================================================
defvar( cds_ff_mptFgrRules )
cds_ff_mptFgrRules = makeTable("cds_ff_mptFgrRules" nil)
cds_ff_mptFgrRules["Initialized"] = nil
cds_ff_mptFgrRules["minRingWidthHSeg"] = 0.062
cds_ff_mptFgrRules["minRingWidthVSeg"] = 0.190
cds_ff_mptFgrRules["FinWidth"] = 0.014
cds_ff_mptFgrRules["FinSpace"] = 0.034
cds_ff_mptFgrRules["FinPitch"] = 0.048
cds_ff_mptFgrRules["minFin"] = 2
cds_ff_mptFgrRules["maxFin"] = 10
cds_ff_mptFgrRules["minVertActFin"] = 2
cds_ff_mptFgrRules["maxVertActFin"] = 100
cds_ff_mptFgrRules["msVertAct"] = 4
cds_ff_mptFgrRules["PolyPitchList"]  = list("0.086" "0.09" "0.094" "0.102" "0.104")
cds_ff_mptFgrRules["PolyWidth"] = 0.018;techGetSpacingRule(tech "allowedWidthRanges" "Poly")
cds_ff_mptFgrRules["PolySpace"] = 0.068;techGetSpacingRule(tech "minSpacing" "Poly")
cds_ff_mptFgrRules["minFing"] = 3
cds_ff_mptFgrRules["maxFing"] = 10
cds_ff_mptFgrRules["Li1Width"]  = 0.030;techGetSpacingRule(tech "allowedWidthRanges" "LiAct")
cds_ff_mptFgrRules["Li1Space"]  = 0.056;techGetSpacingRule(tech "minSpacing" "LiAct")
cds_ff_mptFgrRules["Li1Extension"]  = 0.018
cds_ff_mptFgrRules["PolyExtension"] = 0.048
cds_ff_mptFgrRules["MfgResolution"] = 0.001;techGetMfgGridResolution(tech)
cds_ff_mptFgrRules["meImpNDiff"] = 0.065
cds_ff_mptFgrRules["meImpPDiff"] = 0.065
cds_ff_mptFgrRules["meFinDiffX"] = 0.017
cds_ff_mptFgrRules["meFinDiffY"] = 0.048
cds_ff_mptFgrRules["mwV0"] = 0.032
cds_ff_mptFgrRules["mlV0"] = 0.032
cds_ff_mptFgrRules["msV0"] = 0.042
cds_ff_mptFgrRules["meLiV0"] = -0.001
cds_ff_mptFgrRules["meDiffV0"] = 0.015
cds_ff_mptFgrRules["msImp"] = 0.052
cds_ff_mptFgrRules["mwViaList"] = list(0.032 0.032)
cds_ff_mptFgrRules["mlViaList"] = list(0.032 0.032)
cds_ff_mptFgrRules["msViaList"] = list(0.08 0.08)
cds_ff_mptFgrRules["meMetViaList"] = list(0.018 0.018 0.018)
cds_ff_mptFgrRules["meeMetViaList"] = list(0.018 0.018 0.018)
cds_ff_mptFgrRules["meMetViaList2"] = list(0.01 0.01 0.01)
cds_ff_mptFgrRules["meeMetViaList2"] = list(0.028 0.028 0.028)
cds_ff_mptFgrRules["metViaList2Trip"] = .068
cds_ff_mptFgrRules["topMetList"] = list("M1" "M2" "M3")
cds_ff_mptFgrRules["topViaList"] = list("V1" "V2")
cds_ff_mptFgrRules["diffLayer"] = "Active"
cds_ff_mptFgrRules["impNLayer"] = "Nsvt"
cds_ff_mptFgrRules["wellNwLayer"] = "NWell"
cds_ff_mptFgrRules["impPLayer"] = "Psvt"
cds_ff_mptFgrRules["liLayer"] = "LiAct"
cds_ff_mptFgrRules["v0Layer"] = "V0"
cds_ff_mptFgrRules["polyLayer"] = "Poly"
cds_ff_mptFgrRules["polyPurp"] = "dummy"
cds_ff_mptFgrRules["finLayer"] = "FinArea"
cds_ff_mptFgrRules["finPurp"] = "fin48"
cds_ff_mptFgrRules["vertRefLPP"] = list("Active_drawing" "Poly_drawing" "Nsvt_drawing" "Psvt_drawing")
cds_ff_mptFgrRules["horizRefLPP"] = list("Active_drawing" "Poly_drawing" "Nsvt_drawing" "Psvt_drawing")
;===================================================
;End build table

;API to gen rule value by name
procedure(cds_ff_mptFgrGetRuleValue(ruleName)
    if(cds_ff_mptFgrRules[ruleName] cds_ff_mptFgrRules[ruleName] 0.0)
) ;cds_ff_mptFgrGetRuleValue

;rule table initialization
procedure(cds_ff_mptFgrUpdateRuleValue(gr) let((tech)
    unless(cds_ff_mptFgrRules["Initialized"]
        tech = techGetTechFile(ddGetObj(gr->cv->libName))
        when(type(techGetSpacingRule(tech "minSpacing" "Poly")) == 'flonum
            cds_ff_mptFgrRules["PolySpace"] = techGetSpacingRule(tech "minSpacing" "Poly")
        )
        when(type(car(techGetSpacingRule(tech "allowedWidthRanges" "Poly"))) == 'flonum
            cds_ff_mptFgrRules["PolyWidth"] = car(techGetSpacingRule(tech "allowedWidthRanges" "Poly"))
        )
        when(type(techGetSpacingRule(tech "minSpacing" "LiAct")) == 'flonum
            cds_ff_mptFgrRules["LiActSpace"] = techGetSpacingRule(tech "minSpacing" "LiAct")
        )
        when(type(car(techGetSpacingRule(tech "allowedWidthRanges" "LiAct"))) == 'flonum
            cds_ff_mptFgrRules["LiActWidth"] = car(techGetSpacingRule(tech "allowedWidthRanges" "LiAct"))
        )
        when(cds_ff_mptFgrRules["FinPitch"] - cds_ff_mptFgrRules["FinWidth"] > 0
            cds_ff_mptFgrRules["FinSpace"] = cds_ff_mptFgrRules["FinPitch"] - cds_ff_mptFgrRules["FinWidth"]
        )
        when(type(techGetMfgGridResolution(tech)) == 'flonum
            cds_ff_mptFgrRules["MfgResolution"] = techGetMfgGridResolution(tech)
        )
        cds_ff_mptFgrRules["Initialized"] = t
    )
)) ;cds_ff_mptFgrUpdateRuleValue

;register tf change callback to recal rule value
procedure(cds_ff_mptFgrPreLoadTechTriggerFunc(techId techfile)
    cds_ff_mptFgrRules["Initialized"] = nil
) ;cds_ff_mptFgrPreLoadTechTriggerFunc

tcRegPostLoadTrigger('cds_ff_mptFgrPreLoadTechTriggerFunc)

;procedure to set prop of user define form field 
procedure(cds_ff_mptFgrSetCreateFormUserFieldProp(promptString property value) let((actField)
    importSkillVar(vfoGRAddFieldsInCommonQ)
    actField = car(setof(filed foreach(mapcar fieldRecList vfoGRAddFieldsInCommonQ car(fieldRecList)) filed->prompt == promptString || filed->buttonText == promptString))
    when(actField
        evalstring(sprintf(nil "vfoGRGetCommonQPtr()->%s->%s = %s" actField->hiFieldSym property value))
    )
)) ;cds_ff_mptFgrSetCreateFormUserFieldProp

;procedure to get prop of user define form field
procedure(cds_ff_mptFgrGetCreateFormUserFieldProp(promptString property) let((actField)
    importSkillVar(vfoGRAddFieldsInCommonQ)
    actField = car(setof(filed foreach(mapcar fieldRecList vfoGRAddFieldsInCommonQ car(fieldRecList)) filed->prompt == promptString || filed->buttonText == promptString))
    when(actField
        evalstring(sprintf(nil "vfoGRGetCommonQPtr()->%s->%s" actField->hiFieldSym property))
    )
)) ;cds_ff_mptFgrGetCreateFormUserFieldProp

defclass(cds_ff_mptFgrGuardRing (vfoAdvGuardRing) 
    (
        (topMetal @initarg topMetal @initform "M1");using to GR extension - topMetal
        (vertSegActLen @initarg vertSegActLen @initform 2)
    )
) ;cds_ff_mptFgrGuardRing

defclass(cds_ff_mptFgrGuardRing_ver_0 (cds_ff_mptFgrGuardRing) ());version control

defclass(cds_ff_mptFgrGuardRing_ver_1 (cds_ff_mptFgrGuardRing_ver_0);version control
    ()
) ;cds_ff_mptFgrGuardRing_ver_1

;Need to define to support edit operation
defmethod(vfoGRGetExtraArgumentName ((obj cds_ff_mptFgrGuardRing))
    append( callNextMethod()
        list("topMetal"
             "vertSegActLen"
             "userHorizPitch"
             "userHorizSegWidth"
	     "userHorizRefLPP"
	     "userHorizEnclose"
	     "userHorizHalfGapW"
	     "userMinHorizSegLength"
             "userVertSegWidth"
	     "userVertRefLPP"
	     "userVertEnclose"
	     "userVertHalfGapW"
	     "userMinVertSegLength"
             "numFingers" 
             "numFins"))
)

;procedure to create user defined CDF while install FGR device automatically
defmethod(vfoAdvGRUpdateCDF ( (obj cds_ff_mptFgrGuardRing) libName cellName viewName) let((cellId cdfId paramId cvId)
    cellId = ddGetObj(libName cellName)
    cdfId = cdfGetBaseCellCDF(cellId)
    unless(cdfId
        cdfId = cdfCreateBaseCellCDF(cellId)
    );;unless
    cvId = dbFindOpenCellView(ddGetObj(libName) cellName viewName)
    ;create user defined parameter
    when(cdfFindParamByName(cdfId "topMetal")
        cdfDeleteParam(cdfFindParamByName(cdfId "topMetal"))
    )
    cdfCreateParam(cdfId
        ?name           "topMetal"
        ?prompt         "Top Metal"
        ?choices        cds_ff_mptFgrGetRuleValue("topMetList")
        ?defValue       if(cvId->topMetal cvId->topMetal "M1");sync default from tf
        ?type           "cyclic"
        ?display        "t"
    )
    putprop(cdfId->readers '(lambda (x) x) "topMetal")

    when(cdfFindParamByName(cdfId "userHorizPitch")
        cdfDeleteParam(cdfFindParamByName(cdfId "userHorizPitch"))
    )
    cdfCreateParam(cdfId
        ?name           "userHorizPitch"
        ?prompt         "Poly Pitch"
	?choices        cds_ff_mptFgrGetRuleValue("PolyPitchList")
        ?defValue       car(cds_ff_mptFgrGetRuleValue("PolyPitchList"))
        ?type           "cyclic"
        ?display        "t"
	?callback       "cds_ff_mptFgrHorizPitchCB() cds_ff_mptFgrVertSegWidthCB() cds_ff_mptFgrHorizMinSegLenCB()"
    )
    putprop(cdfId->readers '(lambda (x) x) "userHorizPitch")

    when(cdfFindParamByName(cdfId "userHorizSegWidth")
        cdfDeleteParam(cdfFindParamByName(cdfId "userHorizSegWidth"))
    )
    cdfCreateParam(cdfId
        ?name           "userHorizSegWidth"
        ?prompt         "Horiz Seg W"
        ?defValue       cds_ff_mptFgrGetRuleValue("minRingWidthHSeg")
        ?type           "float"
        ?display        "t"
	?callback       "cds_ff_mptFgrHorizSegWidthCB()"
    )
    putprop(cdfId->readers '(lambda (x) x) "userHorizSegWidth")

    when(cdfFindParamByName(cdfId "userVertSegWidth")
        cdfDeleteParam(cdfFindParamByName(cdfId "userVertSegWidth"))
    )
    cdfCreateParam(cdfId
        ?name           "userVertSegWidth"
        ?prompt         "Vert Seg W"
        ?defValue       cds_ff_mptFgrGetRuleValue("minRingWidthVSeg")
        ?type           "float"
        ?display        "t"
	?callback       "cds_ff_mptFgrVertSegWidthCB()"
    )
    putprop(cdfId->readers '(lambda (x) x) "userVertSegWidth")

    when(cdfFindParamByName(cdfId "vertSegActLen")
        cdfDeleteParam(cdfFindParamByName(cdfId "vertSegActLen"))
    )
    cdfCreateParam(cdfId
        ?name           "vertSegActLen"
        ?prompt         "Vertical Seg Active Fins"
        ?defValue       cds_ff_mptFgrGetRuleValue("minVertActFin")
        ?type           "int"
        ?display        "t"
	?callback       "cds_ff_mptFgrVertSegActLenCB()"
    )
    putprop(cdfId->readers '(lambda (x) x) "vertSegActLen")

    when(cdfFindParamByName(cdfId "numFins")
        cdfDeleteParam(cdfFindParamByName(cdfId "numFins"))
    )
    cdfCreateParam(cdfId
        ?name           "numFins"
        ?prompt         "Fins"
        ?defValue       cds_ff_mptFgrGetRuleValue("minFin")
        ?type           "int"
        ?display        "t"
        ?editable       "nil"
	?callback       "nil"
    )
    putprop(cdfId->readers '(lambda (x) x) "numFins")

    when(cdfFindParamByName(cdfId "numFingers")
        cdfDeleteParam(cdfFindParamByName(cdfId "numFingers"))
    )
    cdfCreateParam(cdfId
        ?name           "numFingers"
        ?prompt         "Fingers"
        ?defValue       cds_ff_mptFgrGetRuleValue("minFing")
        ?type           "int"
        ?display        "t"
        ?editable       "nil"
	?callback       "nil"
    )
    putprop(cdfId->readers '(lambda (x) x) "numFingers")

    ;wrap parameters
    when(cdfFindParamByName(cdfId "userVertRefLPP")
        cdfDeleteParam(cdfFindParamByName(cdfId "userVertRefLPP"))
    )
    cdfCreateParam(cdfId
        ?name           "userVertRefLPP"
        ?prompt         "Vertical Ref"
        ?defValue       "none"
        ?type           "string"
        ?display        "t"
        ?editable       "nil"
    )
    putprop(cdfId->readers '(lambda (x) x) "userVertRefLPP")

    when(cdfFindParamByName(cdfId "userHorizRefLPP")
        cdfDeleteParam(cdfFindParamByName(cdfId "userHorizRefLPP"))
    )
    cdfCreateParam(cdfId
        ?name           "userHorizRefLPP"
        ?prompt         "Horizontal Ref"
        ?defValue       "none"
        ?type           "string"
        ?display        "t"
        ?editable       "nil"
    )
    putprop(cdfId->readers '(lambda (x) x) "userHorizRefLPP")

    when(cdfFindParamByName(cdfId "userHorizEnclose")
        cdfDeleteParam(cdfFindParamByName(cdfId "userHorizEnclose"))
    )
    cdfCreateParam(cdfId
        ?name           "userHorizEnclose"
        ?prompt         "Horizontal Enc"
        ?defValue       0.0
        ?type           "float"
        ?display        "t"
        ?editable       "nil"
    )
    putprop(cdfId->readers '(lambda (x) x) "userHorizEnclose")

    when(cdfFindParamByName(cdfId "userVertEnclose")
        cdfDeleteParam(cdfFindParamByName(cdfId "userVertEnclose"))
    )
    cdfCreateParam(cdfId
        ?name           "userVertEnclose"
        ?prompt         "Vertical Enc"
        ?defValue       0.0
        ?type           "float"
        ?display        "t"
        ?editable       "nil"
    )
    putprop(cdfId->readers '(lambda (x) x) "userVertEnclose")

    when(cdfFindParamByName(cdfId "userVertHalfGapW")
        cdfDeleteParam(cdfFindParamByName(cdfId "userVertHalfGapW"))
    )
    cdfCreateParam(cdfId
        ?name           "userVertHalfGapW"
        ?prompt         "Vertical Half Gap"
        ?defValue       0.0
        ?type           "float"
        ?display        "t"
        ?editable       "nil"
    )
    putprop(cdfId->readers '(lambda (x) x) "userVertHalfGapW")

    when(cdfFindParamByName(cdfId "userHorizHalfGapW")
        cdfDeleteParam(cdfFindParamByName(cdfId "userHorizHalfGapW"))
    )
    cdfCreateParam(cdfId
        ?name           "userHorizHalfGapW"
        ?prompt         "Horizontal Half Gap"
        ?defValue       0.0
        ?type           "float"
        ?display        "t"
        ?editable       "nil"
    )
    putprop(cdfId->readers '(lambda (x) x) "userHorizHalfGapW")

    when(cdfFindParamByName(cdfId "userMinVertSegLength")
        cdfDeleteParam(cdfFindParamByName(cdfId "userMinVertSegLength"))
    )
    cdfCreateParam(cdfId
        ?name           "userMinVertSegLength"
        ?prompt         "Vertical Min Seg Len"
        ?defValue       0.384
        ?type           "float"
        ?display        "t"
        ?editable       "nil"
	?callback       "cds_ff_mptFgrVertMinSegLenCB()"
    )
    putprop(cdfId->readers '(lambda (x) x) "userMinVertSegLength")

    when(cdfFindParamByName(cdfId "userMinHorizSegLength")
        cdfDeleteParam(cdfFindParamByName(cdfId "userMinHorizSegLength"))
    )
    cdfCreateParam(cdfId
        ?name           "userMinHorizSegLength"
        ?prompt         "Horizontal Min Seg Len"
        ?defValue       0.258
        ?type           "float"
        ?display        "t"
        ?editable       "nil"
	?callback       "cds_ff_mptFgrHorizMinSegLenCB()"
    )
    putprop(cdfId->readers '(lambda (x) x) "userMinHorizSegLength")

    foreach(param cdfId->parameters~>name
        paramId = cdfFindParamByName(cdfId param)
        when(paramId
	    unless(paramId->name == "shapeData" || 
		   paramId->name == "topMetal" || 
		   paramId->name == "userVertSegWidth" || 
		   paramId->name == "userHorizPitch" ||
		   paramId->name == "userHorizSegWidth" ||
		   paramId->name == "userMinHorizSegLength" ||
		   paramId->name == "userMinVertSegLength" ||
		   paramId->name == "vertSegActLen" ||
		   paramId->name == "numFingers" ||
		   paramId->name == "numFins"
                paramId->display = "nil"
	    )
        )
    )

    cdfId->doneProc = "cds_ff_mptDoneProc"

    cdfSaveCDF(cdfId)
)) ;vfoUpdateCDF

;modify the create form size
when(isCallable('vfoGRUpdateCreateFormSize) vfoGRUpdateCreateFormSize(400 580))


;procedure to add user defined field on GR creation form
procedure(vfoGRAddCreateFormFields() let((UserSelectTopMet UserSelectFingers UserSelectFins
                                          UserSelectHorizWidth UserSelectHorizRefLPP 
					  UserSelectHorizEnclose UserSelectHorizHalfGapW
					  UserSelectVertWidth UserSelectVertRefLPP 
					  UserSelectVertEnclose UserSelectVertHalfGapW
					  UserSelectMinHorizSegLength UserSelectMinVertSegLength
					  UserSelectPolyPitch UserSelectVertSegActLen
					 )
    importSkillVar(vfoGRAddFieldsInCommonQ)
    UserSelectTopMet = hiCreateCyclicField(
                     ?name        'UserSelectTopMet
                     ?prompt      "Top Metal"
                     ?choices     cds_ff_mptFgrGetRuleValue("topMetList")
                     ?value       car(cds_ff_mptFgrGetRuleValue("topMetList"))
                     ?defValue    car(cds_ff_mptFgrGetRuleValue("topMetList"))
                     ?callback    "cds_ff_mptFgrUserCreateCB()"
                     )
    UserSelectPolyPitch = hiCreateCyclicField(
                     ?name        'UserSelectPolyPitch
                     ?prompt      "Poly Pitch"
		     ?choices     cds_ff_mptFgrGetRuleValue("PolyPitchList")
                     ?value       car(cds_ff_mptFgrGetRuleValue("PolyPitchList"))
                     ?defValue    car(cds_ff_mptFgrGetRuleValue("PolyPitchList"))
                     ?callback    "cds_ff_mptFgrUserCreateCB()"
                     )
    UserSelectVertWidth = hiCreateFloatField(
                     ?name        'UserSelectVertWidth
                     ?prompt      "Vert Seg Width"
                     ?value       cds_ff_mptFgrGetRuleValue("minRingWidthVSeg")
                     ?defValue    cds_ff_mptFgrGetRuleValue("minRingWidthVSeg")
                     ?callback    "cds_ff_mptFgrUserCreateCB()"
                     )
    UserSelectVertRefLPP = hiCreateCyclicField(
                     ?name        'UserSelectVertRefLPP
                     ?prompt      "Y Direction Ref"
		     ?choices     cds_ff_mptFgrGetRuleValue("vertRefLPP")
                     ?value       cadr(cds_ff_mptFgrGetRuleValue("vertRefLPP"))
                     ?defValue    cadr(cds_ff_mptFgrGetRuleValue("vertRefLPP"))
                     ?callback    "cds_ff_mptFgrUserCreateCB()"
                     )
    UserSelectVertHalfGapW = hiCreateFloatField(
                     ?name        'UserSelectVertHalfGapW
                     ?prompt      "X Direction Half Gap W"
                     ?value       0.0
                     ?defValue    0.0
                     ?callback    "cds_ff_mptFgrUserCreateCB()"
                     )
    UserSelectVertEnclose = hiCreateFloatField(
                     ?name        'UserSelectVertEnclose
                     ?prompt      "Y Direction Enclose"
                     ?value       0.0
                     ?defValue    0.0
                     ?callback    "cds_ff_mptFgrUserCreateCB()"
                     )
    UserSelectMinVertSegLength = hiCreateFloatField(
                     ?name        'UserSelectMinVertSegLength
                     ?prompt      "Vertical Min Seg Len"
                     ?value       0.384
                     ?defValue    0.384
                     ?callback    "cds_ff_mptFgrUserCreateCB()"
                     )
    UserSelectHorizWidth = hiCreateFloatField(
                     ?name        'UserSelectHorizWidth
                     ?prompt      "Horiz Seg Width"
                     ?value       cds_ff_mptFgrGetRuleValue("minRingWidthHSeg")
                     ?defValue    cds_ff_mptFgrGetRuleValue("minRingWidthHSeg")
                     ?callback    "cds_ff_mptFgrUserCreateCB()"
                     )
    UserSelectHorizRefLPP = hiCreateCyclicField(
                     ?name        'UserSelectHorizRefLPP
                     ?prompt      "X Direction Ref"
		     ?choices     cds_ff_mptFgrGetRuleValue("horizRefLPP")
                     ?value       cadr(cds_ff_mptFgrGetRuleValue("horizRefLPP"))
                     ?defValue    cadr(cds_ff_mptFgrGetRuleValue("horizRefLPP"))
                     ?callback    "cds_ff_mptFgrUserCreateCB()"
                     )
    UserSelectHorizEnclose = hiCreateFloatField(
                     ?name        'UserSelectHorizEnclose
                     ?prompt      "X Direction Enclose"
                     ?value       0.0
                     ?defValue    0.0
                     ?callback    "cds_ff_mptFgrUserCreateCB()"
                     )
    UserSelectHorizHalfGapW = hiCreateFloatField(
                     ?name        'UserSelectHorizHalfGapW
                     ?prompt      "Y Direction Half Gap W"
                     ?value       0.0
                     ?defValue    0.0
                     ?callback    "cds_ff_mptFgrUserCreateCB()"
                     )
    UserSelectMinHorizSegLength = hiCreateFloatField(
                     ?name        'UserSelectMinHorizSegLength
                     ?prompt      "Horizontal Min Seg Len"
                     ?value       0.258
                     ?defValue    0.258
                     ?callback    "cds_ff_mptFgrUserCreateCB()"
                     )
    UserSelectFingers = hiCreateIntField(
                     ?name        'UserSelectFingers
                     ?prompt      "Fingers"
                     ?value       cds_ff_mptFgrGetRuleValue("minFing")
                     ?defValue    cds_ff_mptFgrGetRuleValue("minFing")
		     ?callback    "cds_ff_mptFgrUserCreateCB()"
                     )
    UserSelectFins = hiCreateIntField(
                     ?name        'UserSelectFins
                     ?prompt      "Fins"
                     ?value       cds_ff_mptFgrGetRuleValue("minFin")
                     ?defValue    cds_ff_mptFgrGetRuleValue("minFin")
		     ?callback    "cds_ff_mptFgrUserCreateCB()"
                     )
    UserSelectVertSegActLen = hiCreateIntField(
                     ?name        'UserSelectVertSegActLen
                     ?prompt      "Vertical Seg Active Fins"
                     ?value       cds_ff_mptFgrGetRuleValue("minVertActFin")
                     ?defValue    cds_ff_mptFgrGetRuleValue("minVertActFin")
		     ?callback    "cds_ff_mptFgrUserCreateCB()"
                     )
    vfoGRAddFieldsInCommonQ = list(
                                   list(UserSelectTopMet		10:46	100:20	80)
				   list(UserSelectPolyPitch    		10:170  100:20  80)
				   list(UserSelectVertWidth		10:200	160:20	110)
				   list(UserSelectFingers		220:200	100:20	60)
				   list(UserSelectHorizWidth		10:230	160:20	110)
				   list(UserSelectFins			220:230	100:20	60)
				   list(UserSelectVertSegActLen		10:260	200:20	140)
				   list(UserSelectVertRefLPP		10:290	200:20	100)
				   list(UserSelectVertEnclose		10:320	180:20	120)
				   list(UserSelectHorizHalfGapW		10:350	200:20	140)
				   list(UserSelectHorizRefLPP		10:380	200:20	100)
				   list(UserSelectHorizEnclose		10:410	180:20	120)
				   list(UserSelectVertHalfGapW		10:440	200:20	140)
				   list(UserSelectMinHorizSegLength	10:470	200:20	140)
   				   list(UserSelectMinVertSegLength	10:500	180:20	120)
				  );send user defined field list back to vfo
    vfoGRSetExtraArgument(list(list("topMetal" "M1")
			       list("vertSegActLen" 0)
			       list("userHorizPitch" "0.086")
                               list("userVertSegWidth" 0.0)
                               list("userVertRefLPP" "Poly_drawing")
                               list("userVertEnclose" 0.0)
                               list("userVertHalfGapW" 0.0)
			       list("userMinVertSegLength" 0.0)
			       list("userHorizSegWidth" 0.0)
                               list("userHorizRefLPP" "Poly_drawing")
                               list("userHorizEnclose" 0.0)
                               list("userHorizHalfGapW" 0.0)
			       list("userMinHorizSegLength" 0.0)
			       list("numFingers" 0)
			       list("numFins" 0)
			      ));register extra argument list for FGR customization to vfo
)) ;vfoGRAddCreateFormFields

;;modify the create form for custom FGR
procedure(vfoGRUpdateCreateForm(form) let(()
    vfoCreateFormPointer = form
    vfoGRSetCreateFormAllFieldsInvisible(t);hide all field on GR form
    vfoGRSetCreateFormFieldProp("Net Name" "invisible" "nil")
    vfoGRSetCreateFormFieldProp("Rectangular" "invisible" "nil")
    vfoGRSetCreateFormFieldProp("Wrap common" "invisible" "nil")
    vfoGRSetCreateFormFieldProp("Create Poly Ring" "value" "\"Create Ring\"")
    ;display user created fields
    cds_ff_mptFgrSetCreateFormUserFieldProp("Top Metal" "invisible" "nil")
    cds_ff_mptFgrSetCreateFormUserFieldProp("Poly Pitch" "invisible" "nil")
    cds_ff_mptFgrSetCreateFormUserFieldProp("Vert Seg Width" "invisible" "nil")
    cds_ff_mptFgrSetCreateFormUserFieldProp("Horiz Seg Width" "invisible" "nil")
    cds_ff_mptFgrSetCreateFormUserFieldProp("Fingers" "invisible" "nil")
    cds_ff_mptFgrSetCreateFormUserFieldProp("Fingers" "editable" "nil")
    cds_ff_mptFgrSetCreateFormUserFieldProp("Fins" "invisible" "nil")
    cds_ff_mptFgrSetCreateFormUserFieldProp("Fins" "editable" "nil")
    cds_ff_mptFgrSetCreateFormUserFieldProp("Vertical Seg Active Fins" "invisible" "nil")
    if(vfoGRGetCreateFormFieldProp("Main Tabs" "value") == 1 then
        cds_ff_mptFgrSetCreateFormUserFieldProp("Y Direction Ref" "invisible" "nil")
        cds_ff_mptFgrSetCreateFormUserFieldProp("X Direction Ref" "invisible" "nil")
        cds_ff_mptFgrSetCreateFormUserFieldProp("Y Direction Enclose" "invisible" "nil")
        cds_ff_mptFgrSetCreateFormUserFieldProp("X Direction Enclose" "invisible" "nil")
        cds_ff_mptFgrSetCreateFormUserFieldProp("Y Direction Half Gap W" "invisible" "nil")
        cds_ff_mptFgrSetCreateFormUserFieldProp("X Direction Half Gap W" "invisible" "nil")
	cds_ff_mptFgrSetCreateFormUserFieldProp("Vertical Min Seg Len" "invisible" "nil")
        cds_ff_mptFgrSetCreateFormUserFieldProp("Horizontal Min Seg Len" "invisible" "nil")
    else
        cds_ff_mptFgrSetCreateFormUserFieldProp("Y Direction Ref" "invisible" "t")
        cds_ff_mptFgrSetCreateFormUserFieldProp("X Direction Ref" "invisible" "t")
        cds_ff_mptFgrSetCreateFormUserFieldProp("Y Direction Enclose" "invisible" "t")
        cds_ff_mptFgrSetCreateFormUserFieldProp("X Direction Enclose" "invisible" "t")
        cds_ff_mptFgrSetCreateFormUserFieldProp("Y Direction Half Gap W" "invisible" "t")
        cds_ff_mptFgrSetCreateFormUserFieldProp("X Direction Half Gap W" "invisible" "t")
	cds_ff_mptFgrSetCreateFormUserFieldProp("Vertical Min Seg Len" "invisible" "t")
        cds_ff_mptFgrSetCreateFormUserFieldProp("Horizontal Min Seg Len" "invisible" "t")
    )
    cds_ff_mptFgrSetCreateFormUserFieldProp("Y Direction Half Gap W" "editable" "nil")
    cds_ff_mptFgrSetCreateFormUserFieldProp("X Direction Half Gap W" "editable" "nil")
    cds_ff_mptFgrSetCreateFormUserFieldProp("Vertical Min Seg Len" "editable" "nil")
    cds_ff_mptFgrSetCreateFormUserFieldProp("Horizontal Min Seg Len" "editable" "nil")
    cds_ff_mptFgrUserCreateCB();execute all user defined fields' CB
)) ;vfoGRUpdateCreateForm

;procedure to generate valid horizontal width value (draw value), used by the cdfCB and create form.
procedure(cds_ff_mptFgrCalcHorizSegWidth(val)
    let((
            (msFin       cds_ff_mptFgrGetRuleValue("FinSpace"))
	    (mwFin       cds_ff_mptFgrGetRuleValue("FinWidth"))
    	    (step        cds_ff_mptFgrGetRuleValue("FinPitch"))
    	    (minFins     cds_ff_mptFgrGetRuleValue("minFin"))
    	    (maxFins     cds_ff_mptFgrGetRuleValue("maxFin"))
	    (epsilon     0.00001)
    	    min newVal max tmp
        )
        min = (minFins * step) - msFin
        max = (maxFins * step) - msFin
        if(numberp(val) then
            tmp = (round((val - mwFin) / step) * step) + mwFin
            cond(
                 (tmp < min - epsilon
  	            newVal = list(min "Setting Horizontal Segment Width to minimum value.\n")
    	         )
	         (tmp > max + epsilon
	            newVal = list(max "Setting Horizontal Segment Width to maximum value.\n")
     	         )
		 (val < tmp - epsilon || val > tmp + epsilon
		    newVal = list(tmp "Adjusting Horizontal Segment Width to be on pitch.\n")
		 )
	         (t
	            newVal = tmp
     	         )
	    )
            else
                newVal = min
        )
	newVal
    )
) ;cds_ff_mptFgrCalcHorizSegWidth

;procedure to generate valid horizontal width value (VFO value), used by the cdfCB and create form.
procedure(cds_ff_mptFgrCalcHorizSegWidthOff(val)
    let((
         (mwFin       cds_ff_mptFgrGetRuleValue("FinWidth"))
	)
	val - mwFin
    )
) ;cds_ff_mptFgrCalcHorizSegWidthOff

;procedure to get fins from horizontal segment width
procedure(cds_ff_mptFgrGetFins(val)
    let((
         (pitch        cds_ff_mptFgrGetRuleValue("FinPitch"))
        )
        fix(val / pitch) + 1
    )
) ;cds_ff_mptFgrGetFins

;procedure to generate valid vertical width value (draw value), used by the cdfCB and create form.
procedure(cds_ff_mptFgrCalcVertSegWidth(val step)
    let((
	    (mwPol       cds_ff_mptFgrGetRuleValue("PolyWidth"))
    	    (minPoly     cds_ff_mptFgrGetRuleValue("minFing"))
    	    (maxPoly     cds_ff_mptFgrGetRuleValue("maxFing"))
	    (epsilon     0.00001)
    	    msPol min newVal max tmp
        )
	msPol = step - mwPol
        min = (minPoly * step) - msPol
        max = (maxPoly * step) - msPol
        if(numberp(val) then
            tmp = (round((val - mwPol) / step) * step) + mwPol
            cond(
                 (tmp < min - epsilon
  	             newVal = list(min "Setting Vertical Segment Width to minimum value.\n")
                 )
	         (tmp > max + epsilon
	             newVal = list(max "Setting Vertical Segment Width to maximum value.\n")
    	         )
		 (val < tmp - epsilon || val > tmp + epsilon
		     newVal = list(tmp "Adjusting Vertical Segment Width to be on pitch.\n")
		 )
	         (t
	             newVal = tmp
    	         )
	    )
            else
                newVal = min
        )
	newVal
    )
) ;cds_ff_mptFgrCalcVertSegWidth

;procedure to generate valid vertical width value (VFO value), used by the cdfCB and create form.
procedure(cds_ff_mptFgrCalcVertSegWidthOff(val)
    let((
         (mwPol       cds_ff_mptFgrGetRuleValue("PolyWidth"))
	)
	val - mwPol
    )
) ;cds_ff_mptFgrCalcVertSegWidthOff

;procedure to get fingers from vertical segment width
procedure(cds_ff_mptFgrGetFing(val step)
    let(()
        fix(val / step) + 1
     )
) ;cds_ff_mptFgrGetFing

;procedure to validate vertical segment active length
procedure(cds_ff_mptFgrGetVertSegActL(val)
    let((
         (minVal	cds_ff_mptFgrGetRuleValue("minVertActFin"))
         (maxVal	cds_ff_mptFgrGetRuleValue("maxVertActFin"))
         (epsilon	0.00001)
         newVal
        )
        ;newVal = fix(val)
        newVal = val
        cond(
             (newVal < minVal - epsilon
                 newVal = list(minVal "Adjusting Vertical Active Fins to Minimum value.\n")
             )
             (newVal > maxVal + epsilon
                 newVal = list(maxVal "Adjusting Vertical Active Fins to Maximum value.\n")
             )
        )
        newVal
     )
) ;cds_ff_mptFgrGetVertSegActL

;procedure to get vertical enclose
procedure(cds_ff_mptFgrGetVertEnclose(val w lay)
    let((
         (meImpN       cds_ff_mptFgrGetRuleValue("meImpNDiff"))
         (meImpP       cds_ff_mptFgrGetRuleValue("meImpPDiff"))
         (mePoly       cds_ff_mptFgrGetRuleValue("PolyExtension"))
         newVal
        )
	newVal = (w / 2.0) + val
	cond(
	     (lay == "Poly"
	         newVal = newVal + mePoly
	     )
	     (lay == "Active"
	         newVal = newVal
	     )
	     (lay == "Nsvt"
	         newVal = newVal + meImpN
	     )
	     (lay == "Psvt"
	         newVal = newVal + meImpP
	     )
         )
         newVal
     )
) ;cds_ff_mptFgrGetVertEnclose

;procedure to calc vertical half width
procedure(cds_ff_mptFgrCalcVertHalfW(lay w)
    let((
         (meImpN       cds_ff_mptFgrGetRuleValue("meImpNDiff"))
         (meImpP       cds_ff_mptFgrGetRuleValue("meImpPDiff"))
         (msImp        cds_ff_mptFgrGetRuleValue("msImp"))
         newVal
        )
	newVal = (w + msImp) / 2.0
	cond(
	     (lay == "Nsvt"
	         newVal = newVal + meImpN
	     )
	     (lay == "Psvt"
	         newVal = newVal + meImpP
	     )
	)
	newVal
     )
) ;cds_ff_mptFgrCalcVertHalfW

;procedure to calc vertical min segment length
procedure(cds_ff_mptFgrCalcVertMinSegL(step)
    let((
         (minNumPitch       8)
        )
     	minNumPitch * step
    )
) ;cds_ff_mptFgrCalcVertMinSegL

;procedure to get horizontal enclose
procedure(cds_ff_mptFgrGetHorizEnclose(val w lay)
    let((
         (meImpN       cds_ff_mptFgrGetRuleValue("meImpNDiff"))
         (meImpP       cds_ff_mptFgrGetRuleValue("meImpPDiff"))
         newVal
        )
	newVal = (w / 2.0) + val
	cond(
	     (lay == "Poly" || lay == "Active"
	         newVal = newVal
             )
	     (lay == "Nsvt"
	         newVal = newVal + meImpN
	     )
	     (lay == "Psvt"
	         newVal = newVal + meImpP
	     )
	)
	newVal
     )
) ;cds_ff_mptFgrGetHorizEnclose

;procedure to calc horizontal half width
procedure(cds_ff_mptFgrCalcHorizHalfW(lay w)
    let((
         (mePoly       cds_ff_mptFgrGetRuleValue("PolyExtension"))
         (msPoly       cds_ff_mptFgrGetRuleValue("PolySpace"))
         newVal
        )
	newVal = ((w + msPoly) / 2.0) + mePoly
     )
) ;cds_ff_mptFgrCalcHorizHalfW

;procedure to calc horizontal min segment length
procedure(cds_ff_mptFgrCalcHorizMinSegL(step)
    let((
         (minNumPitch       3)
        )
     	minNumPitch * step
    )
) ;cds_ff_mptFgrCalcHorizMinSegL

;CDF callback for horizontal min seg len
procedure(cds_ff_mptFgrHorizMinSegLenCB(\@optional (cdfgData inSkill(cdfgData)))
    let((step newVal)
	step = vfoGetParam(cdfgData "userHorizPitch")
	step = cdfParseFloatString(step)
	newVal = cds_ff_mptFgrCalcHorizMinSegL(step)
	vfoSetParam(cdfgData "userMinHorizSegLength" newVal)
	vfoSetParam(cdfgData "minHorizontalSegLength" newVal)
    )
) ;cds_ff_mptFgrHorizMinSegLenCB

;CDF callback for vertical seg act len
procedure(cds_ff_mptFgrVertSegActLenCB(\@optional (cdfgData inSkill(cdfgData)))
    let((input value valueNum)
	input = vfoGetParam(cdfgData "vertSegActLen")
	value = cds_ff_mptFgrGetVertSegActL(input)
	if(listp(value) then
	   valueNum = car(value)
	   when(!vfoIsCommandInDragMode() warn(cadr(value)))
	else
	   valueNum = value
	)
	vfoSetParam(cdfgData "vertSegActLen" valueNum)
    )
) ;cds_ff_mptFgrVertSegActLenCB

;Done proc to snap to snapping grid when CDF is modified
procedure(cds_ff_mptDoneProc(cellId)
    when(!vfoIsCommandInDragMode()
        vfoDoSnapToSnapPattern(cellId)
    )
)

;CDF callback for vertical min seg len
procedure(cds_ff_mptFgrVertMinSegLenCB(\@optional (cdfgData inSkill(cdfgData)))
    let((step newVal)
	step = vfoGetParam(cdfgData "verticalPitch")
	newVal = cds_ff_mptFgrCalcVertMinSegL(step)
	vfoSetParam(cdfgData "userMinVertSegLength" newVal)
	vfoSetParam(cdfgData "minVerticalSegLength" newVal)
    )
) ;cds_ff_mptFgrVertMinSegLenCB

;CDF callback for horizontal pitch
procedure(cds_ff_mptFgrHorizPitchCB(\@optional (cdfgData inSkill(cdfgData)))
    let((input)
	input = vfoGetParam(cdfgData "userHorizPitch")
	vfoSetParam(cdfgData "userHorizPitch" input)
	input = cdfParseFloatString(input)
	vfoSetParam(cdfgData "horizontalPitch" input)
    )
) ;cds_ff_mptFgrHorizPitchCB

;CDF callback for horizontal segment width draw value
procedure(cds_ff_mptFgrHorizSegWidthCB(\@optional (cdfgData inSkill(cdfgData)))
    let((input hSegWidth hSegWidthVal fins)
	input = vfoGetParam(cdfgData "userHorizSegWidth")
	hSegWidth = cds_ff_mptFgrCalcHorizSegWidth(input)
	if(listp(hSegWidth) then
	   hSegWidthVal = car(hSegWidth)
	   when(!vfoIsCommandInDragMode() warn(cadr(hSegWidth)))
	else
	   hSegWidthVal = hSegWidth
	)
	vfoSetParam(cdfgData "userHorizSegWidth" hSegWidthVal)
	fins = cds_ff_mptFgrGetFins(hSegWidthVal)
	vfoSetParam(cdfgData "numFins" fins)
	hSegWidth = cds_ff_mptFgrCalcHorizSegWidthOff(hSegWidthVal)
	vfoSetParam(cdfgData "horizontalSegWidth" hSegWidth)
    )
) ;cds_ff_mptFgrHorizSegWidthCB

;CDF callback for vertical segment width draw value
procedure(cds_ff_mptFgrVertSegWidthCB(\@optional (cdfgData inSkill(cdfgData)))
    let((w vSegWidth fing step vSegWidthVal)
	step = vfoGetParam(cdfgData "userHorizPitch")
	step = cdfParseFloatString(step)
	w = vfoGetParam(cdfgData "userVertSegWidth")
	vSegWidth = cds_ff_mptFgrCalcVertSegWidth(w step)
	if(listp(vSegWidth) then
	   vSegWidthVal = car(vSegWidth)
	   when(!vfoIsCommandInDragMode() warn(cadr(vSegWidth)))
	else
	   vSegWidthVal = vSegWidth
	)
	vfoSetParam(cdfgData "userVertSegWidth" vSegWidthVal)
	fing = cds_ff_mptFgrGetFing(vSegWidthVal step)
	vfoSetParam(cdfgData "numFingers" fing)
	vSegWidth = cds_ff_mptFgrCalcVertSegWidthOff(vSegWidthVal)
	vfoSetParam(cdfgData "verticalSegWidth" vSegWidth)
    )
) ;cds_ff_mptFgrVertSegWidthCB

;create form callback
procedure(cds_ff_mptFgrUserCreateCB(@optional (cdfgData nil))
    let((value valueNum value2 value3 newArgList argList Dev step step2)
        unless(cdfgData 
     	    ;get extraArgument value
            argList = vfoGRGetExtraArgument()
            ; making a new list
            Dev = vfoGRGetCreateFormFieldProp("Device" "value")
            foreach(ele argList
	        cond(
		     (car(ele) == "topMetal"
		         value = cds_ff_mptFgrGetCreateFormUserFieldProp("Top Metal" "value")
                         newArgList = append1(newArgList list("topMetal" value))
			 value = sprintf(nil "%L" value)
			 cds_ff_mptFgrSetCreateFormUserFieldProp("Top Metal" "value" value)
		     )
		     (car(ele) == "userHorizPitch"
		         value = cds_ff_mptFgrGetCreateFormUserFieldProp("Vert Seg Width" "value")
		         step = cds_ff_mptFgrGetCreateFormUserFieldProp("Poly Pitch" "value")
			 step2 = cdfParseFloatString(step)
			 value = cds_ff_mptFgrCalcVertSegWidth(value step2)
			 if(listp(value) then
			    valueNum = car(value)
			    warn(cadr(value))
			 else
			    valueNum = value
			 )
			 value2 = cds_ff_mptFgrCalcVertSegWidthOff(valueNum)
			 value3 = cds_ff_mptFgrGetFing(valueNum step2)
                         newArgList = append1(newArgList list("userHorizPitch" step))
			 step = sprintf(nil "%L" step)
			 cds_ff_mptFgrSetCreateFormUserFieldProp("Poly Pitch" "value" step)
			 step2 = sprintf(nil "%L" step2)
			 vfoGRSetCreateFormFieldProp("Horizontal Pitch" "value" step2)
			 valueNum = sprintf(nil "%L" valueNum)
			 cds_ff_mptFgrSetCreateFormUserFieldProp("Vert Seg Width" "value" valueNum)
			 value2 = sprintf(nil "%L" value2)
			 vfoGRSetCreateFormFieldProp("Vertical Segment Width" "value" value2)
			 value3 = sprintf(nil "%L" value3)
                         cds_ff_mptFgrSetCreateFormUserFieldProp("Fingers" "value" value3)
		     )
		     (car(ele) == "userVertSegWidth"
		         value = cds_ff_mptFgrGetCreateFormUserFieldProp("Vert Seg Width" "value")
		         step = cdfParseFloatString(cds_ff_mptFgrGetCreateFormUserFieldProp("Poly Pitch" "value"))
			 value = cds_ff_mptFgrCalcVertSegWidth(value step)
			 if(listp(value) then
			    valueNum = car(value)
			    warn(cadr(value))
			 else
			    valueNum = value
			 )
			 value2 = cds_ff_mptFgrCalcVertSegWidthOff(valueNum)
			 value3 = cds_ff_mptFgrGetFing(valueNum step)
                         newArgList = append1(newArgList list("userVertSegWidth" valueNum))
			 valueNum = sprintf(nil "%L" valueNum)
			 cds_ff_mptFgrSetCreateFormUserFieldProp("Vert Seg Width" "value" valueNum)
			 value2 = sprintf(nil "%L" value2)
			 vfoGRSetCreateFormFieldProp("Vertical Segment Width" "value" value2)
			 value3 = sprintf(nil "%L" value3)
                         cds_ff_mptFgrSetCreateFormUserFieldProp("Fingers" "value" value3)
		     )
		     (car(ele) == "userVertEnclose"
		         value = cds_ff_mptFgrGetCreateFormUserFieldProp("Y Direction Enclose" "value")
			 value2 = cds_ff_mptFgrGetCreateFormUserFieldProp("Y Direction Ref" "value")
			 value2 = car(parseString(value2 "_"))
			 value3 = cds_ff_mptFgrGetCreateFormUserFieldProp("Horiz Seg Width" "value")
			 value3 = cds_ff_mptFgrGetVertEnclose(value value3 value2)
                         newArgList = append1(newArgList list("userVertEnclose" value))
			 value = sprintf(nil "%L" value)
			 value3 = sprintf(nil "%L" value3)
			 cds_ff_mptFgrSetCreateFormUserFieldProp("Y Direction Enclose" "value" value)
			 vfoGRSetCreateFormFieldProp("Vertical Enclose By" "value" value3)
		     )
		     (car(ele) == "userVertHalfGapW"
		         value = cds_ff_mptFgrGetCreateFormUserFieldProp("Vert Seg Width" "value")
			 value2 = if(Dev == "PGR" "Psvt" "Nsvt")
			 value = cds_ff_mptFgrCalcVertHalfW(value2 value)
                         newArgList = append1(newArgList list("userVertHalfGapW" value))
			 value = sprintf(nil "%L" value)
			 cds_ff_mptFgrSetCreateFormUserFieldProp("X Direction Half Gap W" "value" value)
			 vfoGRSetCreateFormFieldProp("Horizontal Half Gap Width" "value" value)
		     )
		     (car(ele) == "userVertRefLPP"
		         value = cds_ff_mptFgrGetCreateFormUserFieldProp("Y Direction Ref" "value")
                         newArgList = append1(newArgList list("userVertRefLPP" value))
			 value = sprintf(nil "%L" buildString(parseString(value "_")))
			 vfoGRSetCreateFormFieldProp("Vertical Ref. Lpp" "value" value)
		     )
		     (car(ele) == "userHorizSegWidth"
		         value = cds_ff_mptFgrGetCreateFormUserFieldProp("Horiz Seg Width" "value")
			 value = cds_ff_mptFgrCalcHorizSegWidth(value)
			 if(listp(value) then
			    valueNum = car(value)
			    warn(cadr(value))
			 else
			    valueNum = value
			 )
			 value2 = cds_ff_mptFgrCalcHorizSegWidthOff(valueNum)
			 value3 = cds_ff_mptFgrGetFins(valueNum)
                         newArgList = append1(newArgList list("userHorizSegWidth" valueNum))
			 valueNum = sprintf(nil "%L" valueNum)
			 cds_ff_mptFgrSetCreateFormUserFieldProp("Horiz Seg Width" "value" valueNum)
			 value2 = sprintf(nil "%L" value2)
			 vfoGRSetCreateFormFieldProp("Horizontal Segment Width" "value" value2)
			 value3 = sprintf(nil "%L" value3)
                         cds_ff_mptFgrSetCreateFormUserFieldProp("Fins" "value" value3)
		     )
		     (car(ele) == "userHorizEnclose"
		         value = cds_ff_mptFgrGetCreateFormUserFieldProp("X Direction Enclose" "value")
			 value2 = cds_ff_mptFgrGetCreateFormUserFieldProp("X Direction Ref" "value")
			 value2 = car(parseString(value2 "_"))
			 value3 = cds_ff_mptFgrGetCreateFormUserFieldProp("Vert Seg Width" "value")
			 value3 = cds_ff_mptFgrGetHorizEnclose(value value3 value2)
                         newArgList = append1(newArgList list("userHorizEnclose" value))
			 value = sprintf(nil "%L" value)
			 value3 = sprintf(nil "%L" value3)
			 cds_ff_mptFgrSetCreateFormUserFieldProp("X Direction Enclose" "value" value)
			 vfoGRSetCreateFormFieldProp("Horizontal Enclose By" "value" value3)
		     )
		     (car(ele) == "userHorizHalfGapW"
		         value = cds_ff_mptFgrGetCreateFormUserFieldProp("Horiz Seg Width" "value")
			 value2 = if(Dev == "PGR" "Psvt" "Nsvt")
			 value = cds_ff_mptFgrCalcHorizHalfW(value2 value)
                         newArgList = append1(newArgList list("userHorizHalfGapW" value))
			 value = sprintf(nil "%L" value)
			 cds_ff_mptFgrSetCreateFormUserFieldProp("Y Direction Half Gap W" "value" value)
			 vfoGRSetCreateFormFieldProp("Vertical Half Gap Width" "value" value)
		     )
		     (car(ele) == "userHorizRefLPP"
		         value = cds_ff_mptFgrGetCreateFormUserFieldProp("X Direction Ref" "value")
                         newArgList = append1(newArgList list("userHorizRefLPP" value))
			 value = sprintf(nil "%L" buildString(parseString(value "_")))
			 vfoGRSetCreateFormFieldProp("Horizontal Ref. Lpp" "value" value)
		     )
		     (car(ele) == "numFingers"
		         value = cds_ff_mptFgrGetCreateFormUserFieldProp("Fingers" "value")
			 newArgList = append1(newArgList list("numFingers" value))
		     )
		     (car(ele) == "numFins"
		         value = cds_ff_mptFgrGetCreateFormUserFieldProp("Fins" "value")
			 newArgList = append1(newArgList list("numFins" value))
		     )
	             (car(ele) == "userMinVertSegLength"
      			 value = vfoGRGetCreateFormFieldProp("Vertical Pitch" "value")
 		         value = cds_ff_mptFgrCalcVertMinSegL(value)
 			 newArgList = append1(newArgList list("userMinVertSegLength" value))
 			 value = sprintf(nil "%L" value)
 			 cds_ff_mptFgrSetCreateFormUserFieldProp("Vertical Min Seg Len" "value" value)
 			 vfoGRSetCreateFormFieldProp("Min Vertical Seg Length" "value" value)
 		     )
	             (car(ele) == "vertSegActLen"
      			 value = cds_ff_mptFgrGetCreateFormUserFieldProp("Vertical Seg Active Fins" "value")
 		         value = cds_ff_mptFgrGetVertSegActL(value)
			 if(listp(value) then
			    valueNum = car(value)
			    warn(cadr(value))
			 else
			    valueNum = value
			 )
 			 newArgList = append1(newArgList list("vertSegActLen" valueNum))
 			 valueNum = sprintf(nil "%L" valueNum)
 			 cds_ff_mptFgrSetCreateFormUserFieldProp("Vertical Seg Active Fins" "value" valueNum)
 		     )
     		     (car(ele) == "userMinHorizSegLength"
     			 value = vfoGRGetCreateFormFieldProp("Horizontal Pitch" "value")
 		         value = cds_ff_mptFgrCalcHorizMinSegL(value)
 			 newArgList = append1(newArgList list("userMinHorizSegLength" value))
 			 value = sprintf(nil "%L" value)
 			 cds_ff_mptFgrSetCreateFormUserFieldProp("Horizontal Min Seg Len" "value" value)
 			 vfoGRSetCreateFormFieldProp("Min Horizontal Seg Length" "value" value)
 		     )
		     (t
                         newArgList = append1(newArgList ele)
		     )
                )
            )
            ;update/ set extra argument value
            vfoGRSetExtraArgument(newArgList)
        )
    );let
) ;cds_ff_mptFgrUserCreateCB

;turn off convert to polygon due to unsupported
defmethod(vfoSupportsConvertToPolygon? ((obj vfoAdvSfImplClass) instId) nil)

;tunnel form options
;Path, Rectangle, Polygon, Overlapping Shape
procedure(vfoGRUpdateTunnelOptions()
    prog(()
        return(list("Rectangle"
                    "Overlapping Shape")
	)
    )
) ;vfoGRUpdateTunnelOptions

;tunnel form layers
procedure(vfoGRUpdateTunnelLPPs()
    prog(()
        return(list(list("LiAct" "drawing")
                    list("V0" "drawing")
                    list("M1" "drawing")
                    list("V1" "drawing")
                    list("M2" "drawing")
                    list("V2" "drawing")
                    list("M3" "drawing")
                   )
        )
    )
) ;vfoGRUpdateTunnelLPPs

defmethod(vfoSfInitialize ((gr cds_ff_mptFgrGuardRing_ver_1));version control
    cds_ff_mptFgrUpdateRuleValue(gr);sync rule table
    callNextMethod()
) ;vfoSfInitialize

;environment settings for FGR
envSetVal( "layout" "keepGuardRingEndsConnected" 'boolean t )
envSetVal( "layout" "fgrEnableAdvanceWrap" 'boolean t )
envSetVal( "layout" "fgrPostEditPitchCorrection" 'boolean t )
;envSetVal( "layout" "vfoShowOnlyFluidShapeForDrag" 'boolean t )

;test if a closed ring
procedure(cds_ff_mptFgrClosedRing(oriList)
    let((pt1 pt2 closed)
        pt1 = car(oriList)
	pt2 = car(last(oriList))
        if(xCoord(pt1) == xCoord(pt2) && yCoord(pt1) == yCoord(pt2) then
            closed = t
        else
            closed = nil
        )
        closed
    )
) ;cds_ff_mptFgrClosedRing
