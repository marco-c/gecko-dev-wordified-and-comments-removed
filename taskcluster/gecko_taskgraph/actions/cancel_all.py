from
taskgraph
.
actions
.
cancel_all
import
cancel_all_action
from
.
registry
import
register_callback_action
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
(
cancel_all_action
)
