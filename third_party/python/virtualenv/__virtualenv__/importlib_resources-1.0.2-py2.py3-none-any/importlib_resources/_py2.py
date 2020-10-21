import
os
import
errno
import
tempfile
from
.
_compat
import
FileNotFoundError
from
contextlib
import
contextmanager
from
importlib
import
import_module
from
io
import
BytesIO
TextIOWrapper
open
as
io_open
from
pathlib2
import
Path
from
zipfile
import
ZipFile
def
_get_package
(
package
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
    
if
isinstance
(
package
basestring
)
:
        
module
=
import_module
(
package
)
    
else
:
        
module
=
package
    
if
not
hasattr
(
module
'
__path__
'
)
:
        
raise
TypeError
(
"
{
!
r
}
is
not
a
package
"
.
format
(
package
)
)
    
return
module
def
_normalize_path
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
"
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
"
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
open_binary
(
package
resource
)
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
    
package_path
=
os
.
path
.
dirname
(
package
.
__file__
)
    
relative_path
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
    
full_path
=
os
.
path
.
abspath
(
relative_path
)
    
try
:
        
return
io_open
(
full_path
'
rb
'
)
    
except
IOError
:
        
try
:
            
loader
=
package
.
__loader__
            
full_path
=
relative_path
[
len
(
loader
.
archive
)
+
1
:
]
            
data
=
loader
.
get_data
(
full_path
)
        
except
(
IOError
AttributeError
)
:
            
package_name
=
package
.
__name__
            
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
resource
encoding
=
'
utf
-
8
'
errors
=
'
strict
'
)
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
    
package_path
=
os
.
path
.
dirname
(
package
.
__file__
)
    
relative_path
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
    
full_path
=
os
.
path
.
abspath
(
relative_path
)
    
try
:
        
return
io_open
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
IOError
:
        
try
:
            
loader
=
package
.
__loader__
            
full_path
=
relative_path
[
len
(
loader
.
archive
)
+
1
:
]
            
data
=
loader
.
get_data
(
full_path
)
        
except
(
IOError
AttributeError
)
:
            
package_name
=
package
.
__name__
            
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
resource
)
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
resource
encoding
=
'
utf
-
8
'
errors
=
'
strict
'
)
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
resource
)
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
    
package_directory
=
Path
(
package
.
__file__
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
name
)
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
OSError
as
error
:
        
if
error
.
errno
not
in
(
errno
.
ENOENT
errno
.
ENOTDIR
)
:
            
raise
        
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
__file__
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
__loader__
.
archive
    
package_directory
=
Path
(
package
.
__file__
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
)
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
    
package_directory
=
Path
(
package
.
__file__
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
OSError
as
error
:
        
if
error
.
errno
not
in
(
errno
.
ENOENT
errno
.
ENOTDIR
)
:
            
raise
        
archive_path
=
getattr
(
package
.
__loader__
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
