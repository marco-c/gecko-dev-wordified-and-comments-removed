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
json
import
yaml
from
mozbuild
.
util
import
ReadOnlyDict
PARAMETER_NAMES
=
set
(
[
    
'
base_repository
'
    
'
build_date
'
    
'
filters
'
    
'
head_ref
'
    
'
head_repository
'
    
'
head_rev
'
    
'
level
'
    
'
message
'
    
'
moz_build_date
'
    
'
optimize_target_tasks
'
    
'
owner
'
    
'
project
'
    
'
pushdate
'
    
'
pushlog_id
'
    
'
target_tasks_method
'
    
'
triggered_by
'
]
)
class
Parameters
(
ReadOnlyDict
)
:
    
"
"
"
An
immutable
dictionary
with
nicer
KeyError
messages
on
failure
"
"
"
    
def
check
(
self
)
:
        
names
=
set
(
self
)
        
msg
=
[
]
        
missing
=
PARAMETER_NAMES
-
names
        
if
missing
:
            
msg
.
append
(
"
missing
parameters
:
"
+
"
"
.
join
(
missing
)
)
        
extra
=
names
-
PARAMETER_NAMES
        
if
extra
:
            
msg
.
append
(
"
extra
parameters
:
"
+
"
"
.
join
(
extra
)
)
        
if
msg
:
            
raise
Exception
(
"
;
"
.
join
(
msg
)
)
    
def
__getitem__
(
self
k
)
:
        
if
k
not
in
PARAMETER_NAMES
:
            
raise
KeyError
(
"
no
such
parameter
{
!
r
}
"
.
format
(
k
)
)
        
try
:
            
return
super
(
Parameters
self
)
.
__getitem__
(
k
)
        
except
KeyError
:
            
raise
KeyError
(
"
taskgraph
parameter
{
!
r
}
not
found
"
.
format
(
k
)
)
def
load_parameters_file
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
-
-
parameters
option
    
"
"
"
    
import
urllib
    
from
taskgraph
.
util
.
taskcluster
import
get_artifact_url
    
filename
=
options
[
'
parameters
'
]
    
if
not
filename
:
        
return
Parameters
(
)
    
try
:
        
f
=
open
(
filename
)
    
except
IOError
:
        
if
filename
.
startswith
(
"
task
-
id
=
"
)
:
            
task_id
=
filename
.
split
(
"
=
"
)
[
1
]
            
filename
=
get_artifact_url
(
task_id
'
public
/
parameters
.
yml
'
)
        
f
=
urllib
.
urlopen
(
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
        
return
Parameters
(
*
*
yaml
.
safe_load
(
f
)
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
        
return
Parameters
(
*
*
json
.
load
(
f
)
)
    
else
:
        
raise
TypeError
(
"
Parameters
file
{
}
is
not
JSON
or
YAML
"
.
format
(
filename
)
)
