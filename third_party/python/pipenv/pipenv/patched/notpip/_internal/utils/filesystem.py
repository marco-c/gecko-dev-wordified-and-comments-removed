import
errno
import
os
import
os
.
path
import
random
import
shutil
import
stat
import
sys
from
contextlib
import
contextmanager
from
tempfile
import
NamedTemporaryFile
from
pipenv
.
patched
.
notpip
.
_vendor
.
retrying
import
retry
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
compat
import
get_path_uid
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
cast
if
MYPY_CHECK_RUNNING
:
    
from
typing
import
BinaryIO
Iterator
    
class
NamedTemporaryFileResult
(
BinaryIO
)
:
        
property
        
def
file
(
self
)
:
            
pass
def
check_path_owner
(
path
)
:
    
if
sys
.
platform
=
=
"
win32
"
or
not
hasattr
(
os
"
geteuid
"
)
:
        
return
True
    
assert
os
.
path
.
isabs
(
path
)
    
previous
=
None
    
while
path
!
=
previous
:
        
if
os
.
path
.
lexists
(
path
)
:
            
if
os
.
geteuid
(
)
=
=
0
:
                
try
:
                    
path_uid
=
get_path_uid
(
path
)
                
except
OSError
:
                    
return
False
                
return
path_uid
=
=
0
            
else
:
                
return
os
.
access
(
path
os
.
W_OK
)
        
else
:
            
previous
path
=
path
os
.
path
.
dirname
(
path
)
    
return
False
def
copy2_fixed
(
src
dest
)
:
    
"
"
"
Wrap
shutil
.
copy2
(
)
but
map
errors
copying
socket
files
to
    
SpecialFileError
as
expected
.
    
See
also
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
issue37700
.
    
"
"
"
    
try
:
        
shutil
.
copy2
(
src
dest
)
    
except
(
OSError
IOError
)
:
        
for
f
in
[
src
dest
]
:
            
try
:
                
is_socket_file
=
is_socket
(
f
)
            
except
OSError
:
                
pass
            
else
:
                
if
is_socket_file
:
                    
raise
shutil
.
SpecialFileError
(
"
%
s
is
a
socket
"
%
f
)
        
raise
def
is_socket
(
path
)
:
    
return
stat
.
S_ISSOCK
(
os
.
lstat
(
path
)
.
st_mode
)
contextmanager
def
adjacent_tmp_file
(
path
)
:
    
"
"
"
Given
a
path
to
a
file
open
a
temp
file
next
to
it
securely
and
ensure
    
it
is
written
to
disk
after
the
context
reaches
its
end
.
    
"
"
"
    
with
NamedTemporaryFile
(
        
delete
=
False
        
dir
=
os
.
path
.
dirname
(
path
)
        
prefix
=
os
.
path
.
basename
(
path
)
        
suffix
=
'
.
tmp
'
    
)
as
f
:
        
result
=
cast
(
'
NamedTemporaryFileResult
'
f
)
        
try
:
            
yield
result
        
finally
:
            
result
.
file
.
flush
(
)
            
os
.
fsync
(
result
.
file
.
fileno
(
)
)
_replace_retry
=
retry
(
stop_max_delay
=
1000
wait_fixed
=
250
)
if
PY2
:
    
_replace_retry
    
def
replace
(
src
dest
)
:
        
try
:
            
os
.
rename
(
src
dest
)
        
except
OSError
:
            
os
.
remove
(
dest
)
            
os
.
rename
(
src
dest
)
else
:
    
replace
=
_replace_retry
(
os
.
replace
)
def
test_writable_dir
(
path
)
:
    
"
"
"
Check
if
a
directory
is
writable
.
    
Uses
os
.
access
(
)
on
POSIX
tries
creating
files
on
Windows
.
    
"
"
"
    
while
not
os
.
path
.
isdir
(
path
)
:
        
parent
=
os
.
path
.
dirname
(
path
)
        
if
parent
=
=
path
:
            
break
        
path
=
parent
    
if
os
.
name
=
=
'
posix
'
:
        
return
os
.
access
(
path
os
.
W_OK
)
    
return
_test_writable_dir_win
(
path
)
def
_test_writable_dir_win
(
path
)
:
    
basename
=
'
accesstest_deleteme_fishfingers_custard_
'
    
alphabet
=
'
abcdefghijklmnopqrstuvwxyz0123456789
'
    
for
i
in
range
(
10
)
:
        
name
=
basename
+
'
'
.
join
(
random
.
choice
(
alphabet
)
for
_
in
range
(
6
)
)
        
file
=
os
.
path
.
join
(
path
name
)
        
try
:
            
fd
=
os
.
open
(
file
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
O_EXCL
)
        
except
OSError
as
e
:
            
if
e
.
errno
=
=
errno
.
EEXIST
:
                
continue
            
if
e
.
errno
=
=
errno
.
EPERM
:
                
return
False
            
raise
        
else
:
            
os
.
close
(
fd
)
            
os
.
unlink
(
file
)
            
return
True
    
raise
EnvironmentError
(
        
'
Unexpected
condition
testing
for
writable
directory
'
    
)
