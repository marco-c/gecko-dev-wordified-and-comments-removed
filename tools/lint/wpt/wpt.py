import
json
import
os
import
sys
from
mozlint
import
result
from
mozprocess
import
ProcessHandler
results
=
[
]
def
lint
(
files
config
*
*
kwargs
)
:
    
log
=
kwargs
[
"
log
"
]
    
tests_dir
=
os
.
path
.
join
(
kwargs
[
"
root
"
]
"
testing
"
"
web
-
platform
"
"
tests
"
)
    
def
process_line
(
line
)
:
        
try
:
            
data
=
json
.
loads
(
line
)
        
except
ValueError
:
            
return
        
data
[
"
level
"
]
=
"
error
"
        
data
[
"
path
"
]
=
os
.
path
.
relpath
(
            
os
.
path
.
join
(
tests_dir
data
[
"
path
"
]
)
kwargs
[
"
root
"
]
        
)
        
data
.
setdefault
(
"
lineno
"
0
)
        
results
.
append
(
result
.
from_config
(
config
*
*
data
)
)
    
if
files
=
=
[
tests_dir
]
:
        
print
(
            
"
No
specific
files
specified
running
the
full
wpt
lint
"
"
(
this
is
slow
)
"
            
file
=
sys
.
stderr
        
)
        
files
=
[
"
-
-
all
"
]
    
cmd
=
[
"
python3
"
os
.
path
.
join
(
tests_dir
"
wpt
"
)
"
lint
"
"
-
-
json
"
]
+
files
    
log
.
debug
(
"
Command
:
{
}
"
.
format
(
"
"
.
join
(
cmd
)
)
)
    
proc
=
ProcessHandler
(
        
cmd
env
=
os
.
environ
processOutputLine
=
process_line
universal_newlines
=
True
    
)
    
proc
.
run
(
)
    
try
:
        
proc
.
wait
(
)
        
if
proc
.
returncode
!
=
0
:
            
results
.
append
(
                
result
.
from_config
(
                    
config
                    
message
=
"
Lint
process
exited
with
return
code
%
s
"
%
proc
.
returncode
                
)
            
)
    
except
KeyboardInterrupt
:
        
proc
.
kill
(
)
    
return
results
