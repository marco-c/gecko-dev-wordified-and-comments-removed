import
os
import
sys
import
tempfile
from
.
import
abc
as
resources_abc
from
contextlib
import
contextmanager
suppress
from
importlib
import
import_module
from
importlib
.
abc
import
ResourceLoader
from
io
import
BytesIO
TextIOWrapper
from
pathlib
import
Path
from
types
import
ModuleType
from
typing
import
Iterable
Iterator
Optional
Set
Union
from
typing
import
cast
from
typing
.
io
import
BinaryIO
TextIO
from
zipfile
import
ZipFile
Package
=
Union
[
ModuleType
str
]
if
sys
.
version_info
>
=
(
3
6
)
:
    
Resource
=
Union
[
str
os
.
PathLike
]
else
:
    
Resource
=
str
def
_get_package
(
package
)
-
>
ModuleType
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
    
If
a
name
the
module
is
imported
.
If
the
passed
or
imported
module
    
object
is
not
a
package
raise
an
exception
.
    
"
"
"
    
if
hasattr
(
package
'
__spec__
'
)
:
        
if
package
.
__spec__
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
.
__spec__
.
name
)
)
        
else
:
            
return
package
    
else
:
        
module
=
import_module
(
package
)
        
if
module
.
__spec__
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
        
else
:
            
return
module
def
_normalize_path
(
path
)
-
>
str
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
    
else
:
        
return
file_name
def
_get_resource_reader
(
        
package
:
ModuleType
)
-
>
Optional
[
resources_abc
.
ResourceReader
]
:
    
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
cast
(
resources_abc
.
ResourceReader
reader
(
spec
.
name
)
)
def
open_binary
(
package
:
Package
resource
:
Resource
)
-
>
BinaryIO
:
    
"
"
"
Return
a
file
-
like
object
opened
for
binary
reading
of
the
resource
.
"
"
"
    
resource
=
_normalize_path
(
resource
)
    
package
=
_get_package
(
package
)
    
reader
=
_get_resource_reader
(
package
)
    
if
reader
is
not
None
:
        
return
reader
.
open_resource
(
resource
)
    
absolute_package_path
=
os
.
path
.
abspath
(
package
.
__spec__
.
origin
)
    
package_path
=
os
.
path
.
dirname
(
absolute_package_path
)
    
full_path
=
os
.
path
.
join
(
package_path
resource
)
    
try
:
        
return
open
(
full_path
mode
=
'
rb
'
)
    
except
OSError
:
        
loader
=
cast
(
ResourceLoader
package
.
__spec__
.
loader
)
        
data
=
None
        
if
hasattr
(
package
.
__spec__
.
loader
'
get_data
'
)
:
            
with
suppress
(
OSError
)
:
                
data
=
loader
.
get_data
(
full_path
)
        
if
data
is
None
:
            
package_name
=
package
.
__spec__
.
name
            
message
=
'
{
!
r
}
resource
not
found
in
{
!
r
}
'
.
format
(
                
resource
package_name
)
            
raise
FileNotFoundError
(
message
)
        
else
:
            
return
BytesIO
(
data
)
def
open_text
(
package
:
Package
              
resource
:
Resource
              
encoding
:
str
=
'
utf
-
8
'
              
errors
:
str
=
'
strict
'
)
-
>
TextIO
:
    
"
"
"
Return
a
file
-
like
object
opened
for
text
reading
of
the
resource
.
"
"
"
    
resource
=
_normalize_path
(
resource
)
    
package
=
_get_package
(
package
)
    
reader
=
_get_resource_reader
(
package
)
    
if
reader
is
not
None
:
        
return
TextIOWrapper
(
reader
.
open_resource
(
resource
)
encoding
errors
)
    
absolute_package_path
=
os
.
path
.
abspath
(
package
.
__spec__
.
origin
)
    
package_path
=
os
.
path
.
dirname
(
absolute_package_path
)
    
full_path
=
os
.
path
.
join
(
package_path
resource
)
    
try
:
        
return
open
(
full_path
mode
=
'
r
'
encoding
=
encoding
errors
=
errors
)
    
except
OSError
:
        
loader
=
cast
(
ResourceLoader
package
.
__spec__
.
loader
)
        
data
=
None
        
if
hasattr
(
package
.
__spec__
.
loader
'
get_data
'
)
:
            
with
suppress
(
OSError
)
:
                
data
=
loader
.
get_data
(
full_path
)
        
if
data
is
None
:
            
package_name
=
package
.
__spec__
.
name
            
message
=
'
{
!
r
}
resource
not
found
in
{
!
r
}
'
.
format
(
                
resource
package_name
)
            
raise
FileNotFoundError
(
message
)
        
else
:
            
return
TextIOWrapper
(
BytesIO
(
data
)
encoding
errors
)
def
read_binary
(
package
:
Package
resource
:
Resource
)
-
>
bytes
:
    
"
"
"
Return
the
binary
contents
of
the
resource
.
"
"
"
    
resource
=
_normalize_path
(
resource
)
    
package
=
_get_package
(
package
)
    
with
open_binary
(
package
resource
)
as
fp
:
        
return
fp
.
read
(
)
def
read_text
(
package
:
Package
              
resource
:
Resource
              
encoding
:
str
=
'
utf
-
8
'
              
errors
:
str
=
'
strict
'
)
-
>
str
:
    
"
"
"
Return
the
decoded
string
of
the
resource
.
    
The
decoding
-
related
arguments
have
the
same
semantics
as
those
of
    
bytes
.
decode
(
)
.
    
"
"
"
    
resource
=
_normalize_path
(
resource
)
    
package
=
_get_package
(
package
)
    
with
open_text
(
package
resource
encoding
errors
)
as
fp
:
        
return
fp
.
read
(
)
contextmanager
def
path
(
package
:
Package
resource
:
Resource
)
-
>
Iterator
[
Path
]
:
    
"
"
"
A
context
manager
providing
a
file
path
object
to
the
resource
.
    
If
the
resource
does
not
already
exist
on
its
own
on
the
file
system
    
a
temporary
file
will
be
created
.
If
the
file
was
created
the
file
    
will
be
deleted
upon
exiting
the
context
manager
(
no
exception
is
    
raised
if
the
file
was
deleted
prior
to
the
context
manager
    
exiting
)
.
    
"
"
"
    
resource
=
_normalize_path
(
resource
)
    
package
=
_get_package
(
package
)
    
reader
=
_get_resource_reader
(
package
)
    
if
reader
is
not
None
:
        
try
:
            
yield
Path
(
reader
.
resource_path
(
resource
)
)
            
return
        
except
FileNotFoundError
:
            
pass
    
package_directory
=
Path
(
package
.
__spec__
.
origin
)
.
parent
    
file_path
=
package_directory
/
resource
    
if
file_path
.
exists
(
)
:
        
yield
file_path
    
else
:
        
with
open_binary
(
package
resource
)
as
fp
:
            
data
=
fp
.
read
(
)
        
fd
raw_path
=
tempfile
.
mkstemp
(
)
        
try
:
            
os
.
write
(
fd
data
)
            
os
.
close
(
fd
)
            
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
def
is_resource
(
package
:
Package
name
:
str
)
-
>
bool
:
    
"
"
"
True
if
name
is
a
resource
inside
package
.
    
Directories
are
*
not
*
resources
.
    
"
"
"
    
package
=
_get_package
(
package
)
    
_normalize_path
(
name
)
    
reader
=
_get_resource_reader
(
package
)
    
if
reader
is
not
None
:
        
return
reader
.
is_resource
(
name
)
    
try
:
        
package_contents
=
set
(
contents
(
package
)
)
    
except
(
NotADirectoryError
FileNotFoundError
)
:
        
return
False
    
if
name
not
in
package_contents
:
        
return
False
    
path
=
Path
(
package
.
__spec__
.
origin
)
.
parent
/
name
    
if
path
.
is_file
(
)
:
        
return
True
    
if
path
.
is_dir
(
)
:
        
return
False
    
archive_path
=
package
.
__spec__
.
loader
.
archive
    
package_directory
=
Path
(
package
.
__spec__
.
origin
)
.
parent
    
with
ZipFile
(
archive_path
)
as
zf
:
        
toc
=
zf
.
namelist
(
)
    
relpath
=
package_directory
.
relative_to
(
archive_path
)
    
candidate_path
=
relpath
/
name
    
for
entry
in
toc
:
        
try
:
            
relative_to_candidate
=
Path
(
entry
)
.
relative_to
(
candidate_path
)
        
except
ValueError
:
            
continue
        
return
len
(
relative_to_candidate
.
parts
)
=
=
0
    
raise
AssertionError
(
'
Impossible
situation
'
)
def
contents
(
package
:
Package
)
-
>
Iterable
[
str
]
:
    
"
"
"
Return
an
iterable
of
entries
in
package
.
    
Note
that
not
all
entries
are
resources
.
Specifically
directories
are
    
not
considered
resources
.
Use
is_resource
(
)
on
each
entry
returned
here
    
to
check
if
it
is
a
resource
or
not
.
    
"
"
"
    
package
=
_get_package
(
package
)
    
reader
=
_get_resource_reader
(
package
)
    
if
reader
is
not
None
:
        
return
reader
.
contents
(
)
    
if
(
package
.
__spec__
.
origin
=
=
'
namespace
'
and
            
not
package
.
__spec__
.
has_location
)
:
        
return
(
)
    
package_directory
=
Path
(
package
.
__spec__
.
origin
)
.
parent
    
try
:
        
return
os
.
listdir
(
str
(
package_directory
)
)
    
except
(
NotADirectoryError
FileNotFoundError
)
:
        
archive_path
=
getattr
(
package
.
__spec__
.
loader
'
archive
'
None
)
        
if
archive_path
is
None
:
            
raise
        
relpath
=
package_directory
.
relative_to
(
archive_path
)
        
with
ZipFile
(
archive_path
)
as
zf
:
            
toc
=
zf
.
namelist
(
)
        
subdirs_seen
=
set
(
)
        
subdirs_returned
=
[
]
        
for
filename
in
toc
:
            
path
=
Path
(
filename
)
            
if
path
.
parts
[
:
len
(
relpath
.
parts
)
]
!
=
relpath
.
parts
:
                
continue
            
subparts
=
path
.
parts
[
len
(
relpath
.
parts
)
:
]
            
if
len
(
subparts
)
=
=
1
:
                
subdirs_returned
.
append
(
subparts
[
0
]
)
            
elif
len
(
subparts
)
>
1
:
                
subdir
=
subparts
[
0
]
                
if
subdir
not
in
subdirs_seen
:
                    
subdirs_seen
.
add
(
subdir
)
                    
subdirs_returned
.
append
(
subdir
)
        
return
subdirs_returned
