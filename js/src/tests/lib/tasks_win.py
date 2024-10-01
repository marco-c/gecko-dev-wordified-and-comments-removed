import
subprocess
import
sys
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
Empty
Queue
from
.
adaptor
import
xdr_annotate
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
class
MultiQueue
:
    
def
__init__
(
self
*
queues
)
:
        
self
.
queues
=
queues
        
self
.
output_queue
=
Queue
(
maxsize
=
1
)
        
for
q
in
queues
:
            
thread
=
Thread
(
target
=
self
.
_queue_getter
args
=
(
q
)
daemon
=
True
)
            
thread
.
start
(
)
    
def
_queue_getter
(
self
q
)
:
        
while
True
:
            
item
=
q
.
get
(
)
            
self
.
output_queue
.
put
(
item
)
            
if
item
is
EndMarker
:
                
return
    
def
get
(
self
)
:
        
return
self
.
output_queue
.
get
(
)
def
_do_work
(
    
workerId
    
qTasks
    
qHeavyTasks
    
qResults
    
qWatch
    
prefix
    
tempdir
    
run_skipped
    
timeout
    
show_cmd
)
:
    
q
=
qTasks
    
required_end_markers
=
1
    
if
workerId
=
=
0
:
        
q
=
MultiQueue
(
qTasks
qHeavyTasks
)
        
required_end_markers
=
2
    
num_end_markers
=
0
    
while
True
:
        
test
=
q
.
get
(
)
        
if
test
is
EndMarker
:
            
num_end_markers
+
=
1
            
if
num_end_markers
=
=
required_end_markers
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
            
continue
        
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
tempdir
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
        
system_encoding
=
"
mbcs
"
if
sys
.
platform
=
=
"
win32
"
else
"
utf
-
8
"
        
out
=
out
.
decode
(
system_encoding
)
        
err
=
err
.
decode
(
system_encoding
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
tempdir
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
qHeavyTasks
qResults
=
Queue
(
)
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
i
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
                
i
                
qTasks
                
qHeavyTasks
                
qResults
                
qWatch
                
prefix
                
tempdir
                
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
    
if
options
.
use_xdr
:
        
tests
=
xdr_annotate
(
tests
options
)
        
for
test
in
tests
:
            
if
test
.
selfhosted_xdr_mode
=
=
"
encode
"
:
                
qTasks
.
put
(
test
)
                
yield
qResults
.
get
(
block
=
True
)
                
break
            
assert
not
test
.
enable
and
not
options
.
run_skipped
            
yield
NullTestOutput
(
test
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
            
if
test
.
heavy
:
                
qHeavyTasks
.
put
(
test
)
            
else
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
        
qHeavyTasks
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
qHeavyTasks
.
empty
(
)
"
Send
queue
(
heavy
tasks
)
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
