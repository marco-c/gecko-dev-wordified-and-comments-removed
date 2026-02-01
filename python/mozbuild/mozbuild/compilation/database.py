import
os
from
collections
import
OrderedDict
defaultdict
import
mozpack
.
path
as
mozpath
from
mozshellutil
import
quote
as
shell_quote
from
mozbuild
.
backend
.
common
import
CommonBackend
from
mozbuild
.
frontend
.
data
import
(
    
ComputedFlags
    
DirectoryTraversal
    
PerSourceFlag
    
Sources
    
VariablePassthru
)
from
mozbuild
.
util
import
expand_variables
class
CompileDBBackend
(
CommonBackend
)
:
    
def
_init
(
self
)
:
        
CommonBackend
.
_init
(
self
)
        
self
.
_db
=
OrderedDict
(
)
        
self
.
_flags
=
{
}
        
self
.
_envs
=
{
}
        
self
.
_local_flags
=
defaultdict
(
dict
)
        
self
.
_per_source_flags
=
defaultdict
(
list
)
    
def
_build_cmd
(
self
cmd
filename
unified
)
:
        
cmd
=
list
(
cmd
)
        
if
unified
is
None
:
            
cmd
.
append
(
filename
)
        
else
:
            
cmd
.
append
(
unified
)
        
return
cmd
    
def
consume_object
(
self
obj
)
:
        
if
obj
.
relsrcdir
in
(
            
"
build
/
unix
/
elfhack
"
            
"
build
/
unix
/
elfhack
/
inject
"
            
"
build
/
clang
-
plugin
"
            
"
build
/
clang
-
plugin
/
tests
"
        
)
:
            
return
True
        
consumed
=
CommonBackend
.
consume_object
(
self
obj
)
        
if
consumed
:
            
return
True
        
if
isinstance
(
obj
DirectoryTraversal
)
:
            
self
.
_envs
[
obj
.
objdir
]
=
obj
.
config
        
elif
isinstance
(
obj
Sources
)
:
            
for
f
in
obj
.
files
:
                
self
.
_build_db_line
(
                    
obj
.
objdir
obj
.
relsrcdir
obj
.
config
f
obj
.
canonical_suffix
                
)
        
elif
isinstance
(
obj
VariablePassthru
)
:
            
for
var
in
(
"
MOZBUILD_CMFLAGS
"
"
MOZBUILD_CMMFLAGS
"
)
:
                
if
var
in
obj
.
variables
:
                    
self
.
_local_flags
[
obj
.
objdir
]
[
var
]
=
obj
.
variables
[
var
]
        
elif
isinstance
(
obj
PerSourceFlag
)
:
            
self
.
_per_source_flags
[
obj
.
file_name
]
.
extend
(
obj
.
flags
)
        
elif
isinstance
(
obj
ComputedFlags
)
:
            
for
var
flags
in
obj
.
get_flags
(
)
:
                
self
.
_local_flags
[
obj
.
objdir
]
[
"
COMPUTED_
%
s
"
%
var
]
=
flags
        
return
True
    
def
consume_finished
(
self
)
:
        
CommonBackend
.
consume_finished
(
self
)
        
db
=
[
]
        
for
(
directory
filename
unified
)
cmd
in
self
.
_db
.
items
(
)
:
            
env
=
self
.
_envs
[
directory
]
            
cmd
=
self
.
_build_cmd
(
cmd
filename
unified
)
            
variables
=
{
                
"
DIST
"
:
mozpath
.
join
(
env
.
topobjdir
"
dist
"
)
                
"
DEPTH
"
:
env
.
topobjdir
                
"
MOZILLA_DIR
"
:
env
.
topsrcdir
                
"
topsrcdir
"
:
env
.
topsrcdir
                
"
topobjdir
"
:
env
.
topobjdir
            
}
            
variables
.
update
(
self
.
_local_flags
[
directory
]
)
            
c
=
[
]
            
for
a
in
cmd
:
                
accum
=
"
"
                
for
word
in
expand_variables
(
a
variables
)
.
split
(
)
:
                    
has_quote
=
bool
(
word
.
count
(
'
"
'
)
%
2
)
                    
if
accum
and
has_quote
:
                        
c
.
append
(
accum
+
"
"
+
word
)
                        
accum
=
"
"
                    
elif
accum
and
not
has_quote
:
                        
accum
+
=
"
"
+
word
                    
elif
not
accum
and
has_quote
:
                        
accum
=
word
                    
else
:
                        
c
.
append
(
word
)
            
c
.
insert
(
-
1
"
-
ferror
-
limit
=
0
"
)
            
per_source_flags
=
self
.
_per_source_flags
.
get
(
filename
)
            
if
per_source_flags
is
not
None
:
                
c
.
extend
(
per_source_flags
)
            
db
.
append
(
{
                
"
directory
"
:
directory
                
"
command
"
:
shell_quote
(
*
c
)
                
"
file
"
:
mozpath
.
join
(
directory
filename
)
            
}
)
        
import
json
        
outputfile
=
self
.
_outputfile_path
(
)
        
with
self
.
_write_file
(
outputfile
)
as
jsonout
:
            
json
.
dump
(
db
jsonout
indent
=
0
)
    
def
_outputfile_path
(
self
)
:
        
return
os
.
path
.
join
(
self
.
environment
.
topobjdir
"
compile_commands
.
json
"
)
    
def
_process_unified_sources_without_mapping
(
self
obj
)
:
        
for
f
in
list
(
sorted
(
obj
.
files
)
)
:
            
self
.
_build_db_line
(
                
obj
.
objdir
obj
.
relsrcdir
obj
.
config
f
obj
.
canonical_suffix
            
)
    
def
_process_unified_sources
(
self
obj
)
:
        
if
not
obj
.
have_unified_mapping
:
            
return
self
.
_process_unified_sources_without_mapping
(
obj
)
        
for
f
in
obj
.
unified_source_mapping
:
            
self
.
_build_db_line
(
                
obj
.
objdir
obj
.
relsrcdir
obj
.
config
f
[
0
]
obj
.
canonical_suffix
            
)
            
for
entry
in
f
[
1
]
:
                
self
.
_build_db_line
(
                    
obj
.
objdir
                    
obj
.
relsrcdir
                    
obj
.
config
                    
entry
                    
obj
.
canonical_suffix
                    
unified
=
f
[
0
]
                
)
    
def
_handle_idl_manager
(
self
idl_manager
)
:
        
pass
    
def
_handle_ipdl_sources
(
        
self
        
ipdl_dir
        
sorted_ipdl_sources
        
sorted_nonstatic_ipdl_sources
        
sorted_static_ipdl_sources
    
)
:
        
pass
    
def
_handle_webidl_build
(
        
self
        
bindings_dir
        
unified_source_mapping
        
webidls
        
expected_build_output_files
        
global_define_files
    
)
:
        
for
f
in
unified_source_mapping
:
            
self
.
_build_db_line
(
bindings_dir
None
self
.
environment
f
[
0
]
"
.
cpp
"
)
    
COMPILERS
=
{
        
"
.
c
"
:
"
CC
"
        
"
.
cpp
"
:
"
CXX
"
        
"
.
m
"
:
"
CC
"
        
"
.
mm
"
:
"
CXX
"
    
}
    
CFLAGS
=
{
        
"
.
c
"
:
"
CFLAGS
"
        
"
.
cpp
"
:
"
CXXFLAGS
"
        
"
.
m
"
:
"
CFLAGS
"
        
"
.
mm
"
:
"
CXXFLAGS
"
    
}
    
def
_get_compiler_args
(
self
cenv
canonical_suffix
)
:
        
if
canonical_suffix
not
in
self
.
COMPILERS
:
            
return
None
        
return
cenv
.
substs
[
self
.
COMPILERS
[
canonical_suffix
]
]
.
split
(
)
    
def
_build_db_line
(
        
self
objdir
reldir
cenv
filename
canonical_suffix
unified
=
None
    
)
:
        
compiler_args
=
self
.
_get_compiler_args
(
cenv
canonical_suffix
)
        
if
compiler_args
is
None
:
            
return
        
db
=
self
.
_db
.
setdefault
(
            
(
objdir
filename
unified
)
            
compiler_args
+
[
"
-
o
"
"
/
dev
/
null
"
"
-
c
"
]
        
)
        
reldir
=
reldir
or
mozpath
.
relpath
(
objdir
cenv
.
topobjdir
)
        
def
append_var
(
name
)
:
            
value
=
cenv
.
substs
.
get
(
name
)
            
if
not
value
:
                
return
            
if
isinstance
(
value
str
)
:
                
value
=
value
.
split
(
)
            
db
.
extend
(
value
)
        
db
.
append
(
"
(
COMPUTED_
%
s
)
"
%
self
.
CFLAGS
[
canonical_suffix
]
)
        
if
canonical_suffix
=
=
"
.
m
"
:
            
append_var
(
"
OS_COMPILE_CMFLAGS
"
)
            
db
.
append
(
"
(
MOZBUILD_CMFLAGS
)
"
)
        
elif
canonical_suffix
=
=
"
.
mm
"
:
            
append_var
(
"
OS_COMPILE_CMMFLAGS
"
)
            
db
.
append
(
"
(
MOZBUILD_CMMFLAGS
)
"
)
