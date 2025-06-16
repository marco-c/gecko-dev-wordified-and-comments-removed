from
__future__
import
annotations
import
io
from
typing
import
IO
TYPE_CHECKING
Any
Mapping
cast
from
pip
.
_vendor
import
msgpack
from
pip
.
_vendor
.
requests
.
structures
import
CaseInsensitiveDict
from
pip
.
_vendor
.
urllib3
import
HTTPResponse
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
class
Serializer
:
    
serde_version
=
"
4
"
    
def
dumps
(
        
self
        
request
:
PreparedRequest
        
response
:
HTTPResponse
        
body
:
bytes
|
None
=
None
    
)
-
>
bytes
:
        
response_headers
:
CaseInsensitiveDict
[
str
]
=
CaseInsensitiveDict
(
            
response
.
headers
        
)
        
if
body
is
None
:
            
body
=
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
_fp
=
io
.
BytesIO
(
body
)
            
response
.
length_remaining
=
len
(
body
)
        
data
=
{
            
"
response
"
:
{
                
"
body
"
:
body
                
"
headers
"
:
{
str
(
k
)
:
str
(
v
)
for
k
v
in
response
.
headers
.
items
(
)
}
                
"
status
"
:
response
.
status
                
"
version
"
:
response
.
version
                
"
reason
"
:
str
(
response
.
reason
)
                
"
decode_content
"
:
response
.
decode_content
            
}
        
}
        
data
[
"
vary
"
]
=
{
}
        
if
"
vary
"
in
response_headers
:
            
varied_headers
=
response_headers
[
"
vary
"
]
.
split
(
"
"
)
            
for
header
in
varied_headers
:
                
header
=
str
(
header
)
.
strip
(
)
                
header_value
=
request
.
headers
.
get
(
header
None
)
                
if
header_value
is
not
None
:
                    
header_value
=
str
(
header_value
)
                
data
[
"
vary
"
]
[
header
]
=
header_value
        
return
b
"
"
.
join
(
[
f
"
cc
=
{
self
.
serde_version
}
"
.
encode
(
)
self
.
serialize
(
data
)
]
)
    
def
serialize
(
self
data
:
dict
[
str
Any
]
)
-
>
bytes
:
        
return
cast
(
bytes
msgpack
.
dumps
(
data
use_bin_type
=
True
)
)
    
def
loads
(
        
self
        
request
:
PreparedRequest
        
data
:
bytes
        
body_file
:
IO
[
bytes
]
|
None
=
None
    
)
-
>
HTTPResponse
|
None
:
        
if
not
data
:
            
return
None
        
if
not
data
.
startswith
(
f
"
cc
=
{
self
.
serde_version
}
"
.
encode
(
)
)
:
            
return
None
        
data
=
data
[
5
:
]
        
return
self
.
_loads_v4
(
request
data
body_file
)
    
def
prepare_response
(
        
self
        
request
:
PreparedRequest
        
cached
:
Mapping
[
str
Any
]
        
body_file
:
IO
[
bytes
]
|
None
=
None
    
)
-
>
HTTPResponse
|
None
:
        
"
"
"
Verify
our
vary
headers
match
and
construct
a
real
urllib3
        
HTTPResponse
object
.
        
"
"
"
        
if
"
*
"
in
cached
.
get
(
"
vary
"
{
}
)
:
            
return
None
        
for
header
value
in
cached
.
get
(
"
vary
"
{
}
)
.
items
(
)
:
            
if
request
.
headers
.
get
(
header
None
)
!
=
value
:
                
return
None
        
body_raw
=
cached
[
"
response
"
]
.
pop
(
"
body
"
)
        
headers
:
CaseInsensitiveDict
[
str
]
=
CaseInsensitiveDict
(
            
data
=
cached
[
"
response
"
]
[
"
headers
"
]
        
)
        
if
headers
.
get
(
"
transfer
-
encoding
"
"
"
)
=
=
"
chunked
"
:
            
headers
.
pop
(
"
transfer
-
encoding
"
)
        
cached
[
"
response
"
]
[
"
headers
"
]
=
headers
        
try
:
            
body
:
IO
[
bytes
]
            
if
body_file
is
None
:
                
body
=
io
.
BytesIO
(
body_raw
)
            
else
:
                
body
=
body_file
        
except
TypeError
:
            
body
=
io
.
BytesIO
(
body_raw
.
encode
(
"
utf8
"
)
)
        
cached
[
"
response
"
]
.
pop
(
"
strict
"
None
)
        
return
HTTPResponse
(
body
=
body
preload_content
=
False
*
*
cached
[
"
response
"
]
)
    
def
_loads_v4
(
        
self
        
request
:
PreparedRequest
        
data
:
bytes
        
body_file
:
IO
[
bytes
]
|
None
=
None
    
)
-
>
HTTPResponse
|
None
:
        
try
:
            
cached
=
msgpack
.
loads
(
data
raw
=
False
)
        
except
ValueError
:
            
return
None
        
return
self
.
prepare_response
(
request
cached
body_file
)
