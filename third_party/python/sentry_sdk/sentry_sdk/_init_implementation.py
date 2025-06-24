import
warnings
from
typing
import
TYPE_CHECKING
import
sentry_sdk
if
TYPE_CHECKING
:
    
from
typing
import
Any
ContextManager
Optional
    
import
sentry_sdk
.
consts
class
_InitGuard
:
    
_CONTEXT_MANAGER_DEPRECATION_WARNING_MESSAGE
=
(
        
"
Using
the
return
value
of
sentry_sdk
.
init
as
a
context
manager
"
        
"
and
manually
calling
the
__enter__
and
__exit__
methods
on
the
"
        
"
return
value
are
deprecated
.
We
are
no
longer
maintaining
this
"
        
"
functionality
and
we
will
remove
it
in
the
next
major
release
.
"
    
)
    
def
__init__
(
self
client
)
:
        
self
.
_client
=
client
    
def
__enter__
(
self
)
:
        
warnings
.
warn
(
            
self
.
_CONTEXT_MANAGER_DEPRECATION_WARNING_MESSAGE
            
stacklevel
=
2
            
category
=
DeprecationWarning
        
)
        
return
self
    
def
__exit__
(
self
exc_type
exc_value
tb
)
:
        
warnings
.
warn
(
            
self
.
_CONTEXT_MANAGER_DEPRECATION_WARNING_MESSAGE
            
stacklevel
=
2
            
category
=
DeprecationWarning
        
)
        
c
=
self
.
_client
        
if
c
is
not
None
:
            
c
.
close
(
)
def
_check_python_deprecations
(
)
:
    
pass
def
_init
(
*
args
*
*
kwargs
)
:
    
"
"
"
Initializes
the
SDK
and
optionally
integrations
.
    
This
takes
the
same
arguments
as
the
client
constructor
.
    
"
"
"
    
client
=
sentry_sdk
.
Client
(
*
args
*
*
kwargs
)
    
sentry_sdk
.
get_global_scope
(
)
.
set_client
(
client
)
    
_check_python_deprecations
(
)
    
rv
=
_InitGuard
(
client
)
    
return
rv
if
TYPE_CHECKING
:
    
class
init
(
sentry_sdk
.
consts
.
ClientConstructor
_InitGuard
)
:
        
pass
else
:
    
init
=
(
lambda
:
_init
)
(
)
