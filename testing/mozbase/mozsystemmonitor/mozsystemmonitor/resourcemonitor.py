import
multiprocessing
import
os
import
sys
import
time
import
warnings
from
collections
import
OrderedDict
namedtuple
from
contextlib
import
contextmanager
class
PsutilStub
:
    
def
__init__
(
self
)
:
        
self
.
sswap
=
namedtuple
(
            
"
sswap
"
[
"
total
"
"
used
"
"
free
"
"
percent
"
"
sin
"
"
sout
"
]
        
)
        
self
.
sdiskio
=
namedtuple
(
            
"
sdiskio
"
            
[
                
"
read_count
"
                
"
write_count
"
                
"
read_bytes
"
                
"
write_bytes
"
                
"
read_time
"
                
"
write_time
"
            
]
        
)
        
self
.
snetio
=
namedtuple
(
            
"
snetio
"
[
"
bytes_sent
"
"
bytes_recv
"
"
packets_sent
"
"
packets_recv
"
]
        
)
        
self
.
pcputimes
=
namedtuple
(
"
pcputimes
"
[
"
user
"
"
system
"
]
)
        
self
.
svmem
=
namedtuple
(
            
"
svmem
"
            
[
                
"
total
"
                
"
available
"
                
"
percent
"
                
"
used
"
                
"
free
"
                
"
active
"
                
"
inactive
"
                
"
buffers
"
                
"
cached
"
            
]
        
)
    
def
cpu_count
(
self
logical
=
True
)
:
        
return
0
    
def
cpu_percent
(
self
a
b
)
:
        
return
[
0
]
    
def
cpu_times
(
self
percpu
)
:
        
if
percpu
:
            
return
[
self
.
pcputimes
(
0
0
)
]
        
else
:
            
return
self
.
pcputimes
(
0
0
)
    
def
disk_io_counters
(
self
)
:
        
return
self
.
sdiskio
(
0
0
0
0
0
0
)
    
def
net_io_counters
(
self
)
:
        
return
self
.
snetio
(
0
0
0
0
)
    
def
swap_memory
(
self
)
:
        
return
self
.
sswap
(
0
0
0
0
0
0
)
    
def
virtual_memory
(
self
)
:
        
return
self
.
svmem
(
0
0
0
0
0
0
0
0
0
)
try
:
    
import
psutil
    
have_psutil
=
True
except
Exception
:
    
try
:
        
psutil
=
PsutilStub
(
)
    
except
Exception
:
        
psutil
=
None
    
have_psutil
=
False
def
get_disk_io_counters
(
)
:
    
try
:
        
io_counters
=
psutil
.
disk_io_counters
(
)
        
if
io_counters
is
None
:
            
return
PsutilStub
(
)
.
disk_io_counters
(
)
    
except
RuntimeError
:
        
io_counters
=
PsutilStub
(
)
.
disk_io_counters
(
)
    
return
io_counters
def
get_network_io_counters
(
)
:
    
try
:
        
net_counters
=
psutil
.
net_io_counters
(
)
        
if
net_counters
is
None
:
            
return
PsutilStub
(
)
.
net_io_counters
(
)
    
except
(
RuntimeError
AttributeError
)
:
        
net_counters
=
PsutilStub
(
)
.
net_io_counters
(
)
    
return
net_counters
def
_poll
(
pipe
poll_interval
=
0
.
1
)
:
    
"
"
"
Wrap
multiprocessing
.
Pipe
.
poll
to
hide
POLLERR
and
POLLIN
    
exceptions
.
    
multiprocessing
.
Pipe
is
not
actually
a
pipe
on
at
least
Linux
.
    
That
has
an
effect
on
the
expected
outcome
of
reading
from
it
when
    
the
other
end
of
the
pipe
dies
leading
to
possibly
hanging
on
revc
(
)
    
below
.
    
"
"
"
    
try
:
        
return
pipe
.
poll
(
poll_interval
)
    
except
Exception
:
        
return
True
def
_collect
(
pipe
poll_interval
)
:
    
"
"
"
Collects
system
metrics
.
    
This
is
the
main
function
for
the
background
process
.
It
collects
    
data
then
forwards
it
on
a
pipe
until
told
to
stop
.
    
"
"
"
    
data
=
[
]
    
processes
=
[
]
    
sample_processes
=
"
MOZ_PROCESS_SAMPLING
"
in
os
.
environ
    
try
:
        
io_last
=
get_disk_io_counters
(
)
        
net_io_last
=
get_network_io_counters
(
)
        
swap_last
=
psutil
.
swap_memory
(
)
        
psutil
.
cpu_percent
(
None
True
)
        
cpu_last
=
psutil
.
cpu_times
(
True
)
        
last_time
=
time
.
monotonic
(
)
        
sin_index
=
swap_last
.
_fields
.
index
(
"
sin
"
)
        
sout_index
=
swap_last
.
_fields
.
index
(
"
sout
"
)
        
sleep_interval
=
poll_interval
        
known_processes
=
dict
(
)
        
def
update_known_processes
(
)
:
            
nonlocal
known_processes
            
if
not
sample_processes
:
                
return
            
updated_known_processes
=
dict
(
)
            
for
p
in
psutil
.
process_iter
(
)
:
                
pid
=
p
.
pid
                
create_time
=
p
.
create_time
(
)
                
if
pid
in
known_processes
and
create_time
=
=
known_processes
[
pid
]
[
0
]
:
                    
updated_known_processes
[
pid
]
=
known_processes
[
pid
]
                    
del
known_processes
[
pid
]
                
else
:
                    
cmd
=
[
]
                    
try
:
                        
cmd
=
p
.
cmdline
(
)
                    
except
Exception
as
e
:
                        
cmd
=
[
"
exception
"
str
(
e
)
]
                    
ppid
=
0
                    
try
:
                        
ppid
=
p
.
ppid
(
)
                    
except
Exception
:
                        
pass
                    
updated_known_processes
[
pid
]
=
(
create_time
cmd
ppid
)
            
update_time
=
time
.
time
(
)
            
for
pid
(
create_time
cmd
ppid
)
in
known_processes
.
items
(
)
:
                
processes
.
append
(
(
pid
create_time
update_time
cmd
ppid
)
)
            
known_processes
=
updated_known_processes
        
update_known_processes
(
)
        
while
not
_poll
(
pipe
poll_interval
=
sleep_interval
)
:
            
io
=
get_disk_io_counters
(
)
            
net_io
=
get_network_io_counters
(
)
            
virt_mem
=
psutil
.
virtual_memory
(
)
            
swap_mem
=
psutil
.
swap_memory
(
)
            
cpu_percent
=
psutil
.
cpu_percent
(
None
True
)
            
cpu_times
=
psutil
.
cpu_times
(
True
)
            
measured_end_time
=
time
.
monotonic
(
)
            
io_diff
=
[
v
-
io_last
[
i
]
for
i
v
in
enumerate
(
io
)
]
            
io_last
=
io
            
net_io_diff
=
[
                
v
-
net_io_last
[
i
]
for
i
v
in
enumerate
(
net_io
[
:
4
]
)
            
]
            
net_io_last
=
net_io
            
cpu_diff
=
[
]
            
for
core
values
in
enumerate
(
cpu_times
)
:
                
cpu_diff
.
append
(
[
v
-
cpu_last
[
core
]
[
i
]
for
i
v
in
enumerate
(
values
)
]
)
            
cpu_last
=
cpu_times
            
swap_entry
=
list
(
swap_mem
)
            
swap_entry
[
sin_index
]
=
swap_mem
.
sin
-
swap_last
.
sin
            
swap_entry
[
sout_index
]
=
swap_mem
.
sout
-
swap_last
.
sout
            
swap_last
=
swap_mem
            
data
.
append
(
(
                
last_time
                
measured_end_time
                
io_diff
                
net_io_diff
                
cpu_diff
                
cpu_percent
                
list
(
virt_mem
)
                
swap_entry
            
)
)
            
update_known_processes
(
)
            
collection_overhead
=
time
.
monotonic
(
)
-
last_time
-
sleep_interval
            
last_time
=
measured_end_time
            
sleep_interval
=
max
(
poll_interval
/
2
poll_interval
-
collection_overhead
)
    
except
Exception
as
e
:
        
warnings
.
warn
(
"
_collect
failed
:
%
s
"
%
e
)
    
finally
:
        
for
entry
in
data
:
            
pipe
.
send
(
entry
)
        
for
pid
create_time
end_time
cmd
ppid
in
processes
:
            
if
len
(
cmd
)
>
0
:
                
cmd
[
0
]
=
os
.
path
.
basename
(
cmd
[
0
]
)
            
cmdline
=
"
"
.
join
(
[
                
arg
                
for
arg
in
cmd
                
if
not
arg
.
startswith
(
"
-
D
"
)
                
and
not
arg
.
startswith
(
"
-
I
"
)
                
and
not
arg
.
startswith
(
"
-
W
"
)
                
and
not
arg
.
startswith
(
"
-
L
"
)
            
]
)
            
pipe
.
send
(
(
                
"
process
"
                
pid
                
create_time
                
end_time
                
cmdline
                
ppid
                
None
                
None
            
)
)
        
pipe
.
send
(
(
"
done
"
None
None
None
None
None
None
None
)
)
        
pipe
.
close
(
)
    
sys
.
exit
(
0
)
SystemResourceUsage
=
namedtuple
(
    
"
SystemResourceUsage
"
    
[
"
start
"
"
end
"
"
cpu_times
"
"
cpu_percent
"
"
io
"
"
net_io
"
"
virt
"
"
swap
"
]
)
class
SystemResourceMonitor
:
    
"
"
"
Measures
system
resources
.
    
Each
instance
measures
system
resources
from
the
time
it
is
started
    
until
it
is
finished
.
It
does
this
on
a
separate
process
so
it
doesn
'
t
    
impact
execution
of
the
main
Python
process
.
    
Each
instance
is
a
one
-
shot
instance
.
It
cannot
be
used
to
record
multiple
    
durations
.
    
Aside
from
basic
data
gathering
the
class
supports
basic
analysis
    
capabilities
.
You
can
query
for
data
between
ranges
.
You
can
also
tell
it
    
when
certain
events
occur
and
later
grab
data
relevant
to
those
events
or
    
plot
those
events
on
a
timeline
.
    
The
resource
monitor
works
by
periodically
polling
the
state
of
the
    
system
.
By
default
it
polls
every
second
.
This
can
be
adjusted
depending
    
on
the
required
granularity
of
the
data
and
considerations
for
probe
    
overhead
.
It
tries
to
probe
at
the
interval
specified
.
However
variations
    
should
be
expected
.
Fast
and
well
-
behaving
systems
should
experience
    
variations
in
the
1ms
range
.
Larger
variations
may
exist
if
the
system
is
    
under
heavy
load
or
depending
on
how
accurate
socket
polling
is
on
your
    
system
.
    
In
its
current
implementation
data
is
not
available
until
collection
has
    
stopped
.
This
may
change
in
future
iterations
.
    
Usage
    
=
=
=
=
=
    
monitor
=
SystemResourceMonitor
(
)
    
monitor
.
start
(
)
    
#
Record
that
a
single
event
in
time
just
occurred
.
    
foo
.
do_stuff
(
)
    
monitor
.
record_event
(
'
foo_did_stuff
'
)
    
#
Record
that
we
'
re
about
to
perform
a
possibly
long
-
running
event
.
    
with
monitor
.
phase
(
'
long_job
'
)
:
        
foo
.
do_long_running_job
(
)
    
#
Stop
recording
.
Currently
we
need
to
stop
before
data
is
available
.
    
monitor
.
stop
(
)
    
#
Obtain
the
raw
data
for
the
entire
probed
range
.
    
print
(
'
CPU
Usage
:
'
)
    
for
core
in
monitor
.
aggregate_cpu
(
)
:
        
print
(
core
)
    
#
We
can
also
request
data
corresponding
to
a
specific
phase
.
    
for
data
in
monitor
.
phase_usage
(
'
long_job
'
)
:
        
print
(
data
.
cpu_percent
)
    
"
"
"
    
instance
=
None
    
def
__init__
(
self
poll_interval
=
1
.
0
metadata
=
{
}
)
:
        
"
"
"
Instantiate
a
system
resource
monitor
instance
.
        
The
instance
is
configured
with
a
poll
interval
.
This
is
the
interval
        
between
samples
in
float
seconds
.
        
"
"
"
        
self
.
start_time
=
None
        
self
.
end_time
=
None
        
self
.
events
=
[
]
        
self
.
markers
=
[
]
        
self
.
processes
=
[
]
        
self
.
phases
=
OrderedDict
(
)
        
self
.
_active_phases
=
{
}
        
self
.
_active_markers
=
{
}
        
self
.
_running
=
False
        
self
.
_stopped
=
False
        
self
.
_process
=
None
        
if
psutil
is
None
:
            
return
        
try
:
            
cpu_percent
=
psutil
.
cpu_percent
(
0
.
0
True
)
            
cpu_times
=
psutil
.
cpu_times
(
False
)
            
io
=
get_disk_io_counters
(
)
            
net_io
=
get_network_io_counters
(
)
            
virt
=
psutil
.
virtual_memory
(
)
            
swap
=
psutil
.
swap_memory
(
)
        
except
Exception
as
e
:
            
warnings
.
warn
(
"
psutil
failed
to
run
:
%
s
"
%
e
)
            
return
        
self
.
_cpu_cores
=
len
(
cpu_percent
)
        
self
.
_cpu_times_type
=
type
(
cpu_times
)
        
self
.
_cpu_times_len
=
len
(
cpu_times
)
        
self
.
_io_type
=
type
(
io
)
        
self
.
_io_len
=
len
(
io
)
        
self
.
_net_io_type
=
namedtuple
(
"
net_io
"
list
(
net_io
.
_fields
[
:
4
]
)
)
        
self
.
_virt_type
=
type
(
virt
)
        
self
.
_virt_len
=
len
(
virt
)
        
self
.
_swap_type
=
type
(
swap
)
        
self
.
_swap_len
=
len
(
swap
)
        
self
.
start_timestamp
=
time
.
time
(
)
        
self
.
start_time
=
time
.
monotonic
(
)
        
self
.
_pipe
child_pipe
=
multiprocessing
.
Pipe
(
True
)
        
self
.
_process
=
multiprocessing
.
Process
(
            
target
=
_collect
args
=
(
child_pipe
poll_interval
)
        
)
        
self
.
poll_interval
=
poll_interval
        
self
.
metadata
=
metadata
    
def
__del__
(
self
)
:
        
if
self
.
_running
:
            
self
.
_pipe
.
send
(
(
"
terminate
"
)
)
            
self
.
_process
.
join
(
)
    
def
convert_to_monotonic_time
(
self
timestamp
)
:
        
return
timestamp
-
self
.
start_timestamp
+
self
.
start_time
    
def
get_monotonic_time_from_data
(
self
data
)
:
        
"
"
"
Convert
structured
logging
timestamp
to
monotonic
time
.
        
Args
:
            
data
:
Dictionary
with
"
time
"
field
in
milliseconds
        
Returns
:
            
Monotonic
timestamp
        
"
"
"
        
time_sec
=
data
[
"
time
"
]
/
1000
        
return
self
.
convert_to_monotonic_time
(
time_sec
)
    
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
measuring
system
-
wide
CPU
resource
utilization
.
        
You
should
only
call
this
once
per
instance
.
        
"
"
"
        
if
not
self
.
_process
:
            
return
        
self
.
_process
.
start
(
)
        
self
.
_running
=
True
        
self
.
start_time
=
time
.
monotonic
(
)
        
SystemResourceMonitor
.
instance
=
self
    
def
stop
(
self
upload_dir
=
None
)
:
        
"
"
"
Stop
measuring
system
-
wide
CPU
resource
utilization
.
        
You
should
call
this
if
and
only
if
you
have
called
start
(
)
.
You
should
        
always
pair
a
stop
(
)
with
a
start
(
)
.
        
Currently
data
is
not
available
until
you
call
stop
(
)
.
        
Args
:
            
upload_dir
:
Optional
path
to
upload
directory
for
artifact
markers
.
        
"
"
"
        
if
not
self
.
_process
:
            
self
.
_stopped
=
True
            
return
        
self
.
stop_time
=
time
.
monotonic
(
)
        
assert
not
self
.
_stopped
        
try
:
            
self
.
_pipe
.
send
(
(
"
terminate
"
)
)
        
except
Exception
:
            
pass
        
self
.
_stopped
=
True
        
self
.
measurements
=
[
]
        
while
_poll
(
self
.
_pipe
poll_interval
=
0
.
1
)
:
            
try
:
                
(
                    
start_time
                    
end_time
                    
io_diff
                    
net_io_diff
                    
cpu_diff
                    
cpu_percent
                    
virt_mem
                    
swap_mem
                
)
=
self
.
_pipe
.
recv
(
)
            
except
Exception
as
e
:
                
warnings
.
warn
(
"
failed
to
receive
data
:
%
s
"
%
e
)
                
break
            
if
start_time
=
=
"
process
"
:
                
pid
=
end_time
                
start
=
self
.
convert_to_monotonic_time
(
io_diff
)
                
end
=
self
.
convert_to_monotonic_time
(
net_io_diff
)
                
cmd
=
cpu_diff
                
ppid
=
cpu_percent
                
self
.
processes
.
append
(
(
pid
start
end
cmd
ppid
)
)
                
continue
            
if
start_time
=
=
"
done
"
:
                
break
            
try
:
                
io
=
self
.
_io_type
(
*
io_diff
)
                
net_io
=
self
.
_net_io_type
(
*
net_io_diff
)
                
virt
=
self
.
_virt_type
(
*
virt_mem
)
                
swap
=
self
.
_swap_type
(
*
swap_mem
)
                
cpu_times
=
[
self
.
_cpu_times_type
(
*
v
)
for
v
in
cpu_diff
]
                
self
.
measurements
.
append
(
                    
SystemResourceUsage
(
                        
start_time
                        
end_time
                        
cpu_times
                        
cpu_percent
                        
io
                        
net_io
                        
virt
                        
swap
                    
)
                
)
            
except
Exception
:
                
warnings
.
warn
(
                    
"
failed
to
read
the
received
data
:
%
s
"
                    
%
str
(
(
                        
start_time
                        
end_time
                        
io_diff
                        
cpu_diff
                        
cpu_percent
                        
virt_mem
                        
swap_mem
                    
)
)
                
)
                
break
        
if
self
.
_running
:
            
self
.
_process
.
join
(
10
)
            
if
self
.
_process
.
is_alive
(
)
:
                
self
.
_process
.
terminate
(
)
                
self
.
_process
.
join
(
10
)
        
self
.
_running
=
False
        
SystemResourceUsage
.
instance
=
None
        
self
.
end_time
=
time
.
monotonic
(
)
        
if
upload_dir
is
None
:
            
upload_dir
=
os
.
environ
.
get
(
"
UPLOAD_DIR
"
)
or
os
.
environ
.
get
(
                
"
MOZ_UPLOAD_DIR
"
            
)
        
if
upload_dir
and
os
.
path
.
isdir
(
upload_dir
)
:
            
try
:
                
for
filename
in
os
.
listdir
(
upload_dir
)
:
                    
filepath
=
os
.
path
.
join
(
upload_dir
filename
)
                    
if
os
.
path
.
isfile
(
filepath
)
:
                        
stat
=
os
.
stat
(
filepath
)
                        
timestamp
=
self
.
convert_to_monotonic_time
(
stat
.
st_mtime
)
                        
marker_data
=
{
                            
"
type
"
:
"
Artifact
"
                            
"
filename
"
:
filename
                            
"
size
"
:
stat
.
st_size
                        
}
                        
self
.
events
.
append
(
(
timestamp
"
artifact
"
marker_data
)
)
                        
if
filename
=
=
"
sccache
.
log
"
:
                            
self
.
_parse_sccache_log
(
filepath
)
            
except
Exception
as
e
:
                
warnings
.
warn
(
f
"
Failed
to
scan
upload
directory
:
{
e
}
"
)
    
def
_parse_sccache_log
(
self
filepath
)
:
        
"
"
"
Parse
sccache
.
log
and
add
profiler
markers
for
cache
hits
and
misses
.
"
"
"
        
import
re
        
from
datetime
import
datetime
        
parse_start
=
time
.
monotonic
(
)
        
try
:
            
compilations
=
{
}
            
pattern
=
re
.
compile
(
                
r
"
\
[
(
\
d
{
4
}
-
\
d
{
2
}
-
\
d
{
2
}
T
\
d
{
2
}
:
\
d
{
2
}
:
\
d
{
2
}
\
.
\
d
{
3
}
Z
)
.
*
\
]
\
[
(
[
^
\
]
]
+
)
\
]
:
(
.
+
)
(
[
\
d
.
]
+
)
s
(
?
:
|
)
"
            
)
            
with
open
(
filepath
)
as
f
:
                
for
line
in
f
:
                    
match
=
pattern
.
match
(
line
)
                    
if
not
match
:
                        
continue
                    
timestamp_str
=
match
.
group
(
1
)
                    
filename
=
match
.
group
(
2
)
                    
message
=
match
.
group
(
3
)
                    
duration
=
float
(
match
.
group
(
4
)
)
*
1000
                    
dt
=
datetime
.
strptime
(
timestamp_str
"
%
Y
-
%
m
-
%
dT
%
H
:
%
M
:
%
S
.
%
fZ
"
)
                    
timestamp
=
self
.
convert_to_monotonic_time
(
dt
.
timestamp
(
)
)
                    
entry
=
compilations
.
setdefault
(
filename
{
}
)
                    
if
message
=
=
"
generate_hash_key
took
"
:
                        
entry
[
"
hash_time
"
]
=
duration
                        
entry
[
"
start_time
"
]
=
timestamp
-
(
duration
/
1000
)
                    
elif
message
=
=
"
Cache
hit
in
"
:
                        
entry
[
"
lookup_time
"
]
=
duration
                        
entry
[
"
hit
"
]
=
True
                        
entry
[
"
end_time
"
]
=
timestamp
                    
elif
message
=
=
"
Cache
miss
in
"
:
                        
entry
[
"
lookup_time
"
]
=
duration
                        
entry
[
"
hit
"
]
=
False
                    
elif
message
=
=
"
Cache
write
finished
in
"
:
                        
entry
[
"
write_time
"
]
=
duration
                        
entry
[
"
end_time
"
]
=
timestamp
                    
elif
message
=
=
"
Compiled
in
"
:
                        
entry
[
"
compile_time
"
]
=
duration
                    
elif
message
=
=
"
Created
cache
artifact
in
"
:
                        
entry
[
"
artifact_time
"
]
=
duration
            
for
filename
data
in
compilations
.
items
(
)
:
                
if
"
start_time
"
not
in
data
or
"
end_time
"
not
in
data
:
                    
continue
                
marker_data
=
{
                    
"
type
"
:
"
sccache
"
                    
"
file
"
:
filename
                
}
                
if
"
hash_time
"
in
data
:
                    
marker_data
[
"
hash_time
"
]
=
data
[
"
hash_time
"
]
                
if
"
lookup_time
"
in
data
:
                    
marker_data
[
"
lookup_time
"
]
=
data
[
"
lookup_time
"
]
                
if
data
.
get
(
"
hit
"
)
:
                    
marker_data
[
"
status
"
]
=
"
hit
"
                    
marker_data
[
"
color
"
]
=
"
green
"
                
else
:
                    
marker_data
[
"
status
"
]
=
"
miss
"
                    
marker_data
[
"
color
"
]
=
"
yellow
"
                    
if
"
compile_time
"
in
data
:
                        
marker_data
[
"
compile_time
"
]
=
data
[
"
compile_time
"
]
                    
if
"
artifact_time
"
in
data
:
                        
marker_data
[
"
artifact_time
"
]
=
data
[
"
artifact_time
"
]
                    
if
"
write_time
"
in
data
:
                        
marker_data
[
"
write_time
"
]
=
data
[
"
write_time
"
]
                
self
.
markers
.
append
(
(
                    
"
sccache
"
                    
data
[
"
start_time
"
]
                    
data
[
"
end_time
"
]
                    
marker_data
                
)
)
        
except
Exception
as
e
:
            
warnings
.
warn
(
f
"
Failed
to
parse
sccache
.
log
:
{
e
}
"
)
        
else
:
            
parse_end
=
time
.
monotonic
(
)
            
num_markers
=
len
(
compilations
)
            
if
num_markers
>
0
:
                
self
.
markers
.
append
(
(
                    
"
sccache
parsing
"
                    
parse_start
                    
parse_end
                    
{
                        
"
type
"
:
"
Text
"
                        
"
text
"
:
f
"
Parsed
{
num_markers
}
sccache
entries
from
log
"
                    
}
                
)
)
    
staticmethod
    
def
record_event
(
name
timestamp
=
None
data
=
None
)
:
        
"
"
"
Record
an
event
as
occuring
now
.
        
Events
are
actions
that
occur
at
a
specific
point
in
time
.
If
you
are
        
looking
for
an
action
that
has
a
duration
see
the
phase
API
below
.
        
Args
:
            
name
:
Name
of
the
event
(
string
)
            
timestamp
:
Optional
timestamp
(
monotonic
time
)
.
If
not
provided
uses
current
time
.
            
data
:
Optional
marker
payload
dictionary
(
e
.
g
.
{
"
type
"
:
"
TestStatus
"
.
.
.
}
)
        
"
"
"
        
if
SystemResourceMonitor
.
instance
:
            
if
timestamp
is
None
:
                
timestamp
=
time
.
monotonic
(
)
            
if
data
:
                
SystemResourceMonitor
.
instance
.
events
.
append
(
(
timestamp
name
data
)
)
            
else
:
                
SystemResourceMonitor
.
instance
.
events
.
append
(
(
timestamp
name
)
)
    
staticmethod
    
def
record_marker
(
name
start
end
data
)
:
        
"
"
"
Record
a
marker
with
a
duration
and
optional
data
payload
        
Markers
are
typically
used
to
record
when
a
single
command
happened
.
        
For
actions
with
a
longer
duration
that
justifies
tracking
resource
use
        
see
the
phase
API
below
.
        
The
data
parameter
can
be
either
a
dictionary
containing
a
marker
        
payload
(
e
.
g
.
{
"
type
"
:
"
Text
"
"
text
"
:
"
description
"
}
)
or
a
string
.
        
"
"
"
        
if
SystemResourceMonitor
.
instance
:
            
SystemResourceMonitor
.
instance
.
markers
.
append
(
(
name
start
end
data
)
)
    
staticmethod
    
def
begin_marker
(
name
text
disambiguator
=
None
timestamp
=
None
)
:
        
if
SystemResourceMonitor
.
instance
:
            
id
=
name
+
"
:
"
+
text
            
if
disambiguator
:
                
id
+
=
"
:
"
+
disambiguator
            
SystemResourceMonitor
.
instance
.
_active_markers
[
id
]
=
(
                
SystemResourceMonitor
.
instance
.
convert_to_monotonic_time
(
timestamp
)
                
if
timestamp
                
else
time
.
monotonic
(
)
            
)
    
staticmethod
    
def
end_marker
(
name
text
disambiguator
=
None
timestamp
=
None
)
:
        
if
not
SystemResourceMonitor
.
instance
:
            
return
        
end
=
time
.
monotonic
(
)
        
if
timestamp
:
            
end
=
SystemResourceMonitor
.
instance
.
convert_to_monotonic_time
(
timestamp
)
        
id
=
name
+
"
:
"
+
text
        
if
disambiguator
:
            
id
+
=
"
:
"
+
disambiguator
        
if
not
id
in
SystemResourceMonitor
.
instance
.
_active_markers
:
            
return
        
start
=
SystemResourceMonitor
.
instance
.
_active_markers
.
pop
(
id
)
        
data
=
{
"
type
"
:
"
Text
"
"
text
"
:
text
}
        
SystemResourceMonitor
.
instance
.
record_marker
(
name
start
end
data
)
    
staticmethod
    
def
begin_test
(
data
)
:
        
"
"
"
Begin
tracking
a
test
with
enhanced
metadata
support
.
        
Args
:
            
data
:
Dictionary
containing
test
data
(
e
.
g
.
{
"
test
"
:
"
test_name
"
"
time
"
:
timestamp
}
)
        
"
"
"
        
if
SystemResourceMonitor
.
instance
and
"
test
"
in
data
:
            
test_name
=
data
[
"
test
"
]
            
SystemResourceMonitor
.
instance
.
_active_markers
[
test_name
]
=
(
                
SystemResourceMonitor
.
instance
.
get_monotonic_time_from_data
(
data
)
            
)
    
staticmethod
    
def
end_test
(
data
)
:
        
"
"
"
End
tracking
a
test
and
record
it
with
status
and
color
.
        
Args
:
            
data
:
Dictionary
containing
test
data
including
:
                  
-
"
test
"
:
test
name
                  
-
"
status
"
:
test
status
(
"
PASS
"
"
OK
"
"
FAIL
"
"
TIMEOUT
"
"
CRASH
"
etc
.
)
                  
-
"
expected
"
:
the
expected
status
if
it
differs
from
"
status
"
                  
-
"
message
"
:
A
string
describing
the
status
.
        
"
"
"
        
if
not
SystemResourceMonitor
.
instance
or
"
test
"
not
in
data
:
            
return
        
test_name
=
data
[
"
test
"
]
        
if
test_name
not
in
SystemResourceMonitor
.
instance
.
_active_markers
:
            
return
        
start
=
SystemResourceMonitor
.
instance
.
_active_markers
.
pop
(
test_name
)
        
end
=
SystemResourceMonitor
.
instance
.
get_monotonic_time_from_data
(
data
)
        
marker_data
=
{
            
"
type
"
:
"
Test
"
            
"
test
"
:
test_name
            
"
name
"
:
test_name
.
split
(
"
/
"
)
[
-
1
]
        
}
        
extra
=
data
.
get
(
"
extra
"
{
}
)
        
if
extra
and
"
timeoutfactor
"
in
extra
:
            
marker_data
[
"
timeoutfactor
"
]
=
extra
[
"
timeoutfactor
"
]
        
status
=
data
.
get
(
"
status
"
"
"
)
        
if
status
:
            
marker_data
[
"
status
"
]
=
status
            
expected
=
data
.
get
(
"
expected
"
)
            
if
expected
is
not
None
:
                
marker_data
[
"
expected
"
]
=
expected
            
message
=
data
.
get
(
"
message
"
"
"
)
            
will_retry
=
"
will
retry
"
in
message
.
lower
(
)
            
if
status
in
(
"
SKIP
"
"
TIMEOUT
"
)
:
                
marker_data
[
"
color
"
]
=
"
yellow
"
                
if
message
:
                    
marker_data
[
"
message
"
]
=
message
            
elif
status
in
(
"
CRASH
"
"
ERROR
"
)
:
                
marker_data
[
"
color
"
]
=
"
red
"
            
elif
expected
is
None
and
not
will_retry
:
                
marker_data
[
"
color
"
]
=
"
green
"
            
else
:
                
marker_data
[
"
color
"
]
=
"
orange
"
        
SystemResourceMonitor
.
instance
.
record_marker
(
"
test
"
start
end
marker_data
)
    
staticmethod
    
def
test_status
(
data
)
:
        
"
"
"
Record
a
test_status
/
log
/
process_output
event
.
        
Args
:
            
data
:
Dictionary
containing
test_status
/
log
/
process_output
data
including
:
                  
-
"
action
"
:
the
action
type
                  
-
"
test
"
:
test
name
(
optional
)
                  
-
"
subtest
"
:
subtest
name
(
optional
only
for
test_status
/
log
)
                  
-
"
status
"
or
"
level
"
:
status
for
test_status
/
log
                  
-
"
time
"
:
timestamp
in
milliseconds
                  
-
"
message
"
or
"
data
"
:
optional
message
        
"
"
"
        
if
not
SystemResourceMonitor
.
instance
:
            
return
        
timestamp
=
SystemResourceMonitor
.
instance
.
get_monotonic_time_from_data
(
data
)
        
marker_data
=
{
"
type
"
:
"
TestStatus
"
}
        
if
data
.
get
(
"
action
"
)
=
=
"
process_output
"
:
            
marker_name
=
"
output
"
            
message
=
data
.
get
(
"
data
"
)
        
else
:
            
status
=
(
data
.
get
(
"
status
"
)
or
data
.
get
(
"
level
"
)
)
.
upper
(
)
            
marker_name
=
status
            
if
status
=
=
"
PASS
"
:
                
marker_data
[
"
color
"
]
=
"
green
"
            
elif
status
=
=
"
FAIL
"
:
                
marker_data
[
"
color
"
]
=
"
orange
"
            
elif
status
=
=
"
ERROR
"
:
                
marker_data
[
"
color
"
]
=
"
red
"
            
if
subtest
:
=
data
.
get
(
"
subtest
"
)
:
                
marker_data
[
"
subtest
"
]
=
subtest
            
message
=
data
.
get
(
"
message
"
)
        
if
test_name
:
=
data
.
get
(
"
test
"
)
:
            
marker_data
[
"
test
"
]
=
test_name
        
if
message
:
            
marker_data
[
"
message
"
]
=
message
        
if
stack
:
=
data
.
get
(
"
stack
"
)
:
            
marker_data
[
"
stack
"
]
=
stack
        
SystemResourceMonitor
.
record_event
(
marker_name
timestamp
marker_data
)
    
staticmethod
    
def
crash
(
data
)
:
        
"
"
"
Record
a
crash
event
.
        
Args
:
            
data
:
Dictionary
containing
crash
data
including
:
                  
-
"
signature
"
:
crash
signature
                  
-
"
reason
"
:
crash
reason
(
optional
)
                  
-
"
test
"
:
test
name
(
optional
)
                  
-
"
minidump_path
"
:
path
to
minidump
file
(
optional
)
                  
-
"
stack
"
:
structured
stack
(
array
of
frame
dicts
)
(
optional
)
                  
-
"
time
"
:
timestamp
in
milliseconds
        
"
"
"
        
if
not
SystemResourceMonitor
.
instance
:
            
return
        
timestamp
=
SystemResourceMonitor
.
instance
.
get_monotonic_time_from_data
(
data
)
        
marker_data
=
{
            
"
type
"
:
"
Crash
"
            
"
color
"
:
"
red
"
        
}
        
if
signature
:
=
data
.
get
(
"
signature
"
)
:
            
marker_data
[
"
signature
"
]
=
signature
        
if
reason
:
=
data
.
get
(
"
reason
"
)
:
            
marker_data
[
"
reason
"
]
=
reason
        
if
test
:
=
data
.
get
(
"
test
"
)
:
            
marker_data
[
"
test
"
]
=
test
        
if
minidump_path
:
=
data
.
get
(
"
minidump_path
"
)
:
            
minidump_name
=
os
.
path
.
splitext
(
os
.
path
.
basename
(
minidump_path
)
)
[
0
]
            
marker_data
[
"
minidump
"
]
=
minidump_name
        
if
stack
:
=
data
.
get
(
"
crashing_thread_stack
"
)
:
            
marker_data
[
"
stack
"
]
=
stack
        
SystemResourceMonitor
.
record_event
(
"
CRASH
"
timestamp
marker_data
)
    
contextmanager
    
def
phase
(
self
name
)
:
        
"
"
"
Context
manager
for
recording
an
active
phase
.
"
"
"
        
self
.
begin_phase
(
name
)
        
yield
        
self
.
finish_phase
(
name
)
    
def
begin_phase
(
self
name
)
:
        
"
"
"
Record
the
start
of
a
phase
.
        
Phases
are
actions
that
have
a
duration
.
Multiple
phases
can
be
active
        
simultaneously
.
Phases
can
be
closed
in
any
order
.
        
Keep
in
mind
that
if
phases
occur
in
parallel
it
will
become
difficult
        
to
isolate
resource
utilization
specific
to
individual
phases
.
        
"
"
"
        
assert
name
not
in
self
.
_active_phases
        
self
.
_active_phases
[
name
]
=
time
.
monotonic
(
)
    
def
finish_phase
(
self
name
)
:
        
"
"
"
Record
the
end
of
a
phase
.
"
"
"
        
assert
name
in
self
.
_active_phases
        
phase
=
(
self
.
_active_phases
[
name
]
time
.
monotonic
(
)
)
        
self
.
phases
[
name
]
=
phase
        
del
self
.
_active_phases
[
name
]
        
return
phase
[
1
]
-
phase
[
0
]
    
def
range_usage
(
self
start
=
None
end
=
None
)
:
        
"
"
"
Obtain
the
usage
data
falling
within
the
given
time
range
.
        
This
is
a
generator
of
SystemResourceUsage
.
        
If
no
time
range
bounds
are
given
all
data
is
returned
.
        
"
"
"
        
if
not
self
.
_stopped
or
self
.
start_time
is
None
:
            
return
        
if
start
is
None
:
            
start
=
self
.
start_time
        
if
end
is
None
:
            
end
=
self
.
end_time
        
for
entry
in
self
.
measurements
:
            
if
entry
.
start
<
start
:
                
continue
            
if
entry
.
end
>
end
:
                
break
            
yield
entry
    
def
phase_usage
(
self
phase
)
:
        
"
"
"
Obtain
usage
data
for
a
specific
phase
.
        
This
is
a
generator
of
SystemResourceUsage
.
        
"
"
"
        
time_start
time_end
=
self
.
phases
[
phase
]
        
return
self
.
range_usage
(
time_start
time_end
)
    
def
between_events_usage
(
self
start_event
end_event
)
:
        
"
"
"
Obtain
usage
data
between
two
point
events
.
        
This
is
a
generator
of
SystemResourceUsage
.
        
"
"
"
        
start_time
=
None
        
end_time
=
None
        
for
t
name
in
self
.
events
:
            
if
name
=
=
start_event
:
                
start_time
=
t
            
elif
name
=
=
end_event
:
                
end_time
=
t
        
if
start_time
is
None
:
            
raise
Exception
(
"
Could
not
find
start
event
:
%
s
"
%
start_event
)
        
if
end_time
is
None
:
            
raise
Exception
(
"
Could
not
find
end
event
:
%
s
"
%
end_event
)
        
return
self
.
range_usage
(
start_time
end_time
)
    
def
aggregate_cpu_percent
(
self
start
=
None
end
=
None
phase
=
None
per_cpu
=
True
)
:
        
"
"
"
Obtain
the
aggregate
CPU
percent
usage
for
a
range
.
        
Returns
a
list
of
floats
representing
average
CPU
usage
percentage
per
        
core
if
per_cpu
is
True
(
the
default
)
.
If
per_cpu
is
False
return
a
        
single
percentage
value
.
        
By
default
this
will
return
data
for
the
entire
instrumented
interval
.
        
If
phase
is
defined
data
for
a
named
phase
will
be
returned
.
If
start
        
and
end
are
defined
these
times
will
be
fed
into
range_usage
(
)
.
        
"
"
"
        
cpu
=
[
[
]
for
i
in
range
(
0
self
.
_cpu_cores
)
]
        
if
phase
:
            
data
=
self
.
phase_usage
(
phase
)
        
else
:
            
data
=
self
.
range_usage
(
start
end
)
        
for
usage
in
data
:
            
for
i
v
in
enumerate
(
usage
.
cpu_percent
)
:
                
cpu
[
i
]
.
append
(
v
)
        
samples
=
len
(
cpu
[
0
]
)
        
if
not
samples
:
            
return
0
        
if
per_cpu
:
            
return
[
sum
(
x
)
/
samples
for
x
in
cpu
]
        
cores
=
[
sum
(
x
)
for
x
in
cpu
]
        
return
sum
(
cores
)
/
len
(
cpu
)
/
samples
    
def
aggregate_cpu_times
(
self
start
=
None
end
=
None
phase
=
None
per_cpu
=
True
)
:
        
"
"
"
Obtain
the
aggregate
CPU
times
for
a
range
.
        
If
per_cpu
is
True
(
the
default
)
this
returns
a
list
of
named
tuples
.
        
Each
tuple
is
as
if
it
were
returned
by
psutil
.
cpu_times
(
)
.
If
per_cpu
        
is
False
this
returns
a
single
named
tuple
of
the
aforementioned
type
.
        
"
"
"
        
empty
=
[
0
for
i
in
range
(
0
self
.
_cpu_times_len
)
]
        
cpu
=
[
list
(
empty
)
for
i
in
range
(
0
self
.
_cpu_cores
)
]
        
if
phase
:
            
data
=
self
.
phase_usage
(
phase
)
        
else
:
            
data
=
self
.
range_usage
(
start
end
)
        
for
usage
in
data
:
            
for
i
core_values
in
enumerate
(
usage
.
cpu_times
)
:
                
for
j
v
in
enumerate
(
core_values
)
:
                    
cpu
[
i
]
[
j
]
+
=
v
        
if
per_cpu
:
            
return
[
self
.
_cpu_times_type
(
*
v
)
for
v
in
cpu
]
        
sums
=
list
(
empty
)
        
for
core
in
cpu
:
            
for
i
v
in
enumerate
(
core
)
:
                
sums
[
i
]
+
=
v
        
return
self
.
_cpu_times_type
(
*
sums
)
    
def
aggregate_io
(
self
start
=
None
end
=
None
phase
=
None
)
:
        
"
"
"
Obtain
aggregate
I
/
O
counters
for
a
range
.
        
Returns
an
iostat
named
tuple
from
psutil
.
        
"
"
"
        
io
=
[
0
for
i
in
range
(
self
.
_io_len
)
]
        
if
phase
:
            
data
=
self
.
phase_usage
(
phase
)
        
else
:
            
data
=
self
.
range_usage
(
start
end
)
        
for
usage
in
data
:
            
for
i
v
in
enumerate
(
usage
.
io
)
:
                
io
[
i
]
+
=
v
        
return
self
.
_io_type
(
*
io
)
    
def
min_memory_available
(
self
start
=
None
end
=
None
phase
=
None
)
:
        
"
"
"
Return
the
minimum
observed
available
memory
number
from
a
range
.
        
Returns
long
bytes
of
memory
available
.
        
See
psutil
for
notes
on
how
this
is
calculated
.
        
"
"
"
        
if
phase
:
            
data
=
self
.
phase_usage
(
phase
)
        
else
:
            
data
=
self
.
range_usage
(
start
end
)
        
values
=
[
]
        
for
usage
in
data
:
            
values
.
append
(
usage
.
virt
.
available
)
        
return
min
(
values
)
    
def
max_memory_percent
(
self
start
=
None
end
=
None
phase
=
None
)
:
        
"
"
"
Returns
the
maximum
percentage
of
system
memory
used
.
        
Returns
a
float
percentage
.
1
.
00
would
mean
all
system
memory
was
in
        
use
at
one
point
.
        
"
"
"
        
if
phase
:
            
data
=
self
.
phase_usage
(
phase
)
        
else
:
            
data
=
self
.
range_usage
(
start
end
)
        
values
=
[
]
        
for
usage
in
data
:
            
values
.
append
(
usage
.
virt
.
percent
)
        
return
max
(
values
)
    
def
as_profile
(
self
)
:
        
"
"
"
Convert
the
recorded
data
to
an
object
suitable
for
import
into
the
firefox
profiler
"
"
"
        
profile_time
=
time
.
monotonic
(
)
        
start_time
=
self
.
start_time
        
profile
=
{
            
"
meta
"
:
{
                
"
processType
"
:
0
                
"
product
"
:
"
mach
"
                
"
stackwalk
"
:
0
                
"
version
"
:
27
                
"
preprocessedProfileVersion
"
:
47
                
"
symbolicationNotSupported
"
:
True
                
"
interval
"
:
self
.
poll_interval
*
1000
                
"
startTime
"
:
self
.
start_timestamp
*
1000
                
"
profilingStartTime
"
:
0
                
"
logicalCPUs
"
:
psutil
.
cpu_count
(
logical
=
True
)
                
"
physicalCPUs
"
:
psutil
.
cpu_count
(
logical
=
False
)
                
"
mainMemory
"
:
psutil
.
virtual_memory
(
)
[
0
]
                
"
categories
"
:
[
                    
{
                        
"
name
"
:
"
Other
"
                        
"
color
"
:
"
grey
"
                        
"
subcategories
"
:
[
"
Other
"
]
                    
}
                    
{
                        
"
name
"
:
"
Phases
"
                        
"
color
"
:
"
grey
"
                        
"
subcategories
"
:
[
"
Other
"
]
                    
}
                    
{
                        
"
name
"
:
"
Tasks
"
                        
"
color
"
:
"
grey
"
                        
"
subcategories
"
:
[
"
Other
"
]
                    
}
                
]
                
"
markerSchema
"
:
[
                    
{
                        
"
name
"
:
"
Phase
"
                        
"
tooltipLabel
"
:
"
{
marker
.
data
.
phase
}
"
                        
"
tableLabel
"
:
"
{
marker
.
name
}
{
marker
.
data
.
phase
}
CPU
time
:
{
marker
.
data
.
cpuTime
}
(
{
marker
.
data
.
cpuPercent
}
)
"
                        
"
chartLabel
"
:
"
{
marker
.
data
.
phase
}
"
                        
"
display
"
:
[
                            
"
marker
-
chart
"
                            
"
marker
-
table
"
                            
"
timeline
-
overview
"
                        
]
                        
"
data
"
:
[
                            
{
                                
"
key
"
:
"
cpuTime
"
                                
"
label
"
:
"
CPU
Time
"
                                
"
format
"
:
"
duration
"
                            
}
                            
{
                                
"
key
"
:
"
cpuPercent
"
                                
"
label
"
:
"
CPU
Percent
"
                                
"
format
"
:
"
string
"
                            
}
                        
]
                    
}
                    
{
                        
"
name
"
:
"
Text
"
                        
"
tooltipLabel
"
:
"
{
marker
.
name
}
"
                        
"
tableLabel
"
:
"
{
marker
.
name
}
{
marker
.
data
.
text
}
"
                        
"
chartLabel
"
:
"
{
marker
.
data
.
text
}
"
                        
"
display
"
:
[
"
marker
-
chart
"
"
marker
-
table
"
]
                        
"
data
"
:
[
                            
{
                                
"
key
"
:
"
text
"
                                
"
label
"
:
"
Description
"
                                
"
format
"
:
"
string
"
                            
}
                        
]
                    
}
                    
{
                        
"
name
"
:
"
Test
"
                        
"
tooltipLabel
"
:
"
{
marker
.
data
.
name
}
"
                        
"
tableLabel
"
:
"
{
marker
.
data
.
status
}
{
marker
.
data
.
test
}
"
                        
"
chartLabel
"
:
"
{
marker
.
data
.
name
}
"
                        
"
display
"
:
[
"
marker
-
chart
"
"
marker
-
table
"
]
                        
"
colorField
"
:
"
color
"
                        
"
data
"
:
[
                            
{
                                
"
key
"
:
"
test
"
                                
"
label
"
:
"
Test
Name
"
                                
"
format
"
:
"
string
"
                            
}
                            
{
                                
"
key
"
:
"
name
"
                                
"
label
"
:
"
Short
Name
"
                                
"
format
"
:
"
string
"
                                
"
hidden
"
:
True
                            
}
                            
{
                                
"
key
"
:
"
status
"
                                
"
label
"
:
"
Status
"
                                
"
format
"
:
"
string
"
                            
}
                            
{
                                
"
key
"
:
"
expected
"
                                
"
label
"
:
"
Expected
"
                                
"
format
"
:
"
string
"
                            
}
                            
{
                                
"
key
"
:
"
message
"
                                
"
label
"
:
"
Message
"
                                
"
format
"
:
"
string
"
                            
}
                            
{
                                
"
key
"
:
"
timeoutfactor
"
                                
"
label
"
:
"
Timeout
Factor
"
                                
"
format
"
:
"
integer
"
                            
}
                            
{
                                
"
key
"
:
"
color
"
                                
"
hidden
"
:
True
                            
}
                        
]
                    
}
                    
{
                        
"
name
"
:
"
TestStatus
"
                        
"
tableLabel
"
:
"
{
marker
.
data
.
message
}
{
marker
.
data
.
test
}
{
marker
.
data
.
subtest
}
"
                        
"
display
"
:
[
"
marker
-
chart
"
"
marker
-
table
"
]
                        
"
colorField
"
:
"
color
"
                        
"
data
"
:
[
                            
{
                                
"
key
"
:
"
message
"
                                
"
label
"
:
"
Message
"
                                
"
format
"
:
"
string
"
                            
}
                            
{
                                
"
key
"
:
"
test
"
                                
"
label
"
:
"
Test
Name
"
                                
"
format
"
:
"
string
"
                            
}
                            
{
                                
"
key
"
:
"
subtest
"
                                
"
label
"
:
"
Subtest
"
                                
"
format
"
:
"
string
"
                            
}
                            
{
                                
"
key
"
:
"
color
"
                                
"
hidden
"
:
True
                            
}
                        
]
                    
}
                    
{
                        
"
name
"
:
"
Artifact
"
                        
"
tableLabel
"
:
"
{
marker
.
data
.
filename
}
{
marker
.
data
.
size
}
"
                        
"
display
"
:
[
"
marker
-
chart
"
"
marker
-
table
"
]
                        
"
data
"
:
[
                            
{
                                
"
key
"
:
"
filename
"
                                
"
label
"
:
"
Filename
"
                                
"
format
"
:
"
string
"
                            
}
                            
{
                                
"
key
"
:
"
size
"
                                
"
label
"
:
"
Size
"
                                
"
format
"
:
"
bytes
"
                            
}
                        
]
                    
}
                    
{
                        
"
name
"
:
"
Crash
"
                        
"
tableLabel
"
:
"
{
marker
.
data
.
signature
}
{
marker
.
data
.
test
}
"
                        
"
display
"
:
[
"
marker
-
chart
"
"
marker
-
table
"
]
                        
"
colorField
"
:
"
color
"
                        
"
data
"
:
[
                            
{
                                
"
key
"
:
"
signature
"
                                
"
label
"
:
"
Signature
"
                                
"
format
"
:
"
string
"
                            
}
                            
{
                                
"
key
"
:
"
reason
"
                                
"
label
"
:
"
Reason
"
                                
"
format
"
:
"
string
"
                            
}
                            
{
                                
"
key
"
:
"
test
"
                                
"
label
"
:
"
Test
Name
"
                                
"
format
"
:
"
string
"
                            
}
                            
{
                                
"
key
"
:
"
minidump
"
                                
"
label
"
:
"
Minidump
"
                                
"
format
"
:
"
string
"
                            
}
                            
{
                                
"
key
"
:
"
color
"
                                
"
hidden
"
:
True
                            
}
                        
]
                    
}
                    
{
                        
"
name
"
:
"
Mem
"
                        
"
tooltipLabel
"
:
"
{
marker
.
name
}
"
                        
"
display
"
:
[
]
                        
"
data
"
:
[
                            
{
"
key
"
:
"
used
"
"
label
"
:
"
Memory
Used
"
"
format
"
:
"
bytes
"
}
                            
{
                                
"
key
"
:
"
cached
"
                                
"
label
"
:
"
Memory
cached
"
                                
"
format
"
:
"
bytes
"
                            
}
                            
{
                                
"
key
"
:
"
buffers
"
                                
"
label
"
:
"
Memory
buffers
"
                                
"
format
"
:
"
bytes
"
                            
}
                        
]
                        
"
graphs
"
:
[
                            
{
"
key
"
:
"
used
"
"
color
"
:
"
orange
"
"
type
"
:
"
line
-
filled
"
}
                        
]
                    
}
                    
{
                        
"
name
"
:
"
IO
"
                        
"
tooltipLabel
"
:
"
{
marker
.
name
}
"
                        
"
display
"
:
[
]
                        
"
data
"
:
[
                            
{
                                
"
key
"
:
"
write_bytes
"
                                
"
label
"
:
"
Written
"
                                
"
format
"
:
"
bytes
"
                            
}
                            
{
                                
"
key
"
:
"
write_count
"
                                
"
label
"
:
"
Write
count
"
                                
"
format
"
:
"
integer
"
                            
}
                            
{
"
key
"
:
"
read_bytes
"
"
label
"
:
"
Read
"
"
format
"
:
"
bytes
"
}
                            
{
                                
"
key
"
:
"
read_count
"
                                
"
label
"
:
"
Read
count
"
                                
"
format
"
:
"
integer
"
                            
}
                        
]
                        
"
graphs
"
:
[
                            
{
"
key
"
:
"
read_bytes
"
"
color
"
:
"
green
"
"
type
"
:
"
bar
"
}
                            
{
"
key
"
:
"
write_bytes
"
"
color
"
:
"
red
"
"
type
"
:
"
bar
"
}
                        
]
                    
}
                    
{
                        
"
name
"
:
"
NetIO
"
                        
"
tooltipLabel
"
:
"
{
marker
.
name
}
"
                        
"
display
"
:
[
]
                        
"
data
"
:
[
                            
{
                                
"
key
"
:
"
sent_bytes
"
                                
"
label
"
:
"
Sent
"
                                
"
format
"
:
"
bytes
"
                            
}
                            
{
                                
"
key
"
:
"
sent_count
"
                                
"
label
"
:
"
Packets
sent
"
                                
"
format
"
:
"
integer
"
                            
}
                            
{
                                
"
key
"
:
"
recv_bytes
"
                                
"
label
"
:
"
Received
"
                                
"
format
"
:
"
bytes
"
                            
}
                            
{
                                
"
key
"
:
"
recv_count
"
                                
"
label
"
:
"
Packets
received
"
                                
"
format
"
:
"
integer
"
                            
}
                        
]
                        
"
graphs
"
:
[
                            
{
"
key
"
:
"
recv_bytes
"
"
color
"
:
"
blue
"
"
type
"
:
"
bar
"
}
                            
{
"
key
"
:
"
sent_bytes
"
"
color
"
:
"
orange
"
"
type
"
:
"
bar
"
}
                        
]
                    
}
                    
{
                        
"
name
"
:
"
Process
"
                        
"
chartLabel
"
:
"
{
marker
.
data
.
cmd
}
"
                        
"
tooltipLabel
"
:
"
{
marker
.
name
}
"
                        
"
tableLabel
"
:
"
{
marker
.
data
.
cmd
}
"
                        
"
display
"
:
[
"
marker
-
chart
"
"
marker
-
table
"
]
                        
"
data
"
:
[
                            
{
                                
"
key
"
:
"
cmd
"
                                
"
label
"
:
"
Command
line
"
                                
"
format
"
:
"
string
"
                            
}
                            
{
                                
"
key
"
:
"
pid
"
                                
"
label
"
:
"
Process
ID
"
                                
"
format
"
:
"
pid
"
                            
}
                            
{
                                
"
key
"
:
"
ppid
"
                                
"
label
"
:
"
Parent
process
ID
"
                                
"
format
"
:
"
pid
"
                            
}
                        
]
                    
}
                    
{
                        
"
name
"
:
"
Interval
"
                        
"
tooltipLabel
"
:
"
{
marker
.
name
}
"
                        
"
display
"
:
[
]
                        
"
data
"
:
[
                            
{
                                
"
key
"
:
"
interval
"
                                
"
label
"
:
"
Interval
"
                                
"
format
"
:
"
duration
"
                            
}
                        
]
                        
"
graphs
"
:
[
                            
{
"
key
"
:
"
interval
"
"
color
"
:
"
purple
"
"
type
"
:
"
line
"
}
                        
]
                    
}
                    
{
                        
"
name
"
:
"
sccache
"
                        
"
tooltipLabel
"
:
"
{
marker
.
data
.
status
}
:
{
marker
.
data
.
file
}
"
                        
"
tableLabel
"
:
"
{
marker
.
data
.
status
}
:
{
marker
.
data
.
file
}
"
                        
"
chartLabel
"
:
"
{
marker
.
data
.
file
}
"
                        
"
display
"
:
[
"
marker
-
chart
"
"
marker
-
table
"
]
                        
"
colorField
"
:
"
color
"
                        
"
data
"
:
[
                            
{
                                
"
key
"
:
"
file
"
                                
"
label
"
:
"
File
"
                                
"
format
"
:
"
string
"
                            
}
                            
{
                                
"
key
"
:
"
status
"
                                
"
label
"
:
"
Status
"
                                
"
format
"
:
"
string
"
                            
}
                            
{
                                
"
key
"
:
"
hash_time
"
                                
"
label
"
:
"
Hash
Time
"
                                
"
format
"
:
"
duration
"
                            
}
                            
{
                                
"
key
"
:
"
lookup_time
"
                                
"
label
"
:
"
Lookup
Time
"
                                
"
format
"
:
"
duration
"
                            
}
                            
{
                                
"
key
"
:
"
compile_time
"
                                
"
label
"
:
"
Compile
Time
"
                                
"
format
"
:
"
duration
"
                            
}
                            
{
                                
"
key
"
:
"
artifact_time
"
                                
"
label
"
:
"
Artifact
Creation
Time
"
                                
"
format
"
:
"
duration
"
                            
}
                            
{
                                
"
key
"
:
"
write_time
"
                                
"
label
"
:
"
Cache
Write
Time
"
                                
"
format
"
:
"
duration
"
                            
}
                            
{
                                
"
key
"
:
"
color
"
                                
"
hidden
"
:
True
                            
}
                        
]
                    
}
                
]
                
"
usesOnlyOneStackType
"
:
True
            
}
            
"
libs
"
:
[
]
            
"
threads
"
:
[
                
{
                    
"
processType
"
:
"
default
"
                    
"
processName
"
:
"
mach
"
                    
"
processStartupTime
"
:
0
                    
"
processShutdownTime
"
:
None
                    
"
registerTime
"
:
0
                    
"
unregisterTime
"
:
None
                    
"
pausedRanges
"
:
[
]
                    
"
showMarkersInTimeline
"
:
True
                    
"
name
"
:
"
"
                    
"
isMainThread
"
:
False
                    
"
pid
"
:
"
0
"
                    
"
tid
"
:
0
                    
"
samples
"
:
{
                        
"
weightType
"
:
"
samples
"
                        
"
weight
"
:
None
                        
"
stack
"
:
[
]
                        
"
time
"
:
[
]
                        
"
length
"
:
0
                    
}
                    
"
stringArray
"
:
[
"
(
root
)
"
]
                    
"
markers
"
:
{
                        
"
data
"
:
[
]
                        
"
name
"
:
[
]
                        
"
startTime
"
:
[
]
                        
"
endTime
"
:
[
]
                        
"
phase
"
:
[
]
                        
"
category
"
:
[
]
                        
"
stack
"
:
[
]
                        
"
length
"
:
0
                    
}
                    
"
stackTable
"
:
{
                        
"
frame
"
:
[
0
]
                        
"
prefix
"
:
[
None
]
                        
"
category
"
:
[
0
]
                        
"
subcategory
"
:
[
0
]
                        
"
length
"
:
1
                    
}
                    
"
frameTable
"
:
{
                        
"
address
"
:
[
-
1
]
                        
"
inlineDepth
"
:
[
0
]
                        
"
category
"
:
[
None
]
                        
"
subcategory
"
:
[
0
]
                        
"
func
"
:
[
0
]
                        
"
nativeSymbol
"
:
[
None
]
                        
"
innerWindowID
"
:
[
0
]
                        
"
implementation
"
:
[
None
]
                        
"
line
"
:
[
None
]
                        
"
column
"
:
[
None
]
                        
"
length
"
:
1
                    
}
                    
"
funcTable
"
:
{
                        
"
isJS
"
:
[
False
]
                        
"
relevantForJS
"
:
[
False
]
                        
"
name
"
:
[
0
]
                        
"
resource
"
:
[
-
1
]
                        
"
fileName
"
:
[
None
]
                        
"
lineNumber
"
:
[
None
]
                        
"
columnNumber
"
:
[
None
]
                        
"
length
"
:
1
                    
}
                    
"
resourceTable
"
:
{
                        
"
lib
"
:
[
]
                        
"
name
"
:
[
]
                        
"
host
"
:
[
]
                        
"
type
"
:
[
]
                        
"
length
"
:
0
                    
}
                    
"
nativeSymbols
"
:
{
                        
"
libIndex
"
:
[
]
                        
"
address
"
:
[
]
                        
"
name
"
:
[
]
                        
"
functionSize
"
:
[
]
                        
"
length
"
:
0
                    
}
                
}
            
]
            
"
counters
"
:
[
]
        
}
        
OTHER_CATEGORY
=
0
        
PHASE_CATEGORY
=
1
        
TASK_CATEGORY
=
2
        
firstThread
=
profile
[
"
threads
"
]
[
0
]
        
markers
=
firstThread
[
"
markers
"
]
        
for
key
in
self
.
metadata
:
            
profile
[
"
meta
"
]
[
key
]
=
self
.
metadata
[
key
]
        
def
get_string_index
(
string
)
:
            
stringArray
=
firstThread
[
"
stringArray
"
]
            
try
:
                
return
stringArray
.
index
(
string
)
            
except
ValueError
:
                
stringArray
.
append
(
string
)
                
return
len
(
stringArray
)
-
1
        
def
parse_stack
(
stack_string
)
:
            
"
"
"
Parse
a
JavaScript
stack
trace
into
structured
format
.
            
Supports
two
formats
:
            
1
.
JavaScript
Error
.
stack
format
:
"
func
file
:
line
:
col
\
nfunc
file
:
line
:
col
\
n
.
.
.
"
            
2
.
Normalized
nsIStackFrame
format
:
"
file
:
func
:
line
\
nfile
:
func
:
line
\
n
.
.
.
"
            
Returns
an
array
of
frame
dicts
.
            
"
"
"
            
if
not
stack_string
:
                
return
None
            
frames
=
[
]
            
for
line
in
stack_string
.
strip
(
)
.
split
(
"
\
n
"
)
:
                
if
not
line
:
                    
continue
                
file_name
=
None
                
func_part
=
None
                
line_num
=
None
                
col_num
=
None
                
if
"
"
in
line
:
                    
func_part
location
=
line
.
rsplit
(
"
"
1
)
                    
func_part
=
func_part
.
strip
(
)
                    
parts
=
location
.
rsplit
(
"
:
"
2
)
                    
if
len
(
parts
)
=
=
3
:
                        
file_name
line_str
col_str
=
parts
                        
try
:
                            
line_num
=
int
(
line_str
)
                            
col_num
=
int
(
col_str
)
                        
except
ValueError
:
                            
pass
                    
elif
len
(
parts
)
=
=
2
:
                        
file_name
line_str
=
parts
                        
try
:
                            
line_num
=
int
(
line_str
)
                        
except
ValueError
:
                            
pass
                    
else
:
                        
file_name
=
location
                
else
:
                    
parts
=
line
.
rsplit
(
"
:
"
2
)
                    
if
len
(
parts
)
=
=
3
:
                        
file_name
func_part
line_str
=
parts
                        
try
:
                            
line_num
=
int
(
line_str
)
                        
except
ValueError
:
                            
func_part
=
line
.
strip
(
)
                            
file_name
=
None
                    
else
:
                        
func_part
=
line
.
strip
(
)
                
frame_dict
=
{
"
is_js
"
:
True
}
                
if
func_part
:
                    
frame_dict
[
"
function
"
]
=
func_part
                
if
file_name
:
                    
frame_dict
[
"
file
"
]
=
file_name
                
if
line_num
is
not
None
:
                    
frame_dict
[
"
line
"
]
=
line_num
                
if
col_num
is
not
None
:
                    
frame_dict
[
"
column
"
]
=
col_num
                
frames
.
append
(
frame_dict
)
            
return
frames
        
def
get_stack_index
(
stack_frames
)
:
            
"
"
"
Get
a
stack
index
from
a
structured
stack
(
array
of
frame
dicts
)
.
            
Each
frame
dict
contains
:
            
-
function
:
function
name
(
optional
)
            
-
module
:
module
/
library
name
(
optional
)
            
-
file
:
source
file
path
(
optional
)
            
-
line
:
line
number
(
optional
)
            
-
column
:
column
number
(
optional
)
            
-
offset
:
hex
offset
for
unsymbolicated
frames
(
optional
)
            
-
inlined
:
boolean
indicating
if
this
is
an
inlined
frame
(
optional
)
            
-
is_js
:
boolean
indicating
if
this
is
a
JavaScript
frame
(
optional
)
            
Returns
the
index
of
the
innermost
stack
frame
or
None
if
stack_frames
is
empty
.
            
"
"
"
            
if
not
stack_frames
:
                
return
None
            
stackTable
=
firstThread
[
"
stackTable
"
]
            
frameTable
=
firstThread
[
"
frameTable
"
]
            
funcTable
=
firstThread
[
"
funcTable
"
]
            
resourceTable
=
firstThread
[
"
resourceTable
"
]
            
nativeSymbols
=
firstThread
[
"
nativeSymbols
"
]
            
stack_index
=
None
            
inline_depth
=
0
            
for
frame_data
in
reversed
(
stack_frames
)
:
                
if
frame_data
.
get
(
"
inlined
"
)
:
                    
inline_depth
+
=
1
                
else
:
                    
inline_depth
=
0
                
module_name
=
frame_data
.
get
(
"
module
"
)
                
file_name
=
frame_data
.
get
(
"
file
"
)
                
line_num
=
frame_data
.
get
(
"
line
"
)
                
col_num
=
frame_data
.
get
(
"
column
"
)
                
is_js
=
frame_data
.
get
(
"
is_js
"
False
)
                
module_offset
=
frame_data
.
get
(
"
module_offset
"
)
                
function_offset
=
frame_data
.
get
(
"
function_offset
"
)
                
raw_offset
=
frame_data
.
get
(
"
offset
"
)
                
func_name
=
frame_data
.
get
(
"
function
"
)
                
if
not
func_name
and
(
offset
:
=
module_offset
or
raw_offset
)
:
                    
func_name
=
hex
(
offset
)
                
resource_index
=
-
1
                
resource_name
=
module_name
or
(
file_name
if
is_js
else
None
)
                
if
resource_name
:
                    
for
i
name_idx
in
enumerate
(
resourceTable
[
"
name
"
]
)
:
                        
if
firstThread
[
"
stringArray
"
]
[
name_idx
]
=
=
resource_name
:
                            
resource_index
=
i
                            
break
                    
else
:
                        
resource_index
=
resourceTable
[
"
length
"
]
                        
resourceTable
[
"
lib
"
]
.
append
(
None
)
                        
resourceTable
[
"
name
"
]
.
append
(
get_string_index
(
resource_name
)
)
                        
resourceTable
[
"
host
"
]
.
append
(
None
)
                        
resource_type
=
1
if
module_name
else
(
5
if
is_js
else
0
)
                        
resourceTable
[
"
type
"
]
.
append
(
resource_type
)
                        
resourceTable
[
"
length
"
]
+
=
1
                
native_symbol_index
=
None
                
if
(
                    
module_offset
is
not
None
                    
and
function_offset
is
not
None
                    
and
module_name
                
)
:
                    
symbol_address
=
module_offset
-
function_offset
                    
for
i
in
range
(
nativeSymbols
[
"
length
"
]
)
:
                        
if
(
                            
nativeSymbols
[
"
libIndex
"
]
[
i
]
=
=
resource_index
                            
and
nativeSymbols
[
"
address
"
]
[
i
]
=
=
symbol_address
                        
)
:
                            
native_symbol_index
=
i
                            
break
                    
else
:
                        
native_symbol_index
=
nativeSymbols
[
"
length
"
]
                        
nativeSymbols
[
"
libIndex
"
]
.
append
(
resource_index
)
                        
nativeSymbols
[
"
address
"
]
.
append
(
symbol_address
)
                        
nativeSymbols
[
"
name
"
]
.
append
(
get_string_index
(
func_name
)
)
                        
nativeSymbols
[
"
functionSize
"
]
.
append
(
None
)
                        
nativeSymbols
[
"
length
"
]
+
=
1
                
func_name_index
=
get_string_index
(
func_name
)
                
file_name_index
=
get_string_index
(
file_name
)
if
file_name
else
None
                
for
i
name_idx
in
enumerate
(
funcTable
[
"
name
"
]
)
:
                    
if
(
                        
name_idx
=
=
func_name_index
                        
and
funcTable
[
"
resource
"
]
[
i
]
=
=
resource_index
                        
and
funcTable
[
"
fileName
"
]
[
i
]
=
=
file_name_index
                        
and
funcTable
[
"
lineNumber
"
]
[
i
]
=
=
line_num
                    
)
:
                        
func_index
=
i
                        
break
                
else
:
                    
func_index
=
funcTable
[
"
length
"
]
                    
funcTable
[
"
isJS
"
]
.
append
(
is_js
)
                    
funcTable
[
"
relevantForJS
"
]
.
append
(
is_js
)
                    
funcTable
[
"
name
"
]
.
append
(
func_name_index
)
                    
funcTable
[
"
resource
"
]
.
append
(
resource_index
)
                    
funcTable
[
"
fileName
"
]
.
append
(
file_name_index
)
                    
funcTable
[
"
lineNumber
"
]
.
append
(
line_num
)
                    
funcTable
[
"
columnNumber
"
]
.
append
(
col_num
)
                    
funcTable
[
"
length
"
]
+
=
1
                
frame_address
=
module_offset
or
raw_offset
or
-
1
                
for
i
func_idx
in
enumerate
(
frameTable
[
"
func
"
]
)
:
                    
if
(
                        
func_idx
=
=
func_index
                        
and
frameTable
[
"
line
"
]
[
i
]
=
=
line_num
                        
and
frameTable
[
"
column
"
]
[
i
]
=
=
col_num
                        
and
frameTable
[
"
inlineDepth
"
]
[
i
]
=
=
inline_depth
                        
and
frameTable
[
"
nativeSymbol
"
]
[
i
]
=
=
native_symbol_index
                        
and
frameTable
[
"
address
"
]
[
i
]
=
=
frame_address
                    
)
:
                        
frame_index
=
i
                        
break
                
else
:
                    
frame_index
=
frameTable
[
"
length
"
]
                    
frameTable
[
"
address
"
]
.
append
(
frame_address
)
                    
frameTable
[
"
inlineDepth
"
]
.
append
(
inline_depth
)
                    
frameTable
[
"
category
"
]
.
append
(
OTHER_CATEGORY
)
                    
frameTable
[
"
subcategory
"
]
.
append
(
0
)
                    
frameTable
[
"
func
"
]
.
append
(
func_index
)
                    
frameTable
[
"
nativeSymbol
"
]
.
append
(
native_symbol_index
)
                    
frameTable
[
"
innerWindowID
"
]
.
append
(
0
)
                    
frameTable
[
"
implementation
"
]
.
append
(
None
)
                    
frameTable
[
"
line
"
]
.
append
(
line_num
)
                    
frameTable
[
"
column
"
]
.
append
(
col_num
)
                    
frameTable
[
"
length
"
]
+
=
1
                
new_stack_index
=
stackTable
[
"
length
"
]
                
stackTable
[
"
frame
"
]
.
append
(
frame_index
)
                
stackTable
[
"
prefix
"
]
.
append
(
stack_index
)
                
stackTable
[
"
category
"
]
.
append
(
0
)
                
stackTable
[
"
subcategory
"
]
.
append
(
0
)
                
stackTable
[
"
length
"
]
+
=
1
                
stack_index
=
new_stack_index
            
return
stack_index
        
def
add_marker
(
            
name_index
start
end
data
category_index
=
OTHER_CATEGORY
precision
=
None
        
)
:
            
markers
[
"
startTime
"
]
.
append
(
round
(
(
start
-
start_time
)
*
1000
precision
)
)
            
if
end
is
None
:
                
markers
[
"
endTime
"
]
.
append
(
None
)
                
markers
[
"
phase
"
]
.
append
(
0
)
            
else
:
                
markers
[
"
endTime
"
]
.
append
(
round
(
(
end
-
start_time
)
*
1000
precision
)
)
                
markers
[
"
phase
"
]
.
append
(
1
)
            
markers
[
"
category
"
]
.
append
(
category_index
)
            
markers
[
"
name
"
]
.
append
(
name_index
)
            
stack_index
=
None
            
if
isinstance
(
data
dict
)
and
"
stack
"
in
data
:
                
stack
=
data
[
"
stack
"
]
                
del
data
[
"
stack
"
]
                
if
isinstance
(
stack
str
)
:
                    
stack
=
parse_stack
(
stack
)
                
stack_index
=
get_stack_index
(
stack
)
                
if
stack_index
is
not
None
:
                    
data
[
"
cause
"
]
=
{
                        
"
time
"
:
markers
[
"
startTime
"
]
[
-
1
]
                        
"
stack
"
:
stack_index
                    
}
            
markers
[
"
data
"
]
.
append
(
data
)
            
markers
[
"
stack
"
]
.
append
(
stack_index
)
            
markers
[
"
length
"
]
=
markers
[
"
length
"
]
+
1
        
def
format_percent
(
value
)
:
            
return
str
(
round
(
value
1
)
)
+
"
%
"
        
cpu_string_index
=
get_string_index
(
"
CPU
Use
"
)
        
memory_string_index
=
get_string_index
(
"
Memory
"
)
        
io_string_index
=
get_string_index
(
"
IO
"
)
        
network_string_index
=
get_string_index
(
"
NetIO
"
)
        
interval_string_index
=
get_string_index
(
"
Sampling
Interval
"
)
        
valid_cpu_fields
=
set
(
)
        
for
m
in
self
.
measurements
:
            
if
m
.
end
-
m
.
start
<
self
.
poll_interval
/
10
:
                
continue
            
markerData
=
{
                
"
type
"
:
"
CPU
"
                
"
cpuPercent
"
:
format_percent
(
                    
sum
(
list
(
m
.
cpu_percent
)
)
/
len
(
m
.
cpu_percent
)
                
)
            
}
            
total
=
0
            
for
field
in
[
"
nice
"
"
user
"
"
system
"
"
iowait
"
"
softirq
"
"
idle
"
]
:
                
if
hasattr
(
m
.
cpu_times
[
0
]
field
)
:
                    
total
+
=
sum
(
getattr
(
core
field
)
for
core
in
m
.
cpu_times
)
/
(
                        
m
.
end
-
m
.
start
                    
)
            
divisor
=
total
if
total
>
1
else
1
            
total
=
0
            
for
field
in
[
"
nice
"
"
user
"
"
system
"
"
iowait
"
"
softirq
"
]
:
                
if
hasattr
(
m
.
cpu_times
[
0
]
field
)
:
                    
total
+
=
(
                        
sum
(
getattr
(
core
field
)
for
core
in
m
.
cpu_times
)
                        
/
(
m
.
end
-
m
.
start
)
                        
/
divisor
                    
)
                    
if
total
>
0
:
                        
valid_cpu_fields
.
add
(
field
)
                    
markerData
[
field
]
=
round
(
total
3
)
            
for
field
in
[
"
nice
"
"
user
"
"
system
"
"
iowait
"
"
idle
"
]
:
                
if
hasattr
(
m
.
cpu_times
[
0
]
field
)
:
                    
markerData
[
field
+
"
_pct
"
]
=
format_percent
(
                        
100
                        
*
sum
(
getattr
(
core
field
)
for
core
in
m
.
cpu_times
)
                        
/
(
m
.
end
-
m
.
start
)
                        
/
len
(
m
.
cpu_times
)
                    
)
            
add_marker
(
cpu_string_index
m
.
start
m
.
end
markerData
)
            
markerData
=
{
"
type
"
:
"
Mem
"
"
used
"
:
m
.
virt
.
used
}
            
if
hasattr
(
m
.
virt
"
cached
"
)
:
                
markerData
[
"
cached
"
]
=
m
.
virt
.
cached
            
if
hasattr
(
m
.
virt
"
buffers
"
)
:
                
markerData
[
"
buffers
"
]
=
m
.
virt
.
buffers
            
add_marker
(
memory_string_index
m
.
start
m
.
end
markerData
)
            
markerData
=
{
                
"
type
"
:
"
IO
"
                
"
read_count
"
:
m
.
io
.
read_count
                
"
read_bytes
"
:
m
.
io
.
read_bytes
                
"
write_count
"
:
m
.
io
.
write_count
                
"
write_bytes
"
:
m
.
io
.
write_bytes
            
}
            
add_marker
(
io_string_index
m
.
start
m
.
end
markerData
)
            
markerData
=
{
                
"
type
"
:
"
NetIO
"
                
"
recv_count
"
:
m
.
net_io
.
packets_recv
                
"
recv_bytes
"
:
m
.
net_io
.
bytes_recv
                
"
sent_count
"
:
m
.
net_io
.
packets_sent
                
"
sent_bytes
"
:
m
.
net_io
.
bytes_sent
            
}
            
add_marker
(
network_string_index
m
.
start
m
.
end
markerData
)
            
add_marker
(
                
interval_string_index
                
m
.
end
                
None
                
{
                    
"
type
"
:
"
Interval
"
                    
"
interval
"
:
round
(
(
m
.
end
-
m
.
start
)
*
1000
)
                
}
            
)
        
cpuSchema
=
{
            
"
name
"
:
"
CPU
"
            
"
tooltipLabel
"
:
"
{
marker
.
name
}
"
            
"
display
"
:
[
]
            
"
data
"
:
[
{
"
key
"
:
"
cpuPercent
"
"
label
"
:
"
CPU
Percent
"
"
format
"
:
"
string
"
}
]
            
"
graphs
"
:
[
]
        
}
        
cpuData
=
cpuSchema
[
"
data
"
]
        
for
field
label
in
{
            
"
user
"
:
"
User
%
"
            
"
iowait
"
:
"
IO
Wait
%
"
            
"
system
"
:
"
System
%
"
            
"
nice
"
:
"
Nice
%
"
            
"
idle
"
:
"
Idle
%
"
        
}
.
items
(
)
:
            
if
field
in
valid_cpu_fields
or
field
=
=
"
idle
"
:
                
cpuData
.
append
(
{
                    
"
key
"
:
field
+
"
_pct
"
                    
"
label
"
:
label
                    
"
format
"
:
"
string
"
                
}
)
        
cpuGraphs
=
cpuSchema
[
"
graphs
"
]
        
for
field
color
in
{
            
"
softirq
"
:
"
orange
"
            
"
iowait
"
:
"
red
"
            
"
system
"
:
"
grey
"
            
"
user
"
:
"
yellow
"
            
"
nice
"
:
"
blue
"
        
}
.
items
(
)
:
            
if
field
in
valid_cpu_fields
:
                
cpuGraphs
.
append
(
{
"
key
"
:
field
"
color
"
:
color
"
type
"
:
"
bar
"
}
)
        
profile
[
"
meta
"
]
[
"
markerSchema
"
]
.
insert
(
0
cpuSchema
)
        
phase_string_index
=
get_string_index
(
"
Phase
"
)
        
for
phase
v
in
self
.
phases
.
items
(
)
:
            
markerData
=
{
"
type
"
:
"
Phase
"
"
phase
"
:
phase
}
            
cpu_percent_cores
=
self
.
aggregate_cpu_percent
(
phase
=
phase
)
            
if
cpu_percent_cores
:
                
markerData
[
"
cpuPercent
"
]
=
format_percent
(
                    
sum
(
cpu_percent_cores
)
/
len
(
cpu_percent_cores
)
                
)
            
cpu_times
=
[
list
(
c
)
for
c
in
self
.
aggregate_cpu_times
(
phase
=
phase
)
]
            
cpu_times_sum
=
[
0
.
0
]
*
self
.
_cpu_times_len
            
for
i
in
range
(
0
self
.
_cpu_times_len
)
:
                
cpu_times_sum
[
i
]
=
sum
(
core
[
i
]
for
core
in
cpu_times
)
            
total_cpu_time_ms
=
sum
(
cpu_times_sum
)
*
1000
            
if
total_cpu_time_ms
>
0
:
                
markerData
[
"
cpuTime
"
]
=
total_cpu_time_ms
            
add_marker
(
phase_string_index
v
[
0
]
v
[
1
]
markerData
PHASE_CATEGORY
3
)
        
process_string_index
=
get_string_index
(
"
process
"
)
        
for
pid
start
end
cmd
ppid
in
self
.
processes
:
            
markerData
=
{
"
type
"
:
"
Process
"
"
pid
"
:
pid
"
ppid
"
:
ppid
"
cmd
"
:
cmd
}
            
add_marker
(
process_string_index
start
end
markerData
)
        
for
name
start
end
data
in
self
.
markers
:
            
markerData
=
(
                
data
if
isinstance
(
data
dict
)
else
{
"
type
"
:
"
Text
"
"
text
"
:
str
(
data
)
}
            
)
            
add_marker
(
get_string_index
(
name
)
start
end
markerData
TASK_CATEGORY
3
)
        
if
self
.
events
:
            
event_string_index
=
get_string_index
(
"
Event
"
)
            
for
event
in
self
.
events
:
                
if
len
(
event
)
=
=
3
:
                    
event_time
name
data
=
event
                    
add_marker
(
                        
get_string_index
(
name
)
                        
event_time
                        
None
                        
data
                        
OTHER_CATEGORY
                        
3
                    
)
                
elif
len
(
event
)
=
=
2
:
                    
event_time
text
=
event
                    
add_marker
(
                        
event_string_index
                        
event_time
                        
None
                        
{
"
type
"
:
"
Text
"
"
text
"
:
text
}
                        
OTHER_CATEGORY
                        
3
                    
)
        
now
=
time
.
monotonic
(
)
        
profile
[
"
meta
"
]
[
"
profilingEndTime
"
]
=
round
(
            
(
now
-
self
.
start_time
)
*
1000
+
0
.
0005
3
        
)
        
markerData
=
{
            
"
type
"
:
"
Phase
"
            
"
phase
"
:
"
teardown
"
        
}
        
add_marker
(
            
phase_string_index
self
.
stop_time
now
markerData
PHASE_CATEGORY
3
        
)
        
teardown_string_index
=
get_string_index
(
"
resourcemonitor
"
)
        
markerData
=
{
            
"
type
"
:
"
Text
"
            
"
text
"
:
"
stop
"
        
}
        
add_marker
(
            
teardown_string_index
            
self
.
stop_time
            
self
.
end_time
            
markerData
            
TASK_CATEGORY
            
3
        
)
        
markerData
=
{
            
"
type
"
:
"
Text
"
            
"
text
"
:
"
as_profile
"
        
}
        
add_marker
(
            
teardown_string_index
profile_time
now
markerData
TASK_CATEGORY
3
        
)
        
return
profile
