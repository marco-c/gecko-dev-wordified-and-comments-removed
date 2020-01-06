#
-
*
-
coding
:
utf
-
8
-
*
-
from
__future__
import
absolute_import
print_function
unicode_literals
import
os
import
json
import
logging
import
time
import
yaml
from
.
generator
import
TaskGraphGenerator
from
.
create
import
create_tasks
from
.
parameters
import
Parameters
from
.
taskgraph
import
TaskGraph
from
.
try_option_syntax
import
parse_message
from
.
actions
import
render_actions_json
from
taskgraph
.
util
.
partials
import
populate_release_history
logger
=
logging
.
getLogger
(
__name__
)
ARTIFACTS_DIR
=
'
artifacts
'
PER_PROJECT_PARAMETERS
=
{
    
'
try
'
:
{
        
'
target_tasks_method
'
:
'
try_tasks
'
        
'
include_nightly
'
:
True
    
}
    
'
try
-
comm
-
central
'
:
{
        
'
target_tasks_method
'
:
'
try_tasks
'
    
}
    
'
ash
'
:
{
        
'
target_tasks_method
'
:
'
ash_tasks
'
        
'
optimize_target_tasks
'
:
True
        
'
include_nightly
'
:
False
    
}
    
'
cedar
'
:
{
        
'
target_tasks_method
'
:
'
cedar_tasks
'
        
'
optimize_target_tasks
'
:
True
        
'
include_nightly
'
:
False
    
}
    
'
graphics
'
:
{
        
'
target_tasks_method
'
:
'
graphics_tasks
'
        
'
optimize_target_tasks
'
:
True
        
'
include_nightly
'
:
False
    
}
    
'
mozilla
-
beta
'
:
{
        
'
target_tasks_method
'
:
'
mozilla_beta_tasks
'
        
'
optimize_target_tasks
'
:
False
        
'
include_nightly
'
:
True
    
}
    
'
mozilla
-
release
'
:
{
        
'
target_tasks_method
'
:
'
mozilla_release_tasks
'
        
'
optimize_target_tasks
'
:
False
        
'
include_nightly
'
:
True
    
}
    
'
pine
'
:
{
        
'
target_tasks_method
'
:
'
pine_tasks
'
        
'
optimize_target_tasks
'
:
True
        
'
include_nightly
'
:
False
    
}
    
'
default
'
:
{
        
'
target_tasks_method
'
:
'
default
'
        
'
optimize_target_tasks
'
:
True
        
'
include_nightly
'
:
False
    
}
}
def
taskgraph_decision
(
options
parameters
=
None
)
:
    
"
"
"
    
Run
the
decision
task
.
This
function
implements
mach
taskgraph
decision
    
and
is
responsible
for
     
*
processing
decision
task
command
-
line
options
into
parameters
     
*
running
task
-
graph
generation
exactly
the
same
way
the
other
mach
       
taskgraph
commands
do
     
*
generating
a
set
of
artifacts
to
memorialize
the
graph
     
*
calling
TaskCluster
APIs
to
create
the
graph
    
"
"
"
    
parameters
=
parameters
or
get_decision_parameters
(
options
)
    
tgg
=
TaskGraphGenerator
(
        
root_dir
=
options
.
get
(
'
root
'
)
        
parameters
=
parameters
)
    
write_artifact
(
'
parameters
.
yml
'
dict
(
*
*
parameters
)
)
    
write_artifact
(
'
actions
.
json
'
render_actions_json
(
parameters
)
)
    
full_task_json
=
tgg
.
full_task_graph
.
to_json
(
)
    
write_artifact
(
'
full
-
task
-
graph
.
json
'
full_task_json
)
    
_
_
=
TaskGraph
.
from_json
(
full_task_json
)
    
write_artifact
(
'
target
-
tasks
.
json
'
tgg
.
target_task_set
.
tasks
.
keys
(
)
)
    
write_artifact
(
'
task
-
graph
.
json
'
tgg
.
morphed_task_graph
.
to_json
(
)
)
    
write_artifact
(
'
label
-
to
-
taskid
.
json
'
tgg
.
label_to_taskid
)
    
create_tasks
(
tgg
.
morphed_task_graph
tgg
.
label_to_taskid
parameters
)
def
get_decision_parameters
(
options
)
:
    
"
"
"
    
Load
parameters
from
the
command
-
line
options
for
'
taskgraph
decision
'
.
    
This
also
applies
per
-
project
parameters
based
on
the
given
project
.
    
"
"
"
    
parameters
=
{
n
:
options
[
n
]
for
n
in
[
        
'
base_repository
'
        
'
head_repository
'
        
'
head_rev
'
        
'
head_ref
'
        
'
message
'
        
'
project
'
        
'
pushlog_id
'
        
'
pushdate
'
        
'
owner
'
        
'
level
'
        
'
target_tasks_method
'
    
]
if
n
in
options
}
    
for
n
in
(
        
'
comm_base_repository
'
        
'
comm_head_repository
'
        
'
comm_head_rev
'
        
'
comm_head_ref
'
    
)
:
        
if
n
in
options
and
options
[
n
]
is
not
None
:
            
parameters
[
n
]
=
options
[
n
]
    
parameters
[
'
filters
'
]
=
[
        
'
check_servo
'
        
'
target_tasks_method
'
    
]
    
parameters
[
'
existing_tasks
'
]
=
{
}
    
parameters
[
'
do_not_optimize
'
]
=
[
]
    
if
'
'
not
in
parameters
[
'
owner
'
]
:
        
parameters
[
'
owner
'
]
+
=
'
noreply
.
mozilla
.
org
'
    
parameters
[
'
build_date
'
]
=
parameters
[
'
pushdate
'
]
or
int
(
time
.
time
(
)
)
    
parameters
[
'
moz_build_date
'
]
=
time
.
strftime
(
"
%
Y
%
m
%
d
%
H
%
M
%
S
"
                                                 
time
.
gmtime
(
parameters
[
'
build_date
'
]
)
)
    
project
=
parameters
[
'
project
'
]
    
try
:
        
parameters
.
update
(
PER_PROJECT_PARAMETERS
[
project
]
)
    
except
KeyError
:
        
logger
.
warning
(
"
using
default
project
parameters
;
add
{
}
to
"
                       
"
PER_PROJECT_PARAMETERS
in
{
}
to
customize
behavior
"
                       
"
for
this
project
"
.
format
(
project
__file__
)
)
        
parameters
.
update
(
PER_PROJECT_PARAMETERS
[
'
default
'
]
)
    
if
options
.
get
(
'
target_tasks_method
'
)
:
        
parameters
[
'
target_tasks_method
'
]
=
options
[
'
target_tasks_method
'
]
    
parameters
.
setdefault
(
'
release_history
'
dict
(
)
)
    
if
'
nightly
'
in
parameters
.
get
(
'
target_tasks_method
'
'
'
)
:
        
parameters
[
'
release_history
'
]
=
populate_release_history
(
'
Firefox
'
project
)
    
task_config_file
=
os
.
path
.
join
(
os
.
getcwd
(
)
'
try_task_config
.
json
'
)
    
if
'
try
'
in
project
:
        
parameters
[
'
try_mode
'
]
=
None
        
if
os
.
path
.
isfile
(
task_config_file
)
:
            
parameters
[
'
try_mode
'
]
=
'
try_task_config
'
            
with
open
(
task_config_file
'
r
'
)
as
fh
:
                
parameters
[
'
try_task_config
'
]
=
json
.
load
(
fh
)
        
else
:
            
parameters
[
'
try_task_config
'
]
=
None
        
if
'
try
:
'
in
parameters
[
'
message
'
]
:
            
parameters
[
'
try_mode
'
]
=
'
try_option_syntax
'
            
args
=
parse_message
(
parameters
[
'
message
'
]
)
            
parameters
[
'
try_options
'
]
=
args
        
else
:
            
parameters
[
'
try_options
'
]
=
None
        
if
parameters
[
'
try_mode
'
]
:
            
parameters
[
'
optimize_target_tasks
'
]
=
False
        
else
:
            
parameters
[
'
optimize_target_tasks
'
]
=
True
    
else
:
        
parameters
[
'
try_mode
'
]
=
None
        
parameters
[
'
try_task_config
'
]
=
None
        
parameters
[
'
try_options
'
]
=
None
    
return
Parameters
(
*
*
parameters
)
def
write_artifact
(
filename
data
)
:
    
logger
.
info
(
'
writing
artifact
file
{
}
'
.
format
(
filename
)
)
    
if
not
os
.
path
.
isdir
(
ARTIFACTS_DIR
)
:
        
os
.
mkdir
(
ARTIFACTS_DIR
)
    
path
=
os
.
path
.
join
(
ARTIFACTS_DIR
filename
)
    
if
filename
.
endswith
(
'
.
yml
'
)
:
        
with
open
(
path
'
w
'
)
as
f
:
            
yaml
.
safe_dump
(
data
f
allow_unicode
=
True
default_flow_style
=
False
)
    
elif
filename
.
endswith
(
'
.
json
'
)
:
        
with
open
(
path
'
w
'
)
as
f
:
            
json
.
dump
(
data
f
sort_keys
=
True
indent
=
2
separators
=
(
'
'
'
:
'
)
)
    
else
:
        
raise
TypeError
(
"
Don
'
t
know
how
to
write
to
{
}
"
.
format
(
filename
)
)
