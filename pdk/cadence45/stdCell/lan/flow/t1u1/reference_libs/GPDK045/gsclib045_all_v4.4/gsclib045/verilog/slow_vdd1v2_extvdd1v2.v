// File Version: 120125_1645
// Verilog for library /lan/flow/t1u1/peider/dev1/WORK/zambezi45/WORK_ALTOS/gsclib_char/flows/_v_update/verilog/slow_vdd1v2_extvdd1v2 created by Liberate 3.1p1 on Wed Jan 25 16:41:39 PST 2012 for SDF version 2.1

// type:  
`timescale 1ns/10ps
`celldefine
module FSWNX1 (PSOn_out, PSOn);
	output PSOn_out;
	input PSOn;

	// Function
	buf (PSOn_out, PSOn);

	// Timing
	specify
		(PSOn => PSOn_out) = 0;
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module FSWX1 (PSO_out, PSO);
	output PSO_out;
	input PSO;

	// Function
	buf (PSO_out, PSO);

	// Timing
	specify
		(PSO => PSO_out) = 0;
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module HSWDNX1 (PSO1n_out, PSO2n_out, PSO1n, PSO2n);
	output PSO1n_out, PSO2n_out;
	input PSO1n, PSO2n;

	// Function
	buf (PSO1n_out, PSO1n);
	buf (PSO2n_out, PSO2n);

	// Timing
	specify
		(PSO1n => PSO1n_out) = 0;
		(PSO2n => PSO2n_out) = 0;
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module HSWDX1 (PSO1_out, PSO2_out, PSO1, PSO2);
	output PSO1_out, PSO2_out;
	input PSO1, PSO2;

	// Function
	buf (PSO1_out, PSO1);
	buf (PSO2_out, PSO2);

	// Timing
	specify
		(PSO1 => PSO1_out) = 0;
		(PSO2 => PSO2_out) = 0;
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module HSWNX1 (PSOn_out, PSOn);
	output PSOn_out;
	input PSOn;

	// Function
	buf (PSOn_out, PSOn);

	// Timing
	specify
		(PSOn => PSOn_out) = 0;
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module HSWX1 (PSO_out, PSO);
	output PSO_out;
	input PSO;

	// Function
	buf (PSO_out, PSO);

	// Timing
	specify
		(PSO => PSO_out) = 0;
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module ISOHLDX1_OFF (Q, D, ISO);
	output Q;
	input D, ISO;
	reg notifier;
	wire delayed_D, delayed_ISO;

	// Function
	wire int_fwire_clk, int_fwire_IQ;

	not (int_fwire_clk, delayed_ISO);
	altos_latch (int_fwire_IQ, notifier, int_fwire_clk, delayed_D);
	buf (Q, int_fwire_IQ);

	// Timing

	// Additional timing wires
	wire adacond_D, adacond_NOT_D;


	// Additional timing gates
	buf (adacond_D, D);
	not (adacond_NOT_D, D);

	specify
		(D => Q) = 0;
		(negedge ISO => (Q+:D)) = 0;
		$setuphold (posedge ISO, posedge D, 0, 0, notifier,,, delayed_ISO, delayed_D);
		$setuphold (posedge ISO, negedge D, 0, 0, notifier,,, delayed_ISO, delayed_D);
		$width (negedge ISO &&& adacond_D, 0, 0, notifier);
		$width (negedge ISO &&& adacond_NOT_D, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module ISOHLDX1_ON (Q, D, ISO);
	output Q;
	input D, ISO;
	reg notifier;
	wire delayed_D, delayed_ISO;

	// Function
	wire int_fwire_clk, int_fwire_IQ;

	not (int_fwire_clk, delayed_ISO);
	altos_latch (int_fwire_IQ, notifier, int_fwire_clk, delayed_D);
	buf (Q, int_fwire_IQ);

	// Timing

	// Additional timing wires
	wire adacond_D, adacond_NOT_D;


	// Additional timing gates
	buf (adacond_D, D);
	not (adacond_NOT_D, D);

	specify
		(D => Q) = 0;
		(negedge ISO => (Q+:D)) = 0;
		$setuphold (posedge ISO, posedge D, 0, 0, notifier,,, delayed_ISO, delayed_D);
		$setuphold (posedge ISO, negedge D, 0, 0, notifier,,, delayed_ISO, delayed_D);
		$width (negedge ISO &&& adacond_D, 0, 0, notifier);
		$width (negedge ISO &&& adacond_NOT_D, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module ISOHX1_OFF (Y, A, ISO);
	output Y;
	input A, ISO;

	// Function
	or (Y, A, ISO);

	// Timing
	specify
		(A => Y) = 0;
		(ISO => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module ISOHX1_ON (Y, A, ISO);
	output Y;
	input A, ISO;

	// Function
	or (Y, A, ISO);

	// Timing
	specify
		(A => Y) = 0;
		(ISO => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module ISOLX1_OFF (Y, A, ISO);
	output Y;
	input A, ISO;

	// Function
	wire ISO__bar;

	not (ISO__bar, ISO);
	and (Y, A, ISO__bar);

	// Timing
	specify
		(A => Y) = 0;
		(ISO => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module ISOLX1_ON (Y, A, ISO);
	output Y;
	input A, ISO;

	// Function
	wire ISO__bar;

	not (ISO__bar, ISO);
	and (Y, A, ISO__bar);

	// Timing
	specify
		(A => Y) = 0;
		(ISO => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module ISONLX1_OFF (Y, A, ISOn);
	output Y;
	input A, ISOn;

	// Function
	and (Y, A, ISOn);

	// Timing
	specify
		(A => Y) = 0;
		(ISOn => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module ISONLX1_ON (Y, A, ISOn);
	output Y;
	input A, ISOn;

	// Function
	and (Y, A, ISOn);

	// Timing
	specify
		(A => Y) = 0;
		(ISOn => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module PBUFX2 (Y, A);
	output Y;
	input A;

	// Function
	buf (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module PINVX1 (Y, A);
	output Y;
	input A;

	// Function
	not (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RDFFNQX1 (Q, D, RT, CKN);
	output Q;
	input D, RT, CKN;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_CKN;

	// Function
	wire delayed_RT__bar, int_fwire_clk, int_fwire_d;
	wire int_fwire_IQ, xcr_0;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, delayed_D);
	not (int_fwire_clk, delayed_CKN);
	altos_dff_err (xcr_0, int_fwire_clk, int_fwire_d);
	altos_dff (int_fwire_IQ, notifier, int_fwire_clk, int_fwire_d, xcr_0);
	buf (Q, int_fwire_IQ);

	// Timing

	// Additional timing wires
	wire adacond_D, adacond_D_AND_NOT_RT, adacond_NOT_D;
	wire adacond_NOT_D_AND_NOT_RT, adacond_NOT_RT;


	// Additional timing gates
	not (adacond_NOT_RT, RT);
	buf (adacond_D, D);
	not (adacond_NOT_D, D);
	and (adacond_D_AND_NOT_RT, D, adacond_NOT_RT);
	and (adacond_NOT_D_AND_NOT_RT, adacond_NOT_D, adacond_NOT_RT);

	specify
		(RT => Q) = 0;
		(negedge CKN => (Q+:((D && !RT)))) = 0;
		$setuphold (negedge CKN &&& adacond_NOT_RT, posedge D &&& adacond_NOT_RT, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (negedge CKN &&& adacond_NOT_RT, negedge D &&& adacond_NOT_RT, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (posedge CKN &&& adacond_D, negedge RT &&& adacond_D, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (posedge CKN &&& adacond_NOT_D, negedge RT &&& adacond_NOT_D, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$width (posedge CKN &&& adacond_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge CKN &&& adacond_D_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CKN &&& adacond_NOT_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge CKN &&& adacond_NOT_D_AND_NOT_RT, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RDFFNRQX1 (Q, D, RT, RN, CKN);
	output Q;
	input D, RT, RN, CKN;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_CKN;

	// Function
	wire delayed_RT__bar, int_fwire_clk, int_fwire_d;
	wire int_fwire_IQ, int_fwire_r, xcr_0;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, delayed_D);
	not (int_fwire_clk, delayed_CKN);
	not (int_fwire_r, RN);
	altos_dff_r_err (xcr_0, int_fwire_clk, int_fwire_d, int_fwire_r);
	altos_dff_r (int_fwire_IQ, notifier, int_fwire_clk, int_fwire_d, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);

	// Timing

	// Additional timing wires
	wire adacond_CKN_AND_D_AND_NOT_RT, adacond_CKN_AND_NOT_D_AND_NOT_RT, adacond_D_AND_NOT_RT;
	wire adacond_D_AND_RN, adacond_D_AND_RN_AND_NOT_RT, adacond_NOT_CKN_AND_NOT_RT;
	wire adacond_NOT_D_AND_RN, adacond_NOT_D_AND_RN_AND_NOT_RT, adacond_RN_AND_NOT_RT;
	wire CKN__bar, D__bar, RT__bar;


	// Additional timing gates
	not (RT__bar, RT);
	and (adacond_RN_AND_NOT_RT, RN, RT__bar);
	and (adacond_D_AND_RN, D, RN);
	not (D__bar, D);
	and (adacond_NOT_D_AND_RN, D__bar, RN);
	and (adacond_D_AND_NOT_RT, D, RT__bar);
	and (adacond_CKN_AND_D_AND_NOT_RT, CKN, D, RT__bar);
	and (adacond_CKN_AND_NOT_D_AND_NOT_RT, CKN, D__bar, RT__bar);
	not (CKN__bar, CKN);
	and (adacond_NOT_CKN_AND_NOT_RT, CKN__bar, RT__bar);
	and (adacond_D_AND_RN_AND_NOT_RT, D, RN, RT__bar);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT, D__bar, RN, RT__bar);

	specify
		ifnone (RT => Q) = 0;
		if ((CKN&&!RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CKN&&RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CKN&&!RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CKN&&D&&!RT))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((CKN&&!D&&!RT))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CKN&&!RT))
			(negedge RN => (Q+:1'b0)) = 0;
		(negedge CKN => (Q+:((D && !RT)))) = 0;
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT, posedge D &&& adacond_RN_AND_NOT_RT, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT, negedge D &&& adacond_RN_AND_NOT_RT, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (posedge CKN &&& adacond_D_AND_RN, negedge RT &&& adacond_D_AND_RN, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (posedge CKN &&& adacond_NOT_D_AND_RN, negedge RT &&& adacond_NOT_D_AND_RN, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$recovery (posedge RN &&& adacond_D_AND_NOT_RT, negedge CKN &&& adacond_D_AND_NOT_RT, 0, notifier);
		$hold (negedge CKN &&& adacond_D_AND_NOT_RT, posedge RN &&& adacond_D_AND_NOT_RT, 0, notifier);
		$width (negedge RN &&& adacond_CKN_AND_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge RN &&& adacond_CKN_AND_NOT_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge RN &&& adacond_NOT_CKN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CKN &&& adacond_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (negedge CKN &&& adacond_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (negedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RDFFNRX1 (Q, QN, D, RT, RN, CKN);
	output Q, QN;
	input D, RT, RN, CKN;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_CKN;

	// Function
	wire delayed_RT__bar, int_fwire_clk, int_fwire_d;
	wire int_fwire_IQ, int_fwire_IQN, int_fwire_r;
	wire xcr_0;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, delayed_D);
	not (int_fwire_clk, delayed_CKN);
	not (int_fwire_r, RN);
	altos_dff_r_err (xcr_0, int_fwire_clk, int_fwire_d, int_fwire_r);
	altos_dff_r (int_fwire_IQ, notifier, int_fwire_clk, int_fwire_d, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_CKN_AND_D_AND_NOT_RT, adacond_CKN_AND_NOT_D_AND_NOT_RT, adacond_D_AND_NOT_RT;
	wire adacond_D_AND_RN, adacond_D_AND_RN_AND_NOT_RT, adacond_NOT_CKN_AND_NOT_RT;
	wire adacond_NOT_D_AND_RN, adacond_NOT_D_AND_RN_AND_NOT_RT, adacond_RN_AND_NOT_RT;
	wire CKN__bar, D__bar, RT__bar;


	// Additional timing gates
	not (RT__bar, RT);
	and (adacond_RN_AND_NOT_RT, RN, RT__bar);
	and (adacond_D_AND_RN, D, RN);
	not (D__bar, D);
	and (adacond_NOT_D_AND_RN, D__bar, RN);
	and (adacond_D_AND_NOT_RT, D, RT__bar);
	and (adacond_CKN_AND_D_AND_NOT_RT, CKN, D, RT__bar);
	and (adacond_CKN_AND_NOT_D_AND_NOT_RT, CKN, D__bar, RT__bar);
	not (CKN__bar, CKN);
	and (adacond_NOT_CKN_AND_NOT_RT, CKN__bar, RT__bar);
	and (adacond_D_AND_RN_AND_NOT_RT, D, RN, RT__bar);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT, D__bar, RN, RT__bar);

	specify
		ifnone (RT => Q) = 0;
		if ((CKN&&!RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CKN&&RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CKN&&!RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CKN&&D&&!RT))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((CKN&&!D&&!RT))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CKN&&!RT))
			(negedge RN => (Q+:1'b0)) = 0;
		(negedge CKN => (Q+:((D && !RT)))) = 0;
		if ((CKN&&!RN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((!CKN&&RN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((!CKN&&!RN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((CKN&&D&&!RT))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((CKN&&!D&&!RT))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((!CKN&&!RT))
			(negedge RN => (QN-:1'b0)) = 0;
		(negedge CKN => (QN-:((D && !RT)))) = 0;
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT, posedge D &&& adacond_RN_AND_NOT_RT, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT, negedge D &&& adacond_RN_AND_NOT_RT, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (posedge CKN &&& adacond_D_AND_RN, negedge RT &&& adacond_D_AND_RN, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (posedge CKN &&& adacond_NOT_D_AND_RN, negedge RT &&& adacond_NOT_D_AND_RN, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$recovery (posedge RN &&& adacond_D_AND_NOT_RT, negedge CKN &&& adacond_D_AND_NOT_RT, 0, notifier);
		$hold (negedge CKN &&& adacond_D_AND_NOT_RT, posedge RN &&& adacond_D_AND_NOT_RT, 0, notifier);
		$width (negedge RN &&& adacond_CKN_AND_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge RN &&& adacond_CKN_AND_NOT_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge RN &&& adacond_NOT_CKN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CKN &&& adacond_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (negedge CKN &&& adacond_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (negedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RDFFNSQX1 (Q, D, RT, SN, CKN);
	output Q;
	input D, RT, SN, CKN;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_CKN;

	// Function
	wire delayed_RT__bar, int_fwire_clk, int_fwire_d;
	wire int_fwire_IQ, int_fwire_s, xcr_0;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, delayed_D);
	not (int_fwire_clk, delayed_CKN);
	not (int_fwire_s, SN);
	altos_dff_s_err (xcr_0, int_fwire_clk, int_fwire_d, int_fwire_s);
	altos_dff_s (int_fwire_IQ, notifier, int_fwire_clk, int_fwire_d, int_fwire_s, xcr_0);
	buf (Q, int_fwire_IQ);

	// Timing

	// Additional timing wires
	wire adacond_CKN_AND_D_AND_NOT_RT, adacond_CKN_AND_NOT_D_AND_NOT_RT, adacond_D_AND_NOT_RT_AND_SN;
	wire adacond_D_AND_SN, adacond_NOT_CKN_AND_NOT_RT, adacond_NOT_D_AND_NOT_RT;
	wire adacond_NOT_D_AND_NOT_RT_AND_SN, adacond_NOT_D_AND_SN, adacond_NOT_RT_AND_SN;
	wire CKN__bar, D__bar, RT__bar;


	// Additional timing gates
	not (RT__bar, RT);
	and (adacond_NOT_RT_AND_SN, RT__bar, SN);
	and (adacond_D_AND_SN, D, SN);
	not (D__bar, D);
	and (adacond_NOT_D_AND_SN, D__bar, SN);
	and (adacond_NOT_D_AND_NOT_RT, D__bar, RT__bar);
	and (adacond_CKN_AND_D_AND_NOT_RT, CKN, D, RT__bar);
	and (adacond_CKN_AND_NOT_D_AND_NOT_RT, CKN, D__bar, RT__bar);
	not (CKN__bar, CKN);
	and (adacond_NOT_CKN_AND_NOT_RT, CKN__bar, RT__bar);
	and (adacond_D_AND_NOT_RT_AND_SN, D, RT__bar, SN);
	and (adacond_NOT_D_AND_NOT_RT_AND_SN, D__bar, RT__bar, SN);

	specify
		if ((CKN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CKN&&SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CKN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CKN&&D&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CKN&&!D&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CKN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		(negedge CKN => (Q+:((D && !RT)))) = 0;
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_SN, posedge D &&& adacond_NOT_RT_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_SN, negedge D &&& adacond_NOT_RT_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (posedge CKN &&& adacond_D_AND_SN, negedge RT &&& adacond_D_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (posedge CKN &&& adacond_NOT_D_AND_SN, negedge RT &&& adacond_NOT_D_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$recovery (posedge SN &&& adacond_NOT_D_AND_NOT_RT, negedge CKN &&& adacond_NOT_D_AND_NOT_RT, 0, notifier);
		$hold (negedge CKN &&& adacond_NOT_D_AND_NOT_RT, posedge SN &&& adacond_NOT_D_AND_NOT_RT, 0, notifier);
		$width (negedge SN &&& adacond_CKN_AND_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_CKN_AND_NOT_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_NOT_CKN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CKN &&& adacond_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge CKN &&& adacond_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (posedge CKN &&& adacond_NOT_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge CKN &&& adacond_NOT_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RDFFNSRQX1 (Q, D, RT, RN, SN, CKN);
	output Q;
	input D, RT, RN, SN, CKN;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_RN, delayed_SN, delayed_CKN;

	// Function
	wire delayed_RT__bar, int_fwire_clk, int_fwire_d;
	wire int_fwire_IQ, int_fwire_r, int_fwire_s;
	wire xcr_0;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, delayed_D);
	not (int_fwire_clk, delayed_CKN);
	not (int_fwire_s, delayed_SN);
	not (int_fwire_r, delayed_RN);
	altos_dff_sr_err (xcr_0, int_fwire_clk, int_fwire_d, int_fwire_s, int_fwire_r);
	altos_dff_sr_1 (int_fwire_IQ, notifier, int_fwire_clk, int_fwire_d, int_fwire_s, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);

	// Timing

	// Additional timing wires
	wire adacond_CKN_AND_D_AND_NOT_RT, adacond_CKN_AND_D_AND_NOT_RT_AND_SN, adacond_CKN_AND_D_AND_RN_AND_NOT_RT;
	wire adacond_CKN_AND_NOT_D_AND_NOT_RT, adacond_CKN_AND_NOT_D_AND_NOT_RT_AND_SN, adacond_CKN_AND_NOT_D_AND_RN_AND_NOT_RT;
	wire adacond_D_AND_NOT_RT_AND_SN, adacond_D_AND_RN_AND_NOT_RT_AND_SN, adacond_D_AND_RN_AND_SN;
	wire adacond_NOT_CKN_AND_NOT_RT, adacond_NOT_CKN_AND_NOT_RT_AND_SN, adacond_NOT_CKN_AND_RN_AND_NOT_RT;
	wire adacond_NOT_D_AND_RN_AND_NOT_RT, adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, adacond_NOT_D_AND_RN_AND_SN;
	wire adacond_RN_AND_NOT_RT_AND_SN, CKN__bar, D__bar;
	wire RT__bar;


	// Additional timing gates
	not (RT__bar, RT);
	and (adacond_RN_AND_NOT_RT_AND_SN, RN, RT__bar, SN);
	and (adacond_D_AND_RN_AND_SN, D, RN, SN);
	not (D__bar, D);
	and (adacond_NOT_D_AND_RN_AND_SN, D__bar, RN, SN);
	and (adacond_D_AND_NOT_RT_AND_SN, D, RT__bar, SN);
	and (adacond_CKN_AND_D_AND_NOT_RT_AND_SN, CKN, D, RT__bar, SN);
	and (adacond_CKN_AND_NOT_D_AND_NOT_RT_AND_SN, CKN, D__bar, RT__bar, SN);
	not (CKN__bar, CKN);
	and (adacond_NOT_CKN_AND_NOT_RT_AND_SN, CKN__bar, RT__bar, SN);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT, D__bar, RN, RT__bar);
	and (adacond_CKN_AND_D_AND_NOT_RT, CKN, D, RT__bar);
	and (adacond_CKN_AND_NOT_D_AND_NOT_RT, CKN, D__bar, RT__bar);
	and (adacond_NOT_CKN_AND_NOT_RT, CKN__bar, RT__bar);
	and (adacond_CKN_AND_D_AND_RN_AND_NOT_RT, CKN, D, RN, RT__bar);
	and (adacond_CKN_AND_NOT_D_AND_RN_AND_NOT_RT, CKN, D__bar, RN, RT__bar);
	and (adacond_NOT_CKN_AND_RN_AND_NOT_RT, CKN__bar, RN, RT__bar);
	and (adacond_D_AND_RN_AND_NOT_RT_AND_SN, D, RN, RT__bar, SN);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, D__bar, RN, RT__bar, SN);

	specify
		if ((!CKN&&RN&&SN))
			(RT => Q) = 0;
		if ((CKN&&!RN&&SN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CKN&&!RN&&SN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CKN&&RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CKN&&!RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CKN&&RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CKN&&!RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CKN&&D&&!RT&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((CKN&&!D&&!RT&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CKN&&!RT&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((CKN&&D&&!RN&&!RT))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((CKN&&!D&&!RN&&!RT))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((!CKN&&!RN&&!RT))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((CKN&&D&&RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CKN&&D&&!RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CKN&&!D&&RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CKN&&!D&&!RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CKN&&RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CKN&&!RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		(negedge CKN => (Q+:((D && !RT)))) = 0;
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_SN, posedge D &&& adacond_RN_AND_NOT_RT_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_SN, negedge D &&& adacond_RN_AND_NOT_RT_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (posedge CKN &&& adacond_D_AND_RN_AND_SN, negedge RT &&& adacond_D_AND_RN_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (posedge CKN &&& adacond_NOT_D_AND_RN_AND_SN, negedge RT &&& adacond_NOT_D_AND_RN_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (posedge RN &&& adacond_CKN_AND_D_AND_NOT_RT, posedge SN &&& adacond_CKN_AND_D_AND_NOT_RT, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$setuphold (posedge RN &&& adacond_CKN_AND_NOT_D_AND_NOT_RT, posedge SN &&& adacond_CKN_AND_NOT_D_AND_NOT_RT, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$setuphold (posedge RN &&& adacond_NOT_CKN_AND_NOT_RT, posedge SN &&& adacond_NOT_CKN_AND_NOT_RT, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$recovery (posedge RN &&& adacond_D_AND_NOT_RT_AND_SN, negedge CKN &&& adacond_D_AND_NOT_RT_AND_SN, 0, notifier);
		$hold (negedge CKN &&& adacond_D_AND_NOT_RT_AND_SN, posedge RN &&& adacond_D_AND_NOT_RT_AND_SN, 0, notifier);
		$recovery (posedge SN &&& adacond_NOT_D_AND_RN_AND_NOT_RT, negedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, notifier);
		$hold (negedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT, posedge SN &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, notifier);
		$width (negedge RN &&& adacond_CKN_AND_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge RN &&& adacond_CKN_AND_NOT_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge RN &&& adacond_NOT_CKN_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge SN &&& adacond_CKN_AND_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_CKN_AND_NOT_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_NOT_CKN_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CKN &&& adacond_D_AND_RN_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge CKN &&& adacond_D_AND_RN_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (posedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RDFFNSRX1 (Q, QN, D, RT, RN, SN, CKN);
	output Q, QN;
	input D, RT, RN, SN, CKN;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_RN, delayed_SN, delayed_CKN;

	// Function
	wire delayed_RT__bar, int_fwire_clk, int_fwire_d;
	wire int_fwire_IQ, int_fwire_IQN, int_fwire_r;
	wire int_fwire_s, xcr_0;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, delayed_D);
	not (int_fwire_clk, delayed_CKN);
	not (int_fwire_s, delayed_SN);
	not (int_fwire_r, delayed_RN);
	altos_dff_sr_err (xcr_0, int_fwire_clk, int_fwire_d, int_fwire_s, int_fwire_r);
	altos_dff_sr_1 (int_fwire_IQ, notifier, int_fwire_clk, int_fwire_d, int_fwire_s, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_CKN_AND_D_AND_NOT_RT, adacond_CKN_AND_D_AND_NOT_RT_AND_SN, adacond_CKN_AND_D_AND_RN_AND_NOT_RT;
	wire adacond_CKN_AND_NOT_D_AND_NOT_RT, adacond_CKN_AND_NOT_D_AND_NOT_RT_AND_SN, adacond_CKN_AND_NOT_D_AND_RN_AND_NOT_RT;
	wire adacond_D_AND_NOT_RT_AND_SN, adacond_D_AND_RN_AND_NOT_RT_AND_SN, adacond_D_AND_RN_AND_SN;
	wire adacond_NOT_CKN_AND_NOT_RT, adacond_NOT_CKN_AND_NOT_RT_AND_SN, adacond_NOT_CKN_AND_RN_AND_NOT_RT;
	wire adacond_NOT_D_AND_RN_AND_NOT_RT, adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, adacond_NOT_D_AND_RN_AND_SN;
	wire adacond_RN_AND_NOT_RT_AND_SN, CKN__bar, D__bar;
	wire RT__bar;


	// Additional timing gates
	not (RT__bar, RT);
	and (adacond_RN_AND_NOT_RT_AND_SN, RN, RT__bar, SN);
	and (adacond_D_AND_RN_AND_SN, D, RN, SN);
	not (D__bar, D);
	and (adacond_NOT_D_AND_RN_AND_SN, D__bar, RN, SN);
	and (adacond_D_AND_NOT_RT_AND_SN, D, RT__bar, SN);
	and (adacond_CKN_AND_D_AND_NOT_RT_AND_SN, CKN, D, RT__bar, SN);
	and (adacond_CKN_AND_NOT_D_AND_NOT_RT_AND_SN, CKN, D__bar, RT__bar, SN);
	not (CKN__bar, CKN);
	and (adacond_NOT_CKN_AND_NOT_RT_AND_SN, CKN__bar, RT__bar, SN);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT, D__bar, RN, RT__bar);
	and (adacond_CKN_AND_D_AND_NOT_RT, CKN, D, RT__bar);
	and (adacond_CKN_AND_NOT_D_AND_NOT_RT, CKN, D__bar, RT__bar);
	and (adacond_NOT_CKN_AND_NOT_RT, CKN__bar, RT__bar);
	and (adacond_CKN_AND_D_AND_RN_AND_NOT_RT, CKN, D, RN, RT__bar);
	and (adacond_CKN_AND_NOT_D_AND_RN_AND_NOT_RT, CKN, D__bar, RN, RT__bar);
	and (adacond_NOT_CKN_AND_RN_AND_NOT_RT, CKN__bar, RN, RT__bar);
	and (adacond_D_AND_RN_AND_NOT_RT_AND_SN, D, RN, RT__bar, SN);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, D__bar, RN, RT__bar, SN);

	specify
		if ((!CKN&&RN&&SN))
			(RT => Q) = 0;
		if ((CKN&&!RN&&SN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CKN&&!RN&&SN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CKN&&RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CKN&&!RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CKN&&RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CKN&&!RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CKN&&D&&!RT&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((CKN&&!D&&!RT&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CKN&&!RT&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((CKN&&D&&!RN&&!RT))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((CKN&&!D&&!RN&&!RT))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((!CKN&&!RN&&!RT))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((CKN&&D&&RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CKN&&D&&!RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CKN&&!D&&RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CKN&&!D&&!RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CKN&&RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CKN&&!RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		(negedge CKN => (Q+:((D && !RT)))) = 0;
		if ((!CKN&&RN&&SN))
			(RT => QN) = 0;
		if ((CKN&&RN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((CKN&&!RN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((!CKN&&RN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((!CKN&&!RN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((CKN&&!RN&&SN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((!CKN&&!RN&&SN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((CKN&&D&&!RT&&SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((CKN&&!D&&!RT&&SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((!CKN&&!RT&&SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((CKN&&D&&RN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((CKN&&D&&!RN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((CKN&&!D&&RN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((CKN&&!D&&!RN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!CKN&&RN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!CKN&&!RN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((CKN&&D&&!RN&&!RT))
			(posedge SN => (QN-:1'b0)) = 0;
		if ((CKN&&!D&&!RN&&!RT))
			(posedge SN => (QN-:1'b0)) = 0;
		if ((!CKN&&!RN&&!RT))
			(posedge SN => (QN-:1'b0)) = 0;
		(negedge CKN => (QN-:((D && !RT)))) = 0;
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_SN, posedge D &&& adacond_RN_AND_NOT_RT_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_SN, negedge D &&& adacond_RN_AND_NOT_RT_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (posedge CKN &&& adacond_D_AND_RN_AND_SN, negedge RT &&& adacond_D_AND_RN_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (posedge CKN &&& adacond_NOT_D_AND_RN_AND_SN, negedge RT &&& adacond_NOT_D_AND_RN_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (posedge RN &&& adacond_CKN_AND_D_AND_NOT_RT, posedge SN &&& adacond_CKN_AND_D_AND_NOT_RT, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$setuphold (posedge RN &&& adacond_CKN_AND_NOT_D_AND_NOT_RT, posedge SN &&& adacond_CKN_AND_NOT_D_AND_NOT_RT, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$setuphold (posedge RN &&& adacond_NOT_CKN_AND_NOT_RT, posedge SN &&& adacond_NOT_CKN_AND_NOT_RT, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$recovery (posedge RN &&& adacond_D_AND_NOT_RT_AND_SN, negedge CKN &&& adacond_D_AND_NOT_RT_AND_SN, 0, notifier);
		$hold (negedge CKN &&& adacond_D_AND_NOT_RT_AND_SN, posedge RN &&& adacond_D_AND_NOT_RT_AND_SN, 0, notifier);
		$recovery (posedge SN &&& adacond_NOT_D_AND_RN_AND_NOT_RT, negedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, notifier);
		$hold (negedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT, posedge SN &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, notifier);
		$width (negedge RN &&& adacond_CKN_AND_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge RN &&& adacond_CKN_AND_NOT_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge RN &&& adacond_NOT_CKN_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge SN &&& adacond_CKN_AND_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_CKN_AND_NOT_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_NOT_CKN_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CKN &&& adacond_D_AND_RN_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge CKN &&& adacond_D_AND_RN_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (posedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RDFFNSX1 (Q, QN, D, RT, SN, CKN);
	output Q, QN;
	input D, RT, SN, CKN;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_CKN;

	// Function
	wire delayed_RT__bar, int_fwire_clk, int_fwire_d;
	wire int_fwire_IQ, int_fwire_IQN, int_fwire_s;
	wire xcr_0;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, delayed_D);
	not (int_fwire_clk, delayed_CKN);
	not (int_fwire_s, SN);
	altos_dff_s_err (xcr_0, int_fwire_clk, int_fwire_d, int_fwire_s);
	altos_dff_s (int_fwire_IQ, notifier, int_fwire_clk, int_fwire_d, int_fwire_s, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_CKN_AND_D_AND_NOT_RT, adacond_CKN_AND_NOT_D_AND_NOT_RT, adacond_D_AND_NOT_RT_AND_SN;
	wire adacond_D_AND_SN, adacond_NOT_CKN_AND_NOT_RT, adacond_NOT_D_AND_NOT_RT;
	wire adacond_NOT_D_AND_NOT_RT_AND_SN, adacond_NOT_D_AND_SN, adacond_NOT_RT_AND_SN;
	wire CKN__bar, D__bar, RT__bar;


	// Additional timing gates
	not (RT__bar, RT);
	and (adacond_NOT_RT_AND_SN, RT__bar, SN);
	and (adacond_D_AND_SN, D, SN);
	not (D__bar, D);
	and (adacond_NOT_D_AND_SN, D__bar, SN);
	and (adacond_NOT_D_AND_NOT_RT, D__bar, RT__bar);
	and (adacond_CKN_AND_D_AND_NOT_RT, CKN, D, RT__bar);
	and (adacond_CKN_AND_NOT_D_AND_NOT_RT, CKN, D__bar, RT__bar);
	not (CKN__bar, CKN);
	and (adacond_NOT_CKN_AND_NOT_RT, CKN__bar, RT__bar);
	and (adacond_D_AND_NOT_RT_AND_SN, D, RT__bar, SN);
	and (adacond_NOT_D_AND_NOT_RT_AND_SN, D__bar, RT__bar, SN);

	specify
		if ((CKN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CKN&&SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CKN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CKN&&D&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CKN&&!D&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CKN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		(negedge CKN => (Q+:((D && !RT)))) = 0;
		ifnone (RT => QN) = 0;
		if ((CKN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((!CKN&&SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((!CKN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((CKN&&D&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((CKN&&!D&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!CKN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		(negedge CKN => (QN-:((D && !RT)))) = 0;
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_SN, posedge D &&& adacond_NOT_RT_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_SN, negedge D &&& adacond_NOT_RT_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (posedge CKN &&& adacond_D_AND_SN, negedge RT &&& adacond_D_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (posedge CKN &&& adacond_NOT_D_AND_SN, negedge RT &&& adacond_NOT_D_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$recovery (posedge SN &&& adacond_NOT_D_AND_NOT_RT, negedge CKN &&& adacond_NOT_D_AND_NOT_RT, 0, notifier);
		$hold (negedge CKN &&& adacond_NOT_D_AND_NOT_RT, posedge SN &&& adacond_NOT_D_AND_NOT_RT, 0, notifier);
		$width (negedge SN &&& adacond_CKN_AND_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_CKN_AND_NOT_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_NOT_CKN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CKN &&& adacond_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge CKN &&& adacond_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (posedge CKN &&& adacond_NOT_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge CKN &&& adacond_NOT_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RDFFNX1 (Q, QN, D, RT, CKN);
	output Q, QN;
	input D, RT, CKN;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_CKN;

	// Function
	wire delayed_RT__bar, int_fwire_clk, int_fwire_d;
	wire int_fwire_IQ, int_fwire_IQN, xcr_0;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, delayed_D);
	not (int_fwire_clk, delayed_CKN);
	altos_dff_err (xcr_0, int_fwire_clk, int_fwire_d);
	altos_dff (int_fwire_IQ, notifier, int_fwire_clk, int_fwire_d, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_D, adacond_D_AND_NOT_RT, adacond_NOT_D;
	wire adacond_NOT_D_AND_NOT_RT, adacond_NOT_RT;


	// Additional timing gates
	not (adacond_NOT_RT, RT);
	buf (adacond_D, D);
	not (adacond_NOT_D, D);
	and (adacond_D_AND_NOT_RT, D, adacond_NOT_RT);
	and (adacond_NOT_D_AND_NOT_RT, adacond_NOT_D, adacond_NOT_RT);

	specify
		(RT => Q) = 0;
		(negedge CKN => (Q+:((D && !RT)))) = 0;
		(RT => QN) = 0;
		(negedge CKN => (QN-:((D && !RT)))) = 0;
		$setuphold (negedge CKN &&& adacond_NOT_RT, posedge D &&& adacond_NOT_RT, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (negedge CKN &&& adacond_NOT_RT, negedge D &&& adacond_NOT_RT, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (posedge CKN &&& adacond_D, negedge RT &&& adacond_D, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (posedge CKN &&& adacond_NOT_D, negedge RT &&& adacond_NOT_D, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$width (posedge CKN &&& adacond_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge CKN &&& adacond_D_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CKN &&& adacond_NOT_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge CKN &&& adacond_NOT_D_AND_NOT_RT, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RDFFQX1 (Q, D, RT, CK);
	output Q;
	input D, RT, CK;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_CK;

	// Function
	wire delayed_RT__bar, int_fwire_d, int_fwire_IQ;
	wire xcr_0;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, delayed_D);
	altos_dff_err (xcr_0, delayed_CK, int_fwire_d);
	altos_dff (int_fwire_IQ, notifier, delayed_CK, int_fwire_d, xcr_0);
	buf (Q, int_fwire_IQ);

	// Timing

	// Additional timing wires
	wire adacond_D, adacond_D_AND_NOT_RT, adacond_NOT_D;
	wire adacond_NOT_D_AND_NOT_RT, adacond_NOT_RT;


	// Additional timing gates
	not (adacond_NOT_RT, RT);
	buf (adacond_D, D);
	not (adacond_NOT_D, D);
	and (adacond_D_AND_NOT_RT, D, adacond_NOT_RT);
	and (adacond_NOT_D_AND_NOT_RT, adacond_NOT_D, adacond_NOT_RT);

	specify
		(RT => Q) = 0;
		(posedge CK => (Q+:((D && !RT)))) = 0;
		$setuphold (posedge CK &&& adacond_NOT_RT, posedge D &&& adacond_NOT_RT, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (posedge CK &&& adacond_NOT_RT, negedge D &&& adacond_NOT_RT, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (negedge CK &&& adacond_D, negedge RT &&& adacond_D, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (negedge CK &&& adacond_NOT_D, negedge RT &&& adacond_NOT_D, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$width (posedge CK &&& adacond_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge CK &&& adacond_D_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CK &&& adacond_NOT_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge CK &&& adacond_NOT_D_AND_NOT_RT, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RDFFRQX1 (Q, D, RT, RN, CK);
	output Q;
	input D, RT, RN, CK;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_CK;

	// Function
	wire delayed_RT__bar, int_fwire_d, int_fwire_IQ;
	wire int_fwire_r, xcr_0;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, delayed_D);
	not (int_fwire_r, RN);
	altos_dff_r_err (xcr_0, delayed_CK, int_fwire_d, int_fwire_r);
	altos_dff_r (int_fwire_IQ, notifier, delayed_CK, int_fwire_d, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);

	// Timing

	// Additional timing wires
	wire adacond_CK_AND_NOT_RT, adacond_D_AND_NOT_RT, adacond_D_AND_RN;
	wire adacond_D_AND_RN_AND_NOT_RT, adacond_NOT_CK_AND_D_AND_NOT_RT, adacond_NOT_CK_AND_NOT_D_AND_NOT_RT;
	wire adacond_NOT_D_AND_RN, adacond_NOT_D_AND_RN_AND_NOT_RT, adacond_RN_AND_NOT_RT;
	wire CK__bar, D__bar, RT__bar;


	// Additional timing gates
	not (RT__bar, RT);
	and (adacond_RN_AND_NOT_RT, RN, RT__bar);
	and (adacond_D_AND_RN, D, RN);
	not (D__bar, D);
	and (adacond_NOT_D_AND_RN, D__bar, RN);
	and (adacond_D_AND_NOT_RT, D, RT__bar);
	and (adacond_CK_AND_NOT_RT, CK, RT__bar);
	not (CK__bar, CK);
	and (adacond_NOT_CK_AND_D_AND_NOT_RT, CK__bar, D, RT__bar);
	and (adacond_NOT_CK_AND_NOT_D_AND_NOT_RT, CK__bar, D__bar, RT__bar);
	and (adacond_D_AND_RN_AND_NOT_RT, D, RN, RT__bar);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT, D__bar, RN, RT__bar);

	specify
		ifnone (RT => Q) = 0;
		if ((CK&&RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CK&&!RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CK&&!RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CK&&!RT))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CK&&D&&!RT))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CK&&!D&&!RT))
			(negedge RN => (Q+:1'b0)) = 0;
		(posedge CK => (Q+:((D && !RT)))) = 0;
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT, posedge D &&& adacond_RN_AND_NOT_RT, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT, negedge D &&& adacond_RN_AND_NOT_RT, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (negedge CK &&& adacond_D_AND_RN, negedge RT &&& adacond_D_AND_RN, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (negedge CK &&& adacond_NOT_D_AND_RN, negedge RT &&& adacond_NOT_D_AND_RN, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$recovery (posedge RN &&& adacond_D_AND_NOT_RT, posedge CK &&& adacond_D_AND_NOT_RT, 0, notifier);
		$hold (posedge CK &&& adacond_D_AND_NOT_RT, posedge RN &&& adacond_D_AND_NOT_RT, 0, notifier);
		$width (negedge RN &&& adacond_CK_AND_NOT_RT, 0, 0, notifier);
		$width (negedge RN &&& adacond_NOT_CK_AND_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge RN &&& adacond_NOT_CK_AND_NOT_D_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CK &&& adacond_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (negedge CK &&& adacond_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (negedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RDFFRX1 (Q, QN, D, RT, RN, CK);
	output Q, QN;
	input D, RT, RN, CK;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_CK;

	// Function
	wire delayed_RT__bar, int_fwire_d, int_fwire_IQ;
	wire int_fwire_IQN, int_fwire_r, xcr_0;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, delayed_D);
	not (int_fwire_r, RN);
	altos_dff_r_err (xcr_0, delayed_CK, int_fwire_d, int_fwire_r);
	altos_dff_r (int_fwire_IQ, notifier, delayed_CK, int_fwire_d, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_CK_AND_NOT_RT, adacond_D_AND_NOT_RT, adacond_D_AND_RN;
	wire adacond_D_AND_RN_AND_NOT_RT, adacond_NOT_CK_AND_D_AND_NOT_RT, adacond_NOT_CK_AND_NOT_D_AND_NOT_RT;
	wire adacond_NOT_D_AND_RN, adacond_NOT_D_AND_RN_AND_NOT_RT, adacond_RN_AND_NOT_RT;
	wire CK__bar, D__bar, RT__bar;


	// Additional timing gates
	not (RT__bar, RT);
	and (adacond_RN_AND_NOT_RT, RN, RT__bar);
	and (adacond_D_AND_RN, D, RN);
	not (D__bar, D);
	and (adacond_NOT_D_AND_RN, D__bar, RN);
	and (adacond_D_AND_NOT_RT, D, RT__bar);
	and (adacond_CK_AND_NOT_RT, CK, RT__bar);
	not (CK__bar, CK);
	and (adacond_NOT_CK_AND_D_AND_NOT_RT, CK__bar, D, RT__bar);
	and (adacond_NOT_CK_AND_NOT_D_AND_NOT_RT, CK__bar, D__bar, RT__bar);
	and (adacond_D_AND_RN_AND_NOT_RT, D, RN, RT__bar);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT, D__bar, RN, RT__bar);

	specify
		ifnone (RT => Q) = 0;
		if ((CK&&RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CK&&!RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CK&&!RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CK&&!RT))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CK&&D&&!RT))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CK&&!D&&!RT))
			(negedge RN => (Q+:1'b0)) = 0;
		(posedge CK => (Q+:((D && !RT)))) = 0;
		if ((CK&&RN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((CK&&!RN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((!CK&&!RN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((CK&&!RT))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((!CK&&D&&!RT))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((!CK&&!D&&!RT))
			(negedge RN => (QN-:1'b0)) = 0;
		(posedge CK => (QN-:((D && !RT)))) = 0;
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT, posedge D &&& adacond_RN_AND_NOT_RT, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT, negedge D &&& adacond_RN_AND_NOT_RT, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (negedge CK &&& adacond_D_AND_RN, negedge RT &&& adacond_D_AND_RN, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (negedge CK &&& adacond_NOT_D_AND_RN, negedge RT &&& adacond_NOT_D_AND_RN, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$recovery (posedge RN &&& adacond_D_AND_NOT_RT, posedge CK &&& adacond_D_AND_NOT_RT, 0, notifier);
		$hold (posedge CK &&& adacond_D_AND_NOT_RT, posedge RN &&& adacond_D_AND_NOT_RT, 0, notifier);
		$width (negedge RN &&& adacond_CK_AND_NOT_RT, 0, 0, notifier);
		$width (negedge RN &&& adacond_NOT_CK_AND_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge RN &&& adacond_NOT_CK_AND_NOT_D_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CK &&& adacond_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (negedge CK &&& adacond_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (negedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RDFFSQX1 (Q, D, RT, SN, CK);
	output Q;
	input D, RT, SN, CK;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_CK;

	// Function
	wire delayed_RT__bar, int_fwire_d, int_fwire_IQ;
	wire int_fwire_s, xcr_0;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, delayed_D);
	not (int_fwire_s, SN);
	altos_dff_s_err (xcr_0, delayed_CK, int_fwire_d, int_fwire_s);
	altos_dff_s (int_fwire_IQ, notifier, delayed_CK, int_fwire_d, int_fwire_s, xcr_0);
	buf (Q, int_fwire_IQ);

	// Timing

	// Additional timing wires
	wire adacond_CK_AND_NOT_RT, adacond_D_AND_NOT_RT_AND_SN, adacond_D_AND_SN;
	wire adacond_NOT_CK_AND_D_AND_NOT_RT, adacond_NOT_CK_AND_NOT_D_AND_NOT_RT, adacond_NOT_D_AND_NOT_RT;
	wire adacond_NOT_D_AND_NOT_RT_AND_SN, adacond_NOT_D_AND_SN, adacond_NOT_RT_AND_SN;
	wire CK__bar, D__bar, RT__bar;


	// Additional timing gates
	not (RT__bar, RT);
	and (adacond_NOT_RT_AND_SN, RT__bar, SN);
	and (adacond_D_AND_SN, D, SN);
	not (D__bar, D);
	and (adacond_NOT_D_AND_SN, D__bar, SN);
	and (adacond_NOT_D_AND_NOT_RT, D__bar, RT__bar);
	and (adacond_CK_AND_NOT_RT, CK, RT__bar);
	not (CK__bar, CK);
	and (adacond_NOT_CK_AND_D_AND_NOT_RT, CK__bar, D, RT__bar);
	and (adacond_NOT_CK_AND_NOT_D_AND_NOT_RT, CK__bar, D__bar, RT__bar);
	and (adacond_D_AND_NOT_RT_AND_SN, D, RT__bar, SN);
	and (adacond_NOT_D_AND_NOT_RT_AND_SN, D__bar, RT__bar, SN);

	specify
		if ((CK&&SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CK&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CK&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CK&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&D&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&!D&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		(posedge CK => (Q+:((D && !RT)))) = 0;
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_SN, posedge D &&& adacond_NOT_RT_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_SN, negedge D &&& adacond_NOT_RT_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (negedge CK &&& adacond_D_AND_SN, negedge RT &&& adacond_D_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (negedge CK &&& adacond_NOT_D_AND_SN, negedge RT &&& adacond_NOT_D_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$recovery (posedge SN &&& adacond_NOT_D_AND_NOT_RT, posedge CK &&& adacond_NOT_D_AND_NOT_RT, 0, notifier);
		$hold (posedge CK &&& adacond_NOT_D_AND_NOT_RT, posedge SN &&& adacond_NOT_D_AND_NOT_RT, 0, notifier);
		$width (negedge SN &&& adacond_CK_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_NOT_CK_AND_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_NOT_CK_AND_NOT_D_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CK &&& adacond_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge CK &&& adacond_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (posedge CK &&& adacond_NOT_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge CK &&& adacond_NOT_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RDFFSRQX1 (Q, D, RT, RN, SN, CK);
	output Q;
	input D, RT, RN, SN, CK;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_RN, delayed_SN, delayed_CK;

	// Function
	wire delayed_RT__bar, int_fwire_d, int_fwire_IQ;
	wire int_fwire_r, int_fwire_s, xcr_0;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, delayed_D);
	not (int_fwire_s, delayed_SN);
	not (int_fwire_r, delayed_RN);
	altos_dff_sr_err (xcr_0, delayed_CK, int_fwire_d, int_fwire_s, int_fwire_r);
	altos_dff_sr_1 (int_fwire_IQ, notifier, delayed_CK, int_fwire_d, int_fwire_s, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);

	// Timing

	// Additional timing wires
	wire adacond_CK_AND_NOT_RT, adacond_CK_AND_NOT_RT_AND_SN, adacond_CK_AND_RN_AND_NOT_RT;
	wire adacond_D_AND_NOT_RT_AND_SN, adacond_D_AND_RN_AND_NOT_RT_AND_SN, adacond_D_AND_RN_AND_SN;
	wire adacond_NOT_CK_AND_D_AND_NOT_RT, adacond_NOT_CK_AND_D_AND_NOT_RT_AND_SN, adacond_NOT_CK_AND_D_AND_RN_AND_NOT_RT;
	wire adacond_NOT_CK_AND_NOT_D_AND_NOT_RT, adacond_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SN, adacond_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT;
	wire adacond_NOT_D_AND_RN_AND_NOT_RT, adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, adacond_NOT_D_AND_RN_AND_SN;
	wire adacond_RN_AND_NOT_RT_AND_SN, CK__bar, D__bar;
	wire RT__bar;


	// Additional timing gates
	not (RT__bar, RT);
	and (adacond_RN_AND_NOT_RT_AND_SN, RN, RT__bar, SN);
	and (adacond_D_AND_RN_AND_SN, D, RN, SN);
	not (D__bar, D);
	and (adacond_NOT_D_AND_RN_AND_SN, D__bar, RN, SN);
	and (adacond_D_AND_NOT_RT_AND_SN, D, RT__bar, SN);
	and (adacond_CK_AND_NOT_RT_AND_SN, CK, RT__bar, SN);
	not (CK__bar, CK);
	and (adacond_NOT_CK_AND_D_AND_NOT_RT_AND_SN, CK__bar, D, RT__bar, SN);
	and (adacond_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SN, CK__bar, D__bar, RT__bar, SN);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT, D__bar, RN, RT__bar);
	and (adacond_CK_AND_NOT_RT, CK, RT__bar);
	and (adacond_NOT_CK_AND_D_AND_NOT_RT, CK__bar, D, RT__bar);
	and (adacond_NOT_CK_AND_NOT_D_AND_NOT_RT, CK__bar, D__bar, RT__bar);
	and (adacond_CK_AND_RN_AND_NOT_RT, CK, RN, RT__bar);
	and (adacond_NOT_CK_AND_D_AND_RN_AND_NOT_RT, CK__bar, D, RN, RT__bar);
	and (adacond_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT, CK__bar, D__bar, RN, RT__bar);
	and (adacond_D_AND_RN_AND_NOT_RT_AND_SN, D, RN, RT__bar, SN);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, D__bar, RN, RT__bar, SN);

	specify
		if ((CK&&RN&&SN))
			(RT => Q) = 0;
		if ((CK&&!RN&&SN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CK&&!RN&&SN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CK&&RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CK&&!RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CK&&RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CK&&!RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CK&&!RT&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CK&&D&&!RT&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CK&&!D&&!RT&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((CK&&!RN&&!RT))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((!CK&&D&&!RN&&!RT))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((!CK&&!D&&!RN&&!RT))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((CK&&RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CK&&!RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&D&&RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&D&&!RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&!D&&RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&!D&&!RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		(posedge CK => (Q+:((D && !RT)))) = 0;
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_SN, posedge D &&& adacond_RN_AND_NOT_RT_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_SN, negedge D &&& adacond_RN_AND_NOT_RT_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (negedge CK &&& adacond_D_AND_RN_AND_SN, negedge RT &&& adacond_D_AND_RN_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (negedge CK &&& adacond_NOT_D_AND_RN_AND_SN, negedge RT &&& adacond_NOT_D_AND_RN_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (posedge RN &&& adacond_CK_AND_NOT_RT, posedge SN &&& adacond_CK_AND_NOT_RT, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$setuphold (posedge RN &&& adacond_NOT_CK_AND_D_AND_NOT_RT, posedge SN &&& adacond_NOT_CK_AND_D_AND_NOT_RT, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$setuphold (posedge RN &&& adacond_NOT_CK_AND_NOT_D_AND_NOT_RT, posedge SN &&& adacond_NOT_CK_AND_NOT_D_AND_NOT_RT, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$recovery (posedge RN &&& adacond_D_AND_NOT_RT_AND_SN, posedge CK &&& adacond_D_AND_NOT_RT_AND_SN, 0, notifier);
		$hold (posedge CK &&& adacond_D_AND_NOT_RT_AND_SN, posedge RN &&& adacond_D_AND_NOT_RT_AND_SN, 0, notifier);
		$recovery (posedge SN &&& adacond_NOT_D_AND_RN_AND_NOT_RT, posedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, notifier);
		$hold (posedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT, posedge SN &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, notifier);
		$width (negedge RN &&& adacond_CK_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge RN &&& adacond_NOT_CK_AND_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge RN &&& adacond_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge SN &&& adacond_CK_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_NOT_CK_AND_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CK &&& adacond_D_AND_RN_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge CK &&& adacond_D_AND_RN_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (posedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RDFFSRX1 (Q, QN, D, RT, RN, SN, CK);
	output Q, QN;
	input D, RT, RN, SN, CK;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_RN, delayed_SN, delayed_CK;

	// Function
	wire delayed_RT__bar, int_fwire_d, int_fwire_IQ;
	wire int_fwire_IQN, int_fwire_r, int_fwire_s;
	wire xcr_0;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, delayed_D);
	not (int_fwire_s, delayed_SN);
	not (int_fwire_r, delayed_RN);
	altos_dff_sr_err (xcr_0, delayed_CK, int_fwire_d, int_fwire_s, int_fwire_r);
	altos_dff_sr_1 (int_fwire_IQ, notifier, delayed_CK, int_fwire_d, int_fwire_s, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_CK_AND_NOT_RT, adacond_CK_AND_NOT_RT_AND_SN, adacond_CK_AND_RN_AND_NOT_RT;
	wire adacond_D_AND_NOT_RT_AND_SN, adacond_D_AND_RN_AND_NOT_RT_AND_SN, adacond_D_AND_RN_AND_SN;
	wire adacond_NOT_CK_AND_D_AND_NOT_RT, adacond_NOT_CK_AND_D_AND_NOT_RT_AND_SN, adacond_NOT_CK_AND_D_AND_RN_AND_NOT_RT;
	wire adacond_NOT_CK_AND_NOT_D_AND_NOT_RT, adacond_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SN, adacond_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT;
	wire adacond_NOT_D_AND_RN_AND_NOT_RT, adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, adacond_NOT_D_AND_RN_AND_SN;
	wire adacond_RN_AND_NOT_RT_AND_SN, CK__bar, D__bar;
	wire RT__bar;


	// Additional timing gates
	not (RT__bar, RT);
	and (adacond_RN_AND_NOT_RT_AND_SN, RN, RT__bar, SN);
	and (adacond_D_AND_RN_AND_SN, D, RN, SN);
	not (D__bar, D);
	and (adacond_NOT_D_AND_RN_AND_SN, D__bar, RN, SN);
	and (adacond_D_AND_NOT_RT_AND_SN, D, RT__bar, SN);
	and (adacond_CK_AND_NOT_RT_AND_SN, CK, RT__bar, SN);
	not (CK__bar, CK);
	and (adacond_NOT_CK_AND_D_AND_NOT_RT_AND_SN, CK__bar, D, RT__bar, SN);
	and (adacond_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SN, CK__bar, D__bar, RT__bar, SN);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT, D__bar, RN, RT__bar);
	and (adacond_CK_AND_NOT_RT, CK, RT__bar);
	and (adacond_NOT_CK_AND_D_AND_NOT_RT, CK__bar, D, RT__bar);
	and (adacond_NOT_CK_AND_NOT_D_AND_NOT_RT, CK__bar, D__bar, RT__bar);
	and (adacond_CK_AND_RN_AND_NOT_RT, CK, RN, RT__bar);
	and (adacond_NOT_CK_AND_D_AND_RN_AND_NOT_RT, CK__bar, D, RN, RT__bar);
	and (adacond_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT, CK__bar, D__bar, RN, RT__bar);
	and (adacond_D_AND_RN_AND_NOT_RT_AND_SN, D, RN, RT__bar, SN);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, D__bar, RN, RT__bar, SN);

	specify
		if ((CK&&RN&&SN))
			(RT => Q) = 0;
		if ((CK&&!RN&&SN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CK&&!RN&&SN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CK&&RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CK&&!RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CK&&RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CK&&!RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CK&&!RT&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CK&&D&&!RT&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CK&&!D&&!RT&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((CK&&!RN&&!RT))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((!CK&&D&&!RN&&!RT))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((!CK&&!D&&!RN&&!RT))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((CK&&RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CK&&!RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&D&&RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&D&&!RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&!D&&RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&!D&&!RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		(posedge CK => (Q+:((D && !RT)))) = 0;
		if ((CK&&RN&&SN))
			(RT => QN) = 0;
		if ((CK&&RN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((CK&&!RN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((!CK&&RN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((!CK&&!RN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((CK&&!RN&&SN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((!CK&&!RN&&SN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((CK&&!RT&&SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((!CK&&D&&!RT&&SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((!CK&&!D&&!RT&&SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((CK&&RN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((CK&&!RN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!CK&&D&&RN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!CK&&D&&!RN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!CK&&!D&&RN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!CK&&!D&&!RN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((CK&&!RN&&!RT))
			(posedge SN => (QN-:1'b0)) = 0;
		if ((!CK&&D&&!RN&&!RT))
			(posedge SN => (QN-:1'b0)) = 0;
		if ((!CK&&!D&&!RN&&!RT))
			(posedge SN => (QN-:1'b0)) = 0;
		(posedge CK => (QN-:((D && !RT)))) = 0;
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_SN, posedge D &&& adacond_RN_AND_NOT_RT_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_SN, negedge D &&& adacond_RN_AND_NOT_RT_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (negedge CK &&& adacond_D_AND_RN_AND_SN, negedge RT &&& adacond_D_AND_RN_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (negedge CK &&& adacond_NOT_D_AND_RN_AND_SN, negedge RT &&& adacond_NOT_D_AND_RN_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (posedge RN &&& adacond_CK_AND_NOT_RT, posedge SN &&& adacond_CK_AND_NOT_RT, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$setuphold (posedge RN &&& adacond_NOT_CK_AND_D_AND_NOT_RT, posedge SN &&& adacond_NOT_CK_AND_D_AND_NOT_RT, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$setuphold (posedge RN &&& adacond_NOT_CK_AND_NOT_D_AND_NOT_RT, posedge SN &&& adacond_NOT_CK_AND_NOT_D_AND_NOT_RT, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$recovery (posedge RN &&& adacond_D_AND_NOT_RT_AND_SN, posedge CK &&& adacond_D_AND_NOT_RT_AND_SN, 0, notifier);
		$hold (posedge CK &&& adacond_D_AND_NOT_RT_AND_SN, posedge RN &&& adacond_D_AND_NOT_RT_AND_SN, 0, notifier);
		$recovery (posedge SN &&& adacond_NOT_D_AND_RN_AND_NOT_RT, posedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, notifier);
		$hold (posedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT, posedge SN &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, notifier);
		$width (negedge RN &&& adacond_CK_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge RN &&& adacond_NOT_CK_AND_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge RN &&& adacond_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge SN &&& adacond_CK_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_NOT_CK_AND_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CK &&& adacond_D_AND_RN_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge CK &&& adacond_D_AND_RN_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (posedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RDFFSX1 (Q, QN, D, RT, SN, CK);
	output Q, QN;
	input D, RT, SN, CK;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_CK;

	// Function
	wire delayed_RT__bar, int_fwire_d, int_fwire_IQ;
	wire int_fwire_IQN, int_fwire_s, xcr_0;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, delayed_D);
	not (int_fwire_s, SN);
	altos_dff_s_err (xcr_0, delayed_CK, int_fwire_d, int_fwire_s);
	altos_dff_s (int_fwire_IQ, notifier, delayed_CK, int_fwire_d, int_fwire_s, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_CK_AND_NOT_RT, adacond_D_AND_NOT_RT_AND_SN, adacond_D_AND_SN;
	wire adacond_NOT_CK_AND_D_AND_NOT_RT, adacond_NOT_CK_AND_NOT_D_AND_NOT_RT, adacond_NOT_D_AND_NOT_RT;
	wire adacond_NOT_D_AND_NOT_RT_AND_SN, adacond_NOT_D_AND_SN, adacond_NOT_RT_AND_SN;
	wire CK__bar, D__bar, RT__bar;


	// Additional timing gates
	not (RT__bar, RT);
	and (adacond_NOT_RT_AND_SN, RT__bar, SN);
	and (adacond_D_AND_SN, D, SN);
	not (D__bar, D);
	and (adacond_NOT_D_AND_SN, D__bar, SN);
	and (adacond_NOT_D_AND_NOT_RT, D__bar, RT__bar);
	and (adacond_CK_AND_NOT_RT, CK, RT__bar);
	not (CK__bar, CK);
	and (adacond_NOT_CK_AND_D_AND_NOT_RT, CK__bar, D, RT__bar);
	and (adacond_NOT_CK_AND_NOT_D_AND_NOT_RT, CK__bar, D__bar, RT__bar);
	and (adacond_D_AND_NOT_RT_AND_SN, D, RT__bar, SN);
	and (adacond_NOT_D_AND_NOT_RT_AND_SN, D__bar, RT__bar, SN);

	specify
		if ((CK&&SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CK&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CK&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CK&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&D&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&!D&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		(posedge CK => (Q+:((D && !RT)))) = 0;
		ifnone (RT => QN) = 0;
		if ((CK&&SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((CK&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((!CK&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((CK&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!CK&&D&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!CK&&!D&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		(posedge CK => (QN-:((D && !RT)))) = 0;
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_SN, posedge D &&& adacond_NOT_RT_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_SN, negedge D &&& adacond_NOT_RT_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (negedge CK &&& adacond_D_AND_SN, negedge RT &&& adacond_D_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (negedge CK &&& adacond_NOT_D_AND_SN, negedge RT &&& adacond_NOT_D_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$recovery (posedge SN &&& adacond_NOT_D_AND_NOT_RT, posedge CK &&& adacond_NOT_D_AND_NOT_RT, 0, notifier);
		$hold (posedge CK &&& adacond_NOT_D_AND_NOT_RT, posedge SN &&& adacond_NOT_D_AND_NOT_RT, 0, notifier);
		$width (negedge SN &&& adacond_CK_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_NOT_CK_AND_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_NOT_CK_AND_NOT_D_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CK &&& adacond_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge CK &&& adacond_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (posedge CK &&& adacond_NOT_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge CK &&& adacond_NOT_D_AND_NOT_RT_AND_SN, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RDFFX1 (Q, QN, D, RT, CK);
	output Q, QN;
	input D, RT, CK;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_CK;

	// Function
	wire delayed_RT__bar, int_fwire_d, int_fwire_IQ;
	wire int_fwire_IQN, xcr_0;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, delayed_D);
	altos_dff_err (xcr_0, delayed_CK, int_fwire_d);
	altos_dff (int_fwire_IQ, notifier, delayed_CK, int_fwire_d, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_D, adacond_D_AND_NOT_RT, adacond_NOT_D;
	wire adacond_NOT_D_AND_NOT_RT, adacond_NOT_RT;


	// Additional timing gates
	not (adacond_NOT_RT, RT);
	buf (adacond_D, D);
	not (adacond_NOT_D, D);
	and (adacond_D_AND_NOT_RT, D, adacond_NOT_RT);
	and (adacond_NOT_D_AND_NOT_RT, adacond_NOT_D, adacond_NOT_RT);

	specify
		(RT => Q) = 0;
		(posedge CK => (Q+:((D && !RT)))) = 0;
		(RT => QN) = 0;
		(posedge CK => (QN-:((D && !RT)))) = 0;
		$setuphold (posedge CK &&& adacond_NOT_RT, posedge D &&& adacond_NOT_RT, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (posedge CK &&& adacond_NOT_RT, negedge D &&& adacond_NOT_RT, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (negedge CK &&& adacond_D, negedge RT &&& adacond_D, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (negedge CK &&& adacond_NOT_D, negedge RT &&& adacond_NOT_D, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$width (posedge CK &&& adacond_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge CK &&& adacond_D_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CK &&& adacond_NOT_D_AND_NOT_RT, 0, 0, notifier);
		$width (negedge CK &&& adacond_NOT_D_AND_NOT_RT, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RTLATRX1 (Q, QN, D, RT, RN, G);
	output Q, QN;
	input D, RT, RN, G;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_G;

	// Function
	wire delayed_RT__bar, int_fwire_d, int_fwire_IQ;
	wire int_fwire_IQN, int_fwire_r;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_D, delayed_RT__bar);
	not (int_fwire_r, RN);
	altos_latch_r (int_fwire_IQ, notifier, delayed_G, int_fwire_d, int_fwire_r);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_D_AND_NOT_RT, adacond_D_AND_RN, adacond_D_AND_RN_AND_NOT_RT;
	wire adacond_NOT_D_AND_RN, adacond_NOT_D_AND_RN_AND_NOT_RT, adacond_NOT_G_AND_NOT_RT;
	wire adacond_RN_AND_NOT_RT, D__bar, G__bar;
	wire RT__bar;


	// Additional timing gates
	not (RT__bar, RT);
	and (adacond_RN_AND_NOT_RT, RN, RT__bar);
	and (adacond_D_AND_RN, D, RN);
	not (D__bar, D);
	and (adacond_NOT_D_AND_RN, D__bar, RN);
	and (adacond_D_AND_NOT_RT, D, RT__bar);
	not (G__bar, G);
	and (adacond_NOT_G_AND_NOT_RT, G__bar, RT__bar);
	and (adacond_D_AND_RN_AND_NOT_RT, D, RN, RT__bar);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT, D__bar, RN, RT__bar);

	specify
		(D => Q) = 0;
		ifnone (RT => Q) = 0;
		if ((!D&&G&&RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if (!RN)
			(negedge RT => (Q+:1'b0)) = 0;
		if ((D&&G&&!RT))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!G&&!RT))
			(negedge RN => (Q+:1'b0)) = 0;
		(posedge RN => (Q+:1'b1)) = 0;
		(posedge G => (Q+:((D && !RT)))) = 0;
		(D => QN) = 0;
		if ((!D&&G&&RN))
			(negedge RT => (QN+:1'b1)) = 0;
		if (!RN)
			(negedge RT => (QN+:1'b1)) = 0;
		(posedge RN => (QN-:1'b1)) = 0;
		if ((D&&G&&!RT))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((!G&&!RT))
			(negedge RN => (QN-:1'b0)) = 0;
		(posedge G => (QN-:((D && !RT)))) = 0;
		$setuphold (negedge G &&& adacond_RN_AND_NOT_RT, posedge D &&& adacond_RN_AND_NOT_RT, 0, 0, notifier,,, delayed_G, delayed_D);
		$setuphold (negedge G &&& adacond_RN_AND_NOT_RT, negedge D &&& adacond_RN_AND_NOT_RT, 0, 0, notifier,,, delayed_G, delayed_D);
		$setuphold (negedge G &&& adacond_D_AND_RN, negedge RT &&& adacond_D_AND_RN, 0, 0, notifier,,, delayed_G, delayed_RT);
		$setuphold (negedge G &&& adacond_NOT_D_AND_RN, negedge RT &&& adacond_NOT_D_AND_RN, 0, 0, notifier,,, delayed_G, delayed_RT);
		$recovery (posedge RN &&& adacond_D_AND_NOT_RT, negedge G &&& adacond_D_AND_NOT_RT, 0, notifier);
		$hold (negedge G &&& adacond_D_AND_NOT_RT, posedge RN &&& adacond_D_AND_NOT_RT, 0, notifier);
		$width (negedge RN &&& adacond_NOT_G_AND_NOT_RT, 0, 0, notifier);
		$width (posedge G &&& adacond_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge G &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RTLATSRX1 (Q, QN, D, RT, RN, SN, G);
	output Q, QN;
	input D, RT, RN, SN, G;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_RN, delayed_SN, delayed_G;

	// Function
	wire delayed_RT__bar, int_fwire_d, int_fwire_IQ;
	wire int_fwire_IQN, int_fwire_r, int_fwire_s;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_D, delayed_RT__bar);
	not (int_fwire_s, delayed_SN);
	not (int_fwire_r, delayed_RN);
	altos_latch_sr_1 (int_fwire_IQ, notifier, delayed_G, int_fwire_d, int_fwire_s, int_fwire_r);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_D_AND_NOT_RT_AND_SN, adacond_D_AND_RN_AND_NOT_RT_AND_SN, adacond_D_AND_RN_AND_SN;
	wire adacond_NOT_D_AND_RN_AND_NOT_RT, adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, adacond_NOT_D_AND_RN_AND_SN;
	wire adacond_NOT_G_AND_NOT_RT, adacond_NOT_G_AND_NOT_RT_AND_SN, adacond_NOT_G_AND_RN_AND_NOT_RT;
	wire adacond_NOT_G_AND_RN_AND_RT, adacond_OP_G_AND_RT_CP_OR_OP_NOT_G_AND_NOT_RN_AND_RT_CP, adacond_RN_AND_NOT_RT_AND_SN;
	wire D__bar, G__bar, int_twire_0;
	wire int_twire_1, RN__bar, RT__bar;


	// Additional timing gates
	not (RT__bar, RT);
	and (adacond_RN_AND_NOT_RT_AND_SN, RN, RT__bar, SN);
	and (adacond_D_AND_RN_AND_SN, D, RN, SN);
	not (D__bar, D);
	and (adacond_NOT_D_AND_RN_AND_SN, D__bar, RN, SN);
	and (adacond_D_AND_NOT_RT_AND_SN, D, RT__bar, SN);
	not (G__bar, G);
	and (adacond_NOT_G_AND_NOT_RT_AND_SN, G__bar, RT__bar, SN);
	and (adacond_NOT_G_AND_NOT_RT, G__bar, RT__bar);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT, D__bar, RN, RT__bar);
	not (RN__bar, RN);
	and (int_twire_0, G__bar, RN__bar, RT);
	and (int_twire_1, G, RT);
	or (adacond_OP_G_AND_RT_CP_OR_OP_NOT_G_AND_NOT_RN_AND_RT_CP, int_twire_1, int_twire_0);
	and (adacond_NOT_G_AND_RN_AND_RT, G__bar, RN, RT);
	and (adacond_NOT_G_AND_RN_AND_NOT_RT, G__bar, RN, RT__bar);
	and (adacond_D_AND_RN_AND_NOT_RT_AND_SN, D, RN, RT__bar, SN);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, D__bar, RN, RT__bar, SN);

	specify
		(D => Q) = 0;
		ifnone (RT => Q) = 0;
		if ((!RN&&SN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!D&&G&&RN&&SN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((D&&G&&!RT&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!G&&!RT&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		(posedge RN => (Q+:1'b1)) = 0;
		(posedge SN => (Q+:1'b0)) = 0;
		if ((G&&RT) | (!G&&!RN&&RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((D&&!RN&&!RT) | (!D&&G&&!RT) | (!D&&!G&&!RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!G&&RN&&RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!G&&RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		(posedge G => (Q+:((D && !RT)))) = 0;
		(D => QN) = 0;
		if ((!RN&&SN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((!D&&G&&RN&&SN))
			(negedge RT => (QN+:1'b1)) = 0;
		(posedge RN => (QN-:1'b1)) = 0;
		if ((D&&G&&!RT&&SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((!G&&!RT&&SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((G&&RT) | (!G&&!RN&&RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((D&&!RN&&!RT) | (!D&&G&&!RT) | (!D&&!G&&!RN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!G&&RN&&RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!G&&RN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		(posedge SN => (QN-:1'b0)) = 0;
		(posedge G => (QN-:((D && !RT)))) = 0;
		$setuphold (negedge G &&& adacond_RN_AND_NOT_RT_AND_SN, posedge D &&& adacond_RN_AND_NOT_RT_AND_SN, 0, 0, notifier,,, delayed_G, delayed_D);
		$setuphold (negedge G &&& adacond_RN_AND_NOT_RT_AND_SN, negedge D &&& adacond_RN_AND_NOT_RT_AND_SN, 0, 0, notifier,,, delayed_G, delayed_D);
		$setuphold (negedge G &&& adacond_D_AND_RN_AND_SN, negedge RT &&& adacond_D_AND_RN_AND_SN, 0, 0, notifier,,, delayed_G, delayed_RT);
		$setuphold (negedge G &&& adacond_NOT_D_AND_RN_AND_SN, negedge RT &&& adacond_NOT_D_AND_RN_AND_SN, 0, 0, notifier,,, delayed_G, delayed_RT);
		$setuphold (posedge SN &&& adacond_NOT_G_AND_NOT_RT, posedge RN &&& adacond_NOT_G_AND_NOT_RT, 0, 0, notifier,,, delayed_SN, delayed_RN);
		$setuphold (posedge RN &&& adacond_NOT_G_AND_NOT_RT, posedge SN &&& adacond_NOT_G_AND_NOT_RT, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$recovery (posedge RN &&& adacond_D_AND_NOT_RT_AND_SN, negedge G &&& adacond_D_AND_NOT_RT_AND_SN, 0, notifier);
		$hold (negedge G &&& adacond_D_AND_NOT_RT_AND_SN, posedge RN &&& adacond_D_AND_NOT_RT_AND_SN, 0, notifier);
		$recovery (posedge SN &&& adacond_NOT_D_AND_RN_AND_NOT_RT, negedge G &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, notifier);
		$hold (negedge G &&& adacond_NOT_D_AND_RN_AND_NOT_RT, posedge SN &&& adacond_NOT_D_AND_RN_AND_NOT_RT, 0, notifier);
		$width (negedge RN &&& adacond_NOT_G_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge SN &&& adacond_OP_G_AND_RT_CP_OR_OP_NOT_G_AND_NOT_RN_AND_RT_CP, 0, 0, notifier);
		$width (negedge SN &&& adacond_NOT_G_AND_RN_AND_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_NOT_G_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge G &&& adacond_D_AND_RN_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (posedge G &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SN, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module RTLATX1 (Q, QN, D, RT, G);
	output Q, QN;
	input D, RT, G;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_G;

	// Function
	wire delayed_RT__bar, int_fwire_d, int_fwire_IQ;
	wire int_fwire_IQN;

	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_D, delayed_RT__bar);
	altos_latch (int_fwire_IQ, notifier, delayed_G, int_fwire_d);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_D, adacond_D_AND_NOT_RT, adacond_NOT_D;
	wire adacond_NOT_D_AND_NOT_RT, adacond_NOT_RT;


	// Additional timing gates
	not (adacond_NOT_RT, RT);
	buf (adacond_D, D);
	not (adacond_NOT_D, D);
	and (adacond_D_AND_NOT_RT, D, adacond_NOT_RT);
	and (adacond_NOT_D_AND_NOT_RT, adacond_NOT_D, adacond_NOT_RT);

	specify
		(D => Q) = 0;
		(RT => Q) = 0;
		(posedge G => (Q+:((D && !RT)))) = 0;
		(D => QN) = 0;
		(RT => QN) = 0;
		(posedge G => (QN-:((D && !RT)))) = 0;
		$setuphold (negedge G &&& adacond_NOT_RT, posedge D &&& adacond_NOT_RT, 0, 0, notifier,,, delayed_G, delayed_D);
		$setuphold (negedge G &&& adacond_NOT_RT, negedge D &&& adacond_NOT_RT, 0, 0, notifier,,, delayed_G, delayed_D);
		$setuphold (negedge G &&& adacond_D, negedge RT &&& adacond_D, 0, 0, notifier,,, delayed_G, delayed_RT);
		$setuphold (negedge G &&& adacond_NOT_D, negedge RT &&& adacond_NOT_D, 0, 0, notifier,,, delayed_G, delayed_RT);
		$width (posedge G &&& adacond_D_AND_NOT_RT, 0, 0, notifier);
		$width (posedge G &&& adacond_NOT_D_AND_NOT_RT, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module SRDFFNQX1 (Q, D, RT, SE, SI, CKN);
	output Q;
	input D, RT, SE, SI, CKN;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_SE, delayed_SI, delayed_CKN;

	// Function
	wire delayed_RT__bar, delayed_SE__bar, int_fwire_0;
	wire int_fwire_1, int_fwire_2, int_fwire_clk;
	wire int_fwire_d, int_fwire_IQ, xcr_0;

	not (delayed_SE__bar, delayed_SE);
	and (int_fwire_0, delayed_SE__bar, delayed_D);
	and (int_fwire_1, delayed_SE, delayed_SI);
	or (int_fwire_2, int_fwire_1, int_fwire_0);
	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, int_fwire_2);
	not (int_fwire_clk, delayed_CKN);
	altos_dff_err (xcr_0, int_fwire_clk, int_fwire_d);
	altos_dff (int_fwire_IQ, notifier, int_fwire_clk, int_fwire_d, xcr_0);
	buf (Q, int_fwire_IQ);

	// Timing

	// Additional timing wires
	wire adacond_D_AND_NOT_RT_AND_NOT_SI, adacond_NOT_D_AND_NOT_RT_AND_SI, adacond_NOT_RT_AND_NOT_SE;
	wire adacond_NOT_RT_AND_SE, adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP;
	wire adacond_OP_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_SE_CP, adacond_OP_D_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_SE_CP_OR_OP_NOT_D_AND_SE_AND_SI_CP, D__bar;
	wire int_twire_0, int_twire_1, int_twire_2;
	wire int_twire_3, int_twire_4, int_twire_5;
	wire int_twire_6, int_twire_7, int_twire_8;
	wire int_twire_9, int_twire_10, int_twire_11;
	wire RT__bar, SE__bar, SI__bar;


	// Additional timing gates
	not (SE__bar, SE);
	not (RT__bar, RT);
	and (adacond_NOT_RT_AND_NOT_SE, RT__bar, SE__bar);
	not (D__bar, D);
	and (int_twire_0, D__bar, SE, SI);
	and (int_twire_1, D, SE__bar);
	and (int_twire_2, D, SE, SI);
	or (adacond_OP_D_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_SE_CP_OR_OP_NOT_D_AND_SE_AND_SI_CP, int_twire_2, int_twire_1, int_twire_0);
	and (int_twire_3, D__bar, SE__bar);
	not (SI__bar, SI);
	and (int_twire_4, D__bar, SE, SI__bar);
	and (int_twire_5, D, SE, SI__bar);
	or (adacond_OP_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_SE_CP, int_twire_5, int_twire_4, int_twire_3);
	and (adacond_D_AND_NOT_RT_AND_NOT_SI, D, RT__bar, SI__bar);
	and (adacond_NOT_D_AND_NOT_RT_AND_SI, D__bar, RT__bar, SI);
	and (adacond_NOT_RT_AND_SE, RT__bar, SE);
	and (int_twire_6, D__bar, RT__bar, SE, SI);
	and (int_twire_7, D, RT__bar, SE__bar);
	and (int_twire_8, D, RT__bar, SE, SI);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_8, int_twire_7, int_twire_6);
	and (int_twire_9, D__bar, RT__bar, SE__bar);
	and (int_twire_10, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_11, D, RT__bar, SE, SI__bar);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_11, int_twire_10, int_twire_9);

	specify
		(RT => Q) = 0;
		(negedge CKN => (Q+:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_NOT_SE, posedge D &&& adacond_NOT_RT_AND_NOT_SE, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_NOT_SE, negedge D &&& adacond_NOT_RT_AND_NOT_SE, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (posedge CKN &&& adacond_OP_D_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_SE_CP_OR_OP_NOT_D_AND_SE_AND_SI_CP, negedge RT &&& adacond_OP_D_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_SE_CP_OR_OP_NOT_D_AND_SE_AND_SI_CP, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (posedge CKN &&& adacond_OP_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_SE_CP, negedge RT &&& adacond_OP_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_SE_CP, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (negedge CKN &&& adacond_D_AND_NOT_RT_AND_NOT_SI, posedge SE &&& adacond_D_AND_NOT_RT_AND_NOT_SI, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_D_AND_NOT_RT_AND_NOT_SI, negedge SE &&& adacond_D_AND_NOT_RT_AND_NOT_SI, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_D_AND_NOT_RT_AND_SI, posedge SE &&& adacond_NOT_D_AND_NOT_RT_AND_SI, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_D_AND_NOT_RT_AND_SI, negedge SE &&& adacond_NOT_D_AND_NOT_RT_AND_SI, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_SE, posedge SI &&& adacond_NOT_RT_AND_SE, 0, 0, notifier,,, delayed_CKN, delayed_SI);
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_SE, negedge SI &&& adacond_NOT_RT_AND_SE, 0, 0, notifier,,, delayed_CKN, delayed_SI);
		$width (posedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (posedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module SRDFFNRQX1 (Q, D, RT, SE, SI, RN, CKN);
	output Q;
	input D, RT, SE, SI, RN, CKN;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_SE, delayed_SI, delayed_CKN;

	// Function
	wire delayed_RT__bar, delayed_SE__bar, int_fwire_0;
	wire int_fwire_1, int_fwire_2, int_fwire_clk;
	wire int_fwire_d, int_fwire_IQ, int_fwire_r;
	wire xcr_0;

	not (delayed_SE__bar, delayed_SE);
	and (int_fwire_0, delayed_SE__bar, delayed_D);
	and (int_fwire_1, delayed_SE, delayed_SI);
	or (int_fwire_2, int_fwire_1, int_fwire_0);
	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, int_fwire_2);
	not (int_fwire_clk, delayed_CKN);
	not (int_fwire_r, RN);
	altos_dff_r_err (xcr_0, int_fwire_clk, int_fwire_d, int_fwire_r);
	altos_dff_r (int_fwire_IQ, notifier, int_fwire_clk, int_fwire_d, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);

	// Timing

	// Additional timing wires
	wire adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, adacond_NOT_CKN_AND_NOT_RT, adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI;
	wire adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP;
	wire adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_CP;
	wire adacond_OP_D_AND_RN_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_CP, adacond_RN_AND_NOT_RT_AND_NOT_SE, adacond_RN_AND_NOT_RT_AND_SE;
	wire CKN__bar, D__bar, int_twire_0;
	wire int_twire_1, int_twire_2, int_twire_3;
	wire int_twire_4, int_twire_5, int_twire_6;
	wire int_twire_7, int_twire_8, int_twire_9;
	wire int_twire_10, int_twire_11, int_twire_12;
	wire int_twire_13, int_twire_14, int_twire_15;
	wire int_twire_16, int_twire_17, int_twire_18;
	wire int_twire_19, int_twire_20, RT__bar;
	wire SE__bar, SI__bar;


	// Additional timing gates
	not (SE__bar, SE);
	not (RT__bar, RT);
	and (adacond_RN_AND_NOT_RT_AND_NOT_SE, RN, RT__bar, SE__bar);
	not (D__bar, D);
	and (int_twire_0, D__bar, RN, SE, SI);
	and (int_twire_1, D, RN, SE__bar);
	and (int_twire_2, D, RN, SE, SI);
	or (adacond_OP_D_AND_RN_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_CP, int_twire_2, int_twire_1, int_twire_0);
	and (int_twire_3, D__bar, RN, SE__bar);
	not (SI__bar, SI);
	and (int_twire_4, D__bar, RN, SE, SI__bar);
	and (int_twire_5, D, RN, SE, SI__bar);
	or (adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_CP, int_twire_5, int_twire_4, int_twire_3);
	and (adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, D, RN, RT__bar, SI__bar);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, D__bar, RN, RT__bar, SI);
	and (adacond_RN_AND_NOT_RT_AND_SE, RN, RT__bar, SE);
	and (int_twire_6, D__bar, RT__bar, SE, SI);
	and (int_twire_7, D, RT__bar, SE__bar);
	and (int_twire_8, D, RT__bar, SE, SI);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_8, int_twire_7, int_twire_6);
	and (int_twire_9, CKN, D__bar, RT__bar, SE, SI);
	and (int_twire_10, CKN, D, RT__bar, SE__bar);
	and (int_twire_11, CKN, D, RT__bar, SE, SI);
	or (adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_11, int_twire_10, int_twire_9);
	and (int_twire_12, CKN, D__bar, RT__bar, SE__bar);
	and (int_twire_13, CKN, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_14, CKN, D, RT__bar, SE, SI__bar);
	or (adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_14, int_twire_13, int_twire_12);
	not (CKN__bar, CKN);
	and (adacond_NOT_CKN_AND_NOT_RT, CKN__bar, RT__bar);
	and (int_twire_15, D__bar, RN, RT__bar, SE, SI);
	and (int_twire_16, D, RN, RT__bar, SE__bar);
	and (int_twire_17, D, RN, RT__bar, SE, SI);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_17, int_twire_16, int_twire_15);
	and (int_twire_18, D__bar, RN, RT__bar, SE__bar);
	and (int_twire_19, D__bar, RN, RT__bar, SE, SI__bar);
	and (int_twire_20, D, RN, RT__bar, SE, SI__bar);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, int_twire_20, int_twire_19, int_twire_18);

	specify
		ifnone (RT => Q) = 0;
		if ((CKN&&!RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CKN&&RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CKN&&!RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CKN&&D&&!RT&&SE&&SI) | (CKN&&D&&!RT&&!SE) | (CKN&&!D&&!RT&&SE&&SI))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((CKN&&D&&!RT&&SE&&!SI) | (CKN&&!D&&!RT&&SE&&!SI) | (CKN&&!D&&!RT&&!SE))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CKN&&!RT))
			(negedge RN => (Q+:1'b0)) = 0;
		(negedge CKN => (Q+:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_NOT_SE, posedge D &&& adacond_RN_AND_NOT_RT_AND_NOT_SE, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_NOT_SE, negedge D &&& adacond_RN_AND_NOT_RT_AND_NOT_SE, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (posedge CKN &&& adacond_OP_D_AND_RN_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_CP, negedge RT &&& adacond_OP_D_AND_RN_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_CP, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (posedge CKN &&& adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_CP, negedge RT &&& adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_CP, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (negedge CKN &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, posedge SE &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, negedge SE &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, posedge SE &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, negedge SE &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_SE, posedge SI &&& adacond_RN_AND_NOT_RT_AND_SE, 0, 0, notifier,,, delayed_CKN, delayed_SI);
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_SE, negedge SI &&& adacond_RN_AND_NOT_RT_AND_SE, 0, 0, notifier,,, delayed_CKN, delayed_SI);
		$recovery (posedge RN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, notifier);
		$hold (negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, posedge RN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, notifier);
		$width (negedge RN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge RN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (negedge RN &&& adacond_NOT_CKN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (posedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (negedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module SRDFFNRX1 (Q, QN, D, RT, SE, SI, RN, CKN);
	output Q, QN;
	input D, RT, SE, SI, RN, CKN;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_SE, delayed_SI, delayed_CKN;

	// Function
	wire delayed_RT__bar, delayed_SE__bar, int_fwire_0;
	wire int_fwire_1, int_fwire_2, int_fwire_clk;
	wire int_fwire_d, int_fwire_IQ, int_fwire_IQN;
	wire int_fwire_r, xcr_0;

	not (delayed_SE__bar, delayed_SE);
	and (int_fwire_0, delayed_SE__bar, delayed_D);
	and (int_fwire_1, delayed_SE, delayed_SI);
	or (int_fwire_2, int_fwire_1, int_fwire_0);
	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, int_fwire_2);
	not (int_fwire_clk, delayed_CKN);
	not (int_fwire_r, RN);
	altos_dff_r_err (xcr_0, int_fwire_clk, int_fwire_d, int_fwire_r);
	altos_dff_r (int_fwire_IQ, notifier, int_fwire_clk, int_fwire_d, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, adacond_NOT_CKN_AND_NOT_RT, adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI;
	wire adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP;
	wire adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_CP;
	wire adacond_OP_D_AND_RN_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_CP, adacond_RN_AND_NOT_RT_AND_NOT_SE, adacond_RN_AND_NOT_RT_AND_SE;
	wire CKN__bar, D__bar, int_twire_0;
	wire int_twire_1, int_twire_2, int_twire_3;
	wire int_twire_4, int_twire_5, int_twire_6;
	wire int_twire_7, int_twire_8, int_twire_9;
	wire int_twire_10, int_twire_11, int_twire_12;
	wire int_twire_13, int_twire_14, int_twire_15;
	wire int_twire_16, int_twire_17, int_twire_18;
	wire int_twire_19, int_twire_20, RT__bar;
	wire SE__bar, SI__bar;


	// Additional timing gates
	not (SE__bar, SE);
	not (RT__bar, RT);
	and (adacond_RN_AND_NOT_RT_AND_NOT_SE, RN, RT__bar, SE__bar);
	not (D__bar, D);
	and (int_twire_0, D__bar, RN, SE, SI);
	and (int_twire_1, D, RN, SE__bar);
	and (int_twire_2, D, RN, SE, SI);
	or (adacond_OP_D_AND_RN_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_CP, int_twire_2, int_twire_1, int_twire_0);
	and (int_twire_3, D__bar, RN, SE__bar);
	not (SI__bar, SI);
	and (int_twire_4, D__bar, RN, SE, SI__bar);
	and (int_twire_5, D, RN, SE, SI__bar);
	or (adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_CP, int_twire_5, int_twire_4, int_twire_3);
	and (adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, D, RN, RT__bar, SI__bar);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, D__bar, RN, RT__bar, SI);
	and (adacond_RN_AND_NOT_RT_AND_SE, RN, RT__bar, SE);
	and (int_twire_6, D__bar, RT__bar, SE, SI);
	and (int_twire_7, D, RT__bar, SE__bar);
	and (int_twire_8, D, RT__bar, SE, SI);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_8, int_twire_7, int_twire_6);
	and (int_twire_9, CKN, D__bar, RT__bar, SE, SI);
	and (int_twire_10, CKN, D, RT__bar, SE__bar);
	and (int_twire_11, CKN, D, RT__bar, SE, SI);
	or (adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_11, int_twire_10, int_twire_9);
	and (int_twire_12, CKN, D__bar, RT__bar, SE__bar);
	and (int_twire_13, CKN, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_14, CKN, D, RT__bar, SE, SI__bar);
	or (adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_14, int_twire_13, int_twire_12);
	not (CKN__bar, CKN);
	and (adacond_NOT_CKN_AND_NOT_RT, CKN__bar, RT__bar);
	and (int_twire_15, D__bar, RN, RT__bar, SE, SI);
	and (int_twire_16, D, RN, RT__bar, SE__bar);
	and (int_twire_17, D, RN, RT__bar, SE, SI);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_17, int_twire_16, int_twire_15);
	and (int_twire_18, D__bar, RN, RT__bar, SE__bar);
	and (int_twire_19, D__bar, RN, RT__bar, SE, SI__bar);
	and (int_twire_20, D, RN, RT__bar, SE, SI__bar);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, int_twire_20, int_twire_19, int_twire_18);

	specify
		ifnone (RT => Q) = 0;
		if ((CKN&&!RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CKN&&RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CKN&&!RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CKN&&D&&!RT&&SE&&SI) | (CKN&&D&&!RT&&!SE) | (CKN&&!D&&!RT&&SE&&SI))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((CKN&&D&&!RT&&SE&&!SI) | (CKN&&!D&&!RT&&SE&&!SI) | (CKN&&!D&&!RT&&!SE))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CKN&&!RT))
			(negedge RN => (Q+:1'b0)) = 0;
		(negedge CKN => (Q+:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		if ((CKN&&!RN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((!CKN&&RN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((!CKN&&!RN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((CKN&&D&&!RT&&SE&&SI) | (CKN&&D&&!RT&&!SE) | (CKN&&!D&&!RT&&SE&&SI))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((CKN&&D&&!RT&&SE&&!SI) | (CKN&&!D&&!RT&&SE&&!SI) | (CKN&&!D&&!RT&&!SE))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((!CKN&&!RT))
			(negedge RN => (QN-:1'b0)) = 0;
		(negedge CKN => (QN-:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_NOT_SE, posedge D &&& adacond_RN_AND_NOT_RT_AND_NOT_SE, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_NOT_SE, negedge D &&& adacond_RN_AND_NOT_RT_AND_NOT_SE, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (posedge CKN &&& adacond_OP_D_AND_RN_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_CP, negedge RT &&& adacond_OP_D_AND_RN_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_CP, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (posedge CKN &&& adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_CP, negedge RT &&& adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_CP, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (negedge CKN &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, posedge SE &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, negedge SE &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, posedge SE &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, negedge SE &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_SE, posedge SI &&& adacond_RN_AND_NOT_RT_AND_SE, 0, 0, notifier,,, delayed_CKN, delayed_SI);
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_SE, negedge SI &&& adacond_RN_AND_NOT_RT_AND_SE, 0, 0, notifier,,, delayed_CKN, delayed_SI);
		$recovery (posedge RN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, notifier);
		$hold (negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, posedge RN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, notifier);
		$width (negedge RN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge RN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (negedge RN &&& adacond_NOT_CKN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (posedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (negedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module SRDFFNSQX1 (Q, D, RT, SE, SI, SN, CKN);
	output Q;
	input D, RT, SE, SI, SN, CKN;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_SE, delayed_SI, delayed_CKN;

	// Function
	wire delayed_RT__bar, delayed_SE__bar, int_fwire_0;
	wire int_fwire_1, int_fwire_2, int_fwire_clk;
	wire int_fwire_d, int_fwire_IQ, int_fwire_s;
	wire xcr_0;

	not (delayed_SE__bar, delayed_SE);
	and (int_fwire_0, delayed_SE__bar, delayed_D);
	and (int_fwire_1, delayed_SE, delayed_SI);
	or (int_fwire_2, int_fwire_1, int_fwire_0);
	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, int_fwire_2);
	not (int_fwire_clk, delayed_CKN);
	not (int_fwire_s, SN);
	altos_dff_s_err (xcr_0, int_fwire_clk, int_fwire_d, int_fwire_s);
	altos_dff_s (int_fwire_IQ, notifier, int_fwire_clk, int_fwire_d, int_fwire_s, xcr_0);
	buf (Q, int_fwire_IQ);

	// Timing

	// Additional timing wires
	wire adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, adacond_NOT_CKN_AND_NOT_RT, adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN;
	wire adacond_NOT_RT_AND_NOT_SE_AND_SN, adacond_NOT_RT_AND_SE_AND_SN, adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP;
	wire adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP;
	wire adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, adacond_OP_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_SE_AND_SN_CP, adacond_OP_D_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_SI_AND_SN_CP;
	wire CKN__bar, D__bar, int_twire_0;
	wire int_twire_1, int_twire_2, int_twire_3;
	wire int_twire_4, int_twire_5, int_twire_6;
	wire int_twire_7, int_twire_8, int_twire_9;
	wire int_twire_10, int_twire_11, int_twire_12;
	wire int_twire_13, int_twire_14, int_twire_15;
	wire int_twire_16, int_twire_17, int_twire_18;
	wire int_twire_19, int_twire_20, RT__bar;
	wire SE__bar, SI__bar;


	// Additional timing gates
	not (SE__bar, SE);
	not (RT__bar, RT);
	and (adacond_NOT_RT_AND_NOT_SE_AND_SN, RT__bar, SE__bar, SN);
	not (D__bar, D);
	and (int_twire_0, D__bar, SE, SI, SN);
	and (int_twire_1, D, SE__bar, SN);
	and (int_twire_2, D, SE, SI, SN);
	or (adacond_OP_D_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_SI_AND_SN_CP, int_twire_2, int_twire_1, int_twire_0);
	and (int_twire_3, D__bar, SE__bar, SN);
	not (SI__bar, SI);
	and (int_twire_4, D__bar, SE, SI__bar, SN);
	and (int_twire_5, D, SE, SI__bar, SN);
	or (adacond_OP_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_SE_AND_SN_CP, int_twire_5, int_twire_4, int_twire_3);
	and (adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, D, RT__bar, SI__bar, SN);
	and (adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, D__bar, RT__bar, SI, SN);
	and (adacond_NOT_RT_AND_SE_AND_SN, RT__bar, SE, SN);
	and (int_twire_6, D__bar, RT__bar, SE__bar);
	and (int_twire_7, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_8, D, RT__bar, SE, SI__bar);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_8, int_twire_7, int_twire_6);
	and (int_twire_9, CKN, D__bar, RT__bar, SE, SI);
	and (int_twire_10, CKN, D, RT__bar, SE__bar);
	and (int_twire_11, CKN, D, RT__bar, SE, SI);
	or (adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_11, int_twire_10, int_twire_9);
	and (int_twire_12, CKN, D__bar, RT__bar, SE__bar);
	and (int_twire_13, CKN, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_14, CKN, D, RT__bar, SE, SI__bar);
	or (adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_14, int_twire_13, int_twire_12);
	not (CKN__bar, CKN);
	and (adacond_NOT_CKN_AND_NOT_RT, CKN__bar, RT__bar);
	and (int_twire_15, D__bar, RT__bar, SE, SI, SN);
	and (int_twire_16, D, RT__bar, SE__bar, SN);
	and (int_twire_17, D, RT__bar, SE, SI, SN);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, int_twire_17, int_twire_16, int_twire_15);
	and (int_twire_18, D__bar, RT__bar, SE__bar, SN);
	and (int_twire_19, D__bar, RT__bar, SE, SI__bar, SN);
	and (int_twire_20, D, RT__bar, SE, SI__bar, SN);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, int_twire_20, int_twire_19, int_twire_18);

	specify
		if ((CKN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CKN&&SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CKN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CKN&&D&&!RT&&SE&&SI) | (CKN&&D&&!RT&&!SE) | (CKN&&!D&&!RT&&SE&&SI))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CKN&&D&&!RT&&SE&&!SI) | (CKN&&!D&&!RT&&SE&&!SI) | (CKN&&!D&&!RT&&!SE))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CKN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		(negedge CKN => (Q+:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_NOT_SE_AND_SN, posedge D &&& adacond_NOT_RT_AND_NOT_SE_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_NOT_SE_AND_SN, negedge D &&& adacond_NOT_RT_AND_NOT_SE_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (posedge CKN &&& adacond_OP_D_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_SI_AND_SN_CP, negedge RT &&& adacond_OP_D_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (posedge CKN &&& adacond_OP_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_SE_AND_SN_CP, negedge RT &&& adacond_OP_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_SE_AND_SN_CP, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (negedge CKN &&& adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, posedge SE &&& adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, negedge SE &&& adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, posedge SE &&& adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, negedge SE &&& adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_SE_AND_SN, posedge SI &&& adacond_NOT_RT_AND_SE_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SI);
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_SE_AND_SN, negedge SI &&& adacond_NOT_RT_AND_SE_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SI);
		$recovery (posedge SN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, notifier);
		$hold (negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, posedge SN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, notifier);
		$width (negedge SN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge SN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (negedge SN &&& adacond_NOT_CKN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (posedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
		$width (negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module SRDFFNSRQX1 (Q, D, RT, SE, SI, RN, SN, CKN);
	output Q;
	input D, RT, SE, SI, RN, SN, CKN;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_SE, delayed_SI, delayed_RN, delayed_SN, delayed_CKN;

	// Function
	wire delayed_RT__bar, delayed_SE__bar, int_fwire_0;
	wire int_fwire_1, int_fwire_2, int_fwire_clk;
	wire int_fwire_d, int_fwire_IQ, int_fwire_r;
	wire int_fwire_s, xcr_0;

	not (delayed_SE__bar, delayed_SE);
	and (int_fwire_0, delayed_SE__bar, delayed_D);
	and (int_fwire_1, delayed_SE, delayed_SI);
	or (int_fwire_2, int_fwire_1, int_fwire_0);
	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, int_fwire_2);
	not (int_fwire_clk, delayed_CKN);
	not (int_fwire_s, delayed_SN);
	not (int_fwire_r, delayed_RN);
	altos_dff_sr_err (xcr_0, int_fwire_clk, int_fwire_d, int_fwire_s, int_fwire_r);
	altos_dff_sr_1 (int_fwire_IQ, notifier, int_fwire_clk, int_fwire_d, int_fwire_s, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);

	// Timing

	// Additional timing wires
	wire adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, adacond_NOT_CKN_AND_NOT_RT, adacond_NOT_CKN_AND_NOT_RT_AND_SN;
	wire adacond_NOT_CKN_AND_RN_AND_NOT_RT, adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP;
	wire adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP;
	wire adacond_OP_CKN_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_CKN_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP;
	wire adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP;
	wire adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_AND_SN_CP, adacond_OP_D_AND_RN_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_AND_SN_CP, adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN;
	wire adacond_RN_AND_NOT_RT_AND_SE_AND_SN, CKN__bar, D__bar;
	wire int_twire_0, int_twire_1, int_twire_2;
	wire int_twire_3, int_twire_4, int_twire_5;
	wire int_twire_6, int_twire_7, int_twire_8;
	wire int_twire_9, int_twire_10, int_twire_11;
	wire int_twire_12, int_twire_13, int_twire_14;
	wire int_twire_15, int_twire_16, int_twire_17;
	wire int_twire_18, int_twire_19, int_twire_20;
	wire int_twire_21, int_twire_22, int_twire_23;
	wire int_twire_24, int_twire_25, int_twire_26;
	wire int_twire_27, int_twire_28, int_twire_29;
	wire int_twire_30, int_twire_31, int_twire_32;
	wire int_twire_33, int_twire_34, int_twire_35;
	wire RT__bar, SE__bar, SI__bar;


	// Additional timing gates
	not (SE__bar, SE);
	not (RT__bar, RT);
	and (adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, RN, RT__bar, SE__bar, SN);
	not (D__bar, D);
	and (int_twire_0, D__bar, RN, SE, SI, SN);
	and (int_twire_1, D, RN, SE__bar, SN);
	and (int_twire_2, D, RN, SE, SI, SN);
	or (adacond_OP_D_AND_RN_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_AND_SN_CP, int_twire_2, int_twire_1, int_twire_0);
	and (int_twire_3, D__bar, RN, SE__bar, SN);
	not (SI__bar, SI);
	and (int_twire_4, D__bar, RN, SE, SI__bar, SN);
	and (int_twire_5, D, RN, SE, SI__bar, SN);
	or (adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_AND_SN_CP, int_twire_5, int_twire_4, int_twire_3);
	and (adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, D, RN, RT__bar, SI__bar, SN);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, D__bar, RN, RT__bar, SI, SN);
	and (adacond_RN_AND_NOT_RT_AND_SE_AND_SN, RN, RT__bar, SE, SN);
	and (int_twire_6, D__bar, RT__bar, SE, SI, SN);
	and (int_twire_7, D, RT__bar, SE__bar, SN);
	and (int_twire_8, D, RT__bar, SE, SI, SN);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, int_twire_8, int_twire_7, int_twire_6);
	and (int_twire_9, CKN, D__bar, RT__bar, SE, SI, SN);
	and (int_twire_10, CKN, D, RT__bar, SE__bar, SN);
	and (int_twire_11, CKN, D, RT__bar, SE, SI, SN);
	or (adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, int_twire_11, int_twire_10, int_twire_9);
	and (int_twire_12, CKN, D__bar, RT__bar, SE__bar, SN);
	and (int_twire_13, CKN, D__bar, RT__bar, SE, SI__bar, SN);
	and (int_twire_14, CKN, D, RT__bar, SE, SI__bar, SN);
	or (adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, int_twire_14, int_twire_13, int_twire_12);
	not (CKN__bar, CKN);
	and (adacond_NOT_CKN_AND_NOT_RT_AND_SN, CKN__bar, RT__bar, SN);
	and (int_twire_15, D__bar, RN, RT__bar, SE__bar);
	and (int_twire_16, D__bar, RN, RT__bar, SE, SI__bar);
	and (int_twire_17, D, RN, RT__bar, SE, SI__bar);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, int_twire_17, int_twire_16, int_twire_15);
	and (int_twire_18, CKN, D__bar, RT__bar, SE, SI);
	and (int_twire_19, CKN, D, RT__bar, SE__bar);
	and (int_twire_20, CKN, D, RT__bar, SE, SI);
	or (adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_20, int_twire_19, int_twire_18);
	and (int_twire_21, CKN, D__bar, RT__bar, SE__bar);
	and (int_twire_22, CKN, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_23, CKN, D, RT__bar, SE, SI__bar);
	or (adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_23, int_twire_22, int_twire_21);
	and (adacond_NOT_CKN_AND_NOT_RT, CKN__bar, RT__bar);
	and (int_twire_24, CKN, D__bar, RN, RT__bar, SE, SI);
	and (int_twire_25, CKN, D, RN, RT__bar, SE__bar);
	and (int_twire_26, CKN, D, RN, RT__bar, SE, SI);
	or (adacond_OP_CKN_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_26, int_twire_25, int_twire_24);
	and (int_twire_27, CKN, D__bar, RN, RT__bar, SE__bar);
	and (int_twire_28, CKN, D__bar, RN, RT__bar, SE, SI__bar);
	and (int_twire_29, CKN, D, RN, RT__bar, SE, SI__bar);
	or (adacond_OP_CKN_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, int_twire_29, int_twire_28, int_twire_27);
	and (adacond_NOT_CKN_AND_RN_AND_NOT_RT, CKN__bar, RN, RT__bar);
	and (int_twire_30, D__bar, RN, RT__bar, SE, SI, SN);
	and (int_twire_31, D, RN, RT__bar, SE__bar, SN);
	and (int_twire_32, D, RN, RT__bar, SE, SI, SN);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, int_twire_32, int_twire_31, int_twire_30);
	and (int_twire_33, D__bar, RN, RT__bar, SE__bar, SN);
	and (int_twire_34, D__bar, RN, RT__bar, SE, SI__bar, SN);
	and (int_twire_35, D, RN, RT__bar, SE, SI__bar, SN);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, int_twire_35, int_twire_34, int_twire_33);

	specify
		if ((!CKN&&RN&&SN))
			(RT => Q) = 0;
		if ((CKN&&!RN&&SN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CKN&&!RN&&SN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CKN&&RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CKN&&!RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CKN&&RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CKN&&!RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CKN&&D&&!RT&&SE&&SI&&SN) | (CKN&&D&&!RT&&!SE&&SN) | (CKN&&!D&&!RT&&SE&&SI&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((CKN&&D&&!RT&&SE&&!SI&&SN) | (CKN&&!D&&!RT&&SE&&!SI&&SN) | (CKN&&!D&&!RT&&!SE&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CKN&&!RT&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((CKN&&D&&!RN&&!RT&&SE&&SI) | (CKN&&D&&!RN&&!RT&&!SE) | (CKN&&!D&&!RN&&!RT&&SE&&SI))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((CKN&&D&&!RN&&!RT&&SE&&!SI) | (CKN&&!D&&!RN&&!RT&&SE&&!SI) | (CKN&&!D&&!RN&&!RT&&!SE))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((!CKN&&!RN&&!RT))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((CKN&&D&&RN&&!RT&&SE&&SI) | (CKN&&D&&RN&&!RT&&!SE) | (CKN&&!D&&RN&&!RT&&SE&&SI))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CKN&&D&&RN&&!RT&&SE&&!SI) | (CKN&&!D&&RN&&!RT&&SE&&!SI) | (CKN&&!D&&RN&&!RT&&!SE))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CKN&&D&&!RN&&!RT&&SE&&SI) | (CKN&&D&&!RN&&!RT&&!SE) | (CKN&&!D&&!RN&&!RT&&SE&&SI))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CKN&&D&&!RN&&!RT&&SE&&!SI) | (CKN&&!D&&!RN&&!RT&&SE&&!SI) | (CKN&&!D&&!RN&&!RT&&!SE))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CKN&&RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CKN&&!RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		(negedge CKN => (Q+:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, posedge D &&& adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, negedge D &&& adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (posedge CKN &&& adacond_OP_D_AND_RN_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_AND_SN_CP, negedge RT &&& adacond_OP_D_AND_RN_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (posedge CKN &&& adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_AND_SN_CP, negedge RT &&& adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_AND_SN_CP, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (negedge CKN &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, posedge SE &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, negedge SE &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, posedge SE &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, negedge SE &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_SE_AND_SN, posedge SI &&& adacond_RN_AND_NOT_RT_AND_SE_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SI);
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_SE_AND_SN, negedge SI &&& adacond_RN_AND_NOT_RT_AND_SE_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SI);
		$setuphold (posedge RN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, posedge SN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$setuphold (posedge RN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, posedge SN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$setuphold (posedge RN &&& adacond_NOT_CKN_AND_NOT_RT, posedge SN &&& adacond_NOT_CKN_AND_NOT_RT, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$recovery (posedge RN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, notifier);
		$hold (negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, posedge RN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, notifier);
		$recovery (posedge SN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, negedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, notifier);
		$hold (negedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, posedge SN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, notifier);
		$width (negedge RN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (negedge RN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
		$width (negedge RN &&& adacond_NOT_CKN_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge SN &&& adacond_OP_CKN_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge SN &&& adacond_OP_CKN_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (negedge SN &&& adacond_NOT_CKN_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (negedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (posedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
		$width (negedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module SRDFFNSRX1 (Q, QN, D, RT, SE, SI, RN, SN, CKN);
	output Q, QN;
	input D, RT, SE, SI, RN, SN, CKN;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_SE, delayed_SI, delayed_RN, delayed_SN, delayed_CKN;

	// Function
	wire delayed_RT__bar, delayed_SE__bar, int_fwire_0;
	wire int_fwire_1, int_fwire_2, int_fwire_clk;
	wire int_fwire_d, int_fwire_IQ, int_fwire_IQN;
	wire int_fwire_r, int_fwire_s, xcr_0;

	not (delayed_SE__bar, delayed_SE);
	and (int_fwire_0, delayed_SE__bar, delayed_D);
	and (int_fwire_1, delayed_SE, delayed_SI);
	or (int_fwire_2, int_fwire_1, int_fwire_0);
	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, int_fwire_2);
	not (int_fwire_clk, delayed_CKN);
	not (int_fwire_s, delayed_SN);
	not (int_fwire_r, delayed_RN);
	altos_dff_sr_err (xcr_0, int_fwire_clk, int_fwire_d, int_fwire_s, int_fwire_r);
	altos_dff_sr_1 (int_fwire_IQ, notifier, int_fwire_clk, int_fwire_d, int_fwire_s, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, adacond_NOT_CKN_AND_NOT_RT, adacond_NOT_CKN_AND_NOT_RT_AND_SN;
	wire adacond_NOT_CKN_AND_RN_AND_NOT_RT, adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP;
	wire adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP;
	wire adacond_OP_CKN_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_CKN_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP;
	wire adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP;
	wire adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_AND_SN_CP, adacond_OP_D_AND_RN_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_AND_SN_CP, adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN;
	wire adacond_RN_AND_NOT_RT_AND_SE_AND_SN, CKN__bar, D__bar;
	wire int_twire_0, int_twire_1, int_twire_2;
	wire int_twire_3, int_twire_4, int_twire_5;
	wire int_twire_6, int_twire_7, int_twire_8;
	wire int_twire_9, int_twire_10, int_twire_11;
	wire int_twire_12, int_twire_13, int_twire_14;
	wire int_twire_15, int_twire_16, int_twire_17;
	wire int_twire_18, int_twire_19, int_twire_20;
	wire int_twire_21, int_twire_22, int_twire_23;
	wire int_twire_24, int_twire_25, int_twire_26;
	wire int_twire_27, int_twire_28, int_twire_29;
	wire int_twire_30, int_twire_31, int_twire_32;
	wire int_twire_33, int_twire_34, int_twire_35;
	wire RT__bar, SE__bar, SI__bar;


	// Additional timing gates
	not (SE__bar, SE);
	not (RT__bar, RT);
	and (adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, RN, RT__bar, SE__bar, SN);
	not (D__bar, D);
	and (int_twire_0, D__bar, RN, SE, SI, SN);
	and (int_twire_1, D, RN, SE__bar, SN);
	and (int_twire_2, D, RN, SE, SI, SN);
	or (adacond_OP_D_AND_RN_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_AND_SN_CP, int_twire_2, int_twire_1, int_twire_0);
	and (int_twire_3, D__bar, RN, SE__bar, SN);
	not (SI__bar, SI);
	and (int_twire_4, D__bar, RN, SE, SI__bar, SN);
	and (int_twire_5, D, RN, SE, SI__bar, SN);
	or (adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_AND_SN_CP, int_twire_5, int_twire_4, int_twire_3);
	and (adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, D, RN, RT__bar, SI__bar, SN);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, D__bar, RN, RT__bar, SI, SN);
	and (adacond_RN_AND_NOT_RT_AND_SE_AND_SN, RN, RT__bar, SE, SN);
	and (int_twire_6, D__bar, RT__bar, SE, SI, SN);
	and (int_twire_7, D, RT__bar, SE__bar, SN);
	and (int_twire_8, D, RT__bar, SE, SI, SN);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, int_twire_8, int_twire_7, int_twire_6);
	and (int_twire_9, CKN, D__bar, RT__bar, SE, SI, SN);
	and (int_twire_10, CKN, D, RT__bar, SE__bar, SN);
	and (int_twire_11, CKN, D, RT__bar, SE, SI, SN);
	or (adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, int_twire_11, int_twire_10, int_twire_9);
	and (int_twire_12, CKN, D__bar, RT__bar, SE__bar, SN);
	and (int_twire_13, CKN, D__bar, RT__bar, SE, SI__bar, SN);
	and (int_twire_14, CKN, D, RT__bar, SE, SI__bar, SN);
	or (adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, int_twire_14, int_twire_13, int_twire_12);
	not (CKN__bar, CKN);
	and (adacond_NOT_CKN_AND_NOT_RT_AND_SN, CKN__bar, RT__bar, SN);
	and (int_twire_15, D__bar, RN, RT__bar, SE__bar);
	and (int_twire_16, D__bar, RN, RT__bar, SE, SI__bar);
	and (int_twire_17, D, RN, RT__bar, SE, SI__bar);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, int_twire_17, int_twire_16, int_twire_15);
	and (int_twire_18, CKN, D__bar, RT__bar, SE, SI);
	and (int_twire_19, CKN, D, RT__bar, SE__bar);
	and (int_twire_20, CKN, D, RT__bar, SE, SI);
	or (adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_20, int_twire_19, int_twire_18);
	and (int_twire_21, CKN, D__bar, RT__bar, SE__bar);
	and (int_twire_22, CKN, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_23, CKN, D, RT__bar, SE, SI__bar);
	or (adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_23, int_twire_22, int_twire_21);
	and (adacond_NOT_CKN_AND_NOT_RT, CKN__bar, RT__bar);
	and (int_twire_24, CKN, D__bar, RN, RT__bar, SE, SI);
	and (int_twire_25, CKN, D, RN, RT__bar, SE__bar);
	and (int_twire_26, CKN, D, RN, RT__bar, SE, SI);
	or (adacond_OP_CKN_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_26, int_twire_25, int_twire_24);
	and (int_twire_27, CKN, D__bar, RN, RT__bar, SE__bar);
	and (int_twire_28, CKN, D__bar, RN, RT__bar, SE, SI__bar);
	and (int_twire_29, CKN, D, RN, RT__bar, SE, SI__bar);
	or (adacond_OP_CKN_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, int_twire_29, int_twire_28, int_twire_27);
	and (adacond_NOT_CKN_AND_RN_AND_NOT_RT, CKN__bar, RN, RT__bar);
	and (int_twire_30, D__bar, RN, RT__bar, SE, SI, SN);
	and (int_twire_31, D, RN, RT__bar, SE__bar, SN);
	and (int_twire_32, D, RN, RT__bar, SE, SI, SN);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, int_twire_32, int_twire_31, int_twire_30);
	and (int_twire_33, D__bar, RN, RT__bar, SE__bar, SN);
	and (int_twire_34, D__bar, RN, RT__bar, SE, SI__bar, SN);
	and (int_twire_35, D, RN, RT__bar, SE, SI__bar, SN);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, int_twire_35, int_twire_34, int_twire_33);

	specify
		if ((!CKN&&RN&&SN))
			(RT => Q) = 0;
		if ((CKN&&!RN&&SN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CKN&&!RN&&SN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CKN&&RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CKN&&!RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CKN&&RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CKN&&!RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CKN&&D&&!RT&&SE&&SI&&SN) | (CKN&&D&&!RT&&!SE&&SN) | (CKN&&!D&&!RT&&SE&&SI&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((CKN&&D&&!RT&&SE&&!SI&&SN) | (CKN&&!D&&!RT&&SE&&!SI&&SN) | (CKN&&!D&&!RT&&!SE&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CKN&&!RT&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((CKN&&D&&!RN&&!RT&&SE&&SI) | (CKN&&D&&!RN&&!RT&&!SE) | (CKN&&!D&&!RN&&!RT&&SE&&SI))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((CKN&&D&&!RN&&!RT&&SE&&!SI) | (CKN&&!D&&!RN&&!RT&&SE&&!SI) | (CKN&&!D&&!RN&&!RT&&!SE))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((!CKN&&!RN&&!RT))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((CKN&&D&&RN&&!RT&&SE&&SI) | (CKN&&D&&RN&&!RT&&!SE) | (CKN&&!D&&RN&&!RT&&SE&&SI))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CKN&&D&&RN&&!RT&&SE&&!SI) | (CKN&&!D&&RN&&!RT&&SE&&!SI) | (CKN&&!D&&RN&&!RT&&!SE))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CKN&&D&&!RN&&!RT&&SE&&SI) | (CKN&&D&&!RN&&!RT&&!SE) | (CKN&&!D&&!RN&&!RT&&SE&&SI))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CKN&&D&&!RN&&!RT&&SE&&!SI) | (CKN&&!D&&!RN&&!RT&&SE&&!SI) | (CKN&&!D&&!RN&&!RT&&!SE))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CKN&&RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CKN&&!RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		(negedge CKN => (Q+:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		if ((!CKN&&RN&&SN))
			(RT => QN) = 0;
		if ((CKN&&RN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((CKN&&!RN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((!CKN&&RN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((!CKN&&!RN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((CKN&&!RN&&SN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((!CKN&&!RN&&SN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((CKN&&D&&!RT&&SE&&SI&&SN) | (CKN&&D&&!RT&&!SE&&SN) | (CKN&&!D&&!RT&&SE&&SI&&SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((CKN&&D&&!RT&&SE&&!SI&&SN) | (CKN&&!D&&!RT&&SE&&!SI&&SN) | (CKN&&!D&&!RT&&!SE&&SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((!CKN&&!RT&&SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((CKN&&D&&RN&&!RT&&SE&&SI) | (CKN&&D&&RN&&!RT&&!SE) | (CKN&&!D&&RN&&!RT&&SE&&SI))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((CKN&&D&&RN&&!RT&&SE&&!SI) | (CKN&&!D&&RN&&!RT&&SE&&!SI) | (CKN&&!D&&RN&&!RT&&!SE))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((CKN&&D&&!RN&&!RT&&SE&&SI) | (CKN&&D&&!RN&&!RT&&!SE) | (CKN&&!D&&!RN&&!RT&&SE&&SI))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((CKN&&D&&!RN&&!RT&&SE&&!SI) | (CKN&&!D&&!RN&&!RT&&SE&&!SI) | (CKN&&!D&&!RN&&!RT&&!SE))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!CKN&&RN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!CKN&&!RN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((CKN&&D&&!RN&&!RT&&SE&&SI) | (CKN&&D&&!RN&&!RT&&!SE) | (CKN&&!D&&!RN&&!RT&&SE&&SI))
			(posedge SN => (QN-:1'b0)) = 0;
		if ((CKN&&D&&!RN&&!RT&&SE&&!SI) | (CKN&&!D&&!RN&&!RT&&SE&&!SI) | (CKN&&!D&&!RN&&!RT&&!SE))
			(posedge SN => (QN-:1'b0)) = 0;
		if ((!CKN&&!RN&&!RT))
			(posedge SN => (QN-:1'b0)) = 0;
		(negedge CKN => (QN-:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, posedge D &&& adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, negedge D &&& adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (posedge CKN &&& adacond_OP_D_AND_RN_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_AND_SN_CP, negedge RT &&& adacond_OP_D_AND_RN_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (posedge CKN &&& adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_AND_SN_CP, negedge RT &&& adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_AND_SN_CP, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (negedge CKN &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, posedge SE &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, negedge SE &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, posedge SE &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, negedge SE &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_SE_AND_SN, posedge SI &&& adacond_RN_AND_NOT_RT_AND_SE_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SI);
		$setuphold (negedge CKN &&& adacond_RN_AND_NOT_RT_AND_SE_AND_SN, negedge SI &&& adacond_RN_AND_NOT_RT_AND_SE_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SI);
		$setuphold (posedge RN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, posedge SN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$setuphold (posedge RN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, posedge SN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$setuphold (posedge RN &&& adacond_NOT_CKN_AND_NOT_RT, posedge SN &&& adacond_NOT_CKN_AND_NOT_RT, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$recovery (posedge RN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, notifier);
		$hold (negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, posedge RN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, notifier);
		$recovery (posedge SN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, negedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, notifier);
		$hold (negedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, posedge SN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, notifier);
		$width (negedge RN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (negedge RN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
		$width (negedge RN &&& adacond_NOT_CKN_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge SN &&& adacond_OP_CKN_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge SN &&& adacond_OP_CKN_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (negedge SN &&& adacond_NOT_CKN_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (negedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (posedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
		$width (negedge CKN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module SRDFFNSX1 (Q, QN, D, RT, SE, SI, SN, CKN);
	output Q, QN;
	input D, RT, SE, SI, SN, CKN;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_SE, delayed_SI, delayed_CKN;

	// Function
	wire delayed_RT__bar, delayed_SE__bar, int_fwire_0;
	wire int_fwire_1, int_fwire_2, int_fwire_clk;
	wire int_fwire_d, int_fwire_IQ, int_fwire_IQN;
	wire int_fwire_s, xcr_0;

	not (delayed_SE__bar, delayed_SE);
	and (int_fwire_0, delayed_SE__bar, delayed_D);
	and (int_fwire_1, delayed_SE, delayed_SI);
	or (int_fwire_2, int_fwire_1, int_fwire_0);
	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, int_fwire_2);
	not (int_fwire_clk, delayed_CKN);
	not (int_fwire_s, SN);
	altos_dff_s_err (xcr_0, int_fwire_clk, int_fwire_d, int_fwire_s);
	altos_dff_s (int_fwire_IQ, notifier, int_fwire_clk, int_fwire_d, int_fwire_s, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, adacond_NOT_CKN_AND_NOT_RT, adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN;
	wire adacond_NOT_RT_AND_NOT_SE_AND_SN, adacond_NOT_RT_AND_SE_AND_SN, adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP;
	wire adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP;
	wire adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, adacond_OP_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_SE_AND_SN_CP, adacond_OP_D_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_SI_AND_SN_CP;
	wire CKN__bar, D__bar, int_twire_0;
	wire int_twire_1, int_twire_2, int_twire_3;
	wire int_twire_4, int_twire_5, int_twire_6;
	wire int_twire_7, int_twire_8, int_twire_9;
	wire int_twire_10, int_twire_11, int_twire_12;
	wire int_twire_13, int_twire_14, int_twire_15;
	wire int_twire_16, int_twire_17, int_twire_18;
	wire int_twire_19, int_twire_20, RT__bar;
	wire SE__bar, SI__bar;


	// Additional timing gates
	not (SE__bar, SE);
	not (RT__bar, RT);
	and (adacond_NOT_RT_AND_NOT_SE_AND_SN, RT__bar, SE__bar, SN);
	not (D__bar, D);
	and (int_twire_0, D__bar, SE, SI, SN);
	and (int_twire_1, D, SE__bar, SN);
	and (int_twire_2, D, SE, SI, SN);
	or (adacond_OP_D_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_SI_AND_SN_CP, int_twire_2, int_twire_1, int_twire_0);
	and (int_twire_3, D__bar, SE__bar, SN);
	not (SI__bar, SI);
	and (int_twire_4, D__bar, SE, SI__bar, SN);
	and (int_twire_5, D, SE, SI__bar, SN);
	or (adacond_OP_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_SE_AND_SN_CP, int_twire_5, int_twire_4, int_twire_3);
	and (adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, D, RT__bar, SI__bar, SN);
	and (adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, D__bar, RT__bar, SI, SN);
	and (adacond_NOT_RT_AND_SE_AND_SN, RT__bar, SE, SN);
	and (int_twire_6, D__bar, RT__bar, SE__bar);
	and (int_twire_7, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_8, D, RT__bar, SE, SI__bar);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_8, int_twire_7, int_twire_6);
	and (int_twire_9, CKN, D__bar, RT__bar, SE, SI);
	and (int_twire_10, CKN, D, RT__bar, SE__bar);
	and (int_twire_11, CKN, D, RT__bar, SE, SI);
	or (adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_11, int_twire_10, int_twire_9);
	and (int_twire_12, CKN, D__bar, RT__bar, SE__bar);
	and (int_twire_13, CKN, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_14, CKN, D, RT__bar, SE, SI__bar);
	or (adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_14, int_twire_13, int_twire_12);
	not (CKN__bar, CKN);
	and (adacond_NOT_CKN_AND_NOT_RT, CKN__bar, RT__bar);
	and (int_twire_15, D__bar, RT__bar, SE, SI, SN);
	and (int_twire_16, D, RT__bar, SE__bar, SN);
	and (int_twire_17, D, RT__bar, SE, SI, SN);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, int_twire_17, int_twire_16, int_twire_15);
	and (int_twire_18, D__bar, RT__bar, SE__bar, SN);
	and (int_twire_19, D__bar, RT__bar, SE, SI__bar, SN);
	and (int_twire_20, D, RT__bar, SE, SI__bar, SN);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, int_twire_20, int_twire_19, int_twire_18);

	specify
		if ((CKN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CKN&&SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CKN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CKN&&D&&!RT&&SE&&SI) | (CKN&&D&&!RT&&!SE) | (CKN&&!D&&!RT&&SE&&SI))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CKN&&D&&!RT&&SE&&!SI) | (CKN&&!D&&!RT&&SE&&!SI) | (CKN&&!D&&!RT&&!SE))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CKN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		(negedge CKN => (Q+:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		ifnone (RT => QN) = 0;
		if ((CKN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((!CKN&&SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((!CKN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((CKN&&D&&!RT&&SE&&SI) | (CKN&&D&&!RT&&!SE) | (CKN&&!D&&!RT&&SE&&SI))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((CKN&&D&&!RT&&SE&&!SI) | (CKN&&!D&&!RT&&SE&&!SI) | (CKN&&!D&&!RT&&!SE))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!CKN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		(negedge CKN => (QN-:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_NOT_SE_AND_SN, posedge D &&& adacond_NOT_RT_AND_NOT_SE_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_NOT_SE_AND_SN, negedge D &&& adacond_NOT_RT_AND_NOT_SE_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (posedge CKN &&& adacond_OP_D_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_SI_AND_SN_CP, negedge RT &&& adacond_OP_D_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (posedge CKN &&& adacond_OP_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_SE_AND_SN_CP, negedge RT &&& adacond_OP_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_SE_AND_SN_CP, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (negedge CKN &&& adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, posedge SE &&& adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, negedge SE &&& adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, posedge SE &&& adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, negedge SE &&& adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_SE_AND_SN, posedge SI &&& adacond_NOT_RT_AND_SE_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SI);
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_SE_AND_SN, negedge SI &&& adacond_NOT_RT_AND_SE_AND_SN, 0, 0, notifier,,, delayed_CKN, delayed_SI);
		$recovery (posedge SN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, notifier);
		$hold (negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, posedge SN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, notifier);
		$width (negedge SN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_CKN_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge SN &&& adacond_OP_CKN_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_CKN_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (negedge SN &&& adacond_NOT_CKN_AND_NOT_RT, 0, 0, notifier);
		$width (posedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (posedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
		$width (negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module SRDFFNX1 (Q, QN, D, RT, SE, SI, CKN);
	output Q, QN;
	input D, RT, SE, SI, CKN;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_SE, delayed_SI, delayed_CKN;

	// Function
	wire delayed_RT__bar, delayed_SE__bar, int_fwire_0;
	wire int_fwire_1, int_fwire_2, int_fwire_clk;
	wire int_fwire_d, int_fwire_IQ, int_fwire_IQN;
	wire xcr_0;

	not (delayed_SE__bar, delayed_SE);
	and (int_fwire_0, delayed_SE__bar, delayed_D);
	and (int_fwire_1, delayed_SE, delayed_SI);
	or (int_fwire_2, int_fwire_1, int_fwire_0);
	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, int_fwire_2);
	not (int_fwire_clk, delayed_CKN);
	altos_dff_err (xcr_0, int_fwire_clk, int_fwire_d);
	altos_dff (int_fwire_IQ, notifier, int_fwire_clk, int_fwire_d, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_D_AND_NOT_RT_AND_NOT_SI, adacond_NOT_D_AND_NOT_RT_AND_SI, adacond_NOT_RT_AND_NOT_SE;
	wire adacond_NOT_RT_AND_SE, adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP;
	wire adacond_OP_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_SE_CP, adacond_OP_D_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_SE_CP_OR_OP_NOT_D_AND_SE_AND_SI_CP, D__bar;
	wire int_twire_0, int_twire_1, int_twire_2;
	wire int_twire_3, int_twire_4, int_twire_5;
	wire int_twire_6, int_twire_7, int_twire_8;
	wire int_twire_9, int_twire_10, int_twire_11;
	wire RT__bar, SE__bar, SI__bar;


	// Additional timing gates
	not (SE__bar, SE);
	not (RT__bar, RT);
	and (adacond_NOT_RT_AND_NOT_SE, RT__bar, SE__bar);
	not (D__bar, D);
	and (int_twire_0, D__bar, SE, SI);
	and (int_twire_1, D, SE__bar);
	and (int_twire_2, D, SE, SI);
	or (adacond_OP_D_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_SE_CP_OR_OP_NOT_D_AND_SE_AND_SI_CP, int_twire_2, int_twire_1, int_twire_0);
	and (int_twire_3, D__bar, SE__bar);
	not (SI__bar, SI);
	and (int_twire_4, D__bar, SE, SI__bar);
	and (int_twire_5, D, SE, SI__bar);
	or (adacond_OP_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_SE_CP, int_twire_5, int_twire_4, int_twire_3);
	and (adacond_D_AND_NOT_RT_AND_NOT_SI, D, RT__bar, SI__bar);
	and (adacond_NOT_D_AND_NOT_RT_AND_SI, D__bar, RT__bar, SI);
	and (adacond_NOT_RT_AND_SE, RT__bar, SE);
	and (int_twire_6, D__bar, RT__bar, SE, SI);
	and (int_twire_7, D, RT__bar, SE__bar);
	and (int_twire_8, D, RT__bar, SE, SI);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_8, int_twire_7, int_twire_6);
	and (int_twire_9, D__bar, RT__bar, SE__bar);
	and (int_twire_10, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_11, D, RT__bar, SE, SI__bar);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_11, int_twire_10, int_twire_9);

	specify
		(RT => Q) = 0;
		(negedge CKN => (Q+:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		(RT => QN) = 0;
		(negedge CKN => (QN-:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_NOT_SE, posedge D &&& adacond_NOT_RT_AND_NOT_SE, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_NOT_SE, negedge D &&& adacond_NOT_RT_AND_NOT_SE, 0, 0, notifier,,, delayed_CKN, delayed_D);
		$setuphold (posedge CKN &&& adacond_OP_D_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_SE_CP_OR_OP_NOT_D_AND_SE_AND_SI_CP, negedge RT &&& adacond_OP_D_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_SE_CP_OR_OP_NOT_D_AND_SE_AND_SI_CP, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (posedge CKN &&& adacond_OP_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_SE_CP, negedge RT &&& adacond_OP_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_SE_CP, 0, 0, notifier,,, delayed_CKN, delayed_RT);
		$setuphold (negedge CKN &&& adacond_D_AND_NOT_RT_AND_NOT_SI, posedge SE &&& adacond_D_AND_NOT_RT_AND_NOT_SI, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_D_AND_NOT_RT_AND_NOT_SI, negedge SE &&& adacond_D_AND_NOT_RT_AND_NOT_SI, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_D_AND_NOT_RT_AND_SI, posedge SE &&& adacond_NOT_D_AND_NOT_RT_AND_SI, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_D_AND_NOT_RT_AND_SI, negedge SE &&& adacond_NOT_D_AND_NOT_RT_AND_SI, 0, 0, notifier,,, delayed_CKN, delayed_SE);
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_SE, posedge SI &&& adacond_NOT_RT_AND_SE, 0, 0, notifier,,, delayed_CKN, delayed_SI);
		$setuphold (negedge CKN &&& adacond_NOT_RT_AND_SE, negedge SI &&& adacond_NOT_RT_AND_SE, 0, 0, notifier,,, delayed_CKN, delayed_SI);
		$width (posedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (posedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (negedge CKN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module SRDFFQX1 (Q, D, RT, SE, SI, CK);
	output Q;
	input D, RT, SE, SI, CK;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_SE, delayed_SI, delayed_CK;

	// Function
	wire delayed_RT__bar, delayed_SE__bar, int_fwire_0;
	wire int_fwire_1, int_fwire_2, int_fwire_d;
	wire int_fwire_IQ, xcr_0;

	not (delayed_SE__bar, delayed_SE);
	and (int_fwire_0, delayed_SE__bar, delayed_D);
	and (int_fwire_1, delayed_SE, delayed_SI);
	or (int_fwire_2, int_fwire_1, int_fwire_0);
	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, int_fwire_2);
	altos_dff_err (xcr_0, delayed_CK, int_fwire_d);
	altos_dff (int_fwire_IQ, notifier, delayed_CK, int_fwire_d, xcr_0);
	buf (Q, int_fwire_IQ);

	// Timing

	// Additional timing wires
	wire adacond_D_AND_NOT_RT_AND_NOT_SI, adacond_NOT_D_AND_NOT_RT_AND_SI, adacond_NOT_RT_AND_NOT_SE;
	wire adacond_NOT_RT_AND_SE, adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP;
	wire adacond_OP_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_SE_CP, adacond_OP_D_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_SE_CP_OR_OP_NOT_D_AND_SE_AND_SI_CP, D__bar;
	wire int_twire_0, int_twire_1, int_twire_2;
	wire int_twire_3, int_twire_4, int_twire_5;
	wire int_twire_6, int_twire_7, int_twire_8;
	wire int_twire_9, int_twire_10, int_twire_11;
	wire RT__bar, SE__bar, SI__bar;


	// Additional timing gates
	not (SE__bar, SE);
	not (RT__bar, RT);
	and (adacond_NOT_RT_AND_NOT_SE, RT__bar, SE__bar);
	not (D__bar, D);
	and (int_twire_0, D__bar, SE, SI);
	and (int_twire_1, D, SE__bar);
	and (int_twire_2, D, SE, SI);
	or (adacond_OP_D_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_SE_CP_OR_OP_NOT_D_AND_SE_AND_SI_CP, int_twire_2, int_twire_1, int_twire_0);
	and (int_twire_3, D__bar, SE__bar);
	not (SI__bar, SI);
	and (int_twire_4, D__bar, SE, SI__bar);
	and (int_twire_5, D, SE, SI__bar);
	or (adacond_OP_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_SE_CP, int_twire_5, int_twire_4, int_twire_3);
	and (adacond_D_AND_NOT_RT_AND_NOT_SI, D, RT__bar, SI__bar);
	and (adacond_NOT_D_AND_NOT_RT_AND_SI, D__bar, RT__bar, SI);
	and (adacond_NOT_RT_AND_SE, RT__bar, SE);
	and (int_twire_6, D__bar, RT__bar, SE, SI);
	and (int_twire_7, D, RT__bar, SE__bar);
	and (int_twire_8, D, RT__bar, SE, SI);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_8, int_twire_7, int_twire_6);
	and (int_twire_9, D__bar, RT__bar, SE__bar);
	and (int_twire_10, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_11, D, RT__bar, SE, SI__bar);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_11, int_twire_10, int_twire_9);

	specify
		(RT => Q) = 0;
		(posedge CK => (Q+:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_NOT_SE, posedge D &&& adacond_NOT_RT_AND_NOT_SE, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_NOT_SE, negedge D &&& adacond_NOT_RT_AND_NOT_SE, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (negedge CK &&& adacond_OP_D_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_SE_CP_OR_OP_NOT_D_AND_SE_AND_SI_CP, negedge RT &&& adacond_OP_D_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_SE_CP_OR_OP_NOT_D_AND_SE_AND_SI_CP, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (negedge CK &&& adacond_OP_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_SE_CP, negedge RT &&& adacond_OP_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_SE_CP, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (posedge CK &&& adacond_D_AND_NOT_RT_AND_NOT_SI, posedge SE &&& adacond_D_AND_NOT_RT_AND_NOT_SI, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_D_AND_NOT_RT_AND_NOT_SI, negedge SE &&& adacond_D_AND_NOT_RT_AND_NOT_SI, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_D_AND_NOT_RT_AND_SI, posedge SE &&& adacond_NOT_D_AND_NOT_RT_AND_SI, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_D_AND_NOT_RT_AND_SI, negedge SE &&& adacond_NOT_D_AND_NOT_RT_AND_SI, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_SE, posedge SI &&& adacond_NOT_RT_AND_SE, 0, 0, notifier,,, delayed_CK, delayed_SI);
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_SE, negedge SI &&& adacond_NOT_RT_AND_SE, 0, 0, notifier,,, delayed_CK, delayed_SI);
		$width (posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (negedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module SRDFFRQX1 (Q, D, RT, SE, SI, RN, CK);
	output Q;
	input D, RT, SE, SI, RN, CK;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_SE, delayed_SI, delayed_CK;

	// Function
	wire delayed_RT__bar, delayed_SE__bar, int_fwire_0;
	wire int_fwire_1, int_fwire_2, int_fwire_d;
	wire int_fwire_IQ, int_fwire_r, xcr_0;

	not (delayed_SE__bar, delayed_SE);
	and (int_fwire_0, delayed_SE__bar, delayed_D);
	and (int_fwire_1, delayed_SE, delayed_SI);
	or (int_fwire_2, int_fwire_1, int_fwire_0);
	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, int_fwire_2);
	not (int_fwire_r, RN);
	altos_dff_r_err (xcr_0, delayed_CK, int_fwire_d, int_fwire_r);
	altos_dff_r (int_fwire_IQ, notifier, delayed_CK, int_fwire_d, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);

	// Timing

	// Additional timing wires
	wire adacond_CK_AND_NOT_RT, adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI;
	wire adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP;
	wire adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_CP, adacond_OP_D_AND_RN_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_CP, adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP;
	wire adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, adacond_RN_AND_NOT_RT_AND_NOT_SE, adacond_RN_AND_NOT_RT_AND_SE;
	wire CK__bar, D__bar, int_twire_0;
	wire int_twire_1, int_twire_2, int_twire_3;
	wire int_twire_4, int_twire_5, int_twire_6;
	wire int_twire_7, int_twire_8, int_twire_9;
	wire int_twire_10, int_twire_11, int_twire_12;
	wire int_twire_13, int_twire_14, int_twire_15;
	wire int_twire_16, int_twire_17, int_twire_18;
	wire int_twire_19, int_twire_20, RT__bar;
	wire SE__bar, SI__bar;


	// Additional timing gates
	not (SE__bar, SE);
	not (RT__bar, RT);
	and (adacond_RN_AND_NOT_RT_AND_NOT_SE, RN, RT__bar, SE__bar);
	not (D__bar, D);
	and (int_twire_0, D__bar, RN, SE, SI);
	and (int_twire_1, D, RN, SE__bar);
	and (int_twire_2, D, RN, SE, SI);
	or (adacond_OP_D_AND_RN_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_CP, int_twire_2, int_twire_1, int_twire_0);
	and (int_twire_3, D__bar, RN, SE__bar);
	not (SI__bar, SI);
	and (int_twire_4, D__bar, RN, SE, SI__bar);
	and (int_twire_5, D, RN, SE, SI__bar);
	or (adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_CP, int_twire_5, int_twire_4, int_twire_3);
	and (adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, D, RN, RT__bar, SI__bar);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, D__bar, RN, RT__bar, SI);
	and (adacond_RN_AND_NOT_RT_AND_SE, RN, RT__bar, SE);
	and (int_twire_6, D__bar, RT__bar, SE, SI);
	and (int_twire_7, D, RT__bar, SE__bar);
	and (int_twire_8, D, RT__bar, SE, SI);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_8, int_twire_7, int_twire_6);
	and (adacond_CK_AND_NOT_RT, CK, RT__bar);
	not (CK__bar, CK);
	and (int_twire_9, CK__bar, D__bar, RT__bar, SE, SI);
	and (int_twire_10, CK__bar, D, RT__bar, SE__bar);
	and (int_twire_11, CK__bar, D, RT__bar, SE, SI);
	or (adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_11, int_twire_10, int_twire_9);
	and (int_twire_12, CK__bar, D__bar, RT__bar, SE__bar);
	and (int_twire_13, CK__bar, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_14, CK__bar, D, RT__bar, SE, SI__bar);
	or (adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_14, int_twire_13, int_twire_12);
	and (int_twire_15, D__bar, RN, RT__bar, SE, SI);
	and (int_twire_16, D, RN, RT__bar, SE__bar);
	and (int_twire_17, D, RN, RT__bar, SE, SI);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_17, int_twire_16, int_twire_15);
	and (int_twire_18, D__bar, RN, RT__bar, SE__bar);
	and (int_twire_19, D__bar, RN, RT__bar, SE, SI__bar);
	and (int_twire_20, D, RN, RT__bar, SE, SI__bar);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, int_twire_20, int_twire_19, int_twire_18);

	specify
		ifnone (RT => Q) = 0;
		if ((CK&&RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CK&&!RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CK&&!RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CK&&!RT))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CK&&D&&!RT&&SE&&SI) | (!CK&&D&&!RT&&!SE) | (!CK&&!D&&!RT&&SE&&SI))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CK&&D&&!RT&&SE&&!SI) | (!CK&&!D&&!RT&&SE&&!SI) | (!CK&&!D&&!RT&&!SE))
			(negedge RN => (Q+:1'b0)) = 0;
		(posedge CK => (Q+:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_NOT_SE, posedge D &&& adacond_RN_AND_NOT_RT_AND_NOT_SE, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_NOT_SE, negedge D &&& adacond_RN_AND_NOT_RT_AND_NOT_SE, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (negedge CK &&& adacond_OP_D_AND_RN_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_CP, negedge RT &&& adacond_OP_D_AND_RN_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_CP, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (negedge CK &&& adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_CP, negedge RT &&& adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_CP, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (posedge CK &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, posedge SE &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, negedge SE &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, posedge SE &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, negedge SE &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_SE, posedge SI &&& adacond_RN_AND_NOT_RT_AND_SE, 0, 0, notifier,,, delayed_CK, delayed_SI);
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_SE, negedge SI &&& adacond_RN_AND_NOT_RT_AND_SE, 0, 0, notifier,,, delayed_CK, delayed_SI);
		$recovery (posedge RN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, notifier);
		$hold (posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, posedge RN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, notifier);
		$width (negedge RN &&& adacond_CK_AND_NOT_RT, 0, 0, notifier);
		$width (negedge RN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge RN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (posedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (posedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (negedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module SRDFFRX1 (Q, QN, D, RT, SE, SI, RN, CK);
	output Q, QN;
	input D, RT, SE, SI, RN, CK;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_SE, delayed_SI, delayed_CK;

	// Function
	wire delayed_RT__bar, delayed_SE__bar, int_fwire_0;
	wire int_fwire_1, int_fwire_2, int_fwire_d;
	wire int_fwire_IQ, int_fwire_IQN, int_fwire_r;
	wire xcr_0;

	not (delayed_SE__bar, delayed_SE);
	and (int_fwire_0, delayed_SE__bar, delayed_D);
	and (int_fwire_1, delayed_SE, delayed_SI);
	or (int_fwire_2, int_fwire_1, int_fwire_0);
	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, int_fwire_2);
	not (int_fwire_r, RN);
	altos_dff_r_err (xcr_0, delayed_CK, int_fwire_d, int_fwire_r);
	altos_dff_r (int_fwire_IQ, notifier, delayed_CK, int_fwire_d, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_CK_AND_NOT_RT, adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI;
	wire adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP;
	wire adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_CP, adacond_OP_D_AND_RN_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_CP, adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP;
	wire adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, adacond_RN_AND_NOT_RT_AND_NOT_SE, adacond_RN_AND_NOT_RT_AND_SE;
	wire CK__bar, D__bar, int_twire_0;
	wire int_twire_1, int_twire_2, int_twire_3;
	wire int_twire_4, int_twire_5, int_twire_6;
	wire int_twire_7, int_twire_8, int_twire_9;
	wire int_twire_10, int_twire_11, int_twire_12;
	wire int_twire_13, int_twire_14, int_twire_15;
	wire int_twire_16, int_twire_17, int_twire_18;
	wire int_twire_19, int_twire_20, RT__bar;
	wire SE__bar, SI__bar;


	// Additional timing gates
	not (SE__bar, SE);
	not (RT__bar, RT);
	and (adacond_RN_AND_NOT_RT_AND_NOT_SE, RN, RT__bar, SE__bar);
	not (D__bar, D);
	and (int_twire_0, D__bar, RN, SE, SI);
	and (int_twire_1, D, RN, SE__bar);
	and (int_twire_2, D, RN, SE, SI);
	or (adacond_OP_D_AND_RN_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_CP, int_twire_2, int_twire_1, int_twire_0);
	and (int_twire_3, D__bar, RN, SE__bar);
	not (SI__bar, SI);
	and (int_twire_4, D__bar, RN, SE, SI__bar);
	and (int_twire_5, D, RN, SE, SI__bar);
	or (adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_CP, int_twire_5, int_twire_4, int_twire_3);
	and (adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, D, RN, RT__bar, SI__bar);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, D__bar, RN, RT__bar, SI);
	and (adacond_RN_AND_NOT_RT_AND_SE, RN, RT__bar, SE);
	and (int_twire_6, D__bar, RT__bar, SE, SI);
	and (int_twire_7, D, RT__bar, SE__bar);
	and (int_twire_8, D, RT__bar, SE, SI);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_8, int_twire_7, int_twire_6);
	and (adacond_CK_AND_NOT_RT, CK, RT__bar);
	not (CK__bar, CK);
	and (int_twire_9, CK__bar, D__bar, RT__bar, SE, SI);
	and (int_twire_10, CK__bar, D, RT__bar, SE__bar);
	and (int_twire_11, CK__bar, D, RT__bar, SE, SI);
	or (adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_11, int_twire_10, int_twire_9);
	and (int_twire_12, CK__bar, D__bar, RT__bar, SE__bar);
	and (int_twire_13, CK__bar, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_14, CK__bar, D, RT__bar, SE, SI__bar);
	or (adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_14, int_twire_13, int_twire_12);
	and (int_twire_15, D__bar, RN, RT__bar, SE, SI);
	and (int_twire_16, D, RN, RT__bar, SE__bar);
	and (int_twire_17, D, RN, RT__bar, SE, SI);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_17, int_twire_16, int_twire_15);
	and (int_twire_18, D__bar, RN, RT__bar, SE__bar);
	and (int_twire_19, D__bar, RN, RT__bar, SE, SI__bar);
	and (int_twire_20, D, RN, RT__bar, SE, SI__bar);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, int_twire_20, int_twire_19, int_twire_18);

	specify
		ifnone (RT => Q) = 0;
		if ((CK&&RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CK&&!RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CK&&!RN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CK&&!RT))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CK&&D&&!RT&&SE&&SI) | (!CK&&D&&!RT&&!SE) | (!CK&&!D&&!RT&&SE&&SI))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CK&&D&&!RT&&SE&&!SI) | (!CK&&!D&&!RT&&SE&&!SI) | (!CK&&!D&&!RT&&!SE))
			(negedge RN => (Q+:1'b0)) = 0;
		(posedge CK => (Q+:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		if ((CK&&RN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((CK&&!RN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((!CK&&!RN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((CK&&!RT))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((!CK&&D&&!RT&&SE&&SI) | (!CK&&D&&!RT&&!SE) | (!CK&&!D&&!RT&&SE&&SI))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((!CK&&D&&!RT&&SE&&!SI) | (!CK&&!D&&!RT&&SE&&!SI) | (!CK&&!D&&!RT&&!SE))
			(negedge RN => (QN-:1'b0)) = 0;
		(posedge CK => (QN-:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_NOT_SE, posedge D &&& adacond_RN_AND_NOT_RT_AND_NOT_SE, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_NOT_SE, negedge D &&& adacond_RN_AND_NOT_RT_AND_NOT_SE, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (negedge CK &&& adacond_OP_D_AND_RN_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_CP, negedge RT &&& adacond_OP_D_AND_RN_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_CP, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (negedge CK &&& adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_CP, negedge RT &&& adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_CP, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (posedge CK &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, posedge SE &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, negedge SE &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, posedge SE &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, negedge SE &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_SE, posedge SI &&& adacond_RN_AND_NOT_RT_AND_SE, 0, 0, notifier,,, delayed_CK, delayed_SI);
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_SE, negedge SI &&& adacond_RN_AND_NOT_RT_AND_SE, 0, 0, notifier,,, delayed_CK, delayed_SI);
		$recovery (posedge RN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, notifier);
		$hold (posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, posedge RN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, notifier);
		$width (negedge RN &&& adacond_CK_AND_NOT_RT, 0, 0, notifier);
		$width (negedge RN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge RN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (posedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (posedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (negedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module SRDFFSQX1 (Q, D, RT, SE, SI, SN, CK);
	output Q;
	input D, RT, SE, SI, SN, CK;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_SE, delayed_SI, delayed_CK;

	// Function
	wire delayed_RT__bar, delayed_SE__bar, int_fwire_0;
	wire int_fwire_1, int_fwire_2, int_fwire_d;
	wire int_fwire_IQ, int_fwire_s, xcr_0;

	not (delayed_SE__bar, delayed_SE);
	and (int_fwire_0, delayed_SE__bar, delayed_D);
	and (int_fwire_1, delayed_SE, delayed_SI);
	or (int_fwire_2, int_fwire_1, int_fwire_0);
	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, int_fwire_2);
	not (int_fwire_s, SN);
	altos_dff_s_err (xcr_0, delayed_CK, int_fwire_d, int_fwire_s);
	altos_dff_s (int_fwire_IQ, notifier, delayed_CK, int_fwire_d, int_fwire_s, xcr_0);
	buf (Q, int_fwire_IQ);

	// Timing

	// Additional timing wires
	wire adacond_CK_AND_NOT_RT, adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN;
	wire adacond_NOT_RT_AND_NOT_SE_AND_SN, adacond_NOT_RT_AND_SE_AND_SN, adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP;
	wire adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, adacond_OP_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_SE_AND_SN_CP;
	wire adacond_OP_D_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_SI_AND_SN_CP, adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP;
	wire CK__bar, D__bar, int_twire_0;
	wire int_twire_1, int_twire_2, int_twire_3;
	wire int_twire_4, int_twire_5, int_twire_6;
	wire int_twire_7, int_twire_8, int_twire_9;
	wire int_twire_10, int_twire_11, int_twire_12;
	wire int_twire_13, int_twire_14, int_twire_15;
	wire int_twire_16, int_twire_17, int_twire_18;
	wire int_twire_19, int_twire_20, RT__bar;
	wire SE__bar, SI__bar;


	// Additional timing gates
	not (SE__bar, SE);
	not (RT__bar, RT);
	and (adacond_NOT_RT_AND_NOT_SE_AND_SN, RT__bar, SE__bar, SN);
	not (D__bar, D);
	and (int_twire_0, D__bar, SE, SI, SN);
	and (int_twire_1, D, SE__bar, SN);
	and (int_twire_2, D, SE, SI, SN);
	or (adacond_OP_D_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_SI_AND_SN_CP, int_twire_2, int_twire_1, int_twire_0);
	and (int_twire_3, D__bar, SE__bar, SN);
	not (SI__bar, SI);
	and (int_twire_4, D__bar, SE, SI__bar, SN);
	and (int_twire_5, D, SE, SI__bar, SN);
	or (adacond_OP_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_SE_AND_SN_CP, int_twire_5, int_twire_4, int_twire_3);
	and (adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, D, RT__bar, SI__bar, SN);
	and (adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, D__bar, RT__bar, SI, SN);
	and (adacond_NOT_RT_AND_SE_AND_SN, RT__bar, SE, SN);
	and (int_twire_6, D__bar, RT__bar, SE__bar);
	and (int_twire_7, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_8, D, RT__bar, SE, SI__bar);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_8, int_twire_7, int_twire_6);
	and (adacond_CK_AND_NOT_RT, CK, RT__bar);
	not (CK__bar, CK);
	and (int_twire_9, CK__bar, D__bar, RT__bar, SE, SI);
	and (int_twire_10, CK__bar, D, RT__bar, SE__bar);
	and (int_twire_11, CK__bar, D, RT__bar, SE, SI);
	or (adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_11, int_twire_10, int_twire_9);
	and (int_twire_12, CK__bar, D__bar, RT__bar, SE__bar);
	and (int_twire_13, CK__bar, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_14, CK__bar, D, RT__bar, SE, SI__bar);
	or (adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_14, int_twire_13, int_twire_12);
	and (int_twire_15, D__bar, RT__bar, SE, SI, SN);
	and (int_twire_16, D, RT__bar, SE__bar, SN);
	and (int_twire_17, D, RT__bar, SE, SI, SN);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, int_twire_17, int_twire_16, int_twire_15);
	and (int_twire_18, D__bar, RT__bar, SE__bar, SN);
	and (int_twire_19, D__bar, RT__bar, SE, SI__bar, SN);
	and (int_twire_20, D, RT__bar, SE, SI__bar, SN);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, int_twire_20, int_twire_19, int_twire_18);

	specify
		if ((CK&&SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CK&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CK&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CK&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&D&&!RT&&SE&&SI) | (!CK&&D&&!RT&&!SE) | (!CK&&!D&&!RT&&SE&&SI))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&D&&!RT&&SE&&!SI) | (!CK&&!D&&!RT&&SE&&!SI) | (!CK&&!D&&!RT&&!SE))
			(negedge SN => (Q+:1'b1)) = 0;
		(posedge CK => (Q+:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_NOT_SE_AND_SN, posedge D &&& adacond_NOT_RT_AND_NOT_SE_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_NOT_SE_AND_SN, negedge D &&& adacond_NOT_RT_AND_NOT_SE_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (negedge CK &&& adacond_OP_D_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_SI_AND_SN_CP, negedge RT &&& adacond_OP_D_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (negedge CK &&& adacond_OP_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_SE_AND_SN_CP, negedge RT &&& adacond_OP_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_SE_AND_SN_CP, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (posedge CK &&& adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, posedge SE &&& adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, negedge SE &&& adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, posedge SE &&& adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, negedge SE &&& adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_SE_AND_SN, posedge SI &&& adacond_NOT_RT_AND_SE_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SI);
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_SE_AND_SN, negedge SI &&& adacond_NOT_RT_AND_SE_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SI);
		$recovery (posedge SN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, notifier);
		$hold (posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, posedge SN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, notifier);
		$width (negedge SN &&& adacond_CK_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge SN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (negedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
		$width (negedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module SRDFFSRQX1 (Q, D, RT, SE, SI, RN, SN, CK);
	output Q;
	input D, RT, SE, SI, RN, SN, CK;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_SE, delayed_SI, delayed_RN, delayed_SN, delayed_CK;

	// Function
	wire delayed_RT__bar, delayed_SE__bar, int_fwire_0;
	wire int_fwire_1, int_fwire_2, int_fwire_d;
	wire int_fwire_IQ, int_fwire_r, int_fwire_s;
	wire xcr_0;

	not (delayed_SE__bar, delayed_SE);
	and (int_fwire_0, delayed_SE__bar, delayed_D);
	and (int_fwire_1, delayed_SE, delayed_SI);
	or (int_fwire_2, int_fwire_1, int_fwire_0);
	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, int_fwire_2);
	not (int_fwire_s, delayed_SN);
	not (int_fwire_r, delayed_RN);
	altos_dff_sr_err (xcr_0, delayed_CK, int_fwire_d, int_fwire_s, int_fwire_r);
	altos_dff_sr_1 (int_fwire_IQ, notifier, delayed_CK, int_fwire_d, int_fwire_s, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);

	// Timing

	// Additional timing wires
	wire adacond_CK_AND_NOT_RT, adacond_CK_AND_NOT_RT_AND_SN, adacond_CK_AND_RN_AND_NOT_RT;
	wire adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP;
	wire adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP;
	wire adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_AND_SN_CP, adacond_OP_D_AND_RN_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_AND_SN_CP, adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP;
	wire adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP;
	wire adacond_OP_NOT_CK_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_NOT_CK_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN;
	wire adacond_RN_AND_NOT_RT_AND_SE_AND_SN, CK__bar, D__bar;
	wire int_twire_0, int_twire_1, int_twire_2;
	wire int_twire_3, int_twire_4, int_twire_5;
	wire int_twire_6, int_twire_7, int_twire_8;
	wire int_twire_9, int_twire_10, int_twire_11;
	wire int_twire_12, int_twire_13, int_twire_14;
	wire int_twire_15, int_twire_16, int_twire_17;
	wire int_twire_18, int_twire_19, int_twire_20;
	wire int_twire_21, int_twire_22, int_twire_23;
	wire int_twire_24, int_twire_25, int_twire_26;
	wire int_twire_27, int_twire_28, int_twire_29;
	wire int_twire_30, int_twire_31, int_twire_32;
	wire int_twire_33, int_twire_34, int_twire_35;
	wire RT__bar, SE__bar, SI__bar;


	// Additional timing gates
	not (SE__bar, SE);
	not (RT__bar, RT);
	and (adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, RN, RT__bar, SE__bar, SN);
	not (D__bar, D);
	and (int_twire_0, D__bar, RN, SE, SI, SN);
	and (int_twire_1, D, RN, SE__bar, SN);
	and (int_twire_2, D, RN, SE, SI, SN);
	or (adacond_OP_D_AND_RN_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_AND_SN_CP, int_twire_2, int_twire_1, int_twire_0);
	and (int_twire_3, D__bar, RN, SE__bar, SN);
	not (SI__bar, SI);
	and (int_twire_4, D__bar, RN, SE, SI__bar, SN);
	and (int_twire_5, D, RN, SE, SI__bar, SN);
	or (adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_AND_SN_CP, int_twire_5, int_twire_4, int_twire_3);
	and (adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, D, RN, RT__bar, SI__bar, SN);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, D__bar, RN, RT__bar, SI, SN);
	and (adacond_RN_AND_NOT_RT_AND_SE_AND_SN, RN, RT__bar, SE, SN);
	and (int_twire_6, D__bar, RT__bar, SE, SI, SN);
	and (int_twire_7, D, RT__bar, SE__bar, SN);
	and (int_twire_8, D, RT__bar, SE, SI, SN);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, int_twire_8, int_twire_7, int_twire_6);
	and (adacond_CK_AND_NOT_RT_AND_SN, CK, RT__bar, SN);
	not (CK__bar, CK);
	and (int_twire_9, CK__bar, D__bar, RT__bar, SE, SI, SN);
	and (int_twire_10, CK__bar, D, RT__bar, SE__bar, SN);
	and (int_twire_11, CK__bar, D, RT__bar, SE, SI, SN);
	or (adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, int_twire_11, int_twire_10, int_twire_9);
	and (int_twire_12, CK__bar, D__bar, RT__bar, SE__bar, SN);
	and (int_twire_13, CK__bar, D__bar, RT__bar, SE, SI__bar, SN);
	and (int_twire_14, CK__bar, D, RT__bar, SE, SI__bar, SN);
	or (adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, int_twire_14, int_twire_13, int_twire_12);
	and (int_twire_15, D__bar, RN, RT__bar, SE__bar);
	and (int_twire_16, D__bar, RN, RT__bar, SE, SI__bar);
	and (int_twire_17, D, RN, RT__bar, SE, SI__bar);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, int_twire_17, int_twire_16, int_twire_15);
	and (adacond_CK_AND_NOT_RT, CK, RT__bar);
	and (int_twire_18, CK__bar, D__bar, RT__bar, SE, SI);
	and (int_twire_19, CK__bar, D, RT__bar, SE__bar);
	and (int_twire_20, CK__bar, D, RT__bar, SE, SI);
	or (adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_20, int_twire_19, int_twire_18);
	and (int_twire_21, CK__bar, D__bar, RT__bar, SE__bar);
	and (int_twire_22, CK__bar, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_23, CK__bar, D, RT__bar, SE, SI__bar);
	or (adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_23, int_twire_22, int_twire_21);
	and (adacond_CK_AND_RN_AND_NOT_RT, CK, RN, RT__bar);
	and (int_twire_24, CK__bar, D__bar, RN, RT__bar, SE, SI);
	and (int_twire_25, CK__bar, D, RN, RT__bar, SE__bar);
	and (int_twire_26, CK__bar, D, RN, RT__bar, SE, SI);
	or (adacond_OP_NOT_CK_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_26, int_twire_25, int_twire_24);
	and (int_twire_27, CK__bar, D__bar, RN, RT__bar, SE__bar);
	and (int_twire_28, CK__bar, D__bar, RN, RT__bar, SE, SI__bar);
	and (int_twire_29, CK__bar, D, RN, RT__bar, SE, SI__bar);
	or (adacond_OP_NOT_CK_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, int_twire_29, int_twire_28, int_twire_27);
	and (int_twire_30, D__bar, RN, RT__bar, SE, SI, SN);
	and (int_twire_31, D, RN, RT__bar, SE__bar, SN);
	and (int_twire_32, D, RN, RT__bar, SE, SI, SN);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, int_twire_32, int_twire_31, int_twire_30);
	and (int_twire_33, D__bar, RN, RT__bar, SE__bar, SN);
	and (int_twire_34, D__bar, RN, RT__bar, SE, SI__bar, SN);
	and (int_twire_35, D, RN, RT__bar, SE, SI__bar, SN);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, int_twire_35, int_twire_34, int_twire_33);

	specify
		if ((CK&&RN&&SN))
			(RT => Q) = 0;
		if ((CK&&!RN&&SN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CK&&!RN&&SN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CK&&RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CK&&!RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CK&&RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CK&&!RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CK&&!RT&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CK&&D&&!RT&&SE&&SI&&SN) | (!CK&&D&&!RT&&!SE&&SN) | (!CK&&!D&&!RT&&SE&&SI&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CK&&D&&!RT&&SE&&!SI&&SN) | (!CK&&!D&&!RT&&SE&&!SI&&SN) | (!CK&&!D&&!RT&&!SE&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((CK&&!RN&&!RT))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((!CK&&D&&!RN&&!RT&&SE&&SI) | (!CK&&D&&!RN&&!RT&&!SE) | (!CK&&!D&&!RN&&!RT&&SE&&SI))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((!CK&&D&&!RN&&!RT&&SE&&!SI) | (!CK&&!D&&!RN&&!RT&&SE&&!SI) | (!CK&&!D&&!RN&&!RT&&!SE))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((CK&&RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CK&&!RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&D&&RN&&!RT&&SE&&SI) | (!CK&&D&&RN&&!RT&&!SE) | (!CK&&!D&&RN&&!RT&&SE&&SI))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&D&&RN&&!RT&&SE&&!SI) | (!CK&&!D&&RN&&!RT&&SE&&!SI) | (!CK&&!D&&RN&&!RT&&!SE))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&D&&!RN&&!RT&&SE&&SI) | (!CK&&D&&!RN&&!RT&&!SE) | (!CK&&!D&&!RN&&!RT&&SE&&SI))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&D&&!RN&&!RT&&SE&&!SI) | (!CK&&!D&&!RN&&!RT&&SE&&!SI) | (!CK&&!D&&!RN&&!RT&&!SE))
			(negedge SN => (Q+:1'b1)) = 0;
		(posedge CK => (Q+:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, posedge D &&& adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, negedge D &&& adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (negedge CK &&& adacond_OP_D_AND_RN_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_AND_SN_CP, negedge RT &&& adacond_OP_D_AND_RN_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (negedge CK &&& adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_AND_SN_CP, negedge RT &&& adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_AND_SN_CP, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (posedge CK &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, posedge SE &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, negedge SE &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, posedge SE &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, negedge SE &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_SE_AND_SN, posedge SI &&& adacond_RN_AND_NOT_RT_AND_SE_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SI);
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_SE_AND_SN, negedge SI &&& adacond_RN_AND_NOT_RT_AND_SE_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SI);
		$setuphold (posedge RN &&& adacond_CK_AND_NOT_RT, posedge SN &&& adacond_CK_AND_NOT_RT, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$setuphold (posedge RN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, posedge SN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$setuphold (posedge RN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, posedge SN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$recovery (posedge RN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, notifier);
		$hold (posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, posedge RN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, notifier);
		$recovery (posedge SN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, posedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, notifier);
		$hold (posedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, posedge SN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, notifier);
		$width (negedge RN &&& adacond_CK_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge RN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (negedge RN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
		$width (negedge SN &&& adacond_CK_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_OP_NOT_CK_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge SN &&& adacond_OP_NOT_CK_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (posedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (negedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (posedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
		$width (negedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module SRDFFSRX1 (Q, QN, D, RT, SE, SI, RN, SN, CK);
	output Q, QN;
	input D, RT, SE, SI, RN, SN, CK;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_SE, delayed_SI, delayed_RN, delayed_SN, delayed_CK;

	// Function
	wire delayed_RT__bar, delayed_SE__bar, int_fwire_0;
	wire int_fwire_1, int_fwire_2, int_fwire_d;
	wire int_fwire_IQ, int_fwire_IQN, int_fwire_r;
	wire int_fwire_s, xcr_0;

	not (delayed_SE__bar, delayed_SE);
	and (int_fwire_0, delayed_SE__bar, delayed_D);
	and (int_fwire_1, delayed_SE, delayed_SI);
	or (int_fwire_2, int_fwire_1, int_fwire_0);
	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, int_fwire_2);
	not (int_fwire_s, delayed_SN);
	not (int_fwire_r, delayed_RN);
	altos_dff_sr_err (xcr_0, delayed_CK, int_fwire_d, int_fwire_s, int_fwire_r);
	altos_dff_sr_1 (int_fwire_IQ, notifier, delayed_CK, int_fwire_d, int_fwire_s, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_CK_AND_NOT_RT, adacond_CK_AND_NOT_RT_AND_SN, adacond_CK_AND_RN_AND_NOT_RT;
	wire adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP;
	wire adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP;
	wire adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_AND_SN_CP, adacond_OP_D_AND_RN_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_AND_SN_CP, adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP;
	wire adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP;
	wire adacond_OP_NOT_CK_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_NOT_CK_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN;
	wire adacond_RN_AND_NOT_RT_AND_SE_AND_SN, CK__bar, D__bar;
	wire int_twire_0, int_twire_1, int_twire_2;
	wire int_twire_3, int_twire_4, int_twire_5;
	wire int_twire_6, int_twire_7, int_twire_8;
	wire int_twire_9, int_twire_10, int_twire_11;
	wire int_twire_12, int_twire_13, int_twire_14;
	wire int_twire_15, int_twire_16, int_twire_17;
	wire int_twire_18, int_twire_19, int_twire_20;
	wire int_twire_21, int_twire_22, int_twire_23;
	wire int_twire_24, int_twire_25, int_twire_26;
	wire int_twire_27, int_twire_28, int_twire_29;
	wire int_twire_30, int_twire_31, int_twire_32;
	wire int_twire_33, int_twire_34, int_twire_35;
	wire RT__bar, SE__bar, SI__bar;


	// Additional timing gates
	not (SE__bar, SE);
	not (RT__bar, RT);
	and (adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, RN, RT__bar, SE__bar, SN);
	not (D__bar, D);
	and (int_twire_0, D__bar, RN, SE, SI, SN);
	and (int_twire_1, D, RN, SE__bar, SN);
	and (int_twire_2, D, RN, SE, SI, SN);
	or (adacond_OP_D_AND_RN_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_AND_SN_CP, int_twire_2, int_twire_1, int_twire_0);
	and (int_twire_3, D__bar, RN, SE__bar, SN);
	not (SI__bar, SI);
	and (int_twire_4, D__bar, RN, SE, SI__bar, SN);
	and (int_twire_5, D, RN, SE, SI__bar, SN);
	or (adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_AND_SN_CP, int_twire_5, int_twire_4, int_twire_3);
	and (adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, D, RN, RT__bar, SI__bar, SN);
	and (adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, D__bar, RN, RT__bar, SI, SN);
	and (adacond_RN_AND_NOT_RT_AND_SE_AND_SN, RN, RT__bar, SE, SN);
	and (int_twire_6, D__bar, RT__bar, SE, SI, SN);
	and (int_twire_7, D, RT__bar, SE__bar, SN);
	and (int_twire_8, D, RT__bar, SE, SI, SN);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, int_twire_8, int_twire_7, int_twire_6);
	and (adacond_CK_AND_NOT_RT_AND_SN, CK, RT__bar, SN);
	not (CK__bar, CK);
	and (int_twire_9, CK__bar, D__bar, RT__bar, SE, SI, SN);
	and (int_twire_10, CK__bar, D, RT__bar, SE__bar, SN);
	and (int_twire_11, CK__bar, D, RT__bar, SE, SI, SN);
	or (adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, int_twire_11, int_twire_10, int_twire_9);
	and (int_twire_12, CK__bar, D__bar, RT__bar, SE__bar, SN);
	and (int_twire_13, CK__bar, D__bar, RT__bar, SE, SI__bar, SN);
	and (int_twire_14, CK__bar, D, RT__bar, SE, SI__bar, SN);
	or (adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, int_twire_14, int_twire_13, int_twire_12);
	and (int_twire_15, D__bar, RN, RT__bar, SE__bar);
	and (int_twire_16, D__bar, RN, RT__bar, SE, SI__bar);
	and (int_twire_17, D, RN, RT__bar, SE, SI__bar);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, int_twire_17, int_twire_16, int_twire_15);
	and (adacond_CK_AND_NOT_RT, CK, RT__bar);
	and (int_twire_18, CK__bar, D__bar, RT__bar, SE, SI);
	and (int_twire_19, CK__bar, D, RT__bar, SE__bar);
	and (int_twire_20, CK__bar, D, RT__bar, SE, SI);
	or (adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_20, int_twire_19, int_twire_18);
	and (int_twire_21, CK__bar, D__bar, RT__bar, SE__bar);
	and (int_twire_22, CK__bar, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_23, CK__bar, D, RT__bar, SE, SI__bar);
	or (adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_23, int_twire_22, int_twire_21);
	and (adacond_CK_AND_RN_AND_NOT_RT, CK, RN, RT__bar);
	and (int_twire_24, CK__bar, D__bar, RN, RT__bar, SE, SI);
	and (int_twire_25, CK__bar, D, RN, RT__bar, SE__bar);
	and (int_twire_26, CK__bar, D, RN, RT__bar, SE, SI);
	or (adacond_OP_NOT_CK_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_26, int_twire_25, int_twire_24);
	and (int_twire_27, CK__bar, D__bar, RN, RT__bar, SE__bar);
	and (int_twire_28, CK__bar, D__bar, RN, RT__bar, SE, SI__bar);
	and (int_twire_29, CK__bar, D, RN, RT__bar, SE, SI__bar);
	or (adacond_OP_NOT_CK_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, int_twire_29, int_twire_28, int_twire_27);
	and (int_twire_30, D__bar, RN, RT__bar, SE, SI, SN);
	and (int_twire_31, D, RN, RT__bar, SE__bar, SN);
	and (int_twire_32, D, RN, RT__bar, SE, SI, SN);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, int_twire_32, int_twire_31, int_twire_30);
	and (int_twire_33, D__bar, RN, RT__bar, SE__bar, SN);
	and (int_twire_34, D__bar, RN, RT__bar, SE, SI__bar, SN);
	and (int_twire_35, D, RN, RT__bar, SE, SI__bar, SN);
	or (adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, int_twire_35, int_twire_34, int_twire_33);

	specify
		if ((CK&&RN&&SN))
			(RT => Q) = 0;
		if ((CK&&!RN&&SN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((!CK&&!RN&&SN))
			(negedge RT => (Q+:1'b0)) = 0;
		if ((CK&&RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CK&&!RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CK&&RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CK&&!RN&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CK&&!RT&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CK&&D&&!RT&&SE&&SI&&SN) | (!CK&&D&&!RT&&!SE&&SN) | (!CK&&!D&&!RT&&SE&&SI&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((!CK&&D&&!RT&&SE&&!SI&&SN) | (!CK&&!D&&!RT&&SE&&!SI&&SN) | (!CK&&!D&&!RT&&!SE&&SN))
			(negedge RN => (Q+:1'b0)) = 0;
		if ((CK&&!RN&&!RT))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((!CK&&D&&!RN&&!RT&&SE&&SI) | (!CK&&D&&!RN&&!RT&&!SE) | (!CK&&!D&&!RN&&!RT&&SE&&SI))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((!CK&&D&&!RN&&!RT&&SE&&!SI) | (!CK&&!D&&!RN&&!RT&&SE&&!SI) | (!CK&&!D&&!RN&&!RT&&!SE))
			(posedge SN => (Q+:1'b0)) = 0;
		if ((CK&&RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((CK&&!RN&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&D&&RN&&!RT&&SE&&SI) | (!CK&&D&&RN&&!RT&&!SE) | (!CK&&!D&&RN&&!RT&&SE&&SI))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&D&&RN&&!RT&&SE&&!SI) | (!CK&&!D&&RN&&!RT&&SE&&!SI) | (!CK&&!D&&RN&&!RT&&!SE))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&D&&!RN&&!RT&&SE&&SI) | (!CK&&D&&!RN&&!RT&&!SE) | (!CK&&!D&&!RN&&!RT&&SE&&SI))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&D&&!RN&&!RT&&SE&&!SI) | (!CK&&!D&&!RN&&!RT&&SE&&!SI) | (!CK&&!D&&!RN&&!RT&&!SE))
			(negedge SN => (Q+:1'b1)) = 0;
		(posedge CK => (Q+:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		if ((CK&&RN&&SN))
			(RT => QN) = 0;
		if ((CK&&RN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((CK&&!RN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((!CK&&RN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((!CK&&!RN&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((CK&&!RN&&SN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((!CK&&!RN&&SN))
			(negedge RT => (QN+:1'b1)) = 0;
		if ((CK&&!RT&&SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((!CK&&D&&!RT&&SE&&SI&&SN) | (!CK&&D&&!RT&&!SE&&SN) | (!CK&&!D&&!RT&&SE&&SI&&SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((!CK&&D&&!RT&&SE&&!SI&&SN) | (!CK&&!D&&!RT&&SE&&!SI&&SN) | (!CK&&!D&&!RT&&!SE&&SN))
			(negedge RN => (QN-:1'b0)) = 0;
		if ((CK&&RN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((CK&&!RN&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!CK&&D&&RN&&!RT&&SE&&SI) | (!CK&&D&&RN&&!RT&&!SE) | (!CK&&!D&&RN&&!RT&&SE&&SI))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!CK&&D&&RN&&!RT&&SE&&!SI) | (!CK&&!D&&RN&&!RT&&SE&&!SI) | (!CK&&!D&&RN&&!RT&&!SE))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!CK&&D&&!RN&&!RT&&SE&&SI) | (!CK&&D&&!RN&&!RT&&!SE) | (!CK&&!D&&!RN&&!RT&&SE&&SI))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!CK&&D&&!RN&&!RT&&SE&&!SI) | (!CK&&!D&&!RN&&!RT&&SE&&!SI) | (!CK&&!D&&!RN&&!RT&&!SE))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((CK&&!RN&&!RT))
			(posedge SN => (QN-:1'b0)) = 0;
		if ((!CK&&D&&!RN&&!RT&&SE&&SI) | (!CK&&D&&!RN&&!RT&&!SE) | (!CK&&!D&&!RN&&!RT&&SE&&SI))
			(posedge SN => (QN-:1'b0)) = 0;
		if ((!CK&&D&&!RN&&!RT&&SE&&!SI) | (!CK&&!D&&!RN&&!RT&&SE&&!SI) | (!CK&&!D&&!RN&&!RT&&!SE))
			(posedge SN => (QN-:1'b0)) = 0;
		(posedge CK => (QN-:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, posedge D &&& adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, negedge D &&& adacond_RN_AND_NOT_RT_AND_NOT_SE_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (negedge CK &&& adacond_OP_D_AND_RN_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_AND_SN_CP, negedge RT &&& adacond_OP_D_AND_RN_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (negedge CK &&& adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_AND_SN_CP, negedge RT &&& adacond_OP_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_SE_AND_SN_CP, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (posedge CK &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, posedge SE &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, negedge SE &&& adacond_D_AND_RN_AND_NOT_RT_AND_NOT_SI_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, posedge SE &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, negedge SE &&& adacond_NOT_D_AND_RN_AND_NOT_RT_AND_SI_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_SE_AND_SN, posedge SI &&& adacond_RN_AND_NOT_RT_AND_SE_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SI);
		$setuphold (posedge CK &&& adacond_RN_AND_NOT_RT_AND_SE_AND_SN, negedge SI &&& adacond_RN_AND_NOT_RT_AND_SE_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SI);
		$setuphold (posedge RN &&& adacond_CK_AND_NOT_RT, posedge SN &&& adacond_CK_AND_NOT_RT, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$setuphold (posedge RN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, posedge SN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$setuphold (posedge RN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, posedge SN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier,,, delayed_RN, delayed_SN);
		$recovery (posedge RN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, notifier);
		$hold (posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, posedge RN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, notifier);
		$recovery (posedge SN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, posedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, notifier);
		$hold (posedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, posedge SN &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, notifier);
		$width (negedge RN &&& adacond_CK_AND_NOT_RT_AND_SN, 0, 0, notifier);
		$width (negedge RN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (negedge RN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
		$width (negedge SN &&& adacond_CK_AND_RN_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_OP_NOT_CK_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge SN &&& adacond_OP_NOT_CK_AND_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (posedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (negedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (posedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
		$width (negedge CK &&& adacond_OP_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_RN_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module SRDFFSX1 (Q, QN, D, RT, SE, SI, SN, CK);
	output Q, QN;
	input D, RT, SE, SI, SN, CK;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_SE, delayed_SI, delayed_CK;

	// Function
	wire delayed_RT__bar, delayed_SE__bar, int_fwire_0;
	wire int_fwire_1, int_fwire_2, int_fwire_d;
	wire int_fwire_IQ, int_fwire_IQN, int_fwire_s;
	wire xcr_0;

	not (delayed_SE__bar, delayed_SE);
	and (int_fwire_0, delayed_SE__bar, delayed_D);
	and (int_fwire_1, delayed_SE, delayed_SI);
	or (int_fwire_2, int_fwire_1, int_fwire_0);
	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, int_fwire_2);
	not (int_fwire_s, SN);
	altos_dff_s_err (xcr_0, delayed_CK, int_fwire_d, int_fwire_s);
	altos_dff_s (int_fwire_IQ, notifier, delayed_CK, int_fwire_d, int_fwire_s, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_CK_AND_NOT_RT, adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN;
	wire adacond_NOT_RT_AND_NOT_SE_AND_SN, adacond_NOT_RT_AND_SE_AND_SN, adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP;
	wire adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, adacond_OP_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_SE_AND_SN_CP;
	wire adacond_OP_D_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_SI_AND_SN_CP, adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP;
	wire CK__bar, D__bar, int_twire_0;
	wire int_twire_1, int_twire_2, int_twire_3;
	wire int_twire_4, int_twire_5, int_twire_6;
	wire int_twire_7, int_twire_8, int_twire_9;
	wire int_twire_10, int_twire_11, int_twire_12;
	wire int_twire_13, int_twire_14, int_twire_15;
	wire int_twire_16, int_twire_17, int_twire_18;
	wire int_twire_19, int_twire_20, RT__bar;
	wire SE__bar, SI__bar;


	// Additional timing gates
	not (SE__bar, SE);
	not (RT__bar, RT);
	and (adacond_NOT_RT_AND_NOT_SE_AND_SN, RT__bar, SE__bar, SN);
	not (D__bar, D);
	and (int_twire_0, D__bar, SE, SI, SN);
	and (int_twire_1, D, SE__bar, SN);
	and (int_twire_2, D, SE, SI, SN);
	or (adacond_OP_D_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_SI_AND_SN_CP, int_twire_2, int_twire_1, int_twire_0);
	and (int_twire_3, D__bar, SE__bar, SN);
	not (SI__bar, SI);
	and (int_twire_4, D__bar, SE, SI__bar, SN);
	and (int_twire_5, D, SE, SI__bar, SN);
	or (adacond_OP_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_SE_AND_SN_CP, int_twire_5, int_twire_4, int_twire_3);
	and (adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, D, RT__bar, SI__bar, SN);
	and (adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, D__bar, RT__bar, SI, SN);
	and (adacond_NOT_RT_AND_SE_AND_SN, RT__bar, SE, SN);
	and (int_twire_6, D__bar, RT__bar, SE__bar);
	and (int_twire_7, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_8, D, RT__bar, SE, SI__bar);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_8, int_twire_7, int_twire_6);
	and (adacond_CK_AND_NOT_RT, CK, RT__bar);
	not (CK__bar, CK);
	and (int_twire_9, CK__bar, D__bar, RT__bar, SE, SI);
	and (int_twire_10, CK__bar, D, RT__bar, SE__bar);
	and (int_twire_11, CK__bar, D, RT__bar, SE, SI);
	or (adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_11, int_twire_10, int_twire_9);
	and (int_twire_12, CK__bar, D__bar, RT__bar, SE__bar);
	and (int_twire_13, CK__bar, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_14, CK__bar, D, RT__bar, SE, SI__bar);
	or (adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_14, int_twire_13, int_twire_12);
	and (int_twire_15, D__bar, RT__bar, SE, SI, SN);
	and (int_twire_16, D, RT__bar, SE__bar, SN);
	and (int_twire_17, D, RT__bar, SE, SI, SN);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, int_twire_17, int_twire_16, int_twire_15);
	and (int_twire_18, D__bar, RT__bar, SE__bar, SN);
	and (int_twire_19, D__bar, RT__bar, SE, SI__bar, SN);
	and (int_twire_20, D, RT__bar, SE, SI__bar, SN);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, int_twire_20, int_twire_19, int_twire_18);

	specify
		if ((CK&&SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CK&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((!CK&&!SN))
			(negedge RT => (Q+:1'b1)) = 0;
		if ((CK&&!RT))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&D&&!RT&&SE&&SI) | (!CK&&D&&!RT&&!SE) | (!CK&&!D&&!RT&&SE&&SI))
			(negedge SN => (Q+:1'b1)) = 0;
		if ((!CK&&D&&!RT&&SE&&!SI) | (!CK&&!D&&!RT&&SE&&!SI) | (!CK&&!D&&!RT&&!SE))
			(negedge SN => (Q+:1'b1)) = 0;
		(posedge CK => (Q+:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		ifnone (RT => QN) = 0;
		if ((CK&&SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((CK&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((!CK&&!SN))
			(negedge RT => (QN+:1'b0)) = 0;
		if ((CK&&!RT))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!CK&&D&&!RT&&SE&&SI) | (!CK&&D&&!RT&&!SE) | (!CK&&!D&&!RT&&SE&&SI))
			(negedge SN => (QN-:1'b1)) = 0;
		if ((!CK&&D&&!RT&&SE&&!SI) | (!CK&&!D&&!RT&&SE&&!SI) | (!CK&&!D&&!RT&&!SE))
			(negedge SN => (QN-:1'b1)) = 0;
		(posedge CK => (QN-:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_NOT_SE_AND_SN, posedge D &&& adacond_NOT_RT_AND_NOT_SE_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_NOT_SE_AND_SN, negedge D &&& adacond_NOT_RT_AND_NOT_SE_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (negedge CK &&& adacond_OP_D_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_SI_AND_SN_CP, negedge RT &&& adacond_OP_D_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (negedge CK &&& adacond_OP_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_SE_AND_SN_CP, negedge RT &&& adacond_OP_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_SE_AND_SN_CP, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (posedge CK &&& adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, posedge SE &&& adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, negedge SE &&& adacond_D_AND_NOT_RT_AND_NOT_SI_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, posedge SE &&& adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, negedge SE &&& adacond_NOT_D_AND_NOT_RT_AND_SI_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_SE_AND_SN, posedge SI &&& adacond_NOT_RT_AND_SE_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SI);
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_SE_AND_SN, negedge SI &&& adacond_NOT_RT_AND_SE_AND_SN, 0, 0, notifier,,, delayed_CK, delayed_SI);
		$recovery (posedge SN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, notifier);
		$hold (posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, posedge SN &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, notifier);
		$width (negedge SN &&& adacond_CK_AND_NOT_RT, 0, 0, notifier);
		$width (negedge SN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_NOT_CK_AND_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge SN &&& adacond_OP_NOT_CK_AND_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_CK_AND_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (negedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_AND_SN_CP, 0, 0, notifier);
		$width (posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
		$width (negedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_AND_SN_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_AND_SN_CP, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type:  
`timescale 1ns/10ps
`celldefine
module SRDFFX1 (Q, QN, D, RT, SE, SI, CK);
	output Q, QN;
	input D, RT, SE, SI, CK;
	reg notifier;
	wire delayed_D, delayed_RT, delayed_SE, delayed_SI, delayed_CK;

	// Function
	wire delayed_RT__bar, delayed_SE__bar, int_fwire_0;
	wire int_fwire_1, int_fwire_2, int_fwire_d;
	wire int_fwire_IQ, int_fwire_IQN, xcr_0;

	not (delayed_SE__bar, delayed_SE);
	and (int_fwire_0, delayed_SE__bar, delayed_D);
	and (int_fwire_1, delayed_SE, delayed_SI);
	or (int_fwire_2, int_fwire_1, int_fwire_0);
	not (delayed_RT__bar, delayed_RT);
	and (int_fwire_d, delayed_RT__bar, int_fwire_2);
	altos_dff_err (xcr_0, delayed_CK, int_fwire_d);
	altos_dff (int_fwire_IQ, notifier, delayed_CK, int_fwire_d, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (QN, int_fwire_IQN);

	// Timing

	// Additional timing wires
	wire adacond_D_AND_NOT_RT_AND_NOT_SI, adacond_NOT_D_AND_NOT_RT_AND_SI, adacond_NOT_RT_AND_NOT_SE;
	wire adacond_NOT_RT_AND_SE, adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP;
	wire adacond_OP_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_SE_CP, adacond_OP_D_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_SE_CP_OR_OP_NOT_D_AND_SE_AND_SI_CP, D__bar;
	wire int_twire_0, int_twire_1, int_twire_2;
	wire int_twire_3, int_twire_4, int_twire_5;
	wire int_twire_6, int_twire_7, int_twire_8;
	wire int_twire_9, int_twire_10, int_twire_11;
	wire RT__bar, SE__bar, SI__bar;


	// Additional timing gates
	not (SE__bar, SE);
	not (RT__bar, RT);
	and (adacond_NOT_RT_AND_NOT_SE, RT__bar, SE__bar);
	not (D__bar, D);
	and (int_twire_0, D__bar, SE, SI);
	and (int_twire_1, D, SE__bar);
	and (int_twire_2, D, SE, SI);
	or (adacond_OP_D_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_SE_CP_OR_OP_NOT_D_AND_SE_AND_SI_CP, int_twire_2, int_twire_1, int_twire_0);
	and (int_twire_3, D__bar, SE__bar);
	not (SI__bar, SI);
	and (int_twire_4, D__bar, SE, SI__bar);
	and (int_twire_5, D, SE, SI__bar);
	or (adacond_OP_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_SE_CP, int_twire_5, int_twire_4, int_twire_3);
	and (adacond_D_AND_NOT_RT_AND_NOT_SI, D, RT__bar, SI__bar);
	and (adacond_NOT_D_AND_NOT_RT_AND_SI, D__bar, RT__bar, SI);
	and (adacond_NOT_RT_AND_SE, RT__bar, SE);
	and (int_twire_6, D__bar, RT__bar, SE, SI);
	and (int_twire_7, D, RT__bar, SE__bar);
	and (int_twire_8, D, RT__bar, SE, SI);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, int_twire_8, int_twire_7, int_twire_6);
	and (int_twire_9, D__bar, RT__bar, SE__bar);
	and (int_twire_10, D__bar, RT__bar, SE, SI__bar);
	and (int_twire_11, D, RT__bar, SE, SI__bar);
	or (adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, int_twire_11, int_twire_10, int_twire_9);

	specify
		(RT => Q) = 0;
		(posedge CK => (Q+:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		(RT => QN) = 0;
		(posedge CK => (QN-:((!RT && SE && SI) || (!RT && !SE && D)))) = 0;
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_NOT_SE, posedge D &&& adacond_NOT_RT_AND_NOT_SE, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_NOT_SE, negedge D &&& adacond_NOT_RT_AND_NOT_SE, 0, 0, notifier,,, delayed_CK, delayed_D);
		$setuphold (negedge CK &&& adacond_OP_D_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_SE_CP_OR_OP_NOT_D_AND_SE_AND_SI_CP, negedge RT &&& adacond_OP_D_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_SE_CP_OR_OP_NOT_D_AND_SE_AND_SI_CP, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (negedge CK &&& adacond_OP_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_SE_CP, negedge RT &&& adacond_OP_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_SE_CP, 0, 0, notifier,,, delayed_CK, delayed_RT);
		$setuphold (posedge CK &&& adacond_D_AND_NOT_RT_AND_NOT_SI, posedge SE &&& adacond_D_AND_NOT_RT_AND_NOT_SI, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_D_AND_NOT_RT_AND_NOT_SI, negedge SE &&& adacond_D_AND_NOT_RT_AND_NOT_SI, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_D_AND_NOT_RT_AND_SI, posedge SE &&& adacond_NOT_D_AND_NOT_RT_AND_SI, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_D_AND_NOT_RT_AND_SI, negedge SE &&& adacond_NOT_D_AND_NOT_RT_AND_SI, 0, 0, notifier,,, delayed_CK, delayed_SE);
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_SE, posedge SI &&& adacond_NOT_RT_AND_SE, 0, 0, notifier,,, delayed_CK, delayed_SI);
		$setuphold (posedge CK &&& adacond_NOT_RT_AND_SE, negedge SI &&& adacond_NOT_RT_AND_SE, 0, 0, notifier,,, delayed_CK, delayed_SI);
		$width (posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (negedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_SI_CP_OR_OP_D_AND_NOT_RT_AND_NOT_SE_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_SI_CP, 0, 0, notifier);
		$width (posedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
		$width (negedge CK &&& adacond_OP_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_SE_AND_NOT_SI_CP_OR_OP_NOT_D_AND_NOT_RT_AND_NOT_SE_CP, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine
`ifdef _udp_def_altos_latch_
`else
`define _udp_def_altos_latch_
primitive altos_latch (q, v, clk, d);
	output q;
	reg q;
	input v, clk, d;

	table
		* ? ? : ? : x;
		? 1 0 : ? : 0;
		? 1 1 : ? : 1;
		? x 0 : 0 : -;
		? x 1 : 1 : -;
		? 0 ? : ? : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_dff_err_
`else
`define _udp_def_altos_dff_err_
primitive altos_dff_err (q, clk, d);
	output q;
	reg q;
	input clk, d;

	table
		(0x) ? : ? : 0;
		(1x) ? : ? : 1;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_dff_
`else
`define _udp_def_altos_dff_
primitive altos_dff (q, v, clk, d, xcr);
	output q;
	reg q;
	input v, clk, d, xcr;

	table
		*  ?   ? ? : ? : x;
		? (x1) 0 0 : ? : 0;
		? (x1) 1 0 : ? : 1;
		? (x1) 0 1 : 0 : 0;
		? (x1) 1 1 : 1 : 1;
		? (x1) ? x : ? : -;
		? (bx) 0 ? : 0 : -;
		? (bx) 1 ? : 1 : -;
		? (x0) b ? : ? : -;
		? (x0) ? x : ? : -;
		? (01) 0 ? : ? : 0;
		? (01) 1 ? : ? : 1;
		? (10) ? ? : ? : -;
		?  b   * ? : ? : -;
		?  ?   ? * : ? : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_dff_r_err_
`else
`define _udp_def_altos_dff_r_err_
primitive altos_dff_r_err (q, clk, d, r);
	output q;
	reg q;
	input clk, d, r;

	table
		 ?   0 (0x) : ? : -;
		 ?   0 (x0) : ? : -;
		(0x) ?  0   : ? : 0;
		(0x) 0  x   : ? : 0;
		(1x) ?  0   : ? : 1;
		(1x) 0  x   : ? : 1;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_dff_r_
`else
`define _udp_def_altos_dff_r_
primitive altos_dff_r (q, v, clk, d, r, xcr);
	output q;
	reg q;
	input v, clk, d, r, xcr;

	table
		*  ?   ?  ?   ? : ? : x;
		?  ?   ?  1   ? : ? : 0;
		?  b   ? (1?) ? : 0 : -;
		?  x   0 (1?) ? : 0 : -;
		?  ?   ? (10) ? : ? : -;
		?  ?   ? (x0) ? : ? : -;
		?  ?   ? (0x) ? : 0 : -;
		? (x1) 0  ?   0 : ? : 0;
		? (x1) 1  0   0 : ? : 1;
		? (x1) 0  ?   1 : 0 : 0;
		? (x1) 1  0   1 : 1 : 1;
		? (x1) ?  ?   x : ? : -;
		? (bx) 0  ?   ? : 0 : -;
		? (bx) 1  0   ? : 1 : -;
		? (x0) 0  ?   ? : ? : -;
		? (x0) 1  0   ? : ? : -;
		? (x0) ?  0   x : ? : -;
		? (01) 0  ?   ? : ? : 0;
		? (01) 1  0   ? : ? : 1;
		? (10) ?  ?   ? : ? : -;
		?  b   *  ?   ? : ? : -;
		?  ?   ?  ?   * : ? : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_dff_s_err_
`else
`define _udp_def_altos_dff_s_err_
primitive altos_dff_s_err (q, clk, d, s);
	output q;
	reg q;
	input clk, d, s;

	table
		 ?   1 (0x) : ? : -;
		 ?   1 (x0) : ? : -;
		(0x) ?  0   : ? : 0;
		(0x) 1  x   : ? : 0;
		(1x) ?  0   : ? : 1;
		(1x) 1  x   : ? : 1;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_dff_s_
`else
`define _udp_def_altos_dff_s_
primitive altos_dff_s (q, v, clk, d, s, xcr);
	output q;
	reg q;
	input v, clk, d, s, xcr;

	table
		*  ?   ?  ?   ? : ? : x;
		?  ?   ?  1   ? : ? : 1;
		?  b   ? (1?) ? : 1 : -;
		?  x   1 (1?) ? : 1 : -;
		?  ?   ? (10) ? : ? : -;
		?  ?   ? (x0) ? : ? : -;
		?  ?   ? (0x) ? : 1 : -;
		? (x1) 0  0   0 : ? : 0;
		? (x1) 1  ?   0 : ? : 1;
		? (x1) 1  ?   1 : 1 : 1;
		? (x1) 0  0   1 : 0 : 0;
		? (x1) ?  ?   x : ? : -;
		? (bx) 1  ?   ? : 1 : -;
		? (bx) 0  0   ? : 0 : -;
		? (x0) 1  ?   ? : ? : -;
		? (x0) 0  0   ? : ? : -;
		? (x0) ?  0   x : ? : -;
		? (01) 1  ?   ? : ? : 1;
		? (01) 0  0   ? : ? : 0;
		? (10) ?  ?   ? : ? : -;
		?  b   *  ?   ? : ? : -;
		?  ?   ?  ?   * : ? : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_dff_sr_err_
`else
`define _udp_def_altos_dff_sr_err_
primitive altos_dff_sr_err (q, clk, d, s, r);
	output q;
	reg q;
	input clk, d, s, r;

	table
		 ?   1 (0x)  ?   : ? : -;
		 ?   0  ?   (0x) : ? : -;
		 ?   0  ?   (x0) : ? : -;
		(0x) ?  0    0   : ? : 0;
		(0x) 1  x    0   : ? : 0;
		(0x) 0  0    x   : ? : 0;
		(1x) ?  0    0   : ? : 1;
		(1x) 1  x    0   : ? : 1;
		(1x) 0  0    x   : ? : 1;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_dff_sr_0
`else
`define _udp_def_altos_dff_sr_0
primitive altos_dff_sr_0 (q, v, clk, d, s, r, xcr);
	output q;
	reg q;
	input v, clk, d, s, r, xcr;

	table
	//	v,  clk, d, s, r : q' : q;

		*  ?   ?   ?   ?   ? : ? : x;
		?  ?   ?   ?   1   ? : ? : 0;
		?  ?   ?   1   0   ? : ? : 1;
		?  b   ? (1?)  0   ? : 1 : -;
		?  x   1 (1?)  0   ? : 1 : -;
		?  ?   ? (10)  0   ? : ? : -;
		?  ?   ? (x0)  0   ? : ? : -;
		?  ?   ? (0x)  0   ? : 1 : -;
		?  b   ?  0   (1?) ? : 0 : -;
		?  x   0  0   (1?) ? : 0 : -;
		?  ?   ?  0   (10) ? : ? : -;
		?  ?   ?  0   (x0) ? : ? : -;
		?  ?   ?  0   (0x) ? : 0 : -;
		? (x1) 0  0    ?   0 : ? : 0;
		? (x1) 1  ?    0   0 : ? : 1;
		? (x1) 0  0    ?   1 : 0 : 0;
		? (x1) 1  ?    0   1 : 1 : 1;
		? (x1) ?  ?    0   x : ? : -;
		? (x1) ?  0    ?   x : ? : -;
		? (1x) 0  0    ?   ? : 0 : -;
		? (1x) 1  ?    0   ? : 1 : -;
		? (x0) 0  0    ?   ? : ? : -;
		? (x0) 1  ?    0   ? : ? : -;
		? (x0) ?  0    0   x : ? : -;
		? (0x) 0  0    ?   ? : 0 : -;
		? (0x) 1  ?    0   ? : 1 : -;
		? (01) 0  0    ?   ? : ? : 0;
		? (01) 1  ?    0   ? : ? : 1;
		? (10) ?  0    ?   ? : ? : -;
		? (10) ?  ?    0   ? : ? : -;
		?  b   *  0    ?   ? : ? : -;
		?  b   *  ?    0   ? : ? : -;
		?  ?   ?  ?    ?   * : ? : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_dff_sr_1
`else
`define _udp_def_altos_dff_sr_1
primitive altos_dff_sr_1 (q, v, clk, d, s, r, xcr);
	output q;
	reg q;
	input v, clk, d, s, r, xcr;

	table
	//	v,  clk, d, s, r : q' : q;

		*  ?   ?   ?   ?   ? : ? : x;
		?  ?   ?   0   1   ? : ? : 0;
		?  ?   ?   1   ?   ? : ? : 1;
		?  b   ? (1?)  0   ? : 1 : -;
		?  x   1 (1?)  0   ? : 1 : -;
		?  ?   ? (10)  0   ? : ? : -;
		?  ?   ? (x0)  0   ? : ? : -;
		?  ?   ? (0x)  0   ? : 1 : -;
		?  b   ?  0   (1?) ? : 0 : -;
		?  x   0  0   (1?) ? : 0 : -;
		?  ?   ?  0   (10) ? : ? : -;
		?  ?   ?  0   (x0) ? : ? : -;
		?  ?   ?  0   (0x) ? : 0 : -;
		? (x1) 0  0    ?   0 : ? : 0;
		? (x1) 1  ?    0   0 : ? : 1;
		? (x1) 0  0    ?   1 : 0 : 0;
		? (x1) 1  ?    0   1 : 1 : 1;
		? (x1) ?  ?    0   x : ? : -;
		? (x1) ?  0    ?   x : ? : -;
		? (1x) 0  0    ?   ? : 0 : -;
		? (1x) 1  ?    0   ? : 1 : -;
		? (x0) 0  0    ?   ? : ? : -;
		? (x0) 1  ?    0   ? : ? : -;
		? (x0) ?  0    0   x : ? : -;
		? (0x) 0  0    ?   ? : 0 : -;
		? (0x) 1  ?    0   ? : 1 : -;
		? (01) 0  0    ?   ? : ? : 0;
		? (01) 1  ?    0   ? : ? : 1;
		? (10) ?  0    ?   ? : ? : -;
		? (10) ?  ?    0   ? : ? : -;
		?  b   *  0    ?   ? : ? : -;
		?  b   *  ?    0   ? : ? : -;
		?  ?   ?  ?    ?   * : ? : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_latch_r_
`else
`define _udp_def_altos_latch_r_
primitive altos_latch_r (q, v, clk, d, r);
	output q;
	reg q;
	input v, clk, d, r;

	table
		* ? ? ? : ? : x;
		? ? ? 1 : ? : 0;
		? 0 ? 0 : ? : -;
		? 0 ? x : 0 : -;
		? 1 0 0 : ? : 0;
		? 1 0 x : ? : 0;
		? 1 1 0 : ? : 1;
		? x 0 0 : 0 : -;
		? x 0 x : 0 : -;
		? x 1 0 : 1 : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_latch_s_
`else
`define _udp_def_altos_latch_s_
primitive altos_latch_s (q, v, clk, d, s);
	output q;
	reg q;
	input v, clk, d, s;

	table
		* ? ? ? : ? : x;
		? ? ? 1 : ? : 1;
		? 0 ? 0 : ? : -;
		? 0 ? x : 1 : -;
		? 1 1 0 : ? : 1;
		? 1 1 x : ? : 1;
		? 1 0 0 : ? : 0;
		? x 1 0 : 1 : -;
		? x 1 x : 1 : -;
		? x 0 0 : 0 : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_latch_sr_0
`else
`define _udp_def_altos_latch_sr_0
primitive altos_latch_sr_0 (q, v, clk, d, s, r);
	output q;
	reg q;
	input v, clk, d, s, r;

	table
		* ? ? ? ? : ? : x;
		? 1 1 ? 0 : ? : 1;
		? 1 0 0 ? : ? : 0;
		? ? ? 1 0 : ? : 1;
		? ? ? ? 1 : ? : 0;
		? 0 * ? ? : ? : -;
		? 0 ? * 0 : 1 : 1;
		? 0 ? 0 * : 0 : 0;
		? * 1 ? 0 : 1 : 1;
		? * 0 0 ? : 0 : 0;
		? ? 1 * 0 : 1 : 1;
		? ? 0 0 * : 0 : 0;
	endtable
endprimitive
`endif

`ifdef _udp_def_altos_latch_sr_1
`else
`define _udp_def_altos_latch_sr_1
primitive altos_latch_sr_1 (q, v, clk, d, s, r);
	output q;
	reg q;
	input v, clk, d, s, r;

	table
		* ? ? ? ? : ? : x;
		? 1 1 ? 0 : ? : 1;
		? 1 0 0 ? : ? : 0;
		? ? ? 1 ? : ? : 1;
		? ? ? 0 1 : ? : 0;
		? 0 * ? ? : ? : -;
		? 0 ? * 0 : 1 : 1;
		? 0 ? 0 * : 0 : 0;
		? * 1 ? 0 : 1 : 1;
		? * 0 0 ? : 0 : 0;
		? ? 1 * 0 : 1 : 1;
		? ? 0 0 * : 0 : 0;
	endtable
endprimitive
`endif
