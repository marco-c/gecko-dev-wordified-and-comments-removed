"
"
"
This
file
is
originally
based
on
code
from
https
:
/
/
github
.
com
/
nylas
/
nylas
-
perftools
which
is
published
under
the
following
license
:
The
MIT
License
(
MIT
)
Copyright
(
c
)
2014
Nylas
Permission
is
hereby
granted
free
of
charge
to
any
person
obtaining
a
copy
of
this
software
and
associated
documentation
files
(
the
"
Software
"
)
to
deal
in
the
Software
without
restriction
including
without
limitation
the
rights
to
use
copy
modify
merge
publish
distribute
sublicense
and
/
or
sell
copies
of
the
Software
and
to
permit
persons
to
whom
the
Software
is
furnished
to
do
so
subject
to
the
following
conditions
:
The
above
copyright
notice
and
this
permission
notice
shall
be
included
in
all
copies
or
substantial
portions
of
the
Software
.
THE
SOFTWARE
IS
PROVIDED
"
AS
IS
"
WITHOUT
WARRANTY
OF
ANY
KIND
EXPRESS
OR
IMPLIED
INCLUDING
BUT
NOT
LIMITED
TO
THE
WARRANTIES
OF
MERCHANTABILITY
FITNESS
FOR
A
PARTICULAR
PURPOSE
AND
NONINFRINGEMENT
.
IN
NO
EVENT
SHALL
THE
AUTHORS
OR
COPYRIGHT
HOLDERS
BE
LIABLE
FOR
ANY
CLAIM
DAMAGES
OR
OTHER
LIABILITY
WHETHER
IN
AN
ACTION
OF
CONTRACT
TORT
OR
OTHERWISE
ARISING
FROM
OUT
OF
OR
IN
CONNECTION
WITH
THE
SOFTWARE
OR
THE
USE
OR
OTHER
DEALINGS
IN
THE
SOFTWARE
.
"
"
"
import
atexit
import
os
import
platform
import
random
import
sys
import
threading
import
time
import
uuid
import
warnings
from
abc
import
ABC
abstractmethod
from
collections
import
deque
import
sentry_sdk
from
sentry_sdk
.
_lru_cache
import
LRUCache
from
sentry_sdk
.
profiler
.
utils
import
(
    
DEFAULT_SAMPLING_FREQUENCY
    
extract_stack
)
from
sentry_sdk
.
utils
import
(
    
capture_internal_exception
    
get_current_thread_meta
    
is_gevent
    
is_valid_sample_rate
    
logger
    
nanosecond_time
    
set_in_app_in_frames
)
from
typing
import
TYPE_CHECKING
if
TYPE_CHECKING
:
    
from
typing
import
Any
    
from
typing
import
Callable
    
from
typing
import
Deque
    
from
typing
import
Dict
    
from
typing
import
List
    
from
typing
import
Optional
    
from
typing
import
Set
    
from
typing
import
Type
    
from
typing_extensions
import
TypedDict
    
from
sentry_sdk
.
profiler
.
utils
import
(
        
ProcessedStack
        
ProcessedFrame
        
ProcessedThreadMetadata
        
FrameId
        
StackId
        
ThreadId
        
ExtractedSample
    
)
    
from
sentry_sdk
.
_types
import
Event
SamplingContext
ProfilerMode
    
ProcessedSample
=
TypedDict
(
        
"
ProcessedSample
"
        
{
            
"
elapsed_since_start_ns
"
:
str
            
"
thread_id
"
:
ThreadId
            
"
stack_id
"
:
int
        
}
    
)
    
ProcessedProfile
=
TypedDict
(
        
"
ProcessedProfile
"
        
{
            
"
frames
"
:
List
[
ProcessedFrame
]
            
"
stacks
"
:
List
[
ProcessedStack
]
            
"
samples
"
:
List
[
ProcessedSample
]
            
"
thread_metadata
"
:
Dict
[
ThreadId
ProcessedThreadMetadata
]
        
}
    
)
try
:
    
from
gevent
.
monkey
import
get_original
    
from
gevent
.
threadpool
import
ThreadPool
as
_ThreadPool
    
ThreadPool
=
_ThreadPool
    
thread_sleep
=
get_original
(
"
time
"
"
sleep
"
)
except
ImportError
:
    
thread_sleep
=
time
.
sleep
    
ThreadPool
=
None
_scheduler
=
None
PROFILE_MINIMUM_SAMPLES
=
2
def
has_profiling_enabled
(
options
)
:
    
profiles_sampler
=
options
[
"
profiles_sampler
"
]
    
if
profiles_sampler
is
not
None
:
        
return
True
    
profiles_sample_rate
=
options
[
"
profiles_sample_rate
"
]
    
if
profiles_sample_rate
is
not
None
and
profiles_sample_rate
>
0
:
        
return
True
    
profiles_sample_rate
=
options
[
"
_experiments
"
]
.
get
(
"
profiles_sample_rate
"
)
    
if
profiles_sample_rate
is
not
None
:
        
logger
.
warning
(
            
"
_experiments
[
'
profiles_sample_rate
'
]
is
deprecated
.
"
            
"
Please
use
the
non
-
experimental
profiles_sample_rate
option
"
            
"
directly
.
"
        
)
        
if
profiles_sample_rate
>
0
:
            
return
True
    
return
False
def
setup_profiler
(
options
)
:
    
global
_scheduler
    
if
_scheduler
is
not
None
:
        
logger
.
debug
(
"
[
Profiling
]
Profiler
is
already
setup
"
)
        
return
False
    
frequency
=
DEFAULT_SAMPLING_FREQUENCY
    
if
is_gevent
(
)
:
        
default_profiler_mode
=
GeventScheduler
.
mode
    
else
:
        
default_profiler_mode
=
ThreadScheduler
.
mode
    
if
options
.
get
(
"
profiler_mode
"
)
is
not
None
:
        
profiler_mode
=
options
[
"
profiler_mode
"
]
    
else
:
        
profiler_mode
=
options
.
get
(
"
_experiments
"
{
}
)
.
get
(
"
profiler_mode
"
)
        
if
profiler_mode
is
not
None
:
            
logger
.
warning
(
                
"
_experiments
[
'
profiler_mode
'
]
is
deprecated
.
Please
use
the
"
                
"
non
-
experimental
profiler_mode
option
directly
.
"
            
)
        
profiler_mode
=
profiler_mode
or
default_profiler_mode
    
if
(
        
profiler_mode
=
=
ThreadScheduler
.
mode
        
or
profiler_mode
=
=
"
sleep
"
    
)
:
        
_scheduler
=
ThreadScheduler
(
frequency
=
frequency
)
    
elif
profiler_mode
=
=
GeventScheduler
.
mode
:
        
_scheduler
=
GeventScheduler
(
frequency
=
frequency
)
    
else
:
        
raise
ValueError
(
"
Unknown
profiler
mode
:
{
}
"
.
format
(
profiler_mode
)
)
    
logger
.
debug
(
        
"
[
Profiling
]
Setting
up
profiler
in
{
mode
}
mode
"
.
format
(
mode
=
_scheduler
.
mode
)
    
)
    
_scheduler
.
setup
(
)
    
atexit
.
register
(
teardown_profiler
)
    
return
True
def
teardown_profiler
(
)
:
    
global
_scheduler
    
if
_scheduler
is
not
None
:
        
_scheduler
.
teardown
(
)
    
_scheduler
=
None
MAX_PROFILE_DURATION_NS
=
int
(
3e10
)
class
Profile
:
    
def
__init__
(
        
self
        
sampled
        
start_ns
        
hub
=
None
        
scheduler
=
None
    
)
:
        
self
.
scheduler
=
_scheduler
if
scheduler
is
None
else
scheduler
        
self
.
event_id
=
uuid
.
uuid4
(
)
.
hex
        
self
.
sampled
=
sampled
        
self
.
_default_active_thread_id
=
get_current_thread_meta
(
)
[
0
]
or
0
        
self
.
active_thread_id
=
None
        
try
:
            
self
.
start_ns
=
start_ns
        
except
AttributeError
:
            
self
.
start_ns
=
0
        
self
.
stop_ns
=
0
        
self
.
active
=
False
        
self
.
indexed_frames
=
{
}
        
self
.
indexed_stacks
=
{
}
        
self
.
frames
=
[
]
        
self
.
stacks
=
[
]
        
self
.
samples
=
[
]
        
self
.
unique_samples
=
0
        
self
.
_hub
=
None
        
if
hub
is
not
None
:
            
self
.
_hub
=
hub
            
warnings
.
warn
(
                
"
The
hub
parameter
is
deprecated
.
Please
do
not
use
it
.
"
                
DeprecationWarning
                
stacklevel
=
2
            
)
    
def
update_active_thread_id
(
self
)
:
        
self
.
active_thread_id
=
get_current_thread_meta
(
)
[
0
]
        
logger
.
debug
(
            
"
[
Profiling
]
updating
active
thread
id
to
{
tid
}
"
.
format
(
                
tid
=
self
.
active_thread_id
            
)
        
)
    
def
_set_initial_sampling_decision
(
self
sampling_context
)
:
        
"
"
"
        
Sets
the
profile
'
s
sampling
decision
according
to
the
following
        
precedence
rules
:
        
1
.
If
the
transaction
to
be
profiled
is
not
sampled
that
decision
        
will
be
used
regardless
of
anything
else
.
        
2
.
Use
profiles_sample_rate
to
decide
.
        
"
"
"
        
if
not
self
.
sampled
:
            
logger
.
debug
(
                
"
[
Profiling
]
Discarding
profile
because
transaction
is
discarded
.
"
            
)
            
self
.
sampled
=
False
            
return
        
if
self
.
scheduler
is
None
:
            
logger
.
debug
(
                
"
[
Profiling
]
Discarding
profile
because
profiler
was
not
started
.
"
            
)
            
self
.
sampled
=
False
            
return
        
client
=
sentry_sdk
.
get_client
(
)
        
if
not
client
.
is_active
(
)
:
            
self
.
sampled
=
False
            
return
        
options
=
client
.
options
        
if
callable
(
options
.
get
(
"
profiles_sampler
"
)
)
:
            
sample_rate
=
options
[
"
profiles_sampler
"
]
(
sampling_context
)
        
elif
options
[
"
profiles_sample_rate
"
]
is
not
None
:
            
sample_rate
=
options
[
"
profiles_sample_rate
"
]
        
else
:
            
sample_rate
=
options
[
"
_experiments
"
]
.
get
(
"
profiles_sample_rate
"
)
        
if
sample_rate
is
None
:
            
logger
.
debug
(
                
"
[
Profiling
]
Discarding
profile
because
profiling
was
not
enabled
.
"
            
)
            
self
.
sampled
=
False
            
return
        
if
not
is_valid_sample_rate
(
sample_rate
source
=
"
Profiling
"
)
:
            
logger
.
warning
(
                
"
[
Profiling
]
Discarding
profile
because
of
invalid
sample
rate
.
"
            
)
            
self
.
sampled
=
False
            
return
        
self
.
sampled
=
random
.
random
(
)
<
float
(
sample_rate
)
        
if
self
.
sampled
:
            
logger
.
debug
(
"
[
Profiling
]
Initializing
profile
"
)
        
else
:
            
logger
.
debug
(
                
"
[
Profiling
]
Discarding
profile
because
it
'
s
not
included
in
the
random
sample
(
sample
rate
=
{
sample_rate
}
)
"
.
format
(
                    
sample_rate
=
float
(
sample_rate
)
                
)
            
)
    
def
start
(
self
)
:
        
if
not
self
.
sampled
or
self
.
active
:
            
return
        
assert
self
.
scheduler
"
No
scheduler
specified
"
        
logger
.
debug
(
"
[
Profiling
]
Starting
profile
"
)
        
self
.
active
=
True
        
if
not
self
.
start_ns
:
            
self
.
start_ns
=
nanosecond_time
(
)
        
self
.
scheduler
.
start_profiling
(
self
)
    
def
stop
(
self
)
:
        
if
not
self
.
sampled
or
not
self
.
active
:
            
return
        
assert
self
.
scheduler
"
No
scheduler
specified
"
        
logger
.
debug
(
"
[
Profiling
]
Stopping
profile
"
)
        
self
.
active
=
False
        
self
.
stop_ns
=
nanosecond_time
(
)
    
def
__enter__
(
self
)
:
        
scope
=
sentry_sdk
.
get_isolation_scope
(
)
        
old_profile
=
scope
.
profile
        
scope
.
profile
=
self
        
self
.
_context_manager_state
=
(
scope
old_profile
)
        
self
.
start
(
)
        
return
self
    
def
__exit__
(
self
ty
value
tb
)
:
        
self
.
stop
(
)
        
scope
old_profile
=
self
.
_context_manager_state
        
del
self
.
_context_manager_state
        
scope
.
profile
=
old_profile
    
def
write
(
self
ts
sample
)
:
        
if
not
self
.
active
:
            
return
        
if
ts
<
self
.
start_ns
:
            
return
        
offset
=
ts
-
self
.
start_ns
        
if
offset
>
MAX_PROFILE_DURATION_NS
:
            
self
.
stop
(
)
            
return
        
self
.
unique_samples
+
=
1
        
elapsed_since_start_ns
=
str
(
offset
)
        
for
tid
(
stack_id
frame_ids
frames
)
in
sample
:
            
try
:
                
if
stack_id
not
in
self
.
indexed_stacks
:
                    
for
i
frame_id
in
enumerate
(
frame_ids
)
:
                        
if
frame_id
not
in
self
.
indexed_frames
:
                            
self
.
indexed_frames
[
frame_id
]
=
len
(
self
.
indexed_frames
)
                            
self
.
frames
.
append
(
frames
[
i
]
)
                    
self
.
indexed_stacks
[
stack_id
]
=
len
(
self
.
indexed_stacks
)
                    
self
.
stacks
.
append
(
                        
[
self
.
indexed_frames
[
frame_id
]
for
frame_id
in
frame_ids
]
                    
)
                
self
.
samples
.
append
(
                    
{
                        
"
elapsed_since_start_ns
"
:
elapsed_since_start_ns
                        
"
thread_id
"
:
tid
                        
"
stack_id
"
:
self
.
indexed_stacks
[
stack_id
]
                    
}
                
)
            
except
AttributeError
:
                
capture_internal_exception
(
sys
.
exc_info
(
)
)
    
def
process
(
self
)
:
        
thread_metadata
=
{
            
str
(
thread
.
ident
)
:
{
                
"
name
"
:
str
(
thread
.
name
)
            
}
            
for
thread
in
threading
.
enumerate
(
)
        
}
        
return
{
            
"
frames
"
:
self
.
frames
            
"
stacks
"
:
self
.
stacks
            
"
samples
"
:
self
.
samples
            
"
thread_metadata
"
:
thread_metadata
        
}
    
def
to_json
(
self
event_opt
options
)
:
        
profile
=
self
.
process
(
)
        
set_in_app_in_frames
(
            
profile
[
"
frames
"
]
            
options
[
"
in_app_exclude
"
]
            
options
[
"
in_app_include
"
]
            
options
[
"
project_root
"
]
        
)
        
return
{
            
"
environment
"
:
event_opt
.
get
(
"
environment
"
)
            
"
event_id
"
:
self
.
event_id
            
"
platform
"
:
"
python
"
            
"
profile
"
:
profile
            
"
release
"
:
event_opt
.
get
(
"
release
"
"
"
)
            
"
timestamp
"
:
event_opt
[
"
start_timestamp
"
]
            
"
version
"
:
"
1
"
            
"
device
"
:
{
                
"
architecture
"
:
platform
.
machine
(
)
            
}
            
"
os
"
:
{
                
"
name
"
:
platform
.
system
(
)
                
"
version
"
:
platform
.
release
(
)
            
}
            
"
runtime
"
:
{
                
"
name
"
:
platform
.
python_implementation
(
)
                
"
version
"
:
platform
.
python_version
(
)
            
}
            
"
transactions
"
:
[
                
{
                    
"
id
"
:
event_opt
[
"
event_id
"
]
                    
"
name
"
:
event_opt
[
"
transaction
"
]
                    
"
relative_start_ns
"
:
"
0
"
                    
"
relative_end_ns
"
:
str
(
self
.
stop_ns
-
self
.
start_ns
)
                    
"
trace_id
"
:
event_opt
[
"
contexts
"
]
[
"
trace
"
]
[
"
trace_id
"
]
                    
"
active_thread_id
"
:
str
(
                        
self
.
_default_active_thread_id
                        
if
self
.
active_thread_id
is
None
                        
else
self
.
active_thread_id
                    
)
                
}
            
]
        
}
    
def
valid
(
self
)
:
        
client
=
sentry_sdk
.
get_client
(
)
        
if
not
client
.
is_active
(
)
:
            
return
False
        
if
not
has_profiling_enabled
(
client
.
options
)
:
            
return
False
        
if
self
.
sampled
is
None
or
not
self
.
sampled
:
            
if
client
.
transport
:
                
client
.
transport
.
record_lost_event
(
                    
"
sample_rate
"
data_category
=
"
profile
"
                
)
            
return
False
        
if
self
.
unique_samples
<
PROFILE_MINIMUM_SAMPLES
:
            
if
client
.
transport
:
                
client
.
transport
.
record_lost_event
(
                    
"
insufficient_data
"
data_category
=
"
profile
"
                
)
            
logger
.
debug
(
"
[
Profiling
]
Discarding
profile
because
insufficient
samples
.
"
)
            
return
False
        
return
True
    
property
    
def
hub
(
self
)
:
        
warnings
.
warn
(
            
"
The
hub
attribute
is
deprecated
.
Please
do
not
access
it
.
"
            
DeprecationWarning
            
stacklevel
=
2
        
)
        
return
self
.
_hub
    
hub
.
setter
    
def
hub
(
self
value
)
:
        
warnings
.
warn
(
            
"
The
hub
attribute
is
deprecated
.
Please
do
not
set
it
.
"
            
DeprecationWarning
            
stacklevel
=
2
        
)
        
self
.
_hub
=
value
class
Scheduler
(
ABC
)
:
    
mode
=
"
unknown
"
    
def
__init__
(
self
frequency
)
:
        
self
.
interval
=
1
.
0
/
frequency
        
self
.
sampler
=
self
.
make_sampler
(
)
        
self
.
new_profiles
=
deque
(
maxlen
=
128
)
        
self
.
active_profiles
=
set
(
)
    
def
__enter__
(
self
)
:
        
self
.
setup
(
)
        
return
self
    
def
__exit__
(
self
ty
value
tb
)
:
        
self
.
teardown
(
)
    
abstractmethod
    
def
setup
(
self
)
:
        
pass
    
abstractmethod
    
def
teardown
(
self
)
:
        
pass
    
def
ensure_running
(
self
)
:
        
"
"
"
        
Ensure
the
scheduler
is
running
.
By
default
this
method
is
a
no
-
op
.
        
The
method
should
be
overridden
by
any
implementation
for
which
it
is
        
relevant
.
        
"
"
"
        
return
None
    
def
start_profiling
(
self
profile
)
:
        
self
.
ensure_running
(
)
        
self
.
new_profiles
.
append
(
profile
)
    
def
make_sampler
(
self
)
:
        
cwd
=
os
.
getcwd
(
)
        
cache
=
LRUCache
(
max_size
=
256
)
        
def
_sample_stack
(
*
args
*
*
kwargs
)
:
            
"
"
"
            
Take
a
sample
of
the
stack
on
all
the
threads
in
the
process
.
            
This
should
be
called
at
a
regular
interval
to
collect
samples
.
            
"
"
"
            
if
not
self
.
new_profiles
and
not
self
.
active_profiles
:
                
return
            
new_profiles
=
len
(
self
.
new_profiles
)
            
now
=
nanosecond_time
(
)
            
try
:
                
sample
=
[
                    
(
str
(
tid
)
extract_stack
(
frame
cache
cwd
)
)
                    
for
tid
frame
in
sys
.
_current_frames
(
)
.
items
(
)
                
]
            
except
AttributeError
:
                
capture_internal_exception
(
sys
.
exc_info
(
)
)
                
return
            
for
_
in
range
(
new_profiles
)
:
                
self
.
active_profiles
.
add
(
self
.
new_profiles
.
popleft
(
)
)
            
inactive_profiles
=
[
]
            
for
profile
in
self
.
active_profiles
:
                
if
profile
.
active
:
                    
profile
.
write
(
now
sample
)
                
else
:
                    
inactive_profiles
.
append
(
profile
)
            
for
profile
in
inactive_profiles
:
                
self
.
active_profiles
.
remove
(
profile
)
        
return
_sample_stack
class
ThreadScheduler
(
Scheduler
)
:
    
"
"
"
    
This
scheduler
is
based
on
running
a
daemon
thread
that
will
call
    
the
sampler
at
a
regular
interval
.
    
"
"
"
    
mode
=
"
thread
"
    
name
=
"
sentry
.
profiler
.
ThreadScheduler
"
    
def
__init__
(
self
frequency
)
:
        
super
(
)
.
__init__
(
frequency
=
frequency
)
        
self
.
running
=
False
        
self
.
thread
=
None
        
self
.
pid
=
None
        
self
.
lock
=
threading
.
Lock
(
)
    
def
setup
(
self
)
:
        
pass
    
def
teardown
(
self
)
:
        
if
self
.
running
:
            
self
.
running
=
False
            
if
self
.
thread
is
not
None
:
                
self
.
thread
.
join
(
)
    
def
ensure_running
(
self
)
:
        
"
"
"
        
Check
that
the
profiler
has
an
active
thread
to
run
in
and
start
one
if
        
that
'
s
not
the
case
.
        
Note
that
this
might
fail
(
e
.
g
.
in
Python
3
.
12
it
'
s
not
possible
to
        
spawn
new
threads
at
interpreter
shutdown
)
.
In
that
case
self
.
running
        
will
be
False
after
running
this
function
.
        
"
"
"
        
pid
=
os
.
getpid
(
)
        
if
self
.
running
and
self
.
pid
=
=
pid
:
            
return
        
with
self
.
lock
:
            
if
self
.
running
and
self
.
pid
=
=
pid
:
                
return
            
self
.
pid
=
pid
            
self
.
running
=
True
            
self
.
thread
=
threading
.
Thread
(
name
=
self
.
name
target
=
self
.
run
daemon
=
True
)
            
try
:
                
self
.
thread
.
start
(
)
            
except
RuntimeError
:
                
self
.
running
=
False
                
self
.
thread
=
None
                
return
    
def
run
(
self
)
:
        
last
=
time
.
perf_counter
(
)
        
while
self
.
running
:
            
self
.
sampler
(
)
            
elapsed
=
time
.
perf_counter
(
)
-
last
            
if
elapsed
<
self
.
interval
:
                
thread_sleep
(
self
.
interval
-
elapsed
)
            
last
=
time
.
perf_counter
(
)
class
GeventScheduler
(
Scheduler
)
:
    
"
"
"
    
This
scheduler
is
based
on
the
thread
scheduler
but
adapted
to
work
with
    
gevent
.
When
using
gevent
it
may
monkey
patch
the
threading
modules
    
(
threading
and
_thread
)
.
This
results
in
the
use
of
greenlets
instead
    
of
native
threads
.
    
This
is
an
issue
because
the
sampler
CANNOT
run
in
a
greenlet
because
    
1
.
Other
greenlets
doing
sync
work
will
prevent
the
sampler
from
running
    
2
.
The
greenlet
runs
in
the
same
thread
as
other
greenlets
so
when
taking
       
a
sample
other
greenlets
will
have
been
evicted
from
the
thread
.
This
       
results
in
a
sample
containing
only
the
sampler
'
s
code
.
    
"
"
"
    
mode
=
"
gevent
"
    
name
=
"
sentry
.
profiler
.
GeventScheduler
"
    
def
__init__
(
self
frequency
)
:
        
if
ThreadPool
is
None
:
            
raise
ValueError
(
"
Profiler
mode
:
{
}
is
not
available
"
.
format
(
self
.
mode
)
)
        
super
(
)
.
__init__
(
frequency
=
frequency
)
        
self
.
running
=
False
        
self
.
thread
=
None
        
self
.
pid
=
None
        
self
.
lock
=
threading
.
Lock
(
)
    
def
setup
(
self
)
:
        
pass
    
def
teardown
(
self
)
:
        
if
self
.
running
:
            
self
.
running
=
False
            
if
self
.
thread
is
not
None
:
                
self
.
thread
.
join
(
)
    
def
ensure_running
(
self
)
:
        
pid
=
os
.
getpid
(
)
        
if
self
.
running
and
self
.
pid
=
=
pid
:
            
return
        
with
self
.
lock
:
            
if
self
.
running
and
self
.
pid
=
=
pid
:
                
return
            
self
.
pid
=
pid
            
self
.
running
=
True
            
self
.
thread
=
ThreadPool
(
1
)
            
try
:
                
self
.
thread
.
spawn
(
self
.
run
)
            
except
RuntimeError
:
                
self
.
running
=
False
                
self
.
thread
=
None
                
return
    
def
run
(
self
)
:
        
last
=
time
.
perf_counter
(
)
        
while
self
.
running
:
            
self
.
sampler
(
)
            
elapsed
=
time
.
perf_counter
(
)
-
last
            
if
elapsed
<
self
.
interval
:
                
thread_sleep
(
self
.
interval
-
elapsed
)
            
last
=
time
.
perf_counter
(
)
