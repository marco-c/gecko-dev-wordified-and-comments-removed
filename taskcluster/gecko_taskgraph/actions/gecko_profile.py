import
logging
import
requests
from
requests
.
exceptions
import
HTTPError
from
taskgraph
.
util
.
taskcluster
import
get_artifact_from_index
get_task_definition
from
.
registry
import
register_callback_action
from
.
util
import
combine_task_graph_files
create_tasks
fetch_graph_and_labels
PUSHLOG_TMPL
=
"
{
}
/
json
-
pushes
?
version
=
2
&
startID
=
{
}
&
endID
=
{
}
"
INDEX_TMPL
=
"
gecko
.
v2
.
{
}
.
pushlog
-
id
.
{
}
.
decision
"
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
GeckoProfile
"
    
name
=
"
geckoprofile
"
    
symbol
=
"
Gp
"
    
description
=
(
        
"
Take
the
label
of
the
current
task
"
        
"
and
trigger
the
task
with
that
label
"
        
"
on
previous
pushes
in
the
same
project
"
        
"
while
adding
the
-
-
gecko
-
profile
cmd
arg
.
"
        
"
Plus
optional
overrides
for
threads
"
        
"
features
and
sampling
interval
.
"
    
)
    
order
=
200
    
context
=
[
        
{
"
test
-
type
"
:
"
talos
"
}
        
{
"
test
-
type
"
:
"
raptor
"
}
        
{
"
test
-
type
"
:
"
mozperftest
"
}
    
]
    
schema
=
{
        
"
type
"
:
"
object
"
        
"
properties
"
:
{
            
"
depth
"
:
{
                
"
type
"
:
"
integer
"
                
"
default
"
:
1
                
"
minimum
"
:
1
                
"
maximum
"
:
10
                
"
title
"
:
"
Depth
"
                
"
description
"
:
"
How
many
pushes
to
backfill
the
profiling
task
on
.
"
            
}
            
"
gecko_profile_interval
"
:
{
                
"
type
"
:
"
integer
"
                
"
default
"
:
None
                
"
title
"
:
"
Sampling
interval
(
ms
)
"
                
"
description
"
:
"
How
often
to
sample
the
profiler
(
in
ms
)
.
"
            
}
            
"
gecko_profile_features
"
:
{
                
"
type
"
:
"
string
"
                
"
default
"
:
"
"
                
"
title
"
:
"
Features
"
                
"
description
"
:
"
Comma
-
separated
Gecko
profiler
features
.
"
                
"
Example
:
js
stackwalk
cpu
screenshots
memory
"
            
}
            
"
gecko_profile_threads
"
:
{
                
"
type
"
:
"
string
"
                
"
default
"
:
"
"
                
"
title
"
:
"
Threads
"
                
"
description
"
:
"
Comma
-
separated
thread
names
to
profile
.
"
                
"
Example
:
GeckoMain
Compositor
Renderer
"
            
}
        
}
    
}
    
available
=
lambda
parameters
:
True
)
def
geckoprofile_action
(
parameters
graph_config
input
task_group_id
task_id
)
:
    
task
=
get_task_definition
(
task_id
)
    
label
=
task
[
"
metadata
"
]
[
"
name
"
]
    
pushes
=
[
]
    
depth
=
input
.
get
(
"
depth
"
1
)
    
end_id
=
int
(
parameters
[
"
pushlog_id
"
]
)
    
while
True
:
        
start_id
=
max
(
end_id
-
depth
0
)
        
pushlog_url
=
PUSHLOG_TMPL
.
format
(
            
parameters
[
"
head_repository
"
]
start_id
end_id
        
)
        
r
=
requests
.
get
(
pushlog_url
)
        
r
.
raise_for_status
(
)
        
pushes
=
pushes
+
list
(
r
.
json
(
)
[
"
pushes
"
]
.
keys
(
)
)
        
if
len
(
pushes
)
>
=
depth
:
            
break
        
end_id
=
start_id
-
1
        
start_id
-
=
depth
        
if
start_id
<
0
:
            
break
    
pushes
=
sorted
(
pushes
)
[
-
depth
:
]
    
backfill_pushes
=
[
]
    
for
push
in
pushes
:
        
try
:
            
push_params
=
get_artifact_from_index
(
                
INDEX_TMPL
.
format
(
parameters
[
"
project
"
]
push
)
"
public
/
parameters
.
yml
"
            
)
            
push_decision_task_id
full_task_graph
label_to_taskid
_
=
(
                
fetch_graph_and_labels
(
push_params
graph_config
)
            
)
        
except
HTTPError
as
e
:
            
logger
.
info
(
f
"
Skipping
{
push
}
due
to
missing
index
artifacts
!
Error
:
{
e
}
"
)
            
continue
        
if
label
in
full_task_graph
.
tasks
.
keys
(
)
:
            
def
modifier
(
task
)
:
                
if
task
.
label
!
=
label
:
                    
return
task
                
interval
=
input
.
get
(
"
gecko_profile_interval
"
)
                
features
=
input
.
get
(
"
gecko_profile_features
"
)
                
threads
=
input
.
get
(
"
gecko_profile_threads
"
)
                
task_kind
=
task
.
kind
                
env
=
task
.
task
[
"
payload
"
]
[
"
env
"
]
                
perf_flags
=
env
.
get
(
"
PERF_FLAGS
"
"
"
)
                
test_suite
=
task
.
attributes
.
get
(
"
unittest_suite
"
)
                
profiling_command_flags
=
[
"
-
-
gecko
-
profile
"
]
                
if
task_kind
=
=
"
perftest
"
:
                    
if
"
gecko
-
profile
"
not
in
perf_flags
:
                        
env
[
"
PERF_FLAGS
"
]
=
(
perf_flags
+
"
gecko
-
profile
"
)
.
strip
(
)
                    
if
interval
is
not
None
:
                        
env
[
"
MOZ_PROFILER_STARTUP_INTERVAL
"
]
=
str
(
interval
)
                    
if
features
is
not
None
:
                        
env
[
"
MOZ_PROFILER_STARTUP_FEATURES
"
]
=
features
                    
if
threads
is
not
None
:
                        
env
[
"
MOZ_PROFILER_STARTUP_FILTERS
"
]
=
threads
                
elif
test_suite
=
=
"
raptor
"
:
                    
raptor_flags
=
[
]
                    
if
interval
is
not
None
:
                        
raptor_flags
.
append
(
f
"
gecko
-
profile
-
interval
=
{
interval
}
"
)
                    
if
features
is
not
None
:
                        
raptor_flags
.
append
(
f
"
gecko
-
profile
-
features
=
{
features
}
"
)
                    
if
threads
is
not
None
:
                        
raptor_flags
.
append
(
f
"
gecko
-
profile
-
threads
=
{
threads
}
"
)
                    
env
[
"
PERF_FLAGS
"
]
=
(
                        
perf_flags
+
"
"
+
"
"
.
join
(
raptor_flags
)
                    
)
.
strip
(
)
                
elif
test_suite
=
=
"
talos
"
:
                    
if
interval
is
not
None
:
                        
profiling_command_flags
.
append
(
                            
f
"
-
-
gecko
-
profile
-
interval
=
{
interval
}
"
                        
)
                    
if
features
is
not
None
:
                        
profiling_command_flags
.
append
(
                            
f
"
-
-
gecko
-
profile
-
features
=
{
features
}
"
                        
)
                    
if
threads
is
not
None
:
                        
profiling_command_flags
.
append
(
                            
f
"
-
-
gecko
-
profile
-
threads
=
{
threads
}
"
                        
)
                
if
"
command
"
in
task
.
task
[
"
payload
"
]
:
                    
cmd
=
task
.
task
[
"
payload
"
]
[
"
command
"
]
                    
task
.
task
[
"
payload
"
]
[
"
command
"
]
=
add_args_to_perf_command
(
                        
cmd
profiling_command_flags
                    
)
                
task
.
task
[
"
extra
"
]
[
"
treeherder
"
]
[
"
symbol
"
]
+
=
"
-
p
"
                
task
.
task
[
"
extra
"
]
[
"
treeherder
"
]
[
"
groupName
"
]
+
=
"
(
profiling
)
"
                
return
task
            
create_tasks
(
                
graph_config
                
[
label
]
                
full_task_graph
                
label_to_taskid
                
push_params
                
push_decision_task_id
                
push
                
modifier
=
modifier
            
)
            
backfill_pushes
.
append
(
push
)
        
else
:
            
logger
.
info
(
f
"
Could
not
find
{
label
}
on
{
push
}
.
Skipping
.
"
)
    
combine_task_graph_files
(
backfill_pushes
)
def
add_args_to_perf_command
(
payload_commands
extra_args
=
(
)
)
:
    
"
"
"
    
Add
custom
command
line
args
to
a
given
command
.
    
args
:
      
payload_commands
:
the
raw
command
as
seen
by
taskcluster
      
extra_args
:
array
of
args
we
want
to
inject
    
"
"
"
    
perf_command_idx
=
-
1
    
perf_command
=
payload_commands
[
perf_command_idx
]
    
command_form
=
"
default
"
    
if
isinstance
(
perf_command
str
)
:
        
perf_command
=
perf_command
.
split
(
"
"
)
        
command_form
=
"
string
"
    
perf_command
.
extend
(
extra_args
)
    
if
command_form
=
=
"
string
"
:
        
perf_command
=
"
"
.
join
(
perf_command
)
    
payload_commands
[
perf_command_idx
]
=
perf_command
    
return
payload_commands
