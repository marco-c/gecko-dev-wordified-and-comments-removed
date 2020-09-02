import
platform
import
tempfile
import
subprocess
from
pathlib
import
Path
import
shutil
import
os
from
mozperftest
.
layers
import
Layer
POTENTIAL_DMGS
=
{
    
"
browsertime
-
binary
"
:
"
Contents
/
MacOS
/
firefox
"
    
"
xpcshell
-
xre
-
path
"
:
"
Contents
/
MacOS
"
}
class
MacosDevice
(
Layer
)
:
    
"
"
"
Runs
on
macOS
to
mount
DMGs
if
we
see
one
.
"
"
"
    
name
=
"
macos
"
    
activated
=
platform
.
system
(
)
=
=
"
Darwin
"
    
def
__init__
(
self
env
mach_cmd
)
:
        
super
(
MacosDevice
self
)
.
__init__
(
env
mach_cmd
)
        
self
.
_tmp_dirs
=
[
]
    
def
_run_process
(
self
args
)
:
        
p
=
subprocess
.
Popen
(
            
args
            
stdout
=
subprocess
.
PIPE
            
stderr
=
subprocess
.
PIPE
            
universal_newlines
=
True
        
)
        
stdout
stderr
=
p
.
communicate
(
timeout
=
15
)
        
if
p
.
returncode
!
=
0
:
            
raise
subprocess
.
CalledProcessError
(
                
stdout
=
stdout
stderr
=
stderr
returncode
=
p
.
returncode
            
)
        
return
stdout
    
def
extract_app
(
self
dmg
target
)
:
        
mount
=
Path
(
tempfile
.
mkdtemp
(
)
)
        
cmd
=
f
"
hdiutil
attach
-
nobrowse
-
mountpoint
{
str
(
mount
)
}
{
dmg
}
"
        
try
:
            
self
.
_run_process
(
cmd
.
split
(
)
)
        
except
subprocess
.
CalledProcessError
:
            
self
.
error
(
f
"
Can
'
t
mount
{
dmg
}
"
)
            
if
mount
.
exists
(
)
:
                
shutil
.
rmtree
(
str
(
mount
)
)
            
raise
        
found
=
False
        
try
:
            
for
f
in
os
.
listdir
(
str
(
mount
)
)
:
                
if
not
f
.
endswith
(
"
.
app
"
)
:
                    
continue
                
app
=
mount
/
f
                
shutil
.
copytree
(
str
(
app
)
str
(
target
)
)
                
found
=
True
                
break
        
finally
:
            
try
:
                
self
.
_run_process
(
f
"
hdiutil
detach
{
str
(
mount
)
}
"
.
split
(
)
)
            
except
subprocess
.
CalledProcessError
as
e
:
                
self
.
warning
(
"
Detach
failed
{
e
.
stdout
}
"
)
            
finally
:
                
if
mount
.
exists
(
)
:
                    
shutil
.
rmtree
(
str
(
mount
)
)
        
if
not
found
:
            
self
.
error
(
f
"
No
app
file
found
in
{
dmg
}
"
)
            
raise
IOError
(
dmg
)
    
def
run
(
self
metadata
)
:
        
for
option
path_in_dmg
in
POTENTIAL_DMGS
.
items
(
)
:
            
value
=
self
.
get_arg
(
option
)
            
if
value
is
None
or
not
value
.
endswith
(
"
.
dmg
"
)
:
                
continue
            
self
.
info
(
f
"
Mounting
{
value
}
"
)
            
dmg_file
=
Path
(
value
)
            
if
not
dmg_file
.
exists
(
)
:
                
raise
FileNotFoundError
(
str
(
dmg_file
)
)
            
target
=
dmg_file
.
parent
/
dmg_file
.
name
.
split
(
"
.
"
)
[
0
]
            
self
.
_tmp_dirs
.
append
(
target
)
            
self
.
extract_app
(
dmg_file
target
)
            
path
=
target
/
path_in_dmg
            
if
not
path
.
exists
(
)
:
                
raise
FileNotFoundError
(
str
(
path
)
)
            
self
.
info
(
f
"
Using
{
path
}
for
{
option
}
"
)
            
self
.
env
.
set_arg
(
option
str
(
path
)
)
        
return
metadata
    
def
teardown
(
self
)
:
        
for
dir
in
self
.
_tmp_dirs
:
            
if
dir
.
exists
(
)
:
                
shutil
.
rmtree
(
str
(
dir
)
)
