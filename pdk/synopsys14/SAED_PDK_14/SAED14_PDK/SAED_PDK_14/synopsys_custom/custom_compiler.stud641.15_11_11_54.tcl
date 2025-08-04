dm::openLibraryManager
gi::sortItems {libs} -column {Libraries} -order {descending} -in [gi::getWindows 2]
gi::sortItems {libs} -column {Libraries} -order {ascending} -in [gi::getWindows 2]
exit
gi::setActiveWindow 1
gi::setActiveWindow 1 -raise true
