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
find_task_id
get_artifact
from
gecko_taskgraph
.
util
.
attributes
import
INTEGRATION_PROJECTS
TRY_PROJECTS
from
gecko_taskgraph
.
util
.
taskcluster
import
state_task
BACKSTOP_PUSH_INTERVAL
=
20
BACKSTOP_TIME_INTERVAL
=
60
*
4
ANDROID_PERFTEST_BACKSTOP_INDEX
=
(
    
"
{
trust
-
domain
}
.
v2
.
{
project
}
.
latest
.
taskgraph
.
android_backstop
"
)
BACKSTOP_INDEX
=
"
{
trust
-
domain
}
.
v2
.
{
project
}
.
latest
.
taskgraph
.
backstop
"
STRATEGY_TO_INDEX_MAP
=
{
    
"
android_perftest_backstop
"
:
ANDROID_PERFTEST_BACKSTOP_INDEX
    
"
backstop
"
:
BACKSTOP_INDEX
}
def
is_backstop
(
    
params
    
push_interval
=
BACKSTOP_PUSH_INTERVAL
    
time_interval
=
BACKSTOP_TIME_INTERVAL
    
trust_domain
=
"
gecko
"
    
integration_projects
=
INTEGRATION_PROJECTS
    
backstop_strategy
=
"
backstop
"
)
:
    
"
"
"
Determines
whether
the
given
parameters
represent
a
backstop
push
.
    
Args
:
        
push_interval
(
int
)
:
Number
of
pushes
        
time_interval
(
int
)
:
Minutes
between
forced
schedules
.
                             
Use
0
to
disable
.
        
trust_domain
(
str
)
:
"
gecko
"
for
Firefox
"
comm
"
for
Thunderbird
        
integration_projects
(
set
)
:
project
that
uses
backstop
optimization
    
Returns
:
        
bool
:
True
if
this
is
a
backstop
otherwise
False
.
    
"
"
"
    
if
params
.
get
(
backstop_strategy
False
)
:
        
return
True
    
if
params
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
        
return
True
    
project
=
params
[
"
project
"
]
    
if
project
in
TRY_PROJECTS
:
        
return
False
    
if
project
not
in
integration_projects
:
        
return
True
    
if
params
[
"
target_tasks_method
"
]
=
=
"
nothing
"
:
        
return
False
    
subs
=
{
"
trust
-
domain
"
:
trust_domain
"
project
"
:
project
}
    
index
=
STRATEGY_TO_INDEX_MAP
[
backstop_strategy
]
.
format
(
*
*
subs
)
    
try
:
        
last_backstop_id
=
find_task_id
(
index
)
    
except
TaskclusterRestFailure
:
        
return
True
    
if
state_task
(
last_backstop_id
)
in
(
"
failed
"
"
exception
"
)
:
        
return
True
    
try
:
        
last_params
=
get_artifact
(
last_backstop_id
"
public
/
parameters
.
yml
"
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
404
:
            
return
False
        
raise
    
if
int
(
params
[
"
pushlog_id
"
]
)
-
int
(
last_params
[
"
pushlog_id
"
]
)
>
=
push_interval
:
        
return
True
    
if
time_interval
<
=
0
:
        
return
False
    
if
(
params
[
"
pushdate
"
]
-
last_params
[
"
pushdate
"
]
)
/
60
>
=
time_interval
:
        
return
True
    
return
False
