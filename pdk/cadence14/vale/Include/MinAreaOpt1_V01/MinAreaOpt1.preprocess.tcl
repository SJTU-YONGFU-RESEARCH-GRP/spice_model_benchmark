set outputdir [getConf outputDir]

set valeIncludeDir [file dirname [info script]]

# area-fixes
set cpaDeck "$valeIncludeDir/MinAreaOpt1.preproc.xml"
set cpaLayermap "$valeIncludeDir/MinAreaOpt1.cpa_map"
lpaPreProcessEclair "/lan/dfm/grp_ccdrd_work01/jnelson/tool/CPA_19.12.00_190916_EB/eclair-x86_64_RH6-CPA_19.12.00_190916_EB/bin/eclair interactCLI -L ${outputdir}/INPUT.gds -D ${cpaDeck} -l ${cpaLayermap} -o ${outputdir}/preproc,force=1 -m INTERMEDIATE.gds --overlay-top-cellname-from-layout"
