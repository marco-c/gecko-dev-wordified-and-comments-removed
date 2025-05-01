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
from
collections
import
deque
from
contextlib
import
contextmanager
import
sentry_sdk
from
sentry_sdk
.
_compat
import
PY33
PY311
from
sentry_sdk
.
_types
import
MYPY
from
sentry_sdk
.
utils
import
(
    
filename_for_module
    
handle_in_app_impl
    
logger
    
nanosecond_time
)
if
MYPY
:
    
from
types
import
FrameType
    
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
Generator
    
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
Sequence
    
from
typing
import
Tuple
    
from
typing_extensions
import
TypedDict
    
import
sentry_sdk
.
tracing
    
ThreadId
=
str
    
RawStackId
=
Tuple
[
int
int
]
    
RawFrame
=
Tuple
[
        
str
        
Optional
[
str
]
        
Optional
[
str
]
        
str
        
int
    
]
    
RawStack
=
Tuple
[
RawFrame
.
.
.
]
    
RawSample
=
Sequence
[
Tuple
[
str
Tuple
[
RawStackId
RawStack
]
]
]
    
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
    
ProcessedStack
=
List
[
int
]
    
ProcessedFrame
=
TypedDict
(
        
"
ProcessedFrame
"
        
{
            
"
abs_path
"
:
str
            
"
filename
"
:
Optional
[
str
]
            
"
function
"
:
str
            
"
lineno
"
:
int
            
"
module
"
:
Optional
[
str
]
        
}
    
)
    
ProcessedThreadMetadata
=
TypedDict
(
        
"
ProcessedThreadMetadata
"
        
{
"
name
"
:
str
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
    
ProfileContext
=
TypedDict
(
        
"
ProfileContext
"
        
{
"
profile_id
"
:
str
}
    
)
try
:
    
from
gevent
.
monkey
import
is_module_patched
except
ImportError
:
    
def
is_module_patched
(
*
args
*
*
kwargs
)
:
        
return
False
_scheduler
=
None
def
setup_profiler
(
options
)
:
    
"
"
"
    
buffer_secs
determines
the
max
time
a
sample
will
be
buffered
for
    
frequency
determines
the
number
of
samples
to
take
per
second
(
Hz
)
    
"
"
"
    
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
profiling
is
already
setup
"
)
        
return
    
if
not
PY33
:
        
logger
.
warn
(
"
profiling
is
only
supported
on
Python
>
=
3
.
3
"
)
        
return
    
frequency
=
101
    
if
is_module_patched
(
"
threading
"
)
or
is_module_patched
(
"
_thread
"
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
    
profiler_mode
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
profiler_mode
"
default_profiler_mode
)
    
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
        
try
:
            
_scheduler
=
GeventScheduler
(
frequency
=
frequency
)
        
except
ImportError
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
profiler_mode
)
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
MAX_STACK_DEPTH
=
128
def
extract_stack
(
    
frame
    
cwd
    
prev_cache
=
None
    
max_stack_depth
=
MAX_STACK_DEPTH
)
:
    
"
"
"
    
Extracts
the
stack
starting
the
specified
frame
.
The
extracted
stack
    
assumes
the
specified
frame
is
the
top
of
the
stack
and
works
back
    
to
the
bottom
of
the
stack
.
    
In
the
event
that
the
stack
is
more
than
MAX_STACK_DEPTH
frames
deep
    
only
the
first
MAX_STACK_DEPTH
frames
will
be
returned
.
    
"
"
"
    
frames
=
deque
(
maxlen
=
max_stack_depth
)
    
while
frame
is
not
None
:
        
frames
.
append
(
frame
)
        
frame
=
frame
.
f_back
    
if
prev_cache
is
None
:
        
stack
=
tuple
(
extract_frame
(
frame
cwd
)
for
frame
in
frames
)
    
else
:
        
_
prev_stack
prev_frames
=
prev_cache
        
prev_depth
=
len
(
prev_frames
)
        
depth
=
len
(
frames
)
        
stack
=
tuple
(
            
prev_stack
[
i
]
            
if
i
>
=
0
and
frame
is
prev_frames
[
i
]
            
else
extract_frame
(
frame
cwd
)
            
for
i
frame
in
zip
(
range
(
prev_depth
-
depth
prev_depth
)
frames
)
        
)
    
stack_id
=
len
(
stack
)
hash
(
stack
)
    
return
stack_id
stack
frames
def
extract_frame
(
frame
cwd
)
:
    
abs_path
=
frame
.
f_code
.
co_filename
    
try
:
        
module
=
frame
.
f_globals
[
"
__name__
"
]
    
except
Exception
:
        
module
=
None
    
return
(
        
os
.
path
.
join
(
cwd
abs_path
)
        
module
        
filename_for_module
(
module
abs_path
)
or
None
        
get_frame_name
(
frame
)
        
frame
.
f_lineno
    
)
if
PY311
:
    
def
get_frame_name
(
frame
)
:
        
return
frame
.
f_code
.
co_qualname
else
:
    
def
get_frame_name
(
frame
)
:
        
f_code
=
frame
.
f_code
        
co_varnames
=
f_code
.
co_varnames
        
name
=
f_code
.
co_name
        
try
:
            
if
(
                
co_varnames
                
and
co_varnames
[
0
]
=
=
"
self
"
                
and
"
self
"
in
frame
.
f_locals
            
)
:
                
for
cls
in
frame
.
f_locals
[
"
self
"
]
.
__class__
.
__mro__
:
                    
if
name
in
cls
.
__dict__
:
                        
return
"
{
}
.
{
}
"
.
format
(
cls
.
__name__
name
)
        
except
AttributeError
:
            
pass
        
try
:
            
if
(
                
co_varnames
                
and
co_varnames
[
0
]
=
=
"
cls
"
                
and
"
cls
"
in
frame
.
f_locals
            
)
:
                
for
cls
in
frame
.
f_locals
[
"
cls
"
]
.
__mro__
:
                    
if
name
in
cls
.
__dict__
:
                        
return
"
{
}
.
{
}
"
.
format
(
cls
.
__name__
name
)
        
except
AttributeError
:
            
pass
        
return
name
MAX_PROFILE_DURATION_NS
=
int
(
3e10
)
class
Profile
(
object
)
:
    
def
__init__
(
        
self
        
scheduler
        
transaction
        
hub
=
None
    
)
:
        
self
.
scheduler
=
scheduler
        
self
.
transaction
=
transaction
        
self
.
hub
=
hub
        
self
.
active_thread_id
=
None
        
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
        
transaction
.
_profile
=
self
    
def
get_profile_context
(
self
)
:
        
return
{
"
profile_id
"
:
self
.
event_id
}
    
def
__enter__
(
self
)
:
        
hub
=
self
.
hub
or
sentry_sdk
.
Hub
.
current
        
_
scope
=
hub
.
_stack
[
-
1
]
        
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
hub
scope
old_profile
)
        
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
scheduler
.
stop_profiling
(
self
)
        
self
.
stop_ns
=
nanosecond_time
(
)
        
_
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
            
return
        
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
stack
)
in
sample
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
frame
in
stack
:
                    
if
frame
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
frame
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
                            
{
                                
"
abs_path
"
:
frame
[
0
]
                                
"
module
"
:
frame
[
1
]
                                
"
filename
"
:
frame
[
2
]
                                
"
function
"
:
frame
[
3
]
                                
"
lineno
"
:
frame
[
4
]
                            
}
                        
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
frame
]
for
frame
in
stack
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
        
handle_in_app_impl
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
timestamp
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
self
.
transaction
.
name
                    
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
self
.
transaction
.
trace_id
                    
"
active_thread_id
"
:
str
(
                        
self
.
transaction
.
_active_thread_id
                        
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
class
Scheduler
(
object
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
    
def
setup
(
self
)
:
        
raise
NotImplementedError
    
def
teardown
(
self
)
:
        
raise
NotImplementedError
    
def
start_profiling
(
self
profile
)
:
        
profile
.
active
=
True
        
self
.
new_profiles
.
append
(
profile
)
    
def
stop_profiling
(
self
profile
)
:
        
profile
.
active
=
False
    
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
        
last_sample
=
[
            
{
}
        
]
        
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
                
last_sample
[
0
]
=
{
}
                
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
            
raw_sample
=
{
                
tid
:
extract_stack
(
frame
cwd
last_sample
[
0
]
.
get
(
tid
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
            
}
            
last_sample
[
0
]
=
raw_sample
            
sample
=
[
                
(
str
(
tid
)
(
stack_id
stack
)
)
                
for
tid
(
stack_id
stack
_
)
in
raw_sample
.
items
(
)
            
]
            
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
ThreadScheduler
self
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
event
=
threading
.
Event
(
)
        
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
    
def
setup
(
self
)
:
        
self
.
thread
.
start
(
)
    
def
teardown
(
self
)
:
        
self
.
event
.
set
(
)
        
self
.
thread
.
join
(
)
    
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
True
:
            
if
self
.
event
.
is_set
(
)
:
                
break
            
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
                
time
.
sleep
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
        
from
gevent
.
threadpool
import
ThreadPool
        
super
(
GeventScheduler
self
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
event
=
threading
.
Event
(
)
        
self
.
pool
=
ThreadPool
(
1
)
    
def
setup
(
self
)
:
        
self
.
pool
.
spawn
(
self
.
run
)
    
def
teardown
(
self
)
:
        
self
.
event
.
set
(
)
        
self
.
pool
.
join
(
)
    
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
True
:
            
if
self
.
event
.
is_set
(
)
:
                
break
            
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
                
time
.
sleep
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
def
_should_profile
(
transaction
hub
)
:
    
if
not
transaction
.
sampled
:
        
return
False
    
if
_scheduler
is
None
:
        
return
False
    
client
=
hub
.
client
    
if
client
is
None
:
        
return
False
    
options
=
client
.
options
    
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
None
:
        
return
False
    
return
random
.
random
(
)
<
float
(
profiles_sample_rate
)
contextmanager
def
start_profiling
(
transaction
hub
=
None
)
:
    
hub
=
hub
or
sentry_sdk
.
Hub
.
current
    
if
_should_profile
(
transaction
hub
)
:
        
assert
_scheduler
is
not
None
        
with
Profile
(
_scheduler
transaction
hub
)
:
            
yield
    
else
:
        
yield
