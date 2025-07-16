import
codecs
import
errno
import
io
import
os
import
signal
import
subprocess
import
sys
import
threading
import
time
import
traceback
from
datetime
import
datetime
from
queue
import
Empty
Queue
MOZPROCESS_DEBUG
=
os
.
getenv
(
"
MOZPROCESS_DEBUG
"
)
INTERVAL_PROCESS_ALIVE_CHECK
=
0
.
02
isWin
=
os
.
name
=
=
"
nt
"
isPosix
=
os
.
name
=
=
"
posix
"
if
isWin
:
    
from
ctypes
import
WinError
addressof
byref
c_longlong
c_ulong
sizeof
    
from
.
import
winprocess
    
from
.
qijo
import
(
        
IO_COUNTERS
        
JOBOBJECT_ASSOCIATE_COMPLETION_PORT
        
JOBOBJECT_BASIC_LIMIT_INFORMATION
        
JOBOBJECT_EXTENDED_LIMIT_INFORMATION
        
JobObjectAssociateCompletionPortInformation
        
JobObjectExtendedLimitInformation
    
)
class
ProcessHandlerMixin
:
    
"
"
"
    
A
class
for
launching
and
manipulating
local
processes
.
    
:
param
cmd
:
command
to
run
.
May
be
a
string
or
a
list
.
If
specified
as
a
list
the
first
      
element
will
be
interpreted
as
the
command
and
all
additional
elements
will
be
interpreted
      
as
arguments
to
that
command
.
    
:
param
args
:
list
of
arguments
to
pass
to
the
command
(
defaults
to
None
)
.
Must
not
be
set
when
      
cmd
is
specified
as
a
list
.
    
:
param
cwd
:
working
directory
for
command
(
defaults
to
None
)
.
    
:
param
env
:
is
the
environment
to
use
for
the
process
(
defaults
to
os
.
environ
)
.
    
:
param
ignore_children
:
causes
system
to
ignore
child
processes
when
True
      
defaults
to
False
(
which
tracks
child
processes
)
.
    
:
param
kill_on_timeout
:
when
True
the
process
will
be
killed
when
a
timeout
is
reached
.
      
When
False
the
caller
is
responsible
for
killing
the
process
.
      
Failure
to
do
so
could
cause
a
call
to
wait
(
)
to
hang
indefinitely
.
(
Defaults
to
True
.
)
    
:
param
processOutputLine
:
function
or
list
of
functions
to
be
called
for
        
each
line
of
output
produced
by
the
process
(
defaults
to
an
empty
        
list
)
.
    
:
param
processStderrLine
:
function
or
list
of
functions
to
be
called
        
for
each
line
of
error
output
-
stderr
-
produced
by
the
process
        
(
defaults
to
an
empty
list
)
.
If
this
is
not
specified
stderr
lines
        
will
be
sent
to
the
*
processOutputLine
*
callbacks
.
    
:
param
onTimeout
:
function
or
list
of
functions
to
be
called
when
the
process
times
out
.
    
:
param
onFinish
:
function
or
list
of
functions
to
be
called
when
the
process
terminates
      
normally
without
timing
out
.
    
:
param
kwargs
:
additional
keyword
args
to
pass
directly
into
Popen
.
    
NOTE
:
Child
processes
will
be
tracked
by
default
.
If
for
any
reason
    
we
are
unable
to
track
child
processes
and
ignore_children
is
set
to
False
    
then
we
will
fall
back
to
only
tracking
the
root
process
.
The
fallback
    
will
be
logged
.
    
"
"
"
    
class
Process
(
subprocess
.
Popen
)
:
        
"
"
"
        
Represents
our
view
of
a
subprocess
.
        
It
adds
a
kill
(
)
method
which
allows
it
to
be
stopped
explicitly
.
        
"
"
"
        
MAX_IOCOMPLETION_PORT_NOTIFICATION_DELAY
=
180
        
TIMEOUT_BEFORE_SIGKILL
=
1
.
0
        
def
__init__
(
            
self
            
args
            
bufsize
=
0
            
executable
=
None
            
stdin
=
None
            
stdout
=
None
            
stderr
=
None
            
preexec_fn
=
None
            
close_fds
=
False
            
shell
=
False
            
cwd
=
None
            
env
=
None
            
universal_newlines
=
False
            
startupinfo
=
None
            
creationflags
=
0
            
ignore_children
=
False
            
encoding
=
"
utf
-
8
"
        
)
:
            
self
.
_ignore_children
=
ignore_children
            
self
.
_job
=
None
            
self
.
_io_port
=
None
            
if
isWin
:
                
self
.
_cleanup_lock
=
threading
.
Lock
(
)
            
if
not
self
.
_ignore_children
and
not
isWin
:
                
def
setpgidfn
(
)
:
                    
os
.
setpgid
(
0
0
)
                
preexec_fn
=
setpgidfn
            
kwargs
=
{
                
"
bufsize
"
:
bufsize
                
"
executable
"
:
executable
                
"
stdin
"
:
stdin
                
"
stdout
"
:
stdout
                
"
stderr
"
:
stderr
                
"
preexec_fn
"
:
preexec_fn
                
"
close_fds
"
:
close_fds
                
"
shell
"
:
shell
                
"
cwd
"
:
cwd
                
"
env
"
:
env
                
"
startupinfo
"
:
startupinfo
                
"
creationflags
"
:
creationflags
            
}
            
if
sys
.
version_info
.
minor
>
=
6
and
universal_newlines
:
                
kwargs
[
"
universal_newlines
"
]
=
universal_newlines
                
kwargs
[
"
encoding
"
]
=
encoding
            
try
:
                
subprocess
.
Popen
.
__init__
(
self
args
*
*
kwargs
)
            
except
OSError
:
                
print
(
args
file
=
sys
.
stderr
)
                
raise
        
def
debug
(
self
msg
)
:
            
if
not
MOZPROCESS_DEBUG
:
                
return
            
thread
=
threading
.
current_thread
(
)
.
name
            
print
(
f
"
DBG
:
:
MOZPROC
PID
:
{
self
.
pid
}
(
{
thread
}
)
|
{
msg
}
"
)
        
def
__del__
(
self
)
:
            
if
isWin
:
                
_maxint
=
sys
.
maxsize
                
handle
=
getattr
(
self
"
_handle
"
None
)
                
if
handle
:
                    
self
.
_handle
=
int
(
self
.
_handle
)
                    
self
.
_internal_poll
(
_deadstate
=
_maxint
)
                    
self
.
_handle
=
handle
                
if
handle
or
self
.
_job
or
self
.
_io_port
:
                    
self
.
_cleanup
(
)
            
else
:
                
subprocess
.
Popen
.
__del__
(
self
)
        
def
send_signal
(
self
sig
=
None
)
:
            
if
isWin
:
                
try
:
                    
if
not
self
.
_ignore_children
and
self
.
_handle
and
self
.
_job
:
                        
self
.
debug
(
"
calling
TerminateJobObject
"
)
                        
winprocess
.
TerminateJobObject
(
                            
self
.
_job
winprocess
.
ERROR_CONTROL_C_EXIT
                        
)
                    
elif
self
.
_handle
:
                        
self
.
debug
(
"
calling
TerminateProcess
"
)
                        
winprocess
.
TerminateProcess
(
                            
self
.
_handle
winprocess
.
ERROR_CONTROL_C_EXIT
                        
)
                
except
OSError
:
                    
self
.
_cleanup
(
)
                    
traceback
.
print_exc
(
)
                    
raise
OSError
(
"
Could
not
terminate
process
"
)
            
else
:
                
def
send_sig
(
sig
retries
=
0
)
:
                    
pid
=
self
.
detached_pid
or
self
.
pid
                    
if
not
self
.
_ignore_children
:
                        
try
:
                            
os
.
killpg
(
pid
sig
)
                        
except
BaseException
as
e
:
                            
if
retries
<
1
and
getattr
(
e
"
errno
"
None
)
=
=
errno
.
EPERM
:
                                
try
:
                                    
os
.
waitpid
(
-
pid
0
)
                                
finally
:
                                    
return
send_sig
(
sig
retries
+
1
)
                            
if
getattr
(
e
"
errno
"
None
)
!
=
errno
.
ESRCH
:
                                
print
(
                                    
"
Could
not
terminate
process
:
%
s
"
%
self
.
pid
                                    
file
=
sys
.
stderr
                                
)
                                
raise
                    
else
:
                        
os
.
kill
(
pid
sig
)
                
if
sig
is
None
and
isPosix
:
                    
send_sig
(
signal
.
SIGTERM
)
                    
limit
=
time
.
time
(
)
+
self
.
TIMEOUT_BEFORE_SIGKILL
                    
while
time
.
time
(
)
<
=
limit
:
                        
if
self
.
poll
(
)
is
not
None
:
                            
break
                        
time
.
sleep
(
INTERVAL_PROCESS_ALIVE_CHECK
)
                    
else
:
                        
send_sig
(
signal
.
SIGKILL
)
                
else
:
                    
send_sig
(
sig
or
signal
.
SIGKILL
)
        
def
kill
(
self
sig
=
None
timeout
=
None
)
:
            
self
.
send_signal
(
sig
)
            
self
.
returncode
=
self
.
wait
(
timeout
)
            
self
.
_cleanup
(
)
            
return
self
.
returncode
        
def
poll
(
self
)
:
            
"
"
"
Popen
.
poll
            
Check
if
child
process
has
terminated
.
Set
and
return
returncode
attribute
.
            
"
"
"
            
if
isWin
:
                
returncode
=
self
.
_custom_wait
(
timeout
=
0
)
            
else
:
                
returncode
=
subprocess
.
Popen
.
poll
(
self
)
            
if
returncode
is
not
None
:
                
self
.
_cleanup
(
)
            
return
returncode
        
def
wait
(
self
timeout
=
None
)
:
            
"
"
"
Popen
.
wait
            
Called
to
wait
for
a
running
process
to
shut
down
and
return
            
its
exit
code
            
Returns
the
main
process
'
s
exit
code
            
"
"
"
            
self
.
returncode
=
self
.
_custom_wait
(
timeout
=
timeout
)
            
if
self
.
returncode
is
not
None
:
                
self
.
_cleanup
(
)
            
return
self
.
returncode
        
"
"
"
Private
Members
of
Process
class
"
"
"
        
if
isWin
:
            
def
_execute_child
(
self
*
args_tuple
)
:
                
(
                    
args
                    
executable
                    
preexec_fn
                    
close_fds
                    
pass_fds
                    
cwd
                    
env
                    
startupinfo
                    
creationflags
                    
shell
                    
p2cread
                    
p2cwrite
                    
c2pread
                    
c2pwrite
                    
errread
                    
errwrite
                    
*
_
                
)
=
args_tuple
                
if
not
isinstance
(
args
str
)
:
                    
args
=
subprocess
.
list2cmdline
(
args
)
                
creationflags
|
=
winprocess
.
CREATE_NEW_PROCESS_GROUP
                
if
startupinfo
is
None
:
                    
startupinfo
=
winprocess
.
STARTUPINFO
(
)
                
if
None
not
in
(
p2cread
c2pwrite
errwrite
)
:
                    
startupinfo
.
dwFlags
|
=
winprocess
.
STARTF_USESTDHANDLES
                    
startupinfo
.
hStdInput
=
int
(
p2cread
)
                    
startupinfo
.
hStdOutput
=
int
(
c2pwrite
)
                    
startupinfo
.
hStdError
=
int
(
errwrite
)
                
if
shell
:
                    
startupinfo
.
dwFlags
|
=
winprocess
.
STARTF_USESHOWWINDOW
                    
startupinfo
.
wShowWindow
=
winprocess
.
SW_HIDE
                    
comspec
=
os
.
environ
.
get
(
"
COMSPEC
"
"
cmd
.
exe
"
)
                    
args
=
comspec
+
"
/
c
"
+
args
                
can_create_job
=
winprocess
.
CanCreateJobObject
(
)
                
can_nest_jobs
=
self
.
_can_nest_jobs
(
)
                
if
not
(
can_create_job
or
can_nest_jobs
)
and
not
self
.
_ignore_children
:
                    
print
(
                        
"
ProcessManager
UNABLE
to
use
job
objects
to
manage
"
                        
"
child
processes
"
                        
file
=
sys
.
stderr
                    
)
                
creationflags
|
=
winprocess
.
CREATE_SUSPENDED
                
creationflags
|
=
winprocess
.
CREATE_UNICODE_ENVIRONMENT
                
if
can_create_job
:
                    
creationflags
|
=
winprocess
.
CREATE_BREAKAWAY_FROM_JOB
                
if
not
(
can_create_job
or
can_nest_jobs
)
:
                    
print
(
"
ProcessManager
NOT
managing
child
processes
"
)
                
hp
ht
pid
tid
=
winprocess
.
CreateProcess
(
                    
executable
                    
args
                    
None
                    
None
                    
1
                    
creationflags
                    
winprocess
.
EnvironmentBlock
(
env
)
                    
cwd
                    
startupinfo
                
)
                
self
.
_child_created
=
True
                
self
.
_handle
=
hp
                
self
.
_thread
=
ht
                
self
.
pid
=
pid
                
self
.
tid
=
tid
                
if
not
self
.
_ignore_children
and
(
can_create_job
or
can_nest_jobs
)
:
                    
try
:
                        
self
.
_io_port
=
winprocess
.
CreateIoCompletionPort
(
)
                        
self
.
_job
=
winprocess
.
CreateJobObject
(
)
                        
joacp
=
JOBOBJECT_ASSOCIATE_COMPLETION_PORT
(
                            
winprocess
.
COMPKEY_JOBOBJECT
self
.
_io_port
                        
)
                        
winprocess
.
SetInformationJobObject
(
                            
self
.
_job
                            
JobObjectAssociateCompletionPortInformation
                            
addressof
(
joacp
)
                            
sizeof
(
joacp
)
                        
)
                        
limit_flags
=
winprocess
.
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
                        
if
not
can_nest_jobs
:
                            
limit_flags
|
=
winprocess
.
JOB_OBJECT_LIMIT_BREAKAWAY_OK
                        
jbli
=
JOBOBJECT_BASIC_LIMIT_INFORMATION
(
                            
c_longlong
(
0
)
                            
c_longlong
(
0
)
                            
limit_flags
                            
0
                            
0
                            
0
                            
None
                            
0
                            
0
                        
)
                        
iocntr
=
IO_COUNTERS
(
)
                        
jeli
=
JOBOBJECT_EXTENDED_LIMIT_INFORMATION
(
                            
jbli
                            
iocntr
                            
0
                            
0
                            
0
                            
0
                        
)
                        
winprocess
.
SetInformationJobObject
(
                            
self
.
_job
                            
JobObjectExtendedLimitInformation
                            
addressof
(
jeli
)
                            
sizeof
(
jeli
)
                        
)
                        
winprocess
.
AssignProcessToJobObject
(
self
.
_job
int
(
hp
)
)
                        
self
.
_process_events
=
Queue
(
)
                        
self
.
_procmgrthread
=
threading
.
Thread
(
target
=
self
.
_procmgr
)
                    
except
Exception
:
                        
print
(
                            
"
"
"
Exception
trying
to
use
job
objects
;
falling
back
to
not
using
job
objects
for
managing
child
processes
"
"
"
                            
file
=
sys
.
stderr
                        
)
                        
tb
=
traceback
.
format_exc
(
)
                        
print
(
tb
file
=
sys
.
stderr
)
                        
self
.
_cleanup_job_io_port
(
)
                
else
:
                    
self
.
_job
=
None
                
winprocess
.
ResumeThread
(
int
(
ht
)
)
                
if
getattr
(
self
"
_procmgrthread
"
None
)
:
                    
self
.
_procmgrthread
.
start
(
)
                
ht
.
Close
(
)
                
for
i
in
(
p2cread
c2pwrite
errwrite
)
:
                    
if
i
is
not
None
:
                        
i
.
Close
(
)
            
def
_can_nest_jobs
(
self
)
:
                
winver
=
sys
.
getwindowsversion
(
)
                
return
winver
.
major
>
6
or
winver
.
major
=
=
6
and
winver
.
minor
>
=
2
            
def
_procmgr
(
self
)
:
                
if
not
(
self
.
_io_port
)
or
not
(
self
.
_job
)
:
                    
return
                
try
:
                    
self
.
_poll_iocompletion_port
(
)
                
except
Exception
:
                    
traceback
.
print_exc
(
)
                    
self
.
_process_events
.
put
(
{
}
)
                
except
KeyboardInterrupt
:
                    
raise
KeyboardInterrupt
            
def
_poll_iocompletion_port
(
self
)
:
                
self
.
_spawned_procs
=
{
}
                
countdowntokill
=
0
                
self
.
debug
(
"
start
polling
IO
completion
port
"
)
                
while
True
:
                    
msgid
=
c_ulong
(
0
)
                    
compkey
=
c_ulong
(
0
)
                    
pid
=
c_ulong
(
0
)
                    
portstatus
=
winprocess
.
GetQueuedCompletionStatus
(
                        
self
.
_io_port
byref
(
msgid
)
byref
(
compkey
)
byref
(
pid
)
5000
                    
)
                    
if
countdowntokill
!
=
0
:
                        
diff
=
datetime
.
now
(
)
-
countdowntokill
                        
if
diff
.
seconds
>
self
.
MAX_IOCOMPLETION_PORT_NOTIFICATION_DELAY
:
                            
print
(
                                
"
WARNING
|
IO
Completion
Port
failed
to
signal
"
                                
"
process
shutdown
"
                                
file
=
sys
.
stderr
                            
)
                            
print
(
                                
"
Parent
process
%
s
exited
with
children
alive
:
"
                                
%
self
.
pid
                                
file
=
sys
.
stderr
                            
)
                            
print
(
                                
"
PIDS
:
%
s
"
                                
%
"
"
.
join
(
[
str
(
i
)
for
i
in
self
.
_spawned_procs
]
)
                                
file
=
sys
.
stderr
                            
)
                            
print
(
                                
"
Attempting
to
kill
them
but
no
guarantee
of
success
"
                                
file
=
sys
.
stderr
                            
)
                            
self
.
send_signal
(
)
                            
self
.
_process_events
.
put
(
{
self
.
pid
:
"
FINISHED
"
}
)
                            
break
                    
if
not
portstatus
:
                        
errcode
=
winprocess
.
GetLastError
(
)
                        
if
errcode
=
=
winprocess
.
ERROR_ABANDONED_WAIT_0
:
                            
print
(
                                
"
IO
Completion
Port
unexpectedly
closed
"
                                
file
=
sys
.
stderr
                            
)
                            
self
.
_process_events
.
put
(
{
self
.
pid
:
"
FINISHED
"
}
)
                            
break
                        
elif
errcode
=
=
winprocess
.
WAIT_TIMEOUT
:
                            
continue
                        
else
:
                            
print
(
                                
"
Error
Code
%
s
trying
to
query
IO
Completion
Port
"
                                
"
exiting
"
%
errcode
                                
file
=
sys
.
stderr
                            
)
                            
raise
WinError
(
errcode
)
                            
break
                    
if
compkey
.
value
=
=
winprocess
.
COMPKEY_TERMINATE
.
value
:
                        
self
.
debug
(
"
compkeyterminate
detected
"
)
                        
break
                    
if
compkey
.
value
=
=
winprocess
.
COMPKEY_JOBOBJECT
.
value
:
                        
if
msgid
.
value
=
=
winprocess
.
JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO
:
                            
self
.
debug
(
"
job
object
msg
active
processes
zero
"
)
                            
self
.
_process_events
.
put
(
{
self
.
pid
:
"
FINISHED
"
}
)
                            
break
                        
elif
msgid
.
value
=
=
winprocess
.
JOB_OBJECT_MSG_NEW_PROCESS
:
                            
if
pid
.
value
!
=
self
.
pid
:
                                
self
.
_spawned_procs
[
pid
.
value
]
=
1
                                
self
.
debug
(
                                    
"
new
process
detected
with
pid
value
:
%
s
"
                                    
%
pid
.
value
                                
)
                        
elif
msgid
.
value
=
=
winprocess
.
JOB_OBJECT_MSG_EXIT_PROCESS
:
                            
self
.
debug
(
"
process
id
%
s
exited
normally
"
%
pid
.
value
)
                            
if
pid
.
value
=
=
self
.
pid
and
len
(
self
.
_spawned_procs
)
>
0
:
                                
countdowntokill
=
datetime
.
now
(
)
                            
elif
pid
.
value
in
self
.
_spawned_procs
:
                                
del
self
.
_spawned_procs
[
pid
.
value
]
                        
elif
(
                            
msgid
.
value
                            
=
=
winprocess
.
JOB_OBJECT_MSG_ABNORMAL_EXIT_PROCESS
                        
)
:
                            
self
.
debug
(
"
process
id
%
s
exited
abnormally
"
%
pid
.
value
)
                            
if
pid
.
value
=
=
self
.
pid
and
len
(
self
.
_spawned_procs
)
>
0
:
                                
countdowntokill
=
datetime
.
now
(
)
                            
elif
pid
.
value
in
self
.
_spawned_procs
:
                                
del
self
.
_spawned_procs
[
pid
.
value
]
                        
else
:
                            
self
.
debug
(
"
We
got
a
message
%
s
"
%
msgid
.
value
)
                            
pass
            
def
_custom_wait
(
self
timeout
=
None
)
:
                
"
"
"
Custom
implementation
of
wait
.
                
-
timeout
:
number
of
seconds
before
timing
out
.
If
None
                  
will
wait
indefinitely
.
                
"
"
"
                
if
self
.
_handle
:
                    
returncode
=
winprocess
.
GetExitCodeProcess
(
self
.
_handle
)
                    
if
returncode
!
=
winprocess
.
STILL_ACTIVE
:
                        
self
.
returncode
=
returncode
                
else
:
                    
return
self
.
returncode
                
the_timeout
=
0
.
1
if
timeout
is
None
else
timeout
                
if
self
.
_job
:
                    
self
.
debug
(
"
waiting
with
IO
completion
port
"
)
                    
try
:
                        
while
True
:
                            
try
:
                                
item
=
self
.
_process_events
.
get
(
timeout
=
the_timeout
)
                            
except
Empty
:
                                
if
timeout
is
None
:
                                    
continue
                                
else
:
                                    
raise
                            
break
                        
self
.
_process_events
.
put
(
item
)
                        
if
item
[
self
.
pid
]
=
=
"
FINISHED
"
:
                            
self
.
debug
(
"
received
'
FINISHED
'
from
_procmgrthread
"
)
                            
self
.
_process_events
.
task_done
(
)
                    
except
Empty
:
                        
pass
                    
except
Exception
:
                        
traceback
.
print_exc
(
)
                        
raise
OSError
(
                            
"
IO
Completion
Port
failed
to
signal
process
shutdown
"
                        
)
                    
finally
:
                        
if
self
.
_handle
:
                            
returncode
=
winprocess
.
GetExitCodeProcess
(
self
.
_handle
)
                            
if
returncode
!
=
winprocess
.
STILL_ACTIVE
:
                                
self
.
returncode
=
returncode
                
else
:
                    
self
.
debug
(
"
waiting
without
IO
completion
port
"
)
                    
if
not
self
.
_ignore_children
:
                        
self
.
debug
(
"
NOT
USING
JOB
OBJECTS
!
!
!
"
)
                    
if
self
.
returncode
is
not
None
:
                        
return
self
.
returncode
                    
rc
=
None
                    
if
self
.
_handle
:
                        
the_timeout
=
int
(
the_timeout
*
1000
)
                        
while
True
:
                            
rc
=
winprocess
.
WaitForSingleObject
(
                                
self
.
_handle
the_timeout
                            
)
                            
if
timeout
is
None
and
rc
=
=
winprocess
.
WAIT_TIMEOUT
:
                                
continue
                            
break
                    
if
rc
=
=
winprocess
.
WAIT_TIMEOUT
:
                        
pass
                    
elif
rc
=
=
winprocess
.
WAIT_OBJECT_0
:
                        
print
(
"
Single
process
terminated
successfully
"
)
                        
self
.
returncode
=
winprocess
.
GetExitCodeProcess
(
self
.
_handle
)
                    
else
:
                        
rc
=
winprocess
.
GetLastError
(
)
                        
if
rc
:
                            
raise
WinError
(
rc
)
                
return
self
.
returncode
            
def
_cleanup_job_io_port
(
self
)
:
                
"
"
"
Do
the
job
and
IO
port
cleanup
separately
because
there
are
                
cases
where
we
want
to
clean
these
without
killing
_handle
                
(
i
.
e
.
if
we
fail
to
create
the
job
object
in
the
first
place
)
                
"
"
"
                
if
(
                    
getattr
(
self
"
_job
"
)
                    
and
self
.
_job
!
=
winprocess
.
INVALID_HANDLE_VALUE
                
)
:
                    
self
.
_job
.
Close
(
)
                    
self
.
_job
=
None
                
else
:
                    
self
.
_job
=
None
                
if
(
                    
getattr
(
self
"
_io_port
"
None
)
                    
and
self
.
_io_port
!
=
winprocess
.
INVALID_HANDLE_VALUE
                
)
:
                    
self
.
_io_port
.
Close
(
)
                    
self
.
_io_port
=
None
                
else
:
                    
self
.
_io_port
=
None
                
if
getattr
(
self
"
_procmgrthread
"
None
)
:
                    
self
.
_procmgrthread
=
None
            
def
_cleanup
(
self
)
:
                
self
.
_cleanup_lock
.
acquire
(
)
                
self
.
_cleanup_job_io_port
(
)
                
if
self
.
_thread
and
self
.
_thread
!
=
winprocess
.
INVALID_HANDLE_VALUE
:
                    
self
.
_thread
.
Close
(
)
                    
self
.
_thread
=
None
                
else
:
                    
self
.
_thread
=
None
                
if
self
.
_handle
and
self
.
_handle
!
=
winprocess
.
INVALID_HANDLE_VALUE
:
                    
self
.
_handle
.
Close
(
)
                    
self
.
_handle
=
None
                
else
:
                    
self
.
_handle
=
None
                
self
.
_cleanup_lock
.
release
(
)
        
else
:
            
def
_custom_wait
(
self
timeout
=
None
)
:
                
"
"
"
Haven
'
t
found
any
reason
to
differentiate
between
these
platforms
                
so
they
all
use
the
same
wait
callback
.
If
it
is
necessary
to
                
craft
different
styles
of
wait
then
a
new
_custom_wait
method
                
could
be
easily
implemented
.
                
"
"
"
                
try
:
                    
subprocess
.
Popen
.
wait
(
self
timeout
=
timeout
)
                
except
subprocess
.
TimeoutExpired
:
                    
pass
                
return
self
.
returncode
            
def
_cleanup
(
self
)
:
                
pass
    
def
__init__
(
        
self
        
cmd
        
args
=
None
        
cwd
=
None
        
env
=
None
        
ignore_children
=
False
        
kill_on_timeout
=
True
        
processOutputLine
=
(
)
        
processStderrLine
=
(
)
        
onTimeout
=
(
)
        
onFinish
=
(
)
        
*
*
kwargs
    
)
:
        
self
.
cmd
=
cmd
        
self
.
args
=
args
        
self
.
cwd
=
cwd
        
self
.
didTimeout
=
False
        
self
.
didOutputTimeout
=
False
        
self
.
_ignore_children
=
ignore_children
        
self
.
keywordargs
=
kwargs
        
self
.
read_buffer
=
"
"
        
if
env
is
None
:
            
env
=
os
.
environ
.
copy
(
)
        
self
.
env
=
env
        
def
to_callable_list
(
arg
)
:
            
if
callable
(
arg
)
:
                
arg
=
[
arg
]
            
return
CallableList
(
arg
)
        
processOutputLine
=
to_callable_list
(
processOutputLine
)
        
processStderrLine
=
to_callable_list
(
processStderrLine
)
        
onTimeout
=
to_callable_list
(
onTimeout
)
        
onFinish
=
to_callable_list
(
onFinish
)
        
def
on_timeout
(
)
:
            
self
.
didTimeout
=
True
            
self
.
didOutputTimeout
=
self
.
reader
.
didOutputTimeout
            
if
kill_on_timeout
:
                
self
.
kill
(
)
        
onTimeout
.
insert
(
0
on_timeout
)
        
self
.
_stderr
=
subprocess
.
STDOUT
        
if
processStderrLine
:
            
self
.
_stderr
=
subprocess
.
PIPE
        
self
.
reader
=
ProcessReader
(
            
stdout_callback
=
processOutputLine
            
stderr_callback
=
processStderrLine
            
finished_callback
=
onFinish
            
timeout_callback
=
onTimeout
        
)
        
if
isinstance
(
self
.
cmd
list
)
:
            
if
self
.
args
is
not
None
:
                
raise
TypeError
(
"
cmd
and
args
must
not
both
be
lists
"
)
            
(
self
.
cmd
self
.
args
)
=
(
self
.
cmd
[
0
]
self
.
cmd
[
1
:
]
)
        
elif
self
.
args
is
None
:
            
self
.
args
=
[
]
    
def
debug
(
self
msg
)
:
        
if
not
MOZPROCESS_DEBUG
:
            
return
        
cmd
=
self
.
cmd
.
split
(
os
.
sep
)
[
-
1
:
]
        
print
(
f
"
DBG
:
:
MOZPROC
ProcessHandlerMixin
{
cmd
}
|
{
msg
}
"
)
    
property
    
def
timedOut
(
self
)
:
        
"
"
"
True
if
the
process
has
timed
out
for
any
reason
.
"
"
"
        
return
self
.
didTimeout
    
property
    
def
outputTimedOut
(
self
)
:
        
"
"
"
True
if
the
process
has
timed
out
for
no
output
.
"
"
"
        
return
self
.
didOutputTimeout
    
property
    
def
commandline
(
self
)
:
        
"
"
"
the
string
value
of
the
command
line
(
command
+
args
)
"
"
"
        
return
subprocess
.
list2cmdline
(
[
self
.
cmd
]
+
self
.
args
)
    
def
run
(
self
timeout
=
None
outputTimeout
=
None
)
:
        
"
"
"
        
Starts
the
process
.
        
If
timeout
is
not
None
the
process
will
be
allowed
to
continue
for
        
that
number
of
seconds
before
being
killed
.
If
the
process
is
killed
        
due
to
a
timeout
the
onTimeout
handler
will
be
called
.
        
If
outputTimeout
is
not
None
the
process
will
be
allowed
to
continue
        
for
that
number
of
seconds
without
producing
any
output
before
        
being
killed
.
        
"
"
"
        
self
.
didTimeout
=
False
        
self
.
didOutputTimeout
=
False
        
args
=
dict
(
            
stdout
=
subprocess
.
PIPE
            
stderr
=
self
.
_stderr
            
cwd
=
self
.
cwd
            
env
=
self
.
env
            
ignore_children
=
self
.
_ignore_children
        
)
        
args
.
update
(
self
.
keywordargs
)
        
self
.
proc
=
self
.
Process
(
[
self
.
cmd
]
+
self
.
args
*
*
args
)
        
if
isPosix
:
            
self
.
proc
.
pgid
=
self
.
_getpgid
(
self
.
proc
.
pid
)
            
self
.
proc
.
detached_pid
=
None
        
self
.
processOutput
(
timeout
=
timeout
outputTimeout
=
outputTimeout
)
    
def
kill
(
self
sig
=
None
timeout
=
None
)
:
        
"
"
"
        
Kills
the
managed
process
.
        
If
you
created
the
process
with
'
ignore_children
=
False
'
(
the
        
default
)
then
it
will
also
also
kill
all
child
processes
spawned
by
        
it
.
If
you
specified
'
ignore_children
=
True
'
when
creating
the
        
process
only
the
root
process
will
be
killed
.
        
Note
that
this
does
not
manage
any
state
save
any
output
etc
        
it
immediately
kills
the
process
.
        
:
param
sig
:
Signal
used
to
kill
the
process
defaults
to
SIGKILL
                    
(
has
no
effect
on
Windows
)
        
"
"
"
        
if
not
hasattr
(
self
"
proc
"
)
:
            
raise
RuntimeError
(
"
Process
hasn
'
t
been
started
yet
"
)
        
self
.
proc
.
kill
(
sig
=
sig
timeout
=
timeout
)
        
rc
=
self
.
wait
(
0
)
        
if
rc
is
None
:
            
self
.
debug
(
"
kill
:
wait
failed
-
-
process
is
still
alive
"
)
        
return
rc
    
def
poll
(
self
)
:
        
"
"
"
Check
if
child
process
has
terminated
        
Returns
the
current
returncode
value
:
        
-
None
if
the
process
hasn
'
t
terminated
yet
        
-
A
negative
number
if
the
process
was
killed
by
signal
N
(
Unix
only
)
        
-
'
0
'
if
the
process
ended
without
failures
        
"
"
"
        
if
not
hasattr
(
self
"
proc
"
)
:
            
raise
RuntimeError
(
"
Process
hasn
'
t
been
started
yet
"
)
        
elif
not
self
.
_ignore_children
and
self
.
reader
.
is_alive
(
)
:
            
return
None
        
elif
hasattr
(
self
"
returncode
"
)
:
            
return
self
.
returncode
        
else
:
            
return
self
.
proc
.
poll
(
)
    
def
processOutput
(
self
timeout
=
None
outputTimeout
=
None
)
:
        
"
"
"
        
Handle
process
output
until
the
process
terminates
or
times
out
.
        
If
timeout
is
not
None
the
process
will
be
allowed
to
continue
for
        
that
number
of
seconds
before
being
killed
.
        
If
outputTimeout
is
not
None
the
process
will
be
allowed
to
continue
        
for
that
number
of
seconds
without
producing
any
output
before
        
being
killed
.
        
"
"
"
        
if
not
hasattr
(
self
"
proc
"
)
:
            
self
.
run
(
timeout
=
timeout
outputTimeout
=
outputTimeout
)
            
return
        
if
not
self
.
reader
.
is_alive
(
)
:
            
self
.
reader
.
timeout
=
timeout
            
self
.
reader
.
output_timeout
=
outputTimeout
            
self
.
reader
.
start
(
self
.
proc
)
    
def
wait
(
self
timeout
=
None
)
:
        
"
"
"
        
Waits
until
all
output
has
been
read
and
the
process
is
        
terminated
.
        
If
timeout
is
not
None
will
return
after
timeout
seconds
.
        
This
timeout
only
causes
the
wait
function
to
return
and
        
does
not
kill
the
process
.
        
Returns
the
process
exit
code
value
:
        
-
None
if
the
process
hasn
'
t
terminated
yet
        
-
A
negative
number
if
the
process
was
killed
by
signal
N
(
Unix
only
)
        
-
'
0
'
if
the
process
ended
without
failures
        
"
"
"
        
self
.
returncode
=
self
.
proc
.
wait
(
timeout
)
        
if
(
            
self
.
returncode
is
not
None
            
and
self
.
reader
.
thread
            
and
self
.
reader
.
thread
is
not
threading
.
current_thread
(
)
        
)
:
            
if
self
.
_ignore_children
:
                
while
self
.
reader
.
is_still_reading
(
timeout
=
0
.
1
)
:
                    
time
.
sleep
(
0
.
1
)
            
else
:
                
self
.
reader
.
join
(
)
        
return
self
.
returncode
    
property
    
def
pid
(
self
)
:
        
if
not
hasattr
(
self
"
proc
"
)
:
            
raise
RuntimeError
(
"
Process
hasn
'
t
been
started
yet
"
)
        
return
self
.
proc
.
pid
    
staticmethod
    
def
pid_exists
(
pid
)
:
        
if
pid
<
0
:
            
return
False
        
if
isWin
:
            
try
:
                
process
=
winprocess
.
OpenProcess
(
                    
winprocess
.
PROCESS_QUERY_INFORMATION
|
winprocess
.
PROCESS_VM_READ
                    
False
                    
pid
                
)
                
return
winprocess
.
GetExitCodeProcess
(
process
)
=
=
winprocess
.
STILL_ACTIVE
            
except
OSError
as
e
:
                
if
e
.
winerror
=
=
winprocess
.
ERROR_INVALID_PARAMETER
:
                    
return
False
                
if
e
.
winerror
=
=
winprocess
.
ERROR_ACCESS_DENIED
:
                    
return
True
                
raise
        
elif
isPosix
:
            
try
:
                
os
.
kill
(
pid
0
)
            
except
OSError
as
e
:
                
return
e
.
errno
=
=
errno
.
EPERM
            
else
:
                
return
True
    
classmethod
    
def
_getpgid
(
cls
pid
)
:
        
try
:
            
return
os
.
getpgid
(
pid
)
        
except
OSError
as
e
:
            
if
e
.
errno
!
=
errno
.
ESRCH
:
                
raise
    
def
check_for_detached
(
self
new_pid
)
:
        
"
"
"
Check
if
the
current
process
has
been
detached
and
mark
it
appropriately
.
        
In
case
of
application
restarts
the
process
can
spawn
itself
into
a
new
process
group
.
        
From
now
on
the
process
can
no
longer
be
tracked
by
mozprocess
anymore
and
has
to
be
        
marked
as
detached
.
If
the
consumer
of
mozprocess
still
knows
the
new
process
id
it
could
        
check
for
the
detached
state
.
        
new_pid
is
the
new
process
id
of
the
child
process
.
        
"
"
"
        
if
not
hasattr
(
self
"
proc
"
)
:
            
raise
RuntimeError
(
"
Process
hasn
'
t
been
started
yet
"
)
        
if
isPosix
:
            
new_pgid
=
self
.
_getpgid
(
new_pid
)
            
if
new_pgid
and
new_pgid
!
=
self
.
proc
.
pgid
:
                
self
.
proc
.
detached_pid
=
new_pid
                
print
(
                    
'
Child
process
with
id
"
%
s
"
has
been
marked
as
detached
because
it
is
no
'
                    
"
longer
in
the
managed
process
group
.
Keeping
reference
to
the
process
id
"
                    
'
"
%
s
"
which
is
the
new
child
process
.
'
%
(
self
.
pid
new_pid
)
                    
file
=
sys
.
stdout
                
)
class
CallableList
(
list
)
:
    
def
__call__
(
self
*
args
*
*
kwargs
)
:
        
for
e
in
self
:
            
e
(
*
args
*
*
kwargs
)
    
def
__add__
(
self
lst
)
:
        
return
CallableList
(
list
.
__add__
(
self
lst
)
)
class
ProcessReader
:
    
def
__init__
(
        
self
        
stdout_callback
=
None
        
stderr_callback
=
None
        
finished_callback
=
None
        
timeout_callback
=
None
        
timeout
=
None
        
output_timeout
=
None
    
)
:
        
self
.
stdout_callback
=
stdout_callback
or
(
lambda
line
:
True
)
        
self
.
stderr_callback
=
stderr_callback
or
(
lambda
line
:
True
)
        
self
.
finished_callback
=
finished_callback
or
(
lambda
:
True
)
        
self
.
timeout_callback
=
timeout_callback
or
(
lambda
:
True
)
        
self
.
timeout
=
timeout
        
self
.
output_timeout
=
output_timeout
        
self
.
thread
=
None
        
self
.
got_data
=
threading
.
Event
(
)
        
self
.
didOutputTimeout
=
False
    
def
debug
(
self
msg
)
:
        
if
not
MOZPROCESS_DEBUG
:
            
return
        
print
(
f
"
DBG
:
:
MOZPROC
ProcessReader
|
{
msg
}
"
)
    
def
_create_stream_reader
(
self
name
stream
queue
callback
)
:
        
thread
=
threading
.
Thread
(
            
name
=
name
target
=
self
.
_read_stream
args
=
(
stream
queue
callback
)
        
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
        
return
thread
    
def
_read_stream
(
self
stream
queue
callback
)
:
        
sentinel
=
"
"
if
isinstance
(
stream
io
.
TextIOBase
)
else
b
"
"
        
try
:
            
for
line
in
iter
(
stream
.
readline
sentinel
)
:
                
queue
.
put
(
(
line
callback
)
)
        
except
ValueError
as
e
:
            
if
"
I
/
O
operation
on
closed
file
"
in
str
(
e
)
:
                
pass
            
else
:
                
raise
        
queue
.
put
(
(
b
"
"
None
)
)
        
try
:
            
stream
.
close
(
)
        
except
ValueError
:
            
pass
    
def
start
(
self
proc
)
:
        
queue
=
Queue
(
)
        
readers
=
0
        
if
proc
.
stdout
:
            
self
.
_create_stream_reader
(
                
"
ProcessReaderStdout
"
proc
.
stdout
queue
self
.
stdout_callback
            
)
            
readers
+
=
1
        
if
proc
.
stderr
and
proc
.
stderr
!
=
proc
.
stdout
:
            
self
.
_create_stream_reader
(
                
"
ProcessReaderStderr
"
proc
.
stderr
queue
self
.
stderr_callback
            
)
            
readers
+
=
1
        
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
"
ProcessReader
"
            
target
=
self
.
_read
            
args
=
(
queue
readers
)
        
)
        
self
.
thread
.
daemon
=
True
        
self
.
thread
.
start
(
)
        
self
.
debug
(
"
ProcessReader
started
"
)
    
def
_read
(
self
queue
readers
)
:
        
start_time
=
time
.
time
(
)
        
timeout
=
self
.
timeout
        
if
timeout
is
not
None
:
            
timeout
+
=
start_time
        
output_timeout
=
self
.
output_timeout
        
def
get_line
(
)
:
            
queue_timeout
=
None
            
if
timeout
:
                
queue_timeout
=
timeout
-
time
.
time
(
)
            
if
output_timeout
:
                
if
queue_timeout
:
                    
queue_timeout
=
min
(
queue_timeout
output_timeout
)
                
else
:
                    
queue_timeout
=
output_timeout
            
return
queue
.
get
(
timeout
=
queue_timeout
)
        
try
:
            
for
n
in
range
(
readers
)
:
                
for
line
callback
in
iter
(
get_line
(
b
"
"
None
)
)
:
                    
self
.
got_data
.
set
(
)
                    
try
:
                        
callback
(
line
.
rstrip
(
)
)
                    
except
Exception
:
                        
traceback
.
print_exc
(
)
            
try
:
                
self
.
finished_callback
(
)
            
except
Exception
:
                
traceback
.
print_exc
(
)
        
except
Empty
:
            
if
timeout
and
time
.
time
(
)
<
timeout
or
not
timeout
:
                
self
.
didOutputTimeout
=
True
            
try
:
                
self
.
timeout_callback
(
)
            
except
Exception
:
                
traceback
.
print_exc
(
)
        
self
.
debug
(
"
_read
exited
"
)
    
def
is_alive
(
self
)
:
        
if
self
.
thread
:
            
return
self
.
thread
.
is_alive
(
)
        
return
False
    
def
is_still_reading
(
self
timeout
)
:
        
self
.
got_data
.
clear
(
)
        
return
self
.
got_data
.
wait
(
timeout
)
    
def
join
(
self
timeout
=
None
)
:
        
if
self
.
thread
:
            
self
.
thread
.
join
(
timeout
=
timeout
)
class
StoreOutput
:
    
"
"
"
accumulate
stdout
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
output
=
[
]
    
def
__call__
(
self
line
)
:
        
self
.
output
.
append
(
line
)
class
StreamOutput
:
    
"
"
"
pass
output
to
a
stream
and
flush
"
"
"
    
def
__init__
(
self
stream
text
=
True
)
:
        
self
.
stream
=
stream
        
self
.
text
=
text
    
def
__call__
(
self
line
)
:
        
if
self
.
text
:
            
if
isinstance
(
line
bytes
)
:
                
line
=
line
.
decode
(
errors
=
"
ignore
"
)
            
line
+
=
"
\
n
"
        
else
:
            
if
isinstance
(
line
str
)
:
                
line
=
line
.
encode
(
errors
=
"
ignore
"
)
            
line
+
=
b
"
\
n
"
        
try
:
            
self
.
stream
.
write
(
line
)
        
except
TypeError
:
            
print
(
                
"
HEY
!
If
you
'
re
reading
this
you
'
re
about
to
encounter
a
"
                
"
type
error
probably
as
a
result
of
a
conversion
from
"
                
"
Python
2
to
Python
3
.
This
is
almost
definitely
because
"
                
"
you
'
re
trying
to
write
binary
data
to
a
text
-
encoded
"
                
"
stream
or
text
data
to
a
binary
-
encoded
stream
.
Check
how
"
                
"
you
'
re
instantiating
your
ProcessHandler
and
if
the
output
"
                
"
should
be
text
-
encoded
make
sure
you
pass
"
                
"
universal_newlines
=
True
.
"
                
file
=
sys
.
stderr
            
)
            
raise
        
self
.
stream
.
flush
(
)
class
LogOutput
(
StreamOutput
)
:
    
"
"
"
pass
output
to
a
file
"
"
"
    
def
__init__
(
self
filename
)
:
        
self
.
file_obj
=
open
(
filename
"
a
"
)
        
StreamOutput
.
__init__
(
self
self
.
file_obj
True
)
    
def
__del__
(
self
)
:
        
if
self
.
file_obj
is
not
None
:
            
self
.
file_obj
.
close
(
)
class
ProcessHandler
(
ProcessHandlerMixin
)
:
    
"
"
"
    
Convenience
class
for
handling
processes
with
default
output
handlers
.
    
By
default
all
output
is
sent
to
stdout
.
This
can
be
disabled
by
setting
    
the
*
stream
*
argument
to
None
.
    
If
processOutputLine
keyword
argument
is
specified
the
function
or
the
    
list
of
functions
specified
by
this
argument
will
be
called
for
each
line
    
of
output
;
the
output
will
not
be
written
to
stdout
automatically
then
    
if
stream
is
True
(
the
default
)
.
    
If
storeOutput
=
=
True
the
output
produced
by
the
process
will
be
saved
    
as
self
.
output
.
    
If
logfile
is
not
None
the
output
produced
by
the
process
will
be
    
appended
to
the
given
file
.
    
"
"
"
    
def
__init__
(
self
cmd
logfile
=
None
stream
=
True
storeOutput
=
True
*
*
kwargs
)
:
        
kwargs
.
setdefault
(
"
processOutputLine
"
[
]
)
        
if
callable
(
kwargs
[
"
processOutputLine
"
]
)
:
            
kwargs
[
"
processOutputLine
"
]
=
[
kwargs
[
"
processOutputLine
"
]
]
        
if
logfile
:
            
logoutput
=
LogOutput
(
logfile
)
            
kwargs
[
"
processOutputLine
"
]
.
append
(
logoutput
)
        
text
=
kwargs
.
get
(
"
universal_newlines
"
False
)
or
kwargs
.
get
(
"
text
"
False
)
        
if
stream
is
True
:
            
if
text
:
                
stdout
=
codecs
.
getwriter
(
"
utf
-
8
"
)
(
sys
.
stdout
.
buffer
)
            
else
:
                
stdout
=
sys
.
stdout
.
buffer
            
if
not
kwargs
[
"
processOutputLine
"
]
:
                
kwargs
[
"
processOutputLine
"
]
.
append
(
StreamOutput
(
stdout
text
)
)
        
elif
stream
:
            
streamoutput
=
StreamOutput
(
stream
text
)
            
kwargs
[
"
processOutputLine
"
]
.
append
(
streamoutput
)
        
self
.
output
=
None
        
if
storeOutput
:
            
storeoutput
=
StoreOutput
(
)
            
self
.
output
=
storeoutput
.
output
            
kwargs
[
"
processOutputLine
"
]
.
append
(
storeoutput
)
        
ProcessHandlerMixin
.
__init__
(
self
cmd
*
*
kwargs
)
