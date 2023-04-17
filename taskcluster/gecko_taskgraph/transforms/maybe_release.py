from
gecko_taskgraph
.
transforms
.
base
import
TransformSequence
from
gecko_taskgraph
.
util
.
schema
import
resolve_keyed_by
transforms
=
TransformSequence
(
)
transforms
.
add
def
make_task_description
(
config
jobs
)
:
    
for
job
in
jobs
:
        
for
key
in
[
"
worker
-
type
"
"
scopes
"
]
:
            
resolve_keyed_by
(
                
job
                
key
                
item_name
=
job
[
"
name
"
]
                
*
*
{
"
release
-
level
"
:
config
.
params
.
release_level
(
)
}
            
)
        
yield
job
