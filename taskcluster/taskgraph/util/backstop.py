from
__future__
import
absolute_import
print_function
unicode_literals
from
requests
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
        
last_pushdate
=
get_artifact_from_index
(
index
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
True
        
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
