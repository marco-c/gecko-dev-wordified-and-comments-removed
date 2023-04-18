import
logging
from
datetime
import
datetime
import
mozpack
.
path
as
mozpath
from
mozbuild
.
base
import
MozbuildObject
from
mozbuild
.
util
import
memoize
from
taskgraph
.
util
.
taskcluster
import
find_task_id
from
gecko_taskgraph
import
files_changed
from
gecko_taskgraph
.
optimize
import
register_strategy
OptimizationStrategy
from
gecko_taskgraph
.
util
.
taskcluster
import
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
                
"
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
                
+
task
.
label
            
)
            
return
True
        
return
False
register_strategy
(
"
skip
-
unless
-
schedules
"
)
class
SkipUnlessSchedules
(
OptimizationStrategy
)
:
    
memoize
    
def
scheduled_by_push
(
self
repository
revision
)
:
        
changed_files
=
files_changed
.
get_changed_files
(
repository
revision
)
        
mbo
=
MozbuildObject
.
from_environment
(
)
        
rdr
=
mbo
.
mozbuild_reader
(
config_mode
=
"
empty
"
)
        
components
=
set
(
)
        
for
p
m
in
rdr
.
files_info
(
changed_files
)
.
items
(
)
:
            
components
|
=
set
(
m
[
"
SCHEDULES
"
]
.
components
)
        
return
components
    
def
should_remove_task
(
self
task
params
conditions
)
:
        
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
        
scheduled
=
self
.
scheduled_by_push
(
            
params
[
"
head_repository
"
]
params
[
"
head_rev
"
]
        
)
        
conditions
=
set
(
conditions
)
        
if
conditions
&
scheduled
:
            
return
False
        
return
True
register_strategy
(
"
skip
-
unless
-
has
-
relevant
-
tests
"
)
class
SkipUnlessHasRelevantTests
(
OptimizationStrategy
)
:
    
"
"
"
Optimizes
tasks
that
don
'
t
run
any
tests
that
were
    
in
child
directories
of
a
modified
file
.
    
"
"
"
    
memoize
    
def
get_changed_dirs
(
self
repo
rev
)
:
        
changed
=
map
(
mozpath
.
dirname
files_changed
.
get_changed_files
(
repo
rev
)
)
        
return
{
d
for
d
in
changed
if
d
}
    
def
should_remove_task
(
self
task
params
_
)
:
        
if
not
task
.
attributes
.
get
(
"
test_manifests
"
)
:
            
return
True
        
for
d
in
self
.
get_changed_dirs
(
params
[
"
head_repository
"
]
params
[
"
head_rev
"
]
)
:
            
for
t
in
task
.
attributes
[
"
test_manifests
"
]
:
                
if
t
.
startswith
(
d
)
:
                    
logger
.
debug
(
                        
"
{
}
runs
a
test
path
(
{
}
)
contained
by
a
modified
file
(
{
}
)
"
.
format
(
                            
task
.
label
t
d
                        
)
                    
)
                    
return
False
        
return
True
