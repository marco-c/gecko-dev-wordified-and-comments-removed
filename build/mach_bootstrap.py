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
random
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
SEARCH_PATHS
=
[
    
'
python
/
mach
'
    
'
python
/
mozboot
'
    
'
python
/
mozbuild
'
    
'
python
/
mozlint
'
    
'
python
/
mozversioncontrol
'
    
'
python
/
blessings
'
    
'
python
/
compare
-
locales
'
    
'
python
/
configobj
'
    
'
python
/
futures
'
    
'
python
/
jsmin
'
    
'
python
/
psutil
'
    
'
python
/
pylru
'
    
'
python
/
which
'
    
'
python
/
pystache
'
    
'
python
/
pyyaml
/
lib
'
    
'
python
/
requests
'
    
'
python
/
slugid
'
    
'
python
/
py
'
    
'
python
/
pytest
'
    
'
python
/
redo
'
    
'
python
/
voluptuous
'
    
'
build
'
    
'
build
/
pymake
'
    
'
config
'
    
'
dom
/
bindings
'
    
'
dom
/
bindings
/
parser
'
    
'
dom
/
media
/
test
/
external
'
    
'
layout
/
tools
/
reftest
'
    
'
other
-
licenses
/
ply
'
    
'
taskcluster
'
    
'
testing
'
    
'
testing
/
firefox
-
ui
/
harness
'
    
'
testing
/
firefox
-
ui
/
tests
'
    
'
testing
/
marionette
/
harness
'
    
'
testing
/
marionette
/
harness
/
marionette
/
runner
/
mixins
/
browsermob
-
proxy
-
py
'
    
'
testing
/
marionette
/
client
'
    
'
testing
/
mozbase
/
mozcrash
'
    
'
testing
/
mozbase
/
mozdebug
'
    
'
testing
/
mozbase
/
mozdevice
'
    
'
testing
/
mozbase
/
mozfile
'
    
'
testing
/
mozbase
/
mozhttpd
'
    
'
testing
/
mozbase
/
mozinfo
'
    
'
testing
/
mozbase
/
mozinstall
'
    
'
testing
/
mozbase
/
mozleak
'
    
'
testing
/
mozbase
/
mozlog
'
    
'
testing
/
mozbase
/
moznetwork
'
    
'
testing
/
mozbase
/
mozprocess
'
    
'
testing
/
mozbase
/
mozprofile
'
    
'
testing
/
mozbase
/
mozrunner
'
    
'
testing
/
mozbase
/
mozsystemmonitor
'
    
'
testing
/
mozbase
/
mozscreenshot
'
    
'
testing
/
mozbase
/
moztest
'
    
'
testing
/
mozbase
/
mozversion
'
    
'
testing
/
mozbase
/
manifestparser
'
    
'
testing
/
puppeteer
/
firefox
'
    
'
testing
/
taskcluster
'
    
'
testing
/
tools
/
autotry
'
    
'
testing
/
web
-
platform
'
    
'
testing
/
web
-
platform
/
harness
'
    
'
testing
/
web
-
platform
/
tests
/
tools
/
wptserve
'
    
'
testing
/
xpcshell
'
    
'
xpcom
/
idl
-
parser
'
]
MACH_MODULES
=
[
    
'
addon
-
sdk
/
mach_commands
.
py
'
    
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
dom
/
media
/
test
/
external
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
compare
-
locales
/
mach_commands
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
services
/
common
/
tests
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
These
commands
are
unavailable
for
your
current
context
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
TELEMETRY_SUBMISSION_FREQUENCY
=
10
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
SEARCH_PATHS
]
    
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
    
def
telemetry_handler
(
context
data
)
:
        
if
'
BUILD_SYSTEM_TELEMETRY
'
not
in
os
.
environ
:
            
return
        
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
[
0
]
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
        
data
[
'
argv
'
]
=
sys
.
argv
        
data
.
setdefault
(
'
system
'
{
}
)
.
update
(
dict
(
            
architecture
=
list
(
platform
.
architecture
(
)
)
            
machine
=
platform
.
machine
(
)
            
python_version
=
platform
.
python_version
(
)
            
release
=
platform
.
release
(
)
            
system
=
platform
.
system
(
)
            
version
=
platform
.
version
(
)
        
)
)
        
if
platform
.
system
(
)
=
=
'
Linux
'
:
            
dist
=
list
(
platform
.
linux_distribution
(
)
)
            
data
[
'
system
'
]
[
'
linux_distribution
'
]
=
dist
        
elif
platform
.
system
(
)
=
=
'
Windows
'
:
            
win32_ver
=
list
(
(
platform
.
win32_ver
(
)
)
)
            
data
[
'
system
'
]
[
'
win32_ver
'
]
=
win32_ver
        
elif
platform
.
system
(
)
=
=
'
Darwin
'
:
            
r
v
m
=
platform
.
mac_ver
(
)
            
data
[
'
system
'
]
[
'
mac_ver
'
]
=
[
r
list
(
v
)
m
]
        
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
    
def
should_skip_dispatch
(
context
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
mercurial
-
setup
'
)
:
            
return
True
        
if
'
MOZ_AUTOMATION
'
in
os
.
environ
or
'
TASK_ID
'
in
os
.
environ
:
            
return
True
        
if
sys
.
stdin
.
closed
or
not
sys
.
stdin
.
isatty
(
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
should_skip_dispatch
(
context
handler
)
:
            
return
        
if
handler
.
name
in
(
'
environment
'
)
:
            
return
        
if
'
BUILD_SYSTEM_TELEMETRY
'
not
in
os
.
environ
:
            
return
        
if
random
.
randint
(
1
TELEMETRY_SUBMISSION_FREQUENCY
)
!
=
1
:
            
return
        
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
                              
get_state_dir
(
)
[
0
]
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
is_environ
=
get_state_dir
(
)
            
if
is_environ
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
telemetry_handler
'
:
            
return
telemetry_handler
        
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
        
raise
AttributeError
(
key
)
    
mach
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
    
mach
.
populate_context_handler
=
populate_context
    
if
not
mach
.
settings_paths
:
        
mach
.
settings_paths
.
append
(
get_state_dir
(
)
[
0
]
)
    
mach
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
        
mach
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
    
for
path
in
MACH_MODULES
:
        
mach
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
    
return
mach
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
