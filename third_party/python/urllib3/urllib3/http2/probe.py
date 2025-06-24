from
__future__
import
annotations
import
threading
class
_HTTP2ProbeCache
:
    
__slots__
=
(
        
"
_lock
"
        
"
_cache_locks
"
        
"
_cache_values
"
    
)
    
def
__init__
(
self
)
-
>
None
:
        
self
.
_lock
=
threading
.
Lock
(
)
        
self
.
_cache_locks
:
dict
[
tuple
[
str
int
]
threading
.
RLock
]
=
{
}
        
self
.
_cache_values
:
dict
[
tuple
[
str
int
]
bool
|
None
]
=
{
}
    
def
acquire_and_get
(
self
host
:
str
port
:
int
)
-
>
bool
|
None
:
        
value
=
None
        
with
self
.
_lock
:
            
key
=
(
host
port
)
            
try
:
                
value
=
self
.
_cache_values
[
key
]
                
if
value
is
not
None
:
                    
return
value
            
except
KeyError
:
                
self
.
_cache_locks
[
key
]
=
threading
.
RLock
(
)
                
self
.
_cache_values
[
key
]
=
None
        
key_lock
=
self
.
_cache_locks
[
key
]
        
key_lock
.
acquire
(
)
        
try
:
            
value
=
self
.
_cache_values
[
key
]
        
except
BaseException
as
e
:
            
assert
not
isinstance
(
e
KeyError
)
            
key_lock
.
release
(
)
            
raise
        
return
value
    
def
set_and_release
(
        
self
host
:
str
port
:
int
supports_http2
:
bool
|
None
    
)
-
>
None
:
        
key
=
(
host
port
)
        
key_lock
=
self
.
_cache_locks
[
key
]
        
with
key_lock
:
            
if
supports_http2
is
None
and
self
.
_cache_values
[
key
]
is
not
None
:
                
raise
ValueError
(
                    
"
Cannot
reset
HTTP
/
2
support
for
origin
after
value
has
been
set
.
"
                
)
        
self
.
_cache_values
[
key
]
=
supports_http2
        
key_lock
.
release
(
)
    
def
_values
(
self
)
-
>
dict
[
tuple
[
str
int
]
bool
|
None
]
:
        
"
"
"
This
function
is
for
testing
purposes
only
.
Gets
the
current
state
of
the
probe
cache
"
"
"
        
with
self
.
_lock
:
            
return
{
k
:
v
for
k
v
in
self
.
_cache_values
.
items
(
)
}
    
def
_reset
(
self
)
-
>
None
:
        
"
"
"
This
function
is
for
testing
purposes
only
.
Reset
the
cache
values
"
"
"
        
with
self
.
_lock
:
            
self
.
_cache_locks
=
{
}
            
self
.
_cache_values
=
{
}
_HTTP2_PROBE_CACHE
=
_HTTP2ProbeCache
(
)
set_and_release
=
_HTTP2_PROBE_CACHE
.
set_and_release
acquire_and_get
=
_HTTP2_PROBE_CACHE
.
acquire_and_get
_values
=
_HTTP2_PROBE_CACHE
.
_values
_reset
=
_HTTP2_PROBE_CACHE
.
_reset
__all__
=
[
    
"
set_and_release
"
    
"
acquire_and_get
"
]
