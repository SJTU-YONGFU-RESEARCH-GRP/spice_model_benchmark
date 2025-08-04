
procedure(VALEshowDialog1(rtDpl buttonName message debug)
   prog((dboxName buttonSel)

      ;; Each line in message should be less than 80 characters with each new
      ;; line starting with 3 spaces.

      dboxName = strcat("VALE" rtDpl->symName "Msg")
      buttonSel = hiDisplayAppDBox(
         ?name stringToSymbol(dboxName)
         ?dboxBanner "VALE framework Component Module Information"
         ?dboxText message
         ?callback 'nil
         ?dialogType hicWorkingDialog
         ?dialogStyle 'modal
         ?buttonLayout 'UserDefined
         ?buttons list(buttonName "Cancel")
      )
      
      ;; Exit options 
      unless(buttonSel
         printf("VALE ERROR: A problem occurred with the %s dialog box.\n"
            dboxName)
         return()
      )
      if(buttonSel > 1 then
         return()
      )
      return(t)
   )
)
