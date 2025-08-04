from ui import *

gui=cvar.uiptr

# Opening APDK Libs
mylibs = ["CNM25TechLib", "SPICE3Lib", "XSpiceLib", "XtendedLib", "ExampleLib"]
nlib = len(mylibs)
libinit = [0 for i in range(nlib)]
for n in range(nlib):
    libinit[n] = library(mylibs[n]) 
    libinit[n].dbOpenLib("./"+mylibs[n])

gui.updateLibBrowser()

