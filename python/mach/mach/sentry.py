import
abc
import
re
import
sys
from
pathlib
import
Path
from
threading
import
Thread
import
sentry_sdk
from
mozversioncontrol
import
(
    
InvalidRepoPath
    
MissingUpstreamRepo
    
MissingVCSTool
    
get_repository_object
)
from
mach
.
telemetry
import
is_telemetry_enabled
from
mach
.
util
import
get_state_dir
_SENTRY_DSN
=
(
    
"
https
:
/
/
5cfe351fb3a24e8d82c751252b48722b
o1069899
.
ingest
.
sentry
.
io
/
6250014
"
)
class
ErrorReporter
:
    
abc
.
abstractmethod
    
def
report_exception
(
self
exception
)
:
        
"
"
"
Report
the
exception
to
remote
error
-
tracking
software
.
"
"
"
class
SentryErrorReporter
(
ErrorReporter
)
:
    
"
"
"
Reports
errors
using
Sentry
.
"
"
"
    
def
report_exception
(
self
exception
)
:
        
return
sentry_sdk
.
capture_exception
(
exception
)
class
NoopErrorReporter
(
ErrorReporter
)
:
    
"
"
"
Drops
errors
instead
of
reporting
them
.
    
This
is
useful
in
cases
where
error
-
reporting
is
specifically
disabled
such
as
    
when
telemetry
hasn
'
t
been
allowed
.
    
"
"
"
    
def
report_exception
(
self
exception
)
:
        
return
None
def
register_sentry
(
argv
settings
topsrcdir
:
Path
)
:
    
if
not
is_telemetry_enabled
(
settings
)
:
        
return
NoopErrorReporter
(
)
    
global
_is_unmodified_mach_core_thread
    
_is_unmodified_mach_core_thread
=
Thread
(
        
target
=
_is_unmodified_mach_core
        
args
=
[
topsrcdir
]
        
daemon
=
True
    
)
    
_is_unmodified_mach_core_thread
.
start
(
)
    
sentry_sdk
.
init
(
        
_SENTRY_DSN
before_send
=
lambda
event
_
:
_process_event
(
event
topsrcdir
)
    
)
    
sentry_sdk
.
add_breadcrumb
(
message
=
"
.
/
mach
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
argv
)
)
)
    
return
SentryErrorReporter
(
)
def
_process_event
(
sentry_event
topsrcdir
:
Path
)
:
    
repo
=
_get_repository_object
(
topsrcdir
)
    
if
repo
is
None
:
        
return
    
if
repo
.
name
in
(
"
git
"
"
jj
"
)
and
not
repo
.
is_cinnabar_repo
(
)
:
        
base_ref
=
repo
.
base_ref_as_commit
(
)
    
else
:
        
base_ref
=
repo
.
base_ref_as_hg
(
)
    
if
not
base_ref
:
        
return
    
_is_unmodified_mach_core_thread
.
join
(
)
    
if
not
_is_unmodified_mach_core_result
:
        
return
    
for
map_fn
in
(
_settle_mach_module_id
_patch_absolute_paths
_delete_server_name
)
:
        
sentry_event
=
map_fn
(
sentry_event
topsrcdir
)
    
sentry_event
[
"
release
"
]
=
f
"
hg
-
rev
-
{
base_ref
}
"
    
return
sentry_event
def
_settle_mach_module_id
(
sentry_event
_
)
:
    
stacktrace_frames
=
sentry_event
[
"
exception
"
]
[
"
values
"
]
[
0
]
[
"
stacktrace
"
]
[
"
frames
"
]
    
for
frame
in
stacktrace_frames
:
        
module
=
frame
.
get
(
"
module
"
)
        
if
not
module
:
            
continue
        
module
=
re
.
sub
(
            
"
mach
\
\
.
commands
\
\
.
[
a
-
f0
-
9
]
{
32
}
"
"
mach
.
commands
.
<
generated
>
"
module
        
)
        
frame
[
"
module
"
]
=
module
    
return
sentry_event
def
_patch_absolute_paths
(
sentry_event
topsrcdir
:
Path
)
:
    
def
recursive_patch
(
value
needle
replacement
)
:
        
if
isinstance
(
value
list
)
:
            
return
[
recursive_patch
(
v
needle
replacement
)
for
v
in
value
]
        
elif
isinstance
(
value
dict
)
:
            
for
key
in
list
(
value
.
keys
(
)
)
:
                
next_value
=
value
.
pop
(
key
)
                
key
=
needle
.
sub
(
replacement
key
)
                
value
[
key
]
=
recursive_patch
(
next_value
needle
replacement
)
            
return
value
        
elif
isinstance
(
value
str
)
:
            
return
needle
.
sub
(
replacement
value
)
        
else
:
            
return
value
    
for
target_path
replacement
in
(
        
(
get_state_dir
(
)
"
<
statedir
>
"
)
        
(
str
(
topsrcdir
)
"
<
topsrcdir
>
"
)
        
(
str
(
Path
.
home
(
)
)
"
~
"
)
    
)
:
        
repr_path
=
repr
(
target_path
)
[
1
:
-
1
]
        
for
target
in
(
target_path
repr_path
)
:
            
if
target
.
startswith
(
"
/
"
)
:
                
target
=
"
/
?
"
+
target
[
1
:
]
            
slash_regex
=
re
.
compile
(
r
"
[
\
/
\
\
]
"
)
            
target
=
slash_regex
.
sub
(
r
"
[
\
\
/
\
\
\
\
]
"
target
)
            
needle_regex
=
re
.
compile
(
target
re
.
IGNORECASE
)
            
sentry_event
=
recursive_patch
(
sentry_event
needle_regex
replacement
)
    
return
sentry_event
def
_delete_server_name
(
sentry_event
_
)
:
    
sentry_event
.
pop
(
"
server_name
"
)
    
return
sentry_event
def
_get_repository_object
(
topsrcdir
:
Path
)
:
    
try
:
        
return
get_repository_object
(
str
(
topsrcdir
)
)
    
except
(
InvalidRepoPath
MissingVCSTool
)
as
e
:
        
print
(
f
"
Warning
:
{
e
}
"
file
=
sys
.
stderr
)
        
return
None
def
_is_unmodified_mach_core
(
topsrcdir
:
Path
)
:
    
"
"
"
True
if
mach
is
unmodified
compared
to
the
public
tree
.
    
To
avoid
submitting
Sentry
events
for
errors
caused
by
user
'
s
    
local
changes
we
attempt
to
detect
if
mach
(
or
code
affecting
mach
)
    
has
been
modified
in
the
user
'
s
local
state
:
    
*
In
a
revision
off
of
a
"
ancestor
to
central
"
revision
or
:
    
*
In
the
working
uncommitted
state
.
    
If
"
topsrcdir
/
mach
"
and
"
*
.
py
"
haven
'
t
been
touched
then
we
can
be
    
pretty
confident
that
the
Mach
behaviour
that
caused
the
exception
    
also
exists
in
the
public
tree
.
    
"
"
"
    
global
_is_unmodified_mach_core_result
    
repo
=
_get_repository_object
(
topsrcdir
)
    
try
:
        
files
=
set
(
repo
.
get_outgoing_files
(
)
)
|
set
(
repo
.
get_changed_files
(
)
)
        
_is_unmodified_mach_core_result
=
not
any
(
[
            
file
for
file
in
files
if
file
=
=
"
mach
"
or
file
.
endswith
(
"
.
py
"
)
        
]
)
    
except
MissingUpstreamRepo
:
        
_is_unmodified_mach_core_result
=
False
_is_unmodified_mach_core_result
=
None
_is_unmodified_mach_core_thread
=
None
