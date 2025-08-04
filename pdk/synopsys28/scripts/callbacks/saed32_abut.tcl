proc saedAbut {instA instB termA termB abutDir exConn event } {
    #Condition to determine whether abottor is Big
    set pinsizeA   [oa::getValue [oa::PropFind $termA "pycPinSize"]] 
    set pinsizeB   [oa::getValue [oa::PropFind $termB "pycPinSize"]]

    if { $pinsizeA > $pinsizeB } {
        set abuttorIsBig 1
    } elseif {$pinsizeA < $pinsizeB } {
        set abuttorIsBig 2
    } else {
        set abuttorIsBig 0
    }
    
    #Get the Values Stored on the property pycAbutRules 
    set abutRulesValA [split [oa::getValue [oa::PropFind $termA "pycAbutRules"]] "^"]
    set abutRulesValB [split [oa::getValue [oa::PropFind $termB "pycAbutRules"]] "^"]
    set completeEvent [join [split [list $event $exConn $abuttorIsBig] " "] "."]

    if { $event == 1 } {
       set instAnoabutspacing  [lindex [split [lindex $abutRulesValA 6] ":"] 2]
       return [list $instAnoabutspacing 0.0]
    }
    switch -regexp $completeEvent {
        "^2.1.0" {
            set abuttorindex 3
            set abuteeindex 3
          }
        "^2.1.1" {
            set abuttorindex 1
            set abuteeindex 5
          }
        "^2.1.2" {
            set abuttorindex 5
            set abuteeindex 1
          }
        "^2.0.0" {
            set abuttorindex 2
            set abuteeindex 2
          }
        "^2.0.1" {
            set abuttorindex 0
            set abuteeindex 4
          }
        "^2.0.2" {
            set abuttorindex 4
            set abuteeindex 0
          }
        "^3.*.*.*.*" {
          }
    }
    
    # Get the Param Name and Param Value from the Lists abutRulesValA & abutRulesValB
    # and set accordingly  based on the event. 
    if {$event !=3 } {
        regsub -all {:}  [split [lindex [split [lindex $abutRulesValA $abuttorindex]\
        '\;'] 1] '\,']  " " instAParamsList
        regsub -all {:}  [split [lindex [split [lindex $abutRulesValB $abuteeindex]\
        '\;'] 2] '\,']  " " instBParamsList
        for {set i 0} {$i<[llength $instAParamsList]} {incr i 2} {
            iPDK_setParamValue [lindex $instAParamsList $i]\
            [lindex $instAParamsList [expr $i+1]]  $instA 0  
        }
        for {set i 0} {$i<[llength $instBParamsList]} {incr i 2} {
            iPDK_setParamValue [lindex $instBParamsList $i] [lindex $instBParamsList [expr $i+1]] $instB 0  
        }
    }

    if { $event == 2 } {
        return true
    }
}