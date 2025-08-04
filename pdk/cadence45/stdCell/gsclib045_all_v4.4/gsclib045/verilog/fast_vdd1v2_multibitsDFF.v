// File Version: 130312_1256
// Verilog for library /lan/flow/t1u1/peider/dev1/WORK/zambezi45/LPMS_WS/multibitsDFF_Char_flows/_v_update/verilog/fast_vdd1v2_multibitsDFF created by Liberate 12.1 on Tue Mar 12 12:56:20 PDT 2013 for SDF version 2.1
//
// Conformal-LEC: Version 12.10-p100 (07-Nov-2012) (64 bit executable)
//
module SPDFF4RX2_STATETABLE_UDP1(CK, D, SI, SE, RN, IQN, IQ);
input  CK, D, SI, SE, RN, IQN;
output IQ;
wire  N$5, N$4, N$3, N$2, N$1, CK, D, SI, SE, RN, IQN, IQ;
  not U$2(N$5, SE);
  and U$3(N$4, D, N$5);
  and U$4(N$3, SI, SE);
  or U$5(N$2, N$3, N$4);
  not U$6(N$1, RN);
  _HDFF_verplex U$1(.Q(IQ), .QN( ), .S(1'b0), .R(N$1), .CK(CK), .D(N$2));
endmodule

module SPDFF4RX2_STATETABLE1(IQ, IQN, CK, D, SI, SE, RN);
input  CK, D, SI, SE, RN;
output IQ, IQN;
wire  \udp1/N$1 , \udp1/N$2 , \udp1/N$3 , \udp1/N$4 , \udp1/N$5 , IQ, IQN, CK, D, 
    SI, SE, RN;
  _HDFF_verplex \udp1/U$1 (.Q(IQ), .QN( ), .S(1'b0), .R(\udp1/N$1 ), .CK(CK), .D(
    \udp1/N$2 ));
  not U$0(\udp1/N$1 , RN);
  or U$1(\udp1/N$2 , \udp1/N$3 , \udp1/N$4 );
  and U$2(\udp1/N$3 , SI, SE);
  and U$3(\udp1/N$4 , D, \udp1/N$5 );
  not U$4(\udp1/N$5 , SE);
  not U$5(IQN, IQ);
endmodule

module SPDFF4RX2(Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N, D1, D2, D3, D4, SE, SI1, 
    SI2, SI3, SI4, RN, CK);
input  D1, D2, D3, D4, SE, SI1, SI2, SI3, SI4, RN, CK;
output Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N;
wire  Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N, D1, D2, D3, D4, SE, SI1, SI2, SI3, SI4, 
    RN, CK;
  SPDFF4RX2_STATETABLE1 SPDFF4RX2_STATETABLE1_$U1(.IQ(Q1), .IQN(Q1N), .CK(CK),
     .D(D1), .SI(SI1), .SE(SE), .RN(RN));
  SPDFF4RX2_STATETABLE1 SPDFF4RX2_STATETABLE1_$U2(.IQ(Q2), .IQN(Q2N), .CK(CK),
     .D(D2), .SI(SI2), .SE(SE), .RN(RN));
  SPDFF4RX2_STATETABLE1 SPDFF4RX2_STATETABLE1_$U3(.IQ(Q3), .IQN(Q3N), .CK(CK),
     .D(D3), .SI(SI3), .SE(SE), .RN(RN));
  SPDFF4RX2_STATETABLE1 SPDFF4RX2_STATETABLE1_$U4(.IQ(Q4), .IQN(Q4N), .CK(CK),
     .D(D4), .SI(SI4), .SE(SE), .RN(RN));

	// Section written by Liberate 12.1
	reg notifier;
	specify
		(negedge RN => (Q1+:1'b0)) = 0;
		(posedge CK => (Q1:CK)) = 0;
		(negedge RN => (Q2+:1'b0)) = 0;
		(posedge CK => (Q2:CK)) = 0;
		(negedge RN => (Q3+:1'b0)) = 0;
		(posedge CK => (Q3:CK)) = 0;
		(negedge RN => (Q4+:1'b0)) = 0;
		(posedge CK => (Q4:CK)) = 0;
		(negedge RN => (Q1N-:1'b1)) = 0;
		(posedge CK => (Q1N:CK)) = 0;
		(negedge RN => (Q2N-:1'b1)) = 0;
		(posedge CK => (Q2N:CK)) = 0;
		(negedge RN => (Q3N-:1'b1)) = 0;
		(posedge CK => (Q3N:CK)) = 0;
		(negedge RN => (Q4N-:1'b1)) = 0;
		(posedge CK => (Q4N:CK)) = 0;
		$setuphold (posedge CK, posedge D1, 0, 0, notifier);
		$setuphold (posedge CK, negedge D1, 0, 0, notifier);
		$setuphold (posedge CK, posedge D2, 0, 0, notifier);
		$setuphold (posedge CK, negedge D2, 0, 0, notifier);
		$setuphold (posedge CK, posedge D3, 0, 0, notifier);
		$setuphold (posedge CK, negedge D3, 0, 0, notifier);
		$setuphold (posedge CK, posedge D4, 0, 0, notifier);
		$setuphold (posedge CK, negedge D4, 0, 0, notifier);
		$setuphold (posedge CK, posedge SE, 0, 0, notifier);
		$setuphold (posedge CK, negedge SE, 0, 0, notifier);
		$setuphold (posedge CK, posedge SI1, 0, 0, notifier);
		$setuphold (posedge CK, negedge SI1, 0, 0, notifier);
		$setuphold (posedge CK, posedge SI2, 0, 0, notifier);
		$setuphold (posedge CK, negedge SI2, 0, 0, notifier);
		$setuphold (posedge CK, posedge SI3, 0, 0, notifier);
		$setuphold (posedge CK, negedge SI3, 0, 0, notifier);
		$setuphold (posedge CK, posedge SI4, 0, 0, notifier);
		$setuphold (posedge CK, negedge SI4, 0, 0, notifier);
		$recovery (posedge RN, posedge CK, 0, notifier);
		$hold (posedge CK, posedge RN, 0, notifier);
		$width (negedge RN, 0, 0, notifier);
		$width (posedge CK, 0, 0, notifier);
		$width (negedge CK, 0, 0, notifier);
	endspecify
	// End Section written by Liberate 12.1

endmodule

module SPDFF4RX1_STATETABLE_UDP1(CK, D, SI, SE, RN, IQN, IQ);
input  CK, D, SI, SE, RN, IQN;
output IQ;
wire  N$5, N$4, N$3, N$2, N$1, CK, D, SI, SE, RN, IQN, IQ;
  not U$2(N$5, SE);
  and U$3(N$4, D, N$5);
  and U$4(N$3, SI, SE);
  or U$5(N$2, N$3, N$4);
  not U$6(N$1, RN);
  _HDFF_verplex U$1(.Q(IQ), .QN( ), .S(1'b0), .R(N$1), .CK(CK), .D(N$2));
endmodule

module SPDFF4RX1_STATETABLE1(IQ, IQN, CK, D, SI, SE, RN);
input  CK, D, SI, SE, RN;
output IQ, IQN;
wire  \udp1/N$1 , \udp1/N$2 , \udp1/N$3 , \udp1/N$4 , \udp1/N$5 , IQ, IQN, CK, D, 
    SI, SE, RN;
  _HDFF_verplex \udp1/U$1 (.Q(IQ), .QN( ), .S(1'b0), .R(\udp1/N$1 ), .CK(CK), .D(
    \udp1/N$2 ));
  not U$0(\udp1/N$1 , RN);
  or U$1(\udp1/N$2 , \udp1/N$3 , \udp1/N$4 );
  and U$2(\udp1/N$3 , SI, SE);
  and U$3(\udp1/N$4 , D, \udp1/N$5 );
  not U$4(\udp1/N$5 , SE);
  not U$5(IQN, IQ);
endmodule

module SPDFF4RX1(Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N, D1, D2, D3, D4, SE, SI1, 
    SI2, SI3, SI4, RN, CK);
input  D1, D2, D3, D4, SE, SI1, SI2, SI3, SI4, RN, CK;
output Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N;
wire  Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N, D1, D2, D3, D4, SE, SI1, SI2, SI3, SI4, 
    RN, CK;
  SPDFF4RX1_STATETABLE1 SPDFF4RX1_STATETABLE1_$U1(.IQ(Q1), .IQN(Q1N), .CK(CK),
     .D(D1), .SI(SI1), .SE(SE), .RN(RN));
  SPDFF4RX1_STATETABLE1 SPDFF4RX1_STATETABLE1_$U2(.IQ(Q2), .IQN(Q2N), .CK(CK),
     .D(D2), .SI(SI2), .SE(SE), .RN(RN));
  SPDFF4RX1_STATETABLE1 SPDFF4RX1_STATETABLE1_$U3(.IQ(Q3), .IQN(Q3N), .CK(CK),
     .D(D3), .SI(SI3), .SE(SE), .RN(RN));
  SPDFF4RX1_STATETABLE1 SPDFF4RX1_STATETABLE1_$U4(.IQ(Q4), .IQN(Q4N), .CK(CK),
     .D(D4), .SI(SI4), .SE(SE), .RN(RN));

	// Section written by Liberate 12.1
	reg notifier;
	specify
		(negedge RN => (Q1+:1'b0)) = 0;
		(posedge CK => (Q1:CK)) = 0;
		(negedge RN => (Q2+:1'b0)) = 0;
		(posedge CK => (Q2:CK)) = 0;
		(negedge RN => (Q3+:1'b0)) = 0;
		(posedge CK => (Q3:CK)) = 0;
		(negedge RN => (Q4+:1'b0)) = 0;
		(posedge CK => (Q4:CK)) = 0;
		(negedge RN => (Q1N-:1'b1)) = 0;
		(posedge CK => (Q1N:CK)) = 0;
		(negedge RN => (Q2N-:1'b1)) = 0;
		(posedge CK => (Q2N:CK)) = 0;
		(negedge RN => (Q3N-:1'b1)) = 0;
		(posedge CK => (Q3N:CK)) = 0;
		(negedge RN => (Q4N-:1'b1)) = 0;
		(posedge CK => (Q4N:CK)) = 0;
		$setuphold (posedge CK, posedge D1, 0, 0, notifier);
		$setuphold (posedge CK, negedge D1, 0, 0, notifier);
		$setuphold (posedge CK, posedge D2, 0, 0, notifier);
		$setuphold (posedge CK, negedge D2, 0, 0, notifier);
		$setuphold (posedge CK, posedge D3, 0, 0, notifier);
		$setuphold (posedge CK, negedge D3, 0, 0, notifier);
		$setuphold (posedge CK, posedge D4, 0, 0, notifier);
		$setuphold (posedge CK, negedge D4, 0, 0, notifier);
		$setuphold (posedge CK, posedge SE, 0, 0, notifier);
		$setuphold (posedge CK, negedge SE, 0, 0, notifier);
		$setuphold (posedge CK, posedge SI1, 0, 0, notifier);
		$setuphold (posedge CK, negedge SI1, 0, 0, notifier);
		$setuphold (posedge CK, posedge SI2, 0, 0, notifier);
		$setuphold (posedge CK, negedge SI2, 0, 0, notifier);
		$setuphold (posedge CK, posedge SI3, 0, 0, notifier);
		$setuphold (posedge CK, negedge SI3, 0, 0, notifier);
		$setuphold (posedge CK, posedge SI4, 0, 0, notifier);
		$setuphold (posedge CK, negedge SI4, 0, 0, notifier);
		$recovery (posedge RN, posedge CK, 0, notifier);
		$hold (posedge CK, posedge RN, 0, notifier);
		$width (negedge RN, 0, 0, notifier);
		$width (posedge CK, 0, 0, notifier);
		$width (negedge CK, 0, 0, notifier);
	endspecify
	// End Section written by Liberate 12.1

endmodule

module SPDFF2RX2_STATETABLE_UDP1(CK, D, SI, SE, RN, IQN, IQ);
input  CK, D, SI, SE, RN, IQN;
output IQ;
wire  N$5, N$4, N$3, N$2, N$1, CK, D, SI, SE, RN, IQN, IQ;
  not U$2(N$5, SE);
  and U$3(N$4, D, N$5);
  and U$4(N$3, SI, SE);
  or U$5(N$2, N$3, N$4);
  not U$6(N$1, RN);
  _HDFF_verplex U$1(.Q(IQ), .QN( ), .S(1'b0), .R(N$1), .CK(CK), .D(N$2));
endmodule

module SPDFF2RX2_STATETABLE1(IQ, IQN, CK, D, SI, SE, RN);
input  CK, D, SI, SE, RN;
output IQ, IQN;
wire  \udp1/N$1 , \udp1/N$2 , \udp1/N$3 , \udp1/N$4 , \udp1/N$5 , IQ, IQN, CK, D, 
    SI, SE, RN;
  _HDFF_verplex \udp1/U$1 (.Q(IQ), .QN( ), .S(1'b0), .R(\udp1/N$1 ), .CK(CK), .D(
    \udp1/N$2 ));
  not U$0(\udp1/N$1 , RN);
  or U$1(\udp1/N$2 , \udp1/N$3 , \udp1/N$4 );
  and U$2(\udp1/N$3 , SI, SE);
  and U$3(\udp1/N$4 , D, \udp1/N$5 );
  not U$4(\udp1/N$5 , SE);
  not U$5(IQN, IQ);
endmodule

module SPDFF2RX2(Q1, Q2, Q1N, Q2N, D1, D2, SE, SI1, SI2, RN, CK);
input  D1, D2, SE, SI1, SI2, RN, CK;
output Q1, Q2, Q1N, Q2N;
wire  Q1, Q2, Q1N, Q2N, D1, D2, SE, SI1, SI2, RN, CK;
  SPDFF2RX2_STATETABLE1 SPDFF2RX2_STATETABLE1_$U1(.IQ(Q1), .IQN(Q1N), .CK(CK),
     .D(D1), .SI(SI1), .SE(SE), .RN(RN));
  SPDFF2RX2_STATETABLE1 SPDFF2RX2_STATETABLE1_$U2(.IQ(Q2), .IQN(Q2N), .CK(CK),
     .D(D2), .SI(SI2), .SE(SE), .RN(RN));

	// Section written by Liberate 12.1
	reg notifier;
	specify
		(negedge RN => (Q1+:1'b0)) = 0;
		(posedge CK => (Q1:CK)) = 0;
		(negedge RN => (Q2+:1'b0)) = 0;
		(posedge CK => (Q2:CK)) = 0;
		(negedge RN => (Q1N-:1'b1)) = 0;
		(posedge CK => (Q1N:CK)) = 0;
		(negedge RN => (Q2N-:1'b1)) = 0;
		(posedge CK => (Q2N:CK)) = 0;
		$setuphold (posedge CK, posedge D1, 0, 0, notifier);
		$setuphold (posedge CK, negedge D1, 0, 0, notifier);
		$setuphold (posedge CK, posedge D2, 0, 0, notifier);
		$setuphold (posedge CK, negedge D2, 0, 0, notifier);
		$setuphold (posedge CK, posedge SE, 0, 0, notifier);
		$setuphold (posedge CK, negedge SE, 0, 0, notifier);
		$setuphold (posedge CK, posedge SI1, 0, 0, notifier);
		$setuphold (posedge CK, negedge SI1, 0, 0, notifier);
		$setuphold (posedge CK, posedge SI2, 0, 0, notifier);
		$setuphold (posedge CK, negedge SI2, 0, 0, notifier);
		$recovery (posedge RN, posedge CK, 0, notifier);
		$hold (posedge CK, posedge RN, 0, notifier);
		$width (negedge RN, 0, 0, notifier);
		$width (posedge CK, 0, 0, notifier);
		$width (negedge CK, 0, 0, notifier);
	endspecify
	// End Section written by Liberate 12.1

endmodule

module SPDFF2RX1_STATETABLE_UDP1(CK, D, SI, SE, RN, IQN, IQ);
input  CK, D, SI, SE, RN, IQN;
output IQ;
wire  N$5, N$4, N$3, N$2, N$1, CK, D, SI, SE, RN, IQN, IQ;
  not U$2(N$5, SE);
  and U$3(N$4, D, N$5);
  and U$4(N$3, SI, SE);
  or U$5(N$2, N$3, N$4);
  not U$6(N$1, RN);
  _HDFF_verplex U$1(.Q(IQ), .QN( ), .S(1'b0), .R(N$1), .CK(CK), .D(N$2));
endmodule

module SPDFF2RX1_STATETABLE1(IQ, IQN, CK, D, SI, SE, RN);
input  CK, D, SI, SE, RN;
output IQ, IQN;
wire  \udp1/N$1 , \udp1/N$2 , \udp1/N$3 , \udp1/N$4 , \udp1/N$5 , IQ, IQN, CK, D, 
    SI, SE, RN;
  _HDFF_verplex \udp1/U$1 (.Q(IQ), .QN( ), .S(1'b0), .R(\udp1/N$1 ), .CK(CK), .D(
    \udp1/N$2 ));
  not U$0(\udp1/N$1 , RN);
  or U$1(\udp1/N$2 , \udp1/N$3 , \udp1/N$4 );
  and U$2(\udp1/N$3 , SI, SE);
  and U$3(\udp1/N$4 , D, \udp1/N$5 );
  not U$4(\udp1/N$5 , SE);
  not U$5(IQN, IQ);
endmodule

module SPDFF2RX1(Q1, Q2, Q1N, Q2N, D1, D2, SE, SI1, SI2, RN, CK);
input  D1, D2, SE, SI1, SI2, RN, CK;
output Q1, Q2, Q1N, Q2N;
wire  Q1, Q2, Q1N, Q2N, D1, D2, SE, SI1, SI2, RN, CK;
  SPDFF2RX1_STATETABLE1 SPDFF2RX1_STATETABLE1_$U1(.IQ(Q1), .IQN(Q1N), .CK(CK),
     .D(D1), .SI(SI1), .SE(SE), .RN(RN));
  SPDFF2RX1_STATETABLE1 SPDFF2RX1_STATETABLE1_$U2(.IQ(Q2), .IQN(Q2N), .CK(CK),
     .D(D2), .SI(SI2), .SE(SE), .RN(RN));

	// Section written by Liberate 12.1
	reg notifier;
	specify
		(negedge RN => (Q1+:1'b0)) = 0;
		(posedge CK => (Q1:CK)) = 0;
		(negedge RN => (Q2+:1'b0)) = 0;
		(posedge CK => (Q2:CK)) = 0;
		(negedge RN => (Q1N-:1'b1)) = 0;
		(posedge CK => (Q1N:CK)) = 0;
		(negedge RN => (Q2N-:1'b1)) = 0;
		(posedge CK => (Q2N:CK)) = 0;
		$setuphold (posedge CK, posedge D1, 0, 0, notifier);
		$setuphold (posedge CK, negedge D1, 0, 0, notifier);
		$setuphold (posedge CK, posedge D2, 0, 0, notifier);
		$setuphold (posedge CK, negedge D2, 0, 0, notifier);
		$setuphold (posedge CK, posedge SE, 0, 0, notifier);
		$setuphold (posedge CK, negedge SE, 0, 0, notifier);
		$setuphold (posedge CK, posedge SI1, 0, 0, notifier);
		$setuphold (posedge CK, negedge SI1, 0, 0, notifier);
		$setuphold (posedge CK, posedge SI2, 0, 0, notifier);
		$setuphold (posedge CK, negedge SI2, 0, 0, notifier);
		$recovery (posedge RN, posedge CK, 0, notifier);
		$hold (posedge CK, posedge RN, 0, notifier);
		$width (negedge RN, 0, 0, notifier);
		$width (posedge CK, 0, 0, notifier);
		$width (negedge CK, 0, 0, notifier);
	endspecify
	// End Section written by Liberate 12.1

endmodule

module SDFF4RX2_STATETABLE_UDP1(CK, D, SI, SE, RN, IQN, IQ);
input  CK, D, SI, SE, RN, IQN;
output IQ;
wire  N$5, N$4, N$3, N$2, N$1, CK, D, SI, SE, RN, IQN, IQ;
  not U$2(N$5, SE);
  and U$3(N$4, D, N$5);
  and U$4(N$3, SI, SE);
  or U$5(N$2, N$3, N$4);
  not U$6(N$1, RN);
  _HDFF_verplex U$1(.Q(IQ), .QN( ), .S(1'b0), .R(N$1), .CK(CK), .D(N$2));
endmodule

module SDFF4RX2_STATETABLE1(IQ, IQN, CK, D, SI, SE, RN);
input  CK, D, SI, SE, RN;
output IQ, IQN;
wire  \udp1/N$1 , \udp1/N$2 , \udp1/N$3 , \udp1/N$4 , \udp1/N$5 , IQ, IQN, CK, D, 
    SI, SE, RN;
  _HDFF_verplex \udp1/U$1 (.Q(IQ), .QN( ), .S(1'b0), .R(\udp1/N$1 ), .CK(CK), .D(
    \udp1/N$2 ));
  not U$0(\udp1/N$1 , RN);
  or U$1(\udp1/N$2 , \udp1/N$3 , \udp1/N$4 );
  and U$2(\udp1/N$3 , SI, SE);
  and U$3(\udp1/N$4 , D, \udp1/N$5 );
  not U$4(\udp1/N$5 , SE);
  not U$5(IQN, IQ);
endmodule

module SDFF4RX2(Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N, D1, D2, D3, D4, SE, SI, RN, 
    CK);
input  D1, D2, D3, D4, SE, SI, RN, CK;
output Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N;
wire  Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N, D1, D2, D3, D4, SE, SI, RN, CK;
  SDFF4RX2_STATETABLE1 SDFF4RX2_STATETABLE1_$U1(.IQ(Q1), .IQN(Q1N), .CK(CK), .D(
    D1), .SI(SI), .SE(SE), .RN(RN));
  SDFF4RX2_STATETABLE1 SDFF4RX2_STATETABLE1_$U2(.IQ(Q2), .IQN(Q2N), .CK(CK), .D(
    D2), .SI(Q1), .SE(SE), .RN(RN));
  SDFF4RX2_STATETABLE1 SDFF4RX2_STATETABLE1_$U3(.IQ(Q3), .IQN(Q3N), .CK(CK), .D(
    D3), .SI(Q2), .SE(SE), .RN(RN));
  SDFF4RX2_STATETABLE1 SDFF4RX2_STATETABLE1_$U4(.IQ(Q4), .IQN(Q4N), .CK(CK), .D(
    D4), .SI(Q3), .SE(SE), .RN(RN));

	// Section written by Liberate 12.1
	reg notifier;
	specify
		(negedge RN => (Q1+:1'b0)) = 0;
		(posedge CK => (Q1:CK)) = 0;
		(negedge RN => (Q2+:1'b0)) = 0;
		(posedge CK => (Q2:CK)) = 0;
		(negedge RN => (Q3+:1'b0)) = 0;
		(posedge CK => (Q3:CK)) = 0;
		(negedge RN => (Q4+:1'b0)) = 0;
		(posedge CK => (Q4:CK)) = 0;
		(negedge RN => (Q1N-:1'b1)) = 0;
		(posedge CK => (Q1N:CK)) = 0;
		(negedge RN => (Q2N-:1'b1)) = 0;
		(posedge CK => (Q2N:CK)) = 0;
		(negedge RN => (Q3N-:1'b1)) = 0;
		(posedge CK => (Q3N:CK)) = 0;
		(negedge RN => (Q4N-:1'b1)) = 0;
		(posedge CK => (Q4N:CK)) = 0;
		$setuphold (posedge CK, posedge D1, 0, 0, notifier);
		$setuphold (posedge CK, negedge D1, 0, 0, notifier);
		$setuphold (posedge CK, posedge D2, 0, 0, notifier);
		$setuphold (posedge CK, negedge D2, 0, 0, notifier);
		$setuphold (posedge CK, posedge D3, 0, 0, notifier);
		$setuphold (posedge CK, negedge D3, 0, 0, notifier);
		$setuphold (posedge CK, posedge D4, 0, 0, notifier);
		$setuphold (posedge CK, negedge D4, 0, 0, notifier);
		$setuphold (posedge CK, posedge SE, 0, 0, notifier);
		$setuphold (posedge CK, negedge SE, 0, 0, notifier);
		$setuphold (posedge CK, posedge SI, 0, 0, notifier);
		$setuphold (posedge CK, negedge SI, 0, 0, notifier);
		$recovery (posedge RN, posedge CK, 0, notifier);
		$hold (posedge CK, posedge RN, 0, notifier);
		$width (negedge RN, 0, 0, notifier);
		$width (posedge CK, 0, 0, notifier);
		$width (negedge CK, 0, 0, notifier);
	endspecify
	// End Section written by Liberate 12.1

endmodule

module SDFF4RX1_STATETABLE_UDP1(CK, D, SI, SE, RN, IQN, IQ);
input  CK, D, SI, SE, RN, IQN;
output IQ;
wire  N$5, N$4, N$3, N$2, N$1, CK, D, SI, SE, RN, IQN, IQ;
  not U$2(N$5, SE);
  and U$3(N$4, D, N$5);
  and U$4(N$3, SI, SE);
  or U$5(N$2, N$3, N$4);
  not U$6(N$1, RN);
  _HDFF_verplex U$1(.Q(IQ), .QN( ), .S(1'b0), .R(N$1), .CK(CK), .D(N$2));
endmodule

module SDFF4RX1_STATETABLE1(IQ, IQN, CK, D, SI, SE, RN);
input  CK, D, SI, SE, RN;
output IQ, IQN;
wire  \udp1/N$1 , \udp1/N$2 , \udp1/N$3 , \udp1/N$4 , \udp1/N$5 , IQ, IQN, CK, D, 
    SI, SE, RN;
  _HDFF_verplex \udp1/U$1 (.Q(IQ), .QN( ), .S(1'b0), .R(\udp1/N$1 ), .CK(CK), .D(
    \udp1/N$2 ));
  not U$0(\udp1/N$1 , RN);
  or U$1(\udp1/N$2 , \udp1/N$3 , \udp1/N$4 );
  and U$2(\udp1/N$3 , SI, SE);
  and U$3(\udp1/N$4 , D, \udp1/N$5 );
  not U$4(\udp1/N$5 , SE);
  not U$5(IQN, IQ);
endmodule

module SDFF4RX1(Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N, D1, D2, D3, D4, SE, SI, RN, 
    CK);
input  D1, D2, D3, D4, SE, SI, RN, CK;
output Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N;
wire  Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N, D1, D2, D3, D4, SE, SI, RN, CK;
  SDFF4RX1_STATETABLE1 SDFF4RX1_STATETABLE1_$U1(.IQ(Q1), .IQN(Q1N), .CK(CK), .D(
    D1), .SI(SI), .SE(SE), .RN(RN));
  SDFF4RX1_STATETABLE1 SDFF4RX1_STATETABLE1_$U2(.IQ(Q2), .IQN(Q2N), .CK(CK), .D(
    D2), .SI(Q1), .SE(SE), .RN(RN));
  SDFF4RX1_STATETABLE1 SDFF4RX1_STATETABLE1_$U3(.IQ(Q3), .IQN(Q3N), .CK(CK), .D(
    D3), .SI(Q2), .SE(SE), .RN(RN));
  SDFF4RX1_STATETABLE1 SDFF4RX1_STATETABLE1_$U4(.IQ(Q4), .IQN(Q4N), .CK(CK), .D(
    D4), .SI(Q3), .SE(SE), .RN(RN));

	// Section written by Liberate 12.1
	reg notifier;
	specify
		(negedge RN => (Q1+:1'b0)) = 0;
		(posedge CK => (Q1:CK)) = 0;
		(negedge RN => (Q2+:1'b0)) = 0;
		(posedge CK => (Q2:CK)) = 0;
		(negedge RN => (Q3+:1'b0)) = 0;
		(posedge CK => (Q3:CK)) = 0;
		(negedge RN => (Q4+:1'b0)) = 0;
		(posedge CK => (Q4:CK)) = 0;
		(negedge RN => (Q1N-:1'b1)) = 0;
		(posedge CK => (Q1N:CK)) = 0;
		(negedge RN => (Q2N-:1'b1)) = 0;
		(posedge CK => (Q2N:CK)) = 0;
		(negedge RN => (Q3N-:1'b1)) = 0;
		(posedge CK => (Q3N:CK)) = 0;
		(negedge RN => (Q4N-:1'b1)) = 0;
		(posedge CK => (Q4N:CK)) = 0;
		$setuphold (posedge CK, posedge D1, 0, 0, notifier);
		$setuphold (posedge CK, negedge D1, 0, 0, notifier);
		$setuphold (posedge CK, posedge D2, 0, 0, notifier);
		$setuphold (posedge CK, negedge D2, 0, 0, notifier);
		$setuphold (posedge CK, posedge D3, 0, 0, notifier);
		$setuphold (posedge CK, negedge D3, 0, 0, notifier);
		$setuphold (posedge CK, posedge D4, 0, 0, notifier);
		$setuphold (posedge CK, negedge D4, 0, 0, notifier);
		$setuphold (posedge CK, posedge SE, 0, 0, notifier);
		$setuphold (posedge CK, negedge SE, 0, 0, notifier);
		$setuphold (posedge CK, posedge SI, 0, 0, notifier);
		$setuphold (posedge CK, negedge SI, 0, 0, notifier);
		$recovery (posedge RN, posedge CK, 0, notifier);
		$hold (posedge CK, posedge RN, 0, notifier);
		$width (negedge RN, 0, 0, notifier);
		$width (posedge CK, 0, 0, notifier);
		$width (negedge CK, 0, 0, notifier);
	endspecify
	// End Section written by Liberate 12.1

endmodule

module SDFF2RX2_STATETABLE_UDP1(CK, D, SI, SE, RN, IQN, IQ);
input  CK, D, SI, SE, RN, IQN;
output IQ;
wire  N$5, N$4, N$3, N$2, N$1, CK, D, SI, SE, RN, IQN, IQ;
  not U$2(N$5, SE);
  and U$3(N$4, D, N$5);
  and U$4(N$3, SI, SE);
  or U$5(N$2, N$3, N$4);
  not U$6(N$1, RN);
  _HDFF_verplex U$1(.Q(IQ), .QN( ), .S(1'b0), .R(N$1), .CK(CK), .D(N$2));
endmodule

module SDFF2RX2_STATETABLE1(IQ, IQN, CK, D, SI, SE, RN);
input  CK, D, SI, SE, RN;
output IQ, IQN;
wire  \udp1/N$1 , \udp1/N$2 , \udp1/N$3 , \udp1/N$4 , \udp1/N$5 , IQ, IQN, CK, D, 
    SI, SE, RN;
  _HDFF_verplex \udp1/U$1 (.Q(IQ), .QN( ), .S(1'b0), .R(\udp1/N$1 ), .CK(CK), .D(
    \udp1/N$2 ));
  not U$0(\udp1/N$1 , RN);
  or U$1(\udp1/N$2 , \udp1/N$3 , \udp1/N$4 );
  and U$2(\udp1/N$3 , SI, SE);
  and U$3(\udp1/N$4 , D, \udp1/N$5 );
  not U$4(\udp1/N$5 , SE);
  not U$5(IQN, IQ);
endmodule

module SDFF2RX2(Q1, Q2, Q1N, Q2N, D1, D2, SE, SI, RN, CK);
input  D1, D2, SE, SI, RN, CK;
output Q1, Q2, Q1N, Q2N;
wire  Q1, Q2, Q1N, Q2N, D1, D2, SE, SI, RN, CK;
  SDFF2RX2_STATETABLE1 SDFF2RX2_STATETABLE1_$U1(.IQ(Q1), .IQN(Q1N), .CK(CK), .D(
    D1), .SI(SI), .SE(SE), .RN(RN));
  SDFF2RX2_STATETABLE1 SDFF2RX2_STATETABLE1_$U2(.IQ(Q2), .IQN(Q2N), .CK(CK), .D(
    D2), .SI(Q1), .SE(SE), .RN(RN));

	// Section written by Liberate 12.1
	reg notifier;
	specify
		(negedge RN => (Q1+:1'b0)) = 0;
		(posedge CK => (Q1:CK)) = 0;
		(negedge RN => (Q2+:1'b0)) = 0;
		(posedge CK => (Q2:CK)) = 0;
		(negedge RN => (Q1N-:1'b1)) = 0;
		(posedge CK => (Q1N:CK)) = 0;
		(negedge RN => (Q2N-:1'b1)) = 0;
		(posedge CK => (Q2N:CK)) = 0;
		$setuphold (posedge CK, posedge D1, 0, 0, notifier);
		$setuphold (posedge CK, negedge D1, 0, 0, notifier);
		$setuphold (posedge CK, posedge D2, 0, 0, notifier);
		$setuphold (posedge CK, negedge D2, 0, 0, notifier);
		$setuphold (posedge CK, posedge SE, 0, 0, notifier);
		$setuphold (posedge CK, negedge SE, 0, 0, notifier);
		$setuphold (posedge CK, posedge SI, 0, 0, notifier);
		$setuphold (posedge CK, negedge SI, 0, 0, notifier);
		$recovery (posedge RN, posedge CK, 0, notifier);
		$hold (posedge CK, posedge RN, 0, notifier);
		$width (negedge RN, 0, 0, notifier);
		$width (posedge CK, 0, 0, notifier);
		$width (negedge CK, 0, 0, notifier);
	endspecify
	// End Section written by Liberate 12.1

endmodule

module SDFF2RX1_STATETABLE_UDP1(CK, D, SI, SE, RN, IQN, IQ);
input  CK, D, SI, SE, RN, IQN;
output IQ;
wire  N$5, N$4, N$3, N$2, N$1, CK, D, SI, SE, RN, IQN, IQ;
  not U$2(N$5, SE);
  and U$3(N$4, D, N$5);
  and U$4(N$3, SI, SE);
  or U$5(N$2, N$3, N$4);
  not U$6(N$1, RN);
  _HDFF_verplex U$1(.Q(IQ), .QN( ), .S(1'b0), .R(N$1), .CK(CK), .D(N$2));
endmodule

module SDFF2RX1_STATETABLE1(IQ, IQN, CK, D, SI, SE, RN);
input  CK, D, SI, SE, RN;
output IQ, IQN;
wire  \udp1/N$1 , \udp1/N$2 , \udp1/N$3 , \udp1/N$4 , \udp1/N$5 , IQ, IQN, CK, D, 
    SI, SE, RN;
  _HDFF_verplex \udp1/U$1 (.Q(IQ), .QN( ), .S(1'b0), .R(\udp1/N$1 ), .CK(CK), .D(
    \udp1/N$2 ));
  not U$0(\udp1/N$1 , RN);
  or U$1(\udp1/N$2 , \udp1/N$3 , \udp1/N$4 );
  and U$2(\udp1/N$3 , SI, SE);
  and U$3(\udp1/N$4 , D, \udp1/N$5 );
  not U$4(\udp1/N$5 , SE);
  not U$5(IQN, IQ);
endmodule

module SDFF2RX1(Q1, Q2, Q1N, Q2N, D1, D2, SE, SI, RN, CK);
input  D1, D2, SE, SI, RN, CK;
output Q1, Q2, Q1N, Q2N;
wire  Q1, Q2, Q1N, Q2N, D1, D2, SE, SI, RN, CK;
  SDFF2RX1_STATETABLE1 SDFF2RX1_STATETABLE1_$U1(.IQ(Q1), .IQN(Q1N), .CK(CK), .D(
    D1), .SI(SI), .SE(SE), .RN(RN));
  SDFF2RX1_STATETABLE1 SDFF2RX1_STATETABLE1_$U2(.IQ(Q2), .IQN(Q2N), .CK(CK), .D(
    D2), .SI(Q1), .SE(SE), .RN(RN));

	// Section written by Liberate 12.1
	reg notifier;
	specify
		(negedge RN => (Q1+:1'b0)) = 0;
		(posedge CK => (Q1:CK)) = 0;
		(negedge RN => (Q2+:1'b0)) = 0;
		(posedge CK => (Q2:CK)) = 0;
		(negedge RN => (Q1N-:1'b1)) = 0;
		(posedge CK => (Q1N:CK)) = 0;
		(negedge RN => (Q2N-:1'b1)) = 0;
		(posedge CK => (Q2N:CK)) = 0;
		$setuphold (posedge CK, posedge D1, 0, 0, notifier);
		$setuphold (posedge CK, negedge D1, 0, 0, notifier);
		$setuphold (posedge CK, posedge D2, 0, 0, notifier);
		$setuphold (posedge CK, negedge D2, 0, 0, notifier);
		$setuphold (posedge CK, posedge SE, 0, 0, notifier);
		$setuphold (posedge CK, negedge SE, 0, 0, notifier);
		$setuphold (posedge CK, posedge SI, 0, 0, notifier);
		$setuphold (posedge CK, negedge SI, 0, 0, notifier);
		$recovery (posedge RN, posedge CK, 0, notifier);
		$hold (posedge CK, posedge RN, 0, notifier);
		$width (negedge RN, 0, 0, notifier);
		$width (posedge CK, 0, 0, notifier);
		$width (negedge CK, 0, 0, notifier);
	endspecify
	// End Section written by Liberate 12.1

endmodule

module DFF4X2(Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N, D1, D2, D3, D4, CK);
input  D1, D2, D3, D4, CK;
output Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N;
wire  Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N, D1, D2, D3, D4, CK;
wire   [3:0] IQ;
wire   [3:0] IQN;
  _HDFF_verplex U$1(.Q(IQ[0]), .QN(IQN[0]), .S(1'b0), .R(1'b0), .CK(CK), .D(D1));
  _HDFF_verplex U$2(.Q(IQ[1]), .QN(IQN[1]), .S(1'b0), .R(1'b0), .CK(CK), .D(D2));
  _HDFF_verplex U$3(.Q(IQ[2]), .QN(IQN[2]), .S(1'b0), .R(1'b0), .CK(CK), .D(D3));
  _HDFF_verplex U$4(.Q(IQ[3]), .QN(IQN[3]), .S(1'b0), .R(1'b0), .CK(CK), .D(D4));
  buf U$5(Q1, IQ[0]);
  buf U$6(Q2, IQ[1]);
  buf U$7(Q3, IQ[2]);
  buf U$8(Q4, IQ[3]);
  buf U$9(Q1N, IQN[0]);
  buf U$10(Q2N, IQN[1]);
  buf U$11(Q3N, IQN[2]);
  buf U$12(Q4N, IQN[3]);

	// Section written by Liberate 12.1
	reg notifier;
	specify
		(posedge CK => (Q1+:D1)) = 0;
		(posedge CK => (Q2+:D2)) = 0;
		(posedge CK => (Q3+:D3)) = 0;
		(posedge CK => (Q4+:D4)) = 0;
		(posedge CK => (Q1N-:D1)) = 0;
		(posedge CK => (Q2N-:D2)) = 0;
		(posedge CK => (Q3N-:D3)) = 0;
		(posedge CK => (Q4N-:D4)) = 0;
		$setuphold (posedge CK, posedge D1, 0, 0, notifier);
		$setuphold (posedge CK, negedge D1, 0, 0, notifier);
		$setuphold (posedge CK, posedge D2, 0, 0, notifier);
		$setuphold (posedge CK, negedge D2, 0, 0, notifier);
		$setuphold (posedge CK, posedge D3, 0, 0, notifier);
		$setuphold (posedge CK, negedge D3, 0, 0, notifier);
		$setuphold (posedge CK, posedge D4, 0, 0, notifier);
		$setuphold (posedge CK, negedge D4, 0, 0, notifier);
		$width (posedge CK, 0, 0, notifier);
		$width (negedge CK, 0, 0, notifier);
	endspecify
	// End Section written by Liberate 12.1

endmodule

module DFF4X1(Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N, D1, D2, D3, D4, CK);
input  D1, D2, D3, D4, CK;
output Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N;
wire  Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N, D1, D2, D3, D4, CK;
wire   [3:0] IQ;
wire   [3:0] IQN;
  _HDFF_verplex U$1(.Q(IQ[0]), .QN(IQN[0]), .S(1'b0), .R(1'b0), .CK(CK), .D(D1));
  _HDFF_verplex U$2(.Q(IQ[1]), .QN(IQN[1]), .S(1'b0), .R(1'b0), .CK(CK), .D(D2));
  _HDFF_verplex U$3(.Q(IQ[2]), .QN(IQN[2]), .S(1'b0), .R(1'b0), .CK(CK), .D(D3));
  _HDFF_verplex U$4(.Q(IQ[3]), .QN(IQN[3]), .S(1'b0), .R(1'b0), .CK(CK), .D(D4));
  buf U$5(Q1, IQ[0]);
  buf U$6(Q2, IQ[1]);
  buf U$7(Q3, IQ[2]);
  buf U$8(Q4, IQ[3]);
  buf U$9(Q1N, IQN[0]);
  buf U$10(Q2N, IQN[1]);
  buf U$11(Q3N, IQN[2]);
  buf U$12(Q4N, IQN[3]);

	// Section written by Liberate 12.1
	reg notifier;
	specify
		(posedge CK => (Q1+:D1)) = 0;
		(posedge CK => (Q2+:D2)) = 0;
		(posedge CK => (Q3+:D3)) = 0;
		(posedge CK => (Q4+:D4)) = 0;
		(posedge CK => (Q1N-:D1)) = 0;
		(posedge CK => (Q2N-:D2)) = 0;
		(posedge CK => (Q3N-:D3)) = 0;
		(posedge CK => (Q4N-:D4)) = 0;
		$setuphold (posedge CK, posedge D1, 0, 0, notifier);
		$setuphold (posedge CK, negedge D1, 0, 0, notifier);
		$setuphold (posedge CK, posedge D2, 0, 0, notifier);
		$setuphold (posedge CK, negedge D2, 0, 0, notifier);
		$setuphold (posedge CK, posedge D3, 0, 0, notifier);
		$setuphold (posedge CK, negedge D3, 0, 0, notifier);
		$setuphold (posedge CK, posedge D4, 0, 0, notifier);
		$setuphold (posedge CK, negedge D4, 0, 0, notifier);
		$width (posedge CK, 0, 0, notifier);
		$width (negedge CK, 0, 0, notifier);
	endspecify
	// End Section written by Liberate 12.1

endmodule

module DFF4RX2(Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N, D1, D2, D3, D4, RN, CK);
input  D1, D2, D3, D4, RN, CK;
output Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N;
wire  Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N, D1, D2, D3, D4, RN, CK, n$1, n$2, n$3, 
    n$4;
wire   [3:0] IQ;
wire   [3:0] IQN;
  _HDFF_verplex U$1(.Q(IQ[0]), .QN(IQN[0]), .S(1'b0), .R(n$1), .CK(CK), .D(D1));
  _HDFF_verplex U$2(.Q(IQ[1]), .QN(IQN[1]), .S(1'b0), .R(n$2), .CK(CK), .D(D2));
  _HDFF_verplex U$3(.Q(IQ[2]), .QN(IQN[2]), .S(1'b0), .R(n$3), .CK(CK), .D(D3));
  _HDFF_verplex U$4(.Q(IQ[3]), .QN(IQN[3]), .S(1'b0), .R(n$4), .CK(CK), .D(D4));
  buf U$5(Q1, IQ[0]);
  buf U$6(Q2, IQ[1]);
  buf U$7(Q3, IQ[2]);
  buf U$8(Q4, IQ[3]);
  buf U$9(Q1N, IQN[0]);
  buf U$10(Q2N, IQN[1]);
  buf U$11(Q3N, IQN[2]);
  buf U$12(Q4N, IQN[3]);
  not U$13(n$1, RN);
  not U$14(n$2, RN);
  not U$15(n$3, RN);
  not U$16(n$4, RN);

	// Section written by Liberate 12.1
	reg notifier;
	specify
		(negedge RN => (Q1+:1'b0)) = 0;
		(posedge CK => (Q1+:D1)) = 0;
		(negedge RN => (Q2+:1'b0)) = 0;
		(posedge CK => (Q2+:D2)) = 0;
		(negedge RN => (Q3+:1'b0)) = 0;
		(posedge CK => (Q3+:D3)) = 0;
		(negedge RN => (Q4+:1'b0)) = 0;
		(posedge CK => (Q4+:D4)) = 0;
		(negedge RN => (Q1N-:1'b0)) = 0;
		(posedge CK => (Q1N-:D1)) = 0;
		(negedge RN => (Q2N-:1'b0)) = 0;
		(posedge CK => (Q2N-:D2)) = 0;
		(negedge RN => (Q3N-:1'b0)) = 0;
		(posedge CK => (Q3N-:D3)) = 0;
		(negedge RN => (Q4N-:1'b0)) = 0;
		(posedge CK => (Q4N-:D4)) = 0;
		$setuphold (posedge CK, posedge D1, 0, 0, notifier);
		$setuphold (posedge CK, negedge D1, 0, 0, notifier);
		$setuphold (posedge CK, posedge D2, 0, 0, notifier);
		$setuphold (posedge CK, negedge D2, 0, 0, notifier);
		$setuphold (posedge CK, posedge D3, 0, 0, notifier);
		$setuphold (posedge CK, negedge D3, 0, 0, notifier);
		$setuphold (posedge CK, posedge D4, 0, 0, notifier);
		$setuphold (posedge CK, negedge D4, 0, 0, notifier);
		$recovery (posedge RN, posedge CK, 0, notifier);
		$hold (posedge CK, posedge RN, 0, notifier);
		$width (negedge RN, 0, 0, notifier);
		$width (posedge CK, 0, 0, notifier);
		$width (negedge CK, 0, 0, notifier);
	endspecify
	// End Section written by Liberate 12.1

endmodule

module DFF4RX1(Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N, D1, D2, D3, D4, RN, CK);
input  D1, D2, D3, D4, RN, CK;
output Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N;
wire  Q1, Q2, Q3, Q4, Q1N, Q2N, Q3N, Q4N, D1, D2, D3, D4, RN, CK, n$1, n$2, n$3, 
    n$4;
wire   [3:0] IQ;
wire   [3:0] IQN;
  _HDFF_verplex U$1(.Q(IQ[0]), .QN(IQN[0]), .S(1'b0), .R(n$1), .CK(CK), .D(D1));
  _HDFF_verplex U$2(.Q(IQ[1]), .QN(IQN[1]), .S(1'b0), .R(n$2), .CK(CK), .D(D2));
  _HDFF_verplex U$3(.Q(IQ[2]), .QN(IQN[2]), .S(1'b0), .R(n$3), .CK(CK), .D(D3));
  _HDFF_verplex U$4(.Q(IQ[3]), .QN(IQN[3]), .S(1'b0), .R(n$4), .CK(CK), .D(D4));
  buf U$5(Q1, IQ[0]);
  buf U$6(Q2, IQ[1]);
  buf U$7(Q3, IQ[2]);
  buf U$8(Q4, IQ[3]);
  buf U$9(Q1N, IQN[0]);
  buf U$10(Q2N, IQN[1]);
  buf U$11(Q3N, IQN[2]);
  buf U$12(Q4N, IQN[3]);
  not U$13(n$1, RN);
  not U$14(n$2, RN);
  not U$15(n$3, RN);
  not U$16(n$4, RN);

	// Section written by Liberate 12.1
	reg notifier;
	specify
		(negedge RN => (Q1+:1'b0)) = 0;
		(posedge CK => (Q1+:D1)) = 0;
		(negedge RN => (Q2+:1'b0)) = 0;
		(posedge CK => (Q2+:D2)) = 0;
		(negedge RN => (Q3+:1'b0)) = 0;
		(posedge CK => (Q3+:D3)) = 0;
		(negedge RN => (Q4+:1'b0)) = 0;
		(posedge CK => (Q4+:D4)) = 0;
		(negedge RN => (Q1N-:1'b0)) = 0;
		(posedge CK => (Q1N-:D1)) = 0;
		(negedge RN => (Q2N-:1'b0)) = 0;
		(posedge CK => (Q2N-:D2)) = 0;
		(negedge RN => (Q3N-:1'b0)) = 0;
		(posedge CK => (Q3N-:D3)) = 0;
		(negedge RN => (Q4N-:1'b0)) = 0;
		(posedge CK => (Q4N-:D4)) = 0;
		$setuphold (posedge CK, posedge D1, 0, 0, notifier);
		$setuphold (posedge CK, negedge D1, 0, 0, notifier);
		$setuphold (posedge CK, posedge D2, 0, 0, notifier);
		$setuphold (posedge CK, negedge D2, 0, 0, notifier);
		$setuphold (posedge CK, posedge D3, 0, 0, notifier);
		$setuphold (posedge CK, negedge D3, 0, 0, notifier);
		$setuphold (posedge CK, posedge D4, 0, 0, notifier);
		$setuphold (posedge CK, negedge D4, 0, 0, notifier);
		$recovery (posedge RN, posedge CK, 0, notifier);
		$hold (posedge CK, posedge RN, 0, notifier);
		$width (negedge RN, 0, 0, notifier);
		$width (posedge CK, 0, 0, notifier);
		$width (negedge CK, 0, 0, notifier);
	endspecify
	// End Section written by Liberate 12.1

endmodule

module DFF2X2(Q1, Q2, Q1N, Q2N, D1, D2, CK);
input  D1, D2, CK;
output Q1, Q2, Q1N, Q2N;
wire  Q1, Q2, Q1N, Q2N, D1, D2, CK;
wire   [1:0] IQ;
wire   [1:0] IQN;
  _HDFF_verplex U$1(.Q(IQ[0]), .QN(IQN[0]), .S(1'b0), .R(1'b0), .CK(CK), .D(D1));
  _HDFF_verplex U$2(.Q(IQ[1]), .QN(IQN[1]), .S(1'b0), .R(1'b0), .CK(CK), .D(D2));
  buf U$3(Q1, IQ[0]);
  buf U$4(Q2, IQ[1]);
  buf U$5(Q1N, IQN[0]);
  buf U$6(Q2N, IQN[1]);

	// Section written by Liberate 12.1
	reg notifier;
	specify
		(posedge CK => (Q1+:D1)) = 0;
		(posedge CK => (Q2+:D2)) = 0;
		(posedge CK => (Q1N-:D1)) = 0;
		(posedge CK => (Q2N-:D2)) = 0;
		$setuphold (posedge CK, posedge D1, 0, 0, notifier);
		$setuphold (posedge CK, negedge D1, 0, 0, notifier);
		$setuphold (posedge CK, posedge D2, 0, 0, notifier);
		$setuphold (posedge CK, negedge D2, 0, 0, notifier);
		$width (posedge CK, 0, 0, notifier);
		$width (negedge CK, 0, 0, notifier);
	endspecify
	// End Section written by Liberate 12.1

endmodule

module DFF2X1(Q1, Q2, Q1N, Q2N, D1, D2, CK);
input  D1, D2, CK;
output Q1, Q2, Q1N, Q2N;
wire  Q1, Q2, Q1N, Q2N, D1, D2, CK;
wire   [1:0] IQ;
wire   [1:0] IQN;
  _HDFF_verplex U$1(.Q(IQ[0]), .QN(IQN[0]), .S(1'b0), .R(1'b0), .CK(CK), .D(D1));
  _HDFF_verplex U$2(.Q(IQ[1]), .QN(IQN[1]), .S(1'b0), .R(1'b0), .CK(CK), .D(D2));
  buf U$3(Q1, IQ[0]);
  buf U$4(Q2, IQ[1]);
  buf U$5(Q1N, IQN[0]);
  buf U$6(Q2N, IQN[1]);

	// Section written by Liberate 12.1
	reg notifier;
	specify
		(posedge CK => (Q1+:D1)) = 0;
		(posedge CK => (Q2+:D2)) = 0;
		(posedge CK => (Q1N-:D1)) = 0;
		(posedge CK => (Q2N-:D2)) = 0;
		$setuphold (posedge CK, posedge D1, 0, 0, notifier);
		$setuphold (posedge CK, negedge D1, 0, 0, notifier);
		$setuphold (posedge CK, posedge D2, 0, 0, notifier);
		$setuphold (posedge CK, negedge D2, 0, 0, notifier);
		$width (posedge CK, 0, 0, notifier);
		$width (negedge CK, 0, 0, notifier);
	endspecify
	// End Section written by Liberate 12.1

endmodule

module DFF2RX2(Q1, Q2, Q1N, Q2N, D1, D2, RN, CK);
input  D1, D2, RN, CK;
output Q1, Q2, Q1N, Q2N;
wire  Q1, Q2, Q1N, Q2N, D1, D2, RN, CK, n$1, n$2;
wire   [1:0] IQ;
wire   [1:0] IQN;
  _HDFF_verplex U$1(.Q(IQ[0]), .QN(IQN[0]), .S(1'b0), .R(n$1), .CK(CK), .D(D1));
  _HDFF_verplex U$2(.Q(IQ[1]), .QN(IQN[1]), .S(1'b0), .R(n$2), .CK(CK), .D(D2));
  buf U$3(Q1, IQ[0]);
  buf U$4(Q2, IQ[1]);
  buf U$5(Q1N, IQN[0]);
  buf U$6(Q2N, IQN[1]);
  not U$7(n$1, RN);
  not U$8(n$2, RN);

	// Section written by Liberate 12.1
	reg notifier;
	specify
		(negedge RN => (Q1+:1'b0)) = 0;
		(posedge CK => (Q1+:D1)) = 0;
		(negedge RN => (Q2+:1'b0)) = 0;
		(posedge CK => (Q2+:D2)) = 0;
		(negedge RN => (Q1N-:1'b0)) = 0;
		(posedge CK => (Q1N-:D1)) = 0;
		(negedge RN => (Q2N-:1'b0)) = 0;
		(posedge CK => (Q2N-:D2)) = 0;
		$setuphold (posedge CK, posedge D1, 0, 0, notifier);
		$setuphold (posedge CK, negedge D1, 0, 0, notifier);
		$setuphold (posedge CK, posedge D2, 0, 0, notifier);
		$setuphold (posedge CK, negedge D2, 0, 0, notifier);
		$recovery (posedge RN, posedge CK, 0, notifier);
		$hold (posedge CK, posedge RN, 0, notifier);
		$width (negedge RN, 0, 0, notifier);
		$width (posedge CK, 0, 0, notifier);
		$width (negedge CK, 0, 0, notifier);
	endspecify
	// End Section written by Liberate 12.1

endmodule

module DFF2RX1(Q1, Q2, Q1N, Q2N, D1, D2, RN, CK);
input  D1, D2, RN, CK;
output Q1, Q2, Q1N, Q2N;
wire  Q1, Q2, Q1N, Q2N, D1, D2, RN, CK, n$1, n$2;
wire   [1:0] IQ;
wire   [1:0] IQN;
  _HDFF_verplex U$1(.Q(IQ[0]), .QN(IQN[0]), .S(1'b0), .R(n$1), .CK(CK), .D(D1));
  _HDFF_verplex U$2(.Q(IQ[1]), .QN(IQN[1]), .S(1'b0), .R(n$2), .CK(CK), .D(D2));
  buf U$3(Q1, IQ[0]);
  buf U$4(Q2, IQ[1]);
  buf U$5(Q1N, IQN[0]);
  buf U$6(Q2N, IQN[1]);
  not U$7(n$1, RN);
  not U$8(n$2, RN);

	// Section written by Liberate 12.1
	reg notifier;
	specify
		(negedge RN => (Q1+:1'b0)) = 0;
		(posedge CK => (Q1+:D1)) = 0;
		(negedge RN => (Q2+:1'b0)) = 0;
		(posedge CK => (Q2+:D2)) = 0;
		(negedge RN => (Q1N-:1'b0)) = 0;
		(posedge CK => (Q1N-:D1)) = 0;
		(negedge RN => (Q2N-:1'b0)) = 0;
		(posedge CK => (Q2N-:D2)) = 0;
		$setuphold (posedge CK, posedge D1, 0, 0, notifier);
		$setuphold (posedge CK, negedge D1, 0, 0, notifier);
		$setuphold (posedge CK, posedge D2, 0, 0, notifier);
		$setuphold (posedge CK, negedge D2, 0, 0, notifier);
		$recovery (posedge RN, posedge CK, 0, notifier);
		$hold (posedge CK, posedge RN, 0, notifier);
		$width (negedge RN, 0, 0, notifier);
		$width (posedge CK, 0, 0, notifier);
		$width (negedge CK, 0, 0, notifier);
	endspecify
	// End Section written by Liberate 12.1

endmodule

module _HDFF_verplex(Q, QN, S, R, CK, D);
// verplex DFF
output  Q, QN;
input   S, R, CK, D;
wire   N1;
  DFF_UDP  i0(N1, S, R, CK, D);
  buf  (Q, N1);
  not  (QN, N1);
endmodule

primitive DFF_UDP(Q, S, R, CK, D);
output Q;
input  S, R, CK, D;
reg    Q;
  table
    1  0   ?    ?  :  ?  :  1; // Asserting preset
    *  0   ?    ?  :  1  :  1; // Changing preset
    ?  1   ?    ?  :  ?  :  0; // Asserting reset (dominates preset)
    0  *   ?    ?  :  0  :  0; // Changing reset
    0  ?   (01) 0  :  ?  :  0; // rising clock
    ?  0   (01) 1  :  ?  :  1; // rising clock 
    0  ?   p    0  :  0  :  0; // potential rising clock
    ?  0   p    1  :  1  :  1; // potential rising clock
    0  0   n    ?  :  ?  :  -; // Clock falling register output does not change
    0  0   ?    *  :  ?  :  -; // Changing Data
  endtable
endprimitive

