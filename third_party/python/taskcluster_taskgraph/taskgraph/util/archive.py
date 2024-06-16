import
gzip
import
os
import
stat
import
tarfile
DEFAULT_MTIME
=
1451606400
class
HackedType
(
bytes
)
:
    
def
__eq__
(
self
other
)
:
        
if
other
=
=
tarfile
.
CHRTYPE
:
            
return
True
        
return
self
=
=
other
class
TarInfo
(
tarfile
.
TarInfo
)
:
    
staticmethod
    
def
_create_header
(
info
format
encoding
errors
)
:
        
info
[
"
type
"
]
=
HackedType
(
info
[
"
type
"
]
)
        
return
tarfile
.
TarInfo
.
_create_header
(
info
format
encoding
errors
)
def
create_tar_from_files
(
fp
files
)
:
    
"
"
"
Create
a
tar
file
deterministically
.
    
Receives
a
dict
mapping
names
of
files
in
the
archive
to
local
filesystem
    
paths
or
mozpack
.
files
.
BaseFile
instances
.
    
The
files
will
be
archived
and
written
to
the
passed
file
handle
opened
    
for
writing
.
    
Only
regular
files
can
be
written
.
    
FUTURE
accept
a
filename
argument
(
or
create
APIs
to
write
files
)
    
"
"
"
    
with
tarfile
.
open
(
        
name
=
"
"
mode
=
"
w
"
fileobj
=
fp
dereference
=
True
format
=
tarfile
.
GNU_FORMAT
    
)
as
tf
:
        
for
archive_path
f
in
sorted
(
files
.
items
(
)
)
:
            
if
isinstance
(
f
str
)
:
                
s
=
os
.
stat
(
f
)
                
mode
=
s
.
st_mode
                
size
=
s
.
st_size
                
f
=
open
(
f
"
rb
"
)
            
else
:
                
mode
=
0o0644
                
size
=
len
(
f
.
read
(
)
)
                
f
.
seek
(
0
)
            
ti
=
TarInfo
(
archive_path
)
            
ti
.
mode
=
mode
            
ti
.
type
=
tarfile
.
REGTYPE
            
if
not
ti
.
isreg
(
)
:
                
raise
ValueError
(
f
"
not
a
regular
file
:
{
f
}
"
)
            
if
ti
.
mode
&
(
stat
.
S_ISUID
|
stat
.
S_ISGID
)
:
                
raise
ValueError
(
f
"
cannot
add
file
with
setuid
or
setgid
set
:
{
f
}
"
)
            
ti
.
uid
=
0
            
ti
.
gid
=
0
            
ti
.
uname
=
"
"
            
ti
.
gname
=
"
"
            
ti
.
mtime
=
DEFAULT_MTIME
            
ti
.
size
=
size
            
tf
.
addfile
(
ti
f
)
def
create_tar_gz_from_files
(
fp
files
filename
=
None
compresslevel
=
9
)
:
    
"
"
"
Create
a
tar
.
gz
file
deterministically
from
files
.
    
This
is
a
glorified
wrapper
around
create_tar_from_files
that
    
adds
gzip
compression
.
    
The
passed
file
handle
should
be
opened
for
writing
in
binary
mode
.
    
When
the
function
returns
all
data
has
been
written
to
the
handle
.
    
"
"
"
    
gf
=
gzip
.
GzipFile
(
        
filename
=
filename
or
"
"
        
mode
=
"
wb
"
        
fileobj
=
fp
        
compresslevel
=
compresslevel
        
mtime
=
DEFAULT_MTIME
    
)
    
with
gf
:
        
create_tar_from_files
(
gf
files
)
