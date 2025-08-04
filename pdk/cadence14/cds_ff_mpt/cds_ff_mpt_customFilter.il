(define cds_ff_mpt_CustomFilter(inst simulator)
  (setq cellName inst->cellName)
  (setq paramList list())

  rexCompile("^[p1|p2|n1|n2]*vt")
  (if (rexExecute cellName) then
    (setq paramList (list (list "numFins" (get inst "nfin")) (list "l" (get inst "l")) (list "numFingers" (get inst "nf")) (list "m" (get inst "m"))))
    )

  (rexCompile "^r")
  (if (rexExecute cellName) then
    (setq paramList (list (list "segments" (get inst "segments")) (list "connection" (get inst "connection")) (list "calculatedParam" (get inst "calculatedParam")) ))
    calcParam = (get inst "calculatedParam")
    case(calcParam
         ("Resistance" 
              returnList = (list (list "w" (get inst "w")) (list "l" (get inst "l")))
         )
         ("Length"
              returnList = (list (list "w" (get inst "w")) (list "r" (get inst "r")))
         )
        ) 
     (setq paramList (append paramList returnList))
  )

  (rexCompile "^cmim")
  (if (rexExecute cellName) then
    (setq paramList (list (list "calculatedParam" (get inst "calculatedParam")) (list "m" (get inst "m"))))
    calcParam = (get inst "calculatedParam")
    case(calcParam
        ("capacitance"
            returnList = (list (list "w" (get inst "w")) (list "l" (get inst "l")))
        ) 
        ("width"
            returnList = (list (list "c" (get inst "c")) (list "l" (get inst "l"))) 
        )
        ("length"
            returnList = (list (list "c" (get inst "c")) (list "w" (get inst "w")))
        )
    )
    (setq paramList (append paramList returnList))
  )

  (rexCompile "^[pd|nd]*vt")
  (if (rexExecute cellName) then
    (setq paramList (list (list "numFins" (get inst "nfin")) (list "polypitch" (get inst "polypitch")) (list "numFingers" (get inst "nf")) (list "m" (get inst "m"))))
  )

  (rexCompile "npn")
  (if (rexExecute cellName) then
    (setq paramList (list (list "emitterSize" (get inst "emitterSize")) (list "m" (get inst "m"))))
  )

  paramList    
  )

when(fboundp('axlRegisterCustomDeviceFilter)
axlRegisterCustomDeviceFilter("Default" 'cds_ff_mpt_CustomFilter)
)

