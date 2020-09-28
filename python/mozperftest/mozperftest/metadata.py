from
collections
import
defaultdict
from
mozperftest
.
utils
import
MachLogger
class
Metadata
(
MachLogger
)
:
    
def
__init__
(
self
mach_cmd
env
flavor
script
)
:
        
MachLogger
.
__init__
(
self
mach_cmd
)
        
self
.
_mach_cmd
=
mach_cmd
        
self
.
flavor
=
flavor
        
self
.
options
=
defaultdict
(
dict
)
        
self
.
_results
=
[
]
        
self
.
_output
=
None
        
self
.
_env
=
env
        
self
.
script
=
script
    
def
run_hook
(
self
name
*
*
kw
)
:
        
return
self
.
_env
.
hooks
.
run
(
name
*
*
kw
)
    
def
set_output
(
self
output
)
:
        
self
.
_output
=
output
    
def
get_output
(
self
)
:
        
return
self
.
_output
    
def
add_result
(
self
result
)
:
        
self
.
_results
.
append
(
result
)
    
def
get_results
(
self
)
:
        
return
self
.
_results
    
def
clear_results
(
self
)
:
        
self
.
_results
=
[
]
    
def
update_options
(
self
name
options
)
:
        
self
.
options
[
name
]
.
update
(
options
)
    
def
get_options
(
self
name
)
:
        
return
self
.
options
[
name
]
