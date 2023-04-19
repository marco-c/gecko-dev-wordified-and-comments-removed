from
__future__
import
absolute_import
print_function
import
os
from
mozbuild
.
compilation
.
database
import
CompileDBBackend
import
mozpack
.
path
as
mozpath
class
ClangdBackend
(
CompileDBBackend
)
:
    
"
"
"
    
Configuration
that
generates
the
backend
for
clangd
it
is
used
with
clangd
    
extension
for
vscode
    
"
"
"
    
def
_init
(
self
)
:
        
CompileDBBackend
.
_init
(
self
)
    
def
_get_compiler_args
(
self
cenv
canonical_suffix
)
:
        
compiler_args
=
super
(
ClangdBackend
self
)
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
None
        
if
compiler_args
[
0
]
[
-
6
:
]
=
=
"
ccache
"
:
            
compiler_args
.
pop
(
0
)
        
return
compiler_args
    
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
        
cmd
.
append
(
filename
)
        
return
cmd
    
def
_outputfile_path
(
self
)
:
        
clangd_cc_path
=
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
clangd
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
clangd_cc_path
)
:
            
os
.
mkdir
(
clangd_cc_path
)
        
return
mozpath
.
join
(
clangd_cc_path
"
compile_commands
.
json
"
)
    
def
_process_unified_sources
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
