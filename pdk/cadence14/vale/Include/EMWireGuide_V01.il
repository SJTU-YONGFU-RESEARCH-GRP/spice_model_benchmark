list(
   ;; Flow Parameters
   list(nil 'name "title" 'value "M1 Idc width")
   list(nil 'name "feedback" 'value t)
   list(nil 'name "layer" 'value "M1")
   list(nil 'name "outputColumn" 'value "1")
   ;; Input Declarations
   ;; NOTE: "inputs" must be defined before any conditions that use them.
   ;; Anything used in a variable definition below must be declared 
   ;; in "inputs".  A variable definition itself is a declaration of
   ;; that variable and does not need to be placed in "inputs"
   list(nil 'name "inputs"
            'value list("current" "wideWireX" "shortLenX" "temp"))
   ;; Equation Definition
   list(nil 'name "equation"
            'value "(((current/0.001)/(tempFactor * lengthFactor * widthFactor)+const2)/const1)"
   )
   ;; Equation Variable Definitions
   list(nil 'name "const1" 'value 1.72)
   list(nil 'name "const2" 'value 0.00504)
   list(nil 'name "lengthFactor" 'result 1.0 
            'conditions list("and" list(nil 'name "shortLenX" 'op "==" 'value nil)))
   list(nil 'name "lengthFactor" 'result 1.8
            'conditions list("and" list(nil 'name "shortLenX" 'op "==" 'value t)))
   list(nil 'name "widthFactor" 'result 1.0
            'conditions list("and" list(nil 'name "wideWireX" 'op "==" 'value nil)))
   list(nil 'name "widthFactor" 'result 1.4
            'conditions list("and" list(nil 'name "wideWireX" 'op "==" 'value t)))
   list(nil 'name "tempFactor" 'result 1.5  
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 100)))
   list(nil 'name "tempFactor" 'result 1.25
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 105)))
   list(nil 'name "tempFactor" 'result 1.0 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 110)))
   list(nil 'name "tempFactor" 'result 0.75 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 115)))
   list(nil 'name "tempFactor" 'result 0.50 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 120)))
   list(nil 'name "tempFactor" 'result 0.4  
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 125)))
   list(nil 'name "tempFactor" 'result 0.3 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 130)))
   list(nil 'name "tempFactor" 'result 0.2 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 140)))
   list(nil 'name "tempFactor" 'result 0.1 
            'conditions list("and" list(nil 'name "temp" 'op ">" 'value 140)))
)
list(
   ;; Flow Parameters
   list(nil 'name "title" 'value "V1 Idc count")
   list(nil 'name "layer" 'value "V1")
   ;; Input Declarations
   list(nil 'name "inputs"
            'value list("current" "viaType" "temp"))
   ;; Equation Definition
   list(nil 'name "equation"
            'value "int(((current/0.001)/(const1*viaTypeFactor*tempFactor)) + 1)")
   ;; Equation Variable Definitions
   list(nil 'name "const1" 'value 0.0501)
   list(nil 'name "viaTypeFactor" 'result 1
            'conditions list("and" list(nil 'name "viaType" 'op "==" 'value "square")))
   list(nil 'name "viaTypeFactor" 'result 2
            'conditions list("and" list(nil 'name "viaType" 'op "==" 'value "bar")))
   list(nil 'name "viaTypeFactor" 'result 3
            'conditions list("and" list(nil 'name "viaType" 'op "==" 'value "large")))
   list(nil 'name "tempFactor" 'result 1.5 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 100)))
   list(nil 'name "tempFactor" 'result 1.25
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 105)))
   list(nil 'name "tempFactor" 'result 1.0
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 110)))
   list(nil 'name "tempFactor" 'result 0.75
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 115)))
   list(nil 'name "tempFactor" 'result 0.50
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 120)))
   list(nil 'name "tempFactor" 'result 0.4 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 125)))
   list(nil 'name "tempFactor" 'result 0.3
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 130)))
   list(nil 'name "tempFactor" 'result 0.2
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 140)))
   list(nil 'name "tempFactor" 'result 0.1
            'conditions list("and" list(nil 'name "temp" 'op ">" 'value 140)))
)
list(
   ;; Flow Parameters
   list(nil 'name "title" 'value "M1 Irms limit")
   list(nil 'name "layer" 'value "M1")
   list(nil 'name "outputColumn" 'value "2")
   ;; Input Declarations
   list(nil 'name "inputs"
            'value list("M1_Idc_width" "numLinesX" "temp"))
   ;; Equation Definition
   list(nil 'name "equation"
            'value "(((const1*M1_Idc_width/0.001)-const2)*tempFactor*const3*limDeltaT)/numx") 
   ;; Equation Variable Definitions
   list(nil 'name "const1" 'value 1.72)
   list(nil 'name "const2" 'value 0.00504)
   list(nil 'name "const3" 'value 0.707)
   list(nil 'name "limDeltaT" 'value 5)
   list(nil 'name "numx" 'result 4.1 'conditions list("and" list(nil 'name "numLinesX" 'op "==" 'value t)))
   list(nil 'name "numx" 'result 1.0 'conditions list("and" list(nil 'name "numLinesX" 'op "==" 'value nil)))
   list(nil 'name "tempFactor" 'result 1.5
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 100)))
   list(nil 'name "tempFactor" 'result 1.25
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 105)))
   list(nil 'name "tempFactor" 'result 1.0
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 110)))
   list(nil 'name "tempFactor" 'result 0.75
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 115)))
   list(nil 'name "tempFactor" 'result 0.50
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 120)))
   list(nil 'name "tempFactor" 'result 0.4
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 125)))
   list(nil 'name "tempFactor" 'result 0.3
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 130)))
   list(nil 'name "tempFactor" 'result 0.2
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 140)))
   list(nil 'name "tempFactor" 'result 0.1
            'conditions list("and" list(nil 'name "temp" 'op ">" 'value 140)))
)
list(
   ;; Flow Parameters
   list(nil 'name "title" 'value "M2 Idc width")
   list(nil 'name "feedback" 'value t)
   list(nil 'name "layer" 'value "M2")
   list(nil 'name "outputColumn" 'value "1")
   ;; Input Declarations
   list(nil 'name "inputs"
            'value list("current" "wideWireX" "shortLenX" "temp"))
   ;; Equation Definition
   list(nil 'name "equation"
            'value "(((current/0.001)/(tempFactor * lengthFactor * widthFactor)+const2)/const1)"
   )
   ;; Equation Variable Definitions
   list(nil 'name "const1" 'value 2.24)
   list(nil 'name "const2" 'value 0.00068)
   list(nil 'name "lengthFactor" 'result 1.0 
            'conditions list("and" list(nil 'name "shortLenX" 'op "==" 'value nil)))
   list(nil 'name "lengthFactor" 'result 1.8
            'conditions list("and" list(nil 'name "shortLenX" 'op "==" 'value t)))
   list(nil 'name "widthFactor" 'result 1.0
            'conditions list("and" list(nil 'name "wideWireX" 'op "==" 'value nil)))
   list(nil 'name "widthFactor" 'result 1.4
            'conditions list("and" list(nil 'name "wideWireX" 'op "==" 'value t)))
   list(nil 'name "tempFactor" 'result 1.5  
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 100)))
   list(nil 'name "tempFactor" 'result 1.25
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 105)))
   list(nil 'name "tempFactor" 'result 1.0 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 110)))
   list(nil 'name "tempFactor" 'result 0.75 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 115)))
   list(nil 'name "tempFactor" 'result 0.50 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 120)))
   list(nil 'name "tempFactor" 'result 0.4  
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 125)))
   list(nil 'name "tempFactor" 'result 0.3 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 130)))
   list(nil 'name "tempFactor" 'result 0.2 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 140)))
   list(nil 'name "tempFactor" 'result 0.1 
            'conditions list("and" list(nil 'name "temp" 'op ">" 'value 140)))
)
list(
   ;; Flow Parameters
   list(nil 'name "title" 'value "V2 Idc count")
   list(nil 'name "layer" 'value "V2")
   ;; Input Declarations
   list(nil 'name "inputs"
            'value list("current" "viaType" "temp"))
   ;; Equation Definition
   list(nil 'name "equation"
            'value "int(((current/0.001)/(const1*viaTypeFactor*tempFactor)) + 1)")
   ;; Equation Variable Definitions
   list(nil 'name "const1" 'value 0.0711)
   list(nil 'name "viaTypeFactor" 'result 1
            'conditions list("and" list(nil 'name "viaType" 'op "==" 'value "square")))
   list(nil 'name "viaTypeFactor" 'result 2
            'conditions list("and" list(nil 'name "viaType" 'op "==" 'value "bar")))
   list(nil 'name "viaTypeFactor" 'result 3
            'conditions list("and" list(nil 'name "viaType" 'op "==" 'value "large")))
   list(nil 'name "tempFactor" 'result 1.5 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 100)))
   list(nil 'name "tempFactor" 'result 1.25
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 105)))
   list(nil 'name "tempFactor" 'result 1.0
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 110)))
   list(nil 'name "tempFactor" 'result 0.75
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 115)))
   list(nil 'name "tempFactor" 'result 0.50
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 120)))
   list(nil 'name "tempFactor" 'result 0.4 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 125)))
   list(nil 'name "tempFactor" 'result 0.3
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 130)))
   list(nil 'name "tempFactor" 'result 0.2
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 140)))
   list(nil 'name "tempFactor" 'result 0.1
            'conditions list("and" list(nil 'name "temp" 'op ">" 'value 140)))
)
list(
   ;; Flow Parameters
   list(nil 'name "title" 'value "M2 Irms limit")
   list(nil 'name "layer" 'value "M2")
   list(nil 'name "outputColumn" 'value "2")
   ;; Input Declarations
   list(nil 'name "inputs"
            'value list("M2_Idc_width" "numLinesX" "temp"))
   ;; Equation Definition
   list(nil 'name "equation"
            'value "(((const1*M1_Idc_width/0.001)-const2)*tempFactor*const3*limDeltaT)/numx") 
   ;; Equation Variable Definitions
   list(nil 'name "const1" 'value 2.24)
   list(nil 'name "const2" 'value 0.00068)
   list(nil 'name "const3" 'value 0.707)
   list(nil 'name "limDeltaT" 'value 5)
   list(nil 'name "numx" 'result 4.1 'conditions list("and" list(nil 'name "numLinesX" 'op "==" 'value t)))
   list(nil 'name "numx" 'result 1.0 'conditions list("and" list(nil 'name "numLinesX" 'op "==" 'value nil)))
   list(nil 'name "tempFactor" 'result 1.5
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 100)))
   list(nil 'name "tempFactor" 'result 1.25
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 105)))
   list(nil 'name "tempFactor" 'result 1.0
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 110)))
   list(nil 'name "tempFactor" 'result 0.75
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 115)))
   list(nil 'name "tempFactor" 'result 0.50
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 120)))
   list(nil 'name "tempFactor" 'result 0.4
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 125)))
   list(nil 'name "tempFactor" 'result 0.3
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 130)))
   list(nil 'name "tempFactor" 'result 0.2
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 140)))
   list(nil 'name "tempFactor" 'result 0.1
            'conditions list("and" list(nil 'name "temp" 'op ">" 'value 140)))
)
list(
   ;; Flow Parameters
   list(nil 'name "title" 'value "M3 Idc width")
   list(nil 'name "feedback" 'value t)
   list(nil 'name "layer" 'value "M3")
   list(nil 'name "outputColumn" 'value "1")
   ;; Input Declarations
   list(nil 'name "inputs"
            'value list("current" "wideWireX" "shortLenX" "temp"))
   ;; Equation Definition
   list(nil 'name "equation"
            'value "(((current/0.001)/(tempFactor * lengthFactor * widthFactor)+const2)/const1)"
   )
   ;; Equation Variable Definitions
   list(nil 'name "const1" 'value 2.18)
   list(nil 'name "const2" 'value 0.00076)
   list(nil 'name "lengthFactor" 'result 1.0 
            'conditions list("and" list(nil 'name "shortLenX" 'op "==" 'value nil)))
   list(nil 'name "lengthFactor" 'result 1.8
            'conditions list("and" list(nil 'name "shortLenX" 'op "==" 'value t)))
   list(nil 'name "widthFactor" 'result 1.0
            'conditions list("and" list(nil 'name "wideWireX" 'op "==" 'value nil)))
   list(nil 'name "widthFactor" 'result 1.4
            'conditions list("and" list(nil 'name "wideWireX" 'op "==" 'value t)))
   list(nil 'name "tempFactor" 'result 1.5  
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 100)))
   list(nil 'name "tempFactor" 'result 1.25
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 105)))
   list(nil 'name "tempFactor" 'result 1.0 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 110)))
   list(nil 'name "tempFactor" 'result 0.75 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 115)))
   list(nil 'name "tempFactor" 'result 0.50 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 120)))
   list(nil 'name "tempFactor" 'result 0.4  
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 125)))
   list(nil 'name "tempFactor" 'result 0.3 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 130)))
   list(nil 'name "tempFactor" 'result 0.2 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 140)))
   list(nil 'name "tempFactor" 'result 0.1 
            'conditions list("and" list(nil 'name "temp" 'op ">" 'value 140)))
)
list(
   ;; Flow Parameters
   list(nil 'name "title" 'value "V3 Idc count")
   list(nil 'name "layer" 'value "V3")
   ;; Input Declarations
   list(nil 'name "inputs"
            'value list("current" "viaType" "temp"))
   ;; Equation Definition
   list(nil 'name "equation"
            'value "int(((current/0.001)/(const1*viaTypeFactor*tempFactor)) + 1)")
   ;; Equation Variable Definitions
   list(nil 'name "const1" 'value 0.0691)
   list(nil 'name "viaTypeFactor" 'result 1
            'conditions list("and" list(nil 'name "viaType" 'op "==" 'value "square")))
   list(nil 'name "viaTypeFactor" 'result 2
            'conditions list("and" list(nil 'name "viaType" 'op "==" 'value "bar")))
   list(nil 'name "viaTypeFactor" 'result 3
            'conditions list("and" list(nil 'name "viaType" 'op "==" 'value "large")))
   list(nil 'name "tempFactor" 'result 1.5 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 100)))
   list(nil 'name "tempFactor" 'result 1.25
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 105)))
   list(nil 'name "tempFactor" 'result 1.0
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 110)))
   list(nil 'name "tempFactor" 'result 0.75
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 115)))
   list(nil 'name "tempFactor" 'result 0.50
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 120)))
   list(nil 'name "tempFactor" 'result 0.4 
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 125)))
   list(nil 'name "tempFactor" 'result 0.3
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 130)))
   list(nil 'name "tempFactor" 'result 0.2
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 140)))
   list(nil 'name "tempFactor" 'result 0.1
            'conditions list("and" list(nil 'name "temp" 'op ">" 'value 140)))
)
list(
   ;; Flow Parameters
   list(nil 'name "title" 'value "M3 Irms limit")
   list(nil 'name "layer" 'value "M3")
   list(nil 'name "outputColumn" 'value "2")
   ;; Input Declarations
   list(nil 'name "inputs"
            'value list("M2_Idc_width" "numLinesX" "temp"))
   ;; Equation Definition
   list(nil 'name "equation"
            'value "(((const1*M1_Idc_width/0.001)-const2)*tempFactor*const3*limDeltaT)/numx") 
   ;; Equation Variable Definitions
   list(nil 'name "const1" 'value 2.18)
   list(nil 'name "const2" 'value 0.00076)
   list(nil 'name "const3" 'value 0.707)
   list(nil 'name "limDeltaT" 'value 5)
   list(nil 'name "numx" 'result 4.1 'conditions list("and" list(nil 'name "numLinesX" 'op "==" 'value t)))
   list(nil 'name "numx" 'result 1.0 'conditions list("and" list(nil 'name "numLinesX" 'op "==" 'value nil)))
   list(nil 'name "tempFactor" 'result 1.5
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 100)))
   list(nil 'name "tempFactor" 'result 1.25
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 105)))
   list(nil 'name "tempFactor" 'result 1.0
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 110)))
   list(nil 'name "tempFactor" 'result 0.75
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 115)))
   list(nil 'name "tempFactor" 'result 0.50
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 120)))
   list(nil 'name "tempFactor" 'result 0.4
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 125)))
   list(nil 'name "tempFactor" 'result 0.3
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 130)))
   list(nil 'name "tempFactor" 'result 0.2
            'conditions list("and" list(nil 'name "temp" 'op "<=" 'value 140)))
   list(nil 'name "tempFactor" 'result 0.1
            'conditions list("and" list(nil 'name "temp" 'op ">" 'value 140)))
)
