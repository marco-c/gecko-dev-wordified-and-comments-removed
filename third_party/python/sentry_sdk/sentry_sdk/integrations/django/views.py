import
threading
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
_types
import
MYPY
from
sentry_sdk
import
_functools
if
MYPY
:
    
from
typing
import
Any
try
:
    
from
asyncio
import
iscoroutinefunction
except
ImportError
:
    
iscoroutinefunction
=
None
try
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
wrap_async_view
except
(
ImportError
SyntaxError
)
:
    
wrap_async_view
=
None
def
patch_views
(
)
:
    
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
    
from
django
.
template
.
response
import
SimpleTemplateResponse
    
from
sentry_sdk
.
integrations
.
django
import
DjangoIntegration
    
old_make_view_atomic
=
BaseHandler
.
make_view_atomic
    
old_render
=
SimpleTemplateResponse
.
render
    
def
sentry_patched_render
(
self
)
:
        
hub
=
Hub
.
current
        
with
hub
.
start_span
(
            
op
=
OP
.
VIEW_RESPONSE_RENDER
description
=
"
serialize
response
"
        
)
:
            
return
old_render
(
self
)
    
_functools
.
wraps
(
old_make_view_atomic
)
    
def
sentry_patched_make_view_atomic
(
self
*
args
*
*
kwargs
)
:
        
callback
=
old_make_view_atomic
(
self
*
args
*
*
kwargs
)
        
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
and
integration
.
middleware_spans
:
            
if
(
                
iscoroutinefunction
is
not
None
                
and
wrap_async_view
is
not
None
                
and
iscoroutinefunction
(
callback
)
            
)
:
                
sentry_wrapped_callback
=
wrap_async_view
(
hub
callback
)
            
else
:
                
sentry_wrapped_callback
=
_wrap_sync_view
(
hub
callback
)
        
else
:
            
sentry_wrapped_callback
=
callback
        
return
sentry_wrapped_callback
    
SimpleTemplateResponse
.
render
=
sentry_patched_render
    
BaseHandler
.
make_view_atomic
=
sentry_patched_make_view_atomic
def
_wrap_sync_view
(
hub
callback
)
:
    
_functools
.
wraps
(
callback
)
    
def
sentry_wrapped_callback
(
request
*
args
*
*
kwargs
)
:
        
with
hub
.
configure_scope
(
)
as
sentry_scope
:
            
if
sentry_scope
.
profile
is
not
None
:
                
sentry_scope
.
profile
.
active_thread_id
=
threading
.
current_thread
(
)
.
ident
            
with
hub
.
start_span
(
                
op
=
OP
.
VIEW_RENDER
description
=
request
.
resolver_match
.
view_name
            
)
:
                
return
callback
(
request
*
args
*
*
kwargs
)
    
return
sentry_wrapped_callback
