import
unittest
from
pprint
import
pprint
from
unittest
.
mock
import
patch
import
pytest
from
mozunit
import
MockedOpen
main
from
taskgraph
import
create
from
taskgraph
.
util
import
json
taskcluster
from
taskgraph
.
util
.
taskcluster
import
_task_definitions_cache
from
gecko_taskgraph
import
actions
from
gecko_taskgraph
.
actions
.
util
import
(
    
_lower_priority
    
combine_task_graph_files
    
get_pushes_in_gap
    
relativize_datestamps
    
update_priority
)
from
gecko_taskgraph
.
decision
import
read_artifact
TASK_DEF
=
{
    
"
created
"
:
"
2017
-
10
-
10T18
:
33
:
03
.
460Z
"
    
"
deadline
"
:
"
2017
-
10
-
11T18
:
33
:
03
.
461Z
"
    
"
dependencies
"
:
[
]
    
"
expires
"
:
"
2018
-
10
-
10T18
:
33
:
04
.
461Z
"
    
"
payload
"
:
{
        
"
artifacts
"
:
{
            
"
public
"
:
{
                
"
expires
"
:
"
2018
-
10
-
10T18
:
33
:
03
.
463Z
"
                
"
path
"
:
"
/
builds
/
worker
/
artifacts
"
                
"
type
"
:
"
directory
"
            
}
        
}
        
"
maxRunTime
"
:
1800
    
}
}
pytest
.
fixture
(
scope
=
"
module
"
autouse
=
True
)
def
enable_test_mode
(
)
:
    
create
.
testing
=
True
    
taskcluster
.
testing
=
True
class
TestRelativize
(
unittest
.
TestCase
)
:
    
def
test_relativize
(
self
)
:
        
rel
=
relativize_datestamps
(
TASK_DEF
)
        
import
pprint
        
pprint
.
pprint
(
rel
)
        
assert
rel
[
"
created
"
]
=
=
{
"
relative
-
datestamp
"
:
"
0
seconds
"
}
        
assert
rel
[
"
deadline
"
]
=
=
{
"
relative
-
datestamp
"
:
"
86400
seconds
"
}
        
assert
rel
[
"
expires
"
]
=
=
{
"
relative
-
datestamp
"
:
"
31536001
seconds
"
}
        
assert
rel
[
"
payload
"
]
[
"
artifacts
"
]
[
"
public
"
]
[
"
expires
"
]
=
=
{
            
"
relative
-
datestamp
"
:
"
31536000
seconds
"
        
}
class
TestCombineTaskGraphFiles
(
unittest
.
TestCase
)
:
    
def
test_no_suffixes
(
self
)
:
        
with
MockedOpen
(
{
}
)
:
            
combine_task_graph_files
(
[
]
)
            
self
.
assertRaises
(
Exception
open
(
"
artifacts
/
to
-
run
.
json
"
)
)
    
patch
(
"
gecko_taskgraph
.
actions
.
util
.
rename_artifact
"
)
    
def
test_one_suffix
(
self
rename_artifact
)
:
        
combine_task_graph_files
(
[
"
0
"
]
)
        
rename_artifact
.
assert_any_call
(
"
task
-
graph
-
0
.
json
"
"
task
-
graph
.
json
"
)
        
rename_artifact
.
assert_any_call
(
            
"
label
-
to
-
taskid
-
0
.
json
"
"
label
-
to
-
taskid
.
json
"
        
)
        
rename_artifact
.
assert_any_call
(
"
to
-
run
-
0
.
json
"
"
to
-
run
.
json
"
)
    
def
test_several_suffixes
(
self
)
:
        
files
=
{
            
"
artifacts
/
task
-
graph
-
0
.
json
"
:
json
.
dumps
(
{
"
taska
"
:
{
}
}
)
            
"
artifacts
/
label
-
to
-
taskid
-
0
.
json
"
:
json
.
dumps
(
{
"
taska
"
:
"
TASKA
"
}
)
            
"
artifacts
/
to
-
run
-
0
.
json
"
:
json
.
dumps
(
[
"
taska
"
]
)
            
"
artifacts
/
task
-
graph
-
1
.
json
"
:
json
.
dumps
(
{
"
taskb
"
:
{
}
}
)
            
"
artifacts
/
label
-
to
-
taskid
-
1
.
json
"
:
json
.
dumps
(
{
"
taskb
"
:
"
TASKB
"
}
)
            
"
artifacts
/
to
-
run
-
1
.
json
"
:
json
.
dumps
(
[
"
taskb
"
]
)
        
}
        
with
MockedOpen
(
files
)
:
            
combine_task_graph_files
(
[
"
0
"
"
1
"
]
)
            
self
.
assertEqual
(
                
read_artifact
(
"
task
-
graph
.
json
"
)
                
{
                    
"
taska
"
:
{
}
                    
"
taskb
"
:
{
}
                
}
            
)
            
self
.
assertEqual
(
                
read_artifact
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
)
                
{
                    
"
taska
"
:
"
TASKA
"
                    
"
taskb
"
:
"
TASKB
"
                
}
            
)
            
self
.
assertEqual
(
                
sorted
(
read_artifact
(
"
to
-
run
.
json
"
)
)
                
[
                    
"
taska
"
                    
"
taskb
"
                
]
            
)
def
is_subset
(
subset
superset
)
:
    
if
isinstance
(
subset
dict
)
:
        
return
all
(
            
key
in
superset
and
is_subset
(
val
superset
[
key
]
)
            
for
key
val
in
subset
.
items
(
)
        
)
    
if
isinstance
(
subset
list
)
or
isinstance
(
subset
set
)
:
        
return
all
(
            
any
(
is_subset
(
subitem
superitem
)
for
superitem
in
superset
)
            
for
subitem
in
subset
        
)
    
if
isinstance
(
subset
str
)
:
        
return
subset
in
superset
    
return
subset
=
=
superset
pytest
.
mark
.
parametrize
(
    
"
task_def
expected
"
    
[
        
pytest
.
param
(
            
{
"
tags
"
:
{
"
kind
"
:
"
decision
-
task
"
}
}
            
{
                
"
hookPayload
"
:
{
                    
"
decision
"
:
{
                        
"
action
"
:
{
"
cb_name
"
:
"
retrigger
-
decision
"
}
                    
}
                
}
            
}
            
id
=
"
retrigger_decision
"
        
)
        
pytest
.
param
(
            
{
"
tags
"
:
{
"
action
"
:
"
backfill
-
task
"
}
}
            
{
                
"
hookPayload
"
:
{
                    
"
decision
"
:
{
                        
"
action
"
:
{
"
cb_name
"
:
"
retrigger
-
decision
"
}
                    
}
                
}
            
}
            
id
=
"
retrigger_backfill
"
        
)
    
]
)
def
test_extract_applicable_action
(
    
responses
monkeypatch
actions_json
task_def
expected
)
:
    
_task_definitions_cache
.
cache
.
clear
(
)
    
base_url
=
"
https
:
/
/
taskcluster
"
    
decision_task_id
=
"
dddd
"
    
task_id
=
"
tttt
"
    
monkeypatch
.
setenv
(
"
TASK_ID
"
task_id
)
    
monkeypatch
.
setenv
(
"
TASKCLUSTER_ROOT_URL
"
base_url
)
    
monkeypatch
.
setenv
(
"
TASKCLUSTER_PROXY_URL
"
base_url
)
    
responses
.
add
(
        
responses
.
GET
        
f
"
{
base_url
}
/
api
/
queue
/
v1
/
task
/
{
task_id
}
"
        
status
=
200
        
json
=
task_def
    
)
    
action
=
actions
.
util
.
_extract_applicable_action
(
        
actions_json
"
retrigger
"
decision_task_id
task_id
    
)
    
pprint
(
action
indent
=
2
)
    
assert
is_subset
(
expected
action
)
def
test_get_pushes_in_gap_finds_boundary
(
mocker
)
:
    
"
"
"
Stop
early
when
a
push
with
the
label
is
found
within
first
chunk
.
"
"
"
    
label
=
"
raptor
-
browsertime
-
firefox
-
tp6
"
    
parameters
=
{
        
"
pushlog_id
"
:
"
125
"
        
"
head_repository
"
:
"
https
:
/
/
hg
.
mozilla
.
org
/
mozilla
-
central
"
        
"
project
"
:
"
mozilla
-
central
"
    
}
    
mocker
.
patch
(
        
"
gecko_taskgraph
.
actions
.
util
.
get_pushes
"
        
return_value
=
[
str
(
i
)
for
i
in
range
(
100
125
)
]
    
)
    
def
fake_label_to_taskid
(
project
push_id
)
:
        
if
push_id
=
=
"
106
"
:
            
return
{
label
:
"
task
-
abc
"
}
        
return
{
}
    
mocker
.
patch
(
        
"
gecko_taskgraph
.
actions
.
util
.
get_label_to_taskid
"
        
side_effect
=
fake_label_to_taskid
    
)
    
result
=
get_pushes_in_gap
(
parameters
label
)
    
assert
result
=
=
[
str
(
i
)
for
i
in
range
(
107
125
)
]
def
test_get_pushes_in_gap_no_boundary_found
(
mocker
)
:
    
"
"
"
Return
all
fetched
pushes
when
no
boundary
is
found
within
max
depth
.
"
"
"
    
label
=
"
raptor
-
browsertime
-
firefox
-
tp6
"
    
parameters
=
{
        
"
pushlog_id
"
:
"
125
"
        
"
head_repository
"
:
"
https
:
/
/
hg
.
mozilla
.
org
/
mozilla
-
central
"
        
"
project
"
:
"
mozilla
-
central
"
    
}
    
mocker
.
patch
(
        
"
gecko_taskgraph
.
actions
.
util
.
get_pushes
"
        
side_effect
=
[
            
[
str
(
i
)
for
i
in
range
(
100
125
)
]
            
[
str
(
i
)
for
i
in
range
(
75
100
)
]
            
[
str
(
i
)
for
i
in
range
(
50
75
)
]
            
[
str
(
i
)
for
i
in
range
(
25
50
)
]
        
]
    
)
    
mocker
.
patch
(
        
"
gecko_taskgraph
.
actions
.
util
.
get_label_to_taskid
"
        
return_value
=
{
}
    
)
    
result
=
get_pushes_in_gap
(
parameters
label
)
    
assert
result
=
=
[
str
(
i
)
for
i
in
range
(
25
125
)
]
def
test_get_pushes_in_gap_boundary_at_first_push
(
mocker
)
:
    
"
"
"
    
Boundary
found
at
the
first
searched
push
(
124
newest
push
)
    
so
no
pushes
are
added
to
gap
before
returning
    
"
"
"
    
label
=
"
raptor
-
browsertime
-
firefox
-
tp6
"
    
parameters
=
{
        
"
pushlog_id
"
:
"
125
"
        
"
head_repository
"
:
"
https
:
/
/
hg
.
mozilla
.
org
/
mozilla
-
central
"
        
"
project
"
:
"
mozilla
-
central
"
    
}
    
mocker
.
patch
(
        
"
gecko_taskgraph
.
actions
.
util
.
get_pushes
"
        
return_value
=
[
str
(
i
)
for
i
in
range
(
100
125
)
]
    
)
    
def
_label_map
(
project
push_id
)
:
        
if
push_id
=
=
"
124
"
:
            
return
{
label
:
"
task
-
abc
"
}
        
return
{
}
    
mocker
.
patch
(
        
"
gecko_taskgraph
.
actions
.
util
.
get_label_to_taskid
"
        
side_effect
=
_label_map
    
)
    
result
=
get_pushes_in_gap
(
parameters
label
)
    
assert
result
=
=
[
]
pytest
.
mark
.
parametrize
(
    
"
current
new_priority
expected
"
    
[
        
(
"
high
"
"
very
-
low
"
"
very
-
low
"
)
        
(
"
low
"
"
very
-
low
"
"
very
-
low
"
)
        
(
"
very
-
low
"
"
very
-
low
"
"
very
-
low
"
)
        
(
"
lowest
"
"
very
-
low
"
"
lowest
"
)
        
(
None
"
very
-
low
"
"
very
-
low
"
)
        
(
"
high
"
"
unknown
"
"
high
"
)
    
]
)
def
test_lower_priority
(
current
new_priority
expected
)
:
    
assert
_lower_priority
(
current
new_priority
)
=
=
expected
pytest
.
mark
.
parametrize
(
    
"
initial_priority
"
    
[
"
highest
"
"
very
-
high
"
"
high
"
"
medium
"
"
low
"
]
)
def
test_update_priority_lowers_to_very_low
(
initial_priority
)
:
    
task
=
unittest
.
mock
.
MagicMock
(
)
    
task
.
task
=
{
"
priority
"
:
initial_priority
}
    
update_priority
(
task
graph
=
None
max_priority
=
"
very
-
low
"
)
    
assert
task
.
task
[
"
priority
"
]
=
=
"
very
-
low
"
def
test_update_priority_does_not_raise_when_already_lowest
(
)
:
    
task
=
unittest
.
mock
.
MagicMock
(
)
    
task
.
task
=
{
"
priority
"
:
"
lowest
"
}
    
update_priority
(
task
graph
=
None
max_priority
=
"
very
-
low
"
)
    
assert
task
.
task
[
"
priority
"
]
=
=
"
lowest
"
def
test_update_priority_sets_very_low_when_no_priority
(
)
:
    
task
=
unittest
.
mock
.
MagicMock
(
)
    
task
.
task
=
{
}
    
update_priority
(
task
graph
=
None
max_priority
=
"
very
-
low
"
)
    
assert
task
.
task
[
"
priority
"
]
=
=
"
very
-
low
"
def
test_update_priority_not_applied_by_default_in_create_task_from_def
(
monkeypatch
)
:
    
"
"
"
Release
-
critical
actions
that
don
'
t
pass
priority
=
keep
their
priority
.
"
"
"
    
created
=
[
]
    
monkeypatch
.
setattr
(
"
gecko_taskgraph
.
actions
.
util
.
get_session
"
lambda
:
None
)
    
monkeypatch
.
setattr
(
        
"
gecko_taskgraph
.
actions
.
util
.
create
.
create_task
"
        
lambda
session
task_id
label
task_def
:
created
.
append
(
task_def
.
copy
(
)
)
    
)
    
from
gecko_taskgraph
.
actions
.
util
import
create_task_from_def
    
task_def
=
{
        
"
priority
"
:
"
high
"
        
"
schedulerId
"
:
"
"
        
"
metadata
"
:
{
"
name
"
:
"
test
-
task
"
}
        
"
tags
"
:
{
}
    
}
    
create_task_from_def
(
task_def
level
=
1
)
    
assert
created
[
0
]
[
"
priority
"
]
=
=
"
high
"
def
test_update_priority_applied_when_opted_in_in_create_task_from_def
(
monkeypatch
)
:
    
"
"
"
Backfill
/
retrigger
actions
that
pass
priority
=
get
very
-
low
.
"
"
"
    
created
=
[
]
    
monkeypatch
.
setattr
(
"
gecko_taskgraph
.
actions
.
util
.
get_session
"
lambda
:
None
)
    
monkeypatch
.
setattr
(
        
"
gecko_taskgraph
.
actions
.
util
.
create
.
create_task
"
        
lambda
session
task_id
label
task_def
:
created
.
append
(
task_def
.
copy
(
)
)
    
)
    
from
gecko_taskgraph
.
actions
.
util
import
create_task_from_def
    
task_def
=
{
        
"
priority
"
:
"
high
"
        
"
schedulerId
"
:
"
"
        
"
metadata
"
:
{
"
name
"
:
"
test
-
task
"
}
        
"
tags
"
:
{
}
    
}
    
create_task_from_def
(
task_def
level
=
1
max_priority
=
"
very
-
low
"
)
    
assert
created
[
0
]
[
"
priority
"
]
=
=
"
very
-
low
"
def
test_update_priority_does_not_raise_lowest_in_create_task_from_def
(
monkeypatch
)
:
    
"
"
"
priority
=
must
not
bump
a
task
that
is
already
lowest
.
"
"
"
    
created
=
[
]
    
monkeypatch
.
setattr
(
"
gecko_taskgraph
.
actions
.
util
.
get_session
"
lambda
:
None
)
    
monkeypatch
.
setattr
(
        
"
gecko_taskgraph
.
actions
.
util
.
create
.
create_task
"
        
lambda
session
task_id
label
task_def
:
created
.
append
(
task_def
.
copy
(
)
)
    
)
    
from
gecko_taskgraph
.
actions
.
util
import
create_task_from_def
    
task_def
=
{
        
"
priority
"
:
"
lowest
"
        
"
schedulerId
"
:
"
"
        
"
metadata
"
:
{
"
name
"
:
"
test
-
task
"
}
        
"
tags
"
:
{
}
    
}
    
create_task_from_def
(
task_def
level
=
1
max_priority
=
"
very
-
low
"
)
    
assert
created
[
0
]
[
"
priority
"
]
=
=
"
lowest
"
if
__name__
=
=
"
__main__
"
:
    
main
(
)
