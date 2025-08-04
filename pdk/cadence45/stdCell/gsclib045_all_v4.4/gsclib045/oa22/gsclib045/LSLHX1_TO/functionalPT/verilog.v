//Verilog HDL for "gsclib045", "LSLHX1_TO" "functionalPT"

// type:  
`timescale 1ns/10ps
`celldefine
module LSLHX1_TO (Y, A, VSS, VDD, ExtVDD);
	output Y;
	input A;
	input VSS;
	input VDD;
	input ExtVDD;

	// Function
	buf (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine
