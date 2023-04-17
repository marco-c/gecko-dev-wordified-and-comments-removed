from
__future__
import
division
print_function
unicode_literals
import
math
import
os
import
platform
import
shutil
import
site
import
sys
if
sys
.
version_info
[
0
]
<
3
:
    
import
__builtin__
as
builtins
    
class
MetaPathFinder
(
object
)
:
        
pass
else
:
    
from
importlib
.
abc
import
MetaPathFinder
from
types
import
ModuleType
STATE_DIR_FIRST_RUN
=
"
"
"
Mach
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
set
the
MOZBUILD_STATE_PATH
environment
variable
to
the
directory
you
'
d
like
to
use
and
run
Mach
again
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
"
"
"
.
strip
(
)
MACH_MODULES
=
[
    
"
build
/
valgrind
/
mach_commands
.
py
"
    
"
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
"
    
"
dom
/
bindings
/
mach_commands
.
py
"
    
"
js
/
src
/
devtools
/
rootAnalysis
/
mach_commands
.
py
"
    
"
layout
/
tools
/
reftest
/
mach_commands
.
py
"
    
"
mobile
/
android
/
mach_commands
.
py
"
    
"
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
"
    
"
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
"
    
"
python
/
mach_commands
.
py
"
    
"
python
/
mozboot
/
mozboot
/
mach_commands
.
py
"
    
"
python
/
mozbuild
/
mozbuild
/
artifact_commands
.
py
"
    
"
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
"
    
"
python
/
mozbuild
/
mozbuild
/
build_commands
.
py
"
    
"
python
/
mozbuild
/
mozbuild
/
code_analysis
/
mach_commands
.
py
"
    
"
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
"
    
"
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
"
    
"
python
/
mozbuild
/
mozbuild
/
vendor
/
mach_commands
.
py
"
    
"
python
/
mozbuild
/
mozbuild
/
mach_commands
.
py
"
    
"
python
/
mozperftest
/
mozperftest
/
mach_commands
.
py
"
    
"
python
/
mozrelease
/
mozrelease
/
mach_commands
.
py
"
    
"
remote
/
mach_commands
.
py
"
    
"
security
/
manager
/
tools
/
mach_commands
.
py
"
    
"
taskcluster
/
mach_commands
.
py
"
    
"
testing
/
awsy
/
mach_commands
.
py
"
    
"
testing
/
condprofile
/
mach_commands
.
py
"
    
"
testing
/
firefox
-
ui
/
mach_commands
.
py
"
    
"
testing
/
geckodriver
/
mach_commands
.
py
"
    
"
testing
/
mach_commands
.
py
"
    
"
testing
/
marionette
/
mach_commands
.
py
"
    
"
testing
/
mochitest
/
mach_commands
.
py
"
    
"
testing
/
mozharness
/
mach_commands
.
py
"
    
"
testing
/
raptor
/
mach_commands
.
py
"
    
"
testing
/
talos
/
mach_commands
.
py
"
    
"
testing
/
tps
/
mach_commands
.
py
"
    
"
testing
/
web
-
platform
/
mach_commands
.
py
"
    
"
testing
/
xpcshell
/
mach_commands
.
py
"
    
"
toolkit
/
components
/
telemetry
/
tests
/
marionette
/
mach_commands
.
py
"
    
"
toolkit
/
components
/
glean
/
build_scripts
/
mach_commands
.
py
"
    
"
tools
/
browsertime
/
mach_commands
.
py
"
    
"
tools
/
compare
-
locales
/
mach_commands
.
py
"
    
"
tools
/
lint
/
mach_commands
.
py
"
    
"
tools
/
mach_commands
.
py
"
    
"
tools
/
moztreedocs
/
mach_commands
.
py
"
    
"
tools
/
phabricator
/
mach_commands
.
py
"
    
"
tools
/
power
/
mach_commands
.
py
"
    
"
tools
/
tryselect
/
mach_commands
.
py
"
    
"
tools
/
vcs
/
mach_commands
.
py
"
]
CATEGORIES
=
{
    
"
build
"
:
{
        
"
short
"
:
"
Build
Commands
"
        
"
long
"
:
"
Interact
with
the
build
system
"
        
"
priority
"
:
80
    
}
    
"
post
-
build
"
:
{
        
"
short
"
:
"
Post
-
build
Commands
"
        
"
long
"
:
"
Common
actions
performed
after
completing
a
build
.
"
        
"
priority
"
:
70
    
}
    
"
testing
"
:
{
        
"
short
"
:
"
Testing
"
        
"
long
"
:
"
Run
tests
.
"
        
"
priority
"
:
60
    
}
    
"
ci
"
:
{
        
"
short
"
:
"
CI
"
        
"
long
"
:
"
Taskcluster
commands
"
        
"
priority
"
:
59
    
}
    
"
devenv
"
:
{
        
"
short
"
:
"
Development
Environment
"
        
"
long
"
:
"
Set
up
and
configure
your
development
environment
.
"
        
"
priority
"
:
50
    
}
    
"
build
-
dev
"
:
{
        
"
short
"
:
"
Low
-
level
Build
System
Interaction
"
        
"
long
"
:
"
Interact
with
specific
parts
of
the
build
system
.
"
        
"
priority
"
:
20
    
}
    
"
misc
"
:
{
        
"
short
"
:
"
Potpourri
"
        
"
long
"
:
"
Potent
potables
and
assorted
snacks
.
"
        
"
priority
"
:
10
    
}
    
"
release
"
:
{
        
"
short
"
:
"
Release
automation
"
        
"
long
"
:
"
Commands
for
used
in
release
automation
.
"
        
"
priority
"
:
5
    
}
    
"
disabled
"
:
{
        
"
short
"
:
"
Disabled
"
        
"
long
"
:
"
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
"
        
"
These
commands
are
unavailable
for
your
current
context
"
        
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
        
"
priority
"
:
0
    
}
}
INSTALL_PYTHON_GUIDANCE_LINUX
=
"
"
"
See
https
:
/
/
firefox
-
source
-
docs
.
mozilla
.
org
/
setup
/
linux_build
.
html
#
installingpython
for
guidance
on
how
to
install
Python
on
your
system
.
"
"
"
.
strip
(
)
INSTALL_PYTHON_GUIDANCE_OSX
=
"
"
"
See
https
:
/
/
firefox
-
source
-
docs
.
mozilla
.
org
/
setup
/
macos_build
.
html
for
guidance
on
how
to
prepare
your
system
to
build
Firefox
.
Perhaps
you
need
to
update
Xcode
or
install
Python
using
brew
?
"
"
"
.
strip
(
)
INSTALL_PYTHON_GUIDANCE_MOZILLABUILD
=
"
"
"
Python
is
provided
by
MozillaBuild
;
ensure
your
MozillaBuild
installation
is
up
to
date
.
See
https
:
/
/
firefox
-
source
-
docs
.
mozilla
.
org
/
setup
/
windows_build
.
html
#
install
-
mozillabuild
for
details
.
"
"
"
.
strip
(
)
INSTALL_PYTHON_GUIDANCE_OTHER
=
"
"
"
We
do
not
have
specific
instructions
for
your
platform
on
how
to
install
Python
.
You
may
find
Pyenv
(
https
:
/
/
github
.
com
/
pyenv
/
pyenv
)
helpful
if
your
system
package
manager
does
not
provide
a
way
to
install
a
recent
enough
Python
3
.
"
"
"
.
strip
(
)
def
_activate_python_environment
(
topsrcdir
)
:
    
sys
.
path
.
insert
(
0
os
.
path
.
join
(
topsrcdir
"
python
"
"
mach
"
)
)
    
from
mach
.
requirements
import
MachEnvRequirements
    
thunderbird_dir
=
os
.
path
.
join
(
topsrcdir
"
comm
"
)
    
is_thunderbird
=
os
.
path
.
exists
(
thunderbird_dir
)
and
bool
(
        
os
.
listdir
(
thunderbird_dir
)
    
)
    
requirements
=
MachEnvRequirements
.
from_requirements_definition
(
        
topsrcdir
        
is_thunderbird
        
os
.
path
.
join
(
topsrcdir
"
build
"
"
mach_virtualenv_packages
.
txt
"
)
    
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
topsrcdir
pth
.
path
)
for
pth
in
requirements
.
pth_requirements
    
]
def
initialize
(
topsrcdir
)
:
    
if
sys
.
version_info
<
(
3
6
)
:
        
print
(
"
Python
3
.
6
+
is
required
to
run
mach
.
"
)
        
print
(
"
You
are
running
Python
"
platform
.
python_version
(
)
)
        
if
sys
.
platform
.
startswith
(
"
linux
"
)
:
            
print
(
INSTALL_PYTHON_GUIDANCE_LINUX
)
        
elif
sys
.
platform
.
startswith
(
"
darwin
"
)
:
            
print
(
INSTALL_PYTHON_GUIDANCE_OSX
)
        
elif
"
MOZILLABUILD
"
in
os
.
environ
:
            
print
(
INSTALL_PYTHON_GUIDANCE_MOZILLABUILD
)
        
else
:
            
print
(
INSTALL_PYTHON_GUIDANCE_OTHER
)
        
sys
.
exit
(
1
)
    
deleted_dir
=
os
.
path
.
join
(
topsrcdir
"
third_party
"
"
python
"
"
psutil
"
)
    
if
os
.
path
.
exists
(
deleted_dir
)
:
        
shutil
.
rmtree
(
deleted_dir
ignore_errors
=
True
)
    
if
sys
.
prefix
=
=
sys
.
base_prefix
:
        
site_paths
=
set
(
site
.
getsitepackages
(
)
+
[
site
.
getusersitepackages
(
)
]
)
        
sys
.
path
=
[
path
for
path
in
sys
.
path
if
path
not
in
site_paths
]
    
state_dir
=
_create_state_dir
(
)
    
_activate_python_environment
(
topsrcdir
)
    
import
mach
.
base
    
import
mach
.
main
    
from
mach
.
util
import
setenv
    
from
mozboot
.
util
import
get_state_dir
    
try
:
        
import
resource
        
(
soft
hard
)
=
resource
.
getrlimit
(
resource
.
RLIMIT_NOFILE
)
        
limit
=
os
.
environ
.
get
(
"
MOZ_LIMIT_NOFILE
"
)
        
if
limit
:
            
limit
=
int
(
limit
)
        
else
:
            
limit
=
min
(
soft
8192
)
        
if
limit
!
=
soft
:
            
resource
.
setrlimit
(
resource
.
RLIMIT_NOFILE
(
limit
hard
)
)
    
except
ImportError
:
        
pass
    
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
topsrcdir
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
pre_dispatch_handler
(
context
handler
args
)
:
        
if
handler
.
category
=
=
"
testing
"
and
not
handler
.
ok_if_tests_disabled
:
            
from
mozbuild
.
base
import
BuildEnvironmentNotFoundException
            
try
:
                
from
mozbuild
.
base
import
MozbuildObject
                
build
=
MozbuildObject
.
from_environment
(
)
                
if
build
is
not
None
and
hasattr
(
build
"
mozconfig
"
)
:
                    
ac_options
=
build
.
mozconfig
[
"
configure_args
"
]
                    
if
ac_options
and
"
-
-
disable
-
tests
"
in
ac_options
:
                        
print
(
                            
"
Tests
have
been
disabled
by
mozconfig
with
the
flag
"
                            
+
'
"
ac_add_options
-
-
disable
-
tests
"
.
\
n
'
                            
+
"
Remove
the
flag
and
re
-
compile
to
enable
tests
.
"
                        
)
                        
sys
.
exit
(
1
)
            
except
BuildEnvironmentNotFoundException
:
                
pass
    
def
post_dispatch_handler
(
        
context
handler
instance
success
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
:
            
return
        
_finalize_telemetry_glean
(
            
context
.
telemetry
handler
.
name
=
=
"
bootstrap
"
success
        
)
    
def
populate_context
(
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
"
state_dir
"
:
            
return
state_dir
        
if
key
=
=
"
local_state_dir
"
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
"
topdir
"
:
            
return
topsrcdir
        
if
key
=
=
"
pre_dispatch_handler
"
:
            
return
pre_dispatch_handler
        
if
key
=
=
"
post_dispatch_handler
"
:
            
return
post_dispatch_handler
        
if
key
=
=
"
repository
"
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
"
MACH_MAIN_PID
"
not
in
os
.
environ
:
        
setenv
(
"
MACH_MAIN_PID
"
str
(
os
.
getpid
(
)
)
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
state_dir
)
    
driver
.
settings_paths
.
append
(
topsrcdir
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
"
short
"
]
meta
[
"
long
"
]
meta
[
"
priority
"
]
)
    
repo
=
resolve_repository
(
)
    
missing_ok
=
(
        
repo
is
not
None
and
repo
.
sparse_checkout_present
(
)
    
)
or
os
.
path
.
exists
(
os
.
path
.
join
(
topsrcdir
"
INSTALL
"
)
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
topsrcdir
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
missing_ok
:
                
raise
    
return
driver
def
_finalize_telemetry_glean
(
telemetry
is_bootstrap
success
)
:
    
"
"
"
Submit
telemetry
collected
by
Glean
.
    
Finalizes
some
metrics
(
command
success
state
and
duration
system
information
)
and
    
requests
Glean
to
send
the
collected
data
.
    
"
"
"
    
from
mach
.
telemetry
import
MACH_METRICS_PATH
    
from
mozbuild
.
telemetry
import
(
        
get_cpu_brand
        
get_distro_and_version
        
get_psutil_stats
        
get_shell_info
        
get_vscode_running
    
)
    
mach_metrics
=
telemetry
.
metrics
(
MACH_METRICS_PATH
)
    
mach_metrics
.
mach
.
duration
.
stop
(
)
    
mach_metrics
.
mach
.
success
.
set
(
success
)
    
system_metrics
=
mach_metrics
.
mach
.
system
    
cpu_brand
=
get_cpu_brand
(
)
    
if
cpu_brand
:
        
system_metrics
.
cpu_brand
.
set
(
cpu_brand
)
    
distro
version
=
get_distro_and_version
(
)
    
system_metrics
.
distro
.
set
(
distro
)
    
system_metrics
.
distro_version
.
set
(
version
)
    
vscode_terminal
ssh_connection
=
get_shell_info
(
)
    
system_metrics
.
vscode_terminal
.
set
(
vscode_terminal
)
    
system_metrics
.
ssh_connection
.
set
(
ssh_connection
)
    
system_metrics
.
vscode_running
.
set
(
get_vscode_running
(
)
)
    
has_psutil
logical_cores
physical_cores
memory_total
=
get_psutil_stats
(
)
    
if
has_psutil
:
        
system_metrics
.
logical_cores
.
add
(
logical_cores
)
        
system_metrics
.
physical_cores
.
add
(
physical_cores
)
        
if
memory_total
is
not
None
:
            
system_metrics
.
memory
.
accumulate
(
                
int
(
math
.
ceil
(
float
(
memory_total
)
/
(
1024
*
1024
*
1024
)
)
)
            
)
    
telemetry
.
submit
(
is_bootstrap
)
def
_create_state_dir
(
)
:
    
state_dir
=
os
.
environ
.
get
(
"
MOZBUILD_STATE_PATH
"
)
    
if
state_dir
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
                
"
Creating
global
state
directory
from
environment
variable
:
{
}
"
.
format
(
                    
state_dir
                
)
            
)
    
else
:
        
state_dir
=
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
"
MOZ_AUTOMATION
"
)
:
                
print
(
STATE_DIR_FIRST_RUN
.
format
(
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
                    
print
(
"
\
n
"
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
"
Creating
default
state
directory
:
{
}
"
.
format
(
state_dir
)
)
    
os
.
makedirs
(
state_dir
mode
=
0o770
exist_ok
=
True
)
    
return
state_dir
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
(
            
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
        
)
        
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
        
if
sys
.
version_info
[
0
]
>
=
3
and
level
<
0
:
            
level
=
0
        
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
getattr
(
module
"
__file__
"
None
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
"
.
pyc
"
"
.
pyo
"
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
class
FinderHook
(
MetaPathFinder
)
:
    
def
__init__
(
self
klass
)
:
        
self
.
_source_dir
=
(
            
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
        
)
        
self
.
finder_class
=
klass
    
def
find_spec
(
self
full_name
paths
=
None
target
=
None
)
:
        
spec
=
self
.
finder_class
.
find_spec
(
full_name
paths
target
)
        
if
spec
is
None
or
spec
.
origin
is
None
:
            
return
spec
        
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
spec
.
origin
)
)
        
if
not
path
.
endswith
(
(
"
.
pyc
"
"
.
pyo
"
)
)
:
            
return
spec
        
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
spec
        
if
not
os
.
path
.
exists
(
spec
.
origin
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
spec
.
origin
)
:
                
os
.
remove
(
spec
.
origin
)
            
spec
=
self
.
finder_class
.
find_spec
(
full_name
paths
target
)
        
return
spec
class
MetadataHook
(
FinderHook
)
:
    
def
find_distributions
(
self
*
args
*
*
kwargs
)
:
        
return
self
.
finder_class
.
find_distributions
(
*
args
*
*
kwargs
)
def
hook
(
finder
)
:
    
has_find_spec
=
hasattr
(
finder
"
find_spec
"
)
    
has_find_distributions
=
hasattr
(
finder
"
find_distributions
"
)
    
if
has_find_spec
and
has_find_distributions
:
        
return
MetadataHook
(
finder
)
    
elif
has_find_spec
:
        
return
FinderHook
(
finder
)
    
return
finder
if
sys
.
version_info
[
0
]
<
3
:
    
builtins
.
__import__
=
ImportHook
(
builtins
.
__import__
)
else
:
    
sys
.
meta_path
=
[
hook
(
c
)
for
c
in
sys
.
meta_path
]
