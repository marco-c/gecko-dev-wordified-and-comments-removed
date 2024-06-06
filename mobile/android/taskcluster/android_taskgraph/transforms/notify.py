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
notifications
.
message
"
"
notifications
.
emails
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
                    
'
level
'
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
