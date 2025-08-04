dm::openLibraryManager
gi::setCurrentIndex {libs} -index {SAED_PDK_14} -in [gi::getWindows 2]
gi::setItemSelection {libs} -index {SAED_PDK_14} -in [gi::getWindows 2]
db::setAttr geometry -of [gi::getFrames 1] -value 1040x824+753+250
db::setAttr geometry -of [gi::getFrames 1] -value 1040x824+795+321
gi::setCurrentIndex {cells} -index {pfet} -in [gi::getWindows 2]
gi::setItemSelection {cells} -index {pfet} -in [gi::getWindows 2]
gi::setCurrentIndex {views} -index {ivpcell} -in [gi::getWindows 2]
gi::setItemSelection {views} -index {ivpcell} -in [gi::getWindows 2]
gi::executeAction dmOpen -in [gi::getWindows 2]
de::zoom -window [gi::getWindows 3] -factor 2.0 -center {0.004 -0.012}
de::zoom -window [gi::getWindows 3] -factor 0.5 -center {0.004 -0.007}
de::zoom -window [gi::getWindows 3] -factor 0.5 -center {0.006 0.006}
de::zoom -window [gi::getWindows 3] -factor 0.5 -center {0.006 0.006}
de::zoom -window [gi::getWindows 3] -factor 0.5 -center {0.007 0.006}
de::zoom -window [gi::getWindows 3] -factor 2.0 -center {0.086 0.06}
de::zoom -window [gi::getWindows 3] -factor 2.0 -center {0.086 0.06}
de::zoom -window [gi::getWindows 3] -factor 2.0 -center {0.086 0.06}
de::zoom -window [gi::getWindows 3] -factor 0.5 -center {0.086 0.06}
de::zoom -window [gi::getWindows 3] -factor 0.5 -center {0.08 0.051}
gi::setActiveWindow 2
gi::setActiveWindow 2 -raise true
gi::setCurrentIndex {cells} -index {pfet_lvt} -in [gi::getWindows 2]
gi::setItemSelection {cells} -index {pfet_lvt} -in [gi::getWindows 2]
gi::setCurrentIndex {views} -index {ivpcell} -in [gi::getWindows 2]
gi::setItemSelection {views} -index {ivpcell} -in [gi::getWindows 2]
gi::executeAction dmOpen -in [gi::getWindows 2]
de::zoom -window [gi::getWindows 4] -factor 2.0 -center {0.004 0.007}
de::zoom -window [gi::getWindows 4] -factor 2.0 -center {-0.003 0.002}
de::zoom -window [gi::getWindows 4] -factor 2.0 -center {-0.001 0}
de::zoom -window [gi::getWindows 4] -factor 0.5 -center {0.001 0}
de::zoom -window [gi::getWindows 4] -factor 0.5 -center {0.001 0}
de::zoom -window [gi::getWindows 4] -factor 0.5 -center {0.001 0}
de::zoom -window [gi::getWindows 4] -factor 0.5 -center {0.002 0}
de::zoom -window [gi::getWindows 4] -factor 0.5 -center {0.021 0.002}
de::zoom -window [gi::getWindows 4] -factor 0.5 -center {0.022 0.001}
de::zoom -window [gi::getWindows 4] -factor 2.0 -center {0.098 -0.011}
de::zoom -window [gi::getWindows 4] -factor 2.0 -center {0.11 -0.013}
de::fit -window 4 -fitView true
gi::executeAction giCloseWindow -in [gi::getWindows 4]
gi::setActiveWindow 2
gi::setActiveWindow 2 -raise true
gi::setCurrentIndex {views} -index {layout} -in [gi::getWindows 2]
gi::setItemSelection {views} -index {layout} -in [gi::getWindows 2]
gi::executeAction dmOpen -in [gi::getWindows 2]
dr::showDisplayResourceEditor -parent 5
gi::executeAction drLoad -in [gi::getWindows 6]
gi::executeAction giCloseWindow -in [gi::getWindows 6]
gi::setActiveWindow 5
gi::setActiveWindow 5 -raise true
de::zoom -window [gi::getWindows 5] -factor 0.5 -center {0.135 0.05}
de::zoom -window [gi::getWindows 5] -factor 2.0 -center {0.142 0.134}
de::zoom -window [gi::getWindows 5] -factor 0.5 -center {0.145 0.018}
de::zoom -window [gi::getWindows 5] -factor 0.5 -center {0.146 0.017}
de::zoom -window [gi::getWindows 5] -factor 2.0 -center {0.145 0.017}
de::zoom -window [gi::getWindows 5] -factor 2.0 -center {0.238 -0.098}
de::zoom -window [gi::getWindows 5] -factor 0.5 -center {0.036 -0.031}
de::zoom -window [gi::getWindows 5] -factor 2.0 -center {-0.074 0.063}
gi::setActiveWindow 2
gi::setActiveWindow 2 -raise true
gi::setCurrentIndex {views} -index {ivpcell} -in [gi::getWindows 2]
gi::setItemSelection {views} -index {ivpcell} -in [gi::getWindows 2]
gi::setCurrentIndex {cells} -index {rpoly} -in [gi::getWindows 2]
gi::setItemSelection {cells} -index {rpoly} -in [gi::getWindows 2]
gi::setCurrentIndex {views} -index {layout} -in [gi::getWindows 2]
gi::setItemSelection {views} -index {layout} -in [gi::getWindows 2]
gi::executeAction dmOpen -in [gi::getWindows 2]
gi::setActiveDialog [gi::getDialogs {leMissingReferences} -parent [gi::getWindows 7]]
gi::pressButton {ok} -in [gi::getDialogs {leMissingReferences} -parent [gi::getWindows 7]]
de::zoom -window [gi::getWindows 7] -factor 0.5 -center {0.266 0.193}
de::zoom -window [gi::getWindows 7] -factor 0.5 -center {0.266 0.193}
de::zoom -window [gi::getWindows 7] -factor 2.0 -center {0.265 0.192}
gi::executeAction giCloseWindow -in [gi::getWindows 7]
gi::setActiveWindow 2
gi::setActiveWindow 2 -raise true
gi::setCurrentIndex {views} -index {ivpcell} -in [gi::getWindows 2]
gi::setItemSelection {views} -index {ivpcell} -in [gi::getWindows 2]
gi::executeAction dmOpen -in [gi::getWindows 2]
de::zoom -window [gi::getWindows 8] -factor 0.5 -center {0.019 0.01}
de::zoom -window [gi::getWindows 8] -factor 2.0 -center {0.02 0.009}
de::zoom -window [gi::getWindows 8] -factor 2.0 -center {0.02 0.009}
exit
gi::setActiveWindow 2
gi::setActiveWindow 2 -raise true
gi::setActiveWindow 1
gi::setActiveWindow 1 -raise true
