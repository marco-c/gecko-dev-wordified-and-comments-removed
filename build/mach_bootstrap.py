from
__future__
import
print_function
unicode_literals
import
errno
import
json
import
os
import
platform
import
subprocess
import
sys
import
uuid
import
__builtin__
from
types
import
ModuleType
STATE_DIR_FIRST_RUN
=
'
'
'
mach
and
the
build
system
store
shared
state
in
a
common
directory
on
the
filesystem
.
The
following
directory
will
be
created
:
  
{
userdir
}
If
you
would
like
to
use
a
different
directory
hit
CTRL
+
c
and
set
the
MOZBUILD_STATE_PATH
environment
variable
to
the
directory
you
would
like
to
use
and
re
-
run
mach
.
For
this
change
to
take
effect
forever
you
'
ll
likely
want
to
export
this
environment
variable
from
your
shell
'
s
init
scripts
.
Press
ENTER
/
RETURN
to
continue
or
CTRL
+
c
to
abort
.
'
'
'
.
lstrip
(
)
MACH_MODULES
=
[
    
'
build
/
valgrind
/
mach_commands
.
py
'
    
'
devtools
/
shared
/
css
/
generated
/
mach_commands
.
py
'
    
'
dom
/
bindings
/
mach_commands
.
py
'
    
'
layout
/
tools
/
reftest
/
mach_commands
.
py
'
    
'
python
/
mach_commands
.
py
'
    
'
python
/
safety
/
mach_commands
.
py
'
    
'
python
/
mach
/
mach
/
commands
/
commandinfo
.
py
'
    
'
python
/
mach
/
mach
/
commands
/
settings
.
py
'
    
'
python
/
mozboot
/
mozboot
/
mach_commands
.
py
'
    
'
python
/
mozbuild
/
mozbuild
/
mach_commands
.
py
'
    
'
python
/
mozbuild
/
mozbuild
/
backend
/
mach_commands
.
py
'
    
'
python
/
mozbuild
/
mozbuild
/
compilation
/
codecomplete
.
py
'
    
'
python
/
mozbuild
/
mozbuild
/
frontend
/
mach_commands
.
py
'
    
'
python
/
mozrelease
/
mozrelease
/
mach_commands
.
py
'
    
'
taskcluster
/
mach_commands
.
py
'
    
'
testing
/
awsy
/
mach_commands
.
py
'
    
'
testing
/
firefox
-
ui
/
mach_commands
.
py
'
    
'
testing
/
geckodriver
/
mach_commands
.
py
'
    
'
testing
/
mach_commands
.
py
'
    
'
testing
/
marionette
/
mach_commands
.
py
'
    
'
testing
/
mochitest
/
mach_commands
.
py
'
    
'
testing
/
mozharness
/
mach_commands
.
py
'
    
'
testing
/
raptor
/
mach_commands
.
py
'
    
'
testing
/
tps
/
mach_commands
.
py
'
    
'
testing
/
talos
/
mach_commands
.
py
'
    
'
testing
/
web
-
platform
/
mach_commands
.
py
'
    
'
testing
/
xpcshell
/
mach_commands
.
py
'
    
'
tools
/
compare
-
locales
/
mach_commands
.
py
'
    
'
tools
/
docs
/
mach_commands
.
py
'
    
'
tools
/
lint
/
mach_commands
.
py
'
    
'
tools
/
mach_commands
.
py
'
    
'
tools
/
power
/
mach_commands
.
py
'
    
'
tools
/
tryselect
/
mach_commands
.
py
'
    
'
mobile
/
android
/
mach_commands
.
py
'
]
CATEGORIES
=
{
    
'
build
'
:
{
        
'
short
'
:
'
Build
Commands
'
        
'
long
'
:
'
Interact
with
the
build
system
'
        
'
priority
'
:
80
    
}
    
'
post
-
build
'
:
{
        
'
short
'
:
'
Post
-
build
Commands
'
        
'
long
'
:
'
Common
actions
performed
after
completing
a
build
.
'
        
'
priority
'
:
70
    
}
    
'
testing
'
:
{
        
'
short
'
:
'
Testing
'
        
'
long
'
:
'
Run
tests
.
'
        
'
priority
'
:
60
    
}
    
'
ci
'
:
{
        
'
short
'
:
'
CI
'
        
'
long
'
:
'
Taskcluster
commands
'
        
'
priority
'
:
59
    
}
    
'
devenv
'
:
{
        
'
short
'
:
'
Development
Environment
'
        
'
long
'
:
'
Set
up
and
configure
your
development
environment
.
'
        
'
priority
'
:
50
    
}
    
'
build
-
dev
'
:
{
        
'
short
'
:
'
Low
-
level
Build
System
Interaction
'
        
'
long
'
:
'
Interact
with
specific
parts
of
the
build
system
.
'
        
'
priority
'
:
20
    
}
    
'
misc
'
:
{
        
'
short
'
:
'
Potpourri
'
        
'
long
'
:
'
Potent
potables
and
assorted
snacks
.
'
        
'
priority
'
:
10
    
}
    
'
release
'
:
{
        
'
short
'
:
'
Release
automation
'
        
'
long
'
:
'
Commands
for
used
in
release
automation
.
'
        
'
priority
'
:
5
    
}
    
'
disabled
'
:
{
        
'
short
'
:
'
Disabled
'
        
'
long
'
:
'
The
disabled
commands
are
hidden
by
default
.
Use
-
v
to
display
them
.
'
        
'
These
commands
are
unavailable
for
your
current
context
'
        
'
run
"
mach
<
command
>
"
to
see
why
.
'
        
'
priority
'
:
0
    
}
}
def
search_path
(
mozilla_dir
packages_txt
)
:
    
with
open
(
os
.
path
.
join
(
mozilla_dir
packages_txt
)
)
as
f
:
        
packages
=
[
line
.
rstrip
(
)
.
split
(
'
:
'
)
for
line
in
f
]
    
def
handle_package
(
package
)
:
        
if
package
[
0
]
=
=
'
optional
'
:
            
try
:
                
for
path
in
handle_package
(
package
[
1
:
]
)
:
                    
yield
path
            
except
Exception
:
                
pass
        
if
package
[
0
]
in
(
'
windows
'
'
!
windows
'
)
:
            
for_win
=
not
package
[
0
]
.
startswith
(
'
!
'
)
            
is_win
=
sys
.
platform
=
=
'
win32
'
            
if
is_win
=
=
for_win
:
                
for
path
in
handle_package
(
package
[
1
:
]
)
:
                    
yield
path
        
if
package
[
0
]
in
(
'
python2
'
'
python3
'
)
:
            
for_python3
=
package
[
0
]
.
endswith
(
'
3
'
)
            
is_python3
=
sys
.
version_info
[
0
]
>
2
            
if
is_python3
=
=
for_python3
:
                
for
path
in
handle_package
(
package
[
1
:
]
)
:
                    
yield
path
        
if
package
[
0
]
=
=
'
packages
.
txt
'
:
            
assert
len
(
package
)
=
=
2
            
for
p
in
search_path
(
mozilla_dir
package
[
1
]
)
:
                
yield
os
.
path
.
join
(
mozilla_dir
p
)
        
if
package
[
0
]
.
endswith
(
'
.
pth
'
)
:
            
assert
len
(
package
)
=
=
2
            
yield
os
.
path
.
join
(
mozilla_dir
package
[
1
]
)
    
for
package
in
packages
:
        
for
path
in
handle_package
(
package
)
:
            
yield
path
def
bootstrap
(
topsrcdir
mozilla_dir
=
None
)
:
    
if
mozilla_dir
is
None
:
        
mozilla_dir
=
topsrcdir
    
if
sys
.
version_info
[
0
]
!
=
2
or
sys
.
version_info
[
1
]
<
7
:
        
print
(
'
Python
2
.
7
or
above
(
but
not
Python
3
)
is
required
to
run
mach
.
'
)
        
print
(
'
You
are
running
Python
'
platform
.
python_version
(
)
)
        
sys
.
exit
(
1
)
    
sys
.
path
[
0
:
0
]
=
[
os
.
path
.
join
(
mozilla_dir
path
)
                     
for
path
in
search_path
(
mozilla_dir
                                             
'
build
/
virtualenv_packages
.
txt
'
)
]
    
import
mach
.
base
    
import
mach
.
main
    
from
mozboot
.
util
import
get_state_dir
    
from
mozbuild
.
util
import
patch_main
    
patch_main
(
)
    
def
resolve_repository
(
)
:
        
import
mozversioncontrol
        
try
:
            
return
mozversioncontrol
.
get_repository_object
(
path
=
mozilla_dir
)
        
except
(
mozversioncontrol
.
InvalidRepoPath
                
mozversioncontrol
.
MissingVCSTool
)
:
            
return
None
    
def
should_skip_telemetry_submission
(
handler
)
:
        
if
handler
.
name
in
(
'
bootstrap
'
'
doctor
'
'
mach
-
commands
'
'
vcs
-
setup
'
                            
'
environment
'
)
:
            
return
True
        
if
any
(
e
in
os
.
environ
for
e
in
(
'
MOZ_AUTOMATION
'
'
TASK_ID
'
'
MACH_TELEMETRY_NO_SUBMIT
'
)
)
:
            
return
True
        
return
False
    
def
post_dispatch_handler
(
context
handler
instance
result
                              
start_time
end_time
depth
args
)
:
        
"
"
"
Perform
global
operations
after
command
dispatch
.
        
For
now
we
will
use
this
to
handle
build
system
telemetry
.
        
"
"
"
        
if
depth
!
=
1
or
os
.
environ
.
get
(
'
MACH_MAIN_PID
'
)
!
=
str
(
os
.
getpid
(
)
)
:
            
return
        
if
os
.
environ
.
get
(
'
DISABLE_TELEMETRY
'
)
=
=
'
1
'
:
            
return
        
if
not
context
.
settings
.
build
.
telemetry
:
            
return
        
from
mozbuild
.
telemetry
import
gather_telemetry
        
from
mozbuild
.
base
import
MozbuildObject
        
import
mozpack
.
path
as
mozpath
        
if
not
isinstance
(
instance
MozbuildObject
)
:
            
instance
=
MozbuildObject
.
from_environment
(
)
        
try
:
            
substs
=
instance
.
substs
        
except
Exception
:
            
substs
=
{
}
        
paths
=
{
            
instance
.
topsrcdir
:
'
topsrcdir
/
'
            
instance
.
topobjdir
:
'
topobjdir
/
'
            
mozpath
.
normpath
(
os
.
path
.
expanduser
(
'
~
'
)
)
:
'
HOME
/
'
        
}
        
paths
[
mozpath
.
normpath
(
os
.
getcwd
(
)
)
]
=
'
'
        
data
=
gather_telemetry
(
command
=
handler
.
name
success
=
(
result
=
=
0
)
                                
start_time
=
start_time
end_time
=
end_time
                                
mach_context
=
context
substs
=
substs
                                
paths
=
paths
)
        
if
data
:
            
telemetry_dir
=
os
.
path
.
join
(
get_state_dir
(
)
'
telemetry
'
)
            
try
:
                
os
.
mkdir
(
telemetry_dir
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
EEXIST
:
                    
raise
            
outgoing_dir
=
os
.
path
.
join
(
telemetry_dir
'
outgoing
'
)
            
try
:
                
os
.
mkdir
(
outgoing_dir
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
EEXIST
:
                    
raise
            
with
open
(
os
.
path
.
join
(
outgoing_dir
str
(
uuid
.
uuid4
(
)
)
+
'
.
json
'
)
                      
'
w
'
)
as
f
:
                
json
.
dump
(
data
f
sort_keys
=
True
)
        
if
should_skip_telemetry_submission
(
handler
)
:
            
return
True
        
state_dir
=
get_state_dir
(
)
        
machpath
=
os
.
path
.
join
(
instance
.
topsrcdir
'
mach
'
)
        
with
open
(
os
.
devnull
'
wb
'
)
as
devnull
:
            
subprocess
.
Popen
(
[
sys
.
executable
machpath
'
python
'
                              
'
-
-
no
-
virtualenv
'
                              
os
.
path
.
join
(
topsrcdir
'
build
'
                                           
'
submit_telemetry_data
.
py
'
)
                              
state_dir
]
                             
stdout
=
devnull
stderr
=
devnull
)
    
def
populate_context
(
context
key
=
None
)
:
        
if
key
is
None
:
            
return
        
if
key
=
=
'
state_dir
'
:
            
state_dir
=
get_state_dir
(
)
            
if
state_dir
=
=
os
.
environ
.
get
(
'
MOZBUILD_STATE_PATH
'
)
:
                
if
not
os
.
path
.
exists
(
state_dir
)
:
                    
print
(
'
Creating
global
state
directory
from
environment
variable
:
%
s
'
                          
%
state_dir
)
                    
os
.
makedirs
(
state_dir
mode
=
0o770
)
            
else
:
                
if
not
os
.
path
.
exists
(
state_dir
)
:
                    
if
not
os
.
environ
.
get
(
'
MOZ_AUTOMATION
'
)
:
                        
print
(
STATE_DIR_FIRST_RUN
.
format
(
userdir
=
state_dir
)
)
                        
try
:
                            
sys
.
stdin
.
readline
(
)
                        
except
KeyboardInterrupt
:
                            
sys
.
exit
(
1
)
                    
print
(
'
\
nCreating
default
state
directory
:
%
s
'
%
state_dir
)
                    
os
.
makedirs
(
state_dir
mode
=
0o770
)
            
return
state_dir
        
if
key
=
=
'
local_state_dir
'
:
            
return
get_state_dir
(
srcdir
=
True
)
        
if
key
=
=
'
topdir
'
:
            
return
topsrcdir
        
if
key
=
=
'
post_dispatch_handler
'
:
            
return
post_dispatch_handler
        
if
key
=
=
'
repository
'
:
            
return
resolve_repository
(
)
        
raise
AttributeError
(
key
)
    
if
'
MACH_MAIN_PID
'
not
in
os
.
environ
:
        
os
.
environ
[
b
'
MACH_MAIN_PID
'
]
=
str
(
os
.
getpid
(
)
)
.
encode
(
'
ascii
'
)
    
driver
=
mach
.
main
.
Mach
(
os
.
getcwd
(
)
)
    
driver
.
populate_context_handler
=
populate_context
    
if
not
driver
.
settings_paths
:
        
driver
.
settings_paths
.
append
(
get_state_dir
(
)
)
    
driver
.
settings_paths
.
append
(
mozilla_dir
)
    
for
category
meta
in
CATEGORIES
.
items
(
)
:
        
driver
.
define_category
(
category
meta
[
'
short
'
]
meta
[
'
long
'
]
                               
meta
[
'
priority
'
]
)
    
repo
=
resolve_repository
(
)
    
for
path
in
MACH_MODULES
:
        
try
:
            
driver
.
load_commands_from_file
(
os
.
path
.
join
(
mozilla_dir
path
)
)
        
except
mach
.
base
.
MissingFileError
:
            
if
not
repo
or
not
repo
.
sparse_checkout_present
(
)
:
                
raise
    
return
driver
class
ImportHook
(
object
)
:
    
def
__init__
(
self
original_import
)
:
        
self
.
_original_import
=
original_import
        
self
.
_source_dir
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
            
os
.
path
.
dirname
(
os
.
path
.
dirname
(
__file__
)
)
)
)
+
os
.
sep
        
self
.
_modules
=
set
(
)
    
def
__call__
(
self
name
globals
=
None
locals
=
None
fromlist
=
None
                 
level
=
-
1
)
:
        
module
=
self
.
_original_import
(
name
globals
locals
fromlist
level
)
        
if
not
isinstance
(
module
ModuleType
)
:
            
return
module
        
resolved_name
=
module
.
__name__
        
if
resolved_name
in
self
.
_modules
:
            
return
module
        
self
.
_modules
.
add
(
resolved_name
)
        
if
not
hasattr
(
module
'
__file__
'
)
:
            
return
module
        
path
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
module
.
__file__
)
)
        
if
not
path
.
endswith
(
(
'
.
pyc
'
'
.
pyo
'
)
)
:
            
return
module
        
if
not
path
.
startswith
(
self
.
_source_dir
)
:
            
return
module
        
if
not
os
.
path
.
exists
(
module
.
__file__
[
:
-
1
]
)
:
            
if
os
.
path
.
exists
(
module
.
__file__
)
:
                
os
.
remove
(
module
.
__file__
)
            
del
sys
.
modules
[
module
.
__name__
]
            
module
=
self
(
name
globals
locals
fromlist
level
)
        
return
module
__builtin__
.
__import__
=
ImportHook
(
__builtin__
.
__import__
)
