from
__future__
import
annotations
import
os
import
sys
from
typing
import
cast
from
.
_api
import
BaseFileLock
has_fcntl
=
False
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
    
class
UnixFileLock
(
BaseFileLock
)
:
        
"
"
"
Uses
the
:
func
:
fcntl
.
flock
to
hard
lock
the
lock
file
on
unix
systems
.
"
"
"
        
def
_acquire
(
self
)
-
>
None
:
            
raise
NotImplementedError
        
def
_release
(
self
)
-
>
None
:
            
raise
NotImplementedError
else
:
    
try
:
        
import
fcntl
    
except
ImportError
:
        
pass
    
else
:
        
has_fcntl
=
True
    
class
UnixFileLock
(
BaseFileLock
)
:
        
"
"
"
Uses
the
:
func
:
fcntl
.
flock
to
hard
lock
the
lock
file
on
unix
systems
.
"
"
"
        
def
_acquire
(
self
)
-
>
None
:
            
open_mode
=
os
.
O_RDWR
|
os
.
O_CREAT
|
os
.
O_TRUNC
            
fd
=
os
.
open
(
self
.
_lock_file
open_mode
)
            
try
:
                
fcntl
.
flock
(
fd
fcntl
.
LOCK_EX
|
fcntl
.
LOCK_NB
)
            
except
OSError
:
                
os
.
close
(
fd
)
            
else
:
                
self
.
_lock_file_fd
=
fd
        
def
_release
(
self
)
-
>
None
:
            
fd
=
cast
(
int
self
.
_lock_file_fd
)
            
self
.
_lock_file_fd
=
None
            
fcntl
.
flock
(
fd
fcntl
.
LOCK_UN
)
            
os
.
close
(
fd
)
__all__
=
[
    
"
has_fcntl
"
    
"
UnixFileLock
"
]
