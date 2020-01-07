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
jsone
import
pipes
import
yaml
import
os
import
slugid
from
taskgraph
.
util
.
time
import
current_json_time
def
run_decision_task
(
job
params
root
)
:
    
arguments
=
[
]
    
if
'
target
-
tasks
-
method
'
in
job
:
        
arguments
.
append
(
'
-
-
target
-
tasks
-
method
=
{
}
'
.
format
(
job
[
'
target
-
tasks
-
method
'
]
)
)
    
return
[
        
make_decision_task
(
            
params
            
symbol
=
job
[
'
treeherder
-
symbol
'
]
            
arguments
=
arguments
            
root
=
root
)
    
]
def
make_decision_task
(
params
root
symbol
arguments
=
[
]
head_rev
=
None
)
:
    
"
"
"
Generate
a
basic
decision
task
based
on
the
root
.
taskcluster
.
yml
"
"
"
    
with
open
(
os
.
path
.
join
(
root
'
.
taskcluster
.
yml
'
)
'
rb
'
)
as
f
:
        
taskcluster_yml
=
yaml
.
safe_load
(
f
)
    
if
not
head_rev
:
        
head_rev
=
params
[
'
head_rev
'
]
    
slugids
=
{
}
    
def
as_slugid
(
name
)
:
        
name
=
name
[
0
]
        
if
name
not
in
slugids
:
            
slugids
[
name
]
=
slugid
.
nice
(
)
        
return
slugids
[
name
]
    
context
=
{
        
'
tasks_for
'
:
'
cron
'
        
'
repository
'
:
{
            
'
url
'
:
params
[
'
repository_url
'
]
            
'
project
'
:
params
[
'
project
'
]
            
'
level
'
:
params
[
'
level
'
]
        
}
        
'
push
'
:
{
            
'
revision
'
:
params
[
'
head_rev
'
]
            
'
pushlog_id
'
:
-
1
            
'
pushdate
'
:
0
            
'
owner
'
:
'
cron
'
            
'
comment
'
:
'
'
        
}
        
'
cron
'
:
{
            
'
task_id
'
:
os
.
environ
.
get
(
'
TASK_ID
'
'
<
cron
task
id
>
'
)
            
'
job_name
'
:
params
[
'
job_name
'
]
            
'
job_symbol
'
:
symbol
            
'
quoted_args
'
:
'
'
.
join
(
pipes
.
quote
(
a
)
for
a
in
arguments
)
        
}
        
'
now
'
:
current_json_time
(
)
        
'
as_slugid
'
:
as_slugid
    
}
    
rendered
=
jsone
.
render
(
taskcluster_yml
context
)
    
if
len
(
rendered
[
'
tasks
'
]
)
!
=
1
:
        
raise
Exception
(
"
Expected
.
taskcluster
.
yml
to
only
produce
one
cron
task
"
)
    
task
=
rendered
[
'
tasks
'
]
[
0
]
    
task_id
=
task
.
pop
(
'
taskId
'
)
    
return
(
task_id
task
)
