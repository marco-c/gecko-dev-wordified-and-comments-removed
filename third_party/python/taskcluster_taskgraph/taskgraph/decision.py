import
json
import
logging
import
os
import
pathlib
import
shutil
import
time
from
pathlib
import
Path
import
yaml
from
voluptuous
import
Optional
from
taskgraph
.
actions
import
render_actions_json
from
taskgraph
.
create
import
create_tasks
from
taskgraph
.
generator
import
TaskGraphGenerator
from
taskgraph
.
parameters
import
Parameters
from
taskgraph
.
taskgraph
import
TaskGraph
from
taskgraph
.
util
.
python_path
import
find_object
from
taskgraph
.
util
.
schema
import
Schema
validate_schema
from
taskgraph
.
util
.
vcs
import
get_repository
from
taskgraph
.
util
.
yaml
import
load_yaml
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
Path
(
"
artifacts
"
)
PER_PROJECT_PARAMETERS
=
{
    
"
default
"
:
{
        
"
target_tasks_method
"
:
"
default
"
    
}
}
try_task_config_schema_v2
=
Schema
(
    
{
        
Optional
(
"
parameters
"
)
:
{
str
:
object
}
    
}
)
def
full_task_graph_to_runnable_jobs
(
full_task_json
)
:
    
runnable_jobs
=
{
}
    
for
label
node
in
full_task_json
.
items
(
)
:
        
if
not
(
"
extra
"
in
node
[
"
task
"
]
and
"
treeherder
"
in
node
[
"
task
"
]
[
"
extra
"
]
)
:
            
continue
        
th
=
node
[
"
task
"
]
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
        
runnable_jobs
[
label
]
=
{
"
symbol
"
:
th
[
"
symbol
"
]
}
        
for
i
in
(
"
groupName
"
"
groupSymbol
"
"
collection
"
)
:
            
if
i
in
th
:
                
runnable_jobs
[
label
]
[
i
]
=
th
[
i
]
        
if
th
.
get
(
"
machine
"
{
}
)
.
get
(
"
platform
"
)
:
            
runnable_jobs
[
label
]
[
"
platform
"
]
=
th
[
"
machine
"
]
[
"
platform
"
]
    
return
runnable_jobs
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
(
        
lambda
graph_config
:
get_decision_parameters
(
graph_config
options
)
    
)
    
decision_task_id
=
os
.
environ
[
"
TASK_ID
"
]
    
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
"
root
"
)
        
parameters
=
parameters
        
decision_task_id
=
decision_task_id
        
write_artifacts
=
True
    
)
    
write_artifact
(
"
parameters
.
yml
"
dict
(
*
*
tgg
.
parameters
)
)
    
write_artifact
(
        
"
actions
.
json
"
        
render_actions_json
(
tgg
.
parameters
tgg
.
graph_config
decision_task_id
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
"
full
-
task
-
graph
.
json
"
full_task_json
)
    
write_artifact
(
        
"
runnable
-
jobs
.
json
"
full_task_graph_to_runnable_jobs
(
full_task_json
)
    
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
"
target
-
tasks
.
json
"
list
(
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
)
    
write_artifact
(
"
task
-
graph
.
json
"
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
"
label
-
to
-
taskid
.
json
"
tgg
.
label_to_taskid
)
    
RUN_TASK_DIR
=
pathlib
.
Path
(
__file__
)
.
parent
/
"
run
-
task
"
    
shutil
.
copy2
(
RUN_TASK_DIR
/
"
run
-
task
"
ARTIFACTS_DIR
)
    
shutil
.
copy2
(
RUN_TASK_DIR
/
"
fetch
-
content
"
ARTIFACTS_DIR
)
    
create_tasks
(
        
tgg
.
graph_config
        
tgg
.
morphed_task_graph
        
tgg
.
label_to_taskid
        
tgg
.
parameters
        
decision_task_id
=
decision_task_id
    
)
def
get_decision_parameters
(
graph_config
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
            
"
base_repository
"
            
"
head_repository
"
            
"
head_rev
"
            
"
head_ref
"
            
"
head_tag
"
            
"
project
"
            
"
pushlog_id
"
            
"
pushdate
"
            
"
repository_type
"
            
"
owner
"
            
"
level
"
            
"
target_tasks_method
"
            
"
tasks_for
"
        
]
        
if
n
in
options
    
}
    
repo
=
get_repository
(
os
.
getcwd
(
)
)
    
try
:
        
commit_message
=
repo
.
get_commit_message
(
)
    
except
UnicodeDecodeError
:
        
commit_message
=
"
"
    
parameters
[
"
filters
"
]
=
[
        
"
target_tasks_method
"
    
]
    
parameters
[
"
optimize_target_tasks
"
]
=
True
    
parameters
[
"
existing_tasks
"
]
=
{
}
    
parameters
[
"
do_not_optimize
"
]
=
[
]
    
if
"
"
not
in
parameters
[
"
owner
"
]
:
        
parameters
[
"
owner
"
]
+
=
"
noreply
.
mozilla
.
org
"
    
parameters
[
"
build_date
"
]
=
parameters
[
"
pushdate
"
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
"
moz_build_date
"
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
"
build_date
"
]
)
    
)
    
project
=
parameters
[
"
project
"
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
"
default
"
]
)
    
if
options
.
get
(
"
target_tasks_method
"
)
:
        
parameters
[
"
target_tasks_method
"
]
=
options
[
"
target_tasks_method
"
]
    
if
"
DONTBUILD
"
in
commit_message
and
options
[
"
tasks_for
"
]
=
=
"
hg
-
push
"
:
        
parameters
[
"
target_tasks_method
"
]
=
"
nothing
"
    
if
options
.
get
(
"
optimize_target_tasks
"
)
is
not
None
:
        
parameters
[
"
optimize_target_tasks
"
]
=
options
[
"
optimize_target_tasks
"
]
    
if
"
decision
-
parameters
"
in
graph_config
[
"
taskgraph
"
]
:
        
find_object
(
graph_config
[
"
taskgraph
"
]
[
"
decision
-
parameters
"
]
)
(
            
graph_config
parameters
        
)
    
if
options
.
get
(
"
try_task_config_file
"
)
:
        
task_config_file
=
os
.
path
.
abspath
(
options
.
get
(
"
try_task_config_file
"
)
)
    
else
:
        
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
"
try_task_config
.
json
"
)
    
if
(
"
try
"
in
project
and
options
[
"
tasks_for
"
]
=
=
"
hg
-
push
"
)
or
options
[
        
"
tasks_for
"
    
]
=
=
"
github
-
pull
-
request
"
:
        
set_try_config
(
parameters
task_config_file
)
    
result
=
Parameters
(
*
*
parameters
)
    
result
.
check
(
)
    
return
result
def
set_try_config
(
parameters
task_config_file
)
:
    
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
        
logger
.
info
(
f
"
using
try
tasks
from
{
task_config_file
}
"
)
        
with
open
(
task_config_file
)
as
fh
:
            
task_config
=
json
.
load
(
fh
)
        
task_config_version
=
task_config
.
pop
(
"
version
"
)
        
if
task_config_version
=
=
2
:
            
validate_schema
(
                
try_task_config_schema_v2
                
task_config
                
"
Invalid
v2
try_task_config
.
json
.
"
            
)
            
parameters
.
update
(
task_config
[
"
parameters
"
]
)
            
return
        
else
:
            
raise
Exception
(
                
f
"
Unknown
try_task_config
.
json
version
:
{
task_config_version
}
"
            
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
f
"
writing
artifact
file
{
filename
}
"
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
ARTIFACTS_DIR
/
filename
    
if
filename
.
endswith
(
"
.
yml
"
)
:
        
with
open
(
path
"
w
"
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
"
.
json
"
)
:
        
with
open
(
path
"
w
"
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
"
"
"
:
"
)
)
    
elif
filename
.
endswith
(
"
.
gz
"
)
:
        
import
gzip
        
with
gzip
.
open
(
path
"
wb
"
)
as
f
:
            
f
.
write
(
json
.
dumps
(
data
)
)
    
else
:
        
raise
TypeError
(
f
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
filename
}
"
)
def
read_artifact
(
filename
)
:
    
path
=
ARTIFACTS_DIR
/
filename
    
if
filename
.
endswith
(
"
.
yml
"
)
:
        
return
load_yaml
(
path
filename
)
    
elif
filename
.
endswith
(
"
.
json
"
)
:
        
with
open
(
path
)
as
f
:
            
return
json
.
load
(
f
)
    
elif
filename
.
endswith
(
"
.
gz
"
)
:
        
import
gzip
        
with
gzip
.
open
(
path
"
rb
"
)
as
f
:
            
return
json
.
load
(
f
)
    
else
:
        
raise
TypeError
(
f
"
Don
'
t
know
how
to
read
{
filename
}
"
)
def
rename_artifact
(
src
dest
)
:
    
os
.
rename
(
ARTIFACTS_DIR
/
src
ARTIFACTS_DIR
/
dest
)
