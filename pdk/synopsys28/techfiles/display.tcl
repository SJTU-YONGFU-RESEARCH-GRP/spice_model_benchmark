#DisplayResourceTcl
set display_object [db::getNext [dr::getDisplays -filter "%name == {display}"]]
if {$display_object == ""} {
	set display_object [dr::createDisplay display -maxColors 256 -maxStipples 256 -maxLineStyles 256 ]
}
# Colors definition
dr::createColor yellow -display $display_object -red 255 -green 255 -blue 0
dr::createColor white -display $display_object -red 255 -green 255 -blue 255
dr::createColor black -display $display_object -red 0 -green 0 -blue 0
dr::createColor silver -display $display_object -red 198 -green 210 -blue 232
dr::createColor cream -display $display_object -red 255 -green 255 -blue 204
dr::createColor pink -display $display_object -red 255 -green 191 -blue 242
dr::createColor magenta -display $display_object -red 255 -green 0 -blue 255
dr::createColor lime -display $display_object -red 0 -green 255 -blue 0
dr::createColor tan -display $display_object -red 255 -green 230 -blue 191
dr::createColor cyan -display $display_object -red 179 -green 255 -blue 253
dr::createColor cadetBlue -display $display_object -red 57 -green 191 -blue 255
dr::createColor orange -display $display_object -red 255 -green 128 -blue 0
dr::createColor red -display $display_object -red 255 -green 0 -blue 0
dr::createColor purple -display $display_object -red 153 -green 0 -blue 230
dr::createColor green -display $display_object -red 0 -green 255 -blue 0
dr::createColor brown -display $display_object -red 191 -green 64 -blue 38
dr::createColor blue -display $display_object -red 0 -green 0 -blue 255
dr::createColor slate -display $display_object -red 140 -green 140 -blue 166
dr::createColor gold -display $display_object -red 217 -green 204 -blue 0
dr::createColor maroon -display $display_object -red 230 -green 31 -blue 13
dr::createColor violet -display $display_object -red 94 -green 0 -blue 230
dr::createColor forest -display $display_object -red 38 -green 140 -blue 107
dr::createColor chocolate -display $display_object -red 216 -green 0 -blue 4
dr::createColor navy -display $display_object -red 51 -green 51 -blue 153
dr::createColor gray -display $display_object -red 204 -green 204 -blue 217
dr::createColor lightWhite -display $display_object -red 127 -green 127 -blue 127
dr::createColor lightYellow -display $display_object -red 127 -green 127 -blue 0
dr::createColor lightRed -display $display_object -red 127 -green 0 -blue 0
dr::createColor lightPurple -display $display_object -red 76 -green 0 -blue 115
dr::createColor lightGreen -display $display_object -red 0 -green 102 -blue 51
dr::createColor lightGray -display $display_object -red 102 -green 102 -blue 108
dr::createColor lightGold -display $display_object -red 180 -green 0 -blue 0
dr::createColor lightMaroon -display $display_object -red 115 -green 15 -blue 6
dr::createColor lightCyan -display $display_object -red 0 -green 127 -blue 127
dr::createColor lightBlue -display $display_object -red 0 -green 0 -blue 79
dr::createColor winColor1 -display $display_object -red 166 -green 166 -blue 166
dr::createColor winColor2 -display $display_object -red 115 -green 115 -blue 115
dr::createColor winColor3 -display $display_object -red 189 -green 204 -blue 204
dr::createColor winColor4 -display $display_object -red 204 -green 204 -blue 204
dr::createColor winColor5 -display $display_object -red 199 -green 199 -blue 199
dr::createColor blinkRed -display $display_object -red 255 -green 0 -blue 0 -blink true
dr::createColor blinkYellow -display $display_object -red 255 -green 255 -blue 0 -blink true
dr::createColor blinkWhite -display $display_object -red 255 -green 255 -blue 255 -blink true
dr::createColor TrueColorBright -display $display_object -red 166 -green 176 -blue 186
dr::createColor TrueColorGhost -display $display_object -red 160 -green 200 -blue 240
dr::createColor plotcolor0 -display $display_object -red 255 -green 0 -blue 0
dr::createColor plotcolor1 -display $display_object -red 204 -green 0 -blue 255
dr::createColor plotcolor2 -display $display_object -red 0 -green 255 -blue 102
dr::createColor plotcolor3 -display $display_object -red 204 -green 255 -blue 0
dr::createColor plotcolor4 -display $display_object -red 0 -green 102 -blue 255
dr::createColor plotcolor5 -display $display_object -red 255 -green 153 -blue 0
dr::createColor plotcolor6 -display $display_object -red 255 -green 0 -blue 153
dr::createColor plotcolor7 -display $display_object -red 0 -green 255 -blue 255
dr::createColor plotcolor8 -display $display_object -red 51 -green 255 -blue 0
dr::createColor plotcolor9 -display $display_object -red 51 -green 0 -blue 255
dr::createColor plotcolor10 -display $display_object -red 255 -green 153 -blue 153
dr::createColor plotcolor11 -display $display_object -red 235 -green 153 -blue 255
dr::createColor plotcolor12 -display $display_object -red 153 -green 255 -blue 194
dr::createColor plotcolor13 -display $display_object -red 235 -green 255 -blue 153
dr::createColor plotcolor14 -display $display_object -red 153 -green 194 -blue 255
dr::createColor plotcolor15 -display $display_object -red 255 -green 214 -blue 153
dr::createColor plotcolor16 -display $display_object -red 255 -green 153 -blue 214
dr::createColor plotcolor17 -display $display_object -red 153 -green 255 -blue 255
dr::createColor plotcolor18 -display $display_object -red 173 -green 255 -blue 153
dr::createColor plotcolor19 -display $display_object -red 173 -green 153 -blue 255
dr::createColor plotpacketrefcolor -display $display_object -red 255 -green 217 -blue 78
dr::createColor 6 -display $display_object -red 157 -green 188 -blue 255
dr::createColor 8 -display $display_object -red 0 -green 175 -blue 0
dr::createColor 10 -display $display_object -red 0 -green 175 -blue 190
dr::createColor 11 -display $display_object -red 143 -green 184 -blue 255
dr::createColor 13 -display $display_object -red 0 -green 255 -blue 100
dr::createColor 20 -display $display_object -red 90 -green 80 -blue 0
dr::createColor 23 -display $display_object -red 90 -green 80 -blue 255
dr::createColor 25 -display $display_object -red 90 -green 175 -blue 100
dr::createColor 27 -display $display_object -red 90 -green 175 -blue 255
dr::createColor 28 -display $display_object -red 255 -green 0 -blue 190
dr::createColor 31 -display $display_object -red 33 -green 255 -blue 248
dr::createColor 32 -display $display_object -red 180 -green 0 -blue 0
dr::createColor 34 -display $display_object -red 180 -green 0 -blue 190
dr::createColor 35 -display $display_object -red 180 -green 0 -blue 255
dr::createColor 36 -display $display_object -red 180 -green 80 -blue 0
dr::createColor 38 -display $display_object -red 255 -green 81 -blue 232
dr::createColor 40 -display $display_object -red 180 -green 175 -blue 0
dr::createColor 43 -display $display_object -red 180 -green 175 -blue 255
dr::createColor 44 -display $display_object -red 200 -green 75 -blue 55
dr::createColor 47 -display $display_object -red 180 -green 255 -blue 255
dr::createColor 50 -display $display_object -red 211 -green 0 -blue 158
dr::createColor ltGreen -display $display_object -red 0 -green 240 -blue 110
dr::createColor 52 -display $display_object -red 255 -green 6 -blue 2
dr::createColor 55 -display $display_object -red 250 -green 200 -blue 100
dr::createColor 54 -display $display_object -red 255 -green 80 -blue 190
dr::createColor 58 -display $display_object -red 255 -green 143 -blue 74
dr::createColor 59 -display $display_object -red 255 -green 164 -blue 243
dr::createColor 62 -display $display_object -red 255 -green 255 -blue 190
dr::createColor drab -display $display_object -red 0 -green 170 -blue 0
dr::createColor aqua -display $display_object -red 0 -green 178 -blue 178
dr::createColor lead -display $display_object -red 22 -green 255 -blue 22
dr::createColor 21 -display $display_object -red 143 -green 184 -blue 255
# Stipples definition
dr::createStipple blank -display $display_object -pattern [ list \
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  } ]
dr::createStipple solid -display $display_object -pattern [ list \
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  } ]
dr::createStipple dots -display $display_object -pattern [ list \
                                                              { 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  }\
                                                              { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                              { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                              { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                              { 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  }\
                                                              { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                              { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                              { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                              { 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  }\
                                                              { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                              { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                              { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                              { 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  }\
                                                              { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                              { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                              { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  } ]
dr::createStipple dots1 -display $display_object -pattern [ list \
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0  } ]
dr::createStipple hLine -display $display_object -pattern [ list \
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  } ]
dr::createStipple vLine -display $display_object -pattern [ list \
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  } ]
dr::createStipple cross -display $display_object -pattern [ list \
                                                               { 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0  }\
                                                               { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                               { 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0  }\
                                                               { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                               { 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0  }\
                                                               { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                               { 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0  }\
                                                               { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                               { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                               { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  } ]
dr::createStipple grid -display $display_object -pattern [ list \
                                                              { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                              { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                              { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                              { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                              { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                              { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                              { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                              { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                              { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                              { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                              { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                              { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                              { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                              { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                              { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                              { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  } ]
dr::createStipple slash -display $display_object -pattern [ list \
                                                               { 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                               { 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0  }\
                                                               { 0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0  }\
                                                               { 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0  }\
                                                               { 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                               { 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0  }\
                                                               { 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0  } ]
dr::createStipple backSlash -display $display_object -pattern [ list \
                                                                   { 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0  }\
                                                                   { 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  }\
                                                                   { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                                   { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                                   { 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0  }\
                                                                   { 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  }\
                                                                   { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                                   { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                                   { 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0  }\
                                                                   { 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  }\
                                                                   { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                                   { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                                   { 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0  }\
                                                                   { 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  }\
                                                                   { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                                   { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  } ]
dr::createStipple hZigZag -display $display_object -pattern [ list \
                                                                 { 1 1 0 0 0 0 0 0 1 1 0 0 0 0 0 0  }\
                                                                 { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                                 { 0 0 0 1 1 0 0 0 0 0 0 1 1 0 0 0  }\
                                                                 { 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0  }\
                                                                 { 0 0 0 0 0 0 1 1 0 0 0 0 0 0 1 1  }\
                                                                 { 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0  }\
                                                                 { 0 1 1 0 0 0 0 0 0 1 1 0 0 0 0 0  }\
                                                                 { 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0  }\
                                                                 { 0 0 0 0 1 1 0 0 0 0 0 0 1 1 0 0  }\
                                                                 { 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0  }\
                                                                 { 1 0 0 0 0 0 0 1 1 0 0 0 0 0 0 1  }\
                                                                 { 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0  }\
                                                                 { 0 0 1 1 0 0 0 0 0 0 1 1 0 0 0 0  }\
                                                                 { 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0  }\
                                                                 { 0 0 0 0 0 1 1 0 0 0 0 0 0 1 1 0  }\
                                                                 { 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1  } ]
dr::createStipple vZigZag -display $display_object -pattern [ list \
                                                                 { 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0  }\
                                                                 { 1 0 0 0 0 0 1 0 0 0 0 1 0 0 0 0  }\
                                                                 { 0 1 0 0 0 0 1 0 0 0 0 0 1 0 0 0  }\
                                                                 { 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0  }\
                                                                 { 0 0 1 0 0 0 0 0 1 0 0 0 0 1 0 0  }\
                                                                 { 0 0 0 1 0 0 0 0 1 0 0 0 0 0 1 0  }\
                                                                 { 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0  }\
                                                                 { 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 1  }\
                                                                 { 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0  }\
                                                                 { 1 0 0 0 0 0 1 0 0 0 0 1 0 0 0 0  }\
                                                                 { 0 1 0 0 0 0 1 0 0 0 0 0 1 0 0 0  }\
                                                                 { 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0  }\
                                                                 { 0 0 1 0 0 0 0 0 1 0 0 0 0 1 0 0  }\
                                                                 { 0 0 0 1 0 0 0 0 1 0 0 0 0 0 1 0  }\
                                                                 { 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0  }\
                                                                 { 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 1  } ]
dr::createStipple hCurb -display $display_object -pattern [ list \
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 1 1 1 1 1 0 0 0 1 1 1 1 1  }\
                                                               { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                               { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                               { 1 1 1 1 0 0 0 1 1 1 1 1 0 0 0 1  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 1 1 1 1 1 0 0 0 1 1 1 1 1  }\
                                                               { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                               { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                               { 1 1 1 1 0 0 0 1 1 1 1 1 0 0 0 1  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                               { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  } ]
dr::createStipple vCurb -display $display_object -pattern [ list \
                                                               { 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0  }\
                                                               { 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0  }\
                                                               { 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0  }\
                                                               { 0 0 1 1 1 1 0 0 0 0 1 1 1 1 0 0  }\
                                                               { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                               { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                               { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                               { 0 0 1 1 1 1 0 0 0 0 1 1 1 1 0 0  }\
                                                               { 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0  }\
                                                               { 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0  }\
                                                               { 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0  }\
                                                               { 0 0 1 1 1 1 0 0 0 0 1 1 1 1 0 0  }\
                                                               { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                               { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                               { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                               { 0 0 1 1 1 1 0 0 0 0 1 1 1 1 0 0  } ]
dr::createStipple brick -display $display_object -pattern [ list \
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                               { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                               { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0  }\
                                                               { 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0  }\
                                                               { 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                               { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                               { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                               { 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  }\
                                                               { 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0  }\
                                                               { 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0  }\
                                                               { 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0  } ]
dr::createStipple dagger -display $display_object -pattern [ list \
                                                                { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                                { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                                { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                                { 1 1 1 1 1 0 0 0 1 1 1 1 1 0 0 0  }\
                                                                { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                                { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                                { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                                { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                { 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0  }\
                                                                { 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0  }\
                                                                { 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0  }\
                                                                { 0 0 0 1 1 1 1 1 0 0 0 1 1 1 1 1  }\
                                                                { 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0  }\
                                                                { 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0  }\
                                                                { 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0  } ]
dr::createStipple triangle -display $display_object -pattern [ list \
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0  }\
                                                                  { 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0  }\
                                                                  { 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  } ]
dr::createStipple x -display $display_object -pattern [ list \
                                                           { 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0  }\
                                                           { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                           { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                           { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                           { 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0  }\
                                                           { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                           { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                           { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                           { 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0  }\
                                                           { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                           { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                           { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                           { 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0  }\
                                                           { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                           { 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  }\
                                                           { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  } ]
dr::createStipple welldot -display $display_object -pattern [ list \
                                                                 { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                 { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                 { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                 { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                 { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                 { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                 { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                 { 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0  }\
                                                                 { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                 { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                 { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                 { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                 { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                 { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                 { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                 { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  } ]
dr::createStipple impdot -display $display_object -pattern [ list \
                                                                { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                { 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0  }\
                                                                { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                { 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0  }\
                                                                { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  } ]
dr::createStipple hidot -display $display_object -pattern [ list \
                                                               { 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0  }\
                                                               { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                               { 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0  }\
                                                               { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                               { 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0  }\
                                                               { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                               { 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0  }\
                                                               { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                               { 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0  }\
                                                               { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                               { 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0  }\
                                                               { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                               { 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0  }\
                                                               { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  }\
                                                               { 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0  }\
                                                               { 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1  } ]
dr::createStipple rhidot -display $display_object -pattern [ list \
                                                                { 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  }\
                                                                { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                                { 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  }\
                                                                { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                                { 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  }\
                                                                { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                                { 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  }\
                                                                { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                                { 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  }\
                                                                { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                                { 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  }\
                                                                { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                                { 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  }\
                                                                { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  }\
                                                                { 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  }\
                                                                { 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  } ]
dr::createStipple twelldot -display $display_object -pattern [ list \
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  } ]
dr::createStipple slashw -display $display_object -pattern [ list \
                                                                { 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0  }\
                                                                { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                                { 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0  }\
                                                                { 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0  }\
                                                                { 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1  }\
                                                                { 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0  }\
                                                                { 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0  }\
                                                                { 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0  }\
                                                                { 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0  }\
                                                                { 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                                { 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0  }\
                                                                { 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0  }\
                                                                { 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1  }\
                                                                { 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0  }\
                                                                { 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0  }\
                                                                { 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0  } ]
dr::createStipple rotateslash -display $display_object -pattern [ list \
                                                                     { 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0  }\
                                                                     { 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0  }\
                                                                     { 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                                     { 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0  }\
                                                                     { 0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0  }\
                                                                     { 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0  }\
                                                                     { 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                     { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  }\
                                                                     { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0  }\
                                                                     { 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0  }\
                                                                     { 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0  }\
                                                                     { 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0  }\
                                                                     { 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                                     { 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0  }\
                                                                     { 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0  }\
                                                                     { 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0  } ]
dr::createStipple M7 -display $display_object -pattern [ list \
                                                                  { 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0  }\
                                                                  { 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  } ]
# LineStyles definition
dr::createLineStyle solid -display $display_object -width 1 -pattern [ list 1 1 1 ]
dr::createLineStyle dashed -display $display_object -width 1 -pattern [ list 1 1 1 1 0 0 ]
dr::createLineStyle dots -display $display_object -width 1 -pattern [ list 1 0 0 ]
dr::createLineStyle dashDot -display $display_object -width 1 -pattern [ list 1 1 1 0 0 1 0 0 ]
dr::createLineStyle shortDash -display $display_object -width 1 -pattern [ list 1 1 0 0 ]
dr::createLineStyle doubleDash -display $display_object -width 1 -pattern [ list 1 1 1 1 0 0 1 1 0 0 ]
dr::createLineStyle hidden -display $display_object -width 1 -pattern [ list 1 0 0 0 ]
dr::createLineStyle mediumLine -display $display_object -width 2 -pattern [ list 1 1 1 ]
dr::createLineStyle thickLine -display $display_object -width 3 -pattern [ list 1 1 1 ]
dr::createLineStyle hidot -display $display_object -width 1 -pattern [ list 1 1 1 ]
dr::createLineStyle impdot -display $display_object -width 1 -pattern [ list 1 1 1 ]
dr::createLineStyle rhidot -display $display_object -width 1 -pattern [ list 1 1 1 ]
dr::createLineStyle twelldot -display $display_object -width 1 -pattern [ list 1 1 1 ]
dr::createLineStyle welldot -display $display_object -width 1 -pattern [ list 1 1 1 ]
dr::createLineStyle thickDash -display $display_object -width 3 -pattern [ list 1 1 1 1 0 0 ]
dr::createLineStyle lineStyle0 -display $display_object -width 1 -pattern [ list 1 ]
dr::createLineStyle lineStyle1 -display $display_object -width 1 -pattern [ list 1 1 1 1 0 0 0 0 1 1 1 1 0 0 0 0 ]
dr::createLineStyle lineStyle2 -display $display_object -width 1 -pattern [ list 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 ]
dr::createLineStyle lineStyle3 -display $display_object -width 1 -pattern [ list 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 ]
dr::createLineStyle lineStyle4 -display $display_object -width 1 -pattern [ list 1 1 1 1 1 0 0 0 0 0 0 1 1 1 1 1 ]
dr::createLineStyle lineStyle5 -display $display_object -width 1 -pattern [ list 0 0 0 1 1 0 0 0 0 0 0 1 1 0 0 0 ]
dr::createLineStyle mLine -display $display_object -width 2 -pattern [ list 1 1 1 ]
dr::createLineStyle thickLine2 -display $display_object -width 2 -pattern [ list 1 1 1 ]
# Packets definition
dr::createPacket background -display $display_object -stipple blank \
                          -lineStyle solid -fill black -outline black
dr::createPacket grid -display $display_object -stipple blank \
                    -lineStyle solid -fill slate -outline slate
dr::createPacket grid1 -display $display_object -stipple blank \
                     -lineStyle solid -fill white -outline white
dr::createPacket axis -display $display_object -stipple blank \
                    -lineStyle solid -fill white -outline white
dr::createPacket instance -display $display_object -stipple blank \
                            -lineStyle solid -fill red -outline red
dr::createPacket instanceLbl -display $display_object -stipple blank \
                             -lineStyle solid -fill gold -outline gold
dr::createPacket prBoundary -display $display_object -stipple blank \
                        -lineStyle solid -fill purple -outline purple
dr::createPacket prBoundaryBnd -display $display_object -stipple blank \
                               -lineStyle solid -fill cyan -outline cyan
dr::createPacket prBoundaryLbl -display $display_object -stipple blank \
                           -lineStyle solid -fill purple -outline purple
dr::createPacket align -display $display_object -stipple blank \
                         -lineStyle solid -fill tan -outline tan
dr::createPacket alignAssist -display $display_object -stipple blank \
                            -lineStyle solid -fill tan -outline yellow -fillStyle outline
dr::createPacket hardFence -display $display_object -stipple blank \
                             -lineStyle solid -fill red -outline red
dr::createPacket softFence -display $display_object -stipple blank \
                       -lineStyle solid -fill yellow -outline yellow
dr::createPacket text -display $display_object -stipple blank \
                    -lineStyle solid -fill white -outline white
dr::createPacket text1 -display $display_object -stipple blank \
                    -lineStyle dashed -fill white -outline white
dr::createPacket text2 -display $display_object -stipple solid \
                     -lineStyle solid -fill white -outline white
dr::createPacket border -display $display_object -stipple blank \
                          -lineStyle solid -fill tan -outline tan
dr::createPacket device -display $display_object -stipple blank \
                      -lineStyle solid -fill green -outline green
dr::createPacket device2 -display $display_object -stipple blank \
                      -lineStyle dashed -fill green -outline green
dr::createPacket device1 -display $display_object -stipple solid \
                       -lineStyle solid -fill green -outline green
dr::createPacket wire -display $display_object -stipple solid \
            -lineStyle solid -fill cadetBlue -outline cadetBlue
dr::createPacket wireLbl -display $display_object -stipple solid \
               -lineStyle solid -fill cadetBlue -outline cadetBlue
dr::createPacket wireFlt -display $display_object -stipple blank \
                          -lineStyle dashed -fill red -outline red
dr::createPacket highlightUnplaced -display $display_object -stipple X \
                         -lineStyle solid -fill magenta -outline magenta
dr::createPacket deviceAnt -display $display_object -stipple blank \
                       -lineStyle solid -fill yellow -outline yellow
dr::createPacket deviceLbl -display $display_object -stipple blank \
                         -lineStyle solid -fill green -outline green
dr::createPacket pinLbl -display $display_object -stipple blank \
                          -lineStyle solid -fill red -outline red
dr::createPacket pin -display $display_object -stipple solid \
                       -lineStyle solid -fill red -outline red
dr::createPacket pinAnt -display $display_object -stipple blank \
                          -lineStyle solid -fill red -outline red
dr::createPacket annotate -display $display_object -stipple blank \
                      -lineStyle solid -fill orange -outline orange
dr::createPacket annotate1 -display $display_object -stipple blank \
                           -lineStyle solid -fill pink -outline pink
dr::createPacket annotate2 -display $display_object -stipple blank \
                           -lineStyle solid -fill lime -outline lime
dr::createPacket annotate3 -display $display_object -stipple blank \
                           -lineStyle solid -fill cyan -outline cyan
dr::createPacket annotate4 -display $display_object -stipple blank \
                       -lineStyle solid -fill yellow -outline yellow
dr::createPacket annotate5 -display $display_object -stipple blank \
                         -lineStyle solid -fill white -outline white
dr::createPacket annotate6 -display $display_object -stipple blank \
                       -lineStyle solid -fill silver -outline silver
dr::createPacket annotate7 -display $display_object -stipple blank \
                             -lineStyle solid -fill red -outline red
dr::createPacket annotate8 -display $display_object -stipple blank \
                             -lineStyle solid -fill tan -outline tan
dr::createPacket annotate9 -display $display_object -stipple blank \
                         -lineStyle solid -fill green -outline green
dr::createPacket edgeLayer -display $display_object -stipple blank \
                 -lineStyle solid -fill winColor5 -outline winColor5
dr::createPacket edgeLayerPin -display $display_object -stipple blank \
                          -lineStyle solid -fill yellow -outline yellow
dr::createPacket snap -display $display_object -stipple blank \
                  -lineStyle solid -fill yellow -outline yellow
dr::createPacket stretch -display $display_object -stipple blank \
                     -lineStyle solid -fill yellow -outline yellow
dr::createPacket y0 -display $display_object -stipple blank \
                -lineStyle solid -fill yellow -outline yellow
dr::createPacket y1 -display $display_object -stipple blank \
                      -lineStyle solid -fill red -outline red
dr::createPacket y2 -display $display_object -stipple blank \
                  -lineStyle solid -fill green -outline green
dr::createPacket y3 -display $display_object -stipple blank \
              -lineStyle solid -fill magenta -outline magenta
dr::createPacket y4 -display $display_object -stipple blank \
                    -lineStyle solid -fill cyan -outline cyan
dr::createPacket y5 -display $display_object -stipple blank \
                -lineStyle solid -fill purple -outline purple
dr::createPacket y6 -display $display_object -stipple blank \
                -lineStyle solid -fill orange -outline orange
dr::createPacket y7 -display $display_object -stipple blank \
                    -lineStyle solid -fill gold -outline gold
dr::createPacket y8 -display $display_object -stipple blank \
                    -lineStyle solid -fill blue -outline blue
dr::createPacket y9 -display $display_object -stipple blank \
                -lineStyle solid -fill silver -outline silver
dr::createPacket y0Flt -display $display_object -stipple blank \
                   -lineStyle solid -fill yellow -outline yellow
dr::createPacket y1Flt -display $display_object -stipple blank \
                         -lineStyle solid -fill red -outline red
dr::createPacket y2Flt -display $display_object -stipple blank \
                     -lineStyle solid -fill green -outline green
dr::createPacket y3Flt -display $display_object -stipple blank \
                 -lineStyle solid -fill magenta -outline magenta
dr::createPacket y4Flt -display $display_object -stipple blank \
                       -lineStyle solid -fill cyan -outline cyan
dr::createPacket y5Flt -display $display_object -stipple blank \
                   -lineStyle solid -fill purple -outline purple
dr::createPacket y6Flt -display $display_object -stipple blank \
                   -lineStyle solid -fill orange -outline orange
dr::createPacket y7Flt -display $display_object -stipple blank \
                       -lineStyle solid -fill gold -outline gold
dr::createPacket y8Flt -display $display_object -stipple blank \
                       -lineStyle solid -fill blue -outline blue
dr::createPacket y9Flt -display $display_object -stipple blank \
                   -lineStyle solid -fill silver -outline silver
dr::createPacket hilite -display $display_object -stipple blank \
                      -lineStyle solid -fill white -outline white
dr::createPacket hilite1 -display $display_object -stipple blank \
                   -lineStyle solid -fill magenta -outline magenta
dr::createPacket hilite2 -display $display_object -stipple blank \
                           -lineStyle solid -fill tan -outline tan
dr::createPacket hilite3 -display $display_object -stipple blank \
                         -lineStyle solid -fill cyan -outline cyan
dr::createPacket hilite4 -display $display_object -stipple blank \
                     -lineStyle solid -fill orange -outline orange
dr::createPacket hilite5 -display $display_object -stipple blank \
                         -lineStyle solid -fill lime -outline lime
dr::createPacket hilite6 -display $display_object -stipple blank \
                     -lineStyle solid -fill orange -outline orange
dr::createPacket hilite7 -display $display_object -stipple blank \
                       -lineStyle solid -fill cream -outline cream
dr::createPacket hilite8 -display $display_object -stipple blank \
                   -lineStyle solid -fill magenta -outline magenta
dr::createPacket hilite9 -display $display_object -stipple blank \
                         -lineStyle solid -fill pink -outline pink
dr::createPacket select -display $display_object -stipple blank \
                      -lineStyle thickLine -fill tan -outline tan
dr::createPacket drive -display $display_object -stipple blank \
                       -lineStyle solid -fill blue -outline blue
dr::createPacket hiz -display $display_object -stipple blank \
                 -lineStyle solid -fill orange -outline orange
dr::createPacket resist -display $display_object -stipple blank \
                        -lineStyle solid -fill cyan -outline cyan
dr::createPacket spike -display $display_object -stipple blank \
                   -lineStyle solid -fill purple -outline purple
dr::createPacket supply -display $display_object -stipple blank \
                        -lineStyle solid -fill lime -outline lime
dr::createPacket unknown -display $display_object -stipple blank \
                     -lineStyle solid -fill yellow -outline yellow
dr::createPacket unset -display $display_object -stipple blank \
                   -lineStyle solid -fill forest -outline forest
dr::createPacket designFlow -display $display_object -stipple dots \
                           -lineStyle solid -fill blue -outline blue
dr::createPacket designFlow1 -display $display_object -stipple dots \
                        -lineStyle solid -fill purple -outline purple
dr::createPacket designFlow2 -display $display_object -stipple dots \
                      -lineStyle solid -fill magenta -outline magenta
dr::createPacket designFlow3 -display $display_object -stipple dots \
                            -lineStyle solid -fill cyan -outline cyan
dr::createPacket designFlow4 -display $display_object -stipple dots \
                        -lineStyle solid -fill forest -outline forest
dr::createPacket designFlow5 -display $display_object -stipple dots \
                          -lineStyle solid -fill green -outline green
dr::createPacket designFlow6 -display $display_object -stipple dots \
                        -lineStyle solid -fill orange -outline orange
dr::createPacket designFlow7 -display $display_object -stipple dots \
                        -lineStyle solid -fill yellow -outline yellow
dr::createPacket designFlow8 -display $display_object -stipple dots \
                          -lineStyle solid -fill brown -outline brown
dr::createPacket designFlow9 -display $display_object -stipple dots \
                              -lineStyle solid -fill red -outline red
dr::createPacket changedLayerTl0 -display $display_object -stipple blank \
                                   -lineStyle solid -fill red -outline red
dr::createPacket changedLayerTl1 -display $display_object -stipple blank \
                             -lineStyle solid -fill yellow -outline yellow
dr::createPacket markerAno -display $display_object -stipple X \
                       -lineStyle solid -fill blue -outline blue
dr::createPacket markerInf -display $display_object -stipple X \
                     -lineStyle solid -fill green -outline green
dr::createPacket markerAck -display $display_object -stipple X \
                   -lineStyle solid -fill yellow -outline yellow
dr::createPacket markerWarn -display $display_object -stipple X \
          -lineStyle solid -fill blinkYellow -outline blinkYellow
dr::createPacket markerSer -display $display_object -stipple X \
                   -lineStyle solid -fill orange -outline orange
dr::createPacket markerErr -display $display_object -stipple X \
           -lineStyle solid -fill blinkWhite -outline blinkWhite
dr::createPacket markerScr -display $display_object -stipple X \
                         -lineStyle solid -fill red -outline red
dr::createPacket markerCrt -display $display_object -stipple X \
                         -lineStyle solid -fill red -outline red
dr::createPacket markerFat -display $display_object -stipple X \
               -lineStyle solid -fill blinkRed -outline blinkRed
dr::createPacket Row -display $display_object -stipple blank \
                     -lineStyle solid -fill cyan -outline cyan
dr::createPacket RowBnd -display $display_object -stipple blank \
                        -lineStyle solid -fill cyan -outline cyan
dr::createPacket RowLbl -display $display_object -stipple blank \
                        -lineStyle solid -fill cyan -outline cyan
dr::createPacket Group -display $display_object -stipple dots \
                    -lineStyle solid -fill green -outline green
dr::createPacket GroupLbl -display $display_object -stipple blank \
                        -lineStyle solid -fill green -outline green
dr::createPacket GroupBnd -display $display_object -stipple blank \
                        -lineStyle solid -fill green -outline green
dr::createPacket Cannotoccupy -display $display_object -stipple X \
                            -lineStyle solid -fill red -outline red
dr::createPacket CannotoccupyBnd -display $display_object -stipple blank \
                                   -lineStyle solid -fill red -outline red
dr::createPacket Canplace -display $display_object -stipple blank \
                          -lineStyle solid -fill cyan -outline cyan
dr::createPacket Unrouted -display $display_object -stipple blank \
               -lineStyle dashed -fill winColor5 -outline winColor5
dr::createPacket UnroutedTrk -display $display_object -stipple blank \
                        -lineStyle dashed -fill yellow -outline yellow
dr::createPacket Unrouted1 -display $display_object -stipple blank \
                        -lineStyle dashed -fill brown -outline brown
dr::createPacket Unrouted2 -display $display_object -stipple blank \
                            -lineStyle dashed -fill red -outline red
dr::createPacket Unrouted3 -display $display_object -stipple blank \
                          -lineStyle dashed -fill pink -outline pink
dr::createPacket Unrouted4 -display $display_object -stipple blank \
                      -lineStyle dashed -fill orange -outline orange
dr::createPacket Unrouted5 -display $display_object -stipple blank \
                        -lineStyle dashed -fill green -outline green
dr::createPacket Unrouted6 -display $display_object -stipple blank \
                          -lineStyle dashed -fill blue -outline blue
dr::createPacket Unrouted7 -display $display_object -stipple blank \
                      -lineStyle dashed -fill purple -outline purple
dr::createPacket Unrouted8 -display $display_object -stipple blank \
                          -lineStyle dashed -fill gold -outline gold
dr::createPacket Unrouted9 -display $display_object -stipple blank \
                      -lineStyle dashed -fill silver -outline silver
dr::createPacket stroke_white -display $display_object -stipple blank \
                            -lineStyle solid -fill white -outline white
dr::createPacket select1_yellow -display $display_object -stipple blank \
                            -lineStyle solid -fill yellow -outline yellow
dr::createPacket select2_red -display $display_object -stipple blank \
                               -lineStyle solid -fill red -outline red
dr::createPacket select3_blue -display $display_object -stipple blank \
                              -lineStyle solid -fill blue -outline blue
dr::createPacket select4_purple -display $display_object -stipple blank \
                            -lineStyle solid -fill purple -outline purple
dr::createPacket highlight1_yellow -display $display_object -stipple blank \
                          -lineStyle mediumLine -fill yellow -outline yellow
dr::createPacket highlight2_red -display $display_object -stipple blank \
                             -lineStyle mediumLine -fill red -outline red
dr::createPacket highlight3_green -display $display_object -stipple blank \
                           -lineStyle mediumLine -fill green -outline green
dr::createPacket highlight4_blue -display $display_object -stipple blank \
                            -lineStyle mediumLine -fill blue -outline blue
dr::createPacket highlight5_purple -display $display_object -stipple blank \
                          -lineStyle mediumLine -fill purple -outline purple
dr::createPacket highlight6_cyan -display $display_object -stipple blank \
                            -lineStyle mediumLine -fill cyan -outline cyan
dr::createPacket highlight7_white -display $display_object -stipple blank \
                           -lineStyle mediumLine -fill white -outline white
dr::createPacket highlight8_gold -display $display_object -stipple blank \
                            -lineStyle mediumLine -fill gold -outline gold
dr::createPacket highlight9_maroon -display $display_object -stipple blank \
                          -lineStyle mediumLine -fill maroon -outline maroon
dr::createPacket highlight10_gray -display $display_object -stipple blank \
                             -lineStyle mediumLine -fill gray -outline gray
dr::createPacket highlight1_yellow_dim -display $display_object -stipple blank \
                    -lineStyle mediumLine -fill lightYellow -outline lightYellow
dr::createPacket highlight2_red_dim -display $display_object -stipple blank \
                       -lineStyle mediumLine -fill lightRed -outline lightRed
dr::createPacket highlight3_green_dim -display $display_object -stipple blank \
                     -lineStyle mediumLine -fill lightGreen -outline lightGreen
dr::createPacket highlight4_blue_dim -display $display_object -stipple blank \
                      -lineStyle mediumLine -fill lightBlue -outline lightBlue
dr::createPacket highlight5_purple_dim -display $display_object -stipple blank \
                    -lineStyle mediumLine -fill lightPurple -outline lightPurple
dr::createPacket highlight6_cyan_dim -display $display_object -stipple blank \
                      -lineStyle mediumLine -fill lightCyan -outline lightCyan
dr::createPacket highlight7_white_dim -display $display_object -stipple blank \
                     -lineStyle mediumLine -fill lightWhite -outline lightWhite
dr::createPacket highlight8_gold_dim -display $display_object -stipple blank \
                      -lineStyle mediumLine -fill lightGold -outline lightGold
dr::createPacket highlight9_maroon_dim -display $display_object -stipple blank \
                    -lineStyle mediumLine -fill lightMaroon -outline lightMaroon
dr::createPacket highlight10_gray_dim -display $display_object -stipple blank \
                       -lineStyle mediumLine -fill lightGray -outline lightGray
dr::createPacket ruler_white -display $display_object -stipple blank \
                           -lineStyle solid -fill white -outline white
dr::createPacket active_TrueColorBright -display $display_object -stipple blank \
                 -lineStyle dashed -fill TrueColorBright -outline TrueColorBright
dr::createPacket runtime_TrueColorGhost -display $display_object -stipple blank \
                    -lineStyle solid -fill TrueColorGhost -outline TrueColorGhost
dr::createPacket cursor_white -display $display_object -stipple blank \
                            -lineStyle solid -fill white -outline white
dr::createPacket major_grid -display $display_object -stipple blank \
                      -lineStyle shortDash -fill white -outline white
dr::createPacket minor_grid -display $display_object -stipple blank \
                           -lineStyle dots -fill slate -outline slate
dr::createPacket yellow_white -display $display_object -stipple blank \
                           -lineStyle solid -fill yellow -outline white
dr::createPacket transparent_white -display $display_object -stipple blank \
                                -lineStyle solid -fill yellow -outline white -fillStyle outline
dr::createPacket pinUnc -display $display_object -stipple X \
                      -lineStyle solid -fill red -outline red
dr::createPacket wireUnrt -display $display_object -stipple blank \
               -lineStyle dashed -fill cadetBlue -outline cadetBlue
dr::createPacket inherited -display $display_object -stipple inherited \
                 -lineStyle inherited -fill inherited -outline inherited
dr::createPacket plotpacket0 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor0
dr::createPacket plotpacket1 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor1
dr::createPacket plotpacket2 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor2
dr::createPacket plotpacket3 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor3
dr::createPacket plotpacket4 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor4
dr::createPacket plotpacket5 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor5
dr::createPacket plotpacket6 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor6
dr::createPacket plotpacket7 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor7
dr::createPacket plotpacket8 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor8
dr::createPacket plotpacket9 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor9
dr::createPacket plotpacket10 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor10
dr::createPacket plotpacket11 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor11
dr::createPacket plotpacket12 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor12
dr::createPacket plotpacket13 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor13
dr::createPacket plotpacket14 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor14
dr::createPacket plotpacket15 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor15
dr::createPacket plotpacket16 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor16
dr::createPacket plotpacket17 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor17
dr::createPacket plotpacket18 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor18
dr::createPacket plotpacket19 -display $display_object -stipple inherited \
                 -lineStyle mediumLine -fill inherited -outline plotcolor19
dr::createPacket plotpacketref -display $display_object -stipple inherited \
           -lineStyle mediumLine -fill inherited -outline plotpacketrefcolor
dr::createPacket LE_preview -display $display_object -stipple inherited \
                       -lineStyle dots -fill inherited -outline inherited
dr::createPacket LE_hole -display $display_object -stipple blank \
                     -lineStyle solid -fill yellow -outline yellow -fillStyle outline
dr::createPacket pinConn -display $display_object -stipple blank \
                           -lineStyle solid -fill red -outline red -fillStyle stipple
dr::createPacket ruler0 -display $display_object -stipple blank \
                    -lineStyle solid -fill yellow -outline yellow
dr::createPacket ruler1 -display $display_object -stipple blank \
                          -lineStyle solid -fill red -outline red
dr::createPacket ruler2 -display $display_object -stipple blank \
                      -lineStyle solid -fill green -outline green
dr::createPacket ruler3 -display $display_object -stipple blank \
                  -lineStyle solid -fill magenta -outline magenta
dr::createPacket ruler4 -display $display_object -stipple blank \
                        -lineStyle solid -fill cyan -outline cyan
dr::createPacket ruler5 -display $display_object -stipple blank \
                    -lineStyle solid -fill purple -outline purple
dr::createPacket ruler6 -display $display_object -stipple blank \
                    -lineStyle solid -fill orange -outline orange
dr::createPacket ruler7 -display $display_object -stipple blank \
                        -lineStyle solid -fill gold -outline gold
dr::createPacket ruler8 -display $display_object -stipple blank \
                        -lineStyle solid -fill blue -outline blue
dr::createPacket ruler9 -display $display_object -stipple blank \
                    -lineStyle solid -fill silver -outline silver
dr::createPacket invisibleLabel -display $display_object -stipple blank \
                           -lineStyle dashed -fill purple -outline purple
dr::createPacket BJTMY -display $display_object -stipple backSlash \
                               -lineStyle solid -fill 62 -outline 62
dr::createPacket CO -display $display_object -stipple X \
              -lineStyle solid -fill white -outline white
dr::createPacket DIFF -display $display_object -stipple rhidot \
                           -lineStyle solid -fill 40 -outline 40 -fillStyle solid
dr::createPacket DIFF_18 -display $display_object -stipple slashw \
                      -lineStyle solid -fill yellow -outline yellow -fillStyle stipple
dr::createPacket DIOD -display $display_object -stipple backSlash \
              -lineStyle solid -fill plotcolor7 -outline plotcolor7
dr::createPacket DM1EXCL -display $display_object -stipple slash \
                         -lineStyle solid -fill drab -outline drab
dr::createPacket DM2EXCL -display $display_object -stipple slash \
                             -lineStyle solid -fill 28 -outline 28
dr::createPacket DM3EXCL -display $display_object -stipple slash \
                             -lineStyle solid -fill 31 -outline 31
dr::createPacket DM4EXCL -display $display_object -stipple slash \
                             -lineStyle solid -fill 43 -outline 43
dr::createPacket DM5EXCL -display $display_object -stipple slash \
                             -lineStyle solid -fill 40 -outline 40
dr::createPacket DM6EXCL -display $display_object -stipple slash \
                             -lineStyle solid -fill 52 -outline 52
dr::createPacket DM7EXCL -display $display_object -stipple slash \
                     -lineStyle solid -fill orange -outline orange
dr::createPacket DM8EXCL -display $display_object -stipple slash \
                             -lineStyle solid -fill 36 -outline 36
dr::createPacket DM9EXCL -display $display_object -stipple slash \
                             -lineStyle solid -fill 23 -outline 23
dr::createPacket DNW -display $display_object -stipple slashw \
                          -lineStyle solid -fill 36 -outline 36
dr::createPacket ESD_25 -display $display_object -stipple slashw \
                         -lineStyle solid -fill drab -outline drab -fillStyle stipple
dr::createPacket HOTNWL -display $display_object -stipple slash \
                        -lineStyle solid -fill drab -outline drab
dr::createPacket HVTIMP -display $display_object -stipple slash \
                    -lineStyle solid -fill orange -outline orange
dr::createPacket IP -display $display_object -stipple slash \
                  -lineStyle solid -fill white -outline white
dr::createPacket LOGO -display $display_object -stipple solid \
                  -lineStyle solid -fill orange -outline orange
dr::createPacket LVTIMP -display $display_object -stipple slash \
                            -lineStyle solid -fill 31 -outline 31
dr::createPacket M1 -display $display_object -stipple rhidot \
                     -lineStyle solid -fill blue -outline blue
dr::createPacket M1DMY -display $display_object -stipple slash \
                     -lineStyle solid -fill white -outline white
dr::createPacket M1PIN -display $display_object -stipple X \
                   -lineStyle solid -fill blue -outline blue
dr::createPacket M2 -display $display_object -stipple rhidot \
                         -lineStyle solid -fill 50 -outline 50
dr::createPacket M2DMY -display $display_object -stipple slash \
                     -lineStyle solid -fill white -outline white
dr::createPacket M2PIN -display $display_object -stipple X \
                       -lineStyle solid -fill 50 -outline 50
dr::createPacket M3 -display $display_object -stipple rhidot \
                   -lineStyle solid -fill green -outline green
dr::createPacket M3DMY -display $display_object -stipple slash \
                     -lineStyle solid -fill white -outline white
dr::createPacket M3PIN -display $display_object -stipple X \
                 -lineStyle solid -fill green -outline green
dr::createPacket M4 -display $display_object -stipple rhidot \
                 -lineStyle solid -fill silver -outline silver
dr::createPacket M4DMY -display $display_object -stipple slash \
                     -lineStyle solid -fill white -outline white
dr::createPacket M4PIN -display $display_object -stipple X \
               -lineStyle solid -fill silver -outline silver
dr::createPacket M5 -display $display_object -stipple rhidot \
                     -lineStyle solid -fill aqua -outline aqua
dr::createPacket M5DMY -display $display_object -stipple slash \
                     -lineStyle solid -fill white -outline white
dr::createPacket M5PIN -display $display_object -stipple X \
                   -lineStyle solid -fill aqua -outline aqua
dr::createPacket M6 -display $display_object -stipple rhidot \
                         -lineStyle solid -fill 58 -outline 58
dr::createPacket M6DMY -display $display_object -stipple slash \
                     -lineStyle solid -fill white -outline white
dr::createPacket M6PIN -display $display_object -stipple X \
                       -lineStyle solid -fill 58 -outline 58
dr::createPacket M7 -display $display_object -stipple rhidot \
                   -lineStyle solid -fill brown -outline brown
dr::createPacket M7DMY -display $display_object -stipple slash \
                     -lineStyle solid -fill white -outline white
dr::createPacket M7PIN -display $display_object -stipple X \
                 -lineStyle solid -fill brown -outline brown
dr::createPacket M8 -display $display_object -stipple rhidot \
                         -lineStyle solid -fill 43 -outline 43
dr::createPacket M8DMY -display $display_object -stipple slash \
                     -lineStyle solid -fill white -outline white
dr::createPacket M8PIN -display $display_object -stipple X \
                       -lineStyle solid -fill 43 -outline 43
dr::createPacket M9 -display $display_object -stipple rhidot \
                         -lineStyle solid -fill 59 -outline 59
dr::createPacket M9DMY -display $display_object -stipple slash \
                     -lineStyle solid -fill white -outline white
dr::createPacket M9PIN -display $display_object -stipple X \
                       -lineStyle solid -fill 59 -outline 59
dr::createPacket MRPIN -display $display_object -stipple X \
                       -lineStyle solid -fill 59 -outline 59
dr::createPacket DIFFEXCL -display $display_object -stipple hLine \
                              -lineStyle solid -fill 59 -outline 59
dr::createPacket POEXCL -display $display_object -stipple hLine \
                            -lineStyle solid -fill 55 -outline 55
dr::createPacket NIMP -display $display_object -stipple impdot \
                       -lineStyle solid -fill lime -outline lime
dr::createPacket NWELL -display $display_object -stipple slashw \
                    -lineStyle mLine -fill silver -outline silver
dr::createPacket PAD -display $display_object -stipple solid \
                 -lineStyle solid -fill orange -outline orange
dr::createPacket PIMP -display $display_object -stipple impdot \
             -lineStyle solid -fill chocolate -outline chocolate
dr::createPacket PO -display $display_object -stipple rhidot \
                       -lineStyle solid -fill red -outline red
dr::createPacket RM1 -display $display_object -stipple hLine \
                         -lineStyle solid -fill 25 -outline 25
dr::createPacket RM2 -display $display_object -stipple hLine \
                         -lineStyle solid -fill 47 -outline 47
dr::createPacket RM3 -display $display_object -stipple hLine \
                         -lineStyle solid -fill 31 -outline 31
dr::createPacket RM4 -display $display_object -stipple hLine \
                         -lineStyle solid -fill 43 -outline 43
dr::createPacket RM5 -display $display_object -stipple hLine \
                         -lineStyle solid -fill 40 -outline 40
dr::createPacket RM6 -display $display_object -stipple hLine \
                         -lineStyle solid -fill 52 -outline 52
dr::createPacket RM7 -display $display_object -stipple hLine \
                 -lineStyle solid -fill orange -outline orange
dr::createPacket RM8 -display $display_object -stipple hLine \
                         -lineStyle solid -fill 36 -outline 36
dr::createPacket RM9 -display $display_object -stipple hLine \
                         -lineStyle solid -fill 23 -outline 23
dr::createPacket MRDL -display $display_object -stipple rhidot \
                           -lineStyle solid -fill 23 -outline 23
dr::createPacket RNW -display $display_object -stipple hLine \
                     -lineStyle solid -fill drab -outline drab
dr::createPacket RMARK -display $display_object -stipple hLine \
                           -lineStyle solid -fill 54 -outline 54
dr::createPacket SBLK -display $display_object -stipple solid \
                          -lineStyle solid -fill 62 -outline 62
dr::createPacket VIA1 -display $display_object -stipple X \
                  -lineStyle solid -fill cyan -outline cyan
dr::createPacket VIA2 -display $display_object -stipple X \
              -lineStyle solid -fill yellow -outline yellow
dr::createPacket VIA3 -display $display_object -stipple X \
                      -lineStyle solid -fill 27 -outline 27
dr::createPacket VIA4 -display $display_object -stipple X \
              -lineStyle solid -fill orange -outline orange
dr::createPacket VIA5 -display $display_object -stipple X \
                      -lineStyle solid -fill 40 -outline 40
dr::createPacket VIA6 -display $display_object -stipple X \
                      -lineStyle solid -fill 52 -outline 52
dr::createPacket VIA7 -display $display_object -stipple X \
                  -lineStyle solid -fill blue -outline blue
dr::createPacket VIA8 -display $display_object -stipple X \
                  -lineStyle solid -fill drab -outline drab
dr::createPacket VIARDL -display $display_object -stipple X \
                        -lineStyle solid -fill 44 -outline 44
dr::createPacket PrBoundary -display $display_object -stipple impdot \
                         -lineStyle solid -fill yellow -outline yellow
dr::createPacket INDMARK -display $display_object -stipple backSlash \
                             -lineStyle solid -fill drab -outline drab
dr::createPacket CBMMARK -display $display_object -stipple backSlash \
                         -lineStyle solid -fill yellow -outline yellow
dr::createPacket VARMARK -display $display_object -stipple backSlash \
                         -lineStyle solid -fill orange -outline orange
dr::createPacket CTMMARK -display $display_object -stipple backSlash \
                         -lineStyle solid -fill silver -outline silver
dr::createPacket METDMY -display $display_object -stipple rhidot \
                     -lineStyle solid -fill silver -outline silver
dr::createPacket PWELL -display $display_object -stipple slashw \
                    -lineStyle mLine -fill silver -outline silver
dr::createPacket INDPINM -display $display_object -stipple backSlash \
                         -lineStyle mLine -fill orange -outline orange
dr::createPacket DIFF_25 -display $display_object -stipple hCurb \
                                              -fill 11 -outline 11
# PacketAliases definition
dr::createPacketAlias SE_runtime -packet inherited -display $display_object
dr::createPacketAlias LE_runtime -packet inherited -display $display_object
dr::createPacketAlias active -packet active_TrueColorBright -display $display_object
dr::createPacketAlias axis_white -packet axis -display $display_object
dr::createPacketAlias coordinate_mark -packet yellow_white -display $display_object
dr::createPacketAlias cursor -packet cursor_white -display $display_object
dr::createPacketAlias display_major_grid -packet major_grid -display $display_object
dr::createPacketAlias display_minor_grid -packet minor_grid -display $display_object
dr::createPacketAlias ghost_mark -packet transparent_white -display $display_object
dr::createPacketAlias highlight1 -packet highlight1_yellow -display $display_object
dr::createPacketAlias highlight2 -packet highlight2_red -display $display_object
dr::createPacketAlias highlight3 -packet highlight3_green -display $display_object
dr::createPacketAlias highlight4 -packet highlight4_blue -display $display_object
dr::createPacketAlias highlight5 -packet highlight5_purple -display $display_object
dr::createPacketAlias highlight6 -packet highlight6_cyan -display $display_object
dr::createPacketAlias highlight7 -packet highlight7_white -display $display_object
dr::createPacketAlias highlight8 -packet highlight8_gold -display $display_object
dr::createPacketAlias highlight9 -packet highlight9_maroon -display $display_object
dr::createPacketAlias highlight10 -packet highlight10_gray -display $display_object
dr::createPacketAlias highlight1dim -packet highlight1_yellow_dim -display $display_object
dr::createPacketAlias highlight2dim -packet highlight2_red_dim -display $display_object
dr::createPacketAlias highlight3dim -packet highlight3_green_dim -display $display_object
dr::createPacketAlias highlight4dim -packet highlight4_blue_dim -display $display_object
dr::createPacketAlias highlight5dim -packet highlight5_purple_dim -display $display_object
dr::createPacketAlias highlight6dim -packet highlight6_cyan_dim -display $display_object
dr::createPacketAlias highlight7dim -packet highlight7_white_dim -display $display_object
dr::createPacketAlias highlight8dim -packet highlight8_gold_dim -display $display_object
dr::createPacketAlias highlight9dim -packet highlight9_maroon_dim -display $display_object
dr::createPacketAlias highlight10dim -packet highlight10_gray_dim -display $display_object
dr::createPacketAlias net_highlight -packet highlight2_red -display $display_object
dr::createPacketAlias net_highlight2 -packet annotate -display $display_object
dr::createPacketAlias ruler -packet ruler_white -display $display_object
dr::createPacketAlias runtime -packet runtime_TrueColorGhost -display $display_object
dr::createPacketAlias stroke -packet stroke_white -display $display_object
dr::createPacketAlias select1 -packet select1_yellow -display $display_object
dr::createPacketAlias select2 -packet select2_red -display $display_object
dr::createPacketAlias select3 -packet select3_blue -display $display_object
dr::createPacketAlias select4 -packet select4_purple -display $display_object
dr::createPacketAlias textAttach -packet annotate5 -display $display_object
dr::createPacketAlias connNavPartial -packet highlight1_yellow -display $display_object
dr::createPacketAlias connNavFull -packet highlight2_red -display $display_object
dr::createPacketAlias connNavNone -packet highlight3_green -display $display_object
# Text Packets definition
dr::createTextPacket active -display $display_object -color TrueColorBright
dr::createTextPacket block -display $display_object -color inherited \
	 -bold yes
dr::createTextPacket blockName -display $display_object -color green \
	 -bold yes
dr::createTextPacket blockPort -display $display_object -color red \
	 -italic yes
dr::createTextPacket deviceName -display $display_object -color green \
	 -bold yes
dr::createTextPacket instanceName -display $display_object -color green
dr::createTextPacket unboundInstanceName -display $display_object -color red \
	 -italic yes -underline yes
dr::createTextPacket instanceBlock -display $display_object -color green
dr::createTextPacket instanceSignal -display $display_object -color cadetBlue
dr::createTextPacket signal -display $display_object -color cadetBlue
dr::createTextPacket comment -display $display_object -color yellow \
	 -italic yes
dr::createTextPacket identifier -display $display_object -color brown
dr::createTextPacket includeFile -display $display_object -color red \
	 -underline yes
dr::createTextPacket keyword -display $display_object -color inherited \
	 -bold yes
dr::createTextPacket directive -display $display_object -color inherited
dr::createTextPacket whitespace -display $display_object -color inherited
dr::createTextPacket dspfNet -display $display_object -color red
dr::createTextPacket other -display $display_object -color inherited
dr::createTextPacket annotate -display $display_object -color tan
dr::createTextPacket highlight1 -display $display_object -color black \
	 -backgroundColor yellow
dr::createTextPacket highlight2 -display $display_object -color black \
	 -backgroundColor red
dr::createTextPacket highlight3 -display $display_object -color black \
	 -backgroundColor green
dr::createTextPacket highlight4 -display $display_object -color black \
	 -backgroundColor blue
dr::createTextPacket highlight5 -display $display_object -color black \
	 -backgroundColor purple
dr::createTextPacket highlight6 -display $display_object -color black \
	 -backgroundColor cyan
dr::createTextPacket highlight7 -display $display_object -color black \
	 -backgroundColor white
dr::createTextPacket highlight8 -display $display_object -color black \
	 -backgroundColor gold
dr::createTextPacket highlight9 -display $display_object -color black \
	 -backgroundColor maroon
dr::createTextPacket highlight10 -display $display_object -color black \
	 -backgroundColor gray
