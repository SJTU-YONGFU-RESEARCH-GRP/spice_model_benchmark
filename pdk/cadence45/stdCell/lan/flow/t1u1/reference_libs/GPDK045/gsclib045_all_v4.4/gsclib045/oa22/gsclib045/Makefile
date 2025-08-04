### (C) Copyright Cadence Design Systems Inc. 2009
### All Rights Reserved
### Licensed Materials - Property of Cadence Design Systems
###
### No part of this file may be reproduced, stored in a retrieval system,
### or transmitted in any form or by any means --- electronic, mechanical,
### photocopying, recording, or otherwise --- without prior written permission
### of Cadence Design Systems, Inc.
###
### WARRANTY:
### Use all material in this file at your own risk.  Cadence Design Systems
### makes no claims about any material contained in this file.
###
### $Revision: 1.1 $
### $Date: Thu Jul 17 11:48:32 2014 $
### *************************************************************************

LIBRARY=gsclib045
CATFILES=ACH.Cat ADD.Cat AND.Cat ANTENNA.Cat AO.Cat BMX.Cat BUF.Cat CLK.Cat DFF.Cat DLY.Cat EDFF.Cat FILL.Cat HOLD.Cat INV.Cat MDFF.Cat MX.Cat NAND.Cat NOR.Cat OA.Cat OR.Cat SDFF.Cat SEDFF.Cat SMDFF.Cat TIE.Cat TBUF.Cat TLAT.Cat XNOR.Cat XOR.Cat
TOPCATFILE=$(LIBRARY).TopCat

all:	$(CATFILES) $(TOPCATFILE)

clean: 	Makefile 
	rm -rf  $(CATFILES) $(TOPCATFILE)

%.Cat: 	Makefile
	echo "TDMCHECKPOINT=\"1.0\"" > $@ ;
	MEMBERS=`ls | grep ^$*`; \
	for i in $$MEMBERS ; do \
	    if [ -d $$i ] ; then \
		echo "$(LIBRARY)/$$i type=\"cell\"" >> $@ ; \
	    fi ; \
	done ;

$(TOPCATFILE): $(CATFILES)
	echo "TDMCHECKPOINT=\"1.0\"" > $@ ;
	for i in $+ ; do \
	    echo "$(LIBRARY)/$$i type=\"category\"" >> $@ ; \
	done ; 
