import
types
import
functools
from
pip9
.
_vendor
.
requests
.
adapters
import
HTTPAdapter
from
.
controller
import
CacheController
from
.
cache
import
DictCache
from
.
filewrapper
import
CallbackFileWrapper
class
CacheControlAdapter
(
HTTPAdapter
)
:
    
invalidating_methods
=
set
(
[
'
PUT
'
'
DELETE
'
]
)
    
def
__init__
(
self
cache
=
None
                 
cache_etags
=
True
                 
controller_class
=
None
                 
serializer
=
None
                 
heuristic
=
None
                 
*
args
*
*
kw
)
:
        
super
(
CacheControlAdapter
self
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
cache
or
DictCache
(
)
        
self
.
heuristic
=
heuristic
        
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
*
*
kw
)
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
        
if
request
.
method
=
=
'
GET
'
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
CacheControlAdapter
self
)
.
send
(
request
*
*
kw
)
        
return
resp
    
def
build_response
(
self
request
response
from_cache
=
False
)
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
        
if
not
from_cache
and
request
.
method
=
=
'
GET
'
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
response
.
status
=
=
301
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
)
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
=
super
(
CacheControlAdapter
self
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
CacheControlAdapter
self
)
.
close
(
)
