import
logging
import
os
import
shutil
import
sys
import
time
from
collections
import
defaultdict
from
pathlib
import
Path
import
taskgraph
import
yaml
from
redo
import
retry
from
taskgraph
import
create
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
main
import
format_kind_graph_mermaid
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
import
json
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
taskcluster
import
get_artifact
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
from
.
import
GECKO
from
.
actions
import
render_actions_json
from
.
files_changed
import
get_changed_files
from
.
parameters
import
get_app_version
get_version
from
.
util
.
backstop
import
ANDROID_PERFTEST_BACKSTOP_INDEX
BACKSTOP_INDEX
is_backstop
from
.
util
.
bugbug
import
push_schedules
from
.
util
.
hg
import
get_hg_revision_branch
get_hg_revision_info
from
.
util
.
partials
import
populate_release_history
from
.
util
.
taskcluster
import
insert_index
from
.
util
.
taskgraph
import
find_decision_task
find_existing_tasks_from_previous_kinds
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
os
.
environ
.
get
(
"
MOZ_UPLOAD_DIR
"
"
artifacts
"
)
GIT_BACKING_REPO
=
"
https
:
/
/
github
.
com
/
mozilla
-
releng
/
git
-
backing
"
PER_PROJECT_PARAMETERS
=
{
    
"
try
"
:
{
        
"
enable_always_target
"
:
True
        
"
target_tasks_method
"
:
"
try_tasks
"
        
"
release_type
"
:
"
nightly
"
    
}
    
"
kaios
-
try
"
:
{
        
"
target_tasks_method
"
:
"
try_tasks
"
    
}
    
"
ash
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
    
"
cedar
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
    
"
holly
"
:
{
        
"
enable_always_target
"
:
True
        
"
target_tasks_method
"
:
"
holly_tasks
"
    
}
    
"
oak
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
        
"
release_type
"
:
"
nightly
-
oak
"
    
}
    
"
graphics
"
:
{
        
"
target_tasks_method
"
:
"
graphics_tasks
"
    
}
    
"
autoland
"
:
{
        
"
head_git_repository
"
:
"
https
:
/
/
github
.
com
/
mozilla
-
firefox
/
firefox
"
        
"
head_git_ref
"
:
"
autoland
"
        
"
optimize_strategies
"
:
"
gecko_taskgraph
.
optimize
:
project
.
autoland
"
        
"
target_tasks_method
"
:
"
autoland_tasks
"
        
"
test_manifest_loader
"
:
"
bugbug
"
    
}
    
"
mozilla
-
central
"
:
{
        
"
head_git_repository
"
:
"
https
:
/
/
github
.
com
/
mozilla
-
firefox
/
firefox
"
        
"
head_git_ref
"
:
"
main
"
        
"
target_tasks_method
"
:
"
mozilla_central_tasks
"
        
"
release_type
"
:
"
nightly
"
    
}
    
"
mozilla
-
beta
"
:
{
        
"
head_git_repository
"
:
"
https
:
/
/
github
.
com
/
mozilla
-
firefox
/
firefox
"
        
"
head_git_ref
"
:
"
beta
"
        
"
optimize_strategies
"
:
"
gecko_taskgraph
.
optimize
:
project
.
beta
"
        
"
target_tasks_method
"
:
"
mozilla_beta_tasks
"
        
"
release_type
"
:
"
beta
"
    
}
    
"
mozilla
-
release
"
:
{
        
"
head_git_repository
"
:
"
https
:
/
/
github
.
com
/
mozilla
-
firefox
/
firefox
"
        
"
head_git_ref
"
:
"
release
"
        
"
target_tasks_method
"
:
"
mozilla_release_tasks
"
        
"
release_type
"
:
"
release
"
    
}
    
"
mozilla
-
esr140
"
:
{
        
"
head_git_repository
"
:
"
https
:
/
/
github
.
com
/
mozilla
-
firefox
/
firefox
"
        
"
head_git_ref
"
:
"
esr140
"
        
"
target_tasks_method
"
:
"
mozilla_esr140_tasks
"
        
"
release_type
"
:
"
esr140
"
    
}
    
"
mozilla
-
esr153
"
:
{
        
"
head_git_repository
"
:
"
https
:
/
/
github
.
com
/
mozilla
-
firefox
/
firefox
"
        
"
head_git_ref
"
:
"
esr153
"
        
"
target_tasks_method
"
:
"
mozilla_esr153_tasks
"
        
"
release_type
"
:
"
esr153
"
    
}
    
"
pine
"
:
{
        
"
target_tasks_method
"
:
"
pine_tasks
"
        
"
release_type
"
:
"
nightly
-
pine
"
    
}
    
"
maple
"
:
{
        
"
target_tasks_method
"
:
"
nothing
"
        
"
release_type
"
:
"
release
"
    
}
    
"
cypress
"
:
{
        
"
target_tasks_method
"
:
"
cypress_tasks
"
        
"
release_type
"
:
"
nightly
-
cypress
"
    
}
    
"
larch
"
:
{
        
"
target_tasks_method
"
:
"
larch_tasks
"
        
"
release_type
"
:
"
nightly
-
larch
"
    
}
    
"
kaios
"
:
{
        
"
target_tasks_method
"
:
"
kaios_tasks
"
    
}
    
"
toolchains
"
:
{
        
"
target_tasks_method
"
:
"
mozilla_central_tasks
"
    
}
    
"
firefox
"
:
{
        
"
target_tasks_method
"
:
"
firefox_pull_request_tasks
"
    
}
    
"
firefox
-
dev
"
:
{
        
"
enable_always_target
"
:
True
        
"
target_tasks_method
"
:
"
try_tasks
"
        
"
release_type
"
:
"
nightly
"
    
}
    
"
staging
-
firefox
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
full_task_graph_to_manifests_by_task
(
full_task_json
)
:
    
manifests_by_task
=
defaultdict
(
list
)
    
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
        
manifests
=
node
[
"
attributes
"
]
.
get
(
"
test_manifests
"
)
        
if
not
manifests
:
            
continue
        
manifests_by_task
[
label
]
.
extend
(
manifests
)
    
return
manifests_by_task
def
taskgraph_decision
(
options
parameters
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
    
The
parameters
argument
must
be
a
pre
-
resolved
Parameters
object
.
    
"
"
"
    
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
        
enable_verifications
=
options
.
get
(
"
verify
"
True
)
    
)
    
if
not
create
.
testing
:
        
set_decision_indexes
(
decision_task_id
tgg
.
parameters
tgg
.
graph_config
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
kind
-
graph
.
mm
"
format_kind_graph_mermaid
(
tgg
.
kind_graph
)
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
    
write_artifact
(
        
"
manifests
-
by
-
task
.
json
.
gz
"
        
full_task_graph_to_manifests_by_task
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
    
if
push_schedules
.
cache_info
(
)
.
currsize
>
0
:
        
write_artifact
(
            
"
bugbug
-
push
-
schedules
.
json
"
            
push_schedules
(
tgg
.
parameters
[
"
project
"
]
tgg
.
parameters
[
"
head_rev
"
]
)
        
)
    
mozharness_dir
=
Path
(
GECKO
"
testing
"
"
mozharness
"
)
    
scripts_dir
=
Path
(
GECKO
"
taskcluster
"
"
scripts
"
)
    
taskgraph_dir
=
Path
(
taskgraph
.
__file__
)
.
parent
    
to_copy
=
{
        
scripts_dir
/
"
run
-
task
"
:
f
"
{
ARTIFACTS_DIR
}
/
run
-
task
-
hg
"
        
scripts_dir
/
"
tester
"
/
"
test
-
linux
.
sh
"
:
ARTIFACTS_DIR
        
taskgraph_dir
/
"
run
-
task
"
/
"
fetch
-
content
"
:
ARTIFACTS_DIR
        
taskgraph_dir
/
"
run
-
task
"
/
"
run
-
task
"
:
f
"
{
ARTIFACTS_DIR
}
/
run
-
task
-
git
"
        
mozharness_dir
/
"
external_tools
"
/
"
robustcheckout
.
py
"
:
ARTIFACTS_DIR
    
}
    
for
target
dest
in
to_copy
.
items
(
)
:
        
shutil
.
copy2
(
target
dest
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
    
product_dir
=
graph_config
[
"
product
-
dir
"
]
    
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
base_ref
"
            
"
base_rev
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
owner
"
            
"
level
"
            
"
repository_type
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
    
repo_path
=
os
.
getcwd
(
)
    
repo
=
get_repository
(
repo_path
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
    
if
parameters
[
"
repository_type
"
]
=
=
"
hg
"
:
        
parameters
[
"
head_git_repository
"
]
=
GIT_BACKING_REPO
        
if
head_git_rev
:
=
get_hg_revision_info
(
            
GECKO
revision
=
parameters
[
"
head_rev
"
]
info
=
"
extras
.
git_commit
"
        
)
:
            
parameters
[
"
head_git_rev
"
]
=
head_git_rev
        
parameters
[
"
hg_branch
"
]
=
get_hg_revision_branch
(
            
GECKO
revision
=
parameters
[
"
head_rev
"
]
        
)
        
parameters
[
"
files_changed
"
]
=
sorted
(
            
get_changed_files
(
parameters
[
"
head_repository
"
]
parameters
[
"
head_rev
"
]
)
        
)
    
elif
parameters
[
"
repository_type
"
]
=
=
"
git
"
:
        
parameters
[
"
hg_branch
"
]
=
None
        
parameters
[
"
files_changed
"
]
=
repo
.
get_changed_files
(
            
rev
=
parameters
[
"
head_rev
"
]
base
=
parameters
[
"
base_rev
"
]
        
)
    
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
enable_always_target
"
]
=
[
"
docker
-
image
"
]
    
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
    
parameters
[
"
build_number
"
]
=
1
    
parameters
[
"
version
"
]
=
get_version
(
product_dir
)
    
parameters
[
"
app_version
"
]
=
get_app_version
(
product_dir
)
    
parameters
[
"
next_version
"
]
=
None
    
parameters
[
"
optimize_strategies
"
]
=
None
    
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
phabricator_diff
"
]
=
None
    
parameters
[
"
release_type
"
]
=
"
"
    
parameters
[
"
release_eta
"
]
=
"
"
    
parameters
[
"
release_enable_partner_repack
"
]
=
False
    
parameters
[
"
release_enable_partner_attribution
"
]
=
False
    
parameters
[
"
release_partners
"
]
=
[
]
    
parameters
[
"
release_partner_config
"
]
=
{
}
    
parameters
[
"
release_partner_build_number
"
]
=
1
    
parameters
[
"
release_enable_emefree
"
]
=
False
    
parameters
[
"
release_product
"
]
=
None
    
parameters
[
"
test_manifest_loader
"
]
=
"
default
"
    
parameters
[
"
try_mode
"
]
=
None
    
parameters
[
"
try_task_config
"
]
=
{
}
    
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
            
f
"
using
default
project
parameters
;
add
{
project
}
to
"
            
f
"
PER_PROJECT_PARAMETERS
in
{
__file__
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
parameters
.
get
(
"
tasks_for
"
"
"
)
.
startswith
(
"
github
-
pull
-
request
"
)
:
        
parameters
[
"
optimize_strategies
"
]
=
(
            
"
gecko_taskgraph
.
optimize
:
project
.
pull_request
"
        
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
options
.
get
(
"
include_push_tasks
"
)
:
        
get_existing_tasks
(
options
.
get
(
"
rebuild_kinds
"
[
]
)
parameters
graph_config
)
    
parameters
.
setdefault
(
"
release_history
"
dict
(
)
)
    
if
"
nightly
"
in
parameters
.
get
(
"
target_tasks_method
"
"
"
)
:
        
parameters
[
"
release_history
"
]
=
populate_release_history
(
"
Firefox
"
project
)
    
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
    
parameters
[
"
dontbuild
"
]
=
(
        
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
    
)
    
parameters
[
"
backstop
"
]
=
is_backstop
(
parameters
)
    
parameters
[
"
android_perftest_backstop
"
]
=
is_backstop
(
        
parameters
        
push_interval
=
30
        
time_interval
=
60
*
6
        
backstop_strategy
=
"
android_perftest_backstop
"
    
)
    
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
allow_parameter_override
"
)
:
        
note_ref
=
"
refs
/
notes
/
decision
-
parameters
"
        
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
os
.
path
.
isfile
(
task_config_file
)
:
            
set_try_config
(
parameters
task_config_file
)
            
parameters
[
"
try_mode
"
]
=
"
try_task_config
"
        
elif
note_params
:
=
repo
.
get_note
(
note_ref
parameters
[
"
head_repository
"
]
)
:
            
try
:
                
note_params
=
json
.
loads
(
note_params
)
                
logger
.
info
(
                    
f
"
Overriding
parameters
from
{
note_ref
}
:
\
n
{
json
.
dumps
(
note_params
indent
=
2
)
}
"
                
)
                
parameters
.
update
(
note_params
)
                
parameters
[
"
try_mode
"
]
=
"
try_task_config
"
            
except
ValueError
as
e
:
                
raise
Exception
(
f
"
Failed
to
parse
{
note_ref
}
as
JSON
:
{
e
}
"
)
from
e
    
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
get_existing_tasks
(
rebuild_kinds
parameters
graph_config
)
:
    
"
"
"
    
Find
the
decision
task
corresponding
to
the
on
-
push
graph
and
return
    
a
mapping
of
labels
to
task
-
ids
from
it
.
This
will
skip
the
kinds
specificed
    
by
rebuild_kinds
.
    
"
"
"
    
try
:
        
decision_task
=
retry
(
            
find_decision_task
            
args
=
(
parameters
graph_config
)
            
attempts
=
4
            
sleeptime
=
5
*
60
        
)
    
except
Exception
:
        
logger
.
exception
(
"
Didn
'
t
find
existing
push
task
.
"
)
        
sys
.
exit
(
1
)
    
_
task_graph
=
TaskGraph
.
from_json
(
        
get_artifact
(
decision_task
"
public
/
full
-
task
-
graph
.
json
"
)
    
)
    
parameters
[
"
existing_tasks
"
]
=
find_existing_tasks_from_previous_kinds
(
        
task_graph
[
decision_task
]
rebuild_kinds
    
)
def
set_try_config
(
parameters
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
1
)
    
if
task_config_version
=
=
1
:
        
parameters
[
"
try_task_config
"
]
=
task_config
    
elif
task_config_version
=
=
2
:
        
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
set_decision_indexes
(
decision_task_id
params
graph_config
)
:
    
index_paths
=
[
]
    
if
params
[
"
android_perftest_backstop
"
]
:
        
index_paths
.
insert
(
0
ANDROID_PERFTEST_BACKSTOP_INDEX
)
    
if
params
[
"
backstop
"
]
:
        
index_paths
.
insert
(
0
BACKSTOP_INDEX
)
    
subs
=
params
.
copy
(
)
    
subs
[
"
trust
-
domain
"
]
=
graph_config
[
"
trust
-
domain
"
]
    
for
index_path
in
index_paths
:
        
insert_index
(
index_path
.
format
(
*
*
subs
)
decision_task_id
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
)
    
elif
filename
.
endswith
(
"
.
json
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
.
encode
(
"
utf
-
8
"
)
)
    
else
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
            
f
.
write
(
data
)
def
read_artifact
(
filename
)
:
    
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
    
if
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
    
if
filename
.
endswith
(
"
.
json
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
os
.
path
.
join
(
ARTIFACTS_DIR
src
)
os
.
path
.
join
(
ARTIFACTS_DIR
dest
)
)
