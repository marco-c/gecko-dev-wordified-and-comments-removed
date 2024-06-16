from
__future__
import
annotations
import
functools
import
types
import
zlib
from
typing
import
TYPE_CHECKING
Any
Collection
Mapping
from
pip
.
_vendor
.
requests
.
adapters
import
HTTPAdapter
from
pip
.
_vendor
.
cachecontrol
.
cache
import
DictCache
from
pip
.
_vendor
.
cachecontrol
.
controller
import
PERMANENT_REDIRECT_STATUSES
CacheController
from
pip
.
_vendor
.
cachecontrol
.
filewrapper
import
CallbackFileWrapper
if
TYPE_CHECKING
:
    
from
pip
.
_vendor
.
requests
import
PreparedRequest
Response
    
from
pip
.
_vendor
.
urllib3
import
HTTPResponse
    
from
pip
.
_vendor
.
cachecontrol
.
cache
import
BaseCache
    
from
pip
.
_vendor
.
cachecontrol
.
heuristics
import
BaseHeuristic
    
from
pip
.
_vendor
.
cachecontrol
.
serialize
import
Serializer
class
CacheControlAdapter
(
HTTPAdapter
)
:
    
invalidating_methods
=
{
"
PUT
"
"
PATCH
"
"
DELETE
"
}
    
def
__init__
(
        
self
        
cache
:
BaseCache
|
None
=
None
        
cache_etags
:
bool
=
True
        
controller_class
:
type
[
CacheController
]
|
None
=
None
        
serializer
:
Serializer
|
None
=
None
        
heuristic
:
BaseHeuristic
|
None
=
None
        
cacheable_methods
:
Collection
[
str
]
|
None
=
None
        
*
args
:
Any
        
*
*
kw
:
Any
    
)
-
>
None
:
        
super
(
)
.
__init__
(
*
args
*
*
kw
)
        
self
.
cache
=
DictCache
(
)
if
cache
is
None
else
cache
        
self
.
heuristic
=
heuristic
        
self
.
cacheable_methods
=
cacheable_methods
or
(
"
GET
"
)
        
controller_factory
=
controller_class
or
CacheController
        
self
.
controller
=
controller_factory
(
            
self
.
cache
cache_etags
=
cache_etags
serializer
=
serializer
        
)
    
def
send
(
        
self
        
request
:
PreparedRequest
        
stream
:
bool
=
False
        
timeout
:
None
|
float
|
tuple
[
float
float
]
|
tuple
[
float
None
]
=
None
        
verify
:
bool
|
str
=
True
        
cert
:
(
None
|
bytes
|
str
|
tuple
[
bytes
|
str
bytes
|
str
]
)
=
None
        
proxies
:
Mapping
[
str
str
]
|
None
=
None
        
cacheable_methods
:
Collection
[
str
]
|
None
=
None
    
)
-
>
Response
:
        
"
"
"
        
Send
a
request
.
Use
the
request
information
to
see
if
it
        
exists
in
the
cache
and
cache
the
response
if
we
need
to
and
can
.
        
"
"
"
        
cacheable
=
cacheable_methods
or
self
.
cacheable_methods
        
if
request
.
method
in
cacheable
:
            
try
:
                
cached_response
=
self
.
controller
.
cached_request
(
request
)
            
except
zlib
.
error
:
                
cached_response
=
None
            
if
cached_response
:
                
return
self
.
build_response
(
request
cached_response
from_cache
=
True
)
            
request
.
headers
.
update
(
self
.
controller
.
conditional_headers
(
request
)
)
        
resp
=
super
(
)
.
send
(
request
stream
timeout
verify
cert
proxies
)
        
return
resp
    
def
build_response
(
        
self
        
request
:
PreparedRequest
        
response
:
HTTPResponse
        
from_cache
:
bool
=
False
        
cacheable_methods
:
Collection
[
str
]
|
None
=
None
    
)
-
>
Response
:
        
"
"
"
        
Build
a
response
by
making
a
request
or
using
the
cache
.
        
This
will
end
up
calling
send
and
returning
a
potentially
        
cached
response
        
"
"
"
        
cacheable
=
cacheable_methods
or
self
.
cacheable_methods
        
if
not
from_cache
and
request
.
method
in
cacheable
:
            
if
self
.
heuristic
:
                
response
=
self
.
heuristic
.
apply
(
response
)
            
if
response
.
status
=
=
304
:
                
cached_response
=
self
.
controller
.
update_cached_response
(
                    
request
response
                
)
                
if
cached_response
is
not
response
:
                    
from_cache
=
True
                
response
.
read
(
decode_content
=
False
)
                
response
.
release_conn
(
)
                
response
=
cached_response
            
elif
int
(
response
.
status
)
in
PERMANENT_REDIRECT_STATUSES
:
                
self
.
controller
.
cache_response
(
request
response
)
            
else
:
                
response
.
_fp
=
CallbackFileWrapper
(
                    
response
.
_fp
                    
functools
.
partial
(
                        
self
.
controller
.
cache_response
request
response
                    
)
                
)
                
if
response
.
chunked
:
                    
super_update_chunk_length
=
response
.
_update_chunk_length
                    
def
_update_chunk_length
(
self
:
HTTPResponse
)
-
>
None
:
                        
super_update_chunk_length
(
)
                        
if
self
.
chunk_left
=
=
0
:
                            
self
.
_fp
.
_close
(
)
                    
response
.
_update_chunk_length
=
types
.
MethodType
(
                        
_update_chunk_length
response
                    
)
        
resp
:
Response
=
super
(
)
.
build_response
(
request
response
)
        
if
request
.
method
in
self
.
invalidating_methods
and
resp
.
ok
:
            
assert
request
.
url
is
not
None
            
cache_url
=
self
.
controller
.
cache_url
(
request
.
url
)
            
self
.
cache
.
delete
(
cache_url
)
        
resp
.
from_cache
=
from_cache
        
return
resp
    
def
close
(
self
)
-
>
None
:
        
self
.
cache
.
close
(
)
        
super
(
)
.
close
(
)
