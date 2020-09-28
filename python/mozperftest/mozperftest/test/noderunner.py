import
os
import
sys
import
mozpack
.
path
as
mozpath
from
mozperftest
.
layers
import
Layer
from
mozperftest
.
utils
import
silence
class
NodeRunner
(
Layer
)
:
    
name
=
"
node
"
    
def
__init__
(
self
env
mach_cmd
)
:
        
super
(
NodeRunner
self
)
.
__init__
(
env
mach_cmd
)
        
self
.
topsrcdir
=
mach_cmd
.
topsrcdir
        
self
.
_mach_context
=
mach_cmd
.
_mach_context
        
self
.
python_path
=
mach_cmd
.
virtualenv_manager
.
python_path
        
from
mozbuild
.
nodeutil
import
find_node_executable
        
self
.
node_path
=
os
.
path
.
abspath
(
find_node_executable
(
)
[
0
]
)
    
def
setup
(
self
)
:
        
"
"
"
Install
the
Node
.
js
package
.
"
"
"
        
self
.
verify_node_install
(
)
    
def
node
(
self
args
)
:
        
"
"
"
Invoke
node
(
interactively
)
with
the
given
arguments
.
"
"
"
        
return
self
.
run_process
(
            
[
self
.
node_path
]
+
args
            
append_env
=
self
.
append_env
(
)
            
pass_thru
=
True
            
ensure_exit_code
=
False
            
cwd
=
mozpath
.
join
(
self
.
topsrcdir
)
        
)
    
def
append_env
(
self
append_path
=
True
)
:
        
path
=
os
.
environ
.
get
(
"
PATH
"
"
"
)
.
split
(
os
.
pathsep
)
if
append_path
else
[
]
        
node_dir
=
os
.
path
.
dirname
(
self
.
node_path
)
        
path
=
[
node_dir
]
+
path
        
return
{
            
"
PATH
"
:
os
.
pathsep
.
join
(
path
)
            
"
PYTHON
"
:
self
.
python_path
        
}
    
def
verify_node_install
(
self
)
:
        
sys
.
path
.
append
(
mozpath
.
join
(
self
.
topsrcdir
"
tools
"
"
lint
"
"
eslint
"
)
)
        
import
setup_helper
        
with
silence
(
)
:
            
node_valid
=
setup_helper
.
check_node_executables_valid
(
)
        
if
not
node_valid
:
            
setup_helper
.
check_node_executables_valid
(
)
            
raise
ValueError
(
"
Can
'
t
find
Node
.
did
you
run
.
/
mach
bootstrap
?
"
)
        
return
True
