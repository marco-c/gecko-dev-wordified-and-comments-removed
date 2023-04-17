import
asyncio
import
mimetypes
import
os
import
pathlib
import
sys
from
typing
import
(
    
IO
    
TYPE_CHECKING
    
Any
    
Awaitable
    
Callable
    
List
    
Optional
    
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
typedefs
import
LooseHeaders
from
.
web_exceptions
import
(
    
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
Union
[
str
pathlib
.
Path
]
        
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
        
if
isinstance
(
path
str
)
:
            
path
=
pathlib
.
Path
(
path
)
        
self
.
_path
=
path
        
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
sys
.
version_info
<
(
3
7
)
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
        
filepath
=
self
.
_path
        
gzip
=
False
        
if
"
gzip
"
in
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
:
            
gzip_path
=
filepath
.
with_name
(
filepath
.
name
+
"
.
gz
"
)
            
if
gzip_path
.
is_file
(
)
:
                
filepath
=
gzip_path
                
gzip
=
True
        
loop
=
asyncio
.
get_event_loop
(
)
        
st
=
await
loop
.
run_in_executor
(
None
filepath
.
stat
)
        
modsince
=
request
.
if_modified_since
        
if
modsince
is
not
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
        
unmodsince
=
request
.
if_unmodified_since
        
if
unmodsince
is
not
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
:
            
self
.
set_status
(
HTTPPreconditionFailed
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
hdrs
.
CONTENT_TYPE
not
in
self
.
headers
:
            
ct
encoding
=
mimetypes
.
guess_type
(
str
(
filepath
)
)
            
if
not
ct
:
                
ct
=
"
application
/
octet
-
stream
"
            
should_set_ct
=
True
        
else
:
            
encoding
=
"
gzip
"
if
gzip
else
None
            
should_set_ct
=
False
        
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
should_set_ct
:
            
self
.
content_type
=
ct
        
if
encoding
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
encoding
        
if
gzip
:
            
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
request
.
method
=
=
hdrs
.
METH_HEAD
or
self
.
status
in
[
204
304
]
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
        
fobj
=
await
loop
.
run_in_executor
(
None
filepath
.
open
"
rb
"
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
loop
.
run_in_executor
(
None
fobj
.
close
)
