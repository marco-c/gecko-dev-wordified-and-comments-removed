import
time
from
.
intel_power_gadget
import
IntelPowerGadget
IPGResultsHandler
from
.
powerbase
import
PowerBase
class
MacIntelPower
(
PowerBase
)
:
    
"
"
"
MacIntelPower
is
the
OS
and
CPU
dependent
class
for
    
power
measurement
gathering
on
Mac
Intel
-
based
hardware
.
    
:
:
       
from
mozpower
.
macintelpower
import
MacIntelPower
       
#
duration
and
output_file_path
are
used
in
IntelPowerGadget
       
mip
=
MacIntelPower
(
ipg_measure_duration
=
600
output_file_path
=
'
power
-
testing
'
)
       
mip
.
initialize_power_measurements
(
)
       
#
Run
test
.
.
.
       
mip
.
finalize_power_measurements
(
test_name
=
'
raptor
-
test
-
name
'
)
       
perfherder_data
=
mip
.
get_perfherder_data
(
)
    
"
"
"
    
def
__init__
(
self
logger_name
=
"
mozpower
"
*
*
kwargs
)
:
        
"
"
"
Initializes
the
MacIntelPower
object
.
        
:
param
str
logger_name
:
logging
logger
name
.
Defaults
to
'
mozpower
'
.
        
:
param
dict
kwargs
:
optional
keyword
arguments
passed
to
IntelPowerGadget
.
        
"
"
"
        
PowerBase
.
__init__
(
self
logger_name
=
logger_name
os
=
"
darwin
"
cpu
=
"
intel
"
)
        
self
.
ipg
=
IntelPowerGadget
(
self
.
ipg_path
*
*
kwargs
)
        
self
.
ipg_results_handler
=
None
        
self
.
start_time
=
None
        
self
.
end_time
=
None
        
self
.
perfherder_data
=
{
}
    
def
initialize_power_measurements
(
self
)
:
        
"
"
"
Starts
power
measurement
gathering
through
IntelPowerGadget
.
"
"
"
        
self
.
_logger
.
info
(
"
Initializing
power
measurements
.
.
.
"
)
        
self
.
ipg
.
start_ipg
(
)
        
self
.
start_time
=
time
.
time
(
)
    
def
finalize_power_measurements
(
        
self
test_name
=
"
power
-
testing
"
output_dir_path
=
"
"
*
*
kwargs
    
)
:
        
"
"
"
Stops
power
measurement
gathering
through
IntelPowerGadget
cleans
the
data
        
and
produces
partial
perfherder
formatted
data
that
is
stored
in
perfherder_data
.
        
:
param
str
test_name
:
name
of
the
test
that
was
run
.
        
:
param
str
output_dir_path
:
directory
to
store
output
files
.
        
:
param
dict
kwargs
:
contains
optional
arguments
to
stop_ipg
.
        
"
"
"
        
self
.
_logger
.
info
(
"
Finalizing
power
measurements
.
.
.
"
)
        
self
.
end_time
=
time
.
time
(
)
        
self
.
ipg
.
stop_ipg
(
*
*
kwargs
)
        
if
not
output_dir_path
:
            
output_dir_path
=
self
.
ipg
.
output_dir_path
        
self
.
ipg_results_handler
=
IPGResultsHandler
(
            
self
.
ipg
.
output_files
            
output_dir_path
            
ipg_measure_duration
=
self
.
ipg
.
ipg_measure_duration
            
sampling_rate
=
self
.
ipg
.
sampling_rate
            
logger_name
=
self
.
logger_name
        
)
        
self
.
ipg_results_handler
.
clean_ipg_data
(
)
        
self
.
perfherder_data
=
(
            
self
.
ipg_results_handler
.
format_ipg_data_to_partial_perfherder
(
                
self
.
end_time
-
self
.
start_time
test_name
            
)
        
)
    
def
get_perfherder_data
(
self
)
:
        
"
"
"
Returns
the
perfherder
data
output
that
was
produced
.
        
:
returns
:
dict
        
"
"
"
        
return
self
.
perfherder_data
