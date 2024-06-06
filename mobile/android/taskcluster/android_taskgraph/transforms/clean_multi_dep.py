from
taskgraph
.
transforms
.
base
import
TransformSequence
from
taskgraph
.
util
.
schema
import
resolve_keyed_by
from
.
.
build_config
import
CHECKSUMS_EXTENSIONS
transforms
=
TransformSequence
(
)
transforms
.
add
def
remove_dependent_tasks
(
config
tasks
)
:
    
for
task
in
tasks
:
        
try
:
            
del
task
[
"
dependent
-
tasks
"
]
        
except
KeyError
:
            
pass
        
yield
task
