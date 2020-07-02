from
__future__
import
absolute_import
import
abc
import
os
import
re
from
os
.
path
import
expanduser
import
sentry_sdk
from
mozboot
.
util
import
get_state_dir
from
mozversioncontrol
import
get_repository_object
InvalidRepoPath
from
six
import
string_types
from
six
.
moves
.
configparser
import
SafeConfigParser
NoOptionError
_DEVELOPER_BLOCKLIST
=
[
    
'
ahalberstadt
mozilla
.
com
'
    
'
mhentges
mozilla
.
com
'
    
'
rstewart
mozilla
.
com
'
    
'
sledru
mozilla
.
com
'
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
_is_telemetry_enabled
(
cfg_file
)
:
    
config
=
SafeConfigParser
(
)
    
if
not
config
.
read
(
cfg_file
)
:
        
return
False
    
try
:
        
telemetry_enabled
=
config
.
getboolean
(
"
build
"
"
telemetry
"
)
    
except
NoOptionError
:
        
return
False
    
if
not
telemetry_enabled
:
        
return
False
    
return
True
def
register_sentry
(
argv
topsrcdir
=
None
)
:
    
cfg_file
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
machrc
'
)
    
if
not
_is_telemetry_enabled
(
cfg_file
)
:
        
return
NoopErrorReporter
(
)
    
if
topsrcdir
:
        
try
:
            
repo
=
get_repository_object
(
topsrcdir
)
            
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
        
except
InvalidRepoPath
:
            
pass
    
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
