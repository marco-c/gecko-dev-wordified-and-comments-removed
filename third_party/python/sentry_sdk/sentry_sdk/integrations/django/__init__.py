#
-
*
-
coding
:
utf
-
8
-
*
-
from
__future__
import
absolute_import
import
sys
import
threading
import
weakref
from
sentry_sdk
.
_types
import
MYPY
from
sentry_sdk
.
consts
import
OP
SENSITIVE_DATA_SUBSTITUTE
from
sentry_sdk
.
hub
import
Hub
_should_send_default_pii
from
sentry_sdk
.
scope
import
add_global_event_processor
from
sentry_sdk
.
serializer
import
add_global_repr_processor
from
sentry_sdk
.
tracing
import
SOURCE_FOR_STYLE
TRANSACTION_SOURCE_URL
from
sentry_sdk
.
tracing_utils
import
record_sql_queries
from
sentry_sdk
.
utils
import
(
    
AnnotatedValue
    
HAS_REAL_CONTEXTVARS
    
CONTEXTVARS_ERROR_MESSAGE
    
logger
    
capture_internal_exceptions
    
event_from_exception
    
transaction_from_function
    
walk_exception_chain
)
from
sentry_sdk
.
integrations
import
Integration
DidNotEnable
from
sentry_sdk
.
integrations
.
logging
import
ignore_logger
from
sentry_sdk
.
integrations
.
wsgi
import
SentryWsgiMiddleware
from
sentry_sdk
.
integrations
.
_wsgi_common
import
RequestExtractor
try
:
    
from
django
import
VERSION
as
DJANGO_VERSION
    
from
django
.
conf
import
settings
as
django_settings
    
from
django
.
core
import
signals
    
try
:
        
from
django
.
urls
import
resolve
    
except
ImportError
:
        
from
django
.
core
.
urlresolvers
import
resolve
except
ImportError
:
    
raise
DidNotEnable
(
"
Django
not
installed
"
)
from
sentry_sdk
.
integrations
.
django
.
transactions
import
LEGACY_RESOLVER
from
sentry_sdk
.
integrations
.
django
.
templates
import
(
    
get_template_frame_from_exception
    
patch_templates
)
from
sentry_sdk
.
integrations
.
django
.
middleware
import
patch_django_middlewares
from
sentry_sdk
.
integrations
.
django
.
signals_handlers
import
patch_signals
from
sentry_sdk
.
integrations
.
django
.
views
import
patch_views
if
MYPY
:
    
from
typing
import
Any
    
from
typing
import
Callable
    
from
typing
import
Dict
    
from
typing
import
Optional
    
from
typing
import
Union
    
from
typing
import
List
    
from
django
.
core
.
handlers
.
wsgi
import
WSGIRequest
    
from
django
.
http
.
response
import
HttpResponse
    
from
django
.
http
.
request
import
QueryDict
    
from
django
.
utils
.
datastructures
import
MultiValueDict
    
from
sentry_sdk
.
scope
import
Scope
    
from
sentry_sdk
.
integrations
.
wsgi
import
_ScopedResponse
    
from
sentry_sdk
.
_types
import
Event
Hint
EventProcessor
NotImplementedType
if
DJANGO_VERSION
<
(
1
10
)
:
    
def
is_authenticated
(
request_user
)
:
        
return
request_user
.
is_authenticated
(
)
else
:
    
def
is_authenticated
(
request_user
)
:
        
return
request_user
.
is_authenticated
TRANSACTION_STYLE_VALUES
=
(
"
function_name
"
"
url
"
)
class
DjangoIntegration
(
Integration
)
:
    
identifier
=
"
django
"
    
transaction_style
=
"
"
    
middleware_spans
=
None
    
def
__init__
(
self
transaction_style
=
"
url
"
middleware_spans
=
True
)
:
        
if
transaction_style
not
in
TRANSACTION_STYLE_VALUES
:
            
raise
ValueError
(
                
"
Invalid
value
for
transaction_style
:
%
s
(
must
be
in
%
s
)
"
                
%
(
transaction_style
TRANSACTION_STYLE_VALUES
)
            
)
        
self
.
transaction_style
=
transaction_style
        
self
.
middleware_spans
=
middleware_spans
    
staticmethod
    
def
setup_once
(
)
:
        
if
DJANGO_VERSION
<
(
1
8
)
:
            
raise
DidNotEnable
(
"
Django
1
.
8
or
newer
is
required
.
"
)
        
install_sql_hook
(
)
        
ignore_logger
(
"
django
.
server
"
)
        
ignore_logger
(
"
django
.
request
"
)
        
from
django
.
core
.
handlers
.
wsgi
import
WSGIHandler
        
old_app
=
WSGIHandler
.
__call__
        
def
sentry_patched_wsgi_handler
(
self
environ
start_response
)
:
            
if
Hub
.
current
.
get_integration
(
DjangoIntegration
)
is
None
:
                
return
old_app
(
self
environ
start_response
)
            
bound_old_app
=
old_app
.
__get__
(
self
WSGIHandler
)
            
from
django
.
conf
import
settings
            
use_x_forwarded_for
=
settings
.
USE_X_FORWARDED_HOST
            
return
SentryWsgiMiddleware
(
bound_old_app
use_x_forwarded_for
)
(
                
environ
start_response
            
)
        
WSGIHandler
.
__call__
=
sentry_patched_wsgi_handler
        
_patch_get_response
(
)
        
_patch_django_asgi_handler
(
)
        
signals
.
got_request_exception
.
connect
(
_got_request_exception
)
        
add_global_event_processor
        
def
process_django_templates
(
event
hint
)
:
            
if
hint
is
None
:
                
return
event
            
exc_info
=
hint
.
get
(
"
exc_info
"
None
)
            
if
exc_info
is
None
:
                
return
event
            
exception
=
event
.
get
(
"
exception
"
None
)
            
if
exception
is
None
:
                
return
event
            
values
=
exception
.
get
(
"
values
"
None
)
            
if
values
is
None
:
                
return
event
            
for
exception
(
_
exc_value
_
)
in
zip
(
                
reversed
(
values
)
walk_exception_chain
(
exc_info
)
            
)
:
                
frame
=
get_template_frame_from_exception
(
exc_value
)
                
if
frame
is
not
None
:
                    
frames
=
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
                    
for
i
in
reversed
(
range
(
len
(
frames
)
)
)
:
                        
f
=
frames
[
i
]
                        
if
(
                            
f
.
get
(
"
function
"
)
in
(
"
Parser
.
parse
"
"
parse
"
"
render
"
)
                            
and
f
.
get
(
"
module
"
)
=
=
"
django
.
template
.
base
"
                        
)
:
                            
i
+
=
1
                            
break
                    
else
:
                        
i
=
len
(
frames
)
                    
frames
.
insert
(
i
frame
)
            
return
event
        
add_global_repr_processor
        
def
_django_queryset_repr
(
value
hint
)
:
            
try
:
                
from
django
.
db
.
models
.
query
import
QuerySet
            
except
Exception
:
                
return
NotImplemented
            
if
not
isinstance
(
value
QuerySet
)
or
value
.
_result_cache
:
                
return
NotImplemented
            
return
"
<
%
s
from
%
s
at
0x
%
x
>
"
%
(
                
value
.
__class__
.
__name__
                
value
.
__module__
                
id
(
value
)
            
)
        
_patch_channels
(
)
        
patch_django_middlewares
(
)
        
patch_views
(
)
        
patch_templates
(
)
        
patch_signals
(
)
_DRF_PATCHED
=
False
_DRF_PATCH_LOCK
=
threading
.
Lock
(
)
def
_patch_drf
(
)
:
    
"
"
"
    
Patch
Django
Rest
Framework
for
more
/
better
request
data
.
DRF
'
s
request
    
type
is
a
wrapper
around
Django
'
s
request
type
.
The
attribute
we
'
re
    
interested
in
is
request
.
data
which
is
a
cached
property
containing
a
    
parsed
request
body
.
Reading
a
request
body
from
that
property
is
more
    
reliable
than
reading
from
any
of
Django
'
s
own
properties
as
those
don
'
t
    
hold
payloads
in
memory
and
therefore
can
only
be
accessed
once
.
    
We
patch
the
Django
request
object
to
include
a
weak
backreference
to
the
    
DRF
request
object
such
that
we
can
later
use
either
in
    
DjangoRequestExtractor
.
    
This
function
is
not
called
directly
on
SDK
setup
because
importing
almost
    
any
part
of
Django
Rest
Framework
will
try
to
access
Django
settings
(
where
    
sentry_sdk
.
init
(
)
might
be
called
from
in
the
first
place
)
.
Instead
we
    
run
this
function
on
every
request
and
do
the
patching
on
the
first
    
request
.
    
"
"
"
    
global
_DRF_PATCHED
    
if
_DRF_PATCHED
:
        
return
    
with
_DRF_PATCH_LOCK
:
        
if
_DRF_PATCHED
:
            
return
        
_DRF_PATCHED
=
True
        
with
capture_internal_exceptions
(
)
:
            
try
:
                
from
rest_framework
.
views
import
APIView
            
except
ImportError
:
                
pass
            
else
:
                
old_drf_initial
=
APIView
.
initial
                
def
sentry_patched_drf_initial
(
self
request
*
args
*
*
kwargs
)
:
                    
with
capture_internal_exceptions
(
)
:
                        
request
.
_request
.
_sentry_drf_request_backref
=
weakref
.
ref
(
                            
request
                        
)
                        
pass
                    
return
old_drf_initial
(
self
request
*
args
*
*
kwargs
)
                
APIView
.
initial
=
sentry_patched_drf_initial
def
_patch_channels
(
)
:
    
try
:
        
from
channels
.
http
import
AsgiHandler
    
except
ImportError
:
        
return
    
if
not
HAS_REAL_CONTEXTVARS
:
        
logger
.
warning
(
            
"
We
detected
that
you
are
using
Django
channels
2
.
0
.
"
            
+
CONTEXTVARS_ERROR_MESSAGE
        
)
    
from
sentry_sdk
.
integrations
.
django
.
asgi
import
patch_channels_asgi_handler_impl
    
patch_channels_asgi_handler_impl
(
AsgiHandler
)
def
_patch_django_asgi_handler
(
)
:
    
try
:
        
from
django
.
core
.
handlers
.
asgi
import
ASGIHandler
    
except
ImportError
:
        
return
    
if
not
HAS_REAL_CONTEXTVARS
:
        
logger
.
warning
(
            
"
We
detected
that
you
are
using
Django
3
.
"
+
CONTEXTVARS_ERROR_MESSAGE
        
)
    
from
sentry_sdk
.
integrations
.
django
.
asgi
import
patch_django_asgi_handler_impl
    
patch_django_asgi_handler_impl
(
ASGIHandler
)
def
_set_transaction_name_and_source
(
scope
transaction_style
request
)
:
    
try
:
        
transaction_name
=
None
        
if
transaction_style
=
=
"
function_name
"
:
            
fn
=
resolve
(
request
.
path
)
.
func
            
transaction_name
=
transaction_from_function
(
getattr
(
fn
"
view_class
"
fn
)
)
        
elif
transaction_style
=
=
"
url
"
:
            
if
hasattr
(
request
"
urlconf
"
)
:
                
transaction_name
=
LEGACY_RESOLVER
.
resolve
(
                    
request
.
path_info
urlconf
=
request
.
urlconf
                
)
            
else
:
                
transaction_name
=
LEGACY_RESOLVER
.
resolve
(
request
.
path_info
)
        
if
transaction_name
is
None
:
            
transaction_name
=
request
.
path_info
            
source
=
TRANSACTION_SOURCE_URL
        
else
:
            
source
=
SOURCE_FOR_STYLE
[
transaction_style
]
        
scope
.
set_transaction_name
(
            
transaction_name
            
source
=
source
        
)
    
except
Exception
:
        
pass
def
_before_get_response
(
request
)
:
    
hub
=
Hub
.
current
    
integration
=
hub
.
get_integration
(
DjangoIntegration
)
    
if
integration
is
None
:
        
return
    
_patch_drf
(
)
    
with
hub
.
configure_scope
(
)
as
scope
:
        
_set_transaction_name_and_source
(
scope
integration
.
transaction_style
request
)
        
scope
.
add_event_processor
(
            
_make_event_processor
(
weakref
.
ref
(
request
)
integration
)
        
)
def
_attempt_resolve_again
(
request
scope
transaction_style
)
:
    
"
"
"
    
Some
django
middlewares
overwrite
request
.
urlconf
    
so
we
need
to
respect
that
contract
    
so
we
try
to
resolve
the
url
again
.
    
"
"
"
    
if
not
hasattr
(
request
"
urlconf
"
)
:
        
return
    
_set_transaction_name_and_source
(
scope
transaction_style
request
)
def
_after_get_response
(
request
)
:
    
hub
=
Hub
.
current
    
integration
=
hub
.
get_integration
(
DjangoIntegration
)
    
if
integration
is
None
or
integration
.
transaction_style
!
=
"
url
"
:
        
return
    
with
hub
.
configure_scope
(
)
as
scope
:
        
_attempt_resolve_again
(
request
scope
integration
.
transaction_style
)
def
_patch_get_response
(
)
:
    
"
"
"
    
patch
get_response
because
at
that
point
we
have
the
Django
request
object
    
"
"
"
    
from
django
.
core
.
handlers
.
base
import
BaseHandler
    
old_get_response
=
BaseHandler
.
get_response
    
def
sentry_patched_get_response
(
self
request
)
:
        
_before_get_response
(
request
)
        
rv
=
old_get_response
(
self
request
)
        
_after_get_response
(
request
)
        
return
rv
    
BaseHandler
.
get_response
=
sentry_patched_get_response
    
if
hasattr
(
BaseHandler
"
get_response_async
"
)
:
        
from
sentry_sdk
.
integrations
.
django
.
asgi
import
patch_get_response_async
        
patch_get_response_async
(
BaseHandler
_before_get_response
)
def
_make_event_processor
(
weak_request
integration
)
:
    
def
event_processor
(
event
hint
)
:
        
request
=
weak_request
(
)
        
if
request
is
None
:
            
return
event
        
try
:
            
drf_request
=
request
.
_sentry_drf_request_backref
(
)
            
if
drf_request
is
not
None
:
                
request
=
drf_request
        
except
AttributeError
:
            
pass
        
with
capture_internal_exceptions
(
)
:
            
DjangoRequestExtractor
(
request
)
.
extract_into_event
(
event
)
        
if
_should_send_default_pii
(
)
:
            
with
capture_internal_exceptions
(
)
:
                
_set_user_info
(
request
event
)
        
return
event
    
return
event_processor
def
_got_request_exception
(
request
=
None
*
*
kwargs
)
:
    
hub
=
Hub
.
current
    
integration
=
hub
.
get_integration
(
DjangoIntegration
)
    
if
integration
is
not
None
:
        
if
request
is
not
None
and
integration
.
transaction_style
=
=
"
url
"
:
            
with
hub
.
configure_scope
(
)
as
scope
:
                
_attempt_resolve_again
(
request
scope
integration
.
transaction_style
)
        
client
=
hub
.
client
        
event
hint
=
event_from_exception
(
            
sys
.
exc_info
(
)
            
client_options
=
client
.
options
            
mechanism
=
{
"
type
"
:
"
django
"
"
handled
"
:
False
}
        
)
        
hub
.
capture_event
(
event
hint
=
hint
)
class
DjangoRequestExtractor
(
RequestExtractor
)
:
    
def
env
(
self
)
:
        
return
self
.
request
.
META
    
def
cookies
(
self
)
:
        
privacy_cookies
=
[
            
django_settings
.
CSRF_COOKIE_NAME
            
django_settings
.
SESSION_COOKIE_NAME
        
]
        
clean_cookies
=
{
}
        
for
(
key
val
)
in
self
.
request
.
COOKIES
.
items
(
)
:
            
if
key
in
privacy_cookies
:
                
clean_cookies
[
key
]
=
SENSITIVE_DATA_SUBSTITUTE
            
else
:
                
clean_cookies
[
key
]
=
val
        
return
clean_cookies
    
def
raw_data
(
self
)
:
        
return
self
.
request
.
body
    
def
form
(
self
)
:
        
return
self
.
request
.
POST
    
def
files
(
self
)
:
        
return
self
.
request
.
FILES
    
def
size_of_file
(
self
file
)
:
        
return
file
.
size
    
def
parsed_body
(
self
)
:
        
try
:
            
return
self
.
request
.
data
        
except
AttributeError
:
            
return
RequestExtractor
.
parsed_body
(
self
)
def
_set_user_info
(
request
event
)
:
    
user_info
=
event
.
setdefault
(
"
user
"
{
}
)
    
user
=
getattr
(
request
"
user
"
None
)
    
if
user
is
None
or
not
is_authenticated
(
user
)
:
        
return
    
try
:
        
user_info
.
setdefault
(
"
id
"
str
(
user
.
pk
)
)
    
except
Exception
:
        
pass
    
try
:
        
user_info
.
setdefault
(
"
email
"
user
.
email
)
    
except
Exception
:
        
pass
    
try
:
        
user_info
.
setdefault
(
"
username
"
user
.
get_username
(
)
)
    
except
Exception
:
        
pass
def
install_sql_hook
(
)
:
    
"
"
"
If
installed
this
causes
Django
'
s
queries
to
be
captured
.
"
"
"
    
try
:
        
from
django
.
db
.
backends
.
utils
import
CursorWrapper
    
except
ImportError
:
        
from
django
.
db
.
backends
.
util
import
CursorWrapper
    
try
:
        
from
django
.
db
.
backends
import
BaseDatabaseWrapper
    
except
ImportError
:
        
from
django
.
db
.
backends
.
base
.
base
import
BaseDatabaseWrapper
    
try
:
        
real_execute
=
CursorWrapper
.
execute
        
real_executemany
=
CursorWrapper
.
executemany
        
real_connect
=
BaseDatabaseWrapper
.
connect
    
except
AttributeError
:
        
return
    
def
execute
(
self
sql
params
=
None
)
:
        
hub
=
Hub
.
current
        
if
hub
.
get_integration
(
DjangoIntegration
)
is
None
:
            
return
real_execute
(
self
sql
params
)
        
with
record_sql_queries
(
            
hub
self
.
cursor
sql
params
paramstyle
=
"
format
"
executemany
=
False
        
)
:
            
return
real_execute
(
self
sql
params
)
    
def
executemany
(
self
sql
param_list
)
:
        
hub
=
Hub
.
current
        
if
hub
.
get_integration
(
DjangoIntegration
)
is
None
:
            
return
real_executemany
(
self
sql
param_list
)
        
with
record_sql_queries
(
            
hub
self
.
cursor
sql
param_list
paramstyle
=
"
format
"
executemany
=
True
        
)
:
            
return
real_executemany
(
self
sql
param_list
)
    
def
connect
(
self
)
:
        
hub
=
Hub
.
current
        
if
hub
.
get_integration
(
DjangoIntegration
)
is
None
:
            
return
real_connect
(
self
)
        
with
capture_internal_exceptions
(
)
:
            
hub
.
add_breadcrumb
(
message
=
"
connect
"
category
=
"
query
"
)
        
with
hub
.
start_span
(
op
=
OP
.
DB
description
=
"
connect
"
)
:
            
return
real_connect
(
self
)
    
CursorWrapper
.
execute
=
execute
    
CursorWrapper
.
executemany
=
executemany
    
BaseDatabaseWrapper
.
connect
=
connect
    
ignore_logger
(
"
django
.
db
.
backends
"
)
