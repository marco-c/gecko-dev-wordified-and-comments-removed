from
sentry_sdk
import
Hub
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
from
sentry_sdk
.
integrations
import
DidNotEnable
from
sentry_sdk
.
tracing
import
Transaction
TRANSACTION_SOURCE_CUSTOM
from
sentry_sdk
.
utils
import
event_from_exception
if
MYPY
:
    
from
collections
.
abc
import
Awaitable
Callable
    
from
typing
import
Any
try
:
    
import
grpc
    
from
grpc
import
HandlerCallDetails
RpcMethodHandler
    
from
grpc
.
aio
import
AbortError
ServicerContext
except
ImportError
:
    
raise
DidNotEnable
(
"
grpcio
is
not
installed
"
)
class
ServerInterceptor
(
grpc
.
aio
.
ServerInterceptor
)
:
    
def
__init__
(
self
find_name
=
None
)
:
        
self
.
_find_method_name
=
find_name
or
self
.
_find_name
        
super
(
ServerInterceptor
self
)
.
__init__
(
)
    
async
def
intercept_service
(
self
continuation
handler_call_details
)
:
        
self
.
_handler_call_details
=
handler_call_details
        
handler
=
await
continuation
(
handler_call_details
)
        
if
not
handler
.
request_streaming
and
not
handler
.
response_streaming
:
            
handler_factory
=
grpc
.
unary_unary_rpc_method_handler
            
async
def
wrapped
(
request
context
)
:
                
name
=
self
.
_find_method_name
(
context
)
                
if
not
name
:
                    
return
await
handler
(
request
context
)
                
hub
=
Hub
.
current
                
transaction
=
Transaction
.
continue_from_headers
(
                    
dict
(
context
.
invocation_metadata
(
)
)
                    
op
=
OP
.
GRPC_SERVER
                    
name
=
name
                    
source
=
TRANSACTION_SOURCE_CUSTOM
                
)
                
with
hub
.
start_transaction
(
transaction
=
transaction
)
:
                    
try
:
                        
return
await
handler
.
unary_unary
(
request
context
)
                    
except
AbortError
:
                        
raise
                    
except
Exception
as
exc
:
                        
event
hint
=
event_from_exception
(
                            
exc
                            
mechanism
=
{
"
type
"
:
"
grpc
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
                        
raise
        
elif
not
handler
.
request_streaming
and
handler
.
response_streaming
:
            
handler_factory
=
grpc
.
unary_stream_rpc_method_handler
            
async
def
wrapped
(
request
context
)
:
                
async
for
r
in
handler
.
unary_stream
(
request
context
)
:
                    
yield
r
        
elif
handler
.
request_streaming
and
not
handler
.
response_streaming
:
            
handler_factory
=
grpc
.
stream_unary_rpc_method_handler
            
async
def
wrapped
(
request
context
)
:
                
response
=
handler
.
stream_unary
(
request
context
)
                
return
await
response
        
elif
handler
.
request_streaming
and
handler
.
response_streaming
:
            
handler_factory
=
grpc
.
stream_stream_rpc_method_handler
            
async
def
wrapped
(
request
context
)
:
                
async
for
r
in
handler
.
stream_stream
(
request
context
)
:
                    
yield
r
        
return
handler_factory
(
            
wrapped
            
request_deserializer
=
handler
.
request_deserializer
            
response_serializer
=
handler
.
response_serializer
        
)
    
def
_find_name
(
self
context
)
:
        
return
self
.
_handler_call_details
.
method
