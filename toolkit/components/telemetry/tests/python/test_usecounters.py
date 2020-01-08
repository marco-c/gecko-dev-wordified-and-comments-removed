import
mozunit
import
sys
import
unittest
from
os
import
path
from
test_histogramtools_non_strict
import
load_histogram
TELEMETRY_ROOT_PATH
=
path
.
abspath
(
path
.
join
(
path
.
dirname
(
__file__
)
path
.
pardir
path
.
pardir
)
)
sys
.
path
.
append
(
TELEMETRY_ROOT_PATH
)
sys
.
path
.
append
(
path
.
join
(
TELEMETRY_ROOT_PATH
"
build_scripts
"
)
)
from
mozparsers
.
shared_telemetry_utils
import
ParserError
from
mozparsers
import
parse_histograms
class
TestParser
(
unittest
.
TestCase
)
:
    
def
test_usecounter_collection_enabled
(
self
)
:
        
SAMPLE_HISTOGRAM
=
{
            
"
USE_COUNTER2_TEST_HISTOGRAM
"
:
{
                
"
expires_in_version
"
:
"
never
"
                
"
kind
"
:
"
boolean
"
                
"
description
"
:
"
Whether
a
foo
used
bar
"
            
}
        
}
        
histograms
=
load_histogram
(
SAMPLE_HISTOGRAM
)
        
parse_histograms
.
load_whitelist
(
)
        
hist
=
parse_histograms
.
Histogram
(
'
USE_COUNTER2_TEST_HISTOGRAM
'
                                          
histograms
[
'
USE_COUNTER2_TEST_HISTOGRAM
'
]
                                          
strict_type_checks
=
True
)
        
ParserError
.
exit_func
(
)
        
self
.
assertEquals
(
hist
.
dataset
(
)
"
nsITelemetry
:
:
DATASET_RELEASE_CHANNEL_OPTOUT
"
)
    
def
test_usecounter_histogram
(
self
)
:
        
SAMPLE_HISTOGRAM
=
{
            
"
USE_COUNTER2_TEST_HISTOGRAM
"
:
{
                
"
expires_in_version
"
:
"
never
"
                
"
kind
"
:
"
boolean
"
                
"
description
"
:
"
Whether
a
foo
used
bar
"
            
}
        
}
        
histograms
=
load_histogram
(
SAMPLE_HISTOGRAM
)
        
parse_histograms
.
load_whitelist
(
)
        
hist
=
parse_histograms
.
Histogram
(
'
USE_COUNTER2_TEST_HISTOGRAM
'
                                          
histograms
[
'
USE_COUNTER2_TEST_HISTOGRAM
'
]
                                          
strict_type_checks
=
True
)
        
ParserError
.
exit_func
(
)
        
self
.
assertEquals
(
hist
.
expiration
(
)
"
never
"
)
        
self
.
assertEquals
(
hist
.
kind
(
)
"
boolean
"
)
        
self
.
assertEquals
(
hist
.
description
(
)
"
Whether
a
foo
used
bar
"
)
if
__name__
=
=
'
__main__
'
:
    
mozunit
.
main
(
)
