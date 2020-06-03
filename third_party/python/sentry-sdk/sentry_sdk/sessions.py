import
os
import
uuid
import
time
from
datetime
import
datetime
from
threading
import
Thread
Lock
from
contextlib
import
contextmanager
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
format_timestamp
if
MYPY
:
    
import
sentry_sdk
    
from
typing
import
Optional
    
from
typing
import
Union
    
from
typing
import
Any
    
from
typing
import
Dict
    
from
typing
import
Generator
    
from
sentry_sdk
.
_types
import
SessionStatus
def
is_auto_session_tracking_enabled
(
hub
=
None
)
:
    
"
"
"
Utility
function
to
find
out
if
session
tracking
is
enabled
.
"
"
"
    
if
hub
is
None
:
        
hub
=
sentry_sdk
.
Hub
.
current
    
should_track
=
hub
.
scope
.
_force_auto_session_tracking
    
if
should_track
is
None
:
        
exp
=
hub
.
client
.
options
[
"
_experiments
"
]
if
hub
.
client
else
{
}
        
should_track
=
exp
.
get
(
"
auto_session_tracking
"
)
    
return
should_track
contextmanager
def
auto_session_tracking
(
hub
=
None
)
:
    
"
"
"
Starts
and
stops
a
session
automatically
around
a
block
.
"
"
"
    
if
hub
is
None
:
        
hub
=
sentry_sdk
.
Hub
.
current
    
should_track
=
is_auto_session_tracking_enabled
(
hub
)
    
if
should_track
:
        
hub
.
start_session
(
)
    
try
:
        
yield
    
finally
:
        
if
should_track
:
            
hub
.
end_session
(
)
def
_make_uuid
(
    
val
)
:
    
if
isinstance
(
val
uuid
.
UUID
)
:
        
return
val
    
return
uuid
.
UUID
(
val
)
TERMINAL_SESSION_STATES
=
(
"
exited
"
"
abnormal
"
"
crashed
"
)
class
SessionFlusher
(
object
)
:
    
def
__init__
(
        
self
        
flush_func
        
flush_interval
=
10
    
)
:
        
self
.
flush_func
=
flush_func
        
self
.
flush_interval
=
flush_interval
        
self
.
pending
=
{
}
        
self
.
_thread
=
None
        
self
.
_thread_lock
=
Lock
(
)
        
self
.
_thread_for_pid
=
None
        
self
.
_running
=
True
    
def
flush
(
self
)
:
        
pending
=
self
.
pending
        
self
.
pending
=
{
}
        
self
.
flush_func
(
list
(
pending
.
values
(
)
)
)
    
def
_ensure_running
(
self
)
:
        
if
self
.
_thread_for_pid
=
=
os
.
getpid
(
)
and
self
.
_thread
is
not
None
:
            
return
None
        
with
self
.
_thread_lock
:
            
if
self
.
_thread_for_pid
=
=
os
.
getpid
(
)
and
self
.
_thread
is
not
None
:
                
return
None
            
def
_thread
(
)
:
                
while
self
.
_running
:
                    
time
.
sleep
(
self
.
flush_interval
)
                    
if
self
.
pending
and
self
.
_running
:
                        
self
.
flush
(
)
            
thread
=
Thread
(
target
=
_thread
)
            
thread
.
daemon
=
True
            
thread
.
start
(
)
            
self
.
_thread
=
thread
            
self
.
_thread_for_pid
=
os
.
getpid
(
)
        
return
None
    
def
add_session
(
        
self
session
    
)
:
        
self
.
pending
[
session
.
sid
.
hex
]
=
session
.
to_json
(
)
        
self
.
_ensure_running
(
)
    
def
kill
(
self
)
:
        
self
.
_running
=
False
    
def
__del__
(
self
)
:
        
self
.
kill
(
)
class
Session
(
object
)
:
    
def
__init__
(
        
self
        
sid
=
None
        
did
=
None
        
timestamp
=
None
        
started
=
None
        
duration
=
None
        
status
=
None
        
release
=
None
        
environment
=
None
        
user_agent
=
None
        
ip_address
=
None
        
errors
=
None
        
user
=
None
    
)
:
        
if
sid
is
None
:
            
sid
=
uuid
.
uuid4
(
)
        
if
started
is
None
:
            
started
=
datetime
.
utcnow
(
)
        
if
status
is
None
:
            
status
=
"
ok
"
        
self
.
status
=
status
        
self
.
did
=
None
        
self
.
started
=
started
        
self
.
release
=
None
        
self
.
environment
=
None
        
self
.
duration
=
None
        
self
.
user_agent
=
None
        
self
.
ip_address
=
None
        
self
.
errors
=
0
        
self
.
update
(
            
sid
=
sid
            
did
=
did
            
timestamp
=
timestamp
            
duration
=
duration
            
release
=
release
            
environment
=
environment
            
user_agent
=
user_agent
            
ip_address
=
ip_address
            
errors
=
errors
            
user
=
user
        
)
    
def
update
(
        
self
        
sid
=
None
        
did
=
None
        
timestamp
=
None
        
duration
=
None
        
status
=
None
        
release
=
None
        
environment
=
None
        
user_agent
=
None
        
ip_address
=
None
        
errors
=
None
        
user
=
None
    
)
:
        
if
user
:
            
if
ip_address
is
None
:
                
ip_address
=
user
.
get
(
"
ip_address
"
)
            
if
did
is
None
:
                
did
=
user
.
get
(
"
id
"
)
or
user
.
get
(
"
email
"
)
or
user
.
get
(
"
username
"
)
        
if
sid
is
not
None
:
            
self
.
sid
=
_make_uuid
(
sid
)
        
if
did
is
not
None
:
            
self
.
did
=
str
(
did
)
        
if
timestamp
is
None
:
            
timestamp
=
datetime
.
utcnow
(
)
        
self
.
timestamp
=
timestamp
        
if
duration
is
not
None
:
            
self
.
duration
=
duration
        
if
release
is
not
None
:
            
self
.
release
=
release
        
if
environment
is
not
None
:
            
self
.
environment
=
environment
        
if
ip_address
is
not
None
:
            
self
.
ip_address
=
ip_address
        
if
user_agent
is
not
None
:
            
self
.
user_agent
=
user_agent
        
if
errors
is
not
None
:
            
self
.
errors
=
errors
        
if
status
is
not
None
:
            
self
.
status
=
status
    
def
close
(
        
self
status
=
None
    
)
:
        
if
status
is
None
and
self
.
status
=
=
"
ok
"
:
            
status
=
"
exited
"
        
if
status
is
not
None
:
            
self
.
update
(
status
=
status
)
    
def
to_json
(
self
)
:
        
rv
=
{
            
"
sid
"
:
str
(
self
.
sid
)
            
"
init
"
:
True
            
"
started
"
:
format_timestamp
(
self
.
started
)
            
"
timestamp
"
:
format_timestamp
(
self
.
timestamp
)
            
"
status
"
:
self
.
status
        
}
        
if
self
.
errors
:
            
rv
[
"
errors
"
]
=
self
.
errors
        
if
self
.
did
is
not
None
:
            
rv
[
"
did
"
]
=
self
.
did
        
if
self
.
duration
is
not
None
:
            
rv
[
"
duration
"
]
=
self
.
duration
        
attrs
=
{
}
        
if
self
.
release
is
not
None
:
            
attrs
[
"
release
"
]
=
self
.
release
        
if
self
.
environment
is
not
None
:
            
attrs
[
"
environment
"
]
=
self
.
environment
        
if
self
.
ip_address
is
not
None
:
            
attrs
[
"
ip_address
"
]
=
self
.
ip_address
        
if
self
.
user_agent
is
not
None
:
            
attrs
[
"
user_agent
"
]
=
self
.
user_agent
        
if
attrs
:
            
rv
[
"
attrs
"
]
=
attrs
        
return
rv
