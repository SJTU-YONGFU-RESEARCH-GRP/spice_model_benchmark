;;****************** migratemap file supported by GUI ********************

;;***************************** Do NOT Edit ******************************


loLibraryMap["gpdk090"] = "gpdk045"
loLibraryMap["gsclib090"] = "gsclib045"
loParameterMap["mosmap"] = list(
        ;list(targetParam  function of source parameter)
        list("w" "cond( (stringp(w) cdfFormatFloatString(sprintf(nil \"%g\",round(cdfParseFloatString(w) * 1e6/0.005 * .6)*1e-6*0.005),\"n\")) (t round(w*1e6/0.005 * .6)*1e-6*0.005))")
)

loPcellMap = list(
        ;list(sourcePcell inst parent targetPcell parameterMap target-rotation post-callback)
        list("gpdk090/pmos1v/symbol" "*" "*" "gpdk045/pmos1v/symbol" "mosmap" "R0" "None")
        list("gpdk090/nmos1v/symbol" "*" "*" "gpdk045/nmos1v/symbol" "mosmap" "R0" "None")
)

;;**************** Post callback procedures *********************

;;**************** Parameter mapping procedures *********************

;;**************** Technology setup ****************************

;;***************************** Edit After This Line ****************************
