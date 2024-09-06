from
telemetry_harness
.
ping_filters
import
(
    
ANY_PING
    
DELETION_REQUEST_PING
    
MAIN_SHUTDOWN_PING
)
from
telemetry_harness
.
testcase
import
TelemetryTestCase
class
TestDeletionRequestPing
(
TelemetryTestCase
)
:
    
"
"
"
Tests
for
"
deletion
-
request
"
ping
.
"
"
"
    
def
test_deletion_request_ping_across_sessions
(
self
)
:
        
"
"
"
Test
the
"
deletion
-
request
"
ping
behaviour
across
sessions
.
"
"
"
        
ping
=
self
.
wait_for_ping
(
self
.
install_addon
ANY_PING
)
        
client_id
=
ping
[
"
clientId
"
]
        
self
.
assertIsValidUUID
(
client_id
)
        
profile_group_id
=
ping
[
"
profileGroupId
"
]
        
self
.
assertIsValidUUID
(
profile_group_id
)
        
ping
=
self
.
wait_for_ping
(
self
.
disable_telemetry
DELETION_REQUEST_PING
)
        
self
.
assertIn
(
"
clientId
"
ping
)
        
self
.
assertIn
(
"
profileGroupId
"
ping
)
        
self
.
assertIn
(
"
payload
"
ping
)
        
self
.
assertNotIn
(
"
environment
"
ping
[
"
payload
"
]
)
        
self
.
quit_browser
(
)
        
self
.
start_browser
(
)
        
self
.
install_addon
(
)
        
self
.
assertEqual
(
self
.
ping_server
.
pings
[
-
1
]
ping
)
        
self
.
enable_telemetry
(
)
        
with
self
.
marionette
.
using_context
(
self
.
marionette
.
CONTEXT_CHROME
)
:
            
return
self
.
marionette
.
execute_async_script
(
                
"
"
"
                
let
[
resolve
]
=
arguments
;
                
const
{
ClientID
}
=
ChromeUtils
.
importESModule
(
                  
"
resource
:
/
/
gre
/
modules
/
ClientID
.
sys
.
mjs
"
                
)
;
                
ClientID
.
getClientID
(
)
.
then
(
resolve
)
;
                
"
"
"
                
script_timeout
=
1000
            
)
        
main_ping
=
self
.
wait_for_ping
(
self
.
restart_browser
MAIN_SHUTDOWN_PING
)
        
self
.
assertIn
(
"
clientId
"
main_ping
)
        
self
.
assertIsValidUUID
(
main_ping
[
"
clientId
"
]
)
        
self
.
assertNotEqual
(
main_ping
[
"
clientId
"
]
client_id
)
        
self
.
assertIsValidUUID
(
main_ping
[
"
profileGroupId
"
]
)
        
self
.
assertNotEqual
(
main_ping
[
"
profileGroupId
"
]
profile_group_id
)
        
parent_scalars
=
main_ping
[
"
payload
"
]
[
"
processes
"
]
[
"
parent
"
]
[
"
scalars
"
]
        
self
.
assertIn
(
"
telemetry
.
data_upload_optin
"
parent_scalars
)
        
self
.
assertIs
(
parent_scalars
[
"
telemetry
.
data_upload_optin
"
]
True
)
        
for
ping
in
self
.
ping_server
.
pings
:
            
if
"
clientId
"
in
ping
:
                
self
.
assertIsValidUUID
(
ping
[
"
clientId
"
]
)
            
if
"
profileGroupId
"
in
ping
:
                
self
.
assertIsValidUUID
(
ping
[
"
profileGroupId
"
]
)
