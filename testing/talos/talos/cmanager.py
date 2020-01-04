import
mozinfo
import
threading
class
CounterManager
(
object
)
:
    
counterDict
=
{
}
    
def
__init__
(
self
)
:
        
self
.
allCounters
=
{
}
        
self
.
registeredCounters
=
{
}
    
def
_loadCounters
(
self
)
:
        
"
"
"
Loads
all
of
the
counters
defined
in
the
counterDict
"
"
"
        
for
counter
in
self
.
counterDict
.
keys
(
)
:
            
self
.
allCounters
[
counter
]
=
self
.
counterDict
[
counter
]
    
def
registerCounters
(
self
counters
)
:
        
"
"
"
Registers
a
list
of
counters
that
will
be
monitoring
.
        
Only
counters
whose
names
are
found
in
allCounters
will
be
added
        
"
"
"
        
for
counter
in
counters
:
            
if
counter
in
self
.
allCounters
:
                
self
.
registeredCounters
[
counter
]
=
\
                    
[
self
.
allCounters
[
counter
]
[
]
]
    
def
getCounterValue
(
self
counterName
)
:
        
"
"
"
Returns
the
last
value
of
the
counter
'
counterName
'
"
"
"
    
def
updatePidList
(
self
)
:
        
"
"
"
Updates
the
list
of
PIDs
we
'
re
interested
in
"
"
"
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
process
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
_process
=
process
        
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
)
:
        
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
