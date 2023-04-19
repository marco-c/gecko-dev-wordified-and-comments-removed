import
os
import
sys
from
abc
import
ABC
from
errno
import
ENOENT
from
typing
import
cast
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
msvcrt
    
class
WindowsFileLock
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
msvcrt
.
locking
function
to
hard
lock
the
lock
file
on
windows
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
O_RDWR
                
|
os
.
O_CREAT
                
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
ENOENT
:
                    
raise
            
else
:
                
try
:
                    
msvcrt
.
locking
(
fd
msvcrt
.
LK_NBLCK
1
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
            
msvcrt
.
locking
(
fd
msvcrt
.
LK_UNLCK
1
)
            
os
.
close
(
fd
)
            
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
else
:
    
class
WindowsFileLock
(
BaseFileLock
ABC
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
msvcrt
.
locking
function
to
hard
lock
the
lock
file
on
windows
systems
.
"
"
"
__all__
=
[
    
"
WindowsFileLock
"
]
