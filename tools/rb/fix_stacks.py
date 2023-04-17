from
__future__
import
absolute_import
print_function
from
subprocess
import
Popen
PIPE
import
atexit
import
os
import
platform
import
re
import
sys
line_re
=
re
.
compile
(
"
#
\
d
+
:
.
+
\
[
.
+
\
+
0x
[
0
-
9A
-
Fa
-
f
]
+
\
]
"
)
fix_stacks
=
None
def
initFixStacks
(
jsonMode
slowWarning
breakpadSymsDir
hide_errors
)
:
    
base
=
os
.
environ
.
get
(
        
"
MOZ_FETCHES_DIR
"
        
os
.
environ
.
get
(
"
MOZBUILD_STATE_PATH
"
os
.
path
.
expanduser
(
"
~
/
.
mozbuild
"
)
)
    
)
    
fix_stacks_exe
=
base
+
"
/
fix
-
stacks
/
fix
-
stacks
"
    
if
platform
.
system
(
)
=
=
"
Windows
"
:
        
fix_stacks_exe
=
fix_stacks_exe
+
"
.
exe
"
    
if
not
(
os
.
path
.
isfile
(
fix_stacks_exe
)
and
os
.
access
(
fix_stacks_exe
os
.
X_OK
)
)
:
        
raise
Exception
(
"
cannot
find
fix
-
stacks
;
please
run
.
/
mach
bootstrap
"
)
    
args
=
[
fix_stacks_exe
]
    
if
jsonMode
:
        
args
.
append
(
"
-
j
"
)
    
if
breakpadSymsDir
:
        
args
.
append
(
"
-
b
"
)
        
args
.
append
(
breakpadSymsDir
)
    
stderr
=
open
(
os
.
devnull
)
if
hide_errors
else
None
    
global
fix_stacks
    
fix_stacks
=
Popen
(
        
args
stdin
=
PIPE
stdout
=
PIPE
stderr
=
stderr
universal_newlines
=
True
    
)
    
def
cleanup
(
fix_stacks
)
:
        
for
fn
in
[
fix_stacks
.
stdin
.
close
fix_stacks
.
terminate
]
:
            
try
:
                
fn
(
)
            
except
OSError
:
                
pass
    
atexit
.
register
(
cleanup
fix_stacks
)
    
if
slowWarning
:
        
print
(
            
"
Initializing
stack
-
fixing
for
the
first
stack
frame
this
may
take
a
while
.
.
.
"
        
)
def
fixSymbols
(
    
line
jsonMode
=
False
slowWarning
=
False
breakpadSymsDir
=
None
hide_errors
=
False
)
:
    
if
isinstance
(
line
bytes
)
:
        
line_str
=
line
.
decode
(
"
utf
-
8
"
)
    
else
:
        
line_str
=
line
    
if
line_re
.
search
(
line_str
)
is
None
:
        
return
line
    
if
not
fix_stacks
:
        
initFixStacks
(
jsonMode
slowWarning
breakpadSymsDir
hide_errors
)
    
is_missing_newline
=
not
line_str
.
endswith
(
"
\
n
"
)
    
if
is_missing_newline
:
        
line_str
=
line_str
+
"
\
n
"
    
fix_stacks
.
stdin
.
write
(
line_str
)
    
fix_stacks
.
stdin
.
flush
(
)
    
out
=
fix_stacks
.
stdout
.
readline
(
)
    
if
is_missing_newline
:
        
out
=
out
[
:
-
1
]
    
return
bytes
(
out
"
utf
-
8
"
)
if
__name__
=
=
"
__main__
"
:
    
for
line
in
sys
.
stdin
:
        
sys
.
stdout
.
write
(
fixSymbols
(
line
)
)
