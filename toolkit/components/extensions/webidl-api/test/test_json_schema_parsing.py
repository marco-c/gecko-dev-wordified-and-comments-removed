import
json
import
os
import
sys
from
textwrap
import
dedent
import
mozpack
.
path
as
mozpath
import
mozunit
import
pytest
OUR_DIR
=
mozpath
.
abspath
(
mozpath
.
dirname
(
__file__
)
)
sys
.
path
.
append
(
OUR_DIR
)
import
helpers
helpers
.
setup
(
)
from
GenerateWebIDLBindings
import
APIEvent
APIFunction
APINamespace
APIType
Schemas
def
test_parse_simple_single_api_namespace
(
write_jsonschema_fixtures
)
:
    
"
"
"
    
Test
Basic
loading
and
parsing
a
single
API
JSONSchema
:
    
-
single
line
comments
outside
of
the
json
structure
are
ignored
    
-
parse
a
simple
namespace
that
includes
one
permission
type
      
function
and
event
    
"
"
"
    
schema_dir
=
write_jsonschema_fixtures
(
        
{
            
"
test_api
.
json
"
:
dedent
(
                
"
"
"
          
/
/
Single
line
comments
added
before
the
JSON
data
are
tolerated
          
/
/
and
ignored
.
          
[
            
{
              
"
namespace
"
:
"
fantasyApi
"
              
"
permissions
"
:
[
"
fantasyPermission
"
]
              
"
types
"
:
[
                  
{
                    
"
id
"
:
"
MyType
"
                    
"
type
"
:
"
string
"
                    
"
choices
"
:
[
"
value1
"
"
value2
"
]
                  
}
              
]
              
"
functions
"
:
[
                
{
                  
"
name
"
:
"
myMethod
"
                  
"
type
"
:
"
function
"
                  
"
parameters
"
:
[
                    
{
"
name
"
:
"
fnParam
"
"
type
"
:
"
string
"
}
                    
{
"
name
"
:
"
fnRefParam
"
"
ref
"
:
"
MyType
"
}
                  
]
                
}
              
]
              
"
events
"
:
[
                
{
                  
"
name
"
:
"
onSomeEvent
"
                  
"
type
"
:
"
function
"
                  
"
parameters
"
:
[
                     
{
"
name
"
:
"
evParam
"
"
type
"
:
"
string
"
}
                     
{
"
name
"
:
"
evRefParam
"
"
ref
"
:
"
MyType
"
}
                  
]
                
}
              
]
            
}
          
]
        
"
"
"
            
)
        
}
    
)
    
schemas
=
Schemas
(
)
    
schemas
.
load_schemas
(
schema_dir
"
toolkit
"
)
    
assert
schemas
.
get_all_namespace_names
(
)
=
=
[
"
fantasyApi
"
]
    
apiNs
=
schemas
.
api_namespaces
[
"
fantasyApi
"
]
    
assert
isinstance
(
apiNs
APINamespace
)
    
assert
apiNs
.
in_toolkit
    
assert
not
apiNs
.
in_browser
    
assert
not
apiNs
.
in_mobile
    
assert
apiNs
.
api_path_string
=
=
"
fantasyApi
"
    
schemas
.
parse_schemas
(
)
    
assert
set
(
[
"
fantasyPermission
"
]
)
=
=
apiNs
.
permissions
    
assert
[
"
MyType
"
]
=
=
list
(
apiNs
.
types
.
keys
(
)
)
    
assert
[
"
myMethod
"
]
=
=
list
(
apiNs
.
functions
.
keys
(
)
)
    
assert
[
"
onSomeEvent
"
]
=
=
list
(
apiNs
.
events
.
keys
(
)
)
    
type_entry
=
apiNs
.
types
.
get
(
"
MyType
"
)
    
fn_entry
=
apiNs
.
functions
.
get
(
"
myMethod
"
)
    
ev_entry
=
apiNs
.
events
.
get
(
"
onSomeEvent
"
)
    
assert
isinstance
(
type_entry
APIType
)
    
assert
isinstance
(
fn_entry
APIFunction
)
    
assert
isinstance
(
ev_entry
APIEvent
)
def
test_parse_error_on_types_without_id_or_extend
(
    
base_schema
write_jsonschema_fixtures
)
:
    
"
"
"
    
Test
parsing
types
without
id
or
extend
raise
an
error
while
parsing
.
    
"
"
"
    
schema_dir
=
write_jsonschema_fixtures
(
        
{
            
"
test_broken_types
.
json
"
:
json
.
dumps
(
                
[
                    
{
                        
*
*
base_schema
(
)
                        
"
namespace
"
:
"
testBrokenTypeAPI
"
                        
"
types
"
:
[
                            
{
                            
}
                        
]
                    
}
                
]
            
)
        
}
    
)
    
schemas
=
Schemas
(
)
    
schemas
.
load_schemas
(
schema_dir
"
toolkit
"
)
    
with
pytest
.
raises
(
        
Exception
        
match
=
r
"
Error
loading
schema
type
data
defined
in
'
toolkit
testBrokenTypeAPI
'
"
    
)
:
        
schemas
.
parse_schemas
(
)
def
test_parse_ignores_unsupported_types
(
base_schema
write_jsonschema_fixtures
)
:
    
"
"
"
    
Test
parsing
types
without
id
or
extend
raise
an
error
while
parsing
.
    
"
"
"
    
schema_dir
=
write_jsonschema_fixtures
(
        
{
            
"
test_broken_types
.
json
"
:
json
.
dumps
(
                
[
                    
{
                        
*
*
base_schema
(
)
                        
"
namespace
"
:
"
testUnsupportedTypesAPI
"
                        
"
types
"
:
[
                            
{
                                
"
id
"
:
"
AnUnsupportedType
"
                                
"
type
"
:
"
string
"
                                
"
unsupported
"
:
True
                            
}
                            
{
                                
"
unsupported
"
:
True
                            
}
                            
{
"
id
"
:
"
ASupportedType
"
"
type
"
:
"
string
"
}
                        
]
                    
}
                
]
            
)
        
}
    
)
    
schemas
=
Schemas
(
)
    
schemas
.
load_schemas
(
schema_dir
"
toolkit
"
)
    
schemas
.
parse_schemas
(
)
    
apiNs
=
schemas
.
api_namespaces
[
"
testUnsupportedTypesAPI
"
]
    
assert
set
(
apiNs
.
types
.
keys
(
)
)
=
=
set
(
[
"
ASupportedType
"
]
)
def
test_parse_error_on_namespace_with_inconsistent_max_manifest_version
(
    
base_schema
write_jsonschema_fixtures
tmpdir
)
:
    
"
"
"
    
Test
parsing
types
without
id
or
extend
raise
an
error
while
parsing
.
    
"
"
"
    
browser_schema_dir
=
os
.
path
.
join
(
tmpdir
"
browser
"
)
    
mobile_schema_dir
=
os
.
path
.
join
(
tmpdir
"
mobile
"
)
    
os
.
mkdir
(
browser_schema_dir
)
    
os
.
mkdir
(
mobile_schema_dir
)
    
base_namespace_schema
=
{
        
*
*
base_schema
(
)
        
"
namespace
"
:
"
testInconsistentMaxManifestVersion
"
    
}
    
browser_schema
=
{
*
*
base_namespace_schema
"
max_manifest_version
"
:
2
}
    
mobile_schema
=
{
*
*
base_namespace_schema
"
max_manifest_version
"
:
3
}
    
write_jsonschema_fixtures
(
        
{
"
test_inconsistent_maxmv
.
json
"
:
json
.
dumps
(
[
browser_schema
]
)
}
        
browser_schema_dir
    
)
    
write_jsonschema_fixtures
(
        
{
"
test_inconsistent_maxmv
.
json
"
:
json
.
dumps
(
[
mobile_schema
]
)
}
mobile_schema_dir
    
)
    
schemas
=
Schemas
(
)
    
schemas
.
load_schemas
(
browser_schema_dir
"
browser
"
)
    
schemas
.
load_schemas
(
mobile_schema_dir
"
mobile
"
)
    
with
pytest
.
raises
(
        
TypeError
        
match
=
r
"
Error
loading
schema
data
-
overwriting
existing
max_manifest_version
value
"
    
)
:
        
schemas
.
parse_schemas
(
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
