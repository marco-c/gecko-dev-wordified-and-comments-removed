from
sentry_sdk
.
_types
import
MYPY
if
MYPY
:
    
from
typing
import
Optional
    
from
typing
import
Callable
    
from
typing
import
Union
    
from
typing
import
List
    
from
typing
import
Type
    
from
typing
import
Dict
    
from
typing
import
Any
    
from
typing
import
Sequence
    
from
typing_extensions
import
TypedDict
    
from
sentry_sdk
.
transport
import
Transport
    
from
sentry_sdk
.
integrations
import
Integration
    
from
sentry_sdk
.
_types
import
Event
EventProcessor
BreadcrumbProcessor
    
Experiments
=
TypedDict
(
        
"
Experiments
"
        
{
            
"
max_spans
"
:
Optional
[
int
]
            
"
record_sql_params
"
:
Optional
[
bool
]
            
"
auto_enabling_integrations
"
:
Optional
[
bool
]
            
"
auto_session_tracking
"
:
Optional
[
bool
]
        
}
        
total
=
False
    
)
class
ClientConstructor
(
object
)
:
    
def
__init__
(
        
self
        
dsn
=
None
        
with_locals
=
True
        
max_breadcrumbs
=
100
        
release
=
None
        
environment
=
None
        
server_name
=
None
        
shutdown_timeout
=
2
        
integrations
=
[
]
        
in_app_include
=
[
]
        
in_app_exclude
=
[
]
        
default_integrations
=
True
        
dist
=
None
        
transport
=
None
        
sample_rate
=
1
.
0
        
send_default_pii
=
False
        
http_proxy
=
None
        
https_proxy
=
None
        
ignore_errors
=
[
]
        
request_bodies
=
"
medium
"
        
before_send
=
None
        
before_breadcrumb
=
None
        
debug
=
False
        
attach_stacktrace
=
False
        
ca_certs
=
None
        
propagate_traces
=
True
        
traces_sample_rate
=
0
.
0
        
traceparent_v2
=
False
        
_experiments
=
{
}
    
)
:
        
pass
def
_get_default_options
(
)
:
    
import
inspect
    
if
hasattr
(
inspect
"
getfullargspec
"
)
:
        
getargspec
=
inspect
.
getfullargspec
    
else
:
        
getargspec
=
inspect
.
getargspec
    
a
=
getargspec
(
ClientConstructor
.
__init__
)
    
defaults
=
a
.
defaults
or
(
)
    
return
dict
(
zip
(
a
.
args
[
-
len
(
defaults
)
:
]
defaults
)
)
DEFAULT_OPTIONS
=
_get_default_options
(
)
del
_get_default_options
VERSION
=
"
0
.
14
.
3
"
SDK_INFO
=
{
    
"
name
"
:
"
sentry
.
python
"
    
"
version
"
:
VERSION
    
"
packages
"
:
[
{
"
name
"
:
"
pypi
:
sentry
-
sdk
"
"
version
"
:
VERSION
}
]
}
