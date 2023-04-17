from
__future__
import
absolute_import
import
abc
import
re
from
os
.
path
import
expanduser
from
threading
import
Thread
import
sentry_sdk
from
mozboot
.
util
import
get_state_dir
from
mach
.
telemetry
import
is_telemetry_enabled
from
mozversioncontrol
import
(
    
get_repository_object
    
InvalidRepoPath
    
MissingUpstreamRepo
    
MissingVCSTool
)
from
six
import
string_types
_SENTRY_DSN
=
"
https
:
/
/
8228c9aff64949c2ba4a2154dc515f55
sentry
.
prod
.
mozaws
.
net
/
525
"
class
ErrorReporter
(
object
)
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
"
hg
-
rev
-
{
}
"
.
format
(
base_ref
)
    
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
string_types
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
(
target_path
replacement
)
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
topsrcdir
"
<
topsrcdir
>
"
)
        
(
expanduser
(
"
~
"
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
)
:
    
try
:
        
return
get_repository_object
(
topsrcdir
)
    
except
(
InvalidRepoPath
MissingVCSTool
)
:
        
return
None
def
_is_unmodified_mach_core
(
topsrcdir
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
