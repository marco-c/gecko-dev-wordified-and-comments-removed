from
typing
import
Dict
Generator
from
pip
.
_vendor
.
requests
.
models
import
CONTENT_CHUNK_SIZE
Response
from
pip
.
_internal
.
exceptions
import
NetworkConnectionError
HEADERS
:
Dict
[
str
str
]
=
{
"
Accept
-
Encoding
"
:
"
identity
"
}
def
raise_for_status
(
resp
:
Response
)
-
>
None
:
    
http_error_msg
=
"
"
    
if
isinstance
(
resp
.
reason
bytes
)
:
        
try
:
            
reason
=
resp
.
reason
.
decode
(
"
utf
-
8
"
)
        
except
UnicodeDecodeError
:
            
reason
=
resp
.
reason
.
decode
(
"
iso
-
8859
-
1
"
)
    
else
:
        
reason
=
resp
.
reason
    
if
400
<
=
resp
.
status_code
<
500
:
        
http_error_msg
=
(
            
f
"
{
resp
.
status_code
}
Client
Error
:
{
reason
}
for
url
:
{
resp
.
url
}
"
        
)
    
elif
500
<
=
resp
.
status_code
<
600
:
        
http_error_msg
=
(
            
f
"
{
resp
.
status_code
}
Server
Error
:
{
reason
}
for
url
:
{
resp
.
url
}
"
        
)
    
if
http_error_msg
:
        
raise
NetworkConnectionError
(
http_error_msg
response
=
resp
)
def
response_chunks
(
    
response
:
Response
chunk_size
:
int
=
CONTENT_CHUNK_SIZE
)
-
>
Generator
[
bytes
None
None
]
:
    
"
"
"
Given
a
requests
Response
provide
the
data
chunks
.
"
"
"
    
try
:
        
for
chunk
in
response
.
raw
.
stream
(
            
chunk_size
            
decode_content
=
False
        
)
:
            
yield
chunk
    
except
AttributeError
:
        
while
True
:
            
chunk
=
response
.
raw
.
read
(
chunk_size
)
            
if
not
chunk
:
                
break
            
yield
chunk
