import
errno
import
os
import
sys
import
time
from
pathlib
import
Path
class
LockTimeout
(
Exception
)
:
    
"
"
"
Raised
when
a
lock
cannot
be
acquired
within
the
timeout
period
.
"
"
"
    
def
__init__
(
self
lock_file
)
:
        
self
.
lock_file
=
lock_file
        
super
(
)
.
__init__
(
f
"
Timeout
waiting
for
lock
file
:
{
lock_file
}
"
)
def
_is_pid_alive
(
pid
)
:
    
"
"
"
Check
if
a
process
with
the
given
PID
is
still
running
.
"
"
"
    
try
:
        
if
sys
.
platform
=
=
"
win32
"
:
            
import
ctypes
            
PROCESS_QUERY_LIMITED_INFORMATION
=
0x1000
            
handle
=
ctypes
.
windll
.
kernel32
.
OpenProcess
(
                
PROCESS_QUERY_LIMITED_INFORMATION
False
pid
            
)
            
if
handle
:
                
ctypes
.
windll
.
kernel32
.
CloseHandle
(
handle
)
                
return
True
            
return
False
        
else
:
            
os
.
kill
(
pid
0
)
            
return
True
    
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
errno
.
ESRCH
:
            
return
False
        
if
e
.
errno
=
=
errno
.
EPERM
:
            
return
True
        
raise
class
SoftFileLock
:
    
"
"
"
A
simple
cross
-
platform
file
lock
using
exclusive
file
creation
.
"
"
"
    
def
__init__
(
self
lock_file
timeout
=
-
1
)
:
        
self
.
lock_file
=
Path
(
lock_file
)
        
self
.
timeout
=
timeout
        
self
.
_lock_held
=
False
    
def
_is_lock_stale
(
self
)
:
        
"
"
"
Check
if
the
existing
lock
file
is
stale
(
owning
process
no
longer
exists
)
.
"
"
"
        
try
:
            
content
=
self
.
lock_file
.
read_text
(
)
.
strip
(
)
            
if
not
content
:
                
return
True
            
pid
=
int
(
content
)
            
return
not
_is_pid_alive
(
pid
)
        
except
ValueError
:
            
return
True
        
except
OSError
:
            
return
False
    
def
_try_remove_stale_lock
(
self
)
:
        
"
"
"
Attempt
to
remove
a
stale
lock
file
.
Returns
True
if
removed
.
"
"
"
        
if
not
self
.
_is_lock_stale
(
)
:
            
return
False
        
try
:
            
self
.
lock_file
.
unlink
(
)
            
return
True
        
except
OSError
:
            
return
False
    
def
acquire
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
Acquire
the
lock
blocking
until
available
or
timeout
is
reached
.
"
"
"
        
assert
not
self
.
_lock_held
"
acquire
(
)
is
not
reentrant
"
        
if
timeout
is
None
:
            
timeout
=
self
.
timeout
        
start_time
=
time
.
monotonic
(
)
        
poll_interval
=
0
.
1
        
self
.
lock_file
.
parent
.
mkdir
(
parents
=
True
exist_ok
=
True
)
        
while
True
:
            
try
:
                
with
self
.
lock_file
.
open
(
"
x
"
)
as
f
:
                    
f
.
write
(
f
"
{
os
.
getpid
(
)
}
\
n
"
)
                
self
.
_lock_held
=
True
                
return
self
            
except
OSError
as
e
:
                
if
e
.
errno
not
in
(
errno
.
EEXIST
errno
.
EACCES
)
:
                    
raise
                
if
e
.
errno
=
=
errno
.
EACCES
and
sys
.
platform
!
=
"
win32
"
:
                    
raise
                
if
self
.
_try_remove_stale_lock
(
)
:
                    
continue
                
if
timeout
>
=
0
and
time
.
monotonic
(
)
-
start_time
>
=
timeout
:
                    
raise
LockTimeout
(
self
.
lock_file
)
                
time
.
sleep
(
poll_interval
)
                
poll_interval
=
min
(
poll_interval
*
1
.
5
1
.
0
)
    
def
release
(
self
)
:
        
"
"
"
Release
the
lock
by
deleting
the
lock
file
.
"
"
"
        
if
not
self
.
_lock_held
:
            
return
        
while
True
:
            
try
:
                
self
.
lock_file
.
unlink
(
)
                
self
.
_lock_held
=
False
                
break
            
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
errno
.
EACCES
:
                    
time
.
sleep
(
0
.
1
)
                
elif
e
.
errno
=
=
errno
.
ENOENT
:
                    
self
.
_lock_held
=
False
                    
break
                
else
:
                    
raise
    
def
__enter__
(
self
)
:
        
self
.
acquire
(
)
        
return
self
    
def
__exit__
(
self
exc_type
exc_val
exc_tb
)
:
        
self
.
release
(
)
        
return
False
