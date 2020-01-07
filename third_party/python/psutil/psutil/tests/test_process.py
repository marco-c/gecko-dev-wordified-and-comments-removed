"
"
"
Tests
for
psutil
.
Process
class
.
"
"
"
import
collections
import
errno
import
getpass
import
itertools
import
os
import
signal
import
socket
import
subprocess
import
sys
import
tempfile
import
textwrap
import
time
import
types
import
psutil
from
psutil
import
AIX
from
psutil
import
BSD
from
psutil
import
LINUX
from
psutil
import
NETBSD
from
psutil
import
OPENBSD
from
psutil
import
OSX
from
psutil
import
POSIX
from
psutil
import
SUNOS
from
psutil
import
WINDOWS
from
psutil
.
_compat
import
long
from
psutil
.
_compat
import
PY3
from
psutil
.
tests
import
APPVEYOR
from
psutil
.
tests
import
call_until
from
psutil
.
tests
import
copyload_shared_lib
from
psutil
.
tests
import
create_exe
from
psutil
.
tests
import
create_proc_children_pair
from
psutil
.
tests
import
create_zombie_proc
from
psutil
.
tests
import
enum
from
psutil
.
tests
import
get_test_subprocess
from
psutil
.
tests
import
get_winver
from
psutil
.
tests
import
HAS_CPU_AFFINITY
from
psutil
.
tests
import
HAS_ENVIRON
from
psutil
.
tests
import
HAS_IONICE
from
psutil
.
tests
import
HAS_MEMORY_MAPS
from
psutil
.
tests
import
HAS_PROC_CPU_NUM
from
psutil
.
tests
import
HAS_PROC_IO_COUNTERS
from
psutil
.
tests
import
HAS_RLIMIT
from
psutil
.
tests
import
HAS_THREADS
from
psutil
.
tests
import
mock
from
psutil
.
tests
import
PYPY
from
psutil
.
tests
import
PYTHON_EXE
from
psutil
.
tests
import
reap_children
from
psutil
.
tests
import
retry_before_failing
from
psutil
.
tests
import
run_test_module_by_name
from
psutil
.
tests
import
safe_rmpath
from
psutil
.
tests
import
sh
from
psutil
.
tests
import
skip_on_access_denied
from
psutil
.
tests
import
skip_on_not_implemented
from
psutil
.
tests
import
TESTFILE_PREFIX
from
psutil
.
tests
import
TESTFN
from
psutil
.
tests
import
ThreadTask
from
psutil
.
tests
import
TRAVIS
from
psutil
.
tests
import
unittest
from
psutil
.
tests
import
wait_for_pid
from
psutil
.
tests
import
WIN_VISTA
class
TestProcess
(
unittest
.
TestCase
)
:
    
"
"
"
Tests
for
psutil
.
Process
class
.
"
"
"
    
def
setUp
(
self
)
:
        
safe_rmpath
(
TESTFN
)
    
def
tearDown
(
self
)
:
        
reap_children
(
)
    
def
test_pid
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
self
.
assertEqual
(
p
.
pid
os
.
getpid
(
)
)
        
sproc
=
get_test_subprocess
(
)
        
self
.
assertEqual
(
psutil
.
Process
(
sproc
.
pid
)
.
pid
sproc
.
pid
)
        
with
self
.
assertRaises
(
AttributeError
)
:
            
p
.
pid
=
33
    
def
test_kill
(
self
)
:
        
sproc
=
get_test_subprocess
(
)
        
test_pid
=
sproc
.
pid
        
p
=
psutil
.
Process
(
test_pid
)
        
p
.
kill
(
)
        
sig
=
p
.
wait
(
)
        
self
.
assertFalse
(
psutil
.
pid_exists
(
test_pid
)
)
        
if
POSIX
:
            
self
.
assertEqual
(
sig
-
signal
.
SIGKILL
)
    
def
test_terminate
(
self
)
:
        
sproc
=
get_test_subprocess
(
)
        
test_pid
=
sproc
.
pid
        
p
=
psutil
.
Process
(
test_pid
)
        
p
.
terminate
(
)
        
sig
=
p
.
wait
(
)
        
self
.
assertFalse
(
psutil
.
pid_exists
(
test_pid
)
)
        
if
POSIX
:
            
self
.
assertEqual
(
sig
-
signal
.
SIGTERM
)
    
def
test_send_signal
(
self
)
:
        
sig
=
signal
.
SIGKILL
if
POSIX
else
signal
.
SIGTERM
        
sproc
=
get_test_subprocess
(
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
p
.
send_signal
(
sig
)
        
exit_sig
=
p
.
wait
(
)
        
self
.
assertFalse
(
psutil
.
pid_exists
(
p
.
pid
)
)
        
if
POSIX
:
            
self
.
assertEqual
(
exit_sig
-
sig
)
            
sproc
=
get_test_subprocess
(
)
            
p
=
psutil
.
Process
(
sproc
.
pid
)
            
p
.
send_signal
(
sig
)
            
with
mock
.
patch
(
'
psutil
.
os
.
kill
'
                            
side_effect
=
OSError
(
errno
.
ESRCH
"
"
)
)
:
                
with
self
.
assertRaises
(
psutil
.
NoSuchProcess
)
:
                    
p
.
send_signal
(
sig
)
            
sproc
=
get_test_subprocess
(
)
            
p
=
psutil
.
Process
(
sproc
.
pid
)
            
p
.
send_signal
(
sig
)
            
with
mock
.
patch
(
'
psutil
.
os
.
kill
'
                            
side_effect
=
OSError
(
errno
.
EPERM
"
"
)
)
:
                
with
self
.
assertRaises
(
psutil
.
AccessDenied
)
:
                    
psutil
.
Process
(
)
.
send_signal
(
sig
)
            
if
0
in
psutil
.
pids
(
)
:
                
p
=
psutil
.
Process
(
0
)
                
self
.
assertRaises
(
ValueError
p
.
send_signal
signal
.
SIGTERM
)
    
def
test_wait
(
self
)
:
        
sproc
=
get_test_subprocess
(
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
p
.
kill
(
)
        
code
=
p
.
wait
(
)
        
if
POSIX
:
            
self
.
assertEqual
(
code
-
signal
.
SIGKILL
)
        
else
:
            
self
.
assertEqual
(
code
signal
.
SIGTERM
)
        
self
.
assertFalse
(
p
.
is_running
(
)
)
        
sproc
=
get_test_subprocess
(
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
p
.
terminate
(
)
        
code
=
p
.
wait
(
)
        
if
POSIX
:
            
self
.
assertEqual
(
code
-
signal
.
SIGTERM
)
        
else
:
            
self
.
assertEqual
(
code
signal
.
SIGTERM
)
        
self
.
assertFalse
(
p
.
is_running
(
)
)
        
code
=
"
import
time
sys
;
time
.
sleep
(
0
.
01
)
;
sys
.
exit
(
5
)
;
"
        
sproc
=
get_test_subprocess
(
[
PYTHON_EXE
"
-
c
"
code
]
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
self
.
assertEqual
(
p
.
wait
(
)
5
)
        
self
.
assertFalse
(
p
.
is_running
(
)
)
        
sproc
=
get_test_subprocess
(
[
PYTHON_EXE
"
-
c
"
code
]
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
self
.
assertEqual
(
p
.
wait
(
)
5
)
        
self
.
assertIn
(
p
.
wait
(
)
(
5
None
)
)
        
sproc
=
get_test_subprocess
(
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
p
.
name
(
)
        
self
.
assertRaises
(
psutil
.
TimeoutExpired
p
.
wait
0
.
01
)
        
self
.
assertRaises
(
ValueError
p
.
wait
-
1
)
    
def
test_wait_non_children
(
self
)
:
        
p1
p2
=
create_proc_children_pair
(
)
        
self
.
assertRaises
(
psutil
.
TimeoutExpired
p1
.
wait
0
.
01
)
        
self
.
assertRaises
(
psutil
.
TimeoutExpired
p2
.
wait
0
.
01
)
        
p1
.
terminate
(
)
        
p2
.
terminate
(
)
        
ret1
=
p1
.
wait
(
)
        
ret2
=
p2
.
wait
(
)
        
if
POSIX
:
            
self
.
assertEqual
(
ret1
-
signal
.
SIGTERM
)
            
self
.
assertEqual
(
ret2
None
)
        
else
:
            
self
.
assertEqual
(
ret1
signal
.
SIGTERM
)
            
self
.
assertEqual
(
ret1
signal
.
SIGTERM
)
    
def
test_wait_timeout_0
(
self
)
:
        
sproc
=
get_test_subprocess
(
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
self
.
assertRaises
(
psutil
.
TimeoutExpired
p
.
wait
0
)
        
p
.
kill
(
)
        
stop_at
=
time
.
time
(
)
+
2
        
while
True
:
            
try
:
                
code
=
p
.
wait
(
0
)
            
except
psutil
.
TimeoutExpired
:
                
if
time
.
time
(
)
>
=
stop_at
:
                    
raise
            
else
:
                
break
        
if
POSIX
:
            
self
.
assertEqual
(
code
-
signal
.
SIGKILL
)
        
else
:
            
self
.
assertEqual
(
code
signal
.
SIGTERM
)
        
self
.
assertFalse
(
p
.
is_running
(
)
)
    
def
test_cpu_percent
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
p
.
cpu_percent
(
interval
=
0
.
001
)
        
p
.
cpu_percent
(
interval
=
0
.
001
)
        
for
x
in
range
(
100
)
:
            
percent
=
p
.
cpu_percent
(
interval
=
None
)
            
self
.
assertIsInstance
(
percent
float
)
            
self
.
assertGreaterEqual
(
percent
0
.
0
)
            
if
not
POSIX
:
                
self
.
assertLessEqual
(
percent
100
.
0
)
            
else
:
                
self
.
assertGreaterEqual
(
percent
0
.
0
)
        
with
self
.
assertRaises
(
ValueError
)
:
            
p
.
cpu_percent
(
interval
=
-
1
)
    
def
test_cpu_percent_numcpus_none
(
self
)
:
        
with
mock
.
patch
(
'
psutil
.
cpu_count
'
return_value
=
None
)
as
m
:
            
psutil
.
Process
(
)
.
cpu_percent
(
)
            
assert
m
.
called
    
def
test_cpu_times
(
self
)
:
        
times
=
psutil
.
Process
(
)
.
cpu_times
(
)
        
assert
(
times
.
user
>
0
.
0
)
or
(
times
.
system
>
0
.
0
)
times
        
assert
(
times
.
children_user
>
=
0
.
0
)
times
        
assert
(
times
.
children_system
>
=
0
.
0
)
times
        
for
name
in
times
.
_fields
:
            
time
.
strftime
(
"
%
H
:
%
M
:
%
S
"
time
.
localtime
(
getattr
(
times
name
)
)
)
    
def
test_cpu_times_2
(
self
)
:
        
user_time
kernel_time
=
psutil
.
Process
(
)
.
cpu_times
(
)
[
:
2
]
        
utime
ktime
=
os
.
times
(
)
[
:
2
]
        
if
(
max
(
[
user_time
utime
]
)
-
min
(
[
user_time
utime
]
)
)
>
0
.
1
:
            
self
.
fail
(
"
expected
:
%
s
found
:
%
s
"
%
(
utime
user_time
)
)
        
if
(
max
(
[
kernel_time
ktime
]
)
-
min
(
[
kernel_time
ktime
]
)
)
>
0
.
1
:
            
self
.
fail
(
"
expected
:
%
s
found
:
%
s
"
%
(
ktime
kernel_time
)
)
    
unittest
.
skipIf
(
not
HAS_PROC_CPU_NUM
"
not
supported
"
)
    
def
test_cpu_num
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
num
=
p
.
cpu_num
(
)
        
self
.
assertGreaterEqual
(
num
0
)
        
if
psutil
.
cpu_count
(
)
=
=
1
:
            
self
.
assertEqual
(
num
0
)
        
self
.
assertIn
(
p
.
cpu_num
(
)
range
(
psutil
.
cpu_count
(
)
)
)
    
def
test_create_time
(
self
)
:
        
sproc
=
get_test_subprocess
(
)
        
now
=
time
.
time
(
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
create_time
=
p
.
create_time
(
)
        
difference
=
abs
(
create_time
-
now
)
        
if
difference
>
2
:
            
self
.
fail
(
"
expected
:
%
s
found
:
%
s
difference
:
%
s
"
                      
%
(
now
create_time
difference
)
)
        
time
.
strftime
(
"
%
Y
%
m
%
d
%
H
:
%
M
:
%
S
"
time
.
localtime
(
p
.
create_time
(
)
)
)
    
unittest
.
skipIf
(
not
POSIX
'
POSIX
only
'
)
    
unittest
.
skipIf
(
TRAVIS
'
not
reliable
on
TRAVIS
'
)
    
def
test_terminal
(
self
)
:
        
terminal
=
psutil
.
Process
(
)
.
terminal
(
)
        
if
sys
.
stdin
.
isatty
(
)
or
sys
.
stdout
.
isatty
(
)
:
            
tty
=
os
.
path
.
realpath
(
sh
(
'
tty
'
)
)
            
self
.
assertEqual
(
terminal
tty
)
        
else
:
            
self
.
assertIsNone
(
terminal
)
    
unittest
.
skipIf
(
not
HAS_PROC_IO_COUNTERS
'
not
supported
'
)
    
skip_on_not_implemented
(
only_if
=
LINUX
)
    
def
test_io_counters
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
io1
=
p
.
io_counters
(
)
        
with
open
(
PYTHON_EXE
'
rb
'
)
as
f
:
            
f
.
read
(
)
        
io2
=
p
.
io_counters
(
)
        
if
not
BSD
and
not
AIX
:
            
self
.
assertGreater
(
io2
.
read_count
io1
.
read_count
)
            
self
.
assertEqual
(
io2
.
write_count
io1
.
write_count
)
            
if
LINUX
:
                
self
.
assertGreater
(
io2
.
read_chars
io1
.
read_chars
)
                
self
.
assertEqual
(
io2
.
write_chars
io1
.
write_chars
)
        
else
:
            
self
.
assertGreaterEqual
(
io2
.
read_bytes
io1
.
read_bytes
)
            
self
.
assertGreaterEqual
(
io2
.
write_bytes
io1
.
write_bytes
)
        
io1
=
p
.
io_counters
(
)
        
with
tempfile
.
TemporaryFile
(
prefix
=
TESTFILE_PREFIX
)
as
f
:
            
if
PY3
:
                
f
.
write
(
bytes
(
"
x
"
*
1000000
'
ascii
'
)
)
            
else
:
                
f
.
write
(
"
x
"
*
1000000
)
        
io2
=
p
.
io_counters
(
)
        
self
.
assertGreaterEqual
(
io2
.
write_count
io1
.
write_count
)
        
self
.
assertGreaterEqual
(
io2
.
write_bytes
io1
.
write_bytes
)
        
self
.
assertGreaterEqual
(
io2
.
read_count
io1
.
read_count
)
        
self
.
assertGreaterEqual
(
io2
.
read_bytes
io1
.
read_bytes
)
        
if
LINUX
:
            
self
.
assertGreater
(
io2
.
write_chars
io1
.
write_chars
)
            
self
.
assertGreaterEqual
(
io2
.
read_chars
io1
.
read_chars
)
        
for
i
in
range
(
len
(
io2
)
)
:
            
if
BSD
and
i
>
=
2
:
                
continue
            
self
.
assertGreaterEqual
(
io2
[
i
]
0
)
            
self
.
assertGreaterEqual
(
io2
[
i
]
0
)
    
unittest
.
skipIf
(
not
HAS_IONICE
"
not
supported
"
)
    
unittest
.
skipIf
(
WINDOWS
and
get_winver
(
)
<
WIN_VISTA
'
not
supported
'
)
    
def
test_ionice
(
self
)
:
        
if
LINUX
:
            
from
psutil
import
(
IOPRIO_CLASS_NONE
IOPRIO_CLASS_RT
                                
IOPRIO_CLASS_BE
IOPRIO_CLASS_IDLE
)
            
self
.
assertEqual
(
IOPRIO_CLASS_NONE
0
)
            
self
.
assertEqual
(
IOPRIO_CLASS_RT
1
)
            
self
.
assertEqual
(
IOPRIO_CLASS_BE
2
)
            
self
.
assertEqual
(
IOPRIO_CLASS_IDLE
3
)
            
p
=
psutil
.
Process
(
)
            
try
:
                
p
.
ionice
(
2
)
                
ioclass
value
=
p
.
ionice
(
)
                
if
enum
is
not
None
:
                    
self
.
assertIsInstance
(
ioclass
enum
.
IntEnum
)
                
self
.
assertEqual
(
ioclass
2
)
                
self
.
assertEqual
(
value
4
)
                
p
.
ionice
(
3
)
                
ioclass
value
=
p
.
ionice
(
)
                
self
.
assertEqual
(
ioclass
3
)
                
self
.
assertEqual
(
value
0
)
                
p
.
ionice
(
2
0
)
                
ioclass
value
=
p
.
ionice
(
)
                
self
.
assertEqual
(
ioclass
2
)
                
self
.
assertEqual
(
value
0
)
                
p
.
ionice
(
2
7
)
                
ioclass
value
=
p
.
ionice
(
)
                
self
.
assertEqual
(
ioclass
2
)
                
self
.
assertEqual
(
value
7
)
            
finally
:
                
p
.
ionice
(
IOPRIO_CLASS_NONE
)
        
else
:
            
p
=
psutil
.
Process
(
)
            
original
=
p
.
ionice
(
)
            
self
.
assertIsInstance
(
original
int
)
            
try
:
                
value
=
0
                
if
original
=
=
value
:
                    
value
=
1
                
p
.
ionice
(
value
)
                
self
.
assertEqual
(
p
.
ionice
(
)
value
)
            
finally
:
                
p
.
ionice
(
original
)
    
unittest
.
skipIf
(
not
HAS_IONICE
"
not
supported
"
)
    
unittest
.
skipIf
(
WINDOWS
and
get_winver
(
)
<
WIN_VISTA
'
not
supported
'
)
    
def
test_ionice_errs
(
self
)
:
        
sproc
=
get_test_subprocess
(
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
if
LINUX
:
            
self
.
assertRaises
(
ValueError
p
.
ionice
2
10
)
            
self
.
assertRaises
(
ValueError
p
.
ionice
2
-
1
)
            
self
.
assertRaises
(
ValueError
p
.
ionice
4
)
            
self
.
assertRaises
(
TypeError
p
.
ionice
2
"
foo
"
)
            
self
.
assertRaisesRegex
(
                
ValueError
"
can
'
t
specify
value
with
IOPRIO_CLASS_NONE
"
                
p
.
ionice
psutil
.
IOPRIO_CLASS_NONE
1
)
            
self
.
assertRaisesRegex
(
                
ValueError
"
can
'
t
specify
value
with
IOPRIO_CLASS_IDLE
"
                
p
.
ionice
psutil
.
IOPRIO_CLASS_IDLE
1
)
            
self
.
assertRaisesRegex
(
                
ValueError
"
'
ioclass
'
argument
must
be
specified
"
                
p
.
ionice
value
=
1
)
        
else
:
            
self
.
assertRaises
(
ValueError
p
.
ionice
3
)
            
self
.
assertRaises
(
TypeError
p
.
ionice
2
1
)
    
unittest
.
skipIf
(
not
HAS_RLIMIT
"
not
supported
"
)
    
def
test_rlimit_get
(
self
)
:
        
import
resource
        
p
=
psutil
.
Process
(
os
.
getpid
(
)
)
        
names
=
[
x
for
x
in
dir
(
psutil
)
if
x
.
startswith
(
'
RLIMIT
'
)
]
        
assert
names
names
        
for
name
in
names
:
            
value
=
getattr
(
psutil
name
)
            
self
.
assertGreaterEqual
(
value
0
)
            
if
name
in
dir
(
resource
)
:
                
self
.
assertEqual
(
value
getattr
(
resource
name
)
)
                
if
PYPY
:
                    
continue
                
self
.
assertEqual
(
p
.
rlimit
(
value
)
resource
.
getrlimit
(
value
)
)
            
else
:
                
ret
=
p
.
rlimit
(
value
)
                
self
.
assertEqual
(
len
(
ret
)
2
)
                
self
.
assertGreaterEqual
(
ret
[
0
]
-
1
)
                
self
.
assertGreaterEqual
(
ret
[
1
]
-
1
)
    
unittest
.
skipIf
(
not
HAS_RLIMIT
"
not
supported
"
)
    
def
test_rlimit_set
(
self
)
:
        
sproc
=
get_test_subprocess
(
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
p
.
rlimit
(
psutil
.
RLIMIT_NOFILE
(
5
5
)
)
        
self
.
assertEqual
(
p
.
rlimit
(
psutil
.
RLIMIT_NOFILE
)
(
5
5
)
)
        
with
self
.
assertRaises
(
ValueError
)
:
            
psutil
.
_psplatform
.
Process
(
0
)
.
rlimit
(
0
)
        
with
self
.
assertRaises
(
ValueError
)
:
            
p
.
rlimit
(
psutil
.
RLIMIT_NOFILE
(
5
5
5
)
)
    
unittest
.
skipIf
(
not
HAS_RLIMIT
"
not
supported
"
)
    
def
test_rlimit
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
soft
hard
=
p
.
rlimit
(
psutil
.
RLIMIT_FSIZE
)
        
try
:
            
p
.
rlimit
(
psutil
.
RLIMIT_FSIZE
(
1024
hard
)
)
            
with
open
(
TESTFN
"
wb
"
)
as
f
:
                
f
.
write
(
b
"
X
"
*
1024
)
            
with
self
.
assertRaises
(
IOError
)
as
exc
:
                
with
open
(
TESTFN
"
wb
"
)
as
f
:
                    
f
.
write
(
b
"
X
"
*
1025
)
            
self
.
assertEqual
(
exc
.
exception
.
errno
if
PY3
else
exc
.
exception
[
0
]
                             
errno
.
EFBIG
)
        
finally
:
            
p
.
rlimit
(
psutil
.
RLIMIT_FSIZE
(
soft
hard
)
)
            
self
.
assertEqual
(
p
.
rlimit
(
psutil
.
RLIMIT_FSIZE
)
(
soft
hard
)
)
    
unittest
.
skipIf
(
not
HAS_RLIMIT
"
not
supported
"
)
    
def
test_rlimit_infinity
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
soft
hard
=
p
.
rlimit
(
psutil
.
RLIMIT_FSIZE
)
        
try
:
            
p
.
rlimit
(
psutil
.
RLIMIT_FSIZE
(
1024
hard
)
)
            
p
.
rlimit
(
psutil
.
RLIMIT_FSIZE
(
psutil
.
RLIM_INFINITY
hard
)
)
            
with
open
(
TESTFN
"
wb
"
)
as
f
:
                
f
.
write
(
b
"
X
"
*
2048
)
        
finally
:
            
p
.
rlimit
(
psutil
.
RLIMIT_FSIZE
(
soft
hard
)
)
            
self
.
assertEqual
(
p
.
rlimit
(
psutil
.
RLIMIT_FSIZE
)
(
soft
hard
)
)
    
unittest
.
skipIf
(
not
HAS_RLIMIT
"
not
supported
"
)
    
def
test_rlimit_infinity_value
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
soft
hard
=
p
.
rlimit
(
psutil
.
RLIMIT_FSIZE
)
        
self
.
assertEqual
(
psutil
.
RLIM_INFINITY
hard
)
        
p
.
rlimit
(
psutil
.
RLIMIT_FSIZE
(
soft
hard
)
)
    
def
test_num_threads
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
if
OPENBSD
:
            
try
:
                
step1
=
p
.
num_threads
(
)
            
except
psutil
.
AccessDenied
:
                
raise
unittest
.
SkipTest
(
"
on
OpenBSD
this
requires
root
access
"
)
        
else
:
            
step1
=
p
.
num_threads
(
)
        
with
ThreadTask
(
)
:
            
step2
=
p
.
num_threads
(
)
            
self
.
assertEqual
(
step2
step1
+
1
)
    
unittest
.
skipIf
(
not
WINDOWS
'
WINDOWS
only
'
)
    
def
test_num_handles
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
self
.
assertGreater
(
p
.
num_handles
(
)
0
)
    
unittest
.
skipIf
(
not
HAS_THREADS
'
not
supported
'
)
    
def
test_threads
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
if
OPENBSD
:
            
try
:
                
step1
=
p
.
threads
(
)
            
except
psutil
.
AccessDenied
:
                
raise
unittest
.
SkipTest
(
"
on
OpenBSD
this
requires
root
access
"
)
        
else
:
            
step1
=
p
.
threads
(
)
        
with
ThreadTask
(
)
:
            
step2
=
p
.
threads
(
)
            
self
.
assertEqual
(
len
(
step2
)
len
(
step1
)
+
1
)
            
if
LINUX
:
                
self
.
assertEqual
(
step2
[
0
]
.
id
os
.
getpid
(
)
)
            
athread
=
step2
[
0
]
            
self
.
assertEqual
(
athread
.
id
athread
[
0
]
)
            
self
.
assertEqual
(
athread
.
user_time
athread
[
1
]
)
            
self
.
assertEqual
(
athread
.
system_time
athread
[
2
]
)
    
retry_before_failing
(
)
    
skip_on_access_denied
(
only_if
=
OSX
)
    
unittest
.
skipIf
(
not
HAS_THREADS
'
not
supported
'
)
    
def
test_threads_2
(
self
)
:
        
sproc
=
get_test_subprocess
(
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
if
OPENBSD
:
            
try
:
                
p
.
threads
(
)
            
except
psutil
.
AccessDenied
:
                
raise
unittest
.
SkipTest
(
                    
"
on
OpenBSD
this
requires
root
access
"
)
        
self
.
assertAlmostEqual
(
            
p
.
cpu_times
(
)
.
user
            
sum
(
[
x
.
user_time
for
x
in
p
.
threads
(
)
]
)
delta
=
0
.
1
)
        
self
.
assertAlmostEqual
(
            
p
.
cpu_times
(
)
.
system
            
sum
(
[
x
.
system_time
for
x
in
p
.
threads
(
)
]
)
delta
=
0
.
1
)
    
def
test_memory_info
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
rss1
vms1
=
p
.
memory_info
(
)
[
:
2
]
        
percent1
=
p
.
memory_percent
(
)
        
self
.
assertGreater
(
rss1
0
)
        
self
.
assertGreater
(
vms1
0
)
        
memarr
=
[
None
]
*
1500000
        
rss2
vms2
=
p
.
memory_info
(
)
[
:
2
]
        
percent2
=
p
.
memory_percent
(
)
        
self
.
assertGreater
(
rss2
rss1
)
        
self
.
assertGreaterEqual
(
vms2
vms1
)
        
self
.
assertGreater
(
percent2
percent1
)
        
del
memarr
        
if
WINDOWS
:
            
mem
=
p
.
memory_info
(
)
            
self
.
assertEqual
(
mem
.
rss
mem
.
wset
)
            
self
.
assertEqual
(
mem
.
vms
mem
.
pagefile
)
        
mem
=
p
.
memory_info
(
)
        
for
name
in
mem
.
_fields
:
            
self
.
assertGreaterEqual
(
getattr
(
mem
name
)
0
)
    
def
test_memory_full_info
(
self
)
:
        
total
=
psutil
.
virtual_memory
(
)
.
total
        
mem
=
psutil
.
Process
(
)
.
memory_full_info
(
)
        
for
name
in
mem
.
_fields
:
            
value
=
getattr
(
mem
name
)
            
self
.
assertGreaterEqual
(
value
0
msg
=
(
name
value
)
)
            
self
.
assertLessEqual
(
value
total
msg
=
(
name
value
total
)
)
        
if
LINUX
or
WINDOWS
or
OSX
:
            
self
.
assertGreaterEqual
(
mem
.
uss
0
)
        
if
LINUX
:
            
self
.
assertGreaterEqual
(
mem
.
pss
0
)
            
self
.
assertGreaterEqual
(
mem
.
swap
0
)
    
unittest
.
skipIf
(
not
HAS_MEMORY_MAPS
"
not
supported
"
)
    
def
test_memory_maps
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
maps
=
p
.
memory_maps
(
)
        
paths
=
[
x
for
x
in
maps
]
        
self
.
assertEqual
(
len
(
paths
)
len
(
set
(
paths
)
)
)
        
ext_maps
=
p
.
memory_maps
(
grouped
=
False
)
        
for
nt
in
maps
:
            
if
not
nt
.
path
.
startswith
(
'
[
'
)
:
                
assert
os
.
path
.
isabs
(
nt
.
path
)
nt
.
path
                
if
POSIX
:
                    
try
:
                        
assert
os
.
path
.
exists
(
nt
.
path
)
or
\
                            
os
.
path
.
islink
(
nt
.
path
)
nt
.
path
                    
except
AssertionError
:
                        
if
not
LINUX
:
                            
raise
                        
else
:
                            
with
open
(
'
/
proc
/
self
/
smaps
'
)
as
f
:
                                
data
=
f
.
read
(
)
                            
if
"
%
s
(
deleted
)
"
%
nt
.
path
not
in
data
:
                                
raise
                
else
:
                    
if
'
64
'
not
in
os
.
path
.
basename
(
nt
.
path
)
:
                        
assert
os
.
path
.
exists
(
nt
.
path
)
nt
.
path
        
for
nt
in
ext_maps
:
            
for
fname
in
nt
.
_fields
:
                
value
=
getattr
(
nt
fname
)
                
if
fname
=
=
'
path
'
:
                    
continue
                
elif
fname
in
(
'
addr
'
'
perms
'
)
:
                    
assert
value
value
                
else
:
                    
self
.
assertIsInstance
(
value
(
int
long
)
)
                    
assert
value
>
=
0
value
    
unittest
.
skipIf
(
not
HAS_MEMORY_MAPS
"
not
supported
"
)
    
def
test_memory_maps_lists_lib
(
self
)
:
        
with
copyload_shared_lib
(
)
as
path
:
            
def
normpath
(
p
)
:
                
return
os
.
path
.
realpath
(
os
.
path
.
normcase
(
p
)
)
            
libpaths
=
[
normpath
(
x
.
path
)
                        
for
x
in
psutil
.
Process
(
)
.
memory_maps
(
)
]
            
self
.
assertIn
(
normpath
(
path
)
libpaths
)
    
def
test_memory_percent
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
ret
=
p
.
memory_percent
(
)
        
assert
0
<
=
ret
<
=
100
ret
        
ret
=
p
.
memory_percent
(
memtype
=
'
vms
'
)
        
assert
0
<
=
ret
<
=
100
ret
        
assert
0
<
=
ret
<
=
100
ret
        
self
.
assertRaises
(
ValueError
p
.
memory_percent
memtype
=
"
?
!
?
"
)
        
if
LINUX
or
OSX
or
WINDOWS
:
            
ret
=
p
.
memory_percent
(
memtype
=
'
uss
'
)
            
assert
0
<
=
ret
<
=
100
ret
            
assert
0
<
=
ret
<
=
100
ret
    
def
test_is_running
(
self
)
:
        
sproc
=
get_test_subprocess
(
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
assert
p
.
is_running
(
)
        
assert
p
.
is_running
(
)
        
p
.
kill
(
)
        
p
.
wait
(
)
        
assert
not
p
.
is_running
(
)
        
assert
not
p
.
is_running
(
)
    
def
test_exe
(
self
)
:
        
sproc
=
get_test_subprocess
(
)
        
exe
=
psutil
.
Process
(
sproc
.
pid
)
.
exe
(
)
        
try
:
            
self
.
assertEqual
(
exe
PYTHON_EXE
)
        
except
AssertionError
:
            
if
WINDOWS
and
len
(
exe
)
=
=
len
(
PYTHON_EXE
)
:
                
normcase
=
os
.
path
.
normcase
                
self
.
assertEqual
(
normcase
(
exe
)
normcase
(
PYTHON_EXE
)
)
            
else
:
                
ver
=
"
%
s
.
%
s
"
%
(
sys
.
version_info
[
0
]
sys
.
version_info
[
1
]
)
                
try
:
                    
self
.
assertEqual
(
exe
.
replace
(
ver
'
'
)
                                     
PYTHON_EXE
.
replace
(
ver
'
'
)
)
                
except
AssertionError
:
                    
pass
        
out
=
sh
(
[
exe
"
-
c
"
"
import
os
;
print
(
'
hey
'
)
"
]
)
        
self
.
assertEqual
(
out
'
hey
'
)
    
def
test_cmdline
(
self
)
:
        
cmdline
=
[
PYTHON_EXE
"
-
c
"
"
import
time
;
time
.
sleep
(
60
)
"
]
        
sproc
=
get_test_subprocess
(
cmdline
)
        
try
:
            
self
.
assertEqual
(
'
'
.
join
(
psutil
.
Process
(
sproc
.
pid
)
.
cmdline
(
)
)
                             
'
'
.
join
(
cmdline
)
)
        
except
AssertionError
:
            
if
NETBSD
or
OPENBSD
or
AIX
:
                
self
.
assertEqual
(
                    
psutil
.
Process
(
sproc
.
pid
)
.
cmdline
(
)
[
0
]
PYTHON_EXE
)
            
else
:
                
raise
    
def
test_name
(
self
)
:
        
sproc
=
get_test_subprocess
(
PYTHON_EXE
)
        
name
=
psutil
.
Process
(
sproc
.
pid
)
.
name
(
)
.
lower
(
)
        
pyexe
=
os
.
path
.
basename
(
os
.
path
.
realpath
(
sys
.
executable
)
)
.
lower
(
)
        
assert
pyexe
.
startswith
(
name
)
(
pyexe
name
)
    
unittest
.
skipIf
(
SUNOS
"
broken
on
SUNOS
"
)
    
unittest
.
skipIf
(
AIX
"
broken
on
AIX
"
)
    
def
test_prog_w_funky_name
(
self
)
:
        
def
rm
(
)
:
            
try
:
                
safe_rmpath
(
funky_path
)
            
except
OSError
:
                
pass
        
funky_path
=
TESTFN
+
'
foo
bar
)
'
        
create_exe
(
funky_path
)
        
self
.
addCleanup
(
rm
)
        
cmdline
=
[
funky_path
"
-
c
"
                   
"
import
time
;
[
time
.
sleep
(
0
.
01
)
for
x
in
range
(
3000
)
]
;
"
                   
"
arg1
"
"
arg2
"
"
"
"
arg3
"
"
"
]
        
sproc
=
get_test_subprocess
(
cmdline
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
if
TRAVIS
:
            
wait_for_pid
(
p
.
pid
)
        
self
.
assertEqual
(
p
.
cmdline
(
)
cmdline
)
        
self
.
assertEqual
(
p
.
name
(
)
os
.
path
.
basename
(
funky_path
)
)
        
self
.
assertEqual
(
os
.
path
.
normcase
(
p
.
exe
(
)
)
                         
os
.
path
.
normcase
(
funky_path
)
)
    
unittest
.
skipIf
(
not
POSIX
'
POSIX
only
'
)
    
def
test_uids
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
real
effective
saved
=
p
.
uids
(
)
        
self
.
assertEqual
(
real
os
.
getuid
(
)
)
        
self
.
assertEqual
(
effective
os
.
geteuid
(
)
)
        
if
hasattr
(
os
"
getresuid
"
)
:
            
self
.
assertEqual
(
os
.
getresuid
(
)
p
.
uids
(
)
)
    
unittest
.
skipIf
(
not
POSIX
'
POSIX
only
'
)
    
def
test_gids
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
real
effective
saved
=
p
.
gids
(
)
        
self
.
assertEqual
(
real
os
.
getgid
(
)
)
        
self
.
assertEqual
(
effective
os
.
getegid
(
)
)
        
if
hasattr
(
os
"
getresuid
"
)
:
            
self
.
assertEqual
(
os
.
getresgid
(
)
p
.
gids
(
)
)
    
def
test_nice
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
self
.
assertRaises
(
TypeError
p
.
nice
"
str
"
)
        
if
WINDOWS
:
            
try
:
                
init
=
p
.
nice
(
)
                
if
sys
.
version_info
>
(
3
4
)
:
                    
self
.
assertIsInstance
(
init
enum
.
IntEnum
)
                
else
:
                    
self
.
assertIsInstance
(
init
int
)
                
self
.
assertEqual
(
init
psutil
.
NORMAL_PRIORITY_CLASS
)
                
p
.
nice
(
psutil
.
HIGH_PRIORITY_CLASS
)
                
self
.
assertEqual
(
p
.
nice
(
)
psutil
.
HIGH_PRIORITY_CLASS
)
                
p
.
nice
(
psutil
.
NORMAL_PRIORITY_CLASS
)
                
self
.
assertEqual
(
p
.
nice
(
)
psutil
.
NORMAL_PRIORITY_CLASS
)
            
finally
:
                
p
.
nice
(
psutil
.
NORMAL_PRIORITY_CLASS
)
        
else
:
            
first_nice
=
p
.
nice
(
)
            
try
:
                
if
hasattr
(
os
"
getpriority
"
)
:
                    
self
.
assertEqual
(
                        
os
.
getpriority
(
os
.
PRIO_PROCESS
os
.
getpid
(
)
)
p
.
nice
(
)
)
                
p
.
nice
(
1
)
                
self
.
assertEqual
(
p
.
nice
(
)
1
)
                
if
hasattr
(
os
"
getpriority
"
)
:
                    
self
.
assertEqual
(
                        
os
.
getpriority
(
os
.
PRIO_PROCESS
os
.
getpid
(
)
)
p
.
nice
(
)
)
                
if
not
OSX
:
                    
p
.
nice
(
0
)
                    
self
.
assertEqual
(
p
.
nice
(
)
0
)
            
except
psutil
.
AccessDenied
:
                
pass
            
finally
:
                
try
:
                    
p
.
nice
(
first_nice
)
                
except
psutil
.
AccessDenied
:
                    
pass
    
def
test_status
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
self
.
assertEqual
(
p
.
status
(
)
psutil
.
STATUS_RUNNING
)
    
def
test_username
(
self
)
:
        
sproc
=
get_test_subprocess
(
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
username
=
p
.
username
(
)
        
if
WINDOWS
:
            
domain
username
=
username
.
split
(
'
\
\
'
)
            
self
.
assertEqual
(
username
getpass
.
getuser
(
)
)
            
if
'
USERDOMAIN
'
in
os
.
environ
:
                
self
.
assertEqual
(
domain
os
.
environ
[
'
USERDOMAIN
'
]
)
        
else
:
            
self
.
assertEqual
(
username
getpass
.
getuser
(
)
)
    
def
test_cwd
(
self
)
:
        
sproc
=
get_test_subprocess
(
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
self
.
assertEqual
(
p
.
cwd
(
)
os
.
getcwd
(
)
)
    
def
test_cwd_2
(
self
)
:
        
cmd
=
[
PYTHON_EXE
"
-
c
"
               
"
import
os
time
;
os
.
chdir
(
'
.
.
'
)
;
time
.
sleep
(
60
)
"
]
        
sproc
=
get_test_subprocess
(
cmd
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
call_until
(
p
.
cwd
"
ret
=
=
os
.
path
.
dirname
(
os
.
getcwd
(
)
)
"
)
    
unittest
.
skipIf
(
not
HAS_CPU_AFFINITY
'
not
supported
'
)
    
def
test_cpu_affinity
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
initial
=
p
.
cpu_affinity
(
)
        
assert
initial
initial
        
self
.
addCleanup
(
p
.
cpu_affinity
initial
)
        
if
hasattr
(
os
"
sched_getaffinity
"
)
:
            
self
.
assertEqual
(
initial
list
(
os
.
sched_getaffinity
(
p
.
pid
)
)
)
        
self
.
assertEqual
(
len
(
initial
)
len
(
set
(
initial
)
)
)
        
all_cpus
=
list
(
range
(
len
(
psutil
.
cpu_percent
(
percpu
=
True
)
)
)
)
        
for
n
in
all_cpus
if
not
TRAVIS
else
initial
:
            
p
.
cpu_affinity
(
[
n
]
)
            
self
.
assertEqual
(
p
.
cpu_affinity
(
)
[
n
]
)
            
if
hasattr
(
os
"
sched_getaffinity
"
)
:
                
self
.
assertEqual
(
p
.
cpu_affinity
(
)
                                 
list
(
os
.
sched_getaffinity
(
p
.
pid
)
)
)
            
if
hasattr
(
p
"
num_cpu
"
)
:
                
self
.
assertEqual
(
p
.
cpu_affinity
(
)
[
0
]
p
.
num_cpu
(
)
)
        
p
.
cpu_affinity
(
[
]
)
        
if
LINUX
:
            
self
.
assertEqual
(
p
.
cpu_affinity
(
)
p
.
_proc
.
_get_eligible_cpus
(
)
)
        
else
:
            
self
.
assertEqual
(
p
.
cpu_affinity
(
)
all_cpus
)
        
if
hasattr
(
os
"
sched_getaffinity
"
)
:
            
self
.
assertEqual
(
p
.
cpu_affinity
(
)
                             
list
(
os
.
sched_getaffinity
(
p
.
pid
)
)
)
        
self
.
assertRaises
(
TypeError
p
.
cpu_affinity
1
)
        
p
.
cpu_affinity
(
initial
)
        
p
.
cpu_affinity
(
set
(
all_cpus
)
)
        
p
.
cpu_affinity
(
tuple
(
all_cpus
)
)
    
unittest
.
skipIf
(
not
HAS_CPU_AFFINITY
'
not
supported
'
)
    
def
test_cpu_affinity_errs
(
self
)
:
        
sproc
=
get_test_subprocess
(
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
invalid_cpu
=
[
len
(
psutil
.
cpu_times
(
percpu
=
True
)
)
+
10
]
        
self
.
assertRaises
(
ValueError
p
.
cpu_affinity
invalid_cpu
)
        
self
.
assertRaises
(
ValueError
p
.
cpu_affinity
range
(
10000
11000
)
)
        
self
.
assertRaises
(
TypeError
p
.
cpu_affinity
[
0
"
1
"
]
)
        
self
.
assertRaises
(
ValueError
p
.
cpu_affinity
[
0
-
1
]
)
    
unittest
.
skipIf
(
not
HAS_CPU_AFFINITY
'
not
supported
'
)
    
def
test_cpu_affinity_all_combinations
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
initial
=
p
.
cpu_affinity
(
)
        
assert
initial
initial
        
self
.
addCleanup
(
p
.
cpu_affinity
initial
)
        
combos
=
[
]
        
for
l
in
range
(
0
len
(
initial
)
+
1
)
:
            
for
subset
in
itertools
.
combinations
(
initial
l
)
:
                
if
subset
:
                    
combos
.
append
(
list
(
subset
)
)
        
for
combo
in
combos
:
            
p
.
cpu_affinity
(
combo
)
            
self
.
assertEqual
(
p
.
cpu_affinity
(
)
combo
)
    
unittest
.
skipIf
(
BSD
"
broken
on
BSD
"
)
    
unittest
.
skipIf
(
APPVEYOR
"
unreliable
on
APPVEYOR
"
)
    
def
test_open_files
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
files
=
p
.
open_files
(
)
        
self
.
assertFalse
(
TESTFN
in
files
)
        
with
open
(
TESTFN
'
wb
'
)
as
f
:
            
f
.
write
(
b
'
x
'
*
1024
)
            
f
.
flush
(
)
            
files
=
call_until
(
p
.
open_files
"
len
(
ret
)
!
=
%
i
"
%
len
(
files
)
)
            
for
file
in
files
:
                
if
file
.
path
=
=
TESTFN
:
                    
if
LINUX
:
                        
self
.
assertEqual
(
file
.
position
1024
)
                    
break
            
else
:
                
self
.
fail
(
"
no
file
found
;
files
=
%
s
"
%
repr
(
files
)
)
        
for
file
in
files
:
            
assert
os
.
path
.
isfile
(
file
.
path
)
file
        
cmdline
=
"
import
time
;
f
=
open
(
r
'
%
s
'
'
r
'
)
;
time
.
sleep
(
60
)
;
"
%
TESTFN
        
sproc
=
get_test_subprocess
(
[
PYTHON_EXE
"
-
c
"
cmdline
]
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
for
x
in
range
(
100
)
:
            
filenames
=
[
x
.
path
for
x
in
p
.
open_files
(
)
]
            
if
TESTFN
in
filenames
:
                
break
            
time
.
sleep
(
.
01
)
        
else
:
            
self
.
assertIn
(
TESTFN
filenames
)
        
for
file
in
filenames
:
            
assert
os
.
path
.
isfile
(
file
)
file
    
unittest
.
skipIf
(
BSD
"
broken
on
BSD
"
)
    
unittest
.
skipIf
(
APPVEYOR
"
unreliable
on
APPVEYOR
"
)
    
def
test_open_files_2
(
self
)
:
        
with
open
(
TESTFN
'
w
'
)
as
fileobj
:
            
p
=
psutil
.
Process
(
)
            
for
file
in
p
.
open_files
(
)
:
                
if
file
.
path
=
=
fileobj
.
name
or
file
.
fd
=
=
fileobj
.
fileno
(
)
:
                    
break
            
else
:
                
self
.
fail
(
"
no
file
found
;
files
=
%
s
"
%
repr
(
p
.
open_files
(
)
)
)
            
self
.
assertEqual
(
file
.
path
fileobj
.
name
)
            
if
WINDOWS
:
                
self
.
assertEqual
(
file
.
fd
-
1
)
            
else
:
                
self
.
assertEqual
(
file
.
fd
fileobj
.
fileno
(
)
)
            
ntuple
=
p
.
open_files
(
)
[
0
]
            
self
.
assertEqual
(
ntuple
[
0
]
ntuple
.
path
)
            
self
.
assertEqual
(
ntuple
[
1
]
ntuple
.
fd
)
            
self
.
assertNotIn
(
fileobj
.
name
p
.
open_files
(
)
)
    
unittest
.
skipIf
(
not
POSIX
'
POSIX
only
'
)
    
def
test_num_fds
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
start
=
p
.
num_fds
(
)
        
file
=
open
(
TESTFN
'
w
'
)
        
self
.
addCleanup
(
file
.
close
)
        
self
.
assertEqual
(
p
.
num_fds
(
)
start
+
1
)
        
sock
=
socket
.
socket
(
)
        
self
.
addCleanup
(
sock
.
close
)
        
self
.
assertEqual
(
p
.
num_fds
(
)
start
+
2
)
        
file
.
close
(
)
        
sock
.
close
(
)
        
self
.
assertEqual
(
p
.
num_fds
(
)
start
)
    
skip_on_not_implemented
(
only_if
=
LINUX
)
    
unittest
.
skipIf
(
OPENBSD
or
NETBSD
"
not
reliable
on
OPENBSD
&
NETBSD
"
)
    
def
test_num_ctx_switches
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
before
=
sum
(
p
.
num_ctx_switches
(
)
)
        
for
x
in
range
(
500000
)
:
            
after
=
sum
(
p
.
num_ctx_switches
(
)
)
            
if
after
>
before
:
                
return
        
self
.
fail
(
"
num
ctx
switches
still
the
same
after
50
.
000
iterations
"
)
    
def
test_ppid
(
self
)
:
        
if
hasattr
(
os
'
getppid
'
)
:
            
self
.
assertEqual
(
psutil
.
Process
(
)
.
ppid
(
)
os
.
getppid
(
)
)
        
this_parent
=
os
.
getpid
(
)
        
sproc
=
get_test_subprocess
(
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
self
.
assertEqual
(
p
.
ppid
(
)
this_parent
)
        
reap_children
(
recursive
=
True
)
        
if
APPVEYOR
:
            
return
        
for
p
in
psutil
.
process_iter
(
)
:
            
if
p
.
pid
=
=
sproc
.
pid
:
                
continue
            
self
.
assertNotEqual
(
p
.
ppid
(
)
this_parent
msg
=
p
)
    
def
test_parent
(
self
)
:
        
this_parent
=
os
.
getpid
(
)
        
sproc
=
get_test_subprocess
(
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
self
.
assertEqual
(
p
.
parent
(
)
.
pid
this_parent
)
    
def
test_parent_disappeared
(
self
)
:
        
sproc
=
get_test_subprocess
(
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
with
mock
.
patch
(
"
psutil
.
Process
"
                        
side_effect
=
psutil
.
NoSuchProcess
(
0
'
foo
'
)
)
:
            
self
.
assertIsNone
(
p
.
parent
(
)
)
    
def
test_children
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
self
.
assertEqual
(
p
.
children
(
)
[
]
)
        
self
.
assertEqual
(
p
.
children
(
recursive
=
True
)
[
]
)
        
sproc
=
get_test_subprocess
(
creationflags
=
0
)
        
children1
=
p
.
children
(
)
        
children2
=
p
.
children
(
recursive
=
True
)
        
for
children
in
(
children1
children2
)
:
            
self
.
assertEqual
(
len
(
children
)
1
)
            
self
.
assertEqual
(
children
[
0
]
.
pid
sproc
.
pid
)
            
self
.
assertEqual
(
children
[
0
]
.
ppid
(
)
os
.
getpid
(
)
)
    
def
test_children_recursive
(
self
)
:
        
p1
p2
=
create_proc_children_pair
(
)
        
p
=
psutil
.
Process
(
)
        
self
.
assertEqual
(
p
.
children
(
)
[
p1
]
)
        
self
.
assertEqual
(
p
.
children
(
recursive
=
True
)
[
p1
p2
]
)
        
p1
.
terminate
(
)
        
p1
.
wait
(
)
        
self
.
assertEqual
(
p
.
children
(
recursive
=
True
)
[
]
)
    
def
test_children_duplicates
(
self
)
:
        
table
=
collections
.
defaultdict
(
int
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
            
try
:
                
table
[
p
.
ppid
(
)
]
+
=
1
            
except
psutil
.
Error
:
                
pass
        
pid
=
sorted
(
table
.
items
(
)
key
=
lambda
x
:
x
[
1
]
)
[
-
1
]
[
0
]
        
p
=
psutil
.
Process
(
pid
)
        
try
:
            
c
=
p
.
children
(
recursive
=
True
)
        
except
psutil
.
AccessDenied
:
            
pass
        
else
:
            
self
.
assertEqual
(
len
(
c
)
len
(
set
(
c
)
)
)
    
def
test_suspend_resume
(
self
)
:
        
sproc
=
get_test_subprocess
(
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
p
.
suspend
(
)
        
for
x
in
range
(
100
)
:
            
if
p
.
status
(
)
=
=
psutil
.
STATUS_STOPPED
:
                
break
            
time
.
sleep
(
0
.
01
)
        
p
.
resume
(
)
        
self
.
assertNotEqual
(
p
.
status
(
)
psutil
.
STATUS_STOPPED
)
    
def
test_invalid_pid
(
self
)
:
        
self
.
assertRaises
(
TypeError
psutil
.
Process
"
1
"
)
        
self
.
assertRaises
(
ValueError
psutil
.
Process
-
1
)
    
def
test_as_dict
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
d
=
p
.
as_dict
(
attrs
=
[
'
exe
'
'
name
'
]
)
        
self
.
assertEqual
(
sorted
(
d
.
keys
(
)
)
[
'
exe
'
'
name
'
]
)
        
p
=
psutil
.
Process
(
min
(
psutil
.
pids
(
)
)
)
        
d
=
p
.
as_dict
(
attrs
=
[
'
connections
'
]
ad_value
=
'
foo
'
)
        
if
not
isinstance
(
d
[
'
connections
'
]
list
)
:
            
self
.
assertEqual
(
d
[
'
connections
'
]
'
foo
'
)
        
with
mock
.
patch
(
'
psutil
.
Process
.
nice
'
create
=
True
                        
side_effect
=
psutil
.
AccessDenied
)
:
            
self
.
assertEqual
(
                
p
.
as_dict
(
attrs
=
[
"
nice
"
]
ad_value
=
1
)
{
"
nice
"
:
1
}
)
        
with
mock
.
patch
(
'
psutil
.
Process
.
nice
'
create
=
True
                        
side_effect
=
psutil
.
NoSuchProcess
(
p
.
pid
"
name
"
)
)
:
            
self
.
assertRaises
(
                
psutil
.
NoSuchProcess
p
.
as_dict
attrs
=
[
"
nice
"
]
)
        
with
mock
.
patch
(
'
psutil
.
Process
.
nice
'
create
=
True
                        
side_effect
=
psutil
.
ZombieProcess
(
p
.
pid
"
name
"
)
)
:
            
self
.
assertEqual
(
                
p
.
as_dict
(
attrs
=
[
"
nice
"
]
ad_value
=
"
foo
"
)
{
"
nice
"
:
"
foo
"
}
)
        
with
mock
.
patch
(
'
psutil
.
Process
.
nice
'
create
=
True
                        
side_effect
=
NotImplementedError
)
:
            
d
=
p
.
as_dict
(
)
            
self
.
assertNotIn
(
'
nice
'
list
(
d
.
keys
(
)
)
)
            
with
self
.
assertRaises
(
NotImplementedError
)
:
                
p
.
as_dict
(
attrs
=
[
"
nice
"
]
)
        
with
self
.
assertRaises
(
TypeError
)
:
            
p
.
as_dict
(
'
name
'
)
        
with
self
.
assertRaises
(
ValueError
)
:
            
p
.
as_dict
(
[
'
foo
'
]
)
        
with
self
.
assertRaises
(
ValueError
)
:
            
p
.
as_dict
(
[
'
foo
'
'
bar
'
]
)
    
def
test_oneshot
(
self
)
:
        
with
mock
.
patch
(
"
psutil
.
_psplatform
.
Process
.
cpu_times
"
)
as
m
:
            
p
=
psutil
.
Process
(
)
            
with
p
.
oneshot
(
)
:
                
p
.
cpu_times
(
)
                
p
.
cpu_times
(
)
            
self
.
assertEqual
(
m
.
call_count
1
)
        
with
mock
.
patch
(
"
psutil
.
_psplatform
.
Process
.
cpu_times
"
)
as
m
:
            
p
.
cpu_times
(
)
            
p
.
cpu_times
(
)
        
self
.
assertEqual
(
m
.
call_count
2
)
    
def
test_oneshot_twice
(
self
)
:
        
with
mock
.
patch
(
"
psutil
.
_psplatform
.
Process
.
cpu_times
"
)
as
m1
:
            
with
mock
.
patch
(
"
psutil
.
_psplatform
.
Process
.
oneshot_enter
"
)
as
m2
:
                
p
=
psutil
.
Process
(
)
                
with
p
.
oneshot
(
)
:
                    
p
.
cpu_times
(
)
                    
p
.
cpu_times
(
)
                    
with
p
.
oneshot
(
)
:
                        
p
.
cpu_times
(
)
                        
p
.
cpu_times
(
)
                
self
.
assertEqual
(
m1
.
call_count
1
)
                
self
.
assertEqual
(
m2
.
call_count
1
)
        
with
mock
.
patch
(
"
psutil
.
_psplatform
.
Process
.
cpu_times
"
)
as
m
:
            
p
.
cpu_times
(
)
            
p
.
cpu_times
(
)
        
self
.
assertEqual
(
m
.
call_count
2
)
    
def
test_halfway_terminated_process
(
self
)
:
        
sproc
=
get_test_subprocess
(
)
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
p
.
terminate
(
)
        
p
.
wait
(
)
        
if
WINDOWS
:
            
call_until
(
psutil
.
pids
"
%
s
not
in
ret
"
%
p
.
pid
)
        
self
.
assertFalse
(
p
.
is_running
(
)
)
        
excluded_names
=
[
'
pid
'
'
is_running
'
'
wait
'
'
create_time
'
                          
'
oneshot
'
'
memory_info_ex
'
]
        
if
LINUX
and
not
HAS_RLIMIT
:
            
excluded_names
.
append
(
'
rlimit
'
)
        
for
name
in
dir
(
p
)
:
            
if
(
name
.
startswith
(
'
_
'
)
or
                    
name
in
excluded_names
)
:
                
continue
            
try
:
                
meth
=
getattr
(
p
name
)
                
if
name
=
=
'
nice
'
:
                    
if
POSIX
:
                        
ret
=
meth
(
1
)
                    
else
:
                        
ret
=
meth
(
psutil
.
NORMAL_PRIORITY_CLASS
)
                
elif
name
=
=
'
ionice
'
:
                    
ret
=
meth
(
)
                    
ret
=
meth
(
2
)
                
elif
name
=
=
'
rlimit
'
:
                    
ret
=
meth
(
psutil
.
RLIMIT_NOFILE
)
                    
ret
=
meth
(
psutil
.
RLIMIT_NOFILE
(
5
5
)
)
                
elif
name
=
=
'
cpu_affinity
'
:
                    
ret
=
meth
(
)
                    
ret
=
meth
(
[
0
]
)
                
elif
name
=
=
'
send_signal
'
:
                    
ret
=
meth
(
signal
.
SIGTERM
)
                
else
:
                    
ret
=
meth
(
)
            
except
psutil
.
ZombieProcess
:
                
self
.
fail
(
"
ZombieProcess
for
%
r
was
not
supposed
to
happen
"
%
                          
name
)
            
except
psutil
.
NoSuchProcess
:
                
pass
            
except
psutil
.
AccessDenied
:
                
if
OPENBSD
and
name
in
(
'
threads
'
'
num_threads
'
)
:
                    
pass
                
else
:
                    
raise
            
except
NotImplementedError
:
                
pass
            
else
:
                
self
.
fail
(
                    
"
NoSuchProcess
exception
not
raised
for
%
r
retval
=
%
s
"
%
(
                        
name
ret
)
)
    
unittest
.
skipIf
(
not
POSIX
'
POSIX
only
'
)
    
def
test_zombie_process
(
self
)
:
        
def
succeed_or_zombie_p_exc
(
fun
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
*
args
*
*
kwargs
)
            
except
(
psutil
.
ZombieProcess
psutil
.
AccessDenied
)
:
                
pass
        
zpid
=
create_zombie_proc
(
)
        
self
.
addCleanup
(
reap_children
recursive
=
True
)
        
zproc
=
psutil
.
Process
(
zpid
)
        
self
.
assertEqual
(
zproc
.
status
(
)
psutil
.
STATUS_ZOMBIE
)
        
self
.
assertTrue
(
zproc
.
is_running
(
)
)
        
zproc
.
as_dict
(
)
        
ret
=
succeed_or_zombie_p_exc
(
zproc
.
suspend
)
        
if
ret
is
not
None
:
            
self
.
assertEqual
(
ret
[
]
)
        
if
hasattr
(
zproc
"
rlimit
"
)
:
            
succeed_or_zombie_p_exc
(
zproc
.
rlimit
psutil
.
RLIMIT_NOFILE
)
            
succeed_or_zombie_p_exc
(
zproc
.
rlimit
psutil
.
RLIMIT_NOFILE
                                    
(
5
5
)
)
        
succeed_or_zombie_p_exc
(
zproc
.
parent
)
        
if
hasattr
(
zproc
'
cpu_affinity
'
)
:
            
try
:
                
succeed_or_zombie_p_exc
(
zproc
.
cpu_affinity
[
0
]
)
            
except
ValueError
as
err
:
                
if
TRAVIS
and
LINUX
and
"
not
eligible
"
in
str
(
err
)
:
                    
pass
                
else
:
                    
raise
        
succeed_or_zombie_p_exc
(
zproc
.
nice
0
)
        
if
hasattr
(
zproc
'
ionice
'
)
:
            
if
LINUX
:
                
succeed_or_zombie_p_exc
(
zproc
.
ionice
2
0
)
            
else
:
                
succeed_or_zombie_p_exc
(
zproc
.
ionice
0
)
        
if
hasattr
(
zproc
'
rlimit
'
)
:
            
succeed_or_zombie_p_exc
(
zproc
.
rlimit
                                    
psutil
.
RLIMIT_NOFILE
(
5
5
)
)
        
succeed_or_zombie_p_exc
(
zproc
.
suspend
)
        
succeed_or_zombie_p_exc
(
zproc
.
resume
)
        
succeed_or_zombie_p_exc
(
zproc
.
terminate
)
        
succeed_or_zombie_p_exc
(
zproc
.
kill
)
        
self
.
assertTrue
(
psutil
.
pid_exists
(
zpid
)
)
        
if
not
TRAVIS
and
OSX
:
            
self
.
assertIn
(
zpid
psutil
.
pids
(
)
)
            
self
.
assertIn
(
zpid
[
x
.
pid
for
x
in
psutil
.
process_iter
(
)
]
)
            
psutil
.
_pmap
=
{
}
            
self
.
assertIn
(
zpid
[
x
.
pid
for
x
in
psutil
.
process_iter
(
)
]
)
    
unittest
.
skipIf
(
not
POSIX
'
POSIX
only
'
)
    
def
test_zombie_process_is_running_w_exc
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
with
mock
.
patch
(
"
psutil
.
Process
"
                        
side_effect
=
psutil
.
ZombieProcess
(
0
)
)
as
m
:
            
assert
p
.
is_running
(
)
            
assert
m
.
called
    
unittest
.
skipIf
(
not
POSIX
'
POSIX
only
'
)
    
def
test_zombie_process_status_w_exc
(
self
)
:
        
p
=
psutil
.
Process
(
)
        
with
mock
.
patch
(
"
psutil
.
_psplatform
.
Process
.
status
"
                        
side_effect
=
psutil
.
ZombieProcess
(
0
)
)
as
m
:
            
self
.
assertEqual
(
p
.
status
(
)
psutil
.
STATUS_ZOMBIE
)
            
assert
m
.
called
    
def
test_pid_0
(
self
)
:
        
if
0
not
in
psutil
.
pids
(
)
:
            
self
.
assertRaises
(
psutil
.
NoSuchProcess
psutil
.
Process
0
)
            
return
        
p
=
psutil
.
Process
(
0
)
        
for
name
in
psutil
.
_as_dict_attrnames
:
            
if
name
=
=
'
pid
'
:
                
continue
            
meth
=
getattr
(
p
name
)
            
try
:
                
ret
=
meth
(
)
            
except
psutil
.
AccessDenied
:
                
pass
            
else
:
                
if
name
in
(
"
uids
"
"
gids
"
)
:
                    
self
.
assertEqual
(
ret
.
real
0
)
                
elif
name
=
=
"
username
"
:
                    
if
POSIX
:
                        
self
.
assertEqual
(
p
.
username
(
)
'
root
'
)
                    
elif
WINDOWS
:
                        
self
.
assertEqual
(
p
.
username
(
)
'
NT
AUTHORITY
\
\
SYSTEM
'
)
                
elif
name
=
=
"
name
"
:
                    
assert
name
name
        
if
hasattr
(
p
'
rlimit
'
)
:
            
try
:
                
p
.
rlimit
(
psutil
.
RLIMIT_FSIZE
)
            
except
psutil
.
AccessDenied
:
                
pass
        
p
.
as_dict
(
)
        
if
not
OPENBSD
:
            
self
.
assertIn
(
0
psutil
.
pids
(
)
)
            
self
.
assertTrue
(
psutil
.
pid_exists
(
0
)
)
    
unittest
.
skipIf
(
not
HAS_ENVIRON
"
not
supported
"
)
    
def
test_environ
(
self
)
:
        
def
clean_dict
(
d
)
:
            
d
.
pop
(
"
PSUTIL_TESTING
"
None
)
            
d
.
pop
(
"
PLAT
"
None
)
            
d
.
pop
(
"
HOME
"
None
)
            
if
OSX
:
                
d
.
pop
(
"
__CF_USER_TEXT_ENCODING
"
None
)
                
d
.
pop
(
"
VERSIONER_PYTHON_PREFER_32_BIT
"
None
)
                
d
.
pop
(
"
VERSIONER_PYTHON_VERSION
"
None
)
            
return
dict
(
                
[
(
k
.
rstrip
(
"
\
r
\
n
"
)
v
.
rstrip
(
"
\
r
\
n
"
)
)
for
k
v
in
d
.
items
(
)
]
)
        
self
.
maxDiff
=
None
        
p
=
psutil
.
Process
(
)
        
d1
=
clean_dict
(
p
.
environ
(
)
)
        
d2
=
clean_dict
(
os
.
environ
.
copy
(
)
)
        
self
.
assertEqual
(
d1
d2
)
    
unittest
.
skipIf
(
not
HAS_ENVIRON
"
not
supported
"
)
    
unittest
.
skipIf
(
not
POSIX
"
POSIX
only
"
)
    
def
test_weird_environ
(
self
)
:
        
code
=
textwrap
.
dedent
(
"
"
"
            
#
include
<
unistd
.
h
>
            
#
include
<
fcntl
.
h
>
            
char
*
const
argv
[
]
=
{
"
cat
"
0
}
;
            
char
*
const
envp
[
]
=
{
"
A
=
1
"
"
X
"
"
C
=
3
"
0
}
;
            
int
main
(
void
)
{
                
/
*
Close
stderr
on
exec
so
parent
can
wait
for
the
execve
to
                 
*
finish
.
*
/
                
if
(
fcntl
(
2
F_SETFD
FD_CLOEXEC
)
!
=
0
)
                    
return
0
;
                
return
execve
(
"
/
bin
/
cat
"
argv
envp
)
;
            
}
            
"
"
"
)
        
path
=
TESTFN
        
create_exe
(
path
c_code
=
code
)
        
self
.
addCleanup
(
safe_rmpath
path
)
        
sproc
=
get_test_subprocess
(
[
path
]
                                    
stdin
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
        
p
=
psutil
.
Process
(
sproc
.
pid
)
        
wait_for_pid
(
p
.
pid
)
        
self
.
assertTrue
(
p
.
is_running
(
)
)
        
self
.
assertEqual
(
sproc
.
stderr
.
read
(
)
b
"
"
)
        
self
.
assertEqual
(
p
.
environ
(
)
{
"
A
"
:
"
1
"
"
C
"
:
"
3
"
}
)
        
sproc
.
communicate
(
)
        
self
.
assertEqual
(
sproc
.
returncode
0
)
if
POSIX
and
os
.
getuid
(
)
=
=
0
:
    
class
LimitedUserTestCase
(
TestProcess
)
:
        
"
"
"
Repeat
the
previous
tests
by
using
a
limited
user
.
        
Executed
only
on
UNIX
and
only
if
the
user
who
run
the
test
script
        
is
root
.
        
"
"
"
        
if
hasattr
(
os
'
getuid
'
)
:
            
PROCESS_UID
=
os
.
getuid
(
)
            
PROCESS_GID
=
os
.
getgid
(
)
        
def
__init__
(
self
*
args
*
*
kwargs
)
:
            
TestProcess
.
__init__
(
self
*
args
*
*
kwargs
)
            
for
attr
in
[
x
for
x
in
dir
(
self
)
if
x
.
startswith
(
'
test
'
)
]
:
                
meth
=
getattr
(
self
attr
)
                
def
test_
(
self
)
:
                    
try
:
                        
meth
(
)
                    
except
psutil
.
AccessDenied
:
                        
pass
                
setattr
(
self
attr
types
.
MethodType
(
test_
self
)
)
        
def
setUp
(
self
)
:
            
safe_rmpath
(
TESTFN
)
            
TestProcess
.
setUp
(
self
)
            
os
.
setegid
(
1000
)
            
os
.
seteuid
(
1000
)
        
def
tearDown
(
self
)
:
            
os
.
setegid
(
self
.
PROCESS_UID
)
            
os
.
seteuid
(
self
.
PROCESS_GID
)
            
TestProcess
.
tearDown
(
self
)
        
def
test_nice
(
self
)
:
            
try
:
                
psutil
.
Process
(
)
.
nice
(
-
1
)
            
except
psutil
.
AccessDenied
:
                
pass
            
else
:
                
self
.
fail
(
"
exception
not
raised
"
)
        
def
test_zombie_process
(
self
)
:
            
pass
class
TestPopen
(
unittest
.
TestCase
)
:
    
"
"
"
Tests
for
psutil
.
Popen
class
.
"
"
"
    
def
tearDown
(
self
)
:
        
reap_children
(
)
    
def
test_misc
(
self
)
:
        
cmd
=
[
PYTHON_EXE
"
-
c
"
"
import
time
;
time
.
sleep
(
60
)
;
"
]
        
with
psutil
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
as
proc
:
            
proc
.
name
(
)
            
proc
.
cpu_times
(
)
            
proc
.
stdin
            
self
.
assertTrue
(
dir
(
proc
)
)
            
self
.
assertRaises
(
AttributeError
getattr
proc
'
foo
'
)
            
proc
.
terminate
(
)
    
def
test_ctx_manager
(
self
)
:
        
with
psutil
.
Popen
(
[
PYTHON_EXE
"
-
V
"
]
                          
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
                          
stdin
=
subprocess
.
PIPE
)
as
proc
:
            
proc
.
communicate
(
)
        
assert
proc
.
stdout
.
closed
        
assert
proc
.
stderr
.
closed
        
assert
proc
.
stdin
.
closed
        
self
.
assertEqual
(
proc
.
returncode
0
)
    
def
test_kill_terminate
(
self
)
:
        
cmd
=
[
PYTHON_EXE
"
-
c
"
"
import
time
;
time
.
sleep
(
60
)
;
"
]
        
with
psutil
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
as
proc
:
            
proc
.
terminate
(
)
            
proc
.
wait
(
)
            
self
.
assertRaises
(
psutil
.
NoSuchProcess
proc
.
terminate
)
            
self
.
assertRaises
(
psutil
.
NoSuchProcess
proc
.
kill
)
            
self
.
assertRaises
(
psutil
.
NoSuchProcess
proc
.
send_signal
                              
signal
.
SIGTERM
)
            
if
WINDOWS
and
sys
.
version_info
>
=
(
2
7
)
:
                
self
.
assertRaises
(
psutil
.
NoSuchProcess
proc
.
send_signal
                                  
signal
.
CTRL_C_EVENT
)
                
self
.
assertRaises
(
psutil
.
NoSuchProcess
proc
.
send_signal
                                  
signal
.
CTRL_BREAK_EVENT
)
if
__name__
=
=
'
__main__
'
:
    
run_test_module_by_name
(
__file__
)
