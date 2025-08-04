
.subckt saedrvt14_nr2_1 vdd vss vbp vbn x a1 a2
xmi0#2fn1 x a2 vss vbn n08 l=0.014u nf=1 m=1 nfin=2
xmi0#2fn0 x a1 vss vbn n08 l=0.014u nf=1 m=1 nfin=2
xmi0#2fp1 x a1 i0#2fmidp_a_b vbp p08 l=0.014u nf=1 m=1 nfin=3
xmi0#2fp0 i0#2fmidp_a_b a2 vdd vbp p08 l=0.014u nf=1 m=1 nfin=3
.ends saedrvt14_nr2_1
