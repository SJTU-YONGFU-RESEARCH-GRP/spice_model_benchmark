#!/bin/csh

set pwd=`pwd`
echo "VALE Framework initialization ..."
echo "   Setting VALE Framework enablement directory to $pwd"
echo "   Modifying IMFdefaults.il and testcases/.cdsinit"

rm -f tmp
sed 's:__VALE_INSTALL_DIR__:'"$pwd"':' IMFdefaults.il > tmp
mv -f tmp IMFdefaults.il
if (! $?GPDK_INSTALL_DIR) then       
   echo "   WARNING: To use the PDK features with VALE Framework, "
   echo "      please set the GPDK_INSTALL_DIR environment variable and re-run"
else
   if ($GPDK_INSTALL_DIR == "")  then
      echo "   WARNING: To use the PDK features with VALE Framework, "
      echo "      please set the GPDK_INSTALL_DIR environment variable and re-run"
   else 
      sed 's:__GPDK_INSTALL_DIR__:'"$GPDK_INSTALL_DIR"':' IMFdefaults.il > tmp
      mv -f tmp IMFdefaults.il
      echo "   INFO: GPDK_INSTALL_DIR is set to $GPDK_INSTALL_DIR"
  endif
endif 

sed 's:__VALE_INSTALL_DIR__:'"$pwd"':' testcases/.cdsinit > tmp
mv -f tmp testcases/.cdsinit
## Point LOOK.MODIFY.cdsinit to .cdsinit
rm -f testcases/LOOK.MODIFY.cdsinit
ln -s .cdsinit testcases/LOOK.MODIFY.cdsinit

echo "Complete."


