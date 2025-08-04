
.subckt saedrvt14_sgd_nd2_0p5 a1 a2 vbn vbp vdd vss y
xn1 y a1 net11 vbn n08 l=0.014u nf=1.0 m=1 nfin=3
xm5 net11 a2 vss vbn n08 l=0.014u nf=1.0 m=1 nfin=3
xp2 y a2 vdd vbp p08 l=0.014u nf=1.0 m=1 nfin=3
xm4 y a1 vdd vbp p08 l=0.014u nf=1.0 m=1 nfin=3
.ends saedrvt14_sgd_nd2_0p5
