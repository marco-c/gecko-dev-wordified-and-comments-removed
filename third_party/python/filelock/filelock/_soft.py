from
__future__
import
annotations
import
os
import
sys
from
contextlib
import
suppress
from
errno
import
EACCES
EEXIST
from
pathlib
import
Path
from
.
_api
import
BaseFileLock
from
.
_util
import
ensure_directory_exists
raise_on_not_writable_file
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
-
>
None
:
        
raise_on_not_writable_file
(
self
.
lock_file
)
        
ensure_directory_exists
(
self
.
lock_file
)
        
flags
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
            
file_handler
=
os
.
open
(
self
.
lock_file
flags
self
.
_context
.
mode
)
        
except
OSError
as
exception
:
            
if
not
(
                
exception
.
errno
=
=
EEXIST
                
or
(
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
=
=
"
win32
"
)
            
)
:
                
raise
        
else
:
            
self
.
_context
.
lock_file_fd
=
file_handler
    
def
_release
(
self
)
-
>
None
:
        
assert
self
.
_context
.
lock_file_fd
is
not
None
        
os
.
close
(
self
.
_context
.
lock_file_fd
)
        
self
.
_context
.
lock_file_fd
=
None
        
with
suppress
(
OSError
)
:
            
Path
(
self
.
lock_file
)
.
unlink
(
)
__all__
=
[
    
"
SoftFileLock
"
]
