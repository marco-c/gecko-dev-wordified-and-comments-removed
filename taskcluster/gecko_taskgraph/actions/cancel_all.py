import
logging
import
os
from
concurrent
import
futures
from
taskcluster
.
exceptions
import
TaskclusterRestFailure
from
taskgraph
.
util
.
taskcluster
import
CONCURRENCY
cancel_task
from
gecko_taskgraph
.
util
.
taskcluster
import
list_task_group_incomplete_task_ids
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
All
"
    
name
=
"
cancel
-
all
"
    
symbol
=
"
cAll
"
    
description
=
(
        
"
Cancel
all
running
and
pending
tasks
created
by
the
decision
task
"
        
"
this
action
task
is
associated
with
.
"
    
)
    
order
=
400
    
context
=
[
]
)
def
cancel_all_action
(
parameters
graph_config
input
task_group_id
task_id
)
:
    
def
do_cancel_task
(
task_id
)
:
        
logger
.
info
(
f
"
Cancelling
task
{
task_id
}
"
)
        
try
:
            
cancel_task
(
task_id
)
        
except
TaskclusterRestFailure
as
e
:
            
if
e
.
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
    
own_task_id
=
os
.
environ
.
get
(
"
TASK_ID
"
"
"
)
    
to_cancel
=
[
        
t
        
for
t
in
list_task_group_incomplete_task_ids
(
task_group_id
)
        
if
t
!
=
own_task_id
    
]
    
logger
.
info
(
f
"
Cancelling
{
len
(
to_cancel
)
}
tasks
"
)
    
with
futures
.
ThreadPoolExecutor
(
CONCURRENCY
)
as
e
:
        
cancel_futs
=
[
e
.
submit
(
do_cancel_task
t
)
for
t
in
to_cancel
]
        
for
f
in
futures
.
as_completed
(
cancel_futs
)
:
            
f
.
result
(
)
