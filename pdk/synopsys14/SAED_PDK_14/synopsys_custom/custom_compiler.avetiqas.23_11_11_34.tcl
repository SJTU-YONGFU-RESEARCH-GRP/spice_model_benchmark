dm::openLibraryManager
gi::setCurrentIndex {libs} -index {SAED_PDK_32_28} -in [gi::getWindows 2]
gi::setItemSelection {libs} -index {SAED_PDK_32_28} -in [gi::getWindows 2]
gi::setCurrentIndex {cells} -index {nmos3t} -in [gi::getWindows 2]
gi::setItemSelection {cells} -index {nmos3t} -in [gi::getWindows 2]
gi::setCurrentIndex {cells} -index {nmos3t_18} -in [gi::getWindows 2]
gi::setItemSelection {cells} -index {nmos3t_18} -in [gi::getWindows 2]
gi::setCurrentIndex {cells} -index {nmos4t} -in [gi::getWindows 2]
gi::setItemSelection {cells} -index {nmos4t} -in [gi::getWindows 2]
gi::setCurrentIndex {views} -index {symbol} -in [gi::getWindows 2]
gi::setItemSelection {views} -index {symbol} -in [gi::getWindows 2]
gi::executeAction dmOpenRead -in [gi::getWindows 2]
exit
gi::setActiveWindow 2
gi::setActiveWindow 2 -raise true
gi::setActiveWindow 1
gi::setActiveWindow 1 -raise true
