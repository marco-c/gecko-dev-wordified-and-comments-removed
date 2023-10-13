"
"
"
distutils
.
cygwinccompiler
Provides
the
CygwinCCompiler
class
a
subclass
of
UnixCCompiler
that
handles
the
Cygwin
port
of
the
GNU
C
compiler
to
Windows
.
It
also
contains
the
Mingw32CCompiler
class
which
handles
the
mingw32
port
of
GCC
(
same
as
cygwin
in
no
-
cygwin
mode
)
.
"
"
"
import
os
import
re
import
sys
import
copy
import
shlex
import
warnings
from
subprocess
import
check_output
from
.
unixccompiler
import
UnixCCompiler
from
.
file_util
import
write_file
from
.
errors
import
(
    
DistutilsExecError
    
DistutilsPlatformError
    
CCompilerError
    
CompileError
)
from
.
version
import
LooseVersion
suppress_known_deprecation
from
.
_collections
import
RangeMap
_msvcr_lookup
=
RangeMap
.
left
(
    
{
        
1300
:
[
'
msvcr70
'
]
        
1310
:
[
'
msvcr71
'
]
        
1400
:
[
'
msvcr80
'
]
        
1500
:
[
'
msvcr90
'
]
        
1600
:
[
'
msvcr100
'
]
        
1700
:
[
'
msvcr110
'
]
        
1800
:
[
'
msvcr120
'
]
        
1900
:
[
'
vcruntime140
'
]
        
2000
:
RangeMap
.
undefined_value
    
}
)
def
get_msvcr
(
)
:
    
"
"
"
Include
the
appropriate
MSVC
runtime
library
if
Python
was
built
    
with
MSVC
7
.
0
or
later
.
    
"
"
"
    
match
=
re
.
search
(
r
'
MSC
v
\
.
(
\
d
{
4
}
)
'
sys
.
version
)
    
try
:
        
msc_ver
=
int
(
match
.
group
(
1
)
)
    
except
AttributeError
:
        
return
    
try
:
        
return
_msvcr_lookup
[
msc_ver
]
    
except
KeyError
:
        
raise
ValueError
(
"
Unknown
MS
Compiler
version
%
s
"
%
msc_ver
)
_runtime_library_dirs_msg
=
(
    
"
Unable
to
set
runtime
library
search
path
on
Windows
"
    
"
usually
indicated
by
runtime_library_dirs
parameter
to
Extension
"
)
class
CygwinCCompiler
(
UnixCCompiler
)
:
    
"
"
"
Handles
the
Cygwin
port
of
the
GNU
C
compiler
to
Windows
.
"
"
"
    
compiler_type
=
'
cygwin
'
    
obj_extension
=
"
.
o
"
    
static_lib_extension
=
"
.
a
"
    
shared_lib_extension
=
"
.
dll
.
a
"
    
dylib_lib_extension
=
"
.
dll
"
    
static_lib_format
=
"
lib
%
s
%
s
"
    
shared_lib_format
=
"
lib
%
s
%
s
"
    
dylib_lib_format
=
"
cyg
%
s
%
s
"
    
exe_extension
=
"
.
exe
"
    
def
__init__
(
self
verbose
=
0
dry_run
=
0
force
=
0
)
:
        
super
(
)
.
__init__
(
verbose
dry_run
force
)
        
status
details
=
check_config_h
(
)
        
self
.
debug_print
(
            
"
Python
'
s
GCC
status
:
{
}
(
details
:
{
}
)
"
.
format
(
status
details
)
        
)
        
if
status
is
not
CONFIG_H_OK
:
            
self
.
warn
(
                
"
Python
'
s
pyconfig
.
h
doesn
'
t
seem
to
support
your
compiler
.
"
                
"
Reason
:
%
s
.
"
                
"
Compiling
may
fail
because
of
undefined
preprocessor
macros
.
"
%
details
            
)
        
self
.
cc
=
os
.
environ
.
get
(
'
CC
'
'
gcc
'
)
        
self
.
cxx
=
os
.
environ
.
get
(
'
CXX
'
'
g
+
+
'
)
        
self
.
linker_dll
=
self
.
cc
        
shared_option
=
"
-
shared
"
        
self
.
set_executables
(
            
compiler
=
'
%
s
-
mcygwin
-
O
-
Wall
'
%
self
.
cc
            
compiler_so
=
'
%
s
-
mcygwin
-
mdll
-
O
-
Wall
'
%
self
.
cc
            
compiler_cxx
=
'
%
s
-
mcygwin
-
O
-
Wall
'
%
self
.
cxx
            
linker_exe
=
'
%
s
-
mcygwin
'
%
self
.
cc
            
linker_so
=
(
'
{
}
-
mcygwin
{
}
'
.
format
(
self
.
linker_dll
shared_option
)
)
        
)
        
self
.
dll_libraries
=
get_msvcr
(
)
    
property
    
def
gcc_version
(
self
)
:
        
warnings
.
warn
(
            
"
gcc_version
attribute
of
CygwinCCompiler
is
deprecated
.
"
            
"
Instead
of
returning
actual
gcc
version
a
fixed
value
11
.
2
.
0
is
returned
.
"
            
DeprecationWarning
            
stacklevel
=
2
        
)
        
with
suppress_known_deprecation
(
)
:
            
return
LooseVersion
(
"
11
.
2
.
0
"
)
    
def
_compile
(
self
obj
src
ext
cc_args
extra_postargs
pp_opts
)
:
        
"
"
"
Compiles
the
source
by
spawning
GCC
and
windres
if
needed
.
"
"
"
        
if
ext
in
(
'
.
rc
'
'
.
res
'
)
:
            
try
:
                
self
.
spawn
(
[
"
windres
"
"
-
i
"
src
"
-
o
"
obj
]
)
            
except
DistutilsExecError
as
msg
:
                
raise
CompileError
(
msg
)
        
else
:
            
try
:
                
self
.
spawn
(
                    
self
.
compiler_so
+
cc_args
+
[
src
'
-
o
'
obj
]
+
extra_postargs
                
)
            
except
DistutilsExecError
as
msg
:
                
raise
CompileError
(
msg
)
    
def
link
(
        
self
        
target_desc
        
objects
        
output_filename
        
output_dir
=
None
        
libraries
=
None
        
library_dirs
=
None
        
runtime_library_dirs
=
None
        
export_symbols
=
None
        
debug
=
0
        
extra_preargs
=
None
        
extra_postargs
=
None
        
build_temp
=
None
        
target_lang
=
None
    
)
:
        
"
"
"
Link
the
objects
.
"
"
"
        
extra_preargs
=
copy
.
copy
(
extra_preargs
or
[
]
)
        
libraries
=
copy
.
copy
(
libraries
or
[
]
)
        
objects
=
copy
.
copy
(
objects
or
[
]
)
        
if
runtime_library_dirs
:
            
self
.
warn
(
_runtime_library_dirs_msg
)
        
libraries
.
extend
(
self
.
dll_libraries
)
        
if
(
export_symbols
is
not
None
)
and
(
            
target_desc
!
=
self
.
EXECUTABLE
or
self
.
linker_dll
=
=
"
gcc
"
        
)
:
            
temp_dir
=
os
.
path
.
dirname
(
objects
[
0
]
)
            
(
dll_name
dll_extension
)
=
os
.
path
.
splitext
(
                
os
.
path
.
basename
(
output_filename
)
            
)
            
def_file
=
os
.
path
.
join
(
temp_dir
dll_name
+
"
.
def
"
)
            
contents
=
[
"
LIBRARY
%
s
"
%
os
.
path
.
basename
(
output_filename
)
"
EXPORTS
"
]
            
for
sym
in
export_symbols
:
                
contents
.
append
(
sym
)
            
self
.
execute
(
write_file
(
def_file
contents
)
"
writing
%
s
"
%
def_file
)
            
objects
.
append
(
def_file
)
        
if
not
debug
:
            
extra_preargs
.
append
(
"
-
s
"
)
        
UnixCCompiler
.
link
(
            
self
            
target_desc
            
objects
            
output_filename
            
output_dir
            
libraries
            
library_dirs
            
runtime_library_dirs
            
None
            
debug
            
extra_preargs
            
extra_postargs
            
build_temp
            
target_lang
        
)
    
def
runtime_library_dir_option
(
self
dir
)
:
        
self
.
warn
(
_runtime_library_dirs_msg
)
        
return
[
]
    
def
_make_out_path
(
self
output_dir
strip_dir
src_name
)
:
        
norm_src_name
=
os
.
path
.
normcase
(
src_name
)
        
return
super
(
)
.
_make_out_path
(
output_dir
strip_dir
norm_src_name
)
    
property
    
def
out_extensions
(
self
)
:
        
"
"
"
        
Add
support
for
rc
and
res
files
.
        
"
"
"
        
return
{
            
*
*
super
(
)
.
out_extensions
            
*
*
{
ext
:
ext
+
self
.
obj_extension
for
ext
in
(
'
.
res
'
'
.
rc
'
)
}
        
}
class
Mingw32CCompiler
(
CygwinCCompiler
)
:
    
"
"
"
Handles
the
Mingw32
port
of
the
GNU
C
compiler
to
Windows
.
"
"
"
    
compiler_type
=
'
mingw32
'
    
def
__init__
(
self
verbose
=
0
dry_run
=
0
force
=
0
)
:
        
super
(
)
.
__init__
(
verbose
dry_run
force
)
        
shared_option
=
"
-
shared
"
        
if
is_cygwincc
(
self
.
cc
)
:
            
raise
CCompilerError
(
'
Cygwin
gcc
cannot
be
used
with
-
-
compiler
=
mingw32
'
)
        
self
.
set_executables
(
            
compiler
=
'
%
s
-
O
-
Wall
'
%
self
.
cc
            
compiler_so
=
'
%
s
-
mdll
-
O
-
Wall
'
%
self
.
cc
            
compiler_cxx
=
'
%
s
-
O
-
Wall
'
%
self
.
cxx
            
linker_exe
=
'
%
s
'
%
self
.
cc
            
linker_so
=
'
{
}
{
}
'
.
format
(
self
.
linker_dll
shared_option
)
        
)
    
def
runtime_library_dir_option
(
self
dir
)
:
        
raise
DistutilsPlatformError
(
_runtime_library_dirs_msg
)
CONFIG_H_OK
=
"
ok
"
CONFIG_H_NOTOK
=
"
not
ok
"
CONFIG_H_UNCERTAIN
=
"
uncertain
"
def
check_config_h
(
)
:
    
"
"
"
Check
if
the
current
Python
installation
appears
amenable
to
building
    
extensions
with
GCC
.
    
Returns
a
tuple
(
status
details
)
where
'
status
'
is
one
of
the
following
    
constants
:
    
-
CONFIG_H_OK
:
all
is
well
go
ahead
and
compile
    
-
CONFIG_H_NOTOK
:
doesn
'
t
look
good
    
-
CONFIG_H_UNCERTAIN
:
not
sure
-
-
unable
to
read
pyconfig
.
h
    
'
details
'
is
a
human
-
readable
string
explaining
the
situation
.
    
Note
there
are
two
ways
to
conclude
"
OK
"
:
either
'
sys
.
version
'
contains
    
the
string
"
GCC
"
(
implying
that
this
Python
was
built
with
GCC
)
or
the
    
installed
"
pyconfig
.
h
"
contains
the
string
"
__GNUC__
"
.
    
"
"
"
    
from
distutils
import
sysconfig
    
if
"
GCC
"
in
sys
.
version
:
        
return
CONFIG_H_OK
"
sys
.
version
mentions
'
GCC
'
"
    
if
"
Clang
"
in
sys
.
version
:
        
return
CONFIG_H_OK
"
sys
.
version
mentions
'
Clang
'
"
    
fn
=
sysconfig
.
get_config_h_filename
(
)
    
try
:
        
config_h
=
open
(
fn
)
        
try
:
            
if
"
__GNUC__
"
in
config_h
.
read
(
)
:
                
return
CONFIG_H_OK
"
'
%
s
'
mentions
'
__GNUC__
'
"
%
fn
            
else
:
                
return
CONFIG_H_NOTOK
"
'
%
s
'
does
not
mention
'
__GNUC__
'
"
%
fn
        
finally
:
            
config_h
.
close
(
)
    
except
OSError
as
exc
:
        
return
(
CONFIG_H_UNCERTAIN
"
couldn
'
t
read
'
{
}
'
:
{
}
"
.
format
(
fn
exc
.
strerror
)
)
def
is_cygwincc
(
cc
)
:
    
'
'
'
Try
to
determine
if
the
compiler
that
would
be
used
is
from
cygwin
.
'
'
'
    
out_string
=
check_output
(
shlex
.
split
(
cc
)
+
[
'
-
dumpmachine
'
]
)
    
return
out_string
.
strip
(
)
.
endswith
(
b
'
cygwin
'
)
get_versions
=
None
"
"
"
A
stand
-
in
for
the
previous
get_versions
(
)
function
to
prevent
failures
when
monkeypatched
.
See
pypa
/
setuptools
#
2969
.
"
"
"
