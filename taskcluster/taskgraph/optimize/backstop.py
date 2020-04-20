from
__future__
import
absolute_import
print_function
unicode_literals
import
logging
from
collections
import
defaultdict
import
requests
from
redo
import
retry
from
taskgraph
.
optimize
import
OptimizationStrategy
register_strategy
logger
=
logging
.
getLogger
(
__name__
)
PUSH_ENDPOINT
=
"
{
head_repository
}
/
json
-
pushes
/
?
startID
=
{
push_id_start
}
&
endID
=
{
push_id_end
}
"
register_strategy
(
'
backstop
'
args
=
(
10
60
)
)
class
Backstop
(
OptimizationStrategy
)
:
    
"
"
"
Ensures
that
no
task
gets
left
behind
.
    
Will
schedule
all
tasks
either
every
Nth
push
or
M
minutes
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
    
"
"
"
    
def
__init__
(
self
push_interval
time_interval
)
:
        
self
.
push_interval
=
push_interval
        
self
.
time_interval
=
time_interval
        
self
.
push_dates
=
defaultdict
(
dict
)
        
self
.
failed_json_push_calls
=
[
]
    
def
should_remove_task
(
self
task
params
_
)
:
        
project
=
params
[
'
project
'
]
        
pushid
=
int
(
params
[
'
pushlog_id
'
]
)
        
pushdate
=
int
(
params
[
'
pushdate
'
]
)
        
if
project
!
=
'
autoland
'
:
            
return
True
        
if
pushid
%
self
.
push_interval
=
=
0
:
            
return
False
        
if
self
.
minutes_between_pushes
(
                
params
[
"
head_repository
"
]
                
project
                
pushid
                
pushdate
)
>
=
self
.
time_interval
:
            
return
False
        
return
True
    
def
minutes_between_pushes
(
self
repository
project
cur_push_id
cur_push_date
)
:
        
min_between_pushes
=
self
.
time_interval
        
prev_push_id
=
cur_push_id
-
1
        
self
.
push_dates
[
project
]
.
update
(
{
cur_push_id
:
cur_push_date
}
)
        
prev_push_date
=
self
.
push_dates
[
project
]
.
get
(
prev_push_id
0
)
        
if
cur_push_date
>
0
and
prev_push_date
>
0
:
            
return
(
cur_push_date
-
prev_push_date
)
/
60
        
if
prev_push_id
in
self
.
failed_json_push_calls
:
            
return
min_between_pushes
        
url
=
PUSH_ENDPOINT
.
format
(
            
head_repository
=
repository
            
push_id_start
=
prev_push_id
-
1
            
push_id_end
=
prev_push_id
        
)
        
try
:
            
response
=
retry
(
requests
.
get
attempts
=
2
sleeptime
=
10
                             
args
=
(
url
)
                             
kwargs
=
{
'
timeout
'
:
60
'
headers
'
:
{
'
User
-
Agent
'
:
'
TaskCluster
'
}
}
)
            
prev_push_date
=
response
.
json
(
)
.
get
(
str
(
prev_push_id
)
{
}
)
.
get
(
'
date
'
0
)
            
self
.
push_dates
[
project
]
.
update
(
{
prev_push_id
:
prev_push_date
}
)
            
if
cur_push_date
>
0
and
prev_push_date
>
0
:
                
min_between_pushes
=
(
cur_push_date
-
prev_push_date
)
/
60
        
except
requests
.
exceptions
.
Timeout
:
            
logger
.
warning
(
"
json
-
pushes
timeout
enabling
backstop
"
)
            
self
.
failed_json_push_calls
.
append
(
prev_push_id
)
        
except
requests
.
exceptions
.
ConnectionError
:
            
logger
.
warning
(
"
json
-
pushes
connection
error
enabling
backstop
"
)
            
self
.
failed_json_push_calls
.
append
(
prev_push_id
)
        
except
requests
.
exceptions
.
HTTPError
:
            
logger
.
warning
(
"
Bad
Http
response
enabling
backstop
"
)
            
self
.
failed_json_push_calls
.
append
(
prev_push_id
)
        
except
ValueError
as
error
:
            
logger
.
warning
(
"
Invalid
JSON
possible
server
error
:
{
}
"
.
format
(
error
)
)
            
self
.
failed_json_push_calls
.
append
(
prev_push_id
)
        
except
requests
.
exceptions
.
RequestException
as
error
:
            
logger
.
warning
(
error
)
            
self
.
failed_json_push_calls
.
append
(
prev_push_id
)
        
return
min_between_pushes
