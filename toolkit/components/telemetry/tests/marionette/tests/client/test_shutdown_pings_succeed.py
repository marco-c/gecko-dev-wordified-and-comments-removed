from
telemetry_harness
.
testcase
import
TelemetryTestCase
class
TestShutdownPingsSucced
(
TelemetryTestCase
)
:
    
"
"
"
Test
Firefox
shutdown
pings
.
"
"
"
    
def
test_shutdown_pings_succeed
(
self
)
:
        
"
"
"
Test
that
known
Firefox
shutdown
pings
are
received
.
"
"
"
        
ping_types
=
(
            
"
event
"
            
"
first
-
shutdown
"
            
"
main
"
            
"
new
-
profile
"
        
)
        
pings
=
self
.
wait_for_pings
(
            
self
.
restart_browser
lambda
p
:
p
[
"
type
"
]
in
ping_types
len
(
ping_types
)
        
)
        
self
.
assertEqual
(
len
(
pings
)
len
(
ping_types
)
)
        
self
.
assertEqual
(
set
(
ping_types
)
set
(
p
[
"
type
"
]
for
p
in
pings
)
)
