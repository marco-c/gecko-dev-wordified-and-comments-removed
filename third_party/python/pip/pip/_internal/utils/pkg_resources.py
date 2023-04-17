from
typing
import
Dict
Iterable
List
from
pip
.
_vendor
.
pkg_resources
import
yield_lines
class
DictMetadata
:
    
"
"
"
IMetadataProvider
that
reads
metadata
files
from
a
dictionary
.
"
"
"
    
def
__init__
(
self
metadata
)
:
        
self
.
_metadata
=
metadata
    
def
has_metadata
(
self
name
)
:
        
return
name
in
self
.
_metadata
    
def
get_metadata
(
self
name
)
:
        
try
:
            
return
self
.
_metadata
[
name
]
.
decode
(
)
        
except
UnicodeDecodeError
as
e
:
            
e
.
reason
+
=
f
"
in
{
name
}
file
"
            
raise
    
def
get_metadata_lines
(
self
name
)
:
        
return
yield_lines
(
self
.
get_metadata
(
name
)
)
    
def
metadata_isdir
(
self
name
)
:
        
return
False
    
def
metadata_listdir
(
self
name
)
:
        
return
[
]
    
def
run_script
(
self
script_name
namespace
)
:
        
pass
