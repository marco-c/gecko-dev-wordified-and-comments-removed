import
logging
from
datetime
import
datetime
from
taskgraph
import
files_changed
from
taskgraph
.
optimize
.
base
import
OptimizationStrategy
register_strategy
from
taskgraph
.
util
.
taskcluster
import
find_task_id
status_task
logger
=
logging
.
getLogger
(
__name__
)
register_strategy
(
"
index
-
search
"
)
class
IndexSearch
(
OptimizationStrategy
)
:
    
fmt
=
"
%
Y
-
%
m
-
%
dT
%
H
:
%
M
:
%
S
.
%
fZ
"
    
def
should_replace_task
(
self
task
params
deadline
index_paths
)
:
        
"
Look
for
a
task
with
one
of
the
given
index
paths
"
        
for
index_path
in
index_paths
:
            
try
:
                
task_id
=
find_task_id
(
index_path
)
                
status
=
status_task
(
task_id
)
                
if
not
status
or
status
.
get
(
"
state
"
)
in
(
"
exception
"
"
failed
"
)
:
                    
continue
                
if
deadline
and
datetime
.
strptime
(
                    
status
[
"
expires
"
]
self
.
fmt
                
)
<
datetime
.
strptime
(
deadline
self
.
fmt
)
:
                    
continue
                
return
task_id
            
except
KeyError
:
                
pass
        
return
False
register_strategy
(
"
skip
-
unless
-
changed
"
)
class
SkipUnlessChanged
(
OptimizationStrategy
)
:
    
def
should_remove_task
(
self
task
params
file_patterns
)
:
        
if
params
.
get
(
"
repository_type
"
)
!
=
"
hg
"
:
            
raise
RuntimeError
(
                
"
SkipUnlessChanged
optimization
only
works
with
mercurial
repositories
"
            
)
        
if
params
.
get
(
"
pushlog_id
"
)
=
=
-
1
:
            
return
False
        
changed
=
files_changed
.
check
(
params
file_patterns
)
        
if
not
changed
:
            
logger
.
debug
(
                
'
no
files
found
matching
a
pattern
in
skip
-
unless
-
changed
for
"
{
}
"
'
.
format
(
                    
task
.
label
                
)
            
)
            
return
True
        
return
False
