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
        dbCreateWidthSpacingPatternWithColor(
            cv
            "M1_WSP_1X_1"
            list(
                list(list(list(0.032 0.086)) 1 )
            )
            "mask1Color"
            0.0
        )
        dbCreateWidthSpacingPatternWithColor(
            cv
            "M1_WSP_1X_2"
            list(
                list(list(list(0.032 0.086)) 1 )
            )
            "mask2Color"
            0.0
        )
        dbCreateWidthSpacingSnapPatternDef(
            cv
            "M1_1X"
            list("M1" "track")
            "horizontal"
            0.086
            "M1_WSP_1X_1"
            list(list("M1"))
            0.0
            list("M1_WSP_1X_1" "M1_WSP_1X_2")
        )

        ;; M2 1x Track Pattern
	dbCreateWidthSpacingPatternWithColor(
            cv
            "M2_WSP_1X_1"
            list(
                list(list(list(0.032 0.086)) 1 )
            )
            "mask1Color"
            0.0
        )
	dbCreateWidthSpacingPatternWithColor(
            cv
            "M2_WSP_1X_2"
            list(
                list(list(list(0.032 0.086)) 1 )
            )
            "mask2Color"
            0.0
        )
        dbCreateWidthSpacingSnapPatternDef(
            cv
            "M2_1X"
            list("M2" "track")
            "vertical"
            0.086
            "M2_WSP_1X_1"
            list(list("M2"))
            0.0
            list("M2_WSP_1X_1" "M2_WSP_1X_2")
	)
		       
        ;; M3 1x Track Pattern
	dbCreateWidthSpacingPatternWithColor(
            cv
            "M3_WSP_1X_1"
            list(
                list(list(list(0.032 0.086)) 1 )
            )
            "mask1Color"
            0.0
        )
	dbCreateWidthSpacingPatternWithColor(
            cv
            "M3_WSP_1X_2"
            list(
                list(list(list(0.032 0.086)) 1 )
            )
            "mask2Color"
            0.0
        )
        dbCreateWidthSpacingSnapPatternDef(
            cv
            "M3_1X"
            list("M3" "track")
            "horizontal"
            0.086
            "M3_WSP_1X_1"
            list(list("M3"))
            0.0
            list("M3_WSP_1X_1" "M3_WSP_1X_2")
	)
		       
    )
)              
