from
__future__
import
print_function
unicode_literals
division
import
subprocess
from
datetime
import
datetime
timedelta
from
threading
import
Thread
from
six
.
moves
.
queue
import
Queue
Empty
from
.
progressbar
import
ProgressBar
from
.
results
import
NullTestOutput
TestOutput
escape_cmdline
class
EndMarker
:
    
pass
class
TaskFinishedMarker
:
    
pass
def
_do_work
(
qTasks
qResults
qWatch
prefix
run_skipped
timeout
show_cmd
)
:
    
while
True
:
        
test
=
qTasks
.
get
(
)
        
if
test
is
EndMarker
:
            
qWatch
.
put
(
EndMarker
)
            
qResults
.
put
(
EndMarker
)
            
return
        
if
not
test
.
enable
and
not
run_skipped
:
            
qResults
.
put
(
NullTestOutput
(
test
)
)
            
continue
        
cmd
=
test
.
get_command
(
prefix
)
        
if
show_cmd
:
            
print
(
escape_cmdline
(
cmd
)
)
        
tStart
=
datetime
.
now
(
)
        
proc
=
subprocess
.
Popen
(
            
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
PIPE
            
universal_newlines
=
True
)
        
qWatch
.
put
(
proc
)
        
out
err
=
proc
.
communicate
(
)
        
qWatch
.
put
(
TaskFinishedMarker
)
        
dt
=
datetime
.
now
(
)
-
tStart
        
result
=
TestOutput
(
test
cmd
out
err
proc
.
returncode
dt
.
total_seconds
(
)
                            
dt
>
timedelta
(
seconds
=
timeout
)
)
        
qResults
.
put
(
result
)
def
_do_watch
(
qWatch
timeout
)
:
    
while
True
:
        
proc
=
qWatch
.
get
(
True
)
        
if
proc
=
=
EndMarker
:
            
return
        
try
:
            
fin
=
qWatch
.
get
(
block
=
True
timeout
=
timeout
)
            
assert
fin
is
TaskFinishedMarker
"
invalid
finish
marker
"
        
except
Empty
:
            
try
:
                
proc
.
terminate
(
)
            
except
WindowsError
as
ex
:
                
if
ex
.
winerror
!
=
5
:
                    
raise
            
fin
=
qWatch
.
get
(
)
            
assert
fin
is
TaskFinishedMarker
"
invalid
finish
marker
"
def
run_all_tests
(
tests
prefix
pb
options
)
:
    
"
"
"
    
Uses
scatter
-
gather
to
a
thread
-
pool
to
manage
children
.
    
"
"
"
    
qTasks
qResults
=
Queue
(
)
Queue
(
)
    
workers
=
[
]
    
watchdogs
=
[
]
    
for
_
in
range
(
options
.
worker_count
)
:
        
qWatch
=
Queue
(
)
        
watcher
=
Thread
(
target
=
_do_watch
args
=
(
qWatch
options
.
timeout
)
)
        
watcher
.
setDaemon
(
True
)
        
watcher
.
start
(
)
        
watchdogs
.
append
(
watcher
)
        
worker
=
Thread
(
target
=
_do_work
args
=
(
qTasks
qResults
qWatch
                                               
prefix
options
.
run_skipped
                                               
options
.
timeout
options
.
show_cmd
)
)
        
worker
.
setDaemon
(
True
)
        
worker
.
start
(
)
        
workers
.
append
(
worker
)
    
def
_do_push
(
num_workers
qTasks
)
:
        
for
test
in
tests
:
            
qTasks
.
put
(
test
)
        
for
_
in
range
(
num_workers
)
:
            
qTasks
.
put
(
EndMarker
)
    
pusher
=
Thread
(
target
=
_do_push
args
=
(
len
(
workers
)
qTasks
)
)
    
pusher
.
setDaemon
(
True
)
    
pusher
.
start
(
)
    
ended
=
0
    
delay
=
ProgressBar
.
update_granularity
(
)
.
total_seconds
(
)
    
while
ended
<
len
(
workers
)
:
        
try
:
            
result
=
qResults
.
get
(
block
=
True
timeout
=
delay
)
            
if
result
is
EndMarker
:
                
ended
+
=
1
            
else
:
                
yield
result
        
except
Empty
:
            
pb
.
poke
(
)
    
pusher
.
join
(
)
    
for
worker
in
workers
:
        
worker
.
join
(
)
    
for
watcher
in
watchdogs
:
        
watcher
.
join
(
)
    
assert
qTasks
.
empty
(
)
"
Send
queue
not
drained
"
    
assert
qResults
.
empty
(
)
"
Result
queue
not
drained
"
