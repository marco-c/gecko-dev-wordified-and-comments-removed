from
__future__
import
absolute_import
import
os
import
sys
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
typing
import
MYPY_CHECK_RUNNING
if
MYPY_CHECK_RUNNING
:
    
from
typing
import
Optional
Tuple
def
glibc_version_string
(
)
:
    
"
Returns
glibc
version
string
or
None
if
not
using
glibc
.
"
    
return
glibc_version_string_confstr
(
)
or
glibc_version_string_ctypes
(
)
def
glibc_version_string_confstr
(
)
:
    
"
Primary
implementation
of
glibc_version_string
using
os
.
confstr
.
"
    
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
        
return
None
    
try
:
        
_
version
=
os
.
confstr
(
"
CS_GNU_LIBC_VERSION
"
)
.
split
(
)
    
except
(
AttributeError
OSError
ValueError
)
:
        
return
None
    
return
version
def
glibc_version_string_ctypes
(
)
:
    
"
Fallback
implementation
of
glibc_version_string
using
ctypes
.
"
    
try
:
        
import
ctypes
    
except
ImportError
:
        
return
None
    
process_namespace
=
ctypes
.
CDLL
(
None
)
    
try
:
        
gnu_get_libc_version
=
process_namespace
.
gnu_get_libc_version
    
except
AttributeError
:
        
return
None
    
gnu_get_libc_version
.
restype
=
ctypes
.
c_char_p
    
version_str
=
gnu_get_libc_version
(
)
    
if
not
isinstance
(
version_str
str
)
:
        
version_str
=
version_str
.
decode
(
"
ascii
"
)
    
return
version_str
def
libc_ver
(
)
:
    
"
"
"
Try
to
determine
the
glibc
version
    
Returns
a
tuple
of
strings
(
lib
version
)
which
default
to
empty
strings
    
in
case
the
lookup
fails
.
    
"
"
"
    
glibc_version
=
glibc_version_string
(
)
    
if
glibc_version
is
None
:
        
return
(
"
"
"
"
)
    
else
:
        
return
(
"
glibc
"
glibc_version
)
