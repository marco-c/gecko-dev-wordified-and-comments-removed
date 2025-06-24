import
inspect
import
sys
import
threading
import
weakref
from
importlib
import
import_module
import
sentry_sdk
from
sentry_sdk
.
consts
import
OP
SPANDATA
from
sentry_sdk
.
scope
import
add_global_event_processor
should_send_default_pii
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
TransactionSource
from
sentry_sdk
.
tracing_utils
import
add_query_source
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
    
SENSITIVE_DATA_SUBSTITUTE
    
logger
    
capture_internal_exceptions
    
ensure_integration_enabled
    
event_from_exception
    
transaction_from_function
    
walk_exception_chain
)
from
sentry_sdk
.
integrations
import
_check_minimum_version
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
(
    
DEFAULT_HTTP_METHODS_TO_CAPTURE
    
RequestExtractor
)
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
    
from
django
.
conf
import
settings
    
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
    
try
:
        
from
django
.
urls
import
Resolver404
    
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
Resolver404
    
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
ASGIRequest
    
except
Exception
:
        
ASGIRequest
=
None
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
DJANGO_VERSION
[
:
2
]
>
(
1
8
)
:
    
from
sentry_sdk
.
integrations
.
django
.
caching
import
patch_caching
else
:
    
patch_caching
=
None
from
typing
import
TYPE_CHECKING
if
TYPE_CHECKING
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
tracing
import
Span
    
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
    
"
"
"
    
Auto
instrument
a
Django
application
.
    
:
param
transaction_style
:
How
to
derive
transaction
names
.
Either
"
function_name
"
or
"
url
"
.
Defaults
to
"
url
"
.
    
:
param
middleware_spans
:
Whether
to
create
spans
for
middleware
.
Defaults
to
True
.
    
:
param
signals_spans
:
Whether
to
create
spans
for
signals
.
Defaults
to
True
.
    
:
param
signals_denylist
:
A
list
of
signals
to
ignore
when
creating
spans
.
    
:
param
cache_spans
:
Whether
to
create
spans
for
cache
operations
.
Defaults
to
False
.
    
"
"
"
    
identifier
=
"
django
"
    
origin
=
f
"
auto
.
http
.
{
identifier
}
"
    
origin_db
=
f
"
auto
.
db
.
{
identifier
}
"
    
transaction_style
=
"
"
    
middleware_spans
=
None
    
signals_spans
=
None
    
cache_spans
=
None
    
signals_denylist
=
[
]
    
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
        
signals_spans
=
True
        
cache_spans
=
False
        
signals_denylist
=
None
        
http_methods_to_capture
=
DEFAULT_HTTP_METHODS_TO_CAPTURE
    
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
        
self
.
signals_spans
=
signals_spans
        
self
.
signals_denylist
=
signals_denylist
or
[
]
        
self
.
cache_spans
=
cache_spans
        
self
.
http_methods_to_capture
=
tuple
(
map
(
str
.
upper
http_methods_to_capture
)
)
    
staticmethod
    
def
setup_once
(
)
:
        
_check_minimum_version
(
DjangoIntegration
DJANGO_VERSION
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
        
ensure_integration_enabled
(
DjangoIntegration
old_app
)
        
def
sentry_patched_wsgi_handler
(
self
environ
start_response
)
:
            
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
DjangoIntegration
)
            
middleware
=
SentryWsgiMiddleware
(
                
bound_old_app
                
use_x_forwarded_for
                
span_origin
=
DjangoIntegration
.
origin
                
http_methods_to_capture
=
(
                    
integration
.
http_methods_to_capture
                    
if
integration
                    
else
DEFAULT_HTTP_METHODS_TO_CAPTURE
                
)
            
)
            
return
middleware
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
        
if
patch_caching
is
not
None
:
            
patch_caching
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
TransactionSource
.
URL
        
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
Resolver404
:
        
urlconf
=
import_module
(
settings
.
ROOT_URLCONF
)
        
if
hasattr
(
urlconf
"
handler404
"
)
:
            
handler
=
urlconf
.
handler404
            
if
isinstance
(
handler
str
)
:
                
scope
.
transaction
=
handler
            
else
:
                
scope
.
transaction
=
transaction_from_function
(
                    
getattr
(
handler
"
view_class
"
handler
)
                
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
    
scope
=
sentry_sdk
.
get_current_scope
(
)
    
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
        
_make_wsgi_request_event_processor
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
    
scope
=
sentry_sdk
.
get_current_scope
(
)
    
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
_make_wsgi_request_event_processor
(
weak_request
integration
)
:
    
def
wsgi_request_event_processor
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
        
django_3
=
ASGIRequest
is
not
None
        
if
django_3
and
type
(
request
)
=
=
ASGIRequest
:
            
return
event
        
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
should_send_default_pii
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
wsgi_request_event_processor
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
    
client
=
sentry_sdk
.
get_client
(
)
    
integration
=
client
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
        
scope
=
sentry_sdk
.
get_current_scope
(
)
        
_attempt_resolve_again
(
request
scope
integration
.
transaction_style
)
    
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
    
sentry_sdk
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
__init__
(
self
request
)
:
        
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
        
self
.
request
=
request
    
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
key
val
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
Exception
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
    
ensure_integration_enabled
(
DjangoIntegration
real_execute
)
    
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
        
with
record_sql_queries
(
            
cursor
=
self
.
cursor
            
query
=
sql
            
params_list
=
params
            
paramstyle
=
"
format
"
            
executemany
=
False
            
span_origin
=
DjangoIntegration
.
origin_db
        
)
as
span
:
            
_set_db_data
(
span
self
)
            
result
=
real_execute
(
self
sql
params
)
        
with
capture_internal_exceptions
(
)
:
            
add_query_source
(
span
)
        
return
result
    
ensure_integration_enabled
(
DjangoIntegration
real_executemany
)
    
def
executemany
(
self
sql
param_list
)
:
        
with
record_sql_queries
(
            
cursor
=
self
.
cursor
            
query
=
sql
            
params_list
=
param_list
            
paramstyle
=
"
format
"
            
executemany
=
True
            
span_origin
=
DjangoIntegration
.
origin_db
        
)
as
span
:
            
_set_db_data
(
span
self
)
            
result
=
real_executemany
(
self
sql
param_list
)
        
with
capture_internal_exceptions
(
)
:
            
add_query_source
(
span
)
        
return
result
    
ensure_integration_enabled
(
DjangoIntegration
real_connect
)
    
def
connect
(
self
)
:
        
with
capture_internal_exceptions
(
)
:
            
sentry_sdk
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
sentry_sdk
.
start_span
(
            
op
=
OP
.
DB
            
name
=
"
connect
"
            
origin
=
DjangoIntegration
.
origin_db
        
)
as
span
:
            
_set_db_data
(
span
self
)
            
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
def
_set_db_data
(
span
cursor_or_db
)
:
    
db
=
cursor_or_db
.
db
if
hasattr
(
cursor_or_db
"
db
"
)
else
cursor_or_db
    
vendor
=
db
.
vendor
    
span
.
set_data
(
SPANDATA
.
DB_SYSTEM
vendor
)
    
is_psycopg2
=
(
        
hasattr
(
cursor_or_db
"
connection
"
)
        
and
hasattr
(
cursor_or_db
.
connection
"
get_dsn_parameters
"
)
        
and
inspect
.
isroutine
(
cursor_or_db
.
connection
.
get_dsn_parameters
)
    
)
    
if
is_psycopg2
:
        
connection_params
=
cursor_or_db
.
connection
.
get_dsn_parameters
(
)
    
else
:
        
try
:
            
connection_params
=
{
                
"
dbname
"
:
cursor_or_db
.
connection
.
info
.
dbname
                
"
port
"
:
cursor_or_db
.
connection
.
info
.
port
            
}
            
pg_host
=
cursor_or_db
.
connection
.
info
.
host
            
if
pg_host
and
not
pg_host
.
startswith
(
"
/
"
)
:
                
connection_params
[
"
host
"
]
=
pg_host
        
except
Exception
:
            
connection_params
=
db
.
get_connection_params
(
)
    
db_name
=
connection_params
.
get
(
"
dbname
"
)
or
connection_params
.
get
(
"
database
"
)
    
if
db_name
is
not
None
:
        
span
.
set_data
(
SPANDATA
.
DB_NAME
db_name
)
    
server_address
=
connection_params
.
get
(
"
host
"
)
    
if
server_address
is
not
None
:
        
span
.
set_data
(
SPANDATA
.
SERVER_ADDRESS
server_address
)
    
server_port
=
connection_params
.
get
(
"
port
"
)
    
if
server_port
is
not
None
:
        
span
.
set_data
(
SPANDATA
.
SERVER_PORT
str
(
server_port
)
)
    
server_socket_address
=
connection_params
.
get
(
"
unix_socket
"
)
    
if
server_socket_address
is
not
None
:
        
span
.
set_data
(
SPANDATA
.
SERVER_SOCKET_ADDRESS
server_socket_address
)
