import
copy
import
sentry_sdk
from
sentry_sdk
.
_lru_cache
import
LRUCache
from
threading
import
Lock
from
typing
import
TYPE_CHECKING
Any
if
TYPE_CHECKING
:
    
from
typing
import
TypedDict
    
FlagData
=
TypedDict
(
"
FlagData
"
{
"
flag
"
:
str
"
result
"
:
bool
}
)
DEFAULT_FLAG_CAPACITY
=
100
class
FlagBuffer
:
    
def
__init__
(
self
capacity
)
:
        
self
.
capacity
=
capacity
        
self
.
lock
=
Lock
(
)
        
self
.
__buffer
=
LRUCache
(
capacity
)
    
def
clear
(
self
)
:
        
self
.
__buffer
=
LRUCache
(
self
.
capacity
)
    
def
__deepcopy__
(
self
memo
)
:
        
with
self
.
lock
:
            
buffer
=
FlagBuffer
(
self
.
capacity
)
            
buffer
.
__buffer
=
copy
.
deepcopy
(
self
.
__buffer
memo
)
            
return
buffer
    
def
get
(
self
)
:
        
with
self
.
lock
:
            
return
[
                
{
"
flag
"
:
key
"
result
"
:
value
}
for
key
value
in
self
.
__buffer
.
get_all
(
)
            
]
    
def
set
(
self
flag
result
)
:
        
if
isinstance
(
result
FlagBuffer
)
:
            
raise
ValueError
(
                
"
FlagBuffer
instances
can
not
be
inserted
into
the
dictionary
.
"
            
)
        
with
self
.
lock
:
            
self
.
__buffer
.
set
(
flag
result
)
def
add_feature_flag
(
flag
result
)
:
    
"
"
"
    
Records
a
flag
and
its
value
to
be
sent
on
subsequent
error
events
.
    
We
recommend
you
do
this
on
flag
evaluations
.
Flags
are
buffered
per
Sentry
scope
.
    
"
"
"
    
flags
=
sentry_sdk
.
get_isolation_scope
(
)
.
flags
    
flags
.
set
(
flag
result
)
    
span
=
sentry_sdk
.
get_current_span
(
)
    
if
span
:
        
span
.
set_flag
(
f
"
flag
.
evaluation
.
{
flag
}
"
result
)
