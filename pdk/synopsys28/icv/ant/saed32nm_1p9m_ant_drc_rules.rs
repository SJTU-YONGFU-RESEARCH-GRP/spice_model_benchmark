/*
#########################################################################################
# SAED 32/28NM 1p9m icv antena drc deck							#
#											#
# Revision History:									#
# Rev.		date			what						#
# -------------------------------------------------------------------------------------	#	
# 1.0		02/Feb/2011		(First draft)					#
#########################################################################################
*/

#include "icv.rh"

MilkyWay : string = "Y";
OA: string ="N";
GDS: string ="N";


openaccess_options(
    view="layout",
    layer_mapping_file= "./techfiles/saed32.28nm_1p9m_gds.map"
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

////
  NWELLi = assign	  ( {{ == 1 } } );
  DNWi = assign		   ({{ == 2}});
  DIFFi = assign	   ({{==3}});
  DDMYi = assign	   ({{73}});
  PIMPi = assign	   ({{==4}});
  NIMPi = assign	   ({{==5}});
  DIFF_18i = assign 	   ({{==6}});
  PADi = assign		   ({{==7}});
  ESD_25 = assign	   ({{==8}});
  SBLKi = assign	   ({{==9}});
  POi = assign		   ({{==10}});
  PODMYi = assign	   ({{74}});
  M1i	=  assign	   ({{==11}});
  M1i_text = assign_text   ({{==11}});
  M1DMYi = assign	   ({{==64}});
  VIA1i = assign	   ({{==12}});
  M2i	= assign	   ({{==13}});
  M2i_text = assign_text   ({{==13}});
  M2DMYi = assign	   ({{==65}});
  VIA2i = assign	   ({{==14}});
  M3i	= assign           ({{==15}});
  M3i_text = assign_text   ({{==15}});
  M3DMYi = assign  	   ({{==66}});
  VIA3i = assign	   ({{==16}});
  M4i	= assign           ({{==17}});
  M4i_text = assign_text   ({{==17}});
  M4DMYi = assign  	   ({{==67}});
  VIA4i = assign	   ({{==18}});
  M5i	= assign           ({{==19}});
  M5i_text = assign_text   ({{==19}});
  M5DMYi = assign	   ({{68}});
  VIA5i = assign	   ({{20}});
  M6i	= assign           ({{21}});
  M6i_text = assign_text   ({{21}});
  M6DMYi = assign	   ({{69}});
  VIA6i = assign	   ({{22}});
  M7i	= assign	   ({{23}});
  M7i_text = assign_text   ({{23}});
  M7DMYi = assign	   ({{70}});
  VIA7i = assign           ({{24}});
  M8i   = assign           ({{25}});
  M8i_text = assign_text   ({{25}});
  M8DMYi = assign	   ({{71}});
  VIA8i = assign           ({{26}});
  M9i   = assign           ({{27}});
  M9i_text = assign_text   ({{27}});
  M9DMYi = assign	   ({{72}});
  COi 	= assign	   ({{28}});
  HVTIMPi = assign         ({{29}});
  LVTIMPi = assign         ({{30}});	
  M1PIN	= assign           ({{31}});
  M1PIN_text = assign_text ({{31}});
  M2PIN	= assign           ({{32}});
  M2PIN_text = assign_text ({{32}});
  M3PIN	= assign           ({{33}});
  M3PIN_text = assign_text ({{33}});
  M4PIN	= assign           ({{34}});
  M4PIN_text = assign_text ({{34}});
  M5PIN	= assign           ({{35}});
  M5PIN_text = assign_text ({{35}});
  M6PIN	= assign           ({{36}});
  M6PIN_text = assign_text ({{36}});
  M7PIN	= assign           ({{37}});
  M7PIN_text = assign_text ({{37}});
  M8PIN	= assign           ({{38}});
  M8PIN_text = assign_text ({{38}});
  M9PIN	= assign           ({{39}});
  M9PIN_text = assign_text ({{39}});
  MRDLi	= assign           ({{41}});
  HOTNWLi = assign         ({{44}});	
  DIODi	= assign           ({{46}});
  BJTMYi = assign          ({{47}});	
  RNWi = assign            ({{48}});	
  RMARKi = assign          ({{49}});
  LOGO = assign            ({{51}});	
  IP = assign              ({{52}});	
  RM1i = assign            ({{53}});
  RM2i = assign            ({{54}});
  RM3i = assign            ({{55}});
  RM4i = assign            ({{56}});
  RM5i = assign            ({{57}});
  RM6i = assign            ({{58}});
  RM7i = assign            ({{59}});
  RM8i = assign            ({{60}});
  RM9i = assign            ({{61}});
  DIFF_25i = assign        ({{75}});

///data_creation




GATE1    = and ( DIFFi    , POi );
GATE2    = and ( DIFF_25i , POi );
GATE3    = and ( DIFF_18i , POi );
GATE     = GATE1 or GATE2 or GATE3;
GATE_VIA = copy (GATE);
SD       = not ( DIFFi , POi );
CO_PO    = and (POi    , COi );
SD_temp1 = not ( SD    , POi ); 

c_db = connect (
	connect_items = {
		{{GATE}         ,    POi},
	        {{GATE_VIA}     ,   GATE},		
                {{CO_PO}        ,    POi},
                {{SD_temp1}     ,     SD},
                {{M1i,POi}      ,    COi},
                {{M1i,SD_temp1} ,    COi},
                {{M1DMYi,POi}      ,  COi},
                {{M1DMYi,SD_temp1} ,  COi},
                {{VIA1i}           ,  M1i} ,
}
	);


////////

      poly_area_ratio : published function( void ) returning void
      {
           po_area   : double = ns_net_area("po");
           gate_area : double = ns_net_area("gate");
           ratio     : double = po_area / gate_area;
           if ( ratio > 250 )
           {  
              ns_save_net({"ratio", "po_area", "gate_area"},
                              {ratio , po_area, gate_area});
           }
      }

{@"PO.AN.1:  Area(PO) / Area(Gate) > 250";
       net_select (connect_sequence = c_db,
            layer_groups = {"po" => {POi}, "gate" => {GATE}},
            net_function = poly_area_ratio,
            output_from_layers = {POi},
            connected_to_all={GATE}
       );

}

poly_perim_ratio : published function( void ) returning void
      {
           po_perim  : double = ns_net_perimeter("po");
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
            layer_groups = {"po" => {POi}, "gate" => {GATE}},
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
           if ( ratio > 10 )
           {
              ns_save_net({"ratio", "co_area", "gate_area"},
                              {ratio , co_area, gate_area});
           }
      }

{@"CO.AN.3:  Area(CO) / Area(Gate) > 10 ";
       net_select (connect_sequence = c_db,
            layer_groups = {"po" => {POi}, "gate" => {GATE},"co_po" => {CO_PO}},
            net_function = co_area_ratio,
            output_from_layers = {POi},
            connected_to_all={GATE,COi}
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
{"GATE"=>{GATE},"M"=> {M2i},"M_DIO"=>{SD},"MDMY"=>{M2DMYi}},
{"GATE"=>{GATE},"M"=> {M3i},"M_DIO"=>{SD},"MDMY"=>{M3DMYi}},
{"GATE"=>{GATE},"M"=> {M4i},"M_DIO"=>{SD},"MDMY"=>{M4DMYi}},
{"GATE"=>{GATE},"M"=> {M5i},"M_DIO"=>{SD},"MDMY"=>{M5DMYi}},
{"GATE"=>{GATE},"M"=> {M6i},"M_DIO"=>{SD},"MDMY"=>{M6DMYi}},
{"GATE"=>{GATE},"M"=> {M7i},"M_DIO"=>{SD},"MDMY"=>{M7DMYi}},
{"GATE"=>{GATE},"M"=> {M8i},"M_DIO"=>{SD},"MDMY"=>{M8DMYi}}
};


MC: newtype list of polygon_layer ;

V:MC={VIA1i,VIA2i,VIA3i,VIA4i,VIA5i,VIA6i,VIA7i,VIA8i};

M:MC={ M1i,M2i,M3i,M4i,M5i,M6i,M7i,M8i,M9i };

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
   minus_ratio = (m_dio_area>0)?((400*m_dio_area)+ 40000):(1000);
   ratio=met_ratio-minus_ratio;



   if (ratio > 0) {
       nps_save_polygon({"met_ratio"}, {met_ratio});
}
   nps_save_property ("met_ratio", met_ratio );
}


ll:list of polygon_layer;

for(i=0 to 7)
{j=i+1;

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
@"M"+j+".AN.1:  Area(M"+j+") / Area(Gate) > 1000 (wo effective diode)  Area(M"+j+") / Area(Gate) > Ratio (with effective diode) ";
net_polygon_select (
   connect_sequence = c_db,        
   in_property_layer = GM, 
   out_property_layer =GM,
   net_polygon_function = prop_met ,
   layer_groups = METX[i],  
   connected_to_all={M[i]}
);
}


if(i<7){
viaxj=VIAX[j]["VIA"];
c_db = incremental_connect(c_db,
connect_items = {
{{M[i],M[j]} ,    V[i] },
{ MDMY_C[i]  ,    V[i] },
{ viaxj      ,    M[j]  }
});

}else{

c_db = incremental_connect(c_db,
connect_items = {
{{ M[i],M[j]}     ,    V[i] },
{ MDMY_C[i]  ,    V[i] }
});

}
}



















