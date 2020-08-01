"
"
"
Stuff
that
differs
in
different
Python
versions
and
platform
distributions
.
"
"
"
from
__future__
import
absolute_import
division
import
codecs
import
locale
import
logging
import
os
import
shutil
import
sys
from
pipenv
.
patched
.
notpip
.
_vendor
.
six
import
PY2
text_type
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
Text
Tuple
Union
try
:
    
import
ipaddress
except
ImportError
:
    
try
:
        
from
pipenv
.
patched
.
notpip
.
_vendor
import
ipaddress
    
except
ImportError
:
        
import
ipaddr
as
ipaddress
        
ipaddress
.
ip_address
=
ipaddress
.
IPAddress
        
ipaddress
.
ip_network
=
ipaddress
.
IPNetwork
__all__
=
[
    
"
ipaddress
"
"
uses_pycache
"
"
console_to_str
"
    
"
get_path_uid
"
"
stdlib_pkgs
"
"
WINDOWS
"
"
samefile
"
"
get_terminal_size
"
]
logger
=
logging
.
getLogger
(
__name__
)
if
PY2
:
    
import
imp
    
try
:
        
cache_from_source
=
imp
.
cache_from_source
    
except
AttributeError
:
        
cache_from_source
=
None
    
uses_pycache
=
cache_from_source
is
not
None
else
:
    
uses_pycache
=
True
    
from
importlib
.
util
import
cache_from_source
if
PY2
:
    
def
backslashreplace_decode_fn
(
err
)
:
        
raw_bytes
=
(
err
.
object
[
i
]
for
i
in
range
(
err
.
start
err
.
end
)
)
        
raw_bytes
=
(
ord
(
b
)
for
b
in
raw_bytes
)
        
return
u
"
"
.
join
(
u
"
\
\
x
%
x
"
%
c
for
c
in
raw_bytes
)
err
.
end
    
codecs
.
register_error
(
        
"
backslashreplace_decode
"
        
backslashreplace_decode_fn
    
)
    
backslashreplace_decode
=
"
backslashreplace_decode
"
else
:
    
backslashreplace_decode
=
"
backslashreplace
"
def
has_tls
(
)
:
    
try
:
        
import
_ssl
        
return
True
    
except
ImportError
:
        
pass
    
from
pipenv
.
patched
.
notpip
.
_vendor
.
urllib3
.
util
import
IS_PYOPENSSL
    
return
IS_PYOPENSSL
def
str_to_display
(
data
desc
=
None
)
:
    
"
"
"
    
For
display
or
logging
purposes
convert
a
bytes
object
(
or
text
)
to
    
text
(
e
.
g
.
unicode
in
Python
2
)
safe
for
output
.
    
:
param
desc
:
An
optional
phrase
describing
the
input
data
for
use
in
        
the
log
message
if
a
warning
is
logged
.
Defaults
to
"
Bytes
object
"
.
    
This
function
should
never
error
out
and
so
can
take
a
best
effort
    
approach
.
It
is
okay
to
be
lossy
if
needed
since
the
return
value
is
    
just
for
display
.
    
We
assume
the
data
is
in
the
locale
preferred
encoding
.
If
it
won
'
t
    
decode
properly
we
warn
the
user
but
decode
as
best
we
can
.
    
We
also
ensure
that
the
output
can
be
safely
written
to
standard
output
    
without
encoding
errors
.
    
"
"
"
    
if
isinstance
(
data
text_type
)
:
        
return
data
    
encoding
=
locale
.
getpreferredencoding
(
)
    
if
(
not
encoding
)
or
codecs
.
lookup
(
encoding
)
.
name
=
=
"
ascii
"
:
        
encoding
=
"
utf
-
8
"
    
try
:
        
decoded_data
=
data
.
decode
(
encoding
)
    
except
UnicodeDecodeError
:
        
if
desc
is
None
:
            
desc
=
'
Bytes
object
'
        
msg_format
=
'
{
}
does
not
appear
to
be
encoded
as
%
s
'
.
format
(
desc
)
        
logger
.
warning
(
msg_format
encoding
)
        
decoded_data
=
data
.
decode
(
encoding
errors
=
backslashreplace_decode
)
    
output_encoding
=
getattr
(
getattr
(
sys
"
__stderr__
"
None
)
                              
"
encoding
"
None
)
    
if
output_encoding
:
        
output_encoded
=
decoded_data
.
encode
(
            
output_encoding
            
errors
=
"
backslashreplace
"
        
)
        
decoded_data
=
output_encoded
.
decode
(
output_encoding
)
    
return
decoded_data
def
console_to_str
(
data
)
:
    
"
"
"
Return
a
string
safe
for
output
of
subprocess
output
.
    
"
"
"
    
return
str_to_display
(
data
desc
=
'
Subprocess
output
'
)
def
get_path_uid
(
path
)
:
    
"
"
"
    
Return
path
'
s
uid
.
    
Does
not
follow
symlinks
:
        
https
:
/
/
github
.
com
/
pypa
/
pip
/
pull
/
935
#
discussion_r5307003
    
Placed
this
function
in
compat
due
to
differences
on
AIX
and
    
Jython
that
should
eventually
go
away
.
    
:
raises
OSError
:
When
path
is
a
symlink
or
can
'
t
be
read
.
    
"
"
"
    
if
hasattr
(
os
'
O_NOFOLLOW
'
)
:
        
fd
=
os
.
open
(
path
os
.
O_RDONLY
|
os
.
O_NOFOLLOW
)
        
file_uid
=
os
.
fstat
(
fd
)
.
st_uid
        
os
.
close
(
fd
)
    
else
:
        
if
not
os
.
path
.
islink
(
path
)
:
            
file_uid
=
os
.
stat
(
path
)
.
st_uid
        
else
:
            
raise
OSError
(
                
"
%
s
is
a
symlink
;
Will
not
return
uid
for
symlinks
"
%
path
            
)
    
return
file_uid
def
expanduser
(
path
)
:
    
"
"
"
    
Expand
~
and
~
user
constructions
.
    
Includes
a
workaround
for
https
:
/
/
bugs
.
python
.
org
/
issue14768
    
"
"
"
    
expanded
=
os
.
path
.
expanduser
(
path
)
    
if
path
.
startswith
(
'
~
/
'
)
and
expanded
.
startswith
(
'
/
/
'
)
:
        
expanded
=
expanded
[
1
:
]
    
return
expanded
stdlib_pkgs
=
{
"
python
"
"
wsgiref
"
"
argparse
"
}
WINDOWS
=
(
sys
.
platform
.
startswith
(
"
win
"
)
or
           
(
sys
.
platform
=
=
'
cli
'
and
os
.
name
=
=
'
nt
'
)
)
def
samefile
(
file1
file2
)
:
    
"
"
"
Provide
an
alternative
for
os
.
path
.
samefile
on
Windows
/
Python2
"
"
"
    
if
hasattr
(
os
.
path
'
samefile
'
)
:
        
return
os
.
path
.
samefile
(
file1
file2
)
    
else
:
        
path1
=
os
.
path
.
normcase
(
os
.
path
.
abspath
(
file1
)
)
        
path2
=
os
.
path
.
normcase
(
os
.
path
.
abspath
(
file2
)
)
        
return
path1
=
=
path2
if
hasattr
(
shutil
'
get_terminal_size
'
)
:
    
def
get_terminal_size
(
)
:
        
"
"
"
        
Returns
a
tuple
(
x
y
)
representing
the
width
(
x
)
and
the
height
(
y
)
        
in
characters
of
the
terminal
window
.
        
"
"
"
        
return
tuple
(
shutil
.
get_terminal_size
(
)
)
else
:
    
def
get_terminal_size
(
)
:
        
"
"
"
        
Returns
a
tuple
(
x
y
)
representing
the
width
(
x
)
and
the
height
(
y
)
        
in
characters
of
the
terminal
window
.
        
"
"
"
        
def
ioctl_GWINSZ
(
fd
)
:
            
try
:
                
import
fcntl
                
import
termios
                
import
struct
                
cr
=
struct
.
unpack_from
(
                    
'
hh
'
                    
fcntl
.
ioctl
(
fd
termios
.
TIOCGWINSZ
'
12345678
'
)
                
)
            
except
Exception
:
                
return
None
            
if
cr
=
=
(
0
0
)
:
                
return
None
            
return
cr
        
cr
=
ioctl_GWINSZ
(
0
)
or
ioctl_GWINSZ
(
1
)
or
ioctl_GWINSZ
(
2
)
        
if
not
cr
:
            
if
sys
.
platform
!
=
"
win32
"
:
                
try
:
                    
fd
=
os
.
open
(
os
.
ctermid
(
)
os
.
O_RDONLY
)
                    
cr
=
ioctl_GWINSZ
(
fd
)
                    
os
.
close
(
fd
)
                
except
Exception
:
                    
pass
        
if
not
cr
:
            
cr
=
(
os
.
environ
.
get
(
'
LINES
'
25
)
os
.
environ
.
get
(
'
COLUMNS
'
80
)
)
        
return
int
(
cr
[
1
]
)
int
(
cr
[
0
]
)
