import
os
import
sys
from
typing
import
Optional
Tuple
def
glibc_version_string
(
)
-
>
Optional
[
str
]
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
-
>
Optional
[
str
]
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
        
gnu_libc_version
=
os
.
confstr
(
"
CS_GNU_LIBC_VERSION
"
)
        
if
gnu_libc_version
is
None
:
            
return
None
        
_
version
=
gnu_libc_version
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
-
>
Optional
[
str
]
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
-
>
Tuple
[
str
str
]
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
