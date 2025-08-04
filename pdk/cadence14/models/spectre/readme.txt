//  ********************************************************************************
// 		       Advance Node PDK / Generic models			   *
//										   *
//  Copyright (c) 2014								   *	
//  Cadence Design Systems, Inc.  All rights reserved.				   *	
//										   *	
// These models represent a pseudo-process and are intended to be use		   *
// for demonstration purpose only.						   *
// Contact: gscl@cadence.com							   *
//										   *	
// *********************************************************************************
//										   *
//                                                                                 *                                                              
//    Model section description :                                                  *
//										   *
//        1.sections tt,ff,ss,fs,sf						   *
//        0.8V standard-Vt FinFET devices with different geometric		   *
//	  and corner models.							   *
//                                                                                 *
//        2.sections tt_lvt, ff_lvt, ss_lvt, fs_lvt, sf_lvt			   *
//        0.8V standard-Vt FinFET devices with different geometric		   *
//	  and corner models.							   *
//                                                                                 *
//        3.sections tt_hvt, ff_hvt, ss_hvt, fs_hvt, sf_hvt			   *
//        0.8V standard-Vt FinFET devices with different geometric		   *
//	  and corner models.							   *
//                                                                                 *
//        4.sections tt_18 ff_18, ss_18, fs_18, sf_18				   *
//	  1.8V Standard-Vt FinFET devices with different geometric		   *
//	  and corner models.							   *
//										   *
//        5.section mc							           *
//	  0.8V Standard-Vt FinFET devices statistical and mismatch models.	   *
//                                                                                 *
//        6.section mc_lvt						           *
//	  0.8V low-Vt FinFET devices statistical and mismatch models.		   *
//                                                                                 *
//        7.section mc_hvt							   *
//	  0.8V high-Vt FinFET devices statistical and mismatch models.		   *
//										   *
//        8.section mc_18							   *
//	  1.8V standard-Vt FinFET devices statistical and mismatch models.	   *
//										   *
//        9.section mc_mis							   *
//	  0.8V Standard-Vt FinFET devices mismatch part for run together	   *
//	  with corner model.							   *
//										   *
//        10.section mc_lvt_mis							   *
//	  0.8V low-Vt FinFET devices mismatch part for run together		   *
//	  with corner model.							   *
//                                                                                 *
//        11.section mc_hvt_mis							   *
//	  0.8V high-Vt FinFET devices mismatch part for run together		   *
//	  with corner model.							   *
//                                                                                 *
//        12.section mc_18_mis							   *
//	  1.8V standard-Vt FinFET devices mismatch part for run together	   *
//	  with corner model.							   *       
//    ******************************************************************************

notes: 1.  The mc_**_mis sections must be included for the corner models
       2.  If mismatch model needed to be run, set mismod=1, otherwise mismod=0 
