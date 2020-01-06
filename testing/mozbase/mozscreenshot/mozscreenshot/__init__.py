from
__future__
import
absolute_import
print_function
import
os
import
mozinfo
import
tempfile
import
subprocess
from
mozlog
.
formatters
.
process
import
strstatus
def
printstatus
(
name
returncode
)
:
    
"
"
"
    
print
the
status
of
a
command
exit
code
formatted
for
tbpl
.
    
Note
that
mozlog
structured
action
"
process_exit
"
should
be
used
    
instead
of
that
in
new
code
.
    
"
"
"
    
print
(
"
TEST
-
INFO
|
%
s
:
%
s
"
%
(
name
strstatus
(
returncode
)
)
)
def
dump_screen
(
utilityPath
log
)
:
    
"
"
"
dumps
a
screenshot
of
the
entire
screen
to
a
directory
specified
by
    
the
MOZ_UPLOAD_DIR
environment
variable
"
"
"
    
is_structured_log
=
hasattr
(
log
'
process_exit
'
)
    
if
mozinfo
.
isUnix
:
        
utility
=
[
os
.
path
.
join
(
utilityPath
"
screentopng
"
)
]
        
utilityname
=
"
screentopng
"
    
elif
mozinfo
.
isMac
:
        
utility
=
[
'
/
usr
/
sbin
/
screencapture
'
'
-
C
'
'
-
x
'
'
-
t
'
'
png
'
]
        
utilityname
=
"
screencapture
"
    
elif
mozinfo
.
isWin
:
        
utility
=
[
os
.
path
.
join
(
utilityPath
"
screenshot
.
exe
"
)
]
        
utilityname
=
"
screenshot
"
    
parent_dir
=
os
.
environ
.
get
(
'
MOZ_UPLOAD_DIR
'
None
)
    
if
not
parent_dir
:
        
log
.
info
(
'
Failed
to
retrieve
MOZ_UPLOAD_DIR
env
var
'
)
        
return
    
try
:
        
tmpfd
imgfilename
=
tempfile
.
mkstemp
(
            
prefix
=
'
mozilla
-
test
-
fail
-
screenshot_
'
            
suffix
=
'
.
png
'
dir
=
parent_dir
        
)
        
os
.
close
(
tmpfd
)
        
if
is_structured_log
:
            
log
.
process_start
(
utilityname
)
        
returncode
=
subprocess
.
call
(
utility
+
[
imgfilename
]
)
        
if
is_structured_log
:
            
log
.
process_exit
(
utilityname
returncode
)
        
else
:
            
printstatus
(
utilityname
returncode
)
    
except
OSError
as
err
:
        
log
.
info
(
"
Failed
to
start
%
s
for
screenshot
:
%
s
"
                 
%
(
utility
[
0
]
err
.
strerror
)
)
