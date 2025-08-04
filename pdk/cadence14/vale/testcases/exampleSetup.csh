
## MVS
setenv MVSHOME <path to MVS>
setenv DFMHOME $MVSHOME

## PVS/Pegasus
setenv PVSHOME <path to Pegasus>

## Virtuoso
setenv CDSHOME <path to Virtuoso>

set path = ($path ${CDSHOME}/bin ${CDSHOME}/tools/bin ${CDSHOME}/tools/dfII/bin ${PVSHOME}/bin ${PVSHOME}/tools/bin ${MVSHOME}/bin ${MVSHOME}/tools/bin )

setenv LM_LICENSE_FILE <license server string>
