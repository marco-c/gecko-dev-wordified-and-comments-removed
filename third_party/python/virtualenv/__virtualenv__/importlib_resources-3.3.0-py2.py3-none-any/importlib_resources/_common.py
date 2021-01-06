from
__future__
import
absolute_import
import
os
import
tempfile
import
contextlib
import
types
import
importlib
from
.
_compat
import
(
    
Path
FileNotFoundError
    
singledispatch
package_spec
    
)
if
False
:
    
from
typing
import
Union
Any
Optional
    
from
.
abc
import
ResourceReader
    
Package
=
Union
[
types
.
ModuleType
str
]
def
files
(
package
)
:
    
"
"
"
    
Get
a
Traversable
resource
from
a
package
    
"
"
"
    
return
from_package
(
get_package
(
package
)
)
def
normalize_path
(
path
)
:
    
"
"
"
Normalize
a
path
by
ensuring
it
is
a
string
.
    
If
the
resulting
string
contains
path
separators
an
exception
is
raised
.
    
"
"
"
    
str_path
=
str
(
path
)
    
parent
file_name
=
os
.
path
.
split
(
str_path
)
    
if
parent
:
        
raise
ValueError
(
'
{
!
r
}
must
be
only
a
file
name
'
.
format
(
path
)
)
    
return
file_name
def
get_resource_reader
(
package
)
:
    
"
"
"
    
Return
the
package
'
s
loader
if
it
'
s
a
ResourceReader
.
    
"
"
"
    
spec
=
package
.
__spec__
    
reader
=
getattr
(
spec
.
loader
'
get_resource_reader
'
None
)
    
if
reader
is
None
:
        
return
None
    
return
reader
(
spec
.
name
)
def
resolve
(
cand
)
:
    
return
(
        
cand
if
isinstance
(
cand
types
.
ModuleType
)
        
else
importlib
.
import_module
(
cand
)
        
)
def
get_package
(
package
)
:
    
"
"
"
Take
a
package
name
or
module
object
and
return
the
module
.
    
Raise
an
exception
if
the
resolved
module
is
not
a
package
.
    
"
"
"
    
resolved
=
resolve
(
package
)
    
if
package_spec
(
resolved
)
.
submodule_search_locations
is
None
:
        
raise
TypeError
(
'
{
!
r
}
is
not
a
package
'
.
format
(
package
)
)
    
return
resolved
def
from_package
(
package
)
:
    
"
"
"
    
Return
a
Traversable
object
for
the
given
package
.
    
"
"
"
    
spec
=
package_spec
(
package
)
    
reader
=
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
    
return
reader
.
files
(
)
contextlib
.
contextmanager
def
_tempfile
(
reader
suffix
=
'
'
)
:
    
fd
raw_path
=
tempfile
.
mkstemp
(
suffix
=
suffix
)
    
try
:
        
os
.
write
(
fd
reader
(
)
)
        
os
.
close
(
fd
)
        
del
reader
        
yield
Path
(
raw_path
)
    
finally
:
        
try
:
            
os
.
remove
(
raw_path
)
        
except
FileNotFoundError
:
            
pass
singledispatch
def
as_file
(
path
)
:
    
"
"
"
    
Given
a
Traversable
object
return
that
object
as
a
    
path
on
the
local
file
system
in
a
context
manager
.
    
"
"
"
    
return
_tempfile
(
path
.
read_bytes
suffix
=
path
.
name
)
as_file
.
register
(
Path
)
contextlib
.
contextmanager
def
_
(
path
)
:
    
"
"
"
    
Degenerate
behavior
for
pathlib
.
Path
objects
.
    
"
"
"
    
yield
path
