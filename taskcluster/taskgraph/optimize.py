from
__future__
import
absolute_import
print_function
unicode_literals
import
logging
import
os
import
requests
from
collections
import
defaultdict
from
.
graph
import
Graph
from
.
import
files_changed
from
.
taskgraph
import
TaskGraph
from
.
util
.
seta
import
is_low_value_task
from
.
util
.
taskcluster
import
find_task_id
from
.
util
.
parameterization
import
resolve_task_references
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
_optimizations
=
{
}
def
optimize_task_graph
(
target_task_graph
params
do_not_optimize
existing_tasks
=
None
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
=
target_task_graph
                        
params
=
params
                        
do_not_optimize
=
do_not_optimize
                        
named_links_dict
=
named_links_dict
                        
label_to_taskid
=
label_to_taskid
                        
existing_tasks
=
existing_tasks
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
optimize_task
(
task
params
)
:
    
"
"
"
    
Run
the
optimization
for
a
given
task
    
"
"
"
    
if
not
task
.
optimization
:
        
return
False
    
opt_type
arg
=
task
.
optimization
.
items
(
)
[
0
]
    
opt_fn
=
_optimizations
[
opt_type
]
    
return
opt_fn
(
task
params
arg
)
def
annotate_task_graph
(
target_task_graph
params
do_not_optimize
                        
named_links_dict
label_to_taskid
existing_tasks
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
    
opt_counts
=
defaultdict
(
lambda
:
{
'
away
'
:
0
'
replaced
'
:
0
}
)
    
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
        
opt_by
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
existing_tasks
is
not
None
and
label
in
existing_tasks
:
            
optimized
=
True
            
replacement_task_id
=
existing_tasks
[
label
]
            
opt_by
=
"
existing_tasks
"
        
else
:
            
opt_result
=
optimize_task
(
task
params
)
            
optimized
=
bool
(
opt_result
)
            
if
optimized
:
                
opt_by
=
task
.
optimization
.
keys
(
)
[
0
]
                
replacement_task_id
=
opt_result
if
opt_result
is
not
True
else
None
        
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
                
opt_counts
[
opt_by
]
[
'
replaced
'
]
+
=
1
                
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
                
opt_counts
[
opt_by
]
[
'
away
'
]
+
=
1
                
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
    
for
opt_by
in
sorted
(
opt_counts
)
:
        
counts
=
opt_counts
[
opt_by
]
        
if
counts
[
'
away
'
]
and
not
counts
[
'
replaced
'
]
:
            
msg
=
"
optimized
away
{
}
tasks
for
{
}
:
"
.
format
(
counts
[
'
away
'
]
opt_by
)
        
elif
counts
[
'
replaced
'
]
and
not
counts
[
'
away
'
]
:
            
msg
=
"
optimized
{
}
tasks
replacing
with
other
tasks
for
{
}
:
"
.
format
(
                
counts
[
'
away
'
]
opt_by
)
        
else
:
            
msg
=
"
optimized
{
}
tasks
for
{
}
replacing
{
}
and
optimizing
{
}
away
"
.
format
(
                
sum
(
counts
.
values
(
)
)
opt_by
counts
[
'
replaced
'
]
counts
[
'
away
'
]
)
        
logger
.
info
(
msg
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
def
optimization
(
name
)
:
    
def
wrap
(
func
)
:
        
if
name
in
_optimizations
:
            
raise
Exception
(
"
multiple
optimizations
with
name
{
}
"
.
format
(
name
)
)
        
_optimizations
[
name
]
=
func
        
return
func
    
return
wrap
optimization
(
'
index
-
search
'
)
def
opt_index_search
(
task
params
index_paths
)
:
    
for
index_path
in
index_paths
:
        
try
:
            
task_id
=
find_task_id
(
                
index_path
                
use_proxy
=
bool
(
os
.
environ
.
get
(
'
TASK_ID
'
)
)
)
            
return
task_id
        
except
requests
.
exceptions
.
HTTPError
:
            
pass
    
return
False
optimization
(
'
seta
'
)
def
opt_seta
(
task
params
_
)
:
    
bbb_task
=
False
    
if
task
.
task
.
get
(
'
provisionerId
'
'
'
)
=
=
'
buildbot
-
bridge
'
:
        
label
=
task
.
task
.
get
(
'
payload
'
)
.
get
(
'
buildername
'
)
        
bbb_task
=
True
    
else
:
        
label
=
task
.
label
    
if
is_low_value_task
(
label
                         
params
.
get
(
'
project
'
)
                         
params
.
get
(
'
pushlog_id
'
)
                         
params
.
get
(
'
pushdate
'
)
                         
bbb_task
)
:
        
return
True
    
else
:
        
return
False
optimization
(
'
skip
-
unless
-
changed
'
)
def
opt_files_changed
(
task
params
file_patterns
)
:
    
if
params
.
get
(
'
pushlog_id
'
)
=
=
-
1
:
        
return
True
    
changed
=
files_changed
.
check
(
params
file_patterns
)
    
if
not
changed
:
        
logger
.
debug
(
'
no
files
found
matching
a
pattern
in
skip
-
unless
-
changed
for
'
+
                     
task
.
label
)
        
return
True
    
return
False
