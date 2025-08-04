/*	
#########################################################################################
# SAED 32/28NM 1p9m icv lvs  deck							#
#											#
# Revision History:									#
# Rev.		date			what						#
# -------------------------------------------------------------------------------------	#	
# 1.0		02/Feb/2011		(First draft)					#
# 1.1		--/---/2011		Changed tolerances of some device properties	#
# 1.2		21/Feb/2014		Updated for ICV 2013				#
# 1.3           10/Apr/2014		Updates for ICV 2013.06 (edbab@synopsys.com)
# 1.4       12/03/2015      Updated PEX layer mapping to show layers in StarRC OA view
#########################################################################################
*/

#define ICV_REVERT_NETTRAN
#define ICV_REVERT_DEVICE_PROCESSING_LAYER
#define ICV_REVERT_REMOVE_EQUIV_SUM_FILES
#define ICV_REVERT_GENERATE_EQUIV
#define ICV_REVERT_PEX_ALLOW_IMPLICIT_FILENAME
#define ICV_ENABLE_DEVICE_SETTING_APPEND_MODE
#include "icv.rh"
#include "math.rh"

/*#include "./Include/newtype_def.rs"*/

/*       newtype         */
m_st : newtype struct of{
   n: string;
   g: polygon_layer ;
   b: polygon_layer   ;
};

rpd_st : newtype struct of{
   n: string;
   b: polygon_layer ;
   t: polygon_layer   ;
   p: boolean  =true;
   d: boolean  =true;
};

rm_st : newtype struct of{
   n: string;
   b: polygon_layer ;
   t: polygon_layer  ;
  bo: boolean =true;
};

dev_names   :newtype list of string ;
proj_length :newtype list of double ;

inter : newtype enum of {
   ENTERING , LEAVING ,
   ENTERING_LEAVING,
};



/*Defined all needed variables*/




DECK_TYPE : string = "PEX_DECK";
CROSS_REFERENCE : string = "yes";
ICV_RUN_FILE_DIR: string = ".";


openaccess_options(
    view="layout",
    layer_mapping_file= "./techfiles/saed32nm_1p9m_gdsout.map"
    );



library(  
library_name= "CELLNAME.gds",
format=GDSII,
cell= "resistor"
);

layout_netl_fh:handle;
device_db:device_database;
xref_db_h:handle;

schem_netl_fh = schematic(
schematic_file    = {{filename = "CELLNAME.sp",format = SPICE}},
hierarchical_delimiter=SLASH,
expand_multiple_devices=true,
global_nets={"VDD", "VDD12", "VDD22","VDD2","VDDG", "VDDH","VDDL","VDDIO" },
cdl_settings={keep_passive_devices=true,
multiply_global_by_scale=true}
);


error_options(db_path="./TOPCELLNAME_err",
create_vue_output=true );

run_options(
instance_prefix="X",
uppercase=false
);

hierarchy_options(flatten={"*"});

resolution_options(snap_resolution=0.001);
text_options(
	net_prefix="N",
	layout_power={"VDD","VDD12","VDD22", "VDD2","VDDG", "VDDH", "VDDL", "VDDIO"},
	layout_ground={"VSS","VSS12","VDD22", "VSSIO"}
);
net_options(
schematic_power={"VDD","VDD12","VDD22", "VDD2","VDDG", "VDDH", "VDDL", "VDDIO"},
schematic_ground={"VSS","VSS12","VDD22", "VDD2", "VDDH", "VDDL", "VDDIO"},
schematic_global={"VDD","VDD12","VDD22","VSS","VSS12","VDD22", "VDD2","VDDG", "VDDH", "VDDL", "VDDIO", "VSSIO"}
);
prototype_options(false);


//64,72

  NWELLi = assign	   ({{ == 1}});
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
  M1DMYi = assign	   ({{64}});
  VIA1i = assign	   ({{==12}});
  M2i	= assign	   ({{==13}});
  M2i_text = assign_text   ({{==13}});
  M2DMYi = assign	   ({{65}});
  VIA2i = assign	   ({{==14}});
  M3i	= assign           ({{==15}});
  M3i_text = assign_text   ({{==15}});
  M3DMYi = assign  	   ({{66}});
  VIA3i = assign	   ({{==16}});
  M4i	= assign           ({{==17}});
  M4i_text = assign_text   ({{==17}});
  M4DMYi = assign  	   ({{67}});
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
  VIA7i	= assign	   ({{24}});
  M8i_text = assign_text   ({{25}});
  M8DMYi = assign	   ({{71}});
  M8i	= assign	   ({{25}});
  M9i_text = assign_text   ({{27}});
  M9DMYi = assign	   ({{72}});
  M9i = assign             ({{27}});
  COi 	= assign	   ({{28}});
  VIA8i = assign	   ({{26}});
  HVTIMPi = assign         ({{29}});
  LVTIMPi = assign         ({{30}});
  M1PIN	= assign	   ({{31}});
  M1PIN_text = assign_text ({{31}});
  M2PIN	= assign	   ({{32}});
  M2PIN_text = assign_text ({{32}}); 
  M3PIN	= assign	   ({{33}});
  M3PIN_text = assign_text ({{33}});
  M4PIN	= assign	   ({{34}});
  M4PIN_text = assign_text ({{34}});
  M5PIN	= assign           ({{35}});
  M5PIN_text = assign_text ({{35}});
  M6PIN	= assign	   ({{36}});
  M6PIN_text = assign_text ({{36}});
  M7PIN	= assign	   ({{37}});
  M7PIN_text = assign_text ({{37}});
  M8PIN	= assign 	   ({{38}});
  M8PIN_text = assign_text ({{38}});
  M9PIN	= assign	   ({{39}});
  M9PIN_text = assign_text ({{39}});
  MRDLi = assign           ({{41}});
  VIARDLi = assign         ({{42}});
  MRPINi = assign          ({{43}});
  
  HOTNWLi = assign 	   ({{44}});
  DIODi = assign 	   ({{46}});
  BJTMYi = assign 	   ({{47}});
  RNWi = assign		   ({{48}});
  RMARKi = assign          ({{49}});
  LOGO = assign		   ({{51}});
  IP   = assign 	   ({{52}});
  RM1i = assign		   ({{53}});
  RM2i = assign		   ({{54}});
  RM3i = assign		   ({{55}});
  RM4i = assign		   ({{56}});
  RM5i = assign		   ({{57}});
  RM6i = assign		   ({{58}});
  RM7i = assign		   ({{59}});
  RM8i = assign 	   ({{60}});
  RM9i = assign		   ({{61}});
  VARMARKi  = assign       ({{70}});
  CBMMARKi  = assign       ({{71}});
  DIFF_25i  = assign       ({{==75}});



/***********************************************/
 
 nwell = copy (NWELLi); 
 dnw   = copy (DNWi  ); 
 diff  = copy (DIFFi );  
 ddmy  = copy (DDMYi ); 
 pimp  = copy (PIMPi );
 nimp  = copy (NIMPi) ; 
 diff_25 = copy (DIFF_25i); 
 diff_18 = copy (DIFF_18i);
 pad = copy (PADi); 
 esd_25 = copy (ESD_25);
 sblk = copy (SBLKi);
 po = copy (POi); 
 podmy = copy (PODMYi); 

 m1 = copy (M1i );
 m2 = copy (M2i );
 m3 = copy (M3i );
 m4 = copy (M4i );
 m5 = copy (M5i );
 m6 = copy (M6i );
 m7 = copy (M7i );
 m8 = copy (M8i );
 m9 = copy (M9i ); 

 co = copy (COi ); 
 via1 = copy (VIA1i); 
 via2 = copy (VIA2i); 
 via3 = copy (VIA3i); 
 via4 = copy (VIA4i); 
 via5 = copy (VIA5i);
 via6 = copy (VIA6i);
 via7 = copy (VIA7i); 
 via8 = copy (VIA8i);

 hvtimp = copy (HVTIMPi); 
 lvtimp = copy ( LVTIMPi);
 hotnwl = copy (HOTNWLi);

 rm1 = copy (RM1i); 
 rm2 = copy (RM2i); 
 rm3 = copy (RM3i); 
 rm4 = copy (RM4i); 
 rm5 = copy (RM5i); 
 rm6 = copy (RM6i); 
 rm7 = copy (RM7i);
 rm8 = copy (RM8i);
 rm9 = copy (RM9i);


 viardl = copy (VIARDLi);
 mrdl   = copy (MRDLi);

 varmark =copy (VARMARKi);
 diod = copy (DIODi);
 bjtmark  = copy (BJTMYi);
 rnw =      copy (RNWi);
 rmark  = copy (RMARKi);
 cbmmark  = copy (CBMMARKi);
 //ctmmark  = copy (CTMMARKi);
 //indmark  = copy (INDMARKi);



 m1_pin  = copy (M1PIN);
 m2_pin  = copy (M2PIN);
 m3_pin  = copy (M3PIN);
 m4_pin  = copy (M4PIN);
 m5_pin  = copy (M5PIN);
 m6_pin  = copy (M6PIN);
 m7_pin  = copy (M7PIN);
 m8_pin  = copy (M8PIN);
 m9_pin  = copy (M9PIN);

//***************************Define derived, device and terminal layers************************/

chip = cell_extent ( cell_list = {"*"} );
bulk = size ( chip, 1);

pwell =  not ( bulk , nwell ); 


rnwel    = interacting ( nwell ,  rnw );
dnwnwell = interacting ( nwell ,  dnw );
nwres    = and ( nwell , rnw );

nwnr =     not_interacting (nwell, rnwel, include_touch = ALL);
nwoutdnw = not_interacting (nwell, dnw, include_touch = ALL);



imp =  or ( nimp ,  pimp );
ndiff =  and ( nimp , diff  );
pdiff=  and ( pimp , diff ) ;
nact =  and ( ndiff , pwell ) ; 
pact =  and  ( pdiff, nwnr ) ; 
act=    or ( pact  , nact  );
odwr =  interacting  ( diff,  nwres );

/*POLY RESISTORS*/
fpoly = not ( po ,  diff ); 
ponr  = not ( po , rmark ); 
pores = and ( po , rmark ); 

ppores =  and ( pores , pimp ); 
npores =  and ( pores, nimp ); 
ppores_sblk =  and ( ppores , sblk ) ;
npores_sblk =  and ( npores , sblk ) ;

ppores =  not ( ppores , ppores_sblk ) ; 
npores =  not  ( npores, npores_sblk ) ;





/*MOS GATES*/

ngate =  and (po, nact); 
pgate =  and (po, pact); 
gate  =  or (ngate, pgate); 


{
	@ "Interact of HVTIMP and LVTIMP is not allowed";
	interacting( hvtimp, lvtimp);
};
{
	@ "Interact of HVTIMP and DIFF_25 is not allowed";
	interacting( hvtimp, diff_25);
};
{
	@ "Interact of LVTIMP and DIFF_25 is not allowed";
	interacting( lvtimp, diff_25);
};
{
	@ "Interact of HVTIMP and diff_18 is not allowed";
	interacting( hvtimp, diff_18);

};
{
	@ "Interact of LVTIMP and diff_18 is not allowed";
	interacting( lvtimp, diff_18);

};
ngate_12 = not (ngate, (diff_25 or hvtimp or lvtimp or varmark or diff_18)) ;
pgate_12 = pgate not (diff_25 or hvtimp or lvtimp or varmark or diff_18) ;
gate_12 =   or (ngate_12, pgate_12) ; 

ngate_25 = and ( ngate, diff_25) ; 
pgate_25 = and ( pgate, diff_25) ;
ngate_18 = and ( ngate, diff_18) ;
pgate_18 = and ( pgate, diff_18) ;

gate_25 = or ( ngate_25 , pgate_25) ; 
gate_18 = or ( ngate_18 , pgate_18) ;

ngate_12_lvt = and ( ngate ,lvtimp) ;
pgate_12_lvt = and (pgate, lvtimp) ; 
gate_12_lvt  =or (  ngate_12_lvt , pgate_12_lvt) ; 

ngate_12_hvt = and ( ngate, hvtimp) ; 
pgate_12_hvt = and (pgate , hvtimp) ;
gate_12_hvt  = or (ngate_12_hvt, pgate_12_hvt) ; 




/*TAPS*/
ptap = and (pdiff , pwell) ;  
ntap = and (ndiff , nwnr)  ;

/*CONTACTS*/
codiff = and ( co ,diff) ;
copoly = not (co , diff) ;

/*SOURCE/DRAIN*/
sd  = not (act , gate) ;
nsd = nact not (gate or rmark or varmark) ; 
psd = pact not (gate or rmark or varmark) ;


/*Define metal resistors*/
m1res = m1 and rm1 ; 
m2res = m2 and rm2 ;
m3res = m3 and rm3 ;
m4res = m4 and rm4 ;
m5res = m5 and rm5 ;
m6res = m6 and rm6 ;
m7res = m7 and rm7 ;
m8res = m8 and rm8 ;
m9res = m9 and rm9 ;

m1 = m1 not rm1 ; 
m2 = m2 not rm2 ;
m3 = m3 not rm3 ;
m4 = m4 not rm4 ;
m5 = m5 not rm5 ;
m6 = m6 not rm6 ;
m7 = m7 not rm7 ;
m8 = m8 not rm8 ;
m9 = m9 not rm9 ;
{
@"M1" ;
 copy (m1);
}
/*varactor*/
ndif = nimp and diff ; 
pdif = pimp and diff ;

ngate_v = po and ndif ;
pgate_v = po and pdif ;

ngatev = varmark and ngate_v ;
pgatev = varmark and pgate_v ;
ngate_12v = ngatev not (diff_25 or hvtimp or lvtimp or diff_18) ; 
pgate_12v = pgatev not (diff_25 or hvtimp or lvtimp or diff_18) ;

povar   = varmark and po ; 
ngatepl = povar interacting ngate_12v ;
pgatepl = povar interacting pgate_12v ; 

nsdv_ = ndif and varmark ; 
psdv_ = pdif and varmark ;

nsdv  = nsdv_ not ngate_12v ;
psdv  = psdv_ not pgate_12v ;


dores  = diff and rmark ;
pdores = dores and pimp ;
ndores = dores and nimp ;
ndores = ndores not (diff_25 or hvtimp or lvtimp or varmark or diff_18) ; 
pdores = pdores not (diff_25 or hvtimp or lvtimp or varmark or diff_18) ;
pdores_sblk = pdores and sblk ; 
pdores      = pdores not pdores_sblk ; 
ndores_sblk = ndores and sblk ;


/*BOOLEAN ndores NOT ndores_sblk {} TEMP=ndores*/

pactr = pdiff and nwnr ;
nactr = ndiff and pwell ;

psdr  = pactr not (rmark or po) ;
nsdr  = nactr not (rmark or po) ;


ndiffdio1 = diod and nact ;
ndiffdio  = ndiffdio1 and m1 ;

pdiffdio1 = diod and pact ; // Arman
pdiffdio  = pdiffdio1 and m1 ;//

//pdiffdio = interacting (diod, pact, include_touch = NONE); Arman



/*INDUCTOR*/

sec_top_met  = M3i;
top_met      = M4i;
top_via_poss = VIA3i;
//cap_top_via  = CTMMARKi and top_via_poss;
//top_via      = VIA3i not cap_top_via;
psub = buildsub ( NWELLi ) ;

rm = rm1 or rm2 or rm3 or rm4 or rm5 or rm6 or rm7 or rm8 or rm9 ;

tiod1  = diff  not po ;
tiod2  = tiod1 not sblk ;
tiod3  = tiod2 not (rmark or bjtmark ) ;
tiod4  = tiod3 not rnw;
tiod   = tiod4 not varmark ; /* RPO, RMARKER, NWDMY cut ti-od */
nodcon = tiod  and nimp;
podcon = tiod  and pimp;
subtie = podcon and psub;


/**** Inductor ********/
/*inddmy_usize = size ( indmark,  -44.95 );*/
/*ovlp_inddmy  = indmark not inddmy_usize;
met_ovlp_inddmy = sec_top_met and ovlp_inddmy;
inddmy_std  = indmark interacting met_ovlp_inddmy;
ind_std_dmy = inddmy_usize interacting inddmy_std;
std_ind1 = top_met and ind_std_dmy;
std_ind2 = size(size(std_ind1,distance =3,clip_acute = NONE,processing_mode =  CELL_LEVEL),
distance =- 3, clip_acute = NONE, processing_mode = CELL_LEVEL);
std_hole = donut_holes (std_ind2);
std_ind4 = std_ind1 interacting std_hole;
ind_met  = std_ind1 not std_ind4 ; 
ind_met1 = ind_met  and inddmy_usize ;
std_ind5 = ind_met  interacting ind_met1 ;
*/
/* Body for standard inductor */
/*ind_octagon = std_ind4 or std_ind5 ;

indmet1 = m3 and m4 ;
indmet2 = indmet1 not indpinm ;
indbody = indmet2 and indmark ;

indterm_ = indmet1  and indmark ;
indterm  = indterm_ and indpinm ;
*/
//all_stdind_dumy = inddmy_usize interacting ind_octagon ;

/* Dummy for all symmetric inductors */

//sym_all_dmy = inddmy_usize not all_stdind_dumy;

//indpin = sec_top_met and indmark ;
//sym_all_ind1 = top_met and sym_all_dmy ;
//sym_all_ind2 = sym_all_ind1 or indpin  ;
//sz_sym_ind = size(size(sym_all_ind2, distance = 5, clip_acute = NONE, processing_mode = //CELL_LEVEL), distance = -5, clip_acute = NONE, processing_mode = CELL_LEVEL);
//sym_hole = donut_holes (sz_sym_ind) ;
//sym_all_ind3 = sz_sym_ind interacting sym_hole ;
//sym_all_ind  = sym_all_ind2 interacting sym_all_ind3 ;

//induct_body =  ind_octagon or  sym_all_ind ;
//top_metex   =  top_met     not induct_body ;	
//top_metex   =  top_metex   not rm ;               

CONTSB = co and bjtmark ;
CONTS  = co not CONTSB  ;
/************* BJT Data Creation Section****************/

/*Vertical PNP Derivation*/

nwell_hole  = donut_holes (nwnr,INNER);
//dnwell_hole = donut_holes (nxwell_DNWELL,INNER);
sab_hole    = donut_holes (sblk,INNER); 

nwell_hole_sab = nwell_hole or sab_hole ;

T_E_M_P_4444 =  bjtmark interacting diff ; 
T_E_M_P_4 = not_interacting (T_E_M_P_4444,sab_hole,include_touch=ALL);

DIFN_BIP = diff and T_E_M_P_4 ;
ALL_BJT_COLL = psub and T_E_M_P_4 ;
psub = psub not ALL_BJT_COLL ; 
T_E_M_P_43 = nwell and bjtmark ; 
l_0V_BJT_BASE_poss = T_E_M_P_43 not (diff_25 or diff_18) ;
T_E_M_P_44 = DIFN_BIP and pimp ;

l_0V_BJT_COLL_poss = ALL_BJT_COLL not (diff_25 or diff_18) ;
l_0V_BJT_COLL = not_interacting (l_0V_BJT_COLL_poss,nwell_hole_sab,include_touch = ALL); 
l_0V_BJT_BASE = not_interacting (l_0V_BJT_BASE_poss,nwell_hole_sab,include_touch = ALL);

l_0V_BJT_EMIT = T_E_M_P_44 and l_0V_BJT_BASE ;


/*Vertical NPN*/
l_0V_BJT_COLL_NPN_poss  = T_E_M_P_4 not (diff_25 or diff_18);
l_0V_BJT_COLL_NPN_poss1 = l_0V_BJT_COLL_NPN_poss interacting nwell_hole; 
l_0V_BJT_COLL_NPN = not_interacting (l_0V_BJT_COLL_NPN_poss1,sab_hole,include_touch = ALL);
l_0V_BJT_BASE_NPN = l_0V_BJT_COLL_NPN not (diff_25 or diff_18) not nwnr and nwell_hole ; 
l_0V_BJT_EMIT_NPN = ((DIFN_BIP not (diff_25 or diff_18)) and nimp) not nwnr and nwell_hole;


/*Contacts for Vertical PNP*/
l_0V_BJT_COLL_cont = l_0V_BJT_COLL not nwnr  and CONTSB;
l_0V_BJT_BASE_cont = l_0V_BJT_BASE and CONTSB and nimp ;
l_0V_BJT_EMIT_cont = l_0V_BJT_EMIT and CONTSB ;

/*Contacts for Vertical NPN*/
l_0V_BJT_COLL_cont_NPN = l_0V_BJT_COLL_NPN  and nwnr and CONTSB;
l_0V_BJT_BASE_cont_NPN = l_0V_BJT_BASE_NPN  and CONTSB not nimp;
l_0V_BJT_EMIT_cont_NPN = l_0V_BJT_EMIT_NPN  and CONTSB ;

/*MOM CAP*/

cv_1a = m1 and m2 ; 
cv_2a = m2 and m3 ;
cv_3a = m3 and m4 ;
cv_4a = m4 and m5 ;
/*
body_1 = ctmmark interacting cv_1a;
body_2 = ctmmark interacting cv_2a;
body_3 = ctmmark interacting cv_3a;
body_4 = ctmmark interacting cv_4a;


termc_1 = cv_1a  interacting body_1;
term_1  = cv_1a  not body_1;

termc_2 = cv_2a  interacting body_2;
term_2  = cv_2a  not body_2;

termc_3 = cv_3a  interacting body_3;
term_3  = cv_3a  not body_3;

termc_4 = cv_4a  interacting body_4;
term_4  = cv_4a  not body_4;

*/

//F_reg1 = external1(MOM_field1, distance < 0.41, extension = NONE, projection = {IN});
//F_reg1 = external1(MOM_field2, distance < 0.41, extension = NONE, projection = {IN});


subtie = subtie not nwell ;
subtie_scon = copy (subtie);

pwell_cont = copy (ptap);
nwell_cont = (ntap);




/*TEXT*/


m1pin_marker = text_origin(M1PIN_text, shape_size = 0.01, text={"*"},cells={"*"});
m2pin_marker = text_origin(M2PIN_text, shape_size = 0.01, text={"*"},cells={"*"});
m3pin_marker = text_origin(M3PIN_text, shape_size = 0.01, text={"*"},cells={"*"});
m4pin_marker = text_origin(M4PIN_text, shape_size = 0.01, text={"*"},cells={"*"});
m5pin_marker = text_origin(M5PIN_text, shape_size = 0.01, text={"*"},cells={"*"});
m6pin_marker = text_origin(M6PIN_text, shape_size = 0.01, text={"*"},cells={"*"});
m7pin_marker = text_origin(M7PIN_text, shape_size = 0.01, text={"*"},cells={"*"});
m8pin_marker = text_origin(M8PIN_text, shape_size = 0.01, text={"*"},cells={"*"});
m9pin_marker = text_origin(M9PIN_text, shape_size = 0.01, text={"*"},cells={"*"});




/***************************Define Connectivity***************************/

c_db = connect (
	connect_items = {

		{{ptap, pwell}		,pwell_cont},
		{{ntap, nwnr}		,nwell_cont},
		{{m1, nsd}		,codiff},
		{{m1, psd}		,codiff},
		
		{{m1, ntap}		,codiff},
		{{m1, ptap}		,codiff},    

    		{{m1, nsdr}		,codiff},
		{{m1, psdr}		,codiff},
        
    		{{m1, nsdv}		,codiff},
		{{m1, psdv}		,codiff},	
    
    		{{m1, ngatepl}		,copoly},
		{{m1, pgatepl}		,copoly},
       


		{ngate_12 , ponr},    //////overlap touch
    		{pgate_12 , ponr},
    		{ngate_25 , ponr},
    		{pgate_25 , ponr},
    		{ngate_18 , ponr},
    		{pgate_18 , ponr},
    		{ngate_12_lvt , ponr},
    		{pgate_12_lvt , ponr},
    		{ngate_12_hvt , ponr},
    		{pgate_12_hvt , ponr},
    

		{{m1, ponr}		,copoly},
		{{m2, m1}		,via1},
		
		{{m3, m2}		,via2},
		{{m4, m3}		,via3},
		
		{{m5, m4}		,via4},
		{{m6, m5}		,via5},
		
		{{m7, m6}		,via6},
		{{m8, m7}		,via7},
		
	   	{{m9, m8}		,via8},
		{{mrdl, m9}             ,viardl},
		{{l_0V_BJT_BASE, m1}	,l_0V_BJT_BASE_cont},
	    
		{{l_0V_BJT_COLL, m1}	,l_0V_BJT_COLL_cont},
	
		{{l_0V_BJT_EMIT, m1}	,l_0V_BJT_EMIT_cont},
	  
      
		{{l_0V_BJT_COLL_NPN, m1}	,l_0V_BJT_COLL_cont_NPN},
		{{l_0V_BJT_EMIT_NPN, m1}	,codiff},
  		{{l_0V_BJT_BASE_NPN, m1}	,l_0V_BJT_BASE_cont_NPN},
    	/*
		{{m3, term_1}		,via2},
		{{m2, term_1}		,m2},
    		{{m1, term_1}		,via1},
   
		{{m4, term_2}		,via3},
		{{m3, term_2}		,m3},
    		{{m2, term_2}		,via2},
   
    		{{m5, term_3}		,via4},
		{{m4, term_3}		,m4},
    		{{m3, term_3}		,via3},
   
    		{{m6, term_4}		,via5},
		{{m5, term_4}		,m5},
    		{{m4, term_4}		,via4},
   */
    	        //{{top_metex, sec_top_met}	,top_via},
  	//	{{top_metex, sec_top_met} 	,top_via},   //////overlap touch _check
    
		{{subtie, psub}		,subtie_scon},
    	//	{{indterm, m5}		,via4},
	
		{m1pin_marker, m1},
		{m2pin_marker, m2},
		{m3pin_marker, m3},
		    
    		{m4pin_marker, m4},
    		{m5pin_marker, m5},
    		{m6pin_marker, m6},
   		{m7pin_marker, m7},
    		{m8pin_marker, m8},
    		{m9pin_marker, m9}
	}
	);

    c_db =	 text_net(
    		connect_sequence = c_db,
                rename_prefix="N",                              ////new added
    		text_layer_items = {
    			{m1pin_marker, M1PIN_text},
    			{m2pin_marker, M2PIN_text},
    			{m3pin_marker, M3PIN_text},
    			{m4pin_marker, M4PIN_text},
    			{m5pin_marker, M5PIN_text},
    			{m6pin_marker, M6PIN_text},
    			{m7pin_marker, M7PIN_text},
    			{m8pin_marker, M8PIN_text},
    			{m9pin_marker, M9PIN_text}
		},
	attach_text = ALL
);
 /////////////////////////////////////////////////
c_db = create_ports (
	connect_sequence = c_db,
	port_items = {
                {m1pin_marker, m1pin_marker},
       		{m2pin_marker, m2pin_marker},
       		{m3pin_marker, m3pin_marker},
       		{m4pin_marker, m4pin_marker},
       		{m5pin_marker, m5pin_marker},
       		{m6pin_marker, m6pin_marker},
       		{m7pin_marker, m7pin_marker},
       		{m8pin_marker, m8pin_marker},
       		{m9pin_marker, m9pin_marker}
       		}
);
/*#include "./Include/assign.rs"*/

p_l : list of m_st = { 
{"p105"      , pgate_12,     nwnr},
{"p25"       , pgate_25,     nwnr},
{"p18"       , pgate_18,     nwnr},
{"p105_lvt"  , pgate_12_lvt, nwnr},
{"p105_hvt"  , pgate_12_hvt, nwnr}
 };

n_l : list of m_st = {
{"n105"     , ngate_12     , pwell},
{"n25"      , ngate_25     , pwell},
{"n18"      , ngate_18     , pwell},
{"n105_lvt" , ngate_12_lvt , pwell},
{"n105_hvt" , ngate_12_hvt , pwell}
};



rpd_l : list of rpd_st = { 
{"rpdiff"     , pdores     ,psdr,false,true},
{"rndiff"     , ndores     ,nsdr,false,true},
{"rppoly"     , ppores     ,ponr},
{"rnpoly"     , npores     ,ponr,true,false},
{"rppoly_wos" , ppores_sblk,ponr,true,false},
{"rnpoly_wos" , npores_sblk,ponr}
 };





rm_l : list of rm_st = { 
{"rm1" ,m1res,m1},
{"rm2" ,m2res,m2},
{"rm3" ,m3res,m3},
{"rm4" ,m4res,m4},
{"rm5" ,m5res,m5},
{"rm6" ,m6res,m6},
{"rm7" ,m7res,m7},
{"rm8" ,m8res,m8}
 /* {"rm9" ,m9res,m9,false}, */
 };
 

nmos_list:dev_names = {
"n105",
"n25",
"n18",
"n105_lvt",
"n105_hvt"
};

pmos_list:dev_names = {
"p105",
"p25",
"p18",
"p105_lvt",
"p105_hvt"
};

/***********************************/
 
if (DECK_TYPE == "LVS_DECK" || DECK_TYPE=="PEX_DECK") 
{

my_devices = init_device_matrix (c_db);      
///////////////
mos_wpe_property : function (
   length       : double,
   width        : double
) returning void {
     gates            = dev_body();
     well             = dev_processing_layer("key1"); //Arthur
    



    tn : integer;
    ln : integer;
    bn : integer;    
    rn : integer;

    tw : list of double = {};
    bw : list of double = {};
    rw : list of double = {};
    lw : list of double = {};

    



    tl_p : list of projection_data_s = {{well, 1, LEAVING, -1}};
    bl_p : list of projection_data_s = {{well, 1, LEAVING, -1}};
    rl_p : list of projection_data_s = {{well, 1, LEAVING, -1}};
    ll_p : list of projection_data_s = {{well, 1, LEAVING, -1}};

    mos_proximity_list(
        body = gates,
        projection_data = tl_p,      
        direction = TOP,
        width = tw,
        count = tn
    );

    mos_proximity_list(
        body = gates,
        projection_data = bl_p,     
        direction = BOTTOM,  
        width = bw,
        count = bn
    );

    mos_proximity_list(
        body = gates,
        projection_data = rl_p,        
        direction = RIGHT,
        width = rw,
        count = rn
    );

    mos_proximity_list(
        body = gates,
        projection_data = ll_p,        
        direction = LEFT,
        width = lw,
        count = ln
    );


    tl = tl_p[0].projection_length;
    bl = bl_p[0].projection_length;
    rl = rl_p[0].projection_length;
    ll = ll_p[0].projection_length;


    W  : list of double = {};
    SC : list of double = {};
    L  : list of double = {};

    for (i=0 to ln-1) {
        W.push_back(lw[i]);
        SC.push_back(ll[i]);
    }
  
    for (i=0 to rn-1) {
        W.push_back(rw[i]);
        SC.push_back(rl[i]);
    }

    w_count : integer = ln + rn - 1;
    l_count : integer = ln + rn;

    for (i=0 to tn-1) {
        L.push_back(tw[i]);
        SC.push_back(tl[i]);
    }

    for (i=0 to bn-1) {
        L.push_back(bw[i]);
        SC.push_back(bl[i]);
    }

    Sx : double = 0;
    Sy : double = 0;
    Sz : double = 0;

 SCref : double =2.5;
    if (w_count != 0) {
        for (i=0 to w_count) {
           if (dbllt(SC[i], SCref)) {
               Sx = Sx + ( W[i] * ( (1/SC[i]) - (1/(SC[i]+length)) ) );
               Sy = Sy +  W[i] *( ( ( (SC[i]/10.0)+(SCref/100.0) ) * 
                          exp((-10)*(SC[i]/SCref)) ) - ( ( ((SC[i]+length)/10.0)+(SCref/100.0) ) * 
                          exp((-10)*((SC[i]+length)/SCref)) ) ); 
               Sz = Sz +  W[i] *( ( ( (SC[i]/20.0)+(SCref/400.0) ) * 
                          exp((-20)*(SC[i]/SCref)) ) - ( ( ((SC[i]+length)/20.0)+(SCref/400.0) ) *  
                          exp((-20)*((SC[i]+length)/SCref)) ) ) ; 
           }
           
        }
    } 

    SCA : double = 0;
    SCB : double = 0;
    SCC : double = 0;
   

    dj : integer = ln + rn;
    for (j=0 to (bn+tn-1)) {
       kk = j + dj;
       if (dbllt(SC[kk], SCref)) { 
           Sx = Sx + ( L[j] * ( (1/SC[kk]) - (1/(SC[kk]+width)) ) );      
           Sy = Sy + L[j] *( ( ( (SC[kk]/10)+(SCref/100) ) * 
                     exp((-10)*(SC[kk]/SCref)) ) - ( ( ((SC[kk]+width)/10)+(SCref/100) ) * 
                     exp((-10)*((SC[kk]+width)/SCref)) ) );
           Sz = Sz + L[j] *( ( ( (SC[kk]/20)+(SCref/400) ) * 
                     exp((-20)*(SC[kk]/SCref)) ) - ( ( ((SC[kk]+width)/20)+(SCref/400) ) * 
                     exp((-20)*((SC[kk]+width)/SCref)) ) );
       }
    }



    SCA = (1/(width*length)) * ((SCref**2) * Sx);
    SCB = (1/(width*length)) * Sy;
    SCC = (1/(width*length)) * Sz;

    


    if( dev_is_property("SCA") ) { dev_save_double_properties({{"SCA", SCA}}); }
    if( dev_is_property("SCB") ) { dev_save_double_properties({{"SCB", SCB}}); }
    if( dev_is_property("SCC") ) { dev_save_double_properties({{"SCC", SCC}}); }



}
///////////

	/*MOSFETS*/
prop_mos : function(void) returning void {
    gate_set    = dev_body();
    w : double  = (mos_width_1()+ mos_width_2())/2.0;
   nf : integer = dev_count_polygons(gate_set);	
    l : double  = mos_gate_area()/(w*nf);
  nrd : double  = mos_nrd();
  nrs : double  = mos_nrs();
   as : double ;
   ad : double ;
   ps : double ;
   pd : double ;

   as = mos_source_area();
   ad = mos_drain_area();
   ps = mos_source_perim()+mos_width_1();
   pd = mos_drain_perim() +mos_width_2();

mos_wpe_property(l, w);

    dev_save_double_properties(
        {{"nf", nf},
         {"m", 1},
         {"w" , w},
         {"l" , l},
         {"ad", ad},
         {"as", as},
         {"ps", ps},
         {"pd", pd},
         {"nrd", nrd},
         {"nrs", nrs}
        }
    );
};

 
foreach (pm in p_l )
{ 
pmos(my_devices,pm.n, psd ,pm.g, psd,{{pm.b}},
merge_parallel = true,

 //processing_layers={pm.g},
properties = {{"l"  ,   DOUBLE,MICRO},
              {"w"  ,   DOUBLE,MICRO},
              {"nf" ,   DOUBLE },
              {"m"  ,   DOUBLE },
              {"ad" ,   DOUBLE,PICO },
              {"as" ,   DOUBLE,PICO },
              {"ps" ,   DOUBLE,MICRO },
              {"pd" ,   DOUBLE,MICRO },
              {"SCC",   DOUBLE,NONE },
              {"SCA",   DOUBLE,NONE },
              {"SCB",   DOUBLE,NONE }, 
              {"nrd",   DOUBLE,NONE },
              {"nrs",   DOUBLE,NONE }
            },

property_function = prop_mos,
processing_layer_hash={"key1"=>{nwnr}}); //Arthur -> Line 744
};

foreach (nm in n_l )
{
nmos(my_devices,nm.n, nsd ,nm.g, nsd,{{nm.b}},

merge_parallel = true,

properties = {{"l"  ,   DOUBLE,MICRO},
              {"w"  ,   DOUBLE,MICRO},
              {"nf" ,   DOUBLE },
              {"m"  ,   DOUBLE },
              {"ad" ,   DOUBLE,PICO },
              {"as" ,   DOUBLE,PICO },
              {"ps" ,   DOUBLE,MICRO},
              {"pd" ,   DOUBLE,MICRO},
              {"SCC",   DOUBLE,NONE },
              {"SCA",   DOUBLE,NONE },
              {"SCB",   DOUBLE,NONE }, 
              {"nrd",   DOUBLE,NONE },
              {"nrs",   DOUBLE,NONE }
  
            },
property_function = prop_mos,
processing_layer_hash={"key1"=>{pwell}} // Arthur -> Line 744
//x_card = true
);
};
	
	
	/*Vractor*/
/*
prop_cap : function( void ) returning void {
    w : double = cap_width ();	
    l : double = cap_area()/w;   
  
    dev_save_double_properties(
        {
         {"w", w},
         {"l", l}
        }
    );
};


capacitor(my_devices,"nvar",ngate_12v,ngatepl,nsdv,
   properties = {{"lr",DOUBLE},
                 {"wr",DOUBLE}
                },
   property_function = prop_cap,
schematic_devices={{"nvar","plus","minus"}}
 );

capacitor(my_devices,"pvar",pgate_12v,pgatepl,psdv,
   properties = {{"lr",DOUBLE},
                 {"wr",DOUBLE}
                },
   property_function = prop_cap,
schematic_devices={{"pvar","plus","minus"}} 
 );
*/

 /*RESISTORS*/

prop_respd : function( void ) returning void {     	
    w : double = (res_width_term_a()+ res_width_term_b())/2.0;	
    l : double = (res_area()/w)-0.002 ;

    dev_save_double_properties(
        {
         {"w", w},
         {"l", l}
        }
    );
};


foreach (rr in rpd_l )
{
resistor(my_devices,rr.n,rr.b,rr.t,rr.t,
properties = {{"l",   DOUBLE, MICRO},
              {"w",   DOUBLE, MICRO}
              },

property_function = prop_respd,
schematic_devices ={{rr.n,"A","B"}},

x_card=true

 );
};





/*DIODES*/
prop_diode: function( void ) returning void {     	
    p=diode_perim ();
    area: double = diode_area()-(0.524*(p/2-0.524));
    dev_save_double_properties(
        {{"area", area}}
    );
};
np (   my_devices,"nd",ndiffdio ,nsd,pwell ,
   properties =  {{"area", DOUBLE, PICO}
              }

);

pn (   my_devices,"pd",pdiffdio ,nwnr,psd,
   properties =  {{"area", DOUBLE, PICO}
              }//, Arman

///property_function = prop_diode
);

pnp(  my_devices,"vpnp" ,l_0V_BJT_COLL, l_0V_BJT_BASE, l_0V_BJT_EMIT,x_card=true);
	
npn(my_devices,"hnpn",l_0V_BJT_COLL_NPN ,l_0V_BJT_BASE_NPN,
l_0V_BJT_EMIT_NPN,x_card=true);	


	
	/*
capacitor(my_devices,"ccap", body_1,term_1, term_1,
schematic_devices={{"ccap","plus","minus"}},
x_card=true);
capacitor(my_devices,"ccap", body_2,term_2, term_2,
schematic_devices={{"ccap","plus","minus"}},
x_card=true);
capacitor(my_devices,"ccap", body_3,term_3, term_3,
schematic_devices={{"ccap","plus","minus"}},
x_card=true);
capacitor(my_devices,"ccap", body_4,term_4, term_4,
schematic_devices={{"ccap","plus","minus"}},
x_card=true);

*/
device_db=extract_devices (my_devices);
layout_netl_fh=netlist(device_db);
}
/*End of if DECK_TYPE=="LVS_DECK" || DECK_TYPE=="PEX_DECK"*/

//compare section//

compare_settings=init_compare_matrix ();



match(compare_settings,
      match_by_net_name=true,
      detect_permutable_ports=false,
match_condition= {
          layout_ports_without_name=ERROR,
          top_layout_ports_without_name=ERROR,
          port_net_match_non_port_net=ERROR,
          top_schematic_port_net_match_non_port_net=WARNING,
          top_layout_port_net_match_non_port_net=WARNING,
          nets_matched_with_different_name=ERROR,
          ports_matched_with_different_name=ERROR,
          top_ports_matched_with_different_name=ERROR,
          property_mismatch=ERROR,
          equate_by_net_name_fails=ERROR,
          equate_nets_fails=ERROR,
          zero_value_property= ERROR,
          no_global_nets_found= WARNING,
          generate_global_nets=ERROR,
          merging_without_pwr_gnd=ERROR,
          }
   );


foreach (rr in rpd_l )
{
merge_series(compare_settings,RESISTOR,{rr.n},
{{"l",[-0.5,0.5],RELATIVE}}
);
}

foreach (nn in n_l )
{
merge_parallel(compare_settings, NMOS, device_names = {nn.n},
 property_functions = { {"calc_width_length_by_ratio" } }
);
}
foreach (pp in p_l )
{
merge_parallel(compare_settings, PMOS, device_names = {pp.n},
  property_functions = { {"calc_width_length_by_ratio" } }
);
}


check_property(compare_settings,NMOS,
device_names=nmos_list,

property_tolerances={{"l",[-0.1,0.1],RELATIVE},
                     {"w",[-0.1,0.1],RELATIVE},
                    // {"m",[-0.5,0.5],RELATIVE},
                     {"nf",[-0.5,0.5],RELATIVE}  
}
);
check_property(compare_settings,PMOS,
device_names=pmos_list,

property_tolerances={{"l",[-0.1,0.1],RELATIVE},
                     {"w",[-0.1,0.1],RELATIVE},     
                   //  {"m",[-0.5,0.5],RELATIVE},
                     {"nf",[-0.5,0.5],RELATIVE}  
}
);


check_property(compare_settings,RESISTOR,
device_names={"rppoly" , "rnpoly","rppoly_wos" ,"rnpoly_wos"},

property_tolerances={{"w",[-0.5,0.5],RELATIVE},
                     {"l",[-0.5,0.5],RELATIVE}}
);


check_property(compare_settings,PN,
device_names={"pd"},
property_tolerances={{"area",[-0.2,0.2],RELATIVE}} 
);


check_property(compare_settings,NP,
device_names={"nd"},
property_tolerances={{"area",[-0.2,0.2],RELATIVE}}

);



check_property(compare_settings,PNP,
device_names={"vpnp"},
property_tolerances={{"area",[-0.5,0.5],ABSOLUTE}}

);


check_property(compare_settings,NPN,
device_names={"hnpn"},
property_tolerances={{"area",[-0.5,0.5],ABSOLUTE}}

);



filter(compare_settings,NMOS,nmos_list,filter_options=NMOS_1);

filter(compare_settings,PMOS,pmos_list,filter_options=PMOS_1);

filter(compare_settings,RESISTOR,{ "rppoly" , "rnpoly",
"rppoly_wos" ,"rnpoly_wos" },filter_options=RES_1);

filter(compare_settings,NP,{"nd"},filter_options=NP_1);

filter(compare_settings,PN,{"pd"},filter_options=PN_1);

//filter(compare_settings, CAPACITOR ,{"ccap"},filter_options=CAP_1);


/***************************Begin Compare Section************************/



if( DECK_TYPE=="LVS_DECK" || DECK_TYPE=="PEX_DECK" ) {

  xref_db_h =  compare(
	state = compare_settings,
        schematic=schem_netl_fh,
        layout=layout_netl_fh,
        user_functions_file = $SAED32_28_PDK+"/icv/lvs/Include/functions.rs", 
        memory_array_compare =(DECK_TYPE=="PEX_DECK")?(false):(true),
	//remove_equiv_sum_files = NONE,
        write_equiv_netlists   = ALL,
        action_on_error    = EXPLODE,
        remove_dangling_net = LAYOUT_UNTEXTED,
        multiply_width = false,
	push_down_pins = false
	//generate_equiv= {FULL_NAME, CASE_INSENSITIVE_NAME}
    );
};

spice_netlist_fh=spice_netlist_file("block");
if(DECK_TYPE=="LVS_DECK" || CROSS_REFERENCE=="yes")
{write_xref_spice(device_db,
xref_db=xref_db_h,
output_file=spice_netlist_fh);
}else{
write_spice(device_db,spice_netlist_fh);
};

if(  DECK_TYPE=="PEX_DECK" ) {

pex_matrix = init_pex_layer_matrix(device_db);
/*conducting_layer*/

pex_conducting_layer_map(pex_matrix, psub, "SUBSTRATE", tagname="psub",
	   lpp_layer    = {lpp_polygon_layer   = "DIFF",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "DIFF",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "DIFF",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, nwnr, "SUBSTRATE", tagname="nwnr",
lpp_layer    = {lpp_polygon_layer   = "NWELL",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "NWELL",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "NWELL",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, pwell,"SUBSTRATE", tagname="pwell",
lpp_layer    = {lpp_polygon_layer   = "NIMP",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "NIMP",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "NIMP",
                   lpp_subnode_purpose = "subnode"}
);

//pex_conducting_layer_map(pex_matrix, nwell,"SUBSTRATE", tagname="nwell");
//pex_conducting_layer_map(pex_matrix, diff,"DIFF", tagname="diff",rpsq=0);
//pex_conducting_layer_map(pex_matrix, nact ,"DIFF", tagname="nact",rpsq=0);
//pex_conducting_layecheck_propr_map(pex_matrix, pact ,"DIFF", tagname="pact",rpsq=0);

pex_conducting_layer_map(pex_matrix, pdiffdio,"DIFF", tagname="pdiffdio",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "DIFF",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "DIFF",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "DIFF",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, ndiffdio,"DIFF", tagname="ndiffdio",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "DIFF",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "DIFF",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "DIFF",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, nsd,"DIFF", tagname="nsd",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "DIFF",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "DIFF",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "DIFF",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, psd,"DIFF", tagname="psd",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "DIFF",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "DIFF",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "DIFF",
                   lpp_subnode_purpose = "subnode"}
);

//pex_conducting_layer_map(pex_matrix, ntap,"DIFF", tagname="ntap",rpsq=0);
pex_conducting_layer_map(pex_matrix, ptap,"DIFF", tagname="ptap",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "DIFF",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "DIFF",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "DIFF",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, psdr,"DIFF", tagname="psdr",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "DIFF",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "DIFF",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "DIFF",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, nsdr,"DIFF", tagname="nsdr",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "DIFF",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "DIFF",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "DIFF",
                   lpp_subnode_purpose = "subnode"}
);

pex_conducting_layer_map(pex_matrix, nsdv,"DIFF", tagname="nsdv",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "DIFF",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "DIFF",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "DIFF",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, psdv,"DIFF", tagname="psdv",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "DIFF",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "DIFF",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "DIFF",
                   lpp_subnode_purpose = "subnode"}
);


/*pex_conducting_layer_map(pex_matrix, indterm,"M5", tagname="indterm",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "m5",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "m5",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "m5",
                   lpp_subnode_purpose = "subnode"}
);
*/
/*
pex_conducting_layer_map(pex_matrix, term_1,"M2", tagname="term1",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "m2",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "m2",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "m2",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, term_2,"M3", tagname="term2",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "m3",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "m3",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "m3",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, term_3,"M4", tagname="term3",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "m4",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "m4",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "m4",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, term_4,"M5", tagname="term4",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "m5",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "m5",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "m5",
                   lpp_subnode_purpose = "subnode"}
);
*/
pex_conducting_layer_map(pex_matrix, l_0V_BJT_BASE,"DIFF", tagname="l_0V_BJT_BASE",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "DIFF",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "DIFF",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "DIFF",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, l_0V_BJT_COLL,"DIFF", tagname="l_0V_BJT_COLL",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "DIFF",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "DIFF",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "DIFF",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, l_0V_BJT_EMIT,"DIFF", tagname="l_0V_BJT_EMIT",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "DIFF",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "DIFF",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "DIFF",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, l_0V_BJT_COLL_NPN,"DIFF",
 tagname="l_0V_BJT_COLL_NPN",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "DIFF",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "DIFF",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "DIFF",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, l_0V_BJT_EMIT_NPN,"DIFF",
 tagname="l_0V_BJT_EMIT_NPN",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "DIFF",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "DIFF",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "DIFF",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, l_0V_BJT_BASE_NPN,"DIFF",
 tagname="l_0V_BJT_BASE_NPN",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "DIFF",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "DIFF",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "DIFF",
                   lpp_subnode_purpose = "subnode"}
);

//pex_conducting_layer_map(pex_matrix, po,   "POLY", tagname="po",rpsq=0);
pex_conducting_layer_map(pex_matrix, ngatepl,"POLY", tagname="ngatepl",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "PO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "PO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "PO",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, pgatepl,"POLY", tagname="pgatepl",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "PO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "PO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "PO",
                   lpp_subnode_purpose = "subnode"}
);

pex_conducting_layer_map(pex_matrix, subtie_scon , "SUBSTRATE", tagname="subtie_scon ");
pex_conducting_layer_map(pex_matrix, subtie, "SUBSTRATE", tagname="subtie",
lpp_layer    = {lpp_polygon_layer   = "diff",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "diff",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "diff",
                   lpp_subnode_purpose = "subnode"}
);

pex_conducting_layer_map(pex_matrix, pdores ,"DIFF", tagname="pdores",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "diff",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "diff",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "diff",
                   lpp_subnode_purpose = "subnode"}
);

pex_conducting_layer_map(pex_matrix, ndores  ,"DIFF", tagname="ndores ",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "diff",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "diff",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "diff",
                   lpp_subnode_purpose = "subnode"}
);

//pex_conducting_layer_map(pex_matrix, pgate,   "POLY", tagname="pgate",rpsq=0);
//pex_conducting_layer_map(pex_matrix, ngate,"POLY", tagname="ngate",rpsq=0);
pex_conducting_layer_map(pex_matrix, ngate_12,"POLY", tagname="ngate_12",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "PO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "PO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "PO",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, pgate_12,"POLY", tagname="pgate_12",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "PO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "PO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "PO",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, ngate_25,"POLY", tagname="ngate_25",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "PO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "PO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "PO",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, pgate_25,"POLY", tagname="pgate_25",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "PO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "PO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "PO",
                   lpp_subnode_purpose = "subnode"}
);

pex_conducting_layer_map(pex_matrix, ngate_18,"POLY", tagname="ngate_18",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "PO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "PO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "PO",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, pgate_18,"POLY", tagname="pgate_18",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "PO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "PO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "PO",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, ngate_12_lvt,"POLY", tagname="ngate_12_lvt",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "PO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "PO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "PO",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, pgate_12_lvt,"POLY", tagname="pgate_12_lvt",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "PO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "PO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "PO",
                   lpp_subnode_purpose = "subnode"}
);

pex_conducting_layer_map(pex_matrix, ngate_12_hvt,"POLY", tagname="ngate_12_hvt",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "PO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "PO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "PO",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, pgate_12_hvt,"POLY", tagname="pgate_12_hvt",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "PO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "PO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "PO",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, ponr,"POLY", tagname="ponr",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "PO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "PO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "PO",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, ppores,"POLY", tagname="ppores",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "PO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "PO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "PO",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, npores,"POLY", tagname="npores",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "PO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "PO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "PO",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, ppores_sblk,"POLY", tagname="ppores_sblk",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "PO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "PO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "PO",
                   lpp_subnode_purpose = "subnode"}
);
pex_conducting_layer_map(pex_matrix, npores_sblk,"POLY", tagname="npores_sblk",rpsq=0,
lpp_layer    = {lpp_polygon_layer   = "PO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "PO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "PO",
                   lpp_subnode_purpose = "subnode"}
);


pex_conducting_layer_map(pex_matrix, m1,"M1", tagname="m1",
lpp_layer    = {lpp_polygon_layer   = "M1",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "M1",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "M1",
                   lpp_subnode_purpose = "subnode"}
);


pex_conducting_layer_map(pex_matrix, m2,"M2", tagname="m2",
lpp_layer    = {lpp_polygon_layer   = "M2",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "M2",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "M2",
                   lpp_subnode_purpose = "subnode"}
);

pex_conducting_layer_map(pex_matrix, m3,   "M3", tagname="m3",
lpp_layer    = {lpp_polygon_layer   = "M3",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "M3",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "M3",
                   lpp_subnode_purpose = "subnode"}
);

pex_conducting_layer_map(pex_matrix, m4,   "M4", tagname="m4",
lpp_layer    = {lpp_polygon_layer   = "M4",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "M4",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "M4",
                   lpp_subnode_purpose = "subnode"}
);

pex_conducting_layer_map(pex_matrix, m5,   "M5", tagname="m5",
lpp_layer    = {lpp_polygon_layer   = "M5",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "M5",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "M5",
                   lpp_subnode_purpose = "subnode"}
);

pex_conducting_layer_map(pex_matrix, m6,   "M6", tagname="m6",
lpp_layer    = {lpp_polygon_layer   = "M6",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "M6",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "M6",
                   lpp_subnode_purpose = "subnode"}
);

pex_conducting_layer_map(pex_matrix, m7,   "M7", tagname="m7",
lpp_layer    = {lpp_polygon_layer   = "M7",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "M7",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "M7",
                   lpp_subnode_purpose = "subnode"}
);

pex_conducting_layer_map(pex_matrix, m8,   "M8", tagname="m8",
lpp_layer    = {lpp_polygon_layer   = "M8",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "M8",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "M8",
                   lpp_subnode_purpose = "subnode"}
);

pex_conducting_layer_map(pex_matrix, m9,   "M9", tagname="m9",
lpp_layer    = {lpp_polygon_layer   = "M9",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "M9",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "M9",
                   lpp_subnode_purpose = "subnode"}
);

pex_conducting_layer_map(pex_matrix, mrdl,   "MRDL", tagname="mrdl",//MRDL in map needs 2 be 
lpp_layer    = {lpp_polygon_layer   = "MRDL",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "MRDL",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "MRDL",
                   lpp_subnode_purpose = "subnode"}
);

/*-----------------------------------------------------------*/
/* via_layers   */
pex_via_layer_map(pex_matrix, pwell_cont, "SUBCONT", tagname="pwell_cont",
lpp_layer    = {lpp_polygon_layer   = "CO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "CO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "CO",
                   lpp_subnode_purpose = "subnode"}
);//AREA=0.144 RPV=0

pex_via_layer_map(pex_matrix, nwell_cont, "SUBCONT", tagname="nwell_cont",
lpp_layer    = {lpp_polygon_layer   = "CO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "CO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "CO",
                   lpp_subnode_purpose = "subnode"}
);//AREA=0.144 RPV=0


pex_via_layer_map(pex_matrix, codiff, "DIFFCONT", tagname="codiff",
lpp_layer    = {lpp_polygon_layer   = "CO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "CO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "CO",
                   lpp_subnode_purpose = "subnode"}
);

pex_via_layer_map(pex_matrix, copoly, "POLYCONT", tagname="copoly",
lpp_layer    = {lpp_polygon_layer   = "CO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "CO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "CO",
                   lpp_subnode_purpose = "subnode"}
);

pex_via_layer_map(pex_matrix, via1, "VIA1", tagname="via1",
lpp_layer    = {lpp_polygon_layer   = "VIA1",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "VIA1",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "VIA1",
                   lpp_subnode_purpose = "subnode"}
);
pex_via_layer_map(pex_matrix, via2, "VIA2", tagname="via2",
lpp_layer    = {lpp_polygon_layer   = "VIA2",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "VIA2",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "VIA2",
                   lpp_subnode_purpose = "subnode"}
);

pex_via_layer_map(pex_matrix, via3, "VIA3", tagname="via3",
lpp_layer    = {lpp_polygon_layer   = "VIA3",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "VIA3",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "VIA3",
                   lpp_subnode_purpose = "subnode"}
);

pex_via_layer_map(pex_matrix, via4, "VIA4", tagname="via4",
lpp_layer    = {lpp_polygon_layer   = "VIA4",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "VIA4",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "VIA4",
                   lpp_subnode_purpose = "subnode"}
);

pex_via_layer_map(pex_matrix, via5, "VIA5", tagname="via5",
lpp_layer    = {lpp_polygon_layer   = "VIA5",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "VIA5",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "VIA5",
                   lpp_subnode_purpose = "subnode"}
);

pex_via_layer_map(pex_matrix, via6, "VIA6", tagname="via6",
lpp_layer    = {lpp_polygon_layer   = "VIA6",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "VIA6",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "VIA6",
                   lpp_subnode_purpose = "subnode"}
);

pex_via_layer_map(pex_matrix, via7, "VIA7", tagname="via7",
lpp_layer    = {lpp_polygon_layer   = "VIA7",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "VIA7",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "VIA7",
                   lpp_subnode_purpose = "subnode"}
);

pex_via_layer_map(pex_matrix, via8, "VIA8", tagname="via8",
lpp_layer    = {lpp_polygon_layer   = "VIA8",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "VIA8",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "VIA8",
                   lpp_subnode_purpose = "subnode"}
);

pex_via_layer_map(pex_matrix, viardl,"VIARDL",tagname="viardl",
lpp_layer    = {lpp_polygon_layer   = "VIARDL",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "VIARDL",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "VIARDL",
                   lpp_subnode_purpose = "subnode"}
);


pex_via_layer_map(pex_matrix, l_0V_BJT_BASE_cont_NPN, "DIFFCONT",
tagname="l_0V_BJT_BASE_cont_NPN",
lpp_layer    = {lpp_polygon_layer   = "CO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "CO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "CO",
                   lpp_subnode_purpose = "subnode"}
);
pex_via_layer_map(pex_matrix, l_0V_BJT_BASE_cont, "DIFFCONT", tagname="l_0V_BJT_BASE_cont",
lpp_layer    = {lpp_polygon_layer   = "CO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "CO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "CO",
                   lpp_subnode_purpose = "subnode"}
);
pex_via_layer_map(pex_matrix, l_0V_BJT_COLL_cont, "DIFFCONT", tagname="l_0V_BJT_COLL_cont",
lpp_layer    = {lpp_polygon_layer   = "CO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "CO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "CO",
                   lpp_subnode_purpose = "subnode"}
);
pex_via_layer_map(pex_matrix, l_0V_BJT_EMIT_cont, "DIFFCONT", tagname="l_0V_BJT_EMIT_cont",
lpp_layer    = {lpp_polygon_layer   = "CO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "CO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "CO",
                   lpp_subnode_purpose = "subnode"}
);
pex_via_layer_map(pex_matrix, l_0V_BJT_COLL_cont_NPN, "DIFFCONT",
 tagname="l_0V_BJT_COLL_cont_NPN",
lpp_layer    = {lpp_polygon_layer   = "CO",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "CO",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "CO",
                   lpp_subnode_purpose = "subnode"}
);

/*marker_layers*/

pex_marker_layer_map(pex_matrix, m1pin_marker,tagname="m1pin_marker",
lpp_layer    = {lpp_polygon_layer   = "M1PIN",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "M1PIN",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "M1PIN",
                   lpp_subnode_purpose = "subnode"}
);
pex_marker_layer_map(pex_matrix, m2pin_marker,tagname="m2pin_marker",
lpp_layer    = {lpp_polygon_layer   = "M2PIN",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "M2PIN",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "M2PIN",
                   lpp_subnode_purpose = "subnode"}
);
pex_marker_layer_map(pex_matrix, m3pin_marker,tagname="m3pin_marker",
lpp_layer    = {lpp_polygon_layer   = "M3PIN",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "M3PIN",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "M3PIN",
                   lpp_subnode_purpose = "subnode"}
);
pex_marker_layer_map(pex_matrix, m4pin_marker,tagname="m4pin_marker",
lpp_layer    = {lpp_polygon_layer   = "M4PIN",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "M4PIN",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "M4PIN",
                   lpp_subnode_purpose = "subnode"}
);

pex_marker_layer_map(pex_matrix, m5pin_marker,tagname="m5pin_marker",
lpp_layer    = {lpp_polygon_layer   = "M5PIN",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "M5PIN",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "M5PIN",
                   lpp_subnode_purpose = "subnode"}
);
pex_marker_layer_map(pex_matrix, m6pin_marker,tagname="m6pin_marker",
lpp_layer    = {lpp_polygon_layer   = "M6PIN",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "M6PIN",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "M6PIN",
                   lpp_subnode_purpose = "subnode"}
);
pex_marker_layer_map(pex_matrix, m7pin_marker,tagname="m7pin_marker",
lpp_layer    = {lpp_polygon_layer   = "M7PIN",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "M7PIN",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "M7PIN",
                   lpp_subnode_purpose = "subnode"}
);
pex_marker_layer_map(pex_matrix, m8pin_marker,tagname="m8pin_marker",
lpp_layer    = {lpp_polygon_layer   = "M8PIN",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "M8PIN",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "M8PIN",
                   lpp_subnode_purpose = "subnode"}
);
pex_marker_layer_map(pex_matrix, m9pin_marker,tagname="m9pin_marker",
lpp_layer    = {lpp_polygon_layer   = "M9PIN",
                   lpp_polygon_purpose = "drawing",
                   lpp_port_layer      = "M9PIN",
                   lpp_port_purpose    = "net",
                   lpp_subnode_layer   = "M9PIN",
                   lpp_subnode_purpose = "subnode"}
);

pex_lpp_handle = pex_lpp_map_file("pex_lpp_map_file"); 
pex_process_handle = pex_process_map_file("pex_process_map_file"); //+
pex_report_handle = pex_runset_report_file("pex_runset_report_file"); //+
mw_handle = milkyway_library("XTROUT");

pex_generate_results(
    pex_matrix = pex_matrix,
    layout_database = mw_handle,
    pex_process_map_file = pex_process_handle,
    pex_runset_report_file = pex_report_handle,
    pex_lpp_map_file = pex_lpp_handle
);
}
