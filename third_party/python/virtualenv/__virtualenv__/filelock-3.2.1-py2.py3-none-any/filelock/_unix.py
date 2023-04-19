import
os
from
.
_api
import
BaseFileLock
try
:
    
import
fcntl
except
ImportError
:
    
fcntl
=
None
has_fcntl
=
fcntl
is
not
None
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
(
OSError
IOError
)
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
:
        
fd
=
self
.
_lock_file_fd
        
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
