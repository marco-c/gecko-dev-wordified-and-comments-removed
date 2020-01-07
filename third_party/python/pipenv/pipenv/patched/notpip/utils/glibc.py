from
__future__
import
absolute_import
import
re
import
ctypes
import
platform
import
warnings
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
check_glibc_version
(
version_str
required_major
minimum_minor
)
:
    
m
=
re
.
match
(
r
"
(
?
P
<
major
>
[
0
-
9
]
+
)
\
.
(
?
P
<
minor
>
[
0
-
9
]
+
)
"
version_str
)
    
if
not
m
:
        
warnings
.
warn
(
"
Expected
glibc
version
with
2
components
major
.
minor
"
                      
"
got
:
%
s
"
%
version_str
RuntimeWarning
)
        
return
False
    
return
(
int
(
m
.
group
(
"
major
"
)
)
=
=
required_major
and
            
int
(
m
.
group
(
"
minor
"
)
)
>
=
minimum_minor
)
def
have_compatible_glibc
(
required_major
minimum_minor
)
:
    
version_str
=
glibc_version_string
(
)
    
if
version_str
is
None
:
        
return
False
    
return
check_glibc_version
(
version_str
required_major
minimum_minor
)
def
libc_ver
(
)
:
    
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
platform
.
libc_ver
(
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
