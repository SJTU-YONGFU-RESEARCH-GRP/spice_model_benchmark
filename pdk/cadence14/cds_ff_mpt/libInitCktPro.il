
/* The following lines register various objects of the library "cds_ff_mpt", essentially for the use of
   the Circuit Prospector assistant in VSE XL.
   This file should be moved to the directory of that library and loaded by the respective "libInit.il" file.*/

when( isCallable('ciRegisterDevice)
  ciRegisterDevice("nfin" append(ciGetDeviceNames("nfin") '(
                          '("cds_ff_mpt" "n1svt" nil)
                          '("cds_ff_mpt" "n1hvt" nil)
                          '("cds_ff_mpt" "n1lvt" nil)
                          '("cds_ff_mpt" "n2svt" nil)
  )))
  ciRegisterDevice("pfin" append(ciGetDeviceNames("pfin") '(
                          '("cds_ff_mpt" "p1svt" nil)
                          '("cds_ff_mpt" "p1hvt" nil)
                          '("cds_ff_mpt" "p1lvt" nil)
                          '("cds_ff_mpt" "p2svt" nil)
  )))
  ciRegisterDevice("nfet" append(ciGetDeviceNames("nfet") '(
  )))
  ciRegisterDevice("pfet" append(ciGetDeviceNames("pfet") '(
  )))
  ciRegisterDevice("npn" append(ciGetDeviceNames("npn") '(
  )))
  ciRegisterDevice("pmoscap" append(ciGetDeviceNames("pmoscap") '(
  )))
  ciRegisterDevice("npn" append(ciGetDeviceNames("npn") '(
                          '("cds_ff_mpt" "npn" nil)
  )))
  ciRegisterDevice("npn" append(ciGetDeviceNames("pnp") '(
  )))
  ciRegisterDevice("diode" append(ciGetDeviceNames("diode") '(
                          '("cds_ff_mpt" "nd1svt" nil)
                          '("cds_ff_mpt" "nd1hvt" nil)
                          '("cds_ff_mpt" "nd1lvt" nil)
                          '("cds_ff_mpt" "nd2svt" nil)
                          '("cds_ff_mpt" "pd1svt" nil)
                          '("cds_ff_mpt" "pd1hvt" nil)
                          '("cds_ff_mpt" "pd1lvt" nil)
                          '("cds_ff_mpt" "pd2svt" nil)
  )))
  ciRegisterDevice("resistor" append(ciGetDeviceNames("resistor") '(
                          '("cds_ff_mpt" "resm1" nil)
                          '("cds_ff_mpt" "resm10" nil)
                          '("cds_ff_mpt" "resm11" nil)
                          '("cds_ff_mpt" "resm2" nil)
                          '("cds_ff_mpt" "resm3" nil)
                          '("cds_ff_mpt" "resm4" nil)
                          '("cds_ff_mpt" "resm5" nil)
                          '("cds_ff_mpt" "resm6" nil)
                          '("cds_ff_mpt" "resm7" nil)
                          '("cds_ff_mpt" "resmt" nil)
                          '("cds_ff_mpt" "rsnp" nil)
                          '("cds_ff_mpt" "rnsnp" nil)
                          '("cds_ff_mpt" "rspp" nil)
                          '("cds_ff_mpt" "rnspp" nil)
  )))
  ciRegisterDevice("capacitor" append(ciGetDeviceNames("capacitor") '(
                          '("cds_ff_mpt" "mim" nil)
  )))
  ciRegisterDevice("inductor" append(ciGetDeviceNames("inductor") '(
  )))
  ciRegisterDevice("cpfShort" append(ciGetDeviceNames("cpfShort") '(
  )))
  ciRegisterDevice("standardCell" append(ciGetDeviceNames("standardCell") '(
  )))
  ciRegisterDevice("fet"     append(ciGetDeviceNames("nfin")     ciGetDeviceNames("pfin")))
  ciRegisterDevice("moscap"  append(ciGetDeviceNames("nmoscap")  ciGetDeviceNames("pmoscap")))
  ciRegisterDevice("bjt"     append(ciGetDeviceNames("npn")      ciGetDeviceNames("pnp")))
  ciRegisterDevice("passive" append(ciGetDeviceNames("resistor") ciGetDeviceNames("capacitor")))
  ciRegisterDevice("passive" append(ciGetDeviceNames("passive")  ciGetDeviceNames("inductor")))

  ciMapParam("numFins"    	append(ciGetParamMapping("numFins")
	'( "nfin" )))  
  ciMapParam("width"    	append(ciGetParamMapping("width")
	'( "w" )))  
  ciMapParam("length"    	append(ciGetParamMapping("length")
	'( "l" )))  
  ciMapParam("mFactor"    	append(ciGetParamMapping("mFactor")
	'( "m" )))  
  ciMapParam("fingerCount"    	append(ciGetParamMapping("fingerCount")
	'( "nf" )))  
  ciMapParam("resValue"    	append(ciGetParamMapping("resValue")
	'( "r" )))  
  ciMapParam("capValue"    	append(ciGetParamMapping("capValue")
	'( "c" )))  
  ciMapParam("cpfShortParamsForEqNets"    	append(ciGetParamMapping("cpfShortParamsForEqNets")
	'( )))  
  ciMapParam("fetParamListForMatching"    	append(ciGetParamMapping("fetParamListForMatching")
	'( "model" "nfin" "l" "nf" "m" )))  
  ciMapParam("resistorParamListForMatching"    	append(ciGetParamMapping("resistorParamListForMatching")
	'( "model" "w" "l" "r" )))  
  ciMapParam("capacitorParamListForMatching"    	append(ciGetParamMapping("capacitorParamListForMatching")
	'( "model" "w" "l" "c" "m" )))  

  ciMapTerm("gate"      	append(ciGetTermNames("gate")     	'( "G" )))  
  ciMapTerm("source"      	append(ciGetTermNames("source")     	'( "S" )))  
  ciMapTerm("drain"      	append(ciGetTermNames("drain")     	'( "D" )))  
  ciMapTerm("body"      	append(ciGetTermNames("body")     	'( "B" )))  
  ciMapTerm("base"      	append(ciGetTermNames("base")     	'( "B" )))  
  ciMapTerm("emitter"      	append(ciGetTermNames("emitter")     	'( "E" )))  
  ciMapTerm("collector"      	append(ciGetTermNames("collector")     	'( "C" )))  
  ciMapTerm("plus"              append(ciGetTermNames("plus")           '( "PLUS" )))
  ciMapTerm("minus"             append(ciGetTermNames("minus")          '( "MINUS" )))
) ; when
