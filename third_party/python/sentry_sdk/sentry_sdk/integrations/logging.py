import
logging
import
sys
from
datetime
import
datetime
timezone
from
fnmatch
import
fnmatch
import
sentry_sdk
from
sentry_sdk
.
client
import
BaseClient
from
sentry_sdk
.
logger
import
_log_level_to_otel
from
sentry_sdk
.
utils
import
(
    
safe_repr
    
to_string
    
event_from_exception
    
current_stacktrace
    
capture_internal_exceptions
)
from
sentry_sdk
.
integrations
import
Integration
from
typing
import
TYPE_CHECKING
if
TYPE_CHECKING
:
    
from
collections
.
abc
import
MutableMapping
    
from
logging
import
LogRecord
    
from
typing
import
Any
    
from
typing
import
Dict
    
from
typing
import
Optional
DEFAULT_LEVEL
=
logging
.
INFO
DEFAULT_EVENT_LEVEL
=
logging
.
ERROR
LOGGING_TO_EVENT_LEVEL
=
{
    
logging
.
NOTSET
:
"
notset
"
    
logging
.
DEBUG
:
"
debug
"
    
logging
.
INFO
:
"
info
"
    
logging
.
WARN
:
"
warning
"
    
logging
.
WARNING
:
"
warning
"
    
logging
.
ERROR
:
"
error
"
    
logging
.
FATAL
:
"
fatal
"
    
logging
.
CRITICAL
:
"
fatal
"
}
SEVERITY_TO_OTEL_SEVERITY
=
{
    
logging
.
CRITICAL
:
21
    
logging
.
ERROR
:
17
    
logging
.
WARNING
:
13
    
logging
.
INFO
:
9
    
logging
.
DEBUG
:
5
}
_IGNORED_LOGGERS
=
set
(
    
[
"
sentry_sdk
.
errors
"
"
urllib3
.
connectionpool
"
"
urllib3
.
connection
"
]
)
def
ignore_logger
(
    
name
)
:
    
"
"
"
This
disables
recording
(
both
in
breadcrumbs
and
as
events
)
calls
to
    
a
logger
of
a
specific
name
.
Among
other
uses
many
of
our
integrations
    
use
this
to
prevent
their
actions
being
recorded
as
breadcrumbs
.
Exposed
    
to
users
as
a
way
to
quiet
spammy
loggers
.
    
:
param
name
:
The
name
of
the
logger
to
ignore
(
same
string
you
would
pass
to
logging
.
getLogger
)
.
    
"
"
"
    
_IGNORED_LOGGERS
.
add
(
name
)
class
LoggingIntegration
(
Integration
)
:
    
identifier
=
"
logging
"
    
def
__init__
(
        
self
        
level
=
DEFAULT_LEVEL
        
event_level
=
DEFAULT_EVENT_LEVEL
        
sentry_logs_level
=
DEFAULT_LEVEL
    
)
:
        
self
.
_handler
=
None
        
self
.
_breadcrumb_handler
=
None
        
self
.
_sentry_logs_handler
=
None
        
if
level
is
not
None
:
            
self
.
_breadcrumb_handler
=
BreadcrumbHandler
(
level
=
level
)
        
if
sentry_logs_level
is
not
None
:
            
self
.
_sentry_logs_handler
=
SentryLogsHandler
(
level
=
sentry_logs_level
)
        
if
event_level
is
not
None
:
            
self
.
_handler
=
EventHandler
(
level
=
event_level
)
    
def
_handle_record
(
self
record
)
:
        
if
self
.
_handler
is
not
None
and
record
.
levelno
>
=
self
.
_handler
.
level
:
            
self
.
_handler
.
handle
(
record
)
        
if
(
            
self
.
_breadcrumb_handler
is
not
None
            
and
record
.
levelno
>
=
self
.
_breadcrumb_handler
.
level
        
)
:
            
self
.
_breadcrumb_handler
.
handle
(
record
)
        
if
(
            
self
.
_sentry_logs_handler
is
not
None
            
and
record
.
levelno
>
=
self
.
_sentry_logs_handler
.
level
        
)
:
            
self
.
_sentry_logs_handler
.
handle
(
record
)
    
staticmethod
    
def
setup_once
(
)
:
        
old_callhandlers
=
logging
.
Logger
.
callHandlers
        
def
sentry_patched_callhandlers
(
self
record
)
:
            
ignored_loggers
=
_IGNORED_LOGGERS
            
try
:
                
return
old_callhandlers
(
self
record
)
            
finally
:
                
if
(
                    
ignored_loggers
is
not
None
                    
and
record
.
name
.
strip
(
)
not
in
ignored_loggers
                
)
:
                    
integration
=
sentry_sdk
.
get_client
(
)
.
get_integration
(
                        
LoggingIntegration
                    
)
                    
if
integration
is
not
None
:
                        
integration
.
_handle_record
(
record
)
        
logging
.
Logger
.
callHandlers
=
sentry_patched_callhandlers
class
_BaseHandler
(
logging
.
Handler
)
:
    
COMMON_RECORD_ATTRS
=
frozenset
(
        
(
            
"
args
"
            
"
created
"
            
"
exc_info
"
            
"
exc_text
"
            
"
filename
"
            
"
funcName
"
            
"
levelname
"
            
"
levelno
"
            
"
linenno
"
            
"
lineno
"
            
"
message
"
            
"
module
"
            
"
msecs
"
            
"
msg
"
            
"
name
"
            
"
pathname
"
            
"
process
"
            
"
processName
"
            
"
relativeCreated
"
            
"
stack
"
            
"
tags
"
            
"
taskName
"
            
"
thread
"
            
"
threadName
"
            
"
stack_info
"
        
)
    
)
    
def
_can_record
(
self
record
)
:
        
"
"
"
Prevents
ignored
loggers
from
recording
"
"
"
        
for
logger
in
_IGNORED_LOGGERS
:
            
if
fnmatch
(
record
.
name
.
strip
(
)
logger
)
:
                
return
False
        
return
True
    
def
_logging_to_event_level
(
self
record
)
:
        
return
LOGGING_TO_EVENT_LEVEL
.
get
(
            
record
.
levelno
record
.
levelname
.
lower
(
)
if
record
.
levelname
else
"
"
        
)
    
def
_extra_from_record
(
self
record
)
:
        
return
{
            
k
:
v
            
for
k
v
in
vars
(
record
)
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
COMMON_RECORD_ATTRS
            
and
(
not
isinstance
(
k
str
)
or
not
k
.
startswith
(
"
_
"
)
)
        
}
class
EventHandler
(
_BaseHandler
)
:
    
"
"
"
    
A
logging
handler
that
emits
Sentry
events
for
each
log
record
    
Note
that
you
do
not
have
to
use
this
class
if
the
logging
integration
is
enabled
which
it
is
by
default
.
    
"
"
"
    
def
emit
(
self
record
)
:
        
with
capture_internal_exceptions
(
)
:
            
self
.
format
(
record
)
            
return
self
.
_emit
(
record
)
    
def
_emit
(
self
record
)
:
        
if
not
self
.
_can_record
(
record
)
:
            
return
        
client
=
sentry_sdk
.
get_client
(
)
        
if
not
client
.
is_active
(
)
:
            
return
        
client_options
=
client
.
options
        
if
record
.
exc_info
and
record
.
exc_info
[
0
]
is
not
None
:
            
event
hint
=
event_from_exception
(
                
record
.
exc_info
                
client_options
=
client_options
                
mechanism
=
{
"
type
"
:
"
logging
"
"
handled
"
:
True
}
            
)
        
elif
(
record
.
exc_info
and
record
.
exc_info
[
0
]
is
None
)
or
record
.
stack_info
:
            
event
=
{
}
            
hint
=
{
}
            
with
capture_internal_exceptions
(
)
:
                
event
[
"
threads
"
]
=
{
                    
"
values
"
:
[
                        
{
                            
"
stacktrace
"
:
current_stacktrace
(
                                
include_local_variables
=
client_options
[
                                    
"
include_local_variables
"
                                
]
                                
max_value_length
=
client_options
[
"
max_value_length
"
]
                            
)
                            
"
crashed
"
:
False
                            
"
current
"
:
True
                        
}
                    
]
                
}
        
else
:
            
event
=
{
}
            
hint
=
{
}
        
hint
[
"
log_record
"
]
=
record
        
level
=
self
.
_logging_to_event_level
(
record
)
        
if
level
in
{
"
debug
"
"
info
"
"
warning
"
"
error
"
"
critical
"
"
fatal
"
}
:
            
event
[
"
level
"
]
=
level
        
event
[
"
logger
"
]
=
record
.
name
        
if
(
            
sys
.
version_info
<
(
3
11
)
            
and
record
.
name
=
=
"
py
.
warnings
"
            
and
record
.
msg
=
=
"
%
s
"
        
)
:
            
message
=
record
.
args
[
0
]
            
params
=
(
)
        
else
:
            
message
=
record
.
msg
            
params
=
record
.
args
        
event
[
"
logentry
"
]
=
{
            
"
message
"
:
to_string
(
message
)
            
"
formatted
"
:
record
.
getMessage
(
)
            
"
params
"
:
params
        
}
        
event
[
"
extra
"
]
=
self
.
_extra_from_record
(
record
)
        
sentry_sdk
.
capture_event
(
event
hint
=
hint
)
SentryHandler
=
EventHandler
class
BreadcrumbHandler
(
_BaseHandler
)
:
    
"
"
"
    
A
logging
handler
that
records
breadcrumbs
for
each
log
record
.
    
Note
that
you
do
not
have
to
use
this
class
if
the
logging
integration
is
enabled
which
it
is
by
default
.
    
"
"
"
    
def
emit
(
self
record
)
:
        
with
capture_internal_exceptions
(
)
:
            
self
.
format
(
record
)
            
return
self
.
_emit
(
record
)
    
def
_emit
(
self
record
)
:
        
if
not
self
.
_can_record
(
record
)
:
            
return
        
sentry_sdk
.
add_breadcrumb
(
            
self
.
_breadcrumb_from_record
(
record
)
hint
=
{
"
log_record
"
:
record
}
        
)
    
def
_breadcrumb_from_record
(
self
record
)
:
        
return
{
            
"
type
"
:
"
log
"
            
"
level
"
:
self
.
_logging_to_event_level
(
record
)
            
"
category
"
:
record
.
name
            
"
message
"
:
record
.
message
            
"
timestamp
"
:
datetime
.
fromtimestamp
(
record
.
created
timezone
.
utc
)
            
"
data
"
:
self
.
_extra_from_record
(
record
)
        
}
class
SentryLogsHandler
(
_BaseHandler
)
:
    
"
"
"
    
A
logging
handler
that
records
Sentry
logs
for
each
Python
log
record
.
    
Note
that
you
do
not
have
to
use
this
class
if
the
logging
integration
is
enabled
which
it
is
by
default
.
    
"
"
"
    
def
emit
(
self
record
)
:
        
with
capture_internal_exceptions
(
)
:
            
self
.
format
(
record
)
            
if
not
self
.
_can_record
(
record
)
:
                
return
            
client
=
sentry_sdk
.
get_client
(
)
            
if
not
client
.
is_active
(
)
:
                
return
            
if
not
client
.
options
[
"
_experiments
"
]
.
get
(
"
enable_logs
"
False
)
:
                
return
            
self
.
_capture_log_from_record
(
client
record
)
    
def
_capture_log_from_record
(
self
client
record
)
:
        
otel_severity_number
otel_severity_text
=
_log_level_to_otel
(
            
record
.
levelno
SEVERITY_TO_OTEL_SEVERITY
        
)
        
project_root
=
client
.
options
[
"
project_root
"
]
        
attrs
=
self
.
_extra_from_record
(
record
)
        
attrs
[
"
sentry
.
origin
"
]
=
"
auto
.
logger
.
log
"
        
if
isinstance
(
record
.
msg
str
)
:
            
attrs
[
"
sentry
.
message
.
template
"
]
=
record
.
msg
        
if
record
.
args
is
not
None
:
            
if
isinstance
(
record
.
args
tuple
)
:
                
for
i
arg
in
enumerate
(
record
.
args
)
:
                    
attrs
[
f
"
sentry
.
message
.
parameter
.
{
i
}
"
]
=
(
                        
arg
                        
if
isinstance
(
arg
(
str
float
int
bool
)
)
                        
else
safe_repr
(
arg
)
                    
)
        
if
record
.
lineno
:
            
attrs
[
"
code
.
line
.
number
"
]
=
record
.
lineno
        
if
record
.
pathname
:
            
if
project_root
is
not
None
and
record
.
pathname
.
startswith
(
project_root
)
:
                
attrs
[
"
code
.
file
.
path
"
]
=
record
.
pathname
[
len
(
project_root
)
+
1
:
]
            
else
:
                
attrs
[
"
code
.
file
.
path
"
]
=
record
.
pathname
        
if
record
.
funcName
:
            
attrs
[
"
code
.
function
.
name
"
]
=
record
.
funcName
        
if
record
.
thread
:
            
attrs
[
"
thread
.
id
"
]
=
record
.
thread
        
if
record
.
threadName
:
            
attrs
[
"
thread
.
name
"
]
=
record
.
threadName
        
if
record
.
process
:
            
attrs
[
"
process
.
pid
"
]
=
record
.
process
        
if
record
.
processName
:
            
attrs
[
"
process
.
executable
.
name
"
]
=
record
.
processName
        
if
record
.
name
:
            
attrs
[
"
logger
.
name
"
]
=
record
.
name
        
client
.
_capture_experimental_log
(
            
{
                
"
severity_text
"
:
otel_severity_text
                
"
severity_number
"
:
otel_severity_number
                
"
body
"
:
record
.
message
                
"
attributes
"
:
attrs
                
"
time_unix_nano
"
:
int
(
record
.
created
*
1e9
)
                
"
trace_id
"
:
None
            
}
        
)
