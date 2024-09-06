from
asyncio
import
get_event_loop
iscoroutine
from
functools
import
wraps
from
inspect
import
signature
async
def
_run_forever_coro
(
coro
args
kwargs
loop
)
:
    
'
'
'
    
This
helper
function
launches
an
async
main
function
that
was
tagged
with
    
forever
=
True
.
There
are
two
possibilities
:
    
-
The
function
is
a
normal
function
which
handles
initializing
the
event
      
loop
which
is
then
run
forever
    
-
The
function
is
a
coroutine
which
needs
to
be
scheduled
in
the
event
      
loop
which
is
then
run
forever
      
-
There
is
also
the
possibility
that
the
function
is
a
normal
function
        
wrapping
a
coroutine
function
    
The
function
is
therefore
called
unconditionally
and
scheduled
in
the
event
    
loop
if
the
return
value
is
a
coroutine
object
.
    
The
reason
this
is
a
separate
function
is
to
make
absolutely
sure
that
all
    
the
objects
created
are
garbage
collected
after
all
is
said
and
done
;
we
    
do
this
to
ensure
that
any
exceptions
raised
in
the
tasks
are
collected
    
ASAP
.
    
'
'
'
    
thing
=
coro
(
*
args
*
*
kwargs
)
    
if
iscoroutine
(
thing
)
:
        
await
thing
def
autoasync
(
coro
=
None
*
loop
=
None
forever
=
False
pass_loop
=
False
)
:
    
'
'
'
    
Convert
an
asyncio
coroutine
into
a
function
which
when
called
is
    
evaluted
in
an
event
loop
and
the
return
value
returned
.
This
is
intented
    
to
make
it
easy
to
write
entry
points
into
asyncio
coroutines
which
    
otherwise
need
to
be
explictly
evaluted
with
an
event
loop
'
s
    
run_until_complete
.
    
If
loop
is
given
it
is
used
as
the
event
loop
to
run
the
coro
in
.
If
it
    
is
None
(
the
default
)
the
loop
is
retreived
using
asyncio
.
get_event_loop
.
    
This
call
is
defered
until
the
decorated
function
is
called
so
that
    
callers
can
install
custom
event
loops
or
event
loop
policies
after
    
autoasync
is
applied
.
    
If
forever
is
True
the
loop
is
run
forever
after
the
decorated
coroutine
    
is
finished
.
Use
this
for
servers
created
with
asyncio
.
start_server
and
the
    
like
.
    
If
pass_loop
is
True
the
event
loop
object
is
passed
into
the
coroutine
    
as
the
loop
kwarg
when
the
wrapper
function
is
called
.
In
this
case
the
    
wrapper
function
'
s
__signature__
is
updated
to
remove
this
parameter
so
    
that
autoparse
can
still
be
used
on
it
without
generating
a
parameter
for
    
loop
.
    
This
coroutine
can
be
called
with
(
autoasync
(
.
.
.
)
)
or
without
    
(
autoasync
)
arguments
.
    
Examples
:
    
autoasync
    
def
get_file
(
host
port
)
:
        
reader
writer
=
yield
from
asyncio
.
open_connection
(
host
port
)
        
data
=
reader
.
read
(
)
        
sys
.
stdout
.
write
(
data
.
decode
(
)
)
    
get_file
(
host
port
)
    
autoasync
(
forever
=
True
pass_loop
=
True
)
    
def
server
(
host
port
loop
)
:
        
yield_from
loop
.
create_server
(
Proto
host
port
)
    
server
(
'
localhost
'
8899
)
    
'
'
'
    
if
coro
is
None
:
        
return
lambda
c
:
autoasync
(
            
c
loop
=
loop
            
forever
=
forever
            
pass_loop
=
pass_loop
)
    
if
pass_loop
:
        
old_sig
=
signature
(
coro
)
        
new_sig
=
old_sig
.
replace
(
parameters
=
(
            
param
for
name
param
in
old_sig
.
parameters
.
items
(
)
            
if
name
!
=
"
loop
"
)
)
    
wraps
(
coro
)
    
def
autoasync_wrapper
(
*
args
*
*
kwargs
)
:
        
local_loop
=
get_event_loop
(
)
if
loop
is
None
else
loop
        
if
pass_loop
:
            
bound_args
=
old_sig
.
bind_partial
(
)
            
bound_args
.
arguments
.
update
(
                
loop
=
local_loop
                
*
*
new_sig
.
bind
(
*
args
*
*
kwargs
)
.
arguments
)
            
args
kwargs
=
bound_args
.
args
bound_args
.
kwargs
        
if
forever
:
            
local_loop
.
create_task
(
_run_forever_coro
(
                
coro
args
kwargs
local_loop
            
)
)
            
local_loop
.
run_forever
(
)
        
else
:
            
return
local_loop
.
run_until_complete
(
coro
(
*
args
*
*
kwargs
)
)
    
if
pass_loop
:
        
autoasync_wrapper
.
__signature__
=
new_sig
    
return
autoasync_wrapper
