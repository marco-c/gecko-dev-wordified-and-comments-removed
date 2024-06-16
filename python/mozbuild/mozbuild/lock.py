import
errno
import
os
import
stat
import
sys
import
time
class
LockFile
(
object
)
:
    
"
"
"
LockFile
is
used
by
the
lock_file
method
to
hold
the
lock
.
    
This
object
should
not
be
used
directly
but
only
through
    
the
lock_file
method
below
.
    
"
"
"
    
def
__init__
(
self
lockfile
)
:
        
self
.
lockfile
=
lockfile
    
def
__del__
(
self
)
:
        
while
True
:
            
try
:
                
os
.
remove
(
self
.
lockfile
)
                
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
                
else
:
                    
raise
def
lock_file
(
lockfile
max_wait
=
600
)
:
    
"
"
"
Create
and
hold
a
lockfile
of
the
given
name
with
the
given
timeout
.
    
To
release
the
lock
delete
the
returned
object
.
    
"
"
"
    
while
True
:
        
try
:
            
fd
=
os
.
open
(
lockfile
os
.
O_EXCL
|
os
.
O_RDWR
|
os
.
O_CREAT
)
            
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
EEXIST
or
(
                
sys
.
platform
=
=
"
win32
"
and
e
.
errno
=
=
errno
.
EACCES
            
)
:
                
pass
            
else
:
                
raise
        
try
:
            
f
=
open
(
lockfile
"
r
"
)
            
s
=
os
.
stat
(
lockfile
)
        
except
EnvironmentError
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
ENOENT
or
e
.
errno
=
=
errno
.
EACCES
:
                
continue
            
raise
Exception
(
                
"
{
0
}
exists
but
stat
(
)
failed
:
{
1
}
"
.
format
(
lockfile
e
.
strerror
)
            
)
        
now
=
int
(
time
.
time
(
)
)
        
if
now
-
s
[
stat
.
ST_MTIME
]
>
max_wait
:
            
pid
=
f
.
readline
(
)
.
rstrip
(
)
            
raise
Exception
(
                
"
{
0
}
has
been
locked
for
more
than
"
                
"
{
1
}
seconds
(
PID
{
2
}
)
"
.
format
(
lockfile
max_wait
pid
)
            
)
        
f
.
close
(
)
        
time
.
sleep
(
1
)
    
f
=
os
.
fdopen
(
fd
"
w
"
)
    
f
.
write
(
"
{
0
}
\
n
"
.
format
(
os
.
getpid
(
)
)
)
    
f
.
close
(
)
    
return
LockFile
(
lockfile
)
