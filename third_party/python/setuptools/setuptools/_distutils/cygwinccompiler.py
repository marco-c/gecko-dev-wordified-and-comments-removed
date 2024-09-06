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
copy
import
os
import
pathlib
import
shlex
import
sys
import
warnings
from
subprocess
import
check_output
from
.
errors
import
(
    
CCompilerError
    
CompileError
    
DistutilsExecError
    
DistutilsPlatformError
)
from
.
file_util
import
write_file
from
.
unixccompiler
import
UnixCCompiler
from
.
version
import
LooseVersion
suppress_known_deprecation
def
get_msvcr
(
)
:
    
"
"
"
No
longer
needed
but
kept
for
backward
compatibility
.
"
"
"
    
return
[
]
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
False
dry_run
=
False
force
=
False
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
f
"
Python
'
s
GCC
status
:
{
status
}
(
details
:
{
details
}
)
"
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
                
f
"
Reason
:
{
details
}
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
        
self
.
linker_dll_cxx
=
self
.
cxx
        
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
f
'
{
self
.
cc
}
-
mcygwin
-
O
-
Wall
'
            
compiler_so
=
f
'
{
self
.
cc
}
-
mcygwin
-
mdll
-
O
-
Wall
'
            
compiler_cxx
=
f
'
{
self
.
cxx
}
-
mcygwin
-
O
-
Wall
'
            
compiler_so_cxx
=
f
'
{
self
.
cxx
}
-
mcygwin
-
mdll
-
O
-
Wall
'
            
linker_exe
=
f
'
{
self
.
cc
}
-
mcygwin
'
            
linker_so
=
f
'
{
self
.
linker_dll
}
-
mcygwin
{
shared_option
}
'
            
linker_exe_cxx
=
f
'
{
self
.
cxx
}
-
mcygwin
'
            
linker_so_cxx
=
f
'
{
self
.
linker_dll_cxx
}
-
mcygwin
{
shared_option
}
'
        
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
                
if
self
.
detect_language
(
src
)
=
=
'
c
+
+
'
:
                    
self
.
spawn
(
                        
self
.
compiler_so_cxx
                        
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
                
else
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
False
        
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
f
"
LIBRARY
{
os
.
path
.
basename
(
output_filename
)
}
"
"
EXPORTS
"
]
            
contents
.
extend
(
export_symbols
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
f
"
writing
{
def_file
}
"
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
False
dry_run
=
False
force
=
False
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
f
'
{
self
.
cc
}
-
O
-
Wall
'
            
compiler_so
=
f
'
{
self
.
cc
}
-
shared
-
O
-
Wall
'
            
compiler_so_cxx
=
f
'
{
self
.
cxx
}
-
shared
-
O
-
Wall
'
            
compiler_cxx
=
f
'
{
self
.
cxx
}
-
O
-
Wall
'
            
linker_exe
=
f
'
{
self
.
cc
}
'
            
linker_so
=
f
'
{
self
.
linker_dll
}
{
shared_option
}
'
            
linker_exe_cxx
=
f
'
{
self
.
cxx
}
'
            
linker_so_cxx
=
f
'
{
self
.
linker_dll_cxx
}
{
shared_option
}
'
        
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
pathlib
.
Path
(
fn
)
.
read_text
(
encoding
=
'
utf
-
8
'
)
    
except
OSError
as
exc
:
        
return
(
CONFIG_H_UNCERTAIN
f
"
couldn
'
t
read
'
{
fn
}
'
:
{
exc
.
strerror
}
"
)
    
else
:
        
substring
=
'
__GNUC__
'
        
if
substring
in
config_h
:
            
code
=
CONFIG_H_OK
            
mention_inflected
=
'
mentions
'
        
else
:
            
code
=
CONFIG_H_NOTOK
            
mention_inflected
=
'
does
not
mention
'
        
return
code
f
"
{
fn
!
r
}
{
mention_inflected
}
{
substring
!
r
}
"
def
is_cygwincc
(
cc
)
:
    
"
"
"
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
"
"
"
    
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
