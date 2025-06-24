from
__future__
import
absolute_import
import
sys
from
sentry_sdk
.
_compat
import
reraise
from
sentry_sdk
.
consts
import
OP
from
sentry_sdk
.
hub
import
Hub
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
_types
import
TYPE_CHECKING
from
sentry_sdk
.
utils
import
event_from_exception
try
:
    
import
asyncio
    
from
asyncio
.
tasks
import
Task
except
ImportError
:
    
raise
DidNotEnable
(
"
asyncio
not
available
"
)
if
TYPE_CHECKING
:
    
from
typing
import
Any
    
from
collections
.
abc
import
Coroutine
    
from
sentry_sdk
.
_types
import
ExcInfo
def
get_name
(
coro
)
:
    
return
(
        
getattr
(
coro
"
__qualname__
"
None
)
        
or
getattr
(
coro
"
__name__
"
None
)
        
or
"
coroutine
without
__name__
"
    
)
def
patch_asyncio
(
)
:
    
orig_task_factory
=
None
    
try
:
        
loop
=
asyncio
.
get_running_loop
(
)
        
orig_task_factory
=
loop
.
get_task_factory
(
)
        
def
_sentry_task_factory
(
loop
coro
*
*
kwargs
)
:
            
async
def
_coro_creating_hub_and_span
(
)
:
                
hub
=
Hub
(
Hub
.
current
)
                
result
=
None
                
with
hub
:
                    
with
hub
.
start_span
(
op
=
OP
.
FUNCTION
description
=
get_name
(
coro
)
)
:
                        
try
:
                            
result
=
await
coro
                        
except
Exception
:
                            
reraise
(
*
_capture_exception
(
hub
)
)
                
return
result
            
if
orig_task_factory
:
                
return
orig_task_factory
(
loop
_coro_creating_hub_and_span
(
)
*
*
kwargs
)
            
task
=
Task
(
_coro_creating_hub_and_span
(
)
loop
=
loop
*
*
kwargs
)
            
if
task
.
_source_traceback
:
                
del
task
.
_source_traceback
[
-
1
]
            
return
task
        
loop
.
set_task_factory
(
_sentry_task_factory
)
    
except
RuntimeError
:
        
pass
def
_capture_exception
(
hub
)
:
    
exc_info
=
sys
.
exc_info
(
)
    
integration
=
hub
.
get_integration
(
AsyncioIntegration
)
    
if
integration
is
not
None
:
        
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
asyncio
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
    
return
exc_info
class
AsyncioIntegration
(
Integration
)
:
    
identifier
=
"
asyncio
"
    
staticmethod
    
def
setup_once
(
)
:
        
patch_asyncio
(
)
