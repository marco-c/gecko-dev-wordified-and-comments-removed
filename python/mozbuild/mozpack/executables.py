from
__future__
import
absolute_import
print_function
unicode_literals
import
os
import
struct
import
subprocess
from
mozpack
.
errors
import
errors
MACHO_SIGNATURES
=
[
    
0xfeedface
    
0xcefaedfe
    
0xfeedfacf
    
0xcffaedfe
]
FAT_SIGNATURE
=
0xcafebabe
ELF_SIGNATURE
=
0x7f454c46
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
path
)
:
    
'
'
'
    
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
    
'
'
'
    
with
open
(
path
'
rb
'
)
as
f
:
        
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
'
>
L
'
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
'
>
L
'
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
    
'
'
'
    
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
    
'
'
'
    
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
'
OS_ARCH
'
]
=
=
'
WINNT
'
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
'
DLL_SUFFIX
'
]
                                      
substs
[
'
BIN_SUFFIX
'
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
    
'
'
'
    
Return
whether
strip
(
)
should
be
called
    
'
'
'
    
from
buildconfig
import
substs
    
if
'
d3dcompiler
'
in
path
:
        
return
False
    
return
bool
(
substs
.
get
(
'
PKG_STRIP
'
)
)
def
strip
(
path
)
:
    
'
'
'
    
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
    
'
'
'
    
from
buildconfig
import
substs
    
strip
=
substs
[
'
STRIP
'
]
    
flags
=
substs
.
get
(
'
STRIP_FLAGS
'
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
'
Error
executing
'
+
'
'
.
join
(
cmd
)
)
def
may_elfhack
(
path
)
:
    
'
'
'
    
Return
whether
elfhack
(
)
should
be
called
    
'
'
'
    
from
buildconfig
import
substs
    
return
(
'
USE_ELF_HACK
'
in
substs
and
substs
[
'
USE_ELF_HACK
'
]
and
            
path
.
endswith
(
substs
[
'
DLL_SUFFIX
'
]
)
and
            
'
COMPILE_ENVIRONMENT
'
in
substs
and
substs
[
'
COMPILE_ENVIRONMENT
'
]
)
def
elfhack
(
path
)
:
    
'
'
'
    
Execute
the
elfhack
command
on
the
given
path
.
    
'
'
'
    
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
'
build
/
unix
/
elfhack
/
elfhack
'
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
'
Error
executing
'
+
'
'
.
join
(
cmd
)
)
def
xz_compress
(
path
)
:
    
'
'
'
    
Execute
xz
to
compress
the
given
path
.
    
'
'
'
    
if
open
(
path
'
rb
'
)
.
read
(
5
)
[
1
:
]
=
=
'
7zXZ
'
:
        
print
(
'
%
s
is
already
compressed
'
%
path
)
        
return
    
from
buildconfig
import
substs
    
xz
=
substs
.
get
(
'
XZ
'
)
    
cmd
=
[
xz
'
-
zkf
'
path
]
    
cmd
.
extend
(
[
'
-
-
threads
=
1
'
]
)
    
bcj
=
None
    
if
substs
.
get
(
'
MOZ_THUMB2
'
)
:
        
bcj
=
'
-
-
armthumb
'
    
elif
substs
.
get
(
'
CPU_ARCH
'
)
=
=
'
arm
'
:
        
bcj
=
'
-
-
arm
'
    
elif
substs
.
get
(
'
CPU_ARCH
'
)
=
=
'
x86
'
:
        
bcj
=
'
-
-
x86
'
    
if
bcj
:
        
cmd
.
extend
(
[
bcj
]
)
    
cmd
.
extend
(
[
'
-
-
lzma2
=
dict
=
8MiB
lc
=
3
lp
=
0
pb
=
2
mode
=
normal
nice
=
64
mf
=
bt4
depth
=
0
'
]
)
    
print
(
'
xz
-
compressing
%
s
with
%
s
'
%
(
path
'
'
.
join
(
cmd
)
)
)
    
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
'
Error
executing
'
+
'
'
.
join
(
cmd
)
)
        
return
    
os
.
rename
(
path
+
'
.
xz
'
path
)
