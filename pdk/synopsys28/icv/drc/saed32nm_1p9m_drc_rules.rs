/*
#########################################################################################
# SAED 32/28NM 1p9m icv  drc deck							#
#											#
# Revision History:									#
# Rev.		date			what						#
# -------------------------------------------------------------------------------------	#	
# 1.0		16/Nov/2011		Initial release					#
#########################################################################################
*/

#include "icv.rh"

error_options(
    error_limit_per_check = 10000000
);

layout_grid_options (
		    resolution = 0.001,
		    check_45 = {PATH,POLYGON}
    		    );
TOP_MET = 9;

openaccess_options(
    view="layout",
     layer_mapping_file= "./techfiles/saed32nm_1p9m_gdsout.map"
);


/*************************  ASSIGNMENTS  ********************************/

	NWELLi    = assign({{1}});
	DNWi	  = assign({{2}});
	DIFFi	  = assign({{3}});	
	DDMYi     = assign({{3,1}});
	PIMPi	  = assign({{4}});
	NIMPi	  = assign({{5}});
	DIFF_18i  = assign({{6}});
	PADi	  = assign({{7}});
	ESD_25	  = assign({{8}});
	SBLKi	  = assign({{9}});
	POi       = assign({{10}});
	PODMYi    = assign({{10,1}});
	M1i       = assign({{11}});
	M1DMYi    = assign({{11,1}});
	M1i_text  = assign_text({{11}});
	VIA1i     = assign({{12}});
	M2i       = assign({{13}});
	M2i_text  = assign_text({{12}});
        VIA2i     = assign({{14}});
	M2DMYi    = assign({{13,1}});
	M3i       = assign({{15}});
	M3i_text  = assign_text({{13}});
	M3DMYi    = assign({{15,1}});
        VIA3i     = assign({{16}});
	M4i       = assign({{17}});
	M4i_text  = assign_text({{14}}); 
	M4DMYi    = assign({{17,1}});      
        VIA4i     = assign({{18}});
	M5i       = assign({{19}}); 
	M5i_text  = assign_text({{15}});   
        VIA5i     = assign({{20}});
	M6i       = assign({{21}});  
	M6i_text  = assign_text({{16}});
	M6DMYi    = assign({{21,1}});
	VIA6i     = assign({{22}});
	M7i       = assign({{23}});
	M7i_text  = assign_text({{17}});   
	M7DMYi    = assign({{23,1}}); 
	VIA7i     = assign({{24}});
	M8i       = assign({{25}});
	M8i_text  = assign_text({{18}});
	M8DMYi    = assign({{25,1}});
	VIA8i     = assign({{26}});    
	M9i       = assign({{27}});  
	M9i_text  = assign({{19}});
	M9DMYi    = assign({{27,1}});  
	COi       = assign({{28}});
	HVTIMPi   = assign({{29}});
	LVTIMPi   = assign({{30}});
	M1PIN     = assign({{31}});
        M1PIN_text = assign_text({{31}});
	M2PIN     = assign({{32}});
	M2PIN_text = assign_text({{32}});
	M3PIN     = assign({{33}});
	M3PIN_text = assign_text({{33}});
	M4PIN     = assign({{34}});
	M4PIN_text = assign_text({{34}});
	M5PIN     = assign({{35}});
	M5PIN_text = assign_text({{35}});
	M6PIN     = assign({{36}});
	M6PIN_text = assign_text({{36}});
	M7PIN     = assign({{37}});
	M7PIN_text = assign_text({{37}});
	M8PIN     = assign({{38}});
	M8PIN_text = assign_text({{38}});
	M9PIN     = assign({{39}});
	M9PIN_text = assign_text({{39}});
	MRDLi      = assign({{41}});
	VIARDLi	   = assign({{42}});
	HOTNWLi    = assign({{44}});
	DIODi      = assign({{46}});
	BJTMYi     = assign({{47}});
	RNWi      = assign({{48}});
	RMARK     = assign({{49}});
	LOGO      = assign({{51}});
	IP        = assign({{52}});
	RM1i      = assign({{53}});
	RM2i      = assign({{54}});
	RM3i      = assign({{55}});
	RM4i      = assign({{56}});
	RM5i      = assign({{57}});
	RM6i      = assign({{58}});
	RM7i      = assign({{59}});	
	RM8i      = assign({{60}});
	RM9i      = assign({{61}});
	DIFF_25i  = assign({{75}});


/**************************  Data Creation  **************************** */

	nwell   = NWELLi;
	dnw     = DNWi;
	diff    = DIFFi; 
	pimp    = PIMPi;   
	nimp    = NIMPi;    
	diff_25 = DIFF_25i;
	diff_18 = DIFF_18i;   
	pad     = PADi;    	 
	esd_25  = ESD_25;
	sblk    = SBLKi;   
	po      = POi;    
	TOP_MET = 9;
	RECOMMENDED = 0;
	m1 = M1i;   
	m2 = M2i;   
	m3 = M3i;   
	m4 = M4i;   
	m5 = M5i;  
	m6 = M6i;   
	m7 = M7i;  
	m8 = M8i;   
	m9 = M9i;  

	co = COi;   
	via1 = VIA1i;   
	via2 = VIA2i;   
	via3 = VIA3i;   
	via4 = VIA4i;   
	via5 = VIA5i;   
	via6 = VIA6i;   
	via7 = VIA7i;  
	via8 = VIA8i;   
	viat = empty_layer();
	hotnwl = HOTNWLi;   
	rm1 = RM1i;   
	rm2 = RM2i;   
	rm3 = RM3i;   
	rm4 = RM4i;   
	rm5 = RM5i;   
	rm6 = RM6i;   
	rm7 = RM7i;   
	rm8 = RM8i;   
	rm9 = RM9i;   

	diod  =  DIODi;  
	bjtdmy = BJTMYi;   
	rnw    = RNWi;   
	viardl = VIARDLi;
	mrdl = MRDLi;
	mt = empty_layer(); 
    	mt2 = empty_layer();
	hvtimp = HVTIMPi;
	lvtimp = LVTIMPi;

//	pwell_cont = copy (ptap);
//	nwell_cont = (ntap);
	if ( TOP_MET == 9 ) {
    		mt = m9;  
		mt2 = m8;  
	        viat = via8; 
	}

	if( TOP_MET == 8 ) {
    		mt = m8;  
    		mt2 = m7;  
    		viat = via7;
	}

	if( TOP_MET == 7 ) {
    		mt = m7;  
    		mt2 = m6;  
    		viat = via6; 
	}

	if( TOP_MET == 6 ) {
    		mt = m6; 
    		mt2 = m5;  
    		viat = via5; 
	}

/***************************  Define derived layers  ***********************/

	chip = cell_extent ( cell_list = {"*"} );
	bulk = size ( chip, 1);

	pwell = not ( bulk , nwell );

	rnwel = nwell interacting rnw;//
	dnwnwell = nwell interacting dnw;//
	nwres = nwell interacting rnw;//

	nwnr = outside ( nwell , rnwel );//
	nwoutdnw = outside ( nwell , dnw );//
	pwindnw = inside ( pwell , dnw );//

	imp = or ( nimp , pimp ); 
	ndiff = and ( nimp , diff );
	pdiff = and ( pimp , diff );

	nact = and ( ndiff , pwell );
	pact = and ( pdiff , nwell );
	act = or ( pact , nact );

	odwr = diff interacting nwres;//
	od25 = inside ( diff, diff_18 );//
	od18 = inside ( diff, diff_25 );//

	fpoly = not ( po , diff );//

	gate = and ( po , act );
	gate_edge = and_edge (po, act);
	ngate = and ( po , nact );
	pgate = and ( po , pact );
	gate_25 = and ( gate , diff_25 );//
	gate_18 = and ( gate , diff_18 );//
	diff_25_18 = or(diff_25,diff_18);
	gate_s = not(gate,interacting (gate,diff_25_18));
	ptap = and ( pdiff, pwell );
	ntap = and ( ndiff , nwell );
	tap  = or  ( ptap , ntap);
	cood = and ( co , diff );//
	copo = and ( co , po );//
	
	sd = not ( act , gate );//
	sd_tap = not ( diff, gate );//


/********* Begin Rules *******/

/*************************  NWELL RULES ***************************/

/*swg*/
//{ @ "VIA45 must be enclose by M4";
//L=not(m4,via4);
//W=and(m4,via4);
// outside(W,L);
//}


	{
		@ "NWELL.W.1 Minimum width must be 0.23";
		internal1 ( nwell, distance < 0.23 , extension=RADIAL , relational = POINT_TOUCH);
	}


	{
		@ "NWELL.A.1 Minimum area must be 0.45";
		area(nwell, value < 0.45);/*SWG*/
	}
nwell_holes = donut_holes (nwell, INNER);
	{
		@ "NWELL.A.2 Mimimum Enclosed area must be 0.45";
		area(nwell_holes, value < 0.45);
	}
	n1= and(nwell,and(nimp,diff));
	cdb1 = connect ( 		
		    {
		    {{n1},nwell},
		    {{n1,m1},co},
		    {{m1,m2},via1},
		    {{m2,m3},via2},
		    {{m3,m4},via3},
		    {{m4,m5},via4},
		    {{m5,m6},via6},
		    {{m6,m7},via7},
		    {{m7,m8},via8},
		    {{m8,mt},viat}
		    }
	);
	{
		@"NWELL.S.1: Minimum spacing between wells at same potential must be 0.23";
		external1(nwell, distance < 0.23, extension = RADIAL, connectivity = SAME_NET, connect_sequence = cdb1);
	}	    
	{
		@"NWELL.S.2: Minimum spacing between wells at different potential must be 0.46";
		external1(nwell, distance < 0.46, extension = RADIAL, connectivity = DIFFERENT_NET, connect_sequence = cdb1);
	}	    
		    
//************************  DNW RULES *****************************

	{
		@ "DNW.W.1 Minimum width must be 3";
		internal1 ( dnw, distance < 3 ,extension=RADIAL, relational = {POINT_TOUCH} );
	}

	{	
		@ "DNW.S.1 Minumum spacing, Deep_N_Well to Deep_N_Well must be 3.5 ";
		external1 ( dnw, distance < 3.5 ,extension=RADIAL, relational = {POINT_TOUCH});
	}

	{
		@ "DNW.S.2 Minimum spacing, Deep_N_Well to unrelated N_Well must be 2.5";
		external2 ( dnw , nwoutdnw, distance < 2.5 ,extension=RADIAL,  look_thru = COINCIDENT , relational = {POINT_TOUCH,OVERLAP} );
	}
	
		pwoutdnw = not ( pwell , pwindnw );
		nact_1 =  and (pwoutdnw , ndiff );

	{
		@ "DNW.S.3 Minimum spacing, external N+Active to Deep_N_Well must be 1.5";
		external2 ( dnw , nact_1 , distance < 1.5,extension=RADIAL, look_thru = COINCIDENT , relational = {POINT_TOUCH,OVERLAP} );
	}


		pact_1 = and ( dnwnwell , pdiff );

	{	
		@ "DNW.S.4 Minimum spacing, P+Active in N_Well to its Deep_N_Well must be 1";
		external2 ( dnw , pact_1 , distance < 1 ,extension=RADIAL,   look_thru = COINCIDENT , relational = {OVERLAP,POINT_TOUCH });
	}


		dnw_nwell=dnw inside nwell;
		pwell_dnw=pwell inside dnw_nwell;
	
	{
		@ "DNW.E.1 Minimum enclosure, N+Active by isolated P-Well must be 0.7";
		enclose ( nact , pwell_dnw , distance < 0.7 ,extension=RADIAL, intersecting = TOUCH , relational = {POINT_TOUCH,INSIDE});
	}


	{
		@ "DNW.E.2 Minimum enclosure, N_Well beyond Deep_N_Well edge must be 1";
		enclose ( dnw, nwell , distance < 1 ,extension=RADIAL, intersecting = TOUCH , relational = {POINT_TOUCH,INSIDE});
	}
	
		nwanddnw=and(dnw,nwell);
	
	{
		@ "DNW.O.1 Minimum overlap, N_Well over Deep_N_Well edge must be 0.4";
		internal1(nwanddnw, distance < 0.4,extension=RADIAL,relational={POINT_TOUCH});	
	}

//************************** DIFF RULES **********************

	{	
		@ "DIFF.B.1 DIFF must be fully covered by NIMP/PIMP";
		not ( not ( diff, odwr ) , imp );
	}	

	
	{
		@ "DIFF.W.1 Minimum width must be 0.044";
		internal1 ( diff , distance < 0.044 , extension=RADIAL,relational = POINT_TOUCH );
	}
	
    diff_s_009_h = not( diff, internal1 (diff, distance <= 0.09, extension = NONE, direction = HORIZONTAL));
    diff_s_009_v = not( diff, internal1 (diff, distance <= 0.09, extension = NONE, direction = VERTICAL)); 

	
	{
		@ "DIFF.W.2: Minimum space when span on at least one side is > 0.09 (for run length > 0.1) must be 0.055";
		external2 ( diff_s_009_h, diff, distance < 0.055, extension = NONE, direction = HORIZONTAL, look_thru = ALL,projection_length > 0.1, orientation = PARALLEL, intersecting = TOUCH, projection = IN, orthogonal = ALL);
	    
	}
	{
		@ "DIFF.W.2 Minimum space when span on at least one side is > 0.09 (for run length > 0.1) must be 0.055";
		external2 (diff, diff_s_009_v, distance < 0.055, extension = NONE, direction = VERTICAL,look_thru = ALL, projection_length > 0.1,orientation = PARALLEL, intersecting = TOUCH, projection = IN, orthogonal = ALL);
	}

    diff_s_015_h = not( diff, internal1 (diff, distance < 0.15, extension = NONE, direction = HORIZONTAL));
    diff_s_015_v = not( diff, internal1 (diff, distance < 0.15, extension = NONE, direction = VERTICAL)); 
	{
		@ "DIFF.W.3 Minimum space when span on at least one side is > 0.15 (for run length > 0.1) must be 0.065";
		external2 (diff, diff_s_015_h, distance < 0.065,look_thru = ALL, extension = NONE, direction = HORIZONTAL,projection_length > 0.1, orientation = PARALLEL, intersecting = TOUCH, projection = IN, orthogonal = ALL);
	}
	{
		@ "DIFF.W.3 Minimum space when span on at least one side is > 0.15 (for run length > 0.1) must be 0.065";
		external2 (diff, diff_s_015_v, distance < 0.065, extension = NONE,look_thru = ALL,  direction = VERTICAL,projection_length > 0.1, orientation = PARALLEL, intersecting = TOUCH, projection = IN, orthogonal = ALL);
	}
	

	
diff_s_008_h = internal1(diff, distance < 0.08, extension = NONE, direction=HORIZONTAL);
diff_s_008_v = internal1(diff, distance < 0.08, extension = NONE, direction=VERTICAL);
diff_s_0150_h = not(diff, internal1(diff, distance <= 0.150, extension = NONE, direction = HORIZONTAL));
diff_s_0150_v = not(diff, internal1(diff, distance <= 0.150, extension = NONE, direction = VERTICAL));
diff_s_008_0150_h = not (diff, (diff_s_008_h or diff_s_0150_h));
diff_s_008_0150_v = not (diff, (diff_s_008_v or diff_s_0150_v));
 	if( RECOMMENDED == 1 ) {
	{
		@ "R.DIFF.S.5: Min spacing of edge with span <= 0.08 must be 0.07";
		external1 (diff_s_008_h, distance < 0.07, extension = NONE, direction = HORIZONTAL);
	} 
 	{
		@ "R.DIFF.S.5: Min spacing of edge with span <= 0.08 must be 0.07";
		external1 (diff_s_008_v, distance < 0.07, extension = NONE, direction = VERTICAL);
	} 
	{
		@ "R.DIFF.S.6: Min spacing of edge with 0.08 < span < = 0.15 must be 0.08";
		external1(diff_s_008_0150_h, distance < 0.08, extension = NONE, direction = HORIZONTAL);
	} 	
	{
		@ "R.DIFF.S.6: Min spacing of edge with 0.08 < span <= 0.15 must be 0.08";
		external1(diff_s_008_0150_v, distance < 0.08, extension = NONE, direction = VERTICAL);
	} 
	{
		@ "R.DIFF.S.7: Min spacing of edge with span > 0.150 must be 0.085";
		external1(diff_s_0150_h, distance < 0.085, extension = NONE, direction = HORIZONTAL);
	} 	
	{
		@ "R.DIFF.S.7: Min spacing of edge with span > 0.150 must be 0.085";
		external1(diff_s_0150_v, distance < 0.085, extension = NONE, direction = VERTICAL);
	} }
	{
		@ "DIFF.S.1 Minimum spacing must be 0.05";
		external1 ( diff, distance < 0.05, extension = RADIAL, relational = POINT_TOUCH );
	}
    diff_g_01= wide(diff, distance >=0.1);
	{
		@ "DIFF.S.2 Mimimum spacing must be 0.07 when width >= 0.1";
		external1 (diff_g_01, distance < 0.07, extension = RADIAL, relational = POINT_TOUCH);
		
	}
	
	{
		@ "DIFF.S.3 Minimum spacing to DIFF_18 is 0.15";
		external2 ( diff,od18 , distance < 0.15 ,extension=RADIAL, relational = POINT_TOUCH); 
	}

	{
		@ "DIFF.S.4 Minimum spacing to DIFF_25 is 0.15";
		external2 (diff,  od25 , distance < 0.15 ,extension=RADIAL, relational = POINT_TOUCH); 
	}
	

	{
		@ "DIFF.E.1 Source/Drain N+active to Pwell edge ( min enclosure by well ) must be 0.065";
		enclose ( nact , pwell , distance < 0.065 ,extension=RADIAL, relational = INSIDE , intersecting = TOUCH );
	}
		
	{
		@ "DIFF.E.1 Source/Drain P+active to Nwell edge ( min enclosure by well ) must be 0.065";
		enclose ( pact , nwell , distance < 0.065 ,extension=RADIAL, relational = INSIDE , intersecting = TOUCH );
	}

	{
		@ "DIFF.E.2 PTAP minimum enclosure by PWELL must be 0.07";
		enclose ( ptap , pwell , distance < 0.07 , extension=RADIAL,relational = INSIDE , intersecting = TOUCH );
	}

	{
		@ "DIFF.E.2 NTAP minimum enclosure by NWELL must be 0.07";
		enclose ( ntap , nwell , distance < 0.07 ,extension=RADIAL, relational = INSIDE , intersecting = TOUCH );
	}

	{	@ "DIFF.A.1  DIFF minimum area must be 0.02";
		area ( diff, value <  0.02 );
	}
    diff_hole = donut_holes( diff, INNER);
	{
		@ "DIFF.A.2 DIFF minimum enclosed area must be 0.03";
		area(diff_hole, value < 0.03);
	}
	
	{
		@ "DIFF.W.4 Channel width range must be [0.1,3.5]";
		not_length_edge(gate_edge , distance  =  [0.1, 3.5] );
	}
		
		
//*******************************************    PIMP RULES   


	{
		@ "PIMP.W.1 Minimum width must be 0.102";
	        internal1 ( pimp, distance < 0.102 ,extension=RADIAL, relational = POINT_TOUCH );
	}
	
	{
		@ "PIMP.E.1 Enclosure of P+Active must be 0.05";
		enclose ( pact , pimp , distance < 0.05 ,extension=RADIAL, relational = INSIDE , intersecting = TOUCH );
	}
	
	{
		@ "PIMP.E.2 Enclosure of PTAP must be 0.02";
		enclose ( ptap , pimp , distance < 0.02 , extension=RADIAL,relational = INSIDE , intersecting = TOUCH );
	}
	{
		@ "PIMP.E.3: Poly enclosure by pimp must be 0.065";
		enclose (po, imp, distance < 0.065, extension = RADIAL, relational = INSIDE, intersecting = TOUCH);
	}
	
	{
		@ "PIMP.S.1 Minimum space must be 0.102";	/////Arman 0.17 -> 0.102
		external1 ( pimp , distance < 0.102 ,extension=RADIAL, relational = POINT_TOUCH , look_thru = ALL ); 
	}

	{  	
		@ "PIMP.S.2 Overlap of NIMP and PIMP is not allowed";
		and ( pimp , nimp );
	}
	{
		@ "R.PIMP.S.2: Minimum space to butted N+Active must be 0";
		and(and(diff,nimp),pimp);
	}

	{	
		@ "PIMP.S.3 Minimum spacing to N+Active in P_Well must be 0.05";
		external2 ( pimp , nact , distance < 0.05 ,extension=RADIAL, relational = OVERLAP,  look_thru = COINCIDENT );
	}

	{
		@ "PIMP.O.1 Minimum active overlap must be 0.05";
		internal2 ( pimp , diff, distance < 0.05,extension=RADIAL );
	}


//************************************************** NIMP RULES 

	{
		@ "NIMP.W.1 Minimum width must be 0.102";
		internal1 ( nimp, distance < 0.102 ,extension=RADIAL, relational = POINT_TOUCH );
	}
	
	{
		@ "NIMP.E.1 Enclosure of N+Active must be 0.05";
		enclose ( nact , nimp , distance < 0.05 ,extension=RADIAL, relational = INSIDE , intersecting = TOUCH );
	}
	
	{
		@ "NIMP.E.2 Enclosure of NTAP must be 0.02";
		enclose ( ntap , nimp , distance < 0.02 ,extension=RADIAL, relational = INSIDE , intersecting = TOUCH );
	}
	{
		@ "NIMP.E.3: Poly enclosure of NIMP must be 0.065";
		enclose( po,imp, distance < 0.065, extension=RADIAL, relational = INSIDE,intersecting=TOUCH);
	}
	{
		@ "NIMP.S.1 Minimum space is 0.102"; ////Arman 0.17 -> 0.102
		external1 ( nimp , distance < 0.102 ,extension=RADIAL, relational = POINT_TOUCH , look_thru = ALL ); 
	}

	{	
		@ "NIMP.S.3 Minimum spacing to P+Active in N_Well must be 0.05";
		external2 ( nimp , pact , distance < 0.05 ,extension=RADIAL, relational = OVERLAP,  look_thru = COINCIDENT );
	}

	{
		@ "NIMP.O.1 Minimum active overlap must be 0.05";
		internal2 ( nimp , diff, distance < 0.05,extension=RADIAL );
	}
    
	{
		@ "NIMP.S.2: Minimum space to butted P+Active must be 0";
	        and(and(diff, pimp),nimp);
	}

//*********************************************    DIFF_18 RULES  


	
	{
		@ "DIFF_18.W.1 Minimum width must be 0.33";
		internal1 ( diff_18 , distance < 0.33, extension=RADIAL, relational = POINT_TOUCH );
	}

	{
		@ "DIFF_18.S.1 Minimum spacing must be 0.33";
		external1 ( diff_18 , distance < 0.33 ,extension=RADIAL, relational = POINT_TOUCH , look_thru = ALL ); 
	}

	{
		@ "DIFF_18.E.1 Minimum  DIFF enclosure 0.15";
		enclose ( diff , diff_18 , distance < 0.15 ,extension=RADIAL, relational = INSIDE , intersecting = TOUCH );
	}
	
	int_diff = diff interacting diff_18;
	ext_diff = not ( diff , int_diff );
	{	
		@ "DIFF_18.S.2 Minimum space external Active must be 0.15";
		external2 ( diff_18  , ext_diff , distance < 0.15 ,extension=RADIAL, relational = OVERLAP,  look_thru = COINCIDENT );
	}
	{
		@ "DIFF_18.A.1 Min area diff_18 must be 0.40";
		area(diff_18, value < 0.40);
	}
    
	{
		@ "DIFF_18.A.2 Min enclosed area must be 0.40";
		donut_holes(diff_18, INNER, area < 0.40);
	}


 

	

//*********************************************    DIFF_25 RULES  


	
	{
		@ "DIFF_25.W.1 Minimum width must be 0.33";
		internal1 ( diff_25 , distance < 0.33, extension=RADIAL, relational = POINT_TOUCH );
	}

	{
		@ "DIFF_25.S.1 Minimum spacing must be 0.33";
		external1 ( diff_25 , distance < 0.33 ,extension=RADIAL, relational = POINT_TOUCH , look_thru = ALL ); 
	}

	{
		@ "DIFF_25.E.1 Minimum  DIFF enclosure 0.15";
		enclose ( diff , diff_25 , distance < 0.15 ,extension=RADIAL, relational = INSIDE , intersecting = TOUCH );
	}
	
	int_diff = diff interacting diff_25;
	ext_diff = not ( diff , int_diff );
	{	
		@ "DIFF_25.S.2 Minimum space external Active must be 0.15";
		external2 ( diff_25  , ext_diff , distance < 0.15 ,extension=RADIAL, relational = OVERLAP,  look_thru = COINCIDENT );
	}
	{
		@ "DIFF_25.A.1 Min area diff_25 must be 0.40";
		area(diff_25, value < 0.40);
	}
    
	{
		@ "DIFF_25.A.2 Min enclosed area must be 0.40";
		donut_holes(diff_25, INNER, area < 0.40);
	}



//*****************************************************    PAD RULES   

 pad_rect = rectangles (pad);
	{
		@ "PAD.W.1 PAD minimum bonding passivation opening width and length must be respectively 30 and 70";
		not_rectangles(pad_rect, {30,70});
	}
 pad_flip_chip = vertices (pad, count == 8);
 
	{
		@ "PAD.E.1 Minimum enclosure by MRDL 2um";
		enclose ( pad , mrdl , distance < 1 ,extension=RADIAL, relational = INSIDE , intersecting = TOUCH );
	}
	
	{
		@ "PAD.S.1 Minimum spacing 10um";
		external1 ( pad , distance < 10 ,extension=RADIAL, relational = POINT_TOUCH , look_thru = ALL );
	}
	
	padmet = mrdl interacting pad;
	mtout = not (  mrdl , padmet );
	
	{
		@ "PAD.S.2 PAD metal minimum space to unrelated MRDL must be 2um";
		external2 ( padmet , mtout , distance < 2 ,extension=RADIAL, relational = OVERLAP,  look_thru = COINCIDENT );
	}

	{
		@ "Minimal flip-chip passivation opening width must be 50";
		internal1(pad_flip_chip, distance < 50, extension = NONE);
	}

//*************************************   SBLK RULES ********************************

	{
		@ "SBLK.W.1 SBLK minimum width must be 0.33";
		internal1 ( sblk , distance < 0.33 ,extension=RADIAL, relational = POINT_TOUCH );
	}
	
	    poandsblk = and(po,sblk);
	{
		@ "SBLK.W.2: Minimum poly within unsalicided resistor must be 0.4";		
		internal1 ( poandsblk , distance < 0.4 ,extension=RADIAL, relational = POINT_TOUCH );
	}
	
	{
		@ "SBLK.S.1: SBLK minimum spacing must be 0.33";
		external1 ( sblk , distance < 0.33 ,extension=RADIAL, relational = POINT_TOUCH , look_thru = ALL );
	}
		
	{
		@ "SBLK.S.2_1: No contacts are allowed inside SBLK";
		and ( sblk , co );
	}

	{
		@ "SBLK.S.2 Minimum space, SBLK to contact must be 0.13um";
		external2 ( sblk , co , distance < 0.13 ,extension=RADIAL, relational = {OVERLAP,POINT_TOUCH},  look_thru = COINCIDENT, intersecting=TOUCH );
	}


	{
		@ "SBLK.S.3 Minimum space, SBLK to external diff must be 0.18";
		external2 ( sblk , diff , distance < 0.18 ,extension=RADIAL,look_thru = COINCIDENT , relational ={INSIDE, POINT_TOUCH }, intersecting=TOUCH );
	}
    
	 po_out_sblk=not_interacting(po, sblk,include_touch=NONE);
	{
		@ "SBLK.S.4 Minimum space, SBLK to external poly must be 0.3um";
		external2 ( sblk , po_out_sblk , distance < 0.3 ,extension=RADIAL, relational = {POINT_TOUCH,OVERLAP} ,look_thru = COINCIDENT,intersecting = TOUCH );
	}	
	
	
	poandsblk = and ( po , sblk );
	diffandsblk = and ( diff, sblk );
	diffsblk = diff interacting sblk;
	po_1 = po interacting diffsblk;

	
	{
		@ "SBLK.S.5: Minimum spacing of poly resistors in a single SBLK region must be 0.3um";
		external1 ( poandsblk , distance < 0.3 ,extension=RADIAL, relational = POINT_TOUCH , look_thru = ALL );
	}

	{
		@ "SBLK.S.6 Minimum space, SBLK to poly (in a single active region) must be 0.4um";
		external2 ( sblk , po_1 , distance < 0.4 ,extension=RADIAL,look_thru = COINCIDENT , relational = {POINT_TOUCH,OVERLAP}, intersecting=TOUCH );
	}
    po_sb = and_edge (po, sblk);	
	{
		@ "SBLK.C.1: Resistor is poly inside SBLK: poly ends stick out for contacts the entire resistor must be outside well and over field";
		vertex(po_sb,angles=(0,360));
	}



	{
		@ "SBLK.O.1: Minimum SBLK extension of poly or active must be 0.18";
		//Arman  old enclose ( poandsblk , sblk , distance < 0.18 ,extension=RADIAL,intersecting=TOUCH, relational ={INSIDE, POINT_TOUCH} );
		enclose ( poandsblk , sblk , distance < 0.18 ,extension=RADIAL); 		
	}

	{
		@ "SBLK.O.1: Minimum SBLK extension of poly or active must be 0.18";
		enclose ( diffandsblk , sblk , distance < 0.18 ,extension=RADIAL, relational ={INSIDE, POINT_TOUCH }, intersecting=TOUCH );
	}
	poandsblk_w_018 = wide (poandsblk, distance >0.18 );

	{
		@ "SBLK.O.2: Minimum poly extension of SBLK must be 0.18";
		//Arman old_  enclose ( not(poandsblk, poandsblk_w_018) , po , distance < 0.18 ,extension=RADIAL, relational ={INSIDE, POINT_TOUCH }, intersecting=TOUCH );
		enclose ( not(poandsblk, poandsblk_w_018) , po , distance < 0.18 ,extension=RADIAL); 
	}	
		
 //***********************  PO RULES ********************

	{
		@ "PO.W.1: Minimum width must be 0.03";
		internal1 ( po , distance < 0.03 ,extension=RADIAL, relational = POINT_TOUCH );
	}
	po_rect = rectangles(po);
	{
		@ "PO.W.2: Minimum width of horizontal drawn rectangular or L-shape PO must be 0.04";
		internal1(po_rect, distance < 0.04, extension = NONE, direction = VERTICAL);
	}
	po_l_s = vertices (po, count = 6);
	{
		@ "PO.W.2: Minimum width of horizontal drawn rectangular or L-shape PO must be 0.04";
		internal1(po_l_s, distance < 0.04, extension = NONE, direction = VERTICAL);
	}
	po_r_l=po_rect or po_l_s;
	{
		@ "PO.W.3: Minimum width of horizontal drawn PO(except rectangular or L_shape PO) must be 0.064";
		internal1(not(po,po_r_l), distance < 0.064, extension = RADIAL);
	}

	{
		@ "PO.W.4: Minimum gate_25 width  must be 0.36";
		internal1 ( gate_25, distance < 0.36 ,extension=RADIAL, relational = POINT_TOUCH, direction = VERTICAL );
	}
	
	{
		@ "PO.W.4.1: Minimum gate_25 length  must be 0.26";
		internal1 ( gate_25, distance < 0.26 ,extension=RADIAL, relational = POINT_TOUCH, direction = HORIZONTAL );
	}
	{
		@ "PO.W.4_2: Minimum gate_18 width must be 0.16";
		internal1 ( gate_18 , distance < 0.16 ,extension=RADIAL, relational = POINT_TOUCH, direction =  VERTICAL );
	}
	
	{
		@ "PO.W.4_3: Minimum gate_18 length must be 0.15";
		internal1 ( gate_18 , distance < 0.15 ,extension=RADIAL, relational = POINT_TOUCH, direction = HORIZONTAL );
	}
/**********************SPECIAL PO RULES***********************************/

	internal: function (
		a: double
		) returning int_result : polygon_layer {
			    int_result = internal1(gate, distance ==a, extension = NONE, direction = HORIZONTAL);
			    }
	
	distance: list of double = {0.03,0.035,0.04,0.045,0.05,0.06,0.08,0.1};

	result = internal1(gate, distance <=  0.1, extension = NONE, direction = HORIZONTAL);
	a=empty_layer();
	{
    
	for(i=0 to distance.size()-1) {
	
	a=a or internal(distance [i]);
	}
		@ "PO exact channel length";	
		result not a;
	}

	po_W_004 = wide (po, distance >= 0.04);
	{
		@ "PO.S Exact PO center to center space when gate width = 0.03, must be 0.152";
		center_to_center1 (po, distance < 0.152,sides = {length1 = 0.03});
	}
	{
		@ "PO.S Exact PO center to center space when gate width = 0.035, must be 0.152";
		center_to_center1 (po, distance < 0.152,sides = {length1 = 0.035});
	}
	{
		@ "PO.S Exact PO center to center space when gate width >= 0.04, must be 0.182";
		center_to_center1 (po_W_004, distance < 0.182);
	}


	
		fpoly_s_1 = external1 ( fpoly , distance < 0.1 ,extension=RADIAL, relational = POINT_TOUCH);
/*************************************END OF SPECIAL PO RULES***************************************/
	
	{
		@ "PO.S.1: PO minimum spacing over field must be 0.1";
		not ( fpoly_s_1 , gate );
	}
	

	{
		@ "PO.S.2: PO minimum spacing over active must be 0.086";
		external1 ( gate , distance < 0.086 ,extension=RADIAL, relational = POINT_TOUCH);
	}
	

		po_s_3 = internal1(gate, distance <=  0.1, extension = NONE, direction = HORIZONTAL);
		po_s_3_check = not (gate , po_s_3);
	{
		@ "PO.S.3: PO minimum spacing over active must be 0.13, if channel length > 0.1";
		external1 ( po_s_3_check , distance < 0.13 ,extension=RADIAL, relational = POINT_TOUCH);
	}
	
	po_span_01_h = not(po,internal1 (po, distance <= 0.1, extension = NONE, direction = HORIZONTAL));
	
	{
		@" PO.S.4: Minimum spacing of edge with span > 0.1, parallel runlength > 0.1, must be 0.125";
		external1(po_span_01_h, distance < 0.125, extension = NONE, direction = HORIZONTAL, orientation = PARALLEL,corner_configuration = ALL, projection = IN, orthogonal=ALL,projection_length > 0.1,intersecting={});	
	}	
	po_span_01_v = not(po,internal1(po, distance <=0.1, extension = NONE, direction = VERTICAL));
	
	{
		@"PO.S.4: Minimum spacing of edge with span > 0.1, parallel runlength > 0.1, must be 0.125";
		external1(po_span_01_v, distance < 0.125, extension = NONE, direction = VERTICAL, orientation = PARALLEL, projection = IN,orthogonal=ALL,corner_configuration=ALL,projection_length > 0.1, intersecting= {} );
	}

/*SWG	{
		@ "PO.S.3: Minimum field poly to DIFF spacing=0.05um";
		external2 ( fpoly , sd_tap , distance < 0.05 ,extension=RADIAL,look_thru = COINCIDENT );
	}*/

	po_int_gate = po interacting gate;
	diff_int = interacting(diff,po_int_gate);

	{
		@ "PO.S.5: Minimum space of PO inner vertex to DIFF of the same MOS";
		external2(po_int_gate,diff_int, distance < 0.035, direction = VERTICAL, extension = NONE, orientation = PARALLEL );
	}

	{
		@ "PO.S.6: Minimum space of PO to DIFF must be 0.02";
		external2(po,diff,distance < 0.02, extension = RADIAL, relational = POINT_TOUCH);
	}
	diff_s_008= internal1(diff, distance < 0.08, extension = RADIAL);
	{
		@ "PO.S.7: Minimum space of PO to DIFF with width < 0.08, parallel runlength > 0.1 must be 0.035";
		external2(po,diff_s_008,distance < 0.035, extension = NONE,projection_length > 0.1, orientation = PARALLEL, intersecting = TOUCH, projection = IN, orthogonal = ALL);
	}
	gate_g_w_006 = wide (gate, distance > 0.06);
	{
		@ "PO.EX.1: Minimum gate extension of active (end cap) must be  0.06";
		enclose (not( gate ,gate_g_w_006), po , distance < 0.06 , extension=RADIAL);
	}
	if( RECOMMENDED == 1 ) {
 	{
		@ "R.PO.EX.1: Recommended minimum gate extension of active (end cap) must be  0.07";
		enclose (not( gate ,gate_g_w_006), po , distance < 0.07 , extension=RADIAL);
	}}
	po_ex_3 = connect ( 		
		    {
		    {{diff_int,po_int_gate},gate},
		    {{po,m1},co},
		    {{m1,m2},via1},
		    {{m2,m3},via2},
		    {{m3,m4},via3},
		    {{m4,m5},via4},
		    {{m5,m6},via6},
		    {{m6,m7},via7},
		    {{m7,m8},via8},
		    {{m8,mt},viat}
		    }
	);

	po_ex_3_3 = external2(po_int_gate,diff_int, distance < 0.3, direction = VERTICAL, extension = NONE, orientation = PARALLEL,connectivity = SAME_NET, connect_sequence = po_ex_3 );
	
	{copy(po_ex_3_3);}

	{
		@ "PO.EX.3: Minimum gate extension of active (PO distance to DIFF inner vertex < 0.3) must be  0.07";
		enclose (gate,interacting(po,po_ex_3_3) , distance < 0.07 , extension=NONE);
	}

	po_ex_2_3 = external2(po_int_gate,diff_int, distance < 0.5, direction = VERTICAL, extension = NONE, orientation = PARALLEL,connectivity = SAME_NET, connect_sequence = po_ex_3 );
	
	po_ex_2 = not(po_ex_2_3,po_ex_3_3);
	{
		@ "PO.EX.2: Minimum gate extension of active (PO distance to DIFF inner vertex < 0.5) must be  0.065";
		enclose (gate,interacting(po,po_ex_2) , distance < 0.065 , extension=NONE);
	}

	
	{
		@ "PO.EX.4 Minimum gate(width>0.06) extension of active must be 0.08";
		enclose (gate_g_w_006, po, distance < 0.08, extension = RADIAL);
	}

	{
		@ "PO.EX.6 Minimun Active extension of gate must be 0.085";
		enclose ( gate , diff , distance < 0.085 ,extension=RADIAL);
	}
	
		gt_coi_act = not_coincident_edge(gate,act);
		 
	{
		@ "PO.G.1 45 and 90 degree gate benting is not allowed";
		adjacent_edge(gt_coi_act,length > 0.0,angle1 = 90.0);
		adjacent_edge(gt_coi_act,length > 0.0,angle1 = 45.0);
	}
	{
		@ "PO.A.1: Minimum po area must be 0.012";
		area(po, value < 0.012);
	}
	{
		@ "PO.A.2: Maximum gate area must be 40 ";
		not_area(gate, value < 40);
	}
	po_003_1 = wide (po, distance >= 0.1);
	po_003   = not  (po, po_003_1);
	gate_s_01_1 = wide (gate_s, distance >= 0.1);
	gate_s_01 = not  (gate_s, gate_s_01_1);
	g1_ext =external1(po_003,distance == 0.122, look_thru = ALL, extension = NONE, direction = HORIZONTAL);
	po_g_2 =external2(po_003_1,po_003,distance == 0.152, look_thru = ALL, extension = NONE, direction = HORIZONTAL);
	po_g_1 =external1(po_003_1,distance == 0.182, look_thru = ALL, extension = NONE, direction = HORIZONTAL);
	po_good = or(or(po_g_1,po_g_2),g1_ext);
	{
		@"PO.G.2:PO(>0.1) spacing to PO(>0.1) must be exact 0.182,PO(>0.1) spacing to PO(<0.1) must be exact 0.152,PO(<0.1) spacing to PO(<0.1) must be exact 0.122 ";
		not(po,interacting(po,po_good));
	}
	
	
	g2_ext =external2(gate_18,po,distance == 0.182, look_thru = ALL, extension = NONE, direction = HORIZONTAL);
	{
		@"PO.G.2_2:Gate_18 must be surrounded by PO from both sides with exact spacing 0.182"; ///Arman 0.152->0.182
	not(gate_18,interacting(gate_18,g2_ext, count = 2));
	}
	
	g3_ext =external2(gate_25,po,distance == 0.182, look_thru = ALL, extension = NONE, direction = HORIZONTAL);
	{
		@"PO.G.2_3:Gate_25 must be surrounded by PO from both sides with exact spacing 0.182"; ///Nerses 0.152->0.182
	not(gate_25,interacting(gate_25,g3_ext, count = 2));
	}
	
	{
	@"PO.L.1_a: Maximum PO length(PO width < 0.062) between two contacts inside same poly must be 15";
	po_1 = internal1(po,distance < 0.062, extension = RADIAL);
	po_2 = interacting(po,po_1);
	po_3 = interacting( po_2, co, count > 1);
	co_1 = interacting(co,po_3 );
	//ext = external1(co_1,distance<15,extension = RADIAL);
	//co_3 = interacting (co_1, ext);
	//not(co_1,co_3);
	co_2 = size(co_1,distance=0.02);
	//po_edge1 = and_edge(po_2,co_2);
	//po_edge2 =not_edge(po_3,co_2);
	//po_edge3 =and_edge(co_2,po_2);	
	po_c = internal1(po_3,distance < 0.2, extension = RADIAL,orientation = {PARALLEL},intersecting = {}, output_type = CENTERLINE);
	po_c_n = not_edge(po_c,co_2);
	length_edge(po_c_n, distance= [15,900],corners = CONNECT);
	}
	
	{
	@"PO.L.1_b: Maximum PO length (PO width < 0.062) between any point inside gate to nearest contact inside same poly must be 15";
	po_11 = internal1(po,distance < 0.062, extension = RADIAL);
	cp1 =  interacting(po_11,co);
	gp1 =  interacting(po, gate);
	cg1= interacting(co,gp1);
	gp_c = internal1(gp1,distance < 0.2, extension = RADIAL,orientation = {PARALLEL},intersecting = {}, output_type = CENTERLINE);
	gp_n = not_edge(gp_c,cg1);
	length_edge(gp_n, distance= [15,900],corners = CONNECT);
	}

//***********************************************   M1 RULES 
	{
		@"R.M1.L.1: Minimum length of edge connecting convex and concave corners must be 0.04";
		internal_corner1(m1, distance < 0.04, type = {CONVEX_TO_CONCAVE});
	}

	{
		@ "M1.W.1: Minimum M1 width must be 0.05";
		internal1 ( m1 , distance < 0.05 ,extension = RADIAL, relational = POINT_TOUCH );
	}
	{
		@ "M1.W.2: Maximum M1 width must be 5";
		wide (m1,distance>5);
	}

	{
		@ "M1.S.1: Minimum M1 spacing must be 0.05";
		external1 ( m1 , distance < 0.05 ,extension = RADIAL, relational = POINT_TOUCH);
	}

	m1_s_10_1 = internal1 ( m1 , distance <= 0.1 ,extension = RADIAL, relational = POINT_TOUCH );
	m1_s_10_2 = wide(m1, distance >= 0.8);
	{
		@ "M1.S.10: Minimum M1 spacing of end of line (width <= 0.1) to neighbour line (width >= 0.8) must be 0.1";
		external2(m1_s_10_1, m1_s_10_2, distance < 0.1,extension = RADIAL);

	}
 	if( RECOMMENDED == 1 ) {
	{
		@ "R.M1.S.11: Minimum M1 spacing between two end of lines (width <=0.1) must be 0.12";
		external1 ( m1_s_10_1 , distance < 0.12 ,extension = RADIAL, relational = POINT_TOUCH);
	}}
    
    m1_w_015 =wide(m1, distance > 0.15);
    m1_w_03 =wide(m1, distance > 0.3);	
    m1_w_15 = wide(m1, distance > 1.5);	
    m1_w_3 =wide(m1, distance > 3);
  
    	
	{
		@ "M1.S.2: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.06";
	    	external2(m1_w_015,m1,distance < 0.06, extension = NONE,projection_length > 0.15, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M1.S.3: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.1";
	    	external2(m1_w_03,m1,distance < 0.1, extension = NONE,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M1.S.4: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.5";
	    	external2(m1_w_15,m1,distance < 0.5, extension = NONE,projection_length > 1.5, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M1.S.5: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.6";
	   	external2(m1_w_3,m1,distance < 0.6, extension = NONE,projection_length > 3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

    m1_s_01_h = not(m1, internal1(m1,distance < 0.1,extension = NONE, direction = HORIZONTAL));
    m1_s_01_v = not(m1, internal1(m1,distance < 0.1,extension = NONE, direction = VERTICAL));
    m1_s_03_h = not(m1, internal1(m1,distance <= 0.3,extension = NONE, direction = HORIZONTAL));
    m1_s_03_v = not(m1, internal1(m1,distance <= 0.3,extension = NONE, direction = VERTICAL));
	{
	  	@ "M1.S.6: Minimum spacing of M1 with span >= 0.1 with parallel run length > 0.2 must be 0.06";
	  	external1(m1_s_01_h, distance < 0.06, extension = NONE,direction = HORIZONTAL,projection_length > 0.2, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	  	@ "M1.S.6_1: Minimum spacing of M1 with span >= 0.1 with parallel run length > 0.2 must be 0.06";
	   	external1(m1_s_01_v, distance < 0.06, extension = NONE,direction = VERTICAL,projection_length > 0.2, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M1.S.7: Minimum spacing of M1 with span > 0.3 with parallel run length > 0.3 must be 0.075";
	  	external1(m1_s_03_h, distance < 0.075, extension = NONE,direction = HORIZONTAL,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	
	{
	    	@ "M1.S.7_1: Minimum spacing of M1 with span > 0.3 with parallel run length > 0.3 must be 0.075";
	    	external1(m1_s_03_v, distance < 0.075, extension = NONE,direction = VERTICAL,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	m1_s_8 = connect ( 		
		    {
		    {{po,m1},co},
		    {{m1,m2},via1},
		    {{m2,m3},via2},
		    {{m3,m4},via3},
		    {{m4,m5},via4},
		    {{m5,m6},via6},
		    {{m6,m7},via7},
		    {{m7,m8},via8},
		    {{m8,mt},viat}
		    }
	);
/*
	{
		@ "M1.S.8 Minimum spacing to neighboring VIA1 must be 0.08";
		external2 ( m1, via1, distance < 0.08, extension = RADIAL, look_thru = ALL, relational = POINT_TOUCH,connectivity = DIFFERENT_NET,connect_sequence = m1_s_8 );
	}
*/

	{	
		@ "M1.A.1  M1 minimum area must be 0.01";
		area ( m1 , value < 0.01 );
	}
   	 m1_hole = donut_holes (m1, INNER, area > 0.2);
	{
	   	@ "M1.A.2: M1 minimum enclosed area must be 0.2";
	 	not( donut_holes(m1, INNER), m1_hole);
		
	}

		m1wide = size ( m1 , -0.075 ); 
		m1wide = size ( m1wide , 0.075);

	{
		@ "M1.S.9: Minimum spacing when either metal line is wider than 0.15 must be 0.055";
		external2 ( m1 , m1wide , distance < 0.055 ,extension=RADIAL,look_thru = COINCIDENT , intersecting = TOUCH );
	}

	{	
		@"M1.W.2.1: Minimum width of thin wire with length less than 0.1, connected to fat wire with width larges than 0.15, must be 0.06";
		m1_fat_wire_1 = wide(m1,distance >= 0.15);
		m1_not_fat = not(m1,m1_fat_wire_1);
		m1_thin_w_int = interacting_edge(m1_not_fat,m1_fat_wire_1);
		adjacent_edge(m1_thin_w_int,length < 0.06, angle1 > 30, angle2 >30, adjacent_length1 > 0, adjacent_length2 <= 0.1); 
	}	
	{	
		@"M1.W.2.2: Minimum width of thin wire with length less than 0.17, connected to fat wire with width larges than 0.3, must be 0.07";
		m1_fat_wire_2 = wide(m1,distance >= 0.3);
		m1_not_fat_2 = not(m1,m1_fat_wire_2);
		m1_thin_w_int_2 = interacting_edge(m1_not_fat_2,m1_fat_wire_2);
		adjacent_edge(m1_thin_w_int_2,length < 0.07, angle1 > 1, angle2 >1, adjacent_length1 > 0, adjacent_length2 <= 0.17); 
	}	
	{	
		@"M1.W.2.3: Minimum width of thin wire with length less than 0.7, connected to fat wire with width larges than 1.5, must be 0.15";
		m1_fat_wire_3 = wide(m1,distance >= 1.5);
		m1_not_fat_3 = not(m1,m1_fat_wire_3);
		m1_thin_w_int_3 = interacting_edge(m1_not_fat_3,m1_fat_wire_3);
		adjacent_edge(m1_thin_w_int_3,length < 0.15, angle1 > 3, angle2 >3, adjacent_length1 > 0, adjacent_length2 <= 0.7); 
	}	
/*	{	
		@"M1.W.4: Minimum width of thin wire with length less than 1.5, connected to fat wire with width larges than 3, must be 0.3";
		m1_fat_wire_4 = wide(m1,distance >= 3);
		m1_not_fat_4 = not(m1,m1_fat_wire_4);
		m1_thin_w_int_4 = interacting_edge(m1_not_fat_4,m1_fat_wire_4);
		adjacent_edge(m1_thin_w_int_4,length < 0.3, angle1 > 3, angle2 >3, adjacent_length1 > 0, adjacent_length2 <= 1.5); 
	}	
*/	
//********************************************   M2 Rules **********************************************************
 

	{
		@ "M2.W.1: Minimum M2 width must be 0.056";
		internal1 ( m2 , distance < 0.056 ,extension = RADIAL, relational = POINT_TOUCH );
	}
	{
		@ "M2.W.2: Maximum M2 width must be 5";
		wide (m2,distance>5);
	}

	{
		@ "M2.S.1: Minimum M2 spacing must be 0.056";
		external1 ( m2 , distance < 0.056 ,extension = RADIAL, relational = POINT_TOUCH);
	}
    
    m2_w_015 =wide(m2, distance >= 0.15);
    m2_w_03 =wide(m2, distance >= 0.3);	
    m2_w_15 = wide(m2, distance >= 1.5);	
    m2_w_3 =wide(m2, distance >= 3);
  
    	
	{
	    	@ "M2.S.3.1: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.064";
	 	external2(m2_w_015,m2,distance < 0.064, extension = NONE,projection_length >= 0.15, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M2.S.3.2: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.11";
	    	external2(m2_w_03,m2,distance < 0.11, extension = NONE,projection_length >= 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M2.S.3.3: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.6";
	    	external2(m2_w_15,m2,distance < 0.6, extension = NONE,projection_length >= 1.5, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M2.S.3.4: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.7";
	    	external2(m2_w_3,m2,distance < 0.7, extension = NONE,projection_length >= 3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

    m2_s_01_h = not(m2, internal1(m2,distance < 0.1,extension = NONE, direction = HORIZONTAL));
    m2_s_01_v = not(m2, internal1(m2,distance < 0.1,extension = NONE, direction = VERTICAL));
    m2_s_03_h = not(m2, internal1(m2,distance < 0.3,extension = NONE, direction = HORIZONTAL));
    m2_s_03_v = not(m2, internal1(m2,distance < 0.3,extension = NONE, direction = VERTICAL));
	{
	    	@ "M2.S.6: Minimum spacing of M2 with span > 0.1 with parallel run length > 0.2 must be 0.12";
	    	external1(m2_s_01_h, distance < 0.12, extension = NONE,direction = HORIZONTAL,projection_length > 0.2, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M2.S.6_1: Minimum spacing of M2 with span > 0.1 with parallel run length > 0.2 must be 0.12";
	    	external1(m2_s_01_v, distance < 0.12, extension = NONE,direction = VERTICAL,projection_length > 0.2, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M2.S.7: Minimum spacing of M2 with span > 0.3 with parallel run length > 0.3 must be 0.14";
	    	external1(m2_s_03_h, distance < 0.14, extension = NONE,direction = HORIZONTAL,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	
	{
	    	@ "M2.S.7_1: Minimum spacing of M2 with span > 0.3 with parallel run length > 0.3 must be 0.14";
	    	external1(m2_s_03_v, distance < 0.14, extension = NONE,direction = VERTICAL,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	

	{
		@ "M2.S.8: Minimum spacing to neighboring  VIAx must be 0.08";
		external2 ( m2, via1, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
	}
	
	{
		@ "M2.S.8_1: Minimum spacing to neighboring  VIAx must be 0.08";
		external2 ( m2, via2, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
	}
	{	
		@ "M2.A.1  M2 minimum area must be 0.016";
		area ( m2 , value < 0.016 );
	}
    	m2_hole = donut_holes (m2, INNER, area > 0.2);
	{
		@ "M2.A.2: M2 minimum enclosed area must be 0.2";
	    	not( donut_holes(m2, INNER), m2_hole);
		
	}

		m2wide = size ( m2 , -0.075 ); 
		m2wide = size ( m2wide , 0.075);

	{
		@ "M2.S.2: Minimum spacing when either metal line is wider than 0.15 must be 0.06";
		external2 ( m2 , m2wide , distance < 0.06 ,extension=RADIAL,look_thru = COINCIDENT , intersecting = TOUCH );
	}
	
	{	
		@"M2.W.2.1: Minimum width of thin wire with length less than 0.1, connected to fat wire with width larges than 0.15, must be 0.06";
		m2_fat_wire_1 = wide(m2,distance >= 0.15);
		m2_not_fat = not(m2,m2_fat_wire_1);
		m2_thin_w_int = interacting_edge(m2_not_fat,m2_fat_wire_1);
		adjacent_edge(m2_thin_w_int,length < 0.06, angle1 > 30, angle2 >30, adjacent_length1 > 0, adjacent_length2 <= 0.1); 
	}	
	{	
		@"M2.W.2.2: Minimum width of thin wire with length less than 0.17, connected to fat wire with width larges than 0.3, must be 0.07";
		m2_fat_wire_2 = wide(m2,distance >= 0.3);
		m2_not_fat_2 = not(m2,m2_fat_wire_2);
		m2_thin_w_int_2 = interacting_edge(m2_not_fat_2,m2_fat_wire_2);
		adjacent_edge(m2_thin_w_int_2,length < 0.07, angle1 > 1, angle2 >1, adjacent_length1 > 0, adjacent_length2 <= 0.17); 
	}	
	{	
		@"M2.W.2.3: Minimum width of thin wire with length less than 0.7, connected to fat wire with width larges than 1.5, must be 0.15";
		m2_fat_wire_3 = wide(m2,distance >= 1.5);
		m2_not_fat_3 = not(m2,m2_fat_wire_3);
		m2_thin_w_int_3 = interacting_edge(m2_not_fat_3,m2_fat_wire_3);
		adjacent_edge(m2_thin_w_int_3,length < 0.15, angle1 > 3, angle2 >3, adjacent_length1 > 0, adjacent_length2 <= 0.7); 
	}
	{	
		@"M2.W.2.4: Minimum width of thin wire with length less than 1.5, connected to fat wire with width larges than 3, must be 0.3";
		m2_fat_wire_4 = wide(m2,distance >= 3);
		m2_not_fat_4 = not(m2,m2_fat_wire_4);
		m2_thin_w_int_4 = interacting_edge(m2_not_fat_4,m2_fat_wire_4);
		adjacent_edge(m2_thin_w_int_4,length < 0.3, angle1 > 3, angle2 >3, adjacent_length1 > 0, adjacent_length2 <= 1.5); 
	}	
	




//********************************************   M3 Rules **********************************************************
 

	{
		@ "M3.W.1: Minimum M3 width must be 0.056";
		internal1 ( m3 , distance < 0.056 ,extension = RADIAL, relational = POINT_TOUCH );
	}
	{
		@ "M3.W.2: Maximum M3 width must be 5";
		wide (m3,distance>5);
	}

	{
		@ "M3.S.1: Minimum M3 spacing must be 0.056";
		external1 ( m3 , distance < 0.056 ,extension = RADIAL, relational = POINT_TOUCH);
	}
    
    m3_w_015 =wide(m3, distance >= 0.15);
    m3_w_03 =wide(m3, distance >= 0.3);	
    m3_w_15 = wide(m3, distance >= 1.5);	
    m3_w_3 =wide(m3, distance >= 3);
  
    		cdb1 = connect ( 		
		    {
		    {{n1},nwell},
		    {{n1,m1},co},
		    {{m1,m2},via1},
		    {{m2,m3},via2},
		    {{m3,m4},via3},
		    {{m4,m5},via4},
		    {{m5,m6},via6},
		    {{m6,m7},via7},
		    {{m7,m8},via8},
		    {{m8,mt},viat}
		    }
	);
	{
	   	@ "M3.S.3.1: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.064";
	    	external2(m3_w_015,m3,distance < 0.064, extension = NONE,projection_length >= 0.15, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M3.S.3.2: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.11";
	    	external2(m3_w_03,m3,distance < 0.11, extension = NONE,projection_length >= 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
		@ "M3.S.3.3: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.6";
	    	external2(m3_w_15,m3,distance < 0.6, extension = NONE,projection_length >= 1.5, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M3.S.3.4: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.7";
	    	external2(m3_w_3,m3,distance < 0.7, extension = NONE,projection_length >= 3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

    m3_s_01_h = not(m3, internal1(m3,distance < 0.1,extension = NONE, direction = HORIZONTAL));
    m3_s_01_v = not(m3, internal1(m3,distance < 0.1,extension = NONE, direction = VERTICAL));
    m3_s_03_h = not(m3, internal1(m3,distance < 0.3,extension = NONE, direction = HORIZONTAL));
    m3_s_03_v = not(m3, internal1(m3,distance < 0.3,extension = NONE, direction = VERTICAL));
	{
	   	 @ "M3.S.6: Minimum spacing of M3 with span > 0.1 with parallel run length > 0.2 must be 0.12";
	    	external1(m3_s_01_h, distance < 0.12, extension = NONE,direction = HORIZONTAL,projection_length > 0.2, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M3.S.6_1: Minimum spacing of M3 with span > 0.1 with parallel run length > 0.2 must be 0.12";
	    	external1(m3_s_01_v, distance < 0.12, extension = NONE,direction = VERTICAL,projection_length > 0.2, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M3.S.7: Minimum spacing of M3 with span > 0.3 with parallel run length > 0.3 must be 0.14";
	    	external1(m3_s_03_h, distance < 0.14, extension = NONE,direction = HORIZONTAL,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	
	{
	    	@ "M3.S.7_1: Minimum spacing of M3 with span > 0.3 with parallel run length > 0.3 must be 0.14";
	    	external1(m3_s_03_v, distance < 0.14, extension = NONE,direction = VERTICAL,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	

	{
		@ "M3.S.8: Minimum spacing to neighboring  VIAx must be 0.08";
		external2 ( m3, via2, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
	}
	
	{
		@ "M3.S.8_1: Minimum spacing to neighboring  VIAx must be 0.08";
		external2 ( m3, via3, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
	}
	{	
		@ "M3.A.1  M3 minimum area must be 0.016";
		area ( m3 , value < 0.016 );
	}
    m3_hole = donut_holes (m3, INNER, area > 0.2);
	{
		@ "M3.A.2: M3 minimum enclosed area must be 0.2";
	    	not( donut_holes(m3, INNER), m3_hole);
		
	}

		m3wide = size ( m3 , -0.075 ); 
		m3wide = size ( m3wide , 0.075);

	{
		@ "M3.S.2: Minimum spacing when either metal line is wider than 0.15 must be 0.06";
		external2 ( m3 , m3wide , distance < 0.06 ,extension=RADIAL,look_thru = COINCIDENT , intersecting = TOUCH );
	}

		
	{	
		@"R.M3.W.2.1: Minimum width of thin wire with length less than 0.1, connected to fat wire with width larges than 0.15, must be 0.06";
		m3_fat_wire_1 = wide(m3,distance >= 0.15);
		m3_not_fat = not(m3,m3_fat_wire_1);
		m3_thin_w_int = interacting_edge(m3_not_fat,m3_fat_wire_1);
		adjacent_edge(m3_thin_w_int,length < 0.06, angle1 > 30, angle2 >30, adjacent_length1 > 0, adjacent_length2 <= 0.1); 
	}	
	{	
		@"R.M3.W.2.2: Minimum width of thin wire with length less than 0.17, connected to fat wire with width larges than 0.3, must be 0.07";
		m3_fat_wire_2 = wide(m3,distance >= 0.3);
		m3_not_fat_2 = not(m3,m3_fat_wire_2);
		m3_thin_w_int_2 = interacting_edge(m3_not_fat_2,m3_fat_wire_2);
		adjacent_edge(m3_thin_w_int_2,length < 0.07, angle1 > 1, angle2 >1, adjacent_length1 > 0, adjacent_length2 <= 0.17); 
	}	
	{	
		@"R.M3.W.2.3: Minimum width of thin wire with length less than 0.7, connected to fat wire with width larges than 1.5, must be 0.15";
		m3_fat_wire_3 = wide(m3,distance >= 1.5);
		m3_not_fat_3 = not(m3,m3_fat_wire_3);
		m3_thin_w_int_3 = interacting_edge(m3_not_fat_3,m3_fat_wire_3);
		adjacent_edge(m3_thin_w_int_3,length < 0.15, angle1 > 3, angle2 >3, adjacent_length1 > 0, adjacent_length2 <= 0.7); 
	}

	{	
		@"R.M3.W.2.4: Minimum width of thin wire with length less than 1.5, connected to fat wire with width larges than 3, must be 0.3";
		m3_fat_wire_4 = wide(m3,distance >= 3);
		m3_not_fat_4 = not(m3,m3_fat_wire_4);
		m3_thin_w_int_4 = interacting_edge(m3_not_fat_4,m3_fat_wire_4);
		adjacent_edge(m3_thin_w_int_4,length < 0.3, angle1 > 3, angle2 >3, adjacent_length1 > 0, adjacent_length2 <= 1.5); 
	}	
	

//********************************************   M4 Rules **********************************************************
 

	{
		@ "M4.W.1: Minimum M4 width must be 0.056";
		internal1 ( m4 , distance < 0.056 ,extension = RADIAL, relational = POINT_TOUCH );
	}
	{
		@ "M4.W.2: Maximum M4 width must be 5";
		wide (m4,distance>5);
	}

	{
		@ "M4.S.1: Minimum M4 spacing must be 0.056";
		external1 ( m4 , distance < 0.056 ,extension = RADIAL, relational = POINT_TOUCH);
	}
    
    m4_w_015 =wide(m4, distance >= 0.15);
    m4_w_03 =wide(m4, distance >= 0.3);	
    m4_w_15 = wide(m4, distance >= 1.5);	
    m4_w_3 =wide(m4, distance >= 3);
  
    	
	{
	   	@ "M4.S.3.1: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.064";
	    	external2(m4_w_015,m4,distance < 0.064, extension = NONE,projection_length >= 0.15, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M4.S.3.2: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.11";
	    	external2(m4_w_03,m4,distance < 0.11, extension = NONE,projection_length >= 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
		@ "M4.S.3.3: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.6";
	    	external2(m4_w_15,m4,distance < 0.6, extension = NONE,projection_length >= 1.5, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M4.S.3.4: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.7";
	    	external2(m4_w_3,m4,distance < 0.7, extension = NONE,projection_length >= 3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

    m4_s_01_h = not(m4, internal1(m4,distance < 0.1,extension = NONE, direction = HORIZONTAL));
    m4_s_01_v = not(m4, internal1(m4,distance < 0.1,extension = NONE, direction = VERTICAL));
    m4_s_03_h = not(m4, internal1(m4,distance < 0.3,extension = NONE, direction = HORIZONTAL));
    m4_s_03_v = not(m4, internal1(m4,distance < 0.3,extension = NONE, direction = VERTICAL));
	{
	    	@ "M4.S.6: Minimum spacing of M4 with span > 0.1 with parallel run length > 0.2 must be 0.12";
	    	external1(m4_s_01_h, distance < 0.12, extension = NONE,direction = HORIZONTAL,projection_length > 0.2, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M4.S.6_1: Minimum spacing of M4 with span > 0.1 with parallel run length > 0.2 must be 0.12";
	    	external1(m4_s_01_v, distance < 0.12, extension = NONE,direction = VERTICAL,projection_length > 0.2, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M4.S.7: Minimum spacing of M4 with span > 0.3 with parallel run length > 0.3 must be 0.14";
	    	external1(m4_s_03_h, distance < 0.14, extension = NONE,direction = HORIZONTAL,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	
	{
	    	@ "M4.S.7_1: Minimum spacing of M4 with span > 0.3 with parallel run length > 0.3 must be 0.14";
	    	external1(m4_s_03_v, distance < 0.14, extension = NONE,direction = VERTICAL,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	

	{
		@ "M4.S.8: Minimum spacing to neighboring  VIAx must be 0.08";
		external2 ( m4, via4, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
	}
	
	{
		@ "M4.S.8_1: Minimum spacing to neighboring  VIAx must be 0.08";
		external2 ( m4, via3, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
	}
	{	
		@ "M4.A.1  M4 minimum area must be 0.016";
		area ( m4 , value < 0.016 );
	}
    m4_hole = donut_holes (m4, INNER, area > 0.2);
	{
	    	@ "M4.A.2: M4 minimum enclosed area must be 0.2";
	    	not( donut_holes(m4, INNER), m4_hole);
		
	}

		m4wide = size ( m4 , -0.075 ); 
		m4wide = size ( m4wide , 0.075);

	{
		@ "M4.S.2: Minimum spacing when either metal line is wider than 0.15 must be 0.06";
		external2 ( m4 , m4wide , distance < 0.06 ,extension=RADIAL,look_thru = COINCIDENT , intersecting = TOUCH );
	}
	
	{	
		@"R.M4.W.2.1: Minimum width of thin wire with length less than 0.1, connected to fat wire with width larges than 0.15, must be 0.06";
		m4_fat_wire_1 = wide(m4,distance >= 0.15);
		m4_not_fat = not(m4,m4_fat_wire_1);
		m4_thin_w_int = interacting_edge(m4_not_fat,m4_fat_wire_1);
		adjacent_edge(m4_thin_w_int,length < 0.06, angle1 > 30, angle2 >30, adjacent_length1 > 0, adjacent_length2 <= 0.1); 
	}
	{	
		@"R.M4.W.2.2: Minimum width of thin wire with length less than 0.17, connected to fat wire with width larges than 0.3, must be 0.07";
		m4_fat_wire_2 = wide(m4,distance >= 0.3);
		m4_not_fat_2 = not(m4,m4_fat_wire_2);
		m4_thin_w_int_2 = interacting_edge(m4_not_fat_2,m4_fat_wire_2);
		adjacent_edge(m4_thin_w_int_2,length < 0.07, angle1 > 1, angle2 >1, adjacent_length1 > 0, adjacent_length2 <= 0.17); 
	}	
	{	
		@"R.M4.W.2.3: Minimum width of thin wire with length less than 0.7, connected to fat wire with width larges than 1.5, must be 0.15";
		m4_fat_wire_3 = wide(m4,distance >= 1.5);
		m4_not_fat_3 = not(m4,m4_fat_wire_3);
		m4_thin_w_int_3 = interacting_edge(m4_not_fat_3,m4_fat_wire_3);
		adjacent_edge(m4_thin_w_int_3,length < 0.15, angle1 > 3, angle2 >3, adjacent_length1 > 0, adjacent_length2 <= 0.7); 
	}


	{	
		@"R.M4.W.2.4: Minimum width of thin wire with length less than 1.5, connected to fat wire with width larges than 3, must be 0.3";
		m4_fat_wire_4 = wide(m4,distance >= 3);
		m4_not_fat_4 = not(m4,m4_fat_wire_4);
		m4_thin_w_int_4 = interacting_edge(m4_not_fat_4,m4_fat_wire_4);
		adjacent_edge(m4_thin_w_int_4,length < 0.3, angle1 > 3, angle2 >3, adjacent_length1 > 0, adjacent_length2 <= 1.5); 
	}	
	

//********************************************   M5 Rules **********************************************************
 

	{
		@ "M5.W.1: Minimum M5 width must be 0.056";
		internal1 ( m5 , distance < 0.056 ,extension = RADIAL, relational = POINT_TOUCH );
	}
	{
		@ "M5.W.2: Maximum M5 width must be 5";
		wide (m5,distance>5);
	}

	{
		@ "M5.S.1: Minimum M5 spacing must be 0.056";
		external1 ( m5 , distance < 0.056 ,extension = RADIAL, relational = POINT_TOUCH);
	}
    
    m5_w_015 =wide(m5, distance >= 0.15);
    m5_w_03 =wide(m5, distance >= 0.3);	
    m5_w_15 = wide(m5, distance >= 1.5);	
    m5_w_3 =wide(m5, distance >= 3);
  
    	
	{
	    	@ "M5.S.3.1: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.064";
	    	external2(m5_w_015,m5,distance < 0.064, extension = NONE,projection_length >= 0.15, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M5.S.3.2: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.11";
	    	external2(m5_w_03,m5,distance < 0.11, extension = NONE,projection_length >= 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M5.S.3.3: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.6";
	    	external2(m5_w_15,m5,distance < 0.6, extension = NONE,projection_length >= 1.5, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M5.S.3.4: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.7";
	    	external2(m5_w_3,m5,distance < 0.7, extension = NONE,projection_length >= 3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

    m5_s_01_h = not(m5, internal1(m5,distance < 0.1,extension = NONE, direction = HORIZONTAL));
    m5_s_01_v = not(m5, internal1(m5,distance < 0.1,extension = NONE, direction = VERTICAL));
    m5_s_03_h = not(m5, internal1(m5,distance < 0.3,extension = NONE, direction = HORIZONTAL));
    m5_s_03_v = not(m5, internal1(m5,distance < 0.3,extension = NONE, direction = VERTICAL));
	{
	    	@ "M5.S.6: Minimum spacing of M5 with span > 0.1 with parallel run length > 0.2 must be 0.12";
	    	external1(m5_s_01_h, distance < 0.12, extension = NONE,direction = HORIZONTAL,projection_length > 0.2, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	   	@ "M5.S.6_1: Minimum spacing of M5 with span > 0.1 with parallel run length > 0.2 must be 0.12";
	    	external1(m5_s_01_v, distance < 0.12, extension = NONE,direction = VERTICAL,projection_length > 0.2, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M5.S.7: Minimum spacing of M5 with span > 0.3 with parallel run length > 0.3 must be 0.14";
	    	external1(m5_s_03_h, distance < 0.14, extension = NONE,direction = HORIZONTAL,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	
	{
	    	@ "M5.S.7_1: Minimum spacing of M5 with span > 0.3 with parallel run length > 0.3 must be 0.14";
	    	external1(m5_s_03_v, distance < 0.14, extension = NONE,direction = VERTICAL,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	

	{
		@ "M5.S.8: Minimum spacing to neighboring  VIAx must be 0.08";
		external2 ( m5, via4, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
	}
	
	{
		@ "M5.S.8_1: Minimum spacing to neighboring  VIAx must be 0.08";
		external2 ( m5, via5, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
	}
	{	
		@ "M5.A.1  M5 minimum area must be 0.016";
		area ( m5 , value < 0.016 );
	}
    m5_hole = donut_holes (m5, INNER, area > 0.2);
	{
	   	 @ "M5.A.2: M5 minimum enclosed area must be 0.2";
	    	not( donut_holes(m5, INNER), m5_hole);
		
	}

		m5wide = size ( m5 , -0.075 ); 
		m5wide = size ( m5wide , 0.075);

	{
		@ "M5.S.2: Minimum spacing when either metal line is wider than 0.15 must be 0.06";
		external2 ( m5 , m5wide , distance < 0.06 ,extension=RADIAL,look_thru = COINCIDENT , intersecting = TOUCH );
	}

	{	
		@"M5.W.2.1: Minimum width of thin wire with length less than 0.1, connected to fat wire with width larges than 0.15, must be 0.06";
		m5_fat_wire_1 = wide(m5,distance >= 0.15);
		m5_not_fat = not(m5,m5_fat_wire_1);
		m5_thin_w_int = interacting_edge(m5_not_fat,m5_fat_wire_1);
		adjacent_edge(m5_thin_w_int,length < 0.06, angle1 > 30, angle2 >30, adjacent_length1 > 0, adjacent_length2 <= 0.1); 
	}
	{	
		@"M5.W.2.2: Minimum width of thin wire with length less than 0.17, connected to fat wire with width larges than 0.3, must be 0.07";
		m5_fat_wire_2 = wide(m5,distance >= 0.3);
		m5_not_fat_2 = not(m5,m5_fat_wire_2);
		m5_thin_w_int_2 = interacting_edge(m5_not_fat_2,m5_fat_wire_2);
		adjacent_edge(m5_thin_w_int_2,length < 0.07, angle1 > 1, angle2 >1, adjacent_length1 > 0, adjacent_length2 <= 0.17); 
	}	
	{	
		@"M5.W.2.3: Minimum width of thin wire with length less than 0.7, connected to fat wire with width larges than 1.5, must be 0.15";
		m5_fat_wire_3 = wide(m5,distance >= 1.5);
		m5_not_fat_3 = not(m5,m5_fat_wire_3);
		m5_thin_w_int_3 = interacting_edge(m5_not_fat_3,m5_fat_wire_3);
		adjacent_edge(m5_thin_w_int_3,length < 0.15, angle1 > 3, angle2 >3, adjacent_length1 > 0, adjacent_length2 <= 0.7); 
	}

	{	
		@"M5.W.2.4: Minimum width of thin wire with length less than 1.5, connected to fat wire with width larges than 3, must be 0.3";
		m5_fat_wire_4 = wide(m5,distance >= 3);
		m5_not_fat_4 = not(m5,m5_fat_wire_4);
		m5_thin_w_int_4 = interacting_edge(m5_not_fat_4,m5_fat_wire_4);
		adjacent_edge(m5_thin_w_int_4,length < 0.3, angle1 > 3, angle2 >3, adjacent_length1 > 0, adjacent_length2 <= 1.5); 
	}	
	




//********************************************   M6 Rules **********************************************************
 

	{
		@ "M6.W.1: Minimum M6 width must be 0.056";
		internal1 ( m6 , distance < 0.056 ,extension = RADIAL, relational = POINT_TOUCH );
	}
	{
		@ "M6.W.2: Maximum M6 width must be 5";
		wide (m6,distance>5);
	}

	{
		@ "M6.S.1: Minimum M6 spacing must be 0.056";
		external1 ( m6 , distance < 0.056 ,extension = RADIAL, relational = POINT_TOUCH);
	}
    
    m6_w_015 =wide(m6, distance >= 0.15);
    m6_w_03 =wide(m6, distance >= 0.3);	
    m6_w_15 = wide(m6, distance >= 1.5);	
    m6_w_3 =wide(m6, distance >= 3);
  
    	
	{
	 	@ "M6.S.3.1: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.064";
	    	external2(m6_w_015,m6,distance < 0.064, extension = NONE,projection_length >= 0.15, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
		@ "M6.S.3.2: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.11";
	    	external2(m6_w_03,m6,distance < 0.11, extension = NONE,projection_length >= 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M6.S.3.3: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.6";
	    	external2(m6_w_15,m6,distance < 0.6, extension = NONE,projection_length >= 1.5, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M6.S.3.4: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.7";
	    	external2(m6_w_3,m6,distance < 0.7, extension = NONE,projection_length >= 3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

    m6_s_01_h = not(m6, internal1(m6,distance < 0.1,extension = NONE, direction = HORIZONTAL));
    m6_s_01_v = not(m6, internal1(m6,distance < 0.1,extension = NONE, direction = VERTICAL));
    m6_s_03_h = not(m6, internal1(m6,distance < 0.3,extension = NONE, direction = HORIZONTAL));
    m6_s_03_v = not(m6, internal1(m6,distance < 0.3,extension = NONE, direction = VERTICAL));

	
	{
	  	@ "R.M6.S.6: Minimum spacing of M6 with span > 0.1 with parallel run length > 0.2 must be 0.12";
	    	external1(m6_s_01_v, distance < 0.12, extension = NONE,direction = VERTICAL,projection_length > 0.2, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "R.M6.S.6_1: Minimum spacing of M6 with span > 0.1 with parallel run length > 0.2 must be 0.12";
	    	external1(m6_s_01_h, distance < 0.12, extension = NONE,direction = HORIZONTAL,projection_length > 0.2, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	
	{
	    	@ "M6.S.7: Minimum spacing of M6 with span > 0.3 with parallel run length > 0.3 must be 0.14";
	    	external1(m6_s_03_v, distance < 0.14, extension = NONE,direction = VERTICAL,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	
	{
	    	@ "M6.S.7_1: Minimum spacing of M6 with span > 0.3 with parallel run length > 0.3 must be 0.14";
	    	external1(m6_s_03_h, distance < 0.14, extension = NONE,direction = HORIZONTAL,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	

	{
		@ "M6.S.8: Minimum spacing to neighboring  VIAx must be 0.08";
		external2 ( m6, via6, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
	}
	
	{
		@ "M6.S.8_1: Minimum spacing to neighboring VIAx must be 0.08";
		external2 ( m6, via5, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
	}
	{	
		@ "M6.A.1  M6 minimum area must be 0.016";
		area ( m6 , value < 0.016 );
	}
    m6_hole = donut_holes (m6, INNER, area > 0.2);
	{
	    	@ "M6.A.2: M6 minimum enclosed area must be 0.2";
	    	not( donut_holes(m6, INNER), m6_hole);
		
	}

		m6wide = size ( m6 , -0.075 ); 
		m6wide = size ( m6wide , 0.075);

	{
		@ "M6.S.2: Minimum spacing when either metal line is wider than 0.15 must be 0.06";
		external2 ( m6 , m6wide , distance < 0.06 ,extension=RADIAL,look_thru = COINCIDENT , intersecting = TOUCH );
	}
	{	
		@"M6.W.2.1: Minimum width of thin wire with length less than 0.1, connected to fat wire with width larges than 0.15, must be 0.06";
		m6_fat_wire_1 = wide(m6,distance >= 0.15);
		m6_not_fat = not(m6,m6_fat_wire_1);
		m6_thin_w_int = interacting_edge(m6_not_fat,m6_fat_wire_1);
		adjacent_edge(m6_thin_w_int,length < 0.06, angle1 > 30, angle2 >30, adjacent_length1 > 0, adjacent_length2 <= 0.1); 
	}

	{	
		@"M6.W.2.2: Minimum width of thin wire with length less than 0.17, connected to fat wire with width larges than 0.3, must be 0.07";
		m6_fat_wire_2 = wide(m6,distance >= 0.3);
		m6_not_fat_2 = not(m6,m6_fat_wire_2);
		m6_thin_w_int_2 = interacting_edge(m6_not_fat_2,m6_fat_wire_2);
		adjacent_edge(m6_thin_w_int_2,length < 0.07, angle1 > 1, angle2 >1, adjacent_length1 > 0, adjacent_length2 <= 0.17); 
	}	
	{	
		@"M6.W.2.3: Minimum width of thin wire with length less than 0.7, connected to fat wire with width larges than 1.5, must be 0.15";
		m6_fat_wire_3 = wide(m6,distance >= 1.5);
		m6_not_fat_3 = not(m6,m6_fat_wire_3);
		m6_thin_w_int_3 = interacting_edge(m6_not_fat_3,m6_fat_wire_3);
		adjacent_edge(m6_thin_w_int_3,length < 0.15, angle1 > 3, angle2 >3, adjacent_length1 > 0, adjacent_length2 <= 0.7); 
	}
	{	
		@"M6.W.2.4: Minimum width of thin wire with length less than 1.5, connected to fat wire with width larges than 3, must be 0.3";
		m6_fat_wire_4 = wide(m6,distance >= 3);
		m6_not_fat_4 = not(m6,m6_fat_wire_4);
		m6_thin_w_int_4 = interacting_edge(m6_not_fat_4,m6_fat_wire_4);
		adjacent_edge(m6_thin_w_int_4,length < 0.3, angle1 > 3, angle2 >3, adjacent_length1 > 0, adjacent_length2 <= 1.5); 
	}	
	
	



//********************************************   M7 Rules **********************************************************
 

	{
		@ "M7.W.1: Minimum M7 width must be 0.056";
		internal1 ( m7 , distance < 0.056 ,extension = RADIAL, relational = POINT_TOUCH );
	}
	{
		@ "M7.W.2: Maximum M7 width must be 5";
		wide (m7,distance>5);
	}

	{
		@ "M7.S.1: Minimum M7 spacing must be 0.056";
		external1 ( m7 , distance < 0.056 ,extension = RADIAL, relational = POINT_TOUCH);
	}
    
    m7_w_015 =wide(m7, distance >= 0.15);
    m7_w_03 =wide(m7, distance >= 0.3);	
    m7_w_15 = wide(m7, distance >= 1.5);	
    m7_w_3 =wide(m7, distance >= 3);
  
    	
	{
	    	@ "M7.S.3.1: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.064";
	   	external2(m7_w_015,m7,distance < 0.064, extension = NONE,projection_length >= 0.15, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	   	@ "M7.S.3.2: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.11";
	   	external2(m7_w_03,m7,distance < 0.11, extension = NONE,projection_length >= 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	  	@ "M7.S.3.3: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.6";
	   	external2(m7_w_15,m7,distance < 0.6, extension = NONE,projection_length >= 1.5, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	   	@ "M7.S.3.4: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.7";
	    	external2(m7_w_3,m7,distance < 0.7, extension = NONE,projection_length >= 3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

    m7_s_01_h = not(m7, internal1(m7,distance < 0.1,extension = NONE, direction = HORIZONTAL));
    m7_s_01_v = not(m7, internal1(m7,distance < 0.1,extension = NONE, direction = VERTICAL));
    m7_s_03_h = not(m7, internal1(m7,distance < 0.3,extension = NONE, direction = HORIZONTAL));
    m7_s_03_v = not(m7, internal1(m7,distance < 0.3,extension = NONE, direction = VERTICAL));

	{
	   	@ "M7.S.6: Minimum spacing of M7 with span > 0.1 with parallel run length > 0.2 must be 0.12";
	    	external1(m7_s_01_v, distance < 0.12, extension = NONE,direction = VERTICAL,projection_length > 0.2, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M7.S.6_1: Minimum spacing of M7 with span > 0.1 with parallel run length > 0.2 must be 0.12";
	    	external1(m7_s_01_h, distance < 0.12, extension = NONE,direction = HORIZONTAL,projection_length > 0.2, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M7.S.7: Minimum spacing of M7 with span > 0.3 with parallel run length > 0.3 must be 0.14";
	    	external1(m7_s_03_v, distance < 0.14, extension = NONE,direction = VERTICAL,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M7.S.7_1: Minimum spacing of M7 with span > 0.3 with parallel run length > 0.3 must be 0.14";
	   	external1(m7_s_03_h, distance < 0.14, extension = NONE,direction = HORIZONTAL,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	

	{
		@ "M7.S.8: Minimum spacing to neighboring  VIAx must be 0.08";
		external2 ( m7, via7, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
	}
	
	{
		@ "M7.S.8_1: Minimum spacing to neighboring VIAx must be 0.08";
		external2 ( m7, via6, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
	}
	{	
		@ "M7.A.1  M7 minimum area must be 0.016";
		area ( m7 , value < 0.016 );
	}
    m7_hole = donut_holes (m7, INNER, area > 0.2);
	{
	    	@ "M7.A.2: M7 minimum enclosed area must be 0.2";
	    	not( donut_holes(m7, INNER), m7_hole);
		
	}

		m7wide = size ( m7 , -0.075 ); 
		m7wide = size ( m7wide , 0.075);

	{
		@ "M7.S.2: Minimum spacing when either metal line is wider than 0.15 must be 0.06";
		external2 ( m7 , m7wide , distance < 0.06 ,extension=RADIAL,look_thru = COINCIDENT , intersecting = TOUCH );
	}

	{	
		@"M7.W.2.1: Minimum width of thin wire with length less than 0.1, connected to fat wire with width larges than 0.15, must be 0.06";
		m7_fat_wire_1 = wide(m7,distance >= 0.15);
		m7_not_fat = not(m7,m7_fat_wire_1);
		m7_thin_w_int = interacting_edge(m7_not_fat,m7_fat_wire_1);
		adjacent_edge(m7_thin_w_int,length < 0.06, angle1 > 30, angle2 >30, adjacent_length1 > 0, adjacent_length2 <= 0.1); 
	}

	{	
		@"M7.W.2.2: Minimum width of thin wire with length less than 0.17, connected to fat wire with width larges than 0.3, must be 0.07";
		m7_fat_wire_2 = wide(m7,distance >= 0.3);
		m7_not_fat_2 = not(m7,m7_fat_wire_2);
		m7_thin_w_int_2 = interacting_edge(m7_not_fat_2,m7_fat_wire_2);
		adjacent_edge(m7_thin_w_int_2,length < 0.07, angle1 > 1, angle2 >1, adjacent_length1 > 0, adjacent_length2 <= 0.17); 
	}	
	{	
		@"M7.W.2.3: Minimum width of thin wire with length less than 0.7, connected to fat wire with width larges than 1.5, must be 0.15";
		m7_fat_wire_3 = wide(m7,distance >= 1.5);
		m7_not_fat_3 = not(m7,m7_fat_wire_3);
		m7_thin_w_int_3 = interacting_edge(m7_not_fat_3,m7_fat_wire_3);
		adjacent_edge(m7_thin_w_int_3,length < 0.15, angle1 > 3, angle2 >3, adjacent_length1 > 0, adjacent_length2 <= 0.7); 
	}
	{	
		@"M7.W.2.4: Minimum width of thin wire with length less than 1.5, connected to fat wire with width larges than 3, must be 0.3";
		m7_fat_wire_4 = wide(m7,distance >= 3);
		m7_not_fat_4 = not(m7,m7_fat_wire_4);
		m7_thin_w_int_4 = interacting_edge(m7_not_fat_4,m7_fat_wire_4);
		adjacent_edge(m7_thin_w_int_4,length < 0.3, angle1 > 3, angle2 >3, adjacent_length1 > 0, adjacent_length2 <= 1.5); 
	}	
	


//********************************************   M8 Rules **********************************************************
 

	{
		@ "M8.W.1: Minimum M8 width must be 0.056";
		internal1 ( m8 , distance < 0.056 ,extension = RADIAL, relational = POINT_TOUCH );
	}
	{
		@ "M8.W.2: Maximum M8 width must be 5";
		wide (m8,distance>5);
	}

	{
		@ "M8.S.1: Minimum M8 spacing must be 0.056";
		external1 ( m8 , distance < 0.056 ,extension = RADIAL, relational = POINT_TOUCH);
	}
    
    m8_w_015 =wide(m8, distance >= 0.15);
    m8_w_03 =wide(m8, distance >= 0.3);	
    m8_w_15 = wide(m8, distance >= 1.5);	
    m8_w_3 =wide(m8, distance >= 3);
  
    	
	{
	   	@ "M8.S.3.1: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.064";
	    	external2(m8_w_015,m8,distance < 0.064, extension = NONE,projection_length >= 0.15, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M8.S.3.2: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.11";
	   	external2(m8_w_03,m8,distance < 0.11, extension = NONE,projection_length >= 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M8.S.3.3: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.6";
	    	external2(m8_w_15,m8,distance < 0.6, extension = NONE,projection_length >= 1.5, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M8.S.3.4: Minimum spacing depending on metal width of one of lines and their parallel run length must be 0.7";
	    	external2(m8_w_3,m8,distance < 0.7, extension = NONE,projection_length >= 3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

    m8_s_01_h = not(m8, internal1(m8,distance < 0.1,extension = NONE, direction = HORIZONTAL));
    m8_s_01_v = not(m8, internal1(m8,distance < 0.1,extension = NONE, direction = VERTICAL));
    m8_s_03_h = not(m8, internal1(m8,distance < 0.3,extension = NONE, direction = HORIZONTAL));
    m8_s_03_v = not(m8, internal1(m8,distance < 0.3,extension = NONE, direction = VERTICAL));

	{
	    	@ "M8.S.6: Minimum spacing of M8 with span > 0.1 with parallel run length > 0.2 must be 0.12";
	    	external1(m8_s_01_v, distance < 0.12, extension = NONE,direction = VERTICAL,projection_length > 0.2, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
		@ "M8.S.6_1: Minimum spacing of M8 with span > 0.1 with parallel run length > 0.2 must be 0.12";
	    	external1(m8_s_01_h, distance < 0.12, extension = NONE,direction = HORIZONTAL,projection_length > 0.2, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	
	
	{
	    	@ "M8.S.7: Minimum spacing of M8 with span > 0.3 with parallel run length > 0.3 must be 0.14";
	    	external1(m8_s_03_v, distance < 0.14, extension = NONE,direction = VERTICAL,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	
	{
	    	@ "M8.S.7_1: Minimum spacing of M8 with span > 0.3 with parallel run length > 0.3 must be 0.14";
	    	external1(m8_s_03_h, distance < 0.14, extension = NONE,direction = HORIZONTAL,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	
/*
	{
		@ "M8.S.8: Minimum spacing to neighboring  VIAx must be 0.08";
		external2 ( m8, via8, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
	}
	
	{
		@ "M8.S.8_1: Minimum spacing to neighboring VIAx must be 0.08";
		external2 ( m8, via7, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
	}
*/

	{	
		@ "M8.A.1  M8 minimum area must be 0.016";
		area ( m8 , value < 0.016 );
	}
    m8_hole = donut_holes (m8, INNER, area > 0.2);
	{
	    	@ "M8.A.2: M8 minimum enclosed area must be 0.2";
	   	not( donut_holes(m8, INNER), m8_hole);
		
	}

		m8wide = size ( m8 , -0.075 ); 
		m8wide = size ( m8wide , 0.075);

	{
		@ "M8.S.2: Minimum spacing when either metal line is wider than 0.15 must be 0.06";
		external2 ( m8 , m8wide , distance < 0.06 ,extension=RADIAL,look_thru = COINCIDENT , intersecting = TOUCH );
	}


	{	
		@"M8.W.2.1: Minimum width of thin wire with length less than 0.1, connected to fat wire with width larges than 0.15, must be 0.06";
		m8_fat_wire_1 = wide(m8,distance >= 0.15);
		m8_not_fat = not(m8,m8_fat_wire_1);
		m8_thin_w_int = interacting_edge(m8_not_fat,m8_fat_wire_1);
		adjacent_edge(m8_thin_w_int,length < 0.06, angle1 > 30, angle2 >30, adjacent_length1 > 0, adjacent_length2 <= 0.1); 
	}

	{	
		@"M8.W.2.2: Minimum width of thin wire with length less than 0.17, connected to fat wire with width larges than 0.3, must be 0.07";
		m8_fat_wire_2 = wide(m8,distance >= 0.3);
		m8_not_fat_2 = not(m8,m8_fat_wire_2);
		m8_thin_w_int_2 = interacting_edge(m8_not_fat_2,m8_fat_wire_2);
		adjacent_edge(m8_thin_w_int_2,length < 0.07, angle1 > 1, angle2 >1, adjacent_length1 > 0, adjacent_length2 <= 0.17); 
	}	
	{	
		@"M8.W.2.3: Minimum width of thin wire with length less than 0.7, connected to fat wire with width larges than 1.5, must be 0.15";
		m8_fat_wire_3 = wide(m8,distance >= 1.5);
		m8_not_fat_3 = not(m8,m8_fat_wire_3);
		m8_thin_w_int_3 = interacting_edge(m8_not_fat_3,m8_fat_wire_3);
		adjacent_edge(m8_thin_w_int_3,length < 0.15, angle1 > 3, angle2 >3, adjacent_length1 > 0, adjacent_length2 <= 0.7); 
	}
	{	
		@"M8.W.2.4: Minimum width of thin wire with length less than 1.5, connected to fat wire with width larges than 3, must be 0.3";
		m8_fat_wire_4 = wide(m8,distance >= 3);
		m8_not_fat_4 = not(m8,m8_fat_wire_4);
		m8_thin_w_int_4 = interacting_edge(m8_not_fat_4,m8_fat_wire_4);
		adjacent_edge(m8_thin_w_int_4,length < 0.3, angle1 > 3, angle2 >3, adjacent_length1 > 0, adjacent_length2 <= 1.5); 
	}	
		
	

//*******************************************   MT RULES  ***************************************************************************

	{
		@ "MT.W.1: Minimum MT width must be 0.16";
		internal1 ( mt, distance < 0.16 ,extension = RADIAL, relational = POINT_TOUCH );
	}
	{
		@ "MT.W.2: Maximum MT width must be 10";
		wide (mt,distance>10);
	}

	{
		@ "MT.S.1: Minimum MT spacing must be 0.16";
		external1 ( mt, distance < 0.16 ,extension = RADIAL, relational = POINT_TOUCH);
	}

	{	
		@ "MT.A.1  MT minimum area must be 0.055";
		area ( mt, value < 0.055 );
	}
    mt_hole = donut_holes (mt, INNER, area > 0.2);
	{
	    	@ "MT.A.2: MT minimum enclosed area must be 0.2";
	    	not( donut_holes(mt, INNER), mt_hole);
		
	}

		mtwide = size ( mt , -0.25 ); 
		mtwide = size ( mtwide , 0.25);

	{
		@ "R.MT.S.2: Minimum spacing when either metal line is wider than 0.15 must be 0.18";
		external2 ( mt , mtwide , distance < 0.18 ,extension=NONE,look_thru = COINCIDENT ,  orientation = PARALLEL, intersecting = TOUCH, projection = IN, orthogonal = ALL, projection_length > 0.5 );
	}
	
     mtwide1 = wide(mt, distance > 1.7);	
	{
		@ "R.MT.S.3: Minimum spacing when either metal line is wider than 1.7 must be 0.5";
		external2 ( mt, mtwide1,distance < 0.5,extension=NONE,look_thru = COINCIDENT , intersecting = TOUCH, orientation = PARALLEL,  projection = IN, orthogonal = ALL, projection_length > 1.7 );
	}
	
    mt_s_01_h = not(mt, internal1(mt,distance < 0.3,extension = NONE, direction = HORIZONTAL));
    mt_s_01_v = not(mt, internal1(mt,distance < 0.3,extension = NONE, direction = VERTICAL));
    mt_s_03_h = not(mt, internal1(mt,distance < 0.7,extension = NONE, direction = HORIZONTAL));
    mt_s_03_v = not(mt, internal1(mt,distance < 0.7,extension = NONE, direction = VERTICAL));

	{
	    	@ "MT.S.4: Minimum spacing of MT with span > 0.3 with parallel run length > 0.4 must be 0.2";
	    	external1(mt_s_01_v, distance < 0.2, extension = NONE,direction = VERTICAL,projection_length > 0.4, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "MT.S.4_1: Minimum spacing of MT with span > 0.3 with parallel run length > 0.4 must be 0.2";
	    	external1(mt_s_01_h, distance < 0.2, extension = NONE,direction = HORIZONTAL,projection_length > 0.4, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	
	{
	  	@ "MT.S.5: Minimum spacing of MT with span > 0.7 with parallel run length > 0.7 must be 0.24";
	    	external1(mt_s_03_v, distance < 0.24, extension = NONE,direction = VERTICAL,projection_length > 0.7, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	
	{
	 	@ "MT.S.5_1: Minimum spacing of MT with span > 0.7 with parallel run length > 0.7 must be 0.24";
	    	external1(mt_s_03_h, distance < 0.24, extension = NONE,direction = HORIZONTAL,projection_length > 0.7, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	

	

//************************************ CO RULES *****************************/

	{
		@ "CO.W.1: Exact contact size must be 0.042";
		not_rectangles ( co ,sides= {0.042,0.042} );
	}

	{
		@ "CO.S.1: Minimum contact spacing must be 0.05";
		external1 ( co , distance < 0.05 , extension=RADIAL, relational = POINT_TOUCH );
	}
	co_s_2 = connect ( 		
		    {
		    {{po,m1},co},
		    {{m1,m2},via1},
		    {{m2,m3},via2},
		    {{m3,m4},via3},
		    {{m4,m5},via4},
		    {{m5,m6},via6},
		    {{m6,m7},via7},
		    {{m7,m8},via8},
		    {{m8,mt},viat}
		    }
	);
	{
		@ "CO.S.2: Minimum contact spacing to contact on different net must be 0.055";
		external1 ( co , distance < 0.055 , extension=NONE, relational = POINT_TOUCH ,connectivity = DIFFERENT_NET,connect_sequence = co_s_2 );
	}
 	if( RECOMMENDED == 1 ) {
	{
		@ "R.CO.S.2: Minimum contact center to center spacing must be 0.92";
		center_to_center1 (co, distance < 0.92);
	}}

	{
		@ "CO.S.3: (Contact inside DIFF) Minimum space to gate must be 0.04";
		external2 ( cood, gate ,distance < 0.04,extension=RADIAL,look_thru = COINCIDENT , relational = OVERLAP , intersecting = TOUCH);
	}
	
    gate_1 = not ( gate, (internal1(gate, extension = NONE, distance < 0.1)));
	{
		@ "CO.S.7: (Contact inside DIFF) Minimum space to gate (if gate width >=0.1) must be 0.07";
		external2 ( cood, gate_1, distance < 0.07, extension = RADIAL, look_thru = COINCIDENT, relational = OVERLAP, intersecting = TOUCH);	
	}
	
	{
		@ "CO.S.4: (Contact inside Poly) Min. space to Active must be 0.04";
		external2 ( copo  , diff , distance < 0.04 , extension=RADIAL,look_thru = COINCIDENT , relational = OVERLAP , intersecting = TOUCH);
	}
	{
		@ "CO.S.5: (Contact inside DIFF) Minimum space to PO inner vertex must be 0.068";
		external_corner2 ( cood, po, distance < 0.068, type = {CONVEX_TO_CONCAVE});
	}
	{
		@ "CO.S.6: (Contact inside POLY) Minimum space to DIFF inner vertex must be 0.07";
		external_corner2 (copo, diff, distance < 0.07, type = {CONVEX_TO_CONCAVE});
	}
	
    gate_1 = (internal1(gate, extension = NONE, distance < 0.1));
    co_008 = external2 (co, gate_1, distance < 0.07, extension = NONE, direction = HORIZONTAL);
	{
		@"CO.S.3: Co exact space to gate must be 0.04";
		not (co_008, ((external2 (co, gate_1, distance == 0.04, extension = NONE, direction = HORIZONTAL)) or ( external2 ( co, gate_1, distance == 0.07, extension = NONE, direction = HORIZONTAL))));
	}
			
    po_0042 = internal1 (po, distance < 0.042, extension = RADIAL);
    po_2 = not(po, po_1);
    po_01 = wide (po, distance > 0.1);
    po_0042_01 = not (po, ((po_01) or( po_0042) ));

        
        
        {
    	  	@"CO.E.1: Minimum enclosure by poly, if PO width < 0.042 must be -0.006";
    	  	po_int_co= interacting(po_0042,co);
    		po_size = size(po_int_co, 0.006);
    	    	enclose (co, po_size, < 0, relational = {INSIDE},extension = RADIAL);  
    	    
        }
	{
		@ "CO.E.2: Minimum enclosure of co by poly, if PO 0.042 <= width <=0.1 must be 0";
		enclose(  co, po_0042_01, < 0 , relational = {INSIDE}, extension=RADIAL) ;
	}

	{
		@ "CO.E.3: Minimum enclosure of co by poly, if PO  width > 0.1 must be 0.02";
		enclose(  co, po_01, < 0.02 , relational = {INSIDE}, extension=NONE) ;
	}
	co1 = interacting(co, not(po,po_01));
	{
		@ "CO.E.4: Minimum enclose by poly, at least two opposite sides if PO width <=0.1 must be 0.034";
		not_covered_by (co1, (not(po,po_01)), distances = {{{0.034,INTERSECTION},{0},{0.034,INTERSECTION},{0}}}, not_inside = IGNORE);
	}

  co2 = interacting (co, po_01);
	{
		@ "CO.E.5: Minimum enclose by poly, at least two opposite sides if PO width > 0.1 must be 0.05";
		not_covered_by (co2,  po_01, distances = {{{0.05,INTERSECTION},{0},{0.05,INTERSECTION},{0}}}, not_inside = IGNORE);
	}
			
	{
		@ "CO.E.6: Minimum enclosure by DIFF must be 0.01";
		enclose ( cood , diff , distance < 0.01 , extension=RADIAL,  intersecting = TOUCH, relational = {POINT_TOUCH, INSIDE, OUTSIDE}, relational_type =  POLYGON);
	}


	coindiff = co inside diff;
	
	co_e_7 = not_covered_by(cood, diff,distances = {{{0.02},{0.0},{0.02},{0.0}},{{0.0},{0.02},{0.0},{0.02}}});
	co_e_12 = not_covered_by(cood, diff,distances = {{{0.015},{0.015},{0.015},{0.015}}});
	{
	@"CO.E.7/CO.E.12: Min enclosure of contact by DIFF at all sides must be 0.015 or at least two opposite sides must be 0.02 ";
	and(co_e_7,co_e_12);
	}
	
	ptapco = ptap and co;
	ntapco = ptap and co;
	
	{
		@ "CO.E.8: Minimum butted diffusion PIMP enclosure of S/D contact 0.025um";
		enclose(ptapco,pimp,distance < 0.025,extension = RADIAL , intersecting = {TOUCH} , relational = {POINT_TOUCH});
	}


	{
	       	@ "CO.E.8_1: Minimum butted diffusion NIMP enclosure of S/D contact 0.025um";
		enclose(ntapco,nimp,distance < 0.025,extension = RADIAL,intersecting = {TOUCH},relational = {POINT_TOUCH});
	}


	{
		@ "CO.E.12: CONT is not enclosed by M1";
		not ( co , m1 );
	}

	{	
		@ "CO.E.9: Minimum enclosure of any contact by M1 must be 0.002um";
		enclose ( co , m1 , distance < 0.002 , extension = NONE , intersecting = {TOUCH});
	}

	co_m1 = co inside m1;

	{
	        @ "CO.E.10: Min enclosure of contact at end of line must be 0.02";
	            not_covered_by(co_m1,m1,distances = {{{0.0},{0.02},{0.0},{0.02}},
					 {{0.02},{0.0},{0.02},{0.0}}},
					 intersecting = {TOUCH});
	}
	co_po = co inside po;

	{
	        @ "CO.E.11: Min enclosure of contact by PO at two opposite sides (if one side = 0, opposite >=0.01) must be 0.016";
	            not_covered_by(co_po,po,distances = {{{0.0},{0.016},{0.01},{0.016}},
					 {{0.016},{0.0},{0.016},{0.01}}},
					 intersecting = {TOUCH});
	}



	{
		@"CO.S.5: Minimum space to DIFF outer vertex must be 0.018";
		enclose_corner(cood, diff, distance < 0.018, type = CONVEX_TO_CONVEX);
	}
	po_over_cob1 = size (po, distance = 0.006);
	co_b_1 =  or(po_over_cob1,m1);
	{
		@"CO.B.1: CO must be fully covered by M1, and by PO widened by 0.006";
		not(co,co_b_1);
	}
	{
		@"CO.B.2: It is not allowed to place CO on gate";
		and(co,gate);
	}
 	if( RECOMMENDED == 1 ) {
	co_b_3 = and(m1,diff);
	{
		@"R.CO.B.3: All M1/DIFF intersections that have a CO shape, must have more than 2 COs";
		interacting (co_b_3, co, count <= 2);
	}

	co_b_4 = and(m1,po);
	{
		@"R.CO.B.4: All M1/PO intersections that have a CO shape, must have more than 2 COs";
		interacting (co_b_4, co, count <= 2);
	}}

	
//***************************************      VIA1 RULES     *****************************/
    via1sq  = rectangles (via1, {0.05,0.05});
    via1lg  = rectangles (via1, {0.10,0.10});
    via1bar = rectangles (via1, {0.05,0.10});
{
	@ "VIA1.W: VIA1 must be square with 0.05 or 0.10 width and length or VIA1 must be rectangular with length 0.10 and width 0.05";
	not(via1,(via1sq or via1lg or via1bar));
}

{
	@ "VIA1.S.1: Minimum  spacing of VIA1SQ to VIA1SQ must be 0.07";
	external1 ( via1sq , distance < 0.07 ,  extension=RADIAL,relational = POINT_TOUCH  );	
}
{
	@ "VIA1.S.2: Minimum spacing of VIA1SQ to VIABAR must be 0.08";
	external2 (via1sq, via1bar, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "VIA1.S.2_1: Minimum spacing of VIA1SQ to VIA1LG must be 0.08 ";
	external2(via1sq, via1lg, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "VIA1.S.3: Minimum spacing of VIA1BAR or VIA1LG to VIA1BAR or VIA1LG must be 0.085";
	external1(via1bar, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "VIA1.S.3_1: Minimum spacing of VIA1BAR or VIA1LG to VIA1BAR or VIA1LG must be 0.085";
	external1(via1lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "VIA1.S.3_2: Minimum spacing of VIA1BAR or VIA1LG to VIA1BAR or VIA1LG must be 0.085";
	external2(via1bar,via1lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}



{
	@ "VIA1.E.1: Minimum VIA1 enclosure by M1 and M2 must be  0.005";
	enclose ( via1 , m1 , distance < 0.005 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
	enclose ( via1 , m2 , distance < 0.005 , extension=RADIAL, intersecting = TOUCH , relational = POINT_TOUCH );
}
	
{
	@ "VIA1.B.2: VIA1 must be covered by M1 and M2, min. enclosure is 0.005um";
	not ( via1 , m1 );
	not ( via1 , m2 );
}

{
	@ "R.VIA1.E.3: Minimum VIA1BAR enclosure by M1 and M2 at end-of-line must be 0.005";


	not_covered_by(via1bar,m1,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});

	
	not_covered_by(via1bar,m2,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});


}

	via1_e_2_m1 = not_covered_by (via1, m1, distances ={{{0.005},{0.03},{0.005},{0.03}}});
	via1_e_2_m2 = not_covered_by (via1, m2, distances = {{{0.005},{0.03},{0.005},{0.03}}});
	via1_e_2 = or(via1_e_2_m1,via1_e_2_m2);

	via1_e_4_m1 = not_covered_by (via1, m1, distances ={{{0.005},{0.012},{0.012},{0.012}}});
	via1_e_4_m2 = not_covered_by (via1, m2, distances ={{{0.005},{0.012},{0.012},{0.012}}});
	via1_e_4 = or(via1_e_4_m1,via1_e_4_m2);

	via1_e_2_4 = and(via1_e_2,via1_e_4);
{
	@ "VIA1.E.2/VIA1.E.4: Minimum VIA1 enclosure by M1 and M2 at least two opposite sides if other two sides >= 0.005 must be 0.03, or must be 0.012 if one side is >=0.005";
	copy(via1_e_2_4);
	
}

m1_v = wide (m1, > 0.2);
m2_v = wide (m2, > 0.2);

m1_w_01 = interacting(m1_v,via1);
m2_w_01 = interacting(m2_v,via1);



r2 = external1 (via1sq, <= 0.15, extension = RADIAL);
r2_e = interacting (r2,via1sq,count > 1);
r2_v =interacting (via1sq, r2_e);

r3 =external1 (via1lg, <= 0.15, extension = RADIAL);
r3_e =interacting(r3,via1lg,count > 1);
r3_v =interacting (via1lg, r3_e);

r4 = external1 (via1sq, <= 0.7,  extension = RADIAL);
r4_or = or(r4, via1sq);
r4_e = interacting (r4_or,via1sq,count>3);
r4_v = interacting ( via1sq,r4_e);
r5   = external1 (via1lg, <= 0.7,  extension = RADIAL);
r5_or = or(r5,via1lg);
r5_e = interacting (r5_or, via1lg,count >3);
r5_v = interacting (via1lg, r5_e);
{
	@ "VIA1.B.1: When Mx or MX+1 width > 0.2, it is a must to have redundant VIAs (At least one rectangular VIAx, At least two  square VIAx with spacing <=0.15umn,At least four square VIAx with spacing <=0.7um)";
	not(m1_w_01,((interacting (m1_w_01, via1bar, count >= 1)) or (interacting (m1_w_01, r2_v, count >= 2)) or (interacting(m1_w_01,r3_v, count >=2 )) or (interacting(m1_w_01,r4_v, count >= 4)) or (interacting(m1_w_01,r5_v, count >= 4))));
}	

		       
//***************************************      VIA2 RULES     *****************************/
    via2sq  = rectangles (via2, {0.05,0.05});
    via2lg  = rectangles (via2, {0.10,0.10});
    via2bar = rectangles (via2, {0.05,0.10});
{
	@ "R.VIA2.W: VIA2 must be square with 0.05 or 0.10 width and length or VIA2 must be rectangular with length 0.10 and width 0.05";
	not(via2,(via2sq or via2lg or via2bar));
}

{
	@ "R.VIA2.S.1: Minimum  spacing of VIA2SQ to VIA2SQ must be 0.07";
	external1 ( via2sq , distance < 0.07 ,  extension=RADIAL,relational = POINT_TOUCH  );	
}
{
	@ "R.VIA2.S.2: Minimum spacing of VIA2SQ to VIA2BAR must be 0.08";
	external2 (via2sq, via2bar, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA2.S.2: Minimum spacing of VIA2SQ to VIA2LG must be 0.08 ";
	external2(via2sq, via2lg, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA2.S.3: Minimum spacing of VIA2BAR or VIA2LG to VIA2BAR or VIA2LG must be 0.085";
	external1(via2bar, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA2.S.3: Minimum spacing of VIA2BAR or VIA2LG to VIA2BAR or VIA2LG must be 0.085";
	external1(via2lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA2.S.3: Minimum spacing of VIA2BAR or VIA2LG to VIA2BAR or VIA2LG must be 0.085";
	external2(via2bar,via2lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}



{
	@ "R.VIA2.E.1: Minimum VIA2 enclosure by M2 and M3 must be  0.005";
	enclose ( via2 , m2 , distance < 0.005 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
	enclose ( via2 , m3 , distance < 0.005 , extension=RADIAL, intersecting = TOUCH , relational = POINT_TOUCH );
}
	
{
	@ "R.VIA2.E.1: VIA2 must be covered by M2 and M3, min. enclosure is 0.005um";
	not ( via2 , m2 );
	not ( via2 , m3 );
}

{
	@ "R.VIA2.E.3: Minimum VIA2BAR enclosure by M2 and M3 at end-of-line must be 0.005";


	not_covered_by(via2bar,m2,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});

	
	not_covered_by(via2bar,m3,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});


}

	via2_e_2_m1 = not_covered_by (via2, m2, distances ={{{0.005},{0.03},{0.005},{0.03}}});
	via2_e_2_m2 = not_covered_by (via2, m3, distances = {{{0.005},{0.03},{0.005},{0.03}}});
	via2_e_2 = or(via2_e_2_m1,via2_e_2_m2);

	via2_e_4_m1 = not_covered_by (via2, m2, distances ={{{0.005},{0.012},{0.012},{0.012}}});
	via2_e_4_m2 = not_covered_by (via2, m3, distances ={{{0.005},{0.012},{0.012},{0.012}}});
	via2_e_4 = or(via2_e_4_m1,via2_e_4_m2);

	via2_e_2_4 = and(via2_e_2,via2_e_4);
{
	@ "VIA2.E.2/VIA2.E.4: Minimum VIA2 enclosure by M2 and M3 at least two opposite sides if other two sides >= 0.005 must be 0.03, or must be 0.012 if one side is >=0.005";
	copy(via2_e_2_4);
	
}
m1_v_1 = interacting(m2,via2);
m2_v_1 = interacting(m3,via2);
m1_w_02 = wide (m1_v_1, > 0.2);
m2_w_02 = wide (m2_v_1, > 0.2);


r22 = external1 (via2sq, <= 0.15, extension = RADIAL);
r22_e = interacting (r22,via2sq,count > 1);
r22_v =interacting (via2sq, r22_e);

r32 =external1 (via2lg, <= 0.15, extension = RADIAL);
r32_e =interacting(r32,via2lg,count > 1);
r32_v =interacting (via2lg, r32_e);

r42 = external1 (via2sq, <= 0.7,  extension = RADIAL);
r42_or = or(r42, via2sq);
r42_e = interacting (r42_or,via2sq,count>3);
r42_v = interacting ( via2sq,r42_e);
r52   = external1 (via2lg, <= 0.7,  extension = RADIAL);
r52_or = or(r52,via2lg);
r52_e = interacting (r52_or, via2lg,count >3);
r52_v = interacting (via2lg, r52_e);
{
	@ "VIA2.B.1: When Mx or MX+1 width > 0.2, it is a must to have redundant VIAs (At least one rectangular VIAx, At least two  square VIAx with spacing <=0.15umn,At least four square VIAx with spacing <=0.7um)";
	not(m1_w_02,((interacting (m1_w_02, via2bar, count >= 1)) or (interacting (m1_w_02, r22_v, count >= 2)) or (interacting(m1_w_02,r32_v, count >=2 )) or (interacting(m1_w_02,r42_v, count >= 4)) or (interacting(m1_w_02,r52_v, count >= 4))));
}	



//***************************************      VIA3 RULES     *****************************/
    via3sq  = rectangles (via3, {0.05,0.05});
    via3lg  = rectangles (via3, {0.10,0.10});
    via3bar = rectangles (via3, {0.05,0.10});
{
	@ "R.VIA3.W: VIA3 must be square with 0.05 or 0.10 width and length or VIA3 must be rectangular with length 0.10 and width 0.05";
	not(via3,(via3sq or via3lg or via3bar));
}

{
	@ "R.VIA3.S.1: Minimum  spacing of VIA3SQ to VIA3SQ must be 0.07";
	external1 ( via3sq , distance < 0.07 ,  extension=RADIAL,relational = POINT_TOUCH  );	
}
{
	@ "R.VIA3.S.2: Minimum spacing of VIA3SQ to VIA3BAR must be 0.08";
	external2 (via3sq, via3bar, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA3.S.2: Minimum spacing of VIA3SQ to VIA3LG must be 0.08 ";
	external2(via3sq, via3lg, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA3.S.3: Minimum spacing of VIA3BAR or VIA3LG to VIA3BAR or VIA3LG must be 0.085";
	external1(via3bar, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA3.S.3: Minimum spacing of VIA3BAR or VIA3LG to VIA3BAR or VIA3LG must be 0.085";
	external1(via3lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA3.S.3: Minimum spacing of VIA3BAR or VIA3LG to VIA3BAR or VIA3LG must be 0.085";
	external2(via3bar,via3lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}



{
	@ "R.VIA3.E.1: Minimum VIA3 enclosure by M4 and M3 must be  0.005";
	enclose ( via3 , m4 , distance < 0.005 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
	enclose ( via3 , m3 , distance < 0.005 , extension=RADIAL, intersecting = TOUCH , relational = POINT_TOUCH );
}
	
{
	@ "R.VIA3.E.1: VIA3 must be covered by M4 and M3, min. enclosure is 0.005um";
	not ( via3 , m4 );
	not ( via3 , m3 );
}

{
	@ "R.VIA3.E.3: Minimum VIA3BAR enclosure by M4 and M3 at end-of-line must be 0.005";


	not_covered_by(via3bar,m3,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});

	
	not_covered_by(via3bar,m4,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});


}

	via3_e_2_m1 = not_covered_by (via3, m3, distances ={{{0.005},{0.03},{0.005},{0.03}}});
	via3_e_2_m2 = not_covered_by (via3, m4, distances = {{{0.005},{0.03},{0.005},{0.03}}});
	via3_e_2 = or(via3_e_2_m1,via3_e_2_m2);

	via3_e_4_m1 = not_covered_by (via3, m3, distances ={{{0.005},{0.012},{0.012},{0.012}}});
	via3_e_4_m2 = not_covered_by (via3, m4, distances ={{{0.005},{0.012},{0.012},{0.012}}});
	via3_e_4 = or(via3_e_4_m1,via3_e_4_m2);

	via3_e_2_4 = and(via3_e_2,via3_e_4);
{
	@ "VIA3.E.2/VIA3.E.4: Minimum VIA3 enclosure by M3 and M4 at least two opposite sides if other two sides >= 0.005 must be 0.03, or must be 0.012 if one side is >=0.005";
	copy(via3_e_2_4);
	
}
m1_v_3 = interacting(m3, via3);
m2_v_3 = interacting(m4, via3);
m1_w_03 = wide (m1_v_3, > 0.2);
m2_w_03 = wide (m2_v_3, > 0.2);


r23 = external1 (via3sq, <= 0.15, extension = RADIAL);
r23_e = interacting (r23,via3sq,count > 1);
r23_v =interacting (via3sq, r23_e);

r33 =external1 (via3lg, <= 0.15, extension = RADIAL);
r33_e =interacting(r33,via3lg,count > 1);
r33_v =interacting (via3lg, r33_e);

r43 = external1 (via3sq, <= 0.7,  extension = RADIAL);
r43_or = or(r43, via3sq);
r43_e = interacting (r43_or,via3sq,count>3);
r43_v = interacting ( via3sq,r43_e);
r53   = external1 (via3lg, <= 0.7,  extension = RADIAL);
r53_or = or(r53,via3lg);
r53_e = interacting (r53_or, via3lg,count >3);
r53_v = interacting (via3lg, r53_e);


{
	@ "VIA3.B.1: When Mx or MX+1 width > 0.2, it is a must to have redundant VIAs (At least one rectangular VIAx, At least two  square VIAx with spacing <=0.15umn,At least four square VIAx with spacing <=0.7um)";
	not(m1_w_03,((interacting (m1_w_03, via3bar, count >= 1)) or (interacting (m1_w_03, r23_v, count >= 2)) or (interacting(m1_w_03,r33_v, count >=2 )) or (interacting(m1_w_03,r43_v, count >= 4)) or (interacting(m1_w_03,r53_v, count >= 4))));
}	


//***************************************      VIA4 RULES     *****************************/
    via4sq  = rectangles (via4, {0.05,0.05});
    via4lg  = rectangles (via4, {0.10,0.10});
    via4bar = rectangles (via4, {0.05,0.10});
{
	@ "R.VIA4.W: VIA4 must be square with 0.05 or 0.10 width and length or VIA4 must be rectangular with length 0.10 and width 0.05";
	not(via4,(via4sq or via4lg or via4bar));
}

{
	@ "R.VIA4.S.1: Minimum  spacing of VIA4SQ to VIA4SQ must be 0.07";
	external1 ( via4sq , distance < 0.07 ,  extension=RADIAL,relational = POINT_TOUCH  );	
}
{
	@ "R.VIA4.S.2: Minimum spacing of VIA4SQ to VIA4BAR must be 0.08";
	external2 (via4sq, via4bar, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA4.S.2: Minimum spacing of VIA4SQ to VIA4LG must be 0.08 ";
	external2(via4sq, via4lg, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA4.S.3: Minimum spacing of VIA4BAR or VIA4LG to VIA4BAR or VIA4LG must be 0.085";
	external1(via4bar, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA4.S.3: Minimum spacing of VIA4BAR or VIA4LG to VIA4BAR or VIA4LG must be 0.085";
	external1(via4lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA4.S.3: Minimum spacing of VIA4BAR or VIA4LG to VIA4BAR or VIA4LG must be 0.085";
	external2(via4bar,via4lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}



{
	@ "R.VIA4.E.1: Minimum VIA4 enclosure by M4 and M5 must be  0.005";
	enclose ( via4 , m5 , distance < 0.005 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
	enclose ( via4 , m4 , distance < 0.005 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
}
	
{
	@ "R.VIA4.E.1: VIA4 must be covered by M5 and M4, min. enclosure is 0.005um";
	not ( via4 , m5 );
	not ( via4 , m4 );
}

{
	@ "R.VIA4.E.3: Minimum VIA4BAR enclosure by M5 and M4 at end-of-line must be 0.005";


	not_covered_by(via4bar,m4,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});

	
	not_covered_by(via4bar,m5,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});


}

	via4_e_2_m1 = not_covered_by (via4, m4, distances ={{{0.005},{0.03},{0.005},{0.03}}});
	via4_e_2_m2 = not_covered_by (via4, m5, distances = {{{0.005},{0.03},{0.005},{0.03}}});
	via4_e_2 = or(via4_e_2_m1,via4_e_2_m2);

	via4_e_4_m1 = not_covered_by (via4, m4, distances ={{{0.005},{0.012},{0.012},{0.012}}});
	via4_e_4_m2 = not_covered_by (via4, m5, distances ={{{0.005},{0.012},{0.012},{0.012}}});
	via4_e_4 = or(via4_e_4_m1,via4_e_4_m2);

	via4_e_2_4 = and(via4_e_2,via4_e_4);
{
	@ "VIA4.E.2/VIA4.E.4: Minimum VIA4 enclosure by M4 and M5 at least two opposite sides if other two sides >= 0.005 must be 0.03, or must be 0.012 if one side is >=0.005";
	copy(via4_e_2_4);
	
}
m1_v_4 = interacting(m4,via4);
m2_v_4 = interacting(m5,via4);
m1_w_04 = wide (m1_v_4, > 0.2);
m2_w_04 = wide (m2_v_4, > 0.2);


r24 = external1 (via4sq, <= 0.15, extension = RADIAL);
r24_e = interacting (r24,via4sq,count > 1);
r24_v =interacting (via4sq, r24_e);

r34 =external1 (via4lg, <= 0.15, extension = RADIAL);
r34_e =interacting(r34,via4lg,count > 1);
r34_v =interacting (via4lg, r34_e);

r44 = external1 (via4sq, <= 0.7,  extension = RADIAL);
r44_or = or(r44, via4sq);
r44_e = interacting (r44_or,via4sq,count>3);
r44_v = interacting ( via4sq,r44_e);
r54   = external1 (via4lg, <= 0.7,  extension = RADIAL);
r54_or = or(r54,via4lg);
r54_e = interacting (r54_or, via4lg,count >3);
r54_v = interacting (via4lg, r54_e);


{
	@ "VIA4.B.1: When Mx or MX+1 width > 0.2, it is a must to have redundant VIAs (At least one rectangular VIAx, At least two  square VIAx with spacing <=0.15umn,At least four square VIAx with spacing <=0.7um)";
	not(m1_w_04,((interacting (m1_w_04, via4bar, count >= 1)) or (interacting (m1_w_04, r24_v, count >= 2)) or (interacting(m1_w_04,r34_v, count >=2 )) or (interacting(m1_w_04,r44_v, count >= 4)) or (interacting(m1_w_04,r54_v, count >= 4))));
}	



//***************************************      VIA5 RULES     *****************************/
    via5sq  = rectangles (via5, {0.05,0.05});
    via5lg  = rectangles (via5, {0.10,0.10});
    via5bar = rectangles (via5, {0.05,0.10});
{
	@ "R.VIA5.W: VIA5 must be square with 0.05 or 0.10 width and length or VIA5 must be rectangular with length 0.10 and width 0.05";
	not(via5,(via5sq or via5lg or via5bar));
}

{
	@ "R.VIA5.S.1: Minimum  spacing of VIA5SQ to VIA5SQ must be 0.07";
	external1 ( via5sq , distance < 0.07 ,  extension=RADIAL,relational = POINT_TOUCH  );	
}
{
	@ "R.VIA5.S.2: Minimum spacing of VIA5SQ to VIA5BAR must be 0.08";
	external2 (via5sq, via5bar, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA5.S.2: Minimum spacing of VIA5SQ to VIA5LG must be 0.08 ";
	external2(via5sq, via5lg, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA5.S.3: Minimum spacing of VIA5BAR or VIA5LG to VIA5BAR or VIA5LG must be 0.085";
	external1(via5bar, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA5.S.3: Minimum spacing of VIA5BAR or VIA5LG to VIA5BAR or VIA5LG must be 0.085";
	external1(via5lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA5.S.3: Minimum spacing of VIA5BAR or VIA5LG to VIA5BAR or VIA5LG must be 0.085";
	external2(via5bar,via5lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}



{
	@ "R.VIA5.E.1: Minimum VIA5 enclosure by M6 and M5 must be  0.005";
	enclose ( via5 , m6 , distance < 0.005 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
	enclose ( via5 , m5 , distance < 0.005 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
}
	
{
	@ "R.VIA5.E.1: VIA5 must be covered by M5 and M6, min. enclosure is 0.005um";
	not ( via5 , m5 );
	not ( via5 , m6 );
}

{
	@ "R.VIA5.E.3: Minimum VIA5BAR enclosure by M5 and M6 at end-of-line must be 0.005";


	not_covered_by(via5bar,m5,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});

	
	not_covered_by(via5bar,m6,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});


}

	via5_e_2_m1 = not_covered_by (via5, m5, distances ={{{0.005},{0.03},{0.005},{0.03}}});
	via5_e_2_m2 = not_covered_by (via5, m6, distances = {{{0.005},{0.03},{0.005},{0.03}}});
	via5_e_2 = or(via5_e_2_m1,via5_e_2_m2);

	via5_e_4_m1 = not_covered_by (via5, m5, distances ={{{0.005},{0.012},{0.012},{0.012}}});
	via5_e_4_m2 = not_covered_by (via5, m6, distances ={{{0.005},{0.012},{0.012},{0.012}}});
	via5_e_4 = or(via5_e_4_m1,via5_e_4_m2);

	via5_e_2_4 = and(via5_e_2,via5_e_4);
{
	@ "VIA5.E.2/VIA5.E.4: Minimum VIA5 enclosure by M5 and M6 at least two opposite sides if other two sides >= 0.005 must be 0.03, or must be 0.012 if one side is >=0.005";
	copy(via5_e_2_4);
	
}

m1_v_5 = interacting(m5,via5);

m2_v_5 = interacting(m6,via5);

m1_w_05 = wide (m1_v_5, > 0.2);
m2_w_05 = wide (m2_v_5, > 0.2);


r25 = external1 (via5sq, <= 0.15, extension = RADIAL);
r25_e = interacting (r25,via5sq,count > 1);
r25_v =interacting (via5sq, r25_e);

r35 =external1 (via5lg, <= 0.15, extension = RADIAL);
r35_e =interacting(r35,via5lg,count > 1);
r35_v =interacting (via5lg, r35_e);

r45 = external1 (via5sq, <= 0.7,  extension = RADIAL);
r45_or = or(r45, via5sq);
r45_e = interacting (r45_or,via5sq,count>3);
r45_v = interacting ( via5sq,r45_e);
r55   = external1 (via5lg, <= 0.7,  extension = RADIAL);
r55_or = or(r55,via5lg);
r55_e = interacting (r55_or, via5lg,count >3);
r55_v = interacting (via5lg, r55_e);


{
	@ "VIA5.B.1: When Mx or MX+1 width > 0.2, it is a must to have redundant VIAs (At least one rectangular VIAx, At least two  square VIAx with spacing <=0.15umn,At least four square VIAx with spacing <=0.7um)";
	not(m1_w_05,((interacting (m1_w_05, via5bar, count >= 1)) or (interacting (m1_w_05, r25_v, count >= 2)) or (interacting(m1_w_05,r35_v, count >=2 )) or (interacting(m1_w_05,r45_v, count >= 4)) or (interacting(m1_w_05,r55_v, count >= 4))));
}	



//***************************************      VIA6 RULES     *****************************/
    via6sq  = rectangles (via6, {0.05,0.05});
    via6lg  = rectangles (via6, {0.10,0.10});
    via6bar = rectangles (via6, {0.05,0.10});
{
	@ "R.VIA6.W: VIA6 must be square with 0.05 or 0.10 width and length or VIA6 must be rectangular with length 0.10 and width 0.05";
	not(via6,(via6sq or via6lg or via6bar));
}

{
	@ "R.VIA6.S.1: Minimum  spacing of VIA6SQ to VIA6SQ must be 0.07";
	external1 ( via6sq , distance < 0.07 ,  extension=RADIAL,relational = POINT_TOUCH  );	
}
{
	@ "R.VIA6.S.2: Minimum spacing of VIA6SQ to VIA6BAR must be 0.08";
	external2 (via6sq, via6bar, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA6.S.2: Minimum spacing of VIA6SQ to VIA6LG must be 0.08 ";
	external2(via6sq, via6lg, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA6.S.3: Minimum spacing of VIA6BAR or VIA6LG to VIA6BAR or VIA6LG must be 0.085";
	external1(via6bar, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA6.S.3: Minimum spacing of VIA6BAR or VIA6LG to VIA6BAR or VIA6LG must be 0.085";
	external1(via6lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA6.S.3: Minimum spacing of VIA6BAR or VIA6LG to VIA6BAR or VIA6LG must be 0.085";
	external2(via6bar,via6lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}



{
	@ "R.VIA6.E.1: Minimum VIA6 enclosure by M6 and M7 must be  0.005";
	enclose ( via6 , m6 , distance < 0.005 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
	enclose ( via6 , m7 , distance < 0.005 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
}
	
{
	@ "R.VIA6.E.1: VIA6 must be covered by M6 and M7, min. enclosure is 0.005um";
	not ( via6 , m6 );
	not ( via6 , m7 );
}

{
	@ "R.VIA6.E.3: Minimum VIA6BAR enclosure by M7 and M6 at end-of-line must be 0.005";


	not_covered_by(via6bar,m7,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});

	
	not_covered_by(via6bar,m6,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});


}

	via6_e_2_m1 = not_covered_by (via6, m6, distances ={{{0.005},{0.03},{0.005},{0.03}}});
	via6_e_2_m2 = not_covered_by (via6, m7, distances = {{{0.005},{0.03},{0.005},{0.03}}});
	via6_e_2 = or(via6_e_2_m1,via6_e_2_m2);

	via6_e_4_m1 = not_covered_by (via6, m6, distances ={{{0.005},{0.012},{0.012},{0.012}}});
	via6_e_4_m2 = not_covered_by (via6, m7, distances ={{{0.005},{0.012},{0.012},{0.012}}});
	via6_e_4 = or(via6_e_4_m1,via6_e_4_m2);

	via6_e_2_4 = and(via6_e_2,via6_e_4);
{
	@ "VIA6.E.2/VIA6.E.4: Minimum VIA6 enclosure by M6 and M7 at least two opposite sides if other two sides >= 0.005 must be 0.03, or must be 0.012 if one side is >=0.005";
	copy(via6_e_2_4);
	
}


m1_v_6 = interacting(m6, via6);
m2_v_6 = interacting(m7, via6);
m1_w_06 = wide (m1_v_6, > 0.2);
m2_w_06 = wide (m2_v_6, > 0.2);


r26 = external1 (via6sq, <= 0.15, extension = RADIAL);
r26_e = interacting (r26,via6sq,count > 1);
r26_v =interacting (via6sq, r26_e);

r36 =external1 (via6lg, <= 0.15, extension = RADIAL);
r36_e =interacting(r36,via6lg,count > 1);
r36_v =interacting (via6lg, r36_e);

r46 = external1 (via6sq, <= 0.7,  extension = RADIAL);
r46_or = or(r46, via6sq);
r46_e = interacting (r46_or,via6sq,count>3);
r46_v = interacting ( via6sq,r46_e);
r56   = external1 (via6lg, <= 0.7,  extension = RADIAL);
r56_or = or(r56,via6lg);
r56_e = interacting (r56_or, via6lg,count >3);
r56_v = interacting (via6lg, r56_e);


{
	@ "VIA6.B.1: When Mx or MX+1 width > 0.2, it is a must to have redundant VIAs (At least one rectangular VIAx, At least two  square VIAx with spacing <=0.15umn,At least four square VIAx with spacing <=0.7um)";
	not(m1_w_06,((interacting (m1_w_06, via6bar, count >= 1)) or (interacting (m1_w_06, r26_v, count >= 2)) or (interacting(m1_w_06,r36_v, count >=2 )) or (interacting(m1_w_06,r46_v, count >= 4)) or (interacting(m1_w_06,r56_v, count >= 4))));
}	




//***************************************      VIA7 RULES     *****************************/
    via7sq  = rectangles (via7, {0.05,0.05});
    via7lg  = rectangles (via7, {0.10,0.10});
    via7bar = rectangles (via7, {0.05,0.10});
{
	@ "R.VIA7.W: VIA7 must be square with 0.05 or 0.10 width and length or VIA7 must be rectangular with length 0.10 and width 0.05";
	not(via7,(via7sq or via7lg or via7bar));
}

{
	@ "R.VIA7.S.1: Minimum  spacing of VIA7SQ to VIA7SQ must be 0.07";
	external1 ( via7sq , distance < 0.07 ,  extension=RADIAL,relational = POINT_TOUCH  );	
}
{
	@ "R.VIA7.S.2: Minimum spacing of VIA7SQ to VIA7BAR must be 0.08";
	external2 (via7sq, via7bar, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA7.S.2: Minimum spacing of VIA7SQ to VIA7LG must be 0.08 ";
	external2(via7sq, via7lg, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA7.S.3: Minimum spacing of VIA7BAR or VIA7LG to VIA7BAR or VIA7LG must be 0.085";
	external1(via7bar, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA7.S.3: Minimum spacing of VIA7BAR or VIA7LG to VIA7BAR or VIA7LG must be 0.085";
	external1(via7lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "R.VIA7.S.3: Minimum spacing of VIA7BAR or VIA7LG to VIA7BAR or VIA7LG must be 0.085";
	external2(via7bar,via7lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}



{
	@ "R.VIA7.E.1: Minimum VIA7 enclosure by M8 and M7 must be  0.005";
	enclose ( via7 , m7 , distance < 0.005 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
	enclose ( via7 , m8 , distance < 0.005 , extension=RADIAL, intersecting = TOUCH , relational = POINT_TOUCH );
}
	
{
	@ "R.VIA7.E.1: VIA7 must be covered by M8 and M7, min. enclosure is 0.005um";
	not ( via7 , m8 );
	not ( via7 , m7 );
}

{
	@ "R.VIA7.E.3: Minimum VIA7BAR enclosure by M7 and M8 at end-of-line must be 0.005";


	not_covered_by(via7bar,m7,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});

	
	not_covered_by(via7bar,m8,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});


}

	via7_e_2_m1 = not_covered_by (via7, m8, distances ={{{0.005},{0.03},{0.005},{0.03}}});
	via7_e_2_m2 = not_covered_by (via7, m7, distances = {{{0.005},{0.03},{0.005},{0.03}}});
	via7_e_2 = or(via7_e_2_m1,via7_e_2_m2);

	via7_e_4_m1 = not_covered_by (via7, m8, distances ={{{0.005},{0.012},{0.012},{0.012}}});
	via7_e_4_m2 = not_covered_by (via7, m7, distances ={{{0.005},{0.012},{0.012},{0.012}}});
	via7_e_4 = or(via7_e_4_m1,via7_e_4_m2);

	via7_e_2_4 = and(via7_e_2,via7_e_4);
{
	@ "VIA7.E.2/VIA7.E.4: Minimum VIA7 enclosure by M7 and M8 at least two opposite sides if other two sides >= 0.005 must be 0.03, or must be 0.012 if one side is >=0.005";
	copy(via7_e_2_4);
	
}

m1_v_7 =  interacting(m7,via7);
m2_v_7 =  interacting(m8,via7);
m1_w_07 = wide (m1_v_7, > 0.2);
m2_w_07 = wide (m2_v_7, > 0.2);


r27 = external1 (via7sq, <= 0.15, extension = RADIAL);
r27_e = interacting (r27,via7sq,count > 1);
r27_v = interacting (via7sq, r27_e);

r37 =external1 (via7lg, <= 0.15, extension = RADIAL);
r37_e =interacting(r37,via7lg,count > 1);
r37_v =interacting (via7lg, r37_e);

r47 = external1 (via7sq, <= 0.7,  extension = RADIAL);
r47_or = or(r47, via7sq);
r47_e = interacting (r47_or,via7sq,count>3);
r47_v = interacting ( via7sq,r47_e);
r57   = external1 (via7lg, <= 0.7,  extension = RADIAL);
r57_or = or(r57,via7lg);
r57_e = interacting (r57_or, via7lg,count >3);
r57_v = interacting (via7lg, r57_e);


{
	@ "VIA7.B.1: When Mx or MX+1 width > 0.2, it is a must to have redundant VIAs (At least one rectangular VIAx, At least two  square VIAx with spacing <=0.15umn,At least four square VIAx with spacing <=0.7um)";
	not(m1_w_07,((interacting (m1_w_07, via7bar, count >= 1)) or (interacting (m1_w_07, r27_v, count >= 2)) or (interacting(m1_w_07,r37_v, count >=2 )) or (interacting(m1_w_07,r47_v, count >= 4)) or (interacting(m1_w_07,r57_v, count >= 4))));
}	


//********************************* VIAT Rules ******************************************************************************
    {
	@ "R.VIAT.B.5 VIAT must be placed orthogonal, rotation is not allowed";
	not_aspect_ratio(viat,1,orientation = ORTHOGONAL);
    }
    {	
	@ "VIAT.W.1: Exact size must be 0.13";
	not(viat,rectangles(viat, {0.13,0.13}));
    }
    

    {
	@ "VIAT.S.1: Minimum  spacing of VIAT must be 0.12";
	external1 ( viat , distance < 0.12 ,  extension=RADIAL,relational = POINT_TOUCH  );	
    }
    {
	@ "VIAT.E.1: Minimum VIAT enclosure by MT and M8 must be  0.015";
	enclose ( viat , mt , distance < 0.015 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
	enclose ( viat , m8 , distance < 0.015 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
    }
	
    {
	@ "VIAT.B.6: VIAT must be covered by M8 and MT, min. enclosure is 0.015um";
	not ( viat , m8 );
	not ( viat , mt );
    }

    {
	@ "VIAT.E.2: Minimum VIAT enclosure by MT and M8 at end-of-line must be 0.005";


	not_covered_by(viat,mt,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});

	
	not_covered_by(viat,m8,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});


     }

m10_w_02 = wide (mt, > 0.49);
m20_w_02 = wide (m8, > 0.49);


r2k = external1 (viat, <= 0.2, extension = RADIAL);
r2k_e = interacting (r2k,viat,count > 1);
r2k_v =interacting (viat, r2k_e);


r4k = external1 (viat, <= 0.5,  extension = RADIAL);
r4k_e = interacting (r4k,viat,count>3);
r4k_v = interacting ( viat,r4k_e);

{
	@ "VIAT.B.1: When Mx or MT width > 0.49, it is a must to have 1)at least two VIAT with spacing <= 0.2 or 2)at least four VIAT with spacing <= 0.5";
	not(m10_w_02,((interacting (m10_w_02, r2k_v, count >= 2)) or (interacting(m10_w_02,r4k_v, count >=4 )))) or not(m20_w_02,((interacting (m20_w_02, r2k_v, count >= 2)) or (interacting(m20_w_02,r4k_v, count >=4 ))));
}	

m1_w_07 = wide (mt, > 0.7);
m2_w_07 = wide (m8, > 0.7);


r21 = external1 (viat, <= 0.2, extension = RADIAL);
r21_e = interacting (r21,viat,count > 3);
r21_v =interacting (viat, r21_e);


r41 =external1 (viat, <= 0.5,  extension = RADIAL);
r41or = or(r41, viat);
r41_e = interacting (r41or,viat,count>8);
//interacting (r41,viat,count>8);}
r41_v =interacting ( viat,r41_e);

{
	@ "VIAT.B.2: When Mx or MT width > 0.7, it is a must to have 1)at least four VIAT with spacing <= 0.2 or 2)at least nine VIAT with spacing <= 0.5";
	not(m1_w_07,((interacting (m1_w_07, r21_v, count >= 4)) or (interacting(m1_w_07,r41_v, count >=9 )))) or not(m2_w_07,((interacting (m2_w_07, r21_v, count >= 4)) or (interacting(m2_w_07,r41_v, count >=9 ))));
}	

{
	@ "VIAT.B.3: At least two VIAT are required when connection distance is <3, from fat wire with WxL=3x3";
	m8_wide_1 = wide(m8, distance > 3);
	m8_wide   = area(m8_wide_1, value > 9);
	
	m8_thin_1 = not(m8,m8_wide);
	m8_thin = interacting (m8_thin_1, m8_wide); 
	
	ext_viat_1 = external2_edge (viat,m8_wide, distance < 3);
	
	int_viat = touching (viat, ext_viat_1 );
	m8_int_viat = interacting (m8_thin, int_viat);
	interacting ( m8_int_viat, viat, count <= 1 );
	mt_wide_1 = wide(mt, distance > 3);
	mt_wide   = area(mt_wide_1, value > 9);
	
	mt_thin_1 = not(mt,mt_wide);
	mt_thin = interacting (mt_thin_1, mt_wide); 
	
	ext_viat_11 = external2_edge (viat,mt_wide, distance < 3);
	
	int_viat1 = touching (viat, ext_viat_11 );
	mt_int_viat = interacting (mt_thin, int_viat);
	interacting ( mt_int_viat, viat, count <= 1 );
}
{
	@ "VIAT.B.4: At least two VIAT are required when connection distance is <5, from fat wire with WxL=5x10";
	m8_wide_1a = wide(m8, distance > 3);
	m8_widea   = area(m8_wide_1a, value > 9);
	
	m8_thin_1a = not(m8,m8_widea);
	m8_thina = interacting (m8_thin_1a, m8_widea); 
	
	ext_viat_1a = external2_edge (viat,m8_widea, distance < 3);
	
	int_viata = touching (viat, ext_viat_1a );
	m8_int_viata = interacting (m8_thina, int_viata);
	interacting ( m8_int_viata, viat, count <= 1 );
	mt_wide_1a = wide(mt, distance > 3);
	mt_widea   = area(mt_wide_1a, value > 9);
	
	mt_thin_1a = not(mt,mt_widea);
	mt_thina = interacting (mt_thin_1a, mt_widea); 
	
	ext_viat_11a = external2_edge (viat,mt_widea, distance < 3);
	
	int_viat1a = touching (viat, ext_viat_11a );
	mt_int_viata = interacting (mt_thina, int_viata);
	interacting ( mt_int_viata, viat, count <= 1 );
}

//*********************************VIARDL Rules**************************************************

{
	@ "VIARDL.W.1: Exact size must be 2";
	not_rectangles(viardl, {2,2});
}
{
	@ "VIARDL.S.1: Minimum VIARDL spacing must be 2";
	external1(viardl, distance < 2, extension = RADIAL, relational = POINT_TOUCH);
}
{
	@ "VIARDL.E.1: Minimum VIARDL enclosure by MRDL must be 0.5";
	enclose(viardl,mrdl,distance < 0.5, extension = RADIAL, intersecting = {TOUCH},relational = {POINT_TOUCH, INSIDE, OUTSIDE} );
}

//*******************************HVTIMP Rules***************************************************************
{
	@ "HVTIMP.W.1: HVTIMP minimum widht must be 0.15";
	internal1(hvtimp, distance < 0.15, extension = RADIAL);
}
{
	@ "HVTIMP.S.1: HVTIMP minimum spacing must be 0.15";
	external1 (hvtimp, distance < 0.15, extension = RADIAL);
}
{
	@ "HVTIMP.E.1: Minimum enclosure must be 0.05";
	enclose (diff, hvtimp, distance < 0.05, extension = RADIAL, intersecting = {TOUCH}, relational = {POINT_TOUCH, INSIDE});
}

//*******************************LVTIMP Rules****************************************************************
{
	@ "LVTIMP.W.1: LVTIMP minimum widht must be 0.15";
	internal1(lvtimp, distance < 0.15,extension = RADIAL);
}
{
	@ "LVTIMP.S.1: LVTIMP minimum spacing must be 0.15";
	external1 (lvtimp, distance < 0.15, extension = RADIAL);
}
{
	@ "LVTIMP.E.1: Minimum enclosure must be 0.05";
	enclose (diff, lvtimp, distance < 0.05, extension = RADIAL, intersecting = {TOUCH}, relational = {POINT_TOUCH, INSIDE});
}

//*******************************MRDL Rules*******************************************************************
{
	@"MRDL.W.1: Minimum width must be 2";
	internal1(mrdl,distance < 2,extension=RADIAL);
}
{
	@"MRDL.W.2: Maximum width must be 40";
	wide(mrdl, distance > 40);
}
{
	@"MRDL.S.1 Minimum spacing must be 2";
	external1(mrdl, distance < 2,extension = RADIAL);
}
