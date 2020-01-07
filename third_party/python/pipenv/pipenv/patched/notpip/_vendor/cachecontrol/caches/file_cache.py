import
hashlib
import
os
from
pip9
.
_vendor
.
lockfile
import
LockFile
from
pip9
.
_vendor
.
lockfile
.
mkdirlockfile
import
MkdirLockFile
from
.
.
cache
import
BaseCache
from
.
.
controller
import
CacheController
def
_secure_open_write
(
filename
fmode
)
:
    
flags
=
os
.
O_WRONLY
    
flags
|
=
os
.
O_CREAT
|
os
.
O_EXCL
    
if
hasattr
(
os
"
O_NOFOLLOW
"
)
:
        
flags
|
=
os
.
O_NOFOLLOW
    
if
hasattr
(
os
"
O_BINARY
"
)
:
        
flags
|
=
os
.
O_BINARY
    
try
:
        
os
.
remove
(
filename
)
    
except
(
IOError
OSError
)
:
        
pass
    
fd
=
os
.
open
(
filename
flags
fmode
)
    
try
:
        
return
os
.
fdopen
(
fd
"
wb
"
)
    
except
:
        
os
.
close
(
fd
)
        
raise
class
FileCache
(
BaseCache
)
:
    
def
__init__
(
self
directory
forever
=
False
filemode
=
0o0600
                 
dirmode
=
0o0700
use_dir_lock
=
None
lock_class
=
None
)
:
        
if
use_dir_lock
is
not
None
and
lock_class
is
not
None
:
            
raise
ValueError
(
"
Cannot
use
use_dir_lock
and
lock_class
together
"
)
        
if
use_dir_lock
:
            
lock_class
=
MkdirLockFile
        
if
lock_class
is
None
:
            
lock_class
=
LockFile
        
self
.
directory
=
directory
        
self
.
forever
=
forever
        
self
.
filemode
=
filemode
        
self
.
dirmode
=
dirmode
        
self
.
lock_class
=
lock_class
    
staticmethod
    
def
encode
(
x
)
:
        
return
hashlib
.
sha224
(
x
.
encode
(
)
)
.
hexdigest
(
)
    
def
_fn
(
self
name
)
:
        
hashed
=
self
.
encode
(
name
)
        
parts
=
list
(
hashed
[
:
5
]
)
+
[
hashed
]
        
return
os
.
path
.
join
(
self
.
directory
*
parts
)
    
def
get
(
self
key
)
:
        
name
=
self
.
_fn
(
key
)
        
if
not
os
.
path
.
exists
(
name
)
:
            
return
None
        
with
open
(
name
'
rb
'
)
as
fh
:
            
return
fh
.
read
(
)
    
def
set
(
self
key
value
)
:
        
name
=
self
.
_fn
(
key
)
        
try
:
            
os
.
makedirs
(
os
.
path
.
dirname
(
name
)
self
.
dirmode
)
        
except
(
IOError
OSError
)
:
            
pass
        
with
self
.
lock_class
(
name
)
as
lock
:
            
with
_secure_open_write
(
lock
.
path
self
.
filemode
)
as
fh
:
                
fh
.
write
(
value
)
    
def
delete
(
self
key
)
:
        
name
=
self
.
_fn
(
key
)
        
if
not
self
.
forever
:
            
os
.
remove
(
name
)
def
url_to_file_path
(
url
filecache
)
:
    
"
"
"
Return
the
file
cache
path
based
on
the
URL
.
    
This
does
not
ensure
the
file
exists
!
    
"
"
"
    
key
=
CacheController
.
cache_url
(
url
)
    
return
filecache
.
_fn
(
key
)
