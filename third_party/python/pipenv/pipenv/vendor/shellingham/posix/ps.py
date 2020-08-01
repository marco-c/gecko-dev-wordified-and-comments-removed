import
errno
import
subprocess
import
sys
from
.
_core
import
Process
class
PsNotAvailable
(
EnvironmentError
)
:
    
pass
def
get_process_mapping
(
)
:
    
"
"
"
Try
to
look
up
the
process
tree
via
the
output
of
ps
.
    
"
"
"
    
try
:
        
output
=
subprocess
.
check_output
(
[
            
'
ps
'
'
-
ww
'
'
-
o
'
'
pid
=
'
'
-
o
'
'
ppid
=
'
'
-
o
'
'
args
=
'
        
]
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
        
raise
PsNotAvailable
(
'
ps
not
found
'
)
    
except
subprocess
.
CalledProcessError
as
e
:
        
if
not
e
.
output
.
strip
(
)
:
            
return
{
}
        
raise
    
if
not
isinstance
(
output
str
)
:
        
encoding
=
sys
.
getfilesystemencoding
(
)
or
sys
.
getdefaultencoding
(
)
        
output
=
output
.
decode
(
encoding
)
    
processes
=
{
}
    
for
line
in
output
.
split
(
'
\
n
'
)
:
        
try
:
            
pid
ppid
args
=
line
.
strip
(
)
.
split
(
None
2
)
            
args
=
tuple
(
a
.
strip
(
)
for
a
in
args
.
split
(
'
'
)
)
        
except
ValueError
:
            
continue
        
processes
[
pid
]
=
Process
(
args
=
args
pid
=
pid
ppid
=
ppid
)
    
return
processes
