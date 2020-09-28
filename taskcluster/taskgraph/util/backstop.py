from
__future__
import
absolute_import
print_function
unicode_literals
from
taskgraph
.
util
.
taskcluster
import
(
    
find_task_id
    
get_artifact
    
status_task
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
gecko
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
    
Returns
:
        
bool
:
True
if
this
is
a
backtop
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
'
backstop
'
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
=
=
"
try
"
:
        
return
False
    
elif
project
!
=
"
autoland
"
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
    
index
=
BACKSTOP_INDEX
.
format
(
project
=
project
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
status_task
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
    
last_pushdate
=
get_artifact
(
last_backstop_id
'
public
/
parameters
.
yml
'
)
[
"
pushdate
"
]
    
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
