/*
#########################################################################################
# SAED 14nm 1p9m icv  drc deck								#
#											#
# Revision History:									#
# Rev.		date			what						#
# -------------------------------------------------------------------------------------	#	
# 1.0		6/Dec/2016		Initial release					#
#########################################################################################
*/

#include "icv.rh"

error_options(
    error_limit_per_check = ERROR_LIMIT_UNLIMITED
);

layout_grid_options (
		    resolution = 0.001,
		    check_45 = {PATH,POLYGON}
    		    );
TOP_MET = 9;

openaccess_options(
    view="layout",
     layer_mapping_file= "./techfiles/saed14nm_1p9m_gdsout.map"
);


/*************************  ASSIGNMENTS  ********************************/

	FINi    = assign({{1}});
	FINCUTi    = assign({{2}});
	NWELLi    = assign({{3}});
	DNWi	  = assign({{4}});
	DIFFi	  = assign({{5}});	
	DDMYi     = assign({{5,1}});
	PIMPi	  = assign({{6}});
	NIMPi	  = assign({{7}});
	DIFF_15i  = assign({{8}});
	DIFF_18i  = assign({{9}});
	PADi	  = assign({{10}});
	ESD	  = assign({{11}});
	SBLKi	  = assign({{12}});
	POi       = assign({{13}});
	POCUTi       = assign({{14}});
	PODMYi    = assign({{13,1}});
	TSLCOi    = assign({{15}});
	TSLCBi    = assign({{16}});
	CTM1i       = assign({{17}});
	CTM1i_1       = assign({{17, 1}});
	CTM1i_2       = assign({{17, 2}});
	CPOi       = assign({{18}});
	CPOi_1       = assign({{18, 1}});
	CPOi_2       = assign({{18, 2}});
	VIA0i     = assign({{81}});
	M1i       = assign({{19}});
	M1_3i	  = assign({{90}});		/* poxac */
	M1DMYi    = assign({{19,1}});
	M1i_text  = assign_text({{19}});
	VIA1i     = assign({{20}});
	M2i       = assign({{21}});
	M2_3i	  = assign({{91}});		/* poxac2 */
	M2i_text  = assign_text({{21}});
        VIA2i     = assign({{22}});
	M2DMYi    = assign({{21,1}});
	M3i       = assign({{23}});
	M3_3i       = assign({{92}});		/* poxac3 */
	M3i_text  = assign_text({{23}});
	M3DMYi    = assign({{23,1}});
        VIA3i     = assign({{24}});
	M4i       = assign({{25}});
	M4i_text  = assign_text({{25}}); 
	M4DMYi    = assign({{25,1}});      
        VIA4i     = assign({{26}});
	M5i       = assign({{27}}); 
	M5i_text  = assign_text({{27}});   
        VIA5i     = assign({{28}});
	M6i       = assign({{29}});    
	M6i_text  = assign_text({{29}});
	M6DMYi    = assign({{29,1}});
	VIA6i     = assign({{30}});
	M7i       = assign({{31}});
	M7i_text  = assign_text({{31}});   
	M7DMYi    = assign({{31,1}}); 
	VIA7i     = assign({{32}});
	M8i       = assign({{33}});
	M8i_text  = assign_text({{33}});
	M8DMYi    = assign({{33,1}});
	VIA8i     = assign({{34}});    
	M9i       = assign({{35}});   
	M9i_text  = assign({{35}});
	M9DMYi    = assign({{35,1}});  
	HVTIMPi   = assign({{36}});
	LVTIMPi   = assign({{37}});
	M1PIN     = assign({{38}});
        M1PIN_text = assign_text({{38}});
	M2PIN     = assign({{39}});
	M2PIN_text = assign_text({{39}});
	M3PIN     = assign({{40}});
	M3PIN_text = assign_text({{40}});
	M4PIN     = assign({{41}});
	M4PIN_text = assign_text({{41}});
	M5PIN     = assign({{42}});
	M5PIN_text = assign_text({{42}});
	M6PIN     = assign({{43}});
	M6PIN_text = assign_text({{43}});
	M7PIN     = assign({{44}});
	M7PIN_text = assign_text({{44}});
	M8PIN     = assign({{45}});
	M8PIN_text = assign_text({{45}});
	M9PIN     = assign({{46}});
	M9PIN_text = assign_text({{46}});
	MRDLi      = assign({{47}});
	VIARDLi	   = assign({{48}});
	MRPIN      = assign({{49}});
	HOTNWLi    = assign({{50}});
	DIODi      = assign({{51}});
	BJTMYi     = assign({{52}});
	RNWi      = assign({{53}});
	RMARKi     = assign({{54}});
	LOGO      = assign({{56}});
	IP        = assign({{57}});
	RM1i      = assign({{58}});
	RM2i      = assign({{59}});
	RM3i      = assign({{60}});
	RM4i      = assign({{61}});
	RM5i      = assign({{62}});
	RM6i      = assign({{63}});
	RM7i      = assign({{64}});	
	RM8i      = assign({{65}});
	RM9i      = assign({{66}});
	DIFFCUTi      = assign({{82}});
	AXPOLYi      = assign({{83}});
	SLVTIMPi      = assign({{84}});
	FGATEi		= assign({{85}});
	B_VIA0i      = assign({{86}});


/**************************  Data Creation  **************************** */

	fin	= FINi;
	fincut	= FINCUTi;
	nwell   = NWELLi;
	dnw     = DNWi;
	diff    = DIFFi; 
	pimp    = PIMPi;   
	nimp    = NIMPi;    
	diff_15 = DIFF_15i;
	diff_18 = DIFF_18i;   
	pad     = PADi;    	 
	esd	= ESD;
	sblk    = SBLKi;   
	po      = POi;
	pocut	= POCUTi;
	tslco	= TSLCOi;
	tslcb	= TSLCBi;
	ctm1	= CTM1i;
	ctm1_1	= CTM1i_1;
	ctm1_2	= CTM1i_2;
	cpo	= CPOi;
	cpo_1	= CPOi_1;
	cpo_2	= CPOi_2;
	rmark	= RMARKi;
	TOP_MET = 9;
	RECOMMENDED = 0;
	m1 = M1i;   
	m1_3 = M1_3i;		/* poxac */
	m2 = M2i;   
	m2_3 = M2_3i;		/* poxac */
	m3 = M3i;   
	m3_3 = M3_3i;		/* poxac */ 
	m4 = M4i;     
	m5 = M5i;  
	m6 = M6i;   
	m7 = M7i;  
	m8 = M8i;     
	m9 = M9i;  	
	via0 = VIA0i;
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
	diffcut = DIFFCUTi;
	axpoly = AXPOLYi;

	diod  =  DIODi;  
	bjtdmy = BJTMYi;   
	rnw    = RNWi;   
	viardl = VIARDLi;
	mrdl = MRDLi;
	mt = empty_layer(); 
    	mt2 = empty_layer();
	hvtimp = HVTIMPi;
	lvtimp = LVTIMPi;

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

/**************************** DOUBLE PATTERNING ***************************/


/***************************************************************************/

	imp = or ( nimp , pimp ); 
	ndiff = and ( nimp , diff );
	pdiff = and ( pimp , diff );

	nact = and ( ndiff , pwell );
	pact = and ( pdiff , nwell );
	act = or ( pact , nact );

	odwr = diff interacting nwres;//
	od15 = inside ( diff, diff_15 );//
	od18 = inside ( diff, diff_18 );//

	fpoly = not ( po , diff );//

	gate = and ( po not axpoly , act );
	gate_edge = and_edge (po not axpoly , act);
	ngate = and ( po not axpoly, nact );
	pgate = and ( po not axpoly , pact );
	gate_15 = and ( gate , diff_15 );//
	gate_18 = and ( gate , diff_18 );//
	diff_15_18 = or(diff_15,diff_18);
	gate_s = not(gate,interacting (gate,diff_15_18));
	ptap = and ( pdiff, pwell );
	ntap = and ( ndiff , nwell );
	tap  = or  ( ptap , ntap);
	//cood = and ( co , diff );//
	//copo = and ( co , po );//
	
	sd = not ( act , gate );//
	sd_tap = not ( diff, gate );//


/********* Begin Rules *******/

// common unions
ctm1_union = or_list({ctm1, ctm1_1, ctm1_2});
cpo_union = or_list({cpo, cpo_1, cpo_2});

n1= and(nwell,and(nimp,or_list({diff, diff_15, diff_18})));

cdb1 = connect (
                    {
                    {{n1},nwell},
                    {{n1},ctm1},
		    {{po}, cpo},
		    {m1, m1_3},			/*added*/
		    {m2, m2_3},			/*added*/
		    {m3, m3_3},			/*added*/
		    {{cpo, m1}, via0},
		    {{cpo, m1_3}, via0},	/* poxac */
                    {{ctm1, m1}, via0},
		    {{ctm1, m1_3}, via0},	/* poxac */
                    {{m1,m2},via1},
		    {{m1,m2_3},via1},	        /* poxac2 */			
		    {{m1_3,m2},via1},		/* poxac */
		    {{m1_3,m2_3},via1},		/* poxac2 */
                    {{m2_3,m3},via2}, 		/* poxac2 */
                    {{m3,m4},via3},
		    {{m2_3,m3_3},via2}, 	/* poxac3 */
                    {{m3_3,m4},via3},		/* poxac3 */
                    {{m4,m5},via4},
                    {{m5,m6},via5},
                    {{m6,m7},via6},
                    {{m7,m8},via7},
                    {{m8,m9},via8}
                    }
        );

CONNECT_DB : connect_database = NULL_CONNECT_DATABASE;


/******************************** FIN rules ***********************************/

	{
		@"FIN.W.1: FIN exact vertical width must be 0.014";
		correct = internal1(fin, == 0.014, extension = RADIAL, direction = VERTICAL);
		fin not_interacting correct;
	}

	{
                @ "FIN.S.1 Minimum spacing must be 0.036";
                external1 ( fin, distance < 0.036, extension = RADIAL, relational = POINT_TOUCH );
        }
	{
                @ "FIN.C.1: FIN must be orthogonal rectangle";
                not_rectangles(fin, orientation=ORTHOGONAL);
        }

// FIN orientation rule
get_vertical_oriented_fin : function (void) returning void
        {

                prim = df_get_current_data();
                prim_edges = df_edge_layer(prim, "fin_edges");
                hl = df_edge_horizontal_length(prim_edges, 0);
                vl = df_edge_vertical_length(prim_edges, 1);

        if (hl < vl)
                {
                        df_save_data(prim);
                }
        }


{
                @"FIN.C.2: FIN must be horizontally oriented";

        fin_edges = length_edge(fin, >0.014);  
        drc_features(
                primary_layer = fin,
                secondary_layers = {"fin_edges"=> fin_edges},
                drc_function = get_vertical_oriented_fin,
                output_from_layer = fin,
                error_shape = REGION
                    );
}



//////////////////////////////////////



/******************************************************************************/


/*************************  NWELL RULES ***************************/


	{
		@ "NWELL.W.1 Minimum width must be 0.1";
		internal1 ( nwell, distance < 0.1 , extension=RADIAL , relational = POINT_TOUCH);
	}


	{
		@ "NWELL.A.1 Minimum area must be 0.13";
		area(nwell, value < 0.13);
	}
	
nwell_holes = donut_holes (nwell, INNER);
	{
		@ "NWELL.A.2 Minimum Enclosed area must be 0.13";
		area(nwell_holes, value < 0.13);
	}
	
	
	{
		@"NWELL.S.1: Minimum spacing between wells at same potential must be 0.1";
		external1(nwell, distance < 0.1, extension = RADIAL, connectivity = SAME_NET, connect_sequence = cdb1);
	}	    
	{
		@"NWELL.S.2: Minimum spacing between wells at different potential must be 0.1";
		external1(nwell, distance < 0.1, extension = RADIAL, connectivity = DIFFERENT_NET, connect_sequence = cdb1);
	}	    

	{
                @ "NWELL.S.3 N+Active minimum space to N_Well must be 0.05";
                external2 ( nwell, nact , distance < 0.05, extension=RADIAL );
        }

	{
                @ "NWELL.EN.1 P+Active minimum within N_Well must be 0.05";
                enclose ( pact, nwell, distance < 0.05,extension=RADIAL );
        }

	{
                @ "NWELL.C.1 DIFF crossing N_WELL border is not allowed";
		diff_in_nwell = diff interacting nwell;
		diff_in_nwell not nwell;
        }
/*	{
                @ "NWELL.C.2 NWELL must be orthogonal";
                not_rectangles(nwell, orientation = ORTHOGONAL );
        }*/

		    
//************************  DNW RULES *****************************

	{
		@ "DNW.W.1 Minimum width must be 1.8";
		internal1 ( dnw, distance < 1.8 ,extension=RADIAL, relational = {POINT_TOUCH} );
	}

	{	
		@ "DNW.S.1 Minumum spacing, Deep_N_Well to Deep_N_Well must be 3.5 ";
		external1 ( dnw, distance < 3.3 ,extension=RADIAL, relational = {POINT_TOUCH});
	}

	{
		@ "DNW.S.2 Minimum spacing, Deep_N_Well to unrelated N_Well must be 2.5";
		external2 ( dnw , nwoutdnw, distance < 1.7 ,extension=RADIAL,  look_thru = COINCIDENT , relational = {POINT_TOUCH,OVERLAP} );
	}
	
//		pwoutdnw = not ( pwell , pwindnw );
//		nact_1 =  and (pwoutdnw , ndiff );

	{
		@ "DNW.S.3 Minimum spacing, external N+Active to Deep_N_Well must be 1.5";
		external2 ( dnw , (nact not_interacting dnw) , distance < 1.5, extension=RADIAL );
	}


//		pact_1 = and ( dnwnwell , pdiff );

/* kh: removed	{	
		@ "DNW.S.4 Minimum spacing, P+Active in N_Well to its Deep_N_Well must be 1";
		external2 ( dnw , pact_1 , distance < 1 ,extension=RADIAL,   look_thru = COINCIDENT , relational = {OVERLAP,POINT_TOUCH });
	}
*/

//		dnw_nwell=dnw inside nwell;
//		pwell_dnw=pwell inside dnw_nwell;
	
/* kh: removed	{
		@ "DNW.E.1 Minimum enclosure, N+Active by isolated P-Well must be 0.7";
		enclose ( nact , pwell_dnw , distance < 0.7 ,extension=RADIAL, intersecting = TOUCH , relational = {POINT_TOUCH,INSIDE});
	}
*/

	{
                @ "DNW.E.1 Minimum enclosure, N+Active by Deep_N_Weel must be 0.5";
                enclose ( nact, dnw , distance < 0.5 ,extension=RADIAL, intersecting = TOUCH , relational = {POINT_TOUCH,INSIDE});
        }

/* kh: removed
	{
		@ "DNW.E.2 Minimum enclosure, N_Well beyond Deep_N_Well edge must be 1";
		enclose ( dnw, nwell , distance < 0.5 ,extension=RADIAL, intersecting = TOUCH , relational = {POINT_TOUCH,INSIDE});
	}
*/	
		nwanddnw=and(dnw,nwell);
	
	{
		@ "DNW.O.1 Minimum overlap, N_Well over Deep_N_Well edge must be 0.4";
		internal1(nwanddnw, distance < 0.4,extension=RADIAL,relational={POINT_TOUCH});	
	}

	{
                @ "DNW.C.1 N+Active cutting Deep_N_Well is not allowed ";
                nact_in_dnw =nact interacting dnw;
		nact_in_dnw not dnw;
        }

//************************** DIFF RULES **********************

	{	
		@ "DIFF.B.1 DIFF must be fully covered by NIMP/PIMP";
		not ( not ( diff, odwr ) , imp );
	}	
/*
	{
		@ "DIFF.W.4 Channel width range must be [0.1,3.5]";
		not_length_edge(gate_edge , distance  =  [0.1, 3.5] );
	}
*/	
	dnotdcut=not(diff,diffcut);

        {
                @ "DIFF.W.1 Minimum width must be 0.044";
                internal1 ( dnotdcut , distance < 0.044 , extension=RADIAL,relational = POINT_TOUCH );
        }	
	

	{
                @ "DIFF.W.2 DIFF not DIFFCUT minimum C_width must be 0.074";
                internal1 ( dnotdcut, distance < 0.074 ,extension=RADIAL, direction = HORIZONTAL);
        }

	{

                @ "DIFF.W.3 Maximum width must be 23";
                wide(dnotdcut, distance > 23);

        }

	{
                @ "DIFF.S.1 Minimum spacing must be 0.074";
                external1 ( diff, distance < 0.074, extension = RADIAL, relational = POINT_TOUCH );
        }
	{
		@ "DIFF.S.2 Minimum P_space must be 0.1";
                external1(diff, distance < 0.1 ,extension=RADIAL, direction = VERTICAL);
        }
	{
                @ "DIFF.S.3 Minimum notch must be 0.074 ";
		inner_vertices = vertex(diff, > 180, shape_size = 0.001);
                diff_edges = edge_size(diff, inside = 0.001);
                notch = interacting_edge(diff_edges, inner_vertices, count == 2);
                length_edge(notch, < 0.074);
        }
	{
                @ "DIFF.S.4 Minimum spacing to FIN is 0.018";
                external2 (diff,  fin , distance < 0.018 ,extension=RADIAL, relational = POINT_TOUCH);
        }
	{
		@ "DIFF.S.5 Minimum overlap, P_overlap  past FIN must be 0.018";
                internal1 ( (diff interacting fin) not fin, distance < 0.018 ,extension=RADIAL,relational={POINT_TOUCH} , direction = VERTICAL );

        }
	{
                @ "DIFF.A.1  DIFF minimum area must be 0.0066";
                area ( diff, value <  0.0066 );
        }
	{
		@"DIFF.T.1 DIFF on FIN vertex, as well as DIFF vertex on FIN are not allowed";
		diff_vertex = vertex(diff, {90}, shape_size = 0.001);
		fin_vertex = vertex(fin, {90}, shape_size = 0.001);
		diff interacting [include_touch = ALL] fin_vertex;
		fin interacting [include_touch = ALL] diff_vertex;
	}
	{
                @ "DIFF.T.2  DIFF must touch FIN ";
                not_interacting ( diff, fin, include_touch = ALL );
        }


	
//*******************************************    PIMP RULES   


	{
		@ "PIMP.W.1 Minimum width must be 0.1";
	        internal1 ( pimp, distance < 0.1 ,extension=RADIAL, relational = POINT_TOUCH );
	}
	
	{
		@ "PIMP.E.1 Enclosure of P+Active must be 0.04";
		enclose ( pact , pimp , distance < 0.04 ,extension=RADIAL, relational = INSIDE , intersecting = TOUCH );
	}
	
	{
		@ "PIMP.E.2 Enclosure of PTAP must be 0.02";
		enclose ( ptap , pimp , distance < 0.02 , extension=RADIAL,relational = INSIDE , intersecting = TOUCH );
	}
/* kh: commented on 20170406
	{
		@ "PIMP.E.3: Poly enclosure by pimp must be 0.033";
		enclose (po, imp, distance < 0.033, extension = RADIAL, relational = INSIDE, intersecting = TOUCH);
	}
*/	
	{
		@ "PIMP.S.1 Minimum space must be 0.1";
		external1 ( pimp , distance < 0.1 ,extension=RADIAL, relational = POINT_TOUCH , look_thru = ALL ); 
	}

	{  	
		@ "PIMP.O.2 Overlap of NIMP and PIMP is not allowed";
		and ( pimp , nimp );
	}

	{
		@ "PIMP.S.2: Minimum space to butted N+Active must be 0.05";
		external2 ( pimp , nact , distance < 0.05 ,extension=RADIAL, relational = OVERLAP,  look_thru = COINCIDENT );
	} 
	pimp_s3 = nact and pwell;
	{	
		@ "PIMP.S.3 Minimum spacing to N+Active in P_Well must be 0.05";
		external2 ( pimp , pimp_s3 , distance < 0.05 ,extension=RADIAL, relational = OVERLAP,  look_thru = COINCIDENT );
	}

	{
		@ "PIMP.O.1 Minimum active overlap must be 0.05";
		internal2 ( pimp , diff, distance < 0.05,extension=RADIAL );
	}
	{
                @ "PIMP.A.1 Minimum area must be 0.038";
                area ( pimp, value < 0.038);
        }

//************************************************** NIMP RULES 

	{
		@ "NIMP.W.1 Minimum width must be 0.1";
		internal1 ( nimp, distance < 0.1 ,extension=RADIAL, relational = POINT_TOUCH );
	}
	
	{
		@ "NIMP.E.1 Enclosure of N+Active must be 0.04";
		enclose ( nact , nimp , distance < 0.04 ,extension=RADIAL, relational = INSIDE , intersecting = TOUCH );
	}
	
	{
		@ "NIMP.E.2 Enclosure of NTAP must be 0.02";
		enclose ( ntap , nimp , distance < 0.02 ,extension=RADIAL, relational = INSIDE , intersecting = TOUCH );
	}
	{
		@ "NIMP.E.3: Poly enclosure of NIMP in horizontal direction must be 0.034";
		enclose( po,imp, distance < 0.034, extension=RADIAL, relational = INSIDE,intersecting=TOUCH, direction=HORIZONTAL);
	}
	{
		@ "NIMP.S.1 Minimum space is 0.1";
		external1 ( nimp , distance < 0.1 ,extension=RADIAL, relational = POINT_TOUCH ); 
	}
  
	{
		@ "NIMP.S.2: Minimum space to butted P+Active must be 0.05"; 
		external2 ( nimp , pact , distance < 0.05 ,extension=RADIAL, relational = OVERLAP,  look_thru = COINCIDENT );
	}

	{	
		@ "NIMP.S.3 Minimum spacing to P+Active in N_Well must be 0.05";
		external2 ( nimp , pact and nwell, distance < 0.05 ,extension=RADIAL, relational = OVERLAP,  look_thru = COINCIDENT );
	}
/*
	{
		@ "NIMP.S.4: Minimum space to NWELL must be 0.3";
		external2 ( nimp , nwell , distance < 0.3 ,extension=RADIAL,look_thru = COINCIDENT , relational = {POINT_TOUCH,OVERLAP}, intersecting=TOUCH );
	}
*/
	{
		@ "NIMP.O.1 Minimum active overlap must be 0.05";
		internal2 ( nimp , act, distance < 0.05,extension=RADIAL );
	}

	{  	
		@ "NIMP.O.2 Overlap of NIMP and PIMP is not allowed";
		and ( pimp , nimp );
	}  
	{
                @ "NIMP.A.1 Minimum area must be 0.038";
                area ( nimp, value < 0.038 );
        }

//*********************************************    DIFF_18 RULES  
/*	
	{
		@ "DIFF_18.W.1 Minimum width must be 0.5"; 
		internal1 ( diff_18 , distance < 0.5, extension=RADIAL, relational = POINT_TOUCH );
	}
*/
	{
		@ "DIFF_18.S.1 Minimum spacing must be 0.26"; 
		external1 ( diff_18 , distance < 0.26 ,extension=RADIAL, relational = POINT_TOUCH , look_thru = ALL ); 
	}

	{
		@ "DIFF_18.C.1 DIFF_18 must have exact shape of DIFF";
		not(diff interacting diff_18, diff_18 interacting diff); 
	}
	
	int_diff = diff interacting diff_18;
	ext_diff = not ( diff , int_diff );
	{	
		@ "DIFF_18.S.2 Minimum space external DIFF must be 0.1"; 
		external2 ( diff_18  , ext_diff , distance < 0.1 ,extension=RADIAL, relational = OVERLAP,  look_thru = COINCIDENT );
	}
/*	{
		@ "DIFF_18.A.1 Min area diff_18 must be 0.2"; 
		area(diff_18, value < 0.2);
	}*/
    
	{
		@ "DIFF_18.A.2 Max enclosed area must be 10"; 
		less = donut_holes(diff_18, INNER, area <= 10);
		donut_holes(diff_18, INNER) not less;
	}


 

	

//*********************************************    DIFF_15 RULES  


/*	
	{
		@ "DIFF_15.W.1 Minimum width must be 0.5"; 
		internal1 ( diff_15 , distance < 0.5, extension=RADIAL, relational = POINT_TOUCH );
	}
*/
	{
		@ "DIFF_15.S.1 Minimum spacing must be 0.5"; 
		external1 ( diff_15 , distance < 0.5 ,extension=RADIAL, relational = POINT_TOUCH , look_thru = ALL ); 
	}
/*
	{
		@ "DIFF_15.E.1 Minimum  DIFF enclosure 0.3"; 
		enclose ( diff , diff_15 , distance < 0.3 ,extension=RADIAL, relational = INSIDE , intersecting = TOUCH );
	}
*/	
	int_diff = diff interacting diff_15;
	ext_diff = not ( diff , int_diff );
	{	
		@ "DIFF_15.S.2 Minimum space external Active must be 0.2"; 
		external2 ( diff_15  , ext_diff , distance < 0.2 ,extension=RADIAL, relational = OVERLAP,  look_thru = COINCIDENT );
	}

/*	{
		@ "DIFF_15.A.1 Min area diff_15 must be 0.2"; 
		area(diff_15, value < 0.2);
	}
*/    
	{
		@ "DIFF_15.A.2 Min enclosed area must be 0.2"; 
		less = donut_holes(diff_15, INNER, area <= 0.2);
		donut_holes(diff_15, INNER) not less;
	}



//*****************************************************    PAD RULES   

 pad_rect = rectangles (pad);
	{
		@ "PAD.W.1 PAD minimum bonding passivation opening width and length must be respectively 18 and 70";
		not_rectangles(pad_rect, {length1 >= 18,length2 >= 70});
	}
 pad_flip_chip = vertices (pad, count == 8);
 
	{
		@ "PAD.E.1 Minimum enclosure by MRDL 2um";
		enclose ( pad , mrdl , distance < 1 ,extension=RADIAL, relational = INSIDE , intersecting = TOUCH );
	}
	
	{
		@ "PAD.S.1 Minimum spacing 7um";
		external1 ( pad , distance < 7 ,extension=RADIAL, relational = POINT_TOUCH , look_thru = ALL );
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
		@ "SBLK.W.1 SBLK minimum width must be 0.07"; 
		internal1 ( sblk , distance < 0.07 ,extension=RADIAL, relational = POINT_TOUCH );
	}
	
	    poandsblk = and(po,sblk);
	
	{
		@ "SBLK.S.1: SBLK minimum spacing must be 0.02"; 
		external1 ( sblk , distance < 0.02 ,extension=RADIAL, relational = POINT_TOUCH , look_thru = ALL );
	}

	{
		@"SBLK.O.1 Minimum vertical edges overlap past PO 0.03";
		internal1 ( sblk not po,  distance < 0.03, extension=RADIAL, direction =  HORIZONTAL);

	}
/*	{
		@ "SBLK.C.1: SBLK must cover PO"; 
		not (po, sblk);
	}
*/
	{
		@ "SBLK.C.2: SBLK must be orthogonal"; 
		not_rectangles(via0, orientation=ORTHOGONAL);
	}
	
		
 //***********************  PO RULES ********************

        po_thin= internal1(po, distance == 0.014, extension=RADIAL);
        po_thick= not(po, po_thin);
        gate_thin= internal1(gate, distance == 0.014, extension=RADIAL);
        gate_thick_08= internal1(gate, distance == 0.08, extension=RADIAL);
        gate_thick= not(not(gate, gate_thin), gate_thick_08);



	{
		@ "PO.W.1: Minimum width must be 0.014"; 
		internal1 ( po , distance < 0.014 ,extension=RADIAL, relational = POINT_TOUCH );
	}
	
	{
		@ "PO.W.4.1: Minimum gate_15 length  must be 0.26"; 
		internal1 ( gate_15, distance < 0.1 ,extension=RADIAL, relational = POINT_TOUCH, direction = HORIZONTAL );
	}
	{
		@ "PO.W.4_2: Minimum gate_18 width must be 0.15";
		internal1 ( gate_18 , distance < 0.15 ,extension=RADIAL, relational = POINT_TOUCH, direction = HORIZONTAL );
	}

	

	fpoly_s_1 = external1 ( fpoly , distance < 0.05 ,extension=RADIAL, relational = POINT_TOUCH);	
	{
		@ "PO.S.1: PO minimum spacing over field must be 0.05"; 
		not ( fpoly_s_1 , gate );
	}
	

	{
		@ "PO.S.2: Gate minimum spacing must be 0.06"; 
		external1 ( gate , distance < 0.06 ,extension=RADIAL, relational = POINT_TOUCH, direction = HORIZONTAL);
	}

//added
	g2_ext_thin = external2(gate_thin,po_thin interacting axpoly,distance == 0.06, look_thru = ALL, extension = NONE, direction = HORIZONTAL);
	g2_ext_thick = external2(gate_thick,po_thick interacting axpoly,distance == 0.11, look_thru = ALL, extension = NONE, direction = HORIZONTAL);
        g2_ext_thick_08 = external2(gate_thick_08,po_thick interacting axpoly,distance == 0.08, look_thru = ALL, extension = NONE, direction = HORIZONTAL);
	g2_ext = external2(gate,po interacting axpoly,distance == 0.06, look_thru = ALL, extension = NONE, direction = HORIZONTAL);
	g2g = external1(gate, distance < 0.133, extension = NONE, direction= HORIZONTAL, look_thru = ALL,  look_thru_count == 0); // get any neighboring gates
	g2g_thin = external1(gate_thin, distance < 0.133, extension = NONE, direction= HORIZONTAL, look_thru = ALL,  look_thru_count == 0);
	g2g_thick = external1(gate_thick, distance < 0.133, extension = NONE, direction= HORIZONTAL, look_thru = ALL,  look_thru_count == 0);
        g2g_thick_08 = external1(gate_thick_08, distance < 0.133, extension = NONE, direction= HORIZONTAL, look_thru = ALL,  look_thru_count == 0);
	{
		@"PO.S.3.1: thin PO must have at least one PO at one side, spaced by 0.06"; 
	not(gate_thin,interacting(gate_thin,g2_ext_thin, count >= 1)) not (gate_thin interacting [count = 2] g2g_thin); 
	}
/*
	{
		@"PO.S.3.2: thick PO must have at least one PO at one side, spaced by 0.11"; 
	not(gate_thick, interacting(gate_thick,g2_ext_thick, count >= 1)) not (gate_thick interacting [count = 2] g2g_thick); 
	}
*/
//piliposy
        {
                @"PO.S.3.3: thick PO must have at least one PO at one side, spaced by 0.08";
        not(gate_thick_08, interacting(gate_thick_08,g2_ext_thick_08, count >= 1))  not (gate_thick_08 interacting [count = 2] g2g_thick_08);
        }


	po_14 = internal1 ( po , distance = 0.014 ,extension=RADIAL, relational = POINT_TOUCH);
	{
		@"PO.S.4: minimum PO spacing when w = 0.014 must be 0.06"; 
		external1 ( po_14 , distance < 0.06 ,extension=RADIAL, relational = POINT_TOUCH);
	}
	
	po_015m = internal1 ( po , distance = 0.15 ,extension=RADIAL, relational = POINT_TOUCH);
	{
		@"PO.S.5: minimum PO spacing when w = 0.15 must be 0.11"; 
		external1 ( po_015m , distance < 0.11 ,extension=RADIAL, relational = POINT_TOUCH);
	}

	

	{
		@ "PO.S.6: Minimum space of PO to DIFF must be 0.03"; 
		external2(po,diff,distance < 0.03, extension = RADIAL, relational = POINT_TOUCH);
	}

	diff_s_008= internal1(diff, distance < 0.05, extension = RADIAL, direction = VERTICAL);
	{
		@ "PO.S.7: Minimum space of PO to DIFF with vertically measured width < 0.05, parallel runlength > 0.1 must be 0.04"; 
		external2(po,diff_s_008,distance < 0.04, extension = RADIAL);
	}

/***** Vertical orientation of PO *****************/


po_not_r = po not rmark;

get_horizontal_oriented_po : function (void) returning void
        {

                prim = df_get_current_data();
                prim_edges = df_edge_layer(prim, "po_not_r_edges");
                hl = df_edge_horizontal_length(prim_edges, 0);
                vl = df_edge_vertical_length(prim_edges, 1);

        if (dblne(vl, 0) && dblne(hl, 0) && vl < hl)
                {
                        df_save_data(prim);
                }
        }

	

{
		@"PO.C.1: PO must be vertically oriented";
       	
	po_not_r_edges = length_edge(po_not_r, >0);
        drc_features(
                primary_layer = po_not_r,
                secondary_layers = {"po_not_r_edges"=> po_not_r_edges},
                drc_function = get_horizontal_oriented_po,
                output_from_layer = po_not_r,
                error_shape = REGION
                    );
}


/**********************************************/

	{
		@ "PO.EX.1: Minimum gate extension of active (end cap) must be  0.05"; 
		//enclose ( gate , po , distance < 0.04 , extension=RADIAL);
		po_not_gate = (po interacting gate) not gate;
		internal1(po_not_gate, < 0.05, extension = RADIAL, direction = VERTICAL);
	}
	if( RECOMMENDED == 1 ) {
 	{
		@ "R.PO.EX.1: Recommended minimum gate extension of active (end cap) must be  0.45";
		enclose ( gate , po , distance < 0.45 , extension=RADIAL);
	}}

/* kh: commented
	po_int_gate = po interacting gate;
	diff_int = interacting(diff,po_int_gate);

	po_ex_3 = connect ( 		
		    {
		    {{diff_int,po_int_gate},gate},
		    {{po,m1},cpo},
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
		@ "PO.EX.2: Minimum gate extension of active (PO distance to DIFF inner vertex < 0.5) must be  0.045"; 
		enclose (gate,interacting(po,po_ex_2) , distance < 0.045 , extension=NONE);
	}

	
	{
		@ "PO.EX.4 Minimum gate(width>0.06) extension of active must be 0.08";
		enclose (gate_g_w_006, po, distance < 0.08, extension = RADIAL);
	}
*/ 
	{
		@ "PO.EX.2 Minimun Active extension of gate must be 0.06";
		//enclose ( gate , diff , distance < 0.068 ,extension=RADIAL);
		diff_not_gate = (diff interacting gate) not gate;
                internal1(diff_not_gate, < 0.06, extension = RADIAL, direction = HORIZONTAL);
	}
	
		gt_coi_act = not_coincident_edge(gate,act);

	{
		@ "PO.A.1: Minimum po area must be 0.002"; 
		area(po, value < 0.002);
	}
/* kh: commented
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
	
	g3_ext =external2(gate_15,po,distance == 0.182, look_thru = ALL, extension = NONE, direction = HORIZONTAL);
	{
		@"PO.G.2_3:Gate_15 must be surrounded by PO from both sides with exact spacing 0.182"; (gate_25 changed to gate_15)
	not(gate_15,interacting(gate_15,g3_ext, count = 2));
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

*/

//***********************************************   M1 RULES 

	{
		@ "M1.W.1: Minimum M1 width must be 0.034"; 
		internal1 ( m1 , distance < 0.034 ,extension = RADIAL, relational = POINT_TOUCH );
	}
	{
		@ "M1.W.2: Maximum M1 width must be 0.8"; 
		wide (m1,distance > 0.8);
	}

	{
		@ "M1.S.1: Minimum M1 spacing must be 0.026";
		external1 ( m1 , distance < 0.026 ,extension = RADIAL, relational = POINT_TOUCH);
	}


	{
                @ "M1.S.1.1: Minimum space for run length >= 2.7 must be 0.06";
                external1(m1 , distance < 0.06, extension = NONE,projection_length >= 2.7, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
        }


	m1_int_m1_3 = interacting(m1,m1_3);
	m1_3_int_m1 = interacting(m1_3,m1);
	m1_not_int_m1_3 = not_interacting(m1,m1_3);
	m1_3_not_int_m1 = not_interacting(m1_3,m1);


	{
		@ "M1.S.2.1: Minimum spacing of m1 and m1_3 must be 0.026 "; 
	    	external2(m1_not_int_m1_3,m1_3_not_int_m1,distance < 0.026, extension = RADIAL,relational = POINT_TOUCH);
	}

	m1_or_m1_3 = or(m1_int_m1_3, m1_3_int_m1);

	{	
		@"M1.I.1: M1 and M1_3 must not interact";
		copy(m1_or_m1_3);
	}



	{
                @ "M1.S.1.2 Minimum notch must be 0.055";
		//length_edge(interacting_edge(m1, vertex_edge(m1, {> 90}), count == 2), < 0.055);
		inner_vertices = vertex(m1, > 180, shape_size = 0.001);
		m1_edges = edge_size(m1, inside = 0.001);
		notch = interacting_edge(m1_edges, inner_vertices, count == 2);
		length_edge(notch, < 0.055);
        }

    
    m1_w_0058 =wide(m1, distance > 0.058);
    m1_w_006 =wide(m1, distance > 0.06);
    m1_w_0185 =wide(m1, distance > 0.185);	
    m1_w_15 = wide(m1, distance > 1.5);	
   
	{
		@ "M1.S.2: Minimum spacing if metal width of one of lines > 0.058 and  their parallel run length > 0.07 must be 0.05"; 
	    	external2(m1_w_0058,m1,distance < 0.05, extension = NONE,projection_length > 0.07, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M1.S.3: Minimum spacing if metal width of one of lines > 0.06 and  their parallel run length > 0.07 must be 0.055"; 
	    	external2(m1_w_006,m1,distance < 0.055, extension = NONE,projection_length > 0.07, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M1.S.4: Minimum spacing if metal width of one of lines > 1.5 and  their parallel run length > 0 must be 0.55"; 
	    	external2(m1_w_15,m1,distance < 0.55, extension = NONE,projection_length > 0, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M1.S.5: Minimum spacing if metal width of one of lines > 0.185 and  their parallel run length > 0.25 must be 0.085"; 
	   	external2(m1_w_0185,m1,distance < 0.085, extension = NONE,projection_length > 0.25, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

    m1_s_01_h = not(m1, internal1(m1,distance < 0.075,extension = NONE, direction = HORIZONTAL));
    m1_s_01_v = not(m1, internal1(m1,distance < 0.075,extension = NONE, direction = VERTICAL));
    m1_s_03_h = not(m1, internal1(m1,distance <= 0.150,extension = NONE, direction = HORIZONTAL));
    m1_s_03_v = not(m1, internal1(m1,distance <= 0.150,extension = NONE, direction = VERTICAL));
	{
	  	@ "M1.S.6: Minimum spacing of M1 with span >= 0.075 with parallel run length > 0.104 must be 0.06"; 
	  	external1(m1_s_01_h, distance < 0.06, extension = NONE,direction = HORIZONTAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	  	@ "M1.S.6_1: Minimum spacing of M1 with span >= 0.075 with parallel run length > 0.104 must be 0.06"; 
	   	external1(m1_s_01_v, distance < 0.06, extension = NONE,direction = VERTICAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M1.S.7: Minimum spacing of M1 with span > 0.150 with parallel run length > 0.104 must be 0.065"; 
	  	external1(m1_s_03_h, distance < 0.065, extension = NONE,direction = HORIZONTAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	
	{
	    	@ "M1.S.7_1: Minimum spacing of M1 with span > 0.150 with parallel run length > 0.104 must be 0.065"; 
	    	external1(m1_s_03_v, distance < 0.065, extension = NONE,direction = VERTICAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}




	{	
		@ "M1.A.1  M1 minimum area must be 0.005"; 
		area ( m1 , value < 0.005 );
	}
	{
	   	@ "M1.A.2: M1 minimum enclosed area must be 0.04"; 
	 	area( donut_holes(m1, INNER), < 0.04);
	}



/*
	{
		@"M1.R.1: All M1/DIFF intersections must have a CTM1 shape ";
		m1_diff = m1 and diff;
		m1_diff not_interacting ctm1;
	}
	{
                @"M1.R.2: All M1/PO intersections must have a CPO shape ";
                m1_po = m1 and po;
                m1_po not_interacting cpo;
        }
*/

/********************** END M1 rules*****************/




/************************* M1_3 rules *********************/

{
		@ "M1_3.W.1: Minimum M1_3 width must be 0.034"; 
		internal1 ( m1_3 , distance < 0.034 ,extension = RADIAL, relational = POINT_TOUCH );
	}
	{
		@ "M1_3.W.2: Maximum M1_3 width must be 0.8"; 
		wide (m1_3 , distance > 0.8);
	}

	{
		@ "M1_3.S.1: Minimum M1_3 spacing must be 0.026";
		external1 ( m1_3 , distance < 0.026 ,extension = RADIAL, relational = POINT_TOUCH);
	}


	{
                @ "M1_3.S.1.1: Minimum space for run length >= 2.7 must be 0.06";
                external1(m1_3 , distance < 0.06, extension = NONE,projection_length >= 2.7, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
        }

	{
                @ "M1_3.S.1.2 Minimum notch must be 0.055";
		//length_edge(interacting_edge(m1_3, vertex_edge(m1_3, {> 90}), count == 2), < 0.055);
		inner_vertices = vertex(m1_3, > 180, shape_size = 0.001);
		m1_3_edges = edge_size(m1_3, inside = 0.001);
		notch = interacting_edge(m1_3_edges, inner_vertices, count == 2);
		length_edge(notch, < 0.055);
        }

    
    m1_3_w_0058 =wide(m1_3, distance > 0.058);
    m1_3_w_006 =wide(m1_3, distance > 0.06);	
    m1_3_w_15 = wide(m1_3, distance > 1.5);	
    m1_3_w_0185 =wide(m1_3, distance > 0.185);

	{
		@ "M1_3.S.2: Minimum spacing if metal width of one of lines > 0.058 and  their parallel run length > 0.07 must be 0.06"; 
	    	external2(m1_3_w_0058 ,m1,distance < 0.035, extension = NONE,projection_length > 0.07, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M1_3.S.3: Minimum spacing if metal width of one of lines > 0.06 and  their parallel run length > 0.07 must be 0.065"; 
	    	external2(m1_3_w_006,m1,distance < 0.036, extension = NONE,projection_length > 0.07, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M1_3.S.4: Minimum spacing if metal width of one of lines > 1.5 and  their parallel run length > 0 must be 0.55"; 
	    	external2(m1_3_w_15,m1,distance < 0.37, extension = NONE,projection_length > 0, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M1_3.S.5: Minimum spacing if metal width of one of lines > 0.185 and  their parallel run length > 0.25 must be 0.085"; 
	   	external2(m1_3_w_0185,m1,distance < 0.038, extension = NONE,projection_length > 0.25, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

    m1_3_s_01_h = not(m1_3, internal1(m1_3,distance < 0.075,extension = NONE, direction = HORIZONTAL));
    m1_3_s_01_v = not(m1_3, internal1(m1_3,distance < 0.075,extension = NONE, direction = VERTICAL));
    m1_3_s_03_h = not(m1_3, internal1(m1_3,distance <= 0.150,extension = NONE, direction = HORIZONTAL));
    m1_3_s_03_v = not(m1_3, internal1(m1_3,distance <= 0.150,extension = NONE, direction = VERTICAL));
	{
	  	@ "M1_3.S.6: Minimum spacing of M1_3 with span >= 0.075 with parallel run length > 0.104 must be 0.06"; 
	  	external1(m1_3_s_01_h, distance < 0.06, extension = NONE,direction = HORIZONTAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	  	@ "M1_3.S.6_1: Minimum spacing of M1_3 with span >= 0.075 with parallel run length > 0.104 must be 0.06"; 
	   	external1(m1_3_s_01_v, distance < 0.06, extension = NONE,direction = VERTICAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M1_3.S.7: Minimum spacing of M1_3 with span > 0.150 with parallel run length > 0.104 must be 0.065"; 
	  	external1(m1_3_s_03_h, distance < 0.065, extension = NONE,direction = HORIZONTAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	
	{
	    	@ "M1_3.S.7_1: Minimum spacing of M1_3 with span > 0.150 with parallel run length > 0.104 must be 0.065"; 
	    	external1(m1_3_s_03_v, distance < 0.065, extension = NONE,direction = VERTICAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}




	{	
		@ "M1_3.A.1  M1_3 minimum area must be 0.005"; 
		area ( m1_3 , value < 0.005 );
	}
	{
	   	@ "M1_3.A.2: M1_3 minimum enclosed area must be 0.04"; 
	 	area( donut_holes(m1_3, INNER), < 0.04);
	}


/****************** END M1_3 rules ************************/


//***********************************************   M2 RULES 

	{
		@ "M2.W.1: Minimum M2 width must be 0.034"; 
		internal1 ( m2 , distance < 0.034 ,extension = RADIAL, relational = POINT_TOUCH );
	}
	{
		@ "M2.W.2: Maximum M2 width must be 0.8"; 
		wide (m2,distance > 0.8);
	}

	{
		@ "M2.S.1: Minimum M2 spacing must be 0.026";
		external1 ( m2 , distance < 0.026 ,extension = RADIAL, relational = POINT_TOUCH);
	}


	{
                @ "M2.S.1.1: Minimum space for run length >= 2.7 must be 0.06";
                external1(m2 , distance < 0.06, extension = NONE,projection_length >= 2.7, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
        }

	{
                @ "M2.S.1.2 Minimum notch must be 0.055";
		length_edge(interacting_edge(m2, vertex_edge(m2, {> 90}), count == 2), < 0.055);
        }


	m2_int_m2_3 = interacting(m2,m2_3);
	m2_3_int_m2 = interacting(m2_3,m2);
	m2_not_int_m2_3 = not_interacting(m2,m2_3);
	m2_3_not_int_m2 = not_interacting(m2_3,m2);

	{
		@ "M2.S.2.1: Minimum spacing of m2 and m2_3 must be 0.026 "; 
	    	external2(m2_not_int_m2_3,m2_3_not_int_m2,distance < 0.026, extension = RADIAL,relational = POINT_TOUCH);
	}

	m2_or_m2_3 = or(m2_int_m2_3, m2_3_int_m2);

	{	
		@"M2.I.1: M2 and M2_3 must not interact";
		copy(m2_or_m2_3);
	}


    m2_w_0058 =wide(m2, distance > 0.058);
    m2_w_006 =wide(m2, distance > 0.06);	
    m2_w_15 = wide(m2, distance > 1.5);	
    m2_w_0185 =wide(m2, distance > 0.185);

	{
		@ "M2.S.2: Minimum spacing if metal width of one of lines > 0.058 and  their parallel run length > 0.07 must be 0.06"; 
	    	external2(m2_w_0058,m2,distance < 0.06, extension = NONE,projection_length > 0.07, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M2.S.3: Minimum spacing if metal width of one of lines > 0.06 and  their parallel run length > 0.07 must be 0.065"; 
	    	external2(m2_w_006,m2,distance < 0.065, extension = NONE,projection_length > 0.07, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M2.S.4: Minimum spacing if metal width of one of lines > 1.5 and  their parallel run length > 0 must be 0.55"; 
	    	external2(m2_w_15,m2,distance < 0.55, extension = NONE,projection_length > 0, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M2.S.5: Minimum spacing if metal width of one of lines > 0.185 and  their parallel run length > 0.25 must be 0.085"; 
	   	external2(m2_w_0185,m2,distance < 0.085, extension = NONE,projection_length > 0.25, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

    m2_s_01_h = not(m2, internal1(m2,distance < 0.075,extension = NONE, direction = HORIZONTAL));
    m2_s_01_v = not(m2, internal1(m2,distance < 0.075,extension = NONE, direction = VERTICAL));
    m2_s_03_h = not(m2, internal1(m2,distance <= 0.150,extension = NONE, direction = HORIZONTAL));
    m2_s_03_v = not(m2, internal1(m2,distance <= 0.150,extension = NONE, direction = VERTICAL));
	{
	  	@ "M2.S.6: Minimum spacing of M2 with span >= 0.075 with parallel run length > 0.104 must be 0.06"; 
	  	external1(m2_s_01_h, distance < 0.06, extension = NONE,direction = HORIZONTAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	  	@ "M2.S.6_1: Minimum spacing of M2 with span >= 0.075 with parallel run length > 0.104 must be 0.06"; 
	   	external1(m2_s_01_v, distance < 0.06, extension = NONE,direction = VERTICAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M2.S.7: Minimum spacing of M2 with span > 0.150 with parallel run length > 0.3 must be 0.065"; 
	  	external1(m2_s_03_h, distance < 0.065, extension = NONE,direction = HORIZONTAL,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	
	{
	    	@ "M2.S.7_1: Minimum spacing of M2 with span > 0.150 with parallel run length > 0.104 must be 0.065"; 
	    	external1(m2_s_03_v, distance < 0.065, extension = NONE,direction = VERTICAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}




	{	
		@ "M2.A.1  M2 minimum area must be 0.005"; 
		area ( m2 , value < 0.005 );
	}
	{
	   	@ "M2.A.2: M2 minimum enclosed area must be 0.04"; 
	 	area( donut_holes(m2, INNER), < 0.04);
	}




/********************** END M2 rules*****************/




//***********************************************   M2_3 RULES 

	{
		@ "M2_3.W.1: Minimum M2_3 width must be 0.034"; 
		internal1 ( m2_3 , distance < 0.034 ,extension = RADIAL, relational = POINT_TOUCH );
	}
	{
		@ "M2_3.W.2: Maximum M2_3 width must be 0.8"; 
		wide (m2_3,distance > 0.8);
	}

	{
		@ "M2_3.S.1: Minimum M2_3 spacing must be 0.026";
		external1 ( m2_3 , distance < 0.026 ,extension = RADIAL, relational = POINT_TOUCH);
	}


	{
                @ "M2_3.S.1.1: Minimum space for run length >= 2.7 must be 0.06";
                external1(m2_3 , distance < 0.06, extension = NONE,projection_length >= 2.7, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
        }




	{
                @ "M2_3.S.1.2 Minimum notch must be 0.055";
		length_edge(interacting_edge(m2_3, vertex_edge(m2_3, {> 90}), count == 2), < 0.055);
        }

    m2_3_w_0058 =wide(m2_3, distance > 0.058);
    m2_3_w_006 =wide(m2_3, distance > 0.06);	
    m2_3_w_15 = wide(m2_3, distance > 1.5);	
    m2_3_w_0185 =wide(m2_3, distance > 0.185);

	{
		@ "M2_3.S.2: Minimum spacing if metal width of one of lines > 0.058 and  their parallel run length > 0.07 must be 0.06"; 
	    	external2(m2_3_w_0058,m2,distance < 0.06, extension = NONE,projection_length > 0.07, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M2_3.S.3: Minimum spacing if metal width of one of lines > 0.06 and  their parallel run length > 0.07 must be 0.065"; 
	    	external2(m2_3_w_006,m2,distance < 0.065, extension = NONE,projection_length > 0.07, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M2_3.S.4: Minimum spacing if metal width of one of lines > 1.5 and  their parallel run length > 0 must be 0.55"; 
	    	external2(m2_3_w_15,m2,distance < 0.55, extension = NONE,projection_length > 0, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M2_3.S.5: Minimum spacing if metal width of one of lines > 0.185 and  their parallel run length > 0.25 must be 0.085"; 
	   	external2(m2_3_w_0185,m2,distance < 0.085, extension = NONE,projection_length > 0.25, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

    m2_3_s_01_h = not(m2_3, internal1(m2_3,distance < 0.075,extension = NONE, direction = HORIZONTAL));
    m2_3_s_01_v = not(m2_3, internal1(m2_3,distance < 0.075,extension = NONE, direction = VERTICAL));
    m2_3_s_03_h = not(m2_3, internal1(m2_3,distance <= 0.150,extension = NONE, direction = HORIZONTAL));
    m2_3_s_03_v = not(m2_3, internal1(m2_3,distance <= 0.150,extension = NONE, direction = VERTICAL));
	{
	  	@ "M2_3.S.6: Minimum spacing of M2_3 with span >= 0.075 with parallel run length > 0.104 must be 0.06"; 
	  	external1(m2_3_s_01_h, distance < 0.06, extension = NONE,direction = HORIZONTAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	  	@ "M2_3.S.6_1: Minimum spacing of M2_3 with span >= 0.075 with parallel run length > 0.104 must be 0.06"; 
	   	external1(m2_3_s_01_v, distance < 0.06, extension = NONE,direction = VERTICAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M2_3.S.7: Minimum spacing of M2_3 with span > 0.150 with parallel run length > 0.3 must be 0.065"; 
	  	external1(m2_3_s_03_h, distance < 0.065, extension = NONE,direction = HORIZONTAL,projection_length > 0.3, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	
	{
	    	@ "M2_3.S.7_1: Minimum spacing of M2_3 with span > 0.150 with parallel run length > 0.104 must be 0.065"; 
	    	external1(m2_3_s_03_v, distance < 0.065, extension = NONE,direction = VERTICAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}




	{	
		@ "M2_3.A.1  M2_3 minimum area must be 0.005"; 
		area ( m2_3 , value < 0.005 );
	}
	{
	   	@ "M2_3.A.2: M2_3 minimum enclosed area must be 0.04"; 
	 	area( donut_holes(m2_3, INNER), < 0.04);
	}



/********************** END M2_3 rules*****************/





//***********************************************   M3 RULES 

	{
		@ "M3.W.1: Minimum M3 width must be 0.034"; 
		internal1 ( m3 , distance < 0.034 ,extension = RADIAL, relational = POINT_TOUCH );
	}
	{
		@ "M3.W.2: Maximum M3 width must be 0.8"; 
		wide (m3,distance > 0.8);
	}

	{
		@ "M3.S.1: Minimum M3 spacing must be 0.026";
		external1 ( m3 , distance < 0.026 ,extension = RADIAL, relational = POINT_TOUCH);
	}


	{
                @ "M3.S.1.1: Minimum space for run length >= 2.7 must be 0.06";
                external1(m3 , distance < 0.06, extension = NONE,projection_length >= 2.7, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
        }

	{
                @ "M3.S.1.2 Minimum notch must be 0.055";
		length_edge(interacting_edge(m3, vertex_edge(m3, {> 90}), count == 2), < 0.055);
        }


	m3_int_m3_3 = interacting(m3,m3_3);
	m3_3_int_m3 = interacting(m3_3,m3);
	m3_not_int_m3_3 = not_interacting(m3,m3_3);
	m3_3_not_int_m3 = not_interacting(m3_3,m3);

	{
		@ "M3.S.2.1: Minimum spacing of m3 and m3_3 must be 0.026 "; 
	    	external2(m3_not_int_m3_3,m3_3_not_int_m3,distance < 0.026, extension = RADIAL,relational = POINT_TOUCH);
	}

	m3_or_m3_3 = or(m3_int_m3_3, m3_3_int_m3);

	{	
		@"M3.I.1: M3 and M3_3 must not interact";
		copy(m3_or_m3_3);
	}

   
    m3_w_0058 =wide(m3, distance > 0.058);
    m3_w_006 =wide(m3, distance > 0.06);	
    m3_w_15 = wide(m3, distance > 1.5);	
    m3_w_0185 =wide(m3, distance > 0.185);

	{
		@ "M3.S.2: Minimum spacing if metal width of one of lines > 0.058 and  their parallel run length > 0.07 must be 0.06"; 
	    	external2(m3_w_0058,m3,distance < 0.06, extension = NONE,projection_length > 0.07, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M3.S.3: Minimum spacing if metal width of one of lines > 0.06 and  their parallel run length > 0.07 must be 0.065"; 
	    	external2(m3_w_006,m3,distance < 0.065, extension = NONE,projection_length > 0.07, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M3.S.4: Minimum spacing if metal width of one of lines > 1.5 and  their parallel run length > 0 must be 0.55"; 
	    	external2(m3_w_15,m3,distance < 0.55, extension = NONE,projection_length > 0, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M3.S.5: Minimum spacing if metal width of one of lines > 0.185 and  their parallel run length > 0.25 must be 0.085"; 
	   	external2(m3_w_0185,m3,distance < 0.085, extension = NONE,projection_length > 0.25, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

    m3_s_01_h = not(m3, internal1(m3,distance < 0.075,extension = NONE, direction = HORIZONTAL));
    m3_s_01_v = not(m3, internal1(m3,distance < 0.075,extension = NONE, direction = VERTICAL));
    m3_s_03_h = not(m3, internal1(m3,distance <= 0.150,extension = NONE, direction = HORIZONTAL));
    m3_s_03_v = not(m3, internal1(m3,distance <= 0.150,extension = NONE, direction = VERTICAL));
	{
	  	@ "M3.S.6: Minimum spacing of M3 with span >= 0.075 with parallel run length > 0.104 must be 0.06"; 
	  	external1(m3_s_01_h, distance < 0.06, extension = NONE,direction = HORIZONTAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	  	@ "M3.S.6_1: Minimum spacing of M3 with span >= 0.075 with parallel run length > 0.104 must be 0.06"; 
	   	external1(m3_s_01_v, distance < 0.06, extension = NONE,direction = VERTICAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M3.S.7: Minimum spacing of M3 with span > 0.150 with parallel run length > 0.104 must be 0.065"; 
	  	external1(m3_s_03_h, distance < 0.065, extension = NONE,direction = HORIZONTAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	
	{
	    	@ "M3.S.7_1: Minimum spacing of M3 with span > 0.150 with parallel run length > 0.104 must be 0.065"; 
	    	external1(m3_s_03_v, distance < 0.065, extension = NONE,direction = VERTICAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}




	{	
		@ "M3.A.1  M3 minimum area must be 0.005"; 
		area ( m3 , value < 0.005 );
	}
	{
	   	@ "M3.A.2: M3 minimum enclosed area must be 0.04"; 
	 	area( donut_holes(m3, INNER), < 0.04);
	}



/********************** END M3 rules*****************/




/********************** M3_3 rules ******************/
	{
		@ "M3_3.W.1: Minimum M3_3 width must be 0.034"; 
		internal1 ( m3_3 , distance < 0.034 ,extension = RADIAL, relational = POINT_TOUCH );
	}
	{
		@ "M3_3.W.2: Maximum M3_3 width must be 0.8"; 
		wide (m3_3,distance > 0.8);
	}

	{
		@ "M3_3.S.1: Minimum M3_3 spacing must be 0.026";
		external1 ( m3_3 , distance < 0.026 ,extension = RADIAL, relational = POINT_TOUCH);
	}


	{
                @ "M3_3.S.1.1: Minimum space for run length >= 2.7 must be 0.06";
                external1(m3_3 , distance < 0.06, extension = NONE,projection_length >= 2.7, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
        }

	{
                @ "M3_3.S.1.2 Minimum notch must be 0.055";
		length_edge(interacting_edge(m3_3, vertex_edge(m3_3, {> 90}), count == 2), < 0.055);
        }

   
    m3_3_w_0058 =wide(m3_3, distance > 0.058);
    m3_3_w_006 =wide(m3_3, distance > 0.06);	
    m3_3_w_15 = wide(m3_3, distance > 1.5);	
    m3_3_w_0185 =wide(m3_3, distance > 0.185);

	{
		@ "M3_3.S.2: Minimum spacing if metal width of one of lines > 0.058 and  their parallel run length > 0.07 must be 0.06"; 
	    	external2(m3_3_w_0058,m3_3,distance < 0.06, extension = NONE,projection_length > 0.07, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M3_3.S.3: Minimum spacing if metal width of one of lines > 0.06 and  their parallel run length > 0.07 must be 0.065"; 
	    	external2(m3_3_w_006,m3_3,distance < 0.065, extension = NONE,projection_length > 0.07, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	
	{
	    	@ "M3_3.S.4: Minimum spacing if metal width of one of lines > 1.5 and  their parallel run length > 0 must be 0.55"; 
	    	external2(m3_3_w_15,m3_3,distance < 0.55, extension = NONE,projection_length > 0, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M3_3.S.5: Minimum spacing if metal width of one of lines > 0.185 and  their parallel run length > 0.25 must be 0.085"; 
	   	external2(m3_3_w_0185,m3_3,distance < 0.085, extension = NONE,projection_length > 0.25, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

    m3_3_s_01_h = not(m3_3, internal1(m3_3,distance < 0.075,extension = NONE, direction = HORIZONTAL));
    m3_3_s_01_v = not(m3_3, internal1(m3_3,distance < 0.075,extension = NONE, direction = VERTICAL));
    m3_3_s_03_h = not(m3_3, internal1(m3_3,distance <= 0.150,extension = NONE, direction = HORIZONTAL));
    m3_3_s_03_v = not(m3_3, internal1(m3_3,distance <= 0.150,extension = NONE, direction = VERTICAL));
	{
	  	@ "M3_3.S.6: Minimum spacing of M3_3 with span >= 0.075 with parallel run length > 0.104 must be 0.06"; 
	  	external1(m3_3_s_01_h, distance < 0.06, extension = NONE,direction = HORIZONTAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	  	@ "M3_3.S.6_1: Minimum spacing of M3_3 with span >= 0.075 with parallel run length > 0.104 must be 0.06"; 
	   	external1(m3_3_s_01_v, distance < 0.06, extension = NONE,direction = VERTICAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M3_3.S.7: Minimum spacing of M3_3 with span > 0.150 with parallel run length > 0.104 must be 0.065"; 
	  	external1(m3_3_s_03_h, distance < 0.065, extension = NONE,direction = HORIZONTAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}	
	
	{
	    	@ "M3_3.S.7_1: Minimum spacing of M3_3 with span > 0.150 with parallel run length > 0.104 must be 0.065"; 
	    	external1(m3_3_s_03_v, distance < 0.065, extension = NONE,direction = VERTICAL,projection_length > 0.104, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}




	{	
		@ "M3_3.A.1  M3_3 minimum area must be 0.005"; 
		area ( m3_3 , value < 0.005 );
	}
	{
	   	@ "M3_3.A.2: M3_3 minimum enclosed area must be 0.04"; 
	 	area( donut_holes(m3_3, INNER), < 0.04);
	}



/********************** END M3_3 rules*****************/




//***********************************************   M4 RULES 

	m4_w_0_06 = internal1 ( m4 , distance = 0.06 ,extension = RADIAL, relational = POINT_TOUCH );
	m4_w_0_08 = internal1 ( m4 , distance = 0.08 ,extension = RADIAL, relational = POINT_TOUCH );
	m4_w_0_10 = internal1 ( m4 , distance = 0.10 ,extension = RADIAL, relational = POINT_TOUCH );
	m4_w_0_12 = internal1 ( m4 , distance = 0.12 ,extension = RADIAL, relational = POINT_TOUCH );
	m4_w_0_16 = internal1 ( m4 , distance = 0.16 ,extension = RADIAL, relational = POINT_TOUCH );	
	m4_w_0_20_and_more = not ( not (not( not( not( m4,m4_w_0_16 ),m4_w_0_12 ),m4_w_0_10 ),m4_w_0_08) ,m4_w_0_06);	
	{
		@ "M4.W.1: M4 width must be  0.06 , 0.08 , 0.10, 0.12, 0.16 or > 0.2"; 
		internal1 ( m4_w_0_20_and_more , distance < 0.2 ,extension = RADIAL, relational = POINT_TOUCH );
	}

	{
		@ "M4.W.2: Maximum M4 width must be 3"; 
		wide (m4,distance > 3);
	}

	{
		@ "M4.S.1: Minimum M4 spacing must be 0.04";
		external1 ( m4 , distance < 0.04 ,extension = RADIAL, relational = POINT_TOUCH);
	}


	{
                @ "M4.S.1.2 Minimum notch must be 0.04";
		length_edge(interacting_edge(m4, vertex_edge(m4, {> 90}), count == 2), < 0.04);
        }

    
	{
		@ "M4.S.2: Minimum M4 spacing when width is > 0.2 must be 0.06";
		external1 (m4_w_0_20_and_more , distance < 0.06 ,extension = RADIAL, relational = POINT_TOUCH);
	}
	
	{
		@ "M4.S.2.1: Minimum M4 spacing when width =0.16 must be 0.06";
		external1 (m4_w_0_16 , distance < 0.06 ,extension = RADIAL, relational = POINT_TOUCH);
	}
	  
    	m4_w_008 =wide(m5, distance > 0.08);
    	m4_w_07 = not ( m4, internal1 ( m4 , distance <0.7 ,extension = RADIAL, relational = POINT_TOUCH ) );	
    	
	{
	    	@ "M4.S.3.1: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.06 must be 0.06"; 
	    	external2(m4_w_008 , m4, distance < 0.06, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M4.S.3.2: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.08 must be 0.065"; 
	    	external2(m4_w_008 , not ( m4, m4_w_0_06), distance < 0.065, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M4.S.3.3: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.1 must be 0.075"; 
	    	external2(m4_w_008 , not ( not ( m4, m4_w_0_06), m4_w_0_08), distance < 0.075, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
{
	    	@ "M4.S.3.4: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.12 must be 0.1"; 
	    	external2(m4_w_008 , not( not ( not ( m4, m4_w_0_06), m4_w_0_08), m4_w_0_10), distance < 0.1, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M4.S.4.1: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0 must be 0.17"; 
	    	external2(m4_w_07 , m4, distance < 0.17, extension = NONE,projection_length > 0.17, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M4.S.4.2: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0.10 must be 0.18"; 
	    	external2(m4_w_07 , not ( not ( m4, m4_w_0_06), m4_w_0_08), distance < 0.18, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M4.S.4.3: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0.2 must be 0.19"; 
	    	external2(m4_w_07 , m4_w_0_20_and_more, distance < 0.19, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M4.S.4.4: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0.7 must be 0.17"; 
	    	external1(m4_w_07 ,  distance < 0.17, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}


/********************** END M4 rules*****************/

//***********************************************   M5 RULES 

	m5_w_0_06 = internal1 ( m5 , distance = 0.06 ,extension = RADIAL, relational = POINT_TOUCH );
	m5_w_0_08 = internal1 ( m5 , distance = 0.08 ,extension = RADIAL, relational = POINT_TOUCH );
	m5_w_0_10 = internal1 ( m5 , distance = 0.10 ,extension = RADIAL, relational = POINT_TOUCH );
	m5_w_0_12 = internal1 ( m5 , distance = 0.12 ,extension = RADIAL, relational = POINT_TOUCH );
	m5_w_0_16 = internal1 ( m5 , distance = 0.16 ,extension = RADIAL, relational = POINT_TOUCH );	
	m5_w_0_20_and_more = not ( not (not( not( not( m5,m5_w_0_16 ),m5_w_0_12 ),m5_w_0_10 ),m5_w_0_08) ,m5_w_0_06);	
	{
		@ "M5.W.1: m5 width must be  0.06 , 0.08 , 0.10, 0.12, 0.16 or > 0.2"; 
		internal1 ( m5_w_0_20_and_more , distance < 0.2 ,extension = RADIAL, relational = POINT_TOUCH );
	}

	{
		@ "M5.W.2: Maximum m5 width must be 3"; 
		wide (m5,distance > 3);
	}

	{
		@ "M5.S.1: Minimum m5 spacing must be 0.04";
		external1 ( m5 , distance < 0.04 ,extension = RADIAL, relational = POINT_TOUCH);
	}


	{
                @ "M5.S.1.2 Minimum notch must be 0.04";
		length_edge(interacting_edge(m5, vertex_edge(m5, {> 90}), count == 2), < 0.04);
        }

    
	{
		@ "M5.S.2: Minimum m5 spacing when widht is > 0.2 must be 0.06";
		external1 (m5_w_0_20_and_more , distance < 0.06 ,extension = RADIAL, relational = POINT_TOUCH);
	}
	
	{
		@ "M5.S.2.1: Minimum m5 spacing when widht =0.16 must be 0.06";
		external1 (m5_w_0_16 , distance < 0.06 ,extension = RADIAL, relational = POINT_TOUCH);
	}
	  
    	m5_w_008 =wide(m5, distance > 0.08);
    	m5_w_07 = not ( m5, internal1 ( m5 , distance <0.7 ,extension = RADIAL, relational = POINT_TOUCH ) );	
    	
	{
	    	@ "M5.S.3.1: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.06 must be 0.06"; 
	    	external2(m5_w_008 , m5, distance < 0.06, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M5.S.3.2: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.08 must be 0.065"; 
	    	external2(m5_w_008 , not ( m5, m5_w_0_06), distance < 0.065, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M5.S.3.3: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.1 must be 0.075"; 
	    	external2(m5_w_008 , not ( not ( m5, m5_w_0_06), m5_w_0_08), distance < 0.075, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
{
	    	@ "M5.S.3.4: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.12 must be 0.1"; 
	    	external2(m5_w_008 , not( not ( not ( m5, m5_w_0_06), m5_w_0_08), m5_w_0_10), distance < 0.1, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M5.S.4.1: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0 must be 0.17"; 
	    	external2(m5_w_07 , m5, distance < 0.17, extension = NONE,projection_length > 0.17, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M5.S.4.2: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0.10 must be 0.18"; 
	    	external2(m5_w_07 , not ( not ( m5, m5_w_0_06), m5_w_0_08), distance < 0.18, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M5.S.4.3: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0.2 must be 0.19"; 
	    	external2(m5_w_07 , m5_w_0_20_and_more, distance < 0.19, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M5.S.4.4: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0.7 must be 0.17"; 
	    	external1(m5_w_07 ,  distance < 0.17, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	


/********************** END M5 rules*****************/

//***********************************************   M6 RULES 

	m6_w_0_06 = internal1 ( m6 , distance = 0.06 ,extension = RADIAL, relational = POINT_TOUCH );
	m6_w_0_08 = internal1 ( m6 , distance = 0.08 ,extension = RADIAL, relational = POINT_TOUCH );
	m6_w_0_10 = internal1 ( m6 , distance = 0.10 ,extension = RADIAL, relational = POINT_TOUCH );
	m6_w_0_12 = internal1 ( m6 , distance = 0.12 ,extension = RADIAL, relational = POINT_TOUCH );
	m6_w_0_16 = internal1 ( m6 , distance = 0.16 ,extension = RADIAL, relational = POINT_TOUCH );	
	m6_w_0_20_and_more = not ( not (not( not( not( m6,m6_w_0_16 ),m6_w_0_12 ),m6_w_0_10 ),m6_w_0_08) ,m6_w_0_06);	
	{
		@ "M6.W.1: M6 width must be  0.06 , 0.08 , 0.10, 0.12, 0.16 or > 0.2"; 
		internal1 ( m6_w_0_20_and_more , distance < 0.2 ,extension = RADIAL, relational = POINT_TOUCH );
	}

	{
		@ "M6.W.2: Maximum M6 width must be 3"; 
		wide (m6,distance > 3);
	}

	{
		@ "M6.S.1: Minimum M6 spacing must be 0.04";
		external1 ( m6 , distance < 0.04 ,extension = RADIAL, relational = POINT_TOUCH);
	}


	{
                @ "M6.S.1.2 Minimum notch must be 0.04";
		length_edge(interacting_edge(m6, vertex_edge(m6, {> 90}), count == 2), < 0.04);
        }

    
	{
		@ "M6.S.2: Minimum M6 spacing when widht is > 0.2 must be 0.06";
		external1 (m6_w_0_20_and_more , distance < 0.06 ,extension = RADIAL, relational = POINT_TOUCH);
	}
	
	{
		@ "M6.S.2.1: Minimum M6 spacing when widht =0.16 must be 0.06";
		external1 (m6_w_0_16 , distance < 0.06 ,extension = RADIAL, relational = POINT_TOUCH);
	}
	  
    	m6_w_008 =wide(m5, distance > 0.08);
    	m6_w_07 = not ( m6, internal1 ( m6 , distance <0.7 ,extension = RADIAL, relational = POINT_TOUCH ) );	
    	
	{
	    	@ "M6.S.3.1: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.06 must be 0.06"; 
	    	external2(m6_w_008 , m6, distance < 0.06, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M6.S.3.2: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.08 must be 0.065"; 
	    	external2(m6_w_008 , not ( m6, m6_w_0_06), distance < 0.065, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M6.S.3.3: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.1 must be 0.075"; 
	    	external2(m6_w_008 , not ( not ( m6, m6_w_0_06), m6_w_0_08), distance < 0.075, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
{
	    	@ "M6.S.3.4: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.12 must be 0.1"; 
	    	external2(m6_w_008 , not( not ( not ( m6, m6_w_0_06), m6_w_0_08), m6_w_0_10), distance < 0.1, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M6.S.4.1: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0 must be 0.17"; 
	    	external2(m6_w_07 , m6, distance < 0.17, extension = NONE,projection_length > 0.17, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M6.S.4.2: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0.10 must be 0.18"; 
	    	external2(m6_w_07 , not ( not ( m6, m6_w_0_06), m6_w_0_08), distance < 0.18, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M6.S.4.3: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0.2 must be 0.19"; 
	    	external2(m6_w_07 , m6_w_0_20_and_more, distance < 0.19, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M6.S.4.4: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0.7 must be 0.17"; 
	    	external1(m6_w_07 ,  distance < 0.17, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	


/********************** END M6 rules*****************/

//***********************************************   M7 RULES 

	m7_w_0_06 = internal1 ( m7 , distance = 0.06 ,extension = RADIAL, relational = POINT_TOUCH );
	m7_w_0_08 = internal1 ( m7 , distance = 0.08 ,extension = RADIAL, relational = POINT_TOUCH );
	m7_w_0_10 = internal1 ( m7 , distance = 0.10 ,extension = RADIAL, relational = POINT_TOUCH );
	m7_w_0_12 = internal1 ( m7 , distance = 0.12 ,extension = RADIAL, relational = POINT_TOUCH );
	m7_w_0_16 = internal1 ( m7 , distance = 0.16 ,extension = RADIAL, relational = POINT_TOUCH );	
	m7_w_0_20_and_more = not ( not (not( not( not( m7,m7_w_0_16 ),m7_w_0_12 ),m7_w_0_10 ),m7_w_0_08) ,m7_w_0_06);	
	{
		@ "M7.W.1: M7 width must be  0.06 , 0.08 , 0.10, 0.12, 0.16 or > 0.2"; 
		internal1 ( m7_w_0_20_and_more , distance < 0.2 ,extension = RADIAL, relational = POINT_TOUCH );
	}

	{
		@ "M7.W.2: Maximum M7 width must be 3"; 
		wide (m7,distance > 3);
	}

	{
		@ "M7.S.1: Minimum M7 spacing must be 0.04";
		external1 ( m7 , distance < 0.04 ,extension = RADIAL, relational = POINT_TOUCH);
	}


	{
                @ "M7.S.1.2 Minimum notch must be 0.04";
		length_edge(interacting_edge(m7, vertex_edge(m7, {> 90}), count == 2), < 0.04);
        }

    
	{
		@ "M7.S.2: Minimum M7 spacing when widht is > 0.2 must be 0.06";
		external1 (m7_w_0_20_and_more , distance < 0.06 ,extension = RADIAL, relational = POINT_TOUCH);
	}
	
	{
		@ "M7.S.2.1: Minimum M7 spacing when widht =0.16 must be 0.06";
		external1 (m7_w_0_16 , distance < 0.06 ,extension = RADIAL, relational = POINT_TOUCH);
	}
	  
    	m7_w_008 =wide(m5, distance > 0.08);
    	m7_w_07 = not ( m7, internal1 ( m7 , distance <0.7 ,extension = RADIAL, relational = POINT_TOUCH ) );	
    	
	{
	    	@ "M7.S.3.1: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.06 must be 0.06"; 
	    	external2(m7_w_008 , m7, distance < 0.06, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M7.S.3.2: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.08 must be 0.065"; 
	    	external2(m7_w_008 , not ( m7, m7_w_0_06), distance < 0.065, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M7.S.3.3: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.1 must be 0.075"; 
	    	external2(m7_w_008 , not ( not ( m7, m7_w_0_06), m7_w_0_08), distance < 0.075, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
{
	    	@ "M7.S.3.4: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.12 must be 0.1"; 
	    	external2(m7_w_008 , not( not ( not ( m7, m7_w_0_06), m7_w_0_08), m7_w_0_10), distance < 0.1, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M7.S.4.1: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0 must be 0.17"; 
	    	external2(m7_w_07 , m7, distance < 0.17, extension = NONE,projection_length > 0.17, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M7.S.4.2: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0.10 must be 0.18"; 
	    	external2(m7_w_07 , not ( not ( m7, m7_w_0_06), m7_w_0_08), distance < 0.18, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M7.S.4.3: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0.2 must be 0.19"; 
	    	external2(m7_w_07 , m7_w_0_20_and_more, distance < 0.19, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M7.S.4.4: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0.7 must be 0.17"; 
	    	external1(m7_w_07 ,  distance < 0.17, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	

	


/********************** END M7 rules*****************/

//***********************************************   M8 RULES 

	m8_w_0_06 = internal1 ( m8 , distance = 0.06 ,extension = RADIAL, relational = POINT_TOUCH );
	m8_w_0_08 = internal1 ( m8 , distance = 0.08 ,extension = RADIAL, relational = POINT_TOUCH );
	m8_w_0_10 = internal1 ( m8 , distance = 0.10 ,extension = RADIAL, relational = POINT_TOUCH );
	m8_w_0_12 = internal1 ( m8 , distance = 0.12 ,extension = RADIAL, relational = POINT_TOUCH );
	m8_w_0_16 = internal1 ( m8 , distance = 0.16 ,extension = RADIAL, relational = POINT_TOUCH );	
	m8_w_0_20_and_more = not ( not (not( not( not( m8,m8_w_0_16 ),m8_w_0_12 ),m8_w_0_10 ),m8_w_0_08) ,m8_w_0_06);	
	{
		@ "M8.W.1: M8 width must be  0.06 , 0.08 , 0.10, 0.12, 0.16 or > 0.2"; 
		internal1 ( m8_w_0_20_and_more , distance < 0.2 ,extension = RADIAL, relational = POINT_TOUCH );
	}

	{
		@ "M8.W.2: Maximum M8 width must be 3"; 
		wide (m8,distance > 3);
	}

	{
		@ "M8.S.1: Minimum M8 spacing must be 0.04";
		external1 ( m8 , distance < 0.04 ,extension = RADIAL, relational = POINT_TOUCH);
	}


	{
                @ "M8.S.1.2 Minimum notch must be 0.04";
		length_edge(interacting_edge(m8, vertex_edge(m8, {> 90}), count == 2), < 0.04);
        }

    
	{
		@ "M8.S.2: Minimum M8 spacing when widht is > 0.2 must be 0.06";
		external1 (m8_w_0_20_and_more , distance < 0.06 ,extension = RADIAL, relational = POINT_TOUCH);
	}
	
	{
		@ "M8.S.2.1: Minimum M8 spacing when widht =0.16 must be 0.06";
		external1 (m8_w_0_16 , distance < 0.06 ,extension = RADIAL, relational = POINT_TOUCH);
	}
	  
    	m8_w_008 =wide(m5, distance > 0.08);
    	m8_w_07 = not ( m8, internal1 ( m8 , distance <0.7 ,extension = RADIAL, relational = POINT_TOUCH ) );	
    	
	{
	    	@ "M8.S.3.1: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.06 must be 0.06"; 
	    	external2(m8_w_008 , m8, distance < 0.06, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M8.S.3.2: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.08 must be 0.065"; 
	    	external2(m8_w_008 , not ( m8, m8_w_0_06), distance < 0.065, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M8.S.3.3: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.1 must be 0.075"; 
	    	external2(m8_w_008 , not ( not ( m8, m8_w_0_06), m8_w_0_08), distance < 0.075, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
{
	    	@ "M8.S.3.4: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.12 must be 0.1"; 
	    	external2(m8_w_008 , not( not ( not ( m8, m8_w_0_06), m8_w_0_08), m8_w_0_10), distance < 0.1, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M8.S.4.1: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0 must be 0.17"; 
	    	external2(m8_w_07 , m8, distance < 0.17, extension = NONE,projection_length > 0.17, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M8.S.4.2: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0.10 must be 0.18"; 
	    	external2(m8_w_07 , not ( not ( m8, m8_w_0_06), m8_w_0_08), distance < 0.18, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M8.S.4.3: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0.2 must be 0.19"; 
	    	external2(m8_w_07 , m8_w_0_20_and_more, distance < 0.19, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M8.S.4.4: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0.7 must be 0.17"; 
	    	external1(m8_w_07 ,  distance < 0.17, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	
	


/********************** END M8 rules*****************/

//***********************************************   M9 RULES 

	m9_w_0_06 = internal1 ( m9 , distance = 0.06 ,extension = RADIAL, relational = POINT_TOUCH );
	m9_w_0_08 = internal1 ( m9 , distance = 0.08 ,extension = RADIAL, relational = POINT_TOUCH );
	m9_w_0_10 = internal1 ( m9 , distance = 0.10 ,extension = RADIAL, relational = POINT_TOUCH );
	m9_w_0_12 = internal1 ( m9 , distance = 0.12 ,extension = RADIAL, relational = POINT_TOUCH );
	m9_w_0_16 = internal1 ( m9 , distance = 0.16 ,extension = RADIAL, relational = POINT_TOUCH );	
	m9_w_0_20_and_more = not ( not (not( not( not( m9,m9_w_0_16 ),m9_w_0_12 ),m9_w_0_10 ),m9_w_0_08) ,m9_w_0_06);	
	{
		@ "M9.W.1: M9 width must be  0.06 , 0.08 , 0.10, 0.12, 0.16 or > 0.2"; 
		internal1 ( m9_w_0_20_and_more , distance < 0.2 ,extension = RADIAL, relational = POINT_TOUCH );
	}

	{
		@ "M9.W.2: Maximum M9 width must be 3"; 
		wide (m9,distance > 3);
	}

	{
		@ "M9.S.1: Minimum M9 spacing must be 0.04";
		external1 ( m9 , distance < 0.04 ,extension = RADIAL, relational = POINT_TOUCH);
	}


	{
                @ "M9.S.1.2 Minimum notch must be 0.04";
		length_edge(interacting_edge(m9, vertex_edge(m9, {> 90}), count == 2), < 0.04);
        }

    
	{
		@ "M9.S.2: Minimum M9 spacing when widht is > 0.2 must be 0.06";
		external1 (m9_w_0_20_and_more , distance < 0.06 ,extension = RADIAL, relational = POINT_TOUCH);
	}
	
	{
		@ "M9.S.2.1: Minimum M9 spacing when widht =0.16 must be 0.06";
		external1 (m9_w_0_16 , distance < 0.06 ,extension = RADIAL, relational = POINT_TOUCH);
	}
	  
    	m9_w_008 =wide(m5, distance > 0.08);
    	m9_w_07 = not ( m9, internal1 ( m9 , distance <0.7 ,extension = RADIAL, relational = POINT_TOUCH ) );	
    	
	{
	    	@ "M9.S.3.1: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.06 must be 0.06"; 
	    	external2(m9_w_008 , m9, distance < 0.06, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M9.S.3.2: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.08 must be 0.065"; 
	    	external2(m9_w_008 , not ( m9, m9_w_0_06), distance < 0.065, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
	{
	    	@ "M9.S.3.3: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.1 must be 0.075"; 
	    	external2(m9_w_008 , not ( not ( m9, m9_w_0_06), m9_w_0_08), distance < 0.075, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}
{
	    	@ "M9.S.3.4: Minimum spacing if metal width of one of lines > 0.08 and their parallel run length > 0.08 from metal widght >= 0.12 must be 0.1"; 
	    	external2(m9_w_008 , not( not ( not ( m9, m9_w_0_06), m9_w_0_08), m9_w_0_10), distance < 0.1, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M9.S.4.1: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0 must be 0.17"; 
	    	external2(m9_w_07 , m9, distance < 0.17, extension = NONE,projection_length > 0.17, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M9.S.4.2: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0.10 must be 0.18"; 
	    	external2(m9_w_07 , not ( not ( m9, m9_w_0_06), m9_w_0_08), distance < 0.18, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M9.S.4.3: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0.2 must be 0.19"; 
	    	external2(m9_w_07 , m9_w_0_20_and_more, distance < 0.19, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	{
	    	@ "M9.S.4.4: Minimum spacing if metal width of one of lines > 0.7 and their parallel run length > 0.08 from metal widght >= 0.7 must be 0.17"; 
	    	external1(m9_w_07 ,  distance < 0.17, extension = NONE,projection_length > 0.08, orientation = PARALLEL, intersecting = {}, projection = IN, orthogonal = ALL,look_thru = ALL);
	}

	

	


/********************** END M9 rules*****************/




	

//***************************************      CTM1 RULES     *****************************/


	{
                @ "CTM1.W.1 Minimum horizontal width must be 0.03";
                internal1 ( ctm1, < 0.03 ,extension=RADIAL, relational = POINT_TOUCH, direction = HORIZONTAL );
        }

	{
		@"CTM1.W.2 Minimum vertical width is 0.05";
		internal1 ( ctm1, distance <0.05,extension=RADIAL, relational = POINT_TOUCH, direction = VERTICAL );
	}

	{	
		@ "CTM1.S.1: Minimum spacing must be 0.044"; 
		external1 ( ctm1 , distance < 0.044 ,extension = RADIAL, relational = POINT_TOUCH);
	}

	{
		@ "CTM1.S.2: Minimum spacing between same masks must be 0.07"; 
		external1 ( ctm1_1 , distance < 0.07 ,extension = RADIAL, relational = POINT_TOUCH);
		external1 ( ctm1_2 , distance < 0.07 ,extension = RADIAL, relational = POINT_TOUCH);
	}

	ctm1_s3_1 = diff not axpoly;
	ctm1_s3_2 = ctm1 and ctm1_s3_1;
	ctm1_s3_3 = ctm1 and diff;

	{
		@ "CTM1.S.3: CTM1 over (DIFF not AXPOLY) minimum space to PO (touching is not allowed)"; 
		external2(po, ctm1_s3_3, distance < 0.015, extension = RADIAL, intersecting = TOUCH);
	}
	{
                @ "CTM1.S.4: Minimum space of CTM1 to (PO centerline over CPO) 0.02. Touching is not allowed";
		center_to_center2(ctm1, (po and cpo), distance < 0.02);
        }
	{
                @ "CTM1.S.5: Minimum spacing from CTM1 to TSLO must be 0.02";
                external2(ctm1, tslco, distance < 0.02,extension = RADIAL);

        }
		diff_and_fincut=and(diff,fincut);

        {
                @ "CTM1.O.1 Minimum vertical overlap, DIFF over FINCUT must be 0.04";
		ctm1_diff_fincut = ctm1 and diff_and_fincut;
                internal2(ctm1_diff_fincut, diff, distance < 0.04,extension=RADIAL,relational={POINT_TOUCH},direction = VERTICAL);
        }
	{
		@"CTM1.O.2 (CTM1 over (DIFF_15 or DIFF_18) minimum horizontal overlap of (DIFF not FINCUT) 0.05";
		diff_all = diff_15 or diff_18;
		diff_not_fincut = diff not fincut;
		internal1((ctm1 and diff_all) and diff_not_fincut, distance < 0.05,extension=RADIAL,relational={POINT_TOUCH},direction = VERTICAL);
	}
	{
		@"CTM1.O.3: Minimum vertical overlap of TSLO not TSLB: 0.04";
		ctm1_tslco_tslcb = ctm1 and (tslco not tslcb);
		internal1(ctm1_tslco_tslcb, distance < 0.04,extension=RADIAL,relational={POINT_TOUCH},direction = VERTICAL);
	}

	{
		@ "CTM1.A.1: Minimum area must be 0.0008"; 
		area ( ctm1 , value < 0.0008 );	
	}

	{
		@ "CTM1.C.1: CTM1 must be orthogonal rectangle"; 
		not_rectangles(ctm1, orientation=ORTHOGONAL);
	}

	
	ctm1_c2_2 = diff not fincut;
	ctm1_c2_3 = ctm1 and ctm1_c2_2;
/*	
	{
		@ "CTM1.C.2:CTM1 over (DIFF not FINCUT) must touch TSLO"; 
		not_interacting (ctm1_c2_3, tslco);
	}
*/

// ? - 
//	po_c3_1 = po not axpoly;
//	{
//		@ "CTM1.C.3: CTM1 over gate is not allowed"; 
//		and(ctm1, po_c3_1);
//
//	}	


/******************** CPO rules *******************************/

	{
                @ "CPO.W.1 Exact vertical width must be 0.04";
                correct = internal1 ( cpo, distance == 0.04 ,extension=RADIAL, relational = POINT_TOUCH, direction = VERTICAL );
                cpo not_interacting correct;
        }

	{
                @"CPO.W.2 Minimum horizontal width is 0.04";
                internal1 ( cpo, distance <0.04,extension=RADIAL, relational = POINT_TOUCH, direction = HORIZONTAL );
        }
	{
		@"CPO.W.3 Maximum horizontal width 13";
		correct = internal1 ( cpo, distance <=13,extension=RADIAL, relational = POINT_TOUCH, direction = HORIZONTAL );
		cpo not_interacting correct;
	}

	{

                @ "CPO.S.1: Minimum space must be 0.04";
                external1(cpo_union, distance < 0.04,extension = RADIAL, relational = POINT_TOUCH);
        }
	{
                @ "CPO.S.2: Minimum space (same mask) must be 0.04";
                external1 ( cpo_1 , distance < 0.04 ,extension = RADIAL, relational = POINT_TOUCH, direction = VERTICAL);
                external1 ( cpo_2 , distance < 0.04 ,extension = RADIAL, relational = POINT_TOUCH, direction = VERTICAL);
                external1 ( cpo , distance < 0.04 ,extension = RADIAL, relational = POINT_TOUCH, direction = VERTICAL);
        }
	{
                @ "CPO.S.3: Minimum space (same mask) must be 0.04";
                external1 ( cpo_1 , distance < 0.04 ,extension = RADIAL, relational = POINT_TOUCH, direction = HORIZONTAL);
                external1 ( cpo_2 , distance < 0.04 ,extension = RADIAL, relational = POINT_TOUCH, direction = HORIZONTAL);
                external1 ( cpo , distance < 0.04 ,extension = RADIAL, relational = POINT_TOUCH, direction = HORIZONTAL);
        }

/*	{
                @ "CPO.S.4: Minimum space for run length <= 0 (same mask) must be 0.09";
                external1(cpo, distance < 0.09, extension = NONE,projection_length > 0, orientation = PARALLEL, orthogonal = ALL,look_thru = ALL); // must be checked
        }*/
	{
                @ "CPO.S.5: Minimum space to DIFF not FINCUT must be 0.03";
                external2(cpo, (diff not diffcut), distance < 0.03,extension = RADIAL);
        }
	{
                @ "CPO.S.6: Minimum space to (DIFF_15 or DIFF_18) must be 0.03";
                external2(cpo, (diff_15 or diff_18), distance < 0.03,extension = RADIAL);
        }
	{
                @ "CPO.S.7: CPO minimum space to PO for different nets";
                external2(cpo, po, distance < 0.025,extension = RADIAL, connectivity =  DIFFERENT_NET, connect_sequence = cdb1);
        }

	cpo_s8_1 = diff_15 or diff_18;
        cpo_s8_2 = length_edge(cpo_s8_1, >0);
        cpo_s8_3 = touching (po, cpo_s8_2);
	
	cdb1 = incremental_connect(cdb1, {{{po}, cpo_s8_3}});
	
        {
                @ "CPO.S.8: CPO Minimum space to PO touching (DIFF_15 or DIFF_18) for different nets must be 0.04";
                external2(cpo, cpo_s8_3, distance < 0.04,extension = RADIAL, connectivity =  DIFFERENT_NET, connect_sequence = cdb1);
        }
	{
                @ "CPO.O.1: Minimum vertical overlap of (PO not axpoly) must be 0.04";
                internal2 ( cpo , (po not axpoly), distance < 0.04, extension=RADIAL, direction = VERTICAL );
        }

	{
                @ "CPO.C.1: CPO must be orthogonal rectangle";
                not_rectangles(cpo, orientation=ORTHOGONAL);
        }
	 {
                @ "CPO.C.2: CPO touching (DIFF not FINCUT) is not allowed";
                interacting(cpo, (diff not fincut));
        }	
	{
                @ "CPO.C.3: CTM1 over gate is not allowed";
                and(cpo, gate);
        }

/************* CPO orientation rule ************************/

get_vertical_oriented_cpo : function (void) returning void
        {

                prim = df_get_current_data();
                prim_edges = df_edge_layer(prim, "cpo_edges");
                hl = df_edge_horizontal_length(prim_edges, 0);
                vl = df_edge_vertical_length(prim_edges, 1);

        if (hl < vl)
                {
                        df_save_data(prim);
                }
        }


{
                @"CPO.C.4: CPO must be horizontally oriented";

        cpo_edges = length_edge(cpo, >0);
        drc_features(
                primary_layer = cpo,
                secondary_layers = {"cpo_edges"=> cpo_edges},
                drc_function = get_vertical_oriented_cpo,
                output_from_layer = cpo,
                error_shape = REGION
                    );
}





/********************************************************/

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

/*********************************************************/



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
	@ "HVTIMP.W.1: HVTIMP minimum widht must be 0.074"; 
	internal1(hvtimp, distance < 0.074, extension = RADIAL);
}
{
	@ "HVTIMP.S.1: HVTIMP minimum spacing must be 0.074"; 
	external1 (hvtimp, distance < 0.074, extension = RADIAL);
}
/*{
	@ "HVTIMP.E.1: Minimum enclosure must be 0.05"; 
	enclose (diff, hvtimp, distance < 0.05, extension = RADIAL, intersecting = {TOUCH}, relational = {POINT_TOUCH, INSIDE});
}
*/
//*******************************LVTIMP Rules****************************************************************
{
	@ "LVTIMP.W.1: LVTIMP minimum widht must be 0.074"; 
	internal1(lvtimp, distance < 0.074,extension = RADIAL);
}
{
	@ "LVTIMP.S.1: LVTIMP minimum spacing must be 0.074"; 
	external1 (lvtimp, distance < 0.074, extension = RADIAL);
}
/*{
	@ "LVTIMP.E.1: Minimum enclosure must be 0.05"; 
	enclose (diff, lvtimp, distance < 0.05, extension = RADIAL, intersecting = {TOUCH}, relational = {POINT_TOUCH, INSIDE});
}
*/


//*********************************VIA0 Rules**************************************************

    via0sq  = rectangles (via0, {0.03,0.03});
    via0lg  = rectangles (via0, {0.06,0.06});
    via0bar = rectangles (via0, {0.03,0.06});

	{
		@ "VIA0.W.1: Exact length and width of VIA0 must be 0.03"; 
		not_rectangles ( (via0 not_interacting (via0lg or via0bar)) ,sides= {0.03,0.03} );
	}

	{
		@ "VIA0.W.2 and VIA0.W.2a: VIA0 must be rectangular with length 0.06 and width 0.03"; 
		not_interacting(via0 not_interacting (via0sq or via0lg), via0bar);
	}	

	{
		@ "VIA0.S.1: Minimum VIA0 center to center spacing must be 0.074"; 
		center_to_center1 (via0, distance < 0.074);
	}

	{
		@ "VIA0.S.2: Minimum spacing of VIA0 to VIA1BAR must be 0.05"; 
		external2 (via0, via0bar, distance < 0.05, extension = RADIAL, relational = POINT_TOUCH);
	}

	{
		@ "VIA0.E.1: Minimum VIA0 enclosure by M1 must be 0.002"; 
		enclose (via0, m1, distance < 0.002, extension = RADIAL, intersecting = TOUCH, relational = INSIDE);
	}

	{
		@ "VIA0_3.E.2: Minimum VIA0 enclosure by M1_3 must be 0.002"; 						    /* poxac */
		enclose (via0, m1_3, distance < 0.002, extension = RADIAL, intersecting = TOUCH, relational = INSIDE);	    /* poxac */
	}

	{
		@ "VIA0.C.1: VIA0, VIA0BAR must be orthogonal rectangle"; 
		not_rectangles(via0 or via0bar, orientation=ORTHOGONAL);
	}

m1_v = wide (m1, > 0.2);
m1_3_v = wide (m1_3, > 0.2);	/* poxac */

m1_w_01 = interacting(m1_v,via0);
m1_3_w_01 = interacting(m1_3_v,via0);	/* poxac */
cpo_w_01 = interacting(cpo,via0);
ctm1_w_01 = interacting(ctm1,via0);



r2 = external1 (via0sq, <= 0.15, extension = RADIAL);
r2_e = interacting (r2,via0sq,count > 1);
r2_v = interacting (via0sq, r2_e);

r3 =external1 (via0lg, <= 0.15, extension = RADIAL);
r3_e =interacting(r3,via0lg,count > 1);
r3_v =interacting (via0lg, r3_e);

{
	@ "VIA0.R.1: When M1 width > 0.2, it is a must to have redundant VIAs (At least one rectangular VIAx, At least two  square VIAx with spacing <=0.15umn)"; 
	not(m1_w_01,((interacting (m1_w_01, via0bar, count >= 1)) or (interacting (m1_w_01, r2_v, count >= 1)) or (interacting(cpo_w_01,r3_v, count >=1 ))));
	not(m1_w_01,((interacting (m1_w_01, via0bar, count >= 1)) or (interacting (m1_w_01, r2_v, count >= 1)) or (interacting(ctm1_w_01,r3_v, count >=1 ))));
}

	/* poxac */ // skizb	
{
	@ "VIA0_3.R.1: When M1_3 width > 0.2, it is a must to have redundant VIAs (At least one rectangular VIAx, At least two  square VIAx with spacing <=0.15umn)"; 
	not(m1_3_w_01,((interacting (m1_3_w_01, via0bar, count >= 1)) or (interacting (m1_3_w_01, r2_v, count >= 1)) or (interacting(cpo_w_01,r3_v, count >=1 ))));
	not(m1_3_w_01,((interacting (m1_3_w_01, via0bar, count >= 1)) or (interacting (m1_3_w_01, r2_v, count >= 1)) or (interacting(ctm1_w_01,r3_v, count >=1 ))));
}

	/* poxac */ // verj

//***************************************      VIA1 RULES     *****************************/
    via1sq  = rectangles (via1, {0.03,0.03});
    via1lg  = rectangles (via1, {0.06,0.06});
    via1bar = rectangles (via1, {0.03,0.06});
{
        @ "VIA1.W.1 VIA1.W.2 VIA1.W.3 VIA1.W.4: VIA1 must be square with 0.03 or 0.06 width and length or VIA1 must be rectangular with length 0.06 and width 0.03";
        not(via1,(via1sq or via1lg or via1bar));
}


{
        @ "VIA1.S.1: Minimum center to center spacing of VIA1SQ to VIA1SQ: 0.074";
        center_to_center1( via1sq , distance < 0.074 );
}
{
        @ "VIA1.S.2: Minimum spacing of VIA1SQ to VIA1BAR or VIA1LG  must be 0.08";
        external2 (via1sq, via1bar or via1lg, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
        @ "VIA1.S.3: Minimum spacing of VIA1BAR or VIA1LG to VIA1BAR or VIA1LG must be 0.08";
        external1(via1bar or via1lg, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}

{
        @ "VIA1.E.1: Minimum VIA1 enclosure by M1 and M2 must be  0.002";
        enclose ( via1 , m1 and m2 , distance < 0.002 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
}

	/* poxac */ //skizb 
{
        @ "VIA1.E.1.1: Minimum VIA1 enclosure by M1_3 and M2 must be  0.002";
        enclose ( via1 , m1_3 and m2 , distance < 0.002 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
}
	/* poxac */ //verj


	/* poxac2 */ //skizb
{
        @ "VIA1.E.1: Minimum VIA1 enclosure by M1 and M2_3 must be  0.002";
        enclose ( via1 , m1 and m2_3 , distance < 0.002 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
}
	/* poxac2 */ //verj

	/* poxac2 */ //skizb
{
        @ "VIA1.E.1: Minimum VIA1 enclosure by M1_3 and M2_3 must be  0.002";
        enclose ( via1 , m1_3 and m2_3 , distance < 0.002 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
}
	/* poxac2 */ //verj

{
        @ "VIA1.B.2: VIA1 must be covered by (M1 or M1_3) and (M2 or M2_3), min. enclosure is 0.003um";
        //not ( via1 , m1 );
	not ( via1 , m1_3 or m1);	/*added*/
        //not ( via1 , m2 );
	not ( via1 , m2_3 or m2);	/*added*/
}

	m1or = or(m1,m1_3);
	m2or = or(m2,m2_3);
{
	@ "VIA1.E.2: Minimum VIA1BAR enclosure by (M1 or M1_3) and (M2 or M2_3) at end-of-line must be 0.003";


	not_covered_by(via1bar,m1or,distances = {{{0.003,extension = NONE},{0, extension = NONE},
					 {0.003,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.003, extension = NONE},
					 {0,extension = NONE},{0.003,extension = NONE}}},
					 intersecting = {TOUCH});

//	not_covered_by(via1bar,m1_3,distances = {{{0.005,extension = NONE},{0, extension = NONE},	/*added*/
/*					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH}); 
*/
	
	not_covered_by(via1bar,m2or,distances = {{{0.003,extension = NONE},{0, extension = NONE},
					 {0.003,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.003, extension = NONE},
					 {0,extension = NONE},{0.003,extension = NONE}}},
					 intersecting = {TOUCH});

//	not_covered_by(via1bar,m2_3,distances = {{{0.005,extension = NONE},{0, extension = NONE},	/*added*/
/*					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});

*/

}


m1_v = wide (m1, > 0.2);
m2_v = wide (m2, > 0.2);

m1_w_01 = interacting(m1_v,via1);
m2_w_01 = interacting(m2_v,via1);

 /* poxac */ //skizb
m1_3_v = wide (m1_3, > 0.2);
m1_3_w_01 = interacting(m1_3_v,via1);
 /* poxac */ //verj


 /* poxac2 */ //skizb
m2_3_v = wide (m2_3, > 0.2);
m2_3_w_01 = interacting(m2_3_v,via1);

 /* poxac2 */ //verj

via1r2 = external1 (via1sq, <= 0.15, extension = RADIAL);
via1r2_e = interacting (via1r2,via1sq,count > 1);
via1r2_v =interacting (via1sq, via1r2_e);

via1r3 =external1 (via1lg, <= 0.15, extension = RADIAL);
via1r3_e =interacting(via1r3,via1lg,count > 1);
via1r3_v =interacting (via1lg, via1r3_e);

via1r4 = external1 (via1sq, <= 0.7,  extension = RADIAL);
via1r4_or = or(via1r4, via1sq);
via1r4_e = interacting (via1r4_or,via1sq,count>3);
via1r4_v = interacting ( via1sq,via1r4_e);
via1r5   = external1 (via1lg, <= 0.7,  extension = RADIAL);
via1r5_or = or(via1r5,via1lg);
via1r5_e = interacting (via1r5_or, via1lg,count >3);
via1r5_v = interacting (via1lg, via1r5_e);
/*
{
	@"VIA1.R.1: When M1 or M2 width >0.2um, it is a must to have redundant VIAs";
	not(m1_w_01,((interacting (m1_w_01, via1bar, count >= 1)) or (interacting (m1_w_01, via1r2_v, count >= 2)) or (interacting(m1_w_01,r3_v, count >=2 )) or (interacting(m1_w_01,via1r4_v, count >= 4)) or (interacting(m1_w_01,via1r5_v, count >= 4))));
}
*/

//***************************************      VIA2 RULES     *****************************/
    via2sq  = rectangles (via2, {0.03,0.03});
    via2lg  = rectangles (via2, {0.06,0.06});
    via2bar = rectangles (via2, {0.03,0.06});
{
        @ "VIA2.W.1 VIA2.W.2 VIA2.W.3 VIA2.W.4: VIA2 must be square with 0.03 or 0.06 width and length or VIA2 must be rectangular with length 0.06 and width 0.03";
        not(via2,(via2sq or via2lg or via2bar));
}


{
        @ "VIA2.S.1: Minimum center to center spacing of VIA2SQ to VIA2SQ: 0.074";
        center_to_center1( via2sq , distance < 0.074 );
}
{
        @ "VIA2.S.2: Minimum spacing of VIA2SQ to VIA2BAR or VIA2LG  must be 0.08";
        external2 (via2sq, via2bar or via2lg, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
        @ "VIA2.S.3: Minimum spacing of VIA2BAR or VIA2LG to VIA2BAR or VIA2LG must be 0.08";
        external1(via2bar or via2lg, distance < 0.08 , extension = RADIAL, relational = POINT_TOUCH);
}

{
        @ "VIA2.E.1: Minimum VIA2 enclosure by M2 and M3 must be  0.002";
        enclose ( via2 , m2 and m3 , distance < 0.002 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
}


/* poxac3 */ //skizb
{
        @ "VIA2.E.1: Minimum VIA2 enclosure by M2 and M3_3 must be  0.002";
        enclose ( via2 , m2 and m3_3 , distance < 0.002 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
}
/* poxac3 */ //verj

/* poxac2 */ //skizb
{
        @ "VIA2.E.1: Minimum VIA2 enclosure by M2_3 and M3 must be  0.002";
        enclose ( via2 , m2_3 and m3 , distance < 0.002 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
}
/* poxac2 */ //verj

/* poxac3 */ //skizb
{
        @ "VIA2.E.1: Minimum VIA2 enclosure by M2_3 and M3_3 must be  0.002";
        enclose ( via2 , m2_3 and m3_3 , distance < 0.002 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
}
/* poxac3 */ //verj

{
        @ "VIA2.B.2: VIA2 must be covered by (M2 or M2_3) and (M3 or M3_3)";
        //not ( via2 , m2 );
        not ( via2 , m2_3 or m2);	/*added*/
        //not ( via2 , m3 );
        not ( via2 , m3_3 or m3);	/*added*/

}
	m3or = or(m3,m3_3);
	m2or = or(m2,m2_3);

{
	@ "VIA2.E.2: Minimum VIA2BAR enclosure by (M2 or M2_3) and (M3 or M3_3) at end-of-line must be 0.003";


/*	not_covered_by(via2bar,m2,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});*/

	not_covered_by(via2bar,m2or,distances = {{{0.003,extension = NONE},{0, extension = NONE},       /*added*/
					 {0.003,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.003, extension = NONE},
					 {0,extension = NONE},{0.003,extension = NONE}}},
					 intersecting = {TOUCH});

	
/*	not_covered_by(via2bar,m3,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});*/

	not_covered_by(via2bar,m3or,distances = {{{0.003,extension = NONE},{0, extension = NONE},	/*added*/
					 {0.003,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.003, extension = NONE},
					 {0,extension = NONE},{0.003,extension = NONE}}},
					 intersecting = {TOUCH});


}


m2_v = wide (m2, > 0.2);
m3_v = wide (m3, > 0.2);

m2_w_01 = interacting(m2_v,via2);
m3_w_01 = interacting(m3_v,via2);

/* poxac2 */ //skizb
m2_3_v = wide (m2_3, > 0.2);
m2_3_w_01 = interacting(m2_3_v,via2);
/* poxac2 */ //verj				

/* poxac3 */ //skizb
m3_3_v = wide (m3_3, > 0.2);
m3_3_w_01 = interacting(m3_3_v,via2);
/* poxac3 */ //verj


via2r2 = external1 (via2sq, <= 0.15, extension = RADIAL);
via2r2_e = interacting (via2r2,via2sq,count > 1);
via2r2_v =interacting (via2sq, via2r2_e);

via2r3 =external1 (via2lg, <= 0.15, extension = RADIAL);
via2r3_e =interacting(via2r3,via2lg,count > 1);
via2r3_v =interacting (via2lg, via2r3_e);

via2r4 = external1 (via2sq, <= 0.7,  extension = RADIAL);
via2r4_or = or(via2r4, via2sq);
via2r4_e = interacting (via2r4_or,via2sq,count>3);
via2r4_v = interacting ( via2sq,via2r4_e);
via2r5   = external1 (via2lg, <= 0.7,  extension = RADIAL);
via2r5_or = or(via2r5,via2lg);
via2r5_e = interacting (via2r5_or, via2lg,count >3);
via2r5_v = interacting (via2lg, via2r5_e);
/*
{
	@"VIA2.R.1: When M2 or M3 width >0.2um, it is a must to have redundant VIAs";
	not(m2_w_01,((interacting (m2_w_01, via2bar, count >= 1)) or (interacting (m2_w_01, via2r2_v, count >= 2)) or (interacting(m2_w_01,via2r3_v, count >=2 )) or (interacting(m2_w_01,via2r4_v, count >= 4)) or (interacting(m2_w_01,via2r5_v, count >= 4))));
}
*/


//***************************************      VIA3 RULES     *****************************/
    via3sq  = rectangles (via3, {0.06,0.06});
    via3lg  = rectangles (via3, {0.12,0.12});
    via3bar = rectangles (via3, {0.12,0.06});
{
        @ "VIA3.W.1 VIA3.W.2 VIA3.W.3 VIA3.W.4: VIA3 must be square with 0.06 or 0.12 width and length or VIA3 must be rectangular with length 0.12 and width 0.06";
        not(via3,(via3sq or via3lg or via3bar));
}


{
        @ "VIA3.S.1: Minimum center to center spacing of VIA3SQ to VIA3SQ: 0.15";
        center_to_center1( via3sq , distance < 0.15 );
}
{
        @ "VIA3.S.2: Minimum spacing of VIA3SQ to VIA3BAR or VIA3LG  must be 0.08";
        external2 (via3sq, via3bar or via3lg, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
        @ "VIA3.S.3: Minimum spacing of VIA3BAR or VIA3LG to VIA3BAR or VIA3LG must be 0.085";
        external1(via3bar or via3lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}

{
        @ "VIA3.E.1: Minimum VIA3 enclosure by M3 and M4 must be  0.005";
        enclose ( via3 , m3 and m4 , distance < 0.005 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
}

/* poxac3 */ //skizb
{
        @ "VIA3.E.1: Minimum VIA3 enclosure by M3_3 and M4 must be  0.005";
        enclose ( via3 , m3_3 and m4 , distance < 0.005 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
}
/* poxac3 */ //verj

{
        @ "VIA3.B.2: VIA3 must be covered by (M3 or M3_3) and M4, min. enclosure is 0.003um";
        //not ( via3 , m3 );
        not ( via3 , m3_3 or m3);	/*added*/
        not ( via3 , m4 );
}
	m3or = or(m3,m3_3);

{
	@ "VIA3.E.2: Minimum VIA3BAR enclosure by (M3 or M3_3) and M4 at end-of-line must be 0.003";


/*	not_covered_by(via3bar,m3,distances = {{{0.005,extension = NONE},{0, extension = NONE},
					 {0.005,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.005, extension = NONE},
					 {0,extension = NONE},{0.005,extension = NONE}}},
					 intersecting = {TOUCH});*/

	not_covered_by(via3bar,m3or,distances = {{{0.003,extension = NONE},{0, extension = NONE}, /*added*/
					 {0.003,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.003, extension = NONE},
					 {0,extension = NONE},{0.003,extension = NONE}}},
					 intersecting = {TOUCH});

	
	not_covered_by(via3bar,m4,distances = {{{0.003,extension = NONE},{0, extension = NONE},
					 {0.003,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.003, extension = NONE},
					 {0,extension = NONE},{0.003,extension = NONE}}},
					 intersecting = {TOUCH});


}


m3_v = wide (m3, > 0.2);
m4_v = wide (m4, > 0.2);

m3_w_01 = interacting(m3_v,via3);
m4_w_01 = interacting(m4_v,via3);

/* poxac3 */ //skizb
m3_3_v = wide (m3_3, > 0.2);
m3_3_w_01 = interacting(m3_3_v,via3);
/* poxac3 */ //verj

via3r2 = external1 (via3sq, <= 0.15, extension = RADIAL);
via3r2_e = interacting (via3r2,via3sq,count > 1);
via3r2_v =interacting (via3sq, via3r2_e);

via3r3 =external1 (via3lg, <= 0.15, extension = RADIAL);
via3r3_e =interacting(via3r3,via3lg,count > 1);
via3r3_v =interacting (via3lg, via3r3_e);

via3r4 = external1 (via3sq, <= 0.7,  extension = RADIAL);
via3r4_or = or(via3r4, via3sq);
via3r4_e = interacting (via3r4_or,via3sq,count>3);
via3r4_v = interacting ( via3sq,via3r4_e);
via3r5   = external1 (via3lg, <= 0.7,  extension = RADIAL);
via3r5_or = or(via3r5,via3lg);
via3r5_e = interacting (via3r5_or, via3lg,count >3);
via3r5_v = interacting (via3lg, via3r5_e);
/*
{
	@"VIA3.R.1: When M3 or M4 width >0.2um, it is a must to have redundant VIAs";
	not(m3_w_01,((interacting (m3_w_01, via3bar, count >= 1)) or (interacting (m3_w_01, via3r2_v, count >= 2)) or (interacting(m3_w_01,via3r3_v, count >=2 )) or (interacting(m3_w_01,via3r4_v, count >= 4)) or (interacting(m3_w_01,via3r5_v, count >= 4))));
}
*/

//***************************************      VIA4 RULES     *****************************/
    via4sq  = rectangles (via4, {0.06,0.06});
    via4lg  = rectangles (via4, {0.12,0.12});
    via4bar = rectangles (via4, {0.12,0.06});
{
        @ "VIA4.W.1 VIA4.W.2 VIA4.W.3 VIA4.W.4: VIA4 must be square with 0.06 or 0.12 width and length or VIA4 must be rectangular with length 0.12 and width 0.06";
        not(via4,(via4sq or via4lg or via4bar));
}
/*
{
        @ "print via4";
        copy(via4);
}


{
        @ "print via4bar";
	copy(via4bar);
}

{
	@ "print via4lg";
	copy(via4lg);


}

*/

{
        @ "VIA4.S.1: Minimum center to center spacing of VIA4SQ to VIA4SQ: 0.15";
        center_to_center1( via4sq , distance < 0.15 );
}
{
        @ "VIA4.S.2: Minimum spacing of VIA4SQ to VIA4BAR or VIA4LG  must be 0.08";
        external2 (via4sq, via4bar or via4lg, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
        @ "VIA4.S.3: Minimum spacing of VIA4BAR or VIA4LG to VIA4BAR or VIA4LG must be 0.085";
        external1(via4bar or via4lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}

{
        @ "VIA4.E.1: Minimum VIA4 enclosure by M4 and M5 must be  0.005";
        enclose ( via4 , m4 and m5 , distance < 0.005 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
}
{
        @ "VIA4.B.2: VIA4 must be covered by M4 and M5, min. enclosure is 0.005um";
        not ( via4 , m4 );
        not ( via4 , m5 );
}


{
	@ "VIA4.E.2: Minimum VIA4BAR enclosure by M4 and M5 at end-of-line must be 0.003";


	not_covered_by(via4bar,m4,distances = {{{0.003,extension = NONE},{0, extension = NONE},
					 {0.003,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.003, extension = NONE},
					 {0,extension = NONE},{0.003,extension = NONE}}},
					 intersecting = {TOUCH});

	
	not_covered_by(via4bar,m5,distances = {{{0.003,extension = NONE},{0, extension = NONE},
					 {0.003,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.003, extension = NONE},
					 {0,extension = NONE},{0.003,extension = NONE}}},
					 intersecting = {TOUCH});


}


m4_v = wide (m4, > 0.2);
m5_v = wide (m5, > 0.2);

m4_w_01 = interacting(m4_v,via4);
m5_w_01 = interacting(m5_v,via4);



via4r2 = external1 (via4sq, <= 0.15, extension = RADIAL);
via4r2_e = interacting (via4r2,via4sq,count > 1);
via4r2_v =interacting (via4sq, via4r2_e);

via4r3 =external1 (via4lg, <= 0.15, extension = RADIAL);
via4r3_e =interacting(via4r3,via4lg,count > 1);
via4r3_v =interacting (via4lg, via4r3_e);

via4r4 = external1 (via4sq, <= 0.7,  extension = RADIAL);
via4r4_or = or(via4r4, via4sq);
via4r4_e = interacting (via4r4_or,via4sq,count>3);
via4r4_v = interacting ( via4sq,via4r4_e);
via4r5   = external1 (via4lg, <= 0.7,  extension = RADIAL);
via4r5_or = or(via4r5,via4lg);
via4r5_e = interacting (via4r5_or, via4lg,count >3);
via4r5_v = interacting (via4lg, via4r5_e);

/*
{
	@"VIA4.R.1: When M4 or M5 width >0.2um, it is a must to have redundant VIAs";
	not(m4_w_01,((interacting (m4_w_01, via4bar, count >= 1)) or (interacting (m4_w_01, via4r2_v, count >= 2)) or (interacting(m4_w_01,via4r3_v, count >=2 )) or (interacting(m4_w_01,via4r4_v, count >= 4)) or (interacting(m4_w_01,via4r5_v, count >= 4))));
}
*/

//***************************************      VIA5 RULES     *****************************/
    via5sq  = rectangles (via5, {0.06,0.06});
    via5lg  = rectangles (via5, {0.12,0.12});
    via5bar = rectangles (via5, {0.12,0.06});
{
        @ "VIA5.W.1 VIA5.W.2 VIA5.W.3 VIA5.W.4: VIA5 must be square with 0.03 or 0.07 width and length or VIA5 must be rectangular with length 0.06 and width 0.03";
        not(via5,(via5sq or via5lg or via5bar));
}


{
        @ "VIA5.S.1: Minimum center to center spacing of VIA5SQ to VIA5SQ: 0.15";
        center_to_center1( via5sq , distance < 0.15 );
}
{
        @ "VIA5.S.2: Minimum spacing of VIA5SQ to VIA5BAR or VIA5LG  must be 0.08";
        external2 (via5sq, via5bar or via5lg, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
        @ "VIA5.S.3: Minimum spacing of VIA5BAR or VIA5LG to VIA5BAR or VIA5LG must be 0.085";
        external1(via5bar or via5lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}

{
        @ "VIA5.E.1: Minimum VIA5 enclosure by M5 and M6 must be  0.005";
        enclose ( via5 , m5 and m6 , distance < 0.005 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
}
{
        @ "VIA5.B.2: VIA5 must be covered by M5 and M6, min. enclosure is 0.005um";
        not ( via5 , m5 );
        not ( via5 , m6 );
}


{
	@ "VIA5.E.2: Minimum VIA5BAR enclosure by M5 and M6 at end-of-line must be 0.003";


	not_covered_by(via5bar,m5,distances = {{{0.003,extension = NONE},{0, extension = NONE},
					 {0.003,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.003, extension = NONE},
					 {0,extension = NONE},{0.003,extension = NONE}}},
					 intersecting = {TOUCH});

	
	not_covered_by(via5bar,m6,distances = {{{0.003,extension = NONE},{0, extension = NONE},
					 {0.003,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.003, extension = NONE},
					 {0,extension = NONE},{0.003,extension = NONE}}},
					 intersecting = {TOUCH});


}


m5_v = wide (m5, > 0.2);
m6_v = wide (m6, > 0.2);

m5_w_01 = interacting(m5_v,via5);
m6_w_01 = interacting(m6_v,via5);



via5r2 = external1 (via5sq, <= 0.15, extension = RADIAL);
via5r2_e = interacting (via5r2,via5sq,count > 1);
via5r2_v =interacting (via5sq, via5r2_e);

via5r3 =external1 (via5lg, <= 0.15, extension = RADIAL);
via5r3_e =interacting(via5r3,via5lg,count > 1);
via5r3_v =interacting (via5lg, via5r3_e);

via5r4 = external1 (via5sq, <= 0.7,  extension = RADIAL);
via5r4_or = or(via5r4, via5sq);
via5r4_e = interacting (via5r4_or,via5sq,count>3);
via5r4_v = interacting ( via5sq,via5r4_e);
via5r5   = external1 (via5lg, <= 0.7,  extension = RADIAL);
via5r5_or = or(via5r5,via5lg);
via5r5_e = interacting (via5r5_or, via5lg,count >3);
via5r5_v = interacting (via5lg, via5r5_e);
/*
{
	@"VIA5.R.1: When M5 or M6 width >0.2um, it is a must to have redundant VIAs";
	not(m5_w_01,((interacting (m5_w_01, via5bar, count >= 1)) or (interacting (m5_w_01, via5r2_v, count >= 2)) or (interacting(m5_w_01,via5r3_v, count >=2 )) or (interacting(m5_w_01,via5r4_v, count >= 4)) or (interacting(m5_w_01,via5r5_v, count >= 4))));
}
*/

//***************************************      VIA6 RULES     *****************************/
    via6sq  = rectangles (via6, {0.06,0.06});
    via6lg  = rectangles (via6, {0.12,0.12});
    via6bar = rectangles (via6, {0.12,0.06});
{
        @ "VIA6.W.1 VIA6.W.2 VIA6.W.3 VIA6.W.4: VIA6 must be square with 0.03 or 0.07 width and length or VIA6 must be rectangular with length 0.06 and width 0.03";
        not(via6,(via6sq or via6lg or via6bar));
}


{
        @ "VIA6.S.1: Minimum center to center spacing of VIA6SQ to VIA6SQ: 0.15";
        center_to_center1( via6sq , distance < 0.15 );
}
{
        @ "VIA6.S.2: Minimum spacing of VIA6SQ to VIA6BAR or VIA6LG  must be 0.08";
        external2 (via6sq, via6bar or via6lg, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
        @ "VIA6.S.3: Minimum spacing of VIA6BAR or VIA6LG to VIA6BAR or VIA6LG must be 0.085";
        external1(via6bar or via6lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}

{
        @ "VIA6.E.1: Minimum VIA6 enclosure by M6 and M7 must be  0.005";
        enclose ( via6 , m6 and m7 , distance < 0.005 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
}
{
        @ "VIA6.B.2: VIA6 must be covered by M6 and M7, min. enclosure is 0.005um";
        not ( via6 , m6 );
        not ( via6 , m7 );
}


{
	@ "VIA6.E.2: Minimum VIA6BAR enclosure by M6 and M7 at end-of-line must be 0.003";


	not_covered_by(via6bar,m6,distances = {{{0.003,extension = NONE},{0, extension = NONE},
					 {0.003,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.003, extension = NONE},
					 {0,extension = NONE},{0.003,extension = NONE}}},
					 intersecting = {TOUCH});

	
	not_covered_by(via6bar,m7,distances = {{{0.003,extension = NONE},{0, extension = NONE},
					 {0.003,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.003, extension = NONE},
					 {0,extension = NONE},{0.003,extension = NONE}}},
					 intersecting = {TOUCH});


}


m6_v = wide (m6, > 0.2);
m7_v = wide (m7, > 0.2);

m6_w_01 = interacting(m6_v,via6);
m7_w_01 = interacting(m7_v,via6);



via6r2 = external1 (via6sq, <= 0.15, extension = RADIAL);
via6r2_e = interacting (via6r2,via6sq,count > 1);
via6r2_v =interacting (via6sq, via6r2_e);

via6r3 =external1 (via6lg, <= 0.15, extension = RADIAL);
via6r3_e =interacting(via6r3,via6lg,count > 1);
via6r3_v =interacting (via6lg, via6r3_e);

via6r4 = external1 (via6sq, <= 0.7,  extension = RADIAL);
via6r4_or = or(via6r4, via6sq);
via6r4_e = interacting (via6r4_or,via6sq,count>3);
via6r4_v = interacting ( via6sq,via6r4_e);
via6r5   = external1 (via6lg, <= 0.7,  extension = RADIAL);
via6r5_or = or(via6r5,via6lg);
via6r5_e = interacting (via6r5_or, via6lg,count >3);
via6r5_v = interacting (via6lg, via6r5_e);
/*
{
	@"VIA6.R.1: When M6 or M7 width >0.2um, it is a must to have redundant VIAs";
	not(m6_w_01,((interacting (m6_w_01, via6bar, count >= 1)) or (interacting (m6_w_01, via6r2_v, count >= 2)) or (interacting(m6_w_01,via6r3_v, count >=2 )) or (interacting(m6_w_01,via6r4_v, count >= 4)) or (interacting(m6_w_01,via6r5_v, count >= 4))));
}
*/

//***************************************      VIA7 RULES     *****************************/
    via7sq  = rectangles (via7, {0.06,0.06});
    via7lg  = rectangles (via7, {0.12,0.12});
    via7bar = rectangles (via7, {0.12,0.06});
{
        @ "VIA7.W.1 VIA7.W.2 VIA7.W.3 VIA7.W.4: VIA7 must be square with 0.03 or 0.07 width and length or VIA7 must be rectangular with length 0.06 and width 0.03";
        not(via7,(via7sq or via7lg or via7bar));
}


{
        @ "VIA7.S.1: Minimum center to center spacing of VIA7SQ to VIA7SQ: 0.15";
        center_to_center1( via7sq , distance < 0.15 );
}
{
        @ "VIA7.S.2: Minimum spacing of VIA7SQ to VIA7BAR or VIA7LG  must be 0.08";
        external2 (via7sq, via7bar or via7lg, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
        @ "VIA7.S.3: Minimum spacing of VIA7BAR or VIA7LG to VIA7BAR or VIA7LG must be 0.085";
        external1(via7bar or via7lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}

{
        @ "VIA7.E.1: Minimum VIA7 enclosure by M7 and M8 must be  0.005";
        enclose ( via7 , m7 and m8 , distance < 0.005 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
}
{
        @ "VIA7.B.2: VIA7 must be covered by M7 and M8, min. enclosure is 0.005um";
        not ( via7 , m7 );
        not ( via7 , m8 );
}


{
	@ "VIA7.E.2: Minimum VIA7BAR enclosure by M7 and M8 at end-of-line must be 0.003";


	not_covered_by(via7bar,m7,distances = {{{0.003,extension = NONE},{0, extension = NONE},
					 {0.003,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.003, extension = NONE},
					 {0,extension = NONE},{0.003,extension = NONE}}},
					 intersecting = {TOUCH});

	
	not_covered_by(via7bar,m8,distances = {{{0.003,extension = NONE},{0, extension = NONE},
					 {0.003,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.003, extension = NONE},
					 {0,extension = NONE},{0.003,extension = NONE}}},
					 intersecting = {TOUCH});


}


m7_v = wide (m7, > 0.2);
m8_v = wide (m8, > 0.2);

m7_w_01 = interacting(m7_v,via7);
m8_w_01 = interacting(m8_v,via7);



via7r2 = external1 (via7sq, <= 0.15, extension = RADIAL);
via7r2_e = interacting (via7r2,via7sq,count > 1);
via7r2_v =interacting (via7sq, via7r2_e);

via7r3 =external1 (via7lg, <= 0.15, extension = RADIAL);
via7r3_e =interacting(via7r3,via7lg,count > 1);
via7r3_v =interacting (via7lg, via7r3_e);

via7r4 = external1 (via7sq, <= 0.7,  extension = RADIAL);
via7r4_or = or(via7r4, via7sq);
via7r4_e = interacting (via7r4_or,via7sq,count>3);
via7r4_v = interacting ( via7sq,via7r4_e);
via7r5   = external1 (via7lg, <= 0.7,  extension = RADIAL);
via7r5_or = or(via7r5,via7lg);
via7r5_e = interacting (via7r5_or, via7lg,count >3);
via7r5_v = interacting (via7lg, via7r5_e);
/*
{
	@"VIA7.R.1: When M7 or M8 width >0.2um, it is a must to have redundant VIAs";
	not(m7_w_01,((interacting (m7_w_01, via7bar, count >= 1)) or (interacting (m7_w_01, via7r2_v, count >= 2)) or (interacting(m7_w_01,via7r3_v, count >=2 )) or (interacting(m7_w_01,via7r4_v, count >= 4)) or (interacting(m7_w_01,via7r5_v, count >= 4))));
}
*/

//***************************************      VIA8 RULES     *****************************/
    via8sq  = rectangles (via8, {0.06,0.06});
    via8lg  = rectangles (via8, {0.12,0.12});
    via8bar = rectangles (via8, {0.12,0.06});
{
        @ "VIA8.W.1 VIA8.W.2 VIA8.W.3 VIA8.W.4: VIA8 must be square with 0.03 or 0.07 width and length or VIA8 must be rectangular with length 0.06 and width 0.03";
        not(via8,(via8sq or via8lg or via8bar));
}


{
        @ "VIA8.S.1: Minimum center to center spacing of VIA8SQ to VIA8SQ: 0.15";
        center_to_center1( via8sq , distance < 0.15 );
}
{
        @ "VIA8.S.2: Minimum spacing of VIA8SQ to VIA8BAR or VIA8LG  must be 0.08";
        external2 (via8sq, via8bar or via8lg, distance < 0.08, extension = RADIAL, relational = POINT_TOUCH);
}
{
        @ "VIA8.S.3: Minimum spacing of VIA8BAR or VIA8LG to VIA8BAR or VIA8LG must be 0.085";
        external1(via8bar or via8lg, distance < 0.085, extension = RADIAL, relational = POINT_TOUCH);
}

{
        @ "VIA8.E.1: Minimum VIA8 enclosure by M8 and M9 must be  0.005";
        enclose ( via8 , m8 and m9 , distance < 0.005 , extension=RADIAL , intersecting = TOUCH , relational = POINT_TOUCH );
}
{
        @ "VIA8.B.2: VIA8 must be covered by M8 and M9, min. enclosure is 0.005um";
        not ( via8 , m8 );
        not ( via8 , m9 );
}


{
	@ "VIA8.E.2: Minimum VIA8BAR enclosure by M8 and M9 at end-of-line must be 0.003";


	not_covered_by(via8bar,m8,distances = {{{0.003,extension = NONE},{0, extension = NONE},
					 {0.003,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.003, extension = NONE},
					 {0,extension = NONE},{0.003,extension = NONE}}},
					 intersecting = {TOUCH});

	
	not_covered_by(via8bar,m9,distances = {{{0.003,extension = NONE},{0, extension = NONE},
					 {0.003,extension = NONE},{0,extension = NONE}},
					 {{0,extension = NONE},{0.003, extension = NONE},
					 {0,extension = NONE},{0.003,extension = NONE}}},
					 intersecting = {TOUCH});


}


m8_v = wide (m8, > 0.2);
m9_v = wide (m9, > 0.2);

m8_w_01 = interacting(m8_v,via8);
m9_w_01 = interacting(m9_v,via8);



via8r2 = external1 (via8sq, <= 0.15, extension = RADIAL);
via8r2_e = interacting (via8r2,via8sq,count > 1);
via8r2_v =interacting (via8sq, via8r2_e);

via8r3 =external1 (via8lg, <= 0.15, extension = RADIAL);
via8r3_e =interacting(via8r3,via8lg,count > 1);
via8r3_v =interacting (via8lg, via8r3_e);

via8r4 = external1 (via8sq, <= 0.7,  extension = RADIAL);
via8r4_or = or(via8r4, via8sq);
via8r4_e = interacting (via8r4_or,via8sq,count>3);
via8r4_v = interacting ( via8sq,via8r4_e);
via8r5   = external1 (via8lg, <= 0.7,  extension = RADIAL);
via8r5_or = or(via8r5,via8lg);
via8r5_e = interacting (via8r5_or, via8lg,count >3);
via8r5_v = interacting (via8lg, via8r5_e);
/*
{
	@"VIA8.R.1: When M8 or M9 width >0.2um, it is a must to have redundant VIAs";
	not(m8_w_01,((interacting (m8_w_01, via8bar, count >= 1)) or (interacting (m8_w_01, via8r2_v, count >= 2)) or (interacting(m8_w_01,via8r3_v, count >=2 )) or (interacting(m8_w_01,via8r4_v, count >= 4)) or (interacting(m8_w_01,via8r5_v, count >= 4))));
}
*/

//*****************************************************    PAD RULES   
/*
 pad_rect = rectangles (pad);
	{
		@ "PAD.W.1 PAD minimum bonding passivation opening width and length must be respectively 20 and 70";
		not_rectangles(pad_rect, {20,70});
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
*/
