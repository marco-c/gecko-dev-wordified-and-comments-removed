import
os
import
sys
from
errno
import
EACCES
EEXIST
ENOENT
from
.
_api
import
BaseFileLock
from
.
_util
import
raise_on_exist_ro_file
class
SoftFileLock
(
BaseFileLock
)
:
    
"
"
"
Simply
watches
the
existence
of
the
lock
file
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
        
raise_on_exist_ro_file
(
self
.
_lock_file
)
        
mode
=
(
            
os
.
O_WRONLY
            
|
os
.
O_CREAT
            
|
os
.
O_EXCL
            
|
os
.
O_TRUNC
        
)
        
try
:
            
fd
=
os
.
open
(
self
.
_lock_file
mode
)
        
except
OSError
as
exception
:
            
if
exception
.
errno
=
=
EEXIST
:
                
pass
            
elif
exception
.
errno
=
=
ENOENT
:
                
raise
            
elif
exception
.
errno
=
=
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
        
os
.
close
(
self
.
_lock_file_fd
)
        
self
.
_lock_file_fd
=
None
        
try
:
            
os
.
remove
(
self
.
_lock_file
)
        
except
OSError
:
            
pass
__all__
=
[
    
"
SoftFileLock
"
]
