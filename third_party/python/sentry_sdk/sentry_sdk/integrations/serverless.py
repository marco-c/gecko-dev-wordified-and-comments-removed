import
functools
import
sys
from
sentry_sdk
.
hub
import
Hub
from
sentry_sdk
.
utils
import
event_from_exception
from
sentry_sdk
.
_compat
import
reraise
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
Any
    
from
typing
import
Callable
    
from
typing
import
TypeVar
    
from
typing
import
Union
    
from
typing
import
Optional
    
from
typing
import
overload
    
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
else
:
    
def
overload
(
x
)
:
        
return
x
overload
def
serverless_function
(
f
flush
=
True
)
:
    
pass
overload
def
serverless_function
(
f
=
None
flush
=
True
)
:
    
pass
def
serverless_function
(
f
=
None
flush
=
True
)
:
    
def
wrapper
(
f
)
:
        
functools
.
wraps
(
f
)
        
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
            
with
Hub
(
Hub
.
current
)
as
hub
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
                    
scope
.
clear_breadcrumbs
(
)
                
try
:
                    
return
f
(
*
args
*
*
kwargs
)
                
except
Exception
:
                    
_capture_and_reraise
(
)
                
finally
:
                    
if
flush
:
                        
_flush_client
(
)
        
return
inner
    
if
f
is
None
:
        
return
wrapper
    
else
:
        
return
wrapper
(
f
)
def
_capture_and_reraise
(
)
:
    
exc_info
=
sys
.
exc_info
(
)
    
hub
=
Hub
.
current
    
if
hub
is
not
None
and
hub
.
client
is
not
None
:
        
event
hint
=
event_from_exception
(
            
exc_info
            
client_options
=
hub
.
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
serverless
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
    
reraise
(
*
exc_info
)
def
_flush_client
(
)
:
    
hub
=
Hub
.
current
    
if
hub
is
not
None
:
        
hub
.
flush
(
)
