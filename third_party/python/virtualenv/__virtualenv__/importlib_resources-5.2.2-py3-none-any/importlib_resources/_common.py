import
os
import
pathlib
import
tempfile
import
functools
import
contextlib
import
types
import
importlib
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
Traversable
from
.
_compat
import
wrap_spec
Package
=
Union
[
types
.
ModuleType
str
]
Resource
=
Union
[
str
os
.
PathLike
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
f
'
{
path
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
wrap_spec
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
f
'
{
package
!
r
}
is
not
a
package
'
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
wrap_spec
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
        
finally
:
            
os
.
close
(
fd
)
        
del
reader
        
yield
pathlib
.
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
functools
.
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
pathlib
.
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
