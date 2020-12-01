from
__future__
import
absolute_import
import
threading
import
mozinfo
if
mozinfo
.
os
=
=
'
linux
'
:
    
from
talos
.
cmanager_linux
import
LinuxCounterManager
\
        
as
DefaultCounterManager
elif
mozinfo
.
os
=
=
'
win
'
:
    
from
talos
.
cmanager_win32
import
WinCounterManager
\
        
as
DefaultCounterManager
else
:
    
from
talos
.
cmanager_mac
import
MacCounterManager
\
        
as
DefaultCounterManager
class
CounterManagement
(
object
)
:
    
def
__init__
(
self
process_name
counters
resolution
)
:
        
"
"
"
        
Public
interface
to
manage
counters
.
        
On
creation
create
a
thread
to
collect
counters
.
Call
:
meth
:
start
        
to
start
collecting
counters
with
that
thread
.
        
Be
sure
to
call
:
meth
:
stop
to
stop
the
thread
.
        
"
"
"
        
assert
counters
        
self
.
_raw_counters
=
counters
        
self
.
_process_name
=
process_name
        
self
.
_counter_results
=
\
            
dict
(
[
(
counter
[
]
)
for
counter
in
self
.
_raw_counters
]
)
        
self
.
_resolution
=
resolution
        
self
.
_stop
=
threading
.
Event
(
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
_collect
)
        
self
.
_process
=
None
    
def
_collect
(
self
)
:
        
manager
=
DefaultCounterManager
(
self
.
_process_name
self
.
_process
                                        
self
.
_raw_counters
)
        
while
not
self
.
_stop
.
wait
(
self
.
_resolution
)
:
            
for
count_type
in
self
.
_raw_counters
:
                
val
=
manager
.
getCounterValue
(
count_type
)
                
if
val
:
                    
self
.
_counter_results
[
count_type
]
.
append
(
val
)
    
def
start
(
self
process
)
:
        
"
"
"
        
start
the
counter
management
thread
.
        
:
param
process
:
a
psutil
.
Process
instance
representing
the
browser
                        
process
.
        
"
"
"
        
self
.
_process
=
process
        
self
.
_thread
.
start
(
)
    
def
stop
(
self
)
:
        
self
.
_stop
.
set
(
)
        
self
.
_thread
.
join
(
)
    
def
results
(
self
)
:
        
assert
not
self
.
_thread
.
is_alive
(
)
        
return
self
.
_counter_results
