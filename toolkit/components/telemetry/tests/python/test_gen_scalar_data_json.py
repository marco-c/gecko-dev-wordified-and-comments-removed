import
json
import
mozunit
import
os
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
expires
"
:
"
never
"
                    
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
                    
"
stores
"
:
[
"
main
"
]
                
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
expires
"
:
"
never
"
                    
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
                    
"
stores
"
:
[
"
main
"
]
                
}
            
}
        
}
        
io
=
StringIO
(
)
        
try
:
            
tmpfile
=
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
False
)
            
tmpfile
.
write
(
SCALARS_YAML
)
            
tmpfile
.
close
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
        
finally
:
            
if
tmpfile
:
                
os
.
unlink
(
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
