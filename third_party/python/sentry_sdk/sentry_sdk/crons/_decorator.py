from
functools
import
wraps
from
inspect
import
iscoroutinefunction
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
cast
overload
ParamSpec
TypeVar
Union
    
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
    
if
TYPE_CHECKING
:
        
overload
        
def
__call__
(
self
fn
)
:
            
.
.
.
        
overload
        
def
__call__
(
self
fn
)
:
            
.
.
.
    
def
__call__
(
        
self
        
fn
    
)
:
        
if
iscoroutinefunction
(
fn
)
:
            
return
self
.
_async_wrapper
(
fn
)
        
else
:
            
if
TYPE_CHECKING
:
                
fn
=
cast
(
"
Callable
[
P
R
]
"
fn
)
            
return
self
.
_sync_wrapper
(
fn
)
    
def
_async_wrapper
(
self
fn
)
:
        
wraps
(
fn
)
        
async
def
inner
(
*
args
:
"
P
.
args
"
*
*
kwargs
:
"
P
.
kwargs
"
)
:
            
with
self
:
                
return
await
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
    
def
_sync_wrapper
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
:
"
P
.
args
"
*
*
kwargs
:
"
P
.
kwargs
"
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
