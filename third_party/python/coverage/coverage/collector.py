"
"
"
Raw
data
collector
for
coverage
.
py
.
"
"
"
import
os
import
sys
from
coverage
import
env
from
coverage
.
backward
import
litems
range
from
coverage
.
debug
import
short_stack
from
coverage
.
disposition
import
FileDisposition
from
coverage
.
misc
import
CoverageException
isolate_module
from
coverage
.
pytracer
import
PyTracer
os
=
isolate_module
(
os
)
try
:
    
from
coverage
.
tracer
import
CTracer
CFileDisposition
except
ImportError
:
    
if
os
.
getenv
(
'
COVERAGE_TEST_TRACER
'
)
=
=
'
c
'
:
        
sys
.
stderr
.
write
(
"
*
*
*
COVERAGE_TEST_TRACER
is
'
c
'
but
can
'
t
import
CTracer
!
\
n
"
)
        
sys
.
exit
(
1
)
    
CTracer
=
None
class
Collector
(
object
)
:
    
"
"
"
Collects
trace
data
.
    
Creates
a
Tracer
object
for
each
thread
since
they
track
stack
    
information
.
Each
Tracer
points
to
the
same
shared
data
contributing
    
traced
data
points
.
    
When
the
Collector
is
started
it
creates
a
Tracer
for
the
current
thread
    
and
installs
a
function
to
create
Tracers
for
each
new
thread
started
.
    
When
the
Collector
is
stopped
all
active
Tracers
are
stopped
.
    
Threads
started
while
the
Collector
is
stopped
will
never
have
Tracers
    
associated
with
them
.
    
"
"
"
    
_collectors
=
[
]
    
SUPPORTED_CONCURRENCIES
=
set
(
[
"
greenlet
"
"
eventlet
"
"
gevent
"
"
thread
"
]
)
    
def
__init__
(
        
self
should_trace
check_include
should_start_context
file_mapper
        
timid
branch
warn
concurrency
    
)
:
        
"
"
"
Create
a
collector
.
        
should_trace
is
a
function
taking
a
file
name
and
a
frame
and
        
returning
a
coverage
.
FileDisposition
object
.
        
check_include
is
a
function
taking
a
file
name
and
a
frame
.
It
returns
        
a
boolean
:
True
if
the
file
should
be
traced
False
if
not
.
        
should_start_context
is
a
function
taking
a
frame
and
returning
a
        
string
.
If
the
frame
should
be
the
start
of
a
new
context
the
string
        
is
the
new
context
.
If
the
frame
should
not
be
the
start
of
a
new
        
context
return
None
.
        
file_mapper
is
a
function
taking
a
filename
and
returning
a
Unicode
        
filename
.
The
result
is
the
name
that
will
be
recorded
in
the
data
        
file
.
        
If
timid
is
true
then
a
slower
simpler
trace
function
will
be
        
used
.
This
is
important
for
some
environments
where
manipulation
of
        
tracing
functions
make
the
faster
more
sophisticated
trace
function
not
        
operate
properly
.
        
If
branch
is
true
then
branches
will
be
measured
.
This
involves
        
collecting
data
on
which
statements
followed
each
other
(
arcs
)
.
Use
        
get_arc_data
to
get
the
arc
data
.
        
warn
is
a
warning
function
taking
a
single
string
message
argument
        
and
an
optional
slug
argument
which
will
be
a
string
or
None
to
be
        
used
if
a
warning
needs
to
be
issued
.
        
concurrency
is
a
list
of
strings
indicating
the
concurrency
libraries
        
in
use
.
Valid
values
are
"
greenlet
"
"
eventlet
"
"
gevent
"
or
"
thread
"
        
(
the
default
)
.
Of
these
four
values
only
one
can
be
supplied
.
Other
        
values
are
ignored
.
        
"
"
"
        
self
.
should_trace
=
should_trace
        
self
.
check_include
=
check_include
        
self
.
should_start_context
=
should_start_context
        
self
.
file_mapper
=
file_mapper
        
self
.
warn
=
warn
        
self
.
branch
=
branch
        
self
.
threading
=
None
        
self
.
covdata
=
None
        
self
.
static_context
=
None
        
self
.
origin
=
short_stack
(
)
        
self
.
concur_id_func
=
None
        
self
.
mapped_file_cache
=
{
}
        
these_concurrencies
=
self
.
SUPPORTED_CONCURRENCIES
.
intersection
(
concurrency
)
        
if
len
(
these_concurrencies
)
>
1
:
            
raise
CoverageException
(
"
Conflicting
concurrency
settings
:
%
s
"
%
concurrency
)
        
self
.
concurrency
=
these_concurrencies
.
pop
(
)
if
these_concurrencies
else
'
'
        
try
:
            
if
self
.
concurrency
=
=
"
greenlet
"
:
                
import
greenlet
                
self
.
concur_id_func
=
greenlet
.
getcurrent
            
elif
self
.
concurrency
=
=
"
eventlet
"
:
                
import
eventlet
.
greenthread
                
self
.
concur_id_func
=
eventlet
.
greenthread
.
getcurrent
            
elif
self
.
concurrency
=
=
"
gevent
"
:
                
import
gevent
                
self
.
concur_id_func
=
gevent
.
getcurrent
            
elif
self
.
concurrency
=
=
"
thread
"
or
not
self
.
concurrency
:
                
import
threading
                
self
.
threading
=
threading
            
else
:
                
raise
CoverageException
(
"
Don
'
t
understand
concurrency
=
%
s
"
%
concurrency
)
        
except
ImportError
:
            
raise
CoverageException
(
                
"
Couldn
'
t
trace
with
concurrency
=
%
s
the
module
isn
'
t
installed
.
"
%
(
                    
self
.
concurrency
                
)
            
)
        
self
.
reset
(
)
        
if
timid
:
            
self
.
_trace_class
=
PyTracer
        
else
:
            
self
.
_trace_class
=
CTracer
or
PyTracer
        
if
self
.
_trace_class
is
CTracer
:
            
self
.
file_disposition_class
=
CFileDisposition
            
self
.
supports_plugins
=
True
        
else
:
            
self
.
file_disposition_class
=
FileDisposition
            
self
.
supports_plugins
=
False
    
def
__repr__
(
self
)
:
        
return
"
<
Collector
at
0x
%
x
:
%
s
>
"
%
(
id
(
self
)
self
.
tracer_name
(
)
)
    
def
use_data
(
self
covdata
context
)
:
        
"
"
"
Use
covdata
for
recording
data
.
"
"
"
        
self
.
covdata
=
covdata
        
self
.
static_context
=
context
        
self
.
covdata
.
set_context
(
self
.
static_context
)
    
def
tracer_name
(
self
)
:
        
"
"
"
Return
the
class
name
of
the
tracer
we
'
re
using
.
"
"
"
        
return
self
.
_trace_class
.
__name__
    
def
_clear_data
(
self
)
:
        
"
"
"
Clear
out
existing
data
but
stay
ready
for
more
collection
.
"
"
"
        
for
d
in
self
.
data
.
values
(
)
:
            
d
.
clear
(
)
        
for
tracer
in
self
.
tracers
:
            
tracer
.
reset_activity
(
)
    
def
reset
(
self
)
:
        
"
"
"
Clear
collected
data
and
prepare
to
collect
more
.
"
"
"
        
self
.
data
=
{
}
        
self
.
file_tracers
=
{
}
        
if
env
.
PYPY
:
            
import
__pypy__
            
self
.
should_trace_cache
=
__pypy__
.
newdict
(
"
module
"
)
        
else
:
            
self
.
should_trace_cache
=
{
}
        
self
.
tracers
=
[
]
        
self
.
_clear_data
(
)
    
def
_start_tracer
(
self
)
:
        
"
"
"
Start
a
new
Tracer
object
and
store
it
in
self
.
tracers
.
"
"
"
        
tracer
=
self
.
_trace_class
(
)
        
tracer
.
data
=
self
.
data
        
tracer
.
trace_arcs
=
self
.
branch
        
tracer
.
should_trace
=
self
.
should_trace
        
tracer
.
should_trace_cache
=
self
.
should_trace_cache
        
tracer
.
warn
=
self
.
warn
        
if
hasattr
(
tracer
'
concur_id_func
'
)
:
            
tracer
.
concur_id_func
=
self
.
concur_id_func
        
elif
self
.
concur_id_func
:
            
raise
CoverageException
(
                
"
Can
'
t
support
concurrency
=
%
s
with
%
s
only
threads
are
supported
"
%
(
                    
self
.
concurrency
self
.
tracer_name
(
)
                
)
            
)
        
if
hasattr
(
tracer
'
file_tracers
'
)
:
            
tracer
.
file_tracers
=
self
.
file_tracers
        
if
hasattr
(
tracer
'
threading
'
)
:
            
tracer
.
threading
=
self
.
threading
        
if
hasattr
(
tracer
'
check_include
'
)
:
            
tracer
.
check_include
=
self
.
check_include
        
if
hasattr
(
tracer
'
should_start_context
'
)
:
            
tracer
.
should_start_context
=
self
.
should_start_context
            
tracer
.
switch_context
=
self
.
switch_context
        
fn
=
tracer
.
start
(
)
        
self
.
tracers
.
append
(
tracer
)
        
return
fn
    
def
_installation_trace
(
self
frame
event
arg
)
:
        
"
"
"
Called
on
new
threads
installs
the
real
tracer
.
"
"
"
        
sys
.
settrace
(
None
)
        
fn
=
self
.
_start_tracer
(
)
        
if
fn
:
            
fn
=
fn
(
frame
event
arg
)
        
return
fn
    
def
start
(
self
)
:
        
"
"
"
Start
collecting
trace
information
.
"
"
"
        
if
self
.
_collectors
:
            
self
.
_collectors
[
-
1
]
.
pause
(
)
        
self
.
tracers
=
[
]
        
traces0
=
[
]
        
fn0
=
sys
.
gettrace
(
)
        
if
fn0
:
            
tracer0
=
getattr
(
fn0
'
__self__
'
None
)
            
if
tracer0
:
                
traces0
=
getattr
(
tracer0
'
traces
'
[
]
)
        
try
:
            
fn
=
self
.
_start_tracer
(
)
        
except
:
            
if
self
.
_collectors
:
                
self
.
_collectors
[
-
1
]
.
resume
(
)
            
raise
        
self
.
_collectors
.
append
(
self
)
        
for
args
in
traces0
:
            
(
frame
event
arg
)
lineno
=
args
            
try
:
                
fn
(
frame
event
arg
lineno
=
lineno
)
            
except
TypeError
:
                
raise
Exception
(
"
fullcoverage
must
be
run
with
the
C
trace
function
.
"
)
        
if
self
.
threading
:
            
self
.
threading
.
settrace
(
self
.
_installation_trace
)
    
def
stop
(
self
)
:
        
"
"
"
Stop
collecting
trace
information
.
"
"
"
        
assert
self
.
_collectors
        
if
self
.
_collectors
[
-
1
]
is
not
self
:
            
print
(
"
self
.
_collectors
:
"
)
            
for
c
in
self
.
_collectors
:
                
print
(
"
{
!
r
}
\
n
{
}
"
.
format
(
c
c
.
origin
)
)
        
assert
self
.
_collectors
[
-
1
]
is
self
(
            
"
Expected
current
collector
to
be
%
r
but
it
'
s
%
r
"
%
(
self
self
.
_collectors
[
-
1
]
)
        
)
        
self
.
pause
(
)
        
self
.
_collectors
.
pop
(
)
        
if
self
.
_collectors
:
            
self
.
_collectors
[
-
1
]
.
resume
(
)
    
def
pause
(
self
)
:
        
"
"
"
Pause
tracing
but
be
prepared
to
resume
.
"
"
"
        
for
tracer
in
self
.
tracers
:
            
tracer
.
stop
(
)
            
stats
=
tracer
.
get_stats
(
)
            
if
stats
:
                
print
(
"
\
nCoverage
.
py
tracer
stats
:
"
)
                
for
k
in
sorted
(
stats
.
keys
(
)
)
:
                    
print
(
"
%
20s
:
%
s
"
%
(
k
stats
[
k
]
)
)
        
if
self
.
threading
:
            
self
.
threading
.
settrace
(
None
)
    
def
resume
(
self
)
:
        
"
"
"
Resume
tracing
after
a
pause
.
"
"
"
        
for
tracer
in
self
.
tracers
:
            
tracer
.
start
(
)
        
if
self
.
threading
:
            
self
.
threading
.
settrace
(
self
.
_installation_trace
)
        
else
:
            
self
.
_start_tracer
(
)
    
def
_activity
(
self
)
:
        
"
"
"
Has
any
activity
been
traced
?
        
Returns
a
boolean
True
if
any
trace
function
was
invoked
.
        
"
"
"
        
return
any
(
tracer
.
activity
(
)
for
tracer
in
self
.
tracers
)
    
def
switch_context
(
self
new_context
)
:
        
"
"
"
Switch
to
a
new
dynamic
context
.
"
"
"
        
self
.
flush_data
(
)
        
if
self
.
static_context
:
            
context
=
self
.
static_context
            
if
new_context
:
                
context
+
=
"
|
"
+
new_context
        
else
:
            
context
=
new_context
        
self
.
covdata
.
set_context
(
context
)
    
def
cached_mapped_file
(
self
filename
)
:
        
"
"
"
A
locally
cached
version
of
file
names
mapped
through
file_mapper
.
"
"
"
        
key
=
(
type
(
filename
)
filename
)
        
try
:
            
return
self
.
mapped_file_cache
[
key
]
        
except
KeyError
:
            
return
self
.
mapped_file_cache
.
setdefault
(
key
self
.
file_mapper
(
filename
)
)
    
def
mapped_file_dict
(
self
d
)
:
        
"
"
"
Return
a
dict
like
d
but
with
keys
modified
by
file_mapper
.
"
"
"
        
runtime_err
=
None
        
for
_
in
range
(
3
)
:
            
try
:
                
items
=
litems
(
d
)
            
except
RuntimeError
as
ex
:
                
runtime_err
=
ex
            
else
:
                
break
        
else
:
            
raise
runtime_err
        
return
dict
(
(
self
.
cached_mapped_file
(
k
)
v
)
for
k
v
in
items
if
v
)
    
def
flush_data
(
self
)
:
        
"
"
"
Save
the
collected
data
to
our
associated
CoverageData
.
        
Data
may
have
also
been
saved
along
the
way
.
This
forces
the
        
last
of
the
data
to
be
saved
.
        
Returns
True
if
there
was
data
to
save
False
if
not
.
        
"
"
"
        
if
not
self
.
_activity
(
)
:
            
return
False
        
if
self
.
branch
:
            
self
.
covdata
.
add_arcs
(
self
.
mapped_file_dict
(
self
.
data
)
)
        
else
:
            
self
.
covdata
.
add_lines
(
self
.
mapped_file_dict
(
self
.
data
)
)
        
self
.
covdata
.
add_file_tracers
(
self
.
mapped_file_dict
(
self
.
file_tracers
)
)
        
self
.
_clear_data
(
)
        
return
True
