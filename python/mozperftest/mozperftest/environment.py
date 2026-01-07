import
contextlib
import
copy
from
mozperftest
.
argparser
import
FLAVORS
from
mozperftest
.
hooks
import
Hooks
from
mozperftest
.
layers
import
Layers
StopRunError
from
mozperftest
.
metrics
import
pick_metrics
from
mozperftest
.
system
import
pick_system
from
mozperftest
.
test
import
pick_test
from
mozperftest
.
utils
import
MachLogger
SYSTEM
TEST
METRICS
=
0
1
2
class
MachEnvironment
(
MachLogger
)
:
    
def
__init__
(
self
mach_cmd
flavor
=
"
desktop
-
browser
"
hooks
=
None
*
*
kwargs
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
_mach_args
=
dict
(
            
[
(
self
.
_normalize
(
key
)
value
)
for
key
value
in
kwargs
.
items
(
)
]
        
)
        
self
.
layers
=
[
]
        
if
flavor
not
in
FLAVORS
:
            
raise
NotImplementedError
(
flavor
)
        
for
layer
in
(
pick_system
pick_test
pick_metrics
)
:
            
self
.
add_layer
(
layer
(
self
flavor
mach_cmd
)
)
        
if
hooks
is
None
:
            
hooks
=
Hooks
(
mach_cmd
)
        
self
.
hooks
=
hooks
    
contextlib
.
contextmanager
    
def
frozen
(
self
)
:
        
self
.
freeze
(
)
        
try
:
            
with
self
:
                
yield
self
        
finally
:
            
self
.
unfreeze
(
)
    
def
_normalize
(
self
name
)
:
        
if
name
.
startswith
(
"
-
-
"
)
:
            
name
=
name
[
2
:
]
        
return
name
.
replace
(
"
-
"
"
_
"
)
    
def
set_arg
(
self
name
value
)
:
        
"
"
"
Sets
the
argument
"
"
"
        
self
.
_mach_args
[
self
.
_normalize
(
name
)
]
=
value
    
def
get_arg
(
self
name
default
=
None
layer
=
None
)
:
        
name
=
self
.
_normalize
(
name
)
        
marker
=
object
(
)
        
res
=
self
.
_mach_args
.
get
(
name
marker
)
        
if
res
is
marker
:
            
if
layer
is
not
None
and
not
name
.
startswith
(
layer
.
name
)
:
                
name
=
"
%
s_
%
s
"
%
(
layer
.
name
name
)
                
return
self
.
_mach_args
.
get
(
name
default
)
            
return
default
        
return
res
    
def
get_layer
(
self
name
)
:
        
for
layer
in
self
.
layers
:
            
if
isinstance
(
layer
Layers
)
:
                
found
=
layer
.
get_layer
(
name
)
                
if
found
is
not
None
:
                    
return
found
            
elif
layer
.
name
=
=
name
:
                
return
layer
        
return
None
    
def
add_layer
(
self
layer
)
:
        
self
.
layers
.
append
(
layer
)
    
def
freeze
(
self
)
:
        
self
.
_saved_mach_args
=
copy
.
deepcopy
(
self
.
_mach_args
)
    
def
unfreeze
(
self
)
:
        
self
.
_mach_args
=
self
.
_saved_mach_args
        
self
.
_saved_mach_args
=
None
    
def
run
(
self
metadata
)
:
        
try
:
            
with
self
.
layers
[
SYSTEM
]
as
syslayer
self
.
layers
[
TEST
]
as
testlayer
:
                
metadata
=
testlayer
(
syslayer
(
metadata
)
)
            
with
self
.
layers
[
METRICS
]
as
metrics
:
                
metadata
=
metrics
(
metadata
)
        
except
StopRunError
:
            
pass
        
return
metadata
    
def
__enter__
(
self
)
:
        
return
self
    
def
__exit__
(
self
type
value
traceback
)
:
        
return
