# Change the environment variable value $PDK_DIR by replacing the string
# 'PDKDirectory' with the absolute path to the PDK directory (including the
# PDK directory name)

setenv PDK_DIR PDKDirectory

# These environmental variables specify the metal grids offsets from either
# X or Y axis, depending on the metal routing direction. The default offset
# value is 0 nm. To offset a particular grid by 'p' nm, specify the
# variable value as p*10.  Thus, for an offset of 24 nm, the corresponding
# variable value is 240.

setenv VAR_M4_YOFFSET "0"
setenv VAR_M5_XOFFSET "0"
setenv VAR_M6_YOFFSET "0"
setenv VAR_M7_XOFFSET "0"
