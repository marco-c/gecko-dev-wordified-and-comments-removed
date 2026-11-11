import
os
import
struct
import
subprocess
from
io
import
BytesIO
from
mozpack
.
errors
import
errors
MACHO_SIGNATURES
=
[
    
0xFEEDFACE
    
0xCEFAEDFE
    
0xFEEDFACF
    
0xCFFAEDFE
]
FAT_SIGNATURE
=
0xCAFEBABE
ELF_SIGNATURE
=
0x7F454C46
UNKNOWN
=
0
MACHO
=
1
ELF
=
2
def
get_type
(
path_or_fileobj
)
:
    
"
"
"
    
Check
the
signature
of
the
give
file
and
returns
what
kind
of
executable
    
matches
.
    
"
"
"
    
if
hasattr
(
path_or_fileobj
"
peek
"
)
:
        
f
=
BytesIO
(
path_or_fileobj
.
peek
(
8
)
)
    
elif
hasattr
(
path_or_fileobj
"
read
"
)
:
        
f
=
path_or_fileobj
    
else
:
        
f
=
open
(
path_or_fileobj
"
rb
"
)
    
signature
=
f
.
read
(
4
)
    
if
len
(
signature
)
<
4
:
        
return
UNKNOWN
    
signature
=
struct
.
unpack
(
"
>
L
"
signature
)
[
0
]
    
if
signature
=
=
ELF_SIGNATURE
:
        
return
ELF
    
if
signature
in
MACHO_SIGNATURES
:
        
return
MACHO
    
if
signature
!
=
FAT_SIGNATURE
:
        
return
UNKNOWN
    
num
=
f
.
read
(
4
)
    
if
len
(
num
)
<
4
:
        
return
UNKNOWN
    
num
=
struct
.
unpack
(
"
>
L
"
num
)
[
0
]
    
if
num
<
20
:
        
return
MACHO
    
return
UNKNOWN
def
is_executable
(
path
)
:
    
"
"
"
    
Return
whether
a
given
file
path
points
to
an
executable
or
a
library
    
where
an
executable
or
library
is
identified
by
:
    
-
the
file
extension
on
OS
/
2
and
WINNT
    
-
the
file
signature
on
OS
/
X
and
ELF
systems
(
GNU
/
Linux
Android
BSD
Solaris
)
    
As
this
function
is
intended
for
use
to
choose
between
the
ExecutableFile
    
and
File
classes
in
FileFinder
and
choosing
ExecutableFile
only
matters
    
on
OS
/
2
OS
/
X
ELF
and
WINNT
(
in
GCC
build
)
systems
we
don
'
t
bother
    
detecting
other
kind
of
executables
.
    
"
"
"
    
from
buildconfig
import
substs
    
if
not
os
.
path
.
exists
(
path
)
:
        
return
False
    
if
substs
[
"
OS_ARCH
"
]
=
=
"
WINNT
"
:
        
return
path
.
lower
(
)
.
endswith
(
(
substs
[
"
DLL_SUFFIX
"
]
substs
[
"
BIN_SUFFIX
"
]
)
)
    
return
get_type
(
path
)
!
=
UNKNOWN
def
may_strip
(
path
)
:
    
"
"
"
    
Return
whether
strip
(
)
should
be
called
    
"
"
"
    
from
buildconfig
import
substs
    
return
bool
(
substs
.
get
(
"
PKG_STRIP
"
)
)
def
strip
(
path
)
:
    
"
"
"
    
Execute
the
STRIP
command
with
STRIP_FLAGS
on
the
given
path
.
    
"
"
"
    
from
buildconfig
import
substs
    
strip
=
substs
[
"
STRIP
"
]
    
flags
=
substs
.
get
(
"
STRIP_FLAGS
"
[
]
)
    
cmd
=
[
strip
]
+
flags
+
[
path
]
    
if
subprocess
.
call
(
cmd
)
!
=
0
:
        
errors
.
fatal
(
"
Error
executing
"
+
"
"
.
join
(
cmd
)
)
    
if
get_type
(
path
)
=
=
MACHO
:
        
with
open
(
path
"
rb
"
)
as
f
:
            
problems
=
macho_linkedit_errors
(
f
)
        
if
problems
:
            
errors
.
fatal
(
                
f
"
{
path
}
has
a
__LINKEDIT
layout
dyld
rejects
after
{
strip
}
:
"
                
+
"
;
"
.
join
(
problems
)
            
)
LINKEDIT_DATA_COMMANDS
=
{
    
0x1D
:
"
code
signature
"
    
0x1E
:
"
split
segment
info
"
    
0x26
:
"
function
starts
"
    
0x29
:
"
data
in
code
"
    
0x80000033
:
"
exports
trie
"
    
0x80000034
:
"
chained
fixups
"
}
def
macho_linkedit_errors
(
f
)
:
    
"
"
"
    
Return
the
__LINKEDIT
layout
problems
dyld
would
report
for
the
thin
64
-
bit
    
Mach
-
O
file
object
f
:
overlapping
contents
contents
past
the
end
of
the
    
segment
and
misalignment
.
This
follows
dyld
'
s
isValidLinkeditLayout
plus
    
pointer
-
size
string
pool
alignment
which
dyld
on
macOS
27
requires
of
    
binaries
built
against
its
SDK
;
it
is
checked
regardless
of
SDK
.
    
"
"
"
    
f
.
seek
(
0
)
    
magic
_
_
_
ncmds
sizeofcmds
=
struct
.
unpack
(
"
<
6L
"
f
.
read
(
24
)
)
    
if
magic
!
=
0xFEEDFACF
:
        
return
[
]
    
f
.
seek
(
32
)
    
cmds
=
f
.
read
(
sizeofcmds
)
    
linkedit
=
None
    
blobs
=
[
]
    
pos
=
0
    
for
_
in
range
(
ncmds
)
:
        
cmd
size
=
struct
.
unpack_from
(
"
<
2L
"
cmds
pos
)
        
if
cmd
=
=
0x19
:
            
name
_
_
fileoff
filesize
=
struct
.
unpack_from
(
"
<
16s4Q
"
cmds
pos
+
8
)
            
if
name
.
rstrip
(
b
"
\
0
"
)
=
=
b
"
__LINKEDIT
"
:
                
linkedit
=
(
fileoff
fileoff
+
filesize
)
        
elif
cmd
=
=
0x2
:
            
symoff
nsyms
stroff
strsize
=
struct
.
unpack_from
(
"
<
4L
"
cmds
pos
+
8
)
            
blobs
+
=
[
                
(
"
symbol
table
"
symoff
nsyms
*
16
8
)
                
(
"
string
pool
"
stroff
strsize
8
)
            
]
        
elif
cmd
=
=
0xB
:
            
d
=
struct
.
unpack_from
(
"
<
18L
"
cmds
pos
+
8
)
            
blobs
+
=
[
                
(
"
indirect
symbol
table
"
d
[
12
]
d
[
13
]
*
4
4
)
                
(
"
external
relocations
"
d
[
14
]
d
[
15
]
*
8
8
)
                
(
"
local
relocations
"
d
[
16
]
d
[
17
]
*
8
8
)
            
]
        
elif
cmd
in
(
0x22
0x80000022
)
:
            
d
=
struct
.
unpack_from
(
"
<
10L
"
cmds
pos
+
8
)
            
names
=
(
                
"
rebase
opcodes
"
                
"
bind
opcodes
"
                
"
weak
bind
opcodes
"
                
"
lazy
bind
opcodes
"
                
"
exports
trie
"
            
)
            
for
i
name
in
enumerate
(
names
)
:
                
blobs
.
append
(
(
name
d
[
2
*
i
]
d
[
2
*
i
+
1
]
8
)
)
        
elif
cmd
in
LINKEDIT_DATA_COMMANDS
:
            
off
datasize
=
struct
.
unpack_from
(
"
<
2L
"
cmds
pos
+
8
)
            
blobs
.
append
(
(
LINKEDIT_DATA_COMMANDS
[
cmd
]
off
datasize
8
)
)
        
pos
+
=
size
    
if
linkedit
is
None
:
        
return
[
]
    
problems
=
[
]
    
prev_end
prev_name
=
linkedit
[
0
]
None
    
for
name
off
size
align
in
sorted
(
        
(
b
for
b
in
blobs
if
b
[
2
]
)
key
=
lambda
b
:
b
[
1
]
    
)
:
        
if
off
<
linkedit
[
0
]
:
            
problems
.
append
(
f
"
{
name
}
starts
before
__LINKEDIT
"
)
        
elif
off
<
prev_end
:
            
problems
.
append
(
f
"
{
name
}
overlaps
{
prev_name
}
"
)
        
if
off
+
size
>
linkedit
[
1
]
:
            
problems
.
append
(
f
"
{
name
}
extends
past
the
end
of
__LINKEDIT
"
)
        
if
off
%
align
:
            
problems
.
append
(
f
"
{
name
}
at
{
off
:
#
x
}
is
not
{
align
}
-
byte
aligned
"
)
        
prev_end
prev_name
=
off
+
size
name
    
return
problems
def
may_elfhack
(
path
)
:
    
"
"
"
    
Return
whether
elfhack
(
)
should
be
called
    
"
"
"
    
from
buildconfig
import
substs
    
return
(
        
"
USE_ELF_HACK
"
in
substs
        
and
substs
[
"
USE_ELF_HACK
"
]
        
and
path
.
endswith
(
substs
[
"
DLL_SUFFIX
"
]
)
        
and
"
COMPILE_ENVIRONMENT
"
in
substs
        
and
substs
[
"
COMPILE_ENVIRONMENT
"
]
    
)
def
elfhack
(
path
)
:
    
"
"
"
    
Execute
the
elfhack
command
on
the
given
path
.
    
"
"
"
    
from
buildconfig
import
topobjdir
    
cmd
=
[
os
.
path
.
join
(
topobjdir
"
build
/
unix
/
elfhack
/
elfhack
"
)
path
]
    
if
subprocess
.
call
(
cmd
)
!
=
0
:
        
errors
.
fatal
(
"
Error
executing
"
+
"
"
.
join
(
cmd
)
)
