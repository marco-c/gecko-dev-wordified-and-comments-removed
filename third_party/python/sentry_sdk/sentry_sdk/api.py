import
inspect
from
contextlib
import
contextmanager
from
sentry_sdk
.
hub
import
Hub
from
sentry_sdk
.
scope
import
Scope
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
Dict
    
from
typing
import
Optional
    
from
typing
import
overload
    
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
ContextManager
    
from
sentry_sdk
.
_types
import
Event
Hint
Breadcrumb
BreadcrumbHint
    
from
sentry_sdk
.
tracing
import
Span
    
T
=
TypeVar
(
"
T
"
)
    
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
__all__
=
[
    
"
capture_event
"
    
"
capture_message
"
    
"
capture_exception
"
    
"
add_breadcrumb
"
    
"
configure_scope
"
    
"
push_scope
"
    
"
flush
"
    
"
last_event_id
"
    
"
start_span
"
    
"
set_tag
"
    
"
set_context
"
    
"
set_extra
"
    
"
set_user
"
    
"
set_level
"
]
def
hubmethod
(
f
)
:
    
f
.
__doc__
=
"
%
s
\
n
\
n
%
s
"
%
(
        
"
Alias
for
:
py
:
meth
:
sentry_sdk
.
Hub
.
%
s
"
%
f
.
__name__
        
inspect
.
getdoc
(
getattr
(
Hub
f
.
__name__
)
)
    
)
    
return
f
def
scopemethod
(
f
)
:
    
f
.
__doc__
=
"
%
s
\
n
\
n
%
s
"
%
(
        
"
Alias
for
:
py
:
meth
:
sentry_sdk
.
Scope
.
%
s
"
%
f
.
__name__
        
inspect
.
getdoc
(
getattr
(
Scope
f
.
__name__
)
)
    
)
    
return
f
hubmethod
def
capture_event
(
    
event
    
hint
=
None
    
scope
=
None
    
*
*
scope_args
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
        
return
hub
.
capture_event
(
event
hint
scope
=
scope
*
*
scope_args
)
    
return
None
hubmethod
def
capture_message
(
    
message
    
level
=
None
    
scope
=
None
    
*
*
scope_args
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
        
return
hub
.
capture_message
(
message
level
scope
=
scope
*
*
scope_args
)
    
return
None
hubmethod
def
capture_exception
(
    
error
=
None
    
scope
=
None
    
*
*
scope_args
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
        
return
hub
.
capture_exception
(
error
scope
=
scope
*
*
scope_args
)
    
return
None
hubmethod
def
add_breadcrumb
(
    
crumb
=
None
    
hint
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
    
if
hub
is
not
None
:
        
return
hub
.
add_breadcrumb
(
crumb
hint
*
*
kwargs
)
overload
def
configure_scope
(
)
:
    
pass
overload
def
configure_scope
(
    
callback
)
:
    
pass
hubmethod
def
configure_scope
(
    
callback
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
is
not
None
:
        
return
hub
.
configure_scope
(
callback
)
    
elif
callback
is
None
:
        
contextmanager
        
def
inner
(
)
:
            
yield
Scope
(
)
        
return
inner
(
)
    
else
:
        
return
None
overload
def
push_scope
(
)
:
    
pass
overload
def
push_scope
(
    
callback
)
:
    
pass
hubmethod
def
push_scope
(
    
callback
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
is
not
None
:
        
return
hub
.
push_scope
(
callback
)
    
elif
callback
is
None
:
        
contextmanager
        
def
inner
(
)
:
            
yield
Scope
(
)
        
return
inner
(
)
    
else
:
        
return
None
scopemethod
def
set_tag
(
key
value
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
scope
.
set_tag
(
key
value
)
scopemethod
def
set_context
(
key
value
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
scope
.
set_context
(
key
value
)
scopemethod
def
set_extra
(
key
value
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
scope
.
set_extra
(
key
value
)
scopemethod
def
set_user
(
value
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
scope
.
set_user
(
value
)
scopemethod
def
set_level
(
value
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
scope
.
set_level
(
value
)
hubmethod
def
flush
(
    
timeout
=
None
    
callback
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
is
not
None
:
        
return
hub
.
flush
(
timeout
=
timeout
callback
=
callback
)
hubmethod
def
last_event_id
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
        
return
hub
.
last_event_id
(
)
    
return
None
hubmethod
def
start_span
(
    
span
=
None
    
*
*
kwargs
)
:
    
return
Hub
.
current
.
start_span
(
span
=
span
*
*
kwargs
)
