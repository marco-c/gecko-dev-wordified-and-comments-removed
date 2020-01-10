"
"
"
Routines
common
to
all
posix
systems
.
"
"
"
import
errno
import
glob
import
os
import
sys
import
time
from
.
_common
import
memoize
from
.
_common
import
sdiskusage
from
.
_common
import
usage_percent
from
.
_compat
import
PY3
from
.
_compat
import
unicode
__all__
=
[
'
pid_exists
'
'
wait_pid
'
'
disk_usage
'
'
get_terminal_map
'
]
TimeoutExpired
=
None
def
pid_exists
(
pid
)
:
    
"
"
"
Check
whether
pid
exists
in
the
current
process
table
.
"
"
"
    
if
pid
=
=
0
:
        
return
True
    
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
ESRCH
:
            
return
False
        
elif
err
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
        
else
:
            
raise
err
    
else
:
        
return
True
def
wait_pid
(
pid
timeout
=
None
proc_name
=
None
)
:
    
"
"
"
Wait
for
process
with
pid
'
pid
'
to
terminate
and
return
its
    
exit
status
code
as
an
integer
.
    
If
pid
is
not
a
children
of
os
.
getpid
(
)
(
current
process
)
just
    
waits
until
the
process
disappears
and
return
None
.
    
If
pid
does
not
exist
at
all
return
None
immediately
.
    
Raise
TimeoutExpired
on
timeout
expired
.
    
"
"
"
    
def
check_timeout
(
delay
)
:
        
if
timeout
is
not
None
:
            
if
timer
(
)
>
=
stop_at
:
                
raise
TimeoutExpired
(
timeout
pid
=
pid
name
=
proc_name
)
        
time
.
sleep
(
delay
)
        
return
min
(
delay
*
2
0
.
04
)
    
timer
=
getattr
(
time
'
monotonic
'
time
.
time
)
    
if
timeout
is
not
None
:
        
def
waitcall
(
)
:
            
return
os
.
waitpid
(
pid
os
.
WNOHANG
)
        
stop_at
=
timer
(
)
+
timeout
    
else
:
        
def
waitcall
(
)
:
            
return
os
.
waitpid
(
pid
0
)
    
delay
=
0
.
0001
    
while
True
:
        
try
:
            
retpid
status
=
waitcall
(
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
EINTR
:
                
delay
=
check_timeout
(
delay
)
                
continue
            
elif
err
.
errno
=
=
errno
.
ECHILD
:
                
while
True
:
                    
if
pid_exists
(
pid
)
:
                        
delay
=
check_timeout
(
delay
)
                    
else
:
                        
return
            
else
:
                
raise
        
else
:
            
if
retpid
=
=
0
:
                
delay
=
check_timeout
(
delay
)
                
continue
            
if
os
.
WIFSIGNALED
(
status
)
:
                
return
-
os
.
WTERMSIG
(
status
)
            
elif
os
.
WIFEXITED
(
status
)
:
                
return
os
.
WEXITSTATUS
(
status
)
            
else
:
                
raise
ValueError
(
"
unknown
process
exit
status
%
r
"
%
status
)
def
disk_usage
(
path
)
:
    
"
"
"
Return
disk
usage
associated
with
path
.
    
Note
:
UNIX
usually
reserves
5
%
disk
space
which
is
not
accessible
    
by
user
.
In
this
function
"
total
"
and
"
used
"
values
reflect
the
    
total
and
used
disk
space
whereas
"
free
"
and
"
percent
"
represent
    
the
"
free
"
and
"
used
percent
"
user
disk
space
.
    
"
"
"
    
if
PY3
:
        
st
=
os
.
statvfs
(
path
)
    
else
:
        
try
:
            
st
=
os
.
statvfs
(
path
)
        
except
UnicodeEncodeError
:
            
if
isinstance
(
path
unicode
)
:
                
try
:
                    
path
=
path
.
encode
(
sys
.
getfilesystemencoding
(
)
)
                
except
UnicodeEncodeError
:
                    
pass
                
st
=
os
.
statvfs
(
path
)
            
else
:
                
raise
    
total
=
(
st
.
f_blocks
*
st
.
f_frsize
)
    
avail_to_root
=
(
st
.
f_bfree
*
st
.
f_frsize
)
    
avail_to_user
=
(
st
.
f_bavail
*
st
.
f_frsize
)
    
used
=
(
total
-
avail_to_root
)
    
total_user
=
used
+
avail_to_user
    
usage_percent_user
=
usage_percent
(
used
total_user
round_
=
1
)
    
return
sdiskusage
(
        
total
=
total
used
=
used
free
=
avail_to_user
percent
=
usage_percent_user
)
memoize
def
get_terminal_map
(
)
:
    
"
"
"
Get
a
map
of
device
-
id
-
>
path
as
a
dict
.
    
Used
by
Process
.
terminal
(
)
    
"
"
"
    
ret
=
{
}
    
ls
=
glob
.
glob
(
'
/
dev
/
tty
*
'
)
+
glob
.
glob
(
'
/
dev
/
pts
/
*
'
)
    
for
name
in
ls
:
        
assert
name
not
in
ret
name
        
try
:
            
ret
[
os
.
stat
(
name
)
.
st_rdev
]
=
name
        
except
OSError
as
err
:
            
if
err
.
errno
!
=
errno
.
ENOENT
:
                
raise
    
return
ret
