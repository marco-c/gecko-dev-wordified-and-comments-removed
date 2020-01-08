from
__future__
import
with_statement
import
collections
import
errno
import
filecmp
import
os
.
path
import
re
import
tempfile
import
sys
class
memoize
(
object
)
:
  
def
__init__
(
self
func
)
:
    
self
.
func
=
func
    
self
.
cache
=
{
}
  
def
__call__
(
self
*
args
)
:
    
try
:
      
return
self
.
cache
[
args
]
    
except
KeyError
:
      
result
=
self
.
func
(
*
args
)
      
self
.
cache
[
args
]
=
result
      
return
result
class
GypError
(
Exception
)
:
  
"
"
"
Error
class
representing
an
error
which
is
to
be
presented
  
to
the
user
.
The
main
entry
point
will
catch
and
display
this
.
  
"
"
"
  
pass
def
ExceptionAppend
(
e
msg
)
:
  
"
"
"
Append
a
message
to
the
given
exception
'
s
message
.
"
"
"
  
if
not
e
.
args
:
    
e
.
args
=
(
msg
)
  
elif
len
(
e
.
args
)
=
=
1
:
    
e
.
args
=
(
str
(
e
.
args
[
0
]
)
+
'
'
+
msg
)
  
else
:
    
e
.
args
=
(
str
(
e
.
args
[
0
]
)
+
'
'
+
msg
)
+
e
.
args
[
1
:
]
def
FindQualifiedTargets
(
target
qualified_list
)
:
  
"
"
"
  
Given
a
list
of
qualified
targets
return
the
qualified
targets
for
the
  
specified
|
target
|
.
  
"
"
"
  
return
[
t
for
t
in
qualified_list
if
ParseQualifiedTarget
(
t
)
[
1
]
=
=
target
]
def
ParseQualifiedTarget
(
target
)
:
  
target_split
=
target
.
rsplit
(
'
:
'
1
)
  
if
len
(
target_split
)
=
=
2
:
    
[
build_file
target
]
=
target_split
  
else
:
    
build_file
=
None
  
target_split
=
target
.
rsplit
(
'
#
'
1
)
  
if
len
(
target_split
)
=
=
2
:
    
[
target
toolset
]
=
target_split
  
else
:
    
toolset
=
None
  
return
[
build_file
target
toolset
]
def
ResolveTarget
(
build_file
target
toolset
)
:
  
[
parsed_build_file
target
parsed_toolset
]
=
ParseQualifiedTarget
(
target
)
  
if
parsed_build_file
:
    
if
build_file
:
      
build_file
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
os
.
path
.
dirname
(
build_file
)
                                                 
parsed_build_file
)
)
      
if
not
os
.
path
.
isabs
(
build_file
)
:
        
build_file
=
RelativePath
(
build_file
'
.
'
)
    
else
:
      
build_file
=
parsed_build_file
  
if
parsed_toolset
:
    
toolset
=
parsed_toolset
  
return
[
build_file
target
toolset
]
def
BuildFile
(
fully_qualified_target
)
:
  
return
ParseQualifiedTarget
(
fully_qualified_target
)
[
0
]
def
GetEnvironFallback
(
var_list
default
)
:
  
"
"
"
Look
up
a
key
in
the
environment
with
fallback
to
secondary
keys
  
and
finally
falling
back
to
a
default
value
.
"
"
"
  
for
var
in
var_list
:
    
if
var
in
os
.
environ
:
      
return
os
.
environ
[
var
]
  
return
default
def
QualifiedTarget
(
build_file
target
toolset
)
:
  
fully_qualified
=
build_file
+
'
:
'
+
target
  
if
toolset
:
    
fully_qualified
=
fully_qualified
+
'
#
'
+
toolset
  
return
fully_qualified
memoize
def
RelativePath
(
path
relative_to
follow_path_symlink
=
True
)
:
  
if
follow_path_symlink
:
    
path
=
os
.
path
.
realpath
(
path
)
  
else
:
    
path
=
os
.
path
.
abspath
(
path
)
  
relative_to
=
os
.
path
.
realpath
(
relative_to
)
  
if
sys
.
platform
=
=
'
win32
'
:
    
if
(
os
.
path
.
splitdrive
(
path
)
[
0
]
.
lower
(
)
!
=
        
os
.
path
.
splitdrive
(
relative_to
)
[
0
]
.
lower
(
)
)
:
      
return
path
  
path_split
=
path
.
split
(
os
.
path
.
sep
)
  
relative_to_split
=
relative_to
.
split
(
os
.
path
.
sep
)
  
prefix_len
=
len
(
os
.
path
.
commonprefix
(
[
path_split
relative_to_split
]
)
)
  
relative_split
=
[
os
.
path
.
pardir
]
*
(
len
(
relative_to_split
)
-
prefix_len
)
+
\
                   
path_split
[
prefix_len
:
]
  
if
len
(
relative_split
)
=
=
0
:
    
return
'
'
  
return
os
.
path
.
join
(
*
relative_split
)
memoize
def
InvertRelativePath
(
path
toplevel_dir
=
None
)
:
  
"
"
"
Given
a
path
like
foo
/
bar
that
is
relative
to
toplevel_dir
return
  
the
inverse
relative
path
back
to
the
toplevel_dir
.
  
E
.
g
.
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
path
InvertRelativePath
(
path
)
)
)
  
should
always
produce
the
empty
string
unless
the
path
contains
symlinks
.
  
"
"
"
  
if
not
path
:
    
return
path
  
toplevel_dir
=
'
.
'
if
toplevel_dir
is
None
else
toplevel_dir
  
return
RelativePath
(
toplevel_dir
os
.
path
.
join
(
toplevel_dir
path
)
)
def
FixIfRelativePath
(
path
relative_to
)
:
  
if
os
.
path
.
isabs
(
path
)
:
    
return
path
  
return
RelativePath
(
path
relative_to
)
def
UnrelativePath
(
path
relative_to
)
:
  
rel_dir
=
os
.
path
.
dirname
(
relative_to
)
  
return
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
rel_dir
path
)
)
_quote
=
re
.
compile
(
'
[
\
t
\
n
#
%
&
\
'
(
)
*
;
<
=
>
?
[
{
|
}
~
]
|
^
'
)
_escape
=
re
.
compile
(
r
'
(
[
"
\
\
]
)
'
)
def
EncodePOSIXShellArgument
(
argument
)
:
  
"
"
"
Encodes
|
argument
|
suitably
for
consumption
by
POSIX
shells
.
  
argument
may
be
quoted
and
escaped
as
necessary
to
ensure
that
POSIX
shells
  
treat
the
returned
value
as
a
literal
representing
the
argument
passed
to
  
this
function
.
Parameter
(
variable
)
expansions
beginning
with
are
allowed
  
to
remain
intact
without
escaping
the
to
allow
the
argument
to
contain
  
references
to
variables
to
be
expanded
by
the
shell
.
  
"
"
"
  
if
not
isinstance
(
argument
str
)
:
    
argument
=
str
(
argument
)
  
if
_quote
.
search
(
argument
)
:
    
quote
=
'
"
'
  
else
:
    
quote
=
'
'
  
encoded
=
quote
+
re
.
sub
(
_escape
r
'
\
\
\
1
'
argument
)
+
quote
  
return
encoded
def
EncodePOSIXShellList
(
list
)
:
  
"
"
"
Encodes
|
list
|
suitably
for
consumption
by
POSIX
shells
.
  
Returns
EncodePOSIXShellArgument
for
each
item
in
list
and
joins
them
  
together
using
the
space
character
as
an
argument
separator
.
  
"
"
"
  
encoded_arguments
=
[
]
  
for
argument
in
list
:
    
encoded_arguments
.
append
(
EncodePOSIXShellArgument
(
argument
)
)
  
return
'
'
.
join
(
encoded_arguments
)
def
DeepDependencyTargets
(
target_dicts
roots
)
:
  
"
"
"
Returns
the
recursive
list
of
target
dependencies
.
"
"
"
  
dependencies
=
set
(
)
  
pending
=
set
(
roots
)
  
while
pending
:
    
r
=
pending
.
pop
(
)
    
if
r
in
dependencies
:
      
continue
    
dependencies
.
add
(
r
)
    
spec
=
target_dicts
[
r
]
    
pending
.
update
(
set
(
spec
.
get
(
'
dependencies
'
[
]
)
)
)
    
pending
.
update
(
set
(
spec
.
get
(
'
dependencies_original
'
[
]
)
)
)
  
return
list
(
dependencies
-
set
(
roots
)
)
def
BuildFileTargets
(
target_list
build_file
)
:
  
"
"
"
From
a
target_list
returns
the
subset
from
the
specified
build_file
.
  
"
"
"
  
return
[
p
for
p
in
target_list
if
BuildFile
(
p
)
=
=
build_file
]
def
AllTargets
(
target_list
target_dicts
build_file
)
:
  
"
"
"
Returns
all
targets
(
direct
and
dependencies
)
for
the
specified
build_file
.
  
"
"
"
  
bftargets
=
BuildFileTargets
(
target_list
build_file
)
  
deptargets
=
DeepDependencyTargets
(
target_dicts
bftargets
)
  
return
bftargets
+
deptargets
def
WriteOnDiff
(
filename
)
:
  
"
"
"
Write
to
a
file
only
if
the
new
contents
differ
.
  
Arguments
:
    
filename
:
name
of
the
file
to
potentially
write
to
.
  
Returns
:
    
A
file
like
object
which
will
write
to
temporary
file
and
only
overwrite
    
the
target
if
it
differs
(
on
close
)
.
  
"
"
"
  
class
Writer
(
object
)
:
    
"
"
"
Wrapper
around
file
which
only
covers
the
target
if
it
differs
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
      
tmp_fd
self
.
tmp_path
=
tempfile
.
mkstemp
(
          
suffix
=
'
.
tmp
'
          
prefix
=
os
.
path
.
split
(
filename
)
[
1
]
+
'
.
gyp
.
'
          
dir
=
os
.
path
.
split
(
filename
)
[
0
]
)
      
try
:
        
self
.
tmp_file
=
os
.
fdopen
(
tmp_fd
'
wb
'
)
      
except
Exception
:
        
os
.
unlink
(
self
.
tmp_path
)
        
raise
    
def
__getattr__
(
self
attrname
)
:
      
return
getattr
(
self
.
tmp_file
attrname
)
    
def
close
(
self
)
:
      
try
:
        
self
.
tmp_file
.
close
(
)
        
same
=
False
        
try
:
          
same
=
filecmp
.
cmp
(
self
.
tmp_path
filename
False
)
        
except
OSError
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
ENOENT
:
            
raise
        
if
same
:
          
os
.
unlink
(
self
.
tmp_path
)
        
else
:
          
umask
=
os
.
umask
(
077
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
self
.
tmp_path
0666
&
~
umask
)
          
if
sys
.
platform
=
=
'
win32
'
and
os
.
path
.
exists
(
filename
)
:
            
os
.
remove
(
filename
)
          
os
.
rename
(
self
.
tmp_path
filename
)
      
except
Exception
:
        
os
.
unlink
(
self
.
tmp_path
)
        
raise
  
return
Writer
(
)
def
EnsureDirExists
(
path
)
:
  
"
"
"
Make
sure
the
directory
for
|
path
|
exists
.
"
"
"
  
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
path
)
)
  
except
OSError
:
    
pass
def
GetFlavor
(
params
)
:
  
"
"
"
Returns
|
params
.
flavor
|
if
it
'
s
set
the
system
'
s
default
flavor
else
.
"
"
"
  
flavors
=
{
    
'
cygwin
'
:
'
win
'
    
'
win32
'
:
'
win
'
    
'
darwin
'
:
'
mac
'
  
}
  
if
'
flavor
'
in
params
:
    
return
params
[
'
flavor
'
]
  
if
sys
.
platform
in
flavors
:
    
return
flavors
[
sys
.
platform
]
  
if
sys
.
platform
.
startswith
(
'
sunos
'
)
:
    
return
'
solaris
'
  
if
sys
.
platform
.
startswith
(
'
freebsd
'
)
:
    
return
'
freebsd
'
  
if
sys
.
platform
.
startswith
(
'
openbsd
'
)
:
    
return
'
openbsd
'
  
if
sys
.
platform
.
startswith
(
'
netbsd
'
)
:
    
return
'
netbsd
'
  
if
sys
.
platform
.
startswith
(
'
aix
'
)
:
    
return
'
aix
'
  
if
sys
.
platform
.
startswith
(
'
zos
'
)
:
    
return
'
zos
'
  
if
sys
.
platform
.
startswith
(
'
os390
'
)
:
    
return
'
zos
'
  
return
'
linux
'
def
CopyTool
(
flavor
out_path
generator_flags
=
{
}
)
:
  
"
"
"
Finds
(
flock
|
mac
|
win
)
_tool
.
gyp
in
the
gyp
directory
and
copies
it
  
to
|
out_path
|
.
"
"
"
  
prefix
=
{
      
'
aix
'
:
'
flock
'
      
'
solaris
'
:
'
flock
'
      
'
mac
'
:
'
mac
'
      
'
win
'
:
'
win
'
      
}
.
get
(
flavor
None
)
  
if
not
prefix
:
    
return
  
source_path
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
os
.
path
.
abspath
(
__file__
)
)
'
%
s_tool
.
py
'
%
prefix
)
  
with
open
(
source_path
)
as
source_file
:
    
source
=
source_file
.
readlines
(
)
  
header
=
'
#
Generated
by
gyp
.
Do
not
edit
.
\
n
'
  
mac_toolchain_dir
=
generator_flags
.
get
(
'
mac_toolchain_dir
'
None
)
  
if
flavor
=
=
'
mac
'
and
mac_toolchain_dir
:
    
header
+
=
"
import
os
;
\
nos
.
environ
[
'
DEVELOPER_DIR
'
]
=
'
%
s
'
\
n
"
\
        
%
mac_toolchain_dir
  
tool_path
=
os
.
path
.
join
(
out_path
'
gyp
-
%
s
-
tool
'
%
prefix
)
  
with
open
(
tool_path
'
w
'
)
as
tool_file
:
    
tool_file
.
write
(
        
'
'
.
join
(
[
source
[
0
]
header
]
+
source
[
1
:
]
)
)
  
os
.
chmod
(
tool_path
0755
)
def
uniquer
(
seq
idfun
=
None
)
:
    
if
idfun
is
None
:
        
idfun
=
lambda
x
:
x
    
seen
=
{
}
    
result
=
[
]
    
for
item
in
seq
:
        
marker
=
idfun
(
item
)
        
if
marker
in
seen
:
continue
        
seen
[
marker
]
=
1
        
result
.
append
(
item
)
    
return
result
class
OrderedSet
(
collections
.
MutableSet
)
:
  
def
__init__
(
self
iterable
=
None
)
:
    
self
.
end
=
end
=
[
]
    
end
+
=
[
None
end
end
]
    
self
.
map
=
{
}
    
if
iterable
is
not
None
:
      
self
|
=
iterable
  
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
map
)
  
def
__contains__
(
self
key
)
:
    
return
key
in
self
.
map
  
def
add
(
self
key
)
:
    
if
key
not
in
self
.
map
:
      
end
=
self
.
end
      
curr
=
end
[
1
]
      
curr
[
2
]
=
end
[
1
]
=
self
.
map
[
key
]
=
[
key
curr
end
]
  
def
discard
(
self
key
)
:
    
if
key
in
self
.
map
:
      
key
prev_item
next_item
=
self
.
map
.
pop
(
key
)
      
prev_item
[
2
]
=
next_item
      
next_item
[
1
]
=
prev_item
  
def
__iter__
(
self
)
:
    
end
=
self
.
end
    
curr
=
end
[
2
]
    
while
curr
is
not
end
:
      
yield
curr
[
0
]
      
curr
=
curr
[
2
]
  
def
__reversed__
(
self
)
:
    
end
=
self
.
end
    
curr
=
end
[
1
]
    
while
curr
is
not
end
:
      
yield
curr
[
0
]
      
curr
=
curr
[
1
]
  
def
pop
(
self
last
=
True
)
:
    
if
not
self
:
      
raise
KeyError
(
'
set
is
empty
'
)
    
key
=
self
.
end
[
1
]
[
0
]
if
last
else
self
.
end
[
2
]
[
0
]
    
self
.
discard
(
key
)
    
return
key
  
def
__repr__
(
self
)
:
    
if
not
self
:
      
return
'
%
s
(
)
'
%
(
self
.
__class__
.
__name__
)
    
return
'
%
s
(
%
r
)
'
%
(
self
.
__class__
.
__name__
list
(
self
)
)
  
def
__eq__
(
self
other
)
:
    
if
isinstance
(
other
OrderedSet
)
:
      
return
len
(
self
)
=
=
len
(
other
)
and
list
(
self
)
=
=
list
(
other
)
    
return
set
(
self
)
=
=
set
(
other
)
  
def
update
(
self
iterable
)
:
    
for
i
in
iterable
:
      
if
i
not
in
self
:
        
self
.
add
(
i
)
class
CycleError
(
Exception
)
:
  
"
"
"
An
exception
raised
when
an
unexpected
cycle
is
detected
.
"
"
"
  
def
__init__
(
self
nodes
)
:
    
self
.
nodes
=
nodes
  
def
__str__
(
self
)
:
    
return
'
CycleError
:
cycle
involving
:
'
+
str
(
self
.
nodes
)
def
TopologicallySorted
(
graph
get_edges
)
:
  
r
"
"
"
Topologically
sort
based
on
a
user
provided
edge
definition
.
  
Args
:
    
graph
:
A
list
of
node
names
.
    
get_edges
:
A
function
mapping
from
node
name
to
a
hashable
collection
               
of
node
names
which
this
node
has
outgoing
edges
to
.
  
Returns
:
    
A
list
containing
all
of
the
node
in
graph
in
topological
order
.
    
It
is
assumed
that
calling
get_edges
once
for
each
node
and
caching
is
    
cheaper
than
repeatedly
calling
get_edges
.
  
Raises
:
    
CycleError
in
the
event
of
a
cycle
.
  
Example
:
    
graph
=
{
'
a
'
:
'
(
b
)
(
c
)
'
'
b
'
:
'
hi
'
'
c
'
:
'
(
b
)
'
}
    
def
GetEdges
(
node
)
:
      
return
re
.
findall
(
r
'
\
\
(
(
[
^
)
)
]
\
)
'
graph
[
node
]
)
    
print
TopologicallySorted
(
graph
.
keys
(
)
GetEdges
)
    
=
=
>
    
[
'
a
'
'
c
'
b
'
]
  
"
"
"
  
get_edges
=
memoize
(
get_edges
)
  
visited
=
set
(
)
  
visiting
=
set
(
)
  
ordered_nodes
=
[
]
  
def
Visit
(
node
)
:
    
if
node
in
visiting
:
      
raise
CycleError
(
visiting
)
    
if
node
in
visited
:
      
return
    
visited
.
add
(
node
)
    
visiting
.
add
(
node
)
    
for
neighbor
in
get_edges
(
node
)
:
      
Visit
(
neighbor
)
    
visiting
.
remove
(
node
)
    
ordered_nodes
.
insert
(
0
node
)
  
for
node
in
sorted
(
graph
)
:
    
Visit
(
node
)
  
return
ordered_nodes
def
CrossCompileRequested
(
)
:
  
return
(
os
.
environ
.
get
(
'
GYP_CROSSCOMPILE
'
)
or
          
os
.
environ
.
get
(
'
AR_host
'
)
or
          
os
.
environ
.
get
(
'
CC_host
'
)
or
          
os
.
environ
.
get
(
'
CXX_host
'
)
or
          
os
.
environ
.
get
(
'
AR_target
'
)
or
          
os
.
environ
.
get
(
'
CC_target
'
)
or
          
os
.
environ
.
get
(
'
CXX_target
'
)
)
