"
"
"
Creates
an
server
to
offload
non
-
critical
-
path
GN
targets
.
"
"
"
from
__future__
import
annotations
import
argparse
import
json
import
os
import
queue
import
shutil
import
socket
import
subprocess
import
sys
import
threading
from
typing
import
Callable
Dict
List
Optional
Tuple
sys
.
path
.
append
(
os
.
path
.
join
(
os
.
path
.
dirname
(
__file__
)
'
gyp
'
)
)
from
util
import
server_utils
def
log
(
msg
:
str
*
end
:
str
=
'
'
)
:
  
width
=
shutil
.
get_terminal_size
(
)
.
columns
  
prefix
=
f
'
[
{
TaskStats
.
prefix
(
)
}
]
'
  
max_msg_width
=
width
-
len
(
prefix
)
  
if
len
(
msg
)
>
max_msg_width
:
    
length_to_show
=
max_msg_width
-
5
    
msg
=
f
'
{
msg
[
:
2
]
}
.
.
.
{
msg
[
-
length_to_show
:
]
}
'
  
print
(
f
'
\
r
{
prefix
}
{
msg
}
\
033
[
K
'
end
=
end
flush
=
True
)
class
TaskStats
:
  
"
"
"
Class
to
keep
track
of
aggregate
stats
for
all
tasks
across
threads
.
"
"
"
  
_num_processes
=
0
  
_completed_tasks
=
0
  
_total_tasks
=
0
  
_lock
=
threading
.
Lock
(
)
  
classmethod
  
def
no_running_processes
(
cls
)
:
    
return
cls
.
_num_processes
=
=
0
  
classmethod
  
def
add_task
(
cls
)
:
    
cls
.
_total_tasks
+
=
1
  
classmethod
  
def
add_process
(
cls
)
:
    
with
cls
.
_lock
:
      
cls
.
_num_processes
+
=
1
  
classmethod
  
def
remove_process
(
cls
)
:
    
with
cls
.
_lock
:
      
cls
.
_num_processes
-
=
1
  
classmethod
  
def
complete_task
(
cls
)
:
    
with
cls
.
_lock
:
      
cls
.
_completed_tasks
+
=
1
  
classmethod
  
def
prefix
(
cls
)
:
    
with
cls
.
_lock
:
      
word
=
'
process
'
if
cls
.
_num_processes
=
=
1
else
'
processes
'
      
return
(
f
'
{
cls
.
_num_processes
}
{
word
}
'
              
f
'
{
cls
.
_completed_tasks
}
/
{
cls
.
_total_tasks
}
'
)
class
TaskManager
:
  
"
"
"
Class
to
encapsulate
a
threadsafe
queue
and
handle
deactivating
it
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
_queue
:
queue
.
SimpleQueue
[
Task
]
=
queue
.
SimpleQueue
(
)
    
self
.
_deactivated
=
False
  
def
add_task
(
self
task
:
Task
)
:
    
assert
not
self
.
_deactivated
    
TaskStats
.
add_task
(
)
    
self
.
_queue
.
put
(
task
)
    
log
(
f
'
QUEUED
{
task
.
name
}
'
)
    
self
.
_maybe_start_tasks
(
)
  
def
deactivate
(
self
)
:
    
self
.
_deactivated
=
True
    
while
not
self
.
_queue
.
empty
(
)
:
      
try
:
        
task
=
self
.
_queue
.
get_nowait
(
)
      
except
queue
.
Empty
:
        
return
      
task
.
terminate
(
)
  
staticmethod
  
def
_num_running_processes
(
)
:
    
with
open
(
'
/
proc
/
stat
'
)
as
f
:
      
for
line
in
f
:
        
if
line
.
startswith
(
'
procs_running
'
)
:
          
return
int
(
line
.
rstrip
(
)
.
split
(
)
[
1
]
)
    
assert
False
'
Could
not
read
/
proc
/
stat
'
  
def
_maybe_start_tasks
(
self
)
:
    
if
self
.
_deactivated
:
      
return
    
cur_load
=
max
(
self
.
_num_running_processes
(
)
os
.
getloadavg
(
)
[
0
]
)
    
num_started
=
0
    
while
num_started
<
2
and
(
TaskStats
.
no_running_processes
(
)
                               
or
num_started
+
cur_load
<
os
.
cpu_count
(
)
)
:
      
try
:
        
next_task
=
self
.
_queue
.
get_nowait
(
)
      
except
queue
.
Empty
:
        
return
      
num_started
+
=
next_task
.
start
(
self
.
_maybe_start_tasks
)
class
Task
:
  
"
"
"
Class
to
represent
one
task
and
operations
on
it
.
"
"
"
  
def
__init__
(
self
name
:
str
cwd
:
str
cmd
:
List
[
str
]
stamp_file
:
str
)
:
    
self
.
name
=
name
    
self
.
cwd
=
cwd
    
self
.
cmd
=
cmd
    
self
.
stamp_file
=
stamp_file
    
self
.
_terminated
=
False
    
self
.
_lock
=
threading
.
Lock
(
)
    
self
.
_proc
:
Optional
[
subprocess
.
Popen
]
=
None
    
self
.
_thread
:
Optional
[
threading
.
Thread
]
=
None
    
self
.
_return_code
:
Optional
[
int
]
=
None
  
property
  
def
key
(
self
)
:
    
return
(
self
.
cwd
self
.
name
)
  
def
start
(
self
on_complete_callback
:
Callable
[
[
]
None
]
)
-
>
int
:
    
"
"
"
Starts
the
task
if
it
has
not
already
been
terminated
.
    
Returns
the
number
of
processes
that
have
been
started
.
This
is
called
at
    
most
once
when
the
task
is
popped
off
the
task
queue
.
"
"
"
    
env
=
os
.
environ
.
copy
(
)
    
env
[
server_utils
.
BUILD_SERVER_ENV_VARIABLE
]
=
'
1
'
    
with
self
.
_lock
:
      
if
self
.
_terminated
:
        
return
0
      
TaskStats
.
add_process
(
)
      
log
(
f
'
STARTING
{
self
.
name
}
'
)
      
self
.
_proc
=
subprocess
.
Popen
(
          
self
.
cmd
          
stdout
=
subprocess
.
PIPE
          
stderr
=
subprocess
.
STDOUT
          
cwd
=
self
.
cwd
          
env
=
env
          
text
=
True
          
preexec_fn
=
lambda
:
os
.
nice
(
19
)
      
)
      
self
.
_thread
=
threading
.
Thread
(
          
target
=
self
.
_complete_when_process_finishes
          
args
=
(
on_complete_callback
)
)
      
self
.
_thread
.
start
(
)
      
return
1
  
def
terminate
(
self
)
:
    
"
"
"
Can
be
called
multiple
times
to
cancel
and
ignore
the
task
'
s
output
.
"
"
"
    
with
self
.
_lock
:
      
if
self
.
_terminated
:
        
return
      
self
.
_terminated
=
True
    
if
self
.
_proc
:
      
self
.
_proc
.
terminate
(
)
      
self
.
_proc
.
wait
(
)
    
if
self
.
_thread
:
      
self
.
_thread
.
join
(
)
    
else
:
      
self
.
_complete
(
)
  
def
_complete_when_process_finishes
(
self
                                      
on_complete_callback
:
Callable
[
[
]
None
]
)
:
    
assert
self
.
_proc
    
stdout
:
str
=
self
.
_proc
.
communicate
(
)
[
0
]
    
self
.
_return_code
=
self
.
_proc
.
returncode
    
TaskStats
.
remove_process
(
)
    
self
.
_complete
(
stdout
)
    
on_complete_callback
(
)
  
def
_complete
(
self
stdout
:
str
=
'
'
)
:
    
"
"
"
Update
the
user
and
ninja
after
the
task
has
run
or
been
terminated
.
    
This
method
should
only
be
run
once
per
task
.
Avoid
modifying
the
task
so
    
that
this
method
does
not
need
locking
.
"
"
"
    
TaskStats
.
complete_task
(
)
    
failed
=
False
    
if
self
.
_terminated
:
      
log
(
f
'
TERMINATED
{
self
.
name
}
'
)
      
failed
=
True
    
else
:
      
log
(
f
'
FINISHED
{
self
.
name
}
'
)
      
if
stdout
or
self
.
_return_code
!
=
0
:
        
failed
=
True
        
print
(
'
\
n
'
+
'
\
n
'
.
join
(
[
            
f
'
FAILED
:
{
self
.
name
}
'
            
f
'
Return
code
:
{
self
.
_return_code
}
'
            
'
'
.
join
(
self
.
cmd
)
            
stdout
        
]
)
)
    
if
failed
:
      
try
:
        
os
.
unlink
(
os
.
path
.
join
(
self
.
cwd
self
.
stamp_file
)
)
      
except
FileNotFoundError
:
        
pass
    
else
:
      
pass
def
_listen_for_request_data
(
sock
:
socket
.
socket
)
:
  
while
True
:
    
conn
=
sock
.
accept
(
)
[
0
]
    
received
=
[
]
    
with
conn
:
      
while
True
:
        
data
=
conn
.
recv
(
4096
)
        
if
not
data
:
          
break
        
received
.
append
(
data
)
    
if
received
:
      
yield
json
.
loads
(
b
'
'
.
join
(
received
)
)
def
_process_requests
(
sock
:
socket
.
socket
)
:
  
tasks
:
Dict
[
Tuple
[
str
str
]
Task
]
=
{
}
  
task_manager
=
TaskManager
(
)
  
try
:
    
log
(
'
READY
.
.
.
Remember
to
set
android_static_analysis
=
"
build_server
"
in
'
        
'
args
.
gn
files
'
)
    
for
data
in
_listen_for_request_data
(
sock
)
:
      
task
=
Task
(
name
=
data
[
'
name
'
]
                  
cwd
=
data
[
'
cwd
'
]
                  
cmd
=
data
[
'
cmd
'
]
                  
stamp_file
=
data
[
'
stamp_file
'
]
)
      
existing_task
=
tasks
.
get
(
task
.
key
)
      
if
existing_task
:
        
existing_task
.
terminate
(
)
      
tasks
[
task
.
key
]
=
task
      
task_manager
.
add_task
(
task
)
  
except
KeyboardInterrupt
:
    
log
(
'
STOPPING
SERVER
.
.
.
'
end
=
'
\
n
'
)
    
task_manager
.
deactivate
(
)
    
for
task
in
tasks
.
values
(
)
:
      
task
.
terminate
(
)
    
log
(
'
STOPPED
'
end
=
'
\
n
'
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
__doc__
)
  
parser
.
add_argument
(
      
'
-
-
fail
-
if
-
not
-
running
'
      
action
=
'
store_true
'
      
help
=
'
Used
by
GN
to
fail
fast
if
the
build
server
is
not
running
.
'
)
  
args
=
parser
.
parse_args
(
)
  
if
args
.
fail_if_not_running
:
    
with
socket
.
socket
(
socket
.
AF_UNIX
)
as
sock
:
      
try
:
        
sock
.
connect
(
server_utils
.
SOCKET_ADDRESS
)
      
except
socket
.
error
:
        
print
(
'
Build
server
is
not
running
and
'
              
'
android_static_analysis
=
"
build_server
"
is
set
.
\
nPlease
run
'
              
'
this
command
in
a
separate
terminal
:
\
n
\
n
'
              
'
build
/
android
/
fast_local_dev_server
.
py
\
n
'
)
        
return
1
      
else
:
        
return
0
  
with
socket
.
socket
(
socket
.
AF_UNIX
)
as
sock
:
    
sock
.
bind
(
server_utils
.
SOCKET_ADDRESS
)
    
sock
.
listen
(
)
    
_process_requests
(
sock
)
if
__name__
=
=
'
__main__
'
:
  
sys
.
exit
(
main
(
)
)
