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
atexit
import
dis
import
sys
from
coverage
import
env
YIELD_VALUE
=
dis
.
opmap
[
'
YIELD_VALUE
'
]
if
env
.
PY2
:
    
YIELD_VALUE
=
chr
(
YIELD_VALUE
)
class
PyTracer
(
object
)
:
    
"
"
"
Python
implementation
of
the
raw
data
tracer
.
"
"
"
    
def
__init__
(
self
)
:
        
self
.
data
=
None
        
self
.
trace_arcs
=
False
        
self
.
should_trace
=
None
        
self
.
should_trace_cache
=
None
        
self
.
should_start_context
=
None
        
self
.
warn
=
None
        
self
.
threading
=
None
        
self
.
cur_file_dict
=
None
        
self
.
last_line
=
0
        
self
.
cur_file_name
=
None
        
self
.
context
=
None
        
self
.
started_context
=
False
        
self
.
data_stack
=
[
]
        
self
.
last_exc_back
=
None
        
self
.
last_exc_firstlineno
=
0
        
self
.
thread
=
None
        
self
.
stopped
=
False
        
self
.
_activity
=
False
        
self
.
in_atexit
=
False
        
atexit
.
register
(
setattr
self
'
in_atexit
'
True
)
    
def
__repr__
(
self
)
:
        
return
"
<
PyTracer
at
{
}
:
{
}
lines
in
{
}
files
>
"
.
format
(
            
id
(
self
)
            
sum
(
len
(
v
)
for
v
in
self
.
data
.
values
(
)
)
            
len
(
self
.
data
)
        
)
    
def
log
(
self
marker
*
args
)
:
        
"
"
"
For
hard
-
core
logging
of
what
this
tracer
is
doing
.
"
"
"
        
with
open
(
"
/
tmp
/
debug_trace
.
txt
"
"
a
"
)
as
f
:
            
f
.
write
(
"
{
}
{
:
x
}
.
{
:
x
}
[
{
}
]
{
:
x
}
{
}
\
n
"
.
format
(
                
marker
                
id
(
self
)
                
self
.
thread
.
ident
                
len
(
self
.
data_stack
)
                
self
.
threading
.
currentThread
(
)
.
ident
                
"
"
.
join
(
map
(
str
args
)
)
            
)
)
    
def
_trace
(
self
frame
event
arg_unused
)
:
        
"
"
"
The
trace
function
passed
to
sys
.
settrace
.
"
"
"
        
if
(
self
.
stopped
and
sys
.
gettrace
(
)
=
=
self
.
_trace
)
:
            
sys
.
settrace
(
None
)
            
return
None
        
if
self
.
last_exc_back
:
            
if
frame
=
=
self
.
last_exc_back
:
                
if
self
.
trace_arcs
and
self
.
cur_file_dict
:
                    
pair
=
(
self
.
last_line
-
self
.
last_exc_firstlineno
)
                    
self
.
cur_file_dict
[
pair
]
=
None
                
self
.
cur_file_dict
self
.
cur_file_name
self
.
last_line
self
.
started_context
=
(
                    
self
.
data_stack
.
pop
(
)
                
)
            
self
.
last_exc_back
=
None
        
if
event
=
=
'
call
'
:
            
if
self
.
should_start_context
and
self
.
context
is
None
:
                
context_maybe
=
self
.
should_start_context
(
frame
)
                
if
context_maybe
is
not
None
:
                    
self
.
context
=
context_maybe
                    
self
.
started_context
=
True
                    
self
.
switch_context
(
self
.
context
)
                
else
:
                    
self
.
started_context
=
False
            
else
:
                
self
.
started_context
=
False
            
self
.
_activity
=
True
            
self
.
data_stack
.
append
(
                
(
                    
self
.
cur_file_dict
                    
self
.
cur_file_name
                    
self
.
last_line
                    
self
.
started_context
                
)
            
)
            
filename
=
frame
.
f_code
.
co_filename
            
self
.
cur_file_name
=
filename
            
disp
=
self
.
should_trace_cache
.
get
(
filename
)
            
if
disp
is
None
:
                
disp
=
self
.
should_trace
(
filename
frame
)
                
self
.
should_trace_cache
[
filename
]
=
disp
            
self
.
cur_file_dict
=
None
            
if
disp
.
trace
:
                
tracename
=
disp
.
source_filename
                
if
tracename
not
in
self
.
data
:
                    
self
.
data
[
tracename
]
=
{
}
                
self
.
cur_file_dict
=
self
.
data
[
tracename
]
            
if
getattr
(
frame
'
f_lasti
'
-
1
)
<
0
:
                
self
.
last_line
=
-
frame
.
f_code
.
co_firstlineno
            
else
:
                
self
.
last_line
=
frame
.
f_lineno
        
elif
event
=
=
'
line
'
:
            
if
self
.
cur_file_dict
is
not
None
:
                
lineno
=
frame
.
f_lineno
                
if
self
.
trace_arcs
:
                    
self
.
cur_file_dict
[
(
self
.
last_line
lineno
)
]
=
None
                
else
:
                    
self
.
cur_file_dict
[
lineno
]
=
None
                
self
.
last_line
=
lineno
        
elif
event
=
=
'
return
'
:
            
if
self
.
trace_arcs
and
self
.
cur_file_dict
:
                
code
=
frame
.
f_code
.
co_code
                
if
(
not
code
)
or
code
[
frame
.
f_lasti
]
!
=
YIELD_VALUE
:
                    
first
=
frame
.
f_code
.
co_firstlineno
                    
self
.
cur_file_dict
[
(
self
.
last_line
-
first
)
]
=
None
            
self
.
cur_file_dict
self
.
cur_file_name
self
.
last_line
self
.
started_context
=
(
                
self
.
data_stack
.
pop
(
)
            
)
            
if
self
.
started_context
:
                
self
.
context
=
None
                
self
.
switch_context
(
None
)
        
elif
event
=
=
'
exception
'
:
            
self
.
last_exc_back
=
frame
.
f_back
            
self
.
last_exc_firstlineno
=
frame
.
f_code
.
co_firstlineno
        
return
self
.
_trace
    
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
this
Tracer
.
        
Return
a
Python
function
suitable
for
use
with
sys
.
settrace
(
)
.
        
"
"
"
        
self
.
stopped
=
False
        
if
self
.
threading
:
            
if
self
.
thread
is
None
:
                
self
.
thread
=
self
.
threading
.
currentThread
(
)
            
else
:
                
if
self
.
thread
.
ident
!
=
self
.
threading
.
currentThread
(
)
.
ident
:
                    
return
self
.
_trace
        
sys
.
settrace
(
self
.
_trace
)
        
return
self
.
_trace
    
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
this
Tracer
.
"
"
"
        
tf
=
sys
.
gettrace
(
)
        
self
.
stopped
=
True
        
if
self
.
threading
and
self
.
thread
.
ident
!
=
self
.
threading
.
currentThread
(
)
.
ident
:
            
return
        
if
self
.
warn
:
            
dont_warn
=
(
env
.
PYPY
and
env
.
PYPYVERSION
>
=
(
5
4
)
and
self
.
in_atexit
and
tf
is
None
)
            
if
(
not
dont_warn
)
and
tf
!
=
self
.
_trace
:
                
self
.
warn
(
                    
"
Trace
function
changed
measurement
is
likely
wrong
:
%
r
"
%
(
tf
)
                    
slug
=
"
trace
-
changed
"
                
)
    
def
activity
(
self
)
:
        
"
"
"
Has
there
been
any
activity
?
"
"
"
        
return
self
.
_activity
    
def
reset_activity
(
self
)
:
        
"
"
"
Reset
the
activity
(
)
flag
.
"
"
"
        
self
.
_activity
=
False
    
def
get_stats
(
self
)
:
        
"
"
"
Return
a
dictionary
of
statistics
or
None
.
"
"
"
        
return
None
