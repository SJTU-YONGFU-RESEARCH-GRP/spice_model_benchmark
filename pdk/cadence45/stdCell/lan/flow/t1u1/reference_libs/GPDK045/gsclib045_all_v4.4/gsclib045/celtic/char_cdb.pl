#!/usr/bin/perl -w

print "$ENV{PROJECT}" ;

$lp_kit = $ENV{PROJECT} ;


open (BC_SPI, ">main_bc.scs") ;
open (WC_SPI, ">main_wc.scs") ;

print WC_SPI "// WC spectre WRAPPER\n" ;
print WC_SPI "simulator lang=spectre\n" ;
print WC_SPI "global 0\n" ;
print WC_SPI "include \"$lp_kit/TECH/GPDK045/gpdk045/models/spectre/gpdk045.scs\" section=ss\n" ;
print WC_SPI "include \"$lp_kit/LIBS/GPDK045/gsclib045/spectre/gsclib045_schematic.scs\"\n" ;
print WC_SPI "simulatorOptions options temp=125\n" ;

close WC_SPI ;

print BC_SPI "// BC spectre WRAPPER\n" ;
print BC_SPI "simulator lang=spectre\n" ;
print BC_SPI "global 0\n" ;
print BC_SPI "include \"$lp_kit/TECH/GPDK045/gpdk045/models/spectre/gpdk045.scs\" section=ff\n" ;
print BC_SPI "include \"$lp_kit/LIBS/GPDK045/gsclib045/spectre/gsclib045_schematic.scs\"\n" ;
print BC_SPI "simulatorOptions options temp=0\n" ;

close BC_SPI ;


$arg = $ARGV[0];

if ($arg) {
   @LIB_LIST = $arg ;
} else {
@LIB_LIST = (
    "$lp_kit/LIBS/GPDK045/gsclib045/timing/slow.lib",
    "$lp_kit/LIBS/GPDK045/gsclib045/timing/fast.lib",
) ;
}

foreach $library (@LIB_LIST) {
   open (LIB, "$library")  or die "$library is not a valid liberty file";
   

   while (<LIB>) {
       if (/^\s*library\s*\((\w+)\)\s*/) {
          $lib_name = $1 ;
        }
   }
   close LIB;

   $cell_list_file = "${lib_name}\.list" ;

   # print " $cell_list_file \n" ;

   open (LIST, "> $cell_list_file") ;
   print LIST "set cell_list \{ \\\n" ;
   open (LIB, "$library")  or die ;

   while (<LIB>) {
        if (/^\s*cell\s*\(\s*(\w+)\s*\)/) {
            print LIST "$1 \\\n" ;
        }
   }
   print LIST "\}\n " ;
   close LIB;


   close LIST;

         $lvl_cell = 0;
         $cg_cell = 0;
         $VDDL = 1.2;
          if ($lib_name =~ /slow/) {
             $VDD  = 1.08 ;
          } elsif ($lib_name =~ /fast/) {
             $VDD  = 1.32 ;
          }

                                                                                                                                                                               
     if ($lib_name =~ /slow/) {
        $spectre_file = "main_wc\.scs" ;
     } elsif ($lib_name =~ /fast/) {
        $spectre_file = "main_bc\.scs" ;
     }


     $outfile = "char_${lib_name}.tcl" ;


     #if (! (-e $outfile) ) {
         open (OUT, "> $outfile") ;
         print OUT "set_supply -vdd $VDD -gnd 0  \n" ; 
         if ($lvl_cell) { 
             print OUT "set_net -vdd $VDDL VDDL\n";
             $vdd = "VDD VDDL" ;
         } elsif ($cg_cell) {
            print OUT "set_net -vdd $VDD TVDD\n";
             $vdd = "VDD TVDD" ;
         }  else {
             $vdd = "VDD" ;
         }
      #}
         print OUT "read_dotlib $library\n" ;  
         print OUT "\n\n" ;
         print OUT "source $cell_list_file \n" ;  
         print OUT "\n\n" ;
         print OUT " generate_cell_lib \\\n" ; 
         print OUT "   -vdd {$vdd} \\\n" ; 
         print OUT "   -gnd {VSS} \\\n" ; 
         print OUT "   -cell_list \$cell_list \\\n" ; 
         print OUT "   -spectre_file_list $spectre_file \\\n" ; 
         print OUT "   -file ./OUTPUTS/$lib_name.cdb \\\n" ; 
         print OUT "   -text\n\n\n" ; 
         print OUT "validate_cell_lib -cdb ./OUTPUTS/$lib_name.cdb \n";   

         print "\nINFO : Processing cdb file ./OUTPUTS/$lib_name.cdb \n";
         print "INFO : Please see log file ./LOGS/${lib_name}_make_cdb.log for the details \n";
         system "make_cdb $outfile > ./LOGS/${lib_name}_make_cdb.log" ;
         print "INFO : Completed process library $lib_name \n\n" ;
         $lvl_cell = 0;
         $cg_cell = 0;

         close OUT;
}

