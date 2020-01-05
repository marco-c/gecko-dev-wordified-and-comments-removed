import
argparse
from
functools
import
partial
reduce
import
json
import
operator
import
os
import
random
import
string
from
thclient
import
(
TreeherderClient
TreeherderResultSetCollection
                      
TreeherderJobCollection
)
import
time
from
runner
import
format_result_summary
def
geometric_mean
(
iterable
)
:
        
filtered
=
list
(
filter
(
lambda
x
:
x
>
0
iterable
)
)
        
return
(
reduce
(
operator
.
mul
filtered
)
)
*
*
(
1
.
0
/
len
(
filtered
)
)
def
format_testcase_name
(
name
)
:
    
temp
=
name
.
replace
(
'
http
:
/
/
localhost
:
8000
/
page_load_test
/
'
'
'
)
    
temp
=
temp
.
replace
(
'
http
:
/
/
localhost
:
8000
/
tp6
/
'
'
'
)
    
temp
=
temp
.
split
(
'
/
'
)
[
0
]
    
temp
=
temp
[
0
:
80
]
    
return
temp
def
format_perf_data
(
perf_json
engine
=
'
servo
'
)
:
    
suites
=
[
]
    
measurement
=
"
domComplete
"
    
def
get_time_from_nav_start
(
timings
measurement
)
:
        
return
timings
[
measurement
]
-
timings
[
'
navigationStart
'
]
    
measurementFromNavStart
=
partial
(
get_time_from_nav_start
                                      
measurement
=
measurement
)
    
if
(
engine
=
=
'
gecko
'
)
:
        
name
=
'
gecko
.
{
}
'
.
format
(
measurement
)
    
else
:
        
name
=
measurement
    
suite
=
{
        
"
name
"
:
name
        
"
value
"
:
geometric_mean
(
map
(
measurementFromNavStart
perf_json
)
)
        
"
subtests
"
:
[
]
    
}
    
for
testcase
in
perf_json
:
        
if
measurementFromNavStart
(
testcase
)
<
0
:
            
value
=
-
1
        
else
:
            
value
=
measurementFromNavStart
(
testcase
)
        
suite
[
"
subtests
"
]
.
append
(
{
            
"
name
"
:
format_testcase_name
(
testcase
[
"
testcase
"
]
)
            
"
value
"
:
value
        
}
)
    
suites
.
append
(
suite
)
    
return
{
        
"
performance_data
"
:
{
            
"
framework
"
:
{
"
name
"
:
"
servo
-
perf
"
}
            
"
suites
"
:
suites
        
}
    
}
def
create_resultset_collection
(
dataset
)
:
    
print
(
"
[
DEBUG
]
ResultSet
Collection
:
"
)
    
print
(
dataset
)
    
trsc
=
TreeherderResultSetCollection
(
)
    
for
data
in
dataset
:
        
trs
=
trsc
.
get_resultset
(
)
        
trs
.
add_push_timestamp
(
data
[
'
push_timestamp
'
]
)
        
trs
.
add_revision
(
data
[
'
revision
'
]
)
        
trs
.
add_author
(
data
[
'
author
'
]
)
        
revisions
=
[
]
        
for
rev
in
data
[
'
revisions
'
]
:
            
tr
=
trs
.
get_revision
(
)
            
tr
.
add_revision
(
rev
[
'
revision
'
]
)
            
tr
.
add_author
(
rev
[
'
author
'
]
)
            
tr
.
add_comment
(
rev
[
'
comment
'
]
)
            
tr
.
add_repository
(
rev
[
'
repository
'
]
)
            
revisions
.
append
(
tr
)
        
trs
.
add_revisions
(
revisions
)
        
trsc
.
add
(
trs
)
    
return
trsc
def
create_job_collection
(
dataset
)
:
    
print
(
"
[
DEBUG
]
Job
Collection
:
"
)
    
print
(
dataset
)
    
tjc
=
TreeherderJobCollection
(
)
    
for
data
in
dataset
:
        
tj
=
tjc
.
get_job
(
)
        
tj
.
add_revision
(
data
[
'
revision
'
]
)
        
tj
.
add_project
(
data
[
'
project
'
]
)
        
tj
.
add_coalesced_guid
(
data
[
'
job
'
]
[
'
coalesced
'
]
)
        
tj
.
add_job_guid
(
data
[
'
job
'
]
[
'
job_guid
'
]
)
        
tj
.
add_job_name
(
data
[
'
job
'
]
[
'
name
'
]
)
        
tj
.
add_job_symbol
(
data
[
'
job
'
]
[
'
job_symbol
'
]
)
        
tj
.
add_group_name
(
data
[
'
job
'
]
[
'
group_name
'
]
)
        
tj
.
add_group_symbol
(
data
[
'
job
'
]
[
'
group_symbol
'
]
)
        
tj
.
add_description
(
data
[
'
job
'
]
[
'
desc
'
]
)
        
tj
.
add_product_name
(
data
[
'
job
'
]
[
'
product_name
'
]
)
        
tj
.
add_state
(
data
[
'
job
'
]
[
'
state
'
]
)
        
tj
.
add_result
(
data
[
'
job
'
]
[
'
result
'
]
)
        
tj
.
add_reason
(
data
[
'
job
'
]
[
'
reason
'
]
)
        
tj
.
add_who
(
data
[
'
job
'
]
[
'
who
'
]
)
        
tj
.
add_tier
(
data
[
'
job
'
]
[
'
tier
'
]
)
        
tj
.
add_submit_timestamp
(
data
[
'
job
'
]
[
'
submit_timestamp
'
]
)
        
tj
.
add_start_timestamp
(
data
[
'
job
'
]
[
'
start_timestamp
'
]
)
        
tj
.
add_end_timestamp
(
data
[
'
job
'
]
[
'
end_timestamp
'
]
)
        
tj
.
add_machine
(
data
[
'
job
'
]
[
'
machine
'
]
)
        
tj
.
add_build_info
(
            
data
[
'
job
'
]
[
'
build_platform
'
]
[
'
os_name
'
]
            
data
[
'
job
'
]
[
'
build_platform
'
]
[
'
platform
'
]
            
data
[
'
job
'
]
[
'
build_platform
'
]
[
'
architecture
'
]
        
)
        
tj
.
add_machine_info
(
            
data
[
'
job
'
]
[
'
machine_platform
'
]
[
'
os_name
'
]
            
data
[
'
job
'
]
[
'
machine_platform
'
]
[
'
platform
'
]
            
data
[
'
job
'
]
[
'
machine_platform
'
]
[
'
architecture
'
]
        
)
        
tj
.
add_option_collection
(
data
[
'
job
'
]
[
'
option_collection
'
]
)
        
for
artifact_data
in
data
[
'
job
'
]
[
'
artifacts
'
]
:
            
tj
.
add_artifact
(
                
artifact_data
[
'
name
'
]
                
artifact_data
[
'
type
'
]
                
artifact_data
[
'
blob
'
]
            
)
        
tjc
.
add
(
tj
)
        
return
tjc
def
submit
(
perf_data
failures
revision
summary
engine
)
:
    
print
(
"
[
DEBUG
]
failures
:
"
)
    
print
(
list
(
map
(
lambda
x
:
x
[
'
testcase
'
]
failures
)
)
)
    
author
=
"
{
}
<
{
}
>
"
.
format
(
revision
[
'
author
'
]
[
'
name
'
]
                              
revision
[
'
author
'
]
[
'
email
'
]
)
    
dataset
=
[
        
{
            
'
revision
'
:
revision
[
'
commit
'
]
            
'
author
'
:
author
            
'
push_timestamp
'
:
int
(
revision
[
'
author
'
]
[
'
timestamp
'
]
)
            
'
type
'
:
'
push
'
            
'
revisions
'
:
[
                
{
                    
'
comment
'
:
revision
[
'
subject
'
]
                    
'
revision
'
:
revision
[
'
commit
'
]
                    
'
repository
'
:
'
servo
'
                    
'
author
'
:
author
                
}
            
]
        
}
    
]
    
trsc
=
create_resultset_collection
(
dataset
)
    
result
=
"
success
"
    
hashlen
=
len
(
revision
[
'
commit
'
]
)
    
job_guid
=
'
'
.
join
(
        
random
.
choice
(
string
.
ascii_letters
+
string
.
digits
)
for
i
in
range
(
hashlen
)
    
)
    
if
(
engine
=
=
"
gecko
"
)
:
        
project
=
"
servo
"
        
job_symbol
=
'
PLG
'
        
group_symbol
=
'
SPG
'
        
group_name
=
'
Servo
Perf
on
Gecko
'
    
else
:
        
project
=
"
servo
"
        
job_symbol
=
'
PL
'
        
group_symbol
=
'
SP
'
        
group_name
=
'
Servo
Perf
'
    
dataset
=
[
        
{
            
'
project
'
:
project
            
'
revision
'
:
revision
[
'
commit
'
]
            
'
job
'
:
{
                
'
job_guid
'
:
job_guid
                
'
product_name
'
:
project
                
'
reason
'
:
'
scheduler
'
                
'
who
'
:
'
Servo
'
                
'
desc
'
:
'
Servo
Page
Load
Time
Tests
'
                
'
name
'
:
'
Servo
Page
Load
Time
'
                
'
job_symbol
'
:
job_symbol
                
'
group_symbol
'
:
group_symbol
                
'
group_name
'
:
group_name
                
'
submit_timestamp
'
:
str
(
int
(
time
.
time
(
)
)
)
                
'
start_timestamp
'
:
str
(
int
(
time
.
time
(
)
)
)
                
'
end_timestamp
'
:
str
(
int
(
time
.
time
(
)
)
)
                
'
state
'
:
'
completed
'
                
'
result
'
:
result
                
'
machine
'
:
'
local
-
machine
'
                
'
build_platform
'
:
{
                    
'
platform
'
:
'
linux64
'
                    
'
os_name
'
:
'
linux
'
                    
'
architecture
'
:
'
x86_64
'
                
}
                
'
machine_platform
'
:
{
                    
'
platform
'
:
'
linux64
'
                    
'
os_name
'
:
'
linux
'
                    
'
architecture
'
:
'
x86_64
'
                
}
                
'
option_collection
'
:
{
'
opt
'
:
True
}
                
'
tier
'
:
1
                
'
log_references
'
:
[
                    
{
                        
'
url
'
:
'
TBD
'
                        
'
name
'
:
'
test
log
'
                    
}
                
]
                
'
artifacts
'
:
[
                    
{
                        
'
type
'
:
'
json
'
                        
'
name
'
:
'
performance_data
'
                        
'
blob
'
:
perf_data
                    
}
                    
{
                        
'
type
'
:
'
json
'
                        
'
name
'
:
'
Job
Info
'
                        
"
blob
"
:
{
                            
"
job_details
"
:
[
                                
{
                                    
"
content_type
"
:
"
raw_html
"
                                    
"
title
"
:
"
Result
Summary
"
                                    
"
value
"
:
summary
                                
}
                            
]
                        
}
                    
}
                
]
                
'
coalesced
'
:
[
]
            
}
        
}
    
]
    
tjc
=
create_job_collection
(
dataset
)
    
cred
=
{
        
'
client_id
'
:
os
.
environ
[
'
TREEHERDER_CLIENT_ID
'
]
        
'
secret
'
:
os
.
environ
[
'
TREEHERDER_CLIENT_SECRET
'
]
    
}
    
client
=
TreeherderClient
(
server_url
=
'
https
:
/
/
treeherder
.
mozilla
.
org
'
                              
client_id
=
cred
[
'
client_id
'
]
                              
secret
=
cred
[
'
secret
'
]
)
    
client
.
post_collection
(
'
servo
'
trsc
)
    
client
.
post_collection
(
'
servo
'
tjc
)
def
main
(
)
:
    
parser
=
argparse
.
ArgumentParser
(
        
description
=
(
"
Submit
Servo
performance
data
to
Perfherder
.
"
                     
"
Remember
to
set
your
Treeherder
credential
as
environment
"
                     
"
variable
\
'
TREEHERDER_CLIENT_ID
\
'
and
"
                     
"
\
'
TREEHERDER_CLIENT_SECRET
\
'
"
)
)
    
parser
.
add_argument
(
"
perf_json
"
                        
help
=
"
the
output
json
from
runner
"
)
    
parser
.
add_argument
(
"
revision_json
"
                        
help
=
"
the
json
containing
the
servo
revision
data
"
)
    
parser
.
add_argument
(
"
-
-
engine
"
                        
type
=
str
                        
default
=
'
servo
'
                        
help
=
(
"
The
engine
to
run
the
tests
on
.
Currently
only
"
                              
"
servo
and
gecko
are
supported
.
"
)
)
    
args
=
parser
.
parse_args
(
)
    
with
open
(
args
.
perf_json
'
r
'
)
as
f
:
        
result_json
=
json
.
load
(
f
)
    
with
open
(
args
.
revision_json
'
r
'
)
as
f
:
        
revision
=
json
.
load
(
f
)
    
perf_data
=
format_perf_data
(
result_json
args
.
engine
)
    
failures
=
list
(
filter
(
lambda
x
:
x
[
'
domComplete
'
]
=
=
-
1
result_json
)
)
    
summary
=
format_result_summary
(
result_json
)
.
replace
(
'
\
n
'
'
<
br
/
>
'
)
    
submit
(
perf_data
failures
revision
summary
args
.
engine
)
    
print
(
"
Done
!
"
)
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
