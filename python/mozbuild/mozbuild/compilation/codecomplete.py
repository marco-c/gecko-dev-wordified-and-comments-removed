from
mach
.
decorators
import
Command
CommandArgument
from
mozshellutil
import
quote
as
shell_quote
from
mozshellutil
import
split
as
shell_split
Command
(
    
"
compileflags
"
    
category
=
"
devenv
"
    
description
=
"
Display
the
compilation
flags
for
a
given
source
file
"
)
CommandArgument
(
    
"
what
"
default
=
None
help
=
"
Source
file
to
display
compilation
flags
for
"
)
def
compileflags
(
command_context
what
)
:
    
from
mozbuild
.
compilation
import
util
    
from
mozbuild
.
util
import
resolve_target_to_make
    
if
not
util
.
check_top_objdir
(
command_context
.
topobjdir
)
:
        
return
1
    
path_arg
=
command_context
.
_wrap_path_argument
(
what
)
    
make_dir
make_target
=
resolve_target_to_make
(
        
command_context
.
topobjdir
path_arg
.
relpath
(
)
    
)
    
if
make_dir
is
None
and
make_target
is
None
:
        
return
1
    
build_vars
=
util
.
get_build_vars
(
make_dir
command_context
)
    
if
what
.
endswith
(
"
.
c
"
)
:
        
cc
=
"
CC
"
        
name
=
"
COMPILE_CFLAGS
"
    
else
:
        
cc
=
"
CXX
"
        
name
=
"
COMPILE_CXXFLAGS
"
    
if
name
not
in
build_vars
:
        
return
    
flags
=
(
shell_split
(
build_vars
[
cc
]
)
+
shell_split
(
build_vars
[
name
]
)
)
[
1
:
]
    
print
(
"
"
.
join
(
shell_quote
(
arg
)
for
arg
in
util
.
sanitize_cflags
(
flags
)
)
)
