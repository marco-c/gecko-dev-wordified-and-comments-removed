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
gen_scalar_data
class
TestScalarDataJson
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
        
SCALARS_YAML
=
"
"
"
newscalar
:
  
withoptin
:
    
bug_numbers
:
      
-
1456415
    
description
:
opt
-
in
scalar
    
expires
:
never
    
kind
:
uint
    
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
    
release_channel_collection
:
opt
-
in
    
keyed
:
false
  
withoptout
:
    
bug_numbers
:
      
-
1456415
    
description
:
opt
-
out
scalar
    
expires
:
never
    
kind
:
string
    
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
    
release_channel_collection
:
opt
-
out
    
keyed
:
false
        
"
"
"
        
EXPECTED_JSON
=
{
            
"
newscalar
"
:
{
                
"
withoptout
"
:
{
                    
"
kind
"
:
"
nsITelemetry
:
:
SCALAR_TYPE_STRING
"
                    
"
expired
"
:
False
                    
"
record_on_release
"
:
True
                    
"
keyed
"
:
False
                
}
                
"
withoptin
"
:
{
                    
"
kind
"
:
"
nsITelemetry
:
:
SCALAR_TYPE_COUNT
"
                    
"
expired
"
:
False
                    
"
record_on_release
"
:
False
                    
"
keyed
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
SCALARS_YAML
)
            
tmpfile
.
flush
(
)
            
gen_scalar_data
.
generate_JSON_definitions
(
io
tmpfile
.
name
)
        
scalar_definitions
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
scalar_definitions
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
