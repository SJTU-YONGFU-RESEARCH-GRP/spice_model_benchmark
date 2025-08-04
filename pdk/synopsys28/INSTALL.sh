
echo 
echo "====================================="
echo 
echo "Changin path in SOURCEME file"
pdk_path=`dirname $0`
pdk_path=`cd $pdk_path; pwd`
echo "export SAED32_28_PDK=${pdk_path}" > $pdk_path/SOURCEME
echo 
echo "To use PDK follow instructions in ${pdk_path}/README"
echo 
echo "====================================="
echo 
