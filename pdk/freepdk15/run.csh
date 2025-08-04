#!/bin/csh -f

setenv PDK_DIR `pwd`/calibre
setenv OUTPUT_DIR "./output"


setenv LAYOUT_PATH "./INV_X1.gds"

setenv LAYOUT_SYSTEM "GDS"

#cc_1 B A 45.3621f  v1
#cc_1 B A 45.249f v2
#c_2 B 0 7.42904f v1
#c_4 A 0 7.45066f v1
#c_2 B 0 7.42573f v2
#c_4 A 0 7.44803f v2
#c_2 B 0 10.3397f v2opc
#c_4 A 0 9.61365f v2opc
#cc_1 B A 48.5359f v2opc
# type 1
# type 2
# type 3
# type 4
# type 5
# type 6
# type 7
# type 8
# type 9
# type 10
# type 11
# type 12

setenv LAYOUT_PRIMARY "INV_X1"
#1.83976f
#1.6867f
#1.52499f 

#setenv LAYOUT_PATH "./reference_10u_opc.oas"
#cc_1 B A 43.624f
#c_2 B 0 7.4131f
#c_4 A 0 7.4131f
#cc_1 B A 46.4206f opc
#c_2 B 0 10.3549f opc
#c_4 A 0 9.83938f opc

#setenv LAYOUT_SYSTEM "GDSII"
#setenv LAYOUT_PATH "./output/opc.oas"
#setenv LAYOUT_SYSTEM "OASIS"
#setenv LAYOUT_PRIMARY "top"
#cc_1 B A 43.624f
#c_4 A 0 7.4131f
#c_2 B 0 7.4131f

#cc_1 B A 46.4206f
#c_2 B 0 10.3549f
#c_4 A 0 9.83938f

#setenv LAYOUT_PATH "./fractal_cap/test.gds"
#setenv LAYOUT_SYSTEM "GDSII"
#setenv LAYOUT_PRIMARY "topcell"
#c_2 A 0 0.120847f
#c_4 B 0 0.0813617f

#setenv LAYOUT_PATH "./design/reference_cap2.gds"
#setenv LAYOUT_SYSTEM "GDSII"
#setenv LAYOUT_PRIMARY "TOP"
#c_2 A 0 0.087456f
#c_4 B 0 0.118642f
#1.6867f
#2.13138f
#2.13138f

#setenv DRC_DATABASE "./output/drc.rdb"
#setenv DRC_REPORT "./output/drc.rpt"

setenv SOURCE_PATH "./design/cap.sp"
setenv SOURCE_SYSTEM "SPICE"
setenv SOURCE_PRIMARY "TOP"
setenv LVS_REPORT "./output/lvs.rpt"
setenv MASK_DATABASE "./output/svdb2"
setenv ERC_DATABASE "./output/erc.db"
setenv ERC_REPORT "./output/erc.rpt"

setenv PEX_NETLIST "./output/top.pex.sp";
setenv PEX_REPORT "./output/pex.rpt"

#setenv OPC_DATABASE "./output/opc.oas"
#setenv OPC_REPORT "./output/opc.rpt"

mkdir -p output

# Execute OPC
#calibre -drc -hier -turbo -turbo_all ./calibre/calibrenmOPC.tvf -E ./output/opc.svrf |& tee ./output/opc.log

# Execute DRC
#calibre -drc -hier -turbo -turbo_all ./calibre/calibreDRC.tvf -E ./output/drc.svrf |& tee ./output/drc.log
#exit
# Execute LVS
calibre -lvs -hier -turbo -turbo_all ./calibre/calibreLVS.tvf -E ./output/lvs.svrf |& tee ./output/lvs.log

# Execute XRC
# { [ [ -c || -r || -rc || -rcc || -l || -m || -lm || -rl || -rcl || -rccl || -rlm || -rclm || -rcclm || -all |
calibre -xrc -phdb -turbo ./calibre/calibrexRC.tvf -E ./output/xrc.svrf |& tee ./output/xrc.log1
calibre -xrc -pdb -c -turbo ./calibre/calibrexRC.tvf -E ./output/xrc.svrf |& tee ./output/xrc.log2
calibre -xrc -fmt -c ./calibre/calibrexRC.tvf -E ./output/xrc.svrf |& tee ./output/xrc.log3

