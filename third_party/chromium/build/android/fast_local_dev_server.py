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
collections
import
contextlib
import
dataclasses
import
datetime
import
os
import
pathlib
import
re
import
signal
import
shlex
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
import
traceback
import
time
from
typing
import
Callable
Dict
List
Optional
Tuple
IO
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
_SOCKET_TIMEOUT
=
60
_LOGFILE_NAME
=
'
buildserver
.
log
'
_MAX_LOGFILES
=
6
FIRST_LOG_LINE
=
"
"
"
\
#
#
#
#
Start
of
log
for
build
:
{
build_id
}
#
#
#
#
CWD
:
{
outdir
}
"
"
"
BUILD_ID_RE
=
re
.
compile
(
r
'
^
#
#
#
#
Start
of
log
for
build
:
(
?
P
<
build_id
>
.
+
)
'
)
def
server_log
(
msg
:
str
)
:
  
if
OptionsManager
.
is_quiet
(
)
:
    
return
  
print
(
'
\
n
'
+
msg
)
def
print_status
(
prefix
:
str
msg
:
str
)
:
  
if
OptionsManager
.
is_quiet
(
)
:
    
return
  
width
=
shutil
.
get_terminal_size
(
)
.
columns
  
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
'
'
flush
=
True
)
def
_exception_hook
(
exctype
:
type
exc
:
Exception
tb
)
:
  
if
issubclass
(
exctype
KeyboardInterrupt
)
:
    
sys
.
__excepthook__
(
exctype
exc
tb
)
    
return
  
stacktrace
=
'
'
.
join
(
traceback
.
format_exception
(
exctype
exc
tb
)
)
  
stacktrace_lines
=
[
f
'
\
n
{
line
}
'
for
line
in
stacktrace
.
splitlines
(
)
]
  
BuildManager
.
broadcast
(
'
'
.
join
(
stacktrace_lines
)
+
'
\
n
'
)
  
TaskManager
.
deactivate
(
)
  
BuildManager
.
update_remote_titles
(
'
'
)
class
OptionsManager
:
  
_options
=
None
  
classmethod
  
def
set_options
(
cls
options
)
:
    
cls
.
_options
=
options
  
classmethod
  
def
is_quiet
(
cls
)
:
    
assert
cls
.
_options
is
not
None
    
return
cls
.
_options
.
quiet
  
classmethod
  
def
should_remote_print
(
cls
)
:
    
assert
cls
.
_options
is
not
None
    
return
not
cls
.
_options
.
no_remote_print
class
LogfileManager
:
  
_logfiles
:
dict
[
str
IO
[
str
]
]
=
{
}
  
_lock
=
threading
.
RLock
(
)
  
classmethod
  
def
create_logfile
(
cls
build_id
outdir
)
:
    
with
cls
.
_lock
:
      
if
logfile
:
=
cls
.
_logfiles
.
get
(
build_id
None
)
:
        
return
logfile
      
outdir
=
pathlib
.
Path
(
outdir
)
      
latest_logfile
=
outdir
/
f
'
{
_LOGFILE_NAME
}
.
0
'
      
if
latest_logfile
.
exists
(
)
:
        
with
latest_logfile
.
open
(
'
rt
'
)
as
f
:
          
first_line
=
f
.
readline
(
)
          
if
log_build_id
:
=
BUILD_ID_RE
.
search
(
first_line
)
:
            
if
log_build_id
.
group
(
'
build_id
'
)
=
=
build_id
:
              
cls
.
_logfiles
[
build_id
]
=
latest_logfile
.
open
(
'
at
'
)
              
return
cls
.
_logfiles
[
build_id
]
      
filenames
=
os
.
listdir
(
outdir
)
      
logfiles
=
{
f
for
f
in
filenames
if
f
.
startswith
(
_LOGFILE_NAME
)
}
      
for
idx
in
reversed
(
range
(
_MAX_LOGFILES
)
)
:
        
current_name
=
f
'
{
_LOGFILE_NAME
}
.
{
idx
}
'
        
next_name
=
f
'
{
_LOGFILE_NAME
}
.
{
idx
+
1
}
'
        
if
current_name
in
logfiles
:
          
shutil
.
move
(
os
.
path
.
join
(
outdir
current_name
)
                      
os
.
path
.
join
(
outdir
next_name
)
)
      
logfile
=
latest_logfile
.
open
(
'
wt
'
)
      
logfile
.
write
(
FIRST_LOG_LINE
.
format
(
build_id
=
build_id
outdir
=
outdir
)
)
      
logfile
.
flush
(
)
      
cls
.
_logfiles
[
build_id
]
=
logfile
      
return
logfile
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
RLock
(
)
  
classmethod
  
def
no_running_processes
(
cls
)
:
    
with
cls
.
_lock
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
    
with
cls
.
_lock
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
num_pending_tasks
(
cls
)
:
    
with
cls
.
_lock
:
      
return
cls
.
_total_tasks
-
cls
.
_completed_tasks
  
classmethod
  
def
num_completed_tasks
(
cls
)
:
    
with
cls
.
_lock
:
      
return
cls
.
_completed_tasks
  
classmethod
  
def
total_tasks
(
cls
)
:
    
with
cls
.
_lock
:
      
return
cls
.
_total_tasks
  
classmethod
  
def
get_title_message
(
cls
)
:
    
with
cls
.
_lock
:
      
return
f
'
Analysis
Steps
:
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
  
classmethod
  
def
query_build
(
cls
query_build_id
:
str
=
None
)
:
    
builds
=
[
]
    
if
query_build_id
:
      
if
build
:
=
BuildManager
.
get_build
(
query_build_id
)
:
        
builds
.
append
(
build
)
    
else
:
      
builds
=
BuildManager
.
get_all_builds
(
)
    
build_infos
=
[
]
    
for
build
in
builds
:
      
build_infos
.
append
(
build
.
query_build_info
(
)
)
    
return
{
        
'
pid
'
:
os
.
getpid
(
)
        
'
builds
'
:
build_infos
    
}
  
classmethod
  
def
prefix
(
cls
build_id
:
str
=
None
)
:
    
with
cls
.
_lock
:
      
if
build_id
:
        
build
=
BuildManager
.
get_build
(
build_id
)
        
_num_processes
=
build
.
process_count
(
)
        
_completed_tasks
=
build
.
completed_task_count
(
)
        
_total_tasks
=
build
.
total_task_count
(
)
      
else
:
        
_num_processes
=
cls
.
_num_processes
        
_completed_tasks
=
cls
.
_completed_tasks
        
_total_tasks
=
cls
.
_total_tasks
      
word
=
'
process
'
if
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
_num_processes
}
{
word
}
'
              
f
'
{
_completed_tasks
}
/
{
_total_tasks
}
'
)
def
check_pid_alive
(
pid
:
int
)
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
:
    
return
False
  
return
True
dataclasses
.
dataclass
class
Build
:
  
id
:
str
  
pid
:
int
  
env
:
dict
  
stdout
:
IO
[
str
]
  
cwd
:
Optional
[
str
]
=
None
  
_logfile
:
Optional
[
IO
[
str
]
]
=
None
  
_is_ninja_alive
:
bool
=
True
  
_tasks
:
List
[
Task
]
=
dataclasses
.
field
(
default_factory
=
list
)
  
_completed_task_count
=
0
  
_active_process_count
=
0
  
_lock
:
threading
.
RLock
=
dataclasses
.
field
(
default_factory
=
threading
.
RLock
                                             
repr
=
False
                                             
init
=
False
)
  
def
__hash__
(
self
)
:
    
return
hash
(
(
self
.
id
self
.
pid
self
.
cwd
)
)
  
def
add_task
(
self
task
:
Task
)
:
    
self
.
_status_update
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
    
with
self
.
_lock
:
      
self
.
_tasks
.
append
(
task
)
    
TaskStats
.
add_task
(
)
    
TaskManager
.
add_task
(
task
)
  
def
add_process
(
self
task
:
Task
)
:
    
self
.
_status_update
(
f
'
STARTING
{
task
.
name
}
'
)
    
with
self
.
_lock
:
      
self
.
_active_process_count
+
=
1
    
TaskStats
.
add_process
(
)
  
def
task_done
(
self
task
:
Task
status_string
:
str
)
:
    
self
.
_status_update
(
f
'
{
status_string
}
{
task
.
name
}
'
)
    
TaskStats
.
complete_task
(
)
    
TaskManager
.
task_done
(
task
)
    
with
self
.
_lock
:
      
self
.
_completed_task_count
+
=
1
    
BuildManager
.
update_remote_titles
(
)
    
with
self
.
_lock
:
      
if
not
self
.
is_active
(
)
:
        
self
.
_logfile
.
close
(
)
        
BuildManager
.
update_remote_titles
(
'
'
)
  
def
process_complete
(
self
)
:
    
with
self
.
_lock
:
      
self
.
_active_process_count
-
=
1
    
TaskStats
.
remove_process
(
)
  
def
ensure_logfile
(
self
)
:
    
with
self
.
_lock
:
      
if
not
self
.
_logfile
:
        
assert
self
.
cwd
is
not
None
        
self
.
_logfile
=
LogfileManager
.
create_logfile
(
self
.
id
self
.
cwd
)
  
def
log
(
self
message
:
str
)
:
    
with
self
.
_lock
:
      
self
.
ensure_logfile
(
)
      
if
self
.
_logfile
.
closed
:
        
return
      
print
(
message
file
=
self
.
_logfile
flush
=
True
)
  
def
_status_update
(
self
status_message
)
:
    
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
self
.
id
)
}
]
'
    
self
.
log
(
f
'
{
prefix
}
{
status_message
}
'
)
    
print_status
(
prefix
status_message
)
  
def
total_task_count
(
self
)
:
    
with
self
.
_lock
:
      
return
len
(
self
.
_tasks
)
  
def
completed_task_count
(
self
)
:
    
with
self
.
_lock
:
      
return
self
.
_completed_task_count
  
def
pending_task_count
(
self
)
:
    
with
self
.
_lock
:
      
return
self
.
total_task_count
(
)
-
self
.
completed_task_count
(
)
  
def
process_count
(
self
)
:
    
with
self
.
_lock
:
      
return
self
.
_active_process_count
  
def
is_active
(
self
)
:
    
if
self
.
pending_task_count
(
)
>
0
:
      
return
True
    
if
self
.
_is_ninja_alive
:
      
self
.
_is_ninja_alive
=
check_pid_alive
(
self
.
pid
)
    
return
self
.
_is_ninja_alive
  
def
query_build_info
(
self
)
:
    
current_tasks
=
TaskManager
.
get_current_tasks
(
self
.
id
)
    
return
{
        
'
build_id
'
:
self
.
id
        
'
is_active
'
:
self
.
is_active
(
)
        
'
completed_tasks
'
:
self
.
completed_task_count
(
)
        
'
pending_tasks
'
:
self
.
pending_task_count
(
)
        
'
active_tasks
'
:
[
t
.
cmd
for
t
in
current_tasks
]
        
'
outdir
'
:
self
.
cwd
    
}
class
BuildManager
:
  
_builds_by_id
:
dict
[
str
Build
]
=
dict
(
)
  
_cached_ttys
:
dict
[
(
int
int
)
tuple
[
IO
[
str
]
bool
]
]
=
dict
(
)
  
_lock
=
threading
.
RLock
(
)
  
classmethod
  
def
register_builder
(
cls
env
pid
cwd
)
:
    
build_id
=
env
[
'
AUTONINJA_BUILD_ID
'
]
    
stdout
=
cls
.
open_tty
(
env
[
'
AUTONINJA_STDOUT_NAME
'
]
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
cls
.
_lock
:
      
build
=
Build
(
id
=
build_id
                    
pid
=
pid
                    
cwd
=
cwd
                    
env
=
env
                    
stdout
=
stdout
)
      
cls
.
maybe_init_cwd
(
build
cwd
)
      
cls
.
_builds_by_id
[
build_id
]
=
build
    
cls
.
update_remote_titles
(
)
  
classmethod
  
def
maybe_init_cwd
(
cls
build
:
Build
cwd
:
str
)
:
    
if
cwd
is
not
None
:
      
with
cls
.
_lock
:
        
if
build
.
cwd
is
None
:
          
build
.
cwd
=
cwd
        
else
:
          
assert
pathlib
.
Path
(
cwd
)
.
samefile
(
              
build
.
cwd
)
f
'
{
repr
(
cwd
)
}
!
=
{
repr
(
build
.
cwd
)
}
'
        
build
.
ensure_logfile
(
)
  
classmethod
  
def
get_build
(
cls
build_id
)
:
    
with
cls
.
_lock
:
      
return
cls
.
_builds_by_id
.
get
(
build_id
None
)
  
classmethod
  
def
open_tty
(
cls
tty_path
)
:
    
tty
=
open
(
tty_path
'
at
'
)
    
st
=
os
.
stat
(
tty
.
fileno
(
)
)
    
tty_key
=
(
st
.
st_ino
st
.
st_dev
)
    
with
cls
.
_lock
:
      
if
tty_key
not
in
cls
.
_cached_ttys
:
        
cls
.
_cached_ttys
[
tty_key
]
=
(
tty
tty
.
isatty
(
)
)
      
else
:
        
tty
.
close
(
)
      
return
cls
.
_cached_ttys
[
tty_key
]
[
0
]
  
classmethod
  
def
get_active_builds
(
cls
)
-
>
List
[
Build
]
:
    
builds
=
cls
.
get_all_builds
(
)
    
return
list
(
build
for
build
in
builds
if
build
.
is_active
(
)
)
  
classmethod
  
def
get_all_builds
(
cls
)
-
>
List
[
Build
]
:
    
with
cls
.
_lock
:
      
return
list
(
cls
.
_builds_by_id
.
values
(
)
)
  
classmethod
  
def
broadcast
(
cls
msg
:
str
)
:
    
with
cls
.
_lock
:
      
ttys
=
list
(
cls
.
_cached_ttys
.
values
(
)
)
      
builds
=
list
(
cls
.
_builds_by_id
.
values
(
)
)
    
if
OptionsManager
.
should_remote_print
(
)
:
      
for
tty
_unused
in
ttys
:
        
try
:
          
tty
.
write
(
msg
+
'
\
n
'
)
          
tty
.
flush
(
)
        
except
BrokenPipeError
:
          
pass
    
for
build
in
builds
:
      
build
.
log
(
msg
)
    
st
=
os
.
stat
(
sys
.
stderr
.
fileno
(
)
)
    
stderr_key
=
(
st
.
st_ino
st
.
st_dev
)
    
if
stderr_key
not
in
cls
.
_cached_ttys
:
      
print
(
msg
file
=
sys
.
stderr
)
  
classmethod
  
def
update_remote_titles
(
cls
new_title
=
None
)
:
    
if
new_title
is
None
:
      
if
not
cls
.
has_active_builds
(
)
and
TaskStats
.
num_pending_tasks
(
)
=
=
0
:
        
new_title
=
'
'
      
else
:
        
new_title
=
TaskStats
.
get_title_message
(
)
    
with
cls
.
_lock
:
      
ttys
=
list
(
cls
.
_cached_ttys
.
values
(
)
)
    
for
tty
isatty
in
ttys
:
      
if
isatty
:
        
try
:
          
tty
.
write
(
f
'
\
033
]
2
;
{
new_title
}
\
007
'
)
          
tty
.
flush
(
)
        
except
BrokenPipeError
:
          
pass
  
classmethod
  
def
has_active_builds
(
cls
)
:
    
return
bool
(
cls
.
get_active_builds
(
)
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
  
_queue
:
collections
.
deque
[
Task
]
=
collections
.
deque
(
)
  
_current_tasks
:
set
[
Task
]
=
set
(
)
  
_deactivated
=
False
  
_lock
=
threading
.
RLock
(
)
  
classmethod
  
def
add_task
(
cls
task
:
Task
)
:
    
assert
not
cls
.
_deactivated
    
with
cls
.
_lock
:
      
cls
.
_queue
.
appendleft
(
task
)
    
cls
.
_maybe_start_tasks
(
)
  
classmethod
  
def
task_done
(
cls
task
:
Task
)
:
    
with
cls
.
_lock
:
      
cls
.
_current_tasks
.
discard
(
task
)
  
classmethod
  
def
get_current_tasks
(
cls
build_id
)
:
    
with
cls
.
_lock
:
      
return
[
t
for
t
in
cls
.
_current_tasks
if
t
.
build
.
id
=
=
build_id
]
  
classmethod
  
def
deactivate
(
cls
)
:
    
cls
.
_deactivated
=
True
    
tasks_to_terminate
:
list
[
Task
]
=
[
]
    
with
cls
.
_lock
:
      
while
cls
.
_queue
:
        
task
=
cls
.
_queue
.
pop
(
)
        
tasks_to_terminate
.
append
(
task
)
      
tasks_to_terminate
.
extend
(
cls
.
_current_tasks
)
    
for
task
in
tasks_to_terminate
:
      
task
.
terminate
(
)
  
classmethod
  
def
cancel_build
(
cls
build_id
)
:
    
terminated_pending_tasks
:
list
[
Task
]
=
[
]
    
terminated_current_tasks
:
list
[
Task
]
=
[
]
    
with
cls
.
_lock
:
      
for
task
in
cls
.
_queue
:
        
if
task
.
build
.
id
=
=
build_id
:
          
terminated_pending_tasks
.
append
(
task
)
      
for
task
in
terminated_pending_tasks
:
        
cls
.
_queue
.
remove
(
task
)
      
for
task
in
cls
.
_current_tasks
:
        
if
task
.
build
.
id
=
=
build_id
:
          
terminated_current_tasks
.
append
(
task
)
    
for
task
in
terminated_pending_tasks
:
      
task
.
terminate
(
)
    
for
task
in
terminated_current_tasks
:
      
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
  
classmethod
  
def
_maybe_start_tasks
(
cls
)
:
    
if
cls
.
_deactivated
:
      
return
    
cur_load
=
max
(
cls
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
      
with
cls
.
_lock
:
        
try
:
          
next_task
=
cls
.
_queue
.
pop
(
)
          
cls
.
_current_tasks
.
add
(
next_task
)
        
except
IndexError
:
          
return
      
num_started
+
=
next_task
.
start
(
cls
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
build
:
Build
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
build
=
build
    
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
_replaced
=
False
    
self
.
_lock
=
threading
.
RLock
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
_delete_stamp_thread
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
build
.
cwd
self
.
name
)
  
def
__hash__
(
self
)
:
    
return
hash
(
(
self
.
key
self
.
build
.
id
)
)
  
def
__eq__
(
self
other
)
:
    
return
self
.
key
=
=
other
.
key
and
self
.
build
is
other
.
build
  
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
      
self
.
build
.
add_process
(
self
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
build
.
cwd
          
env
=
self
.
build
.
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
replaced
=
False
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
      
self
.
_replaced
=
replaced
    
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
    
self
.
build
.
process_complete
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
    
delete_stamp
=
False
    
status_string
=
'
FINISHED
'
    
if
self
.
_terminated
:
      
status_string
=
'
TERMINATED
'
      
if
not
self
.
_replaced
:
        
delete_stamp
=
True
    
elif
stdout
or
self
.
_return_code
!
=
0
:
      
status_string
=
'
FAILED
'
      
delete_stamp
=
True
      
preamble
=
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
CMD
:
'
+
shlex
.
join
(
self
.
cmd
)
          
'
STDOUT
:
'
      
]
      
message
=
'
\
n
'
.
join
(
preamble
+
[
stdout
]
)
      
self
.
build
.
log
(
message
)
      
server_log
(
message
)
      
if
OptionsManager
.
should_remote_print
(
)
:
        
preamble
=
[
f
'
{
line
}
'
for
line
in
preamble
]
        
remote_message
=
'
\
n
'
.
join
(
preamble
+
[
stdout
]
)
        
self
.
build
.
stdout
.
write
(
f
'
\
n
{
remote_message
}
'
)
        
self
.
build
.
stdout
.
flush
(
)
    
if
delete_stamp
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
build
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
    
self
.
build
.
task_done
(
self
status_string
)
def
_handle_add_task
(
data
current_tasks
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
)
:
  
"
"
"
Handle
messages
of
type
ADD_TASK
.
"
"
"
  
build_id
=
data
[
'
build_id
'
]
  
build
=
BuildManager
.
get_build
(
build_id
)
  
BuildManager
.
maybe_init_cwd
(
build
data
.
get
(
'
cwd
'
)
)
  
new_task
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
                  
cmd
=
data
[
'
cmd
'
]
                  
build
=
build
                  
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
current_tasks
.
get
(
new_task
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
replaced
=
True
)
  
current_tasks
[
new_task
.
key
]
=
new_task
  
build
.
add_task
(
new_task
)
def
_handle_query_build
(
data
connection
:
socket
.
socket
)
:
  
"
"
"
Handle
messages
of
type
QUERY_BUILD
.
"
"
"
  
build_id
=
data
[
'
build_id
'
]
  
response
=
TaskStats
.
query_build
(
build_id
)
  
try
:
    
with
connection
:
      
server_utils
.
SendMessage
(
connection
response
)
  
except
BrokenPipeError
:
    
pass
def
_handle_heartbeat
(
connection
:
socket
.
socket
)
:
  
"
"
"
Handle
messages
of
type
POLL_HEARTBEAT
.
"
"
"
  
try
:
    
with
connection
:
      
server_utils
.
SendMessage
(
connection
{
          
'
status
'
:
'
OK
'
          
'
pid
'
:
os
.
getpid
(
)
      
}
)
  
except
BrokenPipeError
:
    
pass
def
_handle_register_builder
(
data
)
:
  
"
"
"
Handle
messages
of
type
REGISTER_BUILDER
.
"
"
"
  
env
=
data
[
'
env
'
]
  
pid
=
int
(
data
[
'
builder_pid
'
]
)
  
cwd
=
data
[
'
cwd
'
]
  
BuildManager
.
register_builder
(
env
pid
cwd
)
def
_handle_cancel_build
(
data
)
:
  
"
"
"
Handle
messages
of
type
CANCEL_BUILD
.
"
"
"
  
build_id
=
data
[
'
build_id
'
]
  
TaskManager
.
cancel_build
(
build_id
)
  
BuildManager
.
update_remote_titles
(
'
'
)
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
  
"
"
"
Helper
to
encapsulate
getting
a
new
message
.
"
"
"
  
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
    
message
=
server_utils
.
ReceiveMessage
(
conn
)
    
if
message
:
      
yield
message
conn
def
_register_cleanup_signal_handlers
(
)
:
  
original_sigint_handler
=
signal
.
getsignal
(
signal
.
SIGINT
)
  
original_sigterm_handler
=
signal
.
getsignal
(
signal
.
SIGTERM
)
  
def
_cleanup
(
signum
frame
)
:
    
server_log
(
'
STOPPING
SERVER
.
.
.
'
)
    
TaskManager
.
deactivate
(
)
    
server_log
(
'
STOPPED
'
)
    
if
signum
=
=
signal
.
SIGINT
:
      
if
callable
(
original_sigint_handler
)
:
        
original_sigint_handler
(
signum
frame
)
      
else
:
        
raise
KeyboardInterrupt
(
)
    
if
signum
=
=
signal
.
SIGTERM
:
      
if
callable
(
original_sigterm_handler
)
:
        
original_sigterm_handler
(
signum
frame
)
      
else
:
        
sys
.
exit
(
1
)
  
signal
.
signal
(
signal
.
SIGINT
_cleanup
)
  
signal
.
signal
(
signal
.
SIGTERM
_cleanup
)
def
_process_requests
(
sock
:
socket
.
socket
exit_on_idle
:
bool
)
:
  
"
"
"
Main
loop
for
build
server
receiving
request
messages
.
"
"
"
  
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
  
server_log
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
  
_register_cleanup_signal_handlers
(
)
  
while
True
:
    
try
:
      
for
data
connection
in
_listen_for_request_data
(
sock
)
:
        
message_type
=
data
.
get
(
'
message_type
'
server_utils
.
ADD_TASK
)
        
if
message_type
=
=
server_utils
.
POLL_HEARTBEAT
:
          
_handle_heartbeat
(
connection
)
        
elif
message_type
=
=
server_utils
.
ADD_TASK
:
          
connection
.
close
(
)
          
_handle_add_task
(
data
tasks
)
        
elif
message_type
=
=
server_utils
.
QUERY_BUILD
:
          
_handle_query_build
(
data
connection
)
        
elif
message_type
=
=
server_utils
.
REGISTER_BUILDER
:
          
connection
.
close
(
)
          
_handle_register_builder
(
data
)
        
elif
message_type
=
=
server_utils
.
CANCEL_BUILD
:
          
connection
.
close
(
)
          
_handle_cancel_build
(
data
)
        
else
:
          
connection
.
close
(
)
    
except
TimeoutError
:
      
if
(
TaskStats
.
num_pending_tasks
(
)
=
=
0
          
and
not
BuildManager
.
has_active_builds
(
)
and
exit_on_idle
)
:
        
break
    
except
KeyboardInterrupt
:
      
break
  
BuildManager
.
update_remote_titles
(
'
'
)
def
query_build_info
(
build_id
=
None
)
:
  
"
"
"
Communicates
with
the
main
server
to
query
build
info
.
"
"
"
  
return
_send_message_with_response
(
{
      
'
message_type
'
:
server_utils
.
QUERY_BUILD
      
'
build_id
'
:
build_id
  
}
)
def
_wait_for_build
(
build_id
)
:
  
"
"
"
Comunicates
with
the
main
server
waiting
for
a
build
to
complete
.
"
"
"
  
start_time
=
datetime
.
datetime
.
now
(
)
  
while
True
:
    
try
:
      
build_info
=
query_build_info
(
build_id
)
[
'
builds
'
]
[
0
]
    
except
ConnectionRefusedError
:
      
print
(
'
No
server
running
.
It
likely
finished
all
tasks
.
'
)
      
print
(
'
You
can
check
OUTDIR
/
buildserver
.
log
.
0
to
be
sure
.
'
)
      
return
0
    
pending_tasks
=
build_info
[
'
pending_tasks
'
]
    
if
pending_tasks
=
=
0
:
      
print
(
f
'
\
nAll
tasks
completed
for
build_id
:
{
build_id
}
.
'
)
      
return
0
    
current_time
=
datetime
.
datetime
.
now
(
)
    
duration
=
current_time
-
start_time
    
print
(
f
'
\
rWaiting
for
{
pending_tasks
}
tasks
[
{
str
(
duration
)
}
]
\
033
[
K
'
          
end
=
'
'
          
flush
=
True
)
    
time
.
sleep
(
1
)
def
_wait_for_idle
(
)
:
  
"
"
"
Communicates
with
the
main
server
waiting
for
all
builds
to
complete
.
"
"
"
  
start_time
=
datetime
.
datetime
.
now
(
)
  
while
True
:
    
try
:
      
builds
=
query_build_info
(
)
[
'
builds
'
]
    
except
ConnectionRefusedError
:
      
print
(
'
No
server
running
.
It
likely
finished
all
tasks
.
'
)
      
print
(
'
You
can
check
OUTDIR
/
buildserver
.
log
.
0
to
be
sure
.
'
)
      
return
0
    
all_pending_tasks
=
0
    
all_completed_tasks
=
0
    
for
build_info
in
builds
:
      
pending_tasks
=
build_info
[
'
pending_tasks
'
]
      
completed_tasks
=
build_info
[
'
completed_tasks
'
]
      
active
=
build_info
[
'
is_active
'
]
      
if
active
or
pending_tasks
:
        
all_pending_tasks
+
=
pending_tasks
        
all_completed_tasks
+
=
completed_tasks
    
total_tasks
=
all_pending_tasks
+
all_completed_tasks
    
if
all_pending_tasks
=
=
0
:
      
print
(
'
\
nServer
Idle
All
tasks
complete
.
'
)
      
return
0
    
current_time
=
datetime
.
datetime
.
now
(
)
    
duration
=
current_time
-
start_time
    
print
(
        
f
'
\
rWaiting
for
{
all_pending_tasks
}
remaining
tasks
.
'
        
f
'
(
{
all_completed_tasks
}
/
{
total_tasks
}
tasks
complete
)
'
        
f
'
[
{
str
(
duration
)
}
]
\
033
[
K
'
        
end
=
'
'
        
flush
=
True
)
    
time
.
sleep
(
0
.
5
)
def
_check_if_running
(
)
:
  
"
"
"
Communicates
with
the
main
server
to
make
sure
its
running
.
"
"
"
  
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
OSError
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
def
_send_message_and_close
(
message_dict
)
:
  
with
contextlib
.
closing
(
socket
.
socket
(
socket
.
AF_UNIX
)
)
as
sock
:
    
sock
.
connect
(
server_utils
.
SOCKET_ADDRESS
)
    
sock
.
settimeout
(
1
)
    
server_utils
.
SendMessage
(
sock
message_dict
)
def
_send_message_with_response
(
message_dict
)
:
  
with
contextlib
.
closing
(
socket
.
socket
(
socket
.
AF_UNIX
)
)
as
sock
:
    
sock
.
connect
(
server_utils
.
SOCKET_ADDRESS
)
    
sock
.
settimeout
(
1
)
    
server_utils
.
SendMessage
(
sock
message_dict
)
    
return
server_utils
.
ReceiveMessage
(
sock
)
def
_send_cancel_build
(
build_id
)
:
  
_send_message_and_close
(
{
      
'
message_type
'
:
server_utils
.
CANCEL_BUILD
      
'
build_id
'
:
build_id
  
}
)
  
return
0
def
_register_builder
(
build_id
builder_pid
output_directory
)
:
  
if
output_directory
is
not
None
:
    
output_directory
=
str
(
pathlib
.
Path
(
output_directory
)
.
absolute
(
)
)
  
for
_attempt
in
range
(
3
)
:
    
try
:
      
server_utils
.
AssertEnvironmentVariables
(
)
      
_send_message_and_close
(
{
          
'
message_type
'
:
server_utils
.
REGISTER_BUILDER
          
'
env
'
:
dict
(
os
.
environ
)
          
'
builder_pid
'
:
builder_pid
          
'
cwd
'
:
output_directory
      
}
)
      
return
0
    
except
OSError
:
      
time
.
sleep
(
0
.
05
)
  
print
(
f
'
Failed
to
register
builer
for
build_id
=
{
build_id
}
.
'
)
  
return
1
def
poll_server
(
retries
=
3
)
:
  
"
"
"
Communicates
with
the
main
server
to
query
build
info
.
"
"
"
  
for
_attempt
in
range
(
retries
)
:
    
try
:
      
response
=
_send_message_with_response
(
          
{
'
message_type
'
:
server_utils
.
POLL_HEARTBEAT
}
)
      
if
response
:
        
break
    
except
OSError
:
      
time
.
sleep
(
0
.
05
)
  
else
:
    
return
None
  
return
response
[
'
pid
'
]
def
_print_build_status_all
(
)
:
  
try
:
    
query_data
=
query_build_info
(
None
)
  
except
ConnectionRefusedError
:
    
print
(
'
No
server
running
.
Consult
OUTDIR
/
buildserver
.
log
.
0
'
)
    
return
0
  
builds
=
query_data
[
'
builds
'
]
  
pid
=
query_data
[
'
pid
'
]
  
all_active_tasks
=
[
]
  
print
(
f
'
Build
server
(
PID
=
{
pid
}
)
has
{
len
(
builds
)
}
registered
builds
'
)
  
for
build_info
in
builds
:
    
build_id
=
build_info
[
'
build_id
'
]
    
pending_tasks
=
build_info
[
'
pending_tasks
'
]
    
completed_tasks
=
build_info
[
'
completed_tasks
'
]
    
active_tasks
=
build_info
[
'
active_tasks
'
]
    
out_dir
=
build_info
[
'
outdir
'
]
    
active
=
build_info
[
'
is_active
'
]
    
total_tasks
=
pending_tasks
+
completed_tasks
    
all_active_tasks
+
=
active_tasks
    
if
total_tasks
=
=
0
and
not
active
:
      
status
=
'
Finished
without
any
jobs
'
    
else
:
      
if
active
:
        
status
=
'
Siso
still
running
'
      
else
:
        
status
=
'
Siso
finished
'
      
if
out_dir
:
        
status
+
=
f
'
in
{
out_dir
}
'
      
status
+
=
f
'
.
Completed
[
{
completed_tasks
}
/
{
total_tasks
}
]
.
'
      
if
completed_tasks
<
total_tasks
:
        
status
+
=
f
'
{
len
(
active_tasks
)
}
tasks
currently
executing
'
    
print
(
f
'
{
build_id
}
:
{
status
}
'
)
    
if
all_active_tasks
:
      
total
=
len
(
all_active_tasks
)
      
to_show
=
min
(
4
total
)
      
print
(
f
'
Currently
executing
(
showing
{
to_show
}
of
{
total
}
)
:
'
)
      
for
cmd
in
sorted
(
all_active_tasks
)
[
:
to_show
]
:
        
truncated
=
shlex
.
join
(
cmd
)
        
if
len
(
truncated
)
>
200
:
          
truncated
=
truncated
[
:
200
]
+
'
.
.
.
'
        
print
(
truncated
)
  
return
0
def
_print_build_status
(
build_id
)
:
  
server_path
=
os
.
path
.
relpath
(
str
(
server_utils
.
SERVER_SCRIPT
)
)
  
try
:
    
builds
=
query_build_info
(
build_id
)
[
'
builds
'
]
    
if
not
builds
:
      
print
(
f
'
No
build
found
with
id
(
{
build_id
}
)
'
)
      
print
(
'
To
see
the
status
of
all
builds
:
'
            
shlex
.
join
(
[
server_path
'
-
-
print
-
status
-
all
'
]
)
)
      
return
1
    
build_info
=
builds
[
0
]
  
except
ConnectionRefusedError
:
    
print
(
'
No
server
running
.
Consult
OUTDIR
/
buildserver
.
log
.
0
'
)
    
return
0
  
pending_tasks
=
build_info
[
'
pending_tasks
'
]
  
completed_tasks
=
build_info
[
'
completed_tasks
'
]
  
total_tasks
=
pending_tasks
+
completed_tasks
  
if
completed_tasks
:
    
print
(
f
'
Build
Server
Status
:
[
{
completed_tasks
}
/
{
total_tasks
}
]
'
)
    
if
pending_tasks
:
      
print
(
'
To
wait
for
jobs
:
'
shlex
.
join
(
[
server_path
'
-
-
wait
-
for
-
idle
'
]
)
)
  
return
0
def
_wait_for_task_requests
(
exit_on_idle
)
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
    
sock
.
settimeout
(
_SOCKET_TIMEOUT
)
    
try
:
      
sock
.
bind
(
server_utils
.
SOCKET_ADDRESS
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
=
=
98
:
        
if
not
OptionsManager
.
is_quiet
(
)
:
          
pid
=
poll_server
(
)
          
print
(
f
'
Another
instance
is
already
running
(
pid
:
{
pid
}
)
.
'
                
file
=
sys
.
stderr
)
        
return
1
      
raise
    
sock
.
listen
(
)
    
_process_requests
(
sock
exit_on_idle
)
  
return
0
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
  
parser
.
add_argument
(
      
'
-
-
exit
-
on
-
idle
'
      
action
=
'
store_true
'
      
help
=
'
Server
started
on
demand
.
Exit
when
all
tasks
run
out
.
'
)
  
parser
.
add_argument
(
'
-
-
quiet
'
                      
action
=
'
store_true
'
                      
help
=
'
Do
not
output
status
updates
.
'
)
  
parser
.
add_argument
(
'
-
-
no
-
remote
-
print
'
                      
action
=
'
store_true
'
                      
help
=
'
Do
not
output
errors
to
remote
terminals
.
'
)
  
parser
.
add_argument
(
'
-
-
wait
-
for
-
build
'
                      
metavar
=
'
BUILD_ID
'
                      
help
=
'
Wait
for
build
server
to
finish
with
all
tasks
'
                      
'
for
BUILD_ID
and
output
any
pending
messages
.
'
)
  
parser
.
add_argument
(
'
-
-
wait
-
for
-
idle
'
                      
action
=
'
store_true
'
                      
help
=
'
Wait
for
build
server
to
finish
with
all
'
                      
'
pending
tasks
.
'
)
  
parser
.
add_argument
(
'
-
-
print
-
status
'
                      
metavar
=
'
BUILD_ID
'
                      
help
=
'
Print
the
current
state
of
a
build
.
'
)
  
parser
.
add_argument
(
'
-
-
print
-
status
-
all
'
                      
action
=
'
store_true
'
                      
help
=
'
Print
the
current
state
of
all
active
builds
.
'
)
  
parser
.
add_argument
(
      
'
-
-
register
-
build
-
id
'
      
metavar
=
'
BUILD_ID
'
      
help
=
'
Inform
the
build
server
that
a
new
build
has
started
.
'
)
  
parser
.
add_argument
(
'
-
-
output
-
directory
'
                      
help
=
'
Build
directory
(
use
with
-
-
register
-
build
-
id
)
'
)
  
parser
.
add_argument
(
'
-
-
builder
-
pid
'
                      
help
=
'
Builder
process
\
'
s
pid
for
build
BUILD_ID
.
'
)
  
parser
.
add_argument
(
'
-
-
cancel
-
build
'
                      
metavar
=
'
BUILD_ID
'
                      
help
=
'
Cancel
all
pending
and
running
tasks
for
BUILD_ID
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
  
OptionsManager
.
set_options
(
args
)
  
if
args
.
fail_if_not_running
:
    
return
_check_if_running
(
)
  
if
args
.
wait_for_build
:
    
return
_wait_for_build
(
args
.
wait_for_build
)
  
if
args
.
wait_for_idle
:
    
return
_wait_for_idle
(
)
  
if
args
.
print_status
:
    
return
_print_build_status
(
args
.
print_status
)
  
if
args
.
print_status_all
:
    
return
_print_build_status_all
(
)
  
if
args
.
register_build_id
:
    
return
_register_builder
(
args
.
register_build_id
args
.
builder_pid
                             
args
.
output_directory
)
  
if
args
.
cancel_build
:
    
return
_send_cancel_build
(
args
.
cancel_build
)
  
return
_wait_for_task_requests
(
args
.
exit_on_idle
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
excepthook
=
_exception_hook
  
sys
.
exit
(
main
(
)
)
