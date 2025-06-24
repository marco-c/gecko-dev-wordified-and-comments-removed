from
functools
import
wraps
from
sentry_sdk
.
_types
import
TYPE_CHECKING
if
TYPE_CHECKING
:
    
from
typing
import
Any
Callable
ParamSpec
TypeVar
    
P
=
ParamSpec
(
"
P
"
)
    
R
=
TypeVar
(
"
R
"
)
class
MonitorMixin
:
    
def
__call__
(
self
fn
)
:
        
wraps
(
fn
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
self
:
                
return
fn
(
*
args
*
*
kwargs
)
        
return
inner
