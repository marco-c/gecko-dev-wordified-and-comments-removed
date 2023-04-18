from
requests
import
HTTPError
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
(
    
find_task_id
    
get_artifact
    
state_task
)
BACKSTOP_PUSH_INTERVAL
=
20
BACKSTOP_TIME_INTERVAL
=
60
*
4
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
"
backstop
"
False
)
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
    
pushid
=
int
(
params
[
"
pushlog_id
"
]
)
    
pushdate
=
int
(
params
[
"
pushdate
"
]
)
    
if
project
in
TRY_PROJECTS
:
        
return
False
    
elif
project
not
in
integration_projects
:
        
return
True
    
if
pushid
%
push_interval
=
=
0
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
BACKSTOP_INDEX
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
KeyError
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
        
last_pushdate
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
[
            
"
pushdate
"
        
]
    
except
HTTPError
as
e
:
        
if
e
.
response
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
(
pushdate
-
last_pushdate
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
