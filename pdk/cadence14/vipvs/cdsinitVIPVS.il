
let((gpdkInstallDir)
   gpdkInstallDir = getShellEnvVar("GPDK_INSTALL_DIR")
   if(gpdkInstallDir then
      ;; PVS_SNAP_SHOTS_DIRS is where to load the default set of snapshots
      setShellEnvVar("PVS_SNAP_SHOTS_DIRS"
         strcat(gpdkInstallDir "/vipvs/Snapshots"))

      ;; Set the default Snapshot
      setShellEnvVar("Virtuoso_IPVS_initSnapshot" "DRC_GPDK_v1p0")
      
      ;; drdPVSErrorDisplayMaster enables hierarchical list of the output 
      ;; markers (instead of a flat list)
      envSetVal("layout" "drdPVSErrorDisplayMaster" 'boolean nil)
      
      ;; drdBatchVioLimit limits the number of VIPVS markers reported
      envSetVal("layout" "drdBatchVioLimit" 'int 5000000)
      
      ;; drdVioLimitPerRule limits the number of VIPVS markers reported for 
      ;; each rule
      envSetVal("layout" "drdVioLimitPerRule" 'int 500000)
      
      ;; Where to return the VIVPS results
      setShellEnvVar("Virtuoso_IPVS_markerBrowser" "AnnotationBrowser")
      
      ;; Only show the Verify Design button and not the Post Edit button
      ;setShellEnvVar("Virtuoso_IPVS_onlyVD" "YES")
      
      ;; Change the number of cores used (default is 4)
      ;setShellEnvVar("Virtuoso_IPVS_numProcs" "1")
      
      ;; Override the default location of the temporary files
      ;setShellEnvVar("Virtuoso_IPVS_dir" "/dev/shm/jfales")
      
   else
      printf("INFO: Environment variable GPDK_INSTALL_DIR is not set. ")
      printf("VIPVS is not enabled.\n")
   )
)
