import
concurrent
.
futures
as
futures
import
errno
import
os
import
stat
import
sys
from
collections
import
Counter
OrderedDict
defaultdict
import
six
import
mozpack
.
path
as
mozpath
from
mozpack
.
errors
import
errors
from
mozpack
.
files
import
BaseFile
Dest
class
FileRegistry
(
object
)
:
    
"
"
"
    
Generic
container
to
keep
track
of
a
set
of
BaseFile
instances
.
It
    
preserves
the
order
under
which
the
files
are
added
but
doesn
'
t
keep
    
track
of
empty
directories
(
directories
are
not
stored
at
all
)
.
    
The
paths
associated
with
the
BaseFile
instances
are
relative
to
an
    
unspecified
(
virtual
)
root
directory
.
        
registry
=
FileRegistry
(
)
        
registry
.
add
(
'
foo
/
bar
'
file_instance
)
    
"
"
"
    
def
__init__
(
self
)
:
        
self
.
_files
=
OrderedDict
(
)
        
self
.
_required_directories
=
Counter
(
)
        
self
.
_partial_paths_cache
=
{
}
    
def
_partial_paths
(
self
path
)
:
        
"
"
"
        
Turn
"
foo
/
bar
/
baz
/
zot
"
into
[
"
foo
/
bar
/
baz
"
"
foo
/
bar
"
"
foo
"
]
.
        
"
"
"
        
dir_name
=
path
.
rpartition
(
"
/
"
)
[
0
]
        
if
not
dir_name
:
            
return
[
]
        
partial_paths
=
self
.
_partial_paths_cache
.
get
(
dir_name
)
        
if
partial_paths
:
            
return
partial_paths
        
partial_paths
=
[
dir_name
]
+
self
.
_partial_paths
(
dir_name
)
        
self
.
_partial_paths_cache
[
dir_name
]
=
partial_paths
        
return
partial_paths
    
def
add
(
self
path
content
)
:
        
"
"
"
        
Add
a
BaseFile
instance
to
the
container
under
the
given
path
.
        
"
"
"
        
assert
isinstance
(
content
BaseFile
)
        
if
path
in
self
.
_files
:
            
return
errors
.
error
(
"
%
s
already
added
"
%
path
)
        
if
self
.
_required_directories
[
path
]
>
0
:
            
return
errors
.
error
(
"
Can
'
t
add
%
s
:
it
is
a
required
directory
"
%
path
)
        
partial_paths
=
self
.
_partial_paths
(
path
)
        
for
partial_path
in
partial_paths
:
            
if
partial_path
in
self
.
_files
:
                
return
errors
.
error
(
"
Can
'
t
add
%
s
:
%
s
is
a
file
"
%
(
path
partial_path
)
)
        
self
.
_files
[
path
]
=
content
        
self
.
_required_directories
.
update
(
partial_paths
)
    
def
match
(
self
pattern
)
:
        
"
"
"
        
Return
the
list
of
paths
stored
in
the
container
matching
the
        
given
pattern
.
See
the
mozpack
.
path
.
match
documentation
for
a
        
description
of
the
handled
patterns
.
        
"
"
"
        
if
"
*
"
in
pattern
:
            
return
[
p
for
p
in
self
.
paths
(
)
if
mozpath
.
match
(
p
pattern
)
]
        
if
pattern
=
=
"
"
:
            
return
self
.
paths
(
)
        
if
pattern
in
self
.
_files
:
            
return
[
pattern
]
        
return
[
p
for
p
in
self
.
paths
(
)
if
mozpath
.
basedir
(
p
[
pattern
]
)
=
=
pattern
]
    
def
remove
(
self
pattern
)
:
        
"
"
"
        
Remove
paths
matching
the
given
pattern
from
the
container
.
See
the
        
mozpack
.
path
.
match
documentation
for
a
description
of
the
handled
        
patterns
.
        
"
"
"
        
items
=
self
.
match
(
pattern
)
        
if
not
items
:
            
return
errors
.
error
(
                
"
Can
'
t
remove
%
s
:
%
s
"
                
%
(
pattern
"
not
matching
anything
previously
added
"
)
            
)
        
for
i
in
items
:
            
del
self
.
_files
[
i
]
            
self
.
_required_directories
.
subtract
(
self
.
_partial_paths
(
i
)
)
    
def
paths
(
self
)
:
        
"
"
"
        
Return
all
paths
stored
in
the
container
in
the
order
they
were
added
.
        
"
"
"
        
return
list
(
self
.
_files
)
    
def
__len__
(
self
)
:
        
"
"
"
        
Return
number
of
paths
stored
in
the
container
.
        
"
"
"
        
return
len
(
self
.
_files
)
    
def
__contains__
(
self
pattern
)
:
        
raise
RuntimeError
(
            
"
'
in
'
operator
forbidden
for
%
s
.
Use
contains
(
)
.
"
%
self
.
__class__
.
__name__
        
)
    
def
contains
(
self
pattern
)
:
        
"
"
"
        
Return
whether
the
container
contains
paths
matching
the
given
        
pattern
.
See
the
mozpack
.
path
.
match
documentation
for
a
description
of
        
the
handled
patterns
.
        
"
"
"
        
return
len
(
self
.
match
(
pattern
)
)
>
0
    
def
__getitem__
(
self
path
)
:
        
"
"
"
        
Return
the
BaseFile
instance
stored
in
the
container
for
the
given
        
path
.
        
"
"
"
        
return
self
.
_files
[
path
]
    
def
__iter__
(
self
)
:
        
"
"
"
        
Iterate
over
all
(
path
BaseFile
instance
)
pairs
from
the
container
.
            
for
path
file
in
registry
:
                
(
.
.
.
)
        
"
"
"
        
return
six
.
iteritems
(
self
.
_files
)
    
def
required_directories
(
self
)
:
        
"
"
"
        
Return
the
set
of
directories
required
by
the
paths
in
the
container
        
in
no
particular
order
.
The
returned
directories
are
relative
to
an
        
unspecified
(
virtual
)
root
directory
(
and
do
not
include
said
root
        
directory
)
.
        
"
"
"
        
return
set
(
k
for
k
v
in
self
.
_required_directories
.
items
(
)
if
v
>
0
)
    
def
output_to_inputs_tree
(
self
)
:
        
"
"
"
        
Return
a
dictionary
mapping
each
output
path
to
the
set
of
its
        
required
input
paths
.
        
All
paths
are
normalized
.
        
"
"
"
        
tree
=
{
}
        
for
output
file
in
self
:
            
output
=
mozpath
.
normpath
(
output
)
            
tree
[
output
]
=
set
(
mozpath
.
normpath
(
f
)
for
f
in
file
.
inputs
(
)
)
        
return
tree
    
def
input_to_outputs_tree
(
self
)
:
        
"
"
"
        
Return
a
dictionary
mapping
each
input
path
to
the
set
of
        
impacted
output
paths
.
        
All
paths
are
normalized
.
        
"
"
"
        
tree
=
defaultdict
(
set
)
        
for
output
file
in
self
:
            
output
=
mozpath
.
normpath
(
output
)
            
for
input
in
file
.
inputs
(
)
:
                
input
=
mozpath
.
normpath
(
input
)
                
tree
[
input
]
.
add
(
output
)
        
return
dict
(
tree
)
class
FileRegistrySubtree
(
object
)
:
    
"
"
"
A
proxy
class
to
give
access
to
a
subtree
of
an
existing
FileRegistry
.
    
Note
this
doesn
'
t
implement
the
whole
FileRegistry
interface
.
"
"
"
    
def
__new__
(
cls
base
registry
)
:
        
if
not
base
:
            
return
registry
        
return
object
.
__new__
(
cls
)
    
def
__init__
(
self
base
registry
)
:
        
self
.
_base
=
base
        
self
.
_registry
=
registry
    
def
_get_path
(
self
path
)
:
        
return
mozpath
.
join
(
self
.
_base
path
)
if
path
else
self
.
_base
    
def
add
(
self
path
content
)
:
        
return
self
.
_registry
.
add
(
self
.
_get_path
(
path
)
content
)
    
def
match
(
self
pattern
)
:
        
return
[
            
mozpath
.
relpath
(
p
self
.
_base
)
            
for
p
in
self
.
_registry
.
match
(
self
.
_get_path
(
pattern
)
)
        
]
    
def
remove
(
self
pattern
)
:
        
return
self
.
_registry
.
remove
(
self
.
_get_path
(
pattern
)
)
    
def
paths
(
self
)
:
        
return
[
p
for
p
f
in
self
]
    
def
__len__
(
self
)
:
        
return
len
(
self
.
paths
(
)
)
    
def
contains
(
self
pattern
)
:
        
return
self
.
_registry
.
contains
(
self
.
_get_path
(
pattern
)
)
    
def
__getitem__
(
self
path
)
:
        
return
self
.
_registry
[
self
.
_get_path
(
path
)
]
    
def
__iter__
(
self
)
:
        
for
p
f
in
self
.
_registry
:
            
if
mozpath
.
basedir
(
p
[
self
.
_base
]
)
:
                
yield
mozpath
.
relpath
(
p
self
.
_base
)
f
class
FileCopyResult
(
object
)
:
    
"
"
"
Represents
results
of
a
FileCopier
.
copy
operation
.
"
"
"
    
def
__init__
(
self
)
:
        
self
.
updated_files
=
set
(
)
        
self
.
existing_files
=
set
(
)
        
self
.
removed_files
=
set
(
)
        
self
.
removed_directories
=
set
(
)
    
property
    
def
updated_files_count
(
self
)
:
        
return
len
(
self
.
updated_files
)
    
property
    
def
existing_files_count
(
self
)
:
        
return
len
(
self
.
existing_files
)
    
property
    
def
removed_files_count
(
self
)
:
        
return
len
(
self
.
removed_files
)
    
property
    
def
removed_directories_count
(
self
)
:
        
return
len
(
self
.
removed_directories
)
class
FileCopier
(
FileRegistry
)
:
    
"
"
"
    
FileRegistry
with
the
ability
to
copy
the
registered
files
to
a
separate
    
directory
.
    
"
"
"
    
def
copy
(
        
self
        
destination
        
skip_if_older
=
True
        
remove_unaccounted
=
True
        
remove_all_directory_symlinks
=
True
        
remove_empty_directories
=
True
    
)
:
        
"
"
"
        
Copy
all
registered
files
to
the
given
destination
path
.
The
given
        
destination
can
be
an
existing
directory
or
not
exist
at
all
.
It
        
can
'
t
be
e
.
g
.
a
file
.
        
The
copy
process
acts
a
bit
like
rsync
:
files
are
not
copied
when
they
        
don
'
t
need
to
(
see
mozpack
.
files
for
details
on
file
.
copy
)
.
        
By
default
files
in
the
destination
directory
that
aren
'
t
        
registered
are
removed
and
empty
directories
are
deleted
.
In
        
addition
all
directory
symlinks
in
the
destination
directory
        
are
deleted
:
this
is
a
conservative
approach
to
ensure
that
we
        
never
accidently
write
files
into
a
directory
that
is
not
the
        
destination
directory
.
In
the
worst
case
we
might
have
a
        
directory
symlink
in
the
object
directory
to
the
source
        
directory
.
        
To
disable
removing
of
unregistered
files
pass
        
remove_unaccounted
=
False
.
To
disable
removing
empty
        
directories
pass
remove_empty_directories
=
False
.
In
rare
        
cases
you
might
want
to
maintain
directory
symlinks
in
the
        
destination
directory
(
at
least
those
that
are
not
required
to
        
be
regular
directories
)
:
pass
        
remove_all_directory_symlinks
=
False
.
Exercise
caution
with
        
this
flag
:
you
almost
certainly
do
not
want
to
preserve
        
directory
symlinks
.
        
Returns
a
FileCopyResult
that
details
what
changed
.
        
"
"
"
        
assert
isinstance
(
destination
six
.
string_types
)
        
assert
not
os
.
path
.
exists
(
destination
)
or
os
.
path
.
isdir
(
destination
)
        
result
=
FileCopyResult
(
)
        
have_symlinks
=
hasattr
(
os
"
symlink
"
)
        
destination
=
os
.
path
.
normpath
(
destination
)
        
os
.
makedirs
(
destination
exist_ok
=
True
)
        
required_dirs
=
set
(
[
destination
]
)
        
required_dirs
|
=
set
(
            
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
destination
d
)
)
            
for
d
in
self
.
required_directories
(
)
        
)
        
for
d
in
sorted
(
required_dirs
key
=
len
)
:
            
os
.
makedirs
(
d
exist_ok
=
True
)
            
if
have_symlinks
and
d
!
=
destination
:
                
st
=
os
.
lstat
(
d
)
                
if
stat
.
S_ISLNK
(
st
.
st_mode
)
:
                    
os
.
remove
(
d
)
                    
os
.
mkdir
(
d
)
            
if
not
os
.
access
(
d
os
.
W_OK
)
:
                
umask
=
os
.
umask
(
0o077
)
                
os
.
umask
(
umask
)
                
os
.
chmod
(
d
0o777
&
~
umask
)
        
if
isinstance
(
remove_unaccounted
FileRegistry
)
:
            
existing_files
=
set
(
                
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
destination
p
)
)
                
for
p
in
remove_unaccounted
.
paths
(
)
            
)
            
existing_dirs
=
set
(
                
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
destination
p
)
)
                
for
p
in
remove_unaccounted
.
required_directories
(
)
            
)
            
existing_dirs
|
=
{
os
.
path
.
normpath
(
destination
)
}
        
else
:
            
existing_dirs
=
set
(
)
            
existing_files
=
set
(
)
            
for
root
dirs
files
in
os
.
walk
(
destination
)
:
                
if
have_symlinks
:
                    
filtered
=
[
]
                    
for
d
in
dirs
:
                        
full
=
os
.
path
.
join
(
root
d
)
                        
st
=
os
.
lstat
(
full
)
                        
if
stat
.
S_ISLNK
(
st
.
st_mode
)
:
                            
if
remove_all_directory_symlinks
:
                                
os
.
remove
(
full
)
                                
result
.
removed_files
.
add
(
os
.
path
.
normpath
(
full
)
)
                            
else
:
                                
existing_files
.
add
(
os
.
path
.
normpath
(
full
)
)
                        
else
:
                            
filtered
.
append
(
d
)
                    
dirs
[
:
]
=
filtered
                
existing_dirs
.
add
(
os
.
path
.
normpath
(
root
)
)
                
for
d
in
dirs
:
                    
existing_dirs
.
add
(
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
root
d
)
)
)
                
for
f
in
files
:
                    
existing_files
.
add
(
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
root
f
)
)
)
        
dest_files
=
set
(
)
        
copy_results
=
[
]
        
if
sys
.
platform
=
=
"
win32
"
and
len
(
self
)
>
100
:
            
with
futures
.
ThreadPoolExecutor
(
4
)
as
e
:
                
fs
=
[
]
                
for
p
f
in
self
:
                    
destfile
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
destination
p
)
)
                    
fs
.
append
(
(
destfile
e
.
submit
(
f
.
copy
destfile
skip_if_older
)
)
)
            
copy_results
=
[
(
path
f
.
result
)
for
path
f
in
fs
]
        
else
:
            
for
p
f
in
self
:
                
destfile
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
destination
p
)
)
                
copy_results
.
append
(
(
destfile
f
.
copy
(
destfile
skip_if_older
)
)
)
        
for
destfile
copy_result
in
copy_results
:
            
dest_files
.
add
(
destfile
)
            
if
copy_result
:
                
result
.
updated_files
.
add
(
destfile
)
            
else
:
                
result
.
existing_files
.
add
(
destfile
)
        
if
remove_unaccounted
:
            
for
f
in
existing_files
-
dest_files
:
                
if
os
.
name
=
=
"
nt
"
and
not
os
.
access
(
f
os
.
W_OK
)
:
                    
os
.
chmod
(
f
0o600
)
                
os
.
remove
(
f
)
                
result
.
removed_files
.
add
(
f
)
        
if
not
remove_empty_directories
:
            
return
result
        
remove_dirs
=
existing_dirs
-
required_dirs
        
if
not
remove_unaccounted
:
            
parents
=
set
(
)
            
pathsep
=
os
.
path
.
sep
            
for
f
in
existing_files
:
                
path
=
f
                
while
True
:
                    
dirname
=
path
.
rpartition
(
pathsep
)
[
0
]
                    
if
dirname
in
parents
:
                        
break
                    
parents
.
add
(
dirname
)
                    
path
=
dirname
            
remove_dirs
-
=
parents
        
for
d
in
sorted
(
remove_dirs
key
=
len
reverse
=
True
)
:
            
try
:
                
try
:
                    
os
.
rmdir
(
d
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
in
(
errno
.
EPERM
errno
.
EACCES
)
:
                        
os
.
chmod
(
d
0o700
)
                        
os
.
rmdir
(
d
)
                    
else
:
                        
raise
            
except
OSError
as
e
:
                
if
(
                    
isinstance
(
remove_unaccounted
FileRegistry
)
                    
and
e
.
errno
=
=
errno
.
ENOTEMPTY
                
)
:
                    
continue
                
raise
            
result
.
removed_directories
.
add
(
d
)
        
return
result
class
Jarrer
(
FileRegistry
BaseFile
)
:
    
"
"
"
    
FileRegistry
with
the
ability
to
copy
and
pack
the
registered
files
as
a
    
jar
file
.
Also
acts
as
a
BaseFile
instance
to
be
copied
with
a
FileCopier
.
    
"
"
"
    
def
__init__
(
self
compress
=
True
)
:
        
"
"
"
        
Create
a
Jarrer
instance
.
See
mozpack
.
mozjar
.
JarWriter
documentation
        
for
details
on
the
compress
argument
.
        
"
"
"
        
self
.
compress
=
compress
        
self
.
_preload
=
[
]
        
self
.
_compress_options
=
{
}
        
FileRegistry
.
__init__
(
self
)
    
def
add
(
self
path
content
compress
=
None
)
:
        
FileRegistry
.
add
(
self
path
content
)
        
if
compress
is
not
None
:
            
self
.
_compress_options
[
path
]
=
compress
    
def
copy
(
self
dest
skip_if_older
=
True
)
:
        
"
"
"
        
Pack
all
registered
files
in
the
given
destination
jar
.
The
given
        
destination
jar
may
be
a
path
to
jar
file
or
a
Dest
instance
for
        
a
jar
file
.
        
If
the
destination
jar
file
exists
its
(
compressed
)
contents
are
used
        
instead
of
the
registered
BaseFile
instances
when
appropriate
.
        
"
"
"
        
class
DeflaterDest
(
Dest
)
:
            
"
"
"
            
Dest
-
like
class
reading
from
a
file
-
like
object
initially
but
            
switching
to
a
Deflater
object
if
written
to
.
                
dest
=
DeflaterDest
(
original_file
)
                
dest
.
read
(
)
#
Reads
original_file
                
dest
.
write
(
data
)
#
Creates
a
Deflater
and
write
data
there
                
dest
.
read
(
)
#
Re
-
opens
the
Deflater
and
reads
from
it
            
"
"
"
            
def
__init__
(
self
orig
=
None
compress
=
True
)
:
                
self
.
mode
=
None
                
self
.
deflater
=
orig
                
self
.
compress
=
compress
            
def
read
(
self
length
=
-
1
)
:
                
if
self
.
mode
!
=
"
r
"
:
                    
assert
self
.
mode
is
None
                    
self
.
mode
=
"
r
"
                
return
self
.
deflater
.
read
(
length
)
            
def
write
(
self
data
)
:
                
if
self
.
mode
!
=
"
w
"
:
                    
from
mozpack
.
mozjar
import
Deflater
                    
self
.
deflater
=
Deflater
(
self
.
compress
)
                    
self
.
mode
=
"
w
"
                
self
.
deflater
.
write
(
data
)
            
def
exists
(
self
)
:
                
return
self
.
deflater
is
not
None
        
if
isinstance
(
dest
six
.
string_types
)
:
            
dest
=
Dest
(
dest
)
        
assert
isinstance
(
dest
Dest
)
        
from
mozpack
.
mozjar
import
JarReader
JarWriter
        
try
:
            
old_jar
=
JarReader
(
fileobj
=
dest
)
        
except
Exception
:
            
old_jar
=
[
]
        
old_contents
=
dict
(
[
(
f
.
filename
f
)
for
f
in
old_jar
]
)
        
with
JarWriter
(
fileobj
=
dest
compress
=
self
.
compress
)
as
jar
:
            
for
path
file
in
self
:
                
compress
=
self
.
_compress_options
.
get
(
path
self
.
compress
)
                
if
path
in
old_contents
:
                    
deflater
=
DeflaterDest
(
old_contents
[
path
]
compress
)
                
else
:
                    
deflater
=
DeflaterDest
(
compress
=
compress
)
                
file
.
copy
(
deflater
skip_if_older
)
                
jar
.
add
(
path
deflater
.
deflater
mode
=
file
.
mode
compress
=
compress
)
            
if
self
.
_preload
:
                
jar
.
preload
(
self
.
_preload
)
    
def
open
(
self
)
:
        
raise
RuntimeError
(
"
unsupported
"
)
    
def
preload
(
self
paths
)
:
        
"
"
"
        
Add
the
given
set
of
paths
to
the
list
of
preloaded
files
.
See
        
mozpack
.
mozjar
.
JarWriter
documentation
for
details
on
jar
preloading
.
        
"
"
"
        
self
.
_preload
.
extend
(
paths
)
