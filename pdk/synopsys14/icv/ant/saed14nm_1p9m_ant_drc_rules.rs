/*
#########################################################################################
# SAED 14NM 1p9m icv antena drc deck							#
#											#
# Revision History:									#
# Rev.		date			what						#
# -------------------------------------------------------------------------------------	#	
# 1.0		02/05/2017		(First draft)					#
#########################################################################################
*/

#include "icv.rh"

MilkyWay : string = "Y";
OA: string ="N";
GDS: string ="N";


openaccess_options(
    view="layout",
    layer_mapping_file= "./techfiles/saed14.14nm_1p9m_gds.map"  //--- /////////////14nm map file
    );


if (MilkyWay == "Y"){
library(  
library_name= "FAYDER",
format=MILKYWAY,
cell= "DFF"
);

}

else if (OA=="Y"){

library(
    library_name = "OA_Lib",
    format =  OPENACCESS,
    cell = "TOPCELLNAME"

);

}else if (GDS=="Y"){

library(  
library_name= "valod.gds",
format=GDSII,
cell= "DFF"
);
}

run_options(
instance_prefix="X",
uppercase=false                                       
);
                                            		
error_options(db_path="./TOPCELLNAME_err",
create_vue_output=true );			 

resolution_options(snap_resolution=0.001);

text_options(net_prefix="N");
prototype_options(true); 


layout_grid_options (
   resolution = 0.001
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
	M1i_1       = assign({{19, 1}});
	M1i_2       = assign({{19, 2}});
	M1DMYi    = assign({{19,1}});
	M1i_text  = assign_text({{19}});
	VIA1i     = assign({{20}});
	M2i       = assign({{21}});
	M2i_1       = assign({{21, 1}});
	M2i_2       = assign({{21, 2}});
	M2_3i	  = assign({{91}});		/* poxac2 */
	M2i_text  = assign_text({{21}});
        VIA2i     = assign({{22}});
	M2DMYi    = assign({{21,1}});
	M3i       = assign({{23}});
	M3i_1       = assign({{23, 1}});
	M3i_2       = assign({{23, 2}});
	M3_3i       = assign({{92}});		/* poxac3 */
	M3i_text  = assign_text({{23}});
	M3DMYi    = assign({{23,1}});
        VIA3i     = assign({{24}});
	M4i       = assign({{25}});
	M4i_1       = assign({{25, 1}});
	M4i_2       = assign({{25, 2}});
	M4i_text  = assign_text({{25}}); 
	M4DMYi    = assign({{25,1}});      
        VIA4i     = assign({{26}});
	M5i       = assign({{27}}); 
	M5i_1       = assign({{27, 1}}); 
	M5DMYi       = assign({{27, 1}});
	M5i_2       = assign({{27, 2}}); 
	M5i_text  = assign_text({{27}});   
        VIA5i     = assign({{28}});
	M6i       = assign({{29}});  
	M6i_1       = assign({{29, 1}});  
	M6i_2       = assign({{29, 2}});  
	M6i_text  = assign_text({{29}});
	M6DMYi    = assign({{29,1}});
	VIA6i     = assign({{30}});
	M7i       = assign({{31}});
	M7i_1       = assign({{31, 1}});
	M7i_2       = assign({{31, 2}});
	M7i_text  = assign_text({{31}});   
	M7DMYi    = assign({{31,1}}); 
	VIA7i     = assign({{32}});
	M8i       = assign({{33}});
	M8i_1       = assign({{33, 1}});
	M8i_2       = assign({{33, 2}});
	M8i_text  = assign_text({{33}});
	M8DMYi    = assign({{33,1}});
	VIA8i     = assign({{34}});    
	M9i       = assign({{35}});  
	M9i_1       = assign({{35, 1}});  
	M9i_2       = assign({{35, 2}});  
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
	RMARK     = assign({{54}});
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


///data_creation

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
	TOP_MET = 9;
	RECOMMENDED = 0;
	m1 = M1i;   
	m1_1 = M1i_1;   
	m1_2 = M1i_2;  
	m1_3 = M1_3i; 
	m2 = M2i;   
	m2_1 = M2i_1;   
	m2_2 = M2i_2;  
	m2_3 = M2_3i; 
	m3 = M3i;   
	m3_1 = M3i_1;   
	m3_2 = M3i_2;
	m3_3 = M3_3i; 
	m4 = M4i;   
	m4_1 = M4i_1;   
	m4_2 = M4i_2;   
	m5 = M5i;  
	m5_1 = M5i_1;  
	m5_2 = M5i_2;  
	m6 = M6i;   
	m6_1 = M6i_1;   
	m6_2 = M6i_2;   
	m7 = M7i;  
	m7_1 = M7i_1;  
	m7_2 = M7i_2;  
	m8 = M8i;   
	m8_1 = M8i_1;   
	m8_2 = M8i_2;   
	m9 = M9i;  
	m9_1 = M9i_1;  
	m9_2 = M9i_2;  
	
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



POCUT	= POCUTi;
CODIFFVIA   = and ( CTM1i , VIA0i );
COPOVIA     = and ( CPOi , VIA0i ); 
POC      = not ( POi, POCUTi ); 





	pdiff = and(pimp, diff);
	ndiff = and(nimp, diff);
	pact = and(pdiff, nwell);
	nact = and(ndiff, pwell);
	act = or(pact, nact);
	gate_common = and(po not axpoly, act);


	pdiff_15 = and(pimp, diff_15);
	ndiff_15 = and(nimp, diff_15);
	pact_15 = and(pdiff_15, nwell);
	nact_15 = and(ndiff_15, pwell);
	act_15 = or(pact_15, nact_15);
	gate_15 = and(po not axpoly, act_15);

	pdiff_18 = and(pimp, diff_18);
	ndiff_18 = and(nimp, diff_18);
	pact_18 = and(pdiff_18, nwell);
	nact_18 = and(ndiff_18, pwell);
	act_18 = or(pact_18, nact_18);
	gate_18 = and(po not axpoly, act_18);

	GATE     = gate_common or gate_15 or gate_18;

po_cuted = po not POCUT;
GATE_VIA = copy (GATE);
SD       = not ( DIFFi , po_cuted );  /////////------
CO_PO    = and ( po_cuted   , COPOVIA );
SD_temp1 = not ( SD    , po_cuted ); 



/***connect_data***/

c_db = connect (
	connect_items = {
		{{GATE}         ,    po_cuted},
	        {{GATE_VIA}     ,   GATE},		
                {{CO_PO}        ,    po_cuted},
                {{SD_temp1}     ,     SD},
		//{{GATE}     ,     po_cuted},
                {{M1i,POi}      ,    COPOVIA},
                {{M1_3i,POi}      ,    COPOVIA},
                {{M1i,SD_temp1} ,    CODIFFVIA},
                {{M1_3i,SD_temp1} ,    CODIFFVIA},
                {{M1DMYi,POi}      ,  COPOVIA},
                {{M1DMYi,SD_temp1} ,  CODIFFVIA},
                {{VIA1i}           ,  M1_3i} ,
                {{VIA1i}           ,  M1i}
}
	);
////////

      

//annotate_by_property(connect_sequence = c_db, layer1 = po, property_names = "po");
      //ns_save_net("po",po_cuted);
      poly_area_ratio : published function( void ) returning void
      {
           po_area   : double = ns_net_area("po_cuted");
           gate_area : double = ns_net_area("gate");
           ratio     : double = po_area / gate_area;
	    
	   
           if ( ratio > 250 )
           {  
              ns_save_net({"ratio", "po_cuted", "gate_area"},
                              {ratio , po_area, gate_area});
           }
      }

{@"PO.AN.1:  Area(PO) / Area(Gate) > 250";
       net_select (connect_sequence = c_db,
            layer_groups = {"po_cuted" => po_cuted, "gate" => {GATE}},
            net_function = poly_area_ratio,
            output_from_layers = {po_cuted},
            connected_to_all={GATE}
       );

}

poly_perim_ratio : published function( void ) returning void
      {
           po_perim  : double = ns_net_perimeter("po_cuted");
           gate_area : double = ns_net_area("gate");
           ratio     : double =  (po_perim*0.15) / gate_area;
           if ( ratio > 500 )
           {
              ns_save_net({"ratio", "po_perim", "gate_area"},
                              {ratio , po_perim, gate_area});
           }
      }

{@"PO.AN.2:  perimeter*thickness(PO) / Area(Gate) > 500";
       net_select (connect_sequence = c_db,
            layer_groups = {"po_cuted" => {po_cuted}, "gate" => {GATE}},
            net_function = poly_perim_ratio,
            output_from_layers = {POi},
            connected_to_all={GATE}
            
       );
}

co_area_ratio : published function( void ) returning void
      {   
           co_area   : double = ns_net_area("co_po");                    
           gate_area : double = ns_net_area("gate");
           ratio     : double =  co_area/gate_area;
           if ( ratio > 4 )
           {
              ns_save_net({"ratio", "co_area", "gate_area"},
                              {ratio , co_area, gate_area});
           }
      }

{@"CO.AN.3:  Area(CO) / Area(Gate) > 4 ";
       net_select (connect_sequence = c_db,
            layer_groups = {"po_cuted" => {po_cuted}, "gate" => {GATE},"co_po" => {CO_PO}},
            net_function = co_area_ratio,
            output_from_layers = {po_cuted},
            connected_to_all={GATE,COPOVIA}
       );

}

GV=initialize_property(GATE_VIA,{"via_ratio"});
GM=initialize_property(GATE    ,{"met_ratio"});

VIAX: list of layer_groups_h={  
{"GATE_VIA" => {GATE_VIA},"VIA" => {VIA1i},"M_DIO" => {SD}},
{"GATE_VIA" => {GATE_VIA},"VIA" => {VIA2i},"M_DIO" => {SD}},
{"GATE_VIA" => {GATE_VIA},"VIA" => {VIA3i},"M_DIO" => {SD}},
{"GATE_VIA" => {GATE_VIA},"VIA" => {VIA4i},"M_DIO" => {SD}},
{"GATE_VIA" => {GATE_VIA},"VIA" => {VIA5i},"M_DIO" => {SD}},
{"GATE_VIA" => {GATE_VIA},"VIA" => {VIA6i},"M_DIO" => {SD}},
{"GATE_VIA" => {GATE_VIA},"VIA" => {VIA7i},"M_DIO" => {SD}},
{"GATE_VIA" => {GATE_VIA},"VIA" => {VIA8i},"M_DIO" => {SD}}
};

METX:  list of layer_groups_h={ 
{"GATE"=>{GATE},"M"=> {M1i},"M_DIO"=>{SD},"MDMY"=>{M1DMYi}},
//{"GATE"=>{GATE},"M"=> {M1_3i},"M_DIO"=>{SD},"MDMY"=>{M1DMYi}}, //added
{"GATE"=>{GATE},"M"=> {M2i},"M_DIO"=>{SD},"MDMY"=>{M2DMYi}},
//{"GATE"=>{GATE},"M"=> {M2_3i},"M_DIO"=>{SD},"MDMY"=>{M1DMYi}}, //added
{"GATE"=>{GATE},"M"=> {M3i},"M_DIO"=>{SD},"MDMY"=>{M3DMYi}},
//{"GATE"=>{GATE},"M"=> {M3_3i},"M_DIO"=>{SD},"MDMY"=>{M1DMYi}}, //added
{"GATE"=>{GATE},"M"=> {M4i},"M_DIO"=>{SD},"MDMY"=>{M4DMYi}},
{"GATE"=>{GATE},"M"=> {M5i},"M_DIO"=>{SD},"MDMY"=>{M5DMYi}},
{"GATE"=>{GATE},"M"=> {M6i},"M_DIO"=>{SD},"MDMY"=>{M6DMYi}},
{"GATE"=>{GATE},"M"=> {M7i},"M_DIO"=>{SD},"MDMY"=>{M7DMYi}},
{"GATE"=>{GATE},"M"=> {M8i},"M_DIO"=>{SD},"MDMY"=>{M8DMYi}}
};


MC: newtype list of polygon_layer ;

V:MC={VIA1i,VIA2i,VIA3i,VIA4i,VIA5i,VIA6i,VIA7i,VIA8i};

m1 = or(m1,m1_3);
m2 = or(m2,m2_3);
m3 = or(m3,m3_3);

M:MC={ M1i,M2i, M3i, M4i,M5i,M6i,M7i,M8i,M9i };
//M:MC={ M1i,M1_3i,M2i,M1_3i, M3i,M1_3i, M4i,M5i,M6i,M7i,M8i,M9i }; //changed

M_C:list of MC={
 {M2i,M1i},
 {M3i,M2i},
 {M4i,M3i},
 {M5i,M4i},
 {M6i,M5i},
 {M7i,M6i},
 {M8i,M7i},
 {M9i,M8i}
 };

MDMY_C: list of MC ={
 {M2DMYi,M1DMYi},
 {M3DMYi,M2DMYi},
 {M4DMYi,M3DMYi},
 {M5DMYi,M4DMYi},
 {M6DMYi,M5DMYi},
 {M7DMYi,M6DMYi},
 {M8DMYi,M7DMYi},
 {M9DMYi,M8DMYi}
};

prop_via : function (void) returning void
{  
   old_via_ratio = (nps_read_property("via_ratio")>0)?nps_read_property("via_ratio"):0;
   via_area = nps_net_area("VIA");
   m_dio_area = nps_net_area("M_DIO");   
   gate_via_area = nps_net_area("GATE_VIA");
   via_ratio = old_via_ratio + (via_area/gate_via_area);
   minus_ratio = (m_dio_area>0)?((200*m_dio_area)+ 1000):(20);
   ratio=via_ratio-minus_ratio;

   if (ratio > 0) {
       nps_save_polygon({"via_ratio"}, {via_ratio});
   }
   nps_save_property ("via_ratio", via_ratio );
}

prop_met : function (void) returning void
{
   old_met_ratio = (nps_read_property("met_ratio")>0)?nps_read_property("met_ratio"):0;
   met_area = nps_net_area("M");
   mdmy_area = nps_net_area("MDMY");
   m_dio_area = nps_net_area("M_DIO");   
   gate_area = nps_net_area("GATE");
   met_ratio = old_met_ratio + (mdmy_area+met_area/gate_area);
   minus_ratio = (m_dio_area>0)?((400*m_dio_area)+ 40000):(1400);
   ratio=met_ratio-minus_ratio;



   if (ratio > 0) {
       nps_save_polygon({"met_ratio"}, {met_ratio});
}
   nps_save_property ("met_ratio", met_ratio );
}


ll:list of polygon_layer;

for(i=0 to 7)
	{
		j=i+1;

		{
			@"VIA"+j+".AN.1:  Area(VIA"+j+")  / Area(Gate) > 20 (wo effective diode)  Area(VIA"+j+") / Area(Gate) > Ratio (with effective diode) ";

			net_polygon_select (
   						connect_sequence = c_db,        
   						in_property_layer = GV, 
   						out_property_layer =GV,
   						net_polygon_function =  prop_via ,
   						layer_groups = VIAX[i],  
   						connected_to_all={V[i]}
						);
		}

		{
			@"M"+j+".AN.1:  Area(M"+j+") / Area(Gate) > 1400 (wo effective diode)  Area(M"+j+") / Area(Gate) > Ratio (with effective diode) ";
			net_polygon_select (
   						connect_sequence = c_db,        
  						in_property_layer = GM, 
   						out_property_layer =GM,
   						net_polygon_function = prop_met ,
   						layer_groups = METX[i],  
   						connected_to_all={M[i]}
						);
		}


		if(i<7)
			{
					viaxj=VIAX[j]["VIA"];
					c_db = incremental_connect(c_db,
							connect_items = {
										{{M[i],M[j]} ,    V[i] },
										{ MDMY_C[i]  ,    V[i] },
										{ viaxj      ,    M[j]  }
									}
									);

			}
		else
			{

					c_db = incremental_connect(c_db,
						connect_items = {
										{{ M[i],M[j]}     ,    V[i] },
										{ MDMY_C[i]  ,    V[i] }
								}
						);

			}
	}



















