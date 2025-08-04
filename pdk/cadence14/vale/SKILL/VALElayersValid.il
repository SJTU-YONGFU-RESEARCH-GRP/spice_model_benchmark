procedure(VALElayersValid()
   let((vll lppStr)
      when(_IMFdat->wspLayers && _IMFdat->wspPurposes
         foreach(wspLyr _IMFdat->wspLayers
            foreach(wspPurp _IMFdat->wspPurposes
               vll = cons(list(wspLyr wspPurp) vll)
            )
         )
      )
      when(_IMFdat->pRowLpp
         vll = cons(_IMFdat->pRowLpp vll)
      )
      when(_IMFdat->nRowLpp
         vll = cons(_IMFdat->nRowLpp vll)
      )
      when(_IMFdat->instRowLpp
         vll = cons(_IMFdat->instRowLpp vll)
      )
      when(_IMFdat->dummyRowLpp
         vll = cons(_IMFdat->dummyRowLpp vll)
      )
      when(_IMFdat->tapRowLpp
         vll = cons(_IMFdat->tapRowLpp vll)
      )
   
      pteShowRoutingLPP(nil)
      pteShowUsedLPP(nil)
      pteShowValidLPP(nil)
      foreach(lpp vll
         lppStr = buildString(lpp)
    
         ;; Make Layer Valid 
         pteSetValidity(lppStr t "Layers")
      
         ;; Make Layer Visible 
         pteSetVisible(lppStr t "Layers")
      
         ;; Make Layer Selectable 
         pteSetSelectable(lppStr t "Layers")
      )
      pteShowValidLPP(t)
   
   )
)

