import
asyncio
import
os
import
pathlib
import
sys
from
contextlib
import
suppress
from
mimetypes
import
MimeTypes
from
stat
import
S_ISREG
from
types
import
MappingProxyType
from
typing
import
(
    
IO
    
TYPE_CHECKING
    
Any
    
Awaitable
    
Callable
    
Final
    
Iterator
    
List
    
Optional
    
Tuple
    
Union
    
cast
)
from
.
import
hdrs
from
.
abc
import
AbstractStreamWriter
from
.
helpers
import
ETAG_ANY
ETag
must_be_empty_body
from
.
typedefs
import
LooseHeaders
PathLike
from
.
web_exceptions
import
(
    
HTTPForbidden
    
HTTPNotFound
    
HTTPNotModified
    
HTTPPartialContent
    
HTTPPreconditionFailed
    
HTTPRequestRangeNotSatisfiable
)
from
.
web_response
import
StreamResponse
__all__
=
(
"
FileResponse
"
)
if
TYPE_CHECKING
:
    
from
.
web_request
import
BaseRequest
_T_OnChunkSent
=
Optional
[
Callable
[
[
bytes
]
Awaitable
[
None
]
]
]
NOSENDFILE
:
Final
[
bool
]
=
bool
(
os
.
environ
.
get
(
"
AIOHTTP_NOSENDFILE
"
)
)
CONTENT_TYPES
:
Final
[
MimeTypes
]
=
MimeTypes
(
)
if
sys
.
version_info
<
(
3
9
)
:
    
CONTENT_TYPES
.
encodings_map
[
"
.
br
"
]
=
"
br
"
ENCODING_EXTENSIONS
=
MappingProxyType
(
    
{
ext
:
CONTENT_TYPES
.
encodings_map
[
ext
]
for
ext
in
(
"
.
br
"
"
.
gz
"
)
}
)
FALLBACK_CONTENT_TYPE
=
"
application
/
octet
-
stream
"
ADDITIONAL_CONTENT_TYPES
=
MappingProxyType
(
    
{
        
"
application
/
gzip
"
:
"
.
gz
"
        
"
application
/
x
-
brotli
"
:
"
.
br
"
        
"
application
/
x
-
bzip2
"
:
"
.
bz2
"
        
"
application
/
x
-
compress
"
:
"
.
Z
"
        
"
application
/
x
-
xz
"
:
"
.
xz
"
    
}
)
CONTENT_TYPES
.
encodings_map
.
clear
(
)
for
content_type
extension
in
ADDITIONAL_CONTENT_TYPES
.
items
(
)
:
    
CONTENT_TYPES
.
add_type
(
content_type
extension
)
class
FileResponse
(
StreamResponse
)
:
    
"
"
"
A
response
object
can
be
used
to
send
files
.
"
"
"
    
def
__init__
(
        
self
        
path
:
PathLike
        
chunk_size
:
int
=
256
*
1024
        
status
:
int
=
200
        
reason
:
Optional
[
str
]
=
None
        
headers
:
Optional
[
LooseHeaders
]
=
None
    
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
status
=
status
reason
=
reason
headers
=
headers
)
        
self
.
_path
=
pathlib
.
Path
(
path
)
        
self
.
_chunk_size
=
chunk_size
    
async
def
_sendfile_fallback
(
        
self
writer
:
AbstractStreamWriter
fobj
:
IO
[
Any
]
offset
:
int
count
:
int
    
)
-
>
AbstractStreamWriter
:
        
chunk_size
=
self
.
_chunk_size
        
loop
=
asyncio
.
get_event_loop
(
)
        
await
loop
.
run_in_executor
(
None
fobj
.
seek
offset
)
        
chunk
=
await
loop
.
run_in_executor
(
None
fobj
.
read
chunk_size
)
        
while
chunk
:
            
await
writer
.
write
(
chunk
)
            
count
=
count
-
chunk_size
            
if
count
<
=
0
:
                
break
            
chunk
=
await
loop
.
run_in_executor
(
None
fobj
.
read
min
(
chunk_size
count
)
)
        
await
writer
.
drain
(
)
        
return
writer
    
async
def
_sendfile
(
        
self
request
:
"
BaseRequest
"
fobj
:
IO
[
Any
]
offset
:
int
count
:
int
    
)
-
>
AbstractStreamWriter
:
        
writer
=
await
super
(
)
.
prepare
(
request
)
        
assert
writer
is
not
None
        
if
NOSENDFILE
or
self
.
compression
:
            
return
await
self
.
_sendfile_fallback
(
writer
fobj
offset
count
)
        
loop
=
request
.
_loop
        
transport
=
request
.
transport
        
assert
transport
is
not
None
        
try
:
            
await
loop
.
sendfile
(
transport
fobj
offset
count
)
        
except
NotImplementedError
:
            
return
await
self
.
_sendfile_fallback
(
writer
fobj
offset
count
)
        
await
super
(
)
.
write_eof
(
)
        
return
writer
    
staticmethod
    
def
_etag_match
(
etag_value
:
str
etags
:
Tuple
[
ETag
.
.
.
]
*
weak
:
bool
)
-
>
bool
:
        
if
len
(
etags
)
=
=
1
and
etags
[
0
]
.
value
=
=
ETAG_ANY
:
            
return
True
        
return
any
(
            
etag
.
value
=
=
etag_value
for
etag
in
etags
if
weak
or
not
etag
.
is_weak
        
)
    
async
def
_not_modified
(
        
self
request
:
"
BaseRequest
"
etag_value
:
str
last_modified
:
float
    
)
-
>
Optional
[
AbstractStreamWriter
]
:
        
self
.
set_status
(
HTTPNotModified
.
status_code
)
        
self
.
_length_check
=
False
        
self
.
etag
=
etag_value
        
self
.
last_modified
=
last_modified
        
return
await
super
(
)
.
prepare
(
request
)
    
async
def
_precondition_failed
(
        
self
request
:
"
BaseRequest
"
    
)
-
>
Optional
[
AbstractStreamWriter
]
:
        
self
.
set_status
(
HTTPPreconditionFailed
.
status_code
)
        
self
.
content_length
=
0
        
return
await
super
(
)
.
prepare
(
request
)
    
def
_get_file_path_stat_encoding
(
        
self
accept_encoding
:
str
    
)
-
>
Tuple
[
pathlib
.
Path
os
.
stat_result
Optional
[
str
]
]
:
        
"
"
"
Return
the
file
path
stat
result
and
encoding
.
        
If
an
uncompressed
file
is
returned
the
encoding
is
set
to
        
:
py
:
data
:
None
.
        
This
method
should
be
called
from
a
thread
executor
        
since
it
calls
os
.
stat
which
may
block
.
        
"
"
"
        
file_path
=
self
.
_path
        
for
file_extension
file_encoding
in
ENCODING_EXTENSIONS
.
items
(
)
:
            
if
file_encoding
not
in
accept_encoding
:
                
continue
            
compressed_path
=
file_path
.
with_suffix
(
file_path
.
suffix
+
file_extension
)
            
with
suppress
(
OSError
)
:
                
st
=
compressed_path
.
lstat
(
)
                
if
S_ISREG
(
st
.
st_mode
)
:
                    
return
compressed_path
st
file_encoding
        
return
file_path
file_path
.
stat
(
)
None
    
async
def
prepare
(
self
request
:
"
BaseRequest
"
)
-
>
Optional
[
AbstractStreamWriter
]
:
        
loop
=
asyncio
.
get_running_loop
(
)
        
accept_encoding
=
request
.
headers
.
get
(
hdrs
.
ACCEPT_ENCODING
"
"
)
.
lower
(
)
        
try
:
            
file_path
st
file_encoding
=
await
loop
.
run_in_executor
(
                
None
self
.
_get_file_path_stat_encoding
accept_encoding
            
)
        
except
OSError
:
            
self
.
set_status
(
HTTPNotFound
.
status_code
)
            
return
await
super
(
)
.
prepare
(
request
)
        
if
not
S_ISREG
(
st
.
st_mode
)
:
            
self
.
set_status
(
HTTPForbidden
.
status_code
)
            
return
await
super
(
)
.
prepare
(
request
)
        
etag_value
=
f
"
{
st
.
st_mtime_ns
:
x
}
-
{
st
.
st_size
:
x
}
"
        
last_modified
=
st
.
st_mtime
        
ifmatch
=
request
.
if_match
        
if
ifmatch
is
not
None
and
not
self
.
_etag_match
(
            
etag_value
ifmatch
weak
=
False
        
)
:
            
return
await
self
.
_precondition_failed
(
request
)
        
unmodsince
=
request
.
if_unmodified_since
        
if
(
            
unmodsince
is
not
None
            
and
ifmatch
is
None
            
and
st
.
st_mtime
>
unmodsince
.
timestamp
(
)
        
)
:
            
return
await
self
.
_precondition_failed
(
request
)
        
ifnonematch
=
request
.
if_none_match
        
if
ifnonematch
is
not
None
and
self
.
_etag_match
(
            
etag_value
ifnonematch
weak
=
True
        
)
:
            
return
await
self
.
_not_modified
(
request
etag_value
last_modified
)
        
modsince
=
request
.
if_modified_since
        
if
(
            
modsince
is
not
None
            
and
ifnonematch
is
None
            
and
st
.
st_mtime
<
=
modsince
.
timestamp
(
)
        
)
:
            
return
await
self
.
_not_modified
(
request
etag_value
last_modified
)
        
status
=
self
.
_status
        
file_size
=
st
.
st_size
        
count
=
file_size
        
start
=
None
        
ifrange
=
request
.
if_range
        
if
ifrange
is
None
or
st
.
st_mtime
<
=
ifrange
.
timestamp
(
)
:
            
try
:
                
rng
=
request
.
http_range
                
start
=
rng
.
start
                
end
=
rng
.
stop
            
except
ValueError
:
                
self
.
headers
[
hdrs
.
CONTENT_RANGE
]
=
f
"
bytes
*
/
{
file_size
}
"
                
self
.
set_status
(
HTTPRequestRangeNotSatisfiable
.
status_code
)
                
return
await
super
(
)
.
prepare
(
request
)
            
if
start
is
not
None
or
end
is
not
None
:
                
if
start
<
0
and
end
is
None
:
                    
start
+
=
file_size
                    
if
start
<
0
:
                        
start
=
0
                    
count
=
file_size
-
start
                
else
:
                    
count
=
(
                        
min
(
end
if
end
is
not
None
else
file_size
file_size
)
-
start
                    
)
                
if
start
>
=
file_size
:
                    
self
.
headers
[
hdrs
.
CONTENT_RANGE
]
=
f
"
bytes
*
/
{
file_size
}
"
                    
self
.
set_status
(
HTTPRequestRangeNotSatisfiable
.
status_code
)
                    
return
await
super
(
)
.
prepare
(
request
)
                
status
=
HTTPPartialContent
.
status_code
                
self
.
set_status
(
status
)
        
if
hdrs
.
CONTENT_TYPE
not
in
self
.
headers
:
            
self
.
content_type
=
(
                
CONTENT_TYPES
.
guess_type
(
self
.
_path
)
[
0
]
or
FALLBACK_CONTENT_TYPE
            
)
        
if
file_encoding
:
            
self
.
headers
[
hdrs
.
CONTENT_ENCODING
]
=
file_encoding
            
self
.
headers
[
hdrs
.
VARY
]
=
hdrs
.
ACCEPT_ENCODING
            
self
.
_compression
=
False
        
self
.
etag
=
etag_value
        
self
.
last_modified
=
st
.
st_mtime
        
self
.
content_length
=
count
        
self
.
headers
[
hdrs
.
ACCEPT_RANGES
]
=
"
bytes
"
        
real_start
=
cast
(
int
start
)
        
if
status
=
=
HTTPPartialContent
.
status_code
:
            
self
.
headers
[
hdrs
.
CONTENT_RANGE
]
=
"
bytes
{
}
-
{
}
/
{
}
"
.
format
(
                
real_start
real_start
+
count
-
1
file_size
            
)
        
if
count
=
=
0
or
must_be_empty_body
(
request
.
method
self
.
status
)
:
            
return
await
super
(
)
.
prepare
(
request
)
        
try
:
            
fobj
=
await
loop
.
run_in_executor
(
None
file_path
.
open
"
rb
"
)
        
except
PermissionError
:
            
self
.
set_status
(
HTTPForbidden
.
status_code
)
            
return
await
super
(
)
.
prepare
(
request
)
        
if
start
:
            
offset
=
start
        
else
:
            
offset
=
0
        
try
:
            
return
await
self
.
_sendfile
(
request
fobj
offset
count
)
        
finally
:
            
await
asyncio
.
shield
(
loop
.
run_in_executor
(
None
fobj
.
close
)
)
