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
(
    
abspath
    
expanduser
    
join
)
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
_DEVELOPER_BLOCKLIST
=
[
    
"
ahalberstadt
mozilla
.
com
"
    
"
mhentges
mozilla
.
com
"
    
"
rstewart
mozilla
.
com
"
    
"
sledru
mozilla
.
com
"
]
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
        
pass
def
register_sentry
(
argv
settings
topsrcdir
=
None
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
    
if
topsrcdir
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
not
None
:
            
email
=
repo
.
get_user_email
(
)
            
if
email
in
_DEVELOPER_BLOCKLIST
:
                
return
NoopErrorReporter
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
    
if
_any_modified_files_matching_event
(
sentry_event
topsrcdir
)
:
        
return
None
    
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
needle
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
        
(
repr
(
expanduser
(
"
~
"
)
)
[
1
:
-
1
]
"
~
"
)
    
)
:
        
if
needle
is
None
:
            
continue
        
needle_regex
=
re
.
compile
(
re
.
escape
(
needle
)
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
_any_modified_files_matching_event
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
False
    
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
    
except
MissingUpstreamRepo
:
        
return
False
    
files
=
set
(
abspath
(
join
(
topsrcdir
s
)
)
for
s
in
files
)
    
for
exception
in
sentry_event
.
get
(
"
exception
"
{
}
)
.
get
(
"
values
"
[
]
)
:
        
for
frame
in
exception
.
get
(
"
stacktrace
"
{
}
)
.
get
(
"
frames
"
[
]
)
:
            
if
frame
.
get
(
"
abs_path
"
None
)
in
files
:
                
return
True
    
return
False
