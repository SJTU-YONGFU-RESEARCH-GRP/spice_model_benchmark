/*************************************************************************
* DISCLAIMER: The following code is provided for Cadence customers       *
* to use at their own risk. The code may require modification to         *
* satisfy the requirements of any user. The code and any modifications   *
* to the code may not be compatible with current or future versions of   *
* Cadence products. THE CODE IS PROVIDED "AS IS" AND WITH NO WARRANTIES, *
* INCLUDING WITHOUT LIMITATION ANY EXPRESS WARRANTIES OR IMPLIED         *
* WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR USE.         *
*************************************************************************/

;; This procedure name is required for use with the VALE Framework Utilities
;; Load Custom WSPs and Clear Custom WSPs

procedure(WSPdefinitions()
    let((cv)
        cv = geGetWindowCellView()

        ;; M1 1x Track Patterns
        dbCreateWidthSpacingPattern(
            cv
            "M1_WSP_AABA_1"
            list(
                list(list(list(0.032 0.064 "" "mask1Color")) 1 )
                list(list(list(0.032 0.058 "" "mask1Color")) 1 )
                list(list(list(0.052 0.058 "" "mask2Color")) 1 )
                list(list(list(0.032 0.064 "" "mask1Color")) 1 )
            )
        )

        dbCreateWidthSpacingSnapPatternDef(
            cv
            "M1_TESTPAT"
            list("M1" "track")
            "horizontal"
            0.244
            "M1_WSP_AABA_1"
            list(list("M1"))
            0.0
            list("M1_WSP_AABA_1")
        )
		       
    )
)              
