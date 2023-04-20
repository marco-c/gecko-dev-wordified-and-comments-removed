import
errno
import
logging
import
os
import
shutil
import
stat
import
time
"
"
"
File
system
utilities
copied
from
mozfile
.
"
"
"
LOG
=
logging
.
getLogger
(
__name__
)
def
_call_windows_retry
(
func
args
=
(
)
retry_max
=
5
retry_delay
=
0
.
5
)
:
    
"
"
"
    
It
'
s
possible
to
see
spurious
errors
on
Windows
due
to
various
things
    
keeping
a
handle
to
the
directory
open
(
explorer
virus
scanners
etc
)
    
So
we
try
a
few
times
if
it
fails
with
a
known
error
.
    
"
"
"
    
retry_count
=
0
    
while
True
:
        
try
:
            
func
(
*
args
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
not
in
(
errno
.
EACCES
errno
.
ENOTEMPTY
)
:
                
raise
            
if
retry_count
=
=
retry_max
:
                
raise
            
retry_count
+
=
1
            
LOG
.
info
(
'
%
s
(
)
failed
for
"
%
s
"
.
Reason
:
%
s
(
%
s
)
.
Retrying
.
.
.
'
                     
func
.
__name__
args
e
.
strerror
e
.
errno
)
            
time
.
sleep
(
retry_delay
)
        
else
:
            
break
def
remove
(
path
)
:
    
"
"
"
Removes
the
specified
file
link
or
directory
tree
.
    
This
is
a
replacement
for
shutil
.
rmtree
that
works
better
under
    
windows
.
It
does
the
following
things
:
     
-
check
path
access
for
the
current
user
before
trying
to
remove
     
-
retry
operations
on
some
known
errors
due
to
various
things
keeping
       
a
handle
on
file
paths
-
like
explorer
virus
scanners
etc
.
The
       
known
errors
are
errno
.
EACCES
and
errno
.
ENOTEMPTY
and
it
will
       
retry
up
to
5
five
times
with
a
delay
of
0
.
5
seconds
between
each
       
attempt
.
    
Note
that
no
error
will
be
raised
if
the
given
path
does
not
exists
.
    
:
param
path
:
path
to
be
removed
    
"
"
"
    
def
_call_with_windows_retry
(
*
args
*
*
kwargs
)
:
        
try
:
            
_call_windows_retry
(
*
args
*
*
kwargs
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
!
=
errno
.
ENOENT
:
                
raise
    
def
_update_permissions
(
path
)
:
        
"
"
"
Sets
specified
pemissions
depending
on
filetype
"
"
"
        
if
os
.
path
.
islink
(
path
)
:
            
return
        
stats
=
os
.
stat
(
path
)
        
if
os
.
path
.
isfile
(
path
)
:
            
mode
=
stats
.
st_mode
|
stat
.
S_IWUSR
        
elif
os
.
path
.
isdir
(
path
)
:
            
mode
=
stats
.
st_mode
|
stat
.
S_IWUSR
|
stat
.
S_IXUSR
        
else
:
            
return
        
_call_with_windows_retry
(
os
.
chmod
(
path
mode
)
)
    
if
not
os
.
path
.
exists
(
path
)
:
        
return
    
if
os
.
path
.
isfile
(
path
)
or
os
.
path
.
islink
(
path
)
:
        
_update_permissions
(
path
)
        
_call_with_windows_retry
(
os
.
remove
(
path
)
)
    
elif
os
.
path
.
isdir
(
path
)
:
        
_update_permissions
(
path
)
        
for
root
dirs
files
in
os
.
walk
(
path
)
:
            
for
entry
in
dirs
+
files
:
                
_update_permissions
(
os
.
path
.
join
(
root
entry
)
)
        
_call_with_windows_retry
(
shutil
.
rmtree
(
path
)
)
def
move
(
src
dst
)
:
    
"
"
"
    
Move
a
file
or
directory
path
.
    
This
is
a
replacement
for
shutil
.
move
that
works
better
under
windows
    
retrying
operations
on
some
known
errors
due
to
various
things
keeping
    
a
handle
on
file
paths
.
    
"
"
"
    
_call_windows_retry
(
shutil
.
move
(
src
dst
)
)
