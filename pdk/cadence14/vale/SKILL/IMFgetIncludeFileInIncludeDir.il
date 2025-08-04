/*
   Revision log:
   2018-07-25 JF Initial Coding for Change 180725a, part of the Component
                 Module coding efficiency improvements
   2018-07-27 JF Update to test ext for a ".".  If yes, then look for the
                 file in the CM directory, if not, use getShellEnvVar to 
                 find the include file

*/

unless(isCallable('_IMFgetIncludeFileInIncludeDir)
procedure(_IMFgetIncludeFileInIncludeDir(cv rtDpl ext @optional (debug nil))
   prog((erv file erv2)
      when(debug 
         printf("VALE DEBUG: Setting %s path. CM= %L\n" ext rtDpl->cm)
      )
      ;; Change 180727b
      if(rexMatchp("\\." ext) then
         erv = errset(strcat(rtDpl->cm "/Include/" rtDpl->name "_"
            rtDpl->version "/" rtDpl->name  ext))
      else
         erv = errset(getShellEnvVar(ext))
      )
      if(erv then
         ;; neither method threw an exception
         if(erv == list(nil) then
            ;; no env var set, or file path string not valid
            printf("VALE ERROR: Failed to set the ") 
            printf("%L %s file or directory\n" rtDpl->name ext)
            _IMFcmReturn(cv rtDpl "reset" debug)
            return()
         else
            ;; Env var set, or file path string set
            file = car(erv)

            ;; If it is a directory, return the value of the env var
            when(isDir(file)
               return(file)
            )

            ;; Otherwise, test the file path string
            ;; Change 180614a enabled a CM2 ruleset
            unless(isFile(file)
               ;; file path string points to an invalid file, try for CM2
               erv2 = errset(
                  strcat(rtDpl->cm2 "/Include/" rtDpl->name "_" rtDpl->version 
                     "/"  rtDpl->name ext) 
               )
               if(erv2 then
                  ;; could not set the secondary file path string
                  if(erv2 == list(nil) then
                     printf("VALE ERROR: Failed to set the path to the ")
                     printf("%L %s file.\n" rtDpl->name ext)
                     _IMFcmReturn(cv rtDpl "reset" debug) 
                     return()
                  else
                     ;; test the secondary file path string
                     file = car(erv2)
                     unless(isFile(file)
                        printf("VALE ERROR: Please check the path to the ")
                        printf("%s file %L\n" file ext)
                        _IMFcmReturn(cv rtDpl "reset" debug)
                        return()
                     )
                     ;; fall through to the final return
                  )
               else
                  printf("VALE ERROR: A problem occurred while setting the ")
                  printf("path for the %s file for %L\n" ext rtDpl->name)
                  printf("%L\n" errset.errset )
                  _IMFcmReturn(cv rtDpl "reset" debug) 
                  return()
               ) 
            )
         )
      else
         ;; rtDpl->cm is nil, or getShellEnvVar returned an error
         ;; check rtDpl->cm2 per Change 180727b
         if(rexMatchp("\\." ext) then
            erv2 = errset(strcat(rtDpl->cm2 "/Include/" rtDpl->name "_"
               rtDpl->version "/" rtDpl->name ext))
            if(erv2 then
               if(erv2 == list(nil) then
                  printf("VALE ERROR: Failed to set the path to the %L %s file.\n"
                     rtDpl->name ext)
                  _IMFcmReturn(cv rtDpl "reset" debug)
                  return()
               else
                  ;; When rtDpl->cm2 exists and rtDpl->cm does not
                  file = car(erv2)
                  unless(isFile(file)
                     printf("VALE ERROR: Please check the path to the ")
                     printf("%s file %L\n" file ext)
                     _IMFcmReturn(cv rtDpl "reset" debug)
                     return()
                  )
                  ;; fall through to the final return
               )
            else
               printf("VALE ERROR: A problem occurred while setting the path for ")
               printf("the %s file for %L\n%L\n" ext rtDpl->name errset.errset)
               _IMFcmReturn(cv rtDpl "reset" debug)
               return()
            ) 
         else
            printf("VALE ERROR: A problem occurred while setting the path for ")
            printf("%s for %L\n%L\n" ext rtDpl->name errset.errset)
            _IMFcmReturn(cv rtDpl "reset" debug)
            return()
         )
      )
      return(file)
   )
)

)
