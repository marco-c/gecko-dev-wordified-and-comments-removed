import
hashlib
import
os
from
textwrap
import
dedent
from
.
.
cache
import
BaseCache
SeparateBodyBaseCache
from
.
.
controller
import
CacheController
try
:
    
FileNotFoundError
except
NameError
:
    
FileNotFoundError
=
(
IOError
OSError
)
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
_FileCacheMixin
:
    
"
"
"
Shared
implementation
for
both
FileCache
variants
.
"
"
"
    
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
        
try
:
            
from
lockfile
import
LockFile
            
from
lockfile
.
mkdirlockfile
import
MkdirLockFile
        
except
ImportError
:
            
notice
=
dedent
(
                
"
"
"
            
NOTE
:
In
order
to
use
the
FileCache
you
must
have
            
lockfile
installed
.
You
can
install
it
via
pip
:
              
pip
install
lockfile
            
"
"
"
            
)
            
raise
ImportError
(
notice
)
        
else
:
            
if
use_dir_lock
:
                
lock_class
=
MkdirLockFile
            
elif
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
        
try
:
            
with
open
(
name
"
rb
"
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
        
except
FileNotFoundError
:
            
return
None
    
def
set
(
self
key
value
expires
=
None
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
        
self
.
_write
(
name
value
)
    
def
_write
(
self
path
data
:
bytes
)
:
        
"
"
"
        
Safely
write
the
data
to
the
given
path
.
        
"
"
"
        
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
path
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
path
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
data
)
    
def
_delete
(
self
key
suffix
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
+
suffix
        
if
not
self
.
forever
:
            
try
:
                
os
.
remove
(
name
)
            
except
FileNotFoundError
:
                
pass
class
FileCache
(
_FileCacheMixin
BaseCache
)
:
    
"
"
"
    
Traditional
FileCache
:
body
is
stored
in
memory
so
not
suitable
for
large
    
downloads
.
    
"
"
"
    
def
delete
(
self
key
)
:
        
self
.
_delete
(
key
"
"
)
class
SeparateBodyFileCache
(
_FileCacheMixin
SeparateBodyBaseCache
)
:
    
"
"
"
    
Memory
-
efficient
FileCache
:
body
is
stored
in
a
separate
file
reducing
    
peak
memory
usage
.
    
"
"
"
    
def
get_body
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
+
"
.
body
"
        
try
:
            
return
open
(
name
"
rb
"
)
        
except
FileNotFoundError
:
            
return
None
    
def
set_body
(
self
key
body
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
+
"
.
body
"
        
self
.
_write
(
name
body
)
    
def
delete
(
self
key
)
:
        
self
.
_delete
(
key
"
"
)
        
self
.
_delete
(
key
"
.
body
"
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
