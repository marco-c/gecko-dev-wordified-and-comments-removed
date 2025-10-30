import
logging
import
requests
from
taskgraph
.
util
.
taskcluster
import
cancel_task
from
.
registry
import
register_callback_action
logger
=
logging
.
getLogger
(
__name__
)
register_callback_action
(
    
title
=
"
Cancel
Task
"
    
name
=
"
cancel
"
    
symbol
=
"
cx
"
    
description
=
(
"
Cancel
the
given
task
"
)
    
order
=
350
    
context
=
[
{
}
]
)
def
cancel_action
(
parameters
graph_config
input
task_group_id
task_id
)
:
    
try
:
    
except
requests
.
HTTPError
as
e
:
        
if
e
.
response
.
status_code
=
=
409
:
        
cancel_task
(
task_id
)
            
logger
.
info
(
f
"
Task
{
task_id
}
is
past
its
deadline
and
cannot
be
cancelled
.
"
)
            
return
        
raise
