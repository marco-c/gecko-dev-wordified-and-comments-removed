import
logging
from
.
registry
import
register_callback_action
from
.
util
import
create_tasks
fetch_graph_and_labels
from
gecko_taskgraph
.
util
.
taskcluster
import
get_artifact
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
    
name
=
"
run
-
missing
-
tests
"
    
title
=
"
Run
Missing
Tests
"
    
symbol
=
"
rmt
"
    
description
=
(
        
"
Run
tests
in
the
selected
push
that
were
optimized
away
usually
by
SETA
.
"
        
"
\
n
"
        
"
This
action
is
for
use
on
pushes
that
will
be
merged
into
another
branch
"
        
"
to
check
that
optimization
hasn
'
t
hidden
any
failures
.
"
    
)
    
order
=
250
    
context
=
[
]
)
def
run_missing_tests
(
parameters
graph_config
input
task_group_id
task_id
)
:
    
decision_task_id
full_task_graph
label_to_taskid
=
fetch_graph_and_labels
(
        
parameters
graph_config
    
)
    
target_tasks
=
get_artifact
(
decision_task_id
"
public
/
target
-
tasks
.
json
"
)
    
to_run
=
[
]
    
already_run
=
0
    
for
label
in
target_tasks
:
        
task
=
full_task_graph
.
tasks
[
label
]
        
if
task
.
kind
!
=
"
test
"
:
            
continue
        
if
label
in
label_to_taskid
:
            
already_run
+
=
1
            
continue
        
to_run
.
append
(
label
)
    
create_tasks
(
        
graph_config
        
to_run
        
full_task_graph
        
label_to_taskid
        
parameters
        
decision_task_id
    
)
    
logger
.
info
(
        
"
Out
of
{
}
test
tasks
{
}
already
existed
and
the
action
created
{
}
"
.
format
(
            
already_run
+
len
(
to_run
)
already_run
len
(
to_run
)
        
)
    
)
