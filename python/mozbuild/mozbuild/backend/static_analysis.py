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
from
.
.
frontend
.
data
import
Headers
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
consume_object
(
self
obj
)
:
        
if
isinstance
(
obj
Headers
)
:
            
self
.
_process_headers
(
obj
)
        
else
:
            
super
(
)
.
consume_object
(
obj
)
        
return
True
    
def
_process_headers
(
self
obj
)
:
        
for
f
in
obj
.
static_files
:
            
db_line
=
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
            
db_line
.
append
(
"
-
xc
+
+
"
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
