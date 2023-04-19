import
abc
import
sys
import
pathlib
from
contextlib
import
suppress
if
sys
.
version_info
>
=
(
3
10
)
:
    
from
zipfile
import
Path
as
ZipPath
else
:
    
from
zipp
import
Path
as
ZipPath
try
:
    
from
typing
import
runtime_checkable
except
ImportError
:
    
def
runtime_checkable
(
cls
)
:
        
return
cls
try
:
    
from
typing
import
Protocol
except
ImportError
:
    
Protocol
=
abc
.
ABC
class
TraversableResourcesLoader
:
    
"
"
"
    
Adapt
loaders
to
provide
TraversableResources
and
other
    
compatibility
.
    
Used
primarily
for
Python
3
.
9
and
earlier
where
the
native
    
loaders
do
not
yet
implement
TraversableResources
.
    
"
"
"
    
def
__init__
(
self
spec
)
:
        
self
.
spec
=
spec
    
property
    
def
path
(
self
)
:
        
return
self
.
spec
.
origin
    
def
get_resource_reader
(
self
name
)
:
        
from
.
import
readers
_adapters
        
def
_zip_reader
(
spec
)
:
            
with
suppress
(
AttributeError
)
:
                
return
readers
.
ZipReader
(
spec
.
loader
spec
.
name
)
        
def
_namespace_reader
(
spec
)
:
            
with
suppress
(
AttributeError
ValueError
)
:
                
return
readers
.
NamespaceReader
(
spec
.
submodule_search_locations
)
        
def
_available_reader
(
spec
)
:
            
with
suppress
(
AttributeError
)
:
                
return
spec
.
loader
.
get_resource_reader
(
spec
.
name
)
        
def
_native_reader
(
spec
)
:
            
reader
=
_available_reader
(
spec
)
            
return
reader
if
hasattr
(
reader
'
files
'
)
else
None
        
def
_file_reader
(
spec
)
:
            
try
:
                
path
=
pathlib
.
Path
(
self
.
path
)
            
except
TypeError
:
                
return
None
            
if
path
.
exists
(
)
:
                
return
readers
.
FileReader
(
self
)
        
return
(
            
_native_reader
(
self
.
spec
)
            
or
            
_zip_reader
(
self
.
spec
)
            
or
            
_namespace_reader
(
self
.
spec
)
            
or
            
_file_reader
(
self
.
spec
)
            
or
_adapters
.
CompatibilityFiles
(
self
.
spec
)
        
)
def
wrap_spec
(
package
)
:
    
"
"
"
    
Construct
a
package
spec
with
traversable
compatibility
    
on
the
spec
/
loader
/
reader
.
    
Supersedes
_adapters
.
wrap_spec
to
use
TraversableResourcesLoader
    
from
above
for
older
Python
compatibility
(
<
3
.
10
)
.
    
"
"
"
    
from
.
import
_adapters
    
return
_adapters
.
SpecLoaderAdapter
(
package
.
__spec__
TraversableResourcesLoader
)
