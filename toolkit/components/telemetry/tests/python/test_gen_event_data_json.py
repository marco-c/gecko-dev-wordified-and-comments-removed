import
json
import
mozunit
import
sys
import
tempfile
import
unittest
from
StringIO
import
StringIO
from
os
import
path
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
import
gen_event_data
class
TestEventDataJson
(
unittest
.
TestCase
)
:
    
def
test_JSON_definitions_generation
(
self
)
:
        
EVENTS_YAML
=
"
"
"
with
.
optout
:
  
testme1
:
    
objects
:
[
"
test1
"
]
    
bug_numbers
:
[
1456415
]
    
notification_emails
:
[
"
telemetry
-
client
-
dev
mozilla
.
org
"
]
    
record_in_processes
:
[
"
main
"
]
    
description
:
opt
-
out
event
    
release_channel_collection
:
opt
-
out
    
expiry_version
:
never
    
extra_keys
:
      
message
:
a
message
1
with
.
optin
:
  
testme2
:
    
objects
:
[
"
test2
"
]
    
bug_numbers
:
[
1456415
]
    
notification_emails
:
[
"
telemetry
-
client
-
dev
mozilla
.
org
"
]
    
record_in_processes
:
[
"
main
"
]
    
description
:
opt
-
in
event
    
release_channel_collection
:
opt
-
in
    
expiry_version
:
never
    
extra_keys
:
      
message
:
a
message
2
        
"
"
"
        
EXPECTED_JSON
=
{
            
"
with
.
optout
"
:
{
                
"
testme1
"
:
{
                    
"
objects
"
:
[
"
test1
"
]
                    
"
expired
"
:
False
                    
"
methods
"
:
[
"
testme1
"
]
                    
"
extra_keys
"
:
[
"
message
"
]
                    
"
record_on_release
"
:
True
                
}
            
}
            
"
with
.
optin
"
:
{
                
"
testme2
"
:
{
                    
"
objects
"
:
[
"
test2
"
]
                    
"
expired
"
:
False
                    
"
methods
"
:
[
"
testme2
"
]
                    
"
extra_keys
"
:
[
"
message
"
]
                    
"
record_on_release
"
:
False
                
}
            
}
        
}
        
io
=
StringIO
(
)
        
with
tempfile
.
NamedTemporaryFile
(
suffix
=
"
.
json
"
delete
=
True
)
as
tmpfile
:
            
tmpfile
.
write
(
EVENTS_YAML
)
            
tmpfile
.
flush
(
)
            
gen_event_data
.
generate_JSON_definitions
(
io
tmpfile
.
name
)
        
event_definitions
=
json
.
loads
(
io
.
getvalue
(
)
)
        
self
.
assertEqual
(
EXPECTED_JSON
event_definitions
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
