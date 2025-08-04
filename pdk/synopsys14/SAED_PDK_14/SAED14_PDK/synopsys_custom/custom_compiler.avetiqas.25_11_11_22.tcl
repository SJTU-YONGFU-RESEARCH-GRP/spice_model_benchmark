dm::openLibraryManager
gi::setCurrentIndex {libs} -index {SAED_PDK_14} -in [gi::getWindows 2]
gi::setItemSelection {libs} -index {SAED_PDK_14} -in [gi::getWindows 2]
dm::showNewLibrary -parent 2
gi::setActiveDialog [gi::getDialogs {dmNewLibrary} -parent [gi::getWindows 2]]
db::setAttr geometry -of [gi::getDialogs {dmNewLibrary} -parent [gi::getWindows 2]] -value 445x479+727+296
gi::setCurrentIndex {cells} -index {VIA5Cut} -in [gi::getWindows 2]
gi::setItemSelection {cells} -index {VIA5Cut} -in [gi::getWindows 2]
gi::setField {libName} -value {ttt} -in [gi::getDialogs {dmNewLibrary} -parent [gi::getWindows 2]]
gi::pressButton {ok} -in [gi::getDialogs {dmNewLibrary} -parent [gi::getWindows 2]]
gi::setCurrentIndex {libs} -index {ttt} -in [gi::getWindows 2]
gi::setItemSelection {libs} -index {ttt} -in [gi::getWindows 2]
dm::showNewCell -parent 2
gi::setActiveDialog [gi::getDialogs {dmNewCell} -parent [gi::getWindows 2]]
db::setAttr geometry -of [gi::getDialogs {dmNewCell} -parent [gi::getWindows 2]] -value 448x227+725+422
gi::setField {cellName} -value {tt} -in [gi::getDialogs {dmNewCell} -parent [gi::getWindows 2]]
gi::pressButton {ok} -in [gi::getDialogs {dmNewCell} -parent [gi::getWindows 2]]
gi::setCurrentIndex {cells} -index {tt} -in [gi::getWindows 2]
gi::setItemSelection {cells} -index {tt} -in [gi::getWindows 2]
dm::showNewCellView -parent 2
gi::setActiveDialog [gi::getDialogs {dmNewCellView} -parent [gi::getWindows 2]]
db::setAttr geometry -of [gi::getDialogs {dmNewCellView} -parent [gi::getWindows 2]] -value 588x309+655+381
gi::setField {cellViewName} -value {schematic} -in [gi::getDialogs {dmNewCellView} -parent [gi::getWindows 2]]
gi::pressButton {ok} -in [gi::getDialogs {dmNewCellView} -parent [gi::getWindows 2]]
ise::createInst
gi::setActiveDialog [gi::getDialogs {seCreateInst} -parent [gi::getWindows 3]]
db::setAttr geometry -of [gi::getDialogs {seCreateInst}] -value 359x356+629+295
gi::setField {instMasterLib} -value {SAED_PDK_14} -in [gi::getDialogs {seCreateInst} -parent [gi::getWindows 3]]
db::setAttr geometry -of [gi::getDialogs {seCreateInst}] -value 359x356+629+295
gi::setField {instMasterCell} -value {nfet} -in [gi::getDialogs {seCreateInst} -parent [gi::getWindows 3]]
db::setAttr geometry -of [gi::getDialogs {seCreateInst}] -value 359x586+629+295
gi::setField {instMasterCell} -value {nfet_15} -in [gi::getDialogs {seCreateInst} -parent [gi::getWindows 3]]
db::setAttr geometry -of [gi::getDialogs {seCreateInst}] -value 359x586+629+295
gi::setField {instMasterCell} -value {nfet} -in [gi::getDialogs {seCreateInst} -parent [gi::getWindows 3]]
db::setAttr geometry -of [gi::getDialogs {seCreateInst}] -value 359x586+629+295
de::addPoint {2.9 2.4} -context [db::getNext [de::getContexts -window 3]]
de::abortCommand
de::deselectAll [db::getNext [de::getContexts -window 3]]
de::select [de::getActiveFigure [gi::getWindows 3] -point {3.1 2.3875} -index 0 -intent none]
de::deselectAll [db::getNext [de::getContexts -window 3]]
de::select [de::getActiveFigure [gi::getWindows 3] -point {3.0625 2.35625} -index 0 -intent none]
de::deselectAll [db::getNext [de::getContexts -window 3]]
de::deselectAll [db::getNext [de::getContexts -window 3]]
de::select [de::getActiveFigure [gi::getWindows 3] -point {3.0375 2.36875} -index 0 -intent none]
gi::setActiveWindow 2
gi::setActiveWindow 2 -raise true
gi::executeAction menuPreShow -in [gi::getWindows 2]
gi::executeAction menuPreShow -in [gi::getWindows 2]
gi::executeAction menuPreShow -in [gi::getWindows 2]
gi::executeAction menuPreShow -in [gi::getWindows 2]
gi::executeAction menuPreShow -in [gi::getWindows 2]
gi::executeAction menuPreShow -in [gi::getWindows 2]
gi::executeAction menuPreShow -in [gi::getWindows 2]
gi::executeAction dmOpenParamDefEditor -in [gi::getWindows 2]
gi::setField {libraries} -value {SAED_PDK_14} -in [gi::getWindows 4]
gi::setField {cells} -value {nfet} -in [gi::getWindows 4]
gi::expand {cdfTree} -index {0.0.3,0} -in [gi::getWindows 4]
gi::setCurrentIndex {cdfTree} -index {0.0.3.4,1} -in [gi::getWindows 4]
gi::setItemSelection {cdfTree} -index {0.0.3.4,all} -in [gi::getWindows 4]
gi::setField {cdfTree} -index {0.0.3.4,1} -value {0.014u} -in [gi::getWindows 4]
gi::setCurrentIndex {cdfTree} -index {0.0.3.6,1} -in [gi::getWindows 4]
gi::setItemSelection {cdfTree} -index {0.0.3.6,all} -in [gi::getWindows 4]
gi::setField {cdfTree} -index {0.0.3.6,1} -value {nil} -in [gi::getWindows 4]
gi::executeAction dbParameterEditorSave -in [gi::getWindows 4]
gi::setField {cells} -value {pfet} -in [gi::getWindows 4]
gi::expand {cdfTree} -index {0.0.2,0} -in [gi::getWindows 4]
gi::setCurrentIndex {cdfTree} -index {0.0.2.4,1} -in [gi::getWindows 4]
gi::setItemSelection {cdfTree} -index {0.0.2.4,all} -in [gi::getWindows 4]
gi::setField {cdfTree} -index {0.0.2.4,1} -value {0.014u} -in [gi::getWindows 4]
gi::setCurrentIndex {cdfTree} -index {0.0.2.6,1} -in [gi::getWindows 4]
gi::setItemSelection {cdfTree} -index {0.0.2.6,all} -in [gi::getWindows 4]
gi::setField {cdfTree} -index {0.0.2.6,1} -value {nil} -in [gi::getWindows 4]
gi::executeAction dbParameterEditorSave -in [gi::getWindows 4]
gi::executeAction giCloseWindow -in [gi::getWindows 4]
gi::setActiveWindow 2
gi::setActiveWindow 2 -raise true
gi::setActiveWindow 3
gi::setActiveWindow 3 -raise true
de::deselectAll [db::getNext [de::getContexts -window 3]]
de::select [de::getActiveFigure [gi::getWindows 3] -point {3.1 2.35} -index 0 -intent none]
de::deselectAll [db::getNext [de::getContexts -window 3]]
de::deselectAll [db::getNext [de::getContexts -window 3]]
de::select [de::getActiveFigure [gi::getWindows 3] -point {2.90625 2.38125} -index 0 -intent none]
ise::delete
ise::createInst
gi::setActiveDialog [gi::getDialogs {seCreateInst} -parent [gi::getWindows 3]]
db::setAttr geometry -of [gi::getDialogs {seCreateInst}] -value 359x586+629+295
de::abortCommand -context [db::getNext [de::getContexts -window 3]]
gi::executeAction giCloseWindow -in [gi::getWindows 3]
gi::setActiveWindow 2
gi::setActiveWindow 2 -raise true
exit
gi::setActiveWindow 2
gi::setActiveWindow 2 -raise true
gi::setActiveWindow 1
gi::setActiveWindow 1 -raise true
