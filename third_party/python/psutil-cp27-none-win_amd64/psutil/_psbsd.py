"
"
"
FreeBSD
OpenBSD
and
NetBSD
platforms
implementation
.
"
"
"
import
contextlib
import
errno
import
functools
import
os
import
xml
.
etree
.
ElementTree
as
ET
from
collections
import
namedtuple
from
socket
import
AF_INET
from
.
import
_common
from
.
import
_psposix
from
.
import
_psutil_bsd
as
cext
from
.
import
_psutil_posix
as
cext_posix
from
.
_common
import
AF_INET6
from
.
_common
import
conn_tmap
from
.
_common
import
FREEBSD
from
.
_common
import
memoize
from
.
_common
import
memoize_when_activated
from
.
_common
import
NETBSD
from
.
_common
import
OPENBSD
from
.
_common
import
sockfam_to_enum
from
.
_common
import
socktype_to_enum
from
.
_common
import
usage_percent
from
.
_compat
import
which
from
.
_exceptions
import
AccessDenied
from
.
_exceptions
import
NoSuchProcess
from
.
_exceptions
import
ZombieProcess
__extra__all__
=
[
]
if
FREEBSD
:
    
PROC_STATUSES
=
{
        
cext
.
SIDL
:
_common
.
STATUS_IDLE
        
cext
.
SRUN
:
_common
.
STATUS_RUNNING
        
cext
.
SSLEEP
:
_common
.
STATUS_SLEEPING
        
cext
.
SSTOP
:
_common
.
STATUS_STOPPED
        
cext
.
SZOMB
:
_common
.
STATUS_ZOMBIE
        
cext
.
SWAIT
:
_common
.
STATUS_WAITING
        
cext
.
SLOCK
:
_common
.
STATUS_LOCKED
    
}
elif
OPENBSD
or
NETBSD
:
    
PROC_STATUSES
=
{
        
cext
.
SIDL
:
_common
.
STATUS_IDLE
        
cext
.
SSLEEP
:
_common
.
STATUS_SLEEPING
        
cext
.
SSTOP
:
_common
.
STATUS_STOPPED
        
cext
.
SDEAD
:
_common
.
STATUS_ZOMBIE
        
cext
.
SZOMB
:
_common
.
STATUS_ZOMBIE
        
cext
.
SRUN
:
_common
.
STATUS_WAKING
        
cext
.
SONPROC
:
_common
.
STATUS_RUNNING
    
}
elif
NETBSD
:
    
PROC_STATUSES
=
{
        
cext
.
SIDL
:
_common
.
STATUS_IDLE
        
cext
.
SACTIVE
:
_common
.
STATUS_RUNNING
        
cext
.
SDYING
:
_common
.
STATUS_ZOMBIE
        
cext
.
SSTOP
:
_common
.
STATUS_STOPPED
        
cext
.
SZOMB
:
_common
.
STATUS_ZOMBIE
        
cext
.
SDEAD
:
_common
.
STATUS_DEAD
        
cext
.
SSUSPENDED
:
_common
.
STATUS_SUSPENDED
    
}
TCP_STATUSES
=
{
    
cext
.
TCPS_ESTABLISHED
:
_common
.
CONN_ESTABLISHED
    
cext
.
TCPS_SYN_SENT
:
_common
.
CONN_SYN_SENT
    
cext
.
TCPS_SYN_RECEIVED
:
_common
.
CONN_SYN_RECV
    
cext
.
TCPS_FIN_WAIT_1
:
_common
.
CONN_FIN_WAIT1
    
cext
.
TCPS_FIN_WAIT_2
:
_common
.
CONN_FIN_WAIT2
    
cext
.
TCPS_TIME_WAIT
:
_common
.
CONN_TIME_WAIT
    
cext
.
TCPS_CLOSED
:
_common
.
CONN_CLOSE
    
cext
.
TCPS_CLOSE_WAIT
:
_common
.
CONN_CLOSE_WAIT
    
cext
.
TCPS_LAST_ACK
:
_common
.
CONN_LAST_ACK
    
cext
.
TCPS_LISTEN
:
_common
.
CONN_LISTEN
    
cext
.
TCPS_CLOSING
:
_common
.
CONN_CLOSING
    
cext
.
PSUTIL_CONN_NONE
:
_common
.
CONN_NONE
}
if
NETBSD
:
    
PAGESIZE
=
os
.
sysconf
(
"
SC_PAGESIZE
"
)
else
:
    
PAGESIZE
=
os
.
sysconf
(
"
SC_PAGE_SIZE
"
)
AF_LINK
=
cext_posix
.
AF_LINK
kinfo_proc_map
=
dict
(
    
ppid
=
0
    
status
=
1
    
real_uid
=
2
    
effective_uid
=
3
    
saved_uid
=
4
    
real_gid
=
5
    
effective_gid
=
6
    
saved_gid
=
7
    
ttynr
=
8
    
create_time
=
9
    
ctx_switches_vol
=
10
    
ctx_switches_unvol
=
11
    
read_io_count
=
12
    
write_io_count
=
13
    
user_time
=
14
    
sys_time
=
15
    
ch_user_time
=
16
    
ch_sys_time
=
17
    
rss
=
18
    
vms
=
19
    
memtext
=
20
    
memdata
=
21
    
memstack
=
22
    
cpunum
=
23
    
name
=
24
)
svmem
=
namedtuple
(
    
'
svmem
'
[
'
total
'
'
available
'
'
percent
'
'
used
'
'
free
'
              
'
active
'
'
inactive
'
'
buffers
'
'
cached
'
'
shared
'
'
wired
'
]
)
scputimes
=
namedtuple
(
    
'
scputimes
'
[
'
user
'
'
nice
'
'
system
'
'
idle
'
'
irq
'
]
)
pmem
=
namedtuple
(
'
pmem
'
[
'
rss
'
'
vms
'
'
text
'
'
data
'
'
stack
'
]
)
pfullmem
=
pmem
pcputimes
=
namedtuple
(
'
pcputimes
'
                       
[
'
user
'
'
system
'
'
children_user
'
'
children_system
'
]
)
pmmap_grouped
=
namedtuple
(
    
'
pmmap_grouped
'
'
path
rss
private
ref_count
shadow_count
'
)
pmmap_ext
=
namedtuple
(
    
'
pmmap_ext
'
'
addr
perms
path
rss
private
ref_count
shadow_count
'
)
if
FREEBSD
:
    
sdiskio
=
namedtuple
(
'
sdiskio
'
[
'
read_count
'
'
write_count
'
                                     
'
read_bytes
'
'
write_bytes
'
                                     
'
read_time
'
'
write_time
'
                                     
'
busy_time
'
]
)
else
:
    
sdiskio
=
namedtuple
(
'
sdiskio
'
[
'
read_count
'
'
write_count
'
                                     
'
read_bytes
'
'
write_bytes
'
]
)
def
virtual_memory
(
)
:
    
"
"
"
System
virtual
memory
as
a
namedtuple
.
"
"
"
    
mem
=
cext
.
virtual_mem
(
)
    
total
free
active
inactive
wired
cached
buffers
shared
=
mem
    
if
NETBSD
:
        
with
open
(
'
/
proc
/
meminfo
'
'
rb
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
b
'
Buffers
:
'
)
:
                    
buffers
=
int
(
line
.
split
(
)
[
1
]
)
*
1024
                
elif
line
.
startswith
(
b
'
MemShared
:
'
)
:
                    
shared
=
int
(
line
.
split
(
)
[
1
]
)
*
1024
    
avail
=
inactive
+
cached
+
free
    
used
=
active
+
wired
+
cached
    
percent
=
usage_percent
(
(
total
-
avail
)
total
_round
=
1
)
    
return
svmem
(
total
avail
percent
used
free
                 
active
inactive
buffers
cached
shared
wired
)
def
swap_memory
(
)
:
    
"
"
"
System
swap
memory
as
(
total
used
free
sin
sout
)
namedtuple
.
"
"
"
    
total
used
free
sin
sout
=
cext
.
swap_mem
(
)
    
percent
=
usage_percent
(
used
total
_round
=
1
)
    
return
_common
.
sswap
(
total
used
free
percent
sin
sout
)
def
cpu_times
(
)
:
    
"
"
"
Return
system
per
-
CPU
times
as
a
namedtuple
"
"
"
    
user
nice
system
idle
irq
=
cext
.
cpu_times
(
)
    
return
scputimes
(
user
nice
system
idle
irq
)
if
hasattr
(
cext
"
per_cpu_times
"
)
:
    
def
per_cpu_times
(
)
:
        
"
"
"
Return
system
CPU
times
as
a
namedtuple
"
"
"
        
ret
=
[
]
        
for
cpu_t
in
cext
.
per_cpu_times
(
)
:
            
user
nice
system
idle
irq
=
cpu_t
            
item
=
scputimes
(
user
nice
system
idle
irq
)
            
ret
.
append
(
item
)
        
return
ret
else
:
    
def
per_cpu_times
(
)
:
        
"
"
"
Return
system
CPU
times
as
a
namedtuple
"
"
"
        
if
cpu_count_logical
(
)
=
=
1
:
            
return
[
cpu_times
(
)
]
        
if
per_cpu_times
.
__called__
:
            
raise
NotImplementedError
(
"
supported
only
starting
from
FreeBSD
8
"
)
        
per_cpu_times
.
__called__
=
True
        
return
[
cpu_times
(
)
]
    
per_cpu_times
.
__called__
=
False
def
cpu_count_logical
(
)
:
    
"
"
"
Return
the
number
of
logical
CPUs
in
the
system
.
"
"
"
    
return
cext
.
cpu_count_logical
(
)
if
OPENBSD
or
NETBSD
:
    
def
cpu_count_physical
(
)
:
        
return
1
if
cpu_count_logical
(
)
=
=
1
else
None
else
:
    
def
cpu_count_physical
(
)
:
        
"
"
"
Return
the
number
of
physical
CPUs
in
the
system
.
"
"
"
        
ret
=
None
        
s
=
cext
.
cpu_count_phys
(
)
        
if
s
is
not
None
:
            
index
=
s
.
rfind
(
"
<
/
groups
>
"
)
            
if
index
!
=
-
1
:
                
s
=
s
[
:
index
+
9
]
                
root
=
ET
.
fromstring
(
s
)
                
try
:
                    
ret
=
len
(
root
.
findall
(
'
group
/
children
/
group
/
cpu
'
)
)
or
None
                
finally
:
                    
root
.
clear
(
)
        
if
not
ret
:
            
if
cpu_count_logical
(
)
=
=
1
:
                
return
1
        
return
ret
def
cpu_stats
(
)
:
    
"
"
"
Return
various
CPU
stats
as
a
named
tuple
.
"
"
"
    
if
FREEBSD
:
        
ctxsw
intrs
soft_intrs
syscalls
traps
=
cext
.
cpu_stats
(
)
    
elif
NETBSD
:
        
ctxsw
intrs
soft_intrs
syscalls
traps
faults
forks
=
\
            
cext
.
cpu_stats
(
)
        
with
open
(
'
/
proc
/
stat
'
'
rb
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
b
'
intr
'
)
:
                    
intrs
=
int
(
line
.
split
(
)
[
1
]
)
    
elif
OPENBSD
:
        
ctxsw
intrs
soft_intrs
syscalls
traps
faults
forks
=
\
            
cext
.
cpu_stats
(
)
    
return
_common
.
scpustats
(
ctxsw
intrs
soft_intrs
syscalls
)
def
disk_partitions
(
all
=
False
)
:
    
"
"
"
Return
mounted
disk
partitions
as
a
list
of
namedtuples
.
    
'
all
'
argument
is
ignored
see
:
    
https
:
/
/
github
.
com
/
giampaolo
/
psutil
/
issues
/
906
    
"
"
"
    
retlist
=
[
]
    
partitions
=
cext
.
disk_partitions
(
)
    
for
partition
in
partitions
:
        
device
mountpoint
fstype
opts
=
partition
        
ntuple
=
_common
.
sdiskpart
(
device
mountpoint
fstype
opts
)
        
retlist
.
append
(
ntuple
)
    
return
retlist
disk_usage
=
_psposix
.
disk_usage
disk_io_counters
=
cext
.
disk_io_counters
net_io_counters
=
cext
.
net_io_counters
net_if_addrs
=
cext_posix
.
net_if_addrs
def
net_if_stats
(
)
:
    
"
"
"
Get
NIC
stats
(
isup
duplex
speed
mtu
)
.
"
"
"
    
names
=
net_io_counters
(
)
.
keys
(
)
    
ret
=
{
}
    
for
name
in
names
:
        
mtu
=
cext_posix
.
net_if_mtu
(
name
)
        
isup
=
cext_posix
.
net_if_flags
(
name
)
        
duplex
speed
=
cext_posix
.
net_if_duplex_speed
(
name
)
        
if
hasattr
(
_common
'
NicDuplex
'
)
:
            
duplex
=
_common
.
NicDuplex
(
duplex
)
        
ret
[
name
]
=
_common
.
snicstats
(
isup
duplex
speed
mtu
)
    
return
ret
def
net_connections
(
kind
)
:
    
"
"
"
System
-
wide
network
connections
.
"
"
"
    
if
OPENBSD
:
        
ret
=
[
]
        
for
pid
in
pids
(
)
:
            
try
:
                
cons
=
Process
(
pid
)
.
connections
(
kind
)
            
except
(
NoSuchProcess
ZombieProcess
)
:
                
continue
            
else
:
                
for
conn
in
cons
:
                    
conn
=
list
(
conn
)
                    
conn
.
append
(
pid
)
                    
ret
.
append
(
_common
.
sconn
(
*
conn
)
)
        
return
ret
    
if
kind
not
in
_common
.
conn_tmap
:
        
raise
ValueError
(
"
invalid
%
r
kind
argument
;
choose
between
%
s
"
                         
%
(
kind
'
'
.
join
(
[
repr
(
x
)
for
x
in
conn_tmap
]
)
)
)
    
families
types
=
conn_tmap
[
kind
]
    
ret
=
set
(
)
    
if
NETBSD
:
        
rawlist
=
cext
.
net_connections
(
-
1
)
    
else
:
        
rawlist
=
cext
.
net_connections
(
)
    
for
item
in
rawlist
:
        
fd
fam
type
laddr
raddr
status
pid
=
item
        
if
fam
in
families
and
type
in
types
:
            
try
:
                
status
=
TCP_STATUSES
[
status
]
            
except
KeyError
:
                
status
=
TCP_STATUSES
[
cext
.
PSUTIL_CONN_NONE
]
            
if
fam
in
(
AF_INET
AF_INET6
)
:
                
if
laddr
:
                    
laddr
=
_common
.
addr
(
*
laddr
)
                
if
raddr
:
                    
raddr
=
_common
.
addr
(
*
raddr
)
            
fam
=
sockfam_to_enum
(
fam
)
            
type
=
socktype_to_enum
(
type
)
            
nt
=
_common
.
sconn
(
fd
fam
type
laddr
raddr
status
pid
)
            
ret
.
add
(
nt
)
    
return
list
(
ret
)
if
FREEBSD
:
    
def
sensors_battery
(
)
:
        
"
"
"
Return
battery
info
.
"
"
"
        
try
:
            
percent
minsleft
power_plugged
=
cext
.
sensors_battery
(
)
        
except
NotImplementedError
:
            
return
None
        
power_plugged
=
power_plugged
=
=
1
        
if
power_plugged
:
            
secsleft
=
_common
.
POWER_TIME_UNLIMITED
        
elif
minsleft
=
=
-
1
:
            
secsleft
=
_common
.
POWER_TIME_UNKNOWN
        
else
:
            
secsleft
=
minsleft
*
60
        
return
_common
.
sbattery
(
percent
secsleft
power_plugged
)
def
boot_time
(
)
:
    
"
"
"
The
system
boot
time
expressed
in
seconds
since
the
epoch
.
"
"
"
    
return
cext
.
boot_time
(
)
def
users
(
)
:
    
"
"
"
Return
currently
connected
users
as
a
list
of
namedtuples
.
"
"
"
    
retlist
=
[
]
    
rawlist
=
cext
.
users
(
)
    
for
item
in
rawlist
:
        
user
tty
hostname
tstamp
pid
=
item
        
if
pid
=
=
-
1
:
            
assert
OPENBSD
            
pid
=
None
        
if
tty
=
=
'
~
'
:
            
continue
        
nt
=
_common
.
suser
(
user
tty
or
None
hostname
tstamp
pid
)
        
retlist
.
append
(
nt
)
    
return
retlist
memoize
def
_pid_0_exists
(
)
:
    
try
:
        
Process
(
0
)
.
name
(
)
    
except
NoSuchProcess
:
        
return
False
    
except
AccessDenied
:
        
return
True
    
else
:
        
return
True
def
pids
(
)
:
    
"
"
"
Returns
a
list
of
PIDs
currently
running
on
the
system
.
"
"
"
    
ret
=
cext
.
pids
(
)
    
if
OPENBSD
and
(
0
not
in
ret
)
and
_pid_0_exists
(
)
:
        
ret
.
insert
(
0
0
)
    
return
ret
if
OPENBSD
or
NETBSD
:
    
def
pid_exists
(
pid
)
:
        
"
"
"
Return
True
if
pid
exists
.
"
"
"
        
exists
=
_psposix
.
pid_exists
(
pid
)
        
if
not
exists
:
            
return
pid
in
pids
(
)
        
else
:
            
return
True
else
:
    
pid_exists
=
_psposix
.
pid_exists
def
wrap_exceptions
(
fun
)
:
    
"
"
"
Decorator
which
translates
bare
OSError
exceptions
into
    
NoSuchProcess
and
AccessDenied
.
    
"
"
"
    
functools
.
wraps
(
fun
)
    
def
wrapper
(
self
*
args
*
*
kwargs
)
:
        
try
:
            
return
fun
(
self
*
args
*
*
kwargs
)
        
except
OSError
as
err
:
            
if
self
.
pid
=
=
0
:
                
if
0
in
pids
(
)
:
                    
raise
AccessDenied
(
self
.
pid
self
.
_name
)
                
else
:
                    
raise
            
if
err
.
errno
=
=
errno
.
ESRCH
:
                
if
not
pid_exists
(
self
.
pid
)
:
                    
raise
NoSuchProcess
(
self
.
pid
self
.
_name
)
                
else
:
                    
raise
ZombieProcess
(
self
.
pid
self
.
_name
self
.
_ppid
)
            
if
err
.
errno
in
(
errno
.
EPERM
errno
.
EACCES
)
:
                
raise
AccessDenied
(
self
.
pid
self
.
_name
)
            
raise
    
return
wrapper
contextlib
.
contextmanager
def
wrap_exceptions_procfs
(
inst
)
:
    
"
"
"
Same
as
above
for
routines
relying
on
reading
/
proc
fs
.
"
"
"
    
try
:
        
yield
    
except
EnvironmentError
as
err
:
        
if
err
.
errno
in
(
errno
.
ENOENT
errno
.
ESRCH
)
:
            
if
not
pid_exists
(
inst
.
pid
)
:
                
raise
NoSuchProcess
(
inst
.
pid
inst
.
_name
)
            
else
:
                
raise
ZombieProcess
(
inst
.
pid
inst
.
_name
inst
.
_ppid
)
        
if
err
.
errno
in
(
errno
.
EPERM
errno
.
EACCES
)
:
            
raise
AccessDenied
(
inst
.
pid
inst
.
_name
)
        
raise
class
Process
(
object
)
:
    
"
"
"
Wrapper
class
around
underlying
C
implementation
.
"
"
"
    
__slots__
=
[
"
pid
"
"
_name
"
"
_ppid
"
]
    
def
__init__
(
self
pid
)
:
        
self
.
pid
=
pid
        
self
.
_name
=
None
        
self
.
_ppid
=
None
    
memoize_when_activated
    
def
oneshot
(
self
)
:
        
"
"
"
Retrieves
multiple
process
info
in
one
shot
as
a
raw
tuple
.
"
"
"
        
ret
=
cext
.
proc_oneshot_info
(
self
.
pid
)
        
assert
len
(
ret
)
=
=
len
(
kinfo_proc_map
)
        
return
ret
    
def
oneshot_enter
(
self
)
:
        
self
.
oneshot
.
cache_activate
(
)
    
def
oneshot_exit
(
self
)
:
        
self
.
oneshot
.
cache_deactivate
(
)
    
wrap_exceptions
    
def
name
(
self
)
:
        
name
=
self
.
oneshot
(
)
[
kinfo_proc_map
[
'
name
'
]
]
        
return
name
if
name
is
not
None
else
cext
.
proc_name
(
self
.
pid
)
    
wrap_exceptions
    
def
exe
(
self
)
:
        
if
FREEBSD
:
            
return
cext
.
proc_exe
(
self
.
pid
)
        
elif
NETBSD
:
            
if
self
.
pid
=
=
0
:
                
return
"
"
            
with
wrap_exceptions_procfs
(
self
)
:
                
return
os
.
readlink
(
"
/
proc
/
%
s
/
exe
"
%
self
.
pid
)
        
else
:
            
cmdline
=
self
.
cmdline
(
)
            
if
cmdline
:
                
return
which
(
cmdline
[
0
]
)
            
else
:
                
return
"
"
    
wrap_exceptions
    
def
cmdline
(
self
)
:
        
if
OPENBSD
and
self
.
pid
=
=
0
:
            
return
[
]
        
elif
NETBSD
:
            
try
:
                
return
cext
.
proc_cmdline
(
self
.
pid
)
            
except
OSError
as
err
:
                
if
err
.
errno
=
=
errno
.
EINVAL
:
                    
if
not
pid_exists
(
self
.
pid
)
:
                        
raise
NoSuchProcess
(
self
.
pid
self
.
_name
)
                    
else
:
                        
raise
ZombieProcess
(
self
.
pid
self
.
_name
self
.
_ppid
)
                
else
:
                    
raise
        
else
:
            
return
cext
.
proc_cmdline
(
self
.
pid
)
    
wrap_exceptions
    
def
terminal
(
self
)
:
        
tty_nr
=
self
.
oneshot
(
)
[
kinfo_proc_map
[
'
ttynr
'
]
]
        
tmap
=
_psposix
.
get_terminal_map
(
)
        
try
:
            
return
tmap
[
tty_nr
]
        
except
KeyError
:
            
return
None
    
wrap_exceptions
    
def
ppid
(
self
)
:
        
self
.
_ppid
=
self
.
oneshot
(
)
[
kinfo_proc_map
[
'
ppid
'
]
]
        
return
self
.
_ppid
    
wrap_exceptions
    
def
uids
(
self
)
:
        
rawtuple
=
self
.
oneshot
(
)
        
return
_common
.
puids
(
            
rawtuple
[
kinfo_proc_map
[
'
real_uid
'
]
]
            
rawtuple
[
kinfo_proc_map
[
'
effective_uid
'
]
]
            
rawtuple
[
kinfo_proc_map
[
'
saved_uid
'
]
]
)
    
wrap_exceptions
    
def
gids
(
self
)
:
        
rawtuple
=
self
.
oneshot
(
)
        
return
_common
.
pgids
(
            
rawtuple
[
kinfo_proc_map
[
'
real_gid
'
]
]
            
rawtuple
[
kinfo_proc_map
[
'
effective_gid
'
]
]
            
rawtuple
[
kinfo_proc_map
[
'
saved_gid
'
]
]
)
    
wrap_exceptions
    
def
cpu_times
(
self
)
:
        
rawtuple
=
self
.
oneshot
(
)
        
return
_common
.
pcputimes
(
            
rawtuple
[
kinfo_proc_map
[
'
user_time
'
]
]
            
rawtuple
[
kinfo_proc_map
[
'
sys_time
'
]
]
            
rawtuple
[
kinfo_proc_map
[
'
ch_user_time
'
]
]
            
rawtuple
[
kinfo_proc_map
[
'
ch_sys_time
'
]
]
)
    
if
FREEBSD
:
        
wrap_exceptions
        
def
cpu_num
(
self
)
:
            
return
self
.
oneshot
(
)
[
kinfo_proc_map
[
'
cpunum
'
]
]
    
wrap_exceptions
    
def
memory_info
(
self
)
:
        
rawtuple
=
self
.
oneshot
(
)
        
return
pmem
(
            
rawtuple
[
kinfo_proc_map
[
'
rss
'
]
]
            
rawtuple
[
kinfo_proc_map
[
'
vms
'
]
]
            
rawtuple
[
kinfo_proc_map
[
'
memtext
'
]
]
            
rawtuple
[
kinfo_proc_map
[
'
memdata
'
]
]
            
rawtuple
[
kinfo_proc_map
[
'
memstack
'
]
]
)
    
memory_full_info
=
memory_info
    
wrap_exceptions
    
def
create_time
(
self
)
:
        
return
self
.
oneshot
(
)
[
kinfo_proc_map
[
'
create_time
'
]
]
    
wrap_exceptions
    
def
num_threads
(
self
)
:
        
if
hasattr
(
cext
"
proc_num_threads
"
)
:
            
return
cext
.
proc_num_threads
(
self
.
pid
)
        
else
:
            
return
len
(
self
.
threads
(
)
)
    
wrap_exceptions
    
def
num_ctx_switches
(
self
)
:
        
rawtuple
=
self
.
oneshot
(
)
        
return
_common
.
pctxsw
(
            
rawtuple
[
kinfo_proc_map
[
'
ctx_switches_vol
'
]
]
            
rawtuple
[
kinfo_proc_map
[
'
ctx_switches_unvol
'
]
]
)
    
wrap_exceptions
    
def
threads
(
self
)
:
        
rawlist
=
cext
.
proc_threads
(
self
.
pid
)
        
retlist
=
[
]
        
for
thread_id
utime
stime
in
rawlist
:
            
ntuple
=
_common
.
pthread
(
thread_id
utime
stime
)
            
retlist
.
append
(
ntuple
)
        
if
OPENBSD
:
            
self
.
name
(
)
        
return
retlist
    
wrap_exceptions
    
def
connections
(
self
kind
=
'
inet
'
)
:
        
if
kind
not
in
conn_tmap
:
            
raise
ValueError
(
"
invalid
%
r
kind
argument
;
choose
between
%
s
"
                             
%
(
kind
'
'
.
join
(
[
repr
(
x
)
for
x
in
conn_tmap
]
)
)
)
        
if
NETBSD
:
            
families
types
=
conn_tmap
[
kind
]
            
ret
=
set
(
)
            
rawlist
=
cext
.
net_connections
(
self
.
pid
)
            
for
item
in
rawlist
:
                
fd
fam
type
laddr
raddr
status
pid
=
item
                
assert
pid
=
=
self
.
pid
                
if
fam
in
families
and
type
in
types
:
                    
try
:
                        
status
=
TCP_STATUSES
[
status
]
                    
except
KeyError
:
                        
status
=
TCP_STATUSES
[
cext
.
PSUTIL_CONN_NONE
]
                    
if
fam
in
(
AF_INET
AF_INET6
)
:
                        
if
laddr
:
                            
laddr
=
_common
.
addr
(
*
laddr
)
                        
if
raddr
:
                            
raddr
=
_common
.
addr
(
*
raddr
)
                    
fam
=
sockfam_to_enum
(
fam
)
                    
type
=
socktype_to_enum
(
type
)
                    
nt
=
_common
.
pconn
(
fd
fam
type
laddr
raddr
status
)
                    
ret
.
add
(
nt
)
            
self
.
name
(
)
            
return
list
(
ret
)
        
families
types
=
conn_tmap
[
kind
]
        
rawlist
=
cext
.
proc_connections
(
self
.
pid
families
types
)
        
ret
=
[
]
        
for
item
in
rawlist
:
            
fd
fam
type
laddr
raddr
status
=
item
            
if
fam
in
(
AF_INET
AF_INET6
)
:
                
if
laddr
:
                    
laddr
=
_common
.
addr
(
*
laddr
)
                
if
raddr
:
                    
raddr
=
_common
.
addr
(
*
raddr
)
            
fam
=
sockfam_to_enum
(
fam
)
            
type
=
socktype_to_enum
(
type
)
            
status
=
TCP_STATUSES
[
status
]
            
nt
=
_common
.
pconn
(
fd
fam
type
laddr
raddr
status
)
            
ret
.
append
(
nt
)
        
if
OPENBSD
:
            
self
.
name
(
)
        
return
ret
    
wrap_exceptions
    
def
wait
(
self
timeout
=
None
)
:
        
return
_psposix
.
wait_pid
(
self
.
pid
timeout
self
.
_name
)
    
wrap_exceptions
    
def
nice_get
(
self
)
:
        
return
cext_posix
.
getpriority
(
self
.
pid
)
    
wrap_exceptions
    
def
nice_set
(
self
value
)
:
        
return
cext_posix
.
setpriority
(
self
.
pid
value
)
    
wrap_exceptions
    
def
status
(
self
)
:
        
code
=
self
.
oneshot
(
)
[
kinfo_proc_map
[
'
status
'
]
]
        
return
PROC_STATUSES
.
get
(
code
'
?
'
)
    
wrap_exceptions
    
def
io_counters
(
self
)
:
        
rawtuple
=
self
.
oneshot
(
)
        
return
_common
.
pio
(
            
rawtuple
[
kinfo_proc_map
[
'
read_io_count
'
]
]
            
rawtuple
[
kinfo_proc_map
[
'
write_io_count
'
]
]
            
-
1
            
-
1
)
    
wrap_exceptions
    
def
cwd
(
self
)
:
        
"
"
"
Return
process
current
working
directory
.
"
"
"
        
if
OPENBSD
and
self
.
pid
=
=
0
:
            
return
None
        
elif
NETBSD
:
            
with
wrap_exceptions_procfs
(
self
)
:
                
return
os
.
readlink
(
"
/
proc
/
%
s
/
cwd
"
%
self
.
pid
)
        
elif
hasattr
(
cext
'
proc_open_files
'
)
:
            
return
cext
.
proc_cwd
(
self
.
pid
)
or
None
        
else
:
            
raise
NotImplementedError
(
                
"
supported
only
starting
from
FreeBSD
8
"
if
                
FREEBSD
else
"
"
)
    
nt_mmap_grouped
=
namedtuple
(
        
'
mmap
'
'
path
rss
private
ref_count
shadow_count
'
)
    
nt_mmap_ext
=
namedtuple
(
        
'
mmap
'
'
addr
perms
path
rss
private
ref_count
shadow_count
'
)
    
def
_not_implemented
(
self
)
:
        
raise
NotImplementedError
    
if
hasattr
(
cext
'
proc_open_files
'
)
:
        
wrap_exceptions
        
def
open_files
(
self
)
:
            
"
"
"
Return
files
opened
by
process
as
a
list
of
namedtuples
.
"
"
"
            
rawlist
=
cext
.
proc_open_files
(
self
.
pid
)
            
return
[
_common
.
popenfile
(
path
fd
)
for
path
fd
in
rawlist
]
    
else
:
        
open_files
=
_not_implemented
    
if
hasattr
(
cext
'
proc_num_fds
'
)
:
        
wrap_exceptions
        
def
num_fds
(
self
)
:
            
"
"
"
Return
the
number
of
file
descriptors
opened
by
this
process
.
"
"
"
            
ret
=
cext
.
proc_num_fds
(
self
.
pid
)
            
if
NETBSD
:
                
self
.
name
(
)
            
return
ret
    
else
:
        
num_fds
=
_not_implemented
    
if
FREEBSD
:
        
wrap_exceptions
        
def
cpu_affinity_get
(
self
)
:
            
return
cext
.
proc_cpu_affinity_get
(
self
.
pid
)
        
wrap_exceptions
        
def
cpu_affinity_set
(
self
cpus
)
:
            
allcpus
=
tuple
(
range
(
len
(
per_cpu_times
(
)
)
)
)
            
for
cpu
in
cpus
:
                
if
cpu
not
in
allcpus
:
                    
raise
ValueError
(
"
invalid
CPU
#
%
i
(
choose
between
%
s
)
"
                                     
%
(
cpu
allcpus
)
)
            
try
:
                
cext
.
proc_cpu_affinity_set
(
self
.
pid
cpus
)
            
except
OSError
as
err
:
                
if
err
.
errno
in
(
errno
.
EINVAL
errno
.
EDEADLK
)
:
                    
for
cpu
in
cpus
:
                        
if
cpu
not
in
allcpus
:
                            
raise
ValueError
(
                                
"
invalid
CPU
#
%
i
(
choose
between
%
s
)
"
%
(
                                    
cpu
allcpus
)
)
                
raise
        
wrap_exceptions
        
def
memory_maps
(
self
)
:
            
return
cext
.
proc_memory_maps
(
self
.
pid
)
