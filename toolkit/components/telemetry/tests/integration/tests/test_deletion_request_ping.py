import
mozunit
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
def
test_deletion_request_ping
(
browser
helpers
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
"
"
"
    
ping
=
helpers
.
wait_for_ping
(
browser
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
    
profile_group_id
=
ping
[
"
profileGroupId
"
]
    
helpers
.
assert_is_valid_uuid
(
client_id
)
    
helpers
.
assert_is_valid_uuid
(
profile_group_id
)
    
ping
=
helpers
.
wait_for_ping
(
browser
.
disable_telemetry
DELETION_REQUEST_PING
)
    
assert
"
clientId
"
in
ping
    
assert
"
profileGroupId
"
in
ping
    
assert
"
payload
"
in
ping
    
assert
"
environment
"
not
in
ping
[
"
payload
"
]
    
browser
.
quit
(
)
    
browser
.
start_session
(
)
    
browser
.
install_addon
(
)
    
assert
browser
.
ping_server
.
pings
[
-
1
]
=
=
ping
    
browser
.
enable_telemetry
(
)
    
main_ping
=
helpers
.
wait_for_ping
(
browser
.
restart
MAIN_SHUTDOWN_PING
)
    
assert
"
clientId
"
in
main_ping
    
new_client_id
=
main_ping
[
"
clientId
"
]
    
helpers
.
assert_is_valid_uuid
(
new_client_id
)
    
assert
new_client_id
!
=
client_id
    
assert
"
profileGroupId
"
in
main_ping
    
new_profile_group_id
=
main_ping
[
"
profileGroupId
"
]
    
helpers
.
assert_is_valid_uuid
(
new_profile_group_id
)
    
assert
new_profile_group_id
!
=
profile_group_id
    
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
    
assert
"
telemetry
.
data_upload_optin
"
in
parent_scalars
    
assert
parent_scalars
[
"
telemetry
.
data_upload_optin
"
]
is
True
    
for
ping
in
browser
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
            
helpers
.
assert_is_valid_uuid
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
            
helpers
.
assert_is_valid_uuid
(
ping
[
"
profileGroupId
"
]
)
if
__name__
=
=
"
__main__
"
:
    
mozunit
.
main
(
)
