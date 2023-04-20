from
__future__
import
absolute_import
print_function
import
os
import
mozpack
.
path
as
mozpath
from
mozbuild
.
compilation
.
database
import
CompileDBBackend
class
StaticAnalysisBackend
(
CompileDBBackend
)
:
    
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
        
self
.
non_unified_build
=
[
]
        
with
open
(
            
mozpath
.
join
(
self
.
environment
.
topsrcdir
"
build
"
"
non
-
unified
-
compat
"
)
        
)
as
fh
:
            
content
=
fh
.
readlines
(
)
            
self
.
non_unified_build
=
[
                
mozpath
.
join
(
self
.
environment
.
topsrcdir
line
.
strip
(
)
)
                
for
line
in
content
            
]
    
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
or
any
(
            
filename
.
startswith
(
path
)
for
path
in
self
.
non_unified_build
        
)
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
_outputfile_path
(
self
)
:
        
database_path
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
static
-
analysis
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
database_path
)
:
            
os
.
mkdir
(
database_path
)
        
return
mozpath
.
join
(
database_path
"
compile_commands
.
json
"
)
