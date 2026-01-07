import
errno
import
getpass
import
io
import
json
import
logging
import
os
import
re
import
subprocess
import
sys
import
time
from
collections
import
Counter
OrderedDict
namedtuple
from
itertools
import
dropwhile
islice
takewhile
from
textwrap
import
TextWrapper
from
mach
.
site
import
CommandSiteManager
try
:
    
import
psutil
except
Exception
:
    
psutil
=
None
import
mozfile
import
mozpack
.
path
as
mozpath
from
mach
.
mixin
.
logging
import
LoggingMixin
from
mach
.
util
import
get_state_dir
get_virtualenv_base_dir
from
mozsystemmonitor
.
resourcemonitor
import
SystemResourceMonitor
from
mozterm
.
widgets
import
Footer
from
.
.
backend
import
get_backend_class
from
.
.
base
import
MozbuildObject
from
.
.
compilation
.
warnings
import
WarningsCollector
WarningsDatabase
from
.
.
dirutils
import
mkdir
from
.
.
serialized_logging
import
read_serialized_record
from
.
.
telemetry
import
get_cpu_brand
from
.
.
testing
import
install_test_files
from
.
.
util
import
FileAvoidWrite
resolve_target_to_make
from
.
clobber
import
Clobberer
FINDER_SLOW_MESSAGE
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
=
=
=
=
=
=
PERFORMANCE
WARNING
The
OS
X
Finder
application
(
file
indexing
used
by
Spotlight
)
used
a
lot
of
CPU
during
the
build
-
an
average
of
%
f
%
%
(
100
%
%
is
1
core
)
.
This
made
your
build
slower
.
Consider
adding
"
.
noindex
"
to
the
end
of
your
object
directory
name
to
have
Finder
ignore
it
.
Or
add
an
indexing
exclusion
through
the
Spotlight
System
Preferences
.
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
INSTALL_TESTS_CLOBBER
=
"
"
.
join
(
[
    
TextWrapper
(
)
.
fill
(
line
)
+
"
\
n
"
    
for
line
in
"
"
"
The
build
system
was
unable
to
install
tests
because
the
CLOBBER
file
has
\
been
updated
.
This
means
if
you
edited
any
test
files
your
changes
may
not
\
be
picked
up
until
a
full
/
clobber
build
is
performed
.
The
easiest
and
fastest
way
to
perform
a
clobber
build
is
to
run
:
 
mach
clobber
 
mach
build
If
you
did
not
modify
any
test
files
it
is
safe
to
ignore
this
message
\
and
proceed
with
running
tests
.
To
do
this
run
:
 
touch
{
clobber_file
}
"
"
"
.
splitlines
(
)
]
)
CLOBBER_REQUESTED_MESSAGE
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
=
=
=
=
=
=
The
CLOBBER
file
was
updated
prior
to
this
build
.
A
clobber
build
may
be
required
to
succeed
but
we
weren
'
t
expecting
it
to
.
Please
consider
filing
a
bug
for
this
failure
if
you
have
reason
to
believe
this
is
a
clobber
bug
and
not
due
to
local
changes
.
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
BuildOutputResult
=
namedtuple
(
    
"
BuildOutputResult
"
(
"
warning
"
"
state_changed
"
"
message
"
)
)
class
TierStatus
:
    
"
"
"
Represents
the
state
and
progress
of
tier
traversal
.
    
The
build
system
is
organized
into
linear
phases
called
tiers
.
Each
tier
    
executes
in
the
order
it
was
defined
1
at
a
time
.
    
"
"
"
    
def
__init__
(
self
resources
metrics
)
:
        
"
"
"
Accepts
a
SystemResourceMonitor
to
record
results
against
.
"
"
"
        
self
.
tiers
=
OrderedDict
(
)
        
self
.
tier_status
=
OrderedDict
(
)
        
self
.
resources
=
resources
        
self
.
metrics
=
metrics
    
def
set_tiers
(
self
tiers
)
:
        
"
"
"
Record
the
set
of
known
tiers
.
"
"
"
        
for
tier
in
tiers
:
            
self
.
tiers
[
tier
]
=
dict
(
                
begin_time
=
None
                
finish_time
=
None
                
duration
=
None
            
)
            
self
.
tier_status
[
tier
]
=
None
    
def
begin_tier
(
self
tier
)
:
        
"
"
"
Record
that
execution
of
a
tier
has
begun
.
"
"
"
        
self
.
tier_status
[
tier
]
=
"
active
"
        
t
=
self
.
tiers
[
tier
]
        
t
[
"
begin_time
"
]
=
time
.
monotonic
(
)
        
self
.
resources
.
begin_phase
(
tier
)
        
metrics_tier_name
=
"
tier_
"
+
tier
.
replace
(
"
-
"
"
_
"
)
+
"
_duration
"
        
metrics_attribute
=
getattr
(
self
.
metrics
.
mozbuild
metrics_tier_name
None
)
        
if
metrics_attribute
:
            
metrics_attribute
.
start
(
)
    
def
finish_tier
(
self
tier
)
:
        
"
"
"
Record
that
execution
of
a
tier
has
finished
.
"
"
"
        
self
.
tier_status
[
tier
]
=
"
finished
"
        
t
=
self
.
tiers
[
tier
]
        
t
[
"
finish_time
"
]
=
time
.
monotonic
(
)
        
t
[
"
duration
"
]
=
self
.
resources
.
finish_phase
(
tier
)
        
metrics_tier_name
=
"
tier_
"
+
tier
.
replace
(
"
-
"
"
_
"
)
+
"
_duration
"
        
metrics_attribute
=
getattr
(
self
.
metrics
.
mozbuild
metrics_tier_name
None
)
        
if
metrics_attribute
:
            
metrics_attribute
.
stop
(
)
def
record_cargo_timings
(
resource_monitor
timings_path
)
:
    
cargo_start
=
0
    
try
:
        
with
open
(
timings_path
)
as
fh
:
            
unit_data
=
dropwhile
(
lambda
l
:
l
.
rstrip
(
)
!
=
"
const
UNIT_DATA
=
[
"
fh
)
            
unit_data
=
islice
(
unit_data
1
None
)
            
lines
=
takewhile
(
lambda
l
:
l
.
rstrip
(
)
!
=
"
]
;
"
unit_data
)
            
entries
=
json
.
loads
(
"
[
"
+
"
"
.
join
(
lines
)
+
"
]
"
)
            
data
=
[
                
(
                    
"
{
}
v
{
}
{
}
"
.
format
(
                        
entry
[
"
name
"
]
entry
[
"
version
"
]
entry
.
get
(
"
target
"
"
"
)
                    
)
                    
entry
[
"
start
"
]
or
0
                    
entry
[
"
duration
"
]
or
0
                
)
                
for
entry
in
entries
            
]
        
starts
=
[
            
start
            
for
marker
start
in
resource_monitor
.
_active_markers
.
items
(
)
            
if
marker
.
startswith
(
"
Rust
:
"
)
        
]
        
if
len
(
starts
)
!
=
1
:
            
return
        
cargo_start
=
starts
[
0
]
    
except
Exception
:
        
return
    
if
not
cargo_start
:
        
return
    
for
name
start
duration
in
data
:
        
resource_monitor
.
record_marker
(
            
"
RustCrate
"
cargo_start
+
start
cargo_start
+
start
+
duration
name
        
)
class
BuildMonitor
(
MozbuildObject
)
:
    
"
"
"
Monitors
the
output
of
the
build
.
"
"
"
    
def
init
(
self
warnings_path
terminal
metrics
)
:
        
"
"
"
Create
a
new
monitor
.
        
warnings_path
is
a
path
of
a
warnings
database
to
use
.
        
"
"
"
        
self
.
_warnings_path
=
warnings_path
        
self
.
resources
=
SystemResourceMonitor
(
            
poll_interval
=
0
.
1
            
metadata
=
{
"
CPUName
"
:
get_cpu_brand
(
)
}
        
)
        
self
.
_resources_started
=
False
        
self
.
tiers
=
TierStatus
(
self
.
resources
metrics
)
        
self
.
warnings_database
=
WarningsDatabase
(
)
        
if
os
.
path
.
exists
(
warnings_path
)
:
            
try
:
                
self
.
warnings_database
.
load_from_file
(
warnings_path
)
            
except
ValueError
:
                
os
.
remove
(
warnings_path
)
        
self
.
instance_warnings
=
WarningsDatabase
(
)
        
self
.
_terminal
=
terminal
        
def
on_warning
(
warning
)
:
            
if
warning
[
"
type
"
]
=
=
"
error
"
:
                
return
            
filename
=
warning
[
"
filename
"
]
            
if
not
os
.
path
.
exists
(
filename
)
:
                
raise
Exception
(
"
Could
not
find
file
containing
warning
:
%
s
"
%
filename
)
            
self
.
warnings_database
.
insert
(
warning
)
            
self
.
instance_warnings
.
insert
(
warning
.
copy
(
)
)
        
self
.
_warnings_collector
=
WarningsCollector
(
on_warning
objdir
=
self
.
topobjdir
)
        
self
.
build_objects
=
[
]
        
self
.
build_dirs
=
set
(
)
    
def
start
(
self
)
:
        
"
"
"
Record
the
start
of
the
build
.
"
"
"
        
self
.
start_time
=
time
.
monotonic
(
)
        
self
.
_finder_start_cpu
=
self
.
_get_finder_cpu_usage
(
)
    
def
start_resource_recording
(
self
)
:
        
self
.
resources
.
start
(
)
        
self
.
_resources_started
=
True
    
def
on_line
(
self
line
)
:
        
"
"
"
Consume
a
line
of
output
from
the
build
system
.
        
This
will
parse
the
line
for
state
and
determine
whether
more
action
is
        
needed
.
        
Returns
a
BuildOutputResult
instance
.
        
In
this
named
tuple
warning
will
be
an
object
describing
a
new
parsed
        
warning
.
Otherwise
it
will
be
None
.
        
state_changed
indicates
whether
the
build
system
changed
state
with
        
this
line
.
If
the
build
system
changed
state
the
caller
may
want
to
        
query
this
instance
for
the
current
state
in
order
to
update
UI
etc
.
        
message
is
either
None
or
the
content
of
a
message
to
be
        
displayed
to
the
user
(
as
a
str
or
a
logging
.
LogRecord
)
.
        
"
"
"
        
message
=
None
        
plain_line
=
self
.
_terminal
.
strip
(
line
)
if
self
.
_terminal
else
line
.
strip
(
)
        
if
plain_line
.
startswith
(
"
BUILDSTATUS
"
)
:
            
args
=
plain_line
.
split
(
)
            
_
_
disambiguator
=
args
.
pop
(
0
)
.
partition
(
"
"
)
            
action
=
args
.
pop
(
0
)
            
time
=
None
            
regexp
=
re
.
compile
(
r
"
\
d
{
10
}
(
\
.
\
d
{
1
9
}
)
?
"
)
            
if
regexp
.
match
(
action
)
:
                
time
=
float
(
action
)
                
action
=
args
.
pop
(
0
)
            
update_needed
=
True
            
if
action
=
=
"
TIERS
"
:
                
self
.
tiers
.
set_tiers
(
args
)
                
update_needed
=
False
            
elif
action
=
=
"
TIER_START
"
:
                
tier
=
args
[
0
]
                
self
.
tiers
.
begin_tier
(
tier
)
            
elif
action
=
=
"
TIER_FINISH
"
:
                
(
tier
)
=
args
                
self
.
tiers
.
finish_tier
(
tier
)
            
elif
action
=
=
"
OBJECT_FILE
"
:
                
self
.
build_objects
.
append
(
args
[
0
]
)
                
self
.
resources
.
begin_marker
(
"
Object
"
args
[
0
]
disambiguator
)
                
update_needed
=
False
            
elif
action
.
startswith
(
"
START_
"
)
:
                
self
.
resources
.
begin_marker
(
                    
action
[
len
(
"
START_
"
)
:
]
"
"
.
join
(
args
)
disambiguator
time
                
)
                
update_needed
=
False
            
elif
action
.
startswith
(
"
END_
"
)
:
                
self
.
resources
.
end_marker
(
                    
action
[
len
(
"
END_
"
)
:
]
"
"
.
join
(
args
)
disambiguator
time
                
)
                
update_needed
=
False
            
elif
action
=
=
"
BUILD_VERBOSE
"
:
                
build_dir
=
args
[
0
]
                
if
build_dir
not
in
self
.
build_dirs
:
                    
self
.
build_dirs
.
add
(
build_dir
)
                    
message
=
build_dir
                
update_needed
=
False
            
else
:
                
raise
Exception
(
"
Unknown
build
status
:
%
s
"
%
action
)
            
return
BuildOutputResult
(
None
update_needed
message
)
        
elif
plain_line
.
startswith
(
"
Timing
report
saved
to
"
)
:
            
cargo_timings
=
plain_line
[
len
(
"
Timing
report
saved
to
"
)
:
]
            
record_cargo_timings
(
self
.
resources
cargo_timings
)
            
return
BuildOutputResult
(
None
False
None
)
        
if
log_record
:
=
read_serialized_record
(
line
)
:
            
return
BuildOutputResult
(
None
False
log_record
)
        
warning
=
None
        
message
=
line
        
try
:
            
warning
=
self
.
_warnings_collector
.
process_line
(
line
)
        
except
Exception
:
            
pass
        
return
BuildOutputResult
(
warning
False
message
)
    
def
stop_resource_recording
(
self
)
:
        
if
self
.
_resources_started
:
            
self
.
resources
.
stop
(
)
        
self
.
_resources_started
=
False
    
def
finish
(
self
)
:
        
"
"
"
Record
the
end
of
the
build
.
"
"
"
        
self
.
stop_resource_recording
(
)
        
self
.
end_time
=
time
.
monotonic
(
)
        
self
.
_finder_end_cpu
=
self
.
_get_finder_cpu_usage
(
)
        
self
.
elapsed
=
self
.
end_time
-
self
.
start_time
        
self
.
warnings_database
.
prune
(
)
        
self
.
warnings_database
.
save_to_file
(
self
.
_warnings_path
)
    
def
record_usage
(
self
)
:
        
build_resources_profile_path
=
None
        
try
:
            
if
"
MOZ_AUTOMATION
"
in
os
.
environ
and
"
UPLOAD_PATH
"
in
os
.
environ
:
                
build_resources_profile_path
=
mozpath
.
join
(
                    
os
.
environ
[
"
UPLOAD_PATH
"
]
"
profile_build_resources
.
json
"
                
)
            
else
:
                
build_resources_profile_path
=
self
.
_get_state_filename
(
                    
"
profile_build_resources
.
json
"
                
)
            
with
open
(
                
build_resources_profile_path
"
w
"
encoding
=
"
utf
-
8
"
newline
=
"
\
n
"
            
)
as
fh
:
                
to_write
=
json
.
dumps
(
                    
self
.
resources
.
as_profile
(
)
separators
=
(
"
"
"
:
"
)
                
)
                
fh
.
write
(
to_write
)
        
except
Exception
as
e
:
            
self
.
log
(
                
logging
.
WARNING
                
"
build_resources_error
"
                
{
"
msg
"
:
str
(
e
)
}
                
"
Exception
when
writing
resource
usage
file
:
{
msg
}
"
            
)
            
try
:
                
if
build_resources_profile_path
and
os
.
path
.
exists
(
                    
build_resources_profile_path
                
)
:
                    
os
.
remove
(
build_resources_profile_path
)
            
except
Exception
:
                
pass
    
def
_get_finder_cpu_usage
(
self
)
:
        
"
"
"
Obtain
the
CPU
usage
of
the
Finder
app
on
OS
X
.
        
This
is
used
to
detect
high
CPU
usage
.
        
"
"
"
        
if
not
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
            
return
None
        
if
not
psutil
:
            
return
None
        
for
proc
in
psutil
.
process_iter
(
)
:
            
if
proc
.
name
!
=
"
Finder
"
:
                
continue
            
if
proc
.
username
!
=
getpass
.
getuser
(
)
:
                
continue
            
if
not
proc
.
exe
.
endswith
(
"
CoreServices
/
Finder
.
app
/
Contents
/
MacOS
/
Finder
"
)
:
                
continue
            
return
proc
.
get_cpu_times
(
)
        
return
None
    
def
have_high_finder_usage
(
self
)
:
        
"
"
"
Determine
whether
there
was
high
Finder
CPU
usage
during
the
build
.
        
Returns
True
if
there
was
high
Finder
CPU
usage
False
if
there
wasn
'
t
        
or
None
if
there
is
nothing
to
report
.
        
"
"
"
        
if
not
self
.
_finder_start_cpu
:
            
return
None
None
        
if
self
.
elapsed
<
15
:
            
return
None
None
        
if
not
self
.
_finder_end_cpu
:
            
return
None
None
        
start
=
self
.
_finder_start_cpu
        
end
=
self
.
_finder_end_cpu
        
start_total
=
start
.
user
+
start
.
system
        
end_total
=
end
.
user
+
end
.
system
        
cpu_seconds
=
end_total
-
start_total
        
finder_percent
=
cpu_seconds
/
self
.
elapsed
*
100
        
return
finder_percent
>
25
finder_percent
    
def
have_excessive_swapping
(
self
)
:
        
"
"
"
Determine
whether
there
was
excessive
swapping
during
the
build
.
        
Returns
a
tuple
of
(
excessive
swap_in
swap_out
)
.
All
values
are
None
        
if
no
swap
information
is
available
.
        
"
"
"
        
if
not
self
.
have_resource_usage
:
            
return
None
None
None
        
swap_in
=
sum
(
m
.
swap
.
sin
for
m
in
self
.
resources
.
measurements
)
        
swap_out
=
sum
(
m
.
swap
.
sout
for
m
in
self
.
resources
.
measurements
)
        
excessive
=
swap_in
>
512
*
1048576
or
swap_out
>
512
*
1048576
        
return
excessive
swap_in
swap_out
    
property
    
def
have_resource_usage
(
self
)
:
        
"
"
"
Whether
resource
usage
is
available
.
"
"
"
        
return
self
.
resources
.
start_time
is
not
None
    
def
get_resource_usage
(
self
)
:
        
"
"
"
Produce
a
data
structure
containing
the
low
-
level
resource
usage
information
.
        
This
data
structure
can
e
.
g
.
be
serialized
into
JSON
and
saved
for
        
subsequent
analysis
.
        
If
no
resource
usage
is
available
None
is
returned
.
        
"
"
"
        
if
not
self
.
have_resource_usage
:
            
return
None
        
cpu_percent
=
self
.
resources
.
aggregate_cpu_percent
(
phase
=
None
per_cpu
=
False
)
        
io
=
self
.
resources
.
aggregate_io
(
phase
=
None
)
        
return
dict
(
            
cpu_percent
=
cpu_percent
            
io
=
io
        
)
    
def
log_resource_usage
(
self
usage
)
:
        
"
"
"
Summarize
the
resource
usage
of
this
build
in
a
log
message
.
"
"
"
        
if
not
usage
:
            
return
        
params
=
dict
(
            
duration
=
self
.
end_time
-
self
.
start_time
            
cpu_percent
=
usage
[
"
cpu_percent
"
]
            
io_read_bytes
=
usage
[
"
io
"
]
.
read_bytes
            
io_write_bytes
=
usage
[
"
io
"
]
.
write_bytes
        
)
        
message
=
(
            
"
Overall
system
resources
-
Wall
time
:
{
duration
:
.
0f
}
s
;
"
            
"
CPU
:
{
cpu_percent
:
.
0f
}
%
;
"
            
"
Read
bytes
:
{
io_read_bytes
}
;
Write
bytes
:
{
io_write_bytes
}
;
"
        
)
        
if
hasattr
(
usage
[
"
io
"
]
"
read_time
"
)
and
hasattr
(
usage
[
"
io
"
]
"
write_time
"
)
:
            
params
.
update
(
                
io_read_time
=
usage
[
"
io
"
]
.
read_time
                
io_write_time
=
usage
[
"
io
"
]
.
write_time
            
)
            
message
+
=
"
Read
time
:
{
io_read_time
}
;
Write
time
:
{
io_write_time
}
"
        
self
.
log
(
logging
.
WARNING
"
resource_usage
"
params
message
)
        
excessive
sin
sout
=
self
.
have_excessive_swapping
(
)
        
if
excessive
is
not
None
and
(
sin
or
sout
)
:
            
sin
/
=
1048576
            
sout
/
=
1048576
            
self
.
log
(
                
logging
.
WARNING
                
"
swap_activity
"
                
{
"
sin
"
:
sin
"
sout
"
:
sout
}
                
"
Swap
in
/
out
(
MB
)
:
{
sin
}
/
{
sout
}
"
            
)
    
def
ccache_stats
(
self
ccache
=
None
)
:
        
ccache_stats
=
None
        
if
ccache
is
None
:
            
ccache
=
mozfile
.
which
(
"
ccache
"
)
        
if
ccache
:
            
has_machine_format
=
CCacheStats
.
check_version_3_7_or_newer
(
ccache
)
            
try
:
                
output
=
subprocess
.
check_output
(
                    
[
ccache
"
-
-
print
-
stats
"
if
has_machine_format
else
"
-
s
"
]
                    
universal_newlines
=
True
                
)
                
ccache_stats
=
CCacheStats
(
output
has_machine_format
)
            
except
ValueError
as
e
:
                
self
.
log
(
logging
.
WARNING
"
ccache
"
{
"
msg
"
:
str
(
e
)
}
"
{
msg
}
"
)
        
return
ccache_stats
class
TerminalLoggingHandler
(
logging
.
Handler
)
:
    
"
"
"
Custom
logging
handler
that
works
with
terminal
window
dressing
.
    
This
class
should
probably
live
elsewhere
like
the
mach
core
.
Consider
    
this
a
proving
ground
for
its
usefulness
.
    
"
"
"
    
def
__init__
(
self
)
:
        
logging
.
Handler
.
__init__
(
self
)
        
self
.
fh
=
sys
.
stdout
        
self
.
footer
=
None
    
def
flush
(
self
)
:
        
self
.
acquire
(
)
        
try
:
            
self
.
fh
.
flush
(
)
        
finally
:
            
self
.
release
(
)
    
def
emit
(
self
record
)
:
        
msg
=
self
.
format
(
record
)
        
self
.
acquire
(
)
        
try
:
            
if
self
.
footer
:
                
self
.
footer
.
clear
(
)
            
self
.
fh
.
write
(
msg
)
            
self
.
fh
.
write
(
"
\
n
"
)
            
if
self
.
footer
:
                
self
.
footer
.
draw
(
)
            
self
.
fh
.
flush
(
)
        
finally
:
            
self
.
release
(
)
class
BuildProgressFooter
(
Footer
)
:
    
"
"
"
Handles
display
of
a
build
progress
indicator
in
a
terminal
.
    
When
mach
builds
inside
a
blessed
-
supported
terminal
it
will
render
    
progress
information
collected
from
a
BuildMonitor
.
This
class
converts
the
    
state
of
BuildMonitor
into
terminal
output
.
    
"
"
"
    
def
__init__
(
self
terminal
monitor
)
:
        
Footer
.
__init__
(
self
terminal
)
        
self
.
tiers
=
monitor
.
tiers
.
tier_status
.
items
(
)
    
def
draw
(
self
)
:
        
"
"
"
Draws
this
footer
in
the
terminal
.
"
"
"
        
if
not
self
.
tiers
:
            
return
        
parts
=
[
(
"
bold
"
"
TIER
:
"
)
]
        
append
=
parts
.
append
        
for
tier
status
in
self
.
tiers
:
            
if
status
is
None
:
                
append
(
tier
)
            
elif
status
=
=
"
finished
"
:
                
append
(
(
"
green
"
tier
)
)
            
else
:
                
append
(
(
"
underline_yellow
"
tier
)
)
        
self
.
write
(
parts
)
class
OutputManager
(
LoggingMixin
)
:
    
"
"
"
Handles
writing
job
output
to
a
terminal
or
log
.
"
"
"
    
def
__init__
(
self
log_manager
footer
)
:
        
self
.
populate_logger
(
)
        
self
.
footer
=
None
        
terminal
=
log_manager
.
terminal
        
if
not
terminal
:
            
return
        
if
os
.
environ
.
get
(
"
INSIDE_EMACS
"
None
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
"
MACH_NO_TERMINAL_FOOTER
"
None
)
:
            
footer
=
None
        
self
.
t
=
terminal
        
self
.
footer
=
footer
        
self
.
_handler
=
TerminalLoggingHandler
(
)
        
self
.
_handler
.
setFormatter
(
log_manager
.
terminal_formatter
)
        
self
.
_handler
.
footer
=
self
.
footer
        
old
=
log_manager
.
replace_terminal_handler
(
self
.
_handler
)
        
self
.
_handler
.
level
=
old
.
level
    
def
__enter__
(
self
)
:
        
return
self
    
def
__exit__
(
self
exc_type
exc_value
traceback
)
:
        
if
self
.
footer
:
            
self
.
footer
.
clear
(
)
            
self
.
_handler
.
footer
=
None
    
def
write_line
(
self
line
)
:
        
if
self
.
footer
:
            
self
.
footer
.
clear
(
)
        
print
(
line
)
        
if
self
.
footer
:
            
self
.
footer
.
draw
(
)
    
def
refresh
(
self
)
:
        
if
not
self
.
footer
:
            
return
        
self
.
footer
.
clear
(
)
        
self
.
footer
.
draw
(
)
class
BuildOutputManager
(
OutputManager
)
:
    
"
"
"
Handles
writing
build
output
to
a
terminal
to
logs
etc
.
"
"
"
    
def
__init__
(
self
log_manager
monitor
footer
)
:
        
self
.
monitor
=
monitor
        
OutputManager
.
__init__
(
self
log_manager
footer
)
    
def
__exit__
(
self
exc_type
exc_value
traceback
)
:
        
OutputManager
.
__exit__
(
self
exc_type
exc_value
traceback
)
        
self
.
monitor
.
stop_resource_recording
(
)
    
def
on_line
(
self
line
)
:
        
warning
state_changed
message
=
self
.
monitor
.
on_line
(
line
)
        
if
message
:
            
if
isinstance
(
message
logging
.
LogRecord
)
:
                
self
.
log_record
(
"
build_output
"
message
)
            
else
:
                
self
.
log
(
logging
.
INFO
"
build_output
"
{
"
line
"
:
message
}
"
{
line
}
"
)
        
elif
state_changed
:
            
have_handler
=
hasattr
(
self
"
_handler
"
)
            
if
have_handler
:
                
self
.
_handler
.
acquire
(
)
            
try
:
                
self
.
refresh
(
)
            
finally
:
                
if
have_handler
:
                    
self
.
_handler
.
release
(
)
class
StaticAnalysisFooter
(
Footer
)
:
    
"
"
"
Handles
display
of
a
static
analysis
progress
indicator
in
a
terminal
.
"
"
"
    
def
__init__
(
self
terminal
monitor
)
:
        
Footer
.
__init__
(
self
terminal
)
        
self
.
monitor
=
monitor
    
def
draw
(
self
)
:
        
"
"
"
Draws
this
footer
in
the
terminal
.
"
"
"
        
monitor
=
self
.
monitor
        
total
=
monitor
.
num_files
        
processed
=
monitor
.
num_files_processed
        
percent
=
"
(
%
.
2f
%
%
)
"
%
(
processed
*
100
.
0
/
total
)
        
parts
=
[
            
(
"
bright_black
"
"
Processing
"
)
            
(
"
yellow
"
str
(
processed
)
)
            
(
"
bright_black
"
"
of
"
)
            
(
"
yellow
"
str
(
total
)
)
            
(
"
bright_black
"
"
files
"
)
            
(
"
green
"
percent
)
        
]
        
if
monitor
.
current_file
:
            
parts
.
append
(
(
"
bold
"
monitor
.
current_file
)
)
        
self
.
write
(
parts
)
class
StaticAnalysisOutputManager
(
OutputManager
)
:
    
"
"
"
Handles
writing
static
analysis
output
to
a
terminal
or
file
.
"
"
"
    
def
__init__
(
self
log_manager
monitor
footer
)
:
        
self
.
monitor
=
monitor
        
self
.
raw
=
"
"
        
OutputManager
.
__init__
(
self
log_manager
footer
)
    
def
on_line
(
self
line
)
:
        
warning
relevant
=
self
.
monitor
.
on_line
(
line
)
        
if
relevant
:
            
self
.
raw
+
=
line
+
"
\
n
"
        
if
warning
:
            
self
.
log
(
                
logging
.
INFO
                
"
compiler_warning
"
                
warning
                
"
Warning
:
{
flag
}
in
{
filename
}
:
{
message
}
"
            
)
        
if
relevant
:
            
self
.
log
(
logging
.
INFO
"
build_output
"
{
"
line
"
:
line
}
"
{
line
}
"
)
        
else
:
            
have_handler
=
hasattr
(
self
"
_handler
"
)
            
if
have_handler
:
                
self
.
_handler
.
acquire
(
)
            
try
:
                
self
.
refresh
(
)
            
finally
:
                
if
have_handler
:
                    
self
.
_handler
.
release
(
)
    
def
write
(
self
path
output_format
)
:
        
assert
output_format
in
(
            
"
text
"
            
"
json
"
        
)
f
"
Invalid
output
format
{
output_format
}
"
        
path
=
mozpath
.
realpath
(
path
)
        
if
output_format
=
=
"
json
"
:
            
self
.
monitor
.
_warnings_database
.
save_to_file
(
path
)
        
else
:
            
with
open
(
path
"
w
"
encoding
=
"
utf
-
8
"
newline
=
"
\
n
"
)
as
f
:
                
f
.
write
(
self
.
raw
)
        
self
.
log
(
            
logging
.
INFO
            
"
write_output
"
            
{
"
path
"
:
path
"
format
"
:
output_format
}
            
"
Wrote
{
format
}
output
in
{
path
}
"
        
)
class
CCacheStats
:
    
"
"
"
Holds
statistics
from
ccache
.
    
Instances
can
be
subtracted
from
each
other
to
obtain
differences
.
    
print
(
)
or
str
(
)
the
object
to
show
a
ccache
-
s
like
output
    
of
the
captured
stats
.
    
"
"
"
    
STATS_KEYS
=
[
        
(
"
stats_zeroed
"
(
"
stats
zeroed
"
"
stats
zero
time
"
)
)
        
(
"
stats_updated
"
"
stats
updated
"
)
        
(
"
cache_hit_direct
"
"
cache
hit
(
direct
)
"
)
        
(
"
cache_hit_preprocessed
"
"
cache
hit
(
preprocessed
)
"
)
        
(
"
cache_hit_rate
"
"
cache
hit
rate
"
)
        
(
"
cache_miss
"
"
cache
miss
"
)
        
(
"
link
"
"
called
for
link
"
)
        
(
"
preprocessing
"
"
called
for
preprocessing
"
)
        
(
"
multiple
"
"
multiple
source
files
"
)
        
(
"
stdout
"
"
compiler
produced
stdout
"
)
        
(
"
no_output
"
"
compiler
produced
no
output
"
)
        
(
"
empty_output
"
"
compiler
produced
empty
output
"
)
        
(
"
failed
"
"
compile
failed
"
)
        
(
"
error
"
"
ccache
internal
error
"
)
        
(
"
preprocessor_error
"
"
preprocessor
error
"
)
        
(
"
cant_use_pch
"
"
can
'
t
use
precompiled
header
"
)
        
(
"
compiler_missing
"
"
couldn
'
t
find
the
compiler
"
)
        
(
"
cache_file_missing
"
"
cache
file
missing
"
)
        
(
"
bad_args
"
"
bad
compiler
arguments
"
)
        
(
"
unsupported_lang
"
"
unsupported
source
language
"
)
        
(
"
compiler_check_failed
"
"
compiler
check
failed
"
)
        
(
"
autoconf
"
"
autoconf
compile
/
link
"
)
        
(
"
unsupported_code_directive
"
"
unsupported
code
directive
"
)
        
(
"
unsupported_compiler_option
"
"
unsupported
compiler
option
"
)
        
(
"
out_stdout
"
"
output
to
stdout
"
)
        
(
"
out_device
"
"
output
to
a
non
-
regular
file
"
)
        
(
"
no_input
"
"
no
input
file
"
)
        
(
"
bad_extra_file
"
"
error
hashing
extra
file
"
)
        
(
"
num_cleanups
"
"
cleanups
performed
"
)
        
(
"
cache_files
"
"
files
in
cache
"
)
        
(
"
cache_size
"
"
cache
size
"
)
        
(
"
cache_max_size
"
"
max
cache
size
"
)
    
]
    
SKIP_LINES
=
(
        
"
cache
directory
"
        
"
primary
config
"
        
"
secondary
config
"
    
)
    
STATS_KEYS_3_7_PLUS
=
{
        
"
stats_zeroed_timestamp
"
:
"
stats_zeroed
"
        
"
stats_updated_timestamp
"
:
"
stats_updated
"
        
"
direct_cache_hit
"
:
"
cache_hit_direct
"
        
"
preprocessed_cache_hit
"
:
"
cache_hit_preprocessed
"
        
"
cache_miss
"
:
"
cache_miss
"
        
"
called_for_link
"
:
"
link
"
        
"
called_for_preprocessing
"
:
"
preprocessing
"
        
"
multiple_source_files
"
:
"
multiple
"
        
"
compiler_produced_stdout
"
:
"
stdout
"
        
"
compiler_produced_no_output
"
:
"
no_output
"
        
"
compiler_produced_empty_output
"
:
"
empty_output
"
        
"
compile_failed
"
:
"
failed
"
        
"
internal_error
"
:
"
error
"
        
"
preprocessor_error
"
:
"
preprocessor_error
"
        
"
could_not_use_precompiled_header
"
:
"
cant_use_pch
"
        
"
could_not_find_compiler
"
:
"
compiler_missing
"
        
"
missing_cache_file
"
:
"
cache_file_missing
"
        
"
bad_compiler_arguments
"
:
"
bad_args
"
        
"
unsupported_source_language
"
:
"
unsupported_lang
"
        
"
compiler_check_failed
"
:
"
compiler_check_failed
"
        
"
autoconf_test
"
:
"
autoconf
"
        
"
unsupported_code_directive
"
:
"
unsupported_code_directive
"
        
"
unsupported_compiler_option
"
:
"
unsupported_compiler_option
"
        
"
output_to_stdout
"
:
"
out_stdout
"
        
"
output_to_a_non_file
"
:
"
out_device
"
        
"
no_input_file
"
:
"
no_input
"
        
"
error_hashing_extra_file
"
:
"
bad_extra_file
"
        
"
cleanups_performed
"
:
"
num_cleanups
"
        
"
files_in_cache
"
:
"
cache_files
"
        
"
cache_size_kibibyte
"
:
"
cache_size
"
    
}
    
ABSOLUTE_KEYS
=
{
"
cache_files
"
"
cache_size
"
"
cache_max_size
"
}
    
FORMAT_KEYS
=
{
"
cache_size
"
"
cache_max_size
"
}
    
GiB
=
1024
*
*
3
    
MiB
=
1024
*
*
2
    
KiB
=
1024
    
def
__init__
(
self
output
=
None
has_machine_format
=
False
)
:
        
"
"
"
Construct
an
instance
from
the
output
of
ccache
-
s
.
"
"
"
        
self
.
_values
=
{
}
        
if
not
output
:
            
return
        
if
has_machine_format
:
            
self
.
_parse_machine_format
(
output
)
        
else
:
            
self
.
_parse_human_format
(
output
)
    
def
_parse_machine_format
(
self
output
)
:
        
for
line
in
output
.
splitlines
(
)
:
            
line
=
line
.
strip
(
)
            
key
_
value
=
line
.
partition
(
"
\
t
"
)
            
stat_key
=
self
.
STATS_KEYS_3_7_PLUS
.
get
(
key
)
            
if
stat_key
:
                
value
=
int
(
value
)
                
if
key
.
endswith
(
"
_kibibyte
"
)
:
                    
value
*
=
1024
                
self
.
_values
[
stat_key
]
=
value
        
(
direct
preprocessed
miss
)
=
self
.
hit_rates
(
)
        
self
.
_values
[
"
cache_hit_rate
"
]
=
(
direct
+
preprocessed
)
*
100
    
def
_parse_human_format
(
self
output
)
:
        
for
line
in
output
.
splitlines
(
)
:
            
line
=
line
.
strip
(
)
            
if
line
:
                
self
.
_parse_line
(
line
)
    
def
_parse_line
(
self
line
)
:
        
for
stat_key
stat_description
in
self
.
STATS_KEYS
:
            
if
line
.
startswith
(
stat_description
)
:
                
raw_value
=
self
.
_strip_prefix
(
line
stat_description
)
                
self
.
_values
[
stat_key
]
=
self
.
_parse_value
(
raw_value
)
                
break
        
else
:
            
if
not
line
.
startswith
(
self
.
SKIP_LINES
)
:
                
raise
ValueError
(
"
Failed
to
parse
ccache
stats
output
:
%
s
"
%
line
)
    
staticmethod
    
def
_strip_prefix
(
line
prefix
)
:
        
if
isinstance
(
prefix
tuple
)
:
            
for
p
in
prefix
:
                
line
=
CCacheStats
.
_strip_prefix
(
line
p
)
            
return
line
        
return
line
[
len
(
prefix
)
:
]
.
strip
(
)
if
line
.
startswith
(
prefix
)
else
line
    
staticmethod
    
def
_parse_value
(
raw_value
)
:
        
try
:
            
ts
=
time
.
strptime
(
raw_value
"
%
c
"
)
            
return
int
(
time
.
mktime
(
ts
)
)
        
except
ValueError
:
            
if
raw_value
=
=
"
never
"
:
                
return
0
            
pass
        
value
=
raw_value
.
split
(
)
        
unit
=
"
"
        
if
len
(
value
)
=
=
1
:
            
numeric
=
value
[
0
]
        
elif
len
(
value
)
=
=
2
:
            
numeric
unit
=
value
        
else
:
            
raise
ValueError
(
"
Failed
to
parse
ccache
stats
value
:
%
s
"
%
raw_value
)
        
if
"
.
"
in
numeric
:
            
numeric
=
float
(
numeric
)
        
else
:
            
numeric
=
int
(
numeric
)
        
if
unit
in
(
"
GB
"
"
Gbytes
"
)
:
            
unit
=
CCacheStats
.
GiB
        
elif
unit
in
(
"
MB
"
"
Mbytes
"
)
:
            
unit
=
CCacheStats
.
MiB
        
elif
unit
in
(
"
KB
"
"
Kbytes
"
)
:
            
unit
=
CCacheStats
.
KiB
        
else
:
            
unit
=
1
        
return
int
(
numeric
*
unit
)
    
def
hit_rate_message
(
self
)
:
        
return
(
            
"
ccache
(
direct
)
hit
rate
:
{
:
.
1
%
}
;
(
preprocessed
)
hit
rate
:
{
:
.
1
%
}
;
"
            
"
miss
rate
:
{
:
.
1
%
}
"
.
format
(
*
self
.
hit_rates
(
)
)
        
)
    
def
hit_rates
(
self
)
:
        
direct
=
self
.
_values
[
"
cache_hit_direct
"
]
        
preprocessed
=
self
.
_values
[
"
cache_hit_preprocessed
"
]
        
miss
=
self
.
_values
[
"
cache_miss
"
]
        
total
=
float
(
direct
+
preprocessed
+
miss
)
        
if
total
>
0
:
            
direct
/
=
total
            
preprocessed
/
=
total
            
miss
/
=
total
        
return
(
direct
preprocessed
miss
)
    
def
__sub__
(
self
other
)
:
        
result
=
CCacheStats
(
)
        
for
k
prefix
in
self
.
STATS_KEYS
:
            
if
k
not
in
self
.
_values
and
k
not
in
other
.
_values
:
                
continue
            
our_value
=
self
.
_values
.
get
(
k
0
)
            
other_value
=
other
.
_values
.
get
(
k
0
)
            
if
k
in
self
.
ABSOLUTE_KEYS
:
                
result
.
_values
[
k
]
=
our_value
            
else
:
                
result
.
_values
[
k
]
=
our_value
-
other_value
        
return
result
    
def
__str__
(
self
)
:
        
LEFT_ALIGN
=
34
        
lines
=
[
]
        
for
stat_key
stat_description
in
self
.
STATS_KEYS
:
            
if
stat_key
not
in
self
.
_values
:
                
continue
            
value
=
self
.
_values
[
stat_key
]
            
if
stat_key
in
self
.
FORMAT_KEYS
:
                
value
=
"
%
15s
"
%
self
.
_format_value
(
value
)
            
else
:
                
value
=
"
%
8u
"
%
value
            
if
isinstance
(
stat_description
tuple
)
:
                
stat_description
=
stat_description
[
0
]
            
lines
.
append
(
"
%
s
%
s
"
%
(
stat_description
.
ljust
(
LEFT_ALIGN
)
value
)
)
        
return
"
\
n
"
.
join
(
lines
)
    
def
__nonzero__
(
self
)
:
        
relative_values
=
[
            
v
for
k
v
in
self
.
_values
.
items
(
)
if
k
not
in
self
.
ABSOLUTE_KEYS
        
]
        
return
all
(
v
>
=
0
for
v
in
relative_values
)
and
any
(
            
v
>
0
for
v
in
relative_values
        
)
    
def
__bool__
(
self
)
:
        
return
self
.
__nonzero__
(
)
    
staticmethod
    
def
_format_value
(
v
)
:
        
if
v
>
CCacheStats
.
GiB
:
            
return
"
%
.
1f
Gbytes
"
%
(
float
(
v
)
/
CCacheStats
.
GiB
)
        
elif
v
>
CCacheStats
.
MiB
:
            
return
"
%
.
1f
Mbytes
"
%
(
float
(
v
)
/
CCacheStats
.
MiB
)
        
else
:
            
return
"
%
.
1f
Kbytes
"
%
(
float
(
v
)
/
CCacheStats
.
KiB
)
    
staticmethod
    
def
check_version_3_7_or_newer
(
ccache
)
:
        
output_version
=
subprocess
.
check_output
(
            
[
ccache
"
-
-
version
"
]
universal_newlines
=
True
        
)
        
return
CCacheStats
.
_is_version_3_7_or_newer
(
output_version
)
    
staticmethod
    
def
_is_version_3_7_or_newer
(
output
)
:
        
if
"
ccache
version
"
not
in
output
:
            
return
False
        
major
=
0
        
minor
=
0
        
for
line
in
output
.
splitlines
(
)
:
            
version
=
re
.
search
(
r
"
ccache
version
(
\
d
+
)
.
(
\
d
+
)
.
*
"
line
)
            
if
version
:
                
major
=
int
(
version
.
group
(
1
)
)
                
minor
=
int
(
version
.
group
(
2
)
)
                
break
        
return
(
(
major
<
<
8
)
+
minor
)
>
=
(
(
3
<
<
8
)
+
7
)
class
BuildDriver
(
MozbuildObject
)
:
    
"
"
"
Provides
a
high
-
level
API
for
build
actions
.
"
"
"
    
def
__init__
(
self
*
args
*
*
kwargs
)
:
        
MozbuildObject
.
__init__
(
self
*
args
virtualenv_name
=
"
build
"
*
*
kwargs
)
        
self
.
metrics
=
None
        
self
.
mach_context
=
None
    
def
build
(
        
self
        
metrics
        
what
=
None
        
jobs
=
0
        
job_size
=
0
        
directory
=
None
        
verbose
=
False
        
keep_going
=
False
        
mach_context
=
None
        
append_env
=
None
    
)
:
        
warnings_path
=
self
.
_get_state_filename
(
"
warnings
.
json
"
)
        
monitor
=
self
.
_spawn
(
BuildMonitor
)
        
monitor
.
init
(
warnings_path
self
.
log_manager
.
terminal
metrics
)
        
status
=
self
.
_build
(
            
monitor
            
metrics
            
what
            
jobs
            
job_size
            
directory
            
verbose
            
keep_going
            
mach_context
            
append_env
        
)
        
record_usage
=
True
        
if
"
MOZ_AUTOMATION
"
in
os
.
environ
and
what
:
            
record_usage
=
False
        
if
record_usage
:
            
monitor
.
record_usage
(
)
        
return
status
    
def
_build
(
        
self
        
monitor
        
metrics
        
what
=
None
        
jobs
=
0
        
job_size
=
0
        
directory
=
None
        
verbose
=
False
        
keep_going
=
False
        
mach_context
=
None
        
append_env
=
None
    
)
:
        
"
"
"
Invoke
the
build
backend
.
        
what
defines
the
thing
to
build
.
If
not
defined
the
default
        
target
is
used
.
        
"
"
"
        
self
.
metrics
=
metrics
        
self
.
mach_context
=
mach_context
        
footer
=
BuildProgressFooter
(
self
.
log_manager
.
terminal
monitor
)
        
mkdir
(
self
.
topobjdir
not_indexed
=
True
)
        
with
BuildOutputManager
(
self
.
log_manager
monitor
footer
)
as
output
:
            
monitor
.
start
(
)
            
if
directory
is
not
None
and
not
what
:
                
print
(
"
Can
only
use
-
C
/
-
-
directory
with
an
explicit
target
name
.
"
)
                
return
1
            
if
directory
is
not
None
:
                
directory
=
mozpath
.
normsep
(
directory
)
                
if
directory
.
startswith
(
"
/
"
)
:
                    
directory
=
directory
[
1
:
]
            
monitor
.
start_resource_recording
(
)
            
if
self
.
_check_clobber
(
self
.
mozconfig
os
.
environ
)
:
                
return
1
            
self
.
mach_context
.
command_attrs
[
"
clobber
"
]
=
False
            
self
.
metrics
.
mozbuild
.
clobber
.
set
(
False
)
            
config
=
None
            
try
:
                
config
=
self
.
config_environment
            
except
Exception
:
                
self
.
mach_context
.
command_attrs
[
"
clobber
"
]
=
True
                
self
.
metrics
.
mozbuild
.
clobber
.
set
(
True
)
            
clobber_requested
=
False
            
self
.
_write_mozconfig_json
(
)
            
previous_backend
=
None
            
if
config
is
not
None
:
                
previous_backend
=
config
.
substs
.
get
(
"
BUILD_BACKENDS
"
[
None
]
)
[
0
]
            
config_rc
=
None
            
if
config
is
None
or
self
.
build_out_of_date
(
                
mozpath
.
join
(
self
.
topobjdir
"
config
.
status
"
)
                
mozpath
.
join
(
self
.
topobjdir
"
config_status_deps
.
in
"
)
            
)
:
                
if
previous_backend
and
"
Make
"
not
in
previous_backend
:
                    
clobber_requested
=
self
.
_clobber_configure
(
)
                
if
config
is
None
:
                    
print
(
"
Config
object
not
found
by
mach
.
"
)
                
config_rc
=
self
.
configure
(
                    
metrics
                    
buildstatus_messages
=
True
                    
line_handler
=
output
.
on_line
                    
append_env
=
append_env
                
)
                
if
config_rc
!
=
0
:
                    
return
config_rc
                
config
=
self
.
reload_config_environment
(
)
            
if
config
.
substs
.
get
(
"
MOZ_USING_CCACHE
"
)
:
                
ccache
=
config
.
substs
.
get
(
"
CCACHE
"
)
                
ccache_start
=
monitor
.
ccache_stats
(
ccache
)
            
else
:
                
ccache_start
=
None
            
substs
=
config
.
substs
            
mozbuild_metrics
=
metrics
.
mozbuild
            
mozbuild_metrics
.
compiler
.
set
(
substs
.
get
(
"
CC_TYPE
"
None
)
)
            
def
get_substs_flag
(
name
)
:
                
return
bool
(
substs
.
get
(
name
None
)
)
            
host
=
substs
.
get
(
"
host
"
)
            
monitor
.
resources
.
metadata
[
"
oscpu
"
]
=
host
            
target
=
substs
.
get
(
"
target
"
)
            
if
host
!
=
target
:
                
monitor
.
resources
.
metadata
[
"
abi
"
]
=
target
            
product_name
=
substs
.
get
(
"
MOZ_BUILD_APP
"
)
            
app_displayname
=
substs
.
get
(
"
MOZ_APP_DISPLAYNAME
"
)
            
if
app_displayname
:
                
product_name
=
app_displayname
                
app_version
=
substs
.
get
(
"
MOZ_APP_VERSION
"
)
                
if
app_version
:
                    
product_name
+
=
"
"
+
app_version
            
monitor
.
resources
.
metadata
[
"
product
"
]
=
product_name
            
mozbuild_metrics
.
artifact
.
set
(
get_substs_flag
(
"
MOZ_ARTIFACT_BUILDS
"
)
)
            
mozbuild_metrics
.
debug
.
set
(
get_substs_flag
(
"
MOZ_DEBUG
"
)
)
            
mozbuild_metrics
.
opt
.
set
(
get_substs_flag
(
"
MOZ_OPTIMIZE
"
)
)
            
mozbuild_metrics
.
ccache
.
set
(
get_substs_flag
(
"
CCACHE
"
)
)
            
using_sccache
=
get_substs_flag
(
"
MOZ_USING_SCCACHE
"
)
            
mozbuild_metrics
.
sccache
.
set
(
using_sccache
)
            
mozbuild_metrics
.
icecream
.
set
(
get_substs_flag
(
"
CXX_IS_ICECREAM
"
)
)
            
mozbuild_metrics
.
project
.
set
(
substs
.
get
(
"
MOZ_BUILD_APP
"
"
"
)
)
            
mozbuild_metrics
.
target
.
set
(
target
)
            
all_backends
=
config
.
substs
.
get
(
"
BUILD_BACKENDS
"
[
None
]
)
            
active_backend
=
all_backends
[
0
]
            
status
=
None
            
if
not
config_rc
and
any
(
[
                
self
.
backend_out_of_date
(
                    
mozpath
.
join
(
self
.
topobjdir
"
backend
.
%
sBackend
"
%
backend
)
                
)
                
for
backend
in
all_backends
            
]
)
:
                
print
(
"
Build
configuration
changed
.
Regenerating
backend
.
"
)
                
args
=
[
                    
config
.
substs
[
"
PYTHON3
"
]
                    
mozpath
.
join
(
self
.
topobjdir
"
config
.
status
"
)
                
]
                
self
.
run_process
(
args
cwd
=
self
.
topobjdir
pass_thru
=
True
)
            
if
jobs
=
=
0
:
                
for
param
in
self
.
mozconfig
.
get
(
"
make_extra
"
)
or
[
]
:
                    
key
value
=
param
.
split
(
"
=
"
1
)
                    
if
key
=
=
"
MOZ_PARALLEL_BUILD
"
:
                        
jobs
=
int
(
value
)
            
if
"
Make
"
not
in
active_backend
:
                
backend_cls
=
get_backend_class
(
active_backend
)
(
config
)
                
status
=
backend_cls
.
build
(
self
output
jobs
verbose
what
)
                
if
status
and
clobber_requested
:
                    
for
line
in
CLOBBER_REQUESTED_MESSAGE
.
splitlines
(
)
:
                        
self
.
log
(
                            
logging
.
WARNING
"
clobber
"
{
"
msg
"
:
line
.
rstrip
(
)
}
"
{
msg
}
"
                        
)
            
if
what
and
status
is
None
:
                
target_pairs
=
[
]
                
for
target
in
what
:
                    
path_arg
=
self
.
_wrap_path_argument
(
target
)
                    
if
directory
is
not
None
:
                        
make_dir
=
mozpath
.
join
(
self
.
topobjdir
directory
)
                        
make_target
=
target
                    
else
:
                        
make_dir
make_target
=
resolve_target_to_make
(
                            
self
.
topobjdir
path_arg
.
relpath
(
)
                        
)
                    
if
make_dir
is
None
and
make_target
is
None
:
                        
return
1
                    
if
config
.
is_artifact_build
and
target
.
startswith
(
"
installers
-
"
)
:
                        
print
(
                            
"
Localized
Builds
are
not
supported
with
Artifact
Builds
enabled
.
\
n
"
                            
"
You
should
disable
Artifact
Builds
(
Use
-
-
disable
-
compile
-
environment
"
                            
"
in
your
mozconfig
instead
)
then
re
-
build
to
proceed
.
"
                        
)
                        
return
1
                    
if
not
make_dir
and
not
make_target
:
                        
print
(
                            
"
The
specified
directory
doesn
'
t
contain
a
"
                            
"
Makefile
and
the
first
parent
with
one
is
the
"
                            
"
root
of
the
tree
.
Please
specify
a
directory
"
                            
"
with
a
Makefile
or
run
|
mach
build
|
if
you
"
                            
"
want
to
build
the
entire
tree
.
"
                        
)
                        
return
1
                    
target_pairs
.
append
(
(
make_dir
make_target
)
)
                
for
make_dir
make_target
in
target_pairs
:
                    
no_build_status
=
"
1
"
if
make_dir
is
not
None
else
"
"
                    
tgt_env
=
dict
(
append_env
or
{
}
)
                    
tgt_env
[
"
NO_BUILDSTATUS_MESSAGES
"
]
=
no_build_status
                    
status
=
self
.
_run_make
(
                        
directory
=
make_dir
                        
target
=
make_target
                        
line_handler
=
output
.
on_line
                        
log
=
False
                        
print_directory
=
False
                        
ensure_exit_code
=
False
                        
num_jobs
=
jobs
                        
job_size
=
job_size
                        
silent
=
not
verbose
                        
append_env
=
tgt_env
                        
keep_going
=
keep_going
                    
)
                    
if
status
!
=
0
:
                        
break
            
elif
status
is
None
:
                
status
=
self
.
_run_client_mk
(
                    
line_handler
=
output
.
on_line
                    
jobs
=
jobs
                    
job_size
=
job_size
                    
verbose
=
verbose
                    
keep_going
=
keep_going
                    
append_env
=
append_env
                
)
            
self
.
log
(
                
logging
.
WARNING
                
"
warning_summary
"
                
{
"
count
"
:
len
(
monitor
.
warnings_database
)
}
                
"
{
count
}
compiler
warnings
present
.
"
            
)
            
try
:
                
active_backend
=
config
.
substs
.
get
(
"
BUILD_BACKENDS
"
[
None
]
)
[
0
]
                
if
active_backend
:
                    
backend_cls
=
get_backend_class
(
active_backend
)
(
config
)
                    
new_status
=
backend_cls
.
post_build
(
                        
self
output
jobs
verbose
status
                    
)
                    
status
=
new_status
            
except
Exception
as
ex
:
                
self
.
log
(
                    
logging
.
DEBUG
                    
"
post_build
"
                    
{
"
ex
"
:
str
(
ex
)
}
                    
"
Unable
to
run
active
build
backend
'
s
post
-
build
step
;
"
                    
+
"
failing
the
build
due
to
exception
:
{
ex
}
.
"
                
)
                
if
not
status
:
                    
status
=
1
            
monitor
.
finish
(
)
        
if
status
=
=
0
:
            
usage
=
monitor
.
get_resource_usage
(
)
            
if
usage
:
                
self
.
mach_context
.
command_attrs
[
"
usage
"
]
=
usage
                
monitor
.
log_resource_usage
(
usage
)
        
if
not
status
:
            
pathToThirdparty
=
mozpath
.
join
(
                
self
.
topsrcdir
"
tools
"
"
rewriting
"
"
ThirdPartyPaths
.
txt
"
            
)
            
pathToGenerated
=
mozpath
.
join
(
                
self
.
topsrcdir
"
tools
"
"
rewriting
"
"
Generated
.
txt
"
            
)
            
if
os
.
path
.
exists
(
pathToThirdparty
)
:
                
with
(
                    
open
(
pathToThirdparty
encoding
=
"
utf
-
8
"
newline
=
"
\
n
"
)
as
f
                    
open
(
pathToGenerated
encoding
=
"
utf
-
8
"
newline
=
"
\
n
"
)
as
g
                
)
:
                    
LOCAL_SUPPRESS_DIRS
=
tuple
(
                        
[
line
.
strip
(
"
\
n
/
"
)
for
line
in
f
]
                        
+
[
line
.
strip
(
"
\
n
/
"
)
for
line
in
g
]
                    
)
            
else
:
                
LOCAL_SUPPRESS_DIRS
=
(
)
            
suppressed_by_dir
=
Counter
(
)
            
THIRD_PARTY_CODE
=
"
third
-
party
code
"
            
suppressed
=
set
(
                
w
.
replace
(
"
-
Wno
-
error
=
"
"
-
W
"
)
                
for
w
in
substs
.
get
(
"
WARNINGS_CFLAGS
"
[
]
)
                
+
substs
.
get
(
"
WARNINGS_CXXFLAGS
"
[
]
)
                
if
w
.
startswith
(
"
-
Wno
-
error
=
"
)
            
)
            
warnings
=
[
]
            
for
warning
in
sorted
(
monitor
.
instance_warnings
)
:
                
path
=
mozpath
.
normsep
(
warning
[
"
filename
"
]
)
                
if
path
.
startswith
(
self
.
topsrcdir
)
:
                    
path
=
path
[
len
(
self
.
topsrcdir
)
+
1
:
]
                
warning
[
"
normpath
"
]
=
path
                
if
"
MOZ_AUTOMATION
"
not
in
os
.
environ
:
                    
if
path
.
startswith
(
LOCAL_SUPPRESS_DIRS
)
:
                        
suppressed_by_dir
[
THIRD_PARTY_CODE
]
+
=
1
                        
continue
                    
if
warning
[
"
flag
"
]
in
suppressed
:
                        
suppressed_by_dir
[
mozpath
.
dirname
(
path
)
]
+
=
1
                        
continue
                
warnings
.
append
(
warning
)
            
if
THIRD_PARTY_CODE
in
suppressed_by_dir
:
                
suppressed_third_party_code
=
[
                    
(
THIRD_PARTY_CODE
suppressed_by_dir
.
pop
(
THIRD_PARTY_CODE
)
)
                
]
            
else
:
                
suppressed_third_party_code
=
[
]
            
for
d
count
in
suppressed_third_party_code
+
sorted
(
                
suppressed_by_dir
.
items
(
)
            
)
:
                
self
.
log
(
                    
logging
.
WARNING
                    
"
suppressed_warning
"
                    
{
"
dir
"
:
d
"
count
"
:
count
}
                    
"
(
suppressed
{
count
}
warnings
in
{
dir
}
)
"
                
)
            
for
warning
in
warnings
:
                
if
warning
[
"
column
"
]
is
not
None
:
                    
self
.
log
(
                        
logging
.
WARNING
                        
"
compiler_warning
"
                        
warning
                        
"
warning
:
{
normpath
}
:
{
line
}
:
{
column
}
[
{
flag
}
]
{
message
}
"
                    
)
                
else
:
                    
self
.
log
(
                        
logging
.
WARNING
                        
"
compiler_warning
"
                        
warning
                        
"
warning
:
{
normpath
}
:
{
line
}
[
{
flag
}
]
{
message
}
"
                    
)
        
high_finder
finder_percent
=
monitor
.
have_high_finder_usage
(
)
        
if
high_finder
:
            
print
(
FINDER_SLOW_MESSAGE
%
finder_percent
)
        
if
config
.
substs
.
get
(
"
MOZ_USING_CCACHE
"
)
:
            
ccache_end
=
monitor
.
ccache_stats
(
ccache
)
        
else
:
            
ccache_end
=
None
        
ccache_diff
=
None
        
if
ccache_start
and
ccache_end
:
            
ccache_diff
=
ccache_end
-
ccache_start
            
if
ccache_diff
:
                
self
.
log
(
                    
logging
.
INFO
                    
"
ccache
"
                    
{
"
msg
"
:
ccache_diff
.
hit_rate_message
(
)
}
                    
"
{
msg
}
"
                
)
        
notify_minimum_time
=
300
        
try
:
            
notify_minimum_time
=
int
(
os
.
environ
.
get
(
"
MACH_NOTIFY_MINTIME
"
"
300
"
)
)
        
except
ValueError
:
            
pass
        
if
monitor
.
elapsed
>
notify_minimum_time
:
            
self
.
notify
(
"
Build
complete
"
if
not
status
else
"
Build
failed
"
)
        
if
status
:
            
if
what
and
any
(
[
                
target
for
target
in
what
if
target
not
in
(
"
faster
"
"
binaries
"
)
            
]
)
:
                
print
(
                    
"
Hey
!
Builds
initiated
with
mach
build
"
                    
"
A_SPECIFIC_TARGET
may
not
always
work
even
if
the
"
                    
"
code
being
built
is
correct
.
Consider
doing
a
bare
"
                    
"
mach
build
instead
.
"
                
)
            
return
status
        
if
monitor
.
have_resource_usage
:
            
excessive
swap_in
swap_out
=
monitor
.
have_excessive_swapping
(
)
            
print
(
"
To
view
a
profile
of
the
build
run
|
mach
resource
-
usage
|
.
"
)
        
long_build
=
monitor
.
elapsed
>
1200
        
if
long_build
:
            
output
.
on_line
(
                
"
We
know
it
took
a
while
but
your
build
finally
finished
successfully
!
"
            
)
            
if
not
using_sccache
:
                
output
.
on_line
(
                    
"
If
you
are
building
Firefox
often
SCCache
can
save
you
a
lot
"
                    
"
of
time
.
You
can
learn
more
here
:
"
                    
"
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
"
                    
"
configuring_build_options
.
html
#
sccache
"
                
)
        
else
:
            
output
.
on_line
(
"
Your
build
was
successful
!
"
)
        
if
not
what
:
            
try
:
                
if
self
.
substs
[
"
MOZ_BUILD_APP
"
]
!
=
"
mobile
/
android
"
:
                    
print
(
"
To
take
your
build
for
a
test
drive
run
:
|
mach
run
|
"
)
                
app
=
self
.
substs
[
"
MOZ_BUILD_APP
"
]
                
if
app
in
(
"
browser
"
"
mobile
/
android
"
)
:
                    
print
(
                        
"
For
more
information
on
what
to
do
now
see
"
                        
"
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
contributing_code
.
html
"
                    
)
            
except
Exception
:
                
pass
        
return
status
    
def
configure
(
        
self
        
metrics
        
options
=
None
        
buildstatus_messages
=
False
        
line_handler
=
None
        
append_env
=
None
    
)
:
        
self
.
metrics
=
metrics
        
mkdir
(
self
.
topobjdir
not_indexed
=
True
)
        
self
.
_write_mozconfig_json
(
)
        
def
on_line
(
line
)
:
            
self
.
log
(
logging
.
INFO
"
build_output
"
{
"
line
"
:
line
}
"
{
line
}
"
)
        
line_handler
=
line_handler
or
on_line
        
append_env
=
dict
(
append_env
or
{
}
)
        
for
line
in
self
.
mozconfig
[
"
make_extra
"
]
or
[
]
:
            
if
line
.
startswith
(
"
export
"
)
:
                
k
eq
v
=
line
[
len
(
"
export
"
)
:
]
.
partition
(
"
=
"
)
                
if
eq
=
=
"
=
"
:
                    
append_env
[
k
]
=
v
        
build_site
=
CommandSiteManager
.
from_environment
(
            
self
.
topsrcdir
            
lambda
:
get_state_dir
(
specific_to_topsrcdir
=
True
topsrcdir
=
self
.
topsrcdir
)
            
"
build
"
            
get_virtualenv_base_dir
(
self
.
topsrcdir
)
        
)
        
build_site
.
ensure
(
)
        
command
=
[
build_site
.
python_path
mozpath
.
join
(
self
.
topsrcdir
"
configure
.
py
"
)
]
        
if
options
:
            
command
.
extend
(
options
)
        
if
buildstatus_messages
:
            
append_env
[
"
MOZ_CONFIGURE_BUILDSTATUS
"
]
=
"
1
"
            
line_handler
(
"
BUILDSTATUS
TIERS
configure
"
)
            
line_handler
(
"
BUILDSTATUS
TIER_START
configure
"
)
        
env
=
os
.
environ
.
copy
(
)
        
env
.
update
(
append_env
)
        
with
subprocess
.
Popen
(
            
command
            
cwd
=
self
.
topobjdir
            
env
=
env
            
stdout
=
subprocess
.
PIPE
            
stderr
=
subprocess
.
STDOUT
            
universal_newlines
=
True
        
)
as
process
:
            
for
line
in
process
.
stdout
:
                
line_handler
(
line
.
rstrip
(
)
)
            
status
=
process
.
wait
(
)
        
if
buildstatus_messages
:
            
line_handler
(
"
BUILDSTATUS
TIER_FINISH
configure
"
)
        
if
status
:
            
print
(
'
*
*
*
Fix
above
errors
and
then
restart
with
"
.
/
mach
build
"
'
)
        
else
:
            
print
(
"
Configure
complete
!
"
)
            
print
(
"
Be
sure
to
run
|
mach
build
|
to
pick
up
any
changes
"
)
        
return
status
    
def
install_tests
(
self
)
:
        
"
"
"
Install
test
files
.
"
"
"
        
if
self
.
is_clobber_needed
(
)
:
            
print
(
                
INSTALL_TESTS_CLOBBER
.
format
(
                    
clobber_file
=
mozpath
.
join
(
self
.
topobjdir
"
CLOBBER
"
)
                
)
            
)
            
sys
.
exit
(
1
)
        
install_test_files
(
mozpath
.
normpath
(
self
.
topsrcdir
)
self
.
topobjdir
"
_tests
"
)
    
def
_clobber_configure
(
self
)
:
        
clobberer
=
Clobberer
(
self
.
topsrcdir
self
.
topobjdir
)
        
clobber_output
=
io
.
StringIO
(
)
        
res
=
clobberer
.
maybe_do_clobber
(
os
.
getcwd
(
)
False
clobber_output
)
        
required
performed
message
=
res
        
assert
not
performed
        
if
not
required
:
            
return
False
        
def
remove_objdir_path
(
path
)
:
            
path
=
mozpath
.
join
(
self
.
topobjdir
path
)
            
self
.
log
(
                
logging
.
WARNING
                
"
clobber
"
                
{
"
path
"
:
path
}
                
"
CLOBBER
file
has
been
updated
removing
{
path
}
.
"
            
)
            
mozfile
.
remove
(
path
)
        
for
f
in
(
"
old
-
configure
.
vars
"
"
config
.
cache
"
"
configure
.
pkl
"
)
:
            
remove_objdir_path
(
f
)
            
remove_objdir_path
(
mozpath
.
join
(
"
js
"
"
src
"
f
)
)
        
rm_dirs
=
[
            
"
_virtualenvs
"
            
"
_tests
"
        
]
        
for
d
in
rm_dirs
:
            
remove_objdir_path
(
d
)
        
os
.
utime
(
mozpath
.
join
(
self
.
topobjdir
"
CLOBBER
"
)
None
)
        
return
True
    
def
_write_mozconfig_json
(
self
)
:
        
mozconfig_json
=
mozpath
.
join
(
self
.
topobjdir
"
.
mozconfig
.
json
"
)
        
with
FileAvoidWrite
(
mozconfig_json
)
as
fh
:
            
to_write
=
json
.
dumps
(
                
{
                    
"
topsrcdir
"
:
self
.
topsrcdir
                    
"
topobjdir
"
:
self
.
topobjdir
                    
"
mozconfig
"
:
self
.
mozconfig
                
}
                
sort_keys
=
True
                
indent
=
2
            
)
            
to_write
=
"
\
n
"
.
join
(
[
line
.
rstrip
(
)
for
line
in
to_write
.
splitlines
(
)
]
)
            
fh
.
write
(
to_write
)
    
def
_run_client_mk
(
        
self
        
target
=
None
        
line_handler
=
None
        
jobs
=
0
        
job_size
=
0
        
verbose
=
None
        
keep_going
=
False
        
append_env
=
None
    
)
:
        
append_env
=
dict
(
append_env
or
{
}
)
        
append_env
[
"
TOPSRCDIR
"
]
=
self
.
topsrcdir
        
append_env
[
"
CONFIG_GUESS
"
]
=
self
.
resolve_config_guess
(
)
        
mozconfig
=
self
.
mozconfig
        
mozconfig_make_lines
=
[
]
        
for
arg
in
mozconfig
[
"
make_extra
"
]
or
[
]
:
            
mozconfig_make_lines
.
append
(
arg
)
        
if
mozconfig
[
"
make_flags
"
]
:
            
mozconfig_make_lines
.
append
(
                
"
MOZ_MAKE_FLAGS
=
%
s
"
%
"
"
.
join
(
mozconfig
[
"
make_flags
"
]
)
            
)
        
objdir
=
mozpath
.
normsep
(
self
.
topobjdir
)
        
mozconfig_make_lines
.
append
(
"
MOZ_OBJDIR
=
%
s
"
%
objdir
)
        
mozconfig_make_lines
.
append
(
"
OBJDIR
=
%
s
"
%
objdir
)
        
if
mozconfig
[
"
path
"
]
:
            
mozconfig_make_lines
.
append
(
                
"
FOUND_MOZCONFIG
=
%
s
"
%
mozpath
.
normsep
(
mozconfig
[
"
path
"
]
)
            
)
            
mozconfig_make_lines
.
append
(
"
export
FOUND_MOZCONFIG
"
)
        
mozconfig_filtered_lines
=
[
            
line
            
for
line
in
mozconfig_make_lines
            
if
line
.
startswith
(
"
export
"
)
or
"
UPLOAD_EXTRA_FILES
"
in
line
        
]
        
mozconfig_client_mk
=
mozpath
.
join
(
self
.
topobjdir
"
.
mozconfig
-
client
-
mk
"
)
        
with
FileAvoidWrite
(
mozconfig_client_mk
)
as
fh
:
            
fh
.
write
(
"
\
n
"
.
join
(
mozconfig_make_lines
)
)
        
mozconfig_mk
=
mozpath
.
join
(
self
.
topobjdir
"
.
mozconfig
.
mk
"
)
        
with
FileAvoidWrite
(
mozconfig_mk
)
as
fh
:
            
fh
.
write
(
"
\
n
"
.
join
(
mozconfig_filtered_lines
)
)
        
mozconfig_objdir
=
mozpath
.
join
(
self
.
topobjdir
"
.
mozconfig
"
)
        
if
mozconfig
[
"
path
"
]
:
            
with
open
(
mozconfig
[
"
path
"
]
)
as
ifh
:
                
with
FileAvoidWrite
(
mozconfig_objdir
)
as
ofh
:
                    
ofh
.
write
(
ifh
.
read
(
)
)
        
else
:
            
try
:
                
os
.
unlink
(
mozconfig_objdir
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
        
if
mozconfig_make_lines
:
            
self
.
log
(
                
logging
.
WARNING
                
"
mozconfig_content
"
                
{
                    
"
path
"
:
mozconfig
[
"
path
"
]
                    
"
content
"
:
"
\
n
"
.
join
(
mozconfig_make_lines
)
                
}
                
"
Adding
make
options
from
{
path
}
\
n
{
content
}
"
            
)
        
append_env
[
"
OBJDIR
"
]
=
mozpath
.
normsep
(
self
.
topobjdir
)
        
return
self
.
_run_make
(
            
srcdir
=
True
            
filename
=
"
client
.
mk
"
            
ensure_exit_code
=
False
            
print_directory
=
False
            
target
=
target
            
line_handler
=
line_handler
            
log
=
False
            
num_jobs
=
jobs
            
job_size
=
job_size
            
silent
=
not
verbose
            
keep_going
=
keep_going
            
append_env
=
append_env
        
)
    
def
_check_clobber
(
self
mozconfig
env
)
:
        
"
"
"
Run
Clobberer
.
maybe_do_clobber
log
the
result
and
return
a
status
bool
.
        
Wraps
the
clobbering
logic
in
Clobberer
.
maybe_do_clobber
to
provide
logging
        
and
handling
of
the
AUTOCLOBBER
mozconfig
option
.
        
Return
a
bool
indicating
whether
the
clobber
reached
an
error
state
.
For
example
        
return
True
if
the
clobber
was
required
but
not
completed
and
return
False
if
        
the
clobber
was
not
required
and
not
completed
.
        
"
"
"
        
auto_clobber
=
any
(
[
            
env
.
get
(
"
AUTOCLOBBER
"
False
)
            
(
mozconfig
[
"
env
"
]
or
{
}
)
.
get
(
"
added
"
{
}
)
.
get
(
"
AUTOCLOBBER
"
False
)
            
"
AUTOCLOBBER
=
1
"
in
(
mozconfig
[
"
make_extra
"
]
or
[
]
)
        
]
)
        
from
mozbuild
.
base
import
BuildEnvironmentNotFoundException
        
substs
=
dict
(
)
        
try
:
            
substs
=
self
.
substs
        
except
BuildEnvironmentNotFoundException
:
            
pass
        
clobberer
=
Clobberer
(
self
.
topsrcdir
self
.
topobjdir
substs
)
        
clobber_output
=
io
.
StringIO
(
)
        
res
=
clobberer
.
maybe_do_clobber
(
os
.
getcwd
(
)
auto_clobber
clobber_output
)
        
clobber_output
.
seek
(
0
)
        
for
line
in
clobber_output
.
readlines
(
)
:
            
self
.
log
(
logging
.
WARNING
"
clobber
"
{
"
msg
"
:
line
.
rstrip
(
)
}
"
{
msg
}
"
)
        
clobber_required
clobber_performed
clobber_message
=
res
        
if
clobber_required
and
not
clobber_performed
:
            
for
line
in
clobber_message
.
splitlines
(
)
:
                
self
.
log
(
logging
.
WARNING
"
clobber
"
{
"
msg
"
:
line
.
rstrip
(
)
}
"
{
msg
}
"
)
            
return
True
        
if
clobber_performed
and
env
.
get
(
"
TINDERBOX_OUTPUT
"
)
:
            
self
.
log
(
                
logging
.
WARNING
                
"
clobber
"
                
{
"
msg
"
:
"
TinderboxPrint
:
auto
clobber
"
}
                
"
{
msg
}
"
            
)
        
return
False
