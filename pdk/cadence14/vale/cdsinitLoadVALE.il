let((gpdkInstallDir valeInstallDir)
   gpdkInstallDir = getShellEnvVar("GPDK_INSTALL_DIR")
   valeInstallDir = getShellEnvVar("CDS_MVS_IMF_CM") 
   if(gpdkInstallDir then
      if(valeInstallDir then
         ;; Initialize VALE framwork
         IMFappStart()
      else
         valeInstallDir = strcat(gpdkInstallDir "/vale")
         setShellEnvVar("CDS_MVS_IMF_CM" valeInstallDir)
         ;; Initialize VALE framwork
         IMFappStart()
      )
   else
      if(valeInstallDir then
         ;; Initialize VALE framework
         IMFappStart()
      else 
         printf("INFO: Environment variable GPDK_INSTALL_DIR is not set. ")
         printf("Environment variable CDS_MVS_IMF_CM is not set. ")
         printf("VALE Framework is not enabled.\n") 
      )
   )
)
