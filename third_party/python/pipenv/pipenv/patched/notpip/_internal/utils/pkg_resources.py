from
pipenv
.
patched
.
notpip
.
_vendor
.
pkg_resources
import
yield_lines
from
pipenv
.
patched
.
notpip
.
_vendor
.
six
import
ensure_str
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
typing
import
MYPY_CHECK_RUNNING
if
MYPY_CHECK_RUNNING
:
    
from
typing
import
Dict
Iterable
List
class
DictMetadata
(
object
)
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
ensure_str
(
self
.
_metadata
[
name
]
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
"
in
{
}
file
"
.
format
(
name
)
            
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
