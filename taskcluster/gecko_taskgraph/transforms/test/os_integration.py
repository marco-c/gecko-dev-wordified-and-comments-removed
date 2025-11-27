from
taskgraph
.
transforms
.
base
import
TransformSequence
transforms
=
TransformSequence
(
)
transforms
.
add
def
maybe_setup_os_integration
(
config
tasks
)
:
    
if
(
        
config
.
params
[
"
tasks_for
"
]
!
=
"
cron
"
        
or
config
.
params
[
"
target_tasks_method
"
]
!
=
"
os
-
integration
"
    
)
:
        
yield
from
tasks
        
return
    
for
task
in
tasks
:
        
if
task
[
"
suite
"
]
in
(
"
raptor
"
"
talos
"
"
marionette
-
unittest
"
)
:
            
yield
task
            
continue
        
if
(
            
task
.
get
(
"
test
-
manifest
-
loader
"
True
)
is
not
None
            
and
isinstance
(
task
[
"
chunks
"
]
int
)
            
and
task
[
"
chunks
"
]
>
1
        
)
:
            
task
[
"
chunks
"
]
=
"
dynamic
"
        
env
=
task
.
setdefault
(
"
worker
"
{
}
)
.
setdefault
(
"
env
"
{
}
)
        
env
[
"
MOZHARNESS_TEST_TAG
"
]
=
[
"
os_integration
"
]
        
yield
task
