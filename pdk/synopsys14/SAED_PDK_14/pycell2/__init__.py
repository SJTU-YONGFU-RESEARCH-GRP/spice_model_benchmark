from n_fin import *
from pfet import *
#from myinverter import *
#from mynand import *
#from tutorial4 import *
#from diodes import *
from diodes import *
#from rmet import *
from resistor import *
from nfet_15 import *
from nfet_18 import *
from pfet_15 import *
from pfet_18 import *
from nfet_hvt import *
from pfet_hvt import *
from nfet_lvt import *
from pfet_lvt import *
from nfet_slvt import *
from pfet_slvt import *
from nd import *
from pd import *
from nd_esd import *
from pd_esd import *
from nd_TO import *
from pd_TO import *
from ndesd_TO import *
from pdesd_TO import *
from pguardring import *
#from test import *
#from araso import *


def definePcells(lib):
    lib.definePcell(pguardring,"pguardring")
    lib.definePcell(n_fin,"n_fin") 
    #lib.definePcell(test,"test")
    #lib.definePcell(araso,"araso")
    lib.definePcell(pfet,"pfet") 
    lib.definePcell(n_fin_15,"n_fin_15") 
    lib.definePcell(n_fin_18,"n_fin_18") 
    lib.definePcell(p_fin_15,"p_fin_15") 
    lib.definePcell(p_fin_18,"p_fin_18") 
    lib.definePcell(n_fin_hvt,"n_fin_hvt") 
    lib.definePcell(p_fin_hvt,"p_fin_hvt") 
    lib.definePcell(n_fin_lvt,"n_fin_lvt") 
    lib.definePcell(p_fin_lvt,"p_fin_lvt") 
    lib.definePcell(n_fin_slvt,"n_fin_slvt") 
    lib.definePcell(p_fin_slvt,"p_fin_slvt") 
    lib.definePcell(diodes,"diodes")  
    #lib.definePcell(diodes,"diodes") 
    #lib.definePcell(rmet,"rmet")
    lib.definePcell(resistor,"resistor")
    lib.definePcell(nd,"nd")
    lib.definePcell(pd,"pd")
    lib.definePcell(nd_esd,"nd_esd")
    lib.definePcell(pd_esd,"pd_esd")
    lib.definePcell(nd_TO,"nd_TO")
    lib.definePcell(pd_TO,"pd_TO")
    lib.definePcell(ndesd_TO,"ndesd_TO")
    lib.definePcell(pdesd_TO,"pdesd_TO")
    #lib.definePcell(n_fin_ulvt,"nfinulvt") 
    #lib.definePcell(p_fin,"pfin")  
    #lib.definePcell(p_fin_hv,"pfinhv")
    #lib.definePcell(p_fin_lvt,"pfinlvt")
    #lib.definePcell(n_fin_ulvt,"pfinulvt")
    #lib.definePcell(myinverter,"myinverter") 
    #lib.definePcell(mynand,"mynand")
    #lib.definePcell(res,"resistor")
