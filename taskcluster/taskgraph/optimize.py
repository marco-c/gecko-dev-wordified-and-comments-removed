from
__future__
import
absolute_import
print_function
unicode_literals
import
logging
import
re
from
.
graph
import
Graph
from
.
types
import
TaskGraph
from
slugid
import
nice
as
slugid
logger
=
logging
.
getLogger
(
__name__
)
TASK_REFERENCE_PATTERN
=
re
.
compile
(
'
<
(
[
^
>
]
+
)
>
'
)
def
optimize_task_graph
(
target_task_graph
do_not_optimize
)
:
    
"
"
"
    
Perform
task
optimization
without
optimizing
tasks
named
in
    
do_not_optimize
.
    
"
"
"
    
named_links_dict
=
target_task_graph
.
graph
.
named_links_dict
(
)
    
label_to_taskid
=
{
}
    
annotate_task_graph
(
target_task_graph
do_not_optimize
named_links_dict
label_to_taskid
)
    
return
get_subgraph
(
target_task_graph
named_links_dict
label_to_taskid
)
label_to_taskid
def
resolve_task_references
(
label
task_def
taskid_for_edge_name
)
:
    
def
repl
(
match
)
:
        
key
=
match
.
group
(
1
)
        
try
:
            
return
taskid_for_edge_name
[
key
]
        
except
KeyError
:
            
if
key
=
=
'
<
'
:
                
return
key
            
raise
KeyError
(
"
task
'
{
}
'
has
no
dependency
with
label
'
{
}
'
"
.
format
(
label
key
)
)
    
def
recurse
(
val
)
:
        
if
isinstance
(
val
list
)
:
            
return
[
recurse
(
v
)
for
v
in
val
]
        
elif
isinstance
(
val
dict
)
:
            
if
val
.
keys
(
)
=
=
[
'
task
-
reference
'
]
:
                
return
TASK_REFERENCE_PATTERN
.
sub
(
repl
val
[
'
task
-
reference
'
]
)
            
else
:
                
return
{
k
:
recurse
(
v
)
for
k
v
in
val
.
iteritems
(
)
}
        
else
:
            
return
val
    
return
recurse
(
task_def
)
def
annotate_task_graph
(
target_task_graph
do_not_optimize
named_links_dict
label_to_taskid
)
:
    
"
"
"
    
Annotate
each
task
in
the
graph
with
.
optimized
(
boolean
)
and
.
task_id
    
(
possibly
None
)
following
the
rules
for
optimization
and
calling
the
task
    
kinds
'
optimize_task
method
.
    
As
a
side
effect
label_to_taskid
is
updated
with
labels
for
all
optimized
    
tasks
that
are
replaced
with
existing
tasks
.
    
"
"
"
    
for
label
in
target_task_graph
.
graph
.
visit_postorder
(
)
:
        
task
=
target_task_graph
.
tasks
[
label
]
        
named_task_dependencies
=
named_links_dict
.
get
(
label
{
}
)
        
dependencies
=
[
target_task_graph
.
tasks
[
l
]
for
l
in
named_task_dependencies
.
itervalues
(
)
]
        
for
t
in
dependencies
:
            
if
t
.
optimized
and
not
t
.
task_id
:
                
raise
Exception
(
                    
"
task
{
}
was
optimized
away
but
{
}
depends
on
it
"
.
format
(
                        
t
.
label
label
)
)
        
replacement_task_id
=
None
        
if
label
in
do_not_optimize
:
            
optimized
=
False
        
elif
any
(
not
t
.
optimized
for
t
in
dependencies
)
:
            
optimized
=
False
        
else
:
            
optimized
replacement_task_id
=
task
.
kind
.
optimize_task
(
task
named_task_dependencies
)
        
task
.
optimized
=
optimized
        
task
.
task_id
=
replacement_task_id
        
if
replacement_task_id
:
            
label_to_taskid
[
label
]
=
replacement_task_id
        
if
optimized
:
            
if
replacement_task_id
:
                
logger
.
debug
(
"
optimizing
{
}
replacing
with
task
{
}
"
                             
.
format
(
label
replacement_task_id
)
)
            
else
:
                
logger
.
debug
(
"
optimizing
{
}
away
"
.
format
(
label
)
)
        
else
:
            
if
replacement_task_id
:
                
raise
Exception
(
"
{
}
:
optimize_task
returned
False
with
a
taskId
"
.
format
(
label
)
)
def
get_subgraph
(
annotated_task_graph
named_links_dict
label_to_taskid
)
:
    
"
"
"
    
Return
the
subgraph
of
annotated_task_graph
consisting
only
of
    
non
-
optimized
tasks
and
edges
between
them
.
    
To
avoid
losing
track
of
taskIds
for
tasks
optimized
away
this
method
    
simultaneously
substitutes
real
taskIds
for
task
labels
in
the
graph
and
    
populates
each
task
definition
'
s
dependencies
key
with
the
appropriate
    
taskIds
.
Task
references
are
resolved
in
the
process
.
    
"
"
"
    
tasks_by_taskid
=
{
}
    
for
label
in
annotated_task_graph
.
graph
.
visit_postorder
(
)
:
        
task
=
annotated_task_graph
.
tasks
[
label
]
        
if
task
.
optimized
:
            
continue
        
task
.
task_id
=
label_to_taskid
[
label
]
=
slugid
(
)
        
named_task_dependencies
=
{
                
name
:
label_to_taskid
[
label
]
                
for
name
label
in
named_links_dict
.
get
(
label
{
}
)
.
iteritems
(
)
}
        
task
.
task
=
resolve_task_references
(
task
.
label
task
.
task
named_task_dependencies
)
        
task
.
task
.
setdefault
(
'
dependencies
'
[
]
)
.
extend
(
named_task_dependencies
.
itervalues
(
)
)
        
tasks_by_taskid
[
task
.
task_id
]
=
task
    
edges_by_taskid
=
(
        
(
label_to_taskid
.
get
(
left
)
label_to_taskid
.
get
(
right
)
name
)
        
for
(
left
right
name
)
in
annotated_task_graph
.
graph
.
edges
        
)
    
edges_by_taskid
=
set
(
        
(
left
right
name
)
        
for
(
left
right
name
)
in
edges_by_taskid
        
if
left
in
tasks_by_taskid
and
right
in
tasks_by_taskid
        
)
    
return
TaskGraph
(
        
tasks_by_taskid
        
Graph
(
set
(
tasks_by_taskid
)
edges_by_taskid
)
)
