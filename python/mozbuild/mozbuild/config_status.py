import
logging
import
os
import
sys
import
time
from
argparse
import
ArgumentParser
from
itertools
import
chain
from
multiprocessing
import
Pool
get_start_method
from
time
import
process_time
from
mach
.
logging
import
LoggingManager
from
mozbuild
.
backend
import
backends
get_backend_class
from
mozbuild
.
backend
.
configenvironment
import
ConfigEnvironment
from
mozbuild
.
base
import
MachCommandConditions
from
mozbuild
.
frontend
.
emitter
import
TreeMetadataEmitter
from
mozbuild
.
frontend
.
reader
import
BuildReader
from
mozbuild
.
mozinfo
import
write_mozinfo
from
mozbuild
.
util
import
FileAvoidWrite
log_manager
=
LoggingManager
(
)
ANDROID_IDE_ADVERTISEMENT
=
"
"
"
=
=
=
=
=
=
=
=
=
=
=
=
=
ADVERTISEMENT
You
are
building
GeckoView
.
After
your
build
completes
you
can
open
the
top
source
directory
in
Android
Studio
directly
and
build
using
Gradle
.
See
the
documentation
at
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
mobile
/
android
/
index
.
html
#
build
-
using
-
android
-
studio
=
=
=
=
=
=
=
=
=
=
=
=
=
"
"
"
.
strip
(
)
class
BackendPool
:
    
per_process_definitions
=
None
    
def
__init__
(
self
definitions
*
processes
=
None
)
:
        
definitions
=
list
(
definitions
)
        
BackendPool
.
_init_worker
(
definitions
)
        
self
.
pool
=
Pool
(
            
initializer
=
BackendPool
.
_init_worker
            
initargs
=
(
definitions
)
            
processes
=
processes
        
)
    
def
run
(
self
backends
)
:
        
async_tasks
=
self
.
pool
.
map_async
(
BackendPool
.
_run_worker
backends
[
1
:
]
)
        
BackendPool
.
_run_worker
(
backends
[
0
]
)
        
async_tasks
.
wait
(
)
    
staticmethod
    
def
_init_worker
(
state
)
:
        
BackendPool
.
per_process_definitions
=
state
    
staticmethod
    
def
_run_worker
(
backend
)
:
        
return
backend
.
consume
(
BackendPool
.
per_process_definitions
)
def
config_status
(
    
topobjdir
=
"
.
"
    
topsrcdir
=
"
.
"
    
defines
=
None
    
substs
=
None
    
source
=
None
    
mozconfig
=
None
    
args
=
sys
.
argv
[
1
:
]
)
:
    
"
"
"
Main
function
providing
config
.
status
functionality
.
    
Contrary
to
config
.
status
it
doesn
'
t
use
CONFIG_FILES
or
CONFIG_HEADERS
    
variables
.
    
Without
the
-
n
option
this
program
acts
as
config
.
status
and
considers
    
the
current
directory
as
the
top
object
directory
even
when
config
.
status
    
is
in
a
different
directory
.
It
will
however
treat
the
directory
    
containing
config
.
status
as
the
top
object
directory
with
the
-
n
option
.
    
The
options
to
this
function
are
passed
when
creating
the
    
ConfigEnvironment
.
These
lists
as
well
as
the
actual
wrapper
script
    
around
this
function
are
meant
to
be
generated
by
configure
.
    
See
build
/
autoconf
/
config
.
status
.
m4
.
    
"
"
"
    
if
"
CONFIG_FILES
"
in
os
.
environ
:
        
raise
Exception
(
"
Using
the
CONFIG_FILES
environment
variable
is
not
supported
.
"
)
    
if
"
CONFIG_HEADERS
"
in
os
.
environ
:
        
raise
Exception
(
            
"
Using
the
CONFIG_HEADERS
environment
variable
is
not
supported
.
"
        
)
    
if
not
os
.
path
.
isabs
(
topsrcdir
)
:
        
raise
Exception
(
            
"
topsrcdir
must
be
defined
as
an
absolute
directory
:
%
s
"
%
topsrcdir
        
)
    
default_backends
=
[
"
RecursiveMake
"
]
    
default_backends
=
(
substs
or
{
}
)
.
get
(
"
BUILD_BACKENDS
"
[
"
RecursiveMake
"
]
)
    
parser
=
ArgumentParser
(
)
    
parser
.
add_argument
(
        
"
-
v
"
        
"
-
-
verbose
"
        
dest
=
"
verbose
"
        
action
=
"
store_true
"
        
help
=
"
display
verbose
output
"
    
)
    
parser
.
add_argument
(
        
"
-
n
"
        
dest
=
"
not_topobjdir
"
        
action
=
"
store_true
"
        
help
=
"
do
not
consider
current
directory
as
top
object
directory
"
    
)
    
parser
.
add_argument
(
        
"
-
d
"
"
-
-
diff
"
action
=
"
store_true
"
help
=
"
print
diffs
of
changed
files
.
"
    
)
    
parser
.
add_argument
(
        
"
-
b
"
        
"
-
-
backend
"
        
nargs
=
"
+
"
        
choices
=
sorted
(
backends
)
        
default
=
default_backends
        
help
=
"
what
backend
to
build
(
default
:
%
s
)
.
"
%
"
"
.
join
(
default_backends
)
    
)
    
parser
.
add_argument
(
        
"
-
-
dry
-
run
"
action
=
"
store_true
"
help
=
"
do
everything
except
writing
files
out
.
"
    
)
    
options
=
parser
.
parse_args
(
args
)
    
if
not
options
.
not_topobjdir
:
        
topobjdir
=
os
.
path
.
realpath
(
"
.
"
)
    
env
=
ConfigEnvironment
(
        
topsrcdir
        
topobjdir
        
defines
=
defines
        
substs
=
substs
        
source
=
source
        
mozconfig
=
mozconfig
    
)
    
with
FileAvoidWrite
(
os
.
path
.
join
(
topobjdir
"
mozinfo
.
json
"
)
)
as
f
:
        
write_mozinfo
(
f
env
os
.
environ
)
    
cpu_start
=
process_time
(
)
    
time_start
=
time
.
monotonic
(
)
    
selected_backends
=
[
get_backend_class
(
b
)
(
env
)
for
b
in
options
.
backend
]
    
if
options
.
dry_run
:
        
for
b
in
selected_backends
:
            
b
.
dry_run
=
True
    
reader
=
BuildReader
(
env
)
    
emitter
=
TreeMetadataEmitter
(
env
)
    
definitions
=
emitter
.
emit
(
reader
.
read_topsrcdir
(
)
)
    
log_level
=
logging
.
DEBUG
if
options
.
verbose
else
logging
.
INFO
    
log_manager
.
add_terminal_logging
(
level
=
log_level
)
    
log_manager
.
enable_unstructured
(
)
    
print
(
"
Reticulating
splines
.
.
.
"
file
=
sys
.
stderr
)
    
if
len
(
selected_backends
)
>
1
and
get_start_method
(
)
=
=
"
fork
"
:
        
processes
=
min
(
len
(
selected_backends
)
-
1
4
)
        
pool
=
BackendPool
(
definitions
processes
=
processes
)
        
pool
.
run
(
selected_backends
)
    
else
:
        
if
len
(
selected_backends
)
>
1
:
            
definitions
=
list
(
definitions
)
        
for
backend
in
selected_backends
:
            
backend
.
consume
(
definitions
)
    
execution_time
=
0
.
0
    
for
obj
in
chain
(
(
reader
emitter
)
selected_backends
)
:
        
summary
=
obj
.
summary
(
)
        
print
(
summary
file
=
sys
.
stderr
)
        
execution_time
+
=
summary
.
execution_time
        
if
hasattr
(
obj
"
gyp_summary
"
)
:
            
summary
=
obj
.
gyp_summary
(
)
            
print
(
summary
file
=
sys
.
stderr
)
    
cpu_time
=
process_time
(
)
-
cpu_start
    
wall_time
=
time
.
monotonic
(
)
-
time_start
    
efficiency
=
cpu_time
/
wall_time
if
wall_time
else
100
    
untracked
=
wall_time
-
execution_time
    
print
(
        
f
"
Total
wall
time
:
{
wall_time
:
.
2f
}
s
;
CPU
time
:
{
cpu_time
:
.
2f
}
s
;
Efficiency
:
"
        
f
"
{
efficiency
:
.
0
%
}
;
Untracked
:
{
untracked
:
.
2f
}
s
"
        
file
=
sys
.
stderr
    
)
    
if
options
.
diff
:
        
for
the_backend
in
selected_backends
:
            
for
path
diff
in
sorted
(
the_backend
.
file_diffs
.
items
(
)
)
:
                
print
(
"
\
n
"
.
join
(
diff
)
)
    
if
MachCommandConditions
.
is_android
(
env
)
:
        
print
(
ANDROID_IDE_ADVERTISEMENT
)
