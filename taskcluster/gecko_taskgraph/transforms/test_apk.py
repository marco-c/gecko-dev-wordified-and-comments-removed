"
"
"
Apply
some
defaults
and
minor
modifications
to
the
jobs
defined
in
the
test
kinds
.
"
"
"
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
transforms
=
TransformSequence
(
)
transforms
.
add
def
resolve_keys
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
        
for
key
in
(
            
"
routes
"
            
"
scopes
"
            
"
extra
.
notify
"
        
)
:
            
resolve_keyed_by
(
                
task
                
key
                
item_name
=
task
[
"
name
"
]
                
*
*
{
                    
"
level
"
:
config
.
params
[
"
level
"
]
                
}
            
)
        
yield
task
