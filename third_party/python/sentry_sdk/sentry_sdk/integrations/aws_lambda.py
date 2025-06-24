import
functools
import
json
import
re
import
sys
from
copy
import
deepcopy
from
datetime
import
datetime
timedelta
timezone
from
os
import
environ
import
sentry_sdk
from
sentry_sdk
.
api
import
continue_trace
from
sentry_sdk
.
consts
import
OP
from
sentry_sdk
.
scope
import
should_send_default_pii
from
sentry_sdk
.
tracing
import
TransactionSource
from
sentry_sdk
.
utils
import
(
    
AnnotatedValue
    
capture_internal_exceptions
    
ensure_integration_enabled
    
event_from_exception
    
logger
    
TimeoutThread
    
reraise
)
from
sentry_sdk
.
integrations
import
Integration
from
sentry_sdk
.
integrations
.
_wsgi_common
import
_filter_headers
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
TypeVar
    
from
typing
import
Callable
    
from
typing
import
Optional
    
from
sentry_sdk
.
_types
import
EventProcessor
Event
Hint
    
F
=
TypeVar
(
"
F
"
bound
=
Callable
[
.
.
.
Any
]
)
TIMEOUT_WARNING_BUFFER
=
1500
MILLIS_TO_SECONDS
=
1000
.
0
def
_wrap_init_error
(
init_error
)
:
    
ensure_integration_enabled
(
AwsLambdaIntegration
init_error
)
    
def
sentry_init_error
(
*
args
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
        
with
capture_internal_exceptions
(
)
:
            
sentry_sdk
.
get_isolation_scope
(
)
.
clear_breadcrumbs
(
)
            
exc_info
=
sys
.
exc_info
(
)
            
if
exc_info
and
all
(
exc_info
)
:
                
sentry_event
hint
=
event_from_exception
(
                    
exc_info
                    
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
aws_lambda
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
sentry_event
hint
=
hint
)
            
else
:
                
error_info
=
args
[
1
]
                
if
isinstance
(
error_info
str
)
:
                    
error_info
=
json
.
loads
(
error_info
)
                
sentry_event
=
_event_from_error_json
(
error_info
)
                
sentry_sdk
.
capture_event
(
sentry_event
)
        
return
init_error
(
*
args
*
*
kwargs
)
    
return
sentry_init_error
def
_wrap_handler
(
handler
)
:
    
functools
.
wraps
(
handler
)
    
def
sentry_handler
(
aws_event
aws_context
*
args
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
AwsLambdaIntegration
)
        
if
integration
is
None
:
            
return
handler
(
aws_event
aws_context
*
args
*
*
kwargs
)
        
if
isinstance
(
aws_event
list
)
and
len
(
aws_event
)
>
=
1
:
            
request_data
=
aws_event
[
0
]
            
batch_size
=
len
(
aws_event
)
        
else
:
            
request_data
=
aws_event
            
batch_size
=
1
        
if
not
isinstance
(
request_data
dict
)
:
            
request_data
=
{
}
        
configured_time
=
aws_context
.
get_remaining_time_in_millis
(
)
        
with
sentry_sdk
.
isolation_scope
(
)
as
scope
:
            
timeout_thread
=
None
            
with
capture_internal_exceptions
(
)
:
                
scope
.
clear_breadcrumbs
(
)
                
scope
.
add_event_processor
(
                    
_make_request_event_processor
(
                        
request_data
aws_context
configured_time
                    
)
                
)
                
scope
.
set_tag
(
                    
"
aws_region
"
aws_context
.
invoked_function_arn
.
split
(
"
:
"
)
[
3
]
                
)
                
if
batch_size
>
1
:
                    
scope
.
set_tag
(
"
batch_request
"
True
)
                    
scope
.
set_tag
(
"
batch_size
"
batch_size
)
                
if
(
                    
integration
.
timeout_warning
                    
and
configured_time
>
TIMEOUT_WARNING_BUFFER
                
)
:
                    
waiting_time
=
(
                        
configured_time
-
TIMEOUT_WARNING_BUFFER
                    
)
/
MILLIS_TO_SECONDS
                    
timeout_thread
=
TimeoutThread
(
                        
waiting_time
                        
configured_time
/
MILLIS_TO_SECONDS
                    
)
                    
timeout_thread
.
start
(
)
            
headers
=
request_data
.
get
(
"
headers
"
{
}
)
            
if
not
isinstance
(
headers
dict
)
:
                
headers
=
{
}
            
transaction
=
continue_trace
(
                
headers
                
op
=
OP
.
FUNCTION_AWS
                
name
=
aws_context
.
function_name
                
source
=
TransactionSource
.
COMPONENT
                
origin
=
AwsLambdaIntegration
.
origin
            
)
            
with
sentry_sdk
.
start_transaction
(
                
transaction
                
custom_sampling_context
=
{
                    
"
aws_event
"
:
aws_event
                    
"
aws_context
"
:
aws_context
                
}
            
)
:
                
try
:
                    
return
handler
(
aws_event
aws_context
*
args
*
*
kwargs
)
                
except
Exception
:
                    
exc_info
=
sys
.
exc_info
(
)
                    
sentry_event
hint
=
event_from_exception
(
                        
exc_info
                        
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
aws_lambda
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
sentry_event
hint
=
hint
)
                    
reraise
(
*
exc_info
)
                
finally
:
                    
if
timeout_thread
:
                        
timeout_thread
.
stop
(
)
    
return
sentry_handler
def
_drain_queue
(
)
:
    
with
capture_internal_exceptions
(
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
AwsLambdaIntegration
)
        
if
integration
is
not
None
:
            
client
.
flush
(
)
class
AwsLambdaIntegration
(
Integration
)
:
    
identifier
=
"
aws_lambda
"
    
origin
=
f
"
auto
.
function
.
{
identifier
}
"
    
def
__init__
(
self
timeout_warning
=
False
)
:
        
self
.
timeout_warning
=
timeout_warning
    
staticmethod
    
def
setup_once
(
)
:
        
lambda_bootstrap
=
get_lambda_bootstrap
(
)
        
if
not
lambda_bootstrap
:
            
logger
.
warning
(
                
"
Not
running
in
AWS
Lambda
environment
"
                
"
AwsLambdaIntegration
disabled
(
could
not
find
bootstrap
module
)
"
            
)
            
return
        
if
not
hasattr
(
lambda_bootstrap
"
handle_event_request
"
)
:
            
logger
.
warning
(
                
"
Not
running
in
AWS
Lambda
environment
"
                
"
AwsLambdaIntegration
disabled
(
could
not
find
handle_event_request
)
"
            
)
            
return
        
pre_37
=
hasattr
(
lambda_bootstrap
"
handle_http_request
"
)
        
if
pre_37
:
            
old_handle_event_request
=
lambda_bootstrap
.
handle_event_request
            
def
sentry_handle_event_request
(
request_handler
*
args
*
*
kwargs
)
:
                
request_handler
=
_wrap_handler
(
request_handler
)
                
return
old_handle_event_request
(
request_handler
*
args
*
*
kwargs
)
            
lambda_bootstrap
.
handle_event_request
=
sentry_handle_event_request
            
old_handle_http_request
=
lambda_bootstrap
.
handle_http_request
            
def
sentry_handle_http_request
(
request_handler
*
args
*
*
kwargs
)
:
                
request_handler
=
_wrap_handler
(
request_handler
)
                
return
old_handle_http_request
(
request_handler
*
args
*
*
kwargs
)
            
lambda_bootstrap
.
handle_http_request
=
sentry_handle_http_request
            
old_to_json
=
lambda_bootstrap
.
to_json
            
def
sentry_to_json
(
*
args
*
*
kwargs
)
:
                
_drain_queue
(
)
                
return
old_to_json
(
*
args
*
*
kwargs
)
            
lambda_bootstrap
.
to_json
=
sentry_to_json
        
else
:
            
lambda_bootstrap
.
LambdaRuntimeClient
.
post_init_error
=
_wrap_init_error
(
                
lambda_bootstrap
.
LambdaRuntimeClient
.
post_init_error
            
)
            
old_handle_event_request
=
lambda_bootstrap
.
handle_event_request
            
def
sentry_handle_event_request
(
                
lambda_runtime_client
request_handler
*
args
*
*
kwargs
            
)
:
                
request_handler
=
_wrap_handler
(
request_handler
)
                
return
old_handle_event_request
(
                    
lambda_runtime_client
request_handler
*
args
*
*
kwargs
                
)
            
lambda_bootstrap
.
handle_event_request
=
sentry_handle_event_request
            
def
_wrap_post_function
(
f
)
:
                
def
inner
(
*
args
*
*
kwargs
)
:
                    
_drain_queue
(
)
                    
return
f
(
*
args
*
*
kwargs
)
                
return
inner
            
lambda_bootstrap
.
LambdaRuntimeClient
.
post_invocation_result
=
(
                
_wrap_post_function
(
                    
lambda_bootstrap
.
LambdaRuntimeClient
.
post_invocation_result
                
)
            
)
            
lambda_bootstrap
.
LambdaRuntimeClient
.
post_invocation_error
=
(
                
_wrap_post_function
(
                    
lambda_bootstrap
.
LambdaRuntimeClient
.
post_invocation_error
                
)
            
)
def
get_lambda_bootstrap
(
)
:
    
if
"
bootstrap
"
in
sys
.
modules
:
        
return
sys
.
modules
[
"
bootstrap
"
]
    
elif
"
__main__
"
in
sys
.
modules
:
        
module
=
sys
.
modules
[
"
__main__
"
]
        
if
hasattr
(
module
"
awslambdaricmain
"
)
and
hasattr
(
            
module
.
awslambdaricmain
"
bootstrap
"
        
)
:
            
return
module
.
awslambdaricmain
.
bootstrap
        
elif
hasattr
(
module
"
bootstrap
"
)
:
            
return
module
.
bootstrap
        
return
module
    
else
:
        
return
None
def
_make_request_event_processor
(
aws_event
aws_context
configured_timeout
)
:
    
start_time
=
datetime
.
now
(
timezone
.
utc
)
    
def
event_processor
(
sentry_event
hint
start_time
=
start_time
)
:
        
remaining_time_in_milis
=
aws_context
.
get_remaining_time_in_millis
(
)
        
exec_duration
=
configured_timeout
-
remaining_time_in_milis
        
extra
=
sentry_event
.
setdefault
(
"
extra
"
{
}
)
        
extra
[
"
lambda
"
]
=
{
            
"
function_name
"
:
aws_context
.
function_name
            
"
function_version
"
:
aws_context
.
function_version
            
"
invoked_function_arn
"
:
aws_context
.
invoked_function_arn
            
"
aws_request_id
"
:
aws_context
.
aws_request_id
            
"
execution_duration_in_millis
"
:
exec_duration
            
"
remaining_time_in_millis
"
:
remaining_time_in_milis
        
}
        
extra
[
"
cloudwatch
logs
"
]
=
{
            
"
url
"
:
_get_cloudwatch_logs_url
(
aws_context
start_time
)
            
"
log_group
"
:
aws_context
.
log_group_name
            
"
log_stream
"
:
aws_context
.
log_stream_name
        
}
        
request
=
sentry_event
.
get
(
"
request
"
{
}
)
        
if
"
httpMethod
"
in
aws_event
:
            
request
[
"
method
"
]
=
aws_event
[
"
httpMethod
"
]
        
request
[
"
url
"
]
=
_get_url
(
aws_event
aws_context
)
        
if
"
queryStringParameters
"
in
aws_event
:
            
request
[
"
query_string
"
]
=
aws_event
[
"
queryStringParameters
"
]
        
if
"
headers
"
in
aws_event
:
            
request
[
"
headers
"
]
=
_filter_headers
(
aws_event
[
"
headers
"
]
)
        
if
should_send_default_pii
(
)
:
            
user_info
=
sentry_event
.
setdefault
(
"
user
"
{
}
)
            
identity
=
aws_event
.
get
(
"
identity
"
)
            
if
identity
is
None
:
                
identity
=
{
}
            
id
=
identity
.
get
(
"
userArn
"
)
            
if
id
is
not
None
:
                
user_info
.
setdefault
(
"
id
"
id
)
            
ip
=
identity
.
get
(
"
sourceIp
"
)
            
if
ip
is
not
None
:
                
user_info
.
setdefault
(
"
ip_address
"
ip
)
            
if
"
body
"
in
aws_event
:
                
request
[
"
data
"
]
=
aws_event
.
get
(
"
body
"
"
"
)
        
else
:
            
if
aws_event
.
get
(
"
body
"
None
)
:
                
request
[
"
data
"
]
=
AnnotatedValue
.
removed_because_raw_data
(
)
        
sentry_event
[
"
request
"
]
=
deepcopy
(
request
)
        
return
sentry_event
    
return
event_processor
def
_get_url
(
aws_event
aws_context
)
:
    
path
=
aws_event
.
get
(
"
path
"
None
)
    
headers
=
aws_event
.
get
(
"
headers
"
)
    
if
headers
is
None
:
        
headers
=
{
}
    
host
=
headers
.
get
(
"
Host
"
None
)
    
proto
=
headers
.
get
(
"
X
-
Forwarded
-
Proto
"
None
)
    
if
proto
and
host
and
path
:
        
return
"
{
}
:
/
/
{
}
{
}
"
.
format
(
proto
host
path
)
    
return
"
awslambda
:
/
/
/
{
}
"
.
format
(
aws_context
.
function_name
)
def
_get_cloudwatch_logs_url
(
aws_context
start_time
)
:
    
"
"
"
    
Generates
a
CloudWatchLogs
console
URL
based
on
the
context
object
    
Arguments
:
        
aws_context
{
Any
}
-
-
context
from
lambda
handler
    
Returns
:
        
str
-
-
AWS
Console
URL
to
logs
.
    
"
"
"
    
formatstring
=
"
%
Y
-
%
m
-
%
dT
%
H
:
%
M
:
%
SZ
"
    
region
=
environ
.
get
(
"
AWS_REGION
"
"
"
)
    
url
=
(
        
"
https
:
/
/
console
.
{
domain
}
/
cloudwatch
/
home
?
region
=
{
region
}
"
        
"
#
logEventViewer
:
group
=
{
log_group
}
;
stream
=
{
log_stream
}
"
        
"
;
start
=
{
start_time
}
;
end
=
{
end_time
}
"
    
)
.
format
(
        
domain
=
"
amazonaws
.
cn
"
if
region
.
startswith
(
"
cn
-
"
)
else
"
aws
.
amazon
.
com
"
        
region
=
region
        
log_group
=
aws_context
.
log_group_name
        
log_stream
=
aws_context
.
log_stream_name
        
start_time
=
(
start_time
-
timedelta
(
seconds
=
1
)
)
.
strftime
(
formatstring
)
        
end_time
=
(
datetime
.
now
(
timezone
.
utc
)
+
timedelta
(
seconds
=
2
)
)
.
strftime
(
            
formatstring
        
)
    
)
    
return
url
def
_parse_formatted_traceback
(
formatted_tb
)
:
    
frames
=
[
]
    
for
frame
in
formatted_tb
:
        
match
=
re
.
match
(
r
'
File
"
(
.
+
)
"
line
(
\
d
+
)
in
(
.
+
)
'
frame
.
strip
(
)
)
        
if
match
:
            
file_name
line_number
func_name
=
match
.
groups
(
)
            
line_number
=
int
(
line_number
)
            
frames
.
append
(
                
{
                    
"
filename
"
:
file_name
                    
"
function
"
:
func_name
                    
"
lineno
"
:
line_number
                    
"
vars
"
:
None
                    
"
pre_context
"
:
None
                    
"
context_line
"
:
None
                    
"
post_context
"
:
None
                
}
            
)
    
return
frames
def
_event_from_error_json
(
error_json
)
:
    
"
"
"
    
Converts
the
error
JSON
from
AWS
Lambda
into
a
Sentry
error
event
.
    
This
is
not
a
full
fletched
event
but
better
than
nothing
.
    
This
is
an
example
of
where
AWS
creates
the
error
JSON
:
    
https
:
/
/
github
.
com
/
aws
/
aws
-
lambda
-
python
-
runtime
-
interface
-
client
/
blob
/
2
.
2
.
1
/
awslambdaric
/
bootstrap
.
py
#
L479
    
"
"
"
    
event
=
{
        
"
level
"
:
"
error
"
        
"
exception
"
:
{
            
"
values
"
:
[
                
{
                    
"
type
"
:
error_json
.
get
(
"
errorType
"
)
                    
"
value
"
:
error_json
.
get
(
"
errorMessage
"
)
                    
"
stacktrace
"
:
{
                        
"
frames
"
:
_parse_formatted_traceback
(
                            
error_json
.
get
(
"
stackTrace
"
[
]
)
                        
)
                    
}
                    
"
mechanism
"
:
{
                        
"
type
"
:
"
aws_lambda
"
                        
"
handled
"
:
False
                    
}
                
}
            
]
        
}
    
}
    
return
event
