import
logging
import
requests
from
taskcluster
import
TaskclusterRestFailure
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
        
cancel_task
(
task_id
)
    
except
(
requests
.
HTTPError
TaskclusterRestFailure
)
as
e
:
        
status_code
=
None
        
if
isinstance
(
e
requests
.
HTTPError
)
:
            
status_code
=
e
.
response
.
status_code
if
e
.
response
else
None
        
elif
isinstance
(
e
TaskclusterRestFailure
)
:
            
status_code
=
e
.
status_code
        
if
status_code
=
=
409
:
            
logger
.
info
(
                
f
'
Task
"
{
task_id
}
"
is
past
its
deadline
and
cannot
be
cancelled
.
'
            
)
            
return
        
raise
