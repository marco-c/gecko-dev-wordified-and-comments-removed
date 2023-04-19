from
__future__
import
print_function
import
buildconfig
import
errno
import
sys
import
platform
import
os
import
re
import
shutil
import
textwrap
import
subprocess
import
time
import
ctypes
from
optparse
import
OptionParser
from
mozbuild
.
util
import
memoize
from
mozbuild
.
generated_sources
import
(
    
get_filename_with_digest
    
get_generated_sources
    
get_s3_region_and_bucket
)
from
mozpack
.
copier
import
FileRegistry
from
mozpack
.
manifests
import
(
    
InstallManifest
    
UnreadableInstallManifest
)
class
VCSFileInfo
:
    
"
"
"
A
base
class
for
version
-
controlled
file
information
.
Ensures
that
the
    
following
attributes
are
generated
only
once
(
successfully
)
:
        
self
.
root
        
self
.
clean_root
        
self
.
revision
        
self
.
filename
    
The
attributes
are
generated
by
a
single
call
to
the
GetRoot
    
GetRevision
and
GetFilename
methods
.
Those
methods
are
explicitly
not
    
implemented
here
and
must
be
implemented
in
derived
classes
.
"
"
"
    
def
__init__
(
self
file
)
:
        
if
not
file
:
            
raise
ValueError
        
self
.
file
=
file
    
def
__getattr__
(
self
name
)
:
        
"
"
"
__getattr__
is
only
called
for
attributes
that
are
not
set
on
self
        
so
setting
self
.
[
attr
]
will
prevent
future
calls
to
the
GetRoot
        
GetRevision
and
GetFilename
methods
.
We
don
'
t
set
the
values
on
        
failure
on
the
off
chance
that
a
future
call
might
succeed
.
"
"
"
        
if
name
=
=
"
root
"
:
            
root
=
self
.
GetRoot
(
)
            
if
root
:
                
self
.
root
=
root
            
return
root
        
elif
name
=
=
"
clean_root
"
:
            
clean_root
=
self
.
GetCleanRoot
(
)
            
if
clean_root
:
                
self
.
clean_root
=
clean_root
            
return
clean_root
        
elif
name
=
=
"
revision
"
:
            
revision
=
self
.
GetRevision
(
)
            
if
revision
:
                
self
.
revision
=
revision
            
return
revision
        
elif
name
=
=
"
filename
"
:
            
filename
=
self
.
GetFilename
(
)
            
if
filename
:
                
self
.
filename
=
filename
            
return
filename
        
raise
AttributeError
    
def
GetRoot
(
self
)
:
        
"
"
"
This
method
should
return
the
unmodified
root
for
the
file
or
'
None
'
        
on
failure
.
"
"
"
        
raise
NotImplementedError
    
def
GetCleanRoot
(
self
)
:
        
"
"
"
This
method
should
return
the
repository
root
for
the
file
or
'
None
'
        
on
failure
.
"
"
"
        
raise
NotImplementedError
    
def
GetRevision
(
self
)
:
        
"
"
"
This
method
should
return
the
revision
number
for
the
file
or
'
None
'
        
on
failure
.
"
"
"
        
raise
NotImplementedError
    
def
GetFilename
(
self
)
:
        
"
"
"
This
method
should
return
the
repository
-
specific
filename
for
the
        
file
or
'
None
'
on
failure
.
"
"
"
        
raise
NotImplementedError
rootRegex
=
re
.
compile
(
r
"
^
\
S
+
?
:
/
+
(
?
:
[
^
\
s
/
]
*
)
?
(
\
S
+
)
"
)
def
read_output
(
*
args
)
:
    
(
stdout
_
)
=
subprocess
.
Popen
(
        
args
=
args
universal_newlines
=
True
stdout
=
subprocess
.
PIPE
    
)
.
communicate
(
)
    
return
stdout
.
rstrip
(
)
class
HGRepoInfo
:
    
def
__init__
(
self
path
)
:
        
self
.
path
=
path
        
rev
=
os
.
environ
.
get
(
"
MOZ_SOURCE_CHANGESET
"
)
        
if
not
rev
:
            
rev
=
read_output
(
"
hg
"
"
-
R
"
path
"
parent
"
"
-
-
template
=
{
node
}
"
)
        
hg_root
=
os
.
environ
.
get
(
"
MOZ_SOURCE_REPO
"
)
        
if
hg_root
:
            
root
=
hg_root
        
else
:
            
root
=
read_output
(
"
hg
"
"
-
R
"
path
"
showconfig
"
"
paths
.
default
"
)
            
if
not
root
:
                
print
(
"
Failed
to
get
HG
Repo
for
%
s
"
%
path
file
=
sys
.
stderr
)
        
cleanroot
=
None
        
if
root
:
            
match
=
rootRegex
.
match
(
root
)
            
if
match
:
                
cleanroot
=
match
.
group
(
1
)
                
if
cleanroot
.
endswith
(
"
/
"
)
:
                    
cleanroot
=
cleanroot
[
:
-
1
]
        
if
cleanroot
is
None
:
            
print
(
                
textwrap
.
dedent
(
                    
"
"
"
\
            
Could
not
determine
repo
info
for
%
s
.
This
is
either
not
a
clone
of
the
web
-
based
            
repository
or
you
have
not
specified
MOZ_SOURCE_REPO
or
the
clone
is
corrupt
.
"
"
"
                
)
                
%
path
                
sys
.
stderr
            
)
            
sys
.
exit
(
1
)
        
self
.
rev
=
rev
        
self
.
root
=
root
        
self
.
cleanroot
=
cleanroot
    
def
GetFileInfo
(
self
file
)
:
        
return
HGFileInfo
(
file
self
)
class
HGFileInfo
(
VCSFileInfo
)
:
    
def
__init__
(
self
file
repo
)
:
        
VCSFileInfo
.
__init__
(
self
file
)
        
self
.
repo
=
repo
        
self
.
file
=
os
.
path
.
relpath
(
file
repo
.
path
)
    
def
GetRoot
(
self
)
:
        
return
self
.
repo
.
root
    
def
GetCleanRoot
(
self
)
:
        
return
self
.
repo
.
cleanroot
    
def
GetRevision
(
self
)
:
        
return
self
.
repo
.
rev
    
def
GetFilename
(
self
)
:
        
if
self
.
revision
and
self
.
clean_root
:
            
return
"
hg
:
%
s
:
%
s
:
%
s
"
%
(
self
.
clean_root
self
.
file
self
.
revision
)
        
return
self
.
file
class
GitRepoInfo
:
    
"
"
"
    
Info
about
a
local
git
repository
.
Does
not
currently
    
support
discovering
info
about
a
git
clone
the
info
must
be
    
provided
out
-
of
-
band
.
    
"
"
"
    
def
__init__
(
self
path
rev
root
)
:
        
self
.
path
=
path
        
cleanroot
=
None
        
if
root
:
            
match
=
rootRegex
.
match
(
root
)
            
if
match
:
                
cleanroot
=
match
.
group
(
1
)
                
if
cleanroot
.
endswith
(
"
/
"
)
:
                    
cleanroot
=
cleanroot
[
:
-
1
]
        
if
cleanroot
is
None
:
            
print
(
                
textwrap
.
dedent
(
                    
"
"
"
\
            
Could
not
determine
repo
info
for
%
s
(
%
s
)
.
This
is
either
not
a
clone
of
a
web
-
based
            
repository
or
you
have
not
specified
MOZ_SOURCE_REPO
or
the
clone
is
corrupt
.
"
"
"
                
)
                
%
(
path
root
)
                
file
=
sys
.
stderr
            
)
            
sys
.
exit
(
1
)
        
self
.
rev
=
rev
        
self
.
cleanroot
=
cleanroot
    
def
GetFileInfo
(
self
file
)
:
        
return
GitFileInfo
(
file
self
)
class
GitFileInfo
(
VCSFileInfo
)
:
    
def
__init__
(
self
file
repo
)
:
        
VCSFileInfo
.
__init__
(
self
file
)
        
self
.
repo
=
repo
        
self
.
file
=
os
.
path
.
relpath
(
file
repo
.
path
)
    
def
GetRoot
(
self
)
:
        
return
self
.
repo
.
path
    
def
GetCleanRoot
(
self
)
:
        
return
self
.
repo
.
cleanroot
    
def
GetRevision
(
self
)
:
        
return
self
.
repo
.
rev
    
def
GetFilename
(
self
)
:
        
if
self
.
revision
and
self
.
clean_root
:
            
return
"
git
:
%
s
:
%
s
:
%
s
"
%
(
self
.
clean_root
self
.
file
self
.
revision
)
        
return
self
.
file
vcsFileInfoCache
=
{
}
if
platform
.
system
(
)
=
=
"
Windows
"
:
    
def
realpath
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
using
GetFinalPathNameByHandleW
to
get
the
        
path
with
all
components
in
the
case
they
exist
in
on
-
disk
so
        
that
making
links
to
a
case
-
sensitive
server
(
hg
.
mozilla
.
org
)
works
.
        
This
function
also
resolves
any
symlinks
in
the
path
.
        
"
"
"
        
result
=
path
        
ctypes
.
windll
.
kernel32
.
SetErrorMode
(
ctypes
.
c_uint
(
1
)
)
        
handle
=
ctypes
.
windll
.
kernel32
.
CreateFileW
(
            
path
            
0x80000000
            
1
            
None
            
3
            
0x02000000
            
None
        
)
        
if
handle
!
=
-
1
:
            
size
=
ctypes
.
windll
.
kernel32
.
GetFinalPathNameByHandleW
(
handle
None
0
0
)
            
buf
=
ctypes
.
create_unicode_buffer
(
size
)
            
if
(
                
ctypes
.
windll
.
kernel32
.
GetFinalPathNameByHandleW
(
handle
buf
size
0
)
                
>
0
            
)
:
                
result
=
buf
.
value
[
4
:
]
            
ctypes
.
windll
.
kernel32
.
CloseHandle
(
handle
)
        
return
result
else
:
    
realpath
=
os
.
path
.
realpath
def
IsInDir
(
file
dir
)
:
    
return
os
.
path
.
abspath
(
file
)
.
lower
(
)
.
startswith
(
os
.
path
.
abspath
(
dir
)
.
lower
(
)
)
def
GetVCSFilenameFromSrcdir
(
file
srcdir
)
:
    
if
srcdir
not
in
Dumper
.
srcdirRepoInfo
:
        
if
os
.
path
.
isdir
(
os
.
path
.
join
(
srcdir
"
.
hg
"
)
)
:
            
Dumper
.
srcdirRepoInfo
[
srcdir
]
=
HGRepoInfo
(
srcdir
)
        
else
:
            
return
None
    
return
Dumper
.
srcdirRepoInfo
[
srcdir
]
.
GetFileInfo
(
file
)
def
GetVCSFilename
(
file
srcdirs
)
:
    
"
"
"
Given
a
full
path
to
a
file
and
the
top
source
directory
    
look
for
version
control
information
about
this
file
and
return
    
a
tuple
containing
    
1
)
a
specially
formatted
filename
that
contains
the
VCS
type
    
VCS
location
relative
filename
and
revision
number
formatted
like
:
    
vcs
:
vcs
location
:
filename
:
revision
    
For
example
:
    
cvs
:
cvs
.
mozilla
.
org
/
cvsroot
:
mozilla
/
browser
/
app
/
nsBrowserApp
.
cpp
:
1
.
36
    
2
)
the
unmodified
root
information
if
it
exists
"
"
"
    
(
path
filename
)
=
os
.
path
.
split
(
file
)
    
if
path
=
=
"
"
or
filename
=
=
"
"
:
        
return
(
file
None
)
    
fileInfo
=
None
    
root
=
"
"
    
if
file
in
vcsFileInfoCache
:
        
fileInfo
=
vcsFileInfoCache
[
file
]
    
else
:
        
for
srcdir
in
srcdirs
:
            
if
not
IsInDir
(
file
srcdir
)
:
                
continue
            
fileInfo
=
GetVCSFilenameFromSrcdir
(
file
srcdir
)
            
if
fileInfo
:
                
vcsFileInfoCache
[
file
]
=
fileInfo
                
break
    
if
fileInfo
:
        
file
=
fileInfo
.
filename
        
root
=
fileInfo
.
root
    
return
(
file
.
replace
(
"
\
\
"
"
/
"
)
root
)
def
validate_install_manifests
(
install_manifest_args
)
:
    
args
=
[
]
    
for
arg
in
install_manifest_args
:
        
bits
=
arg
.
split
(
"
"
)
        
if
len
(
bits
)
!
=
2
:
            
raise
ValueError
(
                
"
Invalid
format
for
-
-
install
-
manifest
:
"
"
specify
manifest
target_dir
"
            
)
        
manifest_file
destination
=
[
os
.
path
.
abspath
(
b
)
for
b
in
bits
]
        
if
not
os
.
path
.
isfile
(
manifest_file
)
:
            
raise
IOError
(
errno
.
ENOENT
"
Manifest
file
not
found
"
manifest_file
)
        
if
not
os
.
path
.
isdir
(
destination
)
:
            
raise
IOError
(
errno
.
ENOENT
"
Install
directory
not
found
"
destination
)
        
try
:
            
manifest
=
InstallManifest
(
manifest_file
)
        
except
UnreadableInstallManifest
:
            
raise
IOError
(
errno
.
EINVAL
"
Error
parsing
manifest
file
"
manifest_file
)
        
args
.
append
(
(
manifest
destination
)
)
    
return
args
def
make_file_mapping
(
install_manifests
)
:
    
file_mapping
=
{
}
    
for
manifest
destination
in
install_manifests
:
        
destination
=
os
.
path
.
abspath
(
destination
)
        
reg
=
FileRegistry
(
)
        
manifest
.
populate_registry
(
reg
)
        
for
dst
src
in
reg
:
            
if
hasattr
(
src
"
path
"
)
:
                
abs_dest
=
realpath
(
os
.
path
.
join
(
destination
dst
)
)
                
file_mapping
[
abs_dest
]
=
realpath
(
src
.
path
)
    
return
file_mapping
memoize
def
get_generated_file_s3_path
(
filename
rel_path
bucket
)
:
    
"
"
"
Given
a
filename
return
a
path
formatted
similarly
to
    
GetVCSFilename
but
representing
a
file
available
in
an
s3
bucket
.
"
"
"
    
with
open
(
filename
"
rb
"
)
as
f
:
        
path
=
get_filename_with_digest
(
rel_path
f
.
read
(
)
)
        
return
"
s3
:
{
bucket
}
:
{
path
}
:
"
.
format
(
bucket
=
bucket
path
=
path
)
def
GetPlatformSpecificDumper
(
*
*
kwargs
)
:
    
"
"
"
This
function
simply
returns
a
instance
of
a
subclass
of
Dumper
    
that
is
appropriate
for
the
current
platform
.
"
"
"
    
return
{
"
WINNT
"
:
Dumper_Win32
"
Linux
"
:
Dumper_Linux
"
Darwin
"
:
Dumper_Mac
}
[
        
buildconfig
.
substs
[
"
OS_ARCH
"
]
    
]
(
*
*
kwargs
)
def
SourceIndex
(
fileStream
outputPath
vcs_root
s3_bucket
)
:
    
"
"
"
Takes
a
list
of
files
writes
info
to
a
data
block
in
a
.
stream
file
"
"
"
    
result
=
True
    
pdbStreamFile
=
open
(
outputPath
"
w
"
)
    
pdbStreamFile
.
write
(
        
"
SRCSRV
:
ini
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
\
r
\
n
"
        
+
"
VERSION
=
2
\
r
\
n
"
        
+
"
INDEXVERSION
=
2
\
r
\
n
"
        
+
"
VERCTRL
=
http
\
r
\
n
"
        
+
"
SRCSRV
:
variables
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
\
r
\
n
"
        
+
"
SRCSRVVERCTRL
=
http
\
r
\
n
"
        
+
"
RUST_GITHUB_TARGET
=
https
:
/
/
github
.
com
/
rust
-
lang
/
rust
/
raw
/
%
var4
%
/
%
var3
%
\
r
\
n
"
    
)
    
pdbStreamFile
.
write
(
"
HGSERVER
=
"
+
vcs_root
+
"
\
r
\
n
"
)
    
pdbStreamFile
.
write
(
"
HG_TARGET
=
%
hgserver
%
/
raw
-
file
/
%
var4
%
/
%
var3
%
\
r
\
n
"
)
    
if
s3_bucket
:
        
pdbStreamFile
.
write
(
"
S3_BUCKET
=
"
+
s3_bucket
+
"
\
r
\
n
"
)
        
pdbStreamFile
.
write
(
"
S3_TARGET
=
https
:
/
/
%
s3_bucket
%
.
s3
.
amazonaws
.
com
/
%
var3
%
\
r
\
n
"
)
    
pdbStreamFile
.
write
(
"
SRCSRVTRG
=
%
fnvar
%
(
%
var2
%
)
\
r
\
n
"
)
    
pdbStreamFile
.
write
(
        
"
SRCSRV
:
source
files
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
\
r
\
n
"
    
)
    
pdbStreamFile
.
write
(
fileStream
)
    
pdbStreamFile
.
write
(
        
"
SRCSRV
:
end
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
\
r
\
n
\
n
"
    
)
    
pdbStreamFile
.
close
(
)
    
return
result
class
Dumper
:
    
"
"
"
This
class
can
dump
symbols
from
a
file
with
debug
info
and
    
store
the
output
in
a
directory
structure
that
is
valid
for
use
as
    
a
Breakpad
symbol
server
.
Requires
a
path
to
a
dump_syms
binary
-
-
    
|
dump_syms
|
and
a
directory
to
store
symbols
in
-
-
|
symbol_path
|
.
    
Optionally
takes
a
list
of
processor
architectures
to
process
from
    
each
debug
file
-
-
|
archs
|
the
full
path
to
the
top
source
    
directory
-
-
|
srcdir
|
for
generating
relative
source
file
names
    
and
an
option
to
copy
debug
info
files
alongside
the
dumped
    
symbol
files
-
-
|
copy_debug
|
mostly
useful
for
creating
a
    
Microsoft
Symbol
Server
from
the
resulting
output
.
    
You
don
'
t
want
to
use
this
directly
if
you
intend
to
process
files
.
    
Instead
call
GetPlatformSpecificDumper
to
get
an
instance
of
a
    
subclass
.
"
"
"
    
srcdirRepoInfo
=
{
}
    
def
__init__
(
        
self
        
dump_syms
        
symbol_path
        
archs
=
None
        
srcdirs
=
[
]
        
copy_debug
=
False
        
vcsinfo
=
False
        
srcsrv
=
False
        
generated_files
=
None
        
s3_bucket
=
None
        
file_mapping
=
None
    
)
:
        
self
.
dump_syms
=
os
.
path
.
abspath
(
dump_syms
)
        
self
.
symbol_path
=
symbol_path
        
if
archs
is
None
:
            
self
.
archs
=
[
"
"
]
        
else
:
            
self
.
archs
=
[
"
-
a
%
s
"
%
a
for
a
in
archs
.
split
(
)
]
        
self
.
srcdirs
=
[
realpath
(
s
)
for
s
in
srcdirs
]
        
self
.
copy_debug
=
copy_debug
        
self
.
vcsinfo
=
vcsinfo
        
self
.
srcsrv
=
srcsrv
        
self
.
generated_files
=
generated_files
or
{
}
        
self
.
s3_bucket
=
s3_bucket
        
self
.
file_mapping
=
file_mapping
or
{
}
        
rust_sha
=
buildconfig
.
substs
[
"
RUSTC_COMMIT
"
]
        
rust_srcdir
=
"
/
rustc
/
"
+
rust_sha
        
self
.
srcdirs
.
append
(
rust_srcdir
)
        
Dumper
.
srcdirRepoInfo
[
rust_srcdir
]
=
GitRepoInfo
(
            
rust_srcdir
rust_sha
"
https
:
/
/
github
.
com
/
rust
-
lang
/
rust
/
"
        
)
    
def
ShouldProcess
(
self
file
)
:
        
return
True
    
def
RunFileCommand
(
self
file
)
:
        
"
"
"
Utility
function
returns
the
output
of
file
(
1
)
"
"
"
        
return
read_output
(
"
file
"
"
-
Lb
"
file
)
    
def
SourceServerIndexing
(
        
self
debug_file
guid
sourceFileStream
vcs_root
s3_bucket
    
)
:
        
return
"
"
    
def
CopyExeAndDebugInfo
(
self
file
debug_file
guid
code_file
code_id
)
:
        
"
"
"
This
function
will
copy
a
library
or
executable
and
the
file
holding
the
        
debug
information
to
|
symbol_path
|
"
"
"
        
pass
    
def
Process
(
self
file_to_process
count_ctors
=
False
)
:
        
"
"
"
Process
the
given
file
.
"
"
"
        
if
self
.
ShouldProcess
(
os
.
path
.
abspath
(
file_to_process
)
)
:
            
self
.
ProcessFile
(
file_to_process
count_ctors
=
count_ctors
)
    
def
ProcessFile
(
self
file
dsymbundle
=
None
count_ctors
=
False
)
:
        
"
"
"
Dump
symbols
from
these
files
into
a
symbol
file
stored
        
in
the
proper
directory
structure
in
|
symbol_path
|
;
processing
is
performed
        
asynchronously
and
Finish
must
be
called
to
wait
for
it
complete
and
cleanup
.
        
All
files
after
the
first
are
fallbacks
in
case
the
first
file
does
not
process
        
successfully
;
if
it
does
no
other
files
will
be
touched
.
"
"
"
        
print
(
"
Beginning
work
for
file
:
%
s
"
%
file
file
=
sys
.
stderr
)
        
vcs_root
=
os
.
environ
.
get
(
"
MOZ_SOURCE_REPO
"
)
        
for
arch_num
arch
in
enumerate
(
self
.
archs
)
:
            
self
.
ProcessFileWork
(
                
file
arch_num
arch
vcs_root
dsymbundle
count_ctors
=
count_ctors
            
)
    
def
dump_syms_cmdline
(
self
file
arch
dsymbundle
=
None
)
:
        
"
"
"
        
Get
the
commandline
used
to
invoke
dump_syms
.
        
"
"
"
        
return
[
self
.
dump_syms
file
]
    
def
ProcessFileWork
(
        
self
file
arch_num
arch
vcs_root
dsymbundle
=
None
count_ctors
=
False
    
)
:
        
ctors
=
0
        
t_start
=
time
.
time
(
)
        
print
(
"
Processing
file
:
%
s
"
%
file
file
=
sys
.
stderr
)
        
sourceFileStream
=
"
"
        
code_id
code_file
=
None
None
        
try
:
            
cmd
=
self
.
dump_syms_cmdline
(
file
arch
dsymbundle
=
dsymbundle
)
            
print
(
"
"
.
join
(
cmd
)
file
=
sys
.
stderr
)
            
proc
=
subprocess
.
Popen
(
                
cmd
                
universal_newlines
=
True
                
stdout
=
subprocess
.
PIPE
            
)
            
try
:
                
module_line
=
next
(
proc
.
stdout
)
            
except
StopIteration
:
                
module_line
=
"
"
            
if
module_line
.
startswith
(
"
MODULE
"
)
:
                
(
guid
debug_file
)
=
(
module_line
.
split
(
)
)
[
3
:
5
]
                
sym_file
=
re
.
sub
(
"
\
.
pdb
"
"
"
debug_file
)
+
"
.
sym
"
                
rel_path
=
os
.
path
.
join
(
debug_file
guid
sym_file
)
.
replace
(
"
\
\
"
"
/
"
)
                
full_path
=
os
.
path
.
normpath
(
os
.
path
.
join
(
self
.
symbol_path
rel_path
)
)
                
try
:
                    
os
.
makedirs
(
os
.
path
.
dirname
(
full_path
)
)
                
except
OSError
:
                    
pass
                
f
=
open
(
full_path
"
w
"
)
                
f
.
write
(
module_line
)
                
for
line
in
proc
.
stdout
:
                    
if
line
.
startswith
(
"
FILE
"
)
:
                        
(
x
index
filename
)
=
line
.
rstrip
(
)
.
split
(
None
2
)
                        
sourcepath
=
filename
                        
filename
=
realpath
(
filename
)
                        
if
filename
in
self
.
file_mapping
:
                            
filename
=
self
.
file_mapping
[
filename
]
                        
if
self
.
vcsinfo
:
                            
gen_path
=
self
.
generated_files
.
get
(
filename
)
                            
if
gen_path
and
self
.
s3_bucket
:
                                
filename
=
get_generated_file_s3_path
(
                                    
filename
gen_path
self
.
s3_bucket
                                
)
                                
rootname
=
"
"
                            
else
:
                                
(
filename
rootname
)
=
GetVCSFilename
(
                                    
filename
self
.
srcdirs
                                
)
                            
if
vcs_root
is
None
:
                                
if
rootname
:
                                    
vcs_root
=
rootname
                        
if
filename
.
startswith
(
"
hg
:
"
)
:
                            
(
vcs
repo
source_file
revision
)
=
filename
.
split
(
"
:
"
3
)
                            
sourceFileStream
+
=
sourcepath
+
"
*
HG_TARGET
*
"
+
source_file
                            
sourceFileStream
+
=
"
*
"
+
revision
+
"
\
r
\
n
"
                        
elif
filename
.
startswith
(
"
s3
:
"
)
:
                            
(
vcs
bucket
source_file
nothing
)
=
filename
.
split
(
"
:
"
3
)
                            
sourceFileStream
+
=
sourcepath
+
"
*
S3_TARGET
*
"
                            
sourceFileStream
+
=
source_file
+
"
\
r
\
n
"
                        
elif
filename
.
startswith
(
"
git
:
github
.
com
/
rust
-
lang
/
rust
:
"
)
:
                            
(
vcs
repo
source_file
revision
)
=
filename
.
split
(
"
:
"
3
)
                            
sourceFileStream
+
=
sourcepath
+
"
*
RUST_GITHUB_TARGET
*
"
                            
sourceFileStream
+
=
source_file
+
"
*
"
+
revision
+
"
\
r
\
n
"
                        
f
.
write
(
"
FILE
%
s
%
s
\
n
"
%
(
index
filename
)
)
                    
elif
line
.
startswith
(
"
INFO
CODE_ID
"
)
:
                        
bits
=
line
.
rstrip
(
)
.
split
(
None
3
)
                        
if
len
(
bits
)
=
=
4
:
                            
code_id
code_file
=
bits
[
2
:
]
                        
f
.
write
(
line
)
                    
else
:
                        
if
count_ctors
and
line
.
startswith
(
"
FUNC
"
)
:
                            
if
"
_GLOBAL__sub_
"
in
line
:
                                
ctors
+
=
1
                            
elif
"
dynamic
initializer
for
'
"
in
line
:
                                
ctors
+
=
1
                        
f
.
write
(
line
)
                
f
.
close
(
)
                
retcode
=
proc
.
wait
(
)
                
if
retcode
!
=
0
:
                    
raise
RuntimeError
(
                        
"
dump_syms
failed
with
error
code
%
d
while
processing
%
s
\
n
"
                        
%
(
retcode
file
)
                    
)
                
print
(
rel_path
)
                
if
self
.
srcsrv
and
vcs_root
:
                    
self
.
SourceServerIndexing
(
                        
debug_file
guid
sourceFileStream
vcs_root
self
.
s3_bucket
                    
)
                
if
self
.
copy_debug
and
arch_num
=
=
0
:
                    
self
.
CopyExeAndDebugInfo
(
file
debug_file
guid
code_file
code_id
)
            
else
:
                
retcode
=
proc
.
wait
(
)
                
message
=
[
                    
"
dump_syms
failed
to
produce
the
expected
output
"
                    
"
file
:
%
s
"
%
file
                    
"
return
code
:
%
d
"
%
retcode
                    
"
first
line
of
output
:
%
s
"
%
module_line
                
]
                
raise
RuntimeError
(
"
\
n
-
-
-
-
-
-
-
-
-
-
\
n
"
.
join
(
message
)
)
        
except
Exception
as
e
:
            
print
(
"
Unexpected
error
:
%
s
"
%
str
(
e
)
file
=
sys
.
stderr
)
            
raise
        
if
dsymbundle
:
            
shutil
.
rmtree
(
dsymbundle
)
        
if
count_ctors
:
            
import
json
            
perfherder_data
=
{
                
"
framework
"
:
{
"
name
"
:
"
build_metrics
"
}
                
"
suites
"
:
[
                    
{
                        
"
name
"
:
"
compiler_metrics
"
                        
"
subtests
"
:
[
                            
{
                                
"
name
"
:
"
num_static_constructors
"
                                
"
value
"
:
ctors
                                
"
alertChangeType
"
:
"
absolute
"
                                
"
alertThreshold
"
:
3
                            
}
                        
]
                    
}
                
]
            
}
            
perfherder_extra_options
=
os
.
environ
.
get
(
"
PERFHERDER_EXTRA_OPTIONS
"
"
"
)
            
for
opt
in
perfherder_extra_options
.
split
(
)
:
                
for
suite
in
perfherder_data
[
"
suites
"
]
:
                    
if
opt
not
in
suite
.
get
(
"
extraOptions
"
[
]
)
:
                        
suite
.
setdefault
(
"
extraOptions
"
[
]
)
.
append
(
opt
)
            
if
"
asan
"
not
in
perfherder_extra_options
.
lower
(
)
:
                
print
(
                    
"
PERFHERDER_DATA
:
%
s
"
%
json
.
dumps
(
perfherder_data
)
file
=
sys
.
stderr
                
)
        
elapsed
=
time
.
time
(
)
-
t_start
        
print
(
"
Finished
processing
%
s
in
%
.
2fs
"
%
(
file
elapsed
)
file
=
sys
.
stderr
)
def
locate_pdb
(
path
)
:
    
"
"
"
Given
a
path
to
a
binary
attempt
to
locate
the
matching
pdb
file
with
simple
heuristics
:
    
*
Look
for
a
pdb
file
with
the
same
base
name
next
to
the
binary
    
*
Look
for
a
pdb
file
with
the
same
base
name
in
the
cwd
    
Returns
the
path
to
the
pdb
file
if
it
exists
or
None
if
it
could
not
be
located
.
    
"
"
"
    
path
ext
=
os
.
path
.
splitext
(
path
)
    
pdb
=
path
+
"
.
pdb
"
    
if
os
.
path
.
isfile
(
pdb
)
:
        
return
pdb
    
base
=
os
.
path
.
basename
(
pdb
)
    
pdb
=
os
.
path
.
join
(
os
.
getcwd
(
)
base
)
    
if
os
.
path
.
isfile
(
pdb
)
:
        
return
pdb
    
return
None
class
Dumper_Win32
(
Dumper
)
:
    
fixedFilenameCaseCache
=
{
}
    
def
ShouldProcess
(
self
file
)
:
        
"
"
"
This
function
will
allow
processing
of
exe
or
dll
files
that
have
pdb
        
files
with
the
same
base
name
next
to
them
.
"
"
"
        
if
file
.
endswith
(
"
.
exe
"
)
or
file
.
endswith
(
"
.
dll
"
)
:
            
if
locate_pdb
(
file
)
is
not
None
:
                
return
True
        
return
False
    
def
CopyExeAndDebugInfo
(
self
file
debug_file
guid
code_file
code_id
)
:
        
"
"
"
This
function
will
copy
the
executable
or
dll
and
pdb
files
to
|
symbol_path
|
"
"
"
        
pdb_file
=
locate_pdb
(
file
)
        
rel_path
=
os
.
path
.
join
(
debug_file
guid
debug_file
)
.
replace
(
"
\
\
"
"
/
"
)
        
full_path
=
os
.
path
.
normpath
(
os
.
path
.
join
(
self
.
symbol_path
rel_path
)
)
        
shutil
.
copyfile
(
pdb_file
full_path
)
        
print
(
rel_path
)
        
if
code_file
and
code_id
:
            
full_code_path
=
os
.
path
.
join
(
os
.
path
.
dirname
(
file
)
code_file
)
            
if
os
.
path
.
exists
(
full_code_path
)
:
                
rel_path
=
os
.
path
.
join
(
code_file
code_id
code_file
)
.
replace
(
                    
"
\
\
"
"
/
"
                
)
                
full_path
=
os
.
path
.
normpath
(
os
.
path
.
join
(
self
.
symbol_path
rel_path
)
)
                
try
:
                    
os
.
makedirs
(
os
.
path
.
dirname
(
full_path
)
)
                
except
OSError
as
e
:
                    
if
e
.
errno
!
=
errno
.
EEXIST
:
                        
raise
                
shutil
.
copyfile
(
full_code_path
full_path
)
                
print
(
rel_path
)
    
def
SourceServerIndexing
(
        
self
debug_file
guid
sourceFileStream
vcs_root
s3_bucket
    
)
:
        
streamFilename
=
debug_file
+
"
.
stream
"
        
stream_output_path
=
os
.
path
.
abspath
(
streamFilename
)
        
result
=
SourceIndex
(
sourceFileStream
stream_output_path
vcs_root
s3_bucket
)
        
if
self
.
copy_debug
:
            
pdbstr
=
buildconfig
.
substs
[
"
PDBSTR
"
]
            
wine
=
buildconfig
.
substs
.
get
(
"
WINE
"
)
            
if
wine
:
                
cmd
=
[
wine
pdbstr
]
            
else
:
                
cmd
=
[
pdbstr
]
            
subprocess
.
call
(
                
cmd
                
+
[
                    
"
-
w
"
                    
"
-
p
:
"
+
os
.
path
.
basename
(
debug_file
)
                    
"
-
i
:
"
+
os
.
path
.
basename
(
streamFilename
)
                    
"
-
s
:
srcsrv
"
                
]
                
cwd
=
os
.
path
.
dirname
(
stream_output_path
)
            
)
            
os
.
remove
(
stream_output_path
)
        
return
result
class
Dumper_Linux
(
Dumper
)
:
    
objcopy
=
os
.
environ
[
"
OBJCOPY
"
]
if
"
OBJCOPY
"
in
os
.
environ
else
"
objcopy
"
    
def
ShouldProcess
(
self
file
)
:
        
"
"
"
This
function
will
allow
processing
of
files
that
are
        
executable
or
end
with
the
.
so
extension
and
additionally
        
file
(
1
)
reports
as
being
ELF
files
.
It
expects
to
find
the
file
        
command
in
PATH
.
"
"
"
        
if
file
.
endswith
(
"
.
so
"
)
or
os
.
access
(
file
os
.
X_OK
)
:
            
return
self
.
RunFileCommand
(
file
)
.
startswith
(
"
ELF
"
)
        
return
False
    
def
CopyExeAndDebugInfo
(
self
file
debug_file
guid
code_file
code_id
)
:
        
file_dbg
=
file
+
"
.
dbg
"
        
if
(
            
subprocess
.
call
(
[
self
.
objcopy
"
-
-
only
-
keep
-
debug
"
file
file_dbg
]
)
=
=
0
            
and
subprocess
.
call
(
                
[
                    
self
.
objcopy
                    
"
-
-
remove
-
section
"
                    
"
.
gnu_debuglink
"
                    
"
-
-
add
-
gnu
-
debuglink
=
%
s
"
%
file_dbg
                    
file
                
]
            
)
            
=
=
0
        
)
:
            
rel_path
=
os
.
path
.
join
(
debug_file
guid
debug_file
+
"
.
dbg
"
)
            
full_path
=
os
.
path
.
normpath
(
os
.
path
.
join
(
self
.
symbol_path
rel_path
)
)
            
shutil
.
move
(
file_dbg
full_path
)
            
print
(
rel_path
)
        
else
:
            
if
os
.
path
.
isfile
(
file_dbg
)
:
                
os
.
unlink
(
file_dbg
)
class
Dumper_Solaris
(
Dumper
)
:
    
def
RunFileCommand
(
self
file
)
:
        
"
"
"
Utility
function
returns
the
output
of
file
(
1
)
"
"
"
        
try
:
            
output
=
os
.
popen
(
"
file
"
+
file
)
.
read
(
)
            
return
output
.
split
(
"
\
t
"
)
[
1
]
        
except
Exception
:
            
return
"
"
    
def
ShouldProcess
(
self
file
)
:
        
"
"
"
This
function
will
allow
processing
of
files
that
are
        
executable
or
end
with
the
.
so
extension
and
additionally
        
file
(
1
)
reports
as
being
ELF
files
.
It
expects
to
find
the
file
        
command
in
PATH
.
"
"
"
        
if
file
.
endswith
(
"
.
so
"
)
or
os
.
access
(
file
os
.
X_OK
)
:
            
return
self
.
RunFileCommand
(
file
)
.
startswith
(
"
ELF
"
)
        
return
False
class
Dumper_Mac
(
Dumper
)
:
    
def
ShouldProcess
(
self
file
)
:
        
"
"
"
This
function
will
allow
processing
of
files
that
are
        
executable
or
end
with
the
.
dylib
extension
and
additionally
        
file
(
1
)
reports
as
being
Mach
-
O
files
.
It
expects
to
find
the
file
        
command
in
PATH
.
"
"
"
        
if
file
.
endswith
(
"
.
dylib
"
)
or
os
.
access
(
file
os
.
X_OK
)
:
            
return
self
.
RunFileCommand
(
file
)
.
startswith
(
"
Mach
-
O
"
)
        
return
False
    
def
ProcessFile
(
self
file
count_ctors
=
False
)
:
        
print
(
"
Starting
Mac
pre
-
processing
on
file
:
%
s
"
%
file
file
=
sys
.
stderr
)
        
dsymbundle
=
self
.
GenerateDSYM
(
file
)
        
if
dsymbundle
:
            
Dumper
.
ProcessFile
(
                
self
file
dsymbundle
=
dsymbundle
count_ctors
=
count_ctors
            
)
    
def
dump_syms_cmdline
(
self
file
arch
dsymbundle
=
None
)
:
        
"
"
"
        
Get
the
commandline
used
to
invoke
dump_syms
.
        
"
"
"
        
if
dsymbundle
:
            
return
(
                
[
self
.
dump_syms
]
                
+
arch
.
split
(
)
                
+
[
"
-
-
type
"
"
macho
"
"
-
j
"
"
2
"
dsymbundle
file
]
            
)
        
return
Dumper
.
dump_syms_cmdline
(
self
file
arch
)
    
def
GenerateDSYM
(
self
file
)
:
        
"
"
"
dump_syms
on
Mac
needs
to
be
run
on
a
dSYM
bundle
produced
        
by
dsymutil
(
1
)
so
run
dsymutil
here
and
pass
the
bundle
name
        
down
to
the
superclass
method
instead
.
"
"
"
        
t_start
=
time
.
time
(
)
        
print
(
"
Running
Mac
pre
-
processing
on
file
:
%
s
"
%
(
file
)
file
=
sys
.
stderr
)
        
dsymbundle
=
file
+
"
.
dSYM
"
        
if
os
.
path
.
exists
(
dsymbundle
)
:
            
shutil
.
rmtree
(
dsymbundle
)
        
dsymutil
=
buildconfig
.
substs
[
"
DSYMUTIL
"
]
        
cmd
=
(
            
[
dsymutil
]
+
[
a
.
replace
(
"
-
a
"
"
-
-
arch
=
"
)
for
a
in
self
.
archs
if
a
]
+
[
file
]
        
)
        
print
(
"
"
.
join
(
cmd
)
file
=
sys
.
stderr
)
        
dsymutil_proc
=
subprocess
.
Popen
(
            
cmd
universal_newlines
=
True
stdout
=
subprocess
.
PIPE
stderr
=
subprocess
.
PIPE
        
)
        
dsymout
dsymerr
=
dsymutil_proc
.
communicate
(
)
        
if
dsymutil_proc
.
returncode
!
=
0
:
            
raise
RuntimeError
(
"
Error
running
dsymutil
:
%
s
"
%
dsymerr
)
        
if
not
os
.
path
.
exists
(
dsymbundle
)
:
            
print
(
"
No
symbols
found
in
file
:
%
s
"
%
(
file
)
file
=
sys
.
stderr
)
            
return
False
        
if
"
warning
:
no
debug
symbols
in
"
in
dsymerr
:
            
print
(
dsymerr
file
=
sys
.
stderr
)
            
return
False
        
contents_dir
=
os
.
path
.
join
(
dsymbundle
"
Contents
"
"
Resources
"
"
DWARF
"
)
        
if
not
os
.
path
.
exists
(
contents_dir
)
:
            
print
(
                
"
No
DWARF
information
in
.
dSYM
bundle
%
s
"
%
(
dsymbundle
)
                
file
=
sys
.
stderr
            
)
            
return
False
        
files
=
os
.
listdir
(
contents_dir
)
        
if
len
(
files
)
!
=
1
:
            
print
(
"
Unexpected
files
in
.
dSYM
bundle
%
s
"
%
(
files
)
file
=
sys
.
stderr
)
            
return
False
        
otool_out
=
subprocess
.
check_output
(
            
[
buildconfig
.
substs
[
"
OTOOL
"
]
"
-
l
"
os
.
path
.
join
(
contents_dir
files
[
0
]
)
]
            
universal_newlines
=
True
        
)
        
if
"
sectname
__debug_info
"
not
in
otool_out
:
            
print
(
"
No
symbols
in
.
dSYM
bundle
%
s
"
%
(
dsymbundle
)
file
=
sys
.
stderr
)
            
return
False
        
elapsed
=
time
.
time
(
)
-
t_start
        
print
(
"
Finished
processing
%
s
in
%
.
2fs
"
%
(
file
elapsed
)
file
=
sys
.
stderr
)
        
return
dsymbundle
    
def
CopyExeAndDebugInfo
(
self
file
debug_file
guid
code_file
code_id
)
:
        
"
"
"
ProcessFile
has
already
produced
a
dSYM
bundle
so
we
should
just
        
copy
that
to
the
destination
directory
.
However
we
'
ll
package
it
        
into
a
.
tar
because
it
'
s
a
bundle
so
it
'
s
a
directory
.
|
file
|
here
is
        
the
original
filename
.
"
"
"
        
dsymbundle
=
file
+
"
.
dSYM
"
        
rel_path
=
os
.
path
.
join
(
debug_file
guid
os
.
path
.
basename
(
dsymbundle
)
+
"
.
tar
"
)
        
full_path
=
os
.
path
.
abspath
(
os
.
path
.
join
(
self
.
symbol_path
rel_path
)
)
        
success
=
subprocess
.
call
(
            
[
"
tar
"
"
cf
"
full_path
os
.
path
.
basename
(
dsymbundle
)
]
            
cwd
=
os
.
path
.
dirname
(
dsymbundle
)
            
stdout
=
open
(
os
.
devnull
"
w
"
)
            
stderr
=
subprocess
.
STDOUT
        
)
        
if
success
=
=
0
and
os
.
path
.
exists
(
full_path
)
:
            
print
(
rel_path
)
def
main
(
)
:
    
parser
=
OptionParser
(
        
usage
=
"
usage
:
%
prog
[
options
]
<
dump_syms
binary
>
<
symbol
store
path
>
<
debug
info
files
>
"
    
)
    
parser
.
add_option
(
        
"
-
c
"
        
"
-
-
copy
"
        
action
=
"
store_true
"
        
dest
=
"
copy_debug
"
        
default
=
False
        
help
=
"
Copy
debug
info
files
into
the
same
directory
structure
as
symbol
files
"
    
)
    
parser
.
add_option
(
        
"
-
a
"
        
"
-
-
archs
"
        
action
=
"
store
"
        
dest
=
"
archs
"
        
help
=
"
Run
dump_syms
-
a
<
arch
>
for
each
space
separated
"
        
+
"
cpu
architecture
in
ARCHS
(
only
on
OS
X
)
"
    
)
    
parser
.
add_option
(
        
"
-
s
"
        
"
-
-
srcdir
"
        
action
=
"
append
"
        
dest
=
"
srcdir
"
        
default
=
[
]
        
help
=
"
Use
SRCDIR
to
determine
relative
paths
to
source
files
"
    
)
    
parser
.
add_option
(
        
"
-
v
"
        
"
-
-
vcs
-
info
"
        
action
=
"
store_true
"
        
dest
=
"
vcsinfo
"
        
help
=
"
Try
to
retrieve
VCS
info
for
each
FILE
listed
in
the
output
"
    
)
    
parser
.
add_option
(
        
"
-
i
"
        
"
-
-
source
-
index
"
        
action
=
"
store_true
"
        
dest
=
"
srcsrv
"
        
default
=
False
        
help
=
"
Add
source
index
information
to
debug
files
making
them
suitable
"
        
+
"
for
use
in
a
source
server
.
"
    
)
    
parser
.
add_option
(
        
"
-
-
install
-
manifest
"
        
action
=
"
append
"
        
dest
=
"
install_manifests
"
        
default
=
[
]
        
help
=
"
"
"
Use
this
install
manifest
to
map
filenames
back
to
canonical
locations
in
the
source
repository
.
Specify
<
install
manifest
filename
>
<
install
destination
>
as
a
comma
-
separated
pair
.
"
"
"
    
)
    
parser
.
add_option
(
        
"
-
-
count
-
ctors
"
        
action
=
"
store_true
"
        
dest
=
"
count_ctors
"
        
default
=
False
        
help
=
"
Count
static
initializers
"
    
)
    
(
options
args
)
=
parser
.
parse_args
(
)
    
if
options
.
srcsrv
:
        
if
"
PDBSTR
"
not
in
buildconfig
.
substs
:
            
print
(
"
pdbstr
was
not
found
by
configure
.
\
n
"
file
=
sys
.
stderr
)
            
sys
.
exit
(
1
)
    
if
len
(
args
)
<
3
:
        
parser
.
error
(
"
not
enough
arguments
"
)
        
exit
(
1
)
    
try
:
        
manifests
=
validate_install_manifests
(
options
.
install_manifests
)
    
except
(
IOError
ValueError
)
as
e
:
        
parser
.
error
(
str
(
e
)
)
        
exit
(
1
)
    
file_mapping
=
make_file_mapping
(
manifests
)
    
generated_files
=
{
        
realpath
(
os
.
path
.
join
(
buildconfig
.
topobjdir
f
)
)
:
f
        
for
(
f
_
)
in
get_generated_sources
(
)
    
}
    
_
bucket
=
get_s3_region_and_bucket
(
)
    
dumper
=
GetPlatformSpecificDumper
(
        
dump_syms
=
args
[
0
]
        
symbol_path
=
args
[
1
]
        
copy_debug
=
options
.
copy_debug
        
archs
=
options
.
archs
        
srcdirs
=
options
.
srcdir
        
vcsinfo
=
options
.
vcsinfo
        
srcsrv
=
options
.
srcsrv
        
generated_files
=
generated_files
        
s3_bucket
=
bucket
        
file_mapping
=
file_mapping
    
)
    
dumper
.
Process
(
args
[
2
]
options
.
count_ctors
)
if
__name__
=
=
"
__main__
"
:
    
main
(
)
